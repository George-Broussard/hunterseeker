"use client";

import Link from "next/link";
import { useState } from "react";

import { Avatar } from "@/components/avatar";
import type { Conversation } from "@/lib/api";
import { formatAbsoluteTime, formatRelativeTime } from "@/lib/format";

import { counterpart } from "./conversation-summary";
import { QuickReply } from "./quick-reply";
import { UnreadBadge } from "./unread-badge";

export function ConversationListItem({
  conversation,
  viewerId,
  href,
}: {
  conversation: Conversation;
  viewerId?: string | null;
  href: string;
}) {
  const other = counterpart(conversation, viewerId);
  const last = conversation.last_message;
  const fromViewer = last != null && viewerId != null && last.sender.id === viewerId;
  const [replying, setReplying] = useState(false);
  const unread = conversation.unread_count > 0;

  return (
    <li className="px-3 py-2">
      <Link href={href} className="flex items-start gap-3 rounded-md">
        <Avatar name={other.display_name} size="sm" />
        <span className="min-w-0 flex-1">
          <span className="flex items-baseline justify-between gap-2">
            <span className={`truncate text-sm ${unread ? "font-semibold" : "font-medium"}`}>
              {other.display_name}
            </span>
            <time
              dateTime={conversation.updated_at}
              title={formatAbsoluteTime(conversation.updated_at)}
              suppressHydrationWarning
              className="shrink-0 text-[11px] opacity-60"
            >
              {formatRelativeTime(conversation.updated_at)}
            </time>
          </span>
          <span className="flex items-center justify-between gap-2">
            <span className={`truncate text-xs ${unread ? "" : "opacity-70"}`}>
              {last ? `${fromViewer ? "You: " : ""}${last.body}` : "No messages yet"}
            </span>
            <UnreadBadge count={conversation.unread_count} />
          </span>
        </span>
      </Link>
      <div className="pl-11">
        {replying ? (
          <QuickReply conversationId={conversation.id} onSent={() => setReplying(false)} />
        ) : (
          <button
            type="button"
            onClick={() => setReplying(true)}
            className="mt-1 text-[11px] underline underline-offset-4 opacity-70 hover:opacity-100"
          >
            Reply
          </button>
        )}
      </div>
    </li>
  );
}
