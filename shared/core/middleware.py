import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from shared.utils.request_context import set_request_id


async def request_context_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    request.state.request_id = request_id
    set_request_id(request_id)

    started = time.perf_counter()
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-latency-ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
    return response
