"use server";

/**
 * Server actions behind the Feed's interactive parts. The browser never calls the API
 * directly; these run on the server with the server-side client (and, once #7 lands,
 * the caller's token), which keeps the Next.js app a BFF over FastAPI (AGENTS.md §4).
 */

import { createPost, loadFeedPage, type ApiResult, type FeedPage, type FeedPost } from "@/lib/api";

export async function loadMoreFeed(cursor: string): Promise<ApiResult<FeedPage>> {
  return loadFeedPage(cursor);
}

export async function publishPost(body: string): Promise<ApiResult<FeedPost>> {
  const trimmed = body.trim();
  if (!trimmed) return { ok: false, message: "Write something first." };
  return createPost(trimmed);
}
