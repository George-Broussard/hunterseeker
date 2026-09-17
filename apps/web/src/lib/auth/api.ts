/**
 * Server-side calls to the FastAPI auth endpoints (`apps/api/src/hunterseeker/auth`).
 *
 * The web app never touches Postgres (AGENTS.md §4); account creation and password checks
 * happen in the API. Only ever call these from server code — they carry credentials.
 *
 * TODO(#5): move onto the generated typed client in `src/lib/api` once it lands.
 */
import "server-only";

import type { Persona } from "@hunterseeker/shared";

export interface ApiUser {
  id: string;
  email: string;
  name: string;
  role: Persona;
}

export class SignupError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "SignupError";
  }
}

function apiUrl(path: string): string {
  const base = process.env.API_URL ?? "http://localhost:8000";
  return `${base.replace(/\/$/, "")}${path}`;
}

async function postJson(path: string, body: unknown): Promise<Response> {
  return fetch(apiUrl(path), {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });
}

/** Resolves to the user on success, `null` on 401. Throws on anything else (API down, 5xx). */
export async function verifyCredentials(email: string, password: string): Promise<ApiUser | null> {
  const response = await postJson("/api/v1/auth/verify", { email, password });
  if (response.status === 401) return null;
  if (!response.ok) throw new Error(`auth/verify failed: HTTP ${response.status}`);
  return (await response.json()) as ApiUser;
}

/** Creates the account. Throws `SignupError(409)` if the email is taken, `SignupError(422)` on validation. */
export async function signupUser(input: {
  email: string;
  password: string;
  name: string;
  role: Persona;
}): Promise<ApiUser> {
  const response = await postJson("/api/v1/auth/signup", input);
  if (response.status === 409) {
    throw new SignupError(409, "An account with this email already exists.");
  }
  if (response.status === 422) {
    throw new SignupError(422, "Please check the details you entered.");
  }
  if (!response.ok) throw new Error(`auth/signup failed: HTTP ${response.status}`);
  return (await response.json()) as ApiUser;
}
