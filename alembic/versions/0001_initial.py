"""initial

Revision ID: 0001
Revises:
Create Date: 2026-03-12
"""

import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "request_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("service_name", sa.String(length=64), nullable=False),
        sa.Column("input_preview", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=False),
        sa.Column("model", sa.String(length=64), nullable=False),
        sa.Column("prompt_name", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_request_runs_request_id", "request_runs", ["request_id"])
    op.create_index("ix_request_runs_service_name", "request_runs", ["service_name"])

    op.create_table(
        "service_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("request_run_id", sa.Integer(), sa.ForeignKey("request_runs.id"), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("token_usage_input", sa.Integer(), nullable=True),
        sa.Column("token_usage_output", sa.Integer(), nullable=True),
        sa.Column("cost_estimate_usd", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("request_run_id"),
    )

    op.create_table(
        "prompt_templates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("service_name", sa.String(length=64), nullable=False),
        sa.Column("prompt_name", sa.String(length=128), nullable=False),
        sa.Column("version", sa.String(length=32), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_prompt_templates_service_name", "prompt_templates", ["service_name"])


def downgrade() -> None:
    op.drop_index("ix_prompt_templates_service_name", table_name="prompt_templates")
    op.drop_table("prompt_templates")
    op.drop_table("service_results")
    op.drop_index("ix_request_runs_service_name", table_name="request_runs")
    op.drop_index("ix_request_runs_request_id", table_name="request_runs")
    op.drop_table("request_runs")
