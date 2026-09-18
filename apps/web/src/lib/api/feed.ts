/**
 * Feed calls. The Feed is the only surface where posts and Matches mix, and the
 * interleaving is done by the API (AGENTS.md §3): the web app renders one cursor-paginated
 * list and never merges two.
 */

import type { ApiSchema } from "@hunterseeker/shared";

import { api, describeApiError } from "./client";
import type { ApiResult } from "./result";

export type FeedItem = ApiSchema<"FeedItem">;
export type FeedPost = ApiSchema<"Post">;
export type FeedMatchedJob = ApiSchema<"MatchedJobItem">;
export type FeedPage = ApiSchema<"Page_FeedItem_">;

export const FEED_PAGE_SIZE = 20;

/** One page of the calling Seeker's Feed. Pass `cursor` from the previous page's `next_cursor`. */
export async function loadFeedPage(
  cursor: string | null = null,
  limit: number = FEED_PAGE_SIZE,
): Promise<ApiResult<FeedPage>> {
  // TODO(auth): the client will send the Seeker's token once login lands (#7).
  try {
    const { data, error, response } = await api.GET("/api/v1/feed", {
      params: { query: { limit, ...(cursor ? { cursor } : {}) } },
    });
    if (!data) return { ok: false, message: describeApiError(error, response.status) };
    return { ok: true, data };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}

/** Publish a text post. The API stubs this until the Feed backend lands. */
export async function createPost(body: string): Promise<ApiResult<FeedPost>> {
  try {
    const { data, error, response } = await api.POST("/api/v1/feed/posts", { body: { body } });
    if (!data) return { ok: false, message: describeApiError(error, response.status) };
    return { ok: true, data };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}
