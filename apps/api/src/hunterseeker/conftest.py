"""Shared pytest fixtures: an app instance, an in-process HTTP client, and auth headers
for every domain's tests.
"""

import uuid
from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from hunterseeker.auth.models import Role
from hunterseeker.auth.tokens import CurrentUser, encode_api_token
from hunterseeker.core.app import create_app
from hunterseeker.core.settings import get_settings


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


def _bearer_headers(role: Role) -> dict[str, str]:
    user = CurrentUser(id=uuid.uuid4(), role=role, email=f"pytest-{role}@example.com")
    token = encode_api_token(user, get_settings().auth_secret)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def seeker_headers() -> dict[str, str]:
    """A valid bearer token for a Seeker. Domain tests use this to reach persona-gated endpoints."""
    return _bearer_headers("seeker")


@pytest.fixture
def hunter_headers() -> dict[str, str]:
    """A valid bearer token for a Hunter. Domain tests use this to reach persona-gated endpoints."""
    return _bearer_headers("hunter")
