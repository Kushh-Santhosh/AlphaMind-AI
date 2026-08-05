"""
API v1 — Market Data Router (Scaffold)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/market", tags=["Market Data"])


@router.get("/search")
async def search_assets(query: str) -> dict:
    """Multi-asset symbol search. Implementation pending Milestone 4."""
    return {"status": "stub", "query": query}


@router.get("/bars/{symbol}")
async def get_bars(symbol: str, timeframe: str = "1D") -> dict:
    """Fetch OHLCV price bars. Implementation pending Milestone 4."""
    return {"status": "stub", "symbol": symbol, "timeframe": timeframe}


@router.get("/quote/{symbol}")
async def get_quote(symbol: str) -> dict:
    """Fetch latest real-time quote. Implementation pending Milestone 4."""
    return {"status": "stub", "symbol": symbol}
