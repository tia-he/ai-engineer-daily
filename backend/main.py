from fastapi import FastAPI

from app.news import router as news_router
from database import Base, engine


# 如果数据库表尚不存在，就创建数据库表。
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Engineer Daily API",
    description="Backend API for AI Engineer Daily.",
    version="1.0.0",
)


app.include_router(news_router)


@app.get("/")
def read_root():
    return {
        "message": "AI Engineer Daily API is running."
    }