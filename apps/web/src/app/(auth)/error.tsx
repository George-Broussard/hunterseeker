"use client";

// Rendered when a /login or /signup render throws (for example the API is unreachable).
export default function AuthError({ reset }: { reset: () => void }) {
  return (
    <div role="alert" className="space-y-4 text-center">
      <p className="font-medium">Something went wrong.</p>
      <p className="text-sm opacity-70">
        We could not reach the sign-in service. Please try again.
      </p>
      <button
        type="button"
        onClick={reset}
        className="rounded-md bg-foreground px-4 py-2 text-sm font-medium text-background"
      >
        Try again
      </button>
    </div>
  );
}
