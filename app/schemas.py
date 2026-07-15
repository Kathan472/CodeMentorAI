from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    gender: Optional[str] = "Other"


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    gender: Optional[str] = None

    class Config:
        from_attributes = True


class ExplainRequest(BaseModel):
    language: str
    code: Optional[str] = None
    github_url: Optional[str] = None


class FollowUpRequest(BaseModel):
    submission_id: int
    question: str


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    code_snippet: Optional[str]
    github_url: Optional[str]
    language: str
    created_at: str

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    id: int
    user_message: str
    ai_response: str
    tokens_used: int
    created_at: str

    class Config:
        from_attributes = True


class DashboardStatsResponse(BaseModel):
    total_submissions: int
    total_explanations: int
    languages_practiced: dict
    total_tokens_used: int
