"use client";

import { useCallback, useEffect, useRef, useState, useTransition } from "react";

import type { FeedItem, FeedPage } from "@/lib/api";

import { loadMoreFeed } from "./actions";
import { FeedItemCard } from "./feed-item";
import { PostComposer } from "./post-composer";
import { FeedEmpty, FeedError, FeedSkeleton } from "./states";

/**
 * The Feed column: composer, then an infinite-scroll list over the API's cursor pages.
 * The first page arrives from the server component; later pages load through a server
 * action when the sentinel at the bottom scrolls into view.
 */
export function Feed({ initialPage }: { initialPage: FeedPage }) {
  const [items, setItems] = useState<FeedItem[]>(initialPage.items);
  const [cursor, setCursor] = useState<string | null>(initialPage.next_cursor ?? null);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();
  const sentinelRef = useRef<HTMLDivElement>(null);

  const loadMore = useCallback(() => {
    if (!cursor || pending) return;
    setError(null);
    startTransition(async () => {
      const result = await loadMoreFeed(cursor);
      if (!result.ok) {
        setError(result.message);
        return;
      }
      setItems((current) => {
        const seen = new Set(current.map((item) => item.id));
        return [...current, ...result.data.items.filter((item) => !seen.has(item.id))];
      });
      setCursor(result.data.next_cursor ?? null);
    });
  }, [cursor, pending]);

  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel || !cursor) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) loadMore();
      },
      { rootMargin: "400px 0px" },
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [cursor, loadMore]);

  return (
    <div className="flex flex-col gap-4">
      <PostComposer onPosted={(post) => setItems((current) => [post, ...current])} />

      {items.length === 0 ? (
        <FeedEmpty />
      ) : (
        <ul className="flex flex-col gap-4">
          {items.map((item) => (
            <li key={item.id}>
              <FeedItemCard item={item} />
            </li>
          ))}
        </ul>
      )}

      {pending ? <FeedSkeleton count={1} /> : null}
      {error ? <FeedError message={error} onRetry={loadMore} /> : null}
      {cursor ? (
        <div ref={sentinelRef} aria-hidden="true" className="h-px" />
      ) : items.length > 0 ? (
        <p className="py-4 text-center text-xs opacity-60">You&apos;re all caught up.</p>
      ) : null}
    </div>
  );
}
