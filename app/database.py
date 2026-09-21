import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Vercel's deployed function filesystem is read-only except for /tmp.
    # Use /tmp for the SQLite demo; local development uses ./students.db.
    DATABASE_URL = (
        "sqlite:////tmp/students.db"
        if os.getenv("VERCEL")
        else "sqlite:///./students.db"
    )

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
