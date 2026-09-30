"""Persona authorization on the matching router."""

from httpx import AsyncClient

_JOB_ID = "00000000-0000-4000-8000-00000000a001"
_MATCH_ID = "00000000-0000-4000-8000-00000000f001"


async def test_job_board_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/matching/job-board")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_job_board_rejects_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/matching/job-board", headers=hunter_headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


async def test_job_board_allows_seeker(client: AsyncClient, seeker_headers: dict[str, str]) -> None:
    response = await client.get("/api/v1/matching/job-board", headers=seeker_headers)
    assert response.status_code == 200


async def test_get_match_requires_authentication(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/matching/matches/{_MATCH_ID}")
    assert response.status_code == 401


async def test_get_match_rejects_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.get(f"/api/v1/matching/matches/{_MATCH_ID}", headers=hunter_headers)
    assert response.status_code == 403


async def test_get_match_allows_seeker(client: AsyncClient, seeker_headers: dict[str, str]) -> None:
    response = await client.get(f"/api/v1/matching/matches/{_MATCH_ID}", headers=seeker_headers)
    assert response.status_code == 200


async def test_candidates_requires_authentication(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/matching/jobs/{_JOB_ID}/candidates")
    assert response.status_code == 401


async def test_candidates_rejects_seeker(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"/api/v1/matching/jobs/{_JOB_ID}/candidates", headers=seeker_headers
    )
    assert response.status_code == 403


async def test_candidates_allows_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"/api/v1/matching/jobs/{_JOB_ID}/candidates", headers=hunter_headers
    )
    assert response.status_code == 200
