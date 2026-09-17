"""Cursor pagination — the convention for every list endpoint.

Request: ``?cursor=<opaque>&limit=<1..100>``. Response: a :class:`Page` whose
``next_cursor`` is ``null`` on the last page. Cursors are opaque strings; clients must
not construct or decode them. Cursor (not offset) pagination is used because the Feed
and Job Board are append-heavy, continuously re-ranked lists where offsets skip or
repeat items between requests.
"""

from pydantic import BaseModel, Field

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


class CursorQuery(BaseModel):
    """Query parameters accepted by every list endpoint.

    Use as ``params: Annotated[CursorQuery, Query()]`` so FastAPI reads it from the
    query string and documents both fields.
    """

    cursor: str | None = Field(
        default=None,
        description="Opaque cursor from a previous page's `next_cursor`. Omit for the first page.",
    )
    limit: int = Field(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description=f"Page size, 1-{MAX_LIMIT}.",
    )


class Page[ItemT](BaseModel):
    """One page of a cursor-paginated list."""

    items: list[ItemT]
    next_cursor: str | None = Field(
        default=None,
        description="Pass as `cursor` to fetch the next page. `null` on the last page.",
    )
