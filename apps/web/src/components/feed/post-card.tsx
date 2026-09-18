import { Avatar } from "@/components/avatar";
import type { FeedPost } from "@/lib/api";

import { Timestamp } from "./timestamp";

const PERSONA_LABEL = { seeker: "Seeker", hunter: "Hunter" } as const;

/** A post from someone in the Seeker's network. */
export function PostCard({ post }: { post: FeedPost }) {
  return (
    <article className="rounded-lg border border-current/15 p-4">
      <header className="flex items-center gap-3">
        <Avatar name={post.author.display_name} />
        <div className="min-w-0 flex-1">
          <p className="truncate font-medium">{post.author.display_name}</p>
          <p className="text-xs opacity-70">
            Connection · {PERSONA_LABEL[post.author.persona]} · <Timestamp iso={post.created_at} />
          </p>
        </div>
      </header>
      <p className="mt-3 whitespace-pre-wrap text-sm leading-relaxed">{post.body}</p>
      <footer className="mt-3 flex gap-2 text-xs">
        {/* Reactions and comments are placeholders until the Feed backend exists. */}
        <button
          type="button"
          disabled
          title="Reactions are coming soon"
          className="rounded-md border border-current/15 px-2 py-1 opacity-60"
        >
          React
        </button>
        <button
          type="button"
          disabled
          title="Comments are coming soon"
          className="rounded-md border border-current/15 px-2 py-1 opacity-60"
        >
          Comment
        </button>
      </footer>
    </article>
  );
}
