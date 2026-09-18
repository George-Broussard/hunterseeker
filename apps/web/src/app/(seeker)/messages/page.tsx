import Link from "next/link";

import { Avatar } from "@/components/avatar";
import { UnreadBadge, counterpart } from "@/components/messaging";
import { loadConversations } from "@/lib/api";

export const dynamic = "force-dynamic";

// TODO(#7): from the session.
const STUB_VIEWER_ID = "00000000-0000-4000-8000-00000000e001";

/** Placeholder inbox: the same conversations as the rail, full width. Threads land later. */
export default async function MessagesPage() {
  const result = await loadConversations(50);

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-6 p-8">
      <h1 className="text-2xl font-semibold tracking-tight">Messages</h1>
      {result.ok ? (
        <ul className="divide-y divide-current/10 rounded-lg border border-current/15">
          {result.data.map((conversation) => {
            const other = counterpart(conversation, STUB_VIEWER_ID);
            return (
              <li key={conversation.id}>
                <Link
                  href={`/messages/${conversation.id}`}
                  className="flex items-center gap-3 px-4 py-3"
                >
                  <Avatar name={other.display_name} />
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium">{other.display_name}</span>
                    <span className="block truncate text-sm opacity-70">
                      {conversation.last_message?.body ?? "No messages yet"}
                    </span>
                  </span>
                  <UnreadBadge count={conversation.unread_count} />
                </Link>
              </li>
            );
          })}
        </ul>
      ) : (
        <p role="alert" className="rounded-lg border border-current/15 p-4 text-sm">
          Could not load your messages. {result.message}
        </p>
      )}
    </main>
  );
}
