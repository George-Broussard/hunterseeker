"""Fixtures for the auth domain.

Unit tests (passwords, tokens, the dependency) need no database. Router tests need the
``users`` table; they run against ``DATABASE_URL`` and skip when Postgres is unreachable
so ``uv run pytest`` still works without Docker. CI always has the database.
"""

import os
import uuid
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from hunterseeker.auth.models import User
from hunterseeker.core.app import create_app
from hunterseeker.core.db import get_session
from hunterseeker.core.settings import get_settings

TEST_SECRET = "test-secret-not-for-production-at-least-32-bytes"


@pytest.fixture(autouse=True)
def _auth_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUTH_SECRET", TEST_SECRET)
    get_settings.cache_clear()


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """A session on a throwaway ``users`` table. Skips if Postgres is not reachable."""
    url = os.environ.get("DATABASE_URL", get_settings().database_url)
    engine = create_async_engine(url, poolclass=None)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(User.__table__.create, checkfirst=True)  # type: ignore[attr-defined]
    except OSError as exc:  # connection refused etc.
        await engine.dispose()
        pytest.skip(f"Postgres not reachable at {url!r}: {exc}")

    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            yield session
    finally:
        async with engine.begin() as conn:
            await conn.execute(text("DELETE FROM users WHERE email LIKE 'pytest-%@example.com'"))
        await engine.dispose()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    app = create_app()

    async def _override() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_session] = _override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def unique_email() -> str:
    return f"pytest-{uuid.uuid4().hex[:12]}@example.com"
