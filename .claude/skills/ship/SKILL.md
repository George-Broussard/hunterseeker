---
name: ship
description: Open a pull request for the current worktree's branch. Rebases on main, runs the project's checks, pushes, opens the PR linked to its issue, and moves the issue to review. Use when the work for an issue is complete. Never merges — merging is a human action.
---

# /ship — open a PR

Run from inside the worktree for the issue. This gets your work to `main` the only
allowed way: through a PR.

> ### If you are a subagent
> Your Bash cwd is pinned to the main checkout on every call and does not persist, and
> the `EnterWorktree` tool refuses to run for you. Run **every** command as
> `cd .worktrees/<N>-<slug> && <command>` or `git -C .worktrees/<N>-<slug> <args>`.
> The PreToolUse hook resolves both forms to the worktree's branch, so commits there are
> allowed while commits on `main` are still blocked.

## 0. Sanity

```bash
git branch --show-current     # must be <N>-<slug>, never main
git status --porcelain        # commit or stash everything first
```

If you're on `main`, stop — you've been working in the wrong place. Move the changes to
a proper branch/worktree before continuing.

Extract the issue number from the branch name (`42-ats-screening-gate` → 42).

## 1. Rebase on latest main

```bash
git fetch origin main
git rebase origin/main
```

Resolve conflicts if any. If your PR includes a database migration, **regenerate it after
the rebase** so it sits on top of whatever main now has — migration chains are the most
common merge conflict in this repo.

## 2. Run checks

Run whatever the project defines — lint, typecheck, tests, and codegen for
`packages/shared` if the API contract changed. Look for the canonical commands in
AGENTS.md or the relevant `package.json` / `pyproject.toml`. **Do not open a PR with
failing checks.** Fix them or note in the PR why they're expected to fail.

If the API schema changed, regenerate shared types and commit them — never hand-edit.

## 3. Push and open the PR

```bash
git push -u origin <N>-<slug>
gh pr create --base main --title "<imperative summary, matches the issue title>" \
  --body "$(cat <<'EOF'
Closes #<N>

## What changed
<Bullets. What a reviewer needs to know to review this quickly.>

## How it was verified
<What you ran, what you checked manually.>

## Out of scope / follow-ups
<Anything you deliberately left out, with issue numbers if you filed them.>
EOF
)"
```

`Closes #<N>` is required — it's what auto-closes the issue on merge, and it's how
`/cleanup` verifies the loop closed. If the PR is not ready for review, add `--draft`.

## 4. Update the issue

```bash
gh issue edit <N> --add-label status:review --remove-label status:in-progress
gh issue comment <N> --body "PR opened: <PR URL>"
```

## 5. Stop

**Do not merge.** Merging is a human action by default (AGENTS.md §10). Report the PR
URL and wait. If review comments come in, address them on the same branch and push;
don't open a new PR.

Once the PR is merged, run `/cleanup <N>`.
