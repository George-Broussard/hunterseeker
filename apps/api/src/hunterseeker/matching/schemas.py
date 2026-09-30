"""API contract for the matching domain.

A Match is one object with two views (AGENTS.md §6: one score, two views):
:class:`MatchedJob` is what a Seeker sees on the Job Board and in the Feed;
:class:`MatchedCandidate` is what a Hunter sees in a role's ranked candidate list.
Both carry the same :class:`MatchBase` fields.
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from hunterseeker.core.schemas import UserSummary


class JobSummary(BaseModel):
    """A Job as referenced from a Match, an Application, or the Feed."""

    id: UUID
    title: str
    company_profile_id: UUID
    company_name: str
    location: str | None = None
    remote: bool = False
    compensation_min: int | None = Field(default=None, description="Annual, in `currency`.")
    compensation_max: int | None = Field(default=None, description="Annual, in `currency`.")
    currency: str = Field(default="USD", description="ISO 4217 code.")
    seniority: str | None = None
    posted_at: datetime


class MatchBase(BaseModel):
    """Fields every view of a Match shares."""

    id: UUID
    score: float = Field(ge=0.0, le=1.0, description="Normalized 0-1 Match score.")
    ats_pass: Literal[True] = Field(
        default=True,
        description=(
            "Always `true`: a Match exists only if the Seeker's Profile has already passed "
            "the Job's ATS screening. Present so the invariant is visible in the contract."
        ),
    )
    computed_at: datetime = Field(description="When `score` was last (re)computed.")


class MatchedJob(MatchBase):
    """Seeker-side view of a Match: the Job it recommends."""

    job: JobSummary


class MatchedCandidate(MatchBase):
    """Hunter-side view of the same Match: the Seeker it surfaces."""

    seeker: UserSummary
    headline: str | None = Field(
        default=None,
        description="The Seeker's Profile headline. Readable only through this Match.",
    )


class RolePipelineCounts(BaseModel):
    """How many Seekers sit at each point of a Job's pipeline, as shown on a role card."""

    screened: int = Field(
        ge=0,
        description=(
            "Matches for the Job: every Seeker whose Profile passed its ATS screening. "
            "This is the whole candidate pool — nobody unscreened is counted anywhere."
        ),
    )
    interviewing: int = Field(
        ge=0, description="Applications currently in a human interview stage."
    )
    offer: int = Field(ge=0, description="Applications with an offer extended.")


class OpenRole(BaseModel):
    """Hunter-side summary of one open Job: its Match activity and pipeline state.

    The Hunter's mirror of the Job Board card. ``top_candidates`` are Matches, so each one
    has already passed the Job's ATS screening (``ats_pass`` is always ``true``).
    """

    job: JobSummary
    new_match_count: int = Field(
        ge=0, description="Matches created since the calling Hunter last viewed this role."
    )
    pipeline: RolePipelineCounts
    top_candidates: list[MatchedCandidate] = Field(
        max_length=3,
        description="Highest-scoring Matches for the Job, best first. At most three.",
    )
