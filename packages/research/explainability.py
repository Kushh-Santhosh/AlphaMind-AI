"""
AlphaMind AI - Explainability & Lineage Audit Engine

Generates explainability reports for extracted factors, ensuring 100% calculation transparency
and direct citation mapping to source documents and Knowledge Graph entities.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from packages.research.factor_extractor import ExtractedFactor

logger = logging.getLogger(__name__)


class FactorExplainabilityDetail(BaseModel):
    factor_name: str
    factor_value: Any
    confidence_score: float
    citation_source: str
    calculation_formula_lineage: str
    supporting_document_ids: list[str] = Field(default_factory=list)
    related_entity_ids: list[str] = Field(default_factory=list)


class ExplainabilityReport(BaseModel):
    symbol: str
    total_factors_explained: int
    explainability_details: list[FactorExplainabilityDetail] = Field(default_factory=list)


class ExplainabilityEngine:
    """
    Engine formatting human-readable & audit-ready explainability details for every research factor.
    """

    def generate_explainability_report(
        self, symbol: str, factors: list[ExtractedFactor]
    ) -> ExplainabilityReport:
        """Generate audit-ready explainability report for extracted factors."""
        logger.info("Generating explainability audit report for '%s'", symbol)

        details: list[FactorExplainabilityDetail] = []
        for factor in factors:
            details.append(
                FactorExplainabilityDetail(
                    factor_name=factor.factor_name,
                    factor_value=factor.factor_value,
                    confidence_score=factor.confidence,
                    citation_source=factor.evidence_reference,
                    calculation_formula_lineage=factor.calculation_lineage,
                    supporting_document_ids=factor.related_doc_ids,
                    related_entity_ids=factor.related_entity_ids,
                )
            )

        return ExplainabilityReport(
            symbol=symbol,
            total_factors_explained=len(details),
            explainability_details=details,
        )
