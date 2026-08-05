"""API v1 Package — Router Registry."""

from apps.backend.app.api.v1.admin import router as admin_router
from apps.backend.app.api.v1.analyst import router as analyst_router
from apps.backend.app.api.v1.auth import router as auth_router
from apps.backend.app.api.v1.briefings import router as briefings_router
from apps.backend.app.api.v1.broker import router as broker_router
from apps.backend.app.api.v1.dashboards import router as dashboards_router
from apps.backend.app.api.v1.evaluation import router as evaluation_router
from apps.backend.app.api.v1.health import router as health_router
from apps.backend.app.api.v1.market import router as market_router
from apps.backend.app.api.v1.mission_control import router as mission_control_router
from apps.backend.app.api.v1.os_core import router as os_core_router
from apps.backend.app.api.v1.portfolio import router as portfolio_router
from apps.backend.app.api.v1.prediction import router as prediction_router
from apps.backend.app.api.v1.reasoning import router as reasoning_router
from apps.backend.app.api.v1.research import router as research_router
from apps.backend.app.api.v1.simulation import router as simulation_router
from apps.backend.app.api.v1.trading import (
    backtest_router,
    paper_trading_router,
    risk_router,
)
from apps.backend.app.api.v1.v2_funds import router as v2_funds_router
from apps.backend.app.api.v1.workspace import router as workspace_router

__all__ = [
    "health_router",
    "auth_router",
    "market_router",
    "research_router",
    "prediction_router",
    "portfolio_router",
    "evaluation_router",
    "analyst_router",
    "dashboards_router",
    "simulation_router",
    "broker_router",
    "admin_router",
    "os_core_router",
    "reasoning_router",
    "briefings_router",
    "workspace_router",
    "mission_control_router",
    "v2_funds_router",
    "risk_router",
    "backtest_router",
    "paper_trading_router",
]
