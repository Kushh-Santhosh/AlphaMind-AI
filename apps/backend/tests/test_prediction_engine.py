"""
Probabilistic Prediction Engine Test Suite — Forecast Framework, Model Registry,
Ensemble Aggregators, 5-Tier Scenarios, Monte Carlo Simulations, Calibration & Drift, Explainability & Prediction APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.prediction.calibration import CalibrationEngine
from packages.prediction.ensemble_engine import EnsembleEngine
from packages.prediction.explainability import ForecastExplainabilityEngine
from packages.prediction.model_registry import ModelRegistry
from packages.prediction.monte_carlo_engine import MonteCarloSimulationEngine
from packages.prediction.scenario_engine import ScenarioEngine
from packages.prediction.schemas import ConfidenceInterval95, ProbabilisticForecast


def test_probabilistic_forecast_schema() -> None:
    """Test ProbabilisticForecast schema initialization and disclaimer check."""
    ci = ConfidenceInterval95(lower_bound=-0.10, mean_estimate=0.04, upper_bound=0.18)
    scenarios = ScenarioEngine().generate_scenarios("AAPL")
    dist = ScenarioEngine().get_probability_distribution()

    fcst = ProbabilisticForecast(
        symbol="AAPL",
        confidence_interval=ci,
        probability_distribution=dist,
        scenarios=scenarios,
    )

    assert fcst.symbol == "AAPL"
    assert fcst.confidence_interval.mean_estimate == 0.04
    assert len(fcst.scenarios) == 5
    assert "PROBABILISTIC DISCLAIMER" in fcst.disclaimer


def test_model_registry_interchangeability() -> None:
    """Test ModelRegistry registering and interchanging model implementations."""
    registry = ModelRegistry()
    models = registry.list_models()

    assert len(models) >= 9
    m_ids = [m["model_id"] for m in models]
    assert "arima_v1" in m_ids
    assert "tft_v1" in m_ids
    assert "xgboost_v3" in m_ids
    assert "bayesian_v1" in m_ids


@pytest.mark.asyncio
async def test_ensemble_engine_execution() -> None:
    """Test EnsembleEngine weighted average & BMA execution."""
    registry = ModelRegistry()
    engine = EnsembleEngine(registry)

    res = await engine.execute_ensemble("NVDA", {}, method="bayesian_averaging")
    assert res.ensemble_method == "bayesian_averaging"
    assert res.predicted_mean > 0.0
    assert len(res.models_used) >= 4


def test_five_scenario_generation() -> None:
    """Test ScenarioEngine 5-case generation (Bull, Base, Bear, Stress, Black Swan)."""
    engine = ScenarioEngine()
    scenarios = engine.generate_scenarios("MSFT")

    assert len(scenarios) == 5
    names = [s.scenario_name for s in scenarios]
    assert "Bull" in names
    assert "Base" in names
    assert "Bear" in names
    assert "Stress" in names
    assert "Black Swan" in names

    total_prob = sum(s.probability_pct for s in scenarios)
    assert total_prob == 100.0


def test_monte_carlo_simulation_framework() -> None:
    """Test MonteCarloSimulationEngine Student-t stochastic simulation."""
    engine = MonteCarloSimulationEngine()
    sim = engine.run_simulation(
        symbol="GOOGL",
        num_simulations=5000,
        horizon_days=30,
        distribution_type="student_t",
        random_seed=123,
    )

    assert sim.symbol == "GOOGL"
    assert sim.num_simulations == 5000
    assert sim.percentile_5th < sim.percentile_50th_median < sim.percentile_95th
    assert sim.simulation_duration_ms > 0.0


def test_calibration_and_brier_score() -> None:
    """Test CalibrationEngine Brier score evaluation and drift detection."""
    engine = CalibrationEngine()
    report = engine.evaluate_model_calibration("tft_v1")

    assert report.model_id == "tft_v1"
    assert 0.0 <= report.brier_score <= 1.0
    assert len(report.reliability_diagram_points) >= 3
    assert not report.is_drift_detected


def test_forecast_explainability_feature_importance() -> None:
    """Test ForecastExplainabilityEngine feature importance ranking."""
    scenarios = ScenarioEngine().generate_scenarios("TSLA")
    dist = ScenarioEngine().get_probability_distribution()
    ci = ConfidenceInterval95(lower_bound=-0.20, mean_estimate=0.02, upper_bound=0.25)

    fcst = ProbabilisticForecast(
        symbol="TSLA",
        confidence_interval=ci,
        probability_distribution=dist,
        scenarios=scenarios,
    )

    engine = ForecastExplainabilityEngine()
    report = engine.explain_forecast(fcst)

    assert report.symbol == "TSLA"
    assert len(report.feature_importance_weights) >= 3
    assert report.feature_importance_weights[0].importance_weight > 0.0


@pytest.mark.asyncio
async def test_prediction_api_endpoints() -> None:
    """Test Prediction Engine REST APIs."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_fcst = await client.post("/api/v1/prediction/forecast?symbol=AAPL&horizon_days=30")
        res_scen = await client.get("/api/v1/prediction/scenarios/AAPL")
        res_mc = await client.post("/api/v1/prediction/monte-carlo/AAPL?num_simulations=1000")
        res_calib = await client.get("/api/v1/prediction/calibration?model_id=tft_v1")
        res_hist = await client.get("/api/v1/prediction/history/AAPL")
        res_models = await client.get("/api/v1/prediction/models")

    assert res_fcst.status_code == 200
    assert res_scen.status_code == 200
    assert res_mc.status_code == 200
    assert res_calib.status_code == 200
    assert res_hist.status_code == 200
    assert res_models.status_code == 200
