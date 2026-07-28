from sqlalchemy import String, cast, nulls_last, or_, select
from sqlalchemy.orm import Session

from models import Article


def get_news(db: Session) -> list[dict]:
    """
    查询全部新闻，不做任何数量限制。

    只给 ingest_rss.py 的 get_used_source_urls 用，让它能看到完整历史、
    不会把已经用过的来源当成新故事重新抓一遍。首页请用
    get_recent_news——两者不能共用同一个查询，否则"只显示最近几条"
    会连带破坏"永远不重复处理同一条 RSS"这件事。
    """
    statement = select(Article)

    articles = db.scalars(statement).all()

    return [article.to_dict() for article in articles]


def get_recent_news(db: Session, limit: int) -> list[dict]:
    """
    首页"Today's Brief"用的查询：只取最近发布的 limit 篇。

    按 published_at 降序，没有发布时间的（旧的 seed/测试数据）排到
    最后——数量够的话会被自然挤出这个列表，不用手动清理旧数据。
    """
    statement = (
        select(Article).order_by(nulls_last(Article.published_at.desc())).limit(limit)
    )

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


def _matched_fields(article: Article, query: str) -> list[str]:
    """
    判断文章具体是在哪些字段上匹配到了搜索词，用于展示"匹配原因"。
    """
    query_lower = query.lower()
    matched = []

    if query_lower in article.title.lower():
        matched.append("Title")

    if query_lower in article.summary.lower():
        matched.append("Summary")

    if query_lower in article.takeaway.lower():
        matched.append("Takeaway")

    if any(query_lower in concept.lower() for concept in article.concepts):
        matched.append("Concepts")

    return matched


def search_articles(db: Session, query: str) -> list[dict]:
    """
    在标题、AI 摘要、AI 要点、概念标签中搜索文章（不区分大小写）。

    background 主要是解释性内容，容易引入噪音，所以不参与搜索。
    """
    pattern = f"%{query}%"

    statement = select(Article).where(
        or_(
            Article.title.ilike(pattern),
            Article.summary.ilike(pattern),
            Article.takeaway.ilike(pattern),
            cast(Article.concepts, String).ilike(pattern),
        )
    )

    articles = db.scalars(statement).all()

    return [
        {
            **article.to_dict(),
            "matchedIn": _matched_fields(article, query),
        }
        for article in articles
    ]
