# ADR-006: ChromaDB for Vector Search & RAG

## Context
AlphaMind AI requires a vector database for semantic similarity search over chunked SEC 10-K/10-Q filings, financial news articles, and long-term agent research memories.

## Decision
We decide to adopt **ChromaDB** as the primary vector database.

## Alternatives Considered
1. **Pinecone**: Rejected due to proprietary cloud lock-in and monthly cost overhead during early developer phases.
2. **Qdrant**: Excellent vector DB, selected as a pluggable alternative via the Plugin Architecture.
3. **pgvector (PostgreSQL extension)**: Considered, but ChromaDB was selected for native Python integration, multi-collection management, and dedicated embedding pipeline speed.

## Pros
- **Lightweight & Embedded/Server Ready**: Runs embedded locally in developer environment and as a containerized server in production.
- **Native LangChain Integration**: Pre-built integration with LangGraph tools and OpenAI/BGE embeddings.
- **Zero Cloud Costs**: Self-hosted on infrastructure.

## Cons
- Requires monitoring memory footprint when scaling to millions of vector passages.

## Consequences
All vector store interactions MUST be encapsulated in `packages/rag/vector_store.py` supporting pluggable replacements.
