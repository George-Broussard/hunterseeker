"""Embedding documents: the only data that may be turned into a matching vector.

A ``SeekerProfileEmbeddingDoc`` / ``JobEmbeddingDoc`` is an explicit *projection* of a
Profile / Job. It is not the Profile and not the Job — it is the subset of them that the
matching engine is allowed to see semantically.

Two rules from AGENTS.md are enforced here **by construction**, not by filtering:

* §9 — protected characteristics and their proxies are never matching inputs. These
  models simply have no field for a name, photo, contact detail, date, year, school,
  ZIP/city, age, or anything of the kind, and ``extra="forbid"`` rejects any attempt to
  smuggle one in. If a caller wants to embed something, it needs a field here, and adding
  one is a reviewed change.
* §6 — hard constraints are filters, not score inputs. Location, remote policy,
  compensation, work authorization and seniority live as columns on the embedding rows
  (see ``hunterseeker.matching.models``) so a match query can filter then rank. They are
  not serialized into the embedded text. (``seniority_band`` is the one deliberate
  overlap: it is both a filter column and part of the semantic text, because "senior
  backend engineer" and "junior backend engineer" are different jobs, not just different
  rows.)

The free-text fields (``self_summary``, ``responsibilities_summary``, ...) are the one
place §9 content could still leak in via user-written prose. That is a content policy
concern for the Profile editor and the re-embed pipeline, not something this module can
solve structurally; it is called out so nobody assumes otherwise.

``to_text()`` is the canonical serialization that gets embedded. It is deterministic
(stable field order, normalized whitespace, sorted set-like fields) and every output is
tagged with ``EMBEDDING_SCHEMA_VERSION``. Bump the version whenever the *format* or the
*field set* changes, because vectors produced under different versions are not
comparable and must be re-embedded (see ``schema_version`` on the embedding tables).
"""

from __future__ import annotations

import re
from enum import StrEnum
from typing import ClassVar, Final

from pydantic import BaseModel, ConfigDict, field_validator

EMBEDDING_SCHEMA_VERSION: Final[int] = 1
"""Format version of ``to_text()``. Stored per row; mismatched rows are stale."""

_WHITESPACE = re.compile(r"\s+")


class SeniorityBand(StrEnum):
    """Coarse seniority level. Bands, never years — years of experience are an age proxy."""

    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    STAFF = "staff"
    PRINCIPAL = "principal"
    EXECUTIVE = "executive"


class TenureBand(StrEnum):
    """How long a role was held, coarsely. Bands, never dates."""

    UNDER_1_YEAR = "under_1_year"
    ONE_TO_3_YEARS = "1_to_3_years"
    THREE_TO_6_YEARS = "3_to_6_years"
    OVER_6_YEARS = "over_6_years"


def _normalize_text(value: str) -> str:
    """Collapse all whitespace (including newlines) so line-based formatting is stable."""
    return _WHITESPACE.sub(" ", value).strip()


def _normalize_set(values: tuple[str, ...]) -> tuple[str, ...]:
    """Normalize, drop empties, de-duplicate case-insensitively, and sort.

    Used for fields where order carries no meaning (skills, target roles, ...) so that
    two Profiles listing the same skills in a different order embed identically.
    """
    seen: dict[str, str] = {}
    for raw in values:
        text = _normalize_text(raw)
        if text:
            seen.setdefault(text.casefold(), text)
    return tuple(seen[key] for key in sorted(seen))


class _StrictModel(BaseModel):
    """Shared config: immutable, and unknown fields are an error, not ignored."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)


class _EmbeddingDoc(_StrictModel):
    """A top-level document with a canonical ``to_text()``."""

    DOC_KIND: ClassVar[str]

    def to_text(self) -> str:
        """Deterministic serialization of this doc, tagged with the schema version."""
        header = f"[hunterseeker {self.DOC_KIND} embedding schema v{EMBEDDING_SCHEMA_VERSION}]"
        return "\n".join([header, *self._text_lines()])

    def _text_lines(self) -> list[str]:
        raise NotImplementedError


class RoleHistoryEntry(_StrictModel):
    """One past or current role. No employer name, no dates."""

    title: str
    seniority_band: SeniorityBand
    responsibilities_summary: str
    tenure_band: TenureBand

    @field_validator("title", "responsibilities_summary")
    @classmethod
    def _collapse_whitespace(cls, value: str) -> str:
        return _normalize_text(value)

    def _text_line(self) -> str:
        return (
            f"- title: {self.title} | seniority: {self.seniority_band} "
            f"| tenure: {self.tenure_band} | responsibilities: {self.responsibilities_summary}"
        )


class SeekerProfileEmbeddingDoc(_EmbeddingDoc):
    """What may be embedded from a Seeker's Profile.

    Deliberately absent (AGENTS.md §9): name, photo, email/phone/links, date of birth or
    age, any date or year, graduation year, school or employer names, ZIP/city/address.
    Deliberately absent (AGENTS.md §6, filter columns instead): location, remote policy,
    compensation floor, work authorization.
    """

    DOC_KIND: ClassVar[str] = "seeker_profile"

    skills: tuple[str, ...] = ()
    role_history: tuple[RoleHistoryEntry, ...] = ()
    """Most recent first. Order is meaningful and preserved."""
    target_roles: tuple[str, ...] = ()
    target_industries: tuple[str, ...] = ()
    work_style_preferences: tuple[str, ...] = ()
    self_summary: str = ""

    @field_validator("skills", "target_roles", "target_industries", "work_style_preferences")
    @classmethod
    def _normalize_sets(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return _normalize_set(value)

    @field_validator("self_summary")
    @classmethod
    def _collapse_whitespace(cls, value: str) -> str:
        return _normalize_text(value)

    def _text_lines(self) -> list[str]:
        return [
            f"skills: {'; '.join(self.skills)}",
            "role history:",
            *(role._text_line() for role in self.role_history),
            f"target roles: {'; '.join(self.target_roles)}",
            f"target industries: {'; '.join(self.target_industries)}",
            f"work style preferences: {'; '.join(self.work_style_preferences)}",
            f"summary: {self.self_summary}",
        ]


class JobEmbeddingDoc(_EmbeddingDoc):
    """What may be embedded from a Job listing.

    Deliberately absent (AGENTS.md §6, filter columns instead): compensation, location,
    remote policy, work authorization / sponsorship. Also absent: company name and
    anything else that is branding rather than the work itself.
    """

    DOC_KIND: ClassVar[str] = "job"

    title: str
    team_summary: str = ""
    """What the team / domain does — not the company's name or marketing."""
    responsibilities: tuple[str, ...] = ()
    """Order is meaningful (Hunters list the important ones first) and preserved."""
    required_skills: tuple[str, ...] = ()
    nice_to_have_skills: tuple[str, ...] = ()
    seniority_band: SeniorityBand

    @field_validator("required_skills", "nice_to_have_skills")
    @classmethod
    def _normalize_sets(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return _normalize_set(value)

    @field_validator("responsibilities")
    @classmethod
    def _normalize_list(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(text for text in (_normalize_text(item) for item in value) if text)

    @field_validator("title", "team_summary")
    @classmethod
    def _collapse_whitespace(cls, value: str) -> str:
        return _normalize_text(value)

    def _text_lines(self) -> list[str]:
        return [
            f"title: {self.title}",
            f"seniority: {self.seniority_band}",
            f"team: {self.team_summary}",
            "responsibilities:",
            *(f"- {item}" for item in self.responsibilities),
            f"required skills: {'; '.join(self.required_skills)}",
            f"nice to have skills: {'; '.join(self.nice_to_have_skills)}",
        ]
