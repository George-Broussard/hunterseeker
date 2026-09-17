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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings, constructed once."""
    return Settings()
