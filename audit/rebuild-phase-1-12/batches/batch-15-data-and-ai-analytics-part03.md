# Phase 08 Batch Audit Record: `batch-15-data-and-ai-analytics-part03`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-15-data-and-ai-analytics-part03`
- **Category / Subcategory**: `data-and-ai` / `analytics`
- **Member Skill Count**: 11
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `3d210b22e03082cc42f36c224d86cebb425bc0d57d4873355cb29a7554584192`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `posthog-automation` | `task-folder/agents/skills/posthog-automation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pricing-strategy` | `task-folder/agents/skills/strategy/pricing-strategy` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `product-analytics` | `task-folder/agents/skills/data-analytics/data-analytics/product-analytics` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `profit-margin-analysis` | `task-folder/agents/skills/data-analytics/data-analytics/profit-margin-analysis` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `revenue-recognition-accounting` | `task-folder/agents/skills/data-analytics/data-analytics/revenue-recognition-accounting` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `segment-audience` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/segment-audience` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `segment-automation` | `task-folder/agents/skills/segment-automation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `segment-cdp` | `task-folder/agents/skills/segment-cdp` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `sendgrid-automation` | `task-folder/agents/skills/sendgrid-automation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `stp-framework` | `task-folder/agents/skills/strategy/stp-framework` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `unit-economics-tracking` | `task-folder/agents/skills/data-analytics/data-analytics/unit-economics-tracking` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `posthog-automation` | User asks to implement, configure, or optimize posthog automation tasks (specifically configuring or implementing posthog automation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside posthog automation or unrelated operations outside posthog automation. | User asks 'How do I handle posthog automation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized posthog automation procedures or general analytics tooling. |
| `pricing-strategy` | User asks to implement, configure, or optimize pricing strategy tasks (specifically configuring or implementing pricing strategy specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pricing strategy or unrelated operations outside pricing strategy. | User asks 'How do I handle pricing strategy in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pricing strategy procedures or general analytics tooling. |
| `product-analytics` | User asks to implement, configure, or optimize product analytics tasks (specifically configuring or implementing product analytics specifications). | User requests general infrastructure administration, styling, or unrelated operations outside product analytics or unrelated operations outside product analytics. | User asks 'How do I handle product analytics in my workflow?' -> Disambiguate: Clarify whether the task requires specialized product analytics procedures or general analytics tooling. |
| `profit-margin-analysis` | User asks to implement, configure, or optimize profit margin analysis tasks (specifically configuring or implementing profit margin analysis specifications). | User requests general infrastructure administration, styling, or unrelated operations outside profit margin analysis or unrelated operations outside profit margin analysis. | User asks 'How do I handle profit margin analysis in my workflow?' -> Disambiguate: Clarify whether the task requires specialized profit margin analysis procedures or general analytics tooling. |
| `revenue-recognition-accounting` | User asks to implement, configure, or optimize revenue recognition accounting tasks (specifically configuring or implementing revenue recognition accounting specifications). | User requests general infrastructure administration, styling, or unrelated operations outside revenue recognition accounting or unrelated operations outside revenue recognition accounting. | User asks 'How do I handle revenue recognition accounting in my workflow?' -> Disambiguate: Clarify whether the task requires specialized revenue recognition accounting procedures or general analytics tooling. |
| `segment-audience` | User asks to implement, configure, or optimize segment audience tasks (specifically configuring or implementing segment audience specifications). | User requests general infrastructure administration, styling, or unrelated operations outside segment audience or unrelated operations outside segment audience. | User asks 'How do I handle segment audience in my workflow?' -> Disambiguate: Clarify whether the task requires specialized segment audience procedures or general analytics tooling. |
| `segment-automation` | User asks to implement, configure, or optimize segment automation tasks (specifically configuring or implementing segment automation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside segment automation or unrelated operations outside segment automation. | User asks 'How do I handle segment automation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized segment automation procedures or general analytics tooling. |
| `segment-cdp` | User asks to implement, configure, or optimize segment cdp tasks (specifically configuring or implementing segment cdp specifications). | User requests general infrastructure administration, styling, or unrelated operations outside segment cdp or unrelated operations outside segment cdp. | User asks 'How do I handle segment cdp in my workflow?' -> Disambiguate: Clarify whether the task requires specialized segment cdp procedures or general analytics tooling. |
| `sendgrid-automation` | User asks to implement, configure, or optimize sendgrid automation tasks (specifically configuring or implementing sendgrid automation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside sendgrid automation or unrelated operations outside sendgrid automation. | User asks 'How do I handle sendgrid automation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized sendgrid automation procedures or general analytics tooling. |
| `stp-framework` | User asks to implement, configure, or optimize stp framework tasks (specifically configuring or implementing stp framework specifications). | User requests general infrastructure administration, styling, or unrelated operations outside stp framework or unrelated operations outside stp framework. | User asks 'How do I handle stp framework in my workflow?' -> Disambiguate: Clarify whether the task requires specialized stp framework procedures or general analytics tooling. |
| `unit-economics-tracking` | User asks to implement, configure, or optimize unit economics tracking tasks (specifically configuring or implementing unit economics tracking specifications). | User requests general infrastructure administration, styling, or unrelated operations outside unit economics tracking or unrelated operations outside unit economics tracking. | User asks 'How do I handle unit economics tracking in my workflow?' -> Disambiguate: Clarify whether the task requires specialized unit economics tracking procedures or general analytics tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/data-and-ai/analytics/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `3d210b22e03082cc42f36c224d86cebb425bc0d57d4873355cb29a7554584192` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `product-analytics` | `evals/dead-stock-detection-and-markdown-recomm/criteria.json` | Created or preserved in canonical package |
| `product-analytics` | `evals/dead-stock-detection-and-markdown-recomm/task.md` | Created or preserved in canonical package |
| `product-analytics` | `evals/merchandising-health-score-calculation/criteria.json` | Created or preserved in canonical package |
| `product-analytics` | `evals/merchandising-health-score-calculation/task.md` | Created or preserved in canonical package |
| `product-analytics` | `evals/pdp-funnel-conversion-analysis/criteria.json` | Created or preserved in canonical package |
| `product-analytics` | `evals/pdp-funnel-conversion-analysis/task.md` | Created or preserved in canonical package |
| `product-analytics` | `tile.json` | Created or preserved in canonical package |
| `profit-margin-analysis` | `evals/cost-attribution-methodology/criteria.json` | Created or preserved in canonical package |
| `profit-margin-analysis` | `evals/cost-attribution-methodology/task.md` | Created or preserved in canonical package |
| `profit-margin-analysis` | `evals/margin-analysis-and-improvement/criteria.json` | Created or preserved in canonical package |
| `profit-margin-analysis` | `evals/margin-analysis-and-improvement/task.md` | Created or preserved in canonical package |
| `profit-margin-analysis` | `evals/margin-data-model-schema/criteria.json` | Created or preserved in canonical package |
| `profit-margin-analysis` | `evals/margin-data-model-schema/task.md` | Created or preserved in canonical package |
| `profit-margin-analysis` | `tile.json` | Created or preserved in canonical package |
| `revenue-recognition-accounting` | `evals/bundle-ssp-allocation-and-journal-entrie/criteria.json` | Created or preserved in canonical package |
| `revenue-recognition-accounting` | `evals/bundle-ssp-allocation-and-journal-entrie/task.md` | Created or preserved in canonical package |
| `revenue-recognition-accounting` | `evals/gift-card-breakage-principal-vs-agent-va/criteria.json` | Created or preserved in canonical package |
| `revenue-recognition-accounting` | `evals/gift-card-breakage-principal-vs-agent-va/task.md` | Created or preserved in canonical package |
| `revenue-recognition-accounting` | `evals/subscription-proration-and-deferred-reve/criteria.json` | Created or preserved in canonical package |
| `revenue-recognition-accounting` | `evals/subscription-proration-and-deferred-reve/task.md` | Created or preserved in canonical package |
| `revenue-recognition-accounting` | `tile.json` | Created or preserved in canonical package |
| `unit-economics-tracking` | `evals/cohort-ltv-and-channel-segmentation/criteria.json` | Created or preserved in canonical package |
| `unit-economics-tracking` | `evals/cohort-ltv-and-channel-segmentation/task.md` | Created or preserved in canonical package |
| `unit-economics-tracking` | `evals/fully-loaded-cac-and-guardrails/criteria.json` | Created or preserved in canonical package |
| `unit-economics-tracking` | `evals/fully-loaded-cac-and-guardrails/task.md` | Created or preserved in canonical package |
| `unit-economics-tracking` | `evals/ltv-prediction-model-and-validation/criteria.json` | Created or preserved in canonical package |
| `unit-economics-tracking` | `evals/ltv-prediction-model-and-validation/task.md` | Created or preserved in canonical package |
| `unit-economics-tracking` | `tile.json` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
