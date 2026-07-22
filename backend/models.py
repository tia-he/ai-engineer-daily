from typing import Any

from sqlalchemy import JSON, String, Text
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
        }