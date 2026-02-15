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


def test_system_endpoint():
    resp = client.get("/api/v1/system")
    assert resp.status_code == 200
    data = resp.json()
    assert "uptime_s" in data


def test_ups_endpoint():
    resp = client.get("/api/v1/ups")
    assert resp.status_code == 200
    data = resp.json()
    assert "state" in data


def test_services_endpoint():
    resp = client.get("/api/v1/services")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
