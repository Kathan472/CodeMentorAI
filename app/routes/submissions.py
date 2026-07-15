"""
app/routes/submissions.py
-------------------------
Submission history endpoint for CodeMentor AI.

GET /api/submissions — Returns all past code/repo submissions for the current user,
                       sorted newest first (used to populate the History panel in the UI).
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.middleware.auth import get_current_user

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.SubmissionResponse],
    summary="Get the current user's submission history",
)
async def get_user_submissions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns a list of all submissions (code snippets and GitHub repo explanations)
    made by the logged-in user, ordered newest-first.

    Each submission includes:
    - `id`           — Used to fetch chat history via GET /api/chat/{id}
    - `language`     — The programming language of the submission
    - `code_snippet` — The raw code (or repo context) that was explained
    - `github_url`   — Set if the submission was a GitHub repo, null otherwise
    - `created_at`   — ISO 8601 UTC timestamp
    """
    submissions = (
        db.query(models.Submission)
        .filter(models.Submission.user_id == current_user.id)
        .order_by(desc(models.Submission.created_at))
        .all()
    )

    return [
        schemas.SubmissionResponse(
            id=s.id,
            user_id=s.user_id,
            code_snippet=s.code_snippet,
            github_url=s.github_url,
            language=s.language,
            created_at=s.created_at.isoformat() + "Z" if s.created_at else "",
        )
        for s in submissions
    ]
