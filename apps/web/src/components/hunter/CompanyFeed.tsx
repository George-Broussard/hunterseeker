"use client";

import { useState, useTransition } from "react";

import { loadMoreCompanyFeed } from "@/app/(hunter)/hunter/actions";
import type { CompanyProfileSummary, Post } from "@/lib/api/company-feed";

import { CompanyPostCard } from "./CompanyPostCard";
import { CompanyPostComposer } from "./CompanyPostComposer";

interface Props {
  initialItems: Post[];
  initialCursor: string | null;
  companies: CompanyProfileSummary[];
  /** Why the Company Profile list is missing, if it is. The feed still renders. */
  companiesError?: string;
}

/**
 * Client half of the company feed: the composer, the list (seeded from the server
 * render), and cursor-based "load more".
 */
export function CompanyFeed({ initialItems, initialCursor, companies, companiesError }: Props) {
  const [items, setItems] = useState(initialItems);
  const [cursor, setCursor] = useState(initialCursor);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  function loadMore() {
    if (!cursor || pending) return;
    setError(null);
    startTransition(async () => {
      const result = await loadMoreCompanyFeed(cursor);
      if (result.ok) {
        const seen = new Set(items.map((p) => p.id));
        setItems([...items, ...result.value.items.filter((p) => !seen.has(p.id))]);
        setCursor(result.value.nextCursor);
      } else {
        setError(result.message);
      }
    });
  }

  return (
    <div className="flex flex-col gap-4">
      {companiesError ? (
        <p role="alert" className="rounded-lg border border-red-500/40 p-4 text-sm">
          <span className="font-medium">Posting is unavailable.</span> {companiesError}
        </p>
      ) : (
        <CompanyPostComposer
          companies={companies}
          onPosted={(post) => setItems((current) => [post, ...current])}
        />
      )}

      {items.length === 0 ? (
        <p className="rounded-lg border border-dashed border-current/25 p-4 text-sm opacity-70">
          Nothing in your company feed yet. Posts from your Company Profiles and your network show
          up here.
        </p>
      ) : (
        <ul className="flex flex-col gap-4">
          {items.map((post) => (
            <CompanyPostCard key={post.id} post={post} />
          ))}
        </ul>
      )}

      {error ? (
        <p role="alert" className="text-sm text-red-600 dark:text-red-400">
          Could not load more posts. {error}
        </p>
      ) : null}

      {cursor ? (
        <button
          type="button"
          onClick={loadMore}
          disabled={pending}
          className="self-center rounded-md border border-current/25 px-4 py-1.5 text-sm font-medium hover:bg-current/5 disabled:opacity-40"
        >
          {pending ? "Loading…" : "Load more"}
        </button>
      ) : null}
    </div>
  );
}
