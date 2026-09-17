/**
 * @hunterseeker/shared
 *
 * Generated API types and shared constants/enums. `src/api.d.ts` and `openapi.json` are
 * generated — never hand-edit them. Regenerate with:
 *
 *   (cd apps/api && uv run python scripts/export_openapi.py)
 *   pnpm --filter @hunterseeker/shared generate
 */

import type { components, operations, paths } from "./api";

export type { components, operations, paths };

/** A named schema from the API contract, e.g. `ApiSchema<"MatchedJob">`. */
export type ApiSchema<Name extends keyof components["schemas"]> = components["schemas"][Name];

/** Body of every non-2xx API response. */
export type ApiErrorEnvelope = ApiSchema<"ErrorEnvelope">;

/** The two user roles in hunter/seeker. See AGENTS.md §3. */
export const PERSONAS = ["seeker", "hunter"] as const;

export type Persona = (typeof PERSONAS)[number];

/** Placeholder export so the package resolves from the workspace. */
export const SHARED_PACKAGE_NAME = "@hunterseeker/shared";
