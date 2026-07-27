from database import get_db
from main import app


def test_health_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_reports_503_when_database_check_fails(client):
    class BrokenSession:
        def execute(self, *args, **kwargs):
            raise RuntimeError("db unavailable")

    def broken_get_db():
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_get_db

    response = client.get("/health")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "error"
    assert body["database"] == "error"
