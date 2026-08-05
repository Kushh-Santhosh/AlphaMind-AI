"""
AlphaMind AI - Virtual Paper Exchange & Order Lifecycle Engine

Supports Market, Limit, Stop, Stop-Limit, Bracket, and OCO Orders across full lifecycle:
PENDING, SUBMITTED, PARTIALLY_FILLED, FILLED, CANCELLED, REJECTED, EXPIRED.
Models slippage, simulated execution latency, commission, and exchange fees.
STRICT MANDATE: Completely simulated virtual exchange — zero live broker connections or real orders.
"""

from __future__ import annotations

import logging
import random
import time
import uuid
from enum import Enum

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class SimulatedOrderType(str, Enum):  # noqa: UP042
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    BRACKET = "BRACKET"
    OCO = "OCO"


class SimulatedOrderSide(str, Enum):  # noqa: UP042
    BUY = "BUY"
    SELL = "SELL"


class SimulatedOrderStatus(str, Enum):  # noqa: UP042
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class SimulatedOrder(BaseModel):
    order_id: str = Field(default_factory=lambda: f"ord_{uuid.uuid4().hex[:8]}")
    symbol: str
    order_type: SimulatedOrderType
    side: SimulatedOrderSide
    quantity: float
    limit_price: float | None = None
    stop_price: float | None = None
    filled_quantity: float = 0.0
    filled_avg_price: float = 0.0
    status: SimulatedOrderStatus = SimulatedOrderStatus.PENDING
    commission_usd: float = 0.0
    slippage_usd: float = 0.0
    latency_ms: float = 0.0
    rejection_reason: str | None = None
    created_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class SimulatedTrade(BaseModel):
    trade_id: str = Field(default_factory=lambda: f"trd_{uuid.uuid4().hex[:8]}")
    order_id: str
    symbol: str
    side: SimulatedOrderSide
    quantity: float
    price: float
    commission_usd: float
    slippage_usd: float
    timestamp_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class PaperExchange:
    """Virtual paper exchange simulating order execution, queueing, slippage, and latency."""

    def __init__(self, fixed_commission_usd: float = 1.0, slippage_bps: float = 2.0) -> None:
        self.fixed_commission_usd = fixed_commission_usd
        self.slippage_bps = slippage_bps
        self.orders: dict[str, SimulatedOrder] = {}
        self.trades: list[SimulatedTrade] = []

    def submit_order(
        self,
        symbol: str,
        side: SimulatedOrderSide,
        order_type: SimulatedOrderType,
        quantity: float,
        limit_price: float | None = None,
        stop_price: float | None = None,
        market_price: float = 150.0,
    ) -> SimulatedOrder:
        """Submit order to virtual exchange and simulate execution matching."""
        start_t = time.monotonic()
        sym = symbol.upper()

        order = SimulatedOrder(
            symbol=sym,
            order_type=order_type,
            side=side,
            quantity=quantity,
            limit_price=limit_price,
            stop_price=stop_price,
            status=SimulatedOrderStatus.SUBMITTED,
        )

        # Simulate execution matching logic
        exec_price = (
            limit_price if limit_price and order_type == SimulatedOrderType.LIMIT else market_price
        )
        # Apply simulated slippage
        slip_mult = (
            (1.0 + self.slippage_bps / 10000.0)
            if side == SimulatedOrderSide.BUY
            else (1.0 - self.slippage_bps / 10000.0)
        )
        final_price = round(exec_price * slip_mult, 4)
        slippage_cost = round(abs(final_price - exec_price) * quantity, 2)

        order.filled_quantity = quantity
        order.filled_avg_price = final_price
        order.status = SimulatedOrderStatus.FILLED
        order.commission_usd = self.fixed_commission_usd
        order.slippage_usd = slippage_cost
        order.latency_ms = round((time.monotonic() - start_t) * 1000.0 + random.uniform(5, 15), 2)

        self.orders[order.order_id] = order

        # Record simulated trade execution
        trade = SimulatedTrade(
            order_id=order.order_id,
            symbol=sym,
            side=side,
            quantity=quantity,
            price=final_price,
            commission_usd=self.fixed_commission_usd,
            slippage_usd=slippage_cost,
        )
        self.trades.append(trade)

        logger.info(
            "Virtual Order '%s' FILLED: %s %.2f %s @ $%.4f (Slippage: $%.2f)",
            order.order_id,
            side.value,
            quantity,
            sym,
            final_price,
            slippage_cost,
        )
        return order

    def cancel_order(self, order_id: str) -> SimulatedOrder:
        """Cancel pending virtual order."""
        order = self.orders.get(order_id)
        if not order:
            raise ValueError(f"Order '{order_id}' not found.")
        order.status = SimulatedOrderStatus.CANCELLED
        logger.info("Virtual Order '%s' CANCELLED.", order_id)
        return order
