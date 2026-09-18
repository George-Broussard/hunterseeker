/**
 * The Hunter's company feed: posts from the Company Profiles they manage plus their
 * network, and posting *as* a Company Profile.
 */

import type { ApiSchema } from "@hunterseeker/shared";

import { api, describeApiError } from "./client";
import type { ApiResult } from "./result";

export type Post = ApiSchema<"Post">;
export type CompanyProfileSummary = ApiSchema<"CompanyProfileSummary">;
export type CompanyPostCreate = ApiSchema<"CompanyPostCreate">;

/** Mirrors `CompanyPostCreate.body` max_length in the API contract. */
export const POST_BODY_MAX_LENGTH = 5000;

export interface CompanyFeedPage {
  items: Post[];
  /** Opaque; pass back as `cursor` to fetch the next page. `null` on the last page. */
  nextCursor: string | null;
}

export async function listCompanyFeed(
  cursor: string | null = null,
  limit = 20,
): Promise<ApiResult<CompanyFeedPage>> {
  // TODO(auth): the client will send the Hunter's token once login lands (#7).
  try {
    const { data, error, response } = await api.GET("/api/v1/feed/company", {
      params: { query: { limit, ...(cursor ? { cursor } : {}) } },
    });
    if (!data) {
      return { ok: false, message: describeApiError(error, response.status) };
    }
    return { ok: true, value: { items: data.items, nextCursor: data.next_cursor ?? null } };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}

/** Company Profiles the calling Hunter manages — the composer's "post as" choices. */
export async function listCompanyProfiles(): Promise<ApiResult<CompanyProfileSummary[]>> {
  try {
    const { data, error, response } = await api.GET("/api/v1/feed/company-profiles", {
      params: { query: { limit: 100 } },
    });
    if (!data) {
      return { ok: false, message: describeApiError(error, response.status) };
    }
    return { ok: true, value: data.items };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}

export async function createCompanyPost(body: CompanyPostCreate): Promise<ApiResult<Post>> {
  try {
    const { data, error, response } = await api.POST("/api/v1/feed/company/posts", { body });
    if (!data) {
      return { ok: false, message: describeApiError(error, response.status) };
    }
    return { ok: true, value: data };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}
