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


def test_update_ai_metadata_returns_false_for_missing_article(db_session):
    updated = crud.update_ai_metadata(
        db_session,
        "does-not-exist",
        {"summary": "", "takeaway": "", "concepts": [], "background": ""},
    )

    assert updated is False
