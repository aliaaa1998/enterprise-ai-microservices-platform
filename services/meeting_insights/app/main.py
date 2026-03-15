from shared.core.config import get_settings
from shared.core.service_app import ServiceSpec, create_service_app
from shared.prompts.templates import PROMPTS
from shared.schemas.service_models import MeetingInsights

SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "decisions": {"type": "array", "items": {"type": "string"}},
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "owner": {"type": ["string", "null"]},
                    "due_date": {"type": ["string", "null"]},
                },
                "required": ["task", "owner", "due_date"],
                "additionalProperties": False,
            },
        },
        "follow_up_questions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "decisions", "action_items", "follow_up_questions"],
    "additionalProperties": False,
}

settings = get_settings()
prompt = PROMPTS["meeting"]
app = create_service_app(
    ServiceSpec(
        service_name="meeting_insights",
        prompt_name=prompt["name"],
        model=settings.openai_model_meeting,
        system_prompt=prompt["content"],
        schema=SCHEMA,
        output_model=MeetingInsights,
        endpoint="/meeting-insights",
    )
)
