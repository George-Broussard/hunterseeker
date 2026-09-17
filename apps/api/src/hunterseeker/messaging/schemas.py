"""API contract for messaging. One system for both personas (AGENTS.md §7)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from hunterseeker.core.schemas import UserSummary


class Message(BaseModel):
    id: UUID
    conversation_id: UUID
    sender: UserSummary
    body: str = Field(max_length=10_000)
    sent_at: datetime


class Conversation(BaseModel):
    id: UUID
    participants: list[UserSummary] = Field(min_length=2)
    last_message: Message | None = None
    unread_count: int = Field(ge=0, description="Unread by the caller.")
    updated_at: datetime
