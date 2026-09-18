"use client";

import { useState, useTransition } from "react";

import { submitCompanyPost } from "@/app/(hunter)/hunter/actions";
import {
  POST_BODY_MAX_LENGTH,
  type CompanyProfileSummary,
  type Post,
} from "@/lib/api/company-feed";

interface Props {
  companies: CompanyProfileSummary[];
  onPosted: (post: Post) => void;
}

/**
 * Post to the company feed *as* a Company Profile. The selector only appears when the
 * Hunter manages more than one; with exactly one, that one is used silently.
 */
export function CompanyPostComposer({ companies, onPosted }: Props) {
  const [companyId, setCompanyId] = useState(companies[0]?.id ?? "");
  const [body, setBody] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  if (companies.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-current/25 p-4 text-sm opacity-70">
        You don&apos;t manage a Company Profile yet, so there is nothing to post as.
      </p>
    );
  }

  const canSubmit = body.trim().length > 0 && body.length <= POST_BODY_MAX_LENGTH && !pending;

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;
    setError(null);
    startTransition(async () => {
      const result = await submitCompanyPost({ companyProfileId: companyId, body });
      if (result.ok) {
        setBody("");
        onPosted(result.value);
      } else {
        setError(result.message);
      }
    });
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-3 rounded-lg border border-current/15 p-4"
      aria-label="Post as a Company Profile"
    >
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <label htmlFor="company-post-as" className="opacity-70">
          Post as
        </label>
        {companies.length > 1 ? (
          <select
            id="company-post-as"
            value={companyId}
            onChange={(e) => setCompanyId(e.target.value)}
            className="rounded-md border border-current/25 bg-transparent px-2 py-1"
          >
            {companies.map((company) => (
              <option key={company.id} value={company.id}>
                {company.name}
              </option>
            ))}
          </select>
        ) : (
          <span id="company-post-as" className="font-medium">
            {companies[0].name}
          </span>
        )}
      </div>

      <textarea
        value={body}
        onChange={(e) => setBody(e.target.value)}
        rows={3}
        maxLength={POST_BODY_MAX_LENGTH}
        placeholder="Share an update from your company…"
        aria-label="Post body"
        className="w-full resize-y rounded-md border border-current/25 bg-transparent px-3 py-2 text-sm"
      />

      <div className="flex items-center justify-between gap-4">
        <span className="text-xs opacity-60 tabular-nums">
          {body.length}/{POST_BODY_MAX_LENGTH}
        </span>
        <button
          type="submit"
          disabled={!canSubmit}
          className="rounded-md bg-foreground px-4 py-1.5 text-sm font-medium text-background disabled:opacity-40"
        >
          {pending ? "Posting…" : "Post"}
        </button>
      </div>
      {error ? (
        <p role="alert" className="text-sm text-red-600 dark:text-red-400">
          {error}
        </p>
      ) : null}
    </form>
  );
}
