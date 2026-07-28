from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from config import MAX_DAILY_STORIES
from database import get_db
from schemas import Article

router = APIRouter(
    prefix="/news",
    tags=["news"],
)


@router.get(
    "",
    response_model=list[Article],
)
def read_news(db: Session = Depends(get_db)):
    # The brief shows the current rotation of top stories, not the full
    # archive — see crud.get_recent_news. The archive is still fully
    # searchable via /search.
    articles = crud.get_recent_news(db, limit=MAX_DAILY_STORIES)

    return articles


@router.get(
    "/{article_id}",
    response_model=Article,
)
def read_article(
    article_id: str,
    db: Session = Depends(get_db),
):
    article = crud.get_article(db, article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article
