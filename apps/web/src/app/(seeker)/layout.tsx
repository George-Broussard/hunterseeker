import Link from "next/link";

// Layout for Seeker-facing routes. Persona-specific chrome (threshold control, profile
// menu) goes here in later issues; for now a slim nav across the Seeker surfaces.
const NAV = [
  { href: "/", label: "Feed" },
  { href: "/job-board", label: "Job Board" },
  { href: "/messages", label: "Messages" },
] as const;

export default function SeekerLayout({ children }: LayoutProps<"/">) {
  return (
    <>
      <header className="border-b border-current/10">
        <nav
          aria-label="Seeker"
          className="mx-auto flex w-full max-w-6xl items-center gap-6 px-4 py-3 text-sm sm:px-6"
        >
          <Link href="/" className="font-semibold tracking-tight">
            hunter/seeker
          </Link>
          <ul className="flex gap-4">
            {NAV.map(({ href, label }) => (
              <li key={href}>
                <Link
                  href={href}
                  className="opacity-80 hover:opacity-100 hover:underline underline-offset-4"
                >
                  {label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </header>
      {children}
    </>
  );
}
