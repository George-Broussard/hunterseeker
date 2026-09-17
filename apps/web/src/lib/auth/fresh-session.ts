import "server-only";

import { cookies } from "next/headers";
import { getToken } from "next-auth/jwt";

import type { Persona } from "@hunterseeker/shared";

import { getAuthSecret } from "./api-token";
import { isPersona } from "./roles";

/**
 * Read the session cookie that *this* server action just set.
 *
 * `auth()` parses the incoming request's `Cookie` header, so right after
 * `signIn(..., { redirect: false })` it still sees the old (absent) session. The mutable
 * `cookies()` store does reflect the new cookie, so we decode from there.
 */
export async function readFreshSessionRole(): Promise<Persona | null> {
  const jar = await cookies();
  const cookieHeader = jar
    .getAll()
    .map((c) => `${c.name}=${c.value}`)
    .join("; ");
  const req = new Request("http://internal", { headers: { cookie: cookieHeader } });
  const secret = getAuthSecret();
  // Auth.js prefixes the cookie name with __Secure- on https origins; try both.
  for (const secureCookie of [false, true]) {
    const token = await getToken({ req, secret, secureCookie });
    if (isPersona(token?.role)) return token.role;
  }
  return null;
}
