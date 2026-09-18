import { Suspense } from "react";

import {
  CompanyFeedSection,
  CompanyFeedSkeleton,
  HunterRightRail,
  OpenRolesSection,
  OpenRolesSkeleton,
} from "@/components/hunter";

// Per-Hunter and continuously re-ranked: never prerender.
export const dynamic = "force-dynamic";

/**
 * The Hunter's home. Roles and screened candidates lead; the company feed follows;
 * notifications and messages sit in a rail that collapses on narrow screens. Each
 * section streams in behind its own skeleton and fails on its own.
 */
export default function HunterHomePage() {
  return (
    <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-8 p-6 lg:flex-row lg:items-start lg:p-8">
      <div className="flex min-w-0 flex-1 flex-col gap-10">
        <Suspense fallback={<OpenRolesSkeleton />}>
          <OpenRolesSection />
        </Suspense>
        <Suspense fallback={<CompanyFeedSkeleton />}>
          <CompanyFeedSection />
        </Suspense>
      </div>
      <HunterRightRail />
    </main>
  );
}
