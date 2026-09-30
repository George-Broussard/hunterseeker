"""Network (Connections) endpoints. Stub implementation — fixed data in the real shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from hunterseeker.auth.deps import get_current_user
from hunterseeker.auth.tokens import CurrentUser
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
async def list_connections(
    params: Annotated[CursorQuery, Query()],
    user: Annotated[CurrentUser, Depends(get_current_user)],
) -> Page[Connection]:
    """Any persona; same endpoint for Seekers and Hunters."""
    # TODO(network): scope to `user`'s own Connections, once persisted.
    del params, user
    return Page(items=[_STUB_CONNECTION], next_cursor=None)
