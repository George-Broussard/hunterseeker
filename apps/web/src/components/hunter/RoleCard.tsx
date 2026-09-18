import type { OpenRole } from "@/lib/api/matching";

import { CandidateChip } from "./CandidateChip";
import { daysOpen, formatDaysOpen } from "./format";

function Count({ label, value }: { label: string; value: number }) {
  return (
    <span>
      {label} <span className="font-medium tabular-nums">{value}</span>
    </span>
  );
}

/** One open Job: Match activity, pipeline counts, and the top three ranked candidates. */
export function RoleCard({ role }: { role: OpenRole }) {
  const { job, pipeline, top_candidates: candidates } = role;
  const hasNew = role.new_match_count > 0;

  return (
    <li className="flex flex-col gap-3 rounded-lg border border-current/15 p-4">
      <div className="flex flex-wrap items-start justify-between gap-x-4 gap-y-1">
        <div className="min-w-0">
          <h3 className="font-medium">{job.title}</h3>
          <p className="text-sm opacity-70">
            {job.company_name} · {formatDaysOpen(daysOpen(job.posted_at))}
          </p>
        </div>
        <span
          className={
            hasNew
              ? "rounded-full bg-sky-500/15 px-2.5 py-0.5 text-sm font-medium text-sky-700 dark:text-sky-300"
              : "rounded-full border border-current/15 px-2.5 py-0.5 text-sm opacity-70"
          }
        >
          {role.new_match_count} new {role.new_match_count === 1 ? "match" : "matches"}
        </span>
      </div>

      <p className="flex flex-wrap gap-x-2 text-sm opacity-80" aria-label="Pipeline">
        <Count label="Screened" value={pipeline.screened} />
        <span aria-hidden="true">·</span>
        <Count label="Interviewing" value={pipeline.interviewing} />
        <span aria-hidden="true">·</span>
        <Count label="Offer" value={pipeline.offer} />
      </p>

      {candidates.length > 0 ? (
        <ul className="flex flex-wrap gap-2" aria-label="Top candidates">
          {candidates.map((candidate) => (
            <CandidateChip key={candidate.id} candidate={candidate} />
          ))}
        </ul>
      ) : (
        <p className="text-sm opacity-70">
          No Matches yet. Candidates appear as Profiles pass screening.
        </p>
      )}
    </li>
  );
}
