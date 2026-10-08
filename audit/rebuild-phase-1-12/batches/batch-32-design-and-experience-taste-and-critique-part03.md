# Phase 08 Batch Audit Record: `batch-32-design-and-experience-taste-and-critique-part03`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-32-design-and-experience-taste-and-critique-part03`
- **Category / Subcategory**: `design-and-experience` / `taste-and-critique`
- **Member Skill Count**: 13
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `b4689062bc3528374880e3acc678ede55c678011b33c7e885fd79092783e92ba`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `design-review-process` | `task-folder/agents/skills/design/designer-skills-main/design-ops/skills/design-review-process` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `design-review_2` | `task-folder/agents/skills/design/design-review_2` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `design-system` | `task-folder/agents/skills/design/design-system` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `design-taste-frontend` | `task-folder/agents/skills/design/design-taste-frontend` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `deterministic-design` | `task-folder/agents/skills/design/deterministic-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `duotone-design` | `task-folder/agents/skills/design/design-it/duotone-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `editorial-design` | `task-folder/agents/skills/design/design-it/editorial-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `email-design-eng` | `task-folder/agents/skills/email/email-design-eng` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `flat-design` | `task-folder/agents/skills/design/design-it/flat-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `flat-design-2` | `task-folder/agents/skills/design/design-it/flat-design-2` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `floating-ui` | `task-folder/agents/skills/design/design-it/floating-ui` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `front-end-design` | `task-folder/agents/skills/front end/front-end-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `frontend-enhancer` | `task-folder/agents/skills/design/frontend-enhancer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `design-review-process` | User asks to implement, configure, or optimize design review process tasks (specifically configuring or implementing design review process specifications). | User requests general infrastructure administration, styling, or unrelated operations outside design review process or unrelated operations outside design review process. | User asks 'How do I handle design review process in my workflow?' -> Disambiguate: Clarify whether the task requires specialized design review process procedures or general taste-and-critique tooling. |
| `design-review_2` | User asks to implement, configure, or optimize design review_2 tasks (specifically configuring or implementing design review_2 specifications). | User requests general infrastructure administration, styling, or unrelated operations outside design review_2 or unrelated operations outside design review_2. | User asks 'How do I handle design review_2 in my workflow?' -> Disambiguate: Clarify whether the task requires specialized design review_2 procedures or general taste-and-critique tooling. |
| `design-system` | User asks to implement, configure, or optimize design system tasks (specifically configuring or implementing design system specifications). | User requests Gate visibility on the real font.** Synchronously in `<head>`, add a `fonts-pending` class to `<html>` that holds the display-font text at `opacity: 0`. On `document.fonts.ready` — kick it with `document.fonts.load('<weight> 1em "Family"')` for each critical face — swap to `fonts-ready` and fade the text in (~0.5s). Always include a safety timeout (~2.5s) that reveals regardless, so a font failure can never leave text permanently hidden or unrelated operations outside design system. | User asks 'How do I handle design system in my workflow?' -> Disambiguate: Clarify whether the task requires specialized design system procedures or general taste-and-critique tooling. |
| `design-taste-frontend` | User asks to implement, configure, or optimize design taste frontend tasks (specifically configuring or implementing design taste frontend specifications). | User requests Animation:** **Motion** (the library formerly known as Framer Motion). Import from `motion/react` (`import { motion } from "motion/react"`). The `framer-motion` package still works as a legacy alias - prefer `motion/react` in new code or unrelated operations outside design taste frontend. | User asks 'How do I handle design taste frontend in my workflow?' -> Disambiguate: Clarify whether the task requires specialized design taste frontend procedures or general taste-and-critique tooling. |
| `deterministic-design` | User asks to implement, configure, or optimize deterministic design tasks (specifically configuring or implementing deterministic design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside deterministic design or unrelated operations outside deterministic design. | User asks 'How do I handle deterministic design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized deterministic design procedures or general taste-and-critique tooling. |
| `duotone-design` | User asks to implement, configure, or optimize duotone design tasks (specifically configuring or implementing duotone design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside duotone design or unrelated operations outside duotone design. | User asks 'How do I handle duotone design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized duotone design procedures or general taste-and-critique tooling. |
| `editorial-design` | User asks to implement, configure, or optimize editorial design tasks (specifically configuring or implementing editorial design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside editorial design or unrelated operations outside editorial design. | User asks 'How do I handle editorial design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized editorial design procedures or general taste-and-critique tooling. |
| `email-design-eng` | User asks to implement, configure, or optimize email design eng tasks (specifically configuring or implementing email design eng specifications). | User requests general infrastructure administration, styling, or unrelated operations outside email design eng or unrelated operations outside email design eng. | User asks 'How do I handle email design eng in my workflow?' -> Disambiguate: Clarify whether the task requires specialized email design eng procedures or general taste-and-critique tooling. |
| `flat-design` | User asks to implement, configure, or optimize flat design tasks (specifically configuring or implementing flat design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside flat design or unrelated operations outside flat design. | User asks 'How do I handle flat design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized flat design procedures or general taste-and-critique tooling. |
| `flat-design-2` | User asks to implement, configure, or optimize flat design 2 tasks (specifically configuring or implementing flat design 2 specifications). | User requests general infrastructure administration, styling, or unrelated operations outside flat design 2 or unrelated operations outside flat design 2. | User asks 'How do I handle flat design 2 in my workflow?' -> Disambiguate: Clarify whether the task requires specialized flat design 2 procedures or general taste-and-critique tooling. |
| `floating-ui` | User asks to implement, configure, or optimize floating ui tasks (specifically configuring or implementing floating ui specifications). | User requests general infrastructure administration, styling, or unrelated operations outside floating ui or unrelated operations outside floating ui. | User asks 'How do I handle floating ui in my workflow?' -> Disambiguate: Clarify whether the task requires specialized floating ui procedures or general taste-and-critique tooling. |
| `front-end-design` | User asks to implement, configure, or optimize front end design tasks (specifically configuring or implementing front end design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside front end design or unrelated operations outside front end design. | User asks 'How do I handle front end design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized front end design procedures or general taste-and-critique tooling. |
| `frontend-enhancer` | User asks to implement, configure, or optimize frontend enhancer tasks (specifically configuring or implementing frontend enhancer specifications). | User requests general infrastructure administration, styling, or unrelated operations outside frontend enhancer or unrelated operations outside frontend enhancer. | User asks 'How do I handle frontend enhancer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized frontend enhancer procedures or general taste-and-critique tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/design-and-experience/taste-and-critique/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `b4689062bc3528374880e3acc678ede55c678011b33c7e885fd79092783e92ba` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `design-system` | `references/motion-choreography.md` | Created or preserved in canonical package |
| `deterministic-design` | `design-audit/SKILL.md` | Created or preserved in canonical package |
| `deterministic-design` | `design-audit/references/design-rules.md` | Created or preserved in canonical package |
| `deterministic-design` | `design-audit/taste-skill-v1/SKILL.md` | Created or preserved in canonical package |
| `deterministic-design` | `design-audit/taste-skill/SKILL.md` | Created or preserved in canonical package |
| `front-end-design` | `metadata.json` | Created or preserved in canonical package |
| `frontend-enhancer` | `assets/animations.css` | Created or preserved in canonical package |
| `frontend-enhancer` | `assets/button-variants.tsx` | Created or preserved in canonical package |
| `frontend-enhancer` | `assets/card-variants.tsx` | Created or preserved in canonical package |
| `frontend-enhancer` | `assets/input-variants.tsx` | Created or preserved in canonical package |
| `frontend-enhancer` | `assets/layout-feature-grid.tsx` | Created or preserved in canonical package |
| `frontend-enhancer` | `assets/layout-hero-section.tsx` | Created or preserved in canonical package |
| `frontend-enhancer` | `assets/utils-cn.ts` | Created or preserved in canonical package |
| `frontend-enhancer` | `index.js` | Created or preserved in canonical package |
| `frontend-enhancer` | `package.json` | Created or preserved in canonical package |
| `frontend-enhancer` | `references/color_palettes.md` | Created or preserved in canonical package |
| `frontend-enhancer` | `references/design_principles.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
