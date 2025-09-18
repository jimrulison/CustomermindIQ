"""
Authentication router for Growth Acceleration Engine
Simple JWT-based authentication system
"""

import os
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Environment variables
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Security
security = HTTPBearer()

# Router
auth_router = APIRouter()

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    company_name: Optional[str]
    subscription_status: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse

# Helper functions
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"email": email, "payload": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(request: Request, token_data: dict = Depends(verify_token)):
    """Get current user from database"""
    db = request.state.db
    user = await db.users.find_one({"email": token_data["email"]})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Convert MongoDB ObjectId to string
    user["id"] = str(user["_id"])
    del user["_id"]
    
    return user

# Authentication endpoints
@auth_router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, request: Request):
    """Register a new user"""
    db = request.state.db
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user document
    user_doc = {
        "email": user_data.email,
        "full_name": user_data.full_name,
        "company_name": user_data.company_name,
        "password_hash": hashed_password,
        "subscription_status": "trial",
        "subscription_plan": "growth_professional",
        "trial_end_date": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "is_active": True
    }
    
    # Insert user
    result = await db.users.insert_one(user_doc)
    user_doc["id"] = str(result.inserted_id)
    del user_doc["_id"]
    del user_doc["password_hash"]
    
    # Create access token
    access_token = create_access_token({"sub": user_data.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=JWT_EXPIRATION_HOURS * 3600,
        user=UserResponse(**user_doc)
    )

@auth_router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, request: Request):
    """Login user"""
    db = request.state.db
    
    # Find user
    user = await db.users.find_one({"email": user_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token({"sub": user_data.email})
    
    # Prepare user response
    user["id"] = str(user["_id"])
    del user["_id"]
    del user["password_hash"]
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=JWT_EXPIRATION_HOURS * 3600,
        user=UserResponse(**user)
    )

@auth_router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(**current_user)

@auth_router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}

# Password reset endpoints (basic implementation)
@auth_router.post("/forgot-password")
async def forgot_password(email: EmailStr, request: Request):
    """Request password reset (basic implementation)"""
    db = request.state.db
    
    user = await db.users.find_one({"email": email})
    if not user:
        # Don't reveal if user exists or not
        return {"message": "If the email exists, you will receive reset instructions"}
    
    # In a real implementation, you would:
    # 1. Generate a secure reset token
    # 2. Store it in database with expiration
    # 3. Send email with reset link
    
    logger.info(f"Password reset requested for: {email}")
    return {"message": "If the email exists, you will receive reset instructions"}

@auth_router.post("/reset-password")
async def reset_password(token: str, new_password: str, request: Request):
    """Reset password with token (basic implementation)"""
    # In a real implementation, you would:
    # 1. Verify the reset token
    # 2. Check if it's not expired
    # 3. Update user's password
    # 4. Invalidate the reset token
    
    return {"message": "Password reset successfully"}