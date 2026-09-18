"use client";

/** Route-level error boundary. Section loaders never throw, so this catches the unexpected. */
export default function HunterHomeError({ reset }: { reset: () => void }) {
  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-start gap-4 p-8">
      <h1 className="text-xl font-semibold tracking-tight">Something went wrong</h1>
      <p role="alert" className="text-sm opacity-70">
        Your home could not be rendered. Try again; if it keeps happening, the API may be down.
      </p>
      <button
        type="button"
        onClick={reset}
        className="rounded-md border border-current/25 px-4 py-1.5 text-sm font-medium hover:bg-current/5"
      >
        Try again
      </button>
    </main>
  );
}
