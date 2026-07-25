from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.news import router as news_router
from app.search import router as search_router
from config import ALLOWED_ORIGINS
from database import Base, engine


# 如果数据库表尚不存在，就创建数据库表。
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Engineer Daily API",
    description="Backend API for AI Engineer Daily.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)


app.include_router(news_router)
app.include_router(search_router)


@app.get("/")
def read_root():
    return {
        "message": "AI Engineer Daily API is running."
    }