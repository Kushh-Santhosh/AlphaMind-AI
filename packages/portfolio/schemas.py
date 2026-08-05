"""
AlphaMind AI - Portfolio Intelligence Schemas

Defines multi-asset position schemas supporting Cash, Stocks, ETFs, Mutual Funds,
Crypto, Forex, Commodities, Options, Futures, Fixed Income, Tax Lots, P&L, and Fees.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum

from pydantic import BaseModel, Field


class AssetClass(str, Enum):  # noqa: UP042
    CASH = "Cash"
    STOCKS = "Stocks"
    ETFS = "ETFs"
    MUTUAL_FUNDS = "Mutual Funds"
    CRYPTO = "Crypto"
    FOREX = "Forex"
    COMMODITIES = "Commodities"
    OPTIONS = "Options"
    FUTURES = "Futures"
    FIXED_INCOME = "Fixed Income"


class TaxLot(BaseModel):
    lot_id: str = Field(default_factory=lambda: f"lot_{uuid.uuid4().hex[:8]}")
    quantity: float
    purchase_price_usd: float
    purchase_date_utc: str
    fees_paid_usd: float = 0.0


class Position(BaseModel):
    position_id: str = Field(default_factory=lambda: f"pos_{uuid.uuid4().hex[:8]}")
    symbol: str
    asset_class: AssetClass
    quantity: float
    average_cost_usd: float
    current_price_usd: float
    market_value_usd: float = 0.0
    realized_pnl_usd: float = 0.0
    unrealized_pnl_usd: float = 0.0
    currency: str = "USD"
    fees_total_usd: float = 0.0
    sector: str = "Unspecified"
    country: str = "US"
    market_cap_category: str = "Large"  # "Mega", "Large", "Mid", "Small"
    tax_lots: list[TaxLot] = Field(default_factory=list)


class Portfolio(BaseModel):
    """Unified Multi-Asset Class Portfolio Model."""

    portfolio_id: str = Field(default_factory=lambda: f"port_{uuid.uuid4().hex[:8]}")
    name: str = "Default Investment Portfolio"
    created_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    cash_balance_usd: float = 100_000.0
    positions: list[Position] = Field(default_factory=list)
    total_market_value_usd: float = 0.0
    total_realized_pnl_usd: float = 0.0
    total_unrealized_pnl_usd: float = 0.0
    base_currency: str = "USD"
    disclaimer: str = (
        "PORTFOLIO ANALYSIS DISCLAIMER: All risk, drawdown, and scenario metrics "
        "are institutional risk measurement tools for educational and analytical purposes only. "
        "No automated trading, broker execution, or investment recommendations are performed."
    )
