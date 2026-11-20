# Data & AI Triage Summary

**Domain:** `library/data-and-ai/`
**Skills triaged:** 127
**Companion file:** `data-ai-triage.csv`

## Verdicts

| Verdict | Count |
|---|---:|
| keep | 37 |
| merge | 38 |
| move | 37 |
| review | 12 |
| rewrite | 2 |
| prune | 1 |
| **total** | **127** |

## Merge clusters (38 skills → 12 canonical)

| Canonical skill | Absorbs | Count |
|---|---|---:|
| `ai-engineering-toolkit` | ai-agent-development, ai-engineer, ai-ml, llm-app-patterns, llm-application-dev-ai-assistant, llm-ops | 7 |
| `hugging-face-cli` | hugging-face-community-evals, hugging-face-dataset-viewer, hugging-face-datasets, hugging-face-evaluation, hugging-face-jobs, huggingface-best | 7 |
| `langgraph` | autonomous-agent-patterns, langchain-architecture, llm-application-dev-langchain-agent, multi-agent-architect | 5 |
| `gemini-api` | gemini-api-dev, gemini-api-integration, gemini-interactions-api, gemini-omni-flash-api | 5 |
| `llms-txt` *(new)* | llms-create, llms-update | 3 |
| `embedding-strategies` | similarity-search-patterns, vector-database-engineer | 3 |
| `hugging-face-gradio` | huggingface-lora-space-builder, huggingface-zerogpu | 3 |
| `segment-cdp` | segment-automation | 2 |
| `data-engineering-data-pipeline` | data-engineer | 2 |
| `mlops-engineer` | ml-pipeline-workflow | 2 |
| `bigquery-analytics` | bigquery-basics | 2 |
| `prompt-engineering-patterns` | llm-application-dev-prompt-optimize | 2 |
| `rag-implementation` | rag-engineer | 2 |
| `hugging-face-papers` | hugging-face-paper-publisher | 2 |
| `huggingface-tool-builder` | hugging-face-tool-builder | 2 |
| `local-llm-expert` | huggingface-local-models | 2 |

**Net reduction from merges:** 38 → 12 = **26 skills removed**

## Moves (37 skills)

| Destination | Count | Skills |
|---|---:|---|
| `development/fullstack` | 6 | comprehensive-review-pr-enhance, dispatch, unslop-commit, unslop-file, vibe-code-cleanup, context-engineering cluster (4) |
| `marketing-and-seo/cro` | 6 | data-and-ai-marketing-psychology, data-and-ai-positioning, developer-sandbox, grand-slam-offers, predictive-personalization, segment-audience |
| `marketing-and-seo/content-and-campaigns` | 6 | community-marketing, content-commerce_02, influencer-tracking, instagram, public-relations, sendgrid-automation |
| `quality-and-security` | 3 | clean-code-guard, code-review-ai-ai-review, vibe-code-auditor |
| `business-and-operations` | 3 | data-and-ai-pricing-strategy, four-core-documents, revenue-recognition-accounting |
| `development/backend` | 2 | convex, file-uploads |
| `infrastructure-and-ops` | 2 | cloudflare, rclone-cli |
| `marketing-and-seo` | 2 | custom-code-management, stp-framework |
| `development/frontend` | 1 | photopea-embedded-editor |
| `workflow-and-automation/tool-integration` | 1 | n8n-agents |
| `content-and-documentation` | 1 | data-storytelling |

**Net reduction from moves:** 37 → 0 = **37 skills leave the domain**

## Prune (1 skill)

- `earllm-build` — one-off Android project skill with no generalizable value.

## Review (12 skills)

These need a human decision before action:

- `data-storytelling` — communication/documentation; move to content?
- `advanced-evaluation` — generic wrapper; overlaps llm-app-patterns?
- `audio-transcriber` — no LLM/RAG dependency; move to marketing?
- `clarity-gate` — RAG quality gate; quality-and-security or data-and-ai?
- `infinite-gratitude` — external pointer; keep or prune?
- `llm-council` — niche evaluation; distinct from advanced-evaluation?
- `mcp-builder` — overlaps mcp-builder-ms in workflow-and-automation?
- `project-development` — generic software development; move to development?
- `quant-analyst` — quant finance; move to business-and-operations?
- `ai-wrapper-product` — overlaps ai-product in development/fullstack?
- `computer-use-agents` — distinct but narrow; verify placement
- `exa-search` — semantic-search API; adjacent to vector-databases?

## Rewrite (2 skills)

- `business-analyst` — generic persona with no procedure; specialise or merge
- `data-scientist` — aspirational generalist with no procedure; specialise or drop

## Projected domain size

| Action | Skills |
|---|---:|
| Start | 127 |
| Merges | −26 |
| Moves | −37 |
| Prunes | −1 |
| **Projected** | **63** |

The 12 review and 2 rewrite skills are not counted — they stay in place pending decisions.

## Key observations

1. **Hugging Face is the biggest cluster** — 18 skills consolidate to 4 canonical (`hugging-face-cli`, `hugging-face-gradio`, `hugging-face-model-trainer`, `hugging-face-papers`). The `huggingface-*` and `hugging-face-*` prefixes are inconsistent; consolidate under the `hugging-face-*` convention.

2. **Gemini is a clean 5→1 merge** — all five skills cover the same API from different angles.

3. **Marketing misfits are the largest move group** — 17 skills in `analytics` and `llm-and-rag` are actually marketing/business skills. The `analytics` subcategory was being used as a catch-all for any data-adjacent work.

4. **Development misfits are the second largest** — 12 skills in `llm-and-rag` are code-quality, PR review, or codebase hygiene skills that belong in `development/` or `quality-and-security/`.

5. **The `context-engineering` merge target already exists** in `development/fullstack/` — the four context/memory skills in `llm-and-rag` and `vector-databases` should move there rather than consolidating in place.

6. **`llms-txt` is a new skill** — `llms-create` and `llms-update` are two halves of the same `llms.txt` standard; they should merge into a single skill.