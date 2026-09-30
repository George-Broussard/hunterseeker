"""Application settings, loaded from the environment (and a local ``.env`` if present)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the API.

    Values come from environment variables. For local development, ``.env`` is read from
    the current directory or from the repo root (``../../.env`` when running from
    ``apps/api``). See ``.env.example`` at the repo root.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://hunterseeker:hunterseeker@localhost:5432/hunterseeker"
    """SQLAlchemy async URL. Must use the ``postgresql+asyncpg`` driver."""

    echo_sql: bool = False
    """Log every SQL statement. Development only — never enable where PII is stored."""

    embedding_dim: int = 1024
    """Width of the pgvector ``vector(dim)`` columns on the embedding tables.

    The embedding model (and therefore the final dimension) is undecided — see issue #4.
    Until it is, this is a config value with a placeholder default. Changing it after
    the embedding tables exist is a migration plus a full re-embed, not a settings tweak.
    """

    auth_secret: str
    """HMAC secret shared with ``apps/web`` (Auth.js ``AUTH_SECRET``).

    The web app signs the API bearer token with it; ``hunterseeker.auth.deps`` verifies the
    signature with the same value. Required — there is no safe default.
    """

    signup_rate_limit_per_ip: int = 10
    """Max ``POST /auth/signup`` requests per IP within ``signup_rate_limit_window_seconds``.

    Counts every attempt, successful or not — this bounds signup spam, not just abuse.
    """

    signup_rate_limit_window_seconds: float = 3600.0
    """Window for ``signup_rate_limit_per_ip``, in seconds. One hour by default."""

    verify_rate_limit_per_email: int = 5
    """Max failed ``POST /auth/verify`` attempts for one email within
    ``verify_rate_limit_window_seconds`` before that email is locked out.

    Only failures count; a successful verify never contributes to this budget.
    """

    verify_rate_limit_per_ip: int = 20
    """Max failed ``POST /auth/verify`` attempts from one IP within
    ``verify_rate_limit_window_seconds``. Same failure-only counting as the per-email limit.
    """

    verify_rate_limit_window_seconds: float = 900.0
    """Window for both ``/auth/verify`` limits, in seconds. 15 minutes by default."""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings, constructed once."""
    return Settings()
