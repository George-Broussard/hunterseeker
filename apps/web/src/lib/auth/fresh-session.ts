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
  const secure = (process.env.AUTH_URL ?? "").startsWith("https://");
  const token = await getToken({
    req: new Request("http://internal", { headers: { cookie: cookieHeader } }),
    secret: getAuthSecret(),
    secureCookie: secure,
  });
  return isPersona(token?.role) ? token.role : null;
}
