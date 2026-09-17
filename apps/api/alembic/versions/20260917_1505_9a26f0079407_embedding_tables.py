"""embedding tables

Revision ID: 9a26f0079407
Revises: 319842b92cee
Create Date: 2026-09-17 15:05:00.209080+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

from hunterseeker.core.settings import get_settings

# revision identifiers, used by Alembic.
revision: str = "9a26f0079407"
down_revision: str | Sequence[str] | None = "319842b92cee"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Vector width is a setting until issue #4 decides the embedding model. Changing it after
# these tables exist is a new migration plus a full re-embed.
EMBEDDING_DIM = get_settings().embedding_dim

# Shared Postgres enum types. ``create_type=False`` because we create/drop them explicitly
# below (they are used by both tables and by an ARRAY column, where implicit creation is
# unreliable).
remote_policy = postgresql.ENUM(
    "onsite", "hybrid", "remote", name="remote_policy", create_type=False
)
seniority_band = postgresql.ENUM(
    "entry",
    "mid",
    "senior",
    "staff",
    "principal",
    "executive",
    name="seniority_band",
    create_type=False,
)


def _hnsw_cosine_index(name: str, table: str) -> None:
    """HNSW index with cosine distance, as AGENTS.md §4 and issue #4 require."""
    op.create_index(
        name,
        table,
        ["embedding"],
        unique=False,
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )


def upgrade() -> None:
    bind = op.get_bind()
    remote_policy.create(bind, checkfirst=True)
    seniority_band.create(bind, checkfirst=True)

    op.create_table(
        "job_embeddings",
        sa.Column("job_id", sa.Uuid(), nullable=False),
        # Hard-constraint filter columns (AGENTS.md §6). NULL = no constraint stated.
        sa.Column("location_country", sa.String(length=2), nullable=True),
        sa.Column("location_region", sa.String(length=64), nullable=True),
        sa.Column("remote_policy", remote_policy, nullable=False),
        sa.Column("compensation_min", sa.BigInteger(), nullable=True),
        sa.Column("compensation_max", sa.BigInteger(), nullable=True),
        sa.Column("compensation_currency", sa.String(length=3), nullable=True),
        sa.Column("sponsorship_available", sa.Boolean(), nullable=False),
        sa.Column("seniority_band", seniority_band, nullable=False),
        # The vector and its provenance. Stale when source_updated_at > embedded_at.
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("embedded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("job_id"),
    )
    _hnsw_cosine_index("ix_job_embeddings_embedding_hnsw", "job_embeddings")

    op.create_table(
        "seeker_profile_embeddings",
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        # Hard-constraint filter columns (AGENTS.md §6). NULL = no constraint stated.
        sa.Column("location_country", sa.String(length=2), nullable=True),
        sa.Column("location_region", sa.String(length=64), nullable=True),
        sa.Column("remote_policies", postgresql.ARRAY(remote_policy), nullable=False),
        sa.Column("compensation_min", sa.BigInteger(), nullable=True),
        sa.Column("compensation_currency", sa.String(length=3), nullable=True),
        sa.Column(
            "work_authorized_countries", postgresql.ARRAY(sa.String(length=2)), nullable=False
        ),
        sa.Column("seniority_band", seniority_band, nullable=True),
        # The vector and its provenance. Stale when source_updated_at > embedded_at.
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("embedded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("profile_id"),
    )
    _hnsw_cosine_index("ix_seeker_profile_embeddings_embedding_hnsw", "seeker_profile_embeddings")


def downgrade() -> None:
    op.drop_index(
        "ix_seeker_profile_embeddings_embedding_hnsw", table_name="seeker_profile_embeddings"
    )
    op.drop_table("seeker_profile_embeddings")
    op.drop_index("ix_job_embeddings_embedding_hnsw", table_name="job_embeddings")
    op.drop_table("job_embeddings")

    bind = op.get_bind()
    seniority_band.drop(bind, checkfirst=True)
    remote_policy.drop(bind, checkfirst=True)
