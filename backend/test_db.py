from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models import Article


def test_database() -> None:
    with Session(engine) as db:
        statement = select(Article)

        articles = db.scalars(statement).all()

        print(f"Found {len(articles)} articles:\n")

        for article in articles:
            print(f"ID: {article.id}")
            print(f"Title: {article.title}")
            print(f"Concepts: {article.concepts}")
            print(f"Sources: {article.sources}")
            print("-" * 60)


if __name__ == "__main__":
    test_database()