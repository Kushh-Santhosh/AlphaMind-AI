"""
AlphaMind AI v2 - User Strategy Workspace

Allows users to:
  - Follow any AI fund (Conservative, Balanced, Growth, Aggressive, Crypto)
  - Clone a fund's allocation into their own paper portfolio
  - Compare their paper portfolio performance against AI funds
  - Maintain watchlists of assets
  - Receive and manage non-trading alerts

Zero duplicate business logic — reuses MultiStrategyFundEngine for
live fund state and FundDecisionRecord schema for comparison metrics.
"""

from __future__ import annotations

import logging
import time
import uuid

from pydantic import BaseModel, Field

from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine, StrategyFundType

logger = logging.getLogger(__name__)


# ── Schemas ────────────────────────────────────────────────────────────────────


class WatchlistItem(BaseModel):
    symbol: str
    asset_class: str = "EQUITY"
    added_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    notes: str = ""


class WorkspaceAlert(BaseModel):
    alert_id: str = Field(default_factory=lambda: f"alert_{uuid.uuid4().hex[:8]}")
    user_id: str
    title: str
    message: str
    alert_type: str = "INFO"  # INFO | RISK | FORECAST | REBALANCE | BRIEFING
    is_read: bool = False
    created_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class PaperPortfolio(BaseModel):
    portfolio_id: str = Field(default_factory=lambda: f"pp_{uuid.uuid4().hex[:8]}")
    user_id: str
    name: str
    cloned_from_fund_id: str | None = None
    allocations: dict[str, float] = Field(default_factory=dict)
    initial_capital: float = 10000.0
    current_value: float = 10000.0
    created_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    returns_pct: float = 0.0
    sharpe_ratio: float = 0.0


class PerformanceComparison(BaseModel):
    user_portfolio_id: str
    ai_fund_id: str
    user_returns_pct: float
    fund_returns_pct: float
    user_sharpe_ratio: float
    fund_sharpe_ratio: float
    outperformance_pct: float
    generated_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class UserWorkspace(BaseModel):
    workspace_id: str = Field(default_factory=lambda: f"ws_{uuid.uuid4().hex[:8]}")
    user_id: str
    followed_fund_ids: list[str] = Field(default_factory=list)
    paper_portfolios: list[PaperPortfolio] = Field(default_factory=list)
    watchlists: list[WatchlistItem] = Field(default_factory=list)
    alerts: list[WorkspaceAlert] = Field(default_factory=list)
    created_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


# ── Engine ─────────────────────────────────────────────────────────────────────


class UserWorkspaceEngine:
    """
    User Strategy Workspace engine managing multi-user paper portfolios,
    fund following, watchlists, and non-trading alerts.
    Reuses MultiStrategyFundEngine for live AI fund state.
    """

    def __init__(self, fund_engine: MultiStrategyFundEngine) -> None:
        self.fund_engine = fund_engine
        self.workspaces: dict[str, UserWorkspace] = {}

    def get_or_create_workspace(self, user_id: str) -> UserWorkspace:
        """Return existing workspace or create one for the given user."""
        if user_id not in self.workspaces:
            ws = UserWorkspace(user_id=user_id)
            self.workspaces[user_id] = ws
            logger.info(
                "UserWorkspaceEngine: created workspace '%s' for user '%s'",
                ws.workspace_id,
                user_id,
            )
        return self.workspaces[user_id]

    # ── Follow / Unfollow ──────────────────────────────────────────────────────

    def follow_fund(self, user_id: str, fund_id: str) -> UserWorkspace:
        """Subscribe a user's workspace to follow an AI fund."""
        ws = self.get_or_create_workspace(user_id)
        if fund_id not in ws.followed_fund_ids:
            ws.followed_fund_ids.append(fund_id)
        return ws

    def unfollow_fund(self, user_id: str, fund_id: str) -> UserWorkspace:
        """Remove a fund from a user's followed list."""
        ws = self.get_or_create_workspace(user_id)
        ws.followed_fund_ids = [f for f in ws.followed_fund_ids if f != fund_id]
        return ws

    # ── Paper Portfolio ────────────────────────────────────────────────────────

    def clone_fund_into_paper_portfolio(
        self,
        user_id: str,
        fund_id: str,
        portfolio_name: str = "",
    ) -> PaperPortfolio:
        """
        Clone a live AI fund allocation into the user's paper portfolio.
        Reuses fund state from MultiStrategyFundEngine. No business logic is duplicated.
        """
        fund = self.fund_engine.get_fund(StrategyFundType(fund_id))
        if not fund:
            raise ValueError(f"Fund '{fund_id}' not found in MultiStrategyFundEngine.")

        ws = self.get_or_create_workspace(user_id)
        pp = PaperPortfolio(
            user_id=user_id,
            name=portfolio_name or f"{fund.name} Clone",
            cloned_from_fund_id=fund_id,
            allocations=dict(fund.allocations),
            initial_capital=fund.current_market_value_usd,
            current_value=fund.current_market_value_usd,
        )
        ws.paper_portfolios.append(pp)
        logger.info(
            "UserWorkspaceEngine: user '%s' cloned fund '%s' → portfolio '%s'",
            user_id,
            fund_id,
            pp.portfolio_id,
        )
        return pp

    def get_paper_portfolio(self, user_id: str, portfolio_id: str) -> PaperPortfolio | None:
        """Retrieve a specific paper portfolio by ID."""
        ws = self.workspaces.get(user_id)
        if not ws:
            return None
        return next((p for p in ws.paper_portfolios if p.portfolio_id == portfolio_id), None)

    # ── Performance Comparison ─────────────────────────────────────────────────

    def compare_with_fund(
        self,
        user_id: str,
        portfolio_id: str,
        fund_id: str,
    ) -> PerformanceComparison:
        """Compare user paper portfolio performance against a live AI fund."""
        pp = self.get_paper_portfolio(user_id, portfolio_id)
        if not pp:
            raise ValueError(f"Paper portfolio '{portfolio_id}' not found for user '{user_id}'.")

        fund = self.fund_engine.get_fund(StrategyFundType(fund_id))
        if not fund:
            raise ValueError(f"Fund '{fund_id}' not found.")

        return PerformanceComparison(
            user_portfolio_id=portfolio_id,
            ai_fund_id=fund_id,
            user_returns_pct=pp.returns_pct,
            fund_returns_pct=fund.cagr_pct,
            user_sharpe_ratio=pp.sharpe_ratio,
            fund_sharpe_ratio=fund.sharpe_ratio,
            outperformance_pct=pp.returns_pct - fund.cagr_pct,
        )

    # ── Watchlist ──────────────────────────────────────────────────────────────

    def add_to_watchlist(
        self,
        user_id: str,
        symbol: str,
        asset_class: str = "EQUITY",
        notes: str = "",
    ) -> WatchlistItem:
        """Add an asset to a user's watchlist."""
        ws = self.get_or_create_workspace(user_id)
        item = WatchlistItem(symbol=symbol, asset_class=asset_class, notes=notes)
        ws.watchlists.append(item)
        return item

    def remove_from_watchlist(self, user_id: str, symbol: str) -> UserWorkspace:
        """Remove an asset from the user's watchlist."""
        ws = self.get_or_create_workspace(user_id)
        ws.watchlists = [w for w in ws.watchlists if w.symbol != symbol]
        return ws

    # ── Alerts ────────────────────────────────────────────────────────────────

    def add_alert(
        self,
        user_id: str,
        title: str,
        message: str,
        alert_type: str = "INFO",
    ) -> WorkspaceAlert:
        """Create a non-trading alert for a user."""
        ws = self.get_or_create_workspace(user_id)
        alert = WorkspaceAlert(
            user_id=user_id,
            title=title,
            message=message,
            alert_type=alert_type,
        )
        ws.alerts.append(alert)
        return alert

    def mark_alert_read(self, user_id: str, alert_id: str) -> bool:
        """Mark an alert as read."""
        ws = self.workspaces.get(user_id)
        if not ws:
            return False
        for alert in ws.alerts:
            if alert.alert_id == alert_id:
                alert.is_read = True
                return True
        return False

    def get_unread_alerts(self, user_id: str) -> list[WorkspaceAlert]:
        """Return unread alerts for a user."""
        ws = self.workspaces.get(user_id)
        if not ws:
            return []
        return [a for a in ws.alerts if not a.is_read]
