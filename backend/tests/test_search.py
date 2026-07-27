from crud import create_article


def make_article(article_id, **overrides):
    base = {
        "id": article_id,
        "title": "Default Title",
        "summary": "Default summary.",
        "content": "Default content.",
        "takeaway": "Default takeaway.",
        "concepts": ["LLM"],
        "background": "",
        "related_news": [],
        "sources": [],
    }
    base.update(overrides)
    return base


def test_search_matches_title(client, db_session):
    create_article(db_session, make_article("a1", title="OpenAI Ships GPT-5"))
    create_article(db_session, make_article("a2", title="Totally Unrelated"))

    response = client.get("/search", params={"q": "gpt-5"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == "a1"
    assert body[0]["matchedIn"] == ["Title"]


def test_search_matches_concepts(client, db_session):
    create_article(db_session, make_article("a1", concepts=["Vector Search"]))

    response = client.get("/search", params={"q": "vector"})

    body = response.json()
    assert len(body) == 1
    assert "Concepts" in body[0]["matchedIn"]


def test_search_matches_multiple_fields(client, db_session):
    create_article(
        db_session,
        make_article(
            "a1",
            title="Agents",
            summary="talks about agents",
            takeaway="agents matter",
        ),
    )

    response = client.get("/search", params={"q": "agents"})

    body = response.json()
    assert sorted(body[0]["matchedIn"]) == ["Summary", "Takeaway", "Title"]


def test_search_is_case_insensitive(client, db_session):
    create_article(db_session, make_article("a1", title="MCP SDK"))

    response = client.get("/search", params={"q": "mcp"})

    assert len(response.json()) == 1


def test_search_no_match_returns_empty_list(client, db_session):
    create_article(db_session, make_article("a1", title="Something"))

    response = client.get("/search", params={"q": "zzz-no-match"})

    assert response.status_code == 200
    assert response.json() == []


def test_search_background_is_not_searched(client, db_session):
    create_article(db_session, make_article("a1", background="unique-background-term"))

    response = client.get("/search", params={"q": "unique-background-term"})

    assert response.json() == []
