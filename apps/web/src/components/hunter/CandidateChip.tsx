import type { MatchedCandidate } from "@/lib/api/matching";

import { formatScore } from "./format";

/**
 * One ranked candidate on a role card.
 *
 * Only what a Match exposes reaches the Hunter: the Seeker's public display name, the
 * Match score, and the Profile headline (as a tooltip). Contact details are never on a
 * chip — a Hunter reaches a Seeker through messaging (AGENTS.md §8). The "screened"
 * badge is always true by construction: a Match exists only after an ATS pass.
 */
export function CandidateChip({ candidate }: { candidate: MatchedCandidate }) {
  return (
    <li
      className="flex items-center gap-2 rounded-full border border-current/15 py-1 pr-1.5 pl-3 text-sm"
      title={candidate.headline ?? undefined}
    >
      <span className="font-medium">{candidate.seeker.display_name}</span>
      <span className="tabular-nums opacity-70" aria-label="Match score">
        {formatScore(candidate.score)}
      </span>
      <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-xs font-medium text-emerald-700 dark:text-emerald-300">
        screened
      </span>
    </li>
  );
}
