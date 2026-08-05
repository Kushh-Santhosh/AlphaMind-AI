"""
AlphaMind AI - Text Embedding Pipeline

Manages batch embedding generation, re-indexing, embedding versioning, and provider switching.
STRICT RULE: No search or vector similarity retrieval in Milestone 7.
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel

from packages.plugins.provider_manager import BaseProvider, ProviderMetadata
from packages.rag.chunker import DocumentChunk
from packages.rag.vector_store import VectorCollectionName, VectorDocumentRecord, VectorStoreManager

logger = logging.getLogger(__name__)


class EmbeddingJobMetadata(BaseModel):
    job_id: str
    version: str = "v1"
    provider_id: str
    total_chunks: int
    processed_chunks: int
    duration_ms: float = 0.0
    status: str = "completed"


class DummyHuggingFaceEmbeddingProvider(BaseProvider):
    """Secondary Embedding Provider Adapter (HuggingFace BGE-Large)."""

    def __init__(self) -> None:
        metadata = ProviderMetadata(
            provider_id="huggingface_bge",
            provider_name="HuggingFace BGE Large Embedding Model",
            version="v1.5",
            tier="secondary",
            supported_assets=["doc_chunks"],
            rate_limit_per_minute=300,
            timeout_seconds=5.0,
        )
        super().__init__(metadata)

    async def generate_embedding(self, text: str) -> list[float]:
        return [0.02] * 1024


class EmbeddingPipeline:
    """
    Embedding Pipeline processing batch document chunks into vector records.
    """

    def __init__(
        self,
        vector_store: VectorStoreManager,
        provider: BaseProvider,
        version: str = "v1",
    ) -> None:
        self.vector_store = vector_store
        self.provider = provider
        self.version = version

    async def process_batch(
        self,
        chunks: list[DocumentChunk],
        target_collection: VectorCollectionName,
    ) -> EmbeddingJobMetadata:
        """Process batch of document chunks and populate vector store collections."""
        start_time = time.monotonic()
        job_id = f"emb_job_{int(time.time())}"

        for chunk in chunks:
            # Generate embedding vector
            vec = await self.provider.execute_with_resilience(
                self.provider.generate_embedding, chunk.chunk_text  # type: ignore[attr-defined]
            )

            rec = VectorDocumentRecord(
                doc_id=chunk.chunk_id,
                collection_name=target_collection,
                embedding_vector=vec,
                document_text=chunk.chunk_text,
                metadata={
                    "symbol": chunk.symbol,
                    "section_title": chunk.section_title,
                    "version": self.version,
                    "parent_id": chunk.parent_chunk_id,
                },
            )
            self.vector_store.add_document(rec)

        duration = (time.monotonic() - start_time) * 1000.0
        logger.info(
            "Embedding job '%s' processed %d chunks into '%s' in %.2fms.",
            job_id,
            len(chunks),
            target_collection.value,
            duration,
        )

        return EmbeddingJobMetadata(
            job_id=job_id,
            version=self.version,
            provider_id=self.provider.metadata.provider_id,
            total_chunks=len(chunks),
            processed_chunks=len(chunks),
            duration_ms=duration,
        )
