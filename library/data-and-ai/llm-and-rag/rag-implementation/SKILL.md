---
name: "rag-implementation"
description: "RAG (Retrieval-Augmented Generation) implementation workflow covering embedding selection, vector database setup, chunking strategies, and retrieval optimization. Includes an 8-phase workflow plus concrete RAG patterns (semantic chunking, hierarchical retrieval, hybrid search, query expansion, contextual compression, metadata filtering) and sharp edges (failure modes with fixes). Use when working with rag implementation."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# RAG Implementation Workflow

## Overview

Specialized workflow for implementing RAG (Retrieval-Augmented Generation) systems including embedding model selection, vector database setup, chunking strategies, retrieval optimization, and evaluation.

**Role**: RAG Systems Architect

Bridge the gap between raw documents and LLM understanding. Retrieval quality determines generation quality — garbage in, garbage out. Obsess over chunking boundaries, embedding dimensions, and similarity metrics because they make the difference between helpful and hallucinating.

### Principles

- **Retrieval quality > generation quality** — fix retrieval first.
- Chunk size depends on content type and query patterns.
- Embeddings are not magic — they have blind spots.
- Always evaluate retrieval separately from generation.
- Hybrid search beats pure semantic in most cases.

## When to Use This Workflow

Use this workflow when:
- Building RAG-powered applications
- Implementing semantic search
- Creating knowledge-grounded AI
- Setting up document Q&A systems
- Optimizing retrieval quality

## Workflow Phases

### Phase 1: Requirements Analysis

#### Skills to Invoke
- `ai-product` - AI product design
- `rag-engineer` - RAG engineering

#### Actions
1. Define use case
2. Identify data sources
3. Set accuracy requirements
4. Determine latency targets
5. Plan evaluation metrics

#### Copy-Paste Prompts
```
Use @ai-product to define RAG application requirements
```

### Phase 2: Embedding Selection

#### Skills to Invoke
- `embedding-strategies` - Embedding selection
- `rag-engineer` - RAG patterns

#### Actions
1. Evaluate embedding models
2. Test domain relevance
3. Measure embedding quality
4. Consider cost/latency
5. Select model

#### Copy-Paste Prompts
```
Use @embedding-strategies to select optimal embedding model
```

### Phase 3: Vector Database Setup

#### Skills to Invoke
- `vector-database-engineer` - Vector DB
- `similarity-search-patterns` - Similarity search

#### Actions
1. Choose vector database
2. Design schema
3. Configure indexes
4. Set up connection
5. Test queries

#### Copy-Paste Prompts
```
Use @vector-database-engineer to set up vector database
```

### Phase 4: Chunking Strategy

#### Skills to Invoke
- `rag-engineer` - Chunking strategies
- `rag-implementation` - RAG implementation

#### Actions
1. Choose chunk size
2. Implement chunking
3. Add overlap handling
4. Create metadata
5. Test retrieval quality

#### Copy-Paste Prompts
```
Use @rag-engineer to implement chunking strategy
```

### Phase 5: Retrieval Implementation

#### Skills to Invoke
- `similarity-search-patterns` - Similarity search
- `hybrid-search-implementation` - Hybrid search

#### Actions
1. Implement vector search
2. Add keyword search
3. Configure hybrid search
4. Set up reranking
5. Optimize latency

#### Copy-Paste Prompts
```
Use @similarity-search-patterns to implement retrieval
```

```
Use @hybrid-search-implementation to add hybrid search
```

### Phase 6: LLM Integration

#### Skills to Invoke
- `llm-application-dev-ai-assistant` - LLM integration
- `llm-application-dev-prompt-optimize` - Prompt optimization

#### Actions
1. Select LLM provider
2. Design prompt template
3. Implement context injection
4. Add citation handling
5. Test generation quality

#### Copy-Paste Prompts
```
Use @llm-application-dev-ai-assistant to integrate LLM
```

### Phase 7: Caching

#### Skills to Invoke
- `prompt-caching` - Prompt caching
- `rag-engineer` - RAG optimization

#### Actions
1. Implement response caching
2. Set up embedding cache
3. Configure TTL
4. Add cache invalidation
5. Monitor hit rates

#### Copy-Paste Prompts
```
Use @prompt-caching to implement RAG caching
```

### Phase 8: Evaluation

#### Skills to Invoke
- `llm-evaluation` - LLM evaluation
- `evaluation` - AI evaluation

#### Actions
1. Define evaluation metrics
2. Create test dataset
3. Measure retrieval accuracy
4. Evaluate generation quality
5. Iterate on improvements

#### Copy-Paste Prompts
```
Use @llm-evaluation to evaluate RAG system
```

## RAG Architecture

```
User Query -> Embedding -> Vector Search -> Retrieved Docs -> LLM -> Response
                |              |              |              |
            Model         Vector DB     Chunk Store    Prompt + Context
```

## Quality Gates

- [ ] Embedding model selected
- [ ] Vector DB configured
- [ ] Chunking implemented
- [ ] Retrieval working
- [ ] LLM integrated
- [ ] Evaluation passing

## Related Workflow Bundles

- `ai-ml` - AI/ML development
- `ai-agent-development` - AI agents
- `database` - Vector databases

## RAG Patterns

### Semantic Chunking

Chunk by meaning, not arbitrary token counts. **When to use**: documents with natural sections.

- Use sentence boundaries, not token limits.
- Detect topic shifts with embedding similarity.
- Preserve document structure (headers, paragraphs).
- Include overlap for context continuity.
- Add metadata for filtering.

### Hierarchical Retrieval

Multi-level retrieval for better precision. **When to use**: large document collections with varied granularity.

- Index at multiple chunk sizes (paragraph, section, document).
- First pass: coarse retrieval for candidates.
- Second pass: fine-grained retrieval for precision.
- Use parent-child relationships for context.

### Hybrid Search

Combine semantic and keyword search. **When to use**: queries may be keyword-heavy or semantic.

- BM25/TF-IDF for keyword matching.
- Vector similarity for semantic matching.
- Reciprocal Rank Fusion for combining scores.
- Weight tuning based on query type.

### Query Expansion

Expand queries to improve recall. **When to use**: short or ambiguous user queries.

- Use an LLM to generate query variations.
- Add synonyms and related terms.
- Hypothetical Document Embedding (HyDE).
- Multi-query retrieval with deduplication.

### Contextual Compression

Compress retrieved context to fit the window. **When to use**: retrieved chunks exceed context limits.

- Extract relevant sentences only.
- Use an LLM to summarize chunks.
- Remove redundant information.
- Prioritize by relevance score.

### Metadata Filtering

Pre-filter by metadata before semantic search. **When to use**: documents have structured metadata.

- Filter by date, source, category first.
- Reduce search space before vector similarity.
- Combine metadata filters with semantic scores.
- Index metadata for fast filtering.

## Sharp Edges

### Fixed-size chunking breaks sentences and context — HIGH

**Situation**: fixed token/character limits for chunking.
**Symptoms**: retrieved chunks feel incomplete or cut off; answer quality varies wildly; high recall but low precision.
**Why it breaks**: fixed-size chunks split mid-sentence, mid-paragraph, or mid-idea; embeddings represent incomplete thoughts.
**Fix**: semantic chunking that respects structure — split on sentence/paragraph boundaries, detect topic shifts with embedding similarity, include overlap, preserve headers as metadata.

### Pure semantic search without metadata pre-filtering — MEDIUM

**Situation**: only vector similarity, ignoring metadata.
**Symptoms**: returns outdated info; mixes content from wrong sources; users can't scope searches.
**Why it breaks**: semantic search finds similar content, not necessarily relevant content.
**Fix**: pre-filter by metadata (date, source, category) before vector search; post-filter by relevance; include metadata in the retrieval API; allow user-specified filters.

### Same embedding model for different content types — MEDIUM

**Situation**: one embedding model for code, docs, and structured data.
**Symptoms**: code search returns irrelevant results; domain terms not matched; similar concepts not clustered.
**Why it breaks**: embedding models are trained on specific content types.
**Fix**: evaluate embeddings per content type — code-specific embeddings (e.g. CodeBERT) for code, domain-specific or fine-tuned embeddings for domains, benchmark before choosing, separate indices per content type if needed.

### Using first-stage retrieval results directly — MEDIUM

**Situation**: taking top-K from vector search without reranking.
**Symptoms**: clearly relevant docs not in top results; arbitrary ordering; adding more results helps.
**Why it breaks**: first-stage retrieval optimizes for recall, not precision.
**Fix**: retrieve a larger candidate set (top 20–50), rerank with a cross-encoder (query-document pairs), return reranked top-K (e.g. top 5), cache the reranker.

### Cramming maximum context into the LLM prompt — MEDIUM

**Situation**: using all retrieved context regardless of relevance.
**Symptoms**: answers drift with more context; LLM ignores key info; high token costs.
**Why it breaks**: more context isn't better — irrelevant context confuses the model and it has attention limits.
**Fix**: set a minimum similarity cutoff, limit context to truly relevant chunks, summarize/compress if needed, order context by relevance.

### Not measuring retrieval quality separately from generation — HIGH

**Situation**: only evaluating end-to-end RAG quality.
**Symptoms**: can't diagnose poor performance; prompt changes don't help; random quality variations.
**Why it breaks**: if answers are wrong you can't tell whether retrieval or generation failed, leading to wrong fixes.
**Fix**: create a retrieval test set with labeled relevant docs; measure MRR, NDCG, Recall@K; evaluate generation only on correct retrievals; track metrics over time.

### Not updating embeddings when source documents change — MEDIUM

**Situation**: embeddings generated once, never refreshed.
**Symptoms**: returns outdated info; references deleted content; inconsistent with source.
**Why it breaks**: documents change but embeddings don't, eroding trust.
**Fix**: track document versions/hashes, re-embed on change, handle deleted documents, consider TTLs for embeddings.

### Same retrieval strategy for all query types — MEDIUM

**Situation**: pure semantic search for keyword-heavy queries.
**Symptoms**: exact-term searches miss results; concept searches too literal.
**Why it breaks**: keyword queries need exact matches; semantic queries need paraphrase tolerance.
**Fix**: hybrid search — BM25/TF-IDF for keywords, vector similarity for semantics, Reciprocal Rank Fusion to combine, tune weights by query pattern.

## Related Skills

Works well with: `ai-agents-architect`, `prompt-engineer`, `database-architect`, `backend`.

## When to Use

- User mentions or implies: building RAG, vector search, embeddings, semantic search, document retrieval, context retrieval, knowledge base, LLM with documents, chunking strategy, pinecone, weaviate, chromadb, pgvector.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

## Merged from

- `rag-engineer` — RAG patterns (semantic chunking, hierarchical retrieval, hybrid search, query expansion, contextual compression, metadata filtering), sharp edges (failure modes with fixes), role and principles
