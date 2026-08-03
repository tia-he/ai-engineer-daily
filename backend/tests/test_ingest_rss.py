import time
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import httpx

import crud
import ingest_rss
from ingest_rss import (
    assemble_article,
    build_daily_brief,
    enrich_with_page_text,
    extract_body,
    fetch_candidates,
    fetch_page_text,
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


def test_parse_published_at_falls_back_to_updated_parsed():
    struct = time.struct_time((2026, 7, 28, 9, 0, 0, 0, 0, 0))

    result = parse_published_at({"updated_parsed": struct})

    assert result == datetime(2026, 7, 28, 9, 0, 0, tzinfo=UTC)


def test_parse_published_at_prefers_published_over_updated():
    published = time.struct_time((2026, 7, 27, 12, 0, 0, 0, 0, 0))
    updated = time.struct_time((2026, 7, 28, 9, 0, 0, 0, 0, 0))

    result = parse_published_at(
        {"published_parsed": published, "updated_parsed": updated}
    )

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


def fake_get(html: str):
    """A stand-in for httpx.get() returning a 200 response with the given HTML."""

    def get(url, **kwargs):
        return SimpleNamespace(text=html, raise_for_status=lambda: None)

    return get


def test_fetch_page_text_extracts_article_tag(monkeypatch):
    html = (
        "<html><body><nav>Menu</nav><article>"
        + ("Real content. " * 30)
        + "</article></body></html>"
    )
    monkeypatch.setattr(ingest_rss.httpx, "get", fake_get(html))

    text = fetch_page_text("https://example.com/post")

    assert text is not None
    assert "Real content." in text
    assert "Menu" not in text


def test_fetch_page_text_sends_a_browser_user_agent(monkeypatch):
    captured = {}

    def get(url, **kwargs):
        captured.update(kwargs)
        html = "<article>" + ("Real content. " * 30) + "</article>"
        return SimpleNamespace(text=html, raise_for_status=lambda: None)

    monkeypatch.setattr(ingest_rss.httpx, "get", get)

    fetch_page_text("https://example.com/post")

    assert "Mozilla" in captured["headers"]["User-Agent"]


def test_fetch_page_text_returns_none_when_too_short(monkeypatch):
    html = "<html><body><article>Too short.</article></body></html>"
    monkeypatch.setattr(ingest_rss.httpx, "get", fake_get(html))

    assert fetch_page_text("https://example.com/post") is None


def test_fetch_page_text_returns_none_on_request_failure(monkeypatch):
    def raise_error(url, **kwargs):
        raise httpx.ConnectError("boom")

    monkeypatch.setattr(ingest_rss.httpx, "get", raise_error)

    assert fetch_page_text("https://example.com/post") is None


def test_fetch_page_text_returns_none_on_http_error_status(monkeypatch):
    def get(url, **kwargs):
        request = httpx.Request("GET", url)
        response = httpx.Response(403, request=request)

        def raise_for_status():
            raise httpx.HTTPStatusError("blocked", request=request, response=response)

        return SimpleNamespace(raise_for_status=raise_for_status)

    monkeypatch.setattr(ingest_rss.httpx, "get", get)

    assert fetch_page_text("https://example.com/post") is None


def test_enrich_with_page_text_replaces_content_when_richer(monkeypatch):
    richer_text = "Full page detail. " * 30
    monkeypatch.setattr(ingest_rss, "fetch_page_text", lambda url: richer_text)

    entry = {"url": "https://example.com/post", "content": "Short RSS teaser."}
    result = enrich_with_page_text(entry)

    assert result["content"] == richer_text


def test_enrich_with_page_text_keeps_original_when_fetch_fails(monkeypatch):
    monkeypatch.setattr(ingest_rss, "fetch_page_text", lambda url: None)

    entry = {"url": "https://example.com/post", "content": "Short RSS teaser."}
    result = enrich_with_page_text(entry)

    assert result["content"] == "Short RSS teaser."


def test_enrich_with_page_text_keeps_original_when_page_text_is_shorter(monkeypatch):
    monkeypatch.setattr(ingest_rss, "fetch_page_text", lambda url: "short")

    entry = {
        "url": "https://example.com/post",
        "content": "A much longer RSS-provided teaser than the fetched page text.",
    }
    result = enrich_with_page_text(entry)

    assert result["content"] == entry["content"]


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
    recent = time.gmtime()

    class FakeParsed:
        entries = [
            {
                "title": "Seen",
                "link": "https://openai.com/seen",
                "summary": "s",
                "published_parsed": recent,
            },
            {
                "title": "New",
                "link": "https://openai.com/new",
                "summary": "s",
                "published_parsed": recent,
            },
        ]

    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: FakeParsed())

    candidates = fetch_candidates(
        {"name": "OpenAI", "url": "https://x"},
        used_urls={"https://openai.com/seen"},
    )

    assert [c["url"] for c in candidates] == ["https://openai.com/new"]
    assert candidates[0]["source_name"] == "OpenAI"


def test_fetch_candidates_skips_entries_older_than_the_freshness_window(monkeypatch):
    stale = time.gmtime(
        (
            datetime.now(UTC) - timedelta(days=ingest_rss.CANDIDATE_FRESHNESS_DAYS + 1)
        ).timestamp()
    )

    class FakeParsed:
        entries = [
            {
                "title": "Old backlog post",
                "link": "https://openai.com/old",
                "summary": "s",
                "published_parsed": stale,
            }
        ]

    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: FakeParsed())

    candidates = fetch_candidates(
        {"name": "OpenAI", "url": "https://x"}, used_urls=set()
    )

    assert candidates == []


def test_fetch_candidates_skips_entries_with_no_determinable_date(monkeypatch):
    class FakeParsed:
        entries = [
            {"title": "No date", "link": "https://openai.com/no-date", "summary": "s"}
        ]

    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: FakeParsed())

    candidates = fetch_candidates(
        {"name": "OpenAI", "url": "https://x"}, used_urls=set()
    )

    assert candidates == []


def test_fetch_candidates_keeps_entries_within_the_freshness_window(monkeypatch):
    recent = time.gmtime((datetime.now(UTC) - timedelta(days=1)).timestamp())

    class FakeParsed:
        entries = [
            {
                "title": "Fresh post",
                "link": "https://openai.com/fresh",
                "summary": "s",
                "published_parsed": recent,
            }
        ]

    monkeypatch.setattr(ingest_rss.feedparser, "parse", lambda url: FakeParsed())

    candidates = fetch_candidates(
        {"name": "OpenAI", "url": "https://x"}, used_urls=set()
    )

    assert [c["url"] for c in candidates] == ["https://openai.com/fresh"]


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
            [
                {
                    "title": "OpenAI story",
                    "link": "https://openai.com/a",
                    "summary": "s",
                    "published_parsed": time.gmtime(),
                }
            ]
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
        entries = [
            {
                "title": "Story",
                "link": "https://openai.com/a",
                "summary": "s",
                "published_parsed": time.gmtime(),
            }
        ]

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
