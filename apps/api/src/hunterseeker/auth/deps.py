"""FastAPI dependencies for authentication and persona authorization.

Usage in any domain router::

    @router.get("/jobs")
    async def list_jobs(user: Annotated[CurrentUser, Depends(require_role("hunter"))]): ...

Authorization is per-persona and explicit (AGENTS.md §8). ``get_current_user`` only proves
*who* is calling; ownership checks still belong in each endpoint.
"""

from collections.abc import Callable, Coroutine
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from hunterseeker.auth.models import Role
from hunterseeker.auth.tokens import CurrentUser, InvalidTokenError, decode_api_token
from hunterseeker.core.settings import Settings, get_settings

_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return decode_api_token(credentials.credentials, settings.auth_secret)
    except InvalidTokenError as exc:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def require_role(*roles: Role) -> Callable[..., Coroutine[Any, Any, CurrentUser]]:
    """Dependency factory: the caller must be authenticated *and* hold one of ``roles``."""

    async def _require(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Forbidden for this persona")
        return user

    return _require
