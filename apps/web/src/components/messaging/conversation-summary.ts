import type { Conversation } from "@/lib/api";

/**
 * The person on the other side of a conversation, from the viewer's point of view.
 * Falls back to the first participant when the viewer is unknown (pre-auth).
 */
export function counterpart(conversation: Conversation, viewerId?: string | null) {
  return (
    conversation.participants.find((participant) => participant.id !== viewerId) ??
    conversation.participants[0]
  );
}

export function totalUnread(conversations: Conversation[]): number {
  return conversations.reduce((sum, conversation) => sum + conversation.unread_count, 0);
}
