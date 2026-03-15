from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "ai-enterprise-microservices"
    environment: str = "dev"
    log_level: str = "INFO"

    gateway_host: str = "0.0.0.0"
    gateway_port: int = 8000

    summarizer_url: str = "http://summarizer-service:8001"
    meeting_url: str = "http://meeting-insights-service:8002"
    classifier_url: str = "http://ticket-classifier-service:8003"
    contract_url: str = "http://contract-analyzer-service:8004"

    postgres_dsn: str = "postgresql+psycopg://postgres:postgres@postgres:5432/enterprise_ai"
    redis_url: str = "redis://redis:6379/0"

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_request_timeout_seconds: float = 30.0
    openai_model_summarizer: str = "gpt-4.1-mini"
    openai_model_meeting: str = "gpt-4.1-mini"
    openai_model_classifier: str = "gpt-4.1-mini"
    openai_model_contract: str = "gpt-4.1-mini"

    default_max_text_chars: int = 12000
    preview_chars: int = 280
    cache_ttl_seconds: int = 900
    rate_limit_requests_per_minute: int = 60


@lru_cache
def get_settings() -> Settings:
    return Settings()
