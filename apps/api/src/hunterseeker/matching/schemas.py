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
