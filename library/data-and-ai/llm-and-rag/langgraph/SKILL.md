---
name: "langgraph"
description: "Production-grade framework and patterns for building stateful, multi-actor AI applications. Covers LangGraph graph construction (StateGraph), state management with reducers, conditional routing, checkpointers and persistence, human-in-the-loop, parallel execution; LangChain agents/chains/memory/callbacks; multi-agent architecture (supervisor, planner, researcher, coder, validator) with DeepAgents; autonomous coding agent patterns (agent loop, tool design, permissions, sandboxing, browser automation, context management, MCP); and production deployment (Claude Sonnet 4.5, Voyage embeddings, FastAPI streaming, LangSmith). Use when working with langgraph."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# LangGraph & Agent Architectures

Expert in LangGraph - the production-grade framework for building stateful, multi-actor AI applications. Covers graph construction, state management, cycles and branches, persistence with checkpointers, human-in-the-loop patterns, and the ReAct agent pattern. Used in production at LinkedIn, Uber, and 400+ companies. This is LangChain's recommended approach for building agents.

**Role**: LangGraph Agent Architect

You are an expert in building production-grade AI agents with LangGraph. You understand that agents need explicit structure - graphs make the flow visible and debuggable. You design state carefully, use reducers appropriately, and always consider persistence for production. You know when cycles are needed and how to prevent infinite loops.

### Expertise

- Graph topology design
- State schema patterns
- Conditional branching
- Persistence strategies
- Human-in-the-loop
- Tool integration
- Error handling and recovery

## Capabilities

- Graph construction (StateGraph)
- State management and reducers
- Node and edge definitions
- Conditional routing
- Checkpointers and persistence
- Human-in-the-loop patterns
- Tool integration
- Streaming and async execution

## Prerequisites

- Python 3.9+, `langgraph` package, LLM API access (OpenAI, Anthropic, etc.)
- Async programming concepts and graph theory fundamentals

## Scope

- Python-only (TypeScript in early stages)
- Learning curve for graph concepts; state management complexity; debugging can be challenging

## Ecosystem

- **Primary**: LangGraph, LangChain, LangSmith (observability)
- **Integrations**: OpenAI / Anthropic / Google, Tavily (search), SQLite / PostgreSQL (persistence), Redis (state store)
- **Platforms**: Python applications, FastAPI / Flask backends, cloud deployments

## When to Use

- User mentions or implies: langgraph, langchain agent, stateful agent, agent graph, react agent, agent workflow, multi-step agent
- Building autonomous AI agents with tool access
- Implementing complex multi-step LLM workflows
- Managing conversation memory and state
- Integrating LLMs with external data sources and APIs
- Creating modular, reusable LLM application components
- Implementing document processing pipelines
- Architecting supervisor, planner, research, coding, or validation agent roles
- Debugging or optimizing an existing LangChain/LangGraph agent system

## LangGraph Patterns

### Basic Agent Graph

Simple ReAct-style agent with tools. **When to use**: single agent with tool calling.

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    # add_messages reducer appends, doesn't overwrite

# 2. Define Tools
@tool
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(safe_math_evaluator(expression))

tools = [search, calculator]

# 3. Create LLM with tools
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# 4. Define Nodes
def agent(state: AgentState) -> dict:
    """The agent node - calls LLM."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Tool node handles tool execution
tool_node = ToolNode(tools)

# 5. Define Routing
def should_continue(state: AgentState) -> str:
    """Route based on whether tools were called."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 6. Build Graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools", "agent")  # Loop back

app = graph.compile()

# 7. Run
result = app.invoke({"messages": [("user", "What is 25 * 4?")]})
```

### State with Reducers

Complex state management with custom reducers. **When to use**: multiple agents updating shared state.

```python
from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph

# Custom reducer for merging dictionaries
def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}

class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]        # append, don't overwrite
    findings: Annotated[dict, merge_dicts]          # merge
    sources: Annotated[list[str], add]             # accumulate
    current_step: str                               # overwrites (no reducer)
    errors: Annotated[int, lambda a, b: a + b]     # custom reducer

def researcher(state: ResearchState) -> dict:
    # Only return fields being updated
    return {"findings": {"topic_a": "New finding"},
            "sources": ["source1.com"],
            "current_step": "researching"}

def writer(state: ResearchState) -> dict:
    # Access accumulated state
    return {"messages": [("assistant", f"Report based on {len(state['sources'])} sources")],
            "current_step": "writing"}
```

### Conditional Branching

Route to different paths based on state. **When to use**: multiple possible workflows.

```python
from langgraph.graph import StateGraph, START, END

class RouterState(TypedDict):
    query: str
    query_type: str
    result: str

def classifier(state: RouterState) -> dict:
    query = state["query"].lower()
    if "code" in query or "program" in query:
        return {"query_type": "coding"}
    elif "search" in query or "find" in query:
        return {"query_type": "search"}
    else:
        return {"query_type": "chat"}

def route_query(state: RouterState) -> str:
    return state["query_type"]  # Returns node name

graph = StateGraph(RouterState)
graph.add_node("classifier", classifier)
graph.add_node("coding", coding_agent)
graph.add_node("search", search_agent)
graph.add_node("chat", chat_agent)
graph.add_edge(START, "classifier")
graph.add_conditional_edges("classifier", route_query,
    {"coding": "coding", "search": "search", "chat": "chat"})
for node in ("coding", "search", "chat"):
    graph.add_edge(node, END)

app = graph.compile()
```

### Persistence with Checkpointer

Save and resume agent state. **When to use**: multi-turn conversations, long-running agents.

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# SQLite for development (or a file for persistence)
memory = SqliteSaver.from_conn_string("agent_state.db")
# PostgreSQL for production: PostgresSaver.from_conn_string(DATABASE_URL)

app = graph.compile(checkpointer=memory)

# Run with thread_id for conversation continuity
config = {"configurable": {"thread_id": "user-123-session-1"}}
result1 = app.invoke({"messages": [("user", "My name is Alice")]}, config=config)
result2 = app.invoke({"messages": [("user", "What's my name?")]}, config=config)
# Agent knows name is Alice!

# Conversation history / checkpoint history
state = app.get_state(config)
print(state.values["messages"])
for checkpoint in app.get_state_history(config):
    print(checkpoint.config, checkpoint.values)
```

### Human-in-the-Loop

Pause for human approval before actions. **When to use**: sensitive operations, review before execution.

```python
class ApprovalState(TypedDict):
    messages: Annotated[list, add_messages]
    pending_action: dict | None
    approved: bool

def agent(state: ApprovalState) -> dict:
    action = {"type": "send_email", "to": "user@example.com"}
    return {"pending_action": action,
            "messages": [("assistant", f"I want to: {action}")]}

def execute_action(state: ApprovalState) -> dict:
    action = state["pending_action"]
    return {"messages": [("assistant", f"Executed: {action['type']}")],
            "pending_action": None}

def should_execute(state: ApprovalState) -> str:
    return "execute" if state.get("approved") else END  # Wait for approval

graph = StateGraph(ApprovalState)
graph.add_node("agent", agent)
graph.add_node("execute", execute_action)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_execute, ["execute", END])
graph.add_edge("execute", END)

# Compile with interrupt_before for human review
app = graph.compile(checkpointer=memory, interrupt_before=["execute"])

config = {"configurable": {"thread_id": "approval-flow"}}
result = app.invoke({"messages": [("user", "Send report")]}, config)

# Agent paused - human reviews pending state
state = app.get_state(config)
print(f"Pending: {state.values['pending_action']}")

# Human approves - update state and continue
app.update_state(config, {"approved": True})
result = app.invoke(None, config)  # Resume
```

### Parallel Execution (Map-Reduce)

Run multiple branches in parallel. **When to use**: parallel research, batch processing.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send

class ParallelState(TypedDict):
    topics: list[str]
    results: Annotated[list[str], add]
    summary: str

def research_topic(state: dict) -> dict:
    return {"results": [f"Research on {state['topic']}..."]}

def summarize(state: ParallelState) -> dict:
    return {"summary": f"Summary of {len(state['results'])} topics"}

def fanout_topics(state: ParallelState) -> list[Send]:
    return [Send("research", {"topic": topic}) for topic in state["topics"]]

graph = StateGraph(ParallelState)
graph.add_node("research", research_topic)
graph.add_node("summarize", summarize)
graph.add_conditional_edges(START, fanout_topics, ["research"])
graph.add_edge("research", "summarize")
graph.add_edge("summarize", END)

app = graph.compile()
result = app.invoke({"topics": ["AI", "Climate", "Space"], "results": []})
```

## LangChain Foundations

### Core Concepts

**Agents** — autonomous systems that use LLMs to decide which actions to take. Types: **ReAct** (reasoning + acting interleaved), **OpenAI Functions** (function calling API), **Structured Chat** (multi-input tools), **Conversational** (chat interfaces), **Self-Ask with Search** (decomposes complex queries).

**Chains** — sequences of calls to LLMs or utilities. Types: **LLMChain** (prompt + LLM), **SequentialChain**, **RouterChain**, **TransformChain**, **MapReduceChain**.

**Memory** — maintaining context across interactions. Types: **ConversationBufferMemory** (all messages), **ConversationSummaryMemory** (summarizes old messages), **ConversationBufferWindowMemory** (last N messages), **EntityMemory** (tracks entities), **VectorStoreMemory** (semantic retrieval).

**Document processing** — Document Loaders, Text Splitters, Vector Stores, Retrievers, Indexes.

**Callbacks** — hooks for logging, monitoring, debugging; token usage, latency, error handling, custom metrics.

### Quick Start

```python
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools, llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory, verbose=True,
)

result = agent.run("What's the weather in SF? Then calculate 25 * 4")
```

### RAG with LangChain

```python
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

loader = TextLoader('documents.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(texts, OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
)
result = qa_chain({"query": "What is the main topic?"})
```

Production RAG with Claude + Voyage (Anthropic's recommended embeddings):

```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Primary LLM: Claude Sonnet 4.5 (claude-sonnet-4-5)
# Embeddings: Voyage AI (voyage-3-large) — recommended by Anthropic for Claude
# Specialized: voyage-code-3 (code), voyage-finance-2 (finance), voyage-law-2 (legal)
embeddings = VoyageAIEmbeddings(model="voyage-3-large")
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)

# Hybrid retriever with reranking
base_retriever = vectorstore.as_retriever(
    search_type="hybrid", search_kwargs={"k": 20, "alpha": 0.5})

# Advanced RAG: HyDE (hypothetical documents), RAG Fusion (multi-query), Cohere Rerank
```

### Custom Agent with Tools

```python
from langchain.agents import AgentType, initialize_agent
from langchain.tools import tool

@tool
def search_database(query: str) -> str:
    """Search internal database for information."""
    return f"Results for: {query}"

@tool
def send_email(recipient: str, content: str) -> str:
    """Send an email to specified recipient."""
    return f"Email sent to {recipient}"

agent = initialize_agent([search_database, send_email], llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
```

### Multi-Step Chain

```python
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate

extract_chain = LLMChain(llm=llm, output_key="entities",
    prompt=PromptTemplate(input_variables=["text"],
        template="Extract key entities from: {text}\n\nEntities:"))
analyze_chain = LLMChain(llm=llm, output_key="analysis",
    prompt=PromptTemplate(input_variables=["entities"],
        template="Analyze these entities: {entities}\n\nAnalysis:"))
summary_chain = LLMChain(llm=llm, output_key="summary",
    prompt=PromptTemplate(input_variables=["entities", "analysis"],
        template="Summarize:\nEntities: {entities}\nAnalysis: {analysis}\n\nSummary:"))

overall_chain = SequentialChain(
    chains=[extract_chain, analyze_chain, summary_chain],
    input_variables=["text"],
    output_variables=["entities", "analysis", "summary"],
    verbose=True)
```

### Memory Management

Choose the right memory type:

```python
# Short conversations (< 10 messages)
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()

# Long conversations (summarize old messages)
from langchain.memory import ConversationSummaryMemory
memory = ConversationSummaryMemory(llm=llm)

# Sliding window (last N messages)
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=5)

# Entity tracking (people, places, facts)
from langchain.memory import ConversationEntityMemory
memory = ConversationEntityMemory(llm=llm)

# Semantic retrieval of relevant history
from langchain.memory import VectorStoreRetrieverMemory
memory = VectorStoreRetrieverMemory(retriever=retriever)

# Token-based windowing
from langchain.memory import ConversationTokenBufferMemory
```

Hybrid: combine multiple memory types for comprehensive context.

### Callback System

```python
from langchain.callbacks.base import BaseCallbackHandler

class CustomCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM started with prompts: {prompts}")
    def on_llm_end(self, response, **kwargs):
        print(f"LLM ended with response: {response}")
    def on_llm_error(self, error, **kwargs):
        print(f"LLM error: {error}")
    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"Chain started with inputs: {inputs}")
    def on_agent_action(self, action, **kwargs):
        print(f"Agent taking action: {action}")

agent.run("query", callbacks=[CustomCallbackHandler()])
```

### Performance Optimization

```python
# Caching
from langchain.cache import InMemoryCache
import langchain
langchain.llm_cache = InMemoryCache()

# Batch processing
from langchain.document_loaders import DirectoryLoader
from concurrent.futures import ThreadPoolExecutor
loader = DirectoryLoader('./docs')
docs = loader.load()
with ThreadPoolExecutor(max_workers=4) as executor:
    split_docs = list(executor.map(
        lambda doc: text_splitter.split_documents([doc]), docs))

# Streaming responses
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
```

### Testing Strategies

```python
import pytest
from unittest.mock import Mock

def test_agent_tool_selection():
    mock_llm = Mock()
    mock_llm.predict.return_value = "Action: search_database\nAction Input: test query"
    agent = initialize_agent(tools, mock_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    agent.run("test query")
    assert "search_database" in str(mock_llm.predict.call_args)

def test_memory_persistence():
    memory = ConversationBufferMemory()
    memory.save_context({"input": "Hi"}, {"output": "Hello!"})
    history = memory.load_memory_variables({})['history']
    assert "Hi" in history and "Hello!" in history
```

### Common Pitfalls

1. **Memory overflow** — not managing conversation history length
2. **Tool selection errors** — poor tool descriptions confuse agents
3. **Context window exceeded** — exceeding LLM token limits
4. **No error handling** — not catching agent failures
5. **Inefficient retrieval** — not optimizing vector store queries

### Production Checklist

- [ ] Proper error handling
- [ ] Request/response logging
- [ ] Monitor token usage and costs
- [ ] Timeout limits for agent execution
- [ ] Rate limiting
- [ ] Input validation
- [ ] Edge-case tests
- [ ] Observability (callbacks)
- [ ] Fallback strategies
- [ ] Version control prompts and configs

## Multi-Agent Architecture

A structured workflow for creating and updating production-grade multi-agent systems — supervisor agents, planners, researchers, coders, and memory-backed autonomous pipelines.

### Step 1: Understand the Goal

Clarify: the business objective, required agent roles (supervisor, planner, researcher, coder, validator), tools each agent needs, memory strategy (Redis, Vector DB, LangChain Memory), and communication protocol (shared state, message passing).

### Step 2: Define the State Schema

```python
from typing import TypedDict

class AgentState(TypedDict):
    user_goal: str
    tasks: list[str]
    completed_tasks: list[str]
    next_agent: str
    context: dict
    step_count: int          # guards against infinite loops
    error: str | None
```

### Step 3: Define Agent Nodes

Each agent is an async function that reads from state and returns updated state:

```python
import logging
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

async def research_node(state: AgentState) -> AgentState:
    logger.info("research_node: starting")
    llm = ChatOpenAI(model="gpt-4o")
    result = await llm.bind_tools(research_tools).ainvoke(state["user_goal"])
    state["context"]["research"] = result.content
    state["next_agent"] = "coder"
    return state
```

### Step 4: Build the LangGraph

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research",   research_node)
    graph.add_node("coder",      coding_node)
    graph.add_node("validator",  validation_node)
    graph.add_node("tools",      ToolNode(all_tools))
    graph.set_entry_point("supervisor")

    graph.add_conditional_edges("supervisor", route_next,
        {"research": "research", "coder": "coder", "end": END})
    graph.add_edge("research",  "supervisor")
    graph.add_edge("coder",     "validator")
    graph.add_edge("validator", "supervisor")
    return graph.compile()

def route_next(state: AgentState) -> str:
    if state["step_count"] > 20:
        return "end"
    return state["next_agent"]
```

### Step 5: Add Memory

```python
from langchain_community.chat_message_histories import RedisChatMessageHistory

def get_memory(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id, url=os.getenv("REDIS_URL"), ttl=3600)
```

### Step 6: Run and Expose

```python
async def run(user_goal: str, session_id: str):
    graph = build_graph()
    initial_state = AgentState(
        user_goal=user_goal, tasks=[], completed_tasks=[],
        next_agent="supervisor", context={}, step_count=0, error=None)
    return await graph.ainvoke(initial_state)

# FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RunRequest(BaseModel):
    goal: str
    session_id: str

@app.post("/run")
async def run_agent(req: RunRequest):
    return {"result": await run(req.goal, req.session_id)}
```

### Supervisor with Dynamic Delegation

```python
DELEGATION_PROMPT = """
You are a supervisor. Given the current state, decide the next agent.
Available agents: research, coder, validator, end.
Respond with ONLY the agent name.

Goal: {goal}
Completed: {completed}
Context keys available: {context}
"""

async def supervisor_node(state: AgentState) -> AgentState:
    state["step_count"] += 1
    llm = ChatOpenAI(model="gpt-4o")
    decision = await llm.ainvoke(DELEGATION_PROMPT.format(
        goal=state["user_goal"],
        completed=state["completed_tasks"],
        context=list(state["context"].keys())))
    next_agent = decision.content.strip().lower()
    # Validate against allowlist before setting
    allowed = {"research", "coder", "validator", "end"}
    state["next_agent"] = next_agent if next_agent in allowed else "end"
    return state
```

### Reflection Loop (DeepAgents)

```python
async def reflection_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o")
    critique = await llm.ainvoke(
        f"Evaluate this output critically:\n{state['context'].get('code', '')}\n"
        "List any bugs, gaps, or improvements. Be concise.")
    state["context"]["critique"] = critique.content
    state["next_agent"] = "coder" if "bug" in critique.content.lower() else "end"
    return state
```

### Standard Folder Structure

```
multi_agent_system/
├── agents/          # One file per agent role
├── tools/           # Tool definitions and wrappers
├── memory/          # Redis, VectorDB, LangChain memory helpers
├── prompts/         # Prompt templates (one per agent)
├── workflows/       # High-level orchestration logic
├── graphs/          # LangGraph state + compiled graph definitions
├── api/             # FastAPI routes (optional)
├── configs/         # Config loader — no secrets in code
├── tests/           # Unit + integration tests per agent
└── main.py
```

### Updating an Existing Agent

Structure the response as:

```
## Existing Issue        [Describe the current problem]
## Root Cause            [Identify why it's happening in the architecture]
## Proposed Update       [Outline the changes at architecture level]
## Updated Code          [Generate only the changed modules]
## Migration Notes       [What breaks, what's backward-compatible]
## Performance Impact    [Latency / token / memory delta]
```

### Multi-Agent Best Practices

- ✅ One agent = one responsibility — never combine planning + coding + testing in one node
- ✅ Use `TypedDict` for all state schemas — enables type checking and graph validation
- ✅ Bind only the tools each agent needs — reduces hallucinated tool calls
- ✅ Always add a `step_count` guard to prevent infinite routing loops
- ✅ Use `async`/`await` throughout — LangGraph supports async natively
- ✅ Store all secrets in environment variables loaded via `os.getenv()`
- ✅ Set TTLs on all Redis keys scoped to `session_id`
- ✅ Log at every node entry and tool call for observability
- ✅ Validate supervisor routing output against an allowlist of agent names
- ❌ Don't hardcode API keys, model names, or Redis URLs
- ❌ Don't share tool lists across agents that don't need them
- ❌ Don't skip error handling — tool failures and empty LLM responses are common
- ❌ Don't trust unvalidated LLM routing decisions — always check against an allowlist

### Multi-Agent Pitfalls

- **Agent loops indefinitely** → add `step_count` to state; return `"end"` when `step_count > N`
- **Supervisor routes to a non-existent agent** → validate against a hardcoded allowlist
- **Memory leaks across sessions** → scope Redis keys to `session_id`, always set TTL
- **Tool results ignored by the next agent** → write output into `state["context"]` and confirm the next node reads it
- **Agents share too many tools and hallucinate** → `.bind_tools([only_relevant_tools])` per agent
- **Graph fails silently on rate limits** → wrap LLM calls in retry logic with exponential backoff (`tenacity`)

## Autonomous Coding Agent Patterns

Design patterns for building autonomous coding agents, inspired by [Cline](https://github.com/cline/cline) and [OpenAI Codex](https://github.com/openai/codex).

### Core Agent Loop

```
┌─────────────────────────────────────────────────────────────┐
│                     AGENT LOOP                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Think   │───▶│  Decide  │───▶│   Act    │              │
│  │ (Reason) │    │ (Plan)   │    │ (Execute)│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       ▲                               │                     │
│       │         ┌──────────┐          │                     │
│       └─────────│ Observe  │◀─────────┘                     │
│                 │ (Result) │                                │
│                 └──────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

```python
class AgentLoop:
    def __init__(self, llm, tools, max_iterations=50):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_iterations = max_iterations
        self.history = []

    def run(self, task: str) -> str:
        self.history.append({"role": "user", "content": task})
        for _ in range(self.max_iterations):
            response = self.llm.chat(messages=self.history,
                tools=self._format_tools(), tool_choice="auto")
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool(tool_call)
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })
            else:
                return response.content  # No more tool calls = done
        return "Max iterations reached"
```

### Multi-Model Architecture

```python
class MultiModelAgent:
    """Different models for different purposes."""
    def __init__(self):
        self.models = {
            "fast": "llm-fast-model",   # Quick decisions / planning
            "smart": "llm-smart-model", # Complex reasoning
            "code": "llm-code-model",   # Code generation
        }

    def select_model(self, task_type: str) -> str:
        if task_type == "planning":
            return self.models["fast"]
        elif task_type == "code":
            return self.models["code"]
        return self.models["smart"]
```

### Tool Design

Base class with JSON-schema parameters and `ToolResult` (success/output/error):

```python
class Tool:
    @property
    def schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self._get_parameters(),
                "required": self._get_required(),
            },
        }

    def execute(self, **kwargs) -> "ToolResult":
        raise NotImplementedError

class ReadFileTool(Tool):
    name = "read_file"
    description = "Read the contents of a file from the filesystem"

    def _get_parameters(self):
        return {
            "path": {"type": "string", "description": "Absolute path to the file"},
            "start_line": {"type": "integer", "description": "Line to start (1-indexed)"},
            "end_line": {"type": "integer", "description": "Line to stop (inclusive)"},
        }

    def _get_required(self):
        return ["path"]

    def execute(self, path, start_line=None, end_line=None) -> "ToolResult":
        try:
            with open(path) as f:
                lines = f.readlines()
            if start_line and end_line:
                lines = lines[start_line - 1:end_line]
            return ToolResult(success=True, output="".join(lines))
        except FileNotFoundError:
            return ToolResult(success=False, error=f"File not found: {path}")
```

Essential coding-agent tools: file ops (`read_file`, `write_file`, `edit_file`, `list_directory`, `search_files`), code understanding (`search_code`, `get_definition`, `get_references`), terminal (`run_command`, `read_output`, `send_input`), browser (`open_browser`, `click_element`, `type_text`, `screenshot`), context (`ask_user`, `search_web`).

**Edit tool** — precise search/replace with conflict detection:

```python
class EditFileTool(Tool):
    name = "edit_file"
    description = "Edit a file by replacing specific content"

    def execute(self, path, search, replace, expected_occurrences=1) -> "ToolResult":
        with open(path) as f:
            content = f.read()
        actual = content.count(search)
        if actual != expected_occurrences:
            return ToolResult(success=False,
                error=f"Expected {expected_occurrences} occurrences, found {actual}")
        if actual == 0:
            return ToolResult(success=False, error="Search text not found in file")
        with open(path, "w") as f:
            f.write(content.replace(search, replace))
        return ToolResult(success=True, output=f"Replaced {actual} occurrence(s)")
```

### Permission & Safety Patterns

```python
from enum import Enum

class PermissionLevel(Enum):
    AUTO = "auto"              # Fully automatic - no approval needed
    ASK_ONCE = "ask_once"      # Ask once per session
    ASK_EACH = "ask_each"      # Ask every time
    NEVER = "never"            # Never allow

PERMISSION_CONFIG = {
    "read_file": PermissionLevel.AUTO,
    "list_directory": PermissionLevel.AUTO,
    "search_code": PermissionLevel.AUTO,
    "write_file": PermissionLevel.ASK_ONCE,
    "edit_file": PermissionLevel.ASK_ONCE,
    "run_command": PermissionLevel.ASK_EACH,
    "delete_file": PermissionLevel.ASK_EACH,
    "sudo_command": PermissionLevel.NEVER,
    "format_disk": PermissionLevel.NEVER,
}
```

`ApprovalManager.request_approval(tool_name, args)` returns True for AUTO, False for NEVER, consults `session_approvals` for ASK_ONCE, and shows an approval dialog for ASK_EACH. `_assess_risk` escalates commands containing `rm -rf`, `sudo`, `chmod` to HIGH.

**Sandboxed execution** — validate paths stay inside the workspace (`os.path.realpath`), allowlist commands (`npm`, `python`, `node`, `git`, `ls`, `cat`), run with `cwd=workspace`, `timeout=30`, and `HOME=workspace`.

### Browser Automation

`BrowserTool` (Playwright/Puppeteer) with `open_url` (returns screenshot + title), `click` (with `wait_for_load_state("networkidle")`), `type_text` (`page.fill`), and `get_page_content` (extracts visible text). `VisualAgent` uses a vision model to describe a page or locate an element by visual description and click its coordinates.

### Context Management

`ContextManager` supports `@file`, `@folder` (max 20 files), `@url` (fetch + markdown), and `@problems` (IDE diagnostics) context injection, then `format_for_prompt()` into sections. `CheckpointManager` saves/restores agent state (history, context, workspace git ref + dirty status) to JSON for long-running tasks.

### MCP (Model Context Protocol) Integration

`MCPAgent` discovers tools from connected MCP servers (`server.list_tools()`) and can generate a new FastMCP server from a natural-language description ("add a tool that fetches Jira tickets"), saving it under `./mcp_servers/<name>/server.py` and hot-reloading.

## Production Deployment

### Async patterns

Always prefer async: `ainvoke`, `astream`, `aget_relevant_documents`.

```python
async def process_request(message: str, session_id: str):
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config={"configurable": {"thread_id": session_id}})
    return result["messages"][-1].content
```

### Tools with async + error handling

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    query: str = Field(description="Query to process")

async def tool_function(query: str) -> str:
    try:
        return await external_call(query)
    except Exception as e:
        return f"Error: {str(e)}"

tool = StructuredTool.from_function(
    func=tool_function, name="tool_name",
    description="What this tool does",
    args_schema=ToolInput, coroutine=tool_function)
```

### FastAPI server with streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/agent/invoke")
async def invoke_agent(request: AgentRequest):
    if request.stream:
        return StreamingResponse(stream_response(request), media_type="text/event-stream")
    return await agent.ainvoke({"messages": [...]})
```

### Monitoring & observability

- **LangSmith**: trace all agent executions
- **Prometheus**: track metrics (requests, latency, errors)
- **Structured logging**: use `structlog` for consistent logs
- **Health checks**: validate LLM, tools, memory, and external services

### Optimization

- **Caching**: Redis response caching with TTL
- **Connection pooling**: reuse vector DB connections
- **Load balancing**: multiple agent workers with round-robin routing
- **Timeout handling**: set timeouts on all async operations
- **Retry logic**: exponential backoff with max retries

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_with_retry():
    try:
        return await llm.ainvoke(prompt)
    except Exception as e:
        logger.error(f"LLM error: {e}")
        raise
```

### Testing & evaluation

```python
from langsmith.evaluation import evaluate

eval_config = RunEvalConfig(
    evaluators=["qa", "context_qa", "cot_qa"],
    eval_llm=ChatAnthropic(model="claude-sonnet-4-5"))

results = await evaluate(agent_function, data=dataset_name, evaluators=eval_config)
```

### Implementation checklist

- [ ] Initialize LLM with Claude Sonnet 4.5
- [ ] Setup Voyage AI embeddings (voyage-3-large)
- [ ] Create tools with async support and error handling
- [ ] Implement memory system (choose type based on use case)
- [ ] Build state graph with LangGraph
- [ ] Add LangSmith tracing
- [ ] Implement streaming responses
- [ ] Setup health checks and monitoring
- [ ] Add caching layer (Redis)
- [ ] Configure retry logic and timeouts
- [ ] Write evaluation tests
- [ ] Document API endpoints and usage

### Production best practices

1. **Always use async**: `ainvoke`, `astream`, `aget_relevant_documents`
2. **Handle errors gracefully**: try/except with fallbacks
3. **Monitor everything**: trace, log, and metric all operations
4. **Optimize costs**: cache responses, use token limits, compress memory
5. **Secure secrets**: environment variables, never hardcode
6. **Test thoroughly**: unit tests, integration tests, evaluation suites
7. **Document extensively**: API docs, architecture diagrams, runbooks
8. **Version control state**: use checkpointers for reproducibility

## Collaboration

### Delegation triggers

- `crewai|role-based|crew` → crewai (role-based multi-agent approach)
- `observability|tracing|langsmith` → langfuse (LLM observability)
- `structured output|json schema` → structured-output (structured LLM responses)
- `evaluate|benchmark|test agent` → agent-evaluation (evaluate agent performance)

### Production agent stack

```
1. Design agent graph with LangGraph
2. Add structured outputs for tool responses
3. Integrate Langfuse for observability
4. Test and monitor in production
```

### Multi-agent system

```
1. Design agent roles (CrewAI patterns)
2. Implement as LangGraph with subgraphs
3. Add inter-agent communication
4. Orchestrate with supervisor pattern
```

## Security & Safety Notes

- Never expose API keys in generated code. All secrets must use environment variables:
  ```python
  LLM_API_KEY = os.getenv("LLM_API_KEY")   # ✅ correct
  leaked_openai_token = "[redacted API key]"  # ❌ never do this
  ```
- Always validate and sanitize user inputs before injecting them into agent prompts — treat all user input as untrusted.
- Add a permission layer before allowing agents to execute shell commands or write to filesystems.
- If generating a Python REPL tool node, document that it must only run in a sandboxed, isolated environment.
- For production deployments, add rate-limit handling and exponential backoff on all LLM and external API calls.
- Scope all Redis session keys to `session_id` and set a TTL to prevent memory leaks across sessions.

## Related Skills

Works well with: `crewai`, `autonomous-agents`, `langfuse`, `structured-output`, `fastapi-backend`, `python-async`.

## Merged from

- `autonomous-agent-patterns` — agent loop, multi-model architecture, tool design, permissions/safety, sandboxing, browser automation, context management, MCP integration
- `langchain-architecture` — LangChain agents/chains/memory/callbacks, RAG, testing, performance
- `llm-application-dev-langchain-agent` — production LangChain/LangGraph patterns, Claude Sonnet 4.5 + Voyage, FastAPI streaming, monitoring, evaluation
- `multi-agent-architect` — multi-agent architecture workflow, supervisor delegation, folder structure, best practices, pitfalls

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.