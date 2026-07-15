"""
app/routes/dashboard.py
-----------------------
Dashboard statistics endpoint for CodeMentor AI.

GET /api/dashboard/stats — Returns aggregated usage statistics for the current user
"""

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter()


@router.get(
    "/stats",
    response_model=schemas.DashboardStatsResponse,
    summary="Get the current user's usage statistics",
)
async def get_dashboard_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns aggregated statistics for the logged-in user:
    - `total_submissions`   — Total number of code/repo explanation sessions
    - `total_explanations`  — Total number of AI explanations requested
    - `languages_practiced` — Dict of {language: count} for all used languages
    - `total_tokens_used`   — Reserved for future token tracking (currently 0)
    """
    stats = (
        db.query(models.UserStats)
        .filter(models.UserStats.user_id == current_user.id)
        .first()
    )

    # Return zeroed stats for new users who haven't submitted anything yet
    if not stats:
        return schemas.DashboardStatsResponse(
            total_submissions=0,
            total_explanations=0,
            languages_practiced={},
            total_tokens_used=0,
        )

    # Deserialise JSON column in case the DB driver returns a raw string
    languages = stats.languages_practiced or {}
    if isinstance(languages, str):
        try:
            languages = json.loads(languages)
        except Exception:
            languages = {}

    return schemas.DashboardStatsResponse(
        total_submissions=stats.total_submissions or 0,
        total_explanations=stats.total_explanations or 0,
        languages_practiced=languages,
        total_tokens_used=stats.total_tokens_used or 0,
    )
