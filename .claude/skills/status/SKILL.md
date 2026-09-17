---
name: status
description: Show what every agent is currently working on — in-progress issues, open PRs, active worktrees, and stale claims. Run this before picking up any work, and whenever you need to know whether someone else is already on something.
---

# /status — who is working on what

Read-only. Run this before `/claim`, and any time you're unsure whether work overlaps.

## Steps

1. Sync with the remote so you're not reading stale state:
   ```bash
   git fetch origin --prune
   ```

2. List claimed work:
   ```bash
   gh issue list --label status:in-progress --json number,title,labels,assignees,updatedAt \
     --template '{{range .}}#{{.number}}  {{.title}}  [{{range .labels}}{{.name}} {{end}}]  updated {{timeago .updatedAt}}{{"\n"}}{{end}}'
   ```

3. List open PRs (work that's done but not merged — it still owns its files):
   ```bash
   gh pr list --state open --json number,title,headRefName,updatedAt,isDraft \
     --template '{{range .}}#{{.number}}  {{.title}}  ({{.headRefName}}){{if .isDraft}} DRAFT{{end}}  updated {{timeago .updatedAt}}{{"\n"}}{{end}}'
   ```

4. List local worktrees (agents on this machine):
   ```bash
   git worktree list
   ```

5. Flag stale claims. For each in-progress issue, check when its branch last received a
   push:
   ```bash
   git log -1 --format='%cr' origin/<branch>
   ```
   No pushes in **24 hours** → report it as stale. Stale claims may be taken over per
   AGENTS.md §10, but only after commenting on the issue.

6. Report a compact table: issue, title, area labels, branch, last activity, stale?.

## Interpreting overlap

Two pieces of work overlap if they share an `area:*` label **and** would plausibly touch
the same files or the same database tables. Same area alone is not a conflict; same area
plus same module is. When in doubt, read the claim comment on the other issue — it names
the intended scope.
