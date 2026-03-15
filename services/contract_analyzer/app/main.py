from shared.core.config import get_settings
from shared.core.service_app import ServiceSpec, create_service_app
from shared.prompts.templates import PROMPTS
from shared.schemas.service_models import ContractRiskAnalysis

SCHEMA = {
    "type": "object",
    "properties": {
        "risk_level": {"type": "string", "enum": ["low", "medium", "high"]},
        "flagged_clauses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "clause_excerpt": {"type": "string"},
                    "issue_type": {"type": "string"},
                    "rationale": {"type": "string"},
                    "recommended_action": {"type": "string"},
                },
                "required": ["clause_excerpt", "issue_type", "rationale", "recommended_action"],
                "additionalProperties": False,
            },
        },
        "overall_assessment": {"type": "string"},
    },
    "required": ["risk_level", "flagged_clauses", "overall_assessment"],
    "additionalProperties": False,
}

settings = get_settings()
prompt = PROMPTS["contract"]
app = create_service_app(
    ServiceSpec(
        service_name="contract_analyzer",
        prompt_name=prompt["name"],
        model=settings.openai_model_contract,
        system_prompt=prompt["content"],
        schema=SCHEMA,
        output_model=ContractRiskAnalysis,
        endpoint="/analyze-contract",
    )
)
