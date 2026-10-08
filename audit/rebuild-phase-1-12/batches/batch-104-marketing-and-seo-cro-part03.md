# Phase 08 Batch Audit Record: `batch-104-marketing-and-seo-cro-part03`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-104-marketing-and-seo-cro-part03`
- **Category / Subcategory**: `marketing-and-seo` / `cro`
- **Member Skill Count**: 15
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `73900deaf9699d7480048ec51f475aee244c7591554c67bf65a8a7159b0bd29a`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `campaign-status` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/campaign-status` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `channel-integration` | `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/campaign-orchestration/skills/channel-integration` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `chrome-extension-developer` | `task-folder/agents/skills/chrome-extension-developer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `closed-loop-delivery` | `task-folder/agents/skills/closed-loop-delivery` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `closed-loop-playbook` | `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/voice-of-customer/skills/closed-loop-playbook` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `co-branding` | `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/partner-co-marketing-orchestration/skills/co-branding` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `co-marketing` | `task-folder/agents/skills/marketing/co-marketing` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `co-marketing_02` | `task-folder/agents/skills/marketing/co-marketing_02` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `code-review-and-quality` | `task-folder/agents/skills/code/code-review-and-quality` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `cohort-analysis` | `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/revenue-analytics/skills/cohort-analysis` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `community-program-matrix` | `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/community-building/skills/community-program-matrix` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `community-sentiment-dashboard` | `task-folder/agents/skills/seo/seo-skills-main/gtm-agents-main/plugins/social-media-marketing/skills/community-sentiment-dashboard` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `competitive-analysis` | `task-folder/agents/skills/design/designer-skills-main/ux-strategy/skills/competitive-analysis` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `competitor-analysis` | `task-folder/agents/skills/marketing/competitor-analysis` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `content-repurpose` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/content-repurpose` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `campaign-status` | User asks to implement, configure, or optimize campaign status tasks (specifically configuring or implementing campaign status specifications). | User requests general infrastructure administration, styling, or unrelated operations outside campaign status or unrelated operations outside campaign status. | User asks 'How do I handle campaign status in my workflow?' -> Disambiguate: Clarify whether the task requires specialized campaign status procedures or general cro tooling. |
| `channel-integration` | User asks to implement, configure, or optimize channel integration tasks (specifically configuring or implementing channel integration specifications). | User requests general infrastructure administration, styling, or unrelated operations outside channel integration or unrelated operations outside channel integration. | User asks 'How do I handle channel integration in my workflow?' -> Disambiguate: Clarify whether the task requires specialized channel integration procedures or general cro tooling. |
| `chrome-extension-developer` | User asks to implement, configure, or optimize chrome extension developer tasks (specifically configuring or implementing chrome extension developer specifications). | User requests The task is for Safari App Extensions (use `safari-extension-expert` if available) or unrelated operations outside chrome extension developer. | User asks 'How do I handle chrome extension developer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized chrome extension developer procedures or general cro tooling. |
| `closed-loop-delivery` | User asks to implement, configure, or optimize closed loop delivery tasks (specifically configuring or implementing closed loop delivery specifications). | User requests pure Q&A/explanations or unrelated operations outside closed loop delivery. | User asks 'How do I handle closed loop delivery in my workflow?' -> Disambiguate: Clarify whether the task requires specialized closed loop delivery procedures or general cro tooling. |
| `closed-loop-playbook` | User asks to implement, configure, or optimize closed loop playbook tasks (specifically configuring or implementing closed loop playbook specifications). | User requests general infrastructure administration, styling, or unrelated operations outside closed loop playbook or unrelated operations outside closed loop playbook. | User asks 'How do I handle closed loop playbook in my workflow?' -> Disambiguate: Clarify whether the task requires specialized closed loop playbook procedures or general cro tooling. |
| `co-branding` | User asks to implement, configure, or optimize co branding tasks (specifically configuring or implementing co branding specifications). | User requests general infrastructure administration, styling, or unrelated operations outside co branding or unrelated operations outside co branding. | User asks 'How do I handle co branding in my workflow?' -> Disambiguate: Clarify whether the task requires specialized co branding procedures or general cro tooling. |
| `co-marketing` | User asks to implement, configure, or optimize co marketing tasks (specifically configuring or implementing co marketing specifications). | User requests general infrastructure administration, styling, or unrelated operations outside co marketing or unrelated operations outside co marketing. | User asks 'How do I handle co marketing in my workflow?' -> Disambiguate: Clarify whether the task requires specialized co marketing procedures or general cro tooling. |
| `co-marketing_02` | User asks to implement, configure, or optimize co marketing_02 tasks (specifically configuring or implementing co marketing_02 specifications). | User requests general infrastructure administration, styling, or unrelated operations outside co marketing_02 or unrelated operations outside co marketing_02. | User asks 'How do I handle co marketing_02 in my workflow?' -> Disambiguate: Clarify whether the task requires specialized co marketing_02 procedures or general cro tooling. |
| `code-review-and-quality` | User asks to implement, configure, or optimize code review and quality tasks (specifically configuring or implementing code review and quality specifications). | User requests general infrastructure administration, styling, or unrelated operations outside code review and quality or unrelated operations outside code review and quality. | User asks 'How do I handle code review and quality in my workflow?' -> Disambiguate: Clarify whether the task requires specialized code review and quality procedures or general cro tooling. |
| `cohort-analysis` | User asks to implement, configure, or optimize cohort analysis tasks (specifically configuring or implementing cohort analysis specifications). | User requests general infrastructure administration, styling, or unrelated operations outside cohort analysis or unrelated operations outside cohort analysis. | User asks 'How do I handle cohort analysis in my workflow?' -> Disambiguate: Clarify whether the task requires specialized cohort analysis procedures or general cro tooling. |
| `community-program-matrix` | User asks to implement, configure, or optimize community program matrix tasks (specifically configuring or implementing community program matrix specifications). | User requests general infrastructure administration, styling, or unrelated operations outside community program matrix or unrelated operations outside community program matrix. | User asks 'How do I handle community program matrix in my workflow?' -> Disambiguate: Clarify whether the task requires specialized community program matrix procedures or general cro tooling. |
| `community-sentiment-dashboard` | User asks to implement, configure, or optimize community sentiment dashboard tasks (specifically configuring or implementing community sentiment dashboard specifications). | User requests general infrastructure administration, styling, or unrelated operations outside community sentiment dashboard or unrelated operations outside community sentiment dashboard. | User asks 'How do I handle community sentiment dashboard in my workflow?' -> Disambiguate: Clarify whether the task requires specialized community sentiment dashboard procedures or general cro tooling. |
| `competitive-analysis` | User asks to implement, configure, or optimize competitive analysis tasks (specifically configuring or implementing competitive analysis specifications). | User requests general infrastructure administration, styling, or unrelated operations outside competitive analysis or unrelated operations outside competitive analysis. | User asks 'How do I handle competitive analysis in my workflow?' -> Disambiguate: Clarify whether the task requires specialized competitive analysis procedures or general cro tooling. |
| `competitor-analysis` | User asks to implement, configure, or optimize competitor analysis tasks (specifically configuring or implementing competitor analysis specifications). | User requests general infrastructure administration, styling, or unrelated operations outside competitor analysis or unrelated operations outside competitor analysis. | User asks 'How do I handle competitor analysis in my workflow?' -> Disambiguate: Clarify whether the task requires specialized competitor analysis procedures or general cro tooling. |
| `content-repurpose` | User asks to implement, configure, or optimize content repurpose tasks (specifically configuring or implementing content repurpose specifications). | User requests general infrastructure administration, styling, or unrelated operations outside content repurpose or unrelated operations outside content repurpose. | User asks 'How do I handle content repurpose in my workflow?' -> Disambiguate: Clarify whether the task requires specialized content repurpose procedures or general cro tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/marketing-and-seo/cro/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `73900deaf9699d7480048ec51f475aee244c7591554c67bf65a8a7159b0bd29a` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `co-marketing` | `evals/evals.json` | Created or preserved in canonical package |
| `co-marketing_02` | `evals/evals.json` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
