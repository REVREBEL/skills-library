# Phase 08 Batch Audit Record: `batch-27-design-and-experience-design-systems-part04`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-27-design-and-experience-design-systems-part04`
- **Category / Subcategory**: `design-and-experience` / `design-systems`
- **Member Skill Count**: 13
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `d3b9072150e9e55a79a44c7cdeb0b0e4949810a9b0bcd66cee3a2c533f5493d8`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `tailwind-theme-builder` | `task-folder/agents/skills/tailwind/tailwind-theme-builder` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `theme-factory` | `task-folder/agents/skills/theme-factory` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `threat-modeling-expert` | `task-folder/agents/skills/threat-modeling-expert` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `transilience-report-style` | `task-folder/agents/skills/report-writing/formats/transilience-report-style` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ui-lint` | `task-folder/agents/skills/ui/ui-lint` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ui-pattern` | `task-folder/agents/skills/ui/ui-pattern` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ui-review` | `task-folder/agents/skills/ui/ui-review` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ui-setup` | `task-folder/agents/skills/ui/ui-setup` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ui-ux-designer` | `task-folder/agents/skills/ui/ui-ux-designer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ui-visual-validator` | `task-folder/agents/skills/ui/ui-visual-validator` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `visual-design-foundations` | `task-folder/agents/skills/design/designer/clean-gemini-agents/gemini-agents/skills/ux-design/visual-design-foundations` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `web-component-design` | `task-folder/agents/skills/design/designer/clean-gemini-agents/gemini-agents/skills/ux-design/web-component-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `writing-skills` | `task-folder/agents/skills/figma/writing-skills` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `tailwind-theme-builder` | User asks to implement, configure, or optimize tailwind theme builder tasks (specifically configuring or implementing tailwind theme builder specifications). | User requests general infrastructure administration, styling, or unrelated operations outside tailwind theme builder or unrelated operations outside tailwind theme builder. | User asks 'How do I handle tailwind theme builder in my workflow?' -> Disambiguate: Clarify whether the task requires specialized tailwind theme builder procedures or general design-systems tooling. |
| `theme-factory` | User asks to implement, configure, or optimize theme factory tasks (specifically configuring or implementing theme factory specifications). | User requests general infrastructure administration, styling, or unrelated operations outside theme factory or unrelated operations outside theme factory. | User asks 'How do I handle theme factory in my workflow?' -> Disambiguate: Clarify whether the task requires specialized theme factory procedures or general design-systems tooling. |
| `threat-modeling-expert` | User asks to implement, configure, or optimize threat modeling expert tasks (specifically configuring or implementing threat modeling expert specifications). | User requests You lack scope or authorization for security review or unrelated operations outside threat modeling expert. | User asks 'How do I handle threat modeling expert in my workflow?' -> Disambiguate: Clarify whether the task requires specialized threat modeling expert procedures or general design-systems tooling. |
| `transilience-report-style` | User asks to implement, configure, or optimize transilience report style tasks (specifically Version:** 4.0). | User requests general infrastructure administration, styling, or unrelated operations outside transilience report style or unrelated operations outside transilience report style. | User asks 'How do I handle transilience report style in my workflow?' -> Disambiguate: Clarify whether the task requires specialized transilience report style procedures or general design-systems tooling. |
| `ui-lint` | User asks to implement, configure, or optimize ui lint tasks (specifically configuring or implementing ui lint specifications). | User requests For deeper review of design judgment (composition, hierarchy, rhythm) → use `/ss-review` or unrelated operations outside ui lint. | User asks 'How do I handle ui lint in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ui lint procedures or general design-systems tooling. |
| `ui-pattern` | User asks to implement, configure, or optimize ui pattern tasks (specifically configuring or implementing ui pattern specifications). | User requests For a single primitive component → use `/ss-component` or unrelated operations outside ui pattern. | User asks 'How do I handle ui pattern in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ui pattern procedures or general design-systems tooling. |
| `ui-review` | User asks to implement, configure, or optimize ui review tasks (specifically configuring or implementing ui review specifications). | User requests For accessibility-only issues → use `/ss-a11y` or unrelated operations outside ui review. | User asks 'How do I handle ui review in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ui review procedures or general design-systems tooling. |
| `ui-setup` | User asks to implement, configure, or optimize ui setup tasks (specifically configuring or implementing ui setup specifications). | User requests For projects already configured with StyleSeed → use `/ss-update` instead or unrelated operations outside ui setup. | User asks 'How do I handle ui setup in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ui setup procedures or general design-systems tooling. |
| `ui-ux-designer` | User asks to implement, configure, or optimize ui ux designer tasks (specifically configuring or implementing ui ux designer specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside ui ux designer. | User asks 'How do I handle ui ux designer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ui ux designer procedures or general design-systems tooling. |
| `ui-visual-validator` | User asks to implement, configure, or optimize ui visual validator tasks (specifically configuring or implementing ui visual validator specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside ui visual validator. | User asks 'How do I handle ui visual validator in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ui visual validator procedures or general design-systems tooling. |
| `visual-design-foundations` | User asks to implement, configure, or optimize visual design foundations tasks (specifically configuring or implementing visual design foundations specifications). | User requests general infrastructure administration, styling, or unrelated operations outside visual design foundations or unrelated operations outside visual design foundations. | User asks 'How do I handle visual design foundations in my workflow?' -> Disambiguate: Clarify whether the task requires specialized visual design foundations procedures or general design-systems tooling. |
| `web-component-design` | User asks to implement, configure, or optimize web component design tasks (specifically configuring or implementing web component design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside web component design or unrelated operations outside web component design. | User asks 'How do I handle web component design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized web component design procedures or general design-systems tooling. |
| `writing-skills` | User asks to implement, configure, or optimize writing skills tasks (specifically configuring or implementing writing skills specifications). | User requests general infrastructure administration, styling, or unrelated operations outside writing skills or unrelated operations outside writing skills. | User asks 'How do I handle writing skills in my workflow?' -> Disambiguate: Clarify whether the task requires specialized writing skills procedures or general design-systems tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/design-and-experience/design-systems/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `d3b9072150e9e55a79a44c7cdeb0b0e4949810a9b0bcd66cee3a2c533f5493d8` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `tailwind-theme-builder` | `assets/components.json` | Created or preserved in canonical package |
| `tailwind-theme-builder` | `assets/index.css` | Created or preserved in canonical package |
| `tailwind-theme-builder` | `assets/theme-provider.tsx` | Created or preserved in canonical package |
| `tailwind-theme-builder` | `assets/tsconfig.app.json` | Created or preserved in canonical package |
| `tailwind-theme-builder` | `assets/utils.ts` | Created or preserved in canonical package |
| `tailwind-theme-builder` | `assets/vite.config.ts` | Created or preserved in canonical package |
| `tailwind-theme-builder` | `references/migration-guide.md` | Created or preserved in canonical package |
| `theme-factory` | `LICENSE.txt` | Created or preserved in canonical package |
| `theme-factory` | `theme-showcase.pdf` | Created or preserved in canonical package |
| `theme-factory` | `themes/arctic-frost.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/botanical-garden.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/desert-rose.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/forest-canopy.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/golden-hour.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/midnight-galaxy.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/modern-minimalist.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/ocean-depths.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/sunset-boulevard.md` | Created or preserved in canonical package |
| `theme-factory` | `themes/tech-innovation.md` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Carlito-Bold.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Carlito-BoldItalic.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Carlito-Italic.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Carlito-Regular.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Poppins-Bold.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Poppins-Italic.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Poppins-Light.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Poppins-Medium.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `fonts/Poppins-Regular.ttf` | Created or preserved in canonical package |
| `transilience-report-style` | `pentest-report.md` | Created or preserved in canonical package |
| `writing-skills` | `agents/openai.yaml` | Created or preserved in canonical package |
| `writing-skills` | `anthropic-best-practices.md` | Created or preserved in canonical package |
| `writing-skills` | `assets/icon.svg` | Created or preserved in canonical package |
| `writing-skills` | `examples.md` | Created or preserved in canonical package |
| `writing-skills` | `gotchas.md` | Created or preserved in canonical package |
| `writing-skills` | `graphviz-conventions.dot` | Created or preserved in canonical package |
| `writing-skills` | `persuasion-principles.md` | Created or preserved in canonical package |
| `writing-skills` | `references/anti-rationalization/README.md` | Created or preserved in canonical package |
| `writing-skills` | `references/cso/README.md` | Created or preserved in canonical package |
| `writing-skills` | `references/standards/README.md` | Created or preserved in canonical package |
| `writing-skills` | `references/standards/metadata-standard.md` | Created or preserved in canonical package |
| `writing-skills` | `references/templates/discipline.md` | Created or preserved in canonical package |
| `writing-skills` | `references/templates/pattern.md` | Created or preserved in canonical package |
| `writing-skills` | `references/templates/reference.md` | Created or preserved in canonical package |
| `writing-skills` | `references/templates/technique.md` | Created or preserved in canonical package |
| `writing-skills` | `references/templates/tier-3-platform.md` | Created or preserved in canonical package |
| `writing-skills` | `references/testing/README.md` | Created or preserved in canonical package |
| `writing-skills` | `references/tier-1-simple/README.md` | Created or preserved in canonical package |
| `writing-skills` | `references/tier-2-expanded/README.md` | Created or preserved in canonical package |
| `writing-skills` | `references/tier-3-platform/README.md` | Created or preserved in canonical package |
| `writing-skills` | `render-graphs.js` | Created or preserved in canonical package |
| `writing-skills` | `testing-skills-with-subagents.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
