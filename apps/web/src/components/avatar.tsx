import { initials } from "@/lib/format";

/**
 * Initials-only avatar. Deliberately no photo support: images are a proxy for protected
 * characteristics (AGENTS.md §9) and have no place next to hiring surfaces.
 */
export function Avatar({ name, size = "md" }: { name: string; size?: "sm" | "md" }) {
  const dimensions = size === "sm" ? "size-8 text-xs" : "size-10 text-sm";
  return (
    <span
      aria-hidden="true"
      className={`inline-flex shrink-0 select-none items-center justify-center rounded-full bg-current/10 font-medium ${dimensions}`}
    >
      {initials(name)}
    </span>
  );
}
