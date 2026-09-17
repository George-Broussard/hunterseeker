"""API contract for Connections: mutual professional links between any two users."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from hunterseeker.core.schemas import UserSummary

type ConnectionStatus = Literal["pending_sent", "pending_received", "connected"]


class Connection(BaseModel):
    id: UUID
    user: UserSummary = Field(description="The other party, from the caller's point of view.")
    status: ConnectionStatus
    connected_at: datetime | None = Field(default=None, description="Null until accepted.")
