"use client";

import { useId, useState } from "react";

/**
 * On wide screens the rail is always visible; on narrow screens it collapses behind a
 * toggle so roles and candidates stay first on the page. Children are server-rendered.
 */
export function RailDisclosure({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const panelId = useId();

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-controls={panelId}
        className="flex w-full items-center justify-between rounded-lg border border-current/15 px-4 py-2 text-sm font-medium lg:hidden"
      >
        Messages &amp; notifications
        <span aria-hidden="true">{open ? "−" : "+"}</span>
      </button>
      <div id={panelId} className={`${open ? "flex" : "hidden"} flex-col gap-4 lg:flex`}>
        {children}
      </div>
    </>
  );
}
