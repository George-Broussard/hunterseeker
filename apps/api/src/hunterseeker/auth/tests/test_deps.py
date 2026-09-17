"""``get_current_user`` / ``require_role`` behaviour, exercised through a throwaway app."""

import uuid
from collections.abc import AsyncIterator
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient

from hunterseeker.auth.deps import get_current_user, require_role
from hunterseeker.auth.tokens import CurrentUser, encode_api_token

from .conftest import TEST_SECRET

SEEKER = CurrentUser(id=uuid.uuid4(), role="seeker", email="s@example.com")
HUNTER = CurrentUser(id=uuid.uuid4(), role="hunter", email="h@example.com")


def _app() -> FastAPI:
    app = FastAPI()

    @app.get("/whoami")
    async def whoami(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        return user

    @app.get("/hunters-only")
    async def hunters_only(
        user: Annotated[CurrentUser, Depends(require_role("hunter"))],
    ) -> CurrentUser:
        return user

    return app


@pytest.fixture
async def api() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as c:
        yield c


def _bearer(user: CurrentUser) -> dict[str, str]:
    return {"Authorization": f"Bearer {encode_api_token(user, TEST_SECRET)}"}


async def test_no_token_is_401(api: AsyncClient) -> None:
    response = await api.get("/whoami")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


async def test_bad_token_is_401(api: AsyncClient) -> None:
    response = await api.get("/whoami", headers={"Authorization": "Bearer nope"})

    assert response.status_code == 401


async def test_valid_token_yields_user(api: AsyncClient) -> None:
    response = await api.get("/whoami", headers=_bearer(SEEKER))

    assert response.status_code == 200
    assert response.json() == {"id": str(SEEKER.id), "role": "seeker", "email": SEEKER.email}


async def test_require_role_denies_other_persona(api: AsyncClient) -> None:
    assert (await api.get("/hunters-only", headers=_bearer(SEEKER))).status_code == 403
    assert (await api.get("/hunters-only", headers=_bearer(HUNTER))).status_code == 200
