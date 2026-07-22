from schemas import Article

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import get_db


router = APIRouter(
    prefix="/news",
    tags=["news"],
)


@router.get(
    "",
    response_model=list[Article],
)
def read_news(db: Session = Depends(get_db)):
    articles = crud.get_news(db)

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