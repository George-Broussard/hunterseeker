#!/usr/bin/env bash
# Create (or update) the label set that the agent workflow depends on.
# Idempotent — safe to re-run. Requires `gh` authenticated against this repo.
set -euo pipefail

label() {
  local name="$1" color="$2" desc="$3"
  gh label create "$name" --color "$color" --description "$desc" --force >/dev/null
  echo "  $name"
}

echo "status:"
label "status:ready"       "0E8A16" "Unclaimed and ready for an agent to pick up"
label "status:in-progress" "FBCA04" "Claimed — see the claim comment for who and what scope"
label "status:review"      "1D76DB" "PR open, awaiting review/merge"
label "status:blocked"     "B60205" "Cannot proceed — see comments for why"

echo "type:"
label "type:feature"  "A2EEEF" "New capability"
label "type:bug"      "D73A4A" "Something is wrong"
label "type:chore"    "CFD3D7" "Tooling, deps, refactors, docs"
label "type:decision" "5319E7" "An open question that must be resolved before building on it"

echo "area:"
label "area:web"          "BFD4F2" "apps/web — Next.js"
label "area:api"          "BFD4F2" "apps/api — FastAPI, cross-cutting"
label "area:shared"       "BFD4F2" "packages/shared — generated types"
label "area:matching"     "C5DEF5" "Matching engine, embeddings, ATS screening gate"
label "area:ats"          "C5DEF5" "ATS templates and pipeline stages"
label "area:profiles"     "C5DEF5" "Seeker profiles, company profiles"
label "area:applications" "C5DEF5" "Applications and the seeker dashboard"
label "area:feed"         "C5DEF5" "Feed and job board surfaces"
label "area:network"      "C5DEF5" "Connections"
label "area:messaging"    "C5DEF5" "Messaging and notifications"
label "area:imports"      "C5DEF5" "Ashby / Greenhouse / external imports"
label "area:infra"        "D4C5F9" "CI, deploy, database, tooling"
label "area:docs"         "D4C5F9" "AGENTS.md, skills, templates"

echo "done."
