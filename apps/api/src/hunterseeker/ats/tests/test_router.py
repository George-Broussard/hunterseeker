"""Persona authorization on the ats router: hunter-only."""

from httpx import AsyncClient


async def test_templates_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/ats/templates")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_templates_rejects_seeker(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/ats/templates", headers=seeker_headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


async def test_templates_allows_hunter(client: AsyncClient, hunter_headers: dict[str, str]) -> None:
    response = await client.get("/api/v1/ats/templates", headers=hunter_headers)
    assert response.status_code == 200
