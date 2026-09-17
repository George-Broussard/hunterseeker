"""The bearer token ``apps/web`` sends on every API call.

Auth.js keeps its own (encrypted) session cookie in the browser. For the API it mints a
separate, plain HS256 JWT signed with the shared ``AUTH_SECRET``; see
``apps/web/src/lib/auth/api-token.ts`` for the issuing side. Claims:

- ``sub`` / ``user_id``: the account's UUID
- ``role``: ``"hunter"`` or ``"seeker"`` (the persona claim decided in #3)
- ``email``: for display/logging correlation only — never authorize on it
- ``iss`` / ``aud`` / ``iat`` / ``exp``: standard, checked here
"""

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, cast

import jwt

from hunterseeker.auth.models import ROLES, Role

ISSUER = "hunterseeker-web"
AUDIENCE = "hunterseeker-api"
ALGORITHM = "HS256"


@dataclass(frozen=True, slots=True)
class CurrentUser:
    """The authenticated caller, as asserted by a valid token. No database round-trip."""

    id: uuid.UUID
    role: Role
    email: str


class InvalidTokenError(Exception):
    """The bearer token is missing, malformed, expired, or otherwise not trusted."""


def decode_api_token(token: str, secret: str) -> CurrentUser:
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={"require": ["exp", "iat", "sub", "role"]},
        )
    except jwt.PyJWTError as exc:
        raise InvalidTokenError(str(exc)) from exc

    role = payload.get("role")
    if role not in ROLES:
        raise InvalidTokenError("unknown role claim")
    try:
        user_id = uuid.UUID(str(payload["sub"]))
    except ValueError as exc:
        raise InvalidTokenError("sub is not a UUID") from exc

    return CurrentUser(id=user_id, role=cast(Role, role), email=str(payload.get("email", "")))


def encode_api_token(user: CurrentUser, secret: str, *, ttl: timedelta = timedelta(hours=1)) -> str:
    """Mint a token the same way the web app does. Used by tests and local tooling."""
    now = datetime.now(UTC)
    claims: dict[str, Any] = {
        "sub": str(user.id),
        "user_id": str(user.id),
        "role": user.role,
        "email": user.email,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "exp": now + ttl,
    }
    return jwt.encode(claims, secret, algorithm=ALGORITHM)
