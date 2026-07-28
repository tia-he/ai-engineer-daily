import argparse
import logging

import crud
from database import SessionLocal
from logging_config import configure_logging
from openai_client import generate_article_metadata

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate AI metadata (summary/takeaway/concepts/background) "
            "for articles that don't have it yet."
        )
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of pending articles to process (default: 100).",
    )

    return parser.parse_args()


def generate_all(limit: int = 100) -> None:
    """
    为数据库中尚未生成 AI 元数据的文章调用 OpenAI，
    并把结果通过 CRUD 层写回数据库。

    已经包含 AI 元数据的文章（takeaway 不为空）会被跳过。
    单篇文章调用失败不会中断整个脚本。

    最多处理 limit 篇文章，按 published_at 降序（见
    crud.get_articles_pending_ai）：没有发布时间的文章排在最后。
    """
    with SessionLocal() as db:
        pending_articles = crud.get_articles_pending_ai(db, limit=limit)

        if not pending_articles:
            logger.info("No pending articles found. Nothing to generate.")
            return

        logger.info("Found %d articles pending AI generation.", len(pending_articles))

        generated = 0
        failed = 0

        for article in pending_articles:
            ai_data = generate_article_metadata(
                title=article["title"],
                content=article["content"],
            )

            if ai_data is None:
                failed += 1
                continue

            crud.update_ai_metadata(db, article["id"], ai_data)
            generated += 1

            logger.info("Generated AI metadata for: %s", article["title"])

    logger.info("-" * 60)
    logger.info("Generated: %d", generated)
    logger.info("Failed: %d", failed)


if __name__ == "__main__":
    configure_logging()
    args = parse_args()
    generate_all(limit=args.limit)
