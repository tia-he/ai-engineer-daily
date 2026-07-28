import os

# 数据库连接地址，唯一的配置来源。
# 本地开发默认连接本机 PostgreSQL；生产环境通过环境变量覆盖。
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily",
)

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

# 每天最多发布几条精选新闻。宁少勿凑：某天候选故事不够格，
# 当天就可能少于这个数。
MAX_DAILY_STORIES = 5

# 允许跨域访问 API 的前端域名列表（逗号分隔），生产环境通过环境变量覆盖
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
