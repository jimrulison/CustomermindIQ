"""
Customer Mind IQ - Authentication System
Complete user authentication, session management, and role-based access control
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Optional, List, Union
from datetime import datetime, timedelta
import hashlib
import secrets
import jwt
import os
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt
from enum import Enum

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.customer_mind_iq

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30

router = APIRouter()
security = HTTPBearer(auto_error=False)

# User Roles and Permissions
class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin" 
    MANAGER = "manager"
    ANALYST = "analyst"
    MARKETING_USER = "marketing_user"
    SALES_USER = "sales_user"
    CUSTOMER_SUCCESS = "customer_success"
    READ_ONLY = "read_only"
    USER = "user"

class SubscriptionTier(str, Enum):
    FREE = "free"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

# Pydantic Models
class UserRegistration(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    company_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = None
    role: UserRole = UserRole.USER
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

class UserProfile(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    company_name: Optional[str]
    phone: Optional[str]
    role: UserRole
    subscription_tier: SubscriptionTier
    is_active: bool
    email_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    profile_picture: Optional[str]

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

class PasswordReset(BaseModel):
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_profile: UserProfile

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN: {
        "modules": ["all"],
        "actions": ["create", "read", "update", "delete", "admin"],
        "data_access": "all",
        "user_management": True,
        "billing_access": True,
        "system_config": True
    },
    UserRole.ADMIN: {
        "modules": ["all"],
        "actions": ["create", "read", "update", "delete"],
        "data_access": "organization",
        "user_management": True,
        "billing_access": True,
        "system_config": False
    },
    UserRole.MANAGER: {
        "modules": ["customer_intelligence", "marketing_automation", "revenue_analytics", "analytics_insights"],
        "actions": ["create", "read", "update"],
        "data_access": "team",
        "user_management": "team",
        "billing_access": True,
        "system_config": False
    },
    UserRole.ANALYST: {
        "modules": ["customer_intelligence", "analytics_insights", "revenue_analytics"],
        "actions": ["read", "export"],
        "data_access": "assigned",
        "user_management": False,
        "billing_access": False,
        "system_config": False
    },
    UserRole.MARKETING_USER: {
        "modules": ["marketing_automation", "customer_intelligence", "analytics_insights"],
        "actions": ["create", "read", "update"],
        "data_access": "marketing",
        "user_management": False,
        "billing_access": False,
        "system_config": False
    },
    UserRole.SALES_USER: {
        "modules": ["customer_intelligence", "revenue_analytics", "lead_scoring"],
        "actions": ["read", "update"],
        "data_access": "sales",
        "user_management": False,
        "billing_access": False,
        "system_config": False
    },
    UserRole.CUSTOMER_SUCCESS: {
        "modules": ["customer_intelligence", "customer_success", "churn_prevention"],
        "actions": ["read", "update"],
        "data_access": "customer_success",
        "user_management": False,
        "billing_access": False,
        "system_config": False
    },
    UserRole.READ_ONLY: {
        "modules": ["customer_intelligence", "analytics_insights"],
        "actions": ["read"],
        "data_access": "limited",
        "user_management": False,
        "billing_access": False,
        "system_config": False
    },
    UserRole.USER: {
        "modules": ["customer_intelligence", "marketing_automation", "revenue_analytics"],
        "actions": ["read", "create", "update"],
        "data_access": "own",
        "user_management": False,
        "billing_access": "own",
        "system_config": False
    }
}

# Subscription tier module access
SUBSCRIPTION_MODULE_ACCESS = {
    SubscriptionTier.FREE: [
        "customer_intelligence_basic", 
        "basic_analytics", 
        "lead_scoring_basic"
    ],
    SubscriptionTier.PROFESSIONAL: [
        "customer_intelligence", "marketing_automation", "revenue_analytics",
        "analytics_insights", "behavioral_clustering", "churn_prevention",
        "cross_sell_intelligence", "roi_forecasting", "cohort_analysis"
    ],
    SubscriptionTier.ENTERPRISE: [
        "all_modules", "white_label", "custom_integrations", 
        "advanced_ai_models", "dedicated_support", "compliance_suite",
        "ai_command_center", "competitive_intelligence"
    ]
}

# Utility Functions
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserProfile:
    """Get current authenticated user"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_token(credentials.credentials)
    user_id = payload.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account deactivated"
        )
    
    return UserProfile(**user)

def require_role(allowed_roles: List[UserRole]):
    """Decorator to require specific roles"""
    def role_checker(current_user: UserProfile = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

def require_subscription(required_tiers: List[SubscriptionTier]):
    """Decorator to require specific subscription tiers"""
    def subscription_checker(current_user: UserProfile = Depends(get_current_user)):
        if current_user.subscription_tier not in required_tiers:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Upgrade subscription to access this feature"
            )
        return current_user
    return subscription_checker

def check_module_access(user: UserProfile, module_name: str) -> bool:
    """Check if user has access to specific module"""
    # Check role permissions
    role_modules = ROLE_PERMISSIONS.get(user.role, {}).get("modules", [])
    if "all" in role_modules or module_name in role_modules:
        pass  # Role allows access
    else:
        return False
    
    # Check subscription tier access
    tier_modules = SUBSCRIPTION_MODULE_ACCESS.get(user.subscription_tier, [])
    if "all_modules" in tier_modules or module_name in tier_modules:
        return True
    
    return False

# Authentication Endpoints

@router.post("/register", response_model=TokenResponse)
async def register_user(user_data: UserRegistration):
    """Register new user"""
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Generate user ID
    user_id = secrets.token_urlsafe(16)
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user document
    user_doc = {
        "user_id": user_id,
        "email": user_data.email,
        "password_hash": hashed_password,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "company_name": user_data.company_name,
        "phone": user_data.phone,
        "role": user_data.role,
        "subscription_tier": user_data.subscription_tier,
        "is_active": True,
        "email_verified": False,
        "created_at": datetime.utcnow(),
        "last_login": None,
        "profile_picture": None,
        "login_attempts": 0,
        "locked_until": None
    }
    
    # Insert user
    await db.users.insert_one(user_doc)
    
    # Create tokens
    token_data = {"user_id": user_id, "email": user_data.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Update last login
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create user profile
    user_profile = UserProfile(**{k: v for k, v in user_doc.items() if k != "password_hash"})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_profile=user_profile
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(login_data: UserLogin, request: Request):
    """User login"""
    
    # Find user (case-insensitive email lookup)
    user = await db.users.find_one({"email": {"$regex": f"^{login_data.email}$", "$options": "i"}})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is locked
    if user.get("locked_until") and user["locked_until"] > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account temporarily locked due to multiple failed attempts"
        )
    
    # Verify password
    if not verify_password(login_data.password, user["password_hash"]):
        # Increment failed attempts
        await db.users.update_one(
            {"user_id": user["user_id"]},
            {
                "$inc": {"login_attempts": 1},
                "$set": {"last_failed_login": datetime.utcnow()}
            }
        )
        
        # Lock account after 5 failed attempts
        if user.get("login_attempts", 0) >= 4:
            lock_until = datetime.utcnow() + timedelta(minutes=30)
            await db.users.update_one(
                {"user_id": user["user_id"]},
                {"$set": {"locked_until": lock_until}}
            )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account deactivated"
        )
    
    # Reset login attempts and create tokens
    token_data = {"user_id": user["user_id"], "email": user["email"]}
    access_token_expires = timedelta(days=7) if login_data.remember_me else None
    access_token = create_access_token(token_data, access_token_expires)
    refresh_token = create_refresh_token(token_data)
    
    # Update user login info
    await db.users.update_one(
        {"user_id": user["user_id"]},
        {
            "$set": {
                "last_login": datetime.utcnow(),
                "login_attempts": 0,
                "locked_until": None
            }
        }
    )
    
    # Log login activity
    await db.login_logs.insert_one({
        "user_id": user["user_id"],
        "email": user["email"],
        "login_time": datetime.utcnow(),
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "success": True
    })
    
    # Create user profile
    user_profile = UserProfile(**{k: v for k, v in user.items() if k != "password_hash"})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_profile=user_profile
    )

@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_access_token(refresh_token: str):
    """Refresh access token"""
    
    payload = verify_token(refresh_token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = payload.get("user_id")
    user = await db.users.find_one({"user_id": user_id})
    
    if not user or not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    token_data = {"user_id": user["user_id"], "email": user["email"]}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    
    user_profile = UserProfile(**{k: v for k, v in user.items() if k != "password_hash"})
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_profile=user_profile
    )

@router.post("/logout")
async def logout_user(current_user: UserProfile = Depends(get_current_user)):
    """User logout (token invalidation would require token blacklist)"""
    
    # Log logout activity
    await db.login_logs.insert_one({
        "user_id": current_user.user_id,
        "email": current_user.email,
        "logout_time": datetime.utcnow(),
        "action": "logout"
    })
    
    return {"message": "Successfully logged out"}

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: UserProfile = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_update: UserUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Update user profile"""
    
    update_data = {k: v for k, v in profile_update.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.users.update_one(
        {"user_id": current_user.user_id},
        {"$set": update_data}
    )
    
    # Get updated user
    updated_user = await db.users.find_one({"user_id": current_user.user_id})
    return UserProfile(**{k: v for k, v in updated_user.items() if k != "password_hash"})

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: UserProfile = Depends(get_current_user)
):
    """Change user password"""
    
    # Get user with password hash
    user = await db.users.find_one({"user_id": current_user.user_id})
    
    # Verify current password
    if not verify_password(password_data.current_password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Hash new password
    new_password_hash = hash_password(password_data.new_password)
    
    # Update password
    await db.users.update_one(
        {"user_id": current_user.user_id},
        {
            "$set": {
                "password_hash": new_password_hash,
                "password_changed_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Password changed successfully"}

@router.post("/request-password-reset")
async def request_password_reset(reset_request: PasswordReset):
    """Request password reset (would send email in production)"""
    
    user = await db.users.find_one({"email": reset_request.email})
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, you will receive password reset instructions"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    reset_expires = datetime.utcnow() + timedelta(hours=1)
    
    # Store reset token
    await db.users.update_one(
        {"user_id": user["user_id"]},
        {
            "$set": {
                "reset_token": reset_token,
                "reset_token_expires": reset_expires
            }
        }
    )
    
    # In production, send email with reset link
    # For now, return token (remove in production)
    return {
        "message": "Password reset instructions sent to email",
        "reset_token": reset_token  # Remove this in production
    }

# Admin endpoints
@router.get("/admin/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all users (admin only)"""
    
    users = await db.users.find({}, {"password_hash": 0}).skip(skip).limit(limit).to_list(length=limit)
    total_users = await db.users.count_documents({})
    
    return {
        "users": users,
        "total": total_users,
        "skip": skip,
        "limit": limit
    }

@router.put("/admin/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    new_role: UserRole,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Update user role (admin only)"""
    
    # Prevent non-super-admin from creating super-admin
    if new_role == UserRole.SUPER_ADMIN and current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super-admin can assign super-admin role"
        )
    
    result = await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"role": new_role, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"User role updated to {new_role}"}

@router.put("/admin/users/{user_id}/subscription")
async def update_user_subscription(
    user_id: str,
    new_tier: SubscriptionTier,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Update user subscription tier (admin only)"""
    
    result = await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"subscription_tier": new_tier, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"User subscription updated to {new_tier}"}

@router.delete("/admin/users/{user_id}")
async def deactivate_user(
    user_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Deactivate user account (admin only)"""
    
    # Prevent self-deactivation
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    result = await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"is_active": False, "deactivated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User account deactivated"}

# Module access check endpoint
@router.get("/check-access/{module_name}")
async def check_module_access_endpoint(
    module_name: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Check if current user has access to specific module"""
    
    has_access = check_module_access(current_user, module_name)
    
    return {
        "module": module_name,
        "has_access": has_access,
        "user_role": current_user.role,
        "subscription_tier": current_user.subscription_tier
    }

# Initialize default super admin (for first setup)
async def create_default_admin():
    """Create default super admin if none exists"""
    
    admin_exists = await db.users.find_one({"role": UserRole.SUPER_ADMIN})
    if not admin_exists:
        admin_user = {
            "user_id": "admin_" + secrets.token_urlsafe(8),
            "email": "admin@customermindiq.com",
            "password_hash": hash_password("CustomerMindIQ2025!"),
            "first_name": "Super",
            "last_name": "Administrator",
            "company_name": "Customer Mind IQ",
            "phone": None,
            "role": UserRole.SUPER_ADMIN,
            "subscription_tier": SubscriptionTier.ENTERPRISE,
            "is_active": True,
            "email_verified": True,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "profile_picture": None,
            "login_attempts": 0,
            "locked_until": None
        }
        
        await db.users.insert_one(admin_user)
        return admin_user["user_id"]
    
    return None

# Export router and utility functions
__all__ = ["router", "get_current_user", "require_role", "require_subscription", "check_module_access", "create_default_admin"]