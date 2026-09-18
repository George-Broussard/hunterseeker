"""Matching endpoints: the Seeker's Job Board and the Hunter's ranked candidate lists.

Stub implementation — returns fixed data in the real response shape. Business logic
(ATS gate, scoring, threshold) lands with the matching-engine issues.
"""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from hunterseeker.core.errors import NotFoundError
from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.core.schemas import UserSummary
from hunterseeker.matching.schemas import (
    JobSummary,
    MatchedCandidate,
    MatchedJob,
    OpenRole,
    RolePipelineCounts,
)

router = APIRouter(prefix="/matching", tags=["matching"])

_STUB_JOB = JobSummary(
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
)
_STUB_MATCHED_JOB = MatchedJob(
    id=UUID("00000000-0000-4000-8000-00000000f001"),
    score=0.87,
    computed_at=datetime(2026, 9, 17, tzinfo=UTC),
    job=_STUB_JOB,
)
_STUB_CANDIDATE = MatchedCandidate(
    id=_STUB_MATCHED_JOB.id,
    score=_STUB_MATCHED_JOB.score,
    computed_at=_STUB_MATCHED_JOB.computed_at,
    seeker=UserSummary(
        id=UUID("00000000-0000-4000-8000-00000000e001"), persona="seeker", display_name="A. Seeker"
    ),
    headline="Backend engineer, distributed systems",
)

# --- Hunter: open roles -------------------------------------------------------------
# Two Company Profiles so the Hunter home's company selector path is exercised.
_STUB_JOB_2 = JobSummary(
    id=UUID("00000000-0000-4000-8000-00000000a002"),
    title="Product Designer",
    company_profile_id=UUID("00000000-0000-4000-8000-00000000c002"),
    company_name="Acme Robotics",
    location="Remote (US)",
    remote=True,
    compensation_min=140_000,
    compensation_max=170_000,
    seniority="mid",
    posted_at=datetime(2026, 9, 12, tzinfo=UTC),
)


def _stub_candidate(
    match_suffix: str, seeker_suffix: str, name: str, score: float, headline: str
) -> MatchedCandidate:
    return MatchedCandidate(
        id=UUID(f"00000000-0000-4000-8000-00000000f{match_suffix}"),
        score=score,
        computed_at=datetime(2026, 9, 17, tzinfo=UTC),
        seeker=UserSummary(
            id=UUID(f"00000000-0000-4000-8000-00000000e{seeker_suffix}"),
            persona="seeker",
            display_name=name,
        ),
        headline=headline,
    )


_STUB_OPEN_ROLES = [
    OpenRole(
        job=_STUB_JOB,
        new_match_count=4,
        pipeline=RolePipelineCounts(screened=12, interviewing=3, offer=1),
        top_candidates=[
            _STUB_CANDIDATE,
            _stub_candidate("002", "004", "B. Seeker", 0.81, "Platform engineer, Go and Postgres"),
            _stub_candidate("003", "005", "D. Seeker", 0.76, "Backend engineer, payments"),
        ],
    ),
    OpenRole(
        job=_STUB_JOB_2,
        new_match_count=0,
        pipeline=RolePipelineCounts(screened=5, interviewing=0, offer=0),
        top_candidates=[
            _stub_candidate("004", "006", "E. Seeker", 0.72, "Product designer, developer tools"),
        ],
    ),
]


@router.get("/job-board", summary="The calling Seeker's Job Board")
async def list_job_board(params: Annotated[CursorQuery, Query()]) -> Page[MatchedJob]:
    """Matches for the calling Seeker at or above their match threshold, best first."""
    # TODO(auth): seeker-only; scoped to the caller's own Profile.
    del params  # TODO(matching): cursor over (score desc, id) once Matches are persisted.
    return Page(items=[_STUB_MATCHED_JOB], next_cursor=None)


@router.get("/matches/{match_id}", summary="One Match, Seeker view")
async def get_match(match_id: UUID) -> MatchedJob:
    # TODO(auth): seeker-only; the Match must belong to the caller.
    if match_id != _STUB_MATCHED_JOB.id:
        raise NotFoundError("Match not found.", {"match_id": str(match_id)})
    return _STUB_MATCHED_JOB


@router.get("/jobs/{job_id}/candidates", summary="Ranked candidates for a Job")
async def list_candidates(
    job_id: UUID, params: Annotated[CursorQuery, Query()]
) -> Page[MatchedCandidate]:
    """Every Seeker whose Profile passed this Job's ATS screening, best Match first."""
    # TODO(auth): hunter-only; the Job must belong to a Company Profile the caller manages.
    del params
    if job_id != _STUB_JOB.id:
        raise NotFoundError("Job not found.", {"job_id": str(job_id)})
    return Page(items=[_STUB_CANDIDATE], next_cursor=None)


@router.get("/open-roles", summary="The calling Hunter's open roles with Match activity")
async def list_open_roles(params: Annotated[CursorQuery, Query()]) -> Page[OpenRole]:
    """Open Jobs on the Company Profiles the caller manages, most recently posted first.

    Each role carries its new-Match count, pipeline counts, and the top three ranked
    candidates. Candidates are Matches, so all of them have passed the Job's ATS screening.
    """
    # TODO(auth): hunter-only; scoped to Jobs on Company Profiles the caller manages.
    # TODO(matching): "new since last visit" needs a per-Hunter last-viewed timestamp.
    del params
    return Page(items=_STUB_OPEN_ROLES, next_cursor=None)
