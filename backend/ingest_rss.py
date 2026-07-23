import hashlib

import feedparser
from sqlalchemy.orm import Session

import crud
from config import RSS_FEEDS
from database import Base, SessionLocal, engine


def make_article_id(link: str) -> str:
    """
    使用 entry.link 的 MD5 哈希值作为文章的稳定 id。
    """
    return hashlib.md5(link.encode("utf-8")).hexdigest()


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
    """
    Base.metadata.create_all(bind=engine)

    total_inserted = 0
    total_skipped = 0

    with SessionLocal() as db:
        for feed in RSS_FEEDS:
            inserted, skipped = ingest_feed(db, feed)

            print(f"{feed['name']}: inserted {inserted}, skipped {skipped}")

            total_inserted += inserted
            total_skipped += skipped

    print("-" * 60)
    print(f"Total inserted: {total_inserted}")
    print(f"Total skipped (duplicates): {total_skipped}")


if __name__ == "__main__":
    ingest_all_feeds()
