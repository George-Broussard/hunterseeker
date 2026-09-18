"""Account creation and credential verification."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from hunterseeker.auth.models import User
from hunterseeker.auth.passwords import hash_password_async, verify_password_async
from hunterseeker.auth.schemas import SignupRequest, VerifyCredentialsRequest


class EmailTakenError(Exception):
    """An account with this email already exists."""


def normalize_email(email: str) -> str:
    return email.strip().lower()


async def create_user(session: AsyncSession, data: SignupRequest) -> User:
    user = User(
        email=normalize_email(data.email),
        name=data.name,
        password_hash=await hash_password_async(data.password),
        role=data.role,
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise EmailTakenError from exc
    await session.refresh(user)
    return user


async def verify_credentials(session: AsyncSession, data: VerifyCredentialsRequest) -> User | None:
    """Return the user if the email/password pair is valid, else ``None``.

    Always runs one argon2 verification, even when the email is unknown, so response time
    does not reveal whether an account exists.
    """
    result = await session.execute(select(User).where(User.email == normalize_email(data.email)))
    user = result.scalar_one_or_none()
    ok = await verify_password_async(data.password, user.password_hash if user else None)
    return user if ok and user is not None else None
