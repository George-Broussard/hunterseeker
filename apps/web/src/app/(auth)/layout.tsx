import type { ReactNode } from "react";

// Layout for the unauthenticated surfaces: /login and /signup. Centered card with the
// product wordmark; the proxy sends signed-in users away from these routes.
export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <main className="flex flex-1 flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm">
        <header className="mb-8 text-center">
          <p className="text-2xl font-semibold tracking-tight">hunter/seeker</p>
          <p className="mt-1 text-sm opacity-60">Jobs you have already passed the screen for.</p>
        </header>
        <section className="rounded-xl border border-foreground/10 bg-background p-6 shadow-sm">
          {children}
        </section>
      </div>
    </main>
  );
}
