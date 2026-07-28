import json
import logging
import os

from openai import OpenAI

from config import OPENAI_MODEL

logger = logging.getLogger(__name__)

_client: OpenAI | None = None

SELECTION_SYSTEM_PROMPT = (
    "You are an editor picking today's AI Engineer Daily brief for a "
    "software engineer audience. You'll get a numbered list of "
    "candidate stories scraped today from AI company blogs. Group any "
    "candidates that cover the same real-world story (for example, "
    "multiple companies announcing the same shared standard, or the "
    "same event reported by more than one source) into a single story; "
    "most days most stories will be their own group of one. Then pick "
    "at most {max_stories} of the most significant stories for this "
    "audience, ordered most important first. It is fine to pick fewer "
    "than {max_stories} if that's all that genuinely matters today — "
    "do not pad the list with minor stories just to fill it. Respond "
    'with a JSON object: {{"stories": [{{"title": "...", '
    '"indices": [0, 2]}}, ...]}}, where each "indices" list references '
    "positions in the input list. Respond with JSON only."
)

SYNTHESIS_SYSTEM_PROMPT = (
    "You are writing one article for AI Engineer Daily, a briefing for "
    "software engineers on AI industry news. You will get one or more "
    "source excerpts about the same story: each has a source name, a "
    "title, and a body. If there is more than one source, combine "
    "them — keep every distinct, valuable detail, and drop only exact "
    "repetition. None of the output fields may be empty, even when a "
    "source body is just one or two sentences — write as much as that "
    "material honestly supports, never less than a real sentence per "
    "field. Respond with a JSON object with exactly these keys: "
    '"title" (a clear headline), "summary" (a 1-2 sentence teaser), '
    '"content" (the article body: restate the source material as a '
    "normal piece of prose — do not pad or invent detail beyond it, "
    'but never leave it blank), "takeaway" (1-2 sentences on why this '
    "matters to a software engineer — you may add reasonable editorial "
    'interpretation here), "background" (1-3 sentences of context a '
    "reader may need — you may draw on your own general knowledge of "
    "the field for this one, even if the sources do not spell it out), "
    'and "concepts" (a list of 2-5 short technical concept names). '
    "Respond with JSON only."
)


def _get_client() -> OpenAI:
    """
    延迟创建 OpenAI 客户端，第一次调用时才检查 API key 是否存在。
    """
    global _client

    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

        _client = OpenAI(api_key=api_key)

    return _client


def select_top_stories(candidates: list[dict], max_stories: int) -> list[dict] | None:
    """
    把当天抓到的候选故事分组（同一事件的多方报道归为一组）并挑出
    最多 max_stories 组最重要的，按重要性排序。

    candidates 里每项需要 title/content/source_name。返回值里每项是
    {"title": ..., "indices": [...]}，indices 是 candidates 的下标。

    调用失败（网络、解析）时返回 None；调用成功但合理地一个都没选中
    时返回空列表——这两种情况对调用方的含义不同，不能混为一谈。
    """
    client = _get_client()

    listing = "\n".join(
        f"{i}. [{c['source_name']}] {c['title']}: {c['content'][:300]}"
        for i, c in enumerate(candidates)
    )

    prompt = SELECTION_SYSTEM_PROMPT.format(max_stories=max_stories)

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": listing},
            ],
        )

        data = json.loads(response.choices[0].message.content)
        stories = data["stories"][:max_stories]

        return [
            story
            for story in stories
            if isinstance(story.get("indices"), list)
            and story["indices"]
            and all(0 <= i < len(candidates) for i in story["indices"])
        ]
    except Exception:
        logger.exception("Story selection failed")
        return None


def synthesize_article(entries: list[dict]) -> dict | None:
    """
    把同一个故事的一到多篇来源原文合成一篇完整文章。

    entries 里每项需要 title/content/source_name。返回 title/summary/
    content/takeaway/concepts/background，失败时返回 None。
    """
    client = _get_client()

    sources_text = "\n\n".join(
        f"Source: {e['source_name']}\nTitle: {e['title']}\nBody: {e['content']}"
        for e in entries
    )

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
                {"role": "user", "content": sources_text},
            ],
        )

        data = json.loads(response.choices[0].message.content)

        result = {
            "title": data["title"],
            "summary": data["summary"],
            "content": data["content"],
            "takeaway": data["takeaway"],
            "concepts": data["concepts"],
            "background": data["background"],
        }

        # A response that's valid JSON but leaves a required field blank
        # is still a failure — publishing it would put an empty section
        # on the page, which is worse than not publishing that story today.
        text_fields = ("title", "summary", "content", "takeaway", "background")
        if (
            any(not result[field].strip() for field in text_fields)
            or not result["concepts"]
        ):
            logger.warning("Synthesis returned an empty field, discarding: %s", result)
            return None

        return result
    except Exception:
        logger.exception("Article synthesis failed")
        return None
