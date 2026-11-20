---
name: "embedding-strategies"
description: "Guide to selecting and optimizing embedding models for vector search applications. Covers embedding model comparison, embedding pipelines (OpenAI, local sentence-transformers, code), chunking strategies (token, sentence, semantic, recursive), domain-specific pipelines, embedding quality evaluation (precision@k, recall@k, MRR, nDCG), vector database selection and index configuration (HNSW, IVF, PQ), hybrid search, metadata filtering, and similarity search at scale. Use when working with embedding strategies."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Embedding Strategies & Vector Search

Guide to selecting and optimizing embedding models for vector search applications. Use for choosing embedding models for RAG, optimizing chunking, fine-tuning embeddings for domains, comparing model performance, reducing embedding dimensions, handling multilingual content, building semantic search, implementing nearest-neighbor queries, optimizing retrieval latency, scaling to millions of vectors, and combining semantic with keyword search.

## Capabilities

- Vector database selection and architecture (Pinecone, Weaviate, Qdrant, Milvus, pgvector)
- Embedding model selection and optimization
- Index configuration (HNSW, IVF, PQ)
- Hybrid search (vector + keyword) implementation
- Chunking strategies for documents
- Metadata filtering and pre/post-filtering
- Performance tuning and scaling

## Use this skill when

- Choosing embedding models for RAG
- Optimizing chunking strategies
- Fine-tuning embeddings for domains
- Comparing embedding model performance
- Reducing embedding dimensions
- Handling multilingual content
- Building RAG (Retrieval Augmented Generation) systems
- Implementing semantic search over documents
- Creating recommendation engines
- Building image/audio similarity search
- Optimizing vector search latency and recall
- Scaling vector operations to millions of vectors
- Combining semantic and keyword search

## Core Concepts

### 1. Embedding Model Comparison

| Model | Dimensions | Max Tokens | Best For |
|-------|------------|------------|----------|
| **text-embedding-3-large** | 3072 | 8191 | High accuracy |
| **text-embedding-3-small** | 1536 | 8191 | Cost-effective |
| **voyage-2 / voyage-3-large** | 1024 | 4000 | Code, legal; recommended for Claude |
| **bge-large-en-v1.5** | 1024 | 512 | Open source |
| **all-MiniLM-L6-v2** | 384 | 256 | Fast, lightweight |
| **multilingual-e5-large** | 1024 | 512 | Multi-language |

### 2. Embedding Pipeline

```
Document → Chunking → Preprocessing → Embedding Model → Vector
                ↓
        [Overlap, Size]  [Clean, Normalize]  [API/Local]
```

## Templates

### Template 1: OpenAI Embeddings

```python
from openai import OpenAI
from typing import List
import numpy as np

client = OpenAI()

def get_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: int = None
) -> List[List[float]]:
    """Get embeddings from OpenAI."""
    # Handle batching for large lists
    batch_size = 100
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        kwargs = {"input": batch, "model": model}
        if dimensions:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)
        embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(embeddings)

    return all_embeddings


def get_embedding(text: str, **kwargs) -> List[float]:
    """Get single embedding."""
    return get_embeddings([text], **kwargs)[0]


# Dimension reduction with OpenAI (Matryoshka)
def get_reduced_embedding(text: str, dimensions: int = 512) -> List[float]:
    return get_embedding(text, model="text-embedding-3-small", dimensions=dimensions)
```

### Template 2: Local Embeddings with Sentence Transformers

```python
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np

class LocalEmbedder:
    """Local embedding with sentence-transformers."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
        device: str = "cuda"
    ):
        self.model = SentenceTransformer(model_name, device=device)

    def embed(
        self,
        texts: List[str],
        normalize: bool = True,
        show_progress: bool = False
    ) -> np.ndarray:
        """Embed texts with optional normalization."""
        return self.model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a query with BGE-style prefix."""
        # BGE models benefit from query prefix
        query = f"Represent this sentence for searching relevant passages: {query}"
        return self.embed([query])[0]

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        return self.embed(documents)


# E5 model with instructions
class E5Embedder:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, query: str) -> np.ndarray:
        return self.model.encode(f"query: {query}")

    def embed_document(self, document: str) -> np.ndarray:
        return self.model.encode(f"passage: {document}")
```

### Template 3: Chunking Strategies

```python
from typing import List, Tuple
import re

def chunk_by_tokens(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    tokenizer=None
) -> List[str]:
    """Chunk text by token count."""
    import tiktoken
    tokenizer = tokenizer or tiktoken.get_encoding("cl100k_base")

    tokens = tokenizer.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_text = tokenizer.decode(tokens[start:end])
        chunks.append(chunk_text)
        start = end - chunk_overlap

    return chunks


def chunk_by_sentences(
    text: str,
    max_chunk_size: int = 1000,
    min_chunk_size: int = 100
) -> List[str]:
    """Chunk text by sentences, respecting size limits."""
    import nltk
    sentences = nltk.sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)
        if current_size + sentence_size > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0
        current_chunk.append(sentence)
        current_size += sentence_size

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_by_semantic_sections(
    text: str,
    headers_pattern: str = r'^#{1,3}\s+.+$'
) -> List[Tuple[str, str]]:
    """Chunk markdown by headers, preserving hierarchy."""
    lines = text.split('\n')
    chunks = []
    current_header = ""
    current_content = []

    for line in lines:
        if re.match(headers_pattern, line, re.MULTILINE):
            if current_content:
                chunks.append((current_header, '\n'.join(current_content)))
            current_header = line
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        chunks.append((current_header, '\n'.join(current_content)))

    return chunks


def recursive_character_splitter(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: List[str] = None
) -> List[str]:
    """LangChain-style recursive splitter."""
    separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(text: str, separators: List[str]) -> List[str]:
        if not text:
            return []
        separator = separators[0]
        remaining_separators = separators[1:]

        if separator == "":
            # Character-level split
            return [text[i:i+chunk_size]
                    for i in range(0, len(text), chunk_size - chunk_overlap)]

        splits = text.split(separator)
        chunks = []
        current_chunk = []
        current_length = 0

        for split in splits:
            split_length = len(split) + len(separator)
            if current_length + split_length > chunk_size and current_chunk:
                chunk_text = separator.join(current_chunk)
                # Recursively split if still too large
                if len(chunk_text) > chunk_size and remaining_separators:
                    chunks.extend(split_text(chunk_text, remaining_separators))
                else:
                    chunks.append(chunk_text)
                # Start new chunk with overlap
                overlap_splits = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length + len(s) <= chunk_overlap:
                        overlap_splits.insert(0, s)
                        overlap_length += len(s)
                    else:
                        break
                current_chunk = overlap_splits
                current_length = overlap_length
            current_chunk.append(split)
            current_length += split_length

        if current_chunk:
            chunks.append(separator.join(current_chunk))

        return chunks

    return split_text(text, separators)
```

### Template 4: Domain-Specific Embedding Pipeline

```python
class DomainEmbeddingPipeline:
    """Pipeline for domain-specific embeddings."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        preprocessing_fn=None
    ):
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.preprocess = preprocessing_fn or self._default_preprocess

    def _default_preprocess(self, text: str) -> str:
        """Default preprocessing."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    async def process_documents(
        self,
        documents: List[dict],
        id_field: str = "id",
        content_field: str = "content",
        metadata_fields: List[str] = None
    ) -> List[dict]:
        """Process documents for vector storage."""
        processed = []

        for doc in documents:
            content = doc[content_field]
            doc_id = doc[id_field]

            cleaned = self.preprocess(content)
            chunks = chunk_by_tokens(cleaned, self.chunk_size, self.chunk_overlap)
            embeddings = get_embeddings(chunks, self.embedding_model)

            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                record = {
                    "id": f"{doc_id}_chunk_{i}",
                    "document_id": doc_id,
                    "chunk_index": i,
                    "text": chunk,
                    "embedding": embedding
                }
                if metadata_fields:
                    for field in metadata_fields:
                        if field in doc:
                            record[field] = doc[field]
                processed.append(record)

        return processed


# Code-specific pipeline
class CodeEmbeddingPipeline:
    """Specialized pipeline for code embeddings."""

    def __init__(self, model: str = "voyage-code-2"):
        self.model = model

    def chunk_code(self, code: str, language: str) -> List[dict]:
        """Chunk code by functions/classes."""
        import tree_sitter
        # Parse with tree-sitter; extract functions, classes, methods
        # Return chunks with context
        pass

    def embed_with_context(self, chunk: str, context: str) -> List[float]:
        """Embed code with surrounding context."""
        combined = f"Context: {context}\n\nCode:\n{chunk}"
        return get_embedding(combined, model=self.model)
```

### Template 5: Embedding Quality Evaluation

```python
import numpy as np
from typing import List, Tuple

def evaluate_retrieval_quality(
    queries: List[str],
    relevant_docs: List[List[str]],  # relevant doc IDs per query
    retrieved_docs: List[List[str]],  # retrieved doc IDs per query
    k: int = 10
) -> dict:
    """Evaluate embedding quality for retrieval."""

    def precision_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        retrieved_k = retrieved[:k]
        return len(set(retrieved_k) & relevant) / k

    def recall_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        retrieved_k = retrieved[:k]
        return len(set(retrieved_k) & relevant) / len(relevant) if relevant else 0

    def mrr(relevant: set, retrieved: List[str]) -> float:
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                return 1 / (i + 1)
        return 0

    def ndcg_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        dcg = sum(1 / np.log2(i + 2) if doc in relevant else 0
                  for i, doc in enumerate(retrieved[:k]))
        ideal_dcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
        return dcg / ideal_dcg if ideal_dcg > 0 else 0

    metrics = {f"precision@{k}": [], f"recall@{k}": [],
               "mrr": [], f"ndcg@{k}": []}

    for relevant, retrieved in zip(relevant_docs, retrieved_docs):
        relevant_set = set(relevant)
        metrics[f"precision@{k}"].append(precision_at_k(relevant_set, retrieved, k))
        metrics[f"recall@{k}"].append(recall_at_k(relevant_set, retrieved, k))
        metrics["mrr"].append(mrr(relevant_set, retrieved))
        metrics[f"ndcg@{k}"].append(ndcg_at_k(relevant_set, retrieved, k))

    return {name: np.mean(values) for name, values in metrics.items()}


def compute_embedding_similarity(
    embeddings1: np.ndarray,
    embeddings2: np.ndarray,
    metric: str = "cosine"
) -> np.ndarray:
    """Compute similarity matrix between embedding sets."""
    if metric == "cosine":
        norm1 = embeddings1 / np.linalg.norm(embeddings1, axis=1, keepdims=True)
        norm2 = embeddings2 / np.linalg.norm(embeddings2, axis=1, keepdims=True)
        return norm1 @ norm2.T
    elif metric == "euclidean":
        from scipy.spatial.distance import cdist
        return -cdist(embeddings1, embeddings2, metric='euclidean')
    elif metric == "dot":
        return embeddings1 @ embeddings2.T
```

## Vector Databases & Similarity Search

### Choosing a vector database

| DB | Scale | Features |
|---|---|---|
| Pinecone | Billions | Managed, hybrid search, metadata filtering |
| Weaviate | Millions | Self-hosted, GraphQL API, modules |
| Qdrant | Millions | High performance, payload filtering |
| Milvus | Billions | Distributed, GPU acceleration |
| pgvector | Millions | SQL integration, ACID, already in Postgres |

### Index configuration

- **HNSW** (Hierarchical Navigable Small World) — best recall/latency tradeoff; parameters `M` (graph degree), `efConstruction` (build), `ef`/`efSearch` (query). Higher `ef` = better recall, slower query.
- **IVF** (Inverted File) — clusters vectors, searches `nprobe` nearest clusters; good for very large datasets with acceptable recall tradeoff.
- **PQ** (Product Quantization) — compresses vectors to save memory; combine with IVF (IVF-PQ) for billion-scale.

### Hybrid search (vector + keyword)

Combine semantic similarity with BM25/keyword matching via Reciprocal Rank Fusion (RRF):

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
```

### Metadata filtering

- **Pre-filtering**: restrict the candidate set before the ANN search (smaller search space, may miss neighbors if filter is too narrow).
- **Post-filtering**: retrieve top-k then filter (simple, but may return fewer than k results).
- Store filterable fields (source, date, language, doc type) in the vector DB payload and combine with the query.

### Similarity metrics

- **Cosine** — most common for normalized embeddings; insensitive to magnitude.
- **Dot product** — equivalent to cosine on normalized vectors; faster.
- **Euclidean** — sensitive to magnitude; good when distance matters absolutely.

### Scaling to millions of vectors

- Shard by namespace/tenant; replicate for read throughput.
- Batch embedding generation; cache frequent queries.
- Monitor recall vs latency tradeoffs; plan index rebuilds when the corpus grows.
- Watch for embedding drift as models and data evolve.

## Workflow

1. Analyze data characteristics and query patterns
2. Select appropriate embedding model
3. Design chunking and preprocessing pipeline
4. Choose vector database and index type
5. Configure metadata schema for filtering
6. Implement hybrid search if needed
7. Optimize for latency/recall tradeoffs
8. Set up monitoring and reindexing strategies

## Best Practices

### Do's
- **Match model to use case** — code vs prose vs multilingual
- **Chunk thoughtfully** — preserve semantic boundaries
- **Normalize embeddings** — for cosine similarity
- **Batch requests** — more efficient than one-by-one
- **Cache embeddings** — avoid recomputing
- **Choose embedding dimensions based on use case** (384–1536)
- **Implement proper chunking with overlap**
- **Use metadata filtering** to reduce search space
- **Monitor embedding drift** over time
- **Plan for index rebuilding**
- **Cache frequent queries**
- **Test recall vs latency tradeoffs**

### Don'ts
- **Don't ignore token limits** — truncation loses info
- **Don't mix embedding models** — incompatible spaces
- **Don't skip preprocessing** — garbage in, garbage out
- **Don't over-chunk** — lose context

## Resources

- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers](https://www.sbert.net/)
- [MTEB Benchmark](https://huggingface.co/spaces/mteb/leaderboard)

## Merged from

- `similarity-search-patterns` — semantic search, nearest-neighbor queries, retrieval optimization, hybrid search scope
- `vector-database-engineer` — vector database selection, index configuration, metadata filtering, scaling, workflow

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.