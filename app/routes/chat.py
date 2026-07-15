"""
app/routes/chat.py
------------------
AI Chat endpoints for CodeMentor AI.

POST /api/chat/explain          — Submit code or a GitHub URL for an AI explanation (SSE streaming)
POST /api/chat/followup         — Ask a follow-up question about a previous submission (SSE streaming)
GET  /api/chat/{submission_id}  — Retrieve the full chat history for a submission

Both explain and followup stream Server-Sent Events (SSE). Each event is a JSON
object with either a `chunk` key (text fragment) or a `submission_id` key (sent
first so the frontend can reference the session).
"""

import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db, SessionLocal
from app.middleware.auth import get_current_user
from app.models import User, Submission, ChatHistory, UserStats
from app.schemas import ExplainRequest, FollowUpRequest
from app.services.gemini_service import gemini_service
from app.utils.github_fetcher import fetch_github_repo_context

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /api/chat/explain
# ---------------------------------------------------------------------------
@router.post("/explain", summary="Explain code or a GitHub repo (streaming)")
async def explain_code(
    req: ExplainRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Accepts either a code snippet + language OR a public GitHub repository URL.

    Flow:
    1. Fetches GitHub repo contents if a URL was provided.
    2. Saves a Submission record to the database.
    3. Increments the user's stats (submissions, explanations, languages used).
    4. Streams the Gemini AI explanation back as Server-Sent Events.
    5. On completion, saves the full AI response to chat_history.

    The first SSE event always contains `{"submission_id": <id>}` so the frontend
    can track which session this belongs to.
    """
    is_repo = bool(req.github_url)
    repo_context = ""

    # --- GitHub repo path ---
    if is_repo:
        try:
            repo_context = await fetch_github_repo_context(req.github_url)
        except Exception as e:
            # Stream a single error event and close gracefully
            return StreamingResponse(
                (f"data: {json.dumps({'error': str(e)})}\n\n" for _ in range(1)),
                media_type="text/event-stream",
            )
        code_to_save = repo_context
        language = "repository"
    else:
        code_to_save = req.code or ""
        language = req.language

    # --- Save Submission ---
    submission = Submission(
        user_id=current_user.id,
        code_snippet=code_to_save,
        language=language,
        github_url=req.github_url,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # --- Update User Stats ---
    stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()
    if not stats:
        stats = UserStats(
            user_id=current_user.id,
            total_submissions=0,
            total_explanations=0,
            languages_practiced={},
            total_tokens_used=0,
        )
        db.add(stats)

    stats.total_submissions  = (stats.total_submissions  or 0) + 1
    stats.total_explanations = (stats.total_explanations or 0) + 1

    # Track which languages the user has worked with
    langs = dict(stats.languages_practiced or {})
    langs[req.language] = langs.get(req.language, 0) + 1
    stats.languages_practiced = langs
    db.commit()

    # --- SSE Generator ---
    async def event_generator():
        full_response = ""
        try:
            # Send submission ID first so the client can reference this session
            yield f"data: {json.dumps({'submission_id': submission.id})}\n\n"

            # Choose the appropriate Gemini stream
            if is_repo:
                stream = gemini_service.explain_repo_stream(
                    repo_url=req.github_url, repo_context=repo_context
                )
            else:
                stream = gemini_service.explain_code_stream(
                    language=language, code=req.code
                )

            # Stream each text chunk to the client
            async for chunk in stream:
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        finally:
            # Save the full AI response using a fresh DB session.
            # Using a fresh session here ensures this write succeeds even if
            # the request session has been closed by a client disconnect.
            db_save = SessionLocal()
            try:
                chat = ChatHistory(
                    submission_id=submission.id,
                    user_message=f"Please explain this {'repository' if is_repo else 'code'}.",
                    ai_response=full_response,
                )
                db_save.add(chat)
                db_save.commit()
            finally:
                db_save.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# POST /api/chat/followup
# ---------------------------------------------------------------------------
@router.post("/followup", summary="Ask a follow-up question (streaming)")
async def followup_question(
    req: FollowUpRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Handles follow-up questions in an ongoing code explanation session.

    Reconstructs the full conversation history from the database and sends it
    to Gemini as context, ensuring the AI can answer in relation to the original
    code and prior exchanges.
    """
    # Verify the submission exists and belongs to this user
    submission = db.query(Submission).filter(Submission.id == req.submission_id).first()
    if not submission or submission.user_id != current_user.id:
        return StreamingResponse(
            (
                f"data: {json.dumps({'error': 'Submission not found or unauthorized'})}\n\n"
                for _ in range(1)
            ),
            media_type="text/event-stream",
        )

    # Build conversation history context
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.submission_id == req.submission_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )

    context = (
        f"Here is the user's original code in {submission.language}:\n"
        f"```\n{submission.code_snippet}\n```\n\nPast Conversation:\n"
    )
    for chat in history:
        context += f"User: {chat.user_message}\nAI: {chat.ai_response}\n\n"

    # --- SSE Generator ---
    async def event_generator():
        full_response = ""
        try:
            async for chunk in gemini_service.followup_stream(
                context=context, question=req.question
            ):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        finally:
            db_save = SessionLocal()
            try:
                chat = ChatHistory(
                    submission_id=req.submission_id,
                    user_message=req.question,
                    ai_response=full_response,
                )
                db_save.add(chat)
                db_save.commit()
            finally:
                db_save.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# GET /api/chat/{submission_id}
# ---------------------------------------------------------------------------
@router.get(
    "/{submission_id}",
    response_model=List[schemas.ChatHistoryResponse],
    summary="Get chat history for a submission",
)
async def get_submission_chat(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns the ordered list of AI chat messages for a given submission.
    Only accessible by the user who owns the submission.
    """
    # Ownership check
    submission = db.query(Submission).filter(
        Submission.id == submission_id,
        Submission.user_id == current_user.id,
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")

    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.submission_id == submission_id)
        .order_by(ChatHistory.created_at)
        .all()
    )

    return [
        schemas.ChatHistoryResponse(
            id=h.id,
            user_message=h.user_message or "",
            ai_response=h.ai_response or "",
            tokens_used=h.tokens_used or 0,
            created_at=h.created_at.isoformat() if h.created_at else "",
        )
        for h in history
    ]
