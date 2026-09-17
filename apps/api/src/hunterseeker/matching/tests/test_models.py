"""Embedding tables: shape, provenance columns, filter columns, HNSW index, staleness.

These run against the ORM metadata only (no database). The live migration is exercised
by ``alembic upgrade head`` + ``alembic check`` in CI.
"""

from datetime import UTC, datetime, timedelta

import pytest
from pgvector.sqlalchemy import Vector
from sqlalchemy import Index, Table, select

from hunterseeker.core.db import Base
from hunterseeker.core.settings import get_settings
from hunterseeker.matching.models import (
    JobEmbedding,
    RemotePolicy,
    SeekerProfileEmbedding,
)


def _table(model: type[Base]) -> Table:
    table = model.__table__
    assert isinstance(table, Table)
    return table


PROVENANCE_COLUMNS = {"embedding", "model", "schema_version", "source_updated_at", "embedded_at"}


@pytest.mark.parametrize(
    ("model", "table_name", "pk"),
    [
        (SeekerProfileEmbedding, "seeker_profile_embeddings", "profile_id"),
        (JobEmbedding, "job_embeddings", "job_id"),
    ],
    ids=["seeker_profile", "job"],
)
def test_table_shape(model: type[Base], table_name: str, pk: str) -> None:
    table = _table(model)
    assert table.name == table_name
    assert [c.name for c in table.primary_key.columns] == [pk]
    assert set(table.columns.keys()) >= PROVENANCE_COLUMNS
    for name in PROVENANCE_COLUMNS:
        assert not table.columns[name].nullable, name


@pytest.mark.parametrize("model", [SeekerProfileEmbedding, JobEmbedding])
def test_vector_width_comes_from_settings(model: type[Base]) -> None:
    column = _table(model).columns["embedding"]
    assert isinstance(column.type, Vector)
    assert column.type.dim == get_settings().embedding_dim


@pytest.mark.parametrize("model", [SeekerProfileEmbedding, JobEmbedding])
def test_hnsw_cosine_index(model: type[Base]) -> None:
    table = _table(model)
    hnsw = [ix for ix in table.indexes if ix.dialect_options["postgresql"]["using"] == "hnsw"]
    assert len(hnsw) == 1
    index: Index = hnsw[0]
    assert [c.name for c in index.columns] == ["embedding"]
    assert index.dialect_options["postgresql"]["ops"] == {"embedding": "vector_cosine_ops"}
    assert index.name == f"ix_{table.name}_embedding_hnsw"


def test_seeker_filter_columns() -> None:
    cols = set(SeekerProfileEmbedding.__table__.columns.keys())
    assert {
        "location_country",
        "location_region",
        "remote_policies",
        "compensation_min",
        "compensation_currency",
        "work_authorized_countries",
        "seniority_band",
    } <= cols


def test_job_filter_columns() -> None:
    cols = set(JobEmbedding.__table__.columns.keys())
    assert {
        "location_country",
        "location_region",
        "remote_policy",
        "compensation_min",
        "compensation_max",
        "compensation_currency",
        "sponsorship_available",
        "seniority_band",
    } <= cols


@pytest.mark.parametrize("model", [SeekerProfileEmbedding, JobEmbedding])
def test_no_protected_characteristic_or_proxy_columns(model: type[Base]) -> None:
    """AGENTS.md §9: nothing on the embedding rows is a protected characteristic or proxy.

    Location is allowed only at country/region granularity — never city or ZIP.
    """
    suspicious = (
        "name",
        "email",
        "phone",
        "photo",
        "birth",
        "age",
        "year",
        "school",
        "zip",
        "postal",
        "city",
        "address",
        "gender",
        "sex",
        "race",
        "ethnic",
        "nationality",
        "religion",
        "disab",
        "veteran",
    )
    table = _table(model)
    for column in table.columns.keys():  # noqa: SIM118 - ColumnCollection, not a dict
        for needle in suspicious:
            assert needle not in column, f"{table.name}.{column}"


def test_is_stale_in_python_and_sql() -> None:
    embedded = datetime(2026, 9, 17, 12, 0, tzinfo=UTC)
    fresh = JobEmbedding(source_updated_at=embedded, embedded_at=embedded)
    stale = JobEmbedding(source_updated_at=embedded + timedelta(seconds=1), embedded_at=embedded)
    assert fresh.is_stale is False
    assert stale.is_stale is True

    query = select(JobEmbedding.job_id).where(JobEmbedding.is_stale)
    sql = str(query)
    assert "job_embeddings.source_updated_at > job_embeddings.embedded_at" in sql


def test_remote_policy_values_are_stable() -> None:
    """These are Postgres enum labels; changing them is a migration."""
    assert [p.value for p in RemotePolicy] == ["onsite", "hybrid", "remote"]
