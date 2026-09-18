"""Feed endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Query, status

from hunterseeker.core.errors import NotFoundError
from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.core.schemas import UserSummary
from hunterseeker.feed.schemas import (
    CompanyPostCreate,
    CompanyProfileSummary,
    FeedItem,
    MatchedJobItem,
    Post,
)
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


# --- Hunter: company feed -------------------------------------------------------------
# Two Company Profiles so the composer's Company Profile selector path is exercised.
_HUNTER = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e002"), persona="hunter", display_name="H. Hunter"
)
_STUB_COMPANY_PROFILES = [
    CompanyProfileSummary(id=UUID("00000000-0000-4000-8000-00000000c001"), name="Example Co"),
    CompanyProfileSummary(id=UUID("00000000-0000-4000-8000-00000000c002"), name="Acme Robotics"),
]
_STUB_COMPANY_POSTS = [
    Post(
        id=UUID("00000000-0000-4000-8000-000000006101"),
        author=_HUNTER,
        company=_STUB_COMPANY_PROFILES[0],
        body="We're hiring a Senior Backend Engineer. Matches are already rolling in.",
        created_at=datetime(2026, 9, 16, 14, 0, tzinfo=UTC),
    ),
    Post(
        id=UUID("00000000-0000-4000-8000-000000006102"),
        author=UserSummary(
            id=UUID("00000000-0000-4000-8000-00000000e003"),
            persona="seeker",
            display_name="C. Connection",
        ),
        body="Just wrapped up a migration to pgvector — happy to compare notes.",
        created_at=datetime(2026, 9, 16, 9, 0, tzinfo=UTC),
    ),
    Post(
        id=UUID("00000000-0000-4000-8000-000000006103"),
        author=_HUNTER,
        company=_STUB_COMPANY_PROFILES[1],
        body="Acme Robotics is opening a design practice. First role is up now.",
        created_at=datetime(2026, 9, 12, 11, 30, tzinfo=UTC),
    ),
]
# Cursor stub: two pages so clients exercise `next_cursor`. Cursors stay opaque to clients.
_STUB_COMPANY_FEED_PAGE_2 = "stub-page-2"


@router.get("/company", summary="The calling Hunter's company feed")
async def list_company_feed(params: Annotated[CursorQuery, Query()]) -> Page[Post]:
    """Posts from the Company Profiles the caller manages and from their network, newest first."""
    # TODO(auth): hunter-only; scoped to the caller's Company Profiles and Connections.
    if params.cursor is None:
        return Page(items=_STUB_COMPANY_POSTS[:2], next_cursor=_STUB_COMPANY_FEED_PAGE_2)
    if params.cursor == _STUB_COMPANY_FEED_PAGE_2:
        return Page(items=_STUB_COMPANY_POSTS[2:], next_cursor=None)
    return Page(items=[], next_cursor=None)


@router.post(
    "/company/posts",
    status_code=status.HTTP_201_CREATED,
    summary="Post to the company feed as a Company Profile",
)
async def create_company_post(body: CompanyPostCreate) -> Post:
    # TODO(auth): hunter-only; the caller must manage `company_profile_id`.
    company = next((c for c in _STUB_COMPANY_PROFILES if c.id == body.company_profile_id), None)
    if company is None:
        raise NotFoundError(
            "Company Profile not found.", {"company_profile_id": str(body.company_profile_id)}
        )
    return Post(
        id=uuid4(), author=_HUNTER, company=company, body=body.body, created_at=datetime.now(UTC)
    )


@router.get("/company-profiles", summary="Company Profiles the calling Hunter manages")
async def list_company_profiles(
    params: Annotated[CursorQuery, Query()],
) -> Page[CompanyProfileSummary]:
    """The Company Profiles the caller may post as.

    Stopgap until a Company Profile domain exists.
    """
    # TODO(auth): hunter-only; scoped to the caller.
    del params
    return Page(items=_STUB_COMPANY_PROFILES, next_cursor=None)
