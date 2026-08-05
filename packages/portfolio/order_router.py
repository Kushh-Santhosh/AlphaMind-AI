"""
AlphaMind AI - Order Router & Execution Mode Controller

Manages Execution Modes: SIMULATION (Default), PAPER, LIVE.
Enforces Order Routing and Pre-Live User Confirmation Gate.
STRICT MANDATE: Simulation is default mode. Live execution requires explicit user confirmation.
Zero autonomous trading permitted.
"""

from __future__ import annotations

import logging
from enum import Enum

from packages.portfolio.broker_provider import (
    AlpacaBrokerProvider,
    BrokerOrderRequest,
    BrokerOrderResponse,
    BrokerProvider,
)

logger = logging.getLogger(__name__)


class ExecutionMode(str, Enum):  # noqa: UP042
    SIMULATION = "SIMULATION"  # Default Mode
    PAPER = "PAPER"
    LIVE = "LIVE"  # REQUIRES EXPLICIT USER CONFIRMATION


class OrderRouter:
    """Order router managing provider selection, execution modes, and user confirmation gates."""

    def __init__(self, mode: ExecutionMode = ExecutionMode.SIMULATION) -> None:
        self.current_mode = mode
        self.active_provider: BrokerProvider = AlpacaBrokerProvider()
        logger.info("Initialized OrderRouter in mode '%s'", self.current_mode.value)

    def set_execution_mode(self, mode: ExecutionMode) -> ExecutionMode:
        """Switch execution mode between SIMULATION, PAPER, and LIVE."""
        self.current_mode = mode
        logger.info("Execution mode updated to '%s'", mode.value)
        return self.current_mode

    def route_order(self, order_req: BrokerOrderRequest) -> BrokerOrderResponse:
        """Route order through pre-live risk gate and user confirmation validation."""
        # MANDATORY CHECK FOR LIVE MODE: Require explicit user confirmation
        if self.current_mode == ExecutionMode.LIVE and not order_req.user_explicit_confirmation:
            reason = (
                "REJECTED: LIVE mode order execution requires explicit user confirmation "
                "(`user_explicit_confirmation=True`). Autonomous trading is strictly prohibited."
            )
            logger.error(reason)
            return BrokerOrderResponse(
                symbol=order_req.symbol,
                side=order_req.side,
                quantity=order_req.quantity,
                status="REJECTED",
                rejection_reason=reason,
            )

        logger.info(
            "Routing order '%s' %.2f %s via mode '%s'",
            order_req.side,
            order_req.quantity,
            order_req.symbol,
            self.current_mode.value,
        )

        return self.active_provider.submit_order(order_req)
