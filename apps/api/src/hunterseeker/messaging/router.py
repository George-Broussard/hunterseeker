"""Messaging endpoints. Stub implementation — fixed data in the real response shape."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Query, status

from hunterseeker.core.errors import NotFoundError
from hunterseeker.core.pagination import CursorQuery, Page
from hunterseeker.core.schemas import UserSummary
from hunterseeker.messaging.schemas import Conversation, Message, MessageCreate

router = APIRouter(prefix="/messaging", tags=["messaging"])

# TODO(auth): the caller, once the token identifies them.
_SEEKER = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e001"), persona="seeker", display_name="A. Seeker"
)
_HUNTER = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e002"), persona="hunter", display_name="H. Hunter"
)
_CONNECTION = UserSummary(
    id=UUID("00000000-0000-4000-8000-00000000e003"), persona="seeker", display_name="C. Connection"
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
_STUB_CONVERSATION_2_ID = UUID("00000000-0000-4000-8000-000000007002")
_STUB_CONVERSATION_2 = Conversation(
    id=_STUB_CONVERSATION_2_ID,
    participants=[_SEEKER, _CONNECTION],
    last_message=Message(
        id=UUID("00000000-0000-4000-8000-000000007201"),
        conversation_id=_STUB_CONVERSATION_2_ID,
        sender=_SEEKER,
        body="Sounds good, I'll send over the notes tomorrow.",
        sent_at=datetime(2026, 9, 14, 11, 5, tzinfo=UTC),
    ),
    unread_count=0,
    updated_at=datetime(2026, 9, 14, 11, 5, tzinfo=UTC),
)
_STUB_CONVERSATIONS = {c.id: c for c in (_STUB_CONVERSATION, _STUB_CONVERSATION_2)}


@router.get("/conversations", summary="The caller's conversations, most recent first")
async def list_conversations(params: Annotated[CursorQuery, Query()]) -> Page[Conversation]:
    # TODO(auth): any persona; scoped to conversations the caller participates in.
    del params
    return Page(items=list(_STUB_CONVERSATIONS.values()), next_cursor=None)


@router.post(
    "/conversations/{conversation_id}/messages",
    status_code=status.HTTP_201_CREATED,
    summary="Send a message in a conversation",
)
async def send_message(conversation_id: UUID, body: MessageCreate) -> Message:
    # TODO(auth): any persona; the caller must participate in the conversation.
    # TODO(messaging): persist and deliver; transport is an open question (AGENTS.md §11).
    if conversation_id not in _STUB_CONVERSATIONS:
        raise NotFoundError("Conversation not found.", {"conversation_id": str(conversation_id)})
    return Message(
        id=uuid4(),
        conversation_id=conversation_id,
        sender=_SEEKER,
        body=body.body,
        sent_at=datetime.now(UTC),
    )
