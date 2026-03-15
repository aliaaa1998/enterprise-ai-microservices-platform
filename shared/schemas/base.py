from datetime import datetime

from pydantic import BaseModel, Field


class ResponseMeta(BaseModel):
    request_id: str
    service: str
    model: str | None = None
    latency_ms: float
    cached: bool = False
    usage: dict | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResponseEnvelope[T](BaseModel):
    status: str = "ok"
    data: T
    meta: ResponseMeta


class ErrorEnvelope(BaseModel):
    status: str = "error"
    error: str
    request_id: str
