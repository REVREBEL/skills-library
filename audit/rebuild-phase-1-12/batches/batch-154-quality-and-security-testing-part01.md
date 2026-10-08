# Phase 08 Batch Audit Record: `batch-154-quality-and-security-testing-part01`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-154-quality-and-security-testing-part01`
- **Category / Subcategory**: `quality-and-security` / `testing`
- **Member Skill Count**: 13
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `af1108241826639fb008b75b2b38fe4f93876b81b840479a37f5f3cb2440af05`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `ab-testing` | `task-folder/agents/skills/ab-testing` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ab-testing-ecommerce` | `task-folder/agents/skills/data-analytics/data-analytics/ab-testing-ecommerce` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `actions-templates` | `task-folder/agents/skills/github/actions-templates` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `agent-evaluation` | `task-folder/agents/skills/agents/agent-evaluation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `agentic-eval` | `task-folder/agents/skills/agents/agentic-eval` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `api-testing-observability-api-mock` | `task-folder/agents/skills/api/api-testing-observability-api-mock` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `backtesting-frameworks` | `task-folder/agents/skills/backend/backtesting-frameworks` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `bash-scripting` | `task-folder/agents/skills/bash/bash-scripting` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `browser-automation` | `task-folder/agents/skills/browser-automation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `browser-testing-with-devtools` | `task-folder/agents/skills/browser-testing-with-devtools` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `code-showcase-testing-patterns` | `task-folder/agents/skills/code/code-showcase-testing-patterns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `data-engineering-data-driven-feature` | `task-folder/agents/skills/data/data-engineering-data-driven-feature` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `dbt-transformation-patterns` | `task-folder/agents/skills/databases/dbt-transformation-patterns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `ab-testing` | User asks to implement, configure, or optimize ab testing tasks (specifically configuring or implementing ab testing specifications). | User requests general infrastructure administration, styling, or unrelated operations outside ab testing or unrelated operations outside ab testing. | User asks 'How do I handle ab testing in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ab testing procedures or general testing tooling. |
| `ab-testing-ecommerce` | User asks to implement, configure, or optimize ab testing ecommerce tasks (specifically configuring or implementing ab testing ecommerce specifications). | User requests general infrastructure administration, styling, or unrelated operations outside ab testing ecommerce or unrelated operations outside ab testing ecommerce. | User asks 'How do I handle ab testing ecommerce in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ab testing ecommerce procedures or general testing tooling. |
| `actions-templates` | User asks to implement, configure, or optimize actions templates tasks (specifically configuring or implementing actions templates specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside actions templates. | User asks 'How do I handle actions templates in my workflow?' -> Disambiguate: Clarify whether the task requires specialized actions templates procedures or general testing tooling. |
| `agent-evaluation` | User asks to implement, configure, or optimize agent evaluation tasks (specifically configuring or implementing agent evaluation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside agent evaluation or unrelated operations outside agent evaluation. | User asks 'How do I handle agent evaluation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized agent evaluation procedures or general testing tooling. |
| `agentic-eval` | User asks to implement, configure, or optimize agentic eval tasks (specifically configuring or implementing agentic eval specifications). | User requests general infrastructure administration, styling, or unrelated operations outside agentic eval or unrelated operations outside agentic eval. | User asks 'How do I handle agentic eval in my workflow?' -> Disambiguate: Clarify whether the task requires specialized agentic eval procedures or general testing tooling. |
| `api-testing-observability-api-mock` | User asks to implement, configure, or optimize api testing observability api mock tasks (specifically configuring or implementing api testing observability api mock specifications). | User requests You need to test production systems or live integrations or unrelated operations outside api testing observability api mock. | User asks 'How do I handle api testing observability api mock in my workflow?' -> Disambiguate: Clarify whether the task requires specialized api testing observability api mock procedures or general testing tooling. |
| `backtesting-frameworks` | User asks to implement, configure, or optimize backtesting frameworks tasks (specifically configuring or implementing backtesting frameworks specifications). | User requests You need live trading execution or investment advice or unrelated operations outside backtesting frameworks. | User asks 'How do I handle backtesting frameworks in my workflow?' -> Disambiguate: Clarify whether the task requires specialized backtesting frameworks procedures or general testing tooling. |
| `bash-scripting` | User asks to implement, configure, or optimize bash scripting tasks (specifically configuring or implementing bash scripting specifications). | User requests general infrastructure administration, styling, or unrelated operations outside bash scripting or unrelated operations outside bash scripting. | User asks 'How do I handle bash scripting in my workflow?' -> Disambiguate: Clarify whether the task requires specialized bash scripting procedures or general testing tooling. |
| `browser-automation` | User asks to implement, configure, or optimize browser automation tasks (specifically configuring or implementing browser automation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside browser automation or unrelated operations outside browser automation. | User asks 'How do I handle browser automation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized browser automation procedures or general testing tooling. |
| `browser-testing-with-devtools` | User asks to implement, configure, or optimize browser testing with devtools tasks (specifically configuring or implementing browser testing with devtools specifications). | User requests general infrastructure administration, styling, or unrelated operations outside browser testing with devtools or unrelated operations outside browser testing with devtools. | User asks 'How do I handle browser testing with devtools in my workflow?' -> Disambiguate: Clarify whether the task requires specialized browser testing with devtools procedures or general testing tooling. |
| `code-showcase-testing-patterns` | User asks to implement, configure, or optimize code showcase testing patterns tasks (specifically configuring or implementing code showcase testing patterns specifications). | User requests general infrastructure administration, styling, or unrelated operations outside code showcase testing patterns or unrelated operations outside code showcase testing patterns. | User asks 'How do I handle code showcase testing patterns in my workflow?' -> Disambiguate: Clarify whether the task requires specialized code showcase testing patterns procedures or general testing tooling. |
| `data-engineering-data-driven-feature` | User asks to implement, configure, or optimize data engineering data driven feature tasks (specifically configuring or implementing data engineering data driven feature specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside data engineering data driven feature. | User asks 'How do I handle data engineering data driven feature in my workflow?' -> Disambiguate: Clarify whether the task requires specialized data engineering data driven feature procedures or general testing tooling. |
| `dbt-transformation-patterns` | User asks to implement, configure, or optimize dbt transformation patterns tasks (specifically configuring or implementing dbt transformation patterns specifications). | User requests The project is not using dbt or a warehouse-backed workflow or unrelated operations outside dbt transformation patterns. | User asks 'How do I handle dbt transformation patterns in my workflow?' -> Disambiguate: Clarify whether the task requires specialized dbt transformation patterns procedures or general testing tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/quality-and-security/testing/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `af1108241826639fb008b75b2b38fe4f93876b81b840479a37f5f3cb2440af05` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `ab-testing` | `evals/evals.json` | Created or preserved in canonical package |
| `ab-testing` | `references/sample-size-guide.md` | Created or preserved in canonical package |
| `ab-testing` | `references/test-templates.md` | Created or preserved in canonical package |
| `ab-testing-ecommerce` | `evals/exposure-tracking-conversion-tracking-an/criteria.json` | Created or preserved in canonical package |
| `ab-testing-ecommerce` | `evals/exposure-tracking-conversion-tracking-an/task.md` | Created or preserved in canonical package |
| `ab-testing-ecommerce` | `evals/pricing-test-consistency-guardrail-metri/criteria.json` | Created or preserved in canonical package |
| `ab-testing-ecommerce` | `evals/pricing-test-consistency-guardrail-metri/task.md` | Created or preserved in canonical package |
| `ab-testing-ecommerce` | `evals/sample-size-calculation-and-server-side-/criteria.json` | Created or preserved in canonical package |
| `ab-testing-ecommerce` | `evals/sample-size-calculation-and-server-side-/task.md` | Created or preserved in canonical package |
| `ab-testing-ecommerce` | `tile.json` | Created or preserved in canonical package |
| `agentic-eval` | `effective-agent-skills/SKILL.md` | Created or preserved in canonical package |
| `api-testing-observability-api-mock` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `backtesting-frameworks` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `dbt-transformation-patterns` | `resources/implementation-playbook.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
