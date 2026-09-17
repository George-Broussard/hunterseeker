"""API contract for Seeker Profiles.

A Profile is the Seeker's structured self-description and the input to matching. It is
distinct from the Account (auth/billing) and from a Company Profile. Protected
characteristics (and their proxies — photos, graduation years, ZIP codes) are never
fields here; see AGENTS.md §9.
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

type WorkAuthorization = Literal["citizen", "permanent_resident", "visa", "needs_sponsorship"]
type Seniority = Literal["intern", "junior", "mid", "senior", "staff", "principal", "executive"]


class Profile(BaseModel):
    id: UUID
    seeker_id: UUID
    headline: str | None = Field(default=None, max_length=200)
    summary: str | None = Field(default=None, max_length=4000)
    skills: list[str] = Field(default_factory=list)
    locations: list[str] = Field(
        default_factory=list, description="Metro areas the Seeker will work in."
    )
    remote_ok: bool = True
    work_authorization: WorkAuthorization | None = None
    compensation_floor: int | None = Field(
        default=None,
        ge=0,
        description="Annual, in `currency`. A hard constraint, not a score input.",
    )
    currency: str = Field(default="USD", description="ISO 4217 code.")
    seniority: Seniority | None = None
    match_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Seeker-controlled floor. Matches below it are not surfaced.",
    )
    updated_at: datetime


class ProfileUpdate(BaseModel):
    """PATCH body: every field optional; omitted fields are left unchanged."""

    headline: str | None = Field(default=None, max_length=200)
    summary: str | None = Field(default=None, max_length=4000)
    skills: list[str] | None = None
    locations: list[str] | None = None
    remote_ok: bool | None = None
    work_authorization: WorkAuthorization | None = None
    compensation_floor: int | None = Field(default=None, ge=0)
    currency: str | None = None
    seniority: Seniority | None = None
    match_threshold: float | None = Field(default=None, ge=0.0, le=1.0)
