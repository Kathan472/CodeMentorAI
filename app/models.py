"""
app/models.py
-------------
SQLAlchemy ORM models for CodeMentor AI.

Tables:
    - users         → Stores registered user accounts
    - submissions   → Each code snippet or GitHub repo a user submits for explanation
    - chat_history  → Each AI exchange (question + answer) linked to a submission
    - user_stats    → Aggregated statistics per user (updated on each explanation)
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from datetime import datetime
from app.database import Base


class User(Base):
    """Registered user account."""

    __tablename__ = "users"

    id           = Column(Integer, primary_key=True, index=True)
    email        = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name         = Column(String(100))
    gender       = Column(String(50))
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Submission(Base):
    """
    A single code-explain or GitHub-repo-explain session initiated by a user.
    Either `code_snippet` or `github_url` will be populated (not necessarily both).
    """

    __tablename__ = "submissions"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    code_snippet = Column(Text(length=4294967295), nullable=True)  # LONGTEXT
    github_url   = Column(String(255), nullable=True)
    language     = Column(String(50), nullable=False, index=True)
    created_at   = Column(DateTime, default=datetime.utcnow)


class ChatHistory(Base):
    """
    A single turn in the AI conversation for a given submission.
    Stores both the user's message and the AI's markdown response.
    """

    __tablename__ = "chat_history"

    id            = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False, index=True)
    user_message  = Column(Text)
    ai_response   = Column(Text)
    tokens_used   = Column(Integer, default=0)   # Reserved for future token tracking
    created_at    = Column(DateTime, default=datetime.utcnow)


class UserStats(Base):
    """
    Aggregated per-user statistics. One row per user.
    Updated every time the user requests an AI explanation.
    """

    __tablename__ = "user_stats"

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id"), unique=True)
    total_submissions   = Column(Integer, default=0)
    total_explanations  = Column(Integer, default=0)
    languages_practiced = Column(JSON)             # e.g. {"python": 5, "cpp": 2}
    total_tokens_used   = Column(Integer, default=0)
    updated_at          = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
