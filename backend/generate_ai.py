import argparse

import crud
from database import SessionLocal
from openai_client import generate_article_metadata


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

    最多处理 limit 篇文章。注意这不是"最新的 limit 篇"：Article 目前没有
    published_at 字段，而 id 是 md5(link) 哈希值，无法用来判断发布时间的
    新旧，所以这里取到的只是当前待处理文章中的任意一批（见
    crud.get_articles_pending_ai 的说明）。如果未来需要真正按"最近发布"
    处理文章，应该先给 Article 加上 published_at 字段。
    """
    with SessionLocal() as db:
        pending_articles = crud.get_articles_pending_ai(db, limit=limit)

        if not pending_articles:
            print("No pending articles found. Nothing to generate.")
            return

        print(f"Found {len(pending_articles)} articles pending AI generation.")

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

            print(f"Generated AI metadata for: {article['title']}")

    print("-" * 60)
    print(f"Generated: {generated}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    args = parse_args()
    generate_all(limit=args.limit)
