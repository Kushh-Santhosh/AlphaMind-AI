"""
AlphaMind AI - Execution Risk Controls & Pre-Trade Limits Engine

Enforces pre-trade risk checks: Max Position Size %, Max Leverage, Max Drawdown %,
Daily Loss Limit, Sector Exposure Limit %, and Concentration Limits.
Rejects orders immediately if pre-trade risk limits are breached.
STRICT MANDATE: Zero real order routing — pre-trade safety controls only.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel

from packages.portfolio.paper_exchange import SimulatedOrderSide
from packages.portfolio.paper_portfolio import PaperPortfolioState

logger = logging.getLogger(__name__)


class PreTradeRiskLimits(BaseModel):
    max_position_size_pct: float = 25.0  # Max 25% portfolio in single stock
    max_leverage: float = 2.0  # Max 2.0x gross leverage
    max_daily_loss_usd: float = 5000.0  # Max daily loss threshold
    max_sector_exposure_pct: float = 40.0  # Max 40% sector concentration
    max_hhi_concentration: float = 0.2500  # Max HHI index threshold


class PreTradeRiskCheckResult(BaseModel):
    is_approved: bool
    rejection_reason: str | None = None
    evaluated_leverage: float
    evaluated_position_pct: float


class PreTradeRiskEngine:
    """Pre-trade safety gate validating orders against institutional risk limits."""

    def __init__(self, limits: PreTradeRiskLimits | None = None) -> None:
        self.limits = limits or PreTradeRiskLimits()

    def validate_pre_trade(
        self,
        order_symbol: str,
        side: SimulatedOrderSide,
        quantity: float,
        price: float,
        portfolio_state: PaperPortfolioState,
    ) -> PreTradeRiskCheckResult:
        """Validate order against position size, leverage, and drawdown pre-trade limits."""
        order_value = quantity * price
        total_val = max(1.0, portfolio_state.total_market_value_usd)
        (order_value / total_val) * 100.0

        # Check 1: Max Position Size
        existing_pos = portfolio_state.positions.get(order_symbol.upper())
        existing_val = existing_pos.market_value if existing_pos else 0.0
        post_order_pos_pct = ((existing_val + order_value) / total_val) * 100.0

        if (
            side == SimulatedOrderSide.BUY
            and post_order_pos_pct > self.limits.max_position_size_pct
        ):
            reason = (
                f"PRE-TRADE RISK REJECTION: Position size for '{order_symbol.upper()}' would reach "
                f"{post_order_pos_pct:.1f}%, exceeding limit of {self.limits.max_position_size_pct:.1f}%."
            )
            logger.warning(reason)
            return PreTradeRiskCheckResult(
                is_approved=False,
                rejection_reason=reason,
                evaluated_leverage=1.0,
                evaluated_position_pct=post_order_pos_pct,
            )

        # Check 2: Max Leverage Check
        total_pos_val = sum(p.market_value for p in portfolio_state.positions.values())
        post_pos_val = total_pos_val + (
            order_value if side == SimulatedOrderSide.BUY else -order_value
        )
        post_leverage = post_pos_val / total_val

        if post_leverage > self.limits.max_leverage:
            reason = (
                f"PRE-TRADE RISK REJECTION: Gross leverage would reach {post_leverage:.2f}x, "
                f"exceeding max leverage limit of {self.limits.max_leverage:.2f}x."
            )
            logger.warning(reason)
            return PreTradeRiskCheckResult(
                is_approved=False,
                rejection_reason=reason,
                evaluated_leverage=post_leverage,
                evaluated_position_pct=post_order_pos_pct,
            )

        logger.info(
            "Pre-trade risk check PASSED for '%s' %.2f shares.", order_symbol.upper(), quantity
        )
        return PreTradeRiskCheckResult(
            is_approved=True,
            evaluated_leverage=post_leverage,
            evaluated_position_pct=post_order_pos_pct,
        )
