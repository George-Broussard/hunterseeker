import { listOpenRoles } from "@/lib/api/matching";

import { ErrorPanel } from "./ErrorPanel";
import { OpenRolesEmptyState } from "./OpenRolesEmptyState";
import { RoleCard } from "./RoleCard";

/** Server component: the Hunter's open roles, ranked candidates first. */
export async function OpenRolesSection() {
  const result = await listOpenRoles();

  return (
    <section aria-labelledby="open-roles-heading" className="flex flex-col gap-4">
      <header>
        <h2 id="open-roles-heading" className="text-xl font-semibold tracking-tight">
          Open roles
        </h2>
        <p className="text-sm opacity-70">
          Every candidate here has already passed the role&apos;s ATS screening. This is who to talk
          to, not who to reject.
        </p>
      </header>

      {!result.ok ? (
        <ErrorPanel title="Could not load your open roles." message={result.message} />
      ) : result.value.length === 0 ? (
        <OpenRolesEmptyState />
      ) : (
        <ul className="flex flex-col gap-4">
          {result.value.map((role) => (
            <RoleCard key={role.job.id} role={role} />
          ))}
        </ul>
      )}
    </section>
  );
}
