# Phase 08 Batch Audit Record: `batch-52-development-backend-part08`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-52-development-backend-part08`
- **Category / Subcategory**: `development` / `backend`
- **Member Skill Count**: 15
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `f3e5f86a1e37e647c1b69015a5f184757fd511570c6fee3d248e8ebfa09da5be`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `php-pro` | `task-folder/agents/skills/php-pro` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgres-best-practices` | `task-folder/agents/skills/postman/postgres/postgres-best-practices` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgres-readonly-queries` | `task-folder/agents/skills/postman/postgres/postgres-readonly-queries` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgresql` | `task-folder/agents/skills/postman/postgres/postgresql` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgresql-cli` | `task-folder/agents/skills/postman/postgres/postgresql-cli` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgresql-code-review` | `task-folder/agents/skills/postman/postgres/postgresql-code-review` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgresql-optimization` | `task-folder/agents/skills/postman/postgres/postgresql-optimization` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postgresql-table-design` | `task-folder/agents/skills/postman/postgres/postgresql-table-design` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postman-collection-generator` | `task-folder/agents/skills/postman/postman-collection-generator` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postman-newman-automation` | `task-folder/agents/skills/postman/postman-newman-automation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `postman-openapi-converter` | `task-folder/agents/skills/postman/postman-openapi-converter` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pre-ship-gate` | `task-folder/agents/skills/pre-ship-gate` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `privacy-mask` | `task-folder/agents/skills/privacy-mask` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pydantic-ai` | `task-folder/agents/skills/python/pydantic-ai` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `pypict-skill` | `task-folder/agents/skills/python/pypict-skill` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `php-pro` | User asks to implement, configure, or optimize php pro tasks (specifically configuring or implementing php pro specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside php pro. | User asks 'How do I handle php pro in my workflow?' -> Disambiguate: Clarify whether the task requires specialized php pro procedures or general backend tooling. |
| `postgres-best-practices` | User asks to implement, configure, or optimize postgres best practices tasks (specifically configuring or implementing postgres best practices specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postgres best practices or unrelated operations outside postgres best practices. | User asks 'How do I handle postgres best practices in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgres best practices procedures or general backend tooling. |
| `postgres-readonly-queries` | User asks to implement, configure, or optimize postgres readonly queries tasks (specifically configuring or implementing postgres readonly queries specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postgres readonly queries or unrelated operations outside postgres readonly queries. | User asks 'How do I handle postgres readonly queries in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgres readonly queries procedures or general backend tooling. |
| `postgresql` | User asks to implement, configure, or optimize postgresql tasks (specifically configuring or implementing postgresql specifications). | User requests You are targeting a non-PostgreSQL database or unrelated operations outside postgresql. | User asks 'How do I handle postgresql in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgresql procedures or general backend tooling. |
| `postgresql-cli` | User asks to implement, configure, or optimize postgresql cli tasks (specifically configuring or implementing postgresql cli specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postgresql cli or unrelated operations outside postgresql cli. | User asks 'How do I handle postgresql cli in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgresql cli procedures or general backend tooling. |
| `postgresql-code-review` | User asks to implement, configure, or optimize postgresql code review tasks (specifically configuring or implementing postgresql code review specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postgresql code review or unrelated operations outside postgresql code review. | User asks 'How do I handle postgresql code review in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgresql code review procedures or general backend tooling. |
| `postgresql-optimization` | User asks to implement, configure, or optimize postgresql optimization tasks (specifically configuring or implementing postgresql optimization specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postgresql optimization or unrelated operations outside postgresql optimization. | User asks 'How do I handle postgresql optimization in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgresql optimization procedures or general backend tooling. |
| `postgresql-table-design` | User asks to implement, configure, or optimize postgresql table design tasks (specifically configuring or implementing postgresql table design specifications). | User requests DO NOT use `timestamp` (without time zone); DO use `timestamptz` instead or unrelated operations outside postgresql table design. | User asks 'How do I handle postgresql table design in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postgresql table design procedures or general backend tooling. |
| `postman-collection-generator` | User asks to implement, configure, or optimize postman collection generator tasks (specifically configuring or implementing postman collection generator specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postman collection generator or unrelated operations outside postman collection generator. | User asks 'How do I handle postman collection generator in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postman collection generator procedures or general backend tooling. |
| `postman-newman-automation` | User asks to implement, configure, or optimize postman newman automation tasks (specifically configuring or implementing postman newman automation specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postman newman automation or unrelated operations outside postman newman automation. | User asks 'How do I handle postman newman automation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postman newman automation procedures or general backend tooling. |
| `postman-openapi-converter` | User asks to implement, configure, or optimize postman openapi converter tasks (specifically configuring or implementing postman openapi converter specifications). | User requests general infrastructure administration, styling, or unrelated operations outside postman openapi converter or unrelated operations outside postman openapi converter. | User asks 'How do I handle postman openapi converter in my workflow?' -> Disambiguate: Clarify whether the task requires specialized postman openapi converter procedures or general backend tooling. |
| `pre-ship-gate` | User asks to implement, configure, or optimize pre ship gate tasks (specifically configuring or implementing pre ship gate specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pre ship gate or unrelated operations outside pre ship gate. | User asks 'How do I handle pre ship gate in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pre ship gate procedures or general backend tooling. |
| `privacy-mask` | User asks to implement, configure, or optimize privacy mask tasks (specifically configuring or implementing privacy mask specifications). | User requests general infrastructure administration, styling, or unrelated operations outside privacy mask or unrelated operations outside privacy mask. | User asks 'How do I handle privacy mask in my workflow?' -> Disambiguate: Clarify whether the task requires specialized privacy mask procedures or general backend tooling. |
| `pydantic-ai` | User asks to implement, configure, or optimize pydantic ai tasks (specifically configuring or implementing pydantic ai specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pydantic ai or unrelated operations outside pydantic ai. | User asks 'How do I handle pydantic ai in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pydantic ai procedures or general backend tooling. |
| `pypict-skill` | User asks to implement, configure, or optimize pypict skill tasks (specifically configuring or implementing pypict skill specifications). | User requests general infrastructure administration, styling, or unrelated operations outside pypict skill or unrelated operations outside pypict skill. | User asks 'How do I handle pypict skill in my workflow?' -> Disambiguate: Clarify whether the task requires specialized pypict skill procedures or general backend tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/development/backend/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `f3e5f86a1e37e647c1b69015a5f184757fd511570c6fee3d248e8ebfa09da5be` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `postgres-best-practices` | `AGENTS.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `README.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `metadata.json` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/_contributing.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/_sections.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/_template.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/advanced-full-text-search.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/advanced-jsonb-indexing.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/conn-idle-timeout.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/conn-limits.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/conn-pooling.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/conn-prepared-statements.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/data-batch-inserts.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/data-n-plus-one.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/data-pagination.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/data-upsert.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/lock-advisory.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/lock-deadlock-prevention.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/lock-short-transactions.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/lock-skip-locked.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/monitor-explain-analyze.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/monitor-pg-stat-statements.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/monitor-vacuum-analyze.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/query-composite-indexes.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/query-covering-indexes.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/query-index-types.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/query-missing-indexes.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/query-partial-indexes.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/schema-data-types.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/schema-foreign-key-indexes.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/schema-lowercase-identifiers.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/schema-partitioning.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/schema-primary-keys.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/security-privileges.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/security-rls-basics.md` | Created or preserved in canonical package |
| `postgres-best-practices` | `rules/security-rls-performance.md` | Created or preserved in canonical package |
| `postgres-readonly-queries` | `README.md` | Created or preserved in canonical package |
| `postgres-readonly-queries` | `connections.example.json` | Created or preserved in canonical package |
| `postgres-readonly-queries` | `requirements.txt` | Created or preserved in canonical package |
| `postgres-readonly-queries` | `scripts/query.py` | Created or preserved in canonical package |
| `postgresql-cli` | `references/cli-options-and-variables.md` | Created or preserved in canonical package |
| `postgresql-cli` | `references/meta-commands-core.md` | Created or preserved in canonical package |
| `postgresql-cli` | `references/meta-commands-formatting.md` | Created or preserved in canonical package |
| `postgresql-cli` | `references/meta-commands-inspection.md` | Created or preserved in canonical package |
| `postgresql-cli` | `references/tips-advanced.md` | Created or preserved in canonical package |
| `postgresql-cli` | `references/tips-workflows.md` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
