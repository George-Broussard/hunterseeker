import { formatAbsoluteTime, formatRelativeTime } from "@/lib/format";

/** Relative time with the absolute value on hover. Client re-renders may differ by a tick. */
export function Timestamp({ iso, className }: { iso: string; className?: string }) {
  return (
    <time
      dateTime={iso}
      title={formatAbsoluteTime(iso)}
      className={className}
      suppressHydrationWarning
    >
      {formatRelativeTime(iso)}
    </time>
  );
}
