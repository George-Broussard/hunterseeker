"use server";

/** Server action behind the rail's quick reply. Persona-agnostic; runs with the caller's session. */

import { sendMessage, type ApiResult, type Message } from "@/lib/api";

export async function quickReply(
  conversationId: string,
  body: string,
): Promise<ApiResult<Message>> {
  const trimmed = body.trim();
  if (!trimmed) return { ok: false, message: "Write something first." };
  return sendMessage(conversationId, trimmed);
}
