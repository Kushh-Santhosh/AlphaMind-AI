"""
API v1 — Continuous Evaluation & Backtesting Platform Router
"""

from typing import Any

from fastapi import APIRouter

from packages.research.backtest_engine import BacktestEngine, BacktestValidationMode
from packages.research.drift_engine import ModelDriftEngine
from packages.research.forecast_evaluator import ForecastEvaluatorEngine
from packages.research.leaderboard import LeaderboardEngine
from packages.research.model_comparator import ModelComparisonEngine
from packages.research.retraining_workflow import RetrainingWorkflowEngine
from packages.research.strategy_evaluator import StrategyEvaluatorEngine

router = APIRouter(prefix="/api/v1/evaluation", tags=["Continuous Evaluation Platform"])

backtest_engine = BacktestEngine()
forecast_evaluator = ForecastEvaluatorEngine()
comparator_engine = ModelComparisonEngine()
strategy_evaluator = StrategyEvaluatorEngine()
drift_engine = ModelDriftEngine()
leaderboard_engine = LeaderboardEngine()
retraining_engine = RetrainingWorkflowEngine()


@router.post("/backtest")
async def run_backtest(
    strategy_name: str = "Multi-Factor Quantitative Strategy",
    symbol: str = "AAPL",
    validation_mode: BacktestValidationMode = BacktestValidationMode.WALK_FORWARD_VALIDATION,
) -> dict[str, Any]:
    """Execute modular backtest with walk-forward validation and historical replay."""
    res = backtest_engine.run_backtest(strategy_name, symbol, validation_mode)
    return res.model_dump()


@router.get("/metrics")
async def get_forecast_evaluation_metrics(
    model_id: str = "tft_v1", symbol: str = "AAPL"
) -> dict[str, Any]:
    """Fetch forecast evaluation metrics (MAE, RMSE, Brier, Directional Accuracy, ECE)."""
    res = forecast_evaluator.evaluate_forecast_accuracy(model_id, symbol)
    return res.model_dump()


@router.get("/leaderboard")
async def get_model_leaderboard() -> dict[str, Any]:
    """Fetch global predictive model leaderboard rankings."""
    res = leaderboard_engine.get_leaderboard()
    return res.model_dump()


@router.get("/drift")
async def audit_model_drift(model_id: str = "tft_v1") -> dict[str, Any]:
    """Scan for statistical feature drift, prediction drift, and confidence calibration drift."""
    res = drift_engine.audit_model_drift(model_id)
    return res.model_dump()


@router.post("/retrain")
async def trigger_model_retraining(
    model_id: str = "tft_v1", trigger_type: str = "manual"
) -> dict[str, Any]:
    """Trigger retraining workflow and Champion vs Challenger evaluation."""
    job = retraining_engine.trigger_retraining(model_id, trigger_type)
    return job.model_dump()


@router.get("/reports/{report_id}")
async def get_evaluation_report(report_id: str) -> dict[str, Any]:
    """Fetch compiled backtest and evaluation report."""
    comp = comparator_engine.compare_models()
    return {
        "report_id": report_id,
        "status": "completed",
        "model_comparison": comp.model_dump(),
    }
