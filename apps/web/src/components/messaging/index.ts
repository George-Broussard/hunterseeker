/**
 * Shared, persona-agnostic message center. Both the Seeker home (`/`) and the Hunter
 * home (`/hunter`) render `MessageRail`; feed it conversations from
 * `loadConversations()` in `@/lib/api`.
 */
export { ConversationListItem } from "./conversation-list-item";
export { counterpart, totalUnread } from "./conversation-summary";
export { MessageRail, MessageRailSkeleton, type MessageRailProps } from "./message-rail";
export { QuickReply } from "./quick-reply";
export { UnreadBadge } from "./unread-badge";
