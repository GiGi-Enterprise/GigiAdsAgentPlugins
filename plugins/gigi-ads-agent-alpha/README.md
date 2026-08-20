# Gigi-Ads-Agent (Alpha) for Codex

This GitHub-only package connects Codex to Gigi's Alpha environment, which is
backed by the non-production staging service. It is for engineering and invited
tester use and will not be submitted to the OpenAI Plugins Directory.

The endpoint remains intentionally non-routable until the staging AWS API
Gateway is approved and provisioned. After provisioning, the repository's
environment configuration will be updated with the assigned HTTPS endpoint.

OAuth discovery is provided by the staging service. Never put credentials or
static authorization headers in this package.

[Privacy](https://gigico.ai/privacy) · [Terms](https://gigico.ai/terms)
