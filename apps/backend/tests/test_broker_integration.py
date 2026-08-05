"""
Broker Integration Layer Test Suite — Mock Broker Providers, Execution Mode Controller,
Live User Confirmation Gate, Audit Manager, Telemetry, and Broker REST APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.portfolio.broker_audit import BrokerAuditManager
from packages.portfolio.broker_observability import BrokerObservabilityTracker
from packages.portfolio.broker_provider import (
    AlpacaBrokerProvider,
    BinanceSpotBrokerProvider,
    BrokerOrderRequest,
    CCXTBrokerProvider,
    GenericRestBrokerAdapter,
    InteractiveBrokersProvider,
)
from packages.portfolio.order_router import ExecutionMode, OrderRouter


def test_broker_abstraction_mock_providers() -> None:
    """Test all 5 broker provider abstractions using mock adapters."""
    alpaca = AlpacaBrokerProvider()
    ib = InteractiveBrokersProvider()
    ccxt = CCXTBrokerProvider()
    binance = BinanceSpotBrokerProvider()
    generic = GenericRestBrokerAdapter()

    assert alpaca.get_account_summary().cash_balance_usd > 0.0
    assert ib.get_account_summary().connection_status == "CONNECTED"
    assert ccxt.get_account_summary().broker_type.value == "ccxt"
    assert binance.get_account_summary().broker_type.value == "binance_spot"
    assert generic.get_account_summary().broker_type.value == "generic_rest"


def test_execution_mode_controller_default_simulation() -> None:
    """Test default SIMULATION mode and switching between PAPER and LIVE."""
    router = OrderRouter()
    assert router.current_mode == ExecutionMode.SIMULATION

    router.set_execution_mode(ExecutionMode.PAPER)
    assert router.current_mode == ExecutionMode.PAPER

    router.set_execution_mode(ExecutionMode.LIVE)
    assert router.current_mode == ExecutionMode.LIVE


def test_live_order_requires_user_confirmation() -> None:
    """Test that LIVE mode orders WITHOUT explicit user confirmation are REJECTED."""
    router = OrderRouter(mode=ExecutionMode.LIVE)

    unconfirmed_req = BrokerOrderRequest(
        symbol="AAPL",
        side="BUY",
        order_type="MARKET",
        quantity=10.0,
        user_explicit_confirmation=False,  # Unconfirmed
    )

    res_rejected = router.route_order(unconfirmed_req)
    assert res_rejected.status == "REJECTED"
    assert "explicit user confirmation" in res_rejected.rejection_reason

    # Confirmed request
    confirmed_req = BrokerOrderRequest(
        symbol="AAPL",
        side="BUY",
        order_type="MARKET",
        quantity=10.0,
        user_explicit_confirmation=True,  # Confirmed by user
    )

    res_approved = router.route_order(confirmed_req)
    assert res_approved.status == "FILLED"


def test_audit_trail_logging() -> None:
    """Test BrokerAuditManager logging for actions."""
    mgr = BrokerAuditManager()
    req = BrokerOrderRequest(symbol="NVDA", side="BUY", order_type="MARKET", quantity=5.0)
    res = AlpacaBrokerProvider().submit_order(req)

    rec = mgr.log_action("alpaca", ExecutionMode.SIMULATION, req, res)
    assert rec.audit_id.startswith("aud_")
    assert rec.broker_name == "alpaca"
    assert rec.execution_mode == ExecutionMode.SIMULATION


def test_broker_observability_telemetry() -> None:
    """Test BrokerObservabilityTracker latency and health metric tracking."""
    tracker = BrokerObservabilityTracker("alpaca")
    tracker.record_latency(14.2)
    tracker.record_rejection()
    snapshot = tracker.get_health_snapshot()

    assert snapshot.broker_latency_ms == 14.2
    assert snapshot.rejected_orders_count == 1
    assert snapshot.connection_health == "CONNECTED"


@pytest.mark.asyncio
async def test_broker_api_endpoints() -> None:
    """Test Broker REST API endpoints (/account, /positions, /preview-order, /submit-order, /mode, /audit-log, /telemetry)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_acc = await client.get("/api/v1/broker/account")
        res_pos = await client.get("/api/v1/broker/positions")
        res_mode = await client.post("/api/v1/broker/mode?mode=SIMULATION")
        res_preview = await client.post(
            "/api/v1/broker/preview-order",
            json={"symbol": "AAPL", "side": "BUY", "order_type": "MARKET", "quantity": 5.0},
        )
        res_submit = await client.post(
            "/api/v1/broker/submit-order",
            json={
                "symbol": "AAPL",
                "side": "BUY",
                "order_type": "MARKET",
                "quantity": 5.0,
                "user_explicit_confirmation": True,
            },
        )
        res_audit = await client.get("/api/v1/broker/audit-log")
        res_telem = await client.get("/api/v1/broker/telemetry")

    assert res_acc.status_code == 200
    assert res_pos.status_code == 200
    assert res_mode.status_code == 200
    assert res_preview.status_code == 200
    assert res_submit.status_code == 200
    assert res_audit.status_code == 200
    assert res_telem.status_code == 200
