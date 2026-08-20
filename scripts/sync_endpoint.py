#!/usr/bin/env python3
"""Keep every host package aligned with its environment endpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "environments.json"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_manifest(plugin_id: str, endpoint: str) -> dict[str, object]:
    return {
        "mcpServers": {
            plugin_id: {
                "type": "http",
                "url": endpoint,
            }
        }
    }


def package_manifests(plugin_id: str) -> tuple[Path, Path]:
    return (
        ROOT / "plugins" / plugin_id / ".mcp.json",
        ROOT / "claude-plugins" / plugin_id / ".mcp.json",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift without changing files",
    )
    args = parser.parse_args()

    environments = load_json(CONFIG)
    expected_by_path: dict[Path, dict[str, object]] = {}
    for environment, raw in environments.items():
        if not isinstance(raw, dict):
            raise SystemExit(f"{environment}: environment config must be an object")
        plugin_id = raw.get("pluginId")
        endpoint = raw.get("mcp")
        if not isinstance(plugin_id, str) or not plugin_id:
            raise SystemExit(f"{environment}: pluginId must be a string")
        if not isinstance(endpoint, str) or not endpoint.startswith("https://"):
            raise SystemExit(f"{environment}: mcp endpoint must be an https:// URL")
        expected = expected_manifest(plugin_id, endpoint)
        for path in package_manifests(plugin_id):
            expected_by_path[path] = expected

    drifted = [path for path, expected in expected_by_path.items() if load_json(path) != expected]
    if args.check:
        if drifted:
            for path in drifted:
                print(f"endpoint drift: {path.relative_to(ROOT)}")
            return 1
        print(f"endpoint sync: {len(expected_by_path)} manifests match 3 environments")
        return 0

    for path, expected in expected_by_path.items():
        path.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
    print(f"updated {len(expected_by_path)} manifests for 3 environments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
