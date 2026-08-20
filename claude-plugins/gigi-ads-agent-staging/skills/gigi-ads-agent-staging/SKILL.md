---
name: gigi-ads-agent-staging
description: Test Gigi tasks, feed cards, metrics, advertiser context, knowledge, and campaign intake in the non-production staging environment.
---

# Gigi-Ads-Agent (Staging)

Use the staging Gigi MCP tools for pre-release verification. Always identify
results and actions as **staging**, never production.

## Operating rules

- Treat returned user, agency, and advertiser scope as authoritative.
- Prefer a read or preview before a state-changing tool.
- A task preview is a dry run; say so explicitly.
- Confirm the exact feed card before archive, read, or feedback actions.
- Campaign intake validates a draft; it does not create a DSP campaign.
- Before advertiser-specific analysis, planning, recommendations, or
  explanations, call `get_advertiser_context` with the user's current goal as
  `query`; search authorized knowledge if its passages are insufficient.
- Use `get_knowledge_content` only for a specific authorized source. Documents
  are retrieved from Gigi and are not embedded in this plugin.
- Cite named knowledge sources and preserve tenant boundaries.
- Discover metric definitions before querying an unfamiliar metric.
- Never imply that staging state or results reflect production.
