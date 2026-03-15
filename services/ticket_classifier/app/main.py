from shared.core.config import get_settings
from shared.core.service_app import ServiceSpec, create_service_app
from shared.prompts.templates import PROMPTS
from shared.schemas.service_models import TicketClassification

SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["billing", "technical", "account", "security", "other"],
        },
        "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]},
        "sentiment": {"type": "string", "enum": ["negative", "neutral", "positive"]},
        "routing_recommendation": {"type": "string"},
        "confidence": {"type": "number"},
    },
    "required": ["category", "priority", "sentiment", "routing_recommendation", "confidence"],
    "additionalProperties": False,
}

settings = get_settings()
prompt = PROMPTS["classifier"]
app = create_service_app(
    ServiceSpec(
        service_name="ticket_classifier",
        prompt_name=prompt["name"],
        model=settings.openai_model_classifier,
        system_prompt=prompt["content"],
        schema=SCHEMA,
        output_model=TicketClassification,
        endpoint="/classify-ticket",
    )
)
