"""
AlphaMind AI - AI Opportunity Scanner API Router
Exposes continuous multi-factor opportunity scans with transparent factor rankings.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from packages.research.opportunity_scanner import OpportunityScannerEngine

router = APIRouter(prefix="/api/v1/scanner", tags=["Opportunity Scanner"])
_scanner = OpportunityScannerEngine()


@router.get("/opportunities")
async def get_opportunities(
    min_score: float = Query(default=65.0, ge=0.0, le=100.0, description="Minimum Opportunity Score"),
    asset_class: str | None = Query(default=None, description="Asset class filter"),
    theme: str | None = Query(default=None, description="Theme filter like Momentum Breakout, Undervalued Growth, etc."),
) -> dict[str, Any]:
    """Scan and retrieve ranked opportunities across supported universes."""
    opportunities = await _scanner.scan_opportunities(
        min_score=min_score,
        asset_class=asset_class,
        theme_filter=theme,
    )
    return {
        "count": len(opportunities),
        "min_score_filter": min_score,
        "opportunities": opportunities,
    }
