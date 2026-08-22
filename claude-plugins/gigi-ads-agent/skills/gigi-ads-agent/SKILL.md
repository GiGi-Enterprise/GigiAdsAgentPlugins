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
- Metric trend tools return structured rows and may also return an interactive
  chart. Summarize the rows when the host cannot render the optional view.
- Do not imply that a tool mutates a DSP unless its published description
  explicitly says it does.

## Working with agency users

- Treat requests as media-management goals, not API specifications. Translate
  phrases such as "show spend by campaign," "where does frequency stop
  helping," or "compare new-to-brand performance" into metric discovery and
  querying without asking the user to name a dataset, metric code, API
  generation, or tool.
- Never ask whether the user wants legacy or V2. Keep dataset names, metric
  codes, and tool names internal unless they help explain a limitation or the
  user asks for technical detail.
- Load advertiser context before advertiser-specific analysis so configured
  KPIs, attribution preferences, funnel definitions, and agency terminology
  guide the query.
- Ask a business-level clarification only when it would materially change the
  answer, such as promoted-product versus total-brand sales, assisted versus
  first-touch attribution, campaign versus advertiser scope, or whether weekly
  data is acceptable when daily data is unavailable.
- Report the advertiser or campaign scope, date range, time grain, and any
  material attribution or sales-definition assumption. Present conclusions in
  media-manager language.

## Metric questions

- For standard Amazon DSP delivery or performance questions, such as spend,
  impressions, clicks, CPM, CTR, pacing, or campaign, line-item, and creative
  trends, use `list_legacy_metric_definitions` to resolve the exact metric and
  then use `display_metric_trend`.
- For dataset-specific advanced measurement, such as path-to-conversion,
  audience or funnel overlap, assisted attribution, frequency versus
  conversion, NTB, CAC/LTV, ASIN cross-sell, or search-term analysis, use
  `list_metric_definitions` progressively: discover `DATASETS` from the user's
  business concept, inspect `METRIC_NAMES_PER_DATASET`, inspect
  `DIMENSIONS_PER_DATASET`, and inspect the selected metric through `METRICS`.
  Follow the returned `recommendedQueryTool`.
- Do not route solely on the word AMC because standard legacy groups can
  contain AMC-derived fields.
- Do not stop after an irrelevant first page. Refine the business concept and
  paginate discovery before concluding that a metric or dataset is
  unavailable.
- When the user asks for a trend, include a date grouping and choose a
  supported daily, weekly, or monthly grain. If the requested grain is
  unsupported, explain that clearly and offer the closest supported grain
  instead of silently changing it.

## Useful sequences

For feed review: narrow by advertiser or agency when known, list feed cards,
inspect the exact card, then perform only the requested archive, read, or
feedback action.

For a task: list or get the task, explain its schedule and current state, then
use preview only for explicit advertiser IDs.

For campaign intake: start the draft, collect missing fields conversationally
or through the form, save with the returned revision, and validate for
planning. Reload the draft before applying edits after a revision conflict.
