"""The Hunter's company feed stub: cursor paging, posting as a Company Profile."""

from httpx import AsyncClient


async def test_company_feed_pages_through_to_the_end(client: AsyncClient) -> None:
    first = (await client.get("/api/v1/feed/company")).json()
    assert first["items"]
    assert first["next_cursor"] is not None

    second = (
        await client.get("/api/v1/feed/company", params={"cursor": first["next_cursor"]})
    ).json()
    assert second["items"]
    assert second["next_cursor"] is None

    ids = [p["id"] for p in first["items"] + second["items"]]
    assert len(ids) == len(set(ids))


async def test_company_feed_mixes_company_and_network_posts(client: AsyncClient) -> None:
    items = (await client.get("/api/v1/feed/company")).json()["items"]

    assert all(item["kind"] == "post" for item in items)
    assert any(item["company"] is not None for item in items)
    assert any(item["company"] is None for item in items)


async def test_hunter_manages_more_than_one_company_profile(client: AsyncClient) -> None:
    body = (await client.get("/api/v1/feed/company-profiles")).json()

    assert set(body) == {"items", "next_cursor"}
    assert len(body["items"]) >= 2


async def test_create_company_post_returns_the_post_as_that_company(client: AsyncClient) -> None:
    companies = (await client.get("/api/v1/feed/company-profiles")).json()["items"]
    company = companies[1]

    response = await client.post(
        "/api/v1/feed/company/posts",
        json={"company_profile_id": company["id"], "body": "Hello from the company feed."},
    )

    assert response.status_code == 201, response.text
    post = response.json()
    assert post["kind"] == "post"
    assert post["company"] == company
    assert post["author"]["persona"] == "hunter"
    assert post["body"] == "Hello from the company feed."


async def test_create_company_post_rejects_unmanaged_company(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/feed/company/posts",
        json={"company_profile_id": "00000000-0000-4000-8000-0000000000ff", "body": "x"},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


async def test_create_company_post_rejects_empty_body(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/feed/company/posts",
        json={"company_profile_id": "00000000-0000-4000-8000-00000000c001", "body": ""},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
