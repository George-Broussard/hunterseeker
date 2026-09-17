#!/usr/bin/env python3
"""PreToolUse hook: block git operations that would change `main` directly.

AGENTS.md §10: all changes reach main through a PR. This hook enforces it for Bash
tool calls. Exit 2 blocks the call and shows the message to the agent.

Blocks:
  - a push whose refspec targets main (`origin main`, `HEAD:main`, `+main`, -f ...)
  - commit / merge / rebase / cherry-pick / am / revert when the checkout the
    command actually targets is on main

"Actually targets" means: the command is tokenized quote-aware and split into
segments on `&&` / `||` / `;` / `|`; a virtual cwd is tracked through `cd` segments;
`git -C <path>` is honored. Only segments whose command word is `git` are inspected,
so an issue body or commit message that merely mentions a git command is not a
false positive.

Subagents have their cwd pinned to the main checkout, so both
`cd .worktrees/x && git commit` and `git -C .worktrees/x commit` must resolve to the
worktree's branch, not the session's.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys

SEPARATORS = {"&&", "||", ";", "|", "&"}
HISTORY_CMDS = {"commit", "merge", "rebase", "cherry-pick", "am", "revert"}
# Words that can precede the real command without changing what it is.
PREFIX_WORDS = {"env", "command", "builtin", "exec", "nohup", "time"}


def current_branch(path: str) -> str | None:
    """Branch checked out at `path`, or None if it isn't a git checkout."""
    try:
        out = subprocess.run(
            # symbolic-ref (not rev-parse) so this also works on an unborn branch
            ["git", "-C", path, "symbolic-ref", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def tokenize(cmd: str) -> list[str]:
    """shlex with punctuation_chars so `&&`, `||`, `;`, `|` come out as tokens."""
    try:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        lex.commenters = ""
        return list(lex)
    except ValueError:
        # Unbalanced quotes etc. — crude split so we still inspect something.
        return cmd.split()


def segments(tokens: list[str]) -> list[list[str]]:
    segs: list[list[str]] = [[]]
    for tok in tokens:
        if tok in SEPARATORS:
            segs.append([])
        else:
            segs[-1].append(tok)
    return [s for s in segs if s]


def strip_prefix(seg: list[str]) -> list[str]:
    """Drop `env`, `FOO=bar`, etc. so seg[0] is the real command."""
    i = 0
    while i < len(seg):
        w = seg[i]
        if w in PREFIX_WORDS or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", w):
            i += 1
        else:
            break
    return seg[i:]


def resolve(base: str, path: str) -> str:
    path = os.path.expanduser(path)
    return os.path.normpath(path if os.path.isabs(path) else os.path.join(base, path))


def git_target_and_subcommand(seg: list[str], vcwd: str) -> tuple[str, str | None]:
    """For a segment starting with `git`, return (target checkout path, subcommand)."""
    target = vcwd
    i = 1
    while i < len(seg):
        w = seg[i]
        if w == "-C" and i + 1 < len(seg):
            target = resolve(target, seg[i + 1]); i += 2
        elif w.startswith("-C") and len(w) > 2:
            target = resolve(target, w[2:]); i += 1
        elif w.startswith("--work-tree="):
            target = resolve(vcwd, w.split("=", 1)[1]); i += 1
        elif w == "--work-tree" and i + 1 < len(seg):
            target = resolve(vcwd, seg[i + 1]); i += 2
        elif w == "-c" and i + 1 < len(seg):
            i += 2  # git -c key=val
        elif w.startswith("-"):
            i += 1  # other global flags (--no-pager, etc.)
        else:
            return target, w
    return target, None


def push_targets_main(seg: list[str]) -> bool:
    """True if a push segment's refspecs touch main."""
    for w in seg[1:]:
        if w.startswith("-"):
            continue
        # refspec forms: main, +main, HEAD:main, feature:main, refs/heads/main
        dst = w.split(":", 1)[1] if ":" in w else w
        dst = dst.lstrip("+")
        if dst in ("main", "refs/heads/main"):
            return True
    return False


def block(msg: str) -> None:
    print(f"BLOCKED by .claude/hooks/guard-main.py: {msg}\n"
          "All changes to main go through a PR (AGENTS.md §10). "
          "Use /claim to work on a branch in a worktree, then /ship. "
          "From a subagent (cwd pinned to the main checkout), run git as "
          "`git -C .worktrees/<branch> ...`.", file=sys.stderr)
    sys.exit(2)


def check(cmd: str, cwd: str) -> None:
    if not re.search(r"\bgit\b", cmd):
        return
    vcwd = cwd
    for raw in segments(tokenize(cmd)):
        seg = strip_prefix(raw)
        if not seg:
            continue
        head = seg[0]
        if head == "cd":
            vcwd = resolve(vcwd, seg[1]) if len(seg) > 1 else os.path.expanduser("~")
        elif head == "pushd" and len(seg) > 1:
            vcwd = resolve(vcwd, seg[1])
        elif head == "git":
            target, sub = git_target_and_subcommand(seg, vcwd)
            if sub == "push":
                if push_targets_main(seg):
                    block("push targeting main.")
            elif sub in HISTORY_CMDS:
                if current_branch(target) == "main":
                    block(f"`git {sub}` in a checkout on main ({target}).")


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    if payload.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (payload.get("tool_input") or {}).get("command", "")
    cwd = payload.get("cwd") or os.getcwd()
    check(cmd, cwd)
    sys.exit(0)


if __name__ == "__main__":
    main()
