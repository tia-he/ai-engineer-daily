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
    Create any missing tables, then reconcile columns that drifted from the
    model after its table already existed in a deployed database —
    `create_all()` only creates missing tables, it never alters one that's
    already there. Each statement is idempotent (`IF NOT EXISTS` / `IF
    EXISTS`), so this is safe to call on every startup.
    """
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        conn.execute(
            text('ALTER TABLE news ADD COLUMN IF NOT EXISTS "publishedAt" TIMESTAMPTZ')
        )
        conn.execute(
            text('ALTER TABLE news ADD COLUMN IF NOT EXISTS "imageUrl" VARCHAR')
        )
        conn.execute(
            text(
                'ALTER TABLE news ADD COLUMN IF NOT EXISTS "createdAt" '
                "TIMESTAMPTZ NOT NULL DEFAULT now()"
            )
        )
        # relatedNews is no longer populated by anything (dropped along with
        # the "Related" UI section, since nothing ever wrote a real value to
        # it) — drop it rather than leave a NOT NULL column the ORM no
        # longer sends a value for, which would otherwise break every future
        # insert.
        conn.execute(text('ALTER TABLE news DROP COLUMN IF EXISTS "relatedNews"'))
