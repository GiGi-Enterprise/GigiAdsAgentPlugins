---
name: gigi-ads-agent
description: Use Gigi tasks, feed cards, advertising metrics, advertiser context, knowledge, and campaign intake through Gigi tools.
---

# Gigi-Ads-Agent

Use Gigi MCP tools whenever the user asks about Gigi-managed advertisers,
tasks, feed updates, advertising metrics, configured agency or advertiser
context, knowledge, or campaign intake.

## Operating rules

- Treat the user, agency, and advertiser scope returned by Gigi as
  authoritative. Never invent or substitute advertiser IDs. If an advertiser
  is ambiguous, list or ask for the specific advertiser.
- Prefer a read or preview tool before a state-changing tool.
- A task preview is a dry run; say so explicitly.
- Marking a feed card read currently makes it non-executable. Only acknowledge
  that tool guard after the user clearly wants that consequence.
- Archive only after the user has identified the exact card and confirmed it.
- Use only published Gigi tools. Do not reconstruct hidden backend operations.
- Campaign intake collects and validates preferences. It does not create a DSP
  campaign. Never imply that it did.
- Before advertiser-specific analysis, planning, recommendations, or
  explanations, call `get_advertiser_context` with the user's current goal as
  `query`. This loads the current advertiser profile, effective agency and
  advertiser settings, and relevant authorized passages.
- If those passages are absent or insufficient, call `search_knowledge`. Use
  `get_knowledge_content` only when the full text of a specific authorized
  source is needed; do not assume documents are embedded in the plugin.
- Knowledge search results include source IDs and passages. Cite named sources
  and preserve advertiser and agency boundaries.
- Before querying an unfamiliar metric, use `list_metric_definitions` to get
  the exact metric name, supported time grains, and relevant dimensions.
- Metric trend tools return structured rows and may also return an interactive
  chart. Summarize the rows when the host cannot render the optional view.
- Do not imply that a tool mutates a DSP unless its published description
  explicitly says it does.

## Useful sequences

For feed review: narrow by advertiser or agency when known, list feed cards,
inspect the exact card, then perform only the requested archive, read, or
feedback action.

For a task: list or get the task, explain its schedule and current state, then
use preview only for explicit advertiser IDs.

For campaign intake: start the draft, collect missing fields conversationally
or through the form, save with the returned revision, and validate for
planning. Reload the draft before applying edits after a revision conflict.
