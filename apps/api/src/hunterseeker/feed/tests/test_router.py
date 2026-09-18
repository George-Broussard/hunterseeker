"""Feed stub: server-side interleaving of posts and Matches, plus the post composer stub."""

from httpx import AsyncClient


async def test_feed_interleaves_posts_and_matches_server_side(client: AsyncClient) -> None:
    items = (await client.get("/api/v1/feed")).json()["items"]

    kinds = [item["kind"] for item in items]
    assert "post" in kinds and "matched_job" in kinds
    # The client renders one list; the endpoint owns the ordering.
    assert kinds != sorted(kinds), "stub should interleave, not group by kind"
    for item in items:
        if item["kind"] == "matched_job":
            assert item["match"]["ats_pass"] is True


async def test_create_post_echoes_body_as_a_feed_post(client: AsyncClient) -> None:
    response = await client.post("/api/v1/feed/posts", json={"body": "hello, network"})

    assert response.status_code == 201, response.text
    post = response.json()
    assert post["kind"] == "post"
    assert post["body"] == "hello, network"
    assert post["author"]["persona"] == "seeker"


async def test_create_post_rejects_empty_body(client: AsyncClient) -> None:
    response = await client.post("/api/v1/feed/posts", json={"body": ""})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
