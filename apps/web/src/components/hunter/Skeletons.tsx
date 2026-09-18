/** Loading placeholders. Shapes mirror the real sections so the layout does not jump. */

function Bar({ className = "" }: { className?: string }) {
  return <div className={`rounded bg-current/10 ${className}`} />;
}

function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-3 rounded-lg border border-current/15 p-4">{children}</div>
  );
}

export function SectionHeadingSkeleton() {
  return (
    <div className="flex flex-col gap-2">
      <Bar className="h-6 w-40" />
      <Bar className="h-4 w-72 max-w-full" />
    </div>
  );
}

export function OpenRolesSkeleton() {
  return (
    <section
      aria-busy="true"
      aria-label="Loading open roles"
      className="flex animate-pulse flex-col gap-4"
    >
      <SectionHeadingSkeleton />
      {[0, 1].map((i) => (
        <Card key={i}>
          <div className="flex justify-between">
            <Bar className="h-5 w-48" />
            <Bar className="h-5 w-24" />
          </div>
          <Bar className="h-4 w-64" />
          <div className="flex gap-2">
            <Bar className="h-7 w-32 rounded-full" />
            <Bar className="h-7 w-28 rounded-full" />
            <Bar className="h-7 w-36 rounded-full" />
          </div>
        </Card>
      ))}
    </section>
  );
}

export function CompanyFeedSkeleton() {
  return (
    <section
      aria-busy="true"
      aria-label="Loading company feed"
      className="flex animate-pulse flex-col gap-4"
    >
      <SectionHeadingSkeleton />
      <Bar className="h-24 w-full rounded-lg" />
      {[0, 1].map((i) => (
        <Card key={i}>
          <Bar className="h-4 w-40" />
          <Bar className="h-4 w-full" />
          <Bar className="h-4 w-2/3" />
        </Card>
      ))}
    </section>
  );
}

export function RailSkeleton() {
  return (
    <div aria-busy="true" className="flex animate-pulse flex-col gap-4">
      <Card>
        <Bar className="h-5 w-32" />
        <Bar className="h-4 w-full" />
        <Bar className="h-4 w-5/6" />
      </Card>
      <Card>
        <Bar className="h-5 w-24" />
        <Bar className="h-4 w-full" />
      </Card>
    </div>
  );
}
