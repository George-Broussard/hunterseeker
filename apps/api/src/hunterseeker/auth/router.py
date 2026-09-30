"""``/api/v1/auth`` — called server-side by ``apps/web`` (Auth.js Credentials provider).

Persona access: ``signup`` and ``verify`` are unauthenticated by nature (they are how a
session comes to exist); ``me`` requires a valid bearer token for either persona.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from hunterseeker.auth.deps import get_current_user
from hunterseeker.auth.schemas import SignupRequest, UserOut, VerifyCredentialsRequest
from hunterseeker.auth.service import (
    EmailTakenError,
    create_user,
    normalize_email,
    verify_credentials,
)
from hunterseeker.auth.tokens import CurrentUser
from hunterseeker.core.db import get_session
from hunterseeker.core.ratelimit import RateLimiter, client_ip, get_rate_limiter
from hunterseeker.core.settings import Settings, get_settings

router = APIRouter(prefix="/auth", tags=["auth"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
RateLimiterDep = Annotated[RateLimiter, Depends(get_rate_limiter)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def signup(
    data: SignupRequest,
    session: SessionDep,
    request: Request,
    limiter: RateLimiterDep,
    settings: SettingsDep,
) -> UserOut:
    """Create an account with the chosen persona. 409 if the email is already registered.

    Rate-limited per IP (``signup_rate_limit_per_ip`` within
    ``signup_rate_limit_window_seconds``) to bound signup spam — every attempt counts,
    not just successful ones.
    """
    ip_key = f"signup:ip:{client_ip(request)}"
    if not limiter.allowed(
        ip_key,
        limit=settings.signup_rate_limit_per_ip,
        window_seconds=settings.signup_rate_limit_window_seconds,
    ):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many signup attempts")
    limiter.record(ip_key, window_seconds=settings.signup_rate_limit_window_seconds)

    try:
        user = await create_user(session, data)
    except EmailTakenError as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="An account with this email already exists"
        ) from exc
    return UserOut.model_validate(user)


@router.post("/verify", response_model=UserOut)
async def verify(
    data: VerifyCredentialsRequest,
    session: SessionDep,
    request: Request,
    limiter: RateLimiterDep,
    settings: SettingsDep,
) -> UserOut:
    """Check an email/password pair. 401 on any failure — the reason is never disclosed.

    Locked out (429) after ``verify_rate_limit_per_email`` failed attempts for this email,
    or ``verify_rate_limit_per_ip`` failed attempts from this IP, within
    ``verify_rate_limit_window_seconds``. A successful verify never counts against either
    budget, so it never locks out a legitimate, already-correct login.
    """
    email_key = f"verify:email:{normalize_email(data.email)}"
    ip_key = f"verify:ip:{client_ip(request)}"
    window = settings.verify_rate_limit_window_seconds
    if not limiter.allowed(
        email_key, limit=settings.verify_rate_limit_per_email, window_seconds=window
    ) or not limiter.allowed(
        ip_key, limit=settings.verify_rate_limit_per_ip, window_seconds=window
    ):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many verify attempts")

    user = await verify_credentials(session, data)
    if user is None:
        limiter.record(email_key, window_seconds=window)
        limiter.record(ip_key, window_seconds=window)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return UserOut.model_validate(user)


@router.get("/me")
async def me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    """Echo the caller's identity as asserted by their bearer token."""
    return user
