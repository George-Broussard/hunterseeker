"""Persona authorization on the imports router: hunter-only."""

from httpx import AsyncClient


async def test_runs_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/imports/runs")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_runs_rejects_seeker(client: AsyncClient, seeker_headers: dict[str, str]) -> None:
    response = await client.get("/api/v1/imports/runs", headers=seeker_headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


async def test_runs_allows_hunter(client: AsyncClient, hunter_headers: dict[str, str]) -> None:
    response = await client.get("/api/v1/imports/runs", headers=hunter_headers)
    assert response.status_code == 200
