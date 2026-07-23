from schemas import SearchResult

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import crud
from database import get_db


router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get(
    "",
    response_model=list[SearchResult],
)
def search_news(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    return crud.search_articles(db, q)
