"""
AlphaMind AI - Hybrid Retrieval Foundation Interfaces

Defines abstract Protocol contracts for Vector, Graph, Keyword, Metadata Filter,
Hybrid, and Cross-Source Retrieval systems.
STRICT RULE: Interface contracts ONLY — zero retrieval execution in Milestone 7.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class RetrievalQuery(BaseModel):
    query_text: str
    symbol: str
    top_k: int = 5
    metadata_filters: dict[str, Any] = Field(default_factory=dict)
    min_similarity_score: float = 0.70


class RetrievalResultItem(BaseModel):
    item_id: str
    source_type: str  # "vector", "graph", "keyword", "hybrid"
    content: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class HybridRetrievalResponse(BaseModel):
    query: RetrievalQuery
    results: list[RetrievalResultItem] = Field(default_factory=list)
    vector_results_count: int = 0
    graph_results_count: int = 0
    total_execution_ms: float = 0.0


@runtime_checkable
class VectorRetrieverProtocol(Protocol):
    async def retrieve_vectors(self, query: RetrievalQuery) -> list[RetrievalResultItem]: ...


@runtime_checkable
class GraphRetrieverProtocol(Protocol):
    async def retrieve_graph_subgraph(self, query: RetrievalQuery) -> list[RetrievalResultItem]: ...


@runtime_checkable
class KeywordSearchProtocol(Protocol):
    async def search_keywords(self, query: RetrievalQuery) -> list[RetrievalResultItem]: ...


@runtime_checkable
class MetadataFilterProtocol(Protocol):
    async def filter_by_metadata(
        self, collection: str, filters: dict[str, Any]
    ) -> list[RetrievalResultItem]: ...


@runtime_checkable
class HybridRetrieverProtocol(Protocol):
    async def hybrid_search(self, query: RetrievalQuery) -> HybridRetrievalResponse: ...


@runtime_checkable
class CrossSourceRetrieverProtocol(Protocol):
    async def retrieve_cross_source(self, query: RetrievalQuery) -> HybridRetrievalResponse: ...
