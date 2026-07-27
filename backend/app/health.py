from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("")
def read_health(db: Session = Depends(get_db)):
    """
    健康检查：确认数据库连接是否正常。

    数据库不可用时返回 503，而不是让请求方等到超时才发现问题。
    """
    try:
        db.execute(text("SELECT 1"))
    except Exception as error:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "error", "detail": str(error)},
        )

    return {"status": "ok", "database": "ok"}
