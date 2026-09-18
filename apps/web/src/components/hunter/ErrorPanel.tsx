/** Inline error state for one section. The rest of the page keeps rendering. */
export function ErrorPanel({ title, message }: { title: string; message: string }) {
  return (
    <p role="alert" className="rounded-lg border border-red-500/40 p-4 text-sm">
      <span className="font-medium">{title}</span> {message}
    </p>
  );
}
