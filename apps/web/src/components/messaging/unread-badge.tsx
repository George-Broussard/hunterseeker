/** Count pill for unread messages. Renders nothing at zero. */
export function UnreadBadge({ count, label = "unread" }: { count: number; label?: string }) {
  if (count <= 0) return null;
  return (
    <span
      aria-label={`${count} ${label}`}
      className="inline-flex min-w-5 items-center justify-center rounded-full bg-foreground px-1.5 py-0.5 text-[11px] font-semibold leading-none text-background tabular-nums"
    >
      {count > 99 ? "99+" : count}
    </span>
  );
}
