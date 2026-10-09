from datetime import UTC, datetime
from app.application.health_service import HealthService
from app.bootstrap import create_app
from app.config import Settings


class FixedClock:
    def now(self) -> datetime:
        return datetime(2026, 1, 2, 3, 4, 5, 678901, tzinfo=UTC)


def test_health_service_is_framework_independent() -> None:
    result = HealthService(FixedClock()).execute()
    assert result.status == "healthy"
    assert result.timestamp == datetime(2026, 1, 2, 3, 4, 5, 678901, tzinfo=UTC)


def test_health_endpoint() -> None:
    settings = Settings("test", "INFO", 1024, "1000 per minute", "memory://", False)
    app = create_app(settings)
    app.testing = True
    with app.test_client() as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json is not None
    assert response.json["status"] == "healthy"
    assert response.json["timestamp"].endswith("Z")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cache-Control"] == "no-store"


def test_non_json_write_is_rejected() -> None:
    settings = Settings("test", "INFO", 1024, "1000 per minute", "memory://", False)
    app = create_app(settings)
    app.testing = True
    with app.test_client() as client:
        response = client.post("/api/v1/health", data="x", content_type="text/plain")
    assert response.status_code == 415
