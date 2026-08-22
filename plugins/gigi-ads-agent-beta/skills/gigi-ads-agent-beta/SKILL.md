---
name: gigi-ads-agent-beta
description: Verify Gigi tasks, feed cards, metrics, advertiser context, knowledge, and campaign intake in the non-production Beta pre-prod environment.
---

# Gigi-Ads-Agent (Beta)

Use the Beta Gigi MCP tools for pre-prod release-candidate verification. Always
identify results and actions as **Beta (pre-prod)**, never production.

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
- Metric tools return structured rows and may also return an interactive chart.
  Summarize the rows when the host cannot render the optional view.
- Never imply that pre-prod state or results reflect production.

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
