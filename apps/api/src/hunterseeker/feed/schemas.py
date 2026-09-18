"""API contract for the Feed: matched jobs interleaved with posts from the network.

A Feed item is a tagged union on ``kind``. The Job Board (matching domain) is the
matches-only surface; the Feed is the only place posts and Matches mix.
"""

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from hunterseeker.core.schemas import UserSummary
from hunterseeker.matching.schemas import MatchedJob


class CompanyProfileSummary(BaseModel):
    """A Company Profile as referenced from a post.

    Lives in the feed contract until a Company Profile domain exists; see the follow-up
    issue on Company Profile management.
    """

    id: UUID
    name: str


class Post(BaseModel):
    kind: Literal["post"] = "post"
    id: UUID
    author: UserSummary
    company: CompanyProfileSummary | None = Field(
        default=None,
        description=(
            "Set when a Hunter posted *as* a Company Profile they manage; `author` is then "
            "that Hunter. Null for a post made as oneself."
        ),
    )
    body: str = Field(max_length=5000)
    created_at: datetime


class CompanyPostCreate(BaseModel):
    """Body for posting to the company feed as a Company Profile."""

    company_profile_id: UUID = Field(
        description="The Company Profile to post as. The caller must manage it."
    )
    body: str = Field(min_length=1, max_length=5000)


class MatchedJobItem(BaseModel):
    kind: Literal["matched_job"] = "matched_job"
    id: UUID = Field(description="Feed item id, distinct from `match.id`.")
    match: MatchedJob
    created_at: datetime = Field(description="When the Match entered the Feed.")


type FeedItem = Annotated[Post | MatchedJobItem, Field(discriminator="kind")]
