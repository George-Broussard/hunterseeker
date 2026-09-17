"""Async SQLAlchemy engine, session factory, and declarative base.

Everything here is async (AGENTS.md §8). There are no sync sessions in this codebase.
"""

from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from hunterseeker.core.settings import get_settings


class Base(DeclarativeBase):
    """Declarative base for every ORM model.

    Domain packages define their models against this base; Alembic autogenerate reads
    ``Base.metadata``. Each domain package must be imported by ``alembic/env.py`` so its
    tables are registered before autogenerate runs.
    """


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """Return the process-wide async engine, constructed lazily on first use."""
    settings = get_settings()
    return create_async_engine(settings.database_url, echo=settings.echo_sql, pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the process-wide async session factory."""
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding one ``AsyncSession`` per request."""
    async with get_session_factory()() as session:
        yield session
