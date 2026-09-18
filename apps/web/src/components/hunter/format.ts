const DAY_MS = 24 * 60 * 60 * 1000;

/** Whole days since `postedAt`, never negative. */
export function daysOpen(postedAt: string, now: number = Date.now()): number {
  const posted = Date.parse(postedAt);
  if (Number.isNaN(posted)) return 0;
  return Math.max(0, Math.floor((now - posted) / DAY_MS));
}

export function formatDaysOpen(days: number): string {
  if (days === 0) return "Opened today";
  return `Open ${days} ${days === 1 ? "day" : "days"}`;
}

export function formatScore(score: number): string {
  return `${Math.round(score * 100)}%`;
}

// Fixed zone so server render and client hydration agree on the text.
const shortDate = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  timeZone: "UTC",
});

export function formatShortDate(iso: string): string {
  const t = Date.parse(iso);
  return Number.isNaN(t) ? "" : shortDate.format(t);
}
