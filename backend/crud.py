from sqlalchemy.orm import Session
from models import Interview


def create_interview(
    db: Session,
    filename: str,
    role: str,
    skills: str,
    questions: str
):

    interview = Interview(
        filename=filename,
        role=role,
        skills=skills,
        questions=questions
    )

    db.add(interview)

    db.commit()

    db.refresh(interview)

    return interview