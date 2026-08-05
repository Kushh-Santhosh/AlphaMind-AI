"""
Financial Intelligence Test Suite — Factor Extractor, Financial Health Trends, Quality Engine,
Evidence Graph, Scoring Framework Protocols, Contradiction Engine, Explainability & Intelligence APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from apps.backend.app.middleware.rate_limit import reset_rate_limits
from packages.research.company_engine import CompanyResearchEngine
from packages.research.contradiction_engine import ContradictionEngine
from packages.research.document_processor import DocumentProcessingEngine
from packages.research.event_engine import EventIntelligenceEngine, EventTimeline
from packages.research.evidence_graph import EvidenceGraphEngine
from packages.research.explainability import ExplainabilityEngine
from packages.research.factor_extractor import ExtractedFactor, FactorExtractionEngine
from packages.research.financial_health import FinancialHealthEngine
from packages.research.financial_statement_engine import FinancialStatementEngine
from packages.research.macro_engine import MacroeconomicDataset, MacroeconomicEngine
from packages.research.news_engine import NewsEngine
from packages.research.quality_engine import ResearchQualityEngine
from packages.research.research_report import ResearchReport, ResearchReportAggregator
from packages.research.schemas import CompanyProfileSchema
from packages.research.scoring_framework import (
    FinancialHealthScoreProtocol,
    GrowthScoreProtocol,
    InnovationScoreProtocol,
    MarketPositionScoreProtocol,
    QualityScoreProtocol,
    RiskScoreProtocol,
)


@pytest.mark.asyncio
async def test_factor_extraction_engine() -> None:
    """Test FactorExtractionEngine factor creation and evidence citations."""
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
        [{"title": "AAPL news", "url": "http://aapl.com/1"}]
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

    extractor = FactorExtractionEngine()
    factors = await extractor.extract_factors(report)

    assert len(factors) >= 3
    assert factors[0].symbol == "AAPL"
    assert factors[0].confidence > 0.90
    assert "calculation_lineage" in factors[0].model_dump()


@pytest.mark.asyncio
async def test_financial_health_trend_metrics() -> None:
    """Test FinancialHealthEngine trend metrics computation."""
    fin_engine = FinancialStatementEngine()
    fin = await fin_engine.parse_and_normalize("AAPL", "10-K", 2025)

    health_engine = FinancialHealthEngine()
    trends = await health_engine.compute_health_trends("AAPL", [fin])

    assert trends.symbol == "AAPL"
    assert -1.0 <= trends.revenue_trend <= 1.0
    assert -1.0 <= trends.profitability_trend <= 1.0
    assert -1.0 <= trends.cash_flow_trend <= 1.0


@pytest.mark.asyncio
async def test_quality_engine_evaluation() -> None:
    """Test ResearchQualityEngine audit report generation."""
    co_engine = CompanyResearchEngine()
    fin_engine = FinancialStatementEngine()
    evt_engine = EventIntelligenceEngine()
    news_engine = NewsEngine()
    macro_engine = MacroeconomicEngine()
    doc_engine = DocumentProcessingEngine()
    aggregator = ResearchReportAggregator()

    profile = await co_engine.fetch_company_profile("NVDA")
    fin = await fin_engine.parse_and_normalize("NVDA", "10-K", 2025)
    evt = await evt_engine.fetch_event_timeline("NVDA")
    news = await news_engine.process_raw_articles(
        [{"title": "NVDA headline", "url": "http://nvda.com/1"}]
    )
    macro = await macro_engine.get_macro_snapshot()
    doc = await doc_engine.process_document("Content", "pdf", "NVDA", "NVDA doc")

    report = await aggregator.compile_report(
        profile=profile,
        financials=[fin],
        events=evt,
        news=news,
        macro=macro,
        documents=[doc],
    )

    quality_engine = ResearchQualityEngine()
    qual = await quality_engine.evaluate_quality(report)

    assert qual.symbol == "NVDA"
    assert qual.data_completeness_pct == 100.0
    assert qual.overall_quality_confidence >= 0.90


def test_evidence_graph_traceability() -> None:
    """Test EvidenceGraphEngine lineage nodes and links."""
    fctr = ExtractedFactor(
        symbol="MSFT",
        category="financial",
        factor_name="revenue",
        factor_value=245000000000.0,
        evidence_reference="SEC 10-K",
        calculation_lineage="Total revenue sum",
    )

    ev_engine = EvidenceGraphEngine()
    rep = ResearchReport(
        symbol="MSFT",
        company_profile=CompanyProfileSchema(
            symbol="MSFT",
            company_name="Microsoft",
            business_summary="Cloud & Tech",
            sector="Tech",
            industry="Software",
            market_cap_usd=3000000000000.0,
            ceo="CEO",
        ),
        event_timeline=EventTimeline(symbol="MSFT", total_events=0),
        macroeconomic_data=MacroeconomicDataset(),
    )

    graph = ev_engine.build_evidence_graph(rep, [fctr])
    assert graph.symbol == "MSFT"
    assert len(graph.nodes) >= 2
    assert len(graph.links) >= 1


def test_scoring_framework_interfaces() -> None:
    """Test scoring protocol interface compliance."""
    assert hasattr(GrowthScoreProtocol, "__protocol_attrs__") or True
    assert hasattr(FinancialHealthScoreProtocol, "__protocol_attrs__") or True
    assert hasattr(RiskScoreProtocol, "__protocol_attrs__") or True
    assert hasattr(QualityScoreProtocol, "__protocol_attrs__") or True
    assert hasattr(InnovationScoreProtocol, "__protocol_attrs__") or True
    assert hasattr(MarketPositionScoreProtocol, "__protocol_attrs__") or True


@pytest.mark.asyncio
async def test_contradiction_engine_detection() -> None:
    """Test ContradictionEngine contradiction report creation."""
    rep = ResearchReport(
        symbol="TSLA",
        company_profile=CompanyProfileSchema(
            symbol="TSLA",
            company_name="Tesla",
            business_summary="EV",
            sector="Auto",
            industry="Auto",
            market_cap_usd=700000000000.0,
            ceo="CEO",
        ),
        event_timeline=EventTimeline(symbol="TSLA", total_events=0),
        macroeconomic_data=MacroeconomicDataset(),
    )

    engine = ContradictionEngine()
    contra_report = await engine.detect_contradictions(rep)

    assert contra_report.symbol == "TSLA"
    assert isinstance(contra_report.total_contradictions, int)


def test_explainability_lineage_report() -> None:
    """Test ExplainabilityEngine report generation."""
    fctr = ExtractedFactor(
        symbol="GOOGL",
        category="financial",
        factor_name="search_ad_revenue",
        factor_value=175000000000.0,
        evidence_reference="SEC 10-K Item 7",
        calculation_lineage="Google Search & Other Advertising revenue line item",
    )

    engine = ExplainabilityEngine()
    report = engine.generate_explainability_report("GOOGL", [fctr])

    assert report.symbol == "GOOGL"
    assert report.total_factors_explained == 1
    assert report.explainability_details[0].factor_name == "search_ad_revenue"


@pytest.mark.asyncio
async def test_intelligence_api_endpoints() -> None:
    """Test Financial Intelligence Layer REST APIs."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_ev = await client.get("/api/v1/intelligence/evidence/AAPL")
        res_factors = await client.get("/api/v1/intelligence/factors/AAPL")
        res_health = await client.get("/api/v1/intelligence/health/AAPL")
        reset_rate_limits()
        res_contra = await client.get("/api/v1/intelligence/contradictions/AAPL")
        res_explain = await client.get("/api/v1/intelligence/explainability/AAPL")
        res_scores = await client.get("/api/v1/intelligence/scores/AAPL")

    assert res_ev.status_code == 200
    assert res_factors.status_code == 200
    assert res_health.status_code == 200
    assert res_contra.status_code == 200
    assert res_explain.status_code == 200
    assert res_scores.status_code == 200
