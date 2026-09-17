# hunter/seeker

An agentic job board that inverts job search: a Seeker builds a Profile and the system
matches them to jobs they have _already_ passed the ATS screen for. Hunters get a ranked
candidate list per role instead of an inbox of applications.

**Read [`AGENTS.md`](./AGENTS.md) before writing code.** It holds the domain vocabulary,
the tech stack, the matching-engine rules, and the agent workflow (issue → branch →
worktree → PR).

## Run it

```sh
nvm use            # Node version from .nvmrc
corepack enable    # pnpm version from package.json#packageManager
pnpm install
pnpm dev           # Next.js at http://localhost:3000
```

Checks: `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`.

The API (`apps/api`) runs separately — see [`apps/api/README.md`](./apps/api/README.md).
When its contract changes, regenerate the shared types:
`(cd apps/api && uv run python scripts/export_openapi.py) && pnpm --filter @hunterseeker/shared generate`.

## Layout

```
apps/web/          Next.js (App Router) — Seeker and Hunter surfaces
apps/api/          FastAPI — business logic, owns the database
packages/shared/   @hunterseeker/shared — generated API types, shared enums
```
