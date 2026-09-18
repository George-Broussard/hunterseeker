"use client";

import Link from "next/link";
import { useState } from "react";

import type { Conversation } from "@/lib/api";

import { ConversationListItem } from "./conversation-list-item";
import { totalUnread } from "./conversation-summary";
import { UnreadBadge } from "./unread-badge";

export interface MessageRailProps {
  /** Most recent conversations first. The caller decides how many. */
  conversations: Conversation[];
  /** The signed-in user's id, so the rail can show the other participant. Optional pre-auth. */
  viewerId?: string | null;
  /** Set when the conversations could not be loaded; the rail renders an error instead. */
  error?: string | null;
  /** Route prefix for a conversation; `${hrefPrefix}/${conversation.id}`. */
  hrefPrefix?: string;
  /** Heading text. */
  title?: string;
}

/**
 * Message center rail. Persona-agnostic (AGENTS.md §7): the Seeker home and the Hunter
 * home both render it with their own conversation lists.
 *
 * At `lg` and up it is a sticky right-hand column. Below that it collapses to a top bar
 * with an unread badge; tapping the bar expands the list in place.
 */
export function MessageRail({
  conversations,
  viewerId = null,
  error = null,
  hrefPrefix = "/messages",
  title = "Messages",
}: MessageRailProps) {
  const [open, setOpen] = useState(false);
  const unread = totalUnread(conversations);
  const panelId = "message-rail-panel";

  return (
    <aside
      aria-label={title}
      className="rounded-lg border border-current/15 lg:sticky lg:top-4 lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto"
    >
      <div className="flex items-center justify-between gap-2 px-3 py-2 lg:border-b lg:border-current/15">
        <h2 className="flex items-center gap-2 text-sm font-semibold">
          <Link href={hrefPrefix} className="hover:underline underline-offset-4">
            {title}
          </Link>
          <UnreadBadge count={unread} />
        </h2>
        <button
          type="button"
          aria-expanded={open}
          aria-controls={panelId}
          onClick={() => setOpen((value) => !value)}
          className="rounded-md border border-current/15 px-2 py-1 text-xs lg:hidden"
        >
          {open ? "Hide" : "Show"}
        </button>
      </div>

      <div id={panelId} className={`${open ? "block" : "hidden"} lg:block`}>
        {error ? (
          <p role="alert" className="px-3 py-3 text-xs">
            Could not load messages. {error}
          </p>
        ) : conversations.length === 0 ? (
          <p className="px-3 py-3 text-xs opacity-70">
            No conversations yet. Messages from your connections and matches will show up here.
          </p>
        ) : (
          <ul className="divide-y divide-current/10">
            {conversations.map((conversation) => (
              <ConversationListItem
                key={conversation.id}
                conversation={conversation}
                viewerId={viewerId}
                href={`${hrefPrefix}/${conversation.id}`}
              />
            ))}
          </ul>
        )}
      </div>
    </aside>
  );
}

/** Placeholder with the rail's footprint, for route `loading.tsx` files. */
export function MessageRailSkeleton({ rows = 3 }: { rows?: number }) {
  return (
    <aside
      aria-busy="true"
      aria-label="Loading messages"
      className="animate-pulse rounded-lg border border-current/15"
    >
      <div className="px-3 py-2 lg:border-b lg:border-current/15">
        <div className="h-4 w-20 rounded bg-current/10" />
      </div>
      <ul className="hidden lg:block">
        {Array.from({ length: rows }, (_, i) => (
          <li key={i} className="flex gap-3 px-3 py-2">
            <div className="size-8 rounded-full bg-current/10" />
            <div className="flex-1 space-y-2 py-1">
              <div className="h-3 w-1/2 rounded bg-current/10" />
              <div className="h-2 w-3/4 rounded bg-current/10" />
            </div>
          </li>
        ))}
      </ul>
    </aside>
  );
}
