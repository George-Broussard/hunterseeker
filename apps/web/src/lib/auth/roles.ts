import { PERSONAS, type Persona } from "@hunterseeker/shared";

export function isPersona(value: unknown): value is Persona {
  return typeof value === "string" && (PERSONAS as readonly string[]).includes(value);
}

/**
 * Where a signed-in user lands. Hunters go to `/hunter`; Seekers go to their home.
 *
 * TODO(#9): the Seeker home moves to `/`. Change the seeker branch to "/" and drop the
 * `/seeker` placeholder when that lands.
 */
export function homeFor(role: Persona): string {
  return role === "hunter" ? "/hunter" : "/seeker";
}

/** Route prefixes that belong to one persona. Used by the proxy to keep personas apart. */
export const PERSONA_ROUTE_PREFIXES: ReadonlyArray<{ prefix: string; role: Persona }> = [
  { prefix: "/hunter", role: "hunter" },
  { prefix: "/seeker", role: "seeker" }, // TODO(#9): becomes "/" (the Seeker home)
];

/** Paths reachable without a session. Everything else requires one (AGENTS.md §8: default deny). */
export const PUBLIC_PATHS: ReadonlySet<string> = new Set(["/login", "/signup"]);
