import Link from "next/link";

/** Placeholder target for the "Import from Ashby / Greenhouse" CTA. The real flow is its own issue. */
export default function ImportRolesPlaceholderPage() {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-4 p-8">
      <h1 className="text-2xl font-semibold tracking-tight">Import from Ashby / Greenhouse</h1>
      <p className="text-sm opacity-70">
        Placeholder. Importing open postings from an external recruiting platform is built in a
        later issue.
      </p>
      <Link href="/hunter" className="text-sm underline underline-offset-4">
        Back to home
      </Link>
    </main>
  );
}
