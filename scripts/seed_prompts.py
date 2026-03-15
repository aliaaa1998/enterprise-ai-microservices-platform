from sqlalchemy.orm import Session

from shared.db.models import PromptTemplate
from shared.db.session import SessionLocal
from shared.prompts.templates import PROMPTS


def main() -> None:
    db: Session = SessionLocal()
    try:
        for service, prompt in PROMPTS.items():
            db.add(
                PromptTemplate(
                    service_name=service,
                    prompt_name=prompt["name"],
                    version="1.0.0",
                    content=prompt["content"],
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
