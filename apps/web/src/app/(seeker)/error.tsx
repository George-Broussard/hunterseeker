"use client";

/** Route-level error boundary for Seeker pages. Data-fetch failures render inline; this catches the rest. */
export default function SeekerError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-start gap-3 p-8">
      <h1 className="text-lg font-semibold">Something went wrong</h1>
      <p role="alert" className="text-sm opacity-70">
        {error.message || "An unexpected error occurred."}
      </p>
      <button
        type="button"
        onClick={reset}
        className="rounded-md border border-current/15 px-3 py-1.5 text-sm"
      >
        Try again
      </button>
    </main>
  );
}
