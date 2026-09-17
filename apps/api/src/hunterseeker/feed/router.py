"""Feed endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.core.schemas import UserSummary
from hunterseeker.feed.schemas import FeedItem, MatchedJobItem, Post
from hunterseeker.matching.schemas import JobSummary, MatchedJob

router = APIRouter(prefix="/feed", tags=["feed"])

_STUB_ITEMS: list[FeedItem] = [
    Post(
        id=UUID("00000000-0000-4000-8000-000000006001"),
        author=UserSummary(
            id=UUID("00000000-0000-4000-8000-00000000e003"),
            persona="seeker",
            display_name="C. Connection",
        ),
        body="Just wrapped up a migration to pgvector — happy to compare notes.",
        created_at=datetime(2026, 9, 16, 9, 0, tzinfo=UTC),
    ),
    MatchedJobItem(
        id=UUID("00000000-0000-4000-8000-000000006002"),
        match=MatchedJob(
            id=UUID("00000000-0000-4000-8000-00000000f001"),
            score=0.87,
            computed_at=datetime(2026, 9, 17, tzinfo=UTC),
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
        ),
        created_at=datetime(2026, 9, 17, tzinfo=UTC),
    ),
]


@router.get("", summary="The calling Seeker's Feed")
async def list_feed(params: Annotated[CursorQuery, Query()]) -> Page[FeedItem]:
    """Posts from the Seeker's Connections interleaved with new Matches, newest first.

    Matches respect the Seeker's match threshold, as on every seeker-facing surface.
    """
    # TODO(auth): seeker-only; scoped to the caller.
    del params
    return Page(items=_STUB_ITEMS, next_cursor=None)
