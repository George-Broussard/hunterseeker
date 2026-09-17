import type { ApiSchema } from "@hunterseeker/shared";

import { api, describeApiError } from "@/lib/api";

// The Job Board is per-Seeker and re-ranked continuously: never prerender it.
export const dynamic = "force-dynamic";

type MatchedJob = ApiSchema<"MatchedJob">;

async function loadJobBoard(): Promise<
  { ok: true; matches: MatchedJob[] } | { ok: false; message: string }
> {
  // TODO(auth): the client will send the Seeker's token once login lands (#7).
  try {
    const { data, error, response } = await api.GET("/api/v1/matching/job-board", {
      params: { query: { limit: 20 } },
    });
    if (!data) {
      return { ok: false, message: describeApiError(error, response.status) };
    }
    return { ok: true, matches: data.items };
  } catch {
    return { ok: false, message: describeApiError(undefined) };
  }
}

function formatCompensation(job: MatchedJob["job"]): string | null {
  if (job.compensation_min == null && job.compensation_max == null) return null;
  const fmt = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: job.currency,
    maximumFractionDigits: 0,
  });
  const lo = job.compensation_min != null ? fmt.format(job.compensation_min) : null;
  const hi = job.compensation_max != null ? fmt.format(job.compensation_max) : null;
  return lo && hi ? `${lo} - ${hi}` : (lo ?? hi);
}

export default async function SeekerJobBoardPage() {
  const result = await loadJobBoard();

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-6 p-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">Job Board</h1>
        <p className="text-sm opacity-70">
          Every job here has already passed its ATS screen for your Profile.
        </p>
      </header>

      {result.ok ? (
        <ul className="flex flex-col gap-4">
          {result.matches.map((match) => {
            const compensation = formatCompensation(match.job);
            return (
              <li key={match.id} className="rounded-lg border border-current/15 p-4">
                <div className="flex items-baseline justify-between gap-4">
                  <h2 className="font-medium">{match.job.title}</h2>
                  <span className="text-sm tabular-nums" title="Match score">
                    {Math.round(match.score * 100)}% match
                  </span>
                </div>
                <p className="text-sm opacity-70">
                  {match.job.company_name}
                  {match.job.location ? ` · ${match.job.location}` : ""}
                  {match.job.remote ? " · remote" : ""}
                </p>
                {compensation ? <p className="text-sm">{compensation}</p> : null}
              </li>
            );
          })}
        </ul>
      ) : (
        <p role="alert" className="rounded-lg border border-current/15 p-4 text-sm">
          Could not load your Job Board. {result.message}
        </p>
      )}
    </main>
  );
}
