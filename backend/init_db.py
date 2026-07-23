from sqlalchemy import delete
from sqlalchemy.orm import Session

from config import DATABASE_URL
from database import Base, engine
from models import Article


SEED_ARTICLES = [
    {
        "id": "openai-coding-model",
        "title": "OpenAI Releases New Coding Model",
        "summary": (
            "A new model optimized for software engineering tasks."
        ),
        "content": (
            "OpenAI introduced a new coding model with stronger "
            "repository-level reasoning and software engineering "
            "capabilities."
        ),
        "takeaway": (
            "AI coding assistants are evolving from code completion "
            "toward repository-level software engineering."
        ),
        "concepts": [
            "LLM",
            "Code Generation",
            "Repository",
        ],
        "background": (
            "Large language models are becoming capable of "
            "understanding entire repositories instead of individual "
            "files."
        ),
        "related_news": [
            {
                "id": "cursor-agent",
                "title": "Cursor Launches AI Coding Agent",
            }
        ],
        "sources": [
            {
                "name": "OpenAI",
                "url": "https://openai.com",
            }
        ],
    },
    {
        "id": "google-mcp-sdk",
        "title": "Google Launches MCP SDK",
        "summary": (
            "Google announces a new SDK supporting MCP."
        ),
        "content": (
            "Google launches a new SDK supporting the Model Context "
            "Protocol, making it easier for developers to connect AI "
            "applications with external tools."
        ),
        "takeaway": (
            "Support from major companies suggests MCP is becoming "
            "an emerging industry standard."
        ),
        "concepts": [
            "MCP",
            "SDK",
            "Tool Integration",
        ],
        "background": (
            "The Model Context Protocol is an open protocol that "
            "allows AI systems to interact with external tools and "
            "data sources."
        ),
        "related_news": [],
        "sources": [
            {
                "name": "Google Developers",
                "url": "https://developers.google.com",
            }
        ],
    },
    {
        "id": "cursor-agent",
        "title": "Cursor Launches AI Coding Agent",
        "summary": (
            "Cursor adds a new AI coding agent."
        ),
        "content": (
            "Cursor introduces an AI coding agent capable of "
            "understanding project context and completing more complex "
            "software development tasks."
        ),
        "takeaway": (
            "Coding tools are gradually shifting from copilots toward "
            "more autonomous development agents."
        ),
        "concepts": [
            "AI Agent",
            "IDE",
            "Code Generation",
        ],
        "background": (
            "AI-powered development environments are evolving beyond "
            "autocomplete and beginning to perform multi-step coding "
            "tasks."
        ),
        "related_news": [
            {
                "id": "openai-coding-model",
                "title": "OpenAI Releases New Coding Model",
            }
        ],
        "sources": [
            {
                "name": "Cursor",
                "url": "https://cursor.com",
            }
        ],
    },
]


def initialize_database() -> None:
    """
    创建数据库表，并写入开发阶段的初始新闻数据。
    """

    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        # 每次初始化时先清空旧数据，避免重复插入。
        db.execute(delete(Article))

        articles = [
            Article(**article_data)
            for article_data in SEED_ARTICLES
        ]

        db.add_all(articles)
        db.commit()

    print("Database initialized successfully.")
    print(f"Database URL: {DATABASE_URL}")
    print(f"Inserted {len(SEED_ARTICLES)} articles.")


if __name__ == "__main__":
    initialize_database()