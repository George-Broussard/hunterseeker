"""ATS template endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from hunterseeker.ats.schemas import AtsTemplate, HumanStage, ScreeningCriterion, ScreeningStage
from hunterseeker.core.pagination import CursorQuery, Page

router = APIRouter(prefix="/ats", tags=["ats"])

_STUB_TEMPLATE = AtsTemplate(
    id=UUID("00000000-0000-4000-8000-000000009001"),
    hunter_id=UUID("00000000-0000-4000-8000-00000000e002"),
    name="Senior engineering default",
    stages=[
        ScreeningStage(
            name="Eligibility screen",
            criteria=[
                ScreeningCriterion(
                    field="work_authorization", operator="neq", value="needs_sponsorship"
                ),
                ScreeningCriterion(field="skills", operator="contains_all", value=["python"]),
            ],
        ),
        HumanStage(name="Hiring manager review"),
        HumanStage(name="Technical interview"),
        HumanStage(name="Offer"),
    ],
    created_at=datetime(2026, 8, 20, tzinfo=UTC),
    updated_at=datetime(2026, 8, 20, tzinfo=UTC),
)


@router.get("/templates", summary="The calling Hunter's ATS templates")
async def list_templates(params: Annotated[CursorQuery, Query()]) -> Page[AtsTemplate]:
    # TODO(auth): hunter-only; scoped to templates the caller owns.
    del params
    return Page(items=[_STUB_TEMPLATE], next_cursor=None)
