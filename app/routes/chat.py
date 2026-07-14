from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json

from app.database import get_db, SessionLocal
from app.services.gemini_service import gemini_service
from app.middleware.auth import get_current_user
from app.models import User, Submission, ChatHistory
from app.schemas import ExplainRequest, FollowUpRequest

router = APIRouter()

@router.post("/explain")
async def explain_code(
    req: ExplainRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Takes the user's code, saves a Submission, sends it to the Gemini API,
    and streams back an SSE JSON explanation.
    """
    # 1. Save Submission
    submission = Submission(user_id=current_user.id, code_snippet=req.code, language=req.language)
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    async def event_generator():
        full_response = ""
        try:
            # Yield the submission ID first so the client can save it
            yield f"data: {json.dumps({'submission_id': submission.id})}\n\n"
            
            async for chunk in gemini_service.explain_code_stream(language=req.language, code=req.code):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                
        finally:
            # Save ChatHistory using a fresh session to ensure it doesn't fail if the request closes
            db_save = SessionLocal()
            try:
                chat = ChatHistory(
                    submission_id=submission.id,
                    user_message="Please explain this code.",
                    ai_response=full_response
                )
                db_save.add(chat)
                db_save.commit()
            finally:
                db_save.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/followup")
async def followup_question(
    req: FollowUpRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Takes a follow-up question, reconstructs the chat history context,
    sends to Gemini, and streams the response.
    """
    # 1. Verify Submission exists and belongs to user
    submission = db.query(Submission).filter(Submission.id == req.submission_id).first()
    if not submission or submission.user_id != current_user.id:
        return StreamingResponse(
            (f"data: {json.dumps({'error': 'Submission not found or unauthorized'})}\n\n" for _ in range(1)), 
            media_type="text/event-stream"
        )
        
    # 2. Get past chat history
    history = db.query(ChatHistory).filter(ChatHistory.submission_id == req.submission_id).order_by(ChatHistory.created_at.asc()).all()
    
    # 3. Format history for Gemini
    context = f"Here is the user's original code in {submission.language}:\n```\n{submission.code_snippet}\n```\n\nPast Conversation:\n"
    for chat in history:
        context += f"User: {chat.user_message}\nAI: {chat.ai_response}\n\n"
        
    async def event_generator():
        full_response = ""
        try:
            async for chunk in gemini_service.followup_stream(context=context, question=req.question):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                
        finally:
            db_save = SessionLocal()
            try:
                chat = ChatHistory(
                    submission_id=req.submission_id,
                    user_message=req.question,
                    ai_response=full_response
                )
                db_save.add(chat)
                db_save.commit()
            finally:
                db_save.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")
