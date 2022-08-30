from lib2to3.pytree import Base
from unicodedata import name

from pydantic import BaseModel


class ProgrammerListItem(BaseModel):
    name: str

    # O/R マッパのモデルとの互換性を持たせる！
    class Config:
        orm_mode = True


class ProgrammerDetail(BaseModel):
    name: str
    twitter_id: str
    languages: list[str]
