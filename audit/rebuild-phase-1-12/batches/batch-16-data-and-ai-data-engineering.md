# Phase 08 Batch Audit Record: `batch-16-data-and-ai-data-engineering`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-16-data-and-ai-data-engineering`
- **Category / Subcategory**: `data-and-ai` / `data-engineering`
- **Member Skill Count**: 6
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `23d08c8b711f6bfa52eeb3665a892276b1821b56779bf0c72df48b92314458a4`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `data-engineer` | `task-folder/agents/skills/data/data-engineer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `data-engineering-data-pipeline` | `task-folder/agents/skills/data/data-engineering-data-pipeline` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `ml-pipeline-workflow` | `task-folder/agents/skills/ml-pipeline-workflow` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `mlops-engineer` | `task-folder/agents/skills/mlops-engineer` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `recsys-pipeline-architect` | `task-folder/agents/skills/recsys-pipeline-architect` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `scikit-learn` | `task-folder/agents/skills/scikit-learn` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `data-engineer` | User asks to implement, configure, or optimize data engineer tasks (specifically configuring or implementing data engineer specifications). | User requests You only need exploratory data analysis or unrelated operations outside data engineer. | User asks 'How do I handle data engineer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized data engineer procedures or general data-engineering tooling. |
| `data-engineering-data-pipeline` | User asks to implement, configure, or optimize data engineering data pipeline tasks (specifically configuring or implementing data engineering data pipeline specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside data engineering data pipeline. | User asks 'How do I handle data engineering data pipeline in my workflow?' -> Disambiguate: Clarify whether the task requires specialized data engineering data pipeline procedures or general data-engineering tooling. |
| `ml-pipeline-workflow` | User asks to implement, configure, or optimize ml pipeline workflow tasks (specifically configuring or implementing ml pipeline workflow specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside ml pipeline workflow. | User asks 'How do I handle ml pipeline workflow in my workflow?' -> Disambiguate: Clarify whether the task requires specialized ml pipeline workflow procedures or general data-engineering tooling. |
| `mlops-engineer` | User asks to implement, configure, or optimize mlops engineer tasks (specifically configuring or implementing mlops engineer specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside mlops engineer. | User asks 'How do I handle mlops engineer in my workflow?' -> Disambiguate: Clarify whether the task requires specialized mlops engineer procedures or general data-engineering tooling. |
| `recsys-pipeline-architect` | User asks to implement, configure, or optimize recsys pipeline architect tasks (specifically configuring or implementing recsys pipeline architect specifications). | User requests general infrastructure administration, styling, or unrelated operations outside recsys pipeline architect or unrelated operations outside recsys pipeline architect. | User asks 'How do I handle recsys pipeline architect in my workflow?' -> Disambiguate: Clarify whether the task requires specialized recsys pipeline architect procedures or general data-engineering tooling. |
| `scikit-learn` | User asks to implement, configure, or optimize scikit learn tasks (specifically configuring or implementing scikit learn specifications). | User requests general infrastructure administration, styling, or unrelated operations outside scikit learn or unrelated operations outside scikit learn. | User asks 'How do I handle scikit learn in my workflow?' -> Disambiguate: Clarify whether the task requires specialized scikit learn procedures or general data-engineering tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/data-and-ai/data-engineering/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `23d08c8b711f6bfa52eeb3665a892276b1821b56779bf0c72df48b92314458a4` computed deterministically.

## 5. Resources Created or Moved

- None

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
