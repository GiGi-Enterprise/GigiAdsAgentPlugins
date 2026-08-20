# Gigi-Ads-Agent plugins

This repository contains the public, host-facing packages for
**Gigi-Ads-Agent**. Environment-specific hosted Gigi MCP services power Codex,
ChatGPT, and Claude Code; this repository contains no service business logic or
credentials.

| Environment | Package IDs | Distribution |
|---|---|---|
| Alpha (Staging) | `gigi-ads-agent-alpha` | Public GitHub repository only |
| Beta (Pre-Prod) | `gigi-ads-agent-beta` | Public GitHub repository only |
| Production | `gigi-ads-agent` | GitHub plus OpenAI and Claude marketplaces after approval |

The packages intentionally use separate roots so host-specific manifests do
not conflict. Both connect to the endpoint defined in
[`config/environments.json`](config/environments.json) and rely on standard
OAuth discovery. Users never copy or paste service tokens. Non-production
endpoints remain deliberately non-routable until their API Gateways exist, so a
Alpha or Beta package can never silently fall through to production.

Only the production package is submitted to OpenAI or Claude. After OpenAI
approval and publication, ChatGPT users install
**Gigi-Ads-Agent** directly from the Plugins Directory. For an invited private
beta, ChatGPT developer mode can connect to the hosted MCP endpoint without
publishing the plugin or sharing this repository.

See [`docs/installation.md`](docs/installation.md) for local marketplace setup
and [`docs/authentication.md`](docs/authentication.md) for the user sign-in
flow and publication gate.

[Privacy](https://gigico.ai/privacy) · [Terms](https://gigico.ai/terms)

## Validate

```bash
python3 scripts/sync_endpoint.py --check
python3 scripts/validate.py
```

Before tagging or submitting a listing, run the network-aware publication gate:

```bash
python3 scripts/validate.py --release --environment prod
```

It intentionally fails while the selected environment is pending or its
endpoint is not reachable over HTTPS.

During local development, also run the installed host validators:

```bash
claude plugin validate .
python3 /path/to/plugin-creator/scripts/validate_plugin.py \
  plugins/gigi-ads-agent
```
