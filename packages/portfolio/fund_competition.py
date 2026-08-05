"""
AlphaMind AI v2 - Multi-Fund Competition & Public Leaderboard Engine

Ranks and benchmarks 5 permanent virtual strategy funds across CAGR, Sharpe ratio,
Sortino ratio, Max Drawdown, Win Rate, and Brier score calibration.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel

from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine

logger = logging.getLogger(__name__)


class LeaderboardEntry(BaseModel):
    rank: int
    fund_id: str
    name: str
    cagr_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown_pct: float
    win_rate_pct: float
    brier_score: float
    composite_score: float


class FundCompetitionLeaderboard:
    """Leaderboard ranking virtual AI funds by composite risk-adjusted performance."""

    def __init__(self, fund_engine: MultiStrategyFundEngine) -> None:
        self.fund_engine = fund_engine

    def get_leaderboard(self) -> list[LeaderboardEntry]:
        """Compute composite score and rank all 5 virtual funds."""
        funds = self.fund_engine.list_all_funds()

        entries: list[LeaderboardEntry] = []
        for fund in funds:
            # Composite score weighting Sharpe (40%), Sortino (30%), CAGR (20%), Brier Calibration (10%)
            comp_score = round(
                (fund.sharpe_ratio * 0.40)
                + (fund.sortino_ratio * 0.30)
                + (fund.cagr_pct * 0.02)
                + ((1.0 - fund.brier_score) * 0.10),
                3,
            )
            entries.append(
                LeaderboardEntry(
                    rank=1,  # Temporary
                    fund_id=fund.fund_id.value,
                    name=fund.name,
                    cagr_pct=fund.cagr_pct,
                    sharpe_ratio=fund.sharpe_ratio,
                    sortino_ratio=fund.sortino_ratio,
                    max_drawdown_pct=fund.max_drawdown_limit_pct,
                    win_rate_pct=fund.win_rate_pct,
                    brier_score=fund.brier_score,
                    composite_score=comp_score,
                )
            )

        # Sort descending by composite score
        entries.sort(key=lambda x: x.composite_score, reverse=True)
        for idx, entry in enumerate(entries, start=1):
            entry.rank = idx

        return entries
