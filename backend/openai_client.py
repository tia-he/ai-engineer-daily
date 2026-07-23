import json
import os

from openai import OpenAI

from config import OPENAI_MODEL

_client: OpenAI | None = None

SYSTEM_PROMPT = (
    "You are an assistant that writes concise briefings for software "
    "engineers about AI industry news. Given an article's title and "
    "content, respond with a JSON object containing exactly these keys: "
    '"summary" (a 1-2 sentence summary), "takeaway" (one sentence on '
    'why this matters to a software engineer), "concepts" (a list of '
    '2-5 short technical concept names), and "background" (1-2 '
    "sentences of context a reader may need). Respond with JSON only."
)


def _get_client() -> OpenAI:
    """
    延迟创建 OpenAI 客户端，第一次调用时才检查 API key 是否存在。
    """
    global _client

    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable is not set."
            )

        _client = OpenAI(api_key=api_key)

    return _client


def generate_article_metadata(title: str, content: str) -> dict | None:
    """
    调用 OpenAI，为一篇文章生成 summary / takeaway / concepts / background。

    如果调用失败，或者返回内容不是预期的 JSON 格式，返回 None，
    由调用方（generate_ai.py）决定如何处理，不影响其他文章的处理。
    """
    client = _get_client()

    user_prompt = f"Title: {title}\n\nContent: {content}"

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        data = json.loads(response.choices[0].message.content)

        return {
            "summary": data["summary"],
            "takeaway": data["takeaway"],
            "concepts": data["concepts"],
            "background": data["background"],
        }
    except Exception as error:
        print(f"OpenAI generation failed for '{title}': {error}")
        return None
