from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from shared.ai.client import AIClient
from shared.core.middleware import request_context_middleware
from shared.core.processing import persist_run, timed_call
from shared.db.session import get_db_session
from shared.logging.setup import configure_logging
from shared.schemas.base import ResponseEnvelope, ResponseMeta
from shared.schemas.service_models import TextInput


class ServiceSpec(BaseModel):
    service_name: str
    prompt_name: str
    model: str
    system_prompt: str
    schema: dict[str, Any]
    output_model: type[BaseModel]
    endpoint: str = "/process"


def create_service_app(spec: ServiceSpec) -> FastAPI:
    configure_logging()
    app = FastAPI(title=f"{spec.service_name}-service")
    app.middleware("http")(request_context_middleware)
    ai_client = AIClient()

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz")
    def readyz() -> dict[str, str]:
        return {"status": "ready"}

    @app.post(spec.endpoint, response_model=ResponseEnvelope[spec.output_model])
    def process(
        payload: TextInput,
        request: Request,
        db: Session = Depends(get_db_session),  # noqa: B008
    ):
        req_id = request.state.request_id
        text = payload.text.strip()

        def _run():
            raw, usage = ai_client.call_structured(
                model=spec.model,
                system_prompt=spec.system_prompt,
                user_text=text,
                response_schema=spec.schema,
            )
            return (spec.output_model.model_validate(raw), usage)

        try:
            (data, usage), latency_ms = timed_call(_run)
            persist_run(
                db,
                request_id=req_id,
                service_name=spec.service_name,
                input_text=text,
                status="success",
                latency_ms=latency_ms,
                model=spec.model,
                prompt_name=spec.prompt_name,
                result_payload=data.model_dump(),
                usage=usage,
            )
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=502, detail=f"LLM processing failed: {exc}") from exc

        return ResponseEnvelope(
            data=data,
            meta=ResponseMeta(
                request_id=req_id,
                service=spec.service_name,
                model=spec.model,
                latency_ms=latency_ms,
                usage=usage,
            ),
        )

    return app
