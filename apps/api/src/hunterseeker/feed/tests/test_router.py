"""Persona authorization on the feed router: seeker-only."""

from httpx import AsyncClient


async def test_feed_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/feed")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_feed_rejects_hunter(client: AsyncClient, hunter_headers: dict[str, str]) -> None:
    response = await client.get("/api/v1/feed", headers=hunter_headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


async def test_feed_allows_seeker(client: AsyncClient, seeker_headers: dict[str, str]) -> None:
    response = await client.get("/api/v1/feed", headers=seeker_headers)
    assert response.status_code == 200
