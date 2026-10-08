# Phase 08 Batch Audit Record: `batch-18-data-and-ai-llm-and-rag-part02`

## 1. Batch Metadata & Universe Accounting

- **Batch ID**: `batch-18-data-and-ai-llm-and-rag-part02`
- **Category / Subcategory**: `data-and-ai` / `llm-and-rag`
- **Member Skill Count**: 13
- **Batch Status**: `completed`
- **Validation Status**: `verified`
- **Deterministic Manifest Hash (SHA-256)**: `a2632f40f6d75607e5362d3647b74811e9fcad953d35e1b307143d5f5e982474`

## 2. Canonical Skills Summary & Provenance

| Skill Name | Origin Path | Workflow | Upstream Provenance | License | Risk |
|---|---|---|---|---|---|
| `context-window-management` | `task-folder/agents/skills/context/context-window-management` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `conversation-memory` | `task-folder/agents/skills/conversation-memory` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `convex` | `task-folder/agents/skills/convex` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `earllm-build` | `task-folder/agents/skills/earllm-build` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `file-uploads` | `task-folder/agents/skills/files/file-uploads` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `grand-slam-offers` | `task-folder/agents/skills/strategy/grand-slam-offers` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `hugging-face-community-evals` | `task-folder/agents/skills/hugging face/hugging-face-community-evals` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `hugging-face-datasets` | `task-folder/agents/skills/hugging face/hugging-face-datasets` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `hugging-face-evaluation` | `task-folder/agents/skills/hugging face/hugging-face-evaluation` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `infinite-gratitude` | `task-folder/agents/skills/infinite-gratitude` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `langchain-architecture` | `task-folder/agents/skills/langchain-architecture` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `langgraph` | `task-folder/agents/skills/langgraph` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |
| `llm-app-patterns` | `task-folder/agents/skills/llm/llm/llm-app-patterns` | `skill-improver` | Community / Canonical | `not_declared_upstream` | `unknown` |

## 3. Trigger Boundary Evaluation Evidence

| Skill Name | Should Trigger | Should Not Trigger | Ambiguous Neighbor Query |
|---|---|---|---|
| `context-window-management` | User asks to implement, configure, or optimize context window management tasks (specifically configuring or implementing context window management specifications). | User requests general infrastructure administration, styling, or unrelated operations outside context window management or unrelated operations outside context window management. | User asks 'How do I handle context window management in my workflow?' -> Disambiguate: Clarify whether the task requires specialized context window management procedures or general llm-and-rag tooling. |
| `conversation-memory` | User asks to implement, configure, or optimize conversation memory tasks (specifically configuring or implementing conversation memory specifications). | User requests general infrastructure administration, styling, or unrelated operations outside conversation memory or unrelated operations outside conversation memory. | User asks 'How do I handle conversation memory in my workflow?' -> Disambiguate: Clarify whether the task requires specialized conversation memory procedures or general llm-and-rag tooling. |
| `convex` | User asks to implement, configure, or optimize convex tasks (specifically configuring or implementing convex specifications). | User requests general infrastructure administration, styling, or unrelated operations outside convex or unrelated operations outside convex. | User asks 'How do I handle convex in my workflow?' -> Disambiguate: Clarify whether the task requires specialized convex procedures or general llm-and-rag tooling. |
| `earllm-build` | User asks to implement, configure, or optimize earllm build tasks (specifically configuring or implementing earllm build specifications). | User requests A simpler, more specific tool can handle the request or unrelated operations outside earllm build. | User asks 'How do I handle earllm build in my workflow?' -> Disambiguate: Clarify whether the task requires specialized earllm build procedures or general llm-and-rag tooling. |
| `file-uploads` | User asks to implement, configure, or optimize file uploads tasks (specifically Role**: File Upload Specialist). | User requests general infrastructure administration, styling, or unrelated operations outside file uploads or unrelated operations outside file uploads. | User asks 'How do I handle file uploads in my workflow?' -> Disambiguate: Clarify whether the task requires specialized file uploads procedures or general llm-and-rag tooling. |
| `grand-slam-offers` | User asks to implement, configure, or optimize grand slam offers tasks (specifically configuring or implementing grand slam offers specifications). | User requests general infrastructure administration, styling, or unrelated operations outside grand slam offers or unrelated operations outside grand slam offers. | User asks 'How do I handle grand slam offers in my workflow?' -> Disambiguate: Clarify whether the task requires specialized grand slam offers procedures or general llm-and-rag tooling. |
| `hugging-face-community-evals` | User asks to implement, configure, or optimize hugging face community evals tasks (specifically configuring or implementing hugging face community evals specifications). | User requests general infrastructure administration, styling, or unrelated operations outside hugging face community evals or unrelated operations outside hugging face community evals. | User asks 'How do I handle hugging face community evals in my workflow?' -> Disambiguate: Clarify whether the task requires specialized hugging face community evals procedures or general llm-and-rag tooling. |
| `hugging-face-datasets` | User asks to implement, configure, or optimize hugging face datasets tasks (specifically configuring or implementing hugging face datasets specifications). | User requests general infrastructure administration, styling, or unrelated operations outside hugging face datasets or unrelated operations outside hugging face datasets. | User asks 'How do I handle hugging face datasets in my workflow?' -> Disambiguate: Clarify whether the task requires specialized hugging face datasets procedures or general llm-and-rag tooling. |
| `hugging-face-evaluation` | User asks to implement, configure, or optimize hugging face evaluation tasks (specifically Extracting existing evaluation tables from README content). | User requests general infrastructure administration, styling, or unrelated operations outside hugging face evaluation or unrelated operations outside hugging face evaluation. | User asks 'How do I handle hugging face evaluation in my workflow?' -> Disambiguate: Clarify whether the task requires specialized hugging face evaluation procedures or general llm-and-rag tooling. |
| `infinite-gratitude` | User asks to implement, configure, or optimize infinite gratitude tasks (specifically configuring or implementing infinite gratitude specifications). | User requests general infrastructure administration, styling, or unrelated operations outside infinite gratitude or unrelated operations outside infinite gratitude. | User asks 'How do I handle infinite gratitude in my workflow?' -> Disambiguate: Clarify whether the task requires specialized infinite gratitude procedures or general llm-and-rag tooling. |
| `langchain-architecture` | User asks to implement, configure, or optimize langchain architecture tasks (specifically configuring or implementing langchain architecture specifications). | User requests You need a different domain or tool outside this scope or unrelated operations outside langchain architecture. | User asks 'How do I handle langchain architecture in my workflow?' -> Disambiguate: Clarify whether the task requires specialized langchain architecture procedures or general llm-and-rag tooling. |
| `langgraph` | User asks to implement, configure, or optimize langgraph tasks (specifically Role**: LangGraph Agent Architect). | User requests general infrastructure administration, styling, or unrelated operations outside langgraph or unrelated operations outside langgraph. | User asks 'How do I handle langgraph in my workflow?' -> Disambiguate: Clarify whether the task requires specialized langgraph procedures or general llm-and-rag tooling. |
| `llm-app-patterns` | User asks to implement, configure, or optimize llm app patterns tasks (specifically configuring or implementing llm app patterns specifications). | User requests general infrastructure administration, styling, or unrelated operations outside llm app patterns or unrelated operations outside llm app patterns. | User asks 'How do I handle llm app patterns in my workflow?' -> Disambiguate: Clarify whether the task requires specialized llm app patterns procedures or general llm-and-rag tooling. |

## 4. Verification & Consistency Sign-off

- [x] 100% of member packages verified on disk under `task-folder/agents/skills-rebuild/data-and-ai/llm-and-rag/`
- [x] Frontmatter validated with machine-verifiable `<what>. Use when <trigger>` pattern.
- [x] Substantive capability-specific trigger boundary evaluation confirmed.
- [x] Manifest hash `a2632f40f6d75607e5362d3647b74811e9fcad953d35e1b307143d5f5e982474` computed deterministically.

## 5. Resources Created or Moved

| Skill | Resource | Disposition |
|---|---|---|
| `hugging-face-community-evals` | `examples/.env.example` | Created or preserved in canonical package |
| `hugging-face-community-evals` | `examples/USAGE_EXAMPLES.md` | Created or preserved in canonical package |
| `hugging-face-community-evals` | `scripts/inspect_eval_uv.py` | Created or preserved in canonical package |
| `hugging-face-community-evals` | `scripts/inspect_vllm_uv.py` | Created or preserved in canonical package |
| `hugging-face-community-evals` | `scripts/lighteval_vllm_uv.py` | Created or preserved in canonical package |

## 6. Retired Paths

- None

## 7. Unresolved Items

- None
