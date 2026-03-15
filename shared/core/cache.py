import hashlib
import json
from collections.abc import Callable
from typing import Any

from redis import Redis

from shared.core.config import get_settings

settings = get_settings()
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


def make_cache_key(service: str, text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"svc:{service}:{digest}"


def get_cached_json(key: str) -> dict[str, Any] | None:
    raw = redis_client.get(key)
    return json.loads(raw) if raw else None


def set_cached_json(key: str, data: dict[str, Any], ttl_seconds: int | None = None) -> None:
    ttl = ttl_seconds or settings.cache_ttl_seconds
    redis_client.setex(key, ttl, json.dumps(data))


def rate_limited(client_id: str, limit: int | None = None) -> bool:
    max_req = limit or settings.rate_limit_requests_per_minute
    key = f"rl:{client_id}"
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, 60)
    return current > max_req


def cache_wrapper(
    service: str,
    text: str,
    producer: Callable[[], dict[str, Any]],
) -> tuple[dict[str, Any], bool]:
    key = make_cache_key(service, text)
    cached = get_cached_json(key)
    if cached is not None:
        return cached, True
    result = producer()
    set_cached_json(key, result)
    return result, False
