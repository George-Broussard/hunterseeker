"""Embedding docs: deterministic text, and nothing from AGENTS.md §9 can get in."""

import re
from typing import Any

import pytest
from pydantic import ValidationError

from hunterseeker.matching.embedding_docs import (
    EMBEDDING_SCHEMA_VERSION,
    JobEmbeddingDoc,
    RoleHistoryEntry,
    SeekerProfileEmbeddingDoc,
    SeniorityBand,
    TenureBand,
)

# --- Rich fixtures ---------------------------------------------------------------------
# These are what a *full* Profile / Job record might look like once those domains exist.
# Every key that is NOT a doc field is something §6 or §9 says must not be embedded.
# The values are chosen to be distinctive so a substring check is meaningful.

SEEKER_FORBIDDEN: dict[str, Any] = {
    # §9: protected characteristics and proxies
    "full_name": "Ximena Okonkwo-Bartholomew",
    "email": "ximena.okb@example.test",
    "phone": "+1-555-0199-7342",
    "photo_url": "https://cdn.example.test/photos/ximena-8843.jpg",
    "date_of_birth": "1987-04-12",
    "age": 39,
    "graduation_year": 2009,
    "school": "Whitmore Polytechnic Institute",
    "zip_code": "94112",
    "city": "Daly City",
    "street_address": "1234 Mission Street",
    "gender": "female",
    "nationality": "Nigerian",
    "linkedin_url": "https://linkedin.example.test/in/ximenaokb",
    "employment_start_dates": ["2019-03-01", "2015-06-15"],
    "employer_names": ["Zephyrline Robotics", "Cobalt Harbor Analytics"],
    # §6: hard constraints are filter columns, not embedded text
    "location_country": "US",
    "location_region": "CA",
    "remote_policies": ["remote", "hybrid"],
    "compensation_min": 185000,
    "compensation_currency": "USD",
    "work_authorized_countries": ["US", "NG"],
}

SEEKER_ALLOWED: dict[str, Any] = {
    "skills": ("Python", "PostgreSQL", "Kubernetes", "distributed systems"),
    "role_history": (
        {
            "title": "Staff Backend Engineer",
            "seniority_band": "staff",
            "responsibilities_summary": "Owned the ingestion platform and its on-call rotation.",
            "tenure_band": "3_to_6_years",
        },
        {
            "title": "Backend Engineer",
            "seniority_band": "mid",
            "responsibilities_summary": "Built billing services in Python.",
            "tenure_band": "1_to_3_years",
        },
    ),
    "target_roles": ("Staff Engineer", "Principal Engineer"),
    "target_industries": ("robotics", "developer tools"),
    "work_style_preferences": ("async-first", "small teams"),
    "self_summary": "Backend engineer who likes owning systems end to end.",
}

JOB_FORBIDDEN: dict[str, Any] = {
    # §6: filter columns
    "location_country": "DE",
    "location_region": "BE",
    "remote_policy": "hybrid",
    "compensation_min": 95000,
    "compensation_max": 130000,
    "compensation_currency": "EUR",
    "sponsorship_available": True,
    "work_authorization_required": "EU work permit",
    # not the work itself
    "company_name": "Quillfeather Logistics GmbH",
    "hunter_name": "Bartholomew Quillfeather",
    "hunter_email": "bq@quillfeather.example.test",
    "office_address": "Torstrasse 99, 10119 Berlin",
    "posted_at": "2026-09-01",
    "external_id": "greenhouse-4471902",
}

JOB_ALLOWED: dict[str, Any] = {
    "title": "Senior Backend Engineer, Routing",
    "team_summary": "The routing team plans multi-stop deliveries in real time.",
    "responsibilities": (
        "Design and operate the route optimisation service.",
        "Mentor engineers on the team.",
    ),
    "required_skills": ("Go", "PostgreSQL", "graph algorithms"),
    "nice_to_have_skills": ("OR-Tools", "Kubernetes"),
    "seniority_band": "senior",
}


def _all_forbidden_values(record: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for value in record.values():
        if isinstance(value, list):
            out.extend(str(v) for v in value)
        else:
            out.append(str(value))
    return out


# --- Snapshot ----------------------------------------------------------------------------

SEEKER_SNAPSHOT = """\
[hunterseeker seeker_profile embedding schema v1]
skills: distributed systems; Kubernetes; PostgreSQL; Python
role history:
- title: Staff Backend Engineer | seniority: staff | tenure: 3_to_6_years | responsibilities: Owned the ingestion platform and its on-call rotation.
- title: Backend Engineer | seniority: mid | tenure: 1_to_3_years | responsibilities: Built billing services in Python.
target roles: Principal Engineer; Staff Engineer
target industries: developer tools; robotics
work style preferences: async-first; small teams
summary: Backend engineer who likes owning systems end to end."""  # noqa: E501

JOB_SNAPSHOT = """\
[hunterseeker job embedding schema v1]
title: Senior Backend Engineer, Routing
seniority: senior
team: The routing team plans multi-stop deliveries in real time.
responsibilities:
- Design and operate the route optimisation service.
- Mentor engineers on the team.
required skills: Go; graph algorithms; PostgreSQL
nice to have skills: Kubernetes; OR-Tools"""


def test_seeker_to_text_snapshot() -> None:
    assert SeekerProfileEmbeddingDoc(**SEEKER_ALLOWED).to_text() == SEEKER_SNAPSHOT


def test_job_to_text_snapshot() -> None:
    assert JobEmbeddingDoc(**JOB_ALLOWED).to_text() == JOB_SNAPSHOT


def test_snapshots_are_tagged_with_schema_version() -> None:
    assert EMBEDDING_SCHEMA_VERSION == 1, "bump the snapshots when you bump the version"
    tag = f"embedding schema v{EMBEDDING_SCHEMA_VERSION}]"
    assert SEEKER_SNAPSHOT.splitlines()[0].endswith(tag)
    assert JOB_SNAPSHOT.splitlines()[0].endswith(tag)


# --- Determinism -------------------------------------------------------------------------


def test_set_like_fields_are_order_insensitive_and_deduplicated() -> None:
    a = SeekerProfileEmbeddingDoc(skills=("Python", "SQL", "Go"))
    b = SeekerProfileEmbeddingDoc(skills=("Go", "  SQL\n", "python", "Python"))
    assert a.to_text() == b.to_text()
    assert a.skills == ("Go", "Python", "SQL")
    # Case-variants collapse to one spelling regardless of which came first.
    assert (
        SeekerProfileEmbeddingDoc(skills=("go", "Go")).skills
        == SeekerProfileEmbeddingDoc(skills=("Go", "go")).skills
        == ("Go",)
    )


def test_role_history_and_responsibilities_preserve_order() -> None:
    first = RoleHistoryEntry(
        title="A",
        seniority_band=SeniorityBand.MID,
        responsibilities_summary="a",
        tenure_band=TenureBand.UNDER_1_YEAR,
    )
    second = first.model_copy(update={"title": "B"})
    assert (
        SeekerProfileEmbeddingDoc(role_history=(first, second)).to_text()
        != SeekerProfileEmbeddingDoc(role_history=(second, first)).to_text()
    )
    assert (
        JobEmbeddingDoc(title="t", seniority_band="mid", responsibilities=("x", "y")).to_text()
        != JobEmbeddingDoc(title="t", seniority_band="mid", responsibilities=("y", "x")).to_text()
    )


def test_whitespace_is_normalized_so_line_format_is_stable() -> None:
    doc = JobEmbeddingDoc(
        title="  Senior\n\tEngineer ",
        team_summary="line one\n\nline two",
        seniority_band="senior",
        responsibilities=("  ", "keep\nthis"),
    )
    text = doc.to_text()
    assert "title: Senior Engineer" in text
    assert "team: line one line two" in text
    assert text.count("\n- ") == 1
    assert "- keep this" in text


def test_empty_docs_still_serialize_every_field() -> None:
    text = SeekerProfileEmbeddingDoc().to_text()
    assert text.splitlines() == [
        "[hunterseeker seeker_profile embedding schema v1]",
        "skills: ",
        "role history:",
        "target roles: ",
        "target industries: ",
        "work style preferences: ",
        "summary: ",
    ]


# --- AGENTS.md §9 / §6: exclusion by construction --------------------------------------


@pytest.mark.parametrize(
    ("doc_cls", "allowed", "forbidden"),
    [
        (SeekerProfileEmbeddingDoc, SEEKER_ALLOWED, SEEKER_FORBIDDEN),
        (JobEmbeddingDoc, JOB_ALLOWED, JOB_FORBIDDEN),
    ],
    ids=["seeker_profile", "job"],
)
def test_forbidden_record_fields_do_not_exist_on_the_doc(
    doc_cls: type[SeekerProfileEmbeddingDoc | JobEmbeddingDoc],
    allowed: dict[str, Any],
    forbidden: dict[str, Any],
) -> None:
    full_record = {**allowed, **forbidden}

    # The model has no field for any of them ...
    assert set(doc_cls.model_fields).isdisjoint(forbidden)
    # ... so building the doc from the full record is a hard error, not a silent drop.
    with pytest.raises(ValidationError) as excinfo:
        doc_cls(**full_record)
    rejected = {err["loc"][0] for err in excinfo.value.errors() if err["type"] == "extra_forbidden"}
    assert rejected == set(forbidden)


@pytest.mark.parametrize(
    ("doc_cls", "allowed", "forbidden"),
    [
        (SeekerProfileEmbeddingDoc, SEEKER_ALLOWED, SEEKER_FORBIDDEN),
        (JobEmbeddingDoc, JOB_ALLOWED, JOB_FORBIDDEN),
    ],
    ids=["seeker_profile", "job"],
)
def test_forbidden_values_never_reach_the_embedded_text(
    doc_cls: type[SeekerProfileEmbeddingDoc | JobEmbeddingDoc],
    allowed: dict[str, Any],
    forbidden: dict[str, Any],
) -> None:
    full_record = {**allowed, **forbidden}
    # The only legitimate way to get from a full record to a doc: pick the doc's fields.
    projection = {name: full_record[name] for name in doc_cls.model_fields}

    text = doc_cls(**projection).to_text()

    for value in _all_forbidden_values(forbidden):
        # Token match, not substring: "US" must not trip on "ind-us-tries".
        pattern = rf"(?<!\w){re.escape(value)}(?!\w)"
        assert not re.search(pattern, text, re.IGNORECASE), f"{value!r} leaked into the text"


def test_no_field_name_hints_at_a_protected_characteristic() -> None:
    """Guard against the *names* of fields drifting toward §9 territory."""
    suspicious = (
        "name",
        "email",
        "phone",
        "photo",
        "birth",
        "age",
        "year",
        "date",
        "school",
        "university",
        "college",
        "degree",
        "zip",
        "postal",
        "city",
        "address",
        "gender",
        "sex",
        "race",
        "ethnic",
        "national",
        "religion",
        "disab",
        "veteran",
        "marital",
        "employer",
        "company",
    )
    for model in (SeekerProfileEmbeddingDoc, JobEmbeddingDoc, RoleHistoryEntry):
        for field_name in model.model_fields:
            for needle in suspicious:
                assert needle not in field_name, f"{model.__name__}.{field_name}"


def test_docs_are_immutable() -> None:
    doc = JobEmbeddingDoc(title="t", seniority_band="mid")
    with pytest.raises(ValidationError):
        doc.title = "changed"  # type: ignore[misc]
