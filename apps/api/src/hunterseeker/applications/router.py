"""Application endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from hunterseeker.applications.schemas import Application
from hunterseeker.auth.deps import require_role
from hunterseeker.auth.tokens import CurrentUser
from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.matching.schemas import JobSummary

router = APIRouter(prefix="/applications", tags=["applications"])

_STUB_APPLICATION = Application(
    id=UUID("00000000-0000-4000-8000-00000000b001"),
    job=JobSummary(
        id=UUID("00000000-0000-4000-8000-00000000a001"),
        title="Senior Backend Engineer",
        company_profile_id=UUID("00000000-0000-4000-8000-00000000c001"),
        company_name="Example Co",
        location="Austin, TX",
        remote=True,
        compensation_min=160_000,
        compensation_max=200_000,
        seniority="senior",
        posted_at=datetime(2026, 9, 1, tzinfo=UTC),
    ),
    match_id=UUID("00000000-0000-4000-8000-00000000f001"),
    status="in_review",
    current_stage="Hiring manager review",
    submitted_at=datetime(2026, 9, 10, tzinfo=UTC),
    updated_at=datetime(2026, 9, 12, tzinfo=UTC),
)


@router.get("", summary="The calling Seeker's Applications")
async def list_applications(
    params: Annotated[CursorQuery, Query()],
    user: Annotated[CurrentUser, Depends(require_role("seeker"))],
) -> Page[Application]:
    """The Seeker's application dashboard: every Application with its current status."""
    # TODO(applications): scope to `user`'s own Applications, once persisted.
    del params, user
    return Page(items=[_STUB_APPLICATION], next_cursor=None)
