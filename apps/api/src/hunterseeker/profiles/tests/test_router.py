"""Persona authorization on the profiles router: seeker-only."""

from httpx import AsyncClient


async def test_get_my_profile_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/profiles/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_get_my_profile_rejects_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/profiles/me", headers=hunter_headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


async def test_get_my_profile_allows_seeker(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.get("/api/v1/profiles/me", headers=seeker_headers)
    assert response.status_code == 200


async def test_update_my_profile_requires_authentication(client: AsyncClient) -> None:
    response = await client.patch("/api/v1/profiles/me", json={"match_threshold": 0.8})
    assert response.status_code == 401


async def test_update_my_profile_rejects_hunter(
    client: AsyncClient, hunter_headers: dict[str, str]
) -> None:
    response = await client.patch(
        "/api/v1/profiles/me", json={"match_threshold": 0.8}, headers=hunter_headers
    )
    assert response.status_code == 403


async def test_update_my_profile_allows_seeker(
    client: AsyncClient, seeker_headers: dict[str, str]
) -> None:
    response = await client.patch(
        "/api/v1/profiles/me", json={"match_threshold": 0.8}, headers=seeker_headers
    )
    assert response.status_code == 200
