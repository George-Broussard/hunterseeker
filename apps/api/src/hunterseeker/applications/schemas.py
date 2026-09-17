"""API contract for Applications: a Seeker's submission to a Job, moving through its ATS."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from hunterseeker.matching.schemas import JobSummary

type ApplicationStatus = Literal[
    "submitted", "in_review", "interviewing", "offered", "hired", "rejected", "withdrawn"
]


class Application(BaseModel):
    id: UUID
    job: JobSummary
    match_id: UUID = Field(
        description="The Match this Application came through. Applications exist only via a Match."
    )
    status: ApplicationStatus
    current_stage: str = Field(description="Name of the ATS stage the Application is in.")
    submitted_at: datetime
    updated_at: datetime
