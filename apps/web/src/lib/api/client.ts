/**
 * Typed fetch client for the hunter/seeker API.
 *
 * A thin `openapi-fetch` wrapper over the generated `paths` from `@hunterseeker/shared`, so
 * every call is checked against the FastAPI contract: paths, params, request bodies and
 * response shapes (AGENTS.md §4). Business logic stays in `apps/api`; this file only
 * knows how to reach it.
 *
 *   const { data, error } = await api.GET("/api/v1/matching/job-board", {
 *     params: { query: { limit: 20 } },
 *   });
 *   // data: Page_MatchedJob_ | undefined, error: ErrorEnvelope | undefined
 */

import createClient, { type Middleware } from "openapi-fetch";

import type { ApiErrorEnvelope, paths } from "@hunterseeker/shared";

/**
 * Where the API lives. Server-side code (server components, route handlers) reads
 * `API_URL` so it can use an internal address; the browser bundle only ever sees
 * `NEXT_PUBLIC_API_URL`, which Next.js inlines at build time.
 */
export const API_BASE_URL =
  process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/**
 * Returns the bearer token to send, or `null` to send the request unauthenticated.
 * The login work (Auth.js session -> JWT for FastAPI) plugs in here; until then the
 * default client sends no `Authorization` header.
 */
export type AuthTokenProvider = () => string | null | Promise<string | null>;

export interface ApiClientOptions {
  baseUrl?: string;
  getAuthToken?: AuthTokenProvider;
  /** Override `fetch` (tests, custom caching). Defaults to the global `fetch`. */
  fetch?: typeof globalThis.fetch;
}

export type ApiClient = ReturnType<typeof createClient<paths>>;

/** Middleware that attaches `Authorization: Bearer <token>` when a provider yields one. */
export function authMiddleware(getAuthToken: AuthTokenProvider): Middleware {
  return {
    async onRequest({ request }) {
      const token = await getAuthToken();
      if (token) {
        request.headers.set("Authorization", `Bearer ${token}`);
      }
      return request;
    },
  };
}

/** Build a client. Prefer the shared `api` instance unless you need different options. */
export function createApiClient(options: ApiClientOptions = {}): ApiClient {
  const client = createClient<paths>({
    baseUrl: options.baseUrl ?? API_BASE_URL,
    fetch: options.fetch,
  });
  if (options.getAuthToken) {
    client.use(authMiddleware(options.getAuthToken));
  }
  return client;
}

/** The default client. Unauthenticated until the auth token provider is wired in. */
export const api: ApiClient = createApiClient();

/** Human-readable text for an API error envelope (or a transport failure). */
export function describeApiError(error: ApiErrorEnvelope | undefined, status?: number): string {
  if (error?.error) {
    return `${error.error.code}: ${error.error.message}`;
  }
  return status ? `HTTP ${status}` : "The API could not be reached.";
}
