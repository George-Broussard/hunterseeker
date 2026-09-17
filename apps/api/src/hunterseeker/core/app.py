"""FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from hunterseeker.core.db import get_engine


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Dispose of the connection pool when the process shuts down."""
    try:
        yield
    finally:
        await get_engine().dispose()


def create_app() -> FastAPI:
    """Build the FastAPI app. Domain routers get mounted here as they are built."""
    app = FastAPI(title="hunter/seeker API", version="0.1.0", lifespan=lifespan)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
