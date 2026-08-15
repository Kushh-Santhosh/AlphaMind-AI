"""
AlphaMind AI - Asset Universe Discovery API Router
Exposes multi-asset universes (US, Indian, Global ETFs, Crypto) and candidate screening.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from packages.market.universe_engine import AssetUniverseEngine

router = APIRouter(prefix="/api/v1/universe", tags=["Asset Universe"])
_engine = AssetUniverseEngine()


@router.get("/categories")
async def get_universe_categories() -> dict[str, Any]:
    """List available asset universe classes."""
    return {"categories": _engine.list_universes()}


@router.get("/securities")
async def get_securities(
    category: str | None = Query(default=None, description="Universe category like US_EQUITIES, INDIAN_EQUITIES, GLOBAL_ETFS, CRYPTO"),
    status: str | None = Query(default=None, description="Lifecycle status like discovered, screened, researched, deeply_analyzed"),
    sector: str | None = Query(default=None, description="Sector filter"),
) -> dict[str, Any]:
    """Retrieve screened and discovered securities across investment universes."""
    securities = _engine.get_securities(universe=category, status=status, sector=sector)
    return {
        "total_count": len(securities),
        "securities": securities,
    }
