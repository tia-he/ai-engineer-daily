import os
from pathlib import Path

# backend 文件夹
BASE_DIR = Path(__file__).resolve().parent

# 数据库位置
DATABASE_PATH = BASE_DIR / "news.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# RSS 新闻源列表
RSS_FEEDS = [
    {
        "name": "OpenAI",
        "url": "https://openai.com/news/rss.xml",
    },
    {
        "name": "Anthropic",
        "url": "https://www.anthropic.com/news/rss.xml",
    },
    {
        "name": "Google AI",
        "url": "https://blog.google/technology/ai/rss/",
    },
    {
        "name": "Hugging Face",
        "url": "https://huggingface.co/blog/feed.xml",
    },
]

# 生成 AI 元数据使用的 OpenAI 模型，可以通过环境变量覆盖
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")