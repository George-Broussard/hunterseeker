"""The Hunter's open-roles stub honours the no-void invariant from the Hunter side."""

from httpx import AsyncClient


async def test_open_roles_is_cursor_paginated(client: AsyncClient) -> None:
    response = await client.get("/api/v1/matching/open-roles", params={"limit": 5})

    assert response.status_code == 200, response.text
    body = response.json()
    assert set(body) == {"items", "next_cursor"}
    assert body["items"]
    assert body["next_cursor"] is None


async def test_open_role_carries_counts_and_at_most_three_screened_candidates(
    client: AsyncClient,
) -> None:
    roles = (await client.get("/api/v1/matching/open-roles")).json()["items"]

    for role in roles:
        assert role["job"]["title"]
        assert role["new_match_count"] >= 0
        assert set(role["pipeline"]) == {"screened", "interviewing", "offer"}
        assert len(role["top_candidates"]) <= 3
        # Every candidate is a Match, and a Match only exists after an ATS pass.
        assert all(c["ats_pass"] is True for c in role["top_candidates"])
        # Nothing on a candidate reaches a Hunter except the public summary + headline.
        for candidate in role["top_candidates"]:
            assert set(candidate["seeker"]) == {"id", "persona", "display_name"}
        scores = [c["score"] for c in role["top_candidates"]]
        assert scores == sorted(scores, reverse=True)


async def test_top_candidate_is_the_same_match_as_the_ranked_list(client: AsyncClient) -> None:
    role = (await client.get("/api/v1/matching/open-roles")).json()["items"][0]
    job_id = role["job"]["id"]
    ranked = (await client.get(f"/api/v1/matching/jobs/{job_id}/candidates")).json()["items"]

    assert role["top_candidates"][0]["id"] == ranked[0]["id"]
    assert role["top_candidates"][0]["score"] == ranked[0]["score"]
