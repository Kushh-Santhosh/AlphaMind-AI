"""
API v1 — Broker Integration Layer Router
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from packages.portfolio.broker_audit import BrokerAuditManager
from packages.portfolio.broker_observability import BrokerObservabilityTracker
from packages.portfolio.broker_provider import (
    AlpacaBrokerProvider,
    BrokerOrderRequest,
    BrokerProvider,
)
from packages.portfolio.order_router import ExecutionMode, OrderRouter

router = APIRouter(prefix="/api/v1/broker", tags=["Broker Integration Layer"])

order_router = OrderRouter(mode=ExecutionMode.SIMULATION)
audit_manager = BrokerAuditManager()
telemetry_tracker = BrokerObservabilityTracker()
broker_provider: BrokerProvider = AlpacaBrokerProvider()


@router.get("/account")
async def get_broker_account() -> dict[str, Any]:
    """Fetch broker account summary, cash, buying power, and margin requirement."""
    summary = broker_provider.get_account_summary()
    return summary.model_dump()


@router.get("/positions")
async def get_broker_positions() -> list[dict[str, Any]]:
    """Fetch active broker positions."""
    positions = broker_provider.get_positions()
    return [p.model_dump() for p in positions]


@router.post("/mode")
async def set_execution_mode(mode: ExecutionMode) -> dict[str, Any]:
    """Switch execution mode between SIMULATION, PAPER, and LIVE."""
    new_mode = order_router.set_execution_mode(mode)
    return {"current_execution_mode": new_mode.value}


@router.post("/preview-order")
async def preview_order(order_req: BrokerOrderRequest) -> dict[str, Any]:
    """Preview order cost, margin impact, and fee estimations without execution."""
    preview = broker_provider.preview_order(order_req)
    return preview


@router.post("/submit-order")
async def submit_broker_order(order_req: BrokerOrderRequest) -> dict[str, Any]:
    """
    Submit order through execution mode router.
    STRICT MANDATE: LIVE mode orders require explicit user confirmation.
    """
    res = order_router.route_order(order_req)

    # Log audit record
    audit = audit_manager.log_action(
        broker_name=broker_provider.provider_type.value,
        execution_mode=order_router.current_mode,
        order_req=order_req,
        order_res=res,
        risk_result="PASSED" if res.status != "REJECTED" else "REJECTED",
    )

    if res.status == "REJECTED":
        telemetry_tracker.record_rejection()
        raise HTTPException(status_code=400, detail=res.rejection_reason)

    return {
        "order_response": res.model_dump(),
        "audit_id": audit.audit_id,
        "execution_mode": order_router.current_mode.value,
    }


@router.delete("/orders/{order_id}")
async def cancel_broker_order(order_id: str) -> dict[str, Any]:
    """Cancel order at broker."""
    success = broker_provider.cancel_order(order_id)
    return {"order_id": order_id, "cancelled": success}


@router.get("/audit-log")
async def get_broker_audit_log() -> list[dict[str, Any]]:
    """Fetch complete audit trail records for all broker interactions."""
    return [a.model_dump() for a in audit_manager.audit_records]


@router.get("/telemetry")
async def get_broker_telemetry() -> dict[str, Any]:
    """Fetch broker latency, failure count, and connection health snapshot."""
    snapshot = telemetry_tracker.get_health_snapshot()
    return snapshot.model_dump()
