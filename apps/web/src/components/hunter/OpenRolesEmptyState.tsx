import Link from "next/link";

const primary =
  "rounded-md bg-foreground px-4 py-2 text-sm font-medium text-background hover:opacity-90";
const secondary =
  "rounded-md border border-current/25 px-4 py-2 text-sm font-medium hover:bg-current/5";

/** Zero open roles: point the Hunter at the two ways to get one. */
export function OpenRolesEmptyState() {
  return (
    <div className="flex flex-col items-start gap-4 rounded-lg border border-dashed border-current/25 p-6">
      <div>
        <h3 className="font-medium">No open roles yet</h3>
        <p className="text-sm opacity-70">
          Post a role and hunter/seeker will surface screened, ranked candidates here.
        </p>
      </div>
      <div className="flex flex-wrap gap-3">
        <Link href="/hunter/roles/new" className={primary}>
          Create a role
        </Link>
        <Link href="/hunter/imports/new" className={secondary}>
          Import from Ashby / Greenhouse
        </Link>
      </div>
    </div>
  );
}
