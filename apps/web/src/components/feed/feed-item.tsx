import type { FeedItem } from "@/lib/api";

import { MatchedJobCard } from "./matched-job-card";
import { PostCard } from "./post-card";

/** Renders one item of the `kind`-discriminated Feed union. */
export function FeedItemCard({ item }: { item: FeedItem }) {
  switch (item.kind) {
    case "post":
      return <PostCard post={item} />;
    case "matched_job":
      return <MatchedJobCard item={item} />;
  }
}
