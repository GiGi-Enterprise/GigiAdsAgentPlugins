# Authentication

Gigi-Ads-Agent uses the OAuth flow published by Gigi's hosted MCP service. The
plugin packages do not contain API keys, access tokens, OAuth client secrets,
or private service addresses.

## User flow

1. Install **Gigi-Ads-Agent** from the host's approved distribution surface.
   In ChatGPT, this is the OpenAI Plugins Directory after public approval.
2. Choose **Connect**, or ask the host to use a Gigi tool.
3. The host discovers the OAuth metadata and opens the Gigi sign-in page in the
   browser.
4. Sign in with the same Google identity used for Gigi and approve access.
5. Gigi verifies the user's identity and advertising-account permissions.
6. The host stores and refreshes the resulting credential. The user does not
   copy or paste an access token.

The ChatGPT private-beta custom connection follows the same browser OAuth flow;
it changes only how the hosted MCP endpoint is added before directory approval.
Before connecting, Gigi must allowlist the exact OAuth redirect URI displayed
in ChatGPT's app or connection management. A guessed or normalized URI may not
match and should not be used.

Gigi's existing identity and authorization system remains authoritative. Each
MCP request remains subject to the same user, agency, advertiser, and role
boundaries as the Gigi product.

## Discovery contract

The hosted MCP endpoint must expose standard protected-resource and
authorization-server metadata, PKCE, refresh, and revocation behavior. The
exact routes live in the hosted service, not in this public repository. Host
clients should discover them from the MCP challenge instead of hard-coding
private routes.

## Environment endpoints

[`../config/environments.json`](../config/environments.json) is the canonical
environment map. Each environment has a distinct plugin ID, display name, OAuth
issuer, token database, and MCP endpoint. Run `python3 scripts/sync_endpoint.py
--check` to detect drift, or update the config and run
`python3 scripts/sync_endpoint.py` to regenerate all six host manifests.

Alpha targets staging and Beta targets pre-prod. They use their assigned AWS
API Gateway origins and are distributed only through GitHub. Production uses
`https://agent.gigico.tv/mcp` and is the only environment submitted to OpenAI or
Claude. Pending non-production hosts use the reserved `.invalid` domain so they
cannot accidentally connect to production.

Run `python3 scripts/validate.py --release --environment <name>` before tagging
an environment package. The release check rejects pending endpoints and verifies
that the selected endpoint is reachable over HTTPS.

[Privacy](https://gigico.ai/privacy) · [Terms](https://gigico.ai/terms)
