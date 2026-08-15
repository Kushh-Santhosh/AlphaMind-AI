"""
Research Engine Test Suite — Company Engine, SEC Financial Parsers, News Normalization,
Macro Engine, Corporate Events, Document Processor, Entity Resolver & Research Report.
"""

from __future__ import annotations

import pytest

from packages.research.company_engine import CompanyResearchEngine
from packages.research.document_processor import DocumentProcessingEngine
from packages.research.entity_resolver import EntityResolver
from packages.research.event_engine import EventIntelligenceEngine
from packages.research.financial_statement_engine import FinancialStatementEngine
from packages.research.macro_engine import MacroeconomicEngine
from packages.research.news_engine import NewsEngine
from packages.research.research_report import ResearchReportAggregator


@pytest.mark.asyncio
async def test_company_research_engine() -> None:
    """Test CompanyResearchEngine profile collection and normalization."""
    engine = CompanyResearchEngine()
    profile = await engine.fetch_company_profile("AAPL")

    assert profile.symbol == "AAPL"
    assert "Apple" in profile.company_name or "AAPL" in profile.company_name
    assert len(profile.executives) >= 2
    assert profile.share_structure is not None
    assert profile.share_structure.shares_outstanding > 0


@pytest.mark.asyncio
async def test_financial_statement_parser() -> None:
    """Test FinancialStatementEngine 10-K/10-Q XBRL parsing."""
    engine = FinancialStatementEngine()
    fin = await engine.parse_and_normalize("AAPL", "10-K", 2025)

    assert fin.symbol == "AAPL"
    assert fin.fiscal_year == 2025
    assert fin.income_statement.revenue > 100_000_000_000.0
    assert fin.balance_sheet.total_assets > 0
    assert fin.cash_flow_statement.free_cash_flow > 0
    assert "us-gaap:Revenues" in fin.xbrl_tags_normalized


@pytest.mark.asyncio
async def test_news_normalization_and_entity_extraction() -> None:
    """Test NewsEngine normalization, deduplication, entity extraction, and reliability scoring."""
    engine = NewsEngine()
    raw = [
        {
            "title": "AAPL Q2 Earnings Analysis",
            "publisher": "Bloomberg",
            "url": "https://bloomberg.com/1",
        },
        {
            "title": "AAPL Q2 Earnings Analysis",
            "publisher": "Bloomberg",
            "url": "https://bloomberg.com/1",
        },  # Duplicate
        {
            "title": "NVDA Supply Chain Expansion",
            "publisher": "Financial Times",
            "url": "https://ft.com/1",
        },
    ]

    articles = await engine.process_raw_articles(raw)
    assert len(articles) == 2  # Deduplicated
    assert articles[0].source_reliability_score >= 0.85
    assert "AAPL" in articles[0].entities_extracted
    assert articles[0].language == "en"


@pytest.mark.asyncio
async def test_macroeconomic_ingestion() -> None:
    """Test MacroeconomicEngine dataset aggregation."""
    engine = MacroeconomicEngine()
    macro = await engine.get_macro_snapshot()

    assert macro.fed_funds_rate == 5.25
    assert macro.cpi_yoy_pct == 2.8
    assert macro.yield_curve_spread_10y_2y == 0.35
    assert len(macro.observations) >= 3


@pytest.mark.asyncio
async def test_event_intelligence_timeline() -> None:
    """Test EventIntelligenceEngine structured corporate event timeline."""
    engine = EventIntelligenceEngine()
    timeline = await engine.fetch_event_timeline("NVDA")

    assert timeline.symbol == "NVDA"
    assert timeline.total_events >= 4
    event_types = [e.event_type for e in timeline.events]
    assert "earnings" in event_types
    assert "dividend" in event_types
    assert "insider" in event_types


@pytest.mark.asyncio
async def test_document_processing_sections_and_tables() -> None:
    """Test DocumentProcessingEngine section & table extraction."""
    engine = DocumentProcessingEngine()
    doc = await engine.process_document("Raw 10-K Content", "sec_filing", "MSFT", "MSFT 10-K")

    assert doc.symbol == "MSFT"
    assert doc.doc_type == "sec_filing"
    assert len(doc.sections) >= 2
    assert len(doc.tables) >= 1
    assert doc.tables[0].headers == ["Metric", "FY2025", "FY2024"]


def test_entity_resolution_alias_mapping() -> None:
    """Test EntityResolver alias resolution and duplicate prevention."""
    resolver = EntityResolver()

    e1 = resolver.resolve_entity("Apple Inc")
    e2 = resolver.resolve_entity("AAPL US")
    e3 = resolver.resolve_entity("NVIDIA")

    assert e1 is not None and e2 is not None and e3 is not None
    assert e1.entity_id == "ent_company_aapl"
    assert e2.entity_id == "ent_company_aapl"  # Same canonical entity
    assert e3.canonical_name == "NVIDIA Corporation"


@pytest.mark.asyncio
async def test_research_report_aggregation_and_disclaimer() -> None:
    """Test ResearchReportAggregator compilation and SEC/FINRA disclaimer check."""
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
        [{"title": "AAPL news", "url": "http://aapl.com"}]
    )
    macro = await macro_engine.get_macro_snapshot()
    doc = await doc_engine.process_document("content", "pdf", "AAPL", "Doc")

    report = await aggregator.compile_report(
        profile=profile,
        financials=[fin],
        events=evt,
        news=news,
        macro=macro,
        documents=[doc],
    )

    assert report.symbol == "AAPL"
    assert report.confidence_metadata.overall_confidence_score > 0.90
    assert len(report.evidence_references) >= 2
    assert "DISCLAIMER" in report.disclaimer
    assert "investment advice" in report.disclaimer.lower()
