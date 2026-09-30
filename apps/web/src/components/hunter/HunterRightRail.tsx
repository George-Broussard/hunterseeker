import { NotificationsPanel } from "@/components/notifications";

import { MessageRailSlot } from "./MessageRailSlot";
import { RailDisclosure } from "./RailDisclosure";

/** Right rail: notifications above the shared message center. Collapses on narrow screens. */
export function HunterRightRail() {
  return (
    <aside
      aria-label="Messages and notifications"
      className="flex flex-col gap-3 lg:sticky lg:top-8 lg:w-80 lg:shrink-0"
    >
      <RailDisclosure>
        <NotificationsPanel />
        <MessageRailSlot />
      </RailDisclosure>
    </aside>
  );
}
