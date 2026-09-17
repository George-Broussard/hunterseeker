"""ORM model for accounts.

An **Account** (this table) is distinct from a Seeker **Profile** and a **Company Profile**
(AGENTS.md §3); those hang off ``users.id`` in their own domains.
"""

import uuid
from datetime import datetime
from typing import Literal

from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from hunterseeker.core.db import Base

Role = Literal["hunter", "seeker"]
ROLES: tuple[Role, ...] = ("hunter", "seeker")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role IN ('hunter', 'seeker')", name="ck_users_role"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    """Lower-cased before storage; uniqueness is therefore case-insensitive."""

    name: Mapped[str] = mapped_column(String(200))
    password_hash: Mapped[str] = mapped_column(String(255))
    """argon2id PHC string. Never log or return this field."""

    role: Mapped[str] = mapped_column(String(16))
    """Persona chosen at signup: ``"hunter"`` or ``"seeker"``.

    Deliberately a plain column rather than a separate table (issue #7): one role per
    account for now, easy to lift into a many-to-many later when an account can be both.
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
