---
name: issue
description: File a well-formed GitHub issue for a piece of work, a bug, or an open decision. Use whenever you discover work that needs doing — including work you found mid-task that is out of scope for your current issue. Every piece of work in this repo starts as an issue.
---

# /issue — file work

Every unit of work is an issue. This skill files one that another agent can pick up
without asking questions.

## Before filing

Check it doesn't already exist:
```bash
gh issue list --search "<key words>" --state all --limit 10
```
If a matching issue exists, comment on it rather than filing a duplicate.

## Filing

```bash
gh issue create \
  --title "<imperative, specific, under ~70 chars>" \
  --label "type:<feature|bug|chore|decision>" \
  --label "area:<area>" \
  --label "status:ready" \
  --body "$(cat <<'EOF'
## What
<One paragraph. What should exist or change when this is done.>

## Why
<The user-facing or system reason. Link the AGENTS.md section if it derives from one.>

## Scope
- Touches: <modules / directories / tables this will change>
- Does not touch: <anything an agent might reasonably assume is included but isn't>

## Done when
- [ ] <observable, testable condition>
- [ ] <...>

## Notes
<Constraints, gotchas, related issues (#N), open questions.>
EOF
)"
```

## Rules

- **Title is imperative and specific.** "Add ATS screening gate to match pipeline", not
  "matching stuff" or "ATS".
- **Scope is the most important section.** It's what lets another agent decide whether
  their work overlaps with this one. Name the modules and tables.
- **Keep it small.** If "Done when" has more than ~5 items or you can't imagine it as one
  PR, split it into multiple issues and link them.
- **Exactly one `type:*`, at least one `area:*`, and `status:ready`.** Labels are how
  `/status` and `/claim` detect overlap. Run `scripts/setup-labels.sh` if labels are
  missing.
- **Decisions are issues too.** An open question from AGENTS.md §11 gets
  `type:decision`. The "Done when" for a decision is "AGENTS.md updated and the question
  removed from §11".
- **Filing is not claiming.** Filing an issue does not mean you work on it. Use `/claim`
  for that.
- If you found this work while doing something else, mention the originating issue
  (`Found while working on #N`) and go back to your original scope.
