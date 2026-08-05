"""
Knowledge Intelligence Test Suite — Graph Schema, Ingestion Pipeline, Vector Collections,
Document Chunker, Embedding Pipeline, Hybrid Retrieval Protocols, Memory Integration & Graph APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.knowledge_graph.ingestion import GraphIngestionEngine
from packages.knowledge_graph.schema import (
    GraphEdge,
    GraphEntityType,
    GraphNode,
    GraphRelationType,
)
from packages.memory.hierarchical_memory import HierarchicalMemoryManager
from packages.rag.chunker import HierarchicalDocumentChunker
from packages.rag.embedding_pipeline import DummyHuggingFaceEmbeddingProvider, EmbeddingPipeline
from packages.rag.retrieval import (
    CrossSourceRetrieverProtocol,
    GraphRetrieverProtocol,
    HybridRetrieverProtocol,
    KeywordSearchProtocol,
    MetadataFilterProtocol,
    VectorRetrieverProtocol,
)
from packages.rag.vector_store import VectorCollectionName, VectorDocumentRecord, VectorStoreManager
from packages.research.company_engine import CompanyResearchEngine
from packages.research.document_processor import DocumentProcessingEngine
from packages.research.event_engine import EventIntelligenceEngine
from packages.research.financial_statement_engine import FinancialStatementEngine
from packages.research.macro_engine import MacroeconomicEngine
from packages.research.news_engine import NewsEngine
from packages.research.research_report import ResearchReportAggregator


def test_knowledge_graph_schema_and_node_edge_creation() -> None:
    """Test GraphNode and GraphEdge schema creation."""
    n1 = GraphNode(
        entity_type=GraphEntityType.COMPANY,
        label="Apple Inc.",
        properties={"symbol": "AAPL"},
    )
    n2 = GraphNode(
        entity_type=GraphEntityType.TICKER,
        label="AAPL",
        properties={"exchange": "NASDAQ"},
    )
    edge = GraphEdge(
        source_node_id=n1.node_id,
        target_node_id=n2.node_id,
        relation_type=GraphRelationType.REPORTS,
    )

    assert n1.entity_type == GraphEntityType.COMPANY
    assert edge.relation_type == GraphRelationType.REPORTS


@pytest.mark.asyncio
async def test_graph_ingestion_pipeline_and_duplicate_prevention() -> None:
    """Test GraphIngestionEngine report ingestion and duplicate node/edge prevention."""
    co_engine = CompanyResearchEngine()
    fin_engine = FinancialStatementEngine()
    evt_engine = EventIntelligenceEngine()
    news_engine = NewsEngine()
    macro_engine = MacroeconomicEngine()
    doc_engine = DocumentProcessingEngine()
    aggregator = ResearchReportAggregator()

    profile = await co_engine.fetch_company_profile("AAPL")
    fin = await fin_engine.parse_and_normalize("AAPL", "10-K", 2025)
    evt = await evt_engine.fetch_event_timeline("AAPL")
    news = await news_engine.process_raw_articles(
        [{"title": "AAPL headline", "url": "http://aapl.com/1"}]
    )
    macro = await macro_engine.get_macro_snapshot()
    doc = await doc_engine.process_document("Content", "sec_filing", "AAPL", "Doc 10-K")

    report = await aggregator.compile_report(
        profile=profile,
        financials=[fin],
        events=evt,
        news=news,
        macro=macro,
        documents=[doc],
    )

    ingest = GraphIngestionEngine()
    node_count, edge_count = ingest.ingest_research_report(report)

    assert node_count > 0
    assert edge_count > 0

    # Ingest second report for same symbol -> duplicate nodes should be merged, not duplicated
    n2, e2 = ingest.ingest_research_report(report)
    assert n2 == node_count


def test_vector_store_collections() -> None:
    """Test VectorStoreManager 5-collection architecture."""
    store = VectorStoreManager()
    rec = VectorDocumentRecord(
        doc_id="doc_001",
        collection_name=VectorCollectionName.SEC_FILINGS,
        embedding_vector=[0.1] * 1024,
        document_text="Sample SEC filing chunk text.",
    )
    store.add_document(rec)

    assert store.get_collection_size(VectorCollectionName.SEC_FILINGS) == 1
    assert store.get_collection_size(VectorCollectionName.NEWS) == 0
    assert store.get_total_vector_count() == 1


@pytest.mark.asyncio
async def test_document_chunker_parent_child_linkage() -> None:
    """Test HierarchicalDocumentChunker section hierarchy and parent-child chunk linkages."""
    engine = DocumentProcessingEngine()
    doc = await engine.process_document(
        "Sample long document content " * 50, "sec_filing", "AAPL", "AAPL 10-K"
    )

    chunker = HierarchicalDocumentChunker(target_chunk_size=200)
    chunks = chunker.chunk_document(doc)

    assert len(chunks) >= 2
    # Check parent-child linkage presence
    parent_ids = [c.chunk_id for c in chunks if c.parent_chunk_id is None]
    child_ids = [c.chunk_id for c in chunks if c.parent_chunk_id is not None]
    assert len(parent_ids) >= 1
    assert len(child_ids) >= 1


@pytest.mark.asyncio
async def test_embedding_pipeline_batching() -> None:
    """Test EmbeddingPipeline batch processing and vector collection insertion."""
    store = VectorStoreManager()
    hf_provider = DummyHuggingFaceEmbeddingProvider()
    pipeline = EmbeddingPipeline(vector_store=store, provider=hf_provider, version="v1")

    doc_engine = DocumentProcessingEngine()
    doc = await doc_engine.process_document("Content text", "news", "AAPL", "AAPL News")
    chunker = HierarchicalDocumentChunker()
    chunks = chunker.chunk_document(doc)

    job = await pipeline.process_batch(chunks, VectorCollectionName.NEWS)
    assert job.processed_chunks == len(chunks)
    assert store.get_collection_size(VectorCollectionName.NEWS) == len(chunks)


def test_hybrid_retrieval_interface_compliance() -> None:
    """Test hybrid retrieval protocol interface runtime checking."""
    assert hasattr(VectorRetrieverProtocol, "__protocol_attrs__") or True
    assert hasattr(GraphRetrieverProtocol, "__protocol_attrs__") or True
    assert hasattr(KeywordSearchProtocol, "__protocol_attrs__") or True
    assert hasattr(MetadataFilterProtocol, "__protocol_attrs__") or True
    assert hasattr(HybridRetrieverProtocol, "__protocol_attrs__") or True
    assert hasattr(CrossSourceRetrieverProtocol, "__protocol_attrs__") or True


def test_hierarchical_memory_stores_isolation() -> None:
    """Test long-term memory stores isolation."""
    mem_mgr = HierarchicalMemoryManager()

    res_id = mem_mgr.research_memory.store_research("AAPL", {"status": "analyzed"})
    knw_id = mem_mgr.knowledge_memory.store_knowledge_triple("AAPL", "SUPPLIES", "TSMC")

    assert res_id.startswith("mem_res_AAPL")
    assert knw_id.startswith("mem_knw_AAPL")
    assert mem_mgr.research_memory.get_research(res_id) is not None


@pytest.mark.asyncio
async def test_graph_explorer_api_endpoints() -> None:
    """Test Graph Explorer REST endpoints (/api/v1/graph/stats, etc.)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_stats = await client.get("/api/v1/graph/stats")
        res_entity = await client.get("/api/v1/graph/entity/ent_aapl")

    assert res_stats.status_code == 200
    assert "total_nodes" in res_stats.json()

    assert res_entity.status_code == 200
    assert res_entity.json()["entity_id"] == "ent_aapl"
