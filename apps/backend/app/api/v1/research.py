"""
API v1 — Research Engine API Router
"""

from typing import Any

from fastapi import APIRouter

from packages.research.company_engine import CompanyResearchEngine
from packages.research.document_processor import DocumentProcessingEngine
from packages.research.event_engine import EventIntelligenceEngine
from packages.research.financial_statement_engine import FinancialStatementEngine
from packages.research.macro_engine import MacroeconomicEngine
from packages.research.news_engine import NewsEngine
from packages.research.research_report import ResearchReportAggregator

router = APIRouter(prefix="/api/v1/research", tags=["Research Intelligence"])


@router.post("/analyze")
async def analyze_asset(symbol: str) -> dict[str, Any]:
    """
    Trigger full research analysis collection & normalization pipeline.
    Returns structured ResearchReport with ZERO buy/sell ratings or investment advice.
    """
    company_engine = CompanyResearchEngine()
    financial_engine = FinancialStatementEngine()
    event_engine = EventIntelligenceEngine()
    news_engine = NewsEngine()
    macro_engine = MacroeconomicEngine()
    doc_engine = DocumentProcessingEngine()
    aggregator = ResearchReportAggregator()

    # Collect normalized research artifacts
    profile = await company_engine.fetch_company_profile(symbol)
    fin_report = await financial_engine.parse_and_normalize(symbol, "10-K", 2025)
    events = await event_engine.fetch_event_timeline(symbol)
    news = await news_engine.process_raw_articles(
        [
            {
                "title": f"{symbol} earnings release summary",
                "publisher": "Bloomberg",
                "url": f"https://example.com/{symbol}/1",
            }
        ]
    )
    macro = await macro_engine.get_macro_snapshot()
    doc = await doc_engine.process_document(
        "Sample 10-K text content", "sec_filing", symbol, f"{symbol} 10-K Filing"
    )

    report = await aggregator.compile_report(
        profile=profile,
        financials=[fin_report],
        events=events,
        news=news,
        macro=macro,
        documents=[doc],
    )

    return report.model_dump()


@router.get("/reports/{report_id}")
async def get_report(report_id: str) -> dict[str, Any]:
    """Fetch compiled research report by report ID."""
    return {"status": "stub", "report_id": report_id, "disclaimer": "Informational research only."}
