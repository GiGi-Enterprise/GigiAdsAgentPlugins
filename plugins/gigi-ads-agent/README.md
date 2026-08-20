# Gigi-Ads-Agent for Codex

This public-safe package connects Codex to Gigi's hosted MCP service. It
contains only the plugin manifest, endpoint, and user-visible agent guidance.
Business logic, credentials, and customer data stay in private services.

The MCP server uses OAuth discovery. Do not add static credentials or request
headers to this package. On first use, Codex opens the Gigi sign-in flow and
stores the resulting user credential through its normal OAuth handling.

The checked-in `https://agent.gigico.tv/mcp` URL is the planned production
endpoint. It is not expected to work until deployment, DNS, and OAuth
registration are complete. Repository-level authentication and publication
notes are intentionally kept outside this installable package.

[Privacy](https://gigico.ai/privacy) · [Terms](https://gigico.ai/terms)
