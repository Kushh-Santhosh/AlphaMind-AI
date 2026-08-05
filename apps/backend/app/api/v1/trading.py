"""
API v1 — Portfolio, Prediction, Risk, Backtesting & Paper Trading Routers (Scaffolds)
"""

from fastapi import APIRouter

# Portfolio
portfolio_router = APIRouter(prefix="/api/v1/portfolio", tags=["Portfolio"])


@portfolio_router.get("/")
async def get_portfolio() -> dict:
    return {"status": "stub", "message": "Implementation pending Milestone 5."}


@portfolio_router.post("/optimize")
async def optimize_portfolio() -> dict:
    return {"status": "stub", "message": "Implementation pending Milestone 5."}


# Prediction
prediction_router = APIRouter(prefix="/api/v1/prediction", tags=["Prediction"])


@prediction_router.post("/simulate")
async def simulate_monte_carlo() -> dict:
    return {"status": "stub", "message": "Implementation pending Milestone 5."}


# Risk
risk_router = APIRouter(prefix="/api/v1/risk", tags=["Risk"])


@risk_router.get("/{symbol}")
async def get_risk_metrics(symbol: str) -> dict:
    return {"status": "stub", "symbol": symbol}


# Backtesting
backtest_router = APIRouter(prefix="/api/v1/backtest", tags=["Backtesting"])


@backtest_router.post("/run")
async def run_backtest() -> dict:
    return {"status": "stub", "message": "Implementation pending Milestone 5."}


# Paper Trading
paper_trading_router = APIRouter(prefix="/api/v1/trading", tags=["Paper Trading"])


@paper_trading_router.post("/orders")
async def submit_paper_order() -> dict:
    return {"status": "stub", "message": "Implementation pending Milestone 5."}


@paper_trading_router.get("/orders")
async def list_paper_orders() -> dict:
    return {"status": "stub", "message": "Implementation pending Milestone 5."}
