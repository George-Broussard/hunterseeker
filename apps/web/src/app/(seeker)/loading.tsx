import { FeedSkeleton } from "@/components/feed";
import { MessageRailSkeleton } from "@/components/messaging";

export default function SeekerLoading() {
  return (
    <main className="mx-auto grid w-full max-w-6xl flex-1 gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[minmax(0,1fr)_20rem]">
      <div className="lg:order-last">
        <MessageRailSkeleton />
      </div>
      <div className="min-w-0">
        <FeedSkeleton />
      </div>
    </main>
  );
}
