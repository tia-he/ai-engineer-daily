from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Article(Base):
    __tablename__ = "news"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    takeaway: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    concepts: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    background: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    related_news: Mapped[list[dict[str, Any]]] = mapped_column(
        "relatedNews",
        JSON,
        nullable=False,
        default=list,
    )

    sources: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    # 两个字段都可为空：不是每个 RSS 源都带发布时间/配图，取不到就是
    # NULL，前端据此决定是否渲染日期/图片区域，而不是编造数据。
    published_at: Mapped[datetime | None] = mapped_column(
        "publishedAt",
        DateTime(timezone=True),
        nullable=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        "imageUrl",
        String,
        nullable=True,
    )

    # 什么时候被我们的每日流程真正合成/发布的，不是源博客自己的发布
    # 时间（那是 published_at）。首页"最近几条"要按这个排序——按
    # published_at 排会把"今天刚合成、但原文是几天前发的"的文章排到
    # 后面去，显示不出来。
    created_at: Mapped[datetime] = mapped_column(
        "createdAt",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def to_dict(self) -> dict[str, Any]:
        """
        把 SQLAlchemy Article 对象转换成前端需要的 JSON 格式。
        """
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "takeaway": self.takeaway,
            "concepts": self.concepts,
            "background": self.background,
            "relatedNews": self.related_news,
            "sources": self.sources,
            "publishedAt": (
                self.published_at.isoformat() if self.published_at else None
            ),
            "imageUrl": self.image_url,
        }
