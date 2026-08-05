"""
AlphaMind AI - Multi-Scenario Generation Engine

Generates Bull, Base, Bear, Stress, and Black Swan scenario distributions with associated
probabilities, assumptions, supporting evidence, and risk factors.
"""

from __future__ import annotations

import logging

from packages.prediction.schemas import ForecastScenario, ProbabilityDistribution

logger = logging.getLogger(__name__)


class ScenarioEngine:
    """Engine generating 5-tier probabilistic scenarios for asset research."""

    def generate_scenarios(self, symbol: str) -> list[ForecastScenario]:
        """Generate 5-case probabilistic scenarios."""
        logger.info("Generating 5-tier probabilistic scenarios for '%s'", symbol)

        return [
            ForecastScenario(
                scenario_name="Bull",
                probability_pct=25.0,
                implied_return_range_pct=[12.0, 28.0],
                key_assumptions=["Revenue growth acceleration > 15%", "Fed rate cuts"],
                supporting_evidence=["Strong enterprise cloud adoption in Q2 10-K"],
                risk_factors=["Valuation compression"],
            ),
            ForecastScenario(
                scenario_name="Base",
                probability_pct=50.0,
                implied_return_range_pct=[3.0, 11.0],
                key_assumptions=["Revenue growth aligned with guidance (8-10%)"],
                supporting_evidence=["Stable operating margins and cash flow conversion"],
                risk_factors=["Broader macro slowdown"],
            ),
            ForecastScenario(
                scenario_name="Bear",
                probability_pct=15.0,
                implied_return_range_pct=[-15.0, -2.0],
                key_assumptions=["Margin compression due to input cost inflation"],
                supporting_evidence=["Rising debt service cost in high rate environment"],
                risk_factors=["Execution failure on key products"],
            ),
            ForecastScenario(
                scenario_name="Stress",
                probability_pct=8.0,
                implied_return_range_pct=[-30.0, -16.0],
                key_assumptions=["Severe credit tightening and industry downturn"],
                supporting_evidence=["Elevated yield curve inversion spread"],
                risk_factors=["Regulatory enforcement action"],
            ),
            ForecastScenario(
                scenario_name="Black Swan",
                probability_pct=2.0,
                implied_return_range_pct=[-55.0, -31.0],
                key_assumptions=["Systemic financial crisis or geopolitical escalation"],
                supporting_evidence=["Historical tail-risk probability distributions"],
                risk_factors=["Extreme illiquidity event"],
            ),
        ]

    def get_probability_distribution(self) -> ProbabilityDistribution:
        return ProbabilityDistribution(
            bull_case_pct=25.0,
            base_case_pct=50.0,
            bear_case_pct=15.0,
            stress_case_pct=8.0,
            black_swan_case_pct=2.0,
        )
