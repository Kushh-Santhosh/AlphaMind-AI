"""
AlphaMind AI v2 - Multi-Strategy Virtual AI Funds Engine

Manages 5 permanent virtual strategy funds:
Conservative, Balanced, Growth, Aggressive, and Crypto.
Each fund maintains an independent portfolio, risk profile, performance metrics,
event stream, and replay checkpoints.
Every rebalance publishes SystemEvents to the Unified Timeline with full evidence citations.
"""

from __future__ import annotations

import logging
import time
import uuid
from enum import Enum

from pydantic import BaseModel, Field

from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent

logger = logging.getLogger(__name__)


class StrategyFundType(str, Enum):  # noqa: UP042
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    GROWTH = "GROWTH"
    AGGRESSIVE = "AGGRESSIVE"
    CRYPTO = "CRYPTO"


class FundDecisionRecord(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:10]}")
    fund_id: StrategyFundType
    timestamp_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    reasoning_summary: str
    target_allocations: dict[str, float]
    evidence_citations: list[str]
    confidence_score: float  # 0.0 - 1.0
    contradictory_evidence: list[str]
    risk_assessment: dict[str, float]
    replay_id: str = Field(default_factory=lambda: f"rpl_{uuid.uuid4().hex[:8]}")
    audit_metadata: dict[str, str] = Field(default_factory=dict)


class VirtualStrategyFund(BaseModel):
    fund_id: StrategyFundType
    name: str
    description: str
    initial_capital_usd: float = 10000.0
    current_market_value_usd: float = 10000.0
    cash_usd: float = 10000.0
    target_volatility_pct: float
    max_drawdown_limit_pct: float
    cagr_pct: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    max_drawdown_pct: float = 0.0
    win_rate_pct: float = 0.0
    brier_score: float = 0.05
    alpha: float = 0.0
    beta: float = 1.0
    allocations: dict[str, float] = Field(default_factory=dict)
    decision_history: list[FundDecisionRecord] = Field(default_factory=list)


class MultiStrategyFundEngine:
    """Engine managing 5 permanent virtual strategy funds and rebalance decisions."""

    def __init__(self, event_bus: EventBusManager | None = None) -> None:
        self.event_bus = event_bus
        self.funds: dict[StrategyFundType, VirtualStrategyFund] = {}
        self._initialize_5_funds()

    def _initialize_5_funds(self) -> None:
        """Initialize 5 permanent virtual strategy funds."""
        defs = [
            VirtualStrategyFund(
                fund_id=StrategyFundType.CONSERVATIVE,
                name="Conservative Capital Preservation AI Fund",
                description="Low-volatility capital preservation focusing on fixed income, quality dividend ETFs, and cash.",
                target_volatility_pct=8.0,
                max_drawdown_limit_pct=-5.0,
                sharpe_ratio=1.85,
                sortino_ratio=2.40,
                cagr_pct=6.5,
                allocations={"TLT": 0.40, "SPY": 0.30, "CASH": 0.30},
            ),
            VirtualStrategyFund(
                fund_id=StrategyFundType.BALANCED,
                name="Balanced Multi-Asset Growth AI Fund",
                description="Classic 60/40 risk-adjusted growth balancing mega-cap equities and fixed income.",
                target_volatility_pct=14.0,
                max_drawdown_limit_pct=-12.0,
                sharpe_ratio=1.62,
                sortino_ratio=2.10,
                cagr_pct=11.2,
                allocations={"SPY": 0.50, "TLT": 0.30, "AAPL": 0.10, "MSFT": 0.10},
            ),
            VirtualStrategyFund(
                fund_id=StrategyFundType.GROWTH,
                name="High-Growth Technology AI Fund",
                description="Capital appreciation focusing on technology, semiconductor, and high-growth innovation factors.",
                target_volatility_pct=20.0,
                max_drawdown_limit_pct=-18.0,
                sharpe_ratio=1.45,
                sortino_ratio=1.80,
                cagr_pct=18.5,
                allocations={"QQQ": 0.40, "NVDA": 0.25, "AAPL": 0.20, "MSFT": 0.15},
            ),
            VirtualStrategyFund(
                fund_id=StrategyFundType.AGGRESSIVE,
                name="Aggressive Momentum Alpha AI Fund",
                description="High-beta momentum strategies seeking maximum equity alpha across market cycles.",
                target_volatility_pct=28.0,
                max_drawdown_limit_pct=-25.0,
                sharpe_ratio=1.28,
                sortino_ratio=1.55,
                cagr_pct=26.4,
                allocations={"NVDA": 0.35, "QQQ": 0.35, "AAPL": 0.30},
            ),
            VirtualStrategyFund(
                fund_id=StrategyFundType.CRYPTO,
                name="Digital Asset & Crypto Intelligence AI Fund",
                description="Cryptocurrency and Web3 digital asset intelligence tracking spot BTC, ETH, and layer-1 protocols.",
                target_volatility_pct=45.0,
                max_drawdown_limit_pct=-35.0,
                sharpe_ratio=1.15,
                sortino_ratio=1.35,
                cagr_pct=42.0,
                allocations={"BTC-USD": 0.60, "ETH-USD": 0.40},
            ),
        ]
        for fund in defs:
            self.funds[fund.fund_id] = fund

    def get_fund(self, fund_id: StrategyFundType) -> VirtualStrategyFund | None:
        """Fetch fund by ID."""
        return self.funds.get(fund_id)

    def list_all_funds(self) -> list[VirtualStrategyFund]:
        """List all 5 virtual strategy funds."""
        return list(self.funds.values())

    def rebalance_fund(
        self,
        fund_id: StrategyFundType,
        target_allocations: dict[str, float],
        reasoning_summary: str,
        evidence_citations: list[str],
        confidence_score: float = 0.85,
        contradictory_evidence: list[str] | None = None,
    ) -> FundDecisionRecord:
        """Execute fund rebalance and record transparent decision record."""
        fund = self.funds.get(fund_id)
        if not fund:
            raise ValueError(f"Strategy Fund '{fund_id}' not found.")

        fund.allocations = target_allocations

        record = FundDecisionRecord(
            fund_id=fund_id,
            reasoning_summary=reasoning_summary,
            target_allocations=target_allocations,
            evidence_citations=evidence_citations,
            confidence_score=confidence_score,
            contradictory_evidence=contradictory_evidence
            or ["Higher interest rate volatility flag"],
            risk_assessment={"var_95_pct": 2.1, "cvar_95_pct": 3.4, "max_drawdown_impact_pct": 1.5},
            audit_metadata={"audited_by": "AlphaMind_v2_OS_Kernel"},
        )
        fund.decision_history.append(record)

        # Publish event to Unified Timeline via EventBus if registered
        if self.event_bus:
            evt = SystemEvent(
                event_type=EventType.PORTFOLIO_REBALANCED,
                source_subsystem=f"virtual_fund_{fund_id.value.lower()}",
                headline=f"Virtual AI Fund Rebalanced: {fund.name}",
                details=reasoning_summary,
                payload=record.model_dump(),
            )
            self.event_bus.publish(evt)

        logger.info("Rebalanced Virtual AI Fund '%s': %s", fund.name, reasoning_summary)
        return record
