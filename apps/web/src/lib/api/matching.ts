/**
 * Matching endpoints as seen from the web app. Hunter-side calls live here alongside
 * the Seeker-side ones because they are two views of the same Match (AGENTS.md §6).
 */

import type { ApiSchema } from "@hunterseeker/shared";

import { api, describeApiError } from "./client";
import type { ApiResult } from "./result";

export type OpenRole = ApiSchema<"OpenRole">;
export type MatchedCandidate = ApiSchema<"MatchedCandidate">;
export type RolePipelineCounts = ApiSchema<"RolePipelineCounts">;

/**
 * The calling Hunter's open roles, each with Match activity and the top-3 candidates.
 * Every candidate is a Match, so every one of them has already passed the Job's ATS
 * screening — the Hunter never sees an unscreened Seeker here.
 */
export async function listOpenRoles(limit = 20): Promise<ApiResult<OpenRole[]>> {
  // TODO(auth): the client will send the Hunter's token once login lands (#7).
  try {
    const { data, error, response } = await api.GET("/api/v1/matching/open-roles", {
      params: { query: { limit } },
    });
    if (!data) {
      return { ok: false, message: describeApiError(error, response.status) };
    }
    return { ok: true, value: data.items };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}
