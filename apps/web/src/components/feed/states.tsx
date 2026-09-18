/** Loading, empty and error states for the Feed column. All server-renderable. */

function SkeletonCard({ lines }: { lines: number }) {
  return (
    <div className="animate-pulse rounded-lg border border-current/15 p-4">
      <div className="flex items-center gap-3">
        <div className="size-10 rounded-full bg-current/10" />
        <div className="flex-1 space-y-2">
          <div className="h-3 w-1/3 rounded bg-current/10" />
          <div className="h-2 w-1/4 rounded bg-current/10" />
        </div>
      </div>
      <div className="mt-4 space-y-2">
        {Array.from({ length: lines }, (_, i) => (
          <div key={i} className="h-3 rounded bg-current/10" style={{ width: `${90 - i * 15}%` }} />
        ))}
      </div>
    </div>
  );
}

export function FeedSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div aria-busy="true" aria-label="Loading feed" className="flex flex-col gap-4">
      {Array.from({ length: count }, (_, i) => (
        <SkeletonCard key={i} lines={2 + (i % 2)} />
      ))}
    </div>
  );
}

export function FeedEmpty() {
  return (
    <div className="rounded-lg border border-dashed border-current/15 p-8 text-center">
      <p className="font-medium">Your feed is empty</p>
      <p className="mt-1 text-sm opacity-70">
        Add connections and build your profile to fill your feed.
      </p>
    </div>
  );
}

export function FeedError({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div role="alert" className="rounded-lg border border-current/15 p-4 text-sm">
      <p>Could not load your feed. {message}</p>
      {onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-2 rounded-md border border-current/15 px-3 py-1"
        >
          Try again
        </button>
      ) : null}
    </div>
  );
}
