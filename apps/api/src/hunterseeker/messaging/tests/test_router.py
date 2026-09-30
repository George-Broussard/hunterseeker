"""Persona authorization on the messaging router: any persona, scoped to participants."""

from httpx import AsyncClient


async def test_conversations_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/messaging/conversations")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_conversations_allows_seeker(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/messaging/conversations", headers=seeker_headers)
    assert response.status_code == 200


async def test_conversations_allows_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/messaging/conversations", headers=hunter_headers)
    assert response.status_code == 200
