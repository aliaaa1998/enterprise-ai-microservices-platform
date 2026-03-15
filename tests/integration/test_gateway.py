from fastapi.testclient import TestClient

from gateway.app.main import app


def test_gateway_service_registry():
    r = TestClient(app).get("/api/v1/services")
    assert r.status_code == 200
    assert "summarize" in r.json()["services"]


def test_gateway_proxy(monkeypatch):
    monkeypatch.setattr("gateway.app.main.rate_limited", lambda *_: False)
    monkeypatch.setattr(
        "gateway.app.main.cache_wrapper",
        lambda service, text, producer: (
            {"status": "ok", "data": {"summary": "x"}, "meta": {"request_id": "1"}},
            False,
        ),
    )
    r = TestClient(app).post(
        "/api/v1/summarize",
        json={"text": "hello world hello world"},
    )
    assert r.status_code == 200
