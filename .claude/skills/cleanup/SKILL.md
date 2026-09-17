---
name: cleanup
description: Tear down a finished issue's worktree and branch after its PR has merged, and verify the issue closed. Use after every merge. Leaving worktrees behind is a bug — stale worktrees pin stale branches and confuse other agents' conflict checks. Argument is the issue number.
---

# /cleanup <issue-number> — tear down after merge

Run from the **main checkout** (not from inside the worktree you're about to delete).

## 1. Verify it actually merged

```bash
gh pr list --search "<N>" --state merged --json number,title,mergedAt,headRefName
```

If the PR is not merged, **stop**. Do not delete an unmerged branch. If the PR was closed
without merging, ask before deleting anything — the work may still be wanted.

## 2. Remove the worktree and branches

```bash
cd <repo root>
git worktree remove .worktrees/<N>-<slug>
git branch -D <N>-<slug>
git push origin --delete <N>-<slug>   # may already be gone if auto-delete is on; that's fine
git worktree prune
git fetch origin --prune
```

If `git worktree remove` refuses because of uncommitted changes, look at what's there
before forcing. If it's genuinely leftover junk, `--force`. If it's real work that never
got committed, that's a problem worth reporting, not silently deleting.

## 3. Verify the issue closed

```bash
gh issue view <N> --json state,labels
```

`Closes #N` in the PR body should have closed it. If it's still open, close it with a
comment linking the PR. Remove any lingering `status:*` label — closed issues don't carry
a status.

## 4. Sync main

```bash
git checkout main
git pull origin main
```

## 5. Confirm

Report: worktree removed, branches deleted, issue #N state. Then `git worktree list`
should show only the main checkout (and other agents' active worktrees).
