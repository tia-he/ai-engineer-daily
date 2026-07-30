import os

# 数据库连接地址，唯一的配置来源。
# 本地开发默认连接本机 PostgreSQL；生产环境通过环境变量覆盖。
# `or` 而不是默认参数，理由同下面的 OPENAI_MODEL：环境变量"存在但是
# 空字符串"和"完全不存在"不是一回事，只有 `or` 能兜住前者。
DATABASE_URL = (
    os.environ.get("DATABASE_URL")
    or "postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily"
)

# RSS 新闻源列表
#
# Anthropic 曾经在这里（news/rss.xml），但那个地址已经 404 了——他们的
# /news 页面现在是纯前端渲染的 SPA，探测了常见路径/robots.txt/sitemap
# 都找不到替代的 RSS 入口，看起来是彻底不提供 RSS 了，所以移除。
# Google AI 的地址也曾经失效（跳转到一个不返回 RSS 内容的中间页），
# 换成了它实际跳转到的、真正返回 RSS 的地址。
RSS_FEEDS = [
    {
        "name": "OpenAI",
        "url": "https://openai.com/news/rss.xml",
    },
    {
        "name": "Google AI",
        "url": "https://blog.google/innovation-and-ai/technology/ai/rss/",
    },
    {
        "name": "Hugging Face",
        "url": "https://huggingface.co/blog/feed.xml",
    },
    {
        "name": "Mistral AI",
        "url": "https://mistral.ai/rss.xml",
    },
    {
        "name": "DeepMind",
        "url": "https://deepmind.google/blog/rss.xml",
    },
]

# 生成 AI 元数据使用的 OpenAI 模型，可以通过环境变量覆盖。
# `or` 而不是 os.environ.get 的默认参数：GitHub Actions 里
# `${{ secrets.OPENAI_MODEL }}` 在 secret 不存在时会把这个环境变量设成
# 空字符串而不是不设置，.get(key, default) 的默认值只在 key 完全不存在
# 时才生效，空字符串会原样通过，导致 OpenAI 调用时 model 参数是空的。
OPENAI_MODEL = os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"

# 每天最多发布几条精选新闻。宁少勿凑：某天候选故事不够格，
# 当天就可能少于这个数。
MAX_DAILY_STORIES = 5

# 允许跨域访问 API 的前端域名列表（逗号分隔），生产环境通过环境变量覆盖
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
