/**
 * Messaging calls. One system for both personas (AGENTS.md §7): nothing here knows
 * whether the caller is a Seeker or a Hunter.
 */

import type { ApiSchema } from "@hunterseeker/shared";

import { api, describeApiError } from "./client";
import type { ApiResult } from "./result";

export type Conversation = ApiSchema<"Conversation">;
export type Message = ApiSchema<"Message">;

export const RAIL_CONVERSATION_LIMIT = 8;

/** The caller's most recent conversations, for the message rail. */
export async function loadConversations(
  limit: number = RAIL_CONVERSATION_LIMIT,
): Promise<ApiResult<Conversation[]>> {
  // TODO(auth): the client will send the caller's token once login lands (#7).
  try {
    const { data, error, response } = await api.GET("/api/v1/messaging/conversations", {
      params: { query: { limit } },
    });
    if (!data) return { ok: false, message: describeApiError(error, response.status) };
    return { ok: true, data: data.items };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}

/** Send a message in an existing conversation (the rail's quick reply). */
export async function sendMessage(
  conversationId: string,
  body: string,
): Promise<ApiResult<Message>> {
  try {
    const { data, error, response } = await api.POST(
      "/api/v1/messaging/conversations/{conversation_id}/messages",
      { params: { path: { conversation_id: conversationId } }, body: { body } },
    );
    if (!data) return { ok: false, message: describeApiError(error, response.status) };
    return { ok: true, data };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}
