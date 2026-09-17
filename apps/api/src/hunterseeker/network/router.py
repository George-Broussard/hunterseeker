"""Network (Connections) endpoints. Stub implementation — fixed data in the real shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.core.schemas import UserSummary
from hunterseeker.network.schemas import Connection

router = APIRouter(prefix="/network", tags=["network"])

_STUB_CONNECTION = Connection(
    id=UUID("00000000-0000-4000-8000-000000005001"),
    user=UserSummary(
        id=UUID("00000000-0000-4000-8000-00000000e003"),
        persona="seeker",
        display_name="C. Connection",
    ),
    status="connected",
    connected_at=datetime(2026, 8, 1, tzinfo=UTC),
)


@router.get("/connections", summary="The caller's Connections")
async def list_connections(params: Annotated[CursorQuery, Query()]) -> Page[Connection]:
    # TODO(auth): any persona; scoped to the caller. Same endpoint for Seekers and Hunters.
    del params
    return Page(items=[_STUB_CONNECTION], next_cursor=None)
