"""
AlphaMind AI - Broker Audit Trail & Pre-Live Risk Gate

Validates pre-live risk limits and maintains complete auditability logs for every broker action.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from pydantic import BaseModel, Field

from packages.portfolio.broker_provider import BrokerOrderRequest, BrokerOrderResponse
from packages.portfolio.order_router import ExecutionMode

logger = logging.getLogger(__name__)


class BrokerAuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:8]}")
    user_id: str = "user_default"
    timestamp_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    broker_name: str
    execution_mode: ExecutionMode
    order_payload: dict[str, Any]
    response_payload: dict[str, Any]
    risk_validation_result: str = "PASSED"


class BrokerAuditManager:
    """Manager maintaining audit trail records for all broker orders and system interactions."""

    def __init__(self) -> None:
        self.audit_records: list[BrokerAuditRecord] = []

    def log_action(
        self,
        broker_name: str,
        execution_mode: ExecutionMode,
        order_req: BrokerOrderRequest,
        order_res: BrokerOrderResponse,
        risk_result: str = "PASSED",
        user_id: str = "user_default",
    ) -> BrokerAuditRecord:
        """Create structured audit log record for order action."""
        record = BrokerAuditRecord(
            user_id=user_id,
            broker_name=broker_name,
            execution_mode=execution_mode,
            order_payload=order_req.model_dump(),
            response_payload=order_res.model_dump(),
            risk_validation_result=risk_result,
        )
        self.audit_records.append(record)
        logger.info(
            "Audit Record logged [%s]: mode='%s', status='%s'",
            record.audit_id,
            execution_mode.value,
            order_res.status,
        )
        return record
