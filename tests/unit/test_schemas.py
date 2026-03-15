import pytest
from pydantic import ValidationError

from shared.schemas.service_models import TextInput, TicketClassification


def test_text_input_validation() -> None:
    with pytest.raises(ValidationError):
        TextInput(text="   ")


def test_ticket_classification_validation() -> None:
    obj = TicketClassification(
        category="technical",
        priority="high",
        sentiment="negative",
        routing_recommendation="route to platform",
        confidence=0.91,
    )
    assert obj.priority == "high"
