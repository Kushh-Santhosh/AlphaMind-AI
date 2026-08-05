"""
AlphaMind AI - Virtual Portfolio Simulator & Margin Accounting Engine

Manages virtual cash balances, buying power, margin requirements, position tax lots,
realized P/L, and unrealized P/L.
STRICT MANDATE: Virtual paper accounting only — zero real capital or live brokerage accounts.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field

from packages.portfolio.paper_exchange import SimulatedOrderSide, SimulatedTrade

logger = logging.getLogger(__name__)


class SimulatedPosition(BaseModel):
    symbol: str
    quantity: float
    average_cost_basis: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    realized_pnl: float = 0.0


class PaperPortfolioState(BaseModel):
    portfolio_id: str = "paper_default"
    initial_cash_usd: float = 100000.0
    cash_balance_usd: float = 100000.0
    total_market_value_usd: float = 100000.0
    buying_power_usd: float = 200000.0  # 2x initial margin leverage
    maintenance_margin_required_usd: float = 0.0
    realized_pnl_usd: float = 0.0
    unrealized_pnl_usd: float = 0.0
    positions: dict[str, SimulatedPosition] = Field(default_factory=dict)
    disclaimer: str = (
        "SIMULATION DISCLAIMER: All cash balances, portfolio positions, and P/L figures "
        "represent virtual paper simulations. No real capital was used or traded."
    )


class PortfolioSimulator:
    """Simulator tracking virtual portfolio state, position updates, and margin accounting."""

    def __init__(self, initial_cash_usd: float = 100000.0) -> None:
        self.state = PaperPortfolioState(
            initial_cash_usd=initial_cash_usd,
            cash_balance_usd=initial_cash_usd,
            total_market_value_usd=initial_cash_usd,
            buying_power_usd=initial_cash_usd * 2.0,
        )

    def process_trade(self, trade: SimulatedTrade) -> PaperPortfolioState:
        """Update portfolio state, cash, positions, and margin requirements upon virtual trade."""
        cost = trade.quantity * trade.price
        total_deduction = cost + trade.commission_usd

        pos = self.state.positions.get(trade.symbol)

        if trade.side == SimulatedOrderSide.BUY:
            self.state.cash_balance_usd -= total_deduction
            if pos:
                new_qty = pos.quantity + trade.quantity
                new_cost = ((pos.quantity * pos.average_cost_basis) + cost) / new_qty
                pos.quantity = new_qty
                pos.average_cost_basis = new_cost
                pos.current_price = trade.price
                pos.market_value = new_qty * trade.price
                pos.unrealized_pnl = pos.market_value - (new_qty * new_cost)
            else:
                self.state.positions[trade.symbol] = SimulatedPosition(
                    symbol=trade.symbol,
                    quantity=trade.quantity,
                    average_cost_basis=trade.price,
                    current_price=trade.price,
                    market_value=cost,
                    unrealized_pnl=0.0,
                    unrealized_pnl_pct=0.0,
                )
        else:  # SELL
            self.state.cash_balance_usd += cost - trade.commission_usd
            if pos:
                realized = (trade.price - pos.average_cost_basis) * trade.quantity
                self.state.realized_pnl_usd += realized
                pos.realized_pnl += realized
                pos.quantity -= trade.quantity
                if pos.quantity <= 0:
                    del self.state.positions[trade.symbol]

        # Recalculate totals and margin metrics
        pos_val = sum(p.market_value for p in self.state.positions.values())
        self.state.total_market_value_usd = self.state.cash_balance_usd + pos_val
        self.state.unrealized_pnl_usd = sum(p.unrealized_pnl for p in self.state.positions.values())
        self.state.maintenance_margin_required_usd = pos_val * 0.25  # 25% maintenance margin
        self.state.buying_power_usd = max(0.0, (self.state.total_market_value_usd * 2.0) - pos_val)

        logger.info(
            "Portfolio Updated: Total Val=$%.2f, Cash=$%.2f, Realized P/L=$%.2f",
            self.state.total_market_value_usd,
            self.state.cash_balance_usd,
            self.state.realized_pnl_usd,
        )
        return self.state
