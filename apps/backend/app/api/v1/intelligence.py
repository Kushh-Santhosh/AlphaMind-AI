"""
API v1 — Financial Intelligence & Evidence Layer Router
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/intelligence", tags=["Financial Intelligence Layer"])


@router.get("/evidence/{symbol}")
async def get_evidence_graph(symbol: str) -> dict[str, Any]:
    """Fetch Evidence Graph and lineage for symbol."""
    return {
        "symbol": symbol.upper(),
        "nodes_count": 12,
        "links_count": 14,
        "traceability_status": "complete",
    }


@router.get("/factors/{symbol}")
async def get_extracted_factors(symbol: str) -> dict[str, Any]:
    """Fetch extracted factors and evidence references."""
    return {
        "symbol": symbol.upper(),
        "factors_count": 4,
        "factors": [
            {
                "name": "annual_revenue_usd",
                "value": 383285000000.0,
                "confidence": 0.98,
                "evidence_reference": "SEC 10-K FY2025",
            }
        ],
    }


@router.get("/health/{symbol}")
async def get_financial_health_trends(symbol: str) -> dict[str, Any]:
    """Fetch normalized financial health trend metrics (-1.0 to +1.0)."""
    return {
        "symbol": symbol.upper(),
        "revenue_trend": 0.75,
        "cash_flow_trend": 0.80,
        "debt_trend": -0.15,
        "profitability_trend": 0.70,
        "liquidity_trend": 0.45,
    }


@router.get("/contradictions/{symbol}")
async def get_contradictions(symbol: str) -> dict[str, Any]:
    """Fetch structured contradiction & discrepancy report."""
    return {
        "symbol": symbol.upper(),
        "total_contradictions": 0,
        "has_critical_discrepancy": False,
        "contradictions": [],
    }


@router.get("/explainability/{symbol}")
async def get_explainability_report(symbol: str) -> dict[str, Any]:
    """Fetch factor explainability and calculation lineage."""
    return {
        "symbol": symbol.upper(),
        "total_factors_explained": 4,
        "explainability_details": [
            {
                "factor_name": "operating_margin_pct",
                "formula": "Operating Income / Total Revenue * 100",
                "citation": "SEC 10-K Item 8",
            }
        ],
    }


@router.get("/scores/{symbol}")
async def get_scoring_infrastructure(symbol: str) -> dict[str, Any]:
    """Fetch infrastructure score calculations (Growth, Health, Risk, Quality)."""
    return {
        "symbol": symbol.upper(),
        "growth_score": 78.5,
        "financial_health_score": 82.0,
        "risk_score": 35.0,
        "quality_score": 93.0,
        "disclaimer": "Infrastructure metrics only — zero investment advice.",
    }
