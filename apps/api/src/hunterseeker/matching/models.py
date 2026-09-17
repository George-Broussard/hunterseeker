"""pgvector-backed embedding rows for Seeker Profiles and Jobs.

One row per Profile / Job. Each row carries:

* the vector itself, plus the provenance needed to know whether it is still valid —
  ``model`` and ``schema_version`` (which model and which ``to_text()`` format produced
  it) and ``source_updated_at`` / ``embedded_at`` (staleness is simply
  ``source_updated_at > embedded_at``; see ``is_stale``). Embeddings are derived data
  (AGENTS.md §6) — a stale row must be re-embedded, never trusted.
* the **hard-constraint filter columns** (AGENTS.md §6): location, remote policy,
  compensation, work authorization, seniority. They sit on the same row so one SQL
  statement can ``WHERE`` on them and then ``ORDER BY embedding <=> :query``. They are
  filters, never score inputs, and never part of the embedded text — that split is what
  ``hunterseeker.matching.embedding_docs`` exists to enforce.

Nothing on these tables is a protected characteristic or a proxy for one (AGENTS.md
§9). Location is deliberately coarse (country + region, no city/ZIP). Work
authorization is a legal hard constraint that §6 names explicitly; it is filter-only and
must never reach a score or an embedding.

``profile_id`` / ``job_id`` are not yet foreign keys because the ``profiles`` and
``jobs`` tables do not exist. Add the constraints in the migration that creates them.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Index, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declared_attr, mapped_column
from sqlalchemy.sql import ColumnElement

from hunterseeker.core.db import Base
from hunterseeker.core.settings import get_settings
from hunterseeker.matching.embedding_docs import SeniorityBand

# The column width comes from settings until issue #4 fixes the embedding model.
EMBEDDING_DIM: int = get_settings().embedding_dim


class RemotePolicy(StrEnum):
    """Where the work happens. A Job has exactly one; a Seeker accepts one or more."""

    ONSITE = "onsite"
    HYBRID = "hybrid"
    REMOTE = "remote"


# Named Postgres enum types, shared by both tables. ``create_type=False`` on reuse is not
# needed: SQLAlchemy de-duplicates by name within one metadata.
remote_policy_enum = Enum(
    RemotePolicy, name="remote_policy", values_callable=lambda e: [m.value for m in e]
)
seniority_band_enum = Enum(
    SeniorityBand, name="seniority_band", values_callable=lambda e: [m.value for m in e]
)


class EmbeddingRowMixin:
    """Columns every embedding table has: the vector and its provenance."""

    @declared_attr
    @classmethod
    def embedding(cls) -> Mapped[list[float]]:
        return mapped_column(Vector(EMBEDDING_DIM), nullable=False, sort_order=10)

    model: Mapped[str] = mapped_column(String(128), nullable=False, sort_order=11)
    """Identifier of the embedding model that produced ``embedding``."""

    schema_version: Mapped[int] = mapped_column(nullable=False, sort_order=12)
    """``EMBEDDING_SCHEMA_VERSION`` of the ``to_text()`` format that was embedded."""

    source_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, sort_order=13
    )
    """``updated_at`` of the source Profile / Job row at the time it was embedded."""

    embedded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, sort_order=14
    )
    """When the vector was computed."""

    @hybrid_property
    def is_stale(self) -> bool:
        """The source row changed after this vector was computed."""
        return self.source_updated_at > self.embedded_at

    @is_stale.inplace.expression
    @classmethod
    def _is_stale_expression(cls) -> ColumnElement[bool]:
        return cls.source_updated_at > cls.embedded_at


class SeekerProfileEmbedding(EmbeddingRowMixin, Base):
    __tablename__ = "seeker_profile_embeddings"
    __table_args__ = (
        Index(
            "ix_seeker_profile_embeddings_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    # --- Hard-constraint filters (AGENTS.md §6). NULL means "no constraint stated". -------
    location_country: Mapped[str | None] = mapped_column(String(2))
    """ISO 3166-1 alpha-2 country the Seeker is based in."""
    location_region: Mapped[str | None] = mapped_column(String(64))
    """State / province / region within ``location_country``. Never city or ZIP."""
    remote_policies: Mapped[list[RemotePolicy]] = mapped_column(
        ARRAY(remote_policy_enum), nullable=False
    )
    """Remote policies the Seeker will accept. A Job must match one of them."""
    compensation_min: Mapped[int | None] = mapped_column(BigInteger)
    """Annual compensation floor in ``compensation_currency``. Jobs below it are filtered out."""
    compensation_currency: Mapped[str | None] = mapped_column(String(3))
    """ISO 4217 code for ``compensation_min``."""
    work_authorized_countries: Mapped[list[str]] = mapped_column(ARRAY(String(2)), nullable=False)
    """ISO 3166-1 alpha-2 countries the Seeker may work in without sponsorship."""
    seniority_band: Mapped[SeniorityBand | None] = mapped_column(seniority_band_enum)


class JobEmbedding(EmbeddingRowMixin, Base):
    __tablename__ = "job_embeddings"
    __table_args__ = (
        Index(
            "ix_job_embeddings_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    job_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    # --- Hard-constraint filters (AGENTS.md §6). NULL means "no constraint stated". -------
    location_country: Mapped[str | None] = mapped_column(String(2))
    """ISO 3166-1 alpha-2 country of employment (NULL for remote-anywhere roles)."""
    location_region: Mapped[str | None] = mapped_column(String(64))
    """State / province / region within ``location_country``. Never city or ZIP."""
    remote_policy: Mapped[RemotePolicy] = mapped_column(remote_policy_enum, nullable=False)
    compensation_min: Mapped[int | None] = mapped_column(BigInteger)
    """Annual compensation band, in ``compensation_currency``."""
    compensation_max: Mapped[int | None] = mapped_column(BigInteger)
    compensation_currency: Mapped[str | None] = mapped_column(String(3))
    """ISO 4217 code for the compensation band."""
    sponsorship_available: Mapped[bool] = mapped_column(Boolean, nullable=False)
    """Whether the Hunter will sponsor work authorization for this role."""
    seniority_band: Mapped[SeniorityBand] = mapped_column(seniority_band_enum, nullable=False)
