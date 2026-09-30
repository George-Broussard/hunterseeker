"""Rate limiting on /auth/signup and /auth/verify.

Each test drives its threshold down to a small number via env vars so it stays fast and
deterministic, rather than hammering the production default. `client`/`app` are
function-scoped (see the root conftest), so each test gets its own `InMemoryRateLimiter`
via `app.state` — no cross-test leakage to guard against.

`_set_limit` clears the `get_settings` cache *after* setting the env var: the `client`
fixture's `db_session` dependency already calls `get_settings()` once during its own
setup (to read `DATABASE_URL`), which populates the cache with defaults before this
test's body — and its `monkeypatch.setenv` calls — ever run. Clearing only wouldn't be
enough without also setting the env var first; the ordering here matters.
"""

import pytest
from httpx import AsyncClient

from hunterseeker.core.settings import get_settings


def _set_limit(monkeypatch: pytest.MonkeyPatch, **env: str) -> None:
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    get_settings.cache_clear()


def _signup_payload(email: str) -> dict[str, str]:
    return {"email": email, "password": "password123", "name": "Ada", "role": "seeker"}


async def test_signup_allows_up_to_the_limit(
    client: AsyncClient, unique_email: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    _set_limit(monkeypatch, SIGNUP_RATE_LIMIT_PER_IP="2")

    first = await client.post("/api/v1/auth/signup", json=_signup_payload(f"a-{unique_email}"))
    second = await client.post("/api/v1/auth/signup", json=_signup_payload(f"b-{unique_email}"))

    assert first.status_code == 201
    assert second.status_code == 201


async def test_signup_429s_per_ip_over_the_limit(
    client: AsyncClient, unique_email: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    _set_limit(monkeypatch, SIGNUP_RATE_LIMIT_PER_IP="2")

    await client.post("/api/v1/auth/signup", json=_signup_payload(f"a-{unique_email}"))
    await client.post("/api/v1/auth/signup", json=_signup_payload(f"b-{unique_email}"))
    third = await client.post("/api/v1/auth/signup", json=_signup_payload(f"c-{unique_email}"))

    assert third.status_code == 429
    assert third.json()["error"]["code"] == "too_many_requests"


async def test_signup_limit_is_per_ip_not_global_across_emails(
    client: AsyncClient, unique_email: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Every request in a test shares one httpx client, i.e. one "IP" — a failed create
    # (409, duplicate email) still counts against the IP budget same as a 201 would.
    _set_limit(monkeypatch, SIGNUP_RATE_LIMIT_PER_IP="1")

    payload = _signup_payload(unique_email)
    first = await client.post("/api/v1/auth/signup", json=payload)
    second = await client.post("/api/v1/auth/signup", json=payload)

    assert first.status_code == 201
    assert second.status_code == 429


async def test_verify_allows_up_to_the_per_email_limit(
    client: AsyncClient, unique_email: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    _set_limit(monkeypatch, VERIFY_RATE_LIMIT_PER_EMAIL="2", VERIFY_RATE_LIMIT_PER_IP="1000")
    await client.post("/api/v1/auth/signup", json=_signup_payload(unique_email))

    bad = {"email": unique_email, "password": "wrong"}
    first = await client.post("/api/v1/auth/verify", json=bad)
    second = await client.post("/api/v1/auth/verify", json=bad)

    assert first.status_code == 401
    assert second.status_code == 401


async def test_verify_429s_after_per_email_failures_exceed_the_limit(
    client: AsyncClient, unique_email: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    _set_limit(monkeypatch, VERIFY_RATE_LIMIT_PER_EMAIL="2", VERIFY_RATE_LIMIT_PER_IP="1000")
    await client.post("/api/v1/auth/signup", json=_signup_payload(unique_email))

    bad = {"email": unique_email, "password": "wrong"}
    await client.post("/api/v1/auth/verify", json=bad)
    await client.post("/api/v1/auth/verify", json=bad)
    third = await client.post("/api/v1/auth/verify", json=bad)

    assert third.status_code == 429
    assert third.json()["error"]["code"] == "too_many_requests"


async def test_verify_429s_after_per_ip_failures_exceed_the_limit_across_emails(
    client: AsyncClient, unique_email: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Two different unknown emails, same client (same IP) — the per-IP budget catches
    # what a per-email budget alone would miss: one attacker spraying many emails.
    _set_limit(monkeypatch, VERIFY_RATE_LIMIT_PER_EMAIL="1000", VERIFY_RATE_LIMIT_PER_IP="2")

    bad_a = {"email": f"a-{unique_email}", "password": "wrong"}
    bad_b = {"email": f"b-{unique_email}", "password": "wrong"}
    await client.post("/api/v1/auth/verify", json=bad_a)
    await client.post("/api/v1/auth/verify", json=bad_b)
    third = await client.post("/api/v1/auth/verify", json=bad_a)

    assert third.status_code == 429


async def test_verify_success_does_not_count_against_the_limit(
    client: AsyncClient, unique_email: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    _set_limit(monkeypatch, VERIFY_RATE_LIMIT_PER_EMAIL="1", VERIFY_RATE_LIMIT_PER_IP="1000")
    await client.post("/api/v1/auth/signup", json=_signup_payload(unique_email))

    good = {"email": unique_email, "password": "password123"}
    first = await client.post("/api/v1/auth/verify", json=good)
    second = await client.post("/api/v1/auth/verify", json=good)

    assert first.status_code == 200
    assert second.status_code == 200
