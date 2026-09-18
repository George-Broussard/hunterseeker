import { CompanyFeedSkeleton, OpenRolesSkeleton, RailSkeleton } from "@/components/hunter";

/** Route-level fallback while the server render is in flight. Mirrors the page layout. */
export default function HunterHomeLoading() {
  return (
    <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-8 p-6 lg:flex-row lg:items-start lg:p-8">
      <div className="flex min-w-0 flex-1 flex-col gap-10">
        <OpenRolesSkeleton />
        <CompanyFeedSkeleton />
      </div>
      <aside className="hidden lg:block lg:w-80 lg:shrink-0">
        <RailSkeleton />
      </aside>
    </main>
  );
}
