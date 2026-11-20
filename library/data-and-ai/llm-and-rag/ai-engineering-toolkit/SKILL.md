---
name: "ai-engineering-toolkit"
description: "Production-ready AI engineering workflows and patterns: prompt evaluation (8-dimension scoring), context budget planning, RAG pipeline design, agent security audit (65-point checklist), eval harness building, product sense coaching, agent development lifecycle (design through evaluation), production LLM patterns (ReAct, function calling, plan-and-execute, multi-agent), LLMOps, vector databases, caching, and cost estimation. Use when working with ai engineering toolkit."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# AI Engineering Toolkit

## Overview

A collection of structured, expert-level workflows that turn your AI coding assistant into a senior AI engineering partner. Each skill encodes a repeatable methodology — not just "ask AI to help," but a step-by-step decision framework with quantitative scoring, checklists, and decision trees.

The key difference from ad-hoc AI assistance: **every workflow produces consistent, reproducible results** regardless of who runs it or when. You can use the scoring systems as team baselines and write them into CI/CD pipelines.

## When to Use This Skill

- Evaluating or optimizing LLM system prompts before production deployment
- Designing a RAG pipeline and needing structured architecture decisions (not just boilerplate code)
- Planning token budget allocation across context window zones
- Running pre-launch security audits on AI agents
- Building evaluation frameworks for LLM applications
- Thinking through product strategy before writing code
- Building autonomous agents, multi-agent systems, or agent orchestration
- Implementing production LLM features: streaming, caching, rate limiting, fallback
- Choosing between agent architectures and vector databases

## How It Works

### Skill 1: Prompt Evaluator

Scores prompts across 8 dimensions (Clarity, Specificity, Completeness, Conciseness, Structure, Grounding, Safety, Robustness) on a 1-10 scale with weighted aggregation to a 0-100 score. Identifies the 3 weakest dimensions, generates targeted rewrites, and re-evaluates. Supports single prompt, A/B comparison, and batch evaluation modes.

### Skill 2: Context Budget Planner

Analyzes token distribution across 5 context zones (System, Few-shot, User input, Retrieval, Output) and produces an optimized allocation plan. Includes a compression strategy decision tree for each zone. Common finding: output zone squeezed to under 6% — this skill catches that before truncation happens.

### Skill 3: RAG Pipeline Architect

Walks through a complete architecture decision tree: document format → parsing strategy → chunking approach (fixed/semantic/recursive) → embedding model selection → retrieval method (vector/keyword/hybrid) → evaluation metrics (Faithfulness, Relevancy, Context Precision). Covers Naive RAG, Advanced RAG, and Modular RAG patterns.

### Skill 4: Agent Safety Guard

> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

Executes a 65-point red-team audit across 5 attack categories: direct prompt injection, indirect prompt injection (via RAG documents), information extraction (system prompt / API key leakage), tool abuse (SQL injection, path traversal, command injection), and goal hijacking. The AI constructs adversarial test prompts for evaluation purposes, asks the user for confirmation before each test phase, judges pass/fail, and generates fix recommendations. All tests are contained within the evaluation context and do not interact with external systems. It is recommended to run audits in a sandboxed environment (Docker/VM).

### Skill 5: Eval Harness Builder

Designs evaluation metric systems for LLM applications. Includes LLM-as-Judge scoring framework with bias mitigation strategies (position bias, verbosity bias, self-enhancement bias). Outputs CI/CD-ready evaluation pipeline templates.

### Skill 6: Product Sense Coach

A 5-phase guided conversation framework: dig into motivation → assess market opportunity → find the path → design scenarios → analyze competition. Useful for thinking through "should we build this?" before writing any code.

### Skill 7: Agent Development Lifecycle

Seven phases for building AI agents end-to-end:

1. **Agent Design** — define purpose, capabilities, tool needs, memory system, success metrics.
2. **Single Agent Implementation** — choose framework (LangChain, LlamaIndex, CrewAI), implement logic, add tools, configure memory, test behavior.
3. **Multi-Agent System** — define roles, set up communication, configure orchestration, implement task delegation, test coordination.
4. **Agent Orchestration** — design workflow graph, implement state management, add conditional branches, configure persistence, test workflows (LangGraph).
5. **Tool Integration** — identify needs, design interfaces, implement, add error handling, test usage.
6. **Memory Systems** — short-term, long-term, and entity memory; design retrieval.
7. **Evaluation** — define criteria, create test scenarios, measure performance, test edge cases, iterate.

Agent architecture reference:

```
User Input -> Planner -> Agent -> Tools -> Memory -> Response
              |          |        |        |
         Decompose   LLM Core  Actions  Short/Long-term
```

## AI Engineering Capabilities

Use this section as a capability map when scoping AI work:

- **LLM integration & model management** — OpenAI GPT-4o/4o-mini, o1, Claude 4.5 Sonnet/Haiku, Claude 4.1 Opus; open-source Llama 3.1/3.2, Mixtral, Qwen 2.5, DeepSeek-V2; local serving with Ollama, vLLM, TGI; multi-model routing and cost optimization.
- **Advanced RAG** — multi-stage retrieval, vector DBs (Pinecone, Qdrant, Weaviate, Chroma, Milvus, pgvector), hybrid search (vector + BM25), reranking (Cohere rerank-3, BGE reranker, cross-encoders), query understanding, context compression, GraphRAG, HyDE, RAG-Fusion, self-RAG.
- **Agent frameworks** — LangChain/LangGraph, LlamaIndex, CrewAI, AutoGen, OpenAI Assistants API; short-term/long-term/episodic memory; tool integration; evaluation and monitoring.
- **Vector search & embeddings** — HNSW/IVF/LSH indexing, cosine/dot-product/Euclidean metrics, multi-vector representations, embedding drift detection, index/shard/cache optimization.
- **Prompt engineering** — chain-of-thought, tree-of-thoughts, self-consistency, few-shot optimization, dynamic templates, constitutional AI, prompt versioning and A/B testing, safety prompting, multimodal prompting.
- **Production systems** — FastAPI serving, streaming, semantic caching, response memoization, rate limiting, quotas, circuit breakers, A/B testing, observability (LangSmith, Phoenix, Weights & Biases).
- **Multimodal** — vision (GPT-4V, Claude Vision, LLaVA, CLIP), audio (Whisper, ElevenLabs), document AI (OCR, table extraction, LayoutLM), video analysis, cross-modal embeddings.
- **AI safety & governance** — content moderation, prompt injection detection, PII redaction, bias mitigation, auditing, compliance.
- **Data & API** — PDF extraction, web scraping, Airflow/Dagster/Prefect, Kafka/Pulsar, DVC/lakeFS versioning, REST/GraphQL APIs, webhooks, OAuth/JWT, third-party providers (Azure OpenAI, AWS Bedrock, GCP Vertex AI).

Behavioral traits: prioritize production reliability over proof-of-concept; comprehensive error handling and graceful degradation; cost and latency optimization; observability from day one; structured outputs and type safety; adversarial testing.

## Production Patterns

### RAG Pipeline

```python
# Chunking strategies
class ChunkingStrategy:
    FIXED_SIZE = "fixed_size"        # e.g., 512 tokens
    SEMANTIC = "semantic"            # split on paragraphs/sections
    RECURSIVE = "recursive"          # ["\n\n", "\n", " ", ""]
    DOCUMENT_AWARE = "document_aware"  # headers, lists, structure

CHUNK_CONFIG = {
    "chunk_size": 512,        # tokens
    "chunk_overlap": 50,      # token overlap between chunks
    "separators": ["\n\n", "\n", ". ", " "],
}

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks
```

Hybrid search combines semantic similarity with keyword matching via Reciprocal Rank Fusion:

```python
def hybrid_search(query: str, top_k: int = 5, alpha: float = 0.5):
    """
    alpha=1.0: Pure semantic
    alpha=0.0: Pure keyword (BM25)
    alpha=0.5: Balanced
    """
    semantic_results = vector_db.similarity_search(query)
    keyword_results = bm25_search(query)
    return rrf_merge(semantic_results, keyword_results, alpha)

# Multi-query retrieval: generate variations for better recall
def multi_query_retrieval(query: str):
    queries = llm.generate_query_variations(query, n=3)
    all_results = []
    for q in queries:
        all_results.extend(semantic_search(q))
    return deduplicate(all_results)

# Contextual compression: retrieve then compress to relevant parts
def compressed_retrieval(query: str):
    docs = semantic_search(query, top_k=10)
    return llm.extract_relevant_parts(docs, query)
```

Generation with citations:

```python
RAG_PROMPT_TEMPLATE = """
Answer the user's question based ONLY on the following context.
If the context doesn't contain enough information, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""

def generate_with_rag(question: str):
    context_docs = hybrid_search(question, top_k=5)
    context = "\n\n".join([doc.content for doc in context_docs])
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)
    return {
        "answer": llm.generate(prompt),
        "sources": [doc.metadata for doc in context_docs],
    }
```

### Agent Architectures

**ReAct (Reasoning + Acting)** — interleave thought, action, and observation until a final answer:

```python
REACT_PROMPT = """
You are an AI assistant that can use tools to answer questions.

Available tools:
{tools_description}

Use this format:
Thought: [your reasoning about what to do next]
Action: [tool_name(arguments)]
Observation: [tool result - this will be filled in]
... (repeat Thought/Action/Observation as needed)
Thought: I have enough information to answer
Final Answer: [your final response]

Question: {question}
"""

class ReActAgent:
    def __init__(self, tools: list, llm):
        self.tools = {t.name: t for t in tools}
        self.llm = llm
        self.max_iterations = 10

    def run(self, question: str) -> str:
        prompt = REACT_PROMPT.format(
            tools_description=self._format_tools(), question=question)
        for _ in range(self.max_iterations):
            response = self.llm.generate(prompt)
            if "Final Answer:" in response:
                return self._extract_final_answer(response)
            action = self._parse_action(response)
            observation = self._execute_tool(action)
            prompt += f"\nObservation: {observation}\n"
        return "Max iterations reached"
```

**Function Calling** — define tools as JSON-schema functions and let the model request calls:

```python
TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for current information",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"],
        },
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "Math expression"}},
            "required": ["expression"],
        },
    },
]

class FunctionCallingAgent:
    def run(self, question: str) -> str:
        messages = [{"role": "user", "content": question}]
        while True:
            response = self.llm.chat(messages=messages, tools=TOOLS, tool_choice="auto")
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool(tool_call.name, tool_call.arguments)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })
            else:
                return response.content
```

**Plan-and-Execute** — create a plan, execute each step, replan when needed:

```python
class PlanAndExecuteAgent:
    def run(self, task: str) -> str:
        plan = self.planner.create_plan(task)
        results = []
        for step in plan:
            result = self.executor.execute(step, context=results)
            results.append(result)
            if self._needs_replan(task, results):
                plan = self.planner.replan(
                    task, completed=results, remaining=plan[len(results):])
        return self.synthesizer.summarize(task, results)
```

**Multi-Agent Collaboration** — specialized agents with a coordinator and critic:

```python
class AgentTeam:
    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
            "critic": CriticAgent(),
        }
        self.coordinator = CoordinatorAgent()

    def solve(self, task: str) -> str:
        assignments = self.coordinator.decompose(task)
        results = {}
        for assignment in assignments:
            results[assignment.id] = self.agents[assignment.agent].execute(
                assignment.subtask, context=results)
        critique = self.agents["critic"].review(results)
        if critique.needs_revision:
            return self.solve_with_feedback(task, results, critique)
        return self.coordinator.synthesize(results)
```

### Prompt Patterns

Templates with variable validation, few-shot injection, versioning, and chaining:

```python
class PromptTemplate:
    def __init__(self, template: str, variables: list[str]):
        self.template = template
        self.variables = variables

    def format(self, **kwargs) -> str:
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing variables: {missing}")
        return self.template.format(**kwargs)

    def with_examples(self, examples: list[dict]) -> str:
        example_text = "\n\n".join(
            f"Input: {ex['input']}\nOutput: {ex['output']}" for ex in examples)
        return f"{example_text}\n\n{self.template}"

class PromptRegistry:
    """Version prompts and A/B test by user bucket."""
    def register(self, name: str, template: str, version: str): ...
    def get(self, name: str, version: str = "latest") -> str: ...
    def ab_test(self, name: str, user_id: str) -> str:
        variants = self.db.get_all_versions(name)
        return variants[hash(user_id) % len(variants)]
    def record_outcome(self, prompt_id: str, outcome: dict): ...

class PromptChain:
    """Chain prompts, passing each output as the next input."""
    def run(self, initial_input: str) -> dict:
        context = {"input": initial_input}
        for step in self.steps:
            context[step["output_key"]] = llm.generate(
                step["prompt"].format(**context))
        return {"final_output": context[self.steps[-1]["output_key"]]}
```

### LLMOps & Observability

Metrics to track:

| Category | Metrics |
|---|---|
| Performance | latency_p50, latency_p99, tokens_per_second |
| Quality | user_satisfaction, task_completion, hallucination_rate |
| Cost | cost_per_request, tokens_per_request, cache_hit_rate |
| Reliability | error_rate, timeout_rate, retry_rate |

```python
class LLMLogger:
    def log_request(self, request_id: str, data: dict):
        logging.info(f"LLM_REQUEST: {json.dumps({
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "model": data["model"],
            "prompt": data["prompt"][:500],
            "prompt_tokens": data["prompt_tokens"],
            "temperature": data.get("temperature", 1.0),
            "user_id": data.get("user_id"),
        })}")

    def log_response(self, request_id: str, data: dict):
        logging.info(f"LLM_RESPONSE: {json.dumps({
            "request_id": request_id,
            "completion_tokens": data["completion_tokens"],
            "total_tokens": data["total_tokens"],
            "latency_ms": data["latency_ms"],
            "finish_reason": data["finish_reason"],
            "cost_usd": self._calculate_cost(data),
        })}")

@tracer.start_as_current_span("llm_call")
def call_llm(prompt: str) -> str:
    span = trace.get_current_span()
    span.set_attribute("prompt.length", len(prompt))
    response = llm.generate(prompt)
    span.set_attribute("response.length", len(response))
    span.set_attribute("tokens.total", response.usage.total_tokens)
    return response.content
```

Evaluation: score relevance, coherence, groundedness, accuracy, and safety; run benchmarks over a test set and aggregate scores. Use LLM-as-Judge with bias mitigation (position, verbosity, self-enhancement bias).

### Production Patterns

```python
class LLMCache:
    """Deterministic cache keyed by model + prompt + params."""
    def _cache_key(self, prompt: str, model: str, **kwargs) -> str:
        content = f"{model}:{prompt}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get_or_generate(self, prompt: str, model: str, **kwargs) -> str:
        key = self._cache_key(prompt, model, **kwargs)
        cached = self.redis.get(key)
        if cached:
            return cached.decode()
        response = llm.generate(prompt, model=model, **kwargs)
        if kwargs.get("temperature", 1.0) == 0:
            self.redis.setex(key, self.ttl, response)
        return response

class RateLimiter:
    """Wait if the requests-per-minute limit would be exceeded."""
    def acquire(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < 60]
        if len(self.timestamps) >= self.rpm:
            time.sleep(60 - (now - self.timestamps[0]))
        self.timestamps.append(time.time())

@retry(wait=wait_exponential(multiplier=1, min=4, max=60),
       stop=stop_after_attempt(5))
def call_llm_with_retry(prompt: str) -> str:
    # Retry RateLimitError and 5xx; do not retry 4xx client errors
    return llm.generate(prompt)

class LLMWithFallback:
    def __init__(self, primary: str, fallbacks: list[str]):
        self.models = [primary] + fallbacks

    def generate(self, prompt: str, **kwargs) -> str:
        for model in self.models:
            try:
                return llm.generate(prompt, model=model, **kwargs)
            except (RateLimitError, APIError) as e:
                logging.warning(f"Model {model} failed: {e}")
        raise AllModelsFailedError("All models exhausted")
```

## RAG & Vector Database Reference

### Vector DB Selection

| DB | Best For | Hosting | Cost |
|---|---|---|---|
| Chroma | Development, local | Self-hosted | Free |
| pgvector | Already using PostgreSQL | Self/Cloud | Free |
| Pinecone | Managed production | Cloud | $70+/mo |
| Weaviate | Multi-modal, GraphQL | Self/Cloud | Free+ |
| Qdrant | High performance | Self/Cloud | Free+ |

Production feature comparison:

| DB | Scale | Features |
|---|---|---|
| Pinecone | Billions of vectors | Hybrid search, metadata filtering |
| Weaviate | Millions | GraphQL API, modules |
| ChromaDB | Thousands | Simple API, in-memory option |
| pgvector | Millions | SQL integration, ACID |

### Embedding Models

| Model | Dimensions | Cost | Quality |
|---|---|---|---|
| OpenAI text-embedding-3-small | 1536 | $0.02/1M tokens | Good for most use cases |
| OpenAI text-embedding-3-large | 3072 | $0.13/1M tokens | Best for complex queries |
| Local bge-large | 1024 | Free (compute only) | Comparable to OpenAI small |

### pgvector Setup

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE knowledge_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX ON knowledge_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

SELECT content, 1 - (embedding <=> :query_vector) AS similarity
FROM knowledge_embeddings ORDER BY similarity DESC LIMIT 5;
```

### Semantic Cache

Cache responses by embedding similarity (>= 0.95 cosine) instead of exact prompt match, to catch paraphrased queries.

## Prompt Engineering Reference

System prompt anatomy (identity → rules → capabilities → limitations → personalization):

- **Identity**: name, tone, platform
- **Rules**: max length, formatting, conversational constraints
- **Capabilities**: what the assistant can do
- **Limitations**: explicit boundaries (no real-time internet, no financial transactions)
- **Personalization**: `{user_name}`, `{user_preferences}`, `{relevant_history}`

Chain-of-thought scaffolding for structured reasoning:

```python
def cot_analysis(problem: str) -> str:
    steps = [
        "1. What exactly is being asked?",
        "2. What information is critical to solve it?",
        "3. What approaches are possible?",
        "4. Which approach is best and why?",
        "5. What risks or limitations exist?",
    ]
    prompt = f"Analyze step by step:\n\nPROBLEM: {problem}\n\n" + "\n".join(steps)
    return call_llm(prompt)
```

## Cost Estimation

```python
PRICING = {
    "llm-frontier-opus":   {"input": 15.00, "output": 75.00},
    "llm-frontier-sonnet": {"input": 3.00,  "output": 15.00},
    "llm-frontier-haiku":  {"input": 0.80,  "output": 4.00},
}

def estimate_monthly_cost(model, avg_input, avg_output, req_per_day):
    p = PRICING[model]
    daily = (avg_input + avg_output) * req_per_day / 1e6
    monthly = daily * p["input"] * 30
    return {"model": model, "monthly_cost": f"USD {monthly:.2f}"}
```

## Architecture Decision Matrix

| Pattern | Use When | Complexity | Cost |
|---|---|---|---|
| Simple RAG | FAQ, docs search | Low | Low |
| Hybrid RAG | Mixed queries | Medium | Medium |
| ReAct Agent | Multi-step tasks | Medium | Medium |
| Function Calling | Structured tools | Low | Low |
| Plan-Execute | Complex tasks | High | High |
| Multi-Agent | Research tasks | Very High | Very High |

## Checklists

### LLM Integration
- [ ] API keys secured
- [ ] Rate limiting configured
- [ ] Error handling implemented
- [ ] Streaming enabled
- [ ] Token usage tracked

### RAG System
- [ ] Data pipeline working
- [ ] Embeddings generated
- [ ] Vector search optimized
- [ ] Retrieval accuracy tested
- [ ] Caching implemented

### AI Agents
- [ ] Agent roles defined
- [ ] Tools integrated
- [ ] Memory working
- [ ] Orchestration tested
- [ ] Error handling robust

### Observability
- [ ] Tracing enabled
- [ ] Metrics collected
- [ ] Evaluation running
- [ ] Alerts configured
- [ ] Dashboards created

## Examples

### Example 1: Prompt Evaluation

Ask: "Evaluate this system prompt"

```
You are a customer support agent. Help users with their questions. Be nice and helpful.
```

Result: Overall score **28/100**. Weakest dimensions: Safety (1/10, zero injection protection), Specificity (2/10, no output format), Structure (2/10, no sections). Auto-rewrite scores **82/100** with added scope boundaries, response format, escalation rules, and safety guardrails.

### Example 2: Security Audit

Ask: "Run a security audit on my customer support agent"

Result: 65 tests executed. 3 critical failures found: Base64-encoded instruction bypass, path traversal via tool calls, system prompt extraction via role-play. Fix recommendations provided for each.

### Example 3: Build a RAG Assistant

Ask: "Build a RAG assistant over our internal docs"

Workflow: RAG Pipeline Architect → chunking strategy → embedding model → hybrid retrieval → reranking → RAG prompt with citations → context budget → eval harness.

## Best Practices

- ✅ Run prompt-evaluator before any production deployment — set a team baseline (e.g., ≥70/100)
- ✅ Use context-budget-planner early in development, not after hitting truncation issues
- ✅ Run agent-safety-guard as a pre-launch gate, not post-incident
- ✅ Combine skills in sequence: RAG design → context optimization → prompt polish → security audit → eval setup
- ✅ Prefer structured outputs and type safety wherever the API supports them
- ✅ Track cost per request and cache hit rate from day one
- ❌ Don't rely on a single dimension score — look at the full profile
- ❌ Don't skip the security audit because "it's just an internal tool"
- ❌ Don't cache non-deterministic outputs (temperature > 0)

## Security & Safety Notes

- All skills are read-only analysis and advisory workflows. No skills modify files or make network requests.
- The agent-safety-guard skill constructs adversarial test prompts for evaluation purposes only — these are contained within the evaluation context and do not interact with external systems.
- **agent-safety-guard is classified as an offensive skill**: it generates attack payloads (prompt injection, SQL injection, command injection) for authorized security testing. The skill requires explicit user confirmation before executing each test phase. Run in a sandboxed environment when possible.
- No weaponized payloads are included. All adversarial prompts are educational in nature.
- Avoid sending sensitive data to external models without approval. Add guardrails for prompt injection, PII, and policy compliance.

## Installation

```bash
# Via skill install command (the agent / WorkBuddy / Cursor)
/skill install -g viliawang-pm/ai-engineering-toolkit

# Manual
git clone https://github.com/viliawang-pm/ai-engineering-toolkit.git
cp -r ai-engineering-toolkit/skills/* ~/.agents/skills/
```

**Repository**: [github.com/viliawang-pm/ai-engineering-toolkit](https://github.com/viliawang-pm/ai-engineering-toolkit)
**License**: MIT

## Merged from

- `ai-agent-development` — agent development lifecycle workflow
- `ai-engineer` — AI engineering capability map and behavioral traits
- `ai-ml` — workflow bundle and checklists
- `llm-app-patterns` — production code patterns (RAG, agents, prompts, LLMOps, caching)
- `llm-application-dev-ai-assistant` — AI assistant development scope
- `llm-ops` — RAG architecture, vector DB selection, pgvector, semantic cache, cost estimation, eval framework

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.