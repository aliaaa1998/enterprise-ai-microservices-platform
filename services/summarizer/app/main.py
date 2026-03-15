from shared.core.config import get_settings
from shared.core.service_app import ServiceSpec, create_service_app
from shared.prompts.templates import PROMPTS
from shared.schemas.service_models import DocumentSummary

SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "key_points": {"type": "array", "items": {"type": "string"}},
        "action_items": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "key_points", "action_items", "risks"],
    "additionalProperties": False,
}

settings = get_settings()
prompt = PROMPTS["summarizer"]
app = create_service_app(
    ServiceSpec(
        service_name="summarizer",
        prompt_name=prompt["name"],
        model=settings.openai_model_summarizer,
        system_prompt=prompt["content"],
        schema=SCHEMA,
        output_model=DocumentSummary,
        endpoint="/summarize",
    )
)
