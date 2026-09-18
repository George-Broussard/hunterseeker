/**
 * Bounded slot for the shared message center. The real rail is built under
 * `components/messaging/` by the Seeker home issue (#9); once it lands, replace this
 * component with that import in `HunterRightRail` and delete this file.
 */
export function MessageRailSlot() {
  return (
    <section
      aria-labelledby="messages-heading"
      className="flex flex-col gap-2 rounded-lg border border-dashed border-current/25 p-4"
    >
      <h2 id="messages-heading" className="font-medium">
        Messages
      </h2>
      <p className="text-sm opacity-70">
        The message center is shared with the Seeker home and lands with #9.
      </p>
    </section>
  );
}
