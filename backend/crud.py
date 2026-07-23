from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Article


def get_news(db: Session) -> list[dict]:
    """
    查询全部新闻。
    """
    statement = select(Article)

    articles = db.scalars(statement).all()

    return [article.to_dict() for article in articles]


def get_article(db: Session, article_id: str) -> dict | None:
    """
    根据文章 id 查询一篇新闻。
    """
    statement = select(Article).where(Article.id == article_id)

    article = db.scalar(statement)

    if article is None:
        return None

    return article.to_dict()


def create_article(db: Session, article_data: dict) -> bool:
    """
    插入一篇新文章。

    如果该 id 已存在（例如 RSS 重复抓取到同一篇文章），则跳过并返回 False。
    """
    existing = db.get(Article, article_data["id"])

    if existing is not None:
        return False

    article = Article(**article_data)

    db.add(article)
    db.commit()

    return True