from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def ensure_schema() -> None:
    """
    Create any missing tables, then add any columns that were added to a
    model after its table already existed in a deployed database —
    `create_all()` only creates missing tables, it never alters one that's
    already there. Each `ADD COLUMN IF NOT EXISTS` is a no-op once the
    column exists, so this is safe to call on every startup.
    """
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        conn.execute(
            text('ALTER TABLE news ADD COLUMN IF NOT EXISTS "publishedAt" TIMESTAMPTZ')
        )
        conn.execute(
            text('ALTER TABLE news ADD COLUMN IF NOT EXISTS "imageUrl" VARCHAR')
        )
