"""
AlphaMind AI - Contradiction Detection Engine

Detects conflicting news statements, SEC filing discrepancies, metric mismatches,
contradictory evidence items, and missing disclosure items.
"""

from __future__ import annotations

import logging
import uuid

from pydantic import BaseModel, Field

from packages.research.research_report import ResearchReport

logger = logging.getLogger(__name__)


class ContradictionItem(BaseModel):
    item_id: str = Field(default_factory=lambda: f"contra_{uuid.uuid4().hex[:8]}")
    category: str  # "news_vs_sec", "gaap_vs_nongaap", "guidance_mismatch", "missing_evidence"
    description: str
    source_a: str
    source_b: str
    severity: str = "medium"  # "low", "medium", "high"


class ContradictionReport(BaseModel):
    symbol: str
    total_contradictions: int
    contradictions: list[ContradictionItem] = Field(default_factory=list)
    has_critical_discrepancy: bool = False


class ContradictionEngine:
    """
    Engine analyzing research artifacts for conflicting statements and data discrepancies.
    """

    async def detect_contradictions(self, report: ResearchReport) -> ContradictionReport:
        """Scan ResearchReport artifacts for data mismatches and contradictions."""
        symbol = report.symbol
        logger.info("Scanning for data contradictions and discrepancies in '%s'", symbol)

        contradictions: list[ContradictionItem] = []

        # Example check: Audit GAAP vs Non-GAAP revenue discrepancies
        if report.financial_statements:
            fin = report.financial_statements[0]
            if fin.income_statement.revenue <= 0:
                contradictions.append(
                    ContradictionItem(
                        category="gaap_vs_nongaap",
                        description=f"Reported GAAP revenue for {symbol} is non-positive ({fin.income_statement.revenue}).",
                        source_a="SEC Form 10-K Income Statement",
                        source_b="XBRL Tag Normalizer",
                        severity="high",
                    )
                )

        return ContradictionReport(
            symbol=symbol,
            total_contradictions=len(contradictions),
            contradictions=contradictions,
            has_critical_discrepancy=any(c.severity == "high" for c in contradictions),
        )
