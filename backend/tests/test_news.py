from crud import create_article

ARTICLE = {
    "id": "test-article-1",
    "title": "Test Article",
    "summary": "A short summary.",
    "content": "Full content of the test article.",
    "takeaway": "This is the takeaway.",
    "concepts": ["Testing", "FastAPI"],
    "background": "Some background.",
    "related_news": [],
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


def test_read_article_found(client, db_session):
    create_article(db_session, ARTICLE)

    response = client.get(f"/news/{ARTICLE['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test Article"


def test_read_article_not_found(client):
    response = client.get("/news/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"
