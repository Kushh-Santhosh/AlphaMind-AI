"""
AlphaMind AI - Monte Carlo Simulation Framework

Simulates 10,000+ stochastic price trajectories across Normal, Student-t, and Log-Normal distributions.
Includes random seed management, percentile confidence bounds, and full simulation audit logs.
STRICT MANDATE: Zero investment advice or buy/sell execution logic.
"""

from __future__ import annotations

import logging
import math
import random
import time
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MonteCarloSimulationResult(BaseModel):
    simulation_id: str
    symbol: str
    num_simulations: int = 10_000
    horizon_days: int = 30
    distribution_type: str  # "normal", "student_t", "log_normal"
    random_seed: int
    percentile_5th: float
    percentile_50th_median: float
    percentile_95th: float
    simulated_return_mean: float
    simulated_return_std: float
    simulation_duration_ms: float
    audit_trail: dict[str, Any] = Field(default_factory=dict)


class MonteCarloSimulationEngine:
    """Monte Carlo Simulation Engine for stochastic probability estimation."""

    def run_simulation(
        self,
        symbol: str,
        expected_return_annual: float = 0.08,
        volatility_annual: float = 0.20,
        horizon_days: int = 30,
        num_simulations: int = 10_000,
        distribution_type: str = "student_t",
        random_seed: int = 42,
    ) -> MonteCarloSimulationResult:
        """Execute Monte Carlo stochastic simulation over specified horizon."""
        start_time = time.monotonic()
        random.seed(random_seed)

        dt = horizon_days / 365.0
        drift = (expected_return_annual - 0.5 * volatility_annual**2) * dt
        vol_step = volatility_annual * math.sqrt(dt)

        returns: list[float] = []

        for _ in range(num_simulations):
            if distribution_type == "student_t":
                # Heavy-tail simulation via inverse Chi-squared scaling over Gaussian
                z = random.gauss(0.0, 1.0)
                # Degrees of freedom = 5 -> Heavy tails
                u = random.gammavariate(5 / 2, 2)
                t_val = z / math.sqrt(u / 5) if u > 0 else z
                shock = t_val / math.sqrt(5 / 3)  # Scale to unit variance
            elif distribution_type == "log_normal":
                shock = random.lognormvariate(0.0, 0.5) - 1.0
            else:
                shock = random.gauss(0.0, 1.0)

            ret = drift + vol_step * shock
            returns.append(ret)

        returns.sort()
        n = len(returns)
        p5 = returns[int(n * 0.05)]
        p50 = returns[int(n * 0.50)]
        p95 = returns[int(n * 0.95)]
        mean_ret = sum(returns) / n
        var_ret = sum((r - mean_ret) ** 2 for r in returns) / n
        std_ret = math.sqrt(var_ret)

        duration = (time.monotonic() - start_time) * 1000.0
        logger.info(
            "Monte Carlo simulation executed for '%s': %d runs in %.2fms. p5=%.4f, p50=%.4f, p95=%.4f",
            symbol,
            num_simulations,
            duration,
            p5,
            p50,
            p95,
        )

        return MonteCarloSimulationResult(
            simulation_id=f"mc_{symbol.lower()}_{int(time.time())}",
            symbol=symbol,
            num_simulations=num_simulations,
            horizon_days=horizon_days,
            distribution_type=distribution_type,
            random_seed=random_seed,
            percentile_5th=round(p5, 4),
            percentile_50th_median=round(p50, 4),
            percentile_95th=round(p95, 4),
            simulated_return_mean=round(mean_ret, 4),
            simulated_return_std=round(std_ret, 4),
            simulation_duration_ms=round(duration, 2),
            audit_trail={
                "drift": float(drift),
                "volatility_step": float(vol_step),
                "degrees_of_freedom": 5 if distribution_type == "student_t" else None,
            },
        )
