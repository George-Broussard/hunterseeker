"""Persona authorization on the network router: any persona, scoped to the caller."""

from httpx import AsyncClient


async def test_connections_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/network/connections")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_connections_allows_seeker(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/network/connections", headers=seeker_headers)
    assert response.status_code == 200


async def test_connections_allows_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/network/connections", headers=hunter_headers)
    assert response.status_code == 200
