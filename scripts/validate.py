#!/usr/bin/env python3
"""Validate environment isolation and the public plugin repository boundary."""

from __future__ import annotations

import argparse
import http.client
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS = ("staging", "preprod", "prod")
EXPECTED = {
    "staging": {
        "pluginId": "gigi-ads-agent-alpha",
        "displayName": "Gigi-Ads-Agent (Alpha)",
        "marketplaceSubmission": False,
    },
    "preprod": {
        "pluginId": "gigi-ads-agent-beta",
        "displayName": "Gigi-Ads-Agent (Beta)",
        "marketplaceSubmission": False,
    },
    "prod": {
        "pluginId": "gigi-ads-agent",
        "displayName": "Gigi-Ads-Agent",
        "marketplaceSubmission": True,
    },
}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
EXECUTE_API_HOST = re.compile(r"^[a-z0-9]+\.execute-api\.us-east-1\.amazonaws\.com$")


def load_json(relative: str) -> dict[str, object]:
    path = ROOT / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{relative}: JSON root must be an object")
    return value


def validate_release_endpoint(endpoint: str) -> None:
    parsed = urlparse(endpoint)
    if parsed.scheme != "https" or parsed.hostname is None:
        raise AssertionError("release endpoint must be an absolute HTTPS URL")

    connection = http.client.HTTPSConnection(parsed.hostname, parsed.port, timeout=5)
    try:
        connection.request("HEAD", parsed.path or "/")
        response = connection.getresponse()
        response.read()
    except (OSError, http.client.HTTPException) as exc:
        raise AssertionError(
            f"release endpoint is not reachable over HTTPS: {endpoint}: {exc}"
        ) from exc
    finally:
        connection.close()

    if response.status >= 500:
        raise AssertionError(f"release endpoint returned {response.status}: {endpoint}")


def validate_endpoint(environment: str, config: dict[str, object]) -> str:
    endpoint = config.get("mcp")
    status = config.get("endpointStatus")
    assert isinstance(endpoint, str), f"{environment}: mcp must be a string"
    assert status in {"pending", "planned", "live"}, (
        f"{environment}: invalid endpointStatus"
    )
    parsed = urlparse(endpoint)
    assert parsed.scheme == "https" and parsed.hostname, (
        f"{environment}: endpoint must use HTTPS"
    )
    assert parsed.port in {None, 443}, (
        f"{environment}: endpoint must use the default HTTPS port"
    )
    assert parsed.path == "/mcp" and not parsed.params and not parsed.query and not parsed.fragment, (
        f"{environment}: endpoint must be an origin plus /mcp"
    )

    if environment == "prod":
        assert parsed.hostname == "agent.gigico.tv", (
            "production endpoint must be agent.gigico.tv"
        )
        assert status in {"planned", "live"}, "production cannot use a pending sentinel"
    elif status == "pending":
        assert parsed.hostname.endswith(".invalid"), (
            f"{environment}: pending endpoint must use the reserved .invalid domain"
        )
    else:
        assert EXECUTE_API_HOST.fullmatch(parsed.hostname), (
            f"{environment}: configured endpoint must be an us-east-1 execute-api host"
        )
    return endpoint


def validate(*, release: bool = False, environment: str = "prod") -> None:
    configs = load_json("config/environments.json")
    assert tuple(configs) == ENVIRONMENTS, "environment order or membership changed"

    endpoints: dict[str, str] = {}
    for name in ENVIRONMENTS:
        raw = configs[name]
        assert isinstance(raw, dict), f"{name}: configuration must be an object"
        expected = EXPECTED[name]
        for key, value in expected.items():
            assert raw.get(key) == value, f"{name}: wrong {key}"
        distribution = raw.get("distribution")
        assert isinstance(distribution, list) and "github" in distribution
        if name == "prod":
            assert set(distribution) == {"github", "openai", "claude"}
        else:
            assert distribution == ["github"], (
                f"{name}: non-production plugins must remain GitHub-only"
            )
        endpoints[name] = validate_endpoint(name, raw)
        assert isinstance(raw["pluginId"], str)

    assert len(set(endpoints.values())) == len(ENVIRONMENTS), (
        "every environment must use a distinct MCP endpoint"
    )

    for name in ENVIRONMENTS:
        config = configs[name]
        assert isinstance(config, dict)
        plugin_id = str(config["pluginId"])
        display_name = str(config["displayName"])
        endpoint = endpoints[name]
        codex = load_json(f"plugins/{plugin_id}/.codex-plugin/plugin.json")
        claude = load_json(
            f"claude-plugins/{plugin_id}/.claude-plugin/plugin.json"
        )
        for label, manifest in (("Codex", codex), ("Claude", claude)):
            assert manifest["name"] == plugin_id, f"{name} {label}: wrong plugin name"
            version = manifest.get("version")
            assert isinstance(version, str) and SEMVER.fullmatch(version), (
                f"{name} {label}: version must be strict semver"
            )

        interface = codex["interface"]
        assert isinstance(interface, dict)
        assert interface["displayName"] == display_name
        assert claude["displayName"] == display_name

        expected_server = {plugin_id: {"type": "http", "url": endpoint}}
        for relative in (
            f"plugins/{plugin_id}/.mcp.json",
            f"claude-plugins/{plugin_id}/.mcp.json",
        ):
            assert load_json(relative)["mcpServers"] == expected_server

        codex_skill = (
            ROOT / "plugins" / plugin_id / "skills" / plugin_id / "SKILL.md"
        ).read_text(encoding="utf-8")
        claude_skill = (
            ROOT
            / "claude-plugins"
            / plugin_id
            / "skills"
            / plugin_id
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        assert codex_skill == claude_skill, f"{name}: host skill instructions drifted"
        assert f"name: {plugin_id}\n" in codex_skill

    marketplace_plugin_ids = [
        EXPECTED["prod"]["pluginId"],
        EXPECTED["staging"]["pluginId"],
        EXPECTED["preprod"]["pluginId"],
    ]

    codex_market = load_json(".agents/plugins/marketplace.json")
    codex_plugins = codex_market["plugins"]
    assert isinstance(codex_plugins, list)
    assert [entry["name"] for entry in codex_plugins] == marketplace_plugin_ids, (
        "Codex marketplace must list production first, followed by test environments"
    )
    for entry, plugin_id in zip(
        codex_plugins, marketplace_plugin_ids, strict=True
    ):
        assert entry["source"]["path"] == f"./plugins/{plugin_id}"
        assert entry["policy"] == {
            "installation": "AVAILABLE",
            "authentication": "ON_USE",
        }

    claude_market = load_json(".claude-plugin/marketplace.json")
    claude_plugins = claude_market["plugins"]
    assert isinstance(claude_plugins, list)
    assert [entry["name"] for entry in claude_plugins] == marketplace_plugin_ids, (
        "Claude marketplace must list production first, followed by test environments"
    )
    for entry, plugin_id in zip(
        claude_plugins, marketplace_plugin_ids, strict=True
    ):
        assert entry["source"] == f"./claude-plugins/{plugin_id}"

    installation = (ROOT / "docs" / "installation.md").read_text(encoding="utf-8")
    for required_text in (
        "## ChatGPT",
        "OpenAI Plugins Directory",
        "Choose **Connect**",
        "do not clone this repository",
        "exact OAuth redirect URI",
        "gigi-ads-agent-alpha",
        "gigi-ads-agent-beta",
        "https://agent.gigico.tv/mcp",
        "Only `gigi-ads-agent` is submitted",
    ):
        assert required_text in installation, (
            f"installation guidance is missing {required_text!r}"
        )

    forbidden = ("127.0.0.1", "localhost", "Authorization", "Bearer ")
    for package in (ROOT / "plugins", ROOT / "claude-plugins"):
        for path in package.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                for needle in forbidden:
                    assert needle not in text, (
                        f"{path.relative_to(ROOT)} exposes forbidden value {needle!r}"
                    )

    if release:
        selected = configs[environment]
        assert isinstance(selected, dict)
        assert selected["endpointStatus"] != "pending", (
            f"{environment}: endpoint is still pending AWS provisioning"
        )
        validate_release_endpoint(endpoints[environment])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        help="also require the selected MCP endpoint to be live over HTTPS",
    )
    parser.add_argument(
        "--environment",
        choices=ENVIRONMENTS,
        default="prod",
        help="environment checked by --release (default: prod)",
    )
    arguments = parser.parse_args()
    try:
        validate(release=arguments.release, environment=arguments.environment)
    except AssertionError as exc:
        raise SystemExit(f"validation failed: {exc}") from exc
    mode = f"release:{arguments.environment}" if arguments.release else "structural"
    print(f"validated ({mode}): 3 environments, 6 host packages, public-safe boundary")
