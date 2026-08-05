from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "SIPC Genesis" in response.text


def test_gis_status_endpoint() -> None:
    response = client.get("/api/gis/status")

    assert response.status_code == 200
    payload = response.json()
    assert "ready" in payload
    assert "datasets" in payload
    assert isinstance(payload["datasets"], list)
