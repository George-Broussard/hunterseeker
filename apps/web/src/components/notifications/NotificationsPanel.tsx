import type { Notification } from "./types";

// TODO(api): no notifications endpoint exists yet. This fixed list is the stub the
// issue asks for; the panel takes `items` so the API-backed version is a data swap.
const STUB_NOTIFICATIONS: Notification[] = [
  {
    id: "n-001",
    kind: "new_matches",
    text: "4 new screened Matches for Senior Backend Engineer.",
    at: "2026-09-17T08:00:00Z",
    read: false,
  },
  {
    id: "n-002",
    kind: "application_stage",
    text: "A. Seeker moved to Technical interview.",
    at: "2026-09-16T16:10:00Z",
    read: false,
  },
  {
    id: "n-003",
    kind: "connection",
    text: "C. Connection accepted your connection request.",
    at: "2026-09-15T12:30:00Z",
    read: true,
  },
];

const LABEL: Record<Notification["kind"], string> = {
  new_matches: "Matches",
  application_stage: "Pipeline",
  message: "Message",
  connection: "Connections",
};

const shortDate = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  timeZone: "UTC",
});

/** Right-rail notifications list. Server component; no interaction yet. */
export function NotificationsPanel({ items = STUB_NOTIFICATIONS }: { items?: Notification[] }) {
  const unread = items.filter((n) => !n.read).length;

  return (
    <section
      aria-labelledby="notifications-heading"
      className="flex flex-col gap-3 rounded-lg border border-current/15 p-4"
    >
      <header className="flex items-baseline justify-between">
        <h2 id="notifications-heading" className="font-medium">
          Notifications
        </h2>
        {unread > 0 ? (
          <span className="text-xs opacity-70 tabular-nums">{unread} unread</span>
        ) : null}
      </header>

      {items.length === 0 ? (
        <p className="text-sm opacity-70">You&apos;re all caught up.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {items.map((n) => (
            <li key={n.id} className={`flex gap-2 text-sm ${n.read ? "opacity-70" : ""}`}>
              <span
                aria-hidden="true"
                className={`mt-1.5 size-1.5 shrink-0 rounded-full ${n.read ? "bg-transparent" : "bg-sky-500"}`}
              />
              <div className="min-w-0 flex-1">
                <p>{n.text}</p>
                <p className="text-xs opacity-60">
                  {LABEL[n.kind]} ·{" "}
                  <time dateTime={n.at}>{shortDate.format(Date.parse(n.at))}</time>
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
