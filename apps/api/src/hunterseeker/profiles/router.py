"""Profile endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from hunterseeker.auth.deps import require_role
from hunterseeker.auth.tokens import CurrentUser
from hunterseeker.profiles.schemas import Profile, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])

_STUB_PROFILE = Profile(
    id=UUID("00000000-0000-4000-8000-00000000d001"),
    seeker_id=UUID("00000000-0000-4000-8000-00000000e001"),
    headline="Backend engineer, distributed systems",
    summary="Ten years building high-throughput services in Python and Go.",
    skills=["python", "postgresql", "kubernetes"],
    locations=["Austin, TX"],
    remote_ok=True,
    work_authorization="citizen",
    compensation_floor=150_000,
    seniority="senior",
    match_threshold=0.6,
    updated_at=datetime(2026, 9, 15, tzinfo=UTC),
)


@router.get("/me", summary="The calling Seeker's Profile")
async def get_my_profile(
    user: Annotated[CurrentUser, Depends(require_role("seeker"))],
) -> Profile:
    """Returns the caller's own Profile. Hunters never read a Profile by ID — only the
    slice exposed through a Match or an Application (AGENTS.md §8)."""
    # TODO(profiles): return `user`'s own Profile, once Profiles are persisted.
    del user
    return _STUB_PROFILE


@router.patch("/me", summary="Update the calling Seeker's Profile")
async def update_my_profile(
    body: ProfileUpdate, user: Annotated[CurrentUser, Depends(require_role("seeker"))]
) -> Profile:
    """Partial update. Any change here must trigger re-embedding and re-matching."""
    # TODO(profiles): update `user`'s own Profile, once Profiles are persisted.
    # TODO(matching): enqueue re-embed + re-screen on write (AGENTS.md §6).
    del user
    return _STUB_PROFILE.model_copy(
        update={**body.model_dump(exclude_unset=True), "updated_at": datetime.now(UTC)}
    )
