import json
import logging
from typing import Any

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from shared.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AIClient:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_request_timeout_seconds,
        )

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def call_structured(
        self,
        *,
        model: str,
        system_prompt: str,
        user_text: str,
        response_schema: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, int] | None]:
        response = self.client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": [{"type": "input_text", "text": user_text}]},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "structured_output",
                    "schema": response_schema,
                    "strict": True,
                }
            },
        )

        output_text = getattr(response, "output_text", "{}") or "{}"
        parsed = json.loads(output_text)
        usage = None
        if getattr(response, "usage", None):
            usage = {
                "input_tokens": getattr(response.usage, "input_tokens", 0),
                "output_tokens": getattr(response.usage, "output_tokens", 0),
                "total_tokens": getattr(response.usage, "total_tokens", 0),
            }
        logger.info("openai_call_success", extra={"model": model})
        return parsed, usage
