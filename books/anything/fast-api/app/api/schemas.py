from lib2to3.pytree import Base
from typing import Any
from unicodedata import name

from pydantic import BaseModel, Field


class ProgrammerListItem(BaseModel):
    name: str

    # O/R マッパのモデルとの互換性を持たせる！
    class Config:
        orm_mode = True


class ProgrammerDetail(BaseModel):
    name: str
    twitter_id: str
    languages: list[str] = Field(..., min_items=1, max_items=3)
