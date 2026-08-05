"""
AlphaMind AI - Structured Factor Extraction Engine

Extracts structured quantitative and qualitative factors from Company Data,
Financial Statements, News, Events, Macro, Documents, and Knowledge Graph.
STRICT RULE: No price forecasting, trading signals, or buy/sell recommendations.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from pydantic import BaseModel, Field

from packages.research.research_report import ResearchReport

logger = logging.getLogger(__name__)


class ExtractedFactor(BaseModel):
    """Structured Factor Schema with complete evidence lineage."""

    factor_id: str = Field(default_factory=lambda: f"fctr_{uuid.uuid4().hex[:8]}")
    symbol: str
    category: str  # "financial", "macro", "event", "governance", "industry"
    factor_name: str
    factor_value: Any
    weight: float = 1.0
    timestamp_utc: float = Field(default_factory=time.time)
    confidence: float = 0.90  # 0.0 to 1.0
    evidence_reference: str
    calculation_lineage: str
    related_doc_ids: list[str] = Field(default_factory=list)
    related_entity_ids: list[str] = Field(default_factory=list)


class FactorExtractionEngine:
    """
    Engine extracting structured factors across multi-source research artifacts.
    """

    async def extract_factors(self, report: ResearchReport) -> list[ExtractedFactor]:
        """Extract structured factors from unified ResearchReport."""
        symbol = report.symbol
        logger.info("Extracting structured factors for symbol '%s'", symbol)

        factors: list[ExtractedFactor] = []

        # 1. Financial Statement Factors
        if report.financial_statements:
            fin = report.financial_statements[0]
            factors.append(
                ExtractedFactor(
                    symbol=symbol,
                    category="financial",
                    factor_name="annual_revenue_usd",
                    factor_value=fin.income_statement.revenue,
                    weight=1.0,
                    confidence=0.98,
                    evidence_reference=f"SEC 10-K FY{fin.fiscal_year} Income Statement",
                    calculation_lineage="Sum of GAAP top-line total revenues reported in SEC filing",
                    related_doc_ids=[d.doc_id for d in report.documents],
                    related_entity_ids=[report.company_profile.company_id],
                )
            )
            factors.append(
                ExtractedFactor(
                    symbol=symbol,
                    category="financial",
                    factor_name="operating_margin_pct",
                    factor_value=round(
                        (fin.income_statement.operating_income / fin.income_statement.revenue)
                        * 100.0,
                        2,
                    ),
                    weight=0.9,
                    confidence=0.95,
                    evidence_reference=f"SEC 10-K FY{fin.fiscal_year}",
                    calculation_lineage="Operating Income / Total Revenue * 100",
                    related_doc_ids=[d.doc_id for d in report.documents],
                )
            )

        # 2. Macro Factors
        factors.append(
            ExtractedFactor(
                symbol=symbol,
                category="macro",
                factor_name="fed_funds_effective_rate",
                factor_value=report.macroeconomic_data.fed_funds_rate,
                weight=0.8,
                confidence=0.99,
                evidence_reference="FRED St. Louis Fed API - FEDFUNDS",
                calculation_lineage="Latest Federal Reserve Target Rate",
            )
        )

        # 3. News Factors
        if report.news_articles:
            factors.append(
                ExtractedFactor(
                    symbol=symbol,
                    category="news",
                    factor_name="media_article_coverage_count",
                    factor_value=len(report.news_articles),
                    weight=0.5,
                    confidence=0.85,
                    evidence_reference="NewsAPI Feed Aggregator",
                    calculation_lineage="Total deduplicated news articles in window",
                )
            )

        logger.info("Extracted %d structured factors for '%s'.", len(factors), symbol)
        return factors
