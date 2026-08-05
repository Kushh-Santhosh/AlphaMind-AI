"""
AlphaMind AI - Knowledge Intelligence Observability & Metrics Tracker
"""

from __future__ import annotations

import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class KnowledgeIntelligenceMetrics(BaseModel):
    total_nodes_count: int = 0
    total_edges_count: int = 0
    total_embeddings_count: int = 0
    total_chunks_count: int = 0
    indexing_duration_ms: float = 0.0
    retrieval_latency_ms: float = 0.0


class KnowledgeObservabilityTracker:
    """Tracker recording execution metrics for Knowledge Graph and RAG pipeline."""

    _metrics = KnowledgeIntelligenceMetrics()

    @classmethod
    def update_graph_stats(cls, nodes_count: int, edges_count: int) -> None:
        cls._metrics.total_nodes_count = nodes_count
        cls._metrics.total_edges_count = edges_count
        logger.info("Updated Graph metrics: %d nodes, %d edges.", nodes_count, edges_count)

    @classmethod
    def update_vector_stats(cls, embeddings_count: int, chunks_count: int) -> None:
        cls._metrics.total_embeddings_count = embeddings_count
        cls._metrics.total_chunks_count = chunks_count
        logger.info(
            "Updated RAG metrics: %d embeddings, %d chunks.", embeddings_count, chunks_count
        )

    @classmethod
    def get_metrics_snapshot(cls) -> KnowledgeIntelligenceMetrics:
        return cls._metrics
