"""Pydantic models shared by more than one domain's API contract."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

type Persona = Literal["seeker", "hunter"]


class UserSummary(BaseModel):
    """The minimal public view of a user, embedded wherever a user is referenced."""

    id: UUID
    persona: Persona
    display_name: str = Field(description="What other users see. Never a legal name.")
