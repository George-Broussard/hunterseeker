"""Messaging stub: conversation list for the rail and the quick-reply send."""

from httpx import AsyncClient

CONVERSATION_ID = "00000000-0000-4000-8000-000000007001"


async def test_conversations_carry_unread_counts_and_snippets(client: AsyncClient) -> None:
    items = (await client.get("/api/v1/messaging/conversations")).json()["items"]

    assert len(items) >= 2
    assert any(c["unread_count"] > 0 for c in items)
    for conversation in items:
        assert len(conversation["participants"]) >= 2
        assert conversation["last_message"]["body"]


async def test_send_message_returns_the_message(client: AsyncClient) -> None:
    response = await client.post(
        f"/api/v1/messaging/conversations/{CONVERSATION_ID}/messages", json={"body": "On my way."}
    )

    assert response.status_code == 201, response.text
    message = response.json()
    assert message["conversation_id"] == CONVERSATION_ID
    assert message["body"] == "On my way."


async def test_send_message_to_unknown_conversation_is_404(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/messaging/conversations/00000000-0000-4000-8000-0000000000ff/messages",
        json={"body": "hello?"},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
