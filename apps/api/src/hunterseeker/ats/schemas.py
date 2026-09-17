"""API contract for ATS templates.

"ATS" here is *our* configurable, savable, reusable hiring pipeline (AGENTS.md §3) —
never a third-party system. The data model keeps two kinds of stage explicit:

- ``screening`` stages carry machine-evaluable criteria the matching engine runs against
  a Profile *before* a Job is ever surfaced. They are the ATS gate.
- ``human`` stages (phone screen, interview, offer) happen after a Match. They are never
  part of screening.
"""

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field

type CriterionOperator = Literal["eq", "neq", "gte", "lte", "in", "contains_all", "contains_any"]


class ScreeningCriterion(BaseModel):
    """One machine-evaluable check against a Profile field."""

    field: str = Field(
        description="Profile field the check reads, e.g. `work_authorization`, `skills`."
    )
    operator: CriterionOperator
    value: str | int | float | bool | list[str]


class ScreeningStage(BaseModel):
    kind: Literal["screening"] = "screening"
    name: str
    criteria: list[ScreeningCriterion] = Field(
        description="All must pass. Evaluated by the engine before any Match exists."
    )


class HumanStage(BaseModel):
    kind: Literal["human"] = "human"
    name: str
    description: str | None = None


type AtsStage = Annotated[ScreeningStage | HumanStage, Field(discriminator="kind")]


class AtsTemplate(BaseModel):
    id: UUID
    hunter_id: UUID
    name: str
    stages: list[AtsStage] = Field(description="In pipeline order. Screening stages come first.")
    created_at: datetime
    updated_at: datetime
