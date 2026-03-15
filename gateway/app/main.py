import logging
from typing import Any

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from shared.core.cache import cache_wrapper, rate_limited
from shared.core.config import get_settings
from shared.core.middleware import request_context_middleware
from shared.db.models import RequestRun
from shared.db.session import get_db_session
from shared.logging.setup import configure_logging

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="ai-enterprise-microservices-gateway", version="1.0.0")
app.middleware("http")(request_context_middleware)

SERVICE_ROUTES: dict[str, tuple[str, str]] = {
    "summarize": (settings.summarizer_url, "/summarize"),
    "meeting-insights": (settings.meeting_url, "/meeting-insights"),
    "classify-ticket": (settings.classifier_url, "/classify-ticket"),
    "analyze-contract": (settings.contract_url, "/analyze-contract"),
}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/api/v1/services")
def services() -> dict[str, Any]:
    return {"services": list(SERVICE_ROUTES.keys())}


def forward(service_key: str, payload: dict[str, Any], request: Request) -> dict[str, Any]:
    base_url, route = SERVICE_ROUTES[service_key]
    headers = {"x-request-id": request.state.request_id}
    auth = request.headers.get("authorization")
    if auth:
        headers["authorization"] = auth

    with httpx.Client(timeout=settings.openai_request_timeout_seconds) as client:
        resp = client.post(f"{base_url}{route}", json=payload, headers=headers)
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


async def _proxy(service_key: str, request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    client_ip = request.client.host if request.client else "unknown"
    if rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="rate limit exceeded")

    text = payload.get("text", "")
    result, cached = cache_wrapper(
        service_key,
        text,
        lambda: forward(service_key, payload, request),
    )
    if cached and isinstance(result, dict) and "meta" in result:
        result["meta"]["cached"] = True
    return result


@app.post("/api/v1/summarize")
async def summarize(request: Request, payload: dict[str, Any]):
    return await _proxy("summarize", request, payload)


@app.post("/api/v1/meeting-insights")
async def meeting_insights(request: Request, payload: dict[str, Any]):
    return await _proxy("meeting-insights", request, payload)


@app.post("/api/v1/classify-ticket")
async def classify_ticket(request: Request, payload: dict[str, Any]):
    return await _proxy("classify-ticket", request, payload)


@app.post("/api/v1/analyze-contract")
async def analyze_contract(request: Request, payload: dict[str, Any]):
    return await _proxy("analyze-contract", request, payload)


@app.get("/api/v1/history")
def history(
    limit: int = 20,
    db: Session = Depends(get_db_session),  # noqa: B008
) -> dict[str, Any]:
    rows = (
        db.execute(select(RequestRun).order_by(desc(RequestRun.created_at)).limit(limit))
        .scalars()
        .all()
    )
    return {
        "items": [
            {
                "request_id": row.request_id,
                "service_name": row.service_name,
                "status": row.status,
                "latency_ms": row.latency_ms,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    }
