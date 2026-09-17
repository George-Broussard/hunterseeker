"""Messaging endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.core.schemas import UserSummary
from hunterseeker.messaging.schemas import Conversation, Message

router = APIRouter(prefix="/messaging", tags=["messaging"])

_SEEKER = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e001"), persona="seeker", display_name="A. Seeker"
)
_HUNTER = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e002"), persona="hunter", display_name="H. Hunter"
)
_STUB_CONVERSATION_ID = UUID("00000000-0000-4000-8000-000000007001")
_STUB_CONVERSATION = Conversation(
    id=_STUB_CONVERSATION_ID,
    participants=[_SEEKER, _HUNTER],
    last_message=Message(
        id=UUID("00000000-0000-4000-8000-000000007101"),
        conversation_id=_STUB_CONVERSATION_ID,
        sender=_HUNTER,
        body="Thanks for your interest — are you free for a call this week?",
        sent_at=datetime(2026, 9, 16, 15, 30, tzinfo=UTC),
    ),
    unread_count=1,
    updated_at=datetime(2026, 9, 16, 15, 30, tzinfo=UTC),
)


@router.get("/conversations", summary="The caller's conversations, most recent first")
async def list_conversations(params: Annotated[CursorQuery, Query()]) -> Page[Conversation]:
    # TODO(auth): any persona; scoped to conversations the caller participates in.
    del params
    return Page(items=[_STUB_CONVERSATION], next_cursor=None)
