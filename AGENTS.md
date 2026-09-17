# AGENTS.md

Grounding context for AI agents working in this repository. Read this before writing code.

---

## 1. Status: greenfield

**This repository is currently empty.** Nothing described below as "layout" or
"domain model" exists on disk yet — it is the agreed target, not the current state.

Do not assume any file, module, table, or endpoint exists. Check before you reference.
When you build something described here, build it as described here; when this file and
the code disagree, the code wins and this file should be updated in the same PR.

---

## 2. What hunter/seeker is

hunter/seeker is an agentic job board that inverts the usual direction of job search.

The conventional model: a job seeker searches, filters, and applies. hunter/seeker's model: a
seeker builds a rich **profile** describing who they are and what they want, and the
system continuously **matches** them to jobs. The seeker reviews matches rather than
hunting for them. Employers get the mirror image — a ranked list of candidates per role
rather than a pile of inbound applications to triage.

The product is matching-first. Search is a fallback, not the primary interaction. If a
feature can be expressed as "improve the match," prefer that over "add another filter."

### Core tenet: no applications into the void

**A Seeker is never shown a job their resume would be screened out of.** Every job
served to a Seeker is one where their Profile has *already passed* that job's ATS
screening. The ATS runs *before* the job is surfaced, not after the Seeker applies.

This is the promise the product makes to Seekers, and it is the thing that makes
hunter/seeker different from a job board with good recommendations. Any feature, ranking
change, or shortcut that would put a job in front of a Seeker without an ATS pass
breaks that promise. Do not build it.

---

## 3. Vocabulary (use these terms exactly)

These words have specific meanings in this codebase. Use them in code, schemas, APIs,
and UI copy. Do not invent synonyms.

| Term | Meaning |
|---|---|
| **Seeker** | A user looking for a job. |
| **Hunter** | A user posting jobs — recruiter, hiring manager, or agency. |
| **Match** | A scored Seeker↔Job pairing produced by the matching engine. **A Match exists only if the Seeker's Profile has passed the Job's ATS screening.** Bidirectional: the same Match is shown to the Seeker as a job recommendation and to the Hunter as a candidate. |
| **ATS pass** | The result of evaluating a Seeker's Profile against a Job's ATS screening criteria. A precondition for a Match — not a step that happens after applying. |
| **Match score** | Normalized 0–1 strength of a Match. |
| **Match threshold** | A Seeker-controlled floor. Matches below it are not surfaced to that Seeker. |
| **Profile** | A Seeker's structured self-description; the input to matching. Distinct from **Account** (auth/billing) and from **Company Profile**. |
| **Company Profile** | An organization page a Hunter manages and posts from. One Hunter may manage several. |
| **Feed** | The scrollable surface mixing matched jobs with social posts from a Seeker's network. |
| **Job Board** | The Seeker's dedicated, personalized recommendation surface. Matches only — no social posts. Distinct from the Feed. |
| **ATS** | A Hunter-defined, **savable and reusable** hiring pipeline template (stages, gates, criteria) attached to postings. In this codebase "ATS" means *our* configurable pipeline, never a third-party system. |
| **Application** | A Seeker's submission to a Job, moving through that Job's ATS stages. |
| **Connection** | A mutual professional link between any two users, Seeker or Hunter. |
| **Import** | Pulling job postings in from an external recruiting platform (Ashby, Greenhouse, etc.). |

> ### Product name vs. role names — read this carefully
> The product is **hunter/seeker**. The two user roles are **Hunter** and **Seeker**.
> The product name is built from the role names, so they are easy to conflate.
>
> - **The product** is written `hunter/seeker` — lowercase, with the slash, even at the
>   start of a sentence. Never "Hunter/Seeker", "HunterSeeker", or just "Hunter".
>   Where a slash is not allowed (package names, env vars, database names, repo name),
>   use `hunterseeker`. The repo directory is `hunter` for historical reasons only.
> - **The roles** are capitalized in prose and used as-is in code: `Hunter`, `Seeker`,
>   `hunter_id`, `seeker_id`, `HunterProfile`, `role="hunter"`.
>
> A code symbol named `hunter` or `seeker` must always mean the *role*. If you need to
> refer to the platform itself in code, say `platform` or `hunterseeker`. Never name a
> generic module `hunter` — use `app`, `core`, or the specific domain.

---

## 4. Tech stack (decided)

| Layer | Choice | Notes |
|---|---|---|
| Front end | **Next.js (App Router)**, TypeScript | Server components for Feed and Job Board; SSR for public job pages. |
| Back end | **FastAPI** (Python), async | Owns all business logic. Pydantic models are the API contract. |
| Relational | **PostgreSQL** | Users, profiles, jobs, applications, ATS configs, connections, messages. Source of truth. |
| Vectors | **pgvector** in the same Postgres | Embeddings live beside relational data so a match query can filter on salary/location/work-authorization in one statement. Use HNSW indexes. |
| Analytics / large data | **Apache Iceberg** | Append-only, high-volume, non-transactional data: feed impressions, match-score history, application funnel events, import runs. Never the source of truth for anything a user edits. |
| Monorepo | `apps/web`, `apps/api`, `packages/shared` | |

**Rules that follow from this:**

- **The Next.js app is a client of the FastAPI service.** Business logic, matching, and
  direct database access belong in `apps/api`. Next.js route handlers are for
  session/BFF concerns only — do not reach into Postgres from the web app.
- **Do not add a standalone vector service.** Matching stays in Postgres until there is a
  measured reason to move, and that decision is not an agent's to make unilaterally.
- **Postgres vs Iceberg:** if a user can edit it or a transaction depends on it, Postgres.
  If it is an event that only ever gets appended and later aggregated, Iceberg.
- Generate TypeScript types from the FastAPI OpenAPI schema. Do not hand-maintain
  duplicate type definitions across the language boundary.

---

## 5. Planned layout

```
apps/
  web/            # Next.js — App Router, TypeScript
  api/            # FastAPI — business logic, owns the database
packages/
  shared/         # Generated API types, shared constants/enums
```

Inside `apps/api`, organize by domain, not by technical layer — `matching/`, `profiles/`,
`applications/`, `ats/`, `messaging/`, `imports/`, `feed/`, `network/`. Avoid top-level
`models/`, `views/`, `services/` buckets that split one feature across four directories.

---

## 6. The matching engine is the core

Everything else is a surface over Matches. Treat it as the system's center of gravity.

- A Match is computed from a Seeker Profile and a Job in two stages, in this order:
  1. **ATS screening** — evaluate the Profile against the Job's ATS criteria. Fail → no
     Match, full stop. The job is never surfaced to this Seeker.
  2. **Scoring** — only for Profiles that passed, combine vector similarity with hard
     constraints (location, work authorization, compensation band, seniority) to rank.
- **The ATS pass is a gate, not a score input.** Do not fold ATS criteria into the
  similarity score where a strong-enough embedding could outweigh a failed screen.
- **Hard constraints are filters, not score penalties.** Never surface a Match that
  violates work authorization or a stated compensation floor just because semantic
  similarity is high.
- **This means ATS screening criteria must be machine-evaluable against a Profile.**
  When a Hunter builds an ATS template, the screening stage must be expressible as
  criteria the engine can run *before* anyone applies. Stages that need a human (phone
  screen, interview) come after the Match; they are not screening. Keep this
  distinction explicit in the ATS data model.
- When a Job's ATS changes, existing Matches for that Job must be re-screened. A Match
  that no longer passes must be withdrawn from the Seeker's surfaces.
- The same Match object serves both personas. Do not build separate seeker-side and
  hunter-side scoring paths that can disagree — one score, two views.
- Seekers control their own **match threshold**. Respect it on every seeker-facing
  surface. It is a user setting, not a tunable constant.
- Match scores change as profiles and jobs change. Treat scores as **recomputable
  derived data**, and write score history to Iceberg so ranking changes are explainable.
- Embeddings are derived data. Any profile or job write must be able to trigger
  re-embedding; never let an embedding silently go stale against its source row.

---

## 7. Feature surface

**Seeker:** Profile; Job Board (personalized recommendations); Feed (matches + network
posts); adjustable match threshold; application dashboard with statuses; in-app
notifications; Connections; messaging.

**Hunter:** Company Profile and posting; ranked candidate list per open role; savable,
reusable ATS templates; job import from Ashby/Greenhouse and similar; match surfacing for
open roles; outbound notifications to Seekers; Connections; messaging.

**Shared:** messaging and Connections are one system across both personas, not two
parallel implementations. Build them persona-agnostic from the start.

---

## 8. Conventions

- **Authorization is per-persona and must be explicit.** Every endpoint states which
  persona(s) may call it and what ownership is required. A Hunter may read a Seeker's
  Profile only through a Match or an Application that connects them — never by ID alone.
  Default to deny.
- Async throughout in FastAPI. Embedding calls, imports, and notification fan-out are I/O
  bound and must not block a request.
- Migrations for every schema change; no manual DDL.
- Tests alongside the code they test. Matching logic and authorization rules need real
  coverage — they are where correctness actually matters.
- External imports (Ashby, Greenhouse) must be resilient: rate-limited, retried,
  idempotent per external job ID. A re-run must not duplicate postings.
- Never log profile contents, message bodies, or application details.

---

## 9. Constraints worth knowing

This product makes **employment decisions**, which carries obligations most CRUD apps
do not have. This is practical engineering guidance, not legal advice — flag these to a
human rather than deciding alone:

- **Ranking must be explainable.** Persist enough per-Match signal to reconstruct *why*
  someone ranked where they did. Retain score history.
- **Protected characteristics must never be matching inputs** — directly or by proxy.
  Be alert to proxies: photos, names, graduation years, ZIP codes, school prestige.
  If you find yourself adding a feature that correlates with age, race, sex, disability,
  or national origin, stop and raise it.
- Automated hiring tools face bias-audit and disclosure requirements in some
  jurisdictions (e.g. NYC Local Law 144). Assume audit requirements exist.
- Profiles and messages are sensitive PII. Minimize what is collected, scope who can
  read it, and keep it out of logs and analytics exports.

---

## 10. How agents work in this repo

Multiple agents work here concurrently. These rules exist so they don't duplicate work,
collide on files, or leave the repo in a state the next agent has to untangle.
The skills in `.claude/skills/` implement them — use the skills rather than
improvising the steps.

### The unit of work is a GitHub issue

- **Every piece of work starts as an issue.** No issue, no branch. If you discover work
  while doing something else, file an issue (`/issue`) — do not just do it.
- **One issue → one branch → one worktree → one PR.** The branch is named
  `<issue-number>-<short-slug>` (e.g. `42-ats-screening-gate`) and the worktree lives at
  `.worktrees/<branch>`. Never work in the main checkout.
- **Keep issues small.** If it can't plausibly ship in one PR of a few hundred lines,
  split it before claiming. Big issues are where agents collide.
- **Open questions become `type:decision` issues.** Don't build on top of an undecided
  question in §11 — file or find the decision issue and get it resolved first.

### Claiming work (`/claim`)

Before touching anything:

1. `git fetch origin main` and check `gh issue list --label status:in-progress` and
   `gh pr list`. **If another agent has claimed the same issue or an overlapping one,
   stop.** Pick different work or coordinate in the issue comments.
2. Assign yourself, move the label to `status:in-progress`, and post a claim comment
   naming your branch and the scope you intend to touch.
3. Create the worktree from `origin/main`.

> All agents authenticate as the same GitHub account, so **assignment alone does not
> identify who is working.** The `status:in-progress` label plus the claim comment plus
> the branch name are the real claim. Always post the comment.

A claim with no commits pushed for **24 hours** is stale. Another agent may take it
over — but only after commenting on the issue that they are doing so.

### While working

- **Stay in scope.** Touch only what the issue covers. Unrelated fixes → new issue.
- **Never touch another agent's branch, worktree, or PR.** Comment on the PR instead.
- Rebase on `origin/main` early and often. Long-lived branches are where rework comes from.
- One database migration per PR, regenerated after your final rebase. Never hand-edit
  generated code in `packages/shared`; regenerate it.
- If the issue turns out to be wrong or bigger than expected, say so in the issue and
  re-scope *before* you write more code.

### Shipping (`/ship`)

- **Never commit to `main`. Never merge or push to `main` directly.** All changes go
  through a PR. A hook blocks this; do not work around it.
- Rebase on `origin/main`, run the project's checks, push, open the PR with
  `Closes #<issue>` in the body, and move the issue to `status:review`.
- **Merging is a human action by default.** Open the PR and stop. Do not merge your own
  PR unless the issue explicitly says agents may self-merge.

### After merge (`/cleanup`)

- Remove the worktree, delete the local and remote branch, prune, and confirm the issue
  closed. **Leaving worktrees behind is a bug** — a stale worktree pins a stale branch
  and confuses the next agent's conflict check.

### Recording decisions

When work resolves an item in §11, update this file in the same PR. This file is the
shared memory across agents; if it's stale, every agent starts wrong.

---

## 11. Open questions — do not silently decide these

Not yet settled. If your work depends on one, **ask rather than assume**:

- Auth provider and session strategy.
- Embedding model and vector dimensionality.
- Whether matching runs on write, on a schedule, or both.
- Hosting, deployment, and CI.
- Real-time transport for messaging and notifications (websockets vs polling).
- Whether Seekers can apply outside a Match, or only through one. (The no-void tenet
  weighs heavily toward Match-only — an out-of-Match application is by definition one
  that hasn't passed the ATS. Still needs an explicit decision.)
- Moderation model for Feed posts.

When one of these gets decided, record it in this file as part of the same change.
