"use client";

import Link from "next/link";
import { useState } from "react";

import type { FeedMatchedJob } from "@/lib/api";
import { formatCompensation, formatLocation, formatMatchScore } from "@/lib/format";

import { Timestamp } from "./timestamp";

/**
 * A Match surfaced in the Feed. Every Match has already passed the Job's ATS screening —
 * that is the product promise (AGENTS.md §2) — so the card says so in plain text.
 */
export function MatchedJobCard({ item }: { item: FeedMatchedJob }) {
  const { match } = item;
  const { job } = match;
  // TODO(matching): Save / Not interested persist once Match feedback endpoints exist.
  const [saved, setSaved] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  const compensation = formatCompensation(job);
  const location = formatLocation(job);

  if (dismissed) {
    return (
      <div className="flex items-center justify-between gap-4 rounded-lg border border-dashed border-current/15 p-4 text-sm opacity-70">
        <span>Hidden: {job.title}</span>
        <button
          type="button"
          onClick={() => setDismissed(false)}
          className="underline underline-offset-4"
        >
          Undo
        </button>
      </div>
    );
  }

  return (
    <article className="rounded-lg border border-current/15 p-4" data-match-id={match.id}>
      <header className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-wide opacity-70">
            Matched job · <Timestamp iso={item.created_at} />
          </p>
          <h2 className="mt-1 font-medium">{job.title}</h2>
          <p className="text-sm opacity-70">
            {job.company_name}
            {location ? ` · ${location}` : ""}
          </p>
        </div>
        <p className="shrink-0 text-right">
          <span className="block text-lg font-semibold tabular-nums">
            {formatMatchScore(match.score)}
          </span>
          <span className="block text-xs opacity-70">match</span>
        </p>
      </header>

      <p className="mt-3 inline-flex items-center gap-1.5 rounded-full border border-emerald-600/40 bg-emerald-500/10 px-2.5 py-1 text-xs font-medium text-emerald-700 dark:text-emerald-300">
        <span aria-hidden="true">✓</span>
        Passed screening — your Profile already clears this job&apos;s ATS
      </p>

      <dl className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-sm">
        {compensation ? (
          <div>
            <dt className="sr-only">Compensation</dt>
            <dd>{compensation}</dd>
          </div>
        ) : null}
        {job.seniority ? (
          <div>
            <dt className="sr-only">Seniority</dt>
            <dd className="capitalize">{job.seniority}</dd>
          </div>
        ) : null}
      </dl>

      <footer className="mt-4 flex flex-wrap gap-2 text-sm">
        <Link
          href={`/matches/${match.id}`}
          className="rounded-md bg-foreground px-3 py-1.5 font-medium text-background"
        >
          View
        </Link>
        <button
          type="button"
          aria-pressed={saved}
          onClick={() => setSaved((value) => !value)}
          className="rounded-md border border-current/15 px-3 py-1.5 aria-pressed:bg-current/10"
        >
          {saved ? "Saved" : "Save"}
        </button>
        <button
          type="button"
          onClick={() => setDismissed(true)}
          className="rounded-md px-3 py-1.5 opacity-70 hover:opacity-100"
        >
          Not interested
        </button>
      </footer>
    </article>
  );
}
