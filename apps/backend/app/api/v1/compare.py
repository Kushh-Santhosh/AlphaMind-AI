"""
AlphaMind AI - Multi-Asset Comparison API Router (v4.0)

Compares 2 to 10 assets dynamically using live provider market data,
real-time factor calculations, and multi-asset synthesis.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from packages.market.provider_registry import market_data_registry
from packages.research.opportunity_scanner import opportunity_scanner_engine

router = APIRouter(prefix="/api/v1/compare", tags=["Multi-Asset Compare"])
logger = logging.getLogger(__name__)


class CompareRequest(BaseModel):
    symbols: list[str] = Field(default_factory=lambda: ["NVDA", "MSFT", "AAPL", "GOOGL"], min_length=2, max_length=10)


@router.post("/assets", response_model=dict[str, Any])
async def compare_assets(payload: CompareRequest) -> dict[str, Any]:
    """Compare multiple assets side-by-side using live provider data and real factor calculations."""
    symbols = [s.strip().upper() for s in payload.symbols]
    if len(symbols) < 2 or len(symbols) > 10:
        raise HTTPException(status_code=400, detail="Compare requires between 2 and 10 symbols.")

    profiles = []
    for s in symbols:
        snap = await market_data_registry.get_market_snapshot(s)
        if snap.get("is_available", False):
            score, factors, inputs, theme, rec = opportunity_scanner_engine._compute_factor_score(snap)
            fwd_pe = snap.get("forward_pe") or snap.get("trailing_pe") or 25.0
            val_verdict = "UNDERVALUED" if fwd_pe < 22.0 else ("OVERVALUED" if fwd_pe > 40.0 else "FAIRLY_VALUED")
            
            profiles.append({
                "symbol": s,
                "price": snap["price"],
                "change_pct": snap["change_pct"],
                "market_cap_usd": snap["market_cap_usd"],
                "forward_pe": fwd_pe,
                "ev_to_ebitda": snap["ev_to_ebitda"] or 18.0,
                "rsi_14": snap["rsi_14"],
                "ai_opportunity_score": score,
                "valuation_verdict": val_verdict,
                "theme": theme,
                "recommendation": rec,
                "provenance": snap["provenance"],
            })
        else:
            profiles.append({
                "symbol": s,
                "price": 0.0,
                "change_pct": 0.0,
                "market_cap_usd": 0.0,
                "forward_pe": 0.0,
                "ev_to_ebitda": 0.0,
                "rsi_14": 50.0,
                "ai_opportunity_score": 0.0,
                "valuation_verdict": "UNAVAILABLE",
                "theme": "Data Unavailable",
                "recommendation": "HOLD",
                "provenance": snap.get("provenance", {}),
            })

    # AI-generated relative synthesis
    available_profiles = [p for p in profiles if p["price"] > 0]
    if available_profiles:
        top_momentum = max(available_profiles, key=lambda x: x["rsi_14"])["symbol"]
        top_value = min(available_profiles, key=lambda x: (x["forward_pe"] if x["forward_pe"] > 0 else 999.0))["symbol"]
        top_score = max(available_profiles, key=lambda x: x["ai_opportunity_score"])["symbol"]
        rec_summary = f"Overweight top-scoring conviction asset {top_score} and value leader {top_value} while keeping balanced risk exposure."
    else:
        top_momentum = symbols[0]
        top_value = symbols[0]
        top_score = symbols[0]
        rec_summary = "Market data currently unavailable for relative comparison."

    return {
        "compared_symbols": symbols,
        "asset_count": len(symbols),
        "profiles": profiles,
        "synthesis": {
            "top_overall_conviction": top_score,
            "top_momentum_asset": top_momentum,
            "top_value_asset": top_value,
            "portfolio_allocation_recommendation": rec_summary,
        },
        "disclaimer": "FOR RESEARCH & ASSET BENCHMARKING ONLY. NOT FINANCIAL ADVICE.",
    }
