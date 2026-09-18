"use client";

import { useState, useTransition } from "react";

import type { FeedPost } from "@/lib/api";

import { publishPost } from "./actions";

const MAX_LENGTH = 5000;

/** Text-only composer at the top of the Feed. Posting hits the API stub. */
export function PostComposer({ onPosted }: { onPosted: (post: FeedPost) => void }) {
  const [body, setBody] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();
  const canPost = body.trim().length > 0 && !pending;

  function submit() {
    setError(null);
    startTransition(async () => {
      const result = await publishPost(body);
      if (!result.ok) {
        setError(result.message);
        return;
      }
      setBody("");
      onPosted(result.data);
    });
  }

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        if (canPost) submit();
      }}
      className="rounded-lg border border-current/15 p-4"
    >
      <label htmlFor="post-composer" className="sr-only">
        Share an update with your connections
      </label>
      <textarea
        id="post-composer"
        name="body"
        value={body}
        maxLength={MAX_LENGTH}
        rows={3}
        placeholder="Share an update with your connections"
        disabled={pending}
        onChange={(event) => setBody(event.target.value)}
        onKeyDown={(event) => {
          if ((event.metaKey || event.ctrlKey) && event.key === "Enter" && canPost) submit();
        }}
        className="w-full resize-y rounded-md border border-current/15 bg-transparent p-2 text-sm outline-none focus:border-current/40"
      />
      <div className="mt-2 flex items-center justify-between gap-4 text-xs">
        <span className="opacity-70" aria-live="polite">
          {error ? <span role="alert">{error}</span> : `${body.length}/${MAX_LENGTH}`}
        </span>
        <button
          type="submit"
          disabled={!canPost}
          className="rounded-md bg-foreground px-3 py-1.5 text-sm font-medium text-background disabled:opacity-40"
        >
          {pending ? "Posting…" : "Post"}
        </button>
      </div>
    </form>
  );
}
