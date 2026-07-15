"""
app/routes/auth.py
------------------
Authentication endpoints for CodeMentor AI.

POST /api/auth/signup  — Register a new user account
POST /api/auth/login   — Authenticate and receive a JWT access token
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter()


@router.post(
    "/signup",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user account.
    - Checks that the email is not already registered.
    - Hashes the password using bcrypt before storing.
    - Returns the new user's public profile (no password).
    """
    # Check for duplicate email
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # Hash password and persist new user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        gender=user.gender,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post(
    "/login",
    response_model=schemas.Token,
    summary="Login and get a JWT token",
)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Verifies credentials and returns a signed JWT access token.
    The token is valid for the duration set by JWT_EXPIRATION_HOURS in .env.
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    # Reject unknown emails or wrong passwords
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Issue JWT token with user ID and email as payload claims
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
