import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily_test",
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from main import app

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_session():
    """
    每个测试都在一个事务里运行，测试结束后回滚，互不影响。

    使用 join_transaction_mode="create_savepoint"，这样即使被测代码
    自己调用了 db.commit()（例如 crud.create_article），也只是释放/
    重建 SAVEPOINT，不会影响外层事务，teardown 时的 rollback() 仍然
    能清空这次测试写入的所有数据。
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
