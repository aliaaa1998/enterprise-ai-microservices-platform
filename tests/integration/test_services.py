from fastapi.testclient import TestClient

from services.contract_analyzer.app.main import app as contract_app
from services.meeting_insights.app.main import app as meeting_app
from services.summarizer.app.main import app as summarizer_app
from services.ticket_classifier.app.main import app as ticket_app
from shared.db.session import get_db_session


class DummyDB:
    def add(self, *args, **kwargs):
        return None

    def flush(self):
        return None

    def commit(self):
        return None


DUMMY_USAGE = {"input_tokens": 3, "output_tokens": 2, "total_tokens": 5}


def override_db():
    yield DummyDB()


def _patch_llm(monkeypatch, payload):
    monkeypatch.setattr(
        "shared.ai.client.AIClient.call_structured",
        lambda self, **kwargs: (payload, DUMMY_USAGE),
    )


def test_summarizer_endpoint(monkeypatch):
    _patch_llm(
        monkeypatch,
        {"summary": "s", "key_points": [], "action_items": [], "risks": []},
    )
    summarizer_app.dependency_overrides[get_db_session] = override_db
    r = TestClient(summarizer_app).post("/summarize", json={"text": "a" * 20})
    assert r.status_code == 200


def test_meeting_endpoint(monkeypatch):
    _patch_llm(
        monkeypatch,
        {
            "summary": "s",
            "decisions": [],
            "action_items": [],
            "follow_up_questions": [],
        },
    )
    meeting_app.dependency_overrides[get_db_session] = override_db
    r = TestClient(meeting_app).post("/meeting-insights", json={"text": "a" * 20})
    assert r.status_code == 200


def test_ticket_endpoint(monkeypatch):
    _patch_llm(
        monkeypatch,
        {
            "category": "technical",
            "priority": "medium",
            "sentiment": "neutral",
            "routing_recommendation": "ops",
            "confidence": 0.5,
        },
    )
    ticket_app.dependency_overrides[get_db_session] = override_db
    r = TestClient(ticket_app).post("/classify-ticket", json={"text": "a" * 20})
    assert r.status_code == 200


def test_contract_endpoint(monkeypatch):
    _patch_llm(
        monkeypatch,
        {"risk_level": "medium", "flagged_clauses": [], "overall_assessment": "ok"},
    )
    contract_app.dependency_overrides[get_db_session] = override_db
    r = TestClient(contract_app).post("/analyze-contract", json={"text": "a" * 20})
    assert r.status_code == 200
