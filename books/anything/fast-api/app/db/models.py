from ast import Str
from enum import unique
from unicodedata import name

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Programmer(Base):
    __tablename__ = "programmer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    twitter_id = Column(String, nullable=False)
    languages = relationship("ProgrammerLanguage", backref="programmer")


class ProgrammerLanguage(Base):
    __tablename__ = "programmer_language"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    programmer_id = Column(Integer, ForeignKey("programmer.id"))
