import time
from datetime import UTC, datetime

from ingest_rss import parse_image_url, parse_published_at


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
