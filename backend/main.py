from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.news import router as news_router
from app.search import router as search_router
from config import ALLOWED_ORIGINS

# 数据库表结构由 Alembic 管理（见 backend/alembic/），启动前需要运行
# `alembic upgrade head`，这里不再调用 Base.metadata.create_all()。

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