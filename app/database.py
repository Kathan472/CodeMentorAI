"""
app/database.py
---------------
SQLAlchemy database engine and session configuration.

The DATABASE_URL is loaded from the .env file. The app uses TiDB Cloud
(MySQL-compatible) in production, but any MySQL or SQLite URL works locally.

Usage:
    Import `get_db` as a FastAPI dependency to get a scoped session per request.
    Import `SessionLocal` directly for background tasks (e.g. SSE generators).
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ---------------------------------------------------------------------------
# Engine — set echo=True to log SQL queries during development
# ---------------------------------------------------------------------------
engine = create_engine(DATABASE_URL, echo=False)

# ---------------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------------------------------------------------------
# Base class — all ORM models inherit from this
# ---------------------------------------------------------------------------
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session for the duration of a
    request, then closes it automatically when the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
