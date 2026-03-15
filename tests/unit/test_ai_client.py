import json
from types import SimpleNamespace

from shared.ai.client import AIClient


class FakeResponses:
    def create(self, **kwargs):
        payload = {"summary": "ok", "key_points": [], "action_items": [], "risks": []}
        return SimpleNamespace(
            output_text=json.dumps(payload),
            usage=SimpleNamespace(input_tokens=10, output_tokens=5, total_tokens=15),
        )


class FakeOpenAI:
    def __init__(self, *args, **kwargs):
        self.responses = FakeResponses()


def test_call_structured(monkeypatch):
    monkeypatch.setattr("shared.ai.client.OpenAI", FakeOpenAI)
    client = AIClient()
    data, usage = client.call_structured(
        model="gpt-4.1-mini",
        system_prompt="do",
        user_text="hello world",
        response_schema={"type": "object", "properties": {}, "required": []},
    )
    assert "summary" in data
    assert usage and usage["total_tokens"] == 15
