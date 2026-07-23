import crud
from database import SessionLocal
from openai_client import generate_article_metadata


def generate_all() -> None:
    """
    为数据库中尚未生成 AI 元数据的文章调用 OpenAI，
    并把结果通过 CRUD 层写回数据库。

    已经包含 AI 元数据的文章（takeaway 不为空）会被跳过。
    单篇文章调用失败不会中断整个脚本。
    """
    with SessionLocal() as db:
        pending_articles = crud.get_articles_pending_ai(db)

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
    generate_all()
