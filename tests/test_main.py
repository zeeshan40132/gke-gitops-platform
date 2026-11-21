
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"


def test_metrics_endpoint():
    client.get("/")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_errors_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_error_metrics():
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404

    metrics_response = client.get("/metrics")

    assert metrics_response.status_code == 200
    assert 'status_code="404"' in metrics_response.text
