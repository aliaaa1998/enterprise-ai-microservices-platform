PROMPTS = {
    "summarizer": {
        "name": "summarizer_v1",
        "content": "You are an enterprise document analyst. Return concise JSON only.",
    },
    "meeting": {
        "name": "meeting_v1",
        "content": "You extract decisions and actions from meetings. Return concise JSON only.",
    },
    "classifier": {
        "name": "ticket_classifier_v1",
        "content": "Classify support tickets for enterprise routing. Return concise JSON only.",
    },
    "contract": {
        "name": "contract_risk_v1",
        "content": (
            "Screen contracts for risk patterns. "
            "Not legal advice. Return concise JSON only."
        ),
    },
}
