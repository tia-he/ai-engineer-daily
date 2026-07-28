import calendar
import hashlib
import logging
import re
from datetime import UTC, datetime

import feedparser
from sqlalchemy.orm import Session

import crud
from config import MAX_DAILY_STORIES, RSS_FEEDS
from database import SessionLocal, ensure_schema
from logging_config import configure_logging
from openai_client import select_top_stories, synthesize_article

logger = logging.getLogger(__name__)

IMG_SRC_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)


def make_article_id(key: str) -> str:
    """
    对一个字符串取 MD5 作为文章的稳定 id。单来源故事传入它的 link；
    多来源合并的故事传入所有来源 link 排序后拼接的字符串。
    """
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def parse_published_at(entry) -> datetime | None:
    """
    从 feedparser entry 里取真实发布时间。

    entry.published_parsed 是 feedparser 已经解析好的 UTC struct_time；
    源没有提供发布时间（比如缺 pubDate）时它是 None，这里如实返回
    None，不用抓取时间或今天的日期顶替。
    """
    parsed = entry.get("published_parsed")

    if parsed is None:
        return None

    return datetime.fromtimestamp(calendar.timegm(parsed), tz=UTC)


def parse_image_url(entry) -> str | None:
    """
    尽量从 feed 自带的字段里取一张配图，取不到就返回 None（不用占位图）。

    按 media:thumbnail / media:content / image 类型 enclosure / 摘要 HTML
    里的第一个 <img> 的顺序尝试，覆盖大多数博客类 RSS 的常见写法。
    """
    for thumb in entry.get("media_thumbnail", []):
        if thumb.get("url"):
            return thumb["url"]

    for media in entry.get("media_content", []):
        if media.get("url") and media.get("medium", "image") == "image":
            return media["url"]

    for link in entry.get("links", []):
        if link.get("rel") == "enclosure" and link.get("type", "").startswith("image/"):
            return link.get("href")

    match = IMG_SRC_RE.search(entry.get("summary", ""))

    return match.group(1) if match else None


def get_used_source_urls(db: Session) -> set[str]:
    """
    已经出现在任何一篇已发布文章 sources 里的原始链接。用来过滤候选，
    这样同一篇 RSS 帖子不会一直留在候选池里被反复评估。
    """
    return {
        source["url"] for article in crud.get_news(db) for source in article["sources"]
    }


def fetch_candidates(feed: dict, used_urls: set[str]) -> list[dict]:
    """
    抓取单个 RSS 源，返回尚未被任何已发布文章引用过的候选故事。

    这里只做解析，不写数据库——候选要先经过 select_top_stories 挑选，
    再由 synthesize_article 生成完整内容才会真正入库。
    """
    parsed = feedparser.parse(feed["url"])
    candidates = []

    for entry in parsed.entries:
        link = entry.get("link")

        if not link or link in used_urls:
            continue

        candidates.append(
            {
                "title": entry.get("title", "Untitled"),
                "content": entry.get("summary", ""),
                "source_name": feed["name"],
                "url": link,
                "published_at": parse_published_at(entry),
                "image_url": parse_image_url(entry),
            }
        )

    return candidates


def assemble_article(entries: list[dict], ai_data: dict) -> dict:
    """
    把一组候选故事（一到多个来源）加上 synthesize_article 生成的内容，
    组装成 crud.create_article 需要的字段。
    """
    published_dates = [e["published_at"] for e in entries if e["published_at"]]
    image_url = next((e["image_url"] for e in entries if e["image_url"]), None)
    article_id = make_article_id("|".join(sorted(e["url"] for e in entries)))

    return {
        "id": article_id,
        "title": ai_data["title"],
        "summary": ai_data["summary"],
        "content": ai_data["content"],
        "takeaway": ai_data["takeaway"],
        "concepts": ai_data["concepts"],
        "background": ai_data["background"],
        "related_news": [],
        "sources": [{"name": e["source_name"], "url": e["url"]} for e in entries],
        "published_at": max(published_dates) if published_dates else None,
        "image_url": image_url,
    }


def build_daily_brief() -> None:
    """
    抓取 config.RSS_FEEDS 里所有源尚未被引用过的新故事，挑出当天最多
    MAX_DAILY_STORIES 条最重要的（同一事件的多方报道会先被合并成一
    条），为每条调用 OpenAI 合成完整文章后写入数据库。

    这个脚本作为独立进程运行（不经过 main.py 的 API 启动流程），所以
    自己调用 ensure_schema() 建表/补列，不能假定 API 已经先起过一次。
    """
    ensure_schema()

    with SessionLocal() as db:
        used_urls = get_used_source_urls(db)

        candidates = []
        for feed in RSS_FEEDS:
            found = fetch_candidates(feed, used_urls)
            logger.info("%s: %d new candidate(s)", feed["name"], len(found))
            candidates.extend(found)

        if not candidates:
            logger.info("No new candidate stories today.")
            return

        logger.info("Found %d new candidate stories total.", len(candidates))

        selection = select_top_stories(candidates, max_stories=MAX_DAILY_STORIES)

        if selection is None:
            logger.warning("Story selection failed. Nothing published today.")
            return

        if not selection:
            logger.info("Selection found nothing significant today.")
            return

        published = 0

        for story in selection:
            entries = [candidates[i] for i in story["indices"]]
            ai_data = synthesize_article(entries)

            if ai_data is None:
                logger.warning("Synthesis failed for: %s", story.get("title"))
                continue

            article_data = assemble_article(entries, ai_data)

            if crud.create_article(db, article_data):
                published += 1
                logger.info("Published: %s", article_data["title"])
            else:
                logger.info("Already published: %s", article_data["title"])

    logger.info("-" * 60)
    logger.info("Published %d / %d selected stories.", published, len(selection))


if __name__ == "__main__":
    configure_logging()
    build_daily_brief()
