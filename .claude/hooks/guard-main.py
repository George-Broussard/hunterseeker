#!/usr/bin/env python3
"""PreToolUse hook: block git operations that would change `main` directly.

AGENTS.md §10: all changes reach main through a PR. This hook enforces it for Bash
tool calls. Exit 2 blocks the call and shows the message to the agent.

Blocks:
  - `git push` targeting main (any form: `origin main`, `HEAD:main`, `+main`, --force)
  - `git commit` / `git merge` / `git rebase` / `git cherry-pick` / `git am`
    while the working directory is checked out on main
"""
import json
import re
import subprocess
import sys


def current_branch(cwd: str) -> str | None:
    try:
        # symbolic-ref (not rev-parse) so this also works on an unborn branch
        out = subprocess.run(
            ["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def block(msg: str) -> None:
    print(f"BLOCKED by .claude/hooks/guard-main.py: {msg}\n"
          "All changes to main go through a PR (AGENTS.md §10). "
          "Use /claim to work on a branch in a worktree, then /ship.", file=sys.stderr)
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = (payload.get("tool_input") or {}).get("command", "")
    cwd = payload.get("cwd") or "."

    if not re.search(r"\bgit\b", cmd):
        sys.exit(0)

    # --- pushes that target main, regardless of current branch ---
    # Matches: git push origin main | git push origin HEAD:main | git push -f origin +main
    # | git push --force-with-lease origin feature:main | git push origin main --force
    if re.search(r"\bgit\s+push\b", cmd):
        if re.search(r"(^|[\s:+])main(\s|$)", cmd.split("git push", 1)[1]):
            block("`git push` targeting main.")

    # --- history-changing commands while sitting on main ---
    if re.search(r"\bgit\s+(commit|merge|rebase|cherry-pick|am|revert)\b", cmd):
        branch = current_branch(cwd)
        if branch == "main":
            block(f"`{cmd.strip()[:60]}` while checked out on main.")

    sys.exit(0)


if __name__ == "__main__":
    main()
