from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TextInput(BaseModel):
    text: str = Field(min_length=10, max_length=12000)

    @field_validator("text")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text cannot be empty")
        return value


class DocumentSummary(BaseModel):
    summary: str
    key_points: list[str]
    action_items: list[str]
    risks: list[str]


class MeetingActionItem(BaseModel):
    task: str
    owner: str | None = None
    due_date: str | None = None


class MeetingInsights(BaseModel):
    summary: str
    decisions: list[str]
    action_items: list[MeetingActionItem]
    follow_up_questions: list[str]


class TicketClassification(BaseModel):
    category: Literal["billing", "technical", "account", "security", "other"]
    priority: Literal["low", "medium", "high", "urgent"]
    sentiment: Literal["negative", "neutral", "positive"]
    routing_recommendation: str
    confidence: float = Field(ge=0.0, le=1.0)


class FlaggedClause(BaseModel):
    clause_excerpt: str
    issue_type: str
    rationale: str
    recommended_action: str


class ContractRiskAnalysis(BaseModel):
    risk_level: Literal["low", "medium", "high"]
    flagged_clauses: list[FlaggedClause]
    overall_assessment: str
