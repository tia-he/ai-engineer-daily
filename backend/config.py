from pathlib import Path

# backend 文件夹
BASE_DIR = Path(__file__).resolve().parent

# 数据库位置
DATABASE_PATH = BASE_DIR / "news.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"