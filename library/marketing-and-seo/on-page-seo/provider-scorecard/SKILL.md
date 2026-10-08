---
name: "provider-scorecard"
description: "Use to track enrichment provider success, cost, latency, and quality. Use when working with provider scorecard."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Provider Scorecard Skill

## When to Use
- Monthly/weekly ops reviews of enrichment vendors.
- Before renewing contracts or adjusting credit allocations.
- After outages or performance regressions to inform routing changes.

## Framework
1. **Metric Definition** – success rate, fill %, latency, credit burn, confidence.
2. **Data Sources** – provider logs, credit usage tables, QA samples, incident tickets.
3. **Scoring Model** – weight metrics by enrichment type and business priority.
4. **Visualization** – dashboard or memo highlighting leaders/laggards.
5. **Action Tracker** – document optimization experiments and owner assignments.

## Templates
- Scorecard table per provider.
- Executive summary slide with top takeaways.
- Jira/Asana template for provider improvement tasks.

## Tips
- Normalize metrics per enrichment type to avoid unfair comparisons.
- Capture qualitative notes (support responsiveness, roadmap access).
- Pair with `waterfall-blueprint` updates to reflect routing decisions.

---
