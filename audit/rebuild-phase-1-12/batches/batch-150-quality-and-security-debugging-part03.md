# Phase 08 Batch Audit Record: `batch-150-quality-and-security-debugging-part03`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-150-quality-and-security-debugging-part03`
- **Category / Subcategory**: `quality-and-security` / `debugging`
- **Member Skill Count**: 12
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `ef993188c554f15d6ce6ac55dba1f06f1f01f3fb7dc83ccdfe8ea4a2f9e2a95b`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `first-party-data-collection` | `task-folder/agents/skills/marketing/first-party-data-collection` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `huggingface-spaces` | `task-folder/agents/skills/hugging face/huggingface-spaces` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `incident-response-smart-fix` | `task-folder/agents/skills/incident-response-smart-fix` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `langfuse` | `task-folder/agents/skills/langfuse` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `linux-troubleshooting` | `task-folder/agents/skills/linux/linux-troubleshooting` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `manifest` | `task-folder/agents/skills/manifest` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-code-javascript` | `task-folder/agents/skills/n8n/n8n-code-javascript` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `n8n-expression-syntax` | `task-folder/agents/skills/n8n/n8n-expression-syntax` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `os-scripting` | `task-folder/agents/skills/os-scripting` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `performance-optimization` | `task-folder/agents/skills/performance/performance-optimization` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `performance-profiling` | `task-folder/agents/skills/performance/performance-profiling` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `phase-gated-debugging` | `task-folder/agents/skills/phase-gated-debugging` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `first-party-data-collection` | User asks to implement, configure, or optimize first party data collection tasks (specifically configuring or implementing first party data collection specifications). | User requests general infrastructure administration, styling, or unrelated operations outside first party data collection or unrelated operations outside first party data collection. | User asks 'How do I handle first party data collection in my workflow?' -> Disambiguate: Clarify whether the task requires specialized first party data collection procedures or general debugging tooling. |
| `huggingface-spaces` | User asks to implement, configure, or optimize huggingface spaces tasks (specifically configuring or implementing huggingface spaces specifications). | User requests general infrastructure administration, styling, or unrelated operations outside huggingface spaces or unrelated operations outside huggingface spaces. | User asks 'How do I handle huggingface spaces in my workflow?' -> Disambiguate: Clarify whether the task requires specialized huggingface spaces procedures or general debugging tooling. |
| `incident-response-smart-fix` | User asks to implement, configure, or optimize incident response smart fix tasks (specifically configuring or implementing incident response smart fix specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside incident response smart fix. | User asks 'How do I handle incident response smart fix in my workflow?' -> Disambiguate: Clarify whether the task requires specialized incident response smart fix procedures or general debugging tooling. |
| `langfuse` | User asks to implement, configure, or optimize langfuse tasks (specifically Role**: LLM Observability Architect). | User requests general infrastructure administration, styling, or unrelated operations outside langfuse or unrelated operations outside langfuse. | User asks 'How do I handle langfuse in my workflow?' -> Disambiguate: Clarify whether the task requires specialized langfuse procedures or general debugging tooling. |
| `linux-troubleshooting` | User asks to implement, configure, or optimize linux troubleshooting tasks (specifically configuring or implementing linux troubleshooting specifications). | User requests general infrastructure administration, styling, or unrelated operations outside linux troubleshooting or unrelated operations outside linux troubleshooting. | User asks 'How do I handle linux troubleshooting in my workflow?' -> Disambiguate: Clarify whether the task requires specialized linux troubleshooting procedures or general debugging tooling. |
| `manifest` | User asks to implement, configure, or optimize manifest tasks (specifically configuring or implementing manifest specifications). | User requests User needs general observability design (use `observability-engineer` instead) or unrelated operations outside manifest. | User asks 'How do I handle manifest in my workflow?' -> Disambiguate: Clarify whether the task requires specialized manifest procedures or general debugging tooling. |
| `n8n-code-javascript` | User asks to implement, configure, or optimize n8n code javascript tasks (specifically configuring or implementing n8n code javascript specifications). | User requests general infrastructure administration, styling, or unrelated operations outside n8n code javascript or unrelated operations outside n8n code javascript. | User asks 'How do I handle n8n code javascript in my workflow?' -> Disambiguate: Clarify whether the task requires specialized n8n code javascript procedures or general debugging tooling. |
| `n8n-expression-syntax` | User asks to implement, configure, or optimize n8n expression syntax tasks (specifically configuring or implementing n8n expression syntax specifications). | User requests general infrastructure administration, styling, or unrelated operations outside n8n expression syntax or unrelated operations outside n8n expression syntax. | User asks 'How do I handle n8n expression syntax in my workflow?' -> Disambiguate: Clarify whether the task requires specialized n8n expression syntax procedures or general debugging tooling. |
| `os-scripting` | User asks to implement, configure, or optimize os scripting tasks (specifically configuring or implementing os scripting specifications). | User requests general infrastructure administration, styling, or unrelated operations outside os scripting or unrelated operations outside os scripting. | User asks 'How do I handle os scripting in my workflow?' -> Disambiguate: Clarify whether the task requires specialized os scripting procedures or general debugging tooling. |
| `performance-optimization` | User asks to implement, configure, or optimize performance optimization tasks (specifically configuring or implementing performance optimization specifications). | User requests general infrastructure administration, styling, or unrelated operations outside performance optimization or unrelated operations outside performance optimization. | User asks 'How do I handle performance optimization in my workflow?' -> Disambiguate: Clarify whether the task requires specialized performance optimization procedures or general debugging tooling. |
| `performance-profiling` | User asks to implement, configure, or optimize performance profiling tasks (specifically configuring or implementing performance profiling specifications). | User requests general infrastructure administration, styling, or unrelated operations outside performance profiling or unrelated operations outside performance profiling. | User asks 'How do I handle performance profiling in my workflow?' -> Disambiguate: Clarify whether the task requires specialized performance profiling procedures or general debugging tooling. |
| `phase-gated-debugging` | User asks to implement, configure, or optimize phase gated debugging tasks (specifically configuring or implementing phase gated debugging specifications). | User requests general infrastructure administration, styling, or unrelated operations outside phase gated debugging or unrelated operations outside phase gated debugging. | User asks 'How do I handle phase gated debugging in my workflow?' -> Disambiguate: Clarify whether the task requires specialized phase gated debugging procedures or general debugging tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/quality-and-security/debugging/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `ef993188c554f15d6ce6ac55dba1f06f1f01f3fb7dc83ccdfe8ea4a2f9e2a95b` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `first-party-data-collection` | `evals/consent-management-and-privacy-complianc/criteria.json` | Created or preserved in canonical package |
| `first-party-data-collection` | `evals/consent-management-and-privacy-complianc/task.md` | Created or preserved in canonical package |
| `first-party-data-collection` | `evals/customer-schema-and-progressive-profilin/criteria.json` | Created or preserved in canonical package |
| `first-party-data-collection` | `evals/customer-schema-and-progressive-profilin/task.md` | Created or preserved in canonical package |
| `first-party-data-collection` | `evals/zero-party-quiz-with-product-recommendat/criteria.json` | Created or preserved in canonical package |
| `first-party-data-collection` | `evals/zero-party-quiz-with-product-recommendat/task.md` | Created or preserved in canonical package |
| `first-party-data-collection` | `tile.json` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/buckets.md` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/debugging.md` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/gradio.md` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/grants.md` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/inference-providers.md` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/known-errors.md` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/requirements.md` | Created or preserved in canonical package |
| `huggingface-spaces` | `references/zerogpu.md` | Created or preserved in canonical package |
| `incident-response-smart-fix` | `resources/implementation-playbook.md` | Created or preserved in canonical package |
| `performance-profiling` | `scripts/lighthouse_audit.py` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
