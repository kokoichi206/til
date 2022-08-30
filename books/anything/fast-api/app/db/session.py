from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Engine = create_engine(
    "sqlite:///sample_db.sqlite3",
    encoding="utf-8",
    echo=False,
)

SessionLocal = sessionmaker(bind=Engine)
