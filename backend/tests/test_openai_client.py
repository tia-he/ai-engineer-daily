import json
from types import SimpleNamespace

import openai_client
from openai_client import select_top_stories, synthesize_article


def fake_client(content: dict):
    """A stand-in OpenAI client whose chat.completions.create() always
    returns the given dict, JSON-encoded, in the shape the real SDK uses."""

    def create(**_kwargs):
        message = SimpleNamespace(content=json.dumps(content))
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    return SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )


def broken_client():
    """A stand-in client whose chat.completions.create() raises — the
    per-call failure mode select_top_stories/synthesize_article catch and
    turn into None, as opposed to _get_client() itself raising (a missing
    API key), which is meant to crash the whole run instead of being
    swallowed one story at a time."""

    def create(**_kwargs):
        raise RuntimeError("boom")

    return SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )


CANDIDATES = [
    {"title": "OpenAI ships X", "content": "...", "source_name": "OpenAI"},
    {"title": "Google ships Y", "content": "...", "source_name": "Google AI"},
]


def test_select_top_stories_returns_valid_selections(monkeypatch):
    monkeypatch.setattr(
        openai_client,
        "_get_client",
        lambda: fake_client({"stories": [{"title": "X", "indices": [0]}]}),
    )

    result = select_top_stories(CANDIDATES, max_stories=5)

    assert result == [{"title": "X", "indices": [0]}]


def test_select_top_stories_drops_out_of_range_indices(monkeypatch):
    monkeypatch.setattr(
        openai_client,
        "_get_client",
        lambda: fake_client(
            {
                "stories": [
                    {"title": "Valid", "indices": [0]},
                    {"title": "Bad", "indices": [99]},
                ]
            }
        ),
    )

    result = select_top_stories(CANDIDATES, max_stories=5)

    assert result == [{"title": "Valid", "indices": [0]}]


def test_select_top_stories_truncates_to_max_stories(monkeypatch):
    monkeypatch.setattr(
        openai_client,
        "_get_client",
        lambda: fake_client(
            {
                "stories": [
                    {"title": "A", "indices": [0]},
                    {"title": "B", "indices": [1]},
                    {"title": "C", "indices": [0]},
                ]
            }
        ),
    )

    result = select_top_stories(CANDIDATES, max_stories=2)

    assert len(result) == 2


def test_select_top_stories_returns_none_on_failure(monkeypatch):
    monkeypatch.setattr(openai_client, "_get_client", broken_client)

    assert select_top_stories(CANDIDATES, max_stories=5) is None


def test_synthesize_article_returns_expected_shape(monkeypatch):
    monkeypatch.setattr(
        openai_client,
        "_get_client",
        lambda: fake_client(
            {
                "title": "Merged",
                "summary": "S",
                "content": "C",
                "takeaway": "TK",
                "concepts": ["A", "B"],
                "background": "BG",
            }
        ),
    )

    result = synthesize_article(
        [{"title": "T", "content": "C", "source_name": "OpenAI"}]
    )

    assert result == {
        "title": "Merged",
        "summary": "S",
        "content": "C",
        "takeaway": "TK",
        "concepts": ["A", "B"],
        "background": "BG",
    }


def test_synthesize_article_returns_none_on_failure(monkeypatch):
    monkeypatch.setattr(openai_client, "_get_client", broken_client)

    assert (
        synthesize_article([{"title": "T", "content": "C", "source_name": "X"}]) is None
    )


def test_synthesize_article_rejects_a_blank_field(monkeypatch):
    monkeypatch.setattr(
        openai_client,
        "_get_client",
        lambda: fake_client(
            {
                "title": "Merged",
                "summary": "S",
                "content": "",
                "takeaway": "TK",
                "concepts": ["A"],
                "background": "BG",
            }
        ),
    )

    result = synthesize_article([{"title": "T", "content": "C", "source_name": "X"}])

    assert result is None


def test_synthesize_article_rejects_empty_concepts(monkeypatch):
    monkeypatch.setattr(
        openai_client,
        "_get_client",
        lambda: fake_client(
            {
                "title": "Merged",
                "summary": "S",
                "content": "C",
                "takeaway": "TK",
                "concepts": [],
                "background": "BG",
            }
        ),
    )

    result = synthesize_article([{"title": "T", "content": "C", "source_name": "X"}])

    assert result is None
