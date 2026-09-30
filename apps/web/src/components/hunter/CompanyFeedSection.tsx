import { listCompanyFeed, listCompanyProfiles } from "@/lib/api/company-feed";

import { CompanyFeed } from "./CompanyFeed";
import { ErrorPanel } from "./ErrorPanel";

/** Server component: first page of the company feed plus the Hunter's Company Profiles. */
export async function CompanyFeedSection() {
  const [feed, companies] = await Promise.all([listCompanyFeed(), listCompanyProfiles()]);

  return (
    <section aria-labelledby="company-feed-heading" className="flex flex-col gap-4">
      <header>
        <h2 id="company-feed-heading" className="text-xl font-semibold tracking-tight">
          Company feed
        </h2>
        <p className="text-sm opacity-70">
          Posts from the Company Profiles you manage and from your network.
        </p>
      </header>

      {!feed.ok ? (
        <ErrorPanel title="Could not load your company feed." message={feed.message} />
      ) : (
        <CompanyFeed
          initialItems={feed.value.items}
          initialCursor={feed.value.nextCursor}
          companies={companies.ok ? companies.value : []}
          companiesError={companies.ok ? undefined : companies.message}
        />
      )}
    </section>
  );
}
