"""
Continuous Evaluation Platform Test Suite — Backtest Engine, Forecast Evaluator, Model Comparator,
Strategy Evaluator, Drift Engine, Model Leaderboard, Retraining Champion vs Challenger, and Evaluation APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.research.backtest_engine import BacktestEngine, BacktestValidationMode
from packages.research.drift_engine import ModelDriftEngine
from packages.research.forecast_evaluator import ForecastEvaluatorEngine
from packages.research.leaderboard import LeaderboardEngine
from packages.research.model_comparator import ModelComparisonEngine
from packages.research.retraining_workflow import ModelApprovalState, RetrainingWorkflowEngine
from packages.research.strategy_evaluator import StrategyEvaluatorEngine


def test_backtest_engine_walk_forward_validation() -> None:
    """Test BacktestEngine execution using Walk-Forward Validation."""
    engine = BacktestEngine()
    res = engine.run_backtest(
        "Quant Momentum", "AAPL", BacktestValidationMode.WALK_FORWARD_VALIDATION
    )

    assert res.strategy_name == "Quant Momentum"
    assert res.symbol == "AAPL"
    assert res.validation_mode == BacktestValidationMode.WALK_FORWARD_VALIDATION
    assert res.cumulative_return_pct > 0.0
    assert res.sharpe_ratio > 1.0
    assert "DISCLAIMER" in res.disclaimer


def test_forecast_evaluation_metrics() -> None:
    """Test ForecastEvaluatorEngine accuracy metrics calculation."""
    engine = ForecastEvaluatorEngine()
    metrics = engine.evaluate_forecast_accuracy("tft_v1", "NVDA")

    assert metrics.model_id == "tft_v1"
    assert metrics.symbol == "NVDA"
    assert metrics.directional_accuracy_pct > 50.0
    assert 0.0 <= metrics.brier_score <= 1.0
    assert metrics.coverage_pct >= 90.0


def test_model_comparison_across_asset_classes() -> None:
    """Test ModelComparisonEngine multi-model ranking across asset classes."""
    engine = ModelComparisonEngine()
    report = engine.compare_models()

    assert report.total_models_compared >= 9
    assert len(report.asset_class_breakdown) >= 4
    asset_classes = [a.asset_class for a in report.asset_class_breakdown]
    assert "Stocks" in asset_classes
    assert "ETFs" in asset_classes


def test_strategy_evaluator_vs_benchmark() -> None:
    """Test StrategyEvaluatorEngine strategy comparison against S&P 500 benchmark."""
    engine = StrategyEvaluatorEngine()
    report = engine.evaluate_strategies("MSFT")

    assert "S&P 500" in report.benchmark_name
    assert len(report.evaluated_strategies) == 5
    names = [s.strategy_name for s in report.evaluated_strategies]
    assert "Buy & Hold Strategy" in names
    assert "Multi-Factor Quantitative Strategy" in names


def test_drift_engine_detection_and_alerts() -> None:
    """Test ModelDriftEngine statistical drift scanning and alert emission."""
    engine = ModelDriftEngine()
    report = engine.audit_model_drift("tft_v1")

    assert report.model_id == "tft_v1"
    assert report.is_retraining_recommended
    assert len(report.drift_alerts) >= 1
    assert report.drift_alerts[0].drift_type == "feature_drift"


def test_model_leaderboard_ranking() -> None:
    """Test LeaderboardEngine composite model ranking."""
    engine = LeaderboardEngine()
    lb = engine.get_leaderboard()

    assert len(lb.entries) >= 5
    assert lb.entries[0].rank == 1
    assert lb.entries[0].overall_leaderboard_score > lb.entries[1].overall_leaderboard_score


def test_retraining_champion_vs_challenger_workflow() -> None:
    """Test RetrainingWorkflowEngine Champion vs Challenger evaluation & approval."""
    engine = RetrainingWorkflowEngine()
    job = engine.trigger_retraining("xgboost_v3", trigger_type="drift_alert")

    assert job.model_id == "xgboost_v3"
    assert job.evaluation_summary.is_challenger_superior
    assert job.evaluation_summary.approval_state == ModelApprovalState.PENDING_APPROVAL

    # Approve Challenger
    approved_eval = engine.approve_model(job.evaluation_summary.evaluation_id, approve=True)
    assert approved_eval.approval_state == ModelApprovalState.APPROVED


@pytest.mark.asyncio
async def test_evaluation_api_endpoints() -> None:
    """Test Continuous Evaluation REST API endpoints (/backtest, /metrics, /leaderboard, /drift, /retrain)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_bt = await client.post("/api/v1/evaluation/backtest?strategy_name=Momentum&symbol=AAPL")
        res_metrics = await client.get("/api/v1/evaluation/metrics?model_id=tft_v1&symbol=AAPL")
        res_lb = await client.get("/api/v1/evaluation/leaderboard")
        res_drift = await client.get("/api/v1/evaluation/drift?model_id=tft_v1")
        res_retrain = await client.post("/api/v1/evaluation/retrain?model_id=tft_v1")
        res_rep = await client.get("/api/v1/evaluation/reports/rep_001")

    assert res_bt.status_code == 200
    assert res_metrics.status_code == 200
    assert res_lb.status_code == 200
    assert res_drift.status_code == 200
    assert res_retrain.status_code == 200
    assert res_rep.status_code == 200
