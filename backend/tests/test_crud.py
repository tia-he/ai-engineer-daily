from datetime import UTC, datetime

import crud

ARTICLE = {
    "id": "crud-1",
    "title": "Title",
    "summary": "Summary",
    "content": "Content",
    "takeaway": "",
    "concepts": [],
    "background": "",
    "related_news": [],
    "sources": [],
}


def test_create_article_returns_true_when_new(db_session):
    created = crud.create_article(db_session, ARTICLE)

    assert created is True


def test_create_article_returns_false_on_duplicate_id(db_session):
    crud.create_article(db_session, ARTICLE)
    created_again = crud.create_article(db_session, ARTICLE)

    assert created_again is False


def test_to_dict_serializes_published_at_and_image_url(db_session):
    crud.create_article(
        db_session,
        {
            **ARTICLE,
            "id": "with-media",
            "published_at": datetime(2026, 7, 27, tzinfo=UTC),
            "image_url": "https://example.com/cover.jpg",
        },
    )

    article = crud.get_article(db_session, "with-media")

    # Postgres round-trips the timezone (`...+00:00`); SQLite doesn't carry
    # tzinfo through DateTime(timezone=True), so only the naive prefix is
    # asserted here to stay valid under either backend.
    assert article["publishedAt"].startswith("2026-07-27T00:00:00")
    assert article["imageUrl"] == "https://example.com/cover.jpg"


def test_to_dict_leaves_published_at_and_image_url_none_when_absent(db_session):
    crud.create_article(db_session, {**ARTICLE, "id": "no-media"})

    article = crud.get_article(db_session, "no-media")

    assert article["publishedAt"] is None
    assert article["imageUrl"] is None


def test_get_recent_news_orders_by_created_at_not_published_at(db_session):
    # Deliberately inverted: the article with the *earliest* published_at
    # (the source blog's own date) is the one our pipeline generated most
    # recently, and should still show up first on the homepage.
    crud.create_article(
        db_session,
        {
            **ARTICLE,
            "id": "old-source-new-brief",
            "published_at": datetime(2020, 1, 1, tzinfo=UTC),
            "created_at": datetime(2026, 7, 28, tzinfo=UTC),
        },
    )
    crud.create_article(
        db_session,
        {
            **ARTICLE,
            "id": "new-source-old-brief",
            "published_at": datetime(2026, 7, 28, tzinfo=UTC),
            "created_at": datetime(2026, 1, 1, tzinfo=UTC),
        },
    )

    recent = crud.get_recent_news(db_session, limit=10)

    assert [a["id"] for a in recent] == ["old-source-new-brief", "new-source-old-brief"]


def test_get_recent_news_respects_limit(db_session):
    for i in range(5):
        crud.create_article(db_session, {**ARTICLE, "id": f"a{i}"})

    recent = crud.get_recent_news(db_session, limit=2)

    assert len(recent) == 2


def test_get_news_is_not_limited(db_session):
    for i in range(5):
        crud.create_article(db_session, {**ARTICLE, "id": f"b{i}"})

    assert len(crud.get_news(db_session)) == 5
