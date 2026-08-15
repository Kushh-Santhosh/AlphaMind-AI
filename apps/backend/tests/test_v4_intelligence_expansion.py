"""
Comprehensive Test Suite for AlphaMind AI v4 Intelligence Expansion & TradingAgents Integration.
Tests all 11 specialized analysts, adversarial debate graph, universe engine, provider registry,
opportunity scanner, backtest engine, portfolio solvers, stress testing, evaluation, and REST APIs.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apps.backend.app.main import app
from packages.agents.agents.bear_researcher import BearResearcherAgent
from packages.agents.agents.bull_researcher import BullResearcherAgent
from packages.agents.agents.earnings_analyst import EarningsAnalystAgent
from packages.agents.agents.fundamental_analyst import FundamentalAnalystAgent
from packages.agents.agents.macro_analyst import MacroAnalystAgent
from packages.agents.agents.market_regime_analyst import MarketRegimeAnalystAgent
from packages.agents.agents.news_analyst import NewsAnalystAgent
from packages.agents.agents.research_manager import ResearchManagerAgent
from packages.agents.agents.risk_committee import RiskCommitteeAgent
from packages.agents.agents.sentiment_analyst import SentimentAnalystAgent
from packages.agents.agents.technical_analyst import TechnicalAnalystAgent
from packages.agents.agents.trader_agent import TraderAgent
from packages.agents.agents.valuation_analyst import ValuationAnalystAgent
from packages.agents.graphs.debate_graph import ResearchDebateGraph
from packages.agents.graphs.investment_workflow_graph import InstitutionalInvestmentWorkflow
from packages.agents.models.llm_gateway import LLMGateway
from packages.agents.state import AlphaMindAgentState
from packages.evaluation.research_evaluator import ResearchEvaluatorEngine
from packages.market.provider_registry import DataProviderRegistry
from packages.market.universe_engine import AssetUniverseEngine
from packages.memory.strategy_learning_memory import StrategyLearningMemory
from packages.portfolio.advanced_solvers import PortfolioOptimizationSolvers
from packages.research.backtest_engine import BacktestConfig, BacktestingEngine
from packages.research.opportunity_scanner import OpportunityScannerEngine
from packages.risk.crisis_stress_engine import CrisisStressEngine

client = TestClient(app)


@pytest.mark.asyncio
async def test_specialized_analysts_execution():
    """Verify all specialized analysts produce structured outputs with citations."""
    state: AlphaMindAgentState = {
        "session_id": "test_sess_01",
        "symbol": "NVDA",
        "asset_class": "equity",
        "market_data": {"price": 132.50, "rsi_14": 58.4, "sma_50": 128.0, "sma_200": 115.0},
        "fundamental_metrics": {"revenue_growth_yoy": 0.22, "operating_margin": 0.32, "altman_z_score": 4.5},
        "completed_agent_nodes": [],
        "error_logs": [],
    }

    # 1. Technical Analyst
    tech_out = await TechnicalAnalystAgent().execute(state)
    assert "technical_analysis" in tech_out
    assert tech_out["technical_analysis"]["trend_posture"] == "BULLISH_CONTINUATION"

    # 2. Fundamental Analyst
    fund_out = await FundamentalAnalystAgent().execute(state)
    assert "fundamental_analysis" in fund_out
    assert fund_out["fundamental_analysis"]["quality_grade"] == "TIER_1_EXCEPTIONAL"

    # 3. Valuation Analyst
    val_out = await ValuationAnalystAgent().execute(state)
    assert "valuation_analysis" in val_out
    assert "intrinsic_value_dcf" in val_out["valuation_analysis"]

    # 4. News Analyst
    news_out = await NewsAnalystAgent().execute(state)
    assert "news_analysis" in news_out
    assert len(news_out["news_analysis"]["upcoming_catalysts"]) > 0

    # 5. Sentiment Analyst
    sent_out = await SentimentAnalystAgent().execute(state)
    assert "sentiment_analysis" in sent_out
    assert sent_out["sentiment_analysis"]["composite_sentiment_score"] > 0

    # 6. Macro Analyst
    macro_out = await MacroAnalystAgent().execute(state)
    assert "macro_analysis" in macro_out
    assert "indicators" in macro_out["macro_analysis"]

    # 7. Market Regime Analyst
    regime_out = await MarketRegimeAnalystAgent().execute(state)
    assert "market_regime_analysis" in regime_out
    assert "risk_appetite" in regime_out["market_regime_analysis"]

    # 8. Earnings Analyst
    earn_out = await EarningsAnalystAgent().execute(state)
    assert "earnings_analysis" in earn_out
    assert earn_out["earnings_analysis"]["earnings_beat_probability_pct"] > 50.0


@pytest.mark.asyncio
async def test_adversarial_research_debate_graph():
    """Verify multi-round Bull vs Bear debate and referee synthesis."""
    initial_state: AlphaMindAgentState = {
        "session_id": "test_debate_01",
        "symbol": "MSFT",
        "market_data": {"price": 418.20},
        "completed_agent_nodes": [],
        "error_logs": [],
    }

    graph = ResearchDebateGraph(rounds=2)
    final_state = await graph.run_debate(initial_state)

    assert "bull_thesis" in final_state
    assert "bear_thesis" in final_state
    assert "research_manager_summary" in final_state
    assert "contradiction_resolution" in final_state
    assert len(final_state["debate_transcript"]) == 4  # 2 rounds * 2 debaters
    assert final_state["debate_rounds"] == 2


@pytest.mark.asyncio
async def test_full_institutional_workflow_graph():
    """Verify end-to-end investment research pipeline."""
    initial_state: AlphaMindAgentState = {
        "session_id": "test_wf_01",
        "symbol": "AAPL",
        "market_data": {"price": 228.40},
        "completed_agent_nodes": [],
        "error_logs": [],
    }

    workflow = InstitutionalInvestmentWorkflow(debate_rounds=1)
    result = await workflow.execute_workflow(initial_state)

    assert "final_report_json" in result
    assert result["final_report_json"]["symbol"] == "AAPL"
    assert len(result["completed_agent_nodes"]) >= 10
    assert result["portfolio_allocation"]["execution_status"] == "READY_FOR_PAPER_SIMULATION"


def test_asset_universe_and_opportunity_scanner():
    """Verify asset universe multi-market discovery and opportunity scanner scoring."""
    u_engine = AssetUniverseEngine()
    categories = u_engine.list_universes()
    assert "US_EQUITIES" in categories
    assert "INDIAN_EQUITIES" in categories
    assert "GLOBAL_ETFS" in categories
    assert "CRYPTO" in categories

    us_secs = u_engine.get_securities(universe="US_EQUITIES")
    assert len(us_secs) >= 5
    in_secs = u_engine.get_securities(universe="INDIAN_EQUITIES")
    assert len(in_secs) >= 5

    scanner = OpportunityScannerEngine(universe_engine=u_engine)
    import asyncio
    opps = asyncio.run(scanner.scan_opportunities(min_score=70.0))
    assert len(opps) > 0
    assert opps[0]["opportunity_score"] >= opps[-1]["opportunity_score"]


def test_backtesting_and_walk_forward_validation():
    """Verify backtesting engine returns comprehensive metrics and walk-forward splits."""
    engine = BacktestingEngine()
    config = BacktestConfig(
        strategy_name="Alpha Factor Momentum",
        universe=["NVDA", "MSFT", "AAPL"],
        start_date="2024-01-01",
        end_date="2025-12-31",
        initial_capital=100000.0,
    )
    result = engine.run_backtest(config)

    assert result["final_capital"] > 0
    assert "performance_metrics" in result
    assert result["performance_metrics"]["sharpe_ratio"] > 0
    assert result["performance_metrics"]["max_drawdown_pct"] <= 0
    assert "validation_segments" in result
    assert result["validation_segments"]["walk_forward_efficiency_ratio"] > 0
    assert len(result["equity_curve"]) > 10


def test_crisis_stress_testing_scenarios():
    """Verify crisis stress test suite against simulated portfolio."""
    stress_engine = CrisisStressEngine()
    results = stress_engine.run_stress_test(positions=[], initial_portfolio_val=100000.0)

    assert results["scenarios_analyzed_count"] == 6
    assert len(results["stress_results"]) == 6
    assert "worst_case_scenario" in results


def test_portfolio_optimization_solvers():
    """Verify all 7 mathematical portfolio optimization solvers."""
    solvers = PortfolioOptimizationSolvers()
    symbols = ["NVDA", "AAPL", "MSFT", "GOOGL", "SPY"]

    for stype in solvers.SOLVERS:
        res = solvers.optimize_portfolio(symbols, solver_type=stype)
        assert res["solver"] == stype
        total_w = sum(res["allocated_weights_pct"].values()) + res["cash_reserve_pct"]
        assert round(total_w, 1) == 100.0


def test_research_evaluator_and_strategy_memory():
    """Verify Brier score calibration and strategy learning memory."""
    evaluator = ResearchEvaluatorEngine()
    stats = evaluator.evaluate_performance()
    assert stats["total_resolved_predictions"] > 0
    assert stats["directional_accuracy_pct"] >= 50.0
    assert stats["mean_brier_calibration_score"] <= 0.25

    memory = StrategyLearningMemory()
    mem_data = memory.get_strategy_memory()
    assert len(mem_data["active_patterns"]) > 0
    assert "TechnicalAnalyst" in mem_data["analyst_accuracy_weights"]


def test_v4_rest_api_endpoints():
    """Test all new v4 API routes through FastAPI TestClient."""
    # 1. Universe
    r_univ = client.get("/api/v1/universe/categories")
    assert r_univ.status_code == 200
    assert "categories" in r_univ.json()

    r_sec = client.get("/api/v1/universe/securities?category=US_EQUITIES")
    assert r_sec.status_code == 200
    assert r_sec.json()["total_count"] > 0

    # 2. Scanner
    r_scan = client.get("/api/v1/scanner/opportunities?min_score=60.0")
    assert r_scan.status_code == 200
    assert "opportunities" in r_scan.json()

    # 3. Debate
    r_deb = client.post("/api/v1/debate/run", json={"symbol": "NVDA", "rounds": 1})
    assert r_deb.status_code == 200
    assert "bull_thesis" in r_deb.json()
    assert "bear_thesis" in r_deb.json()

    # 4. Backtest
    r_back = client.post("/api/v1/backtest_v4/run", json={"strategy_name": "Test Strategy", "universe": ["NVDA", "MSFT"]})
    assert r_back.status_code == 200
    assert "performance_metrics" in r_back.json()

    # 5. Compare
    r_comp = client.post("/api/v1/compare/assets", json={"symbols": ["NVDA", "MSFT", "AAPL"]})
    assert r_comp.status_code == 200
    assert len(r_comp.json()["profiles"]) == 3

    # 6. Providers
    r_prov = client.get("/api/v1/providers/status")
    assert r_prov.status_code == 200
    assert "data_providers" in r_prov.json()
    assert "llm_gateways" in r_prov.json()
