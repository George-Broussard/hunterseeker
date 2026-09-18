/**
 * The typed API client, authenticated as the signed-in user.
 *
 * Server components, route handlers and server actions use this instead of the bare `api`
 * from `@/lib/api`: every request carries `Authorization: Bearer <session.apiToken>`,
 * which FastAPI's `get_current_user` validates (persona role included).
 *
 *   const { data } = await authenticatedApi.GET("/api/v1/auth/me");
 */
import "server-only";

import { createApiClient } from "@/lib/api";

import { auth } from "./index";

export const authenticatedApi = createApiClient({
  getAuthToken: async () => (await auth())?.apiToken ?? null,
});
