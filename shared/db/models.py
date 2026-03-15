from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.db.session import Base


class RequestRun(Base):
    __tablename__ = "request_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    service_name: Mapped[str] = mapped_column(String(64), index=True)
    input_preview: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(32))
    latency_ms: Mapped[float] = mapped_column(Float)
    model: Mapped[str] = mapped_column(String(64))
    prompt_name: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    result: Mapped["ServiceResult"] = relationship(back_populates="run", uselist=False)


class ServiceResult(Base):
    __tablename__ = "service_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_run_id: Mapped[int] = mapped_column(ForeignKey("request_runs.id"), unique=True)
    payload_json: Mapped[str] = mapped_column(Text)
    token_usage_input: Mapped[int | None] = mapped_column(Integer, nullable=True)
    token_usage_output: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost_estimate_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    run: Mapped[RequestRun] = relationship(back_populates="result")


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(64), index=True)
    prompt_name: Mapped[str] = mapped_column(String(128))
    version: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
