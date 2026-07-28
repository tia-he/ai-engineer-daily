import time
from datetime import UTC, datetime

import crud
import ingest_rss
from ingest_rss import (
    assemble_article,
    build_daily_brief,
    extract_body,
    fetch_candidates,
    get_used_source_urls,
    parse_image_url,
    parse_published_at,
)


def test_parse_published_at_returns_none_without_pubdate():
    assert parse_published_at({}) is None


def test_parse_published_at_converts_struct_time_to_utc():
    struct = time.struct_time((2026, 7, 27, 12, 0, 0, 0, 0, 0))

    result = parse_published_at({"published_parsed": struct})

    assert result == datetime(2026, 7, 27, 12, 0, 0, tzinfo=UTC)


def test_parse_image_url_returns_none_without_any_image():
    assert parse_image_url({"summary": "<p>No image here.</p>"}) is None


def test_parse_image_url_prefers_media_thumbnail():
    entry = {
        "media_thumbnail": [{"url": "https://example.com/thumb.jpg"}],
        "media_content": [{"url": "https://example.com/content.jpg"}],
    }

    assert parse_image_url(entry) == "https://example.com/thumb.jpg"

    entry = {
        "media_content": [{"url": "https://example.com/content.jpg"}],
    }

    assert parse_image_url(entry) == "https://example.com/content.jpg"


def test_parse_image_url_falls_back_to_image_enclosure():
    entry = {
        "links": [
            {"rel": "alternate", "type": "text/html", "href": "https://example.com"},
            {
                "rel": "enclosure",
                "type": "image/png",
                "href": "https://example.com/cover.png",
            },
        ],
    }

    assert parse_image_url(entry) == "https://example.com/cover.png"


def test_parse_image_url_falls_back_to_img_tag_in_summary():
    entry = {
        "summary": '<p>Intro</p><img src="https://example.com/inline.jpg" alt="">',
    }

    assert parse_image_url(entry) == "https://example.com/inline.jpg"


def test_extract_body_prefers_full_content_over_summary():
    entry = {
        "summary": "A one-line teaser.",
        "content": [{"value": "The full multi-paragraph post body."}],
    }

    assert extract_body(entry) == "The full multi-paragraph post body."


def test_extract_body_falls_back_to_summary_when_no_content():
    entry = {"summary": "A one-line teaser."}

    assert extract_body(entry) == "A one-line teaser."


def test_extract_body_falls_back_to_summary_when_content_is_blank():
    entry = {"summary": "A one-line teaser.", "content": [{"value": "   "}]}

    assert extract_body(entry) == "A one-line teaser."


def test_get_used_source_urls_collects_every_source_across_articles(db_session):
    crud.create_article(
        db_session,
        {
            "id": "a1",
            "title": "T1",
            "summary": "S1",
            "content": "C1",
            "takeaway": "TK1",
            "concepts": [],
            "background": "",
            "related_news": [],
            "sources": [
                {"name": "OpenAI", "url": "https://openai.com/a"},
                {"name": "The Verge", "url": "https://theverge.com/a"},
            ],
        },
    )

    assert get_used_source_urls(db_session) == {
        "https://openai.com/a",
        "https://theverge.com/a",
    }


def test_fetch_candidates_skips_entries_without_a_link(monkeypatch):
    class FakeParsed:
        entries = [{"title": "No link"}]

    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: FakeParsed())

    candidates = fetch_candidates(
        {"name": "OpenAI", "url": "https://x"}, used_urls=set()
    )

    assert candidates == []


def test_fetch_candidates_skips_already_used_urls(monkeypatch):
    class FakeParsed:
        entries = [
            {"title": "Seen", "link": "https://openai.com/seen", "summary": "s"},
            {"title": "New", "link": "https://openai.com/new", "summary": "s"},
        ]

    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: FakeParsed())

    candidates = fetch_candidates(
        {"name": "OpenAI", "url": "https://x"},
        used_urls={"https://openai.com/seen"},
    )

    assert [c["url"] for c in candidates] == ["https://openai.com/new"]
    assert candidates[0]["source_name"] == "OpenAI"


def test_assemble_article_combines_multiple_sources():
    entries = [
        {
            "title": "OpenAI post",
            "content": "...",
            "source_name": "OpenAI",
            "url": "https://openai.com/a",
            "published_at": datetime(2026, 7, 20, tzinfo=UTC),
            "image_url": None,
        },
        {
            "title": "Google post",
            "content": "...",
            "source_name": "Google AI",
            "url": "https://blog.google/a",
            "published_at": datetime(2026, 7, 27, tzinfo=UTC),
            "image_url": "https://blog.google/a.jpg",
        },
    ]
    ai_data = {
        "title": "Merged title",
        "summary": "Merged summary",
        "content": "Merged content",
        "takeaway": "Merged takeaway",
        "concepts": ["MCP"],
        "background": "Merged background",
    }

    article = assemble_article(entries, ai_data)

    assert article["title"] == "Merged title"
    assert article["sources"] == [
        {"name": "OpenAI", "url": "https://openai.com/a"},
        {"name": "Google AI", "url": "https://blog.google/a"},
    ]
    # The later of the two publish dates, and the one image the entries had.
    assert article["published_at"] == datetime(2026, 7, 27, tzinfo=UTC)
    assert article["image_url"] == "https://blog.google/a.jpg"


def test_assemble_article_id_is_stable_regardless_of_entry_order():
    entries_a = [
        {
            "title": "A",
            "content": "",
            "source_name": "OpenAI",
            "url": "https://openai.com/a",
            "published_at": None,
            "image_url": None,
        },
        {
            "title": "B",
            "content": "",
            "source_name": "Google AI",
            "url": "https://blog.google/a",
            "published_at": None,
            "image_url": None,
        },
    ]
    entries_b = list(reversed(entries_a))
    ai_data = {
        "title": "T",
        "summary": "S",
        "content": "C",
        "takeaway": "TK",
        "concepts": [],
        "background": "",
    }

    assert (
        assemble_article(entries_a, ai_data)["id"]
        == assemble_article(entries_b, ai_data)["id"]
    )


def test_build_daily_brief_publishes_selected_stories(db_session, monkeypatch):
    class FakeParsed:
        def __init__(self, entries):
            self.entries = entries

    feeds_by_url = {
        "https://openai.com/rss": FakeParsed(
            [{"title": "OpenAI story", "link": "https://openai.com/a", "summary": "s"}]
        ),
    }

    monkeypatch.setattr(
        ingest_rss, "RSS_FEEDS", [{"name": "OpenAI", "url": "https://openai.com/rss"}]
    )
    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: feeds_by_url[url])
    monkeypatch.setattr(
        ingest_rss,
        "select_top_stories",
        lambda candidates, max_stories: [{"title": "x", "indices": [0]}],
    )
    monkeypatch.setattr(
        ingest_rss,
        "synthesize_article",
        lambda entries: {
            "title": "Synthesized",
            "summary": "Summary",
            "content": "Content",
            "takeaway": "Takeaway",
            "concepts": ["A"],
            "background": "Background",
        },
    )
    monkeypatch.setattr(ingest_rss, "SessionLocal", lambda: db_session)
    monkeypatch.setattr(db_session, "close", lambda: None)
    monkeypatch.setattr(ingest_rss, "ensure_schema", lambda: None)

    build_daily_brief()

    articles = crud.get_news(db_session)
    assert len(articles) == 1
    assert articles[0]["title"] == "Synthesized"
    assert articles[0]["sources"] == [{"name": "OpenAI", "url": "https://openai.com/a"}]


def test_build_daily_brief_does_nothing_when_selection_fails(db_session, monkeypatch):
    class FakeParsed:
        entries = [{"title": "Story", "link": "https://openai.com/a", "summary": "s"}]

    monkeypatch.setattr(
        ingest_rss, "RSS_FEEDS", [{"name": "OpenAI", "url": "https://openai.com/rss"}]
    )
    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: FakeParsed())
    monkeypatch.setattr(
        ingest_rss, "select_top_stories", lambda candidates, max_stories: None
    )
    monkeypatch.setattr(ingest_rss, "SessionLocal", lambda: db_session)
    monkeypatch.setattr(db_session, "close", lambda: None)
    monkeypatch.setattr(ingest_rss, "ensure_schema", lambda: None)

    build_daily_brief()

    assert crud.get_news(db_session) == []
