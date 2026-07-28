import calendar
import hashlib
import logging
import re
from datetime import UTC, datetime

import feedparser
from sqlalchemy.orm import Session

import crud
from config import RSS_FEEDS
from database import SessionLocal
from logging_config import configure_logging

logger = logging.getLogger(__name__)

IMG_SRC_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)


def make_article_id(link: str) -> str:
    """
    使用 entry.link 的 MD5 哈希值作为文章的稳定 id。
    """
    return hashlib.md5(link.encode("utf-8")).hexdigest()


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


def parse_entry(feed_name: str, entry) -> dict | None:
    """
    把 feedparser 的 entry 转换成 crud.create_article 需要的字段。

    AI 相关字段（takeaway/concepts/background/related_news）暂时留空，
    等待未来的 OpenAI summarization 环节填充。
    """
    link = entry.get("link")

    if not link:
        return None

    summary = entry.get("summary", "")

    return {
        "id": make_article_id(link),
        "title": entry.get("title", "Untitled"),
        "summary": summary,
        "content": summary,
        "takeaway": "",
        "concepts": [],
        "background": "",
        "related_news": [],
        "sources": [
            {
                "name": feed_name,
                "url": link,
            }
        ],
        "published_at": parse_published_at(entry),
        "image_url": parse_image_url(entry),
    }


def ingest_feed(db: Session, feed: dict) -> tuple[int, int]:
    """
    抓取单个 RSS 源，返回 (新增数量, 跳过数量)。
    """
    parsed = feedparser.parse(feed["url"])

    inserted = 0
    skipped = 0

    for entry in parsed.entries:
        article_data = parse_entry(feed["name"], entry)

        if article_data is None:
            continue

        created = crud.create_article(db, article_data)

        if created:
            inserted += 1
        else:
            skipped += 1

    return inserted, skipped


def ingest_all_feeds() -> None:
    """
    抓取 config.RSS_FEEDS 中的所有 RSS 源，写入数据库。
    已存在的文章（相同 id）会被跳过，不会重复插入。

    表结构由 main.py 启动时的 Base.metadata.create_all() 创建；这里假定
    表已经存在（先起过一次 API，或在此之前跑过 init_db.py）。
    """
    total_inserted = 0
    total_skipped = 0

    with SessionLocal() as db:
        for feed in RSS_FEEDS:
            inserted, skipped = ingest_feed(db, feed)

            logger.info("%s: inserted %d, skipped %d", feed["name"], inserted, skipped)

            total_inserted += inserted
            total_skipped += skipped

    logger.info("-" * 60)
    logger.info("Total inserted: %d", total_inserted)
    logger.info("Total skipped (duplicates): %d", total_skipped)


if __name__ == "__main__":
    configure_logging()
    ingest_all_feeds()
