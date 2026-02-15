from fastapi.testclient import TestClient

from ndefender_system_controller.main import app


def test_ws_hello_envelope():
    client = TestClient(app)
    with client.websocket_connect("/api/v1/ws") as ws:
        msg = ws.receive_json()
    assert msg["type"] == "LOG_EVENT"
    assert msg["data"]["message"] == "HELLO"
    assert isinstance(msg["timestamp_ms"], int)
    assert msg["source"] == "system"
