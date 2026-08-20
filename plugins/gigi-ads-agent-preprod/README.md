# Gigi-Ads-Agent (Pre-Prod) for Codex

This GitHub-only package connects Codex to Gigi's non-production pre-prod
environment. It is for release-candidate testing and will not be submitted to
the OpenAI Plugins Directory.

The endpoint remains intentionally non-routable until the pre-prod AWS API
Gateway is provisioned. After provisioning, the repository's environment
configuration will be updated with the assigned HTTPS endpoint.

OAuth discovery is provided by the pre-prod service. Never put credentials or
static authorization headers in this package.

[Privacy](https://gigico.ai/privacy) · [Terms](https://gigico.ai/terms)
