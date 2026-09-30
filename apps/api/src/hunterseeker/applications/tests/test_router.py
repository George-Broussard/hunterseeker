"""Persona authorization on the applications router: seeker-only."""

from httpx import AsyncClient


async def test_applications_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/applications")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_applications_rejects_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/applications", headers=hunter_headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


async def test_applications_allows_seeker(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/applications", headers=seeker_headers)
    assert response.status_code == 200
