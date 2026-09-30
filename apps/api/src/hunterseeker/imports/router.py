"""Import endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from hunterseeker.auth.deps import require_role
from hunterseeker.auth.tokens import CurrentUser
from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.imports.schemas import ImportRun

router = APIRouter(prefix="/imports", tags=["imports"])

_STUB_RUN = ImportRun(
    id=UUID("00000000-0000-4000-8000-000000004001"),
    company_profile_id=UUID("00000000-0000-4000-8000-00000000c001"),
    source="greenhouse",
    status="succeeded",
    started_at=datetime(2026, 9, 17, 6, 0, tzinfo=UTC),
    finished_at=datetime(2026, 9, 17, 6, 2, tzinfo=UTC),
    jobs_seen=42,
    jobs_created=3,
    jobs_updated=39,
)


@router.get("/runs", summary="Import runs for the calling Hunter's Company Profiles")
async def list_import_runs(
    params: Annotated[CursorQuery, Query()],
    user: Annotated[CurrentUser, Depends(require_role("hunter"))],
) -> Page[ImportRun]:
    # TODO(imports): scope to Company Profiles `user` manages, once persisted.
    del params, user
    return Page(items=[_STUB_RUN], next_cursor=None)
