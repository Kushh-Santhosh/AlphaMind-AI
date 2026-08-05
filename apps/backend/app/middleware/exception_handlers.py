"""
FastAPI Exception Handlers — Maps domain exceptions to HTTP responses.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.backend.app.exceptions import (
    AgentExecutionException,
    AlphaMindBaseException,
    DataProviderException,
    ForbiddenException,
    HallucinationVerificationException,
    PredictionSafetyViolationException,
    UnauthorizedException,
)

MANDATORY_DISCLAIMER = (
    "DISCLAIMER: AlphaMind AI is an automated quantitative research engine. "
    "All outputs are for informational and educational purposes only and do not "
    "constitute financial, investment, legal, or tax advice."
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom domain exception handlers on the FastAPI app instance."""

    @app.exception_handler(AlphaMindBaseException)
    async def alphamind_exception_handler(
        request: Request, exc: AlphaMindBaseException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "disclaimer": MANDATORY_DISCLAIMER},
        )

    @app.exception_handler(DataProviderException)
    async def data_provider_handler(request: Request, exc: DataProviderException) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={"error": exc.message, "hint": "System is in fallback data mode."},
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
        return JSONResponse(status_code=401, content={"error": exc.message})

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
        return JSONResponse(status_code=403, content={"error": exc.message})

    @app.exception_handler(HallucinationVerificationException)
    async def hallucination_handler(
        request: Request, exc: HallucinationVerificationException
    ) -> JSONResponse:
        return JSONResponse(status_code=422, content={"error": exc.message})

    @app.exception_handler(PredictionSafetyViolationException)
    async def prediction_safety_handler(
        request: Request, exc: PredictionSafetyViolationException
    ) -> JSONResponse:
        return JSONResponse(status_code=422, content={"error": exc.message})

    @app.exception_handler(AgentExecutionException)
    async def agent_exception_handler(
        request: Request, exc: AgentExecutionException
    ) -> JSONResponse:
        return JSONResponse(status_code=500, content={"error": exc.message})
