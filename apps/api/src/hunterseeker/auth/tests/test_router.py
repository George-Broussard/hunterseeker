"""Signup / verify / me against a real Postgres (skipped if none is reachable)."""

from httpx import AsyncClient

from hunterseeker.auth.tokens import CurrentUser, encode_api_token

from .conftest import TEST_SECRET


async def test_signup_creates_user_with_role(client: AsyncClient, unique_email: str) -> None:
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": unique_email, "password": "password123", "name": "Ada", "role": "seeker"},
    )

    assert response.status_code == 201, response.text
    body = response.json()
    assert body["email"] == unique_email
    assert body["name"] == "Ada"
    assert body["role"] == "seeker"
    assert "password" not in body and "password_hash" not in body


async def test_signup_duplicate_email_is_409(client: AsyncClient, unique_email: str) -> None:
    payload = {"email": unique_email, "password": "password123", "name": "Ada", "role": "hunter"}
    assert (await client.post("/api/v1/auth/signup", json=payload)).status_code == 201

    response = await client.post(
        "/api/v1/auth/signup", json={**payload, "email": unique_email.upper()}
    )

    assert response.status_code == 409


async def test_signup_validation(client: AsyncClient, unique_email: str) -> None:
    base = {"email": unique_email, "password": "password123", "name": "Ada", "role": "seeker"}
    for bad in (
        {"password": "short"},
        {"role": "admin"},
        {"email": "not-an-email"},
        {"name": "   "},
    ):
        response = await client.post("/api/v1/auth/signup", json={**base, **bad})
        assert response.status_code == 422, bad


async def test_verify_success_and_failure(client: AsyncClient, unique_email: str) -> None:
    payload = {"email": unique_email, "password": "password123", "name": "Ada", "role": "hunter"}
    created = (await client.post("/api/v1/auth/signup", json=payload)).json()

    ok = await client.post(
        "/api/v1/auth/verify", json={"email": unique_email.upper(), "password": "password123"}
    )
    assert ok.status_code == 200
    assert ok.json() == created

    bad_password = await client.post(
        "/api/v1/auth/verify", json={"email": unique_email, "password": "password124"}
    )
    unknown_user = await client.post(
        "/api/v1/auth/verify", json={"email": f"nobody-{unique_email}", "password": "password123"}
    )
    assert bad_password.status_code == 401
    assert unknown_user.status_code == 401
    assert bad_password.json() == unknown_user.json()


async def test_me_requires_and_echoes_token(client: AsyncClient, unique_email: str) -> None:
    created = (
        await client.post(
            "/api/v1/auth/signup",
            json={"email": unique_email, "password": "password123", "name": "A", "role": "seeker"},
        )
    ).json()
    user = CurrentUser(id=created["id"], role="seeker", email=unique_email)

    assert (await client.get("/api/v1/auth/me")).status_code == 401
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {encode_api_token(user, TEST_SECRET)}"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "role": "seeker", "email": unique_email}
