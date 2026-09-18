# hunter/seeker API

FastAPI service that owns business logic, matching, and the database
(see `AGENTS.md` §4). Async throughout: SQLAlchemy async engine, `asyncpg`, Alembic
running against the async engine.

## Layout

```
apps/api/
  alembic/                 # migrations (env.py is async)
  scripts/export_openapi.py  # writes packages/shared/openapi.json
  src/hunterseeker/
    main.py                # ASGI entrypoint: `app = create_app()`
    core/                  # settings, db engine/session, app factory, /health,
                           # error envelope (errors.py), cursor pagination (pagination.py)
    auth/                  # users table, /api/v1/auth/{signup,verify,me}, get_current_user
    matching/ profiles/ applications/ ats/ messaging/ imports/ feed/ network/
      router.py            # endpoints, mounted at /api/v1/<domain>
      schemas.py           # Pydantic models — the API contract for the domain
```

Code is organised **by domain**, not by technical layer (AGENTS.md §5). Tests live next
to the code they test (`<domain>/tests/`). Every domain currently ships stub endpoints
that return fixed data in the real response shape; each carries a `# TODO(auth): ...`
marker naming the persona and ownership rule it will enforce.

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

## API conventions

### Routers

Each domain exposes one `APIRouter` in `<domain>/router.py` with `prefix="/<domain>"` and
`tags=["<domain>"]`; `core/app.py` mounts them all under `/api/v1`. Operation ids are
`<tag>_<function name>` (e.g. `matching_list_job_board`) and become the names in the
generated TypeScript. Every endpoint declares its response model via the return
annotation — Pydantic models are the contract.

### Error envelope

Every non-2xx response has the same body:

```json
{ "error": { "code": "not_found", "message": "Match not found.", "details": { "match_id": "…" } } }
```

| Field     | Meaning                                                                           |
|-----------|-----------------------------------------------------------------------------------|
| `code`    | Stable snake_case identifier for clients to branch on (`not_found`, `validation_error`, `forbidden`, …). |
| `message` | Human-readable. May change; never parse it.                                       |
| `details` | Free-form JSON context, or `null`. Validation errors put Pydantic's error list here. |

Raise `hunterseeker.core.errors.ApiError(status_code, code, message, details)` (or a
subclass such as `NotFoundError`) from domain code. `install_error_handlers` also
normalises FastAPI's `HTTPException`, request validation errors (`422`,
`validation_error`) and unhandled exceptions (`500`, `internal_server_error`, no
internals leaked) into the envelope. The OpenAPI document declares `ErrorEnvelope` for
`422`, `4XX` and `5XX` on every operation.

### Pagination

List endpoints are **cursor-paginated**. Request `?cursor=<opaque>&limit=<1..100>`
(default 20) and receive:

```json
{ "items": [ … ], "next_cursor": "…" }
```

`next_cursor` is `null` on the last page; pass it back as `cursor` otherwise. Cursors are
opaque — never construct or decode them client-side. Use `CursorQuery` as
`params: Annotated[CursorQuery, Query()]` and return `Page[Item]` from
`hunterseeker.core.pagination`. Cursor rather than offset pagination because the Feed and
Job Board are append-heavy, continuously re-ranked lists where offsets skip or repeat
items between requests.

### API contract → TypeScript

`packages/shared/openapi.json` and `packages/shared/src/api.d.ts` are generated from
this service and committed. Whenever a router or schema changes:

```bash
uv run python scripts/export_openapi.py            # from apps/api
pnpm --filter @hunterseeker/shared generate        # from the repo root
```

`.github/workflows/ci-shared.yml` reruns both and fails if the committed files differ.
`uv run python scripts/export_openapi.py --check` does the first half locally. The web
app consumes the types through the `openapi-fetch` client in `apps/web/src/lib/api`.

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
| `AUTH_SECRET`  | *(required)* — shared with `apps/web`; verifies the bearer token     |

## Authentication

Sessions live in `apps/web` (Auth.js, decided in #3). The web app calls
`POST /api/v1/auth/signup` and `POST /api/v1/auth/verify` server-side, then sends a
short-lived HS256 JWT (`sub`, `role`, `email`; signed with `AUTH_SECRET`) as
`Authorization: Bearer …` on every API request. Endpoints get the caller via
`hunterseeker.auth.deps.get_current_user` / `require_role("hunter")` — no database
round-trip, the token is the authority. Ownership checks still belong in each endpoint.
