from fastapi.testclient import TestClient

from ndefender_system_controller.main import app

client = TestClient(app)


def test_health_ok():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert isinstance(data["timestamp_ms"], int)
    assert isinstance(data["version"], str)


def test_status_stub():
    resp = client.get("/api/v1/status")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["timestamp_ms"], int)
    assert data["services"] == []
