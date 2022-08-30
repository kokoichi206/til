from lib2to3.pytree import Base
from unicodedata import name

from pydantic import BaseModel


class ProgrammerListItem(BaseModel):
    name: str


class ProgrammerDetail(BaseModel):
    name: str
    twitter_id: str
    languages: list[str]
