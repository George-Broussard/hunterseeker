import Link from "next/link";

/**
 * Placeholder conversation page so the rail has somewhere to link. The thread view
 * (message history, composer, read receipts) is a later messaging issue.
 */
export default async function ConversationPage({ params }: PageProps<"/messages/[id]">) {
  const { id } = await params;

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-4 p-8">
      <Link href="/" className="text-sm opacity-70 hover:opacity-100">
        &larr; Back to your feed
      </Link>
      <h1 className="text-2xl font-semibold tracking-tight">Conversation</h1>
      <p className="text-sm opacity-70">
        Conversation <code className="text-xs">{id}</code>. The full thread view is coming in a
        later issue; use the quick reply in the message rail for now.
      </p>
    </main>
  );
}
