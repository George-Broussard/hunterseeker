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


class Post(BaseModel):
    kind: Literal["post"] = "post"
    id: UUID
    author: UserSummary
    body: str = Field(max_length=5000)
    created_at: datetime


class MatchedJobItem(BaseModel):
    kind: Literal["matched_job"] = "matched_job"
    id: UUID = Field(description="Feed item id, distinct from `match.id`.")
    match: MatchedJob
    created_at: datetime = Field(description="When the Match entered the Feed.")


type FeedItem = Annotated[Post | MatchedJobItem, Field(discriminator="kind")]
