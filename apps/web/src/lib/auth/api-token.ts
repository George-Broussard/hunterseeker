/**
 * The bearer token the web app presents to FastAPI.
 *
 * Auth.js's own session cookie is encrypted (JWE) and meant only for this app. For the API
 * we mint a plain HS256 JWT signed with the same `AUTH_SECRET`; `hunterseeker.auth.deps`
 * on the API side verifies it. Keep the claim names in sync with
 * `apps/api/src/hunterseeker/auth/tokens.py`.
 */
import { SignJWT } from "jose";

import type { Persona } from "@hunterseeker/shared";

export const API_TOKEN_ISSUER = "hunterseeker-web";
export const API_TOKEN_AUDIENCE = "hunterseeker-api";
const API_TOKEN_TTL = "1h";

export interface ApiTokenClaims {
  userId: string;
  role: Persona;
  email: string;
}

export function getAuthSecret(): string {
  const secret = process.env.AUTH_SECRET;
  if (!secret) throw new Error("AUTH_SECRET is not set (see .env.example)");
  return secret;
}

export async function signApiToken(claims: ApiTokenClaims): Promise<string> {
  return new SignJWT({ user_id: claims.userId, role: claims.role, email: claims.email })
    .setProtectedHeader({ alg: "HS256", typ: "JWT" })
    .setSubject(claims.userId)
    .setIssuer(API_TOKEN_ISSUER)
    .setAudience(API_TOKEN_AUDIENCE)
    .setIssuedAt()
    .setExpirationTime(API_TOKEN_TTL)
    .sign(new TextEncoder().encode(getAuthSecret()));
}
