# hunter/seeker API

FastAPI service that owns business logic, matching, and the database
(see `AGENTS.md` §4). Async throughout: SQLAlchemy async engine, `asyncpg`, Alembic
running against the async engine.

## Layout

```
apps/api/
  alembic/                 # migrations (env.py is async)
  src/hunterseeker/
    main.py                # ASGI entrypoint: `app = create_app()`
    core/                  # settings, db engine/session, app factory, /health
    matching/ profiles/ applications/ ats/ messaging/ imports/ feed/ network/
                           # domain packages (empty until their issues land)
```

Code is organised **by domain**, not by technical layer (AGENTS.md §5). Tests live next
to the code they test (`<domain>/tests/`).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — installs the pinned Python (`.python-version`) and deps.
- Docker (for the local Postgres + pgvector database).

## Run

All commands below are run from `apps/api/`.

```bash
# 1. Start Postgres 16 + pgvector (repo root docker-compose.yml; named volume persists data)
cp ../../.env.example ../../.env      # once; edit if you change ports/credentials
docker compose -f ../../docker-compose.yml up -d db

# 2. Install deps into .venv
uv sync

# 3. Apply migrations (the initial one enables the `vector` extension)
uv run alembic upgrade head

# 4. Serve with reload
uv run fastapi dev src/hunterseeker/main.py
curl localhost:8000/health   # -> {"status":"ok"}
```

Production-style serve: `uv run uvicorn hunterseeker.main:app --host 0.0.0.0 --port 8000`.

## Test / lint / typecheck

```bash
uv run pytest
uv run ruff check
uv run ruff format --check     # or `uv run ruff format` to fix
uv run mypy
```

CI (`.github/workflows/ci-api.yml`) runs exactly these plus `alembic upgrade head`
against a throwaway pgvector container.

## Migrations

```bash
uv run alembic revision --autogenerate -m "describe the change"   # needs the db up
uv run alembic upgrade head
uv run alembic downgrade -1
uv run alembic history
```

Rules (AGENTS.md §8, §10):

- Every schema change goes through a migration. No manual DDL.
- One migration per PR, regenerated after your final rebase on `main`.
- Autogenerate only sees models whose modules are imported in `alembic/env.py`. When a
  domain package gains models, import it there.

## Configuration

`pydantic-settings` reads environment variables, falling back to `.env` in the current
directory or at the repo root. See `../../.env.example`.

| Variable       | Default                                                              |
|----------------|----------------------------------------------------------------------|
| `DATABASE_URL` | `postgresql+asyncpg://hunterseeker:hunterseeker@localhost:5432/hunterseeker` |
| `ECHO_SQL`     | `false`                                                              |
