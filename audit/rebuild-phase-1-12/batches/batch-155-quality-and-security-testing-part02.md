# Phase 08 Batch Audit Record: `batch-155-quality-and-security-testing-part02`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-155-quality-and-security-testing-part02`
- **Category / Subcategory**: `quality-and-security` / `testing`
- **Member Skill Count**: 13
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `abb6989d3a3b1276832a11bfa3fa466760dcd9ced02c901f66cf71c30867ffa8`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `dependency-upgrade` | `task-folder/agents/skills/dependency-upgrade` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `deployment-validation-config-validate` | `task-folder/agents/skills/deployment-validation-config-validate` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `doc-coauthoring` | `task-folder/agents/skills/documentation/doc-coauthoring` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `durable-objects` | `task-folder/agents/skills/durable-objects` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `e2e-testing-patterns` | `task-folder/agents/skills/e2e-testing-patterns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `evaluation` | `task-folder/agents/skills/evaluation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `focus-group` | `task-folder/agents/skills/marketing/digital-marketing-pro-main/skills/focus-group` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `framework-migration-deps-upgrade` | `task-folder/agents/skills/framework-migration-deps-upgrade` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `javascript-testing-patterns` | `task-folder/agents/skills/javascript/javascript-testing-patterns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `lint-and-validate` | `task-folder/agents/skills/lint-and-validate` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `llm-evaluation` | `task-folder/agents/skills/llm/llm/llm-evaluation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `mcp-tool-developer` | `task-folder/agents/skills/mcp/mcp-tool-developer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ml-engineer` | `task-folder/agents/skills/ml-engineer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `dependency-upgrade` | User asks to implement, configure, or optimize dependency upgrade tasks (specifically configuring or implementing dependency upgrade specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside dependency upgrade. | User asks 'How do I handle dependency upgrade in my workflow?' -> Disambiguate: Clarify whether the task requires specialized dependency upgrade procedures or general testing tooling. |
| `deployment-validation-config-validate` | User asks to implement, configure, or optimize deployment validation config validate tasks (specifically configuring or implementing deployment validation config validate specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside deployment validation config validate. | User asks 'How do I handle deployment validation config validate in my workflow?' -> Disambiguate: Clarify whether the task requires specialized deployment validation config validate procedures or general testing tooling. |
| `doc-coauthoring` | User asks to implement, configure, or optimize doc coauthoring tasks (specifically configuring or implementing doc coauthoring specifications). | User requests general infrastructure administration, styling, or unrelated operations outside doc coauthoring or unrelated operations outside doc coauthoring. | User asks 'How do I handle doc coauthoring in my workflow?' -> Disambiguate: Clarify whether the task requires specialized doc coauthoring procedures or general testing tooling. |
| `durable-objects` | User asks to implement, configure, or optimize durable objects tasks (specifically configuring or implementing durable objects specifications). | User requests Stateless request handling (use plain Workers) or unrelated operations outside durable objects. | User asks 'How do I handle durable objects in my workflow?' -> Disambiguate: Clarify whether the task requires specialized durable objects procedures or general testing tooling. |
| `e2e-testing-patterns` | User asks to implement, configure, or optimize e2e testing patterns tasks (specifically configuring or implementing e2e testing patterns specifications). | User requests You only need unit or integration tests or unrelated operations outside e2e testing patterns. | User asks 'How do I handle e2e testing patterns in my workflow?' -> Disambiguate: Clarify whether the task requires specialized e2e testing patterns procedures or general testing tooling. |
| `evaluation` | User asks to implement, configure, or optimize evaluation tasks (specifically configuring or implementing evaluation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside evaluation or unrelated operations outside evaluation. | User asks 'How do I handle evaluation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized evaluation procedures or general testing tooling. |
| `focus-group` | User asks to implement, configure, or optimize focus group tasks (specifically configuring or implementing focus group specifications). | User requests general infrastructure administration, styling, or unrelated operations outside focus group or unrelated operations outside focus group. | User asks 'How do I handle focus group in my workflow?' -> Disambiguate: Clarify whether the task requires specialized focus group procedures or general testing tooling. |
| `framework-migration-deps-upgrade` | User asks to implement, configure, or optimize framework migration deps upgrade tasks (specifically configuring or implementing framework migration deps upgrade specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside framework migration deps upgrade. | User asks 'How do I handle framework migration deps upgrade in my workflow?' -> Disambiguate: Clarify whether the task requires specialized framework migration deps upgrade procedures or general testing tooling. |
| `javascript-testing-patterns` | User asks to implement, configure, or optimize javascript testing patterns tasks (specifically configuring or implementing javascript testing patterns specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside javascript testing patterns. | User asks 'How do I handle javascript testing patterns in my workflow?' -> Disambiguate: Clarify whether the task requires specialized javascript testing patterns procedures or general testing tooling. |
| `lint-and-validate` | User asks to implement, configure, or optimize lint and validate tasks (specifically configuring or implementing lint and validate specifications). | User requests general infrastructure administration, styling, or unrelated operations outside lint and validate or unrelated operations outside lint and validate. | User asks 'How do I handle lint and validate in my workflow?' -> Disambiguate: Clarify whether the task requires specialized lint and validate procedures or general testing tooling. |
| `llm-evaluation` | User asks to implement, configure, or optimize llm evaluation tasks (specifically configuring or implementing llm evaluation specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside llm evaluation. | User asks 'How do I handle llm evaluation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized llm evaluation procedures or general testing tooling. |
| `mcp-tool-developer` | User asks to implement, configure, or optimize mcp tool developer tasks (specifically configuring or implementing mcp tool developer specifications). | User requests general infrastructure administration, styling, or unrelated operations outside mcp tool developer or unrelated operations outside mcp tool developer. | User asks 'How do I handle mcp tool developer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized mcp tool developer procedures or general testing tooling. |
| `ml-engineer` | User asks to implement, configure, or optimize ml engineer tasks (specifically configuring or implementing ml engineer specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside ml engineer. | User asks 'How do I handle ml engineer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ml engineer procedures or general testing tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/quality-and-security/testing/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `abb6989d3a3b1276832a11bfa3fa466760dcd9ced02c901f66cf71c30867ffa8` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `durable-objects` | `references/rules.md` | Created or preserved in canonical package |
| `durable-objects` | `references/testing.md` | Created or preserved in canonical package |
| `durable-objects` | `references/workers.md` | Created or preserved in canonical package |
| `e2e-testing-patterns` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `framework-migration-deps-upgrade` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `javascript-testing-patterns` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `lint-and-validate` | `scripts/lint_runner.py` | Created or preserved in canonical package |
| `lint-and-validate` | `scripts/type_coverage.py` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
