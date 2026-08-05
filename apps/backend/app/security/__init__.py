"""
Backend Security — JWT Authentication & RBAC Dependency Utilities.
Stubs only. No business logic.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),  # noqa: B008
) -> dict[str, str]:
    """
    Dependency that validates JWT bearer token and returns user payload.
    Implementation stubbed — full JWT validation implemented in Milestone 4.
    """
    # STUB: Full JWT validation and user lookup implemented in Milestone 4
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication implementation pending Milestone 4.",
    )


async def require_role(role: str) -> None:
    """
    RBAC role enforcement dependency.
    Stub — full RBAC implementation in Milestone 4.
    """
    # STUB: Full RBAC check implemented in Milestone 4
    pass
