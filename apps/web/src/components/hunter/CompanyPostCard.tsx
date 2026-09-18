import type { Post } from "@/lib/api/company-feed";

import { formatShortDate } from "./format";

/** A post in the company feed: by a Company Profile the Hunter manages, or from their network. */
export function CompanyPostCard({ post }: { post: Post }) {
  const byline = post.company
    ? `${post.company.name} · posted by ${post.author.display_name}`
    : `${post.author.display_name} · ${post.author.persona}`;

  return (
    <li className="flex flex-col gap-2 rounded-lg border border-current/15 p-4">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 text-sm">
        <span className={post.company ? "font-medium" : "opacity-80"}>{byline}</span>
        <time dateTime={post.created_at} className="opacity-60">
          {formatShortDate(post.created_at)}
        </time>
      </div>
      <p className="text-sm whitespace-pre-wrap">{post.body}</p>
    </li>
  );
}
