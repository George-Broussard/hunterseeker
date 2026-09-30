import Link from "next/link";

/** Placeholder target for the "Create a role" CTA. The real form is its own issue. */
export default function CreateRolePlaceholderPage() {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-4 p-8">
      <h1 className="text-2xl font-semibold tracking-tight">Create a role</h1>
      <p className="text-sm opacity-70">
        Placeholder. Posting a Job — title, Company Profile, and the ATS template whose screening
        stage gates every Match — is built in a later issue.
      </p>
      <Link href="/hunter" className="text-sm underline underline-offset-4">
        Back to home
      </Link>
    </main>
  );
}
