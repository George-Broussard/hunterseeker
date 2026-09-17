// Skeleton shown while a /login or /signup page is streaming in.
export default function AuthLoading() {
  return (
    <div className="animate-pulse space-y-4" aria-busy="true" aria-label="Loading">
      <div className="h-6 w-1/2 rounded bg-foreground/10" />
      <div className="h-10 rounded bg-foreground/10" />
      <div className="h-10 rounded bg-foreground/10" />
      <div className="h-10 rounded bg-foreground/20" />
    </div>
  );
}
