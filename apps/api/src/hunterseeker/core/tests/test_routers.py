"""Every domain router is mounted under /api/v1/<domain> and its stubs return the contract."""

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from hunterseeker.core.app import API_V1_PREFIX

DOMAINS = ["profiles", "matching", "applications", "ats", "messaging", "feed", "network", "imports"]

# Any persona that passes auth reaches these; used for the generic contract tests below.
LIST_ENDPOINTS = [
    ("/api/v1/matching/job-board", "seeker_headers"),
    ("/api/v1/matching/jobs/00000000-0000-4000-8000-00000000a001/candidates", "hunter_headers"),
    ("/api/v1/applications", "seeker_headers"),
    ("/api/v1/ats/templates", "hunter_headers"),
    ("/api/v1/messaging/conversations", "seeker_headers"),
    ("/api/v1/feed", "seeker_headers"),
    ("/api/v1/network/connections", "seeker_headers"),
    ("/api/v1/imports/runs", "hunter_headers"),
]


@pytest.mark.parametrize("domain", DOMAINS)
def test_every_domain_is_mounted(app: FastAPI, domain: str) -> None:
    prefix = f"{API_V1_PREFIX}/{domain}"
    paths = app.openapi()["paths"]
    assert any(path.startswith(prefix) for path in paths), f"no routes under {prefix}"


@pytest.mark.parametrize(("path", "headers_fixture"), LIST_ENDPOINTS)
async def test_list_endpoints_are_cursor_paginated(
    client: AsyncClient, request: pytest.FixtureRequest, path: str, headers_fixture: str
) -> None:
    headers = request.getfixturevalue(headers_fixture)
    response = await client.get(path, params={"limit": 5}, headers=headers)

    assert response.status_code == 200, response.text
    body = response.json()
    assert set(body) == {"items", "next_cursor"}
    assert isinstance(body["items"], list) and body["items"]
    assert body["next_cursor"] is None


async def test_job_board_matches_carry_score_and_ats_pass(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    body = (await client.get("/api/v1/matching/job-board", headers=seeker_headers)).json()

    match = body["items"][0]
    assert 0.0 <= match["score"] <= 1.0
    assert match["ats_pass"] is True
    assert match["job"]["title"]


async def test_candidate_list_is_the_same_match_from_the_hunter_side(
    client: AsyncClient, seeker_headers: dict[str, str], hunter_headers: dict[str, str]
) -> None:
    job_board = (await client.get("/api/v1/matching/job-board", headers=seeker_headers)).json()[
        "items"
    ][0]
    job_id = job_board["job"]["id"]
    candidates = (
        await client.get(f"/api/v1/matching/jobs/{job_id}/candidates", headers=hunter_headers)
    ).json()["items"]

    assert candidates[0]["id"] == job_board["id"]
    assert candidates[0]["score"] == job_board["score"]
    assert candidates[0]["seeker"]["persona"] == "seeker"


async def test_feed_is_a_tagged_union_of_posts_and_matched_jobs(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    items = (await client.get("/api/v1/feed", headers=seeker_headers)).json()["items"]

    assert {item["kind"] for item in items} == {"post", "matched_job"}
    matched = next(item for item in items if item["kind"] == "matched_job")
    assert matched["match"]["ats_pass"] is True


async def test_ats_template_separates_screening_from_human_stages(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    template = (await client.get("/api/v1/ats/templates", headers=hunter_headers)).json()["items"][
        0
    ]

    kinds = [stage["kind"] for stage in template["stages"]]
    assert kinds[0] == "screening"
    assert "human" in kinds
    assert template["stages"][0]["criteria"]


async def test_profile_patch_returns_updated_profile(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.patch(
        "/api/v1/profiles/me", json={"match_threshold": 0.8}, headers=seeker_headers
    )

    assert response.status_code == 200
    assert response.json()["match_threshold"] == 0.8


async def test_openapi_uses_readable_operation_ids(app: FastAPI) -> None:
    schema = app.openapi()

    op = schema["paths"]["/api/v1/matching/job-board"]["get"]
    assert op["operationId"] == "matching_list_job_board"
    assert op["responses"]["422"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/ErrorEnvelope"
    )
