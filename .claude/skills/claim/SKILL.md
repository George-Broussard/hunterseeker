---
name: claim
description: Claim a GitHub issue and set up an isolated worktree and branch for it. Use this to start any piece of work. It checks that no other agent is already on the same or overlapping work, assigns the issue, labels it in-progress, posts a claim comment, and creates the worktree. Argument is the issue number.
---

# /claim <issue-number> — start work on an issue

Never work in the main checkout. Never start work without claiming. This skill does both
correctly.

## 1. Check for overlap — this is the whole point

```bash
git fetch origin --prune
gh issue view <N> --json number,title,labels,assignees,body,comments
gh issue list --label status:in-progress --json number,title,labels
gh pr list --state open --json number,title,headRefName
git worktree list
```

**Stop and do not claim if any of these is true:**

- The issue already has `status:in-progress` and a claim comment less than 24 hours old.
- The issue is `status:blocked` or is a `type:decision` that hasn't been decided.
- The issue depends on another issue (look for "depends on #N" / "blocked by #N") that
  isn't closed.
- An in-progress issue or open PR shares an `area:*` label with this one **and** its
  scope names the same modules or tables. Read the other claim comment to check.

If the claim on the issue is older than 24 hours with no pushes to its branch, you may
take it over: comment first (`Taking over stale claim from <date>; no activity on
<branch> since <date>.`), then proceed.

If there's overlap with active work, either pick a different issue or comment on both
issues proposing how to split the boundary. Do not just start.

## 2. Claim

Pick a branch name: `<N>-<short-kebab-slug>`, e.g. `42-ats-screening-gate`. Under ~40 chars.

```bash
gh issue edit <N> --add-assignee @me --add-label status:in-progress --remove-label status:ready
gh issue comment <N> --body "$(cat <<'EOF'
**Claimed** by agent `<agent-id>` on <YYYY-MM-DD HH:MM>.

- Branch: `<N>-<slug>`
- Intended scope: <modules, directories, tables you expect to touch>
- Will not touch: <anything adjacent you're deliberately leaving alone>
EOF
)"
```

`<agent-id>` is any identifier unique to your session — `$(hostname -s)-$(date +%m%d%H%M)`
is fine. **All agents share one GitHub account, so the comment is what actually
identifies you.** Do not skip it.

> ### If you are a subagent
> Your Bash cwd is pinned to the main checkout on every call and does not persist, and
> the `EnterWorktree` tool refuses to run for you. Run **every** command as
> `cd .worktrees/<N>-<slug> && <command>` or `git -C .worktrees/<N>-<slug> <args>`.
> The PreToolUse hook resolves both forms to the worktree's branch, so commits there are
> allowed while commits on `main` are still blocked.

## 3. Create the worktree

```bash
mkdir -p .worktrees
git worktree add .worktrees/<N>-<slug> -b <N>-<slug> origin/main
```

Then work **only inside** `.worktrees/<N>-<slug>`. The main checkout stays on `main` and
stays clean.

If your tool has a native worktree feature (e.g. Claude Code's `EnterWorktree`), you may
use it instead — but the branch name must still be `<N>-<slug>` so `/status` and other
agents can see which issue it belongs to.

## 4. Confirm

Report: issue number, branch, worktree path, and the scope you posted. Then start.

## While working

- Push early and often (`git push -u origin <N>-<slug>`). Pushed commits are how other
  agents see your claim is alive; an unpushed branch looks stale after 24h.
- Rebase on `origin/main` whenever it moves.
- If the scope changes materially, edit your claim comment. Other agents rely on it.
- Out-of-scope discoveries → `/issue`, then return to your scope.
