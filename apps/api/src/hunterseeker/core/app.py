"""FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute

from hunterseeker.applications.router import router as applications_router
from hunterseeker.ats.router import router as ats_router
from hunterseeker.auth.router import router as auth_router
from hunterseeker.core.db import get_engine
from hunterseeker.core.errors import ERROR_RESPONSES, install_error_handlers
from hunterseeker.feed.router import router as feed_router
from hunterseeker.imports.router import router as imports_router
from hunterseeker.matching.router import router as matching_router
from hunterseeker.messaging.router import router as messaging_router
from hunterseeker.network.router import router as network_router
from hunterseeker.profiles.router import router as profiles_router

API_V1_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Dispose of the connection pool when the process shuts down."""
    try:
        yield
    finally:
        await get_engine().dispose()


def _operation_id(route: APIRoute) -> str:
    """`<tag>_<function name>` — stable, readable ids for the generated TS client."""
    tag = str(route.tags[0]) if route.tags else "root"
    return f"{tag}_{route.name}"


def create_app() -> FastAPI:
    """Build the FastAPI app. Each domain's router is mounted under ``/api/v1/<domain>``."""
    app = FastAPI(
        title="hunter/seeker API",
        version="0.1.0",
        lifespan=lifespan,
        generate_unique_id_function=_operation_id,
        responses=ERROR_RESPONSES,
    )
    install_error_handlers(app)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    api_v1 = APIRouter(prefix=API_V1_PREFIX)
    api_v1.include_router(profiles_router)
    api_v1.include_router(matching_router)
    api_v1.include_router(applications_router)
    api_v1.include_router(ats_router)
    api_v1.include_router(messaging_router)
    api_v1.include_router(feed_router)
    api_v1.include_router(network_router)
    api_v1.include_router(imports_router)
    app.include_router(api_v1)
    app.include_router(auth_router, prefix="/api/v1")

    return app
