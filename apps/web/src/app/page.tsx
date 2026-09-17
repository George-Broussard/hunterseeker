import Link from "next/link";

import { PERSONAS } from "@hunterseeker/shared";

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-6 p-8">
      <h1 className="text-3xl font-semibold tracking-tight">hunter/seeker</h1>
      <p className="max-w-md text-center text-sm opacity-70">
        Placeholder. The Seeker and Hunter surfaces live in their own route groups.
      </p>
      <nav className="flex gap-4 text-sm underline underline-offset-4">
        {PERSONAS.map((persona) => (
          <Link key={persona} href={`/${persona}`}>
            {persona}
          </Link>
        ))}
      </nav>
    </main>
  );
}
