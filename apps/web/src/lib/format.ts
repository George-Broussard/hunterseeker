/** Display formatting shared by the Feed, Job Board and messaging surfaces. */

import type { ApiSchema } from "@hunterseeker/shared";

type JobSummary = ApiSchema<"JobSummary">;

/** "$160,000 - $200,000", one bound if only one is set, `null` if neither. */
export function formatCompensation(job: JobSummary): string | null {
  if (job.compensation_min == null && job.compensation_max == null) return null;
  const fmt = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: job.currency,
    maximumFractionDigits: 0,
  });
  const lo = job.compensation_min != null ? fmt.format(job.compensation_min) : null;
  const hi = job.compensation_max != null ? fmt.format(job.compensation_max) : null;
  if (lo && hi) return `${lo} - ${hi}`;
  if (lo) return `${lo}+`;
  return `up to ${hi}`;
}

/** "Austin, TX · remote", either half alone, or `null`. */
export function formatLocation(job: JobSummary): string | null {
  const parts = [job.location, job.remote ? "remote" : null].filter(Boolean);
  return parts.length ? parts.join(" · ") : null;
}

/** 0-1 match score as a whole percentage, e.g. 0.87 -> "87%". */
export function formatMatchScore(score: number): string {
  return `${Math.round(score * 100)}%`;
}

const RELATIVE_UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ["year", 60 * 60 * 24 * 365],
  ["month", 60 * 60 * 24 * 30],
  ["week", 60 * 60 * 24 * 7],
  ["day", 60 * 60 * 24],
  ["hour", 60 * 60],
  ["minute", 60],
];

/** "3 days ago", "just now". Callers rendering this in JSX should suppress hydration warnings. */
export function formatRelativeTime(iso: string, now: Date = new Date()): string {
  const seconds = Math.round((new Date(iso).getTime() - now.getTime()) / 1000);
  if (Math.abs(seconds) < 60) return "just now";
  const rtf = new Intl.RelativeTimeFormat("en-US", { numeric: "always" });
  for (const [unit, size] of RELATIVE_UNITS) {
    if (Math.abs(seconds) >= size) return rtf.format(Math.round(seconds / size), unit);
  }
  return "just now";
}

/** Deterministic absolute timestamp for `title`/`dateTime` attributes. */
export function formatAbsoluteTime(iso: string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "UTC",
  }).format(new Date(iso));
}

/** Up to two initials for an avatar: "C. Connection" -> "CC", "Northwind" -> "N". */
export function initials(name: string): string {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0]?.toUpperCase() ?? "")
    .join("");
}
