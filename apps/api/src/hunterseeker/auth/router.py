"""``/api/v1/auth`` — called server-side by ``apps/web`` (Auth.js Credentials provider).

Persona access: ``signup`` and ``verify`` are unauthenticated by nature (they are how a
session comes to exist); ``me`` requires a valid bearer token for either persona.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from hunterseeker.auth.deps import get_current_user
from hunterseeker.auth.schemas import SignupRequest, UserOut, VerifyCredentialsRequest
from hunterseeker.auth.service import EmailTakenError, create_user, verify_credentials
from hunterseeker.auth.tokens import CurrentUser
from hunterseeker.core.db import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def signup(data: SignupRequest, session: SessionDep) -> UserOut:
    """Create an account with the chosen persona. 409 if the email is already registered."""
    try:
        user = await create_user(session, data)
    except EmailTakenError as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="An account with this email already exists"
        ) from exc
    return UserOut.model_validate(user)


@router.post("/verify", response_model=UserOut)
async def verify(data: VerifyCredentialsRequest, session: SessionDep) -> UserOut:
    """Check an email/password pair. 401 on any failure — the reason is never disclosed."""
    user = await verify_credentials(session, data)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return UserOut.model_validate(user)


@router.get("/me")
async def me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    """Echo the caller's identity as asserted by their bearer token."""
    return user
