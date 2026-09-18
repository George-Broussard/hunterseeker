import Link from "next/link";
import { notFound } from "next/navigation";

import { api, describeApiError } from "@/lib/api";
import { formatCompensation, formatLocation, formatMatchScore } from "@/lib/format";

export const dynamic = "force-dynamic";

/**
 * Placeholder Match detail page: where "View" on a matched-job card lands. The full job
 * page (description, ATS stages, apply) is a later issue.
 */
export default async function MatchPage({ params }: PageProps<"/matches/[id]">) {
  const { id } = await params;
  const { data, error, response } = await api.GET("/api/v1/matching/matches/{match_id}", {
    params: { path: { match_id: id } },
  });
  if (response.status === 404) notFound();
  if (!data) throw new Error(describeApiError(error, response.status));

  const { job } = data;
  const compensation = formatCompensation(job);
  const location = formatLocation(job);

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-4 p-8">
      <Link href="/" className="text-sm opacity-70 hover:opacity-100">
        &larr; Back to your feed
      </Link>
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">{job.title}</h1>
        <p className="opacity-70">
          {job.company_name}
          {location ? ` · ${location}` : ""}
        </p>
      </header>
      <p className="inline-flex w-fit items-center gap-1.5 rounded-full border border-emerald-600/40 bg-emerald-500/10 px-2.5 py-1 text-xs font-medium text-emerald-700 dark:text-emerald-300">
        <span aria-hidden="true">✓</span>
        Passed screening — your Profile already clears this job&apos;s ATS
      </p>
      <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-1 text-sm">
        <dt className="opacity-70">Match score</dt>
        <dd className="tabular-nums">{formatMatchScore(data.score)}</dd>
        {compensation ? (
          <>
            <dt className="opacity-70">Compensation</dt>
            <dd>{compensation}</dd>
          </>
        ) : null}
        {job.seniority ? (
          <>
            <dt className="opacity-70">Seniority</dt>
            <dd className="capitalize">{job.seniority}</dd>
          </>
        ) : null}
      </dl>
      <p className="text-sm opacity-70">
        The full job page and application flow land in a later issue.
      </p>
    </main>
  );
}
