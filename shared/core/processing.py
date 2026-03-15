import json
import time
from typing import Any

from sqlalchemy.orm import Session

from shared.db.models import RequestRun, ServiceResult


def safe_preview(text: str, max_chars: int = 280) -> str:
    return " ".join(text.strip().split())[:max_chars]


def estimate_cost(usage: dict[str, int] | None) -> float | None:
    if not usage:
        return None
    input_cost = usage.get("input_tokens", 0) * 0.0000003
    output_cost = usage.get("output_tokens", 0) * 0.0000012
    return round(input_cost + output_cost, 6)


def persist_run(
    db: Session,
    *,
    request_id: str,
    service_name: str,
    input_text: str,
    status: str,
    latency_ms: float,
    model: str,
    prompt_name: str,
    result_payload: dict[str, Any],
    usage: dict[str, int] | None,
) -> None:
    run = RequestRun(
        request_id=request_id,
        service_name=service_name,
        input_preview=safe_preview(input_text),
        status=status,
        latency_ms=latency_ms,
        model=model,
        prompt_name=prompt_name,
    )
    db.add(run)
    db.flush()
    db.add(
        ServiceResult(
            request_run_id=run.id,
            payload_json=json.dumps(result_payload),
            token_usage_input=usage.get("input_tokens") if usage else None,
            token_usage_output=usage.get("output_tokens") if usage else None,
            cost_estimate_usd=estimate_cost(usage),
        )
    )
    db.commit()


def timed_call(fn):
    started = time.perf_counter()
    output = fn()
    return output, (time.perf_counter() - started) * 1000
