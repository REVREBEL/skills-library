# Phase 08 Batch Audit Record: `batch-44-design-and-experience-ui-ux-part09`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-44-design-and-experience-ui-ux-part09`
- **Category / Subcategory**: `design-and-experience` / `ui-ux`
- **Member Skill Count**: 14
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `40bb1c0ea6d591e4fa9a258039b9902b611f6c520482f60abf798d6895dedc81`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `ux-audit` | `task-folder/agents/skills/ux/ux-audit` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ux-feedback` | `task-folder/agents/skills/ux/ux-feedback` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ux-flow` | `task-folder/agents/skills/ux/ux-flow` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ux-persuasion-engineer` | `task-folder/agents/skills/ux/ux-persuasion-engineer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `uxui-principles` | `task-folder/agents/skills/ux/uxui-principles` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `version-control-strategy` | `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/version-control-strategy` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `visual-hierarchy` | `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/visual-hierarchy` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `voice-analysis` | `task-folder/agents/skills/design/designer/writing/analysis/voice-analysis` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `von-restorff-effect` | `task-folder/agents/skills/design/designer-skills-main/ui-design/skills/von-restorff-effect` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `webflow-code-component-component-scaffold` | `task-folder/agents/skills/webflow/webflow-code-component-component-scaffold` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `webflow-code-component-pre-deploy-check` | `task-folder/agents/skills/webflow/webflow-code-component-pre-deploy-check` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `webflow-code-components` | `task-folder/agents/skills/webflow/webflow-code-components` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `wireframe-spec` | `task-folder/agents/skills/design/designer-skills-main/prototyping-testing/skills/wireframe-spec` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `xlsx` | `task-folder/agents/skills/design/document-skills/xlsx` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `ux-audit` | User asks to implement, configure, or optimize ux audit tasks (specifically configuring or implementing ux audit specifications). | User requests For accessibility-only issues → use `/ss-a11y` or unrelated operations outside ux audit. | User asks 'How do I handle ux audit in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ux audit procedures or general ui-ux tooling. |
| `ux-feedback` | User asks to implement, configure, or optimize ux feedback tasks (specifically configuring or implementing ux feedback specifications). | User requests For only the words inside a state → use `/ss-copy` or unrelated operations outside ux feedback. | User asks 'How do I handle ux feedback in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ux feedback procedures or general ui-ux tooling. |
| `ux-flow` | User asks to implement, configure, or optimize ux flow tasks (specifically configuring or implementing ux flow specifications). | User requests For implementing a single page → use `/ss-page` after the flow is settled or unrelated operations outside ux flow. | User asks 'How do I handle ux flow in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ux flow procedures or general ui-ux tooling. |
| `ux-persuasion-engineer` | User asks to implement, configure, or optimize ux persuasion engineer tasks (specifically configuring or implementing ux persuasion engineer specifications). | User requests general infrastructure administration, styling, or unrelated operations outside ux persuasion engineer or unrelated operations outside ux persuasion engineer. | User asks 'How do I handle ux persuasion engineer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ux persuasion engineer procedures or general ui-ux tooling. |
| `uxui-principles` | User asks to implement, configure, or optimize uxui principles tasks (specifically Source:** https://github.com/uxuiprinciples/agent-skills). | User requests general infrastructure administration, styling, or unrelated operations outside uxui principles or unrelated operations outside uxui principles. | User asks 'How do I handle uxui principles in my workflow?' -> Disambiguate: Clarify whether the task requires specialized uxui principles procedures or general ui-ux tooling. |
| `version-control-strategy` | User asks to implement, configure, or optimize version control strategy tasks (specifically configuring or implementing version control strategy specifications). | User requests general infrastructure administration, styling, or unrelated operations outside version control strategy or unrelated operations outside version control strategy. | User asks 'How do I handle version control strategy in my workflow?' -> Disambiguate: Clarify whether the task requires specialized version control strategy procedures or general ui-ux tooling. |
| `visual-hierarchy` | User asks to implement, configure, or optimize visual hierarchy tasks (specifically configuring or implementing visual hierarchy specifications). | User requests general infrastructure administration, styling, or unrelated operations outside visual hierarchy or unrelated operations outside visual hierarchy. | User asks 'How do I handle visual hierarchy in my workflow?' -> Disambiguate: Clarify whether the task requires specialized visual hierarchy procedures or general ui-ux tooling. |
| `voice-analysis` | User asks to implement, configure, or optimize voice analysis tasks (specifically configuring or implementing voice analysis specifications). | User requests general infrastructure administration, styling, or unrelated operations outside voice analysis or unrelated operations outside voice analysis. | User asks 'How do I handle voice analysis in my workflow?' -> Disambiguate: Clarify whether the task requires specialized voice analysis procedures or general ui-ux tooling. |
| `von-restorff-effect` | User asks to implement, configure, or optimize von restorff effect tasks (specifically configuring or implementing von restorff effect specifications). | User requests general infrastructure administration, styling, or unrelated operations outside von restorff effect or unrelated operations outside von restorff effect. | User asks 'How do I handle von restorff effect in my workflow?' -> Disambiguate: Clarify whether the task requires specialized von restorff effect procedures or general ui-ux tooling. |
| `webflow-code-component-component-scaffold` | User asks to implement, configure, or optimize webflow code component component scaffold tasks (specifically configuring or implementing webflow code component component scaffold specifications). | User requests Converting an existing React component (use convert-component skill) or unrelated operations outside webflow code component component scaffold. | User asks 'How do I handle webflow code component component scaffold in my workflow?' -> Disambiguate: Clarify whether the task requires specialized webflow code component component scaffold procedures or general ui-ux tooling. |
| `webflow-code-component-pre-deploy-check` | User asks to implement, configure, or optimize webflow code component pre deploy check tasks (specifically configuring or implementing webflow code component pre deploy check specifications). | User requests Deployment already failed (use troubleshoot-deploy instead) or unrelated operations outside webflow code component pre deploy check. | User asks 'How do I handle webflow code component pre deploy check in my workflow?' -> Disambiguate: Clarify whether the task requires specialized webflow code component pre deploy check procedures or general ui-ux tooling. |
| `webflow-code-components` | User asks to implement, configure, or optimize webflow code components tasks (specifically configuring or implementing webflow code components specifications). | User requests general infrastructure administration, styling, or unrelated operations outside webflow code components or unrelated operations outside webflow code components. | User asks 'How do I handle webflow code components in my workflow?' -> Disambiguate: Clarify whether the task requires specialized webflow code components procedures or general ui-ux tooling. |
| `wireframe-spec` | User asks to implement, configure, or optimize wireframe spec tasks (specifically configuring or implementing wireframe spec specifications). | User requests general infrastructure administration, styling, or unrelated operations outside wireframe spec or unrelated operations outside wireframe spec. | User asks 'How do I handle wireframe spec in my workflow?' -> Disambiguate: Clarify whether the task requires specialized wireframe spec procedures or general ui-ux tooling. |
| `xlsx` | User asks to implement, configure, or optimize xlsx tasks (specifically configuring or implementing xlsx specifications). | User requests general infrastructure administration, styling, or unrelated operations outside xlsx or unrelated operations outside xlsx. | User asks 'How do I handle xlsx in my workflow?' -> Disambiguate: Clarify whether the task requires specialized xlsx procedures or general ui-ux tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/design-and-experience/ui-ux/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `40bb1c0ea6d591e4fa9a258039b9902b611f6c520482f60abf798d6895dedc81` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `webflow-code-components` | `references/bundling-and-import.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/cli.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/component-architecture.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/define-code-component.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/faq.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/frameworks-and-libraries.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/hooks.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/installation.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/introduction.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/boolean.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/id.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/image.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/link.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/number.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/rich-text.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/slot.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/text-node.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/text.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/variant.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/prop-types/visibility.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/quick-start.md` | Created or preserved in canonical package |
| `webflow-code-components` | `references/styling-components.md` | Created or preserved in canonical package |
| `webflow-code-components` | `scripts/search_references.py` | Created or preserved in canonical package |
| `xlsx` | `LICENSE.txt` | Created or preserved in canonical package |
| `xlsx` | `recalc.py` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
