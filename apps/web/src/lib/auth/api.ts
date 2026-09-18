/**
 * Server-side calls to the FastAPI auth endpoints (`apps/api/src/hunterseeker/auth`),
 * through the typed client from #5 so the request/response shapes are checked against
 * the generated contract.
 *
 * The web app never touches Postgres (AGENTS.md §4); account creation and password checks
 * happen in the API. Only ever call these from server code — they carry credentials.
 */
import "server-only";

import type { ApiSchema } from "@hunterseeker/shared";

import { api } from "@/lib/api";

export type ApiUser = ApiSchema<"UserOut">;

export class SignupError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "SignupError";
  }
}

/** Resolves to the user on success, `null` on 401. Throws on anything else (API down, 5xx). */
export async function verifyCredentials(email: string, password: string): Promise<ApiUser | null> {
  const { data, response } = await api.POST("/api/v1/auth/verify", {
    body: { email, password },
    cache: "no-store",
  });
  if (response.status === 401) return null;
  if (!data) throw new Error(`auth/verify failed: HTTP ${response.status}`);
  return data;
}

/** Creates the account. Throws `SignupError(409)` if the email is taken, `SignupError(422)` on validation. */
export async function signupUser(input: ApiSchema<"SignupRequest">): Promise<ApiUser> {
  const { data, response } = await api.POST("/api/v1/auth/signup", {
    body: input,
    cache: "no-store",
  });
  if (response.status === 409) {
    throw new SignupError(409, "An account with this email already exists.");
  }
  if (response.status === 422) {
    throw new SignupError(422, "Please check the details you entered.");
  }
  if (!data) throw new Error(`auth/signup failed: HTTP ${response.status}`);
  return data;
}
