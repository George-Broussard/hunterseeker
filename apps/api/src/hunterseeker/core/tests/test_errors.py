"""Every error response uses the {"error": {code, message, details}} envelope."""

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from hunterseeker.core.errors import ApiError, code_for_status


def _assert_envelope(body: dict[str, object], code: str) -> dict[str, object]:
    assert set(body) == {"error"}
    error = body["error"]
    assert isinstance(error, dict)
    assert set(error) == {"code", "message", "details"}
    assert error["code"] == code
    assert isinstance(error["message"], str) and error["message"]
    return error


async def test_api_error_from_domain_code(client: AsyncClient) -> None:
    response = await client.get("/api/v1/matching/matches/00000000-0000-4000-8000-0000000000ff")

    assert response.status_code == 404
    error = _assert_envelope(response.json(), "not_found")
    assert error["details"] == {"match_id": "00000000-0000-4000-8000-0000000000ff"}


async def test_unknown_route_uses_envelope(client: AsyncClient) -> None:
    response = await client.get("/api/v1/nope")

    assert response.status_code == 404
    _assert_envelope(response.json(), "not_found")


async def test_method_not_allowed_uses_envelope(client: AsyncClient) -> None:
    response = await client.delete("/api/v1/feed")

    assert response.status_code == 405
    _assert_envelope(response.json(), "method_not_allowed")


async def test_validation_error_uses_envelope_with_details(client: AsyncClient) -> None:
    response = await client.get("/api/v1/feed", params={"limit": 0})

    assert response.status_code == 422
    error = _assert_envelope(response.json(), "validation_error")
    details = error["details"]
    assert isinstance(details, list) and details[0]["loc"] == ["query", "limit"]


async def test_unhandled_exception_uses_envelope_without_leaking(app: FastAPI) -> None:
    @app.get("/boom")
    async def boom() -> None:
        raise RuntimeError("secret internal state")

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/boom")

    assert response.status_code == 500
    error = _assert_envelope(response.json(), "internal_server_error")
    assert "secret" not in str(error)


async def test_custom_api_error_status_and_code(app: FastAPI) -> None:
    @app.get("/teapot")
    async def teapot() -> None:
        raise ApiError(409, "already_applied", "You already applied to this Job.")

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/teapot")

    assert response.status_code == 409
    _assert_envelope(response.json(), "already_applied")


def test_code_for_status() -> None:
    assert code_for_status(404) == "not_found"
    assert code_for_status(405) == "method_not_allowed"
    assert code_for_status(500) == "internal_server_error"
    assert code_for_status(599) == "http_599"
