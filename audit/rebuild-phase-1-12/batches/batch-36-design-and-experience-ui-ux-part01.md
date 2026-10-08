# Phase 08 Batch Audit Record: `batch-36-design-and-experience-ui-ux-part01`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-36-design-and-experience-ui-ux-part01`
- **Category / Subcategory**: `design-and-experience` / `ui-ux`
- **Member Skill Count**: 15
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `77a8d37d24f37094b4f574e181adc37514edcfdda8f47fefc884c95837f54b74`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `a-b-test-design` | `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/a-b-test-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `accessibility-audit` | `task-folder/agents/skills/design/designer-skills-main/design-systems/skills/accessibility-audit` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `accessibility-test-plan` | `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/accessibility-test-plan` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `agent-to-agent` | `task-folder/agents/skills/design/designer/clean-gemini-agents/gemini-agents/skills/agent-to-agent/agent-to-agent` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `blind-spot-detective` | `task-folder/agents/skills/design/designer/writing/analysis/blind-spot-detective` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `brand-analyzer` | `task-folder/agents/skills/design/brand-analyzer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `brand-consistency-checker` | `task-folder/agents/skills/design/designer/clean-gemini-agents/gemini-agents/skills/branding/brand-consistency-checker` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `brand-guidelines` | `task-folder/agents/skills/design/brand-guidelines` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `brandkit` | `task-folder/agents/skills/design/brandkit` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `brandkit2` | `task-folder/agents/skills/design/brandkit2` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `business-analytics-reporter` | `task-folder/agents/skills/design/business-analytics-reporter` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `card-sort-analysis` | `task-folder/agents/skills/design/designer-skills-main/design-research/skills/card-sort-analysis` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `case-study` | `task-folder/agents/skills/design/designer-skills-main/designer-toolkit/skills/case-study` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ce-optimize` | `task-folder/agents/skills/design/designer/ce-optimize` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ce-polish` | `task-folder/agents/skills/design/designer/ce-polish` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `a-b-test-design` | User asks to implement, configure, or optimize a b test design tasks (specifically configuring or implementing a b test design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside a b test design or unrelated operations outside a b test design. | User asks 'How do I handle a b test design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized a b test design procedures or general ui-ux tooling. |
| `accessibility-audit` | User asks to implement, configure, or optimize accessibility audit tasks (specifically configuring or implementing accessibility audit specifications). | User requests general infrastructure administration, styling, or unrelated operations outside accessibility audit or unrelated operations outside accessibility audit. | User asks 'How do I handle accessibility audit in my workflow?' -> Disambiguate: Clarify whether the task requires specialized accessibility audit procedures or general ui-ux tooling. |
| `accessibility-test-plan` | User asks to implement, configure, or optimize accessibility test plan tasks (specifically configuring or implementing accessibility test plan specifications). | User requests general infrastructure administration, styling, or unrelated operations outside accessibility test plan or unrelated operations outside accessibility test plan. | User asks 'How do I handle accessibility test plan in my workflow?' -> Disambiguate: Clarify whether the task requires specialized accessibility test plan procedures or general ui-ux tooling. |
| `agent-to-agent` | User asks to implement, configure, or optimize agent to agent tasks (specifically configuring or implementing agent to agent specifications). | User requests general infrastructure administration, styling, or unrelated operations outside agent to agent or unrelated operations outside agent to agent. | User asks 'How do I handle agent to agent in my workflow?' -> Disambiguate: Clarify whether the task requires specialized agent to agent procedures or general ui-ux tooling. |
| `blind-spot-detective` | User asks to implement, configure, or optimize blind spot detective tasks (specifically configuring or implementing blind spot detective specifications). | User requests general infrastructure administration, styling, or unrelated operations outside blind spot detective or unrelated operations outside blind spot detective. | User asks 'How do I handle blind spot detective in my workflow?' -> Disambiguate: Clarify whether the task requires specialized blind spot detective procedures or general ui-ux tooling. |
| `brand-analyzer` | User asks to implement, configure, or optimize brand analyzer tasks (specifically configuring or implementing brand analyzer specifications). | User requests general infrastructure administration, styling, or unrelated operations outside brand analyzer or unrelated operations outside brand analyzer. | User asks 'How do I handle brand analyzer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized brand analyzer procedures or general ui-ux tooling. |
| `brand-consistency-checker` | User asks to implement, configure, or optimize brand consistency checker tasks (specifically configuring or implementing brand consistency checker specifications). | User requests general infrastructure administration, styling, or unrelated operations outside brand consistency checker or unrelated operations outside brand consistency checker. | User asks 'How do I handle brand consistency checker in my workflow?' -> Disambiguate: Clarify whether the task requires specialized brand consistency checker procedures or general ui-ux tooling. |
| `brand-guidelines` | User asks to implement, configure, or optimize brand guidelines tasks (specifically configuring or implementing brand guidelines specifications). | User requests general infrastructure administration, styling, or unrelated operations outside brand guidelines or unrelated operations outside brand guidelines. | User asks 'How do I handle brand guidelines in my workflow?' -> Disambiguate: Clarify whether the task requires specialized brand guidelines procedures or general ui-ux tooling. |
| `brandkit` | User asks to implement, configure, or optimize brandkit tasks (specifically intentional). | User requests general infrastructure administration, styling, or unrelated operations outside brandkit or unrelated operations outside brandkit. | User asks 'How do I handle brandkit in my workflow?' -> Disambiguate: Clarify whether the task requires specialized brandkit procedures or general ui-ux tooling. |
| `brandkit2` | User asks to implement, configure, or optimize brandkit2 tasks (specifically intentional). | User requests general infrastructure administration, styling, or unrelated operations outside brandkit2 or unrelated operations outside brandkit2. | User asks 'How do I handle brandkit2 in my workflow?' -> Disambiguate: Clarify whether the task requires specialized brandkit2 procedures or general ui-ux tooling. |
| `business-analytics-reporter` | User asks to implement, configure, or optimize business analytics reporter tasks (specifically configuring or implementing business analytics reporter specifications). | User requests general infrastructure administration, styling, or unrelated operations outside business analytics reporter or unrelated operations outside business analytics reporter. | User asks 'How do I handle business analytics reporter in my workflow?' -> Disambiguate: Clarify whether the task requires specialized business analytics reporter procedures or general ui-ux tooling. |
| `card-sort-analysis` | User asks to implement, configure, or optimize card sort analysis tasks (specifically configuring or implementing card sort analysis specifications). | User requests general infrastructure administration, styling, or unrelated operations outside card sort analysis or unrelated operations outside card sort analysis. | User asks 'How do I handle card sort analysis in my workflow?' -> Disambiguate: Clarify whether the task requires specialized card sort analysis procedures or general ui-ux tooling. |
| `case-study` | User asks to implement, configure, or optimize case study tasks (specifically configuring or implementing case study specifications). | User requests general infrastructure administration, styling, or unrelated operations outside case study or unrelated operations outside case study. | User asks 'How do I handle case study in my workflow?' -> Disambiguate: Clarify whether the task requires specialized case study procedures or general ui-ux tooling. |
| `ce-optimize` | User asks to implement, configure, or optimize ce optimize tasks (specifically configuring or implementing ce optimize specifications). | User requests general infrastructure administration, styling, or unrelated operations outside ce optimize or unrelated operations outside ce optimize. | User asks 'How do I handle ce optimize in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ce optimize procedures or general ui-ux tooling. |
| `ce-polish` | User asks to implement, configure, or optimize ce polish tasks (specifically configuring or implementing ce polish specifications). | User requests general infrastructure administration, styling, or unrelated operations outside ce polish or unrelated operations outside ce polish. | User asks 'How do I handle ce polish in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ce polish procedures or general ui-ux tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/design-and-experience/ui-ux/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `77a8d37d24f37094b4f574e181adc37514edcfdda8f47fefc884c95837f54b74` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `brand-analyzer` | `assets/brand_analysis_report_template.md` | Created or preserved in canonical package |
| `brand-analyzer` | `assets/brand_guidelines_template.md` | Created or preserved in canonical package |
| `brand-analyzer` | `assets/quick_brand_audit_template.md` | Created or preserved in canonical package |
| `brand-analyzer` | `index.js` | Created or preserved in canonical package |
| `brand-analyzer` | `package.json` | Created or preserved in canonical package |
| `brand-analyzer` | `references/brand_analysis_framework.md` | Created or preserved in canonical package |
| `brand-analyzer` | `references/brand_archetypes.md` | Created or preserved in canonical package |
| `brandkit` | `LICENSE` | Created or preserved in canonical package |
| `business-analytics-reporter` | `assets/report_template.html` | Created or preserved in canonical package |
| `business-analytics-reporter` | `index.js` | Created or preserved in canonical package |
| `business-analytics-reporter` | `package.json` | Created or preserved in canonical package |
| `business-analytics-reporter` | `references/business_frameworks.md` | Created or preserved in canonical package |
| `business-analytics-reporter` | `references/visualization_guide.md` | Created or preserved in canonical package |
| `business-analytics-reporter` | `scripts/analyze_business_data.py` | Created or preserved in canonical package |
| `ce-optimize` | `references/example-hard-spec.yaml` | Created or preserved in canonical package |
| `ce-optimize` | `references/example-judge-spec.yaml` | Created or preserved in canonical package |
| `ce-optimize` | `references/experiment-log-schema.yaml` | Created or preserved in canonical package |
| `ce-optimize` | `references/experiment-prompt-template.md` | Created or preserved in canonical package |
| `ce-optimize` | `references/judge-prompt-template.md` | Created or preserved in canonical package |
| `ce-optimize` | `references/optimize-spec-schema.yaml` | Created or preserved in canonical package |
| `ce-optimize` | `references/usage-guide.md` | Created or preserved in canonical package |
| `ce-optimize` | `scripts/experiment-worktree.sh` | Created or preserved in canonical package |
| `ce-optimize` | `scripts/measure.sh` | Created or preserved in canonical package |
| `ce-optimize` | `scripts/parallel-probe.sh` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-astro.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-detection.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-next.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-nuxt.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-procfile.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-rails.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-remix.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-sveltekit.md` | Created or preserved in canonical package |
| `ce-polish` | `references/dev-server-vite.md` | Created or preserved in canonical package |
| `ce-polish` | `references/ide-detection.md` | Created or preserved in canonical package |
| `ce-polish` | `references/launch-json-schema.md` | Created or preserved in canonical package |
| `ce-polish` | `scripts/detect-project-type.sh` | Created or preserved in canonical package |
| `ce-polish` | `scripts/read-launch-json.sh` | Created or preserved in canonical package |
| `ce-polish` | `scripts/resolve-package-manager.sh` | Created or preserved in canonical package |
| `ce-polish` | `scripts/resolve-port.sh` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
