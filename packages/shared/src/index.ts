/**
 * @hunterseeker/shared
 *
 * Generated API types and shared constants/enums. Generated files under `src/generated/`
 * (once they exist) must never be hand-edited — run `pnpm --filter @hunterseeker/shared generate`.
 */

/** The two user roles in hunter/seeker. See AGENTS.md §3. */
export const PERSONAS = ["seeker", "hunter"] as const;

export type Persona = (typeof PERSONAS)[number];

/** Placeholder export so the package resolves from the workspace. */
export const SHARED_PACKAGE_NAME = "@hunterseeker/shared";
