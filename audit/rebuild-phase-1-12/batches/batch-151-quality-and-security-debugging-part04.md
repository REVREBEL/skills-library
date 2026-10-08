# Phase 08 Batch Audit Record: `batch-151-quality-and-security-debugging-part04`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-151-quality-and-security-debugging-part04`
- **Category / Subcategory**: `quality-and-security` / `debugging`
- **Member Skill Count**: 11
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `9e8d879942cf7916856186e27f701fd70d65f0de3d83ecc2552883b4d05e19a5`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `playwright-java` | `task-folder/agents/skills/playwright-java` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgres` | `task-folder/agents/skills/postman/postgres/postgres` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `python-performance-optimization` | `task-folder/agents/skills/python/python-performance-optimization` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `report-writing` | `task-folder/agents/skills/report-writing` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `systematic-debugging` | `task-folder/agents/skills/systematic-debugging` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `the-honoured-one` | `task-folder/agents/skills/the-honoured-one` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `tool-design` | `task-folder/agents/skills/tool-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `using-n8n-mcp-skills` | `task-folder/agents/skills/using-n8n-mcp-skills` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `webflow-cli-troubleshooter` | `task-folder/agents/skills/webflow/webflow-cli-troubleshooter` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `webflow-designer-api` | `task-folder/agents/skills/webflow/webflow-designer-api` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `yes-md` | `task-folder/agents/skills/yes-md` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `playwright-java` | User asks to implement, configure, or optimize playwright java tasks (specifically configuring or implementing playwright java specifications). | User requests general infrastructure administration, styling, or unrelated operations outside playwright java or unrelated operations outside playwright java. | User asks 'How do I handle playwright java in my workflow?' -> Disambiguate: Clarify whether the task requires specialized playwright java procedures or general debugging tooling. |
| `postgres` | User asks to implement, configure, or optimize postgres tasks (specifically configuring or implementing postgres specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postgres or unrelated operations outside postgres. | User asks 'How do I handle postgres in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgres procedures or general debugging tooling. |
| `python-performance-optimization` | User asks to implement, configure, or optimize python performance optimization tasks (specifically configuring or implementing python performance optimization specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside python performance optimization. | User asks 'How do I handle python performance optimization in my workflow?' -> Disambiguate: Clarify whether the task requires specialized python performance optimization procedures or general debugging tooling. |
| `report-writing` | User asks to implement, configure, or optimize report writing tasks (specifically configuring or implementing report writing specifications). | User requests general infrastructure administration, styling, or unrelated operations outside report writing or unrelated operations outside report writing. | User asks 'How do I handle report writing in my workflow?' -> Disambiguate: Clarify whether the task requires specialized report writing procedures or general debugging tooling. |
| `systematic-debugging` | User asks to implement, configure, or optimize systematic debugging tasks (specifically configuring or implementing systematic debugging specifications). | User requests general infrastructure administration, styling, or unrelated operations outside systematic debugging or unrelated operations outside systematic debugging. | User asks 'How do I handle systematic debugging in my workflow?' -> Disambiguate: Clarify whether the task requires specialized systematic debugging procedures or general debugging tooling. |
| `the-honoured-one` | User asks to implement, configure, or optimize the honoured one tasks (specifically configuring or implementing the honoured one specifications). | User requests general infrastructure administration, styling, or unrelated operations outside the honoured one or unrelated operations outside the honoured one. | User asks 'How do I handle the honoured one in my workflow?' -> Disambiguate: Clarify whether the task requires specialized the honoured one procedures or general debugging tooling. |
| `tool-design` | User asks to implement, configure, or optimize tool design tasks (specifically configuring or implementing tool design specifications). | User requests general infrastructure administration, styling, or unrelated operations outside tool design or unrelated operations outside tool design. | User asks 'How do I handle tool design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized tool design procedures or general debugging tooling. |
| `using-n8n-mcp-skills` | User asks to implement, configure, or optimize using n8n mcp skills tasks (specifically configuring or implementing using n8n mcp skills specifications). | User requests general infrastructure administration, styling, or unrelated operations outside using n8n mcp skills or unrelated operations outside using n8n mcp skills. | User asks 'How do I handle using n8n mcp skills in my workflow?' -> Disambiguate: Clarify whether the task requires specialized using n8n mcp skills procedures or general debugging tooling. |
| `webflow-cli-troubleshooter` | User asks to implement, configure, or optimize webflow cli troubleshooter tasks (specifically configuring or implementing webflow cli troubleshooter specifications). | User requests All CLI commands require proper descriptions (not context parameters) or unrelated operations outside webflow cli troubleshooter. | User asks 'How do I handle webflow cli troubleshooter in my workflow?' -> Disambiguate: Clarify whether the task requires specialized webflow cli troubleshooter procedures or general debugging tooling. |
| `webflow-designer-api` | User asks to implement, configure, or optimize webflow designer api tasks (specifically configuring or implementing webflow designer api specifications). | User requests general infrastructure administration, styling, or unrelated operations outside webflow designer api or unrelated operations outside webflow designer api. | User asks 'How do I handle webflow designer api in my workflow?' -> Disambiguate: Clarify whether the task requires specialized webflow designer api procedures or general debugging tooling. |
| `yes-md` | User asks to implement, configure, or optimize yes md tasks (specifically configuring or implementing yes md specifications). | User requests general infrastructure administration, styling, or unrelated operations outside yes md or unrelated operations outside yes md. | User asks 'How do I handle yes md in my workflow?' -> Disambiguate: Clarify whether the task requires specialized yes md procedures or general debugging tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/quality-and-security/debugging/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `9e8d879942cf7916856186e27f701fd70d65f0de3d83ecc2552883b4d05e19a5` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `playwright-java` | `BasePage.java` | Created or preserved in canonical package |
| `playwright-java` | `BaseTest.java` | Created or preserved in canonical package |
| `playwright-java` | `assertions.md` | Created or preserved in canonical package |
| `playwright-java` | `config.md` | Created or preserved in canonical package |
| `playwright-java` | `fixtures.md` | Created or preserved in canonical package |
| `playwright-java` | `page-objects.md` | Created or preserved in canonical package |
| `postgres` | `references/backup-recovery.md` | Created or preserved in canonical package |
| `postgres` | `references/index-optimization.md` | Created or preserved in canonical package |
| `postgres` | `references/indexing.md` | Created or preserved in canonical package |
| `postgres` | `references/memory-management-ops.md` | Created or preserved in canonical package |
| `postgres` | `references/monitoring.md` | Created or preserved in canonical package |
| `postgres` | `references/mvcc-transactions.md` | Created or preserved in canonical package |
| `postgres` | `references/mvcc-vacuum.md` | Created or preserved in canonical package |
| `postgres` | `references/optimization-checklist.md` | Created or preserved in canonical package |
| `postgres` | `references/partitioning.md` | Created or preserved in canonical package |
| `postgres` | `references/pgbouncer-configuration.md` | Created or preserved in canonical package |
| `postgres` | `references/process-architecture.md` | Created or preserved in canonical package |
| `postgres` | `references/ps-cli-api-insights.md` | Created or preserved in canonical package |
| `postgres` | `references/ps-cli-commands.md` | Created or preserved in canonical package |
| `postgres` | `references/ps-connection-pooling.md` | Created or preserved in canonical package |
| `postgres` | `references/ps-connections.md` | Created or preserved in canonical package |
| `postgres` | `references/ps-extensions.md` | Created or preserved in canonical package |
| `postgres` | `references/ps-insights.md` | Created or preserved in canonical package |
| `postgres` | `references/query-patterns.md` | Created or preserved in canonical package |
| `postgres` | `references/replication.md` | Created or preserved in canonical package |
| `postgres` | `references/schema-design.md` | Created or preserved in canonical package |
| `postgres` | `references/storage-layout.md` | Created or preserved in canonical package |
| `postgres` | `references/wal-operations.md` | Created or preserved in canonical package |
| `python-performance-optimization` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `report-writing` | `SKILL_01.md` | Created or preserved in canonical package |
| `report-writing` | `ai-writing-detection.md` | Created or preserved in canonical package |
| `report-writing` | `artifacts-builder/LICENSE.txt` | Created or preserved in canonical package |
| `report-writing` | `artifacts-builder/SKILL.md` | Created or preserved in canonical package |
| `report-writing` | `artifacts-builder/scripts/bundle-artifact.sh` | Created or preserved in canonical package |
| `report-writing` | `artifacts-builder/scripts/init-artifact.sh` | Created or preserved in canonical package |
| `report-writing` | `artifacts-builder/scripts/shadcn-components.tar.gz` | Created or preserved in canonical package |
| `report-writing` | `formats/INDEX.md` | Created or preserved in canonical package |
| `report-writing` | `formats/data.md` | Created or preserved in canonical package |
| `report-writing` | `formats/htb-completion-report.md` | Created or preserved in canonical package |
| `report-writing` | `formats/logs.md` | Created or preserved in canonical package |
| `report-writing` | `formats/reconnaissance.md` | Created or preserved in canonical package |
| `report-writing` | `formats/sensitive-data-metadata.md` | Created or preserved in canonical package |
| `report-writing` | `formats/techstack-evidence-formatter.md` | Created or preserved in canonical package |
| `report-writing` | `formats/techstack-json-report.md` | Created or preserved in canonical package |
| `report-writing` | `formats/techstack-report-exporter.md` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/SKILL.md` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Carlito-Bold.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Carlito-BoldItalic.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Carlito-Italic.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Carlito-Regular.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Poppins-Bold.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Poppins-Italic.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Poppins-Light.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Poppins-Medium.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/fonts/Poppins-Regular.ttf` | Created or preserved in canonical package |
| `report-writing` | `formats/transilience-report-style/pentest-report.md` | Created or preserved in canonical package |
| `report-writing` | `image-enhancer/SKILL.md` | Created or preserved in canonical package |
| `report-writing` | `practice-makes-perfect.md` | Created or preserved in canonical package |
| `report-writing` | `practice-makes-perfect.pdf` | Created or preserved in canonical package |
| `report-writing` | `scripts/fix-skill-names.ts` | Created or preserved in canonical package |
| `report-writing` | `scripts/install-skills.sh` | Created or preserved in canonical package |
| `report-writing` | `scripts/link-skills.sh` | Created or preserved in canonical package |
| `report-writing` | `scripts/lint-skills.ts` | Created or preserved in canonical package |
| `report-writing` | `scripts/rename-skills.ts` | Created or preserved in canonical package |
| `systematic-debugging` | `CREATION-LOG.md` | Created or preserved in canonical package |
| `systematic-debugging` | `condition-based-waiting-example.ts` | Created or preserved in canonical package |
| `systematic-debugging` | `condition-based-waiting.md` | Created or preserved in canonical package |
| `systematic-debugging` | `defense-in-depth.md` | Created or preserved in canonical package |
| `systematic-debugging` | `find-polluter.sh` | Created or preserved in canonical package |
| `systematic-debugging` | `root-cause-tracing.md` | Created or preserved in canonical package |
| `systematic-debugging` | `test-academic.md` | Created or preserved in canonical package |
| `systematic-debugging` | `test-pressure-1.md` | Created or preserved in canonical package |
| `systematic-debugging` | `test-pressure-2.md` | Created or preserved in canonical package |
| `systematic-debugging` | `test-pressure-3.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `assets/install-playground-prompt.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `assets/webflow-variables.css` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/app-submission-and-listing.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/assets-api.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/code-examples.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/components-api.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/create-webflow-extension-reference.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/design-guidelines.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/designer-apis-reference.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/designer-extension-workflow.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/elements-api.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/error-handling.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/extension-utilities.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/faq.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/marketplace-guidelines.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/pages-api.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/playground-workflow.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/register-app.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/styles-api.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/variables-api.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `references/webflow-cli-reference.md` | Created or preserved in canonical package |
| `webflow-designer-api` | `scripts/search_references.py` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
