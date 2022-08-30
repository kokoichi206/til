from app.api.schemas import ProgrammerDetail
from app.db.models import Programmer, ProgrammerLanguage
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_programmers(
    db: Session,
) -> list[Programmer]:
    programmers = db.scalars(select(Programmer).order_by("id")).all()
    return programmers


def add_programmer(
    db: Session,
    programmer_detail: ProgrammerDetail,
):
    programmer = Programmer()
    programmer.name = programmer_detail.name
    programmer.twitter_id = programmer_detail.twitter_id
    programmer.languages = [
        ProgrammerLanguage(name=language) for language in programmer_detail.languages
    ]
    db.add(programmer)
    db.commit()
