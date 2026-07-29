from config import MAX_DAILY_STORIES
from crud import create_article

ARTICLE = {
    "id": "test-article-1",
    "title": "Test Article",
    "summary": "A short summary.",
    "content": "Full content of the test article.",
    "takeaway": "This is the takeaway.",
    "concepts": ["Testing", "FastAPI"],
    "background": "Some background.",
    "sources": [{"name": "Example", "url": "https://example.com"}],
}


def test_read_news_empty(client):
    response = client.get("/news")

    assert response.status_code == 200
    assert response.json() == []


def test_read_news_returns_seeded_articles(client, db_session):
    create_article(db_session, ARTICLE)

    response = client.get("/news")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == "test-article-1"
    assert body[0]["title"] == "Test Article"


def test_read_news_caps_at_max_daily_stories(client, db_session):
    for i in range(MAX_DAILY_STORIES + 3):
        create_article(db_session, {**ARTICLE, "id": f"article-{i}"})

    response = client.get("/news")

    assert response.status_code == 200
    assert len(response.json()) == MAX_DAILY_STORIES


def test_read_article_found(client, db_session):
    create_article(db_session, ARTICLE)

    response = client.get(f"/news/{ARTICLE['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Article"


def test_read_article_not_found(client):
    response = client.get("/news/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"
