# Installation

The repository is the distribution boundary for host-visible plugin code. It
does not contain private backend services, customer data, or credentials.

## ChatGPT

### Public directory

After OpenAI approves the submission and Gigi publishes it:

1. Open ChatGPT's Plugins Directory.
2. Find **Gigi-Ads-Agent** and choose **Install**.
3. Choose **Connect**. ChatGPT opens the Gigi sign-in flow in the browser.
4. Sign in and approve access, then return to ChatGPT.

ChatGPT users do not clone this repository or install its source. The reviewed
listing and MCP metadata are distributed through the OpenAI Plugins Directory.

### Private beta

Before public approval, an invited tester can add a developer-mode custom MCP
connection (sometimes called a custom connector) to the hosted endpoint:

1. In ChatGPT, open **Settings → Security and login** and enable Developer
   mode, if permitted by the user's workspace.
2. Open ChatGPT Plugins, select the plus button, and create a connection named
   **Gigi-Ads-Agent** using `https://agent.gigico.tv/mcp`.
3. Copy the exact OAuth redirect URI shown in ChatGPT's app or connection
   management and have it allowlisted by Gigi. Do not guess or alter this URI.
4. Review the discovered tools, choose **Connect**, and complete browser OAuth.

This beta route requires the hosted HTTPS endpoint and OAuth discovery to be
live. It does not publish the plugin or require access to this repository.

Custom full-MCP connections with write actions are currently available on
ChatGPT web for Business, Enterprise, and Edu workspaces, subject to workspace
policy. Pro developer mode currently supports read/fetch tools only, so it can
test Gigi read workflows but not write workflows.

## Codex

### Public directory

After OpenAI approval and publication, **Gigi-Ads-Agent** appears in the same
universal Plugins Directory used by ChatGPT and Codex. A Codex user selects the
plugin, installs it, and chooses **Connect** when first prompted; no repository
checkout is required.

### Local or private testing

The public GitHub repository is also the Alpha/staging and Beta/pre-prod distribution
surface. Add it as a repository marketplace, then run exactly one of the three
install commands for the intended environment:

```bash
codex plugin marketplace add GiGi-Enterprise/GigiAdsAgentPlugins

# Alpha (Staging)
codex plugin add gigi-ads-agent-alpha@gigi-ads-agent

# Beta (Pre-Prod)
codex plugin add gigi-ads-agent-beta@gigi-ads-agent

# Production
codex plugin add gigi-ads-agent@gigi-ads-agent
```

Install only the environment you intend to use, or keep the environment suffix
visible throughout testing. Start a new task after installing or updating so
Codex loads the plugin's tools and skill. The repo marketplace is not how a
public ChatGPT user installs the approved production plugin.

## Claude Code

Use a current Claude Code release. Older clients that do not recognize the
plugin manifest's `displayName` field cannot install the exact
**Gigi-Ads-Agent** package; update Claude Code before adding the marketplace.

### Public/community marketplace

After Anthropic approves the public submission, users add Anthropic's community
marketplace and install the reviewed plugin:

```bash
claude plugin marketplace add anthropics/claude-plugins-community
claude plugin install gigi-ads-agent@claude-community
```

Anthropic's review pins a public GitHub commit of the plugin package. This
plugin-only repository is therefore visible to users and reviewers; the hosted
service implementation remains in its private repository.

### Local or private testing

For local development, add the repository marketplace and run exactly one
environment-specific install command:

```bash
claude plugin marketplace add GiGi-Enterprise/GigiAdsAgentPlugins

# Alpha (Staging)
claude plugin install gigi-ads-agent-alpha@gigi-ads-agent

# Beta (Pre-Prod)
claude plugin install gigi-ads-agent-beta@gigi-ads-agent

# Production
claude plugin install gigi-ads-agent@gigi-ads-agent
```

After installation, start a new Claude Code session. Invoke a Gigi tool and use
`/mcp` to complete OAuth when prompted.

Only `gigi-ads-agent` is submitted to Anthropic's public marketplace. The
Alpha and Beta entries remain available only when a user explicitly adds
Gigi's GitHub repository marketplace. Do not use a pending non-production
package until its API Gateway endpoint and OAuth flow are operational.
