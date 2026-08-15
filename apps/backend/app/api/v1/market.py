"""
AlphaMind AI - Real Market Data API Router (v4.0)

Exposes real-time quotes, OHLCV historical bars, multi-asset symbol search,
and macroeconomic indicators backed by live providers with strict provenance metadata.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from packages.market.provider_registry import market_data_registry
from packages.market.universe_engine import asset_universe_engine

router = APIRouter(prefix="/api/v1/market", tags=["Market Data"])
logger = logging.getLogger(__name__)


@router.get("/search")
async def search_assets(query: str = Query(..., min_length=1)) -> dict[str, Any]:
    """Multi-asset symbol search across active universes."""
    q = query.strip().upper()
    all_sec = asset_universe_engine.get_securities()
    matches = [
        s for s in all_sec
        if q in s["symbol"].upper() or q in s["name"].upper() or q in s["sector"].upper()
    ]
    return {
        "query": query,
        "count": len(matches),
        "results": matches[:20],
    }


@router.get("/quote/{symbol}")
async def get_quote(symbol: str) -> dict[str, Any]:
    """Fetch latest quote and data provenance for a symbol."""
    snap = await market_data_registry.get_market_snapshot(symbol)
    if not snap.get("is_available", False):
        raise HTTPException(
            status_code=404,
            detail=f"Market data for symbol '{symbol}' is unavailable from provider: {snap.get('error_message')}",
        )
    return snap


@router.get("/snapshot/{symbol}")
async def get_market_snapshot(symbol: str) -> dict[str, Any]:
    """Fetch comprehensive market snapshot including technicals and fundamentals."""
    return await market_data_registry.get_market_snapshot(symbol)


@router.get("/bars/{symbol}")
async def get_bars(
    symbol: str,
    period: str = Query("1y", description="Data period (1mo, 3mo, 6mo, 1y, 2y, 5y)"),
    interval: str = Query("1d", description="Bar interval (1d, 1wk, 1mo)"),
) -> dict[str, Any]:
    """Fetch historical OHLCV price bars for charting and backtesting."""
    hist = await market_data_registry.get_historical_ohlcv(symbol, period=period, interval=interval)
    if hist.empty:
        raise HTTPException(status_code=404, detail=f"No historical price bars found for symbol '{symbol}'.")

    bars = []
    for dt, row in hist.iterrows():
        ts_str = dt.isoformat() if hasattr(dt, "isoformat") else str(dt)
        bars.append({
            "timestamp": ts_str,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": float(row["Volume"]),
        })

    return {
        "symbol": symbol.upper(),
        "period": period,
        "interval": interval,
        "count": len(bars),
        "bars": bars,
    }


@router.get("/macro")
async def get_macroeconomic_data() -> dict[str, Any]:
    """Fetch live macroeconomic series and business cycle phase."""
    return await market_data_registry.get_macroeconomic_series()
