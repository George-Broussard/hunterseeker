"""API contract for job imports from external recruiting platforms."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

type ImportSource = Literal["ashby", "greenhouse"]
type ImportRunStatus = Literal["queued", "running", "succeeded", "failed"]


class ImportRun(BaseModel):
    """One execution of an import. Idempotent per external job id; re-runs never duplicate."""

    id: UUID
    company_profile_id: UUID
    source: ImportSource
    status: ImportRunStatus
    started_at: datetime | None = None
    finished_at: datetime | None = None
    jobs_seen: int = Field(default=0, ge=0)
    jobs_created: int = Field(default=0, ge=0)
    jobs_updated: int = Field(default=0, ge=0)
    error: str | None = Field(default=None, description="Set when `status` is `failed`.")
