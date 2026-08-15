"""
AlphaMind AI - FastAPI Application Gateway Entrypoint
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.backend.app.api.v1 import (
    admin_router,
    analyst_router,
    auth_router,
    backtest_router,
    backtest_v4_router,
    briefings_router,
    broker_router,
    compare_router,
    dashboards_router,
    debate_router,
    evaluation_router,
    health_router,
    market_router,
    mission_control_router,
    os_core_router,
    paper_trading_router,
    portfolio_router,
    prediction_router,
    providers_router,
    reasoning_router,
    research_router,
    risk_router,
    scanner_router,
    simulation_router,
    universe_router,
    v2_funds_router,
    workspace_router,
)
from apps.backend.app.api.v1.graph import router as graph_router
from apps.backend.app.api.v1.intelligence import router as intelligence_router
from apps.backend.app.api.v1.metrics import router as metrics_router
from apps.backend.app.api.v1.workflows import router as workflows_router
from apps.backend.app.core.config import settings
from apps.backend.app.middleware.disclaimer import DisclaimerMiddleware
from apps.backend.app.middleware.exception_handlers import register_exception_handlers
from apps.backend.app.middleware.rate_limit import RateLimitMiddleware


def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title="AlphaMind AI — Autonomous Research Gateway",
        description=(
            "Institutional-grade AI investment research and quantitative analytics API. "
            "All outputs are probabilistic and for informational purposes only."
        ),
        version="0.4.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Middleware registration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(DisclaimerMiddleware)

    # Exception handler registration
    register_exception_handlers(app)

    @app.get("/health", tags=["System"])
    async def root_health() -> dict[str, str]:
        """Root health check endpoint."""
        return {"status": "healthy", "service": "alphamind-backend", "version": "0.4.0"}

    # API Router registration
    app.include_router(health_router)
    app.include_router(metrics_router)
    app.include_router(workflows_router)
    app.include_router(graph_router)
    app.include_router(intelligence_router)
    app.include_router(prediction_router)
    app.include_router(portfolio_router)
    app.include_router(evaluation_router)
    app.include_router(analyst_router)
    app.include_router(dashboards_router)
    app.include_router(simulation_router)
    app.include_router(broker_router)
    app.include_router(admin_router)
    app.include_router(os_core_router)
    app.include_router(reasoning_router)
    app.include_router(briefings_router)
    app.include_router(workspace_router)
    app.include_router(mission_control_router)
    app.include_router(v2_funds_router)
    app.include_router(auth_router)
    app.include_router(market_router)
    app.include_router(research_router)
    app.include_router(risk_router)
    app.include_router(backtest_router)
    app.include_router(backtest_v4_router)
    app.include_router(paper_trading_router)
    app.include_router(debate_router)
    app.include_router(universe_router)
    app.include_router(scanner_router)
    app.include_router(compare_router)
    app.include_router(providers_router)

    return app


app = create_app()
