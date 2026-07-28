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


def test_get_articles_pending_ai_only_returns_empty_takeaway(db_session):
    crud.create_article(db_session, {**ARTICLE, "id": "pending-1", "takeaway": ""})
    crud.create_article(
        db_session, {**ARTICLE, "id": "done-1", "takeaway": "Has a takeaway"}
    )

    pending = crud.get_articles_pending_ai(db_session, limit=10)

    ids = [article["id"] for article in pending]
    assert "pending-1" in ids
    assert "done-1" not in ids


def test_get_articles_pending_ai_respects_limit(db_session):
    for i in range(5):
        crud.create_article(
            db_session, {**ARTICLE, "id": f"pending-{i}", "takeaway": ""}
        )

    pending = crud.get_articles_pending_ai(db_session, limit=2)

    assert len(pending) == 2


def test_update_ai_metadata_writes_all_fields(db_session):
    crud.create_article(db_session, {**ARTICLE, "id": "update-1", "takeaway": ""})

    updated = crud.update_ai_metadata(
        db_session,
        "update-1",
        {
            "summary": "New summary",
            "takeaway": "New takeaway",
            "concepts": ["A", "B"],
            "background": "New background",
        },
    )

    assert updated is True
    article = crud.get_article(db_session, "update-1")
    assert article["summary"] == "New summary"
    assert article["takeaway"] == "New takeaway"
    assert article["concepts"] == ["A", "B"]
    assert article["background"] == "New background"


def test_get_articles_pending_ai_orders_newest_first_with_nulls_last(db_session):
    crud.create_article(
        db_session,
        {
            **ARTICLE,
            "id": "no-date",
            "takeaway": "",
            "published_at": None,
        },
    )
    crud.create_article(
        db_session,
        {
            **ARTICLE,
            "id": "older",
            "takeaway": "",
            "published_at": datetime(2026, 1, 1, tzinfo=UTC),
        },
    )
    crud.create_article(
        db_session,
        {
            **ARTICLE,
            "id": "newer",
            "takeaway": "",
            "published_at": datetime(2026, 7, 1, tzinfo=UTC),
        },
    )

    pending = crud.get_articles_pending_ai(db_session, limit=10)

    ids = [article["id"] for article in pending]
    assert ids == ["newer", "older", "no-date"]


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


def test_update_ai_metadata_returns_false_for_missing_article(db_session):
    updated = crud.update_ai_metadata(
        db_session,
        "does-not-exist",
        {"summary": "", "takeaway": "", "concepts": [], "background": ""},
    )

    assert updated is False
