"""
Financial Research Disclaimer Injection Middleware.
Ensures every API response body includes the mandatory SEC/FINRA disclaimer.
"""

from collections.abc import Awaitable, Callable
from typing import cast

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

MANDATORY_SEC_FINRA_DISCLAIMER = (
    "AlphaMind AI is an automated quantitative research engine. "
    "All outputs, probability distributions, confidence intervals, and research signals "
    "are for informational and educational purposes only and do not constitute financial, "
    "investment, legal, or tax advice. Past quantitative performance is no guarantee of "
    "future outcomes. Trading financial instruments carries substantial risk of loss."
)


class DisclaimerMiddleware(BaseHTTPMiddleware):
    """
    Middleware that injects the mandatory financial research disclaimer
    into all JSON API responses containing prediction or research payloads.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        response.headers["X-Financial-Disclaimer"] = MANDATORY_SEC_FINRA_DISCLAIMER
        return cast(Response, response)
