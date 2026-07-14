from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.gemini_service import gemini_service
from app.utils.security import get_current_user
from app.models import User

router = APIRouter()

class ExplainRequest(BaseModel):
    language: str
    code: str

class ExplainResponse(BaseModel):
    success: bool
    explanation: str

@router.post("/explain", response_model=ExplainResponse)
async def explain_code(
    req: ExplainRequest,
    current_user: User = Depends(get_current_user)  # Require authentication!
):
    """
    Takes the user's code, sends it to the Gemini API with a tailored prompt,
    and returns a beautifully formatted Markdown explanation.
    """
    explanation = await gemini_service.explain_code(language=req.language, code=req.code)
    
    return ExplainResponse(
        success=True,
        explanation=explanation
    )
