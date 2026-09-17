"""Tests for guard-main.py.  Run:  python3 -m unittest .claude/hooks/test_guard_main.py"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("guard_main", HERE / "guard-main.py")
guard = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(guard)


def _git(path: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(path), *args], check=True, capture_output=True)


class GuardMainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.on_main = root / "on-main"
        cls.on_main.mkdir()
        _git(cls.on_main, "init", "-q", "-b", "main")
        cls.on_feature = root / "on-feature"
        cls.on_feature.mkdir()
        _git(cls.on_feature, "init", "-q", "-b", "42-feature")
        # a nested "worktree-like" checkout under the main one, as .worktrees/<x> would be
        cls.nested = cls.on_main / ".worktrees" / "7-nested"
        cls.nested.mkdir(parents=True)
        _git(cls.nested, "init", "-q", "-b", "7-nested")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def assert_blocked(self, cmd: str, cwd: Path) -> None:
        with self.assertRaises(SystemExit, msg=f"expected block: {cmd}") as cm:
            guard.check(cmd, str(cwd))
        self.assertEqual(cm.exception.code, 2)

    def assert_allowed(self, cmd: str, cwd: Path) -> None:
        try:
            guard.check(cmd, str(cwd))
        except SystemExit as e:  # pragma: no cover
            self.fail(f"expected allow but got exit {e.code}: {cmd}")

    # --- pushes: independent of cwd ---
    def test_push_to_main_forms_blocked(self) -> None:
        for cmd in [
            "git push origin main",
            "git push -f origin HEAD:main",
            "git push origin +main",
            "git push --force-with-lease origin feature:main",
            "git push origin refs/heads/main",
            "git push origin main --force",
        ]:
            self.assert_blocked(cmd, self.on_feature)

    def test_push_to_feature_allowed(self) -> None:
        for cmd in [
            "git push -u origin 42-feature",
            "git push origin main-feature",
            "git push origin 7-domain",
            "git push --force-with-lease",
            "git push",
        ]:
            self.assert_allowed(cmd, self.on_main)

    # --- history commands: depend on the targeted checkout ---
    def test_commit_on_main_blocked(self) -> None:
        self.assert_blocked("git commit -m x", self.on_main)
        self.assert_blocked("git merge 42-feature", self.on_main)
        self.assert_blocked("git rebase origin/main", self.on_main)

    def test_commit_on_feature_allowed(self) -> None:
        self.assert_allowed("git commit -m x", self.on_feature)
        self.assert_allowed("git rebase origin/main", self.on_feature)

    def test_cd_into_worktree_then_commit_allowed(self) -> None:
        # the subagent case: cwd pinned to main, but the command cds first
        self.assert_allowed("cd .worktrees/7-nested && git add -A && git commit -m x", self.on_main)
        self.assert_allowed(f"cd {self.nested} && git commit -m x", self.on_main)

    def test_cd_back_to_main_then_commit_blocked(self) -> None:
        self.assert_blocked(f"cd {self.nested} && cd ../.. && git commit -m x", self.on_main)

    def test_dash_C_worktree_allowed(self) -> None:
        self.assert_allowed("git -C .worktrees/7-nested commit -m x", self.on_main)
        self.assert_allowed(f"git -C {self.nested} commit -m x", self.on_main)

    def test_dash_C_main_blocked(self) -> None:
        # the latent false negative from #12
        self.assert_blocked(f"git -C {self.on_main} commit -m x", self.on_feature)
        self.assert_blocked("git -C ../.. commit -m x", self.nested)

    def test_global_flags_before_subcommand(self) -> None:
        self.assert_blocked("git --no-pager -c user.name=x commit -m x", self.on_main)
        self.assert_allowed("git --no-pager -c user.name=x commit -m x", self.on_feature)

    def test_env_prefix(self) -> None:
        self.assert_blocked("GIT_AUTHOR_NAME=x git commit -m x", self.on_main)
        self.assert_blocked("env FOO=1 git commit -m x", self.on_main)

    # --- text that merely mentions git is not a command ---
    def test_mentions_in_arguments_not_blocked(self) -> None:
        self.assert_allowed('gh issue create --body "run git commit then git push origin main"', self.on_main)
        self.assert_allowed("echo 'git commit -m x'", self.on_main)
        self.assert_allowed(
            'gh pr create --base main --title "x" --body "git push origin main is blocked"',
            self.on_main,
        )

    def test_push_then_pr_base_main_in_same_command(self) -> None:
        # the orchestrator false positive: push to feature + gh pr create --base main
        self.assert_allowed(
            'git push -u origin 42-feature && gh pr create --base main --title t --body b',
            self.on_feature,
        )

    def test_heredoc_body_mentioning_git(self) -> None:
        cmd = 'gh issue create --title t --body "$(cat <<\'EOF\'\nUse git commit and git push origin main.\nEOF\n)"'
        self.assert_allowed(cmd, self.on_main)

    def test_non_git_commands_ignored(self) -> None:
        self.assert_allowed("ls -la && pnpm test", self.on_main)

    def test_unbalanced_quotes_still_inspected(self) -> None:
        self.assert_blocked('git commit -m "unterminated', self.on_main)


if __name__ == "__main__":
    unittest.main()
