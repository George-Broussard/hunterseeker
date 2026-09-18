"""Feed endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Query, status

from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.core.schemas import UserSummary
from hunterseeker.feed.schemas import FeedItem, MatchedJobItem, Post, PostCreate
from hunterseeker.matching.schemas import JobSummary, MatchedJob

router = APIRouter(prefix="/feed", tags=["feed"])

# TODO(auth): the caller, once the token identifies them.
_STUB_CALLER = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e001"), persona="seeker", display_name="A. Seeker"
)
_STUB_CONNECTION = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e003"), persona="seeker", display_name="C. Connection"
)
_STUB_HUNTER = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e002"), persona="hunter", display_name="H. Hunter"
)

_STUB_ITEMS: list[FeedItem] = [
    Post(
        id=UUID("00000000-0000-4000-8000-000000006001"),
        author=_STUB_CONNECTION,
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
    Post(
        id=UUID("00000000-0000-4000-8000-000000006003"),
        author=_STUB_HUNTER,
        body="We're opening two platform roles next month. Ask me anything about the team.",
        created_at=datetime(2026, 9, 15, 17, 45, tzinfo=UTC),
    ),
    MatchedJobItem(
        id=UUID("00000000-0000-4000-8000-000000006004"),
        match=MatchedJob(
            id=UUID("00000000-0000-4000-8000-00000000f002"),
            score=0.74,
            computed_at=datetime(2026, 9, 15, tzinfo=UTC),
            job=JobSummary(
                id=UUID("00000000-0000-4000-8000-00000000a002"),
                title="Staff Data Platform Engineer",
                company_profile_id=UUID("00000000-0000-4000-8000-00000000c002"),
                company_name="Northwind Analytics",
                location=None,
                remote=True,
                compensation_min=190_000,
                compensation_max=None,
                seniority="staff",
                posted_at=datetime(2026, 9, 10, tzinfo=UTC),
            ),
        ),
        created_at=datetime(2026, 9, 15, tzinfo=UTC),
    ),
]


@router.get("", summary="The calling Seeker's Feed")
async def list_feed(params: Annotated[CursorQuery, Query()]) -> Page[FeedItem]:
    """Posts from the Seeker's Connections interleaved with new Matches, newest first.

    Interleaving is done here, server-side; clients render one list and never merge two.
    Matches respect the Seeker's match threshold, as on every seeker-facing surface.
    """
    # TODO(auth): seeker-only; scoped to the caller.
    del params
    return Page(items=_STUB_ITEMS, next_cursor=None)


@router.post("/posts", status_code=status.HTTP_201_CREATED, summary="Publish a post")
async def create_post(body: PostCreate) -> Post:
    """Publish a text post to the caller's Connections' Feeds."""
    # TODO(auth): any persona; the author is the caller.
    # TODO(feed): persist; moderation model is an open question (AGENTS.md §11).
    return Post(id=uuid4(), author=_STUB_CALLER, body=body.body, created_at=datetime.now(UTC))
