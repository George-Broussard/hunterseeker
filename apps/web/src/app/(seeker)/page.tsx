import { Feed, FeedError } from "@/components/feed";
import { MessageRail } from "@/components/messaging";
import { loadConversations, loadFeedPage } from "@/lib/api";

// The Feed is per-Seeker and continuously re-ranked: never prerender it.
export const dynamic = "force-dynamic";

// TODO(#7/#10): once auth lands, `/` needs a role check — a Hunter hitting `/` should go to
// `/hunter`. That belongs in the route guard (#7 owns it), not here.

// TODO(#7): the viewer's id comes from the session; until then, the API stub's caller.
const STUB_VIEWER_ID = "00000000-0000-4000-8000-00000000e001";

/**
 * Seeker home: the Feed (posts from Connections interleaved with Matches — the API does
 * the interleaving) with the message center in the right rail.
 */
export default async function SeekerHomePage() {
  const [feed, conversations] = await Promise.all([loadFeedPage(), loadConversations()]);

  return (
    <main className="mx-auto grid w-full max-w-6xl flex-1 gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[minmax(0,1fr)_20rem]">
      <div className="lg:order-last">
        <MessageRail
          conversations={conversations.ok ? conversations.data : []}
          error={conversations.ok ? null : conversations.message}
          viewerId={STUB_VIEWER_ID}
        />
      </div>

      <section aria-label="Feed" className="min-w-0">
        <h1 className="sr-only">Feed</h1>
        {feed.ok ? <Feed initialPage={feed.data} /> : <FeedError message={feed.message} />}
      </section>
    </main>
  );
}
