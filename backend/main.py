import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.health import router as health_router
from app.news import router as news_router
from app.search import router as search_router
from config import ALLOWED_ORIGINS
from database import Base, engine
from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    logger.info(
        "%s %s -> %d (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response


app.include_router(health_router)
app.include_router(news_router)
app.include_router(search_router)


@app.get("/")
def read_root():
    return {"message": "AI Engineer Daily API is running."}
