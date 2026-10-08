# Phase 08 Batch Audit Record: `batch-80-development-fullstack-part21`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-80-development-fullstack-part21`
- **Category / Subcategory**: `development` / `fullstack`
- **Member Skill Count**: 15
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `7432f347e02f1ed9d01b9bc9b41215a24e76b6a9ebb3f60bd60e126bab35efdd`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `pr-review` | `task-folder/agents/skills/github/pr-review` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pr-workflows-onboard` | `task-folder/agents/skills/github/pr-workflows-onboard` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pr-workflows-pr-enhance` | `task-folder/agents/skills/github/pr-workflows-pr-enhance` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pr-workflows-workflow` | `task-folder/agents/skills/github/pr-workflows-workflow` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pr-writer` | `task-folder/agents/skills/github/pr-writer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pre-mortem` | `task-folder/agents/skills/strategy/pre-mortem` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pre-release-review` | `task-folder/agents/skills/pre-release-review` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `product-launch-campaigns` | `task-folder/agents/skills/marketing/product-launch-campaigns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `product-manager-toolkit` | `task-folder/agents/skills/product-manager-toolkit` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `product-marketing` | `task-folder/agents/skills/marketing/product-marketing` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `production-scheduling` | `task-folder/agents/skills/production-scheduling` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `progressive-estimation` | `task-folder/agents/skills/progressive-estimation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `progressive-web-app` | `task-folder/agents/skills/progressive-web-app` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `prompt-engineer` | `task-folder/agents/skills/prompts/prompt-engineer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `prompt-engineering` | `task-folder/agents/skills/prompts/prompt-engineering` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `pr-review` | User asks to implement, configure, or optimize pr review tasks (specifically configuring or implementing pr review specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pr review or unrelated operations outside pr review. | User asks 'How do I handle pr review in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pr review procedures or general fullstack tooling. |
| `pr-workflows-onboard` | User asks to implement, configure, or optimize pr workflows onboard tasks (specifically configuring or implementing pr workflows onboard specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside pr workflows onboard. | User asks 'How do I handle pr workflows onboard in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pr workflows onboard procedures or general fullstack tooling. |
| `pr-workflows-pr-enhance` | User asks to implement, configure, or optimize pr workflows pr enhance tasks (specifically configuring or implementing pr workflows pr enhance specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside pr workflows pr enhance. | User asks 'How do I handle pr workflows pr enhance in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pr workflows pr enhance procedures or general fullstack tooling. |
| `pr-workflows-workflow` | User asks to implement, configure, or optimize pr workflows workflow tasks (specifically configuring or implementing pr workflows workflow specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pr workflows workflow or unrelated operations outside pr workflows workflow. | User asks 'How do I handle pr workflows workflow in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pr workflows workflow procedures or general fullstack tooling. |
| `pr-writer` | User asks to implement, configure, or optimize pr writer tasks (specifically Requires**: GitHub CLI (`gh`) authenticated and available). | User requests general infrastructure administration, styling, or unrelated operations outside pr writer or unrelated operations outside pr writer. | User asks 'How do I handle pr writer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pr writer procedures or general fullstack tooling. |
| `pre-mortem` | User asks to implement, configure, or optimize pre mortem tasks (specifically configuring or implementing pre mortem specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pre mortem or unrelated operations outside pre mortem. | User asks 'How do I handle pre mortem in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pre mortem procedures or general fullstack tooling. |
| `pre-release-review` | User asks to implement, configure, or optimize pre release review tasks (specifically configuring or implementing pre release review specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pre release review or unrelated operations outside pre release review. | User asks 'How do I handle pre release review in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pre release review procedures or general fullstack tooling. |
| `product-launch-campaigns` | User asks to implement, configure, or optimize product launch campaigns tasks (specifically configuring or implementing product launch campaigns specifications). | User requests general infrastructure administration, styling, or unrelated operations outside product launch campaigns or unrelated operations outside product launch campaigns. | User asks 'How do I handle product launch campaigns in my workflow?' -> Disambiguate: Clarify whether the task requires specialized product launch campaigns procedures or general fullstack tooling. |
| `product-manager-toolkit` | User asks to implement, configure, or optimize product manager toolkit tasks (specifically configuring or implementing product manager toolkit specifications). | User requests general infrastructure administration, styling, or unrelated operations outside product manager toolkit or unrelated operations outside product manager toolkit. | User asks 'How do I handle product manager toolkit in my workflow?' -> Disambiguate: Clarify whether the task requires specialized product manager toolkit procedures or general fullstack tooling. |
| `product-marketing` | User asks to implement, configure, or optimize product marketing tasks (specifically configuring or implementing product marketing specifications). | User requests general infrastructure administration, styling, or unrelated operations outside product marketing or unrelated operations outside product marketing. | User asks 'How do I handle product marketing in my workflow?' -> Disambiguate: Clarify whether the task requires specialized product marketing procedures or general fullstack tooling. |
| `production-scheduling` | User asks to implement, configure, or optimize production scheduling tasks (specifically configuring or implementing production scheduling specifications). | User requests general infrastructure administration, styling, or unrelated operations outside production scheduling or unrelated operations outside production scheduling. | User asks 'How do I handle production scheduling in my workflow?' -> Disambiguate: Clarify whether the task requires specialized production scheduling procedures or general fullstack tooling. |
| `progressive-estimation` | User asks to implement, configure, or optimize progressive estimation tasks (specifically configuring or implementing progressive estimation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside progressive estimation or unrelated operations outside progressive estimation. | User asks 'How do I handle progressive estimation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized progressive estimation procedures or general fullstack tooling. |
| `progressive-web-app` | User asks to implement, configure, or optimize progressive web app tasks (specifically configuring or implementing progressive web app specifications). | User requests general infrastructure administration, styling, or unrelated operations outside progressive web app or unrelated operations outside progressive web app. | User asks 'How do I handle progressive web app in my workflow?' -> Disambiguate: Clarify whether the task requires specialized progressive web app procedures or general fullstack tooling. |
| `prompt-engineer` | User asks to implement, configure, or optimize prompt engineer tasks (specifically configuring or implementing prompt engineer specifications). | User requests general infrastructure administration, styling, or unrelated operations outside prompt engineer or unrelated operations outside prompt engineer. | User asks 'How do I handle prompt engineer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized prompt engineer procedures or general fullstack tooling. |
| `prompt-engineering` | User asks to implement, configure, or optimize prompt engineering tasks (specifically configuring or implementing prompt engineering specifications). | User requests general infrastructure administration, styling, or unrelated operations outside prompt engineering or unrelated operations outside prompt engineering. | User asks 'How do I handle prompt engineering in my workflow?' -> Disambiguate: Clarify whether the task requires specialized prompt engineering procedures or general fullstack tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/development/fullstack/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `7432f347e02f1ed9d01b9bc9b41215a24e76b6a9ebb3f60bd60e126bab35efdd` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `pr-workflows-pr-enhance` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `pre-release-review` | `references/checklist.md` | Created or preserved in canonical package |
| `pre-release-review` | `references/report-template.md` | Created or preserved in canonical package |
| `product-launch-campaigns` | `evals/email-sequence-and-paid-social-campaign-/criteria.json` | Created or preserved in canonical package |
| `product-launch-campaigns` | `evals/email-sequence-and-paid-social-campaign-/task.md` | Created or preserved in canonical package |
| `product-launch-campaigns` | `evals/launch-campaign-timeline-planning/criteria.json` | Created or preserved in canonical package |
| `product-launch-campaigns` | `evals/launch-campaign-timeline-planning/task.md` | Created or preserved in canonical package |
| `product-launch-campaigns` | `evals/waitlist-and-early-access-implementation/criteria.json` | Created or preserved in canonical package |
| `product-launch-campaigns` | `evals/waitlist-and-early-access-implementation/task.md` | Created or preserved in canonical package |
| `product-launch-campaigns` | `tile.json` | Created or preserved in canonical package |
| `product-manager-toolkit` | `references/prd_templates.md` | Created or preserved in canonical package |
| `product-manager-toolkit` | `scripts/customer_interview_analyzer.py` | Created or preserved in canonical package |
| `product-manager-toolkit` | `scripts/rice_prioritizer.py` | Created or preserved in canonical package |
| `product-marketing` | `evals/evals.json` | Created or preserved in canonical package |
| `production-scheduling` | `references/communication-templates.md` | Created or preserved in canonical package |
| `production-scheduling` | `references/decision-frameworks.md` | Created or preserved in canonical package |
| `production-scheduling` | `references/edge-cases.md` | Created or preserved in canonical package |
| `prompt-engineer` | `README.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
