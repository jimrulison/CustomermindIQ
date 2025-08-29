"""
Customer Mind IQ - Advanced Admin System
Banner management, discount system, account impersonation, and analytics dashboard
"""

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Optional, List, Union, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid
import os
from motor.motor_asyncio import AsyncIOMotorClient
from auth.auth_system import get_current_user, require_role, UserRole, UserProfile, SubscriptionTier

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.customer_mind_iq

router = APIRouter()

# Enums
class BannerType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"
    ANNOUNCEMENT = "announcement"
    TRAINING = "training"
    MAINTENANCE = "maintenance"

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    FREE_MONTHS = "free_months"
    UPGRADE_DISCOUNT = "upgrade_discount"

class BannerStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SCHEDULED = "scheduled"
    EXPIRED = "expired"
    PAUSED = "paused"

# Pydantic Models
class BannerCreate(BaseModel):
    title: str = Field(..., max_length=200)
    message: str = Field(..., max_length=1000)
    banner_type: BannerType = BannerType.INFO
    target_users: List[str] = Field(default_factory=list)  # Empty = all users
    target_tiers: List[SubscriptionTier] = Field(default_factory=list)  # Empty = all tiers
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_dismissible: bool = True
    priority: int = Field(default=0, ge=0, le=10)  # 0-10, 10 is highest
    call_to_action: Optional[str] = None
    cta_url: Optional[str] = None

class BannerUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    banner_type: Optional[BannerType] = None
    target_users: Optional[List[str]] = None
    target_tiers: Optional[List[SubscriptionTier]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_dismissible: Optional[bool] = None
    priority: Optional[int] = None
    call_to_action: Optional[str] = None
    cta_url: Optional[str] = None
    status: Optional[BannerStatus] = None

class Banner(BaseModel):
    banner_id: str
    title: str
    message: str
    banner_type: BannerType
    status: BannerStatus
    target_users: List[str]
    target_tiers: List[SubscriptionTier]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    is_dismissible: bool
    priority: int
    call_to_action: Optional[str]
    cta_url: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime
    views: int = 0
    clicks: int = 0
    dismissals: int = 0

class DiscountCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    discount_type: DiscountType
    value: float = Field(..., gt=0)  # Percentage (1-100) or fixed amount
    target_tiers: List[SubscriptionTier] = Field(default_factory=list)
    target_users: List[str] = Field(default_factory=list)  # Specific user emails
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None  # Max number of uses
    per_user_limit: Optional[int] = 1  # Max uses per user
    minimum_purchase: Optional[float] = None
    is_active: bool = True

class DiscountUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    target_tiers: Optional[List[SubscriptionTier]] = None
    target_users: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    per_user_limit: Optional[int] = None
    minimum_purchase: Optional[float] = None
    is_active: Optional[bool] = None

class Discount(BaseModel):
    discount_id: str
    name: str
    description: str
    discount_type: DiscountType
    value: float
    target_tiers: List[SubscriptionTier]
    target_users: List[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    usage_limit: Optional[int]
    per_user_limit: int
    minimum_purchase: Optional[float]
    is_active: bool
    created_by: str
    created_at: datetime
    updated_at: datetime
    total_uses: int = 0
    total_revenue_impact: float = 0.0

class ImpersonationRequest(BaseModel):
    target_user_id: str
    reason: str = Field(..., max_length=500)
    duration_minutes: int = Field(default=60, ge=5, le=480)  # 5 minutes to 8 hours

class ImpersonationSession(BaseModel):
    session_id: str
    admin_user_id: str
    target_user_id: str
    reason: str
    start_time: datetime
    end_time: datetime
    is_active: bool
    admin_actions: List[Dict[str, Any]] = Field(default_factory=list)

# Banner Management Endpoints
@router.post("/admin/banners", response_model=Banner)
async def create_banner(
    banner_data: BannerCreate,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new banner announcement"""
    
    banner_id = str(uuid.uuid4())
    
    # Determine status based on dates
    now = datetime.utcnow()
    if banner_data.start_date and banner_data.start_date > now:
        status = BannerStatus.SCHEDULED
    elif banner_data.end_date and banner_data.end_date < now:
        status = BannerStatus.EXPIRED
    else:
        status = BannerStatus.ACTIVE
    
    banner_doc = {
        "banner_id": banner_id,
        "title": banner_data.title,
        "message": banner_data.message,
        "banner_type": banner_data.banner_type,
        "status": status,
        "target_users": banner_data.target_users,
        "target_tiers": banner_data.target_tiers,
        "start_date": banner_data.start_date,
        "end_date": banner_data.end_date,
        "is_dismissible": banner_data.is_dismissible,
        "priority": banner_data.priority,
        "call_to_action": banner_data.call_to_action,
        "cta_url": banner_data.cta_url,
        "created_by": current_user.user_id,
        "created_at": now,
        "updated_at": now,
        "views": 0,
        "clicks": 0,
        "dismissals": 0
    }
    
    await db.banners.insert_one(banner_doc)
    
    return Banner(**banner_doc)

@router.get("/admin/banners")
async def get_all_banners(
    status: Optional[BannerStatus] = None,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all banners (admin only)"""
    
    query = {}
    if status:
        query["status"] = status
    
    banners = await db.banners.find(query).sort("priority", -1).to_list(length=100)
    
    return {
        "banners": banners,
        "total": len(banners)
    }

@router.get("/banners/active")
async def get_active_banners(
    current_user: UserProfile = Depends(get_current_user)
):
    """Get active banners for current user"""
    
    now = datetime.utcnow()
    
    # Query for active banners
    query = {
        "$and": [
            {"status": BannerStatus.ACTIVE},
            {
                "$or": [
                    {"start_date": {"$lte": now}},
                    {"start_date": None}
                ]
            },
            {
                "$or": [
                    {"end_date": {"$gte": now}},
                    {"end_date": None}
                ]
            }
        ]
    }
    
    banners = await db.banners.find(query).sort("priority", -1).to_list(length=50)
    
    # Filter by user and tier targeting
    filtered_banners = []
    for banner in banners:
        # Check if banner targets this user specifically
        if banner["target_users"] and current_user.email not in banner["target_users"]:
            continue
        
        # Check if banner targets this user's tier
        if banner["target_tiers"] and current_user.subscription_tier not in banner["target_tiers"]:
            continue
        
        filtered_banners.append(banner)
    
    return {
        "banners": filtered_banners,
        "count": len(filtered_banners)
    }

@router.put("/admin/banners/{banner_id}")
async def update_banner(
    banner_id: str,
    banner_update: BannerUpdate,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Update banner"""
    
    update_data = {k: v for k, v in banner_update.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.banners.update_one(
        {"banner_id": banner_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found"
        )
    
    updated_banner = await db.banners.find_one({"banner_id": banner_id})
    return Banner(**updated_banner)

@router.delete("/admin/banners/{banner_id}")
async def delete_banner(
    banner_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Delete banner"""
    
    result = await db.banners.delete_one({"banner_id": banner_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banner not found"
        )
    
    return {"message": "Banner deleted successfully"}

@router.post("/banners/{banner_id}/track")
async def track_banner_interaction(
    banner_id: str,
    action: str,  # "view", "click", "dismiss"
    current_user: UserProfile = Depends(get_current_user)
):
    """Track banner interactions for analytics"""
    
    # Update banner statistics
    update_field = f"{action}s"
    if action in ["view", "click", "dismiss"]:
        await db.banners.update_one(
            {"banner_id": banner_id},
            {"$inc": {update_field: 1}}
        )
        
        # Log interaction for detailed analytics
        await db.banner_interactions.insert_one({
            "banner_id": banner_id,
            "user_id": current_user.user_id,
            "action": action,
            "timestamp": datetime.utcnow(),
            "user_tier": current_user.subscription_tier
        })
    
    return {"message": f"Banner {action} tracked"}

# Discount Management Endpoints
@router.post("/admin/discounts", response_model=Discount)
async def create_discount(
    discount_data: DiscountCreate,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new discount"""
    
    discount_id = str(uuid.uuid4())
    
    discount_doc = {
        "discount_id": discount_id,
        "name": discount_data.name,
        "description": discount_data.description,
        "discount_type": discount_data.discount_type,
        "value": discount_data.value,
        "target_tiers": discount_data.target_tiers,
        "target_users": discount_data.target_users,
        "start_date": discount_data.start_date,
        "end_date": discount_data.end_date,
        "usage_limit": discount_data.usage_limit,
        "per_user_limit": discount_data.per_user_limit,
        "minimum_purchase": discount_data.minimum_purchase,
        "is_active": discount_data.is_active,
        "created_by": current_user.user_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "total_uses": 0,
        "total_revenue_impact": 0.0
    }
    
    await db.discounts.insert_one(discount_doc)
    
    return Discount(**discount_doc)

@router.get("/admin/discounts")
async def get_all_discounts(
    active_only: bool = False,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all discounts (admin only)"""
    
    query = {}
    if active_only:
        query["is_active"] = True
    
    discounts = await db.discounts.find(query).sort("created_at", -1).to_list(length=100)
    
    return {
        "discounts": discounts,
        "total": len(discounts)
    }

@router.get("/discounts/available")
async def get_available_discounts(
    tier: Optional[SubscriptionTier] = None,
    current_user: UserProfile = Depends(get_current_user)
):
    """Get available discounts for current user"""
    
    now = datetime.utcnow()
    target_tier = tier or current_user.subscription_tier
    
    # Query for active discounts
    query = {
        "is_active": True,
        "$and": [
            {
                "$or": [
                    {"start_date": {"$lte": now}},
                    {"start_date": None}
                ]
            },
            {
                "$or": [
                    {"end_date": {"$gte": now}},
                    {"end_date": None}
                ]
            }
        ]
    }
    
    discounts = await db.discounts.find(query).to_list(length=50)
    
    # Filter by user and tier targeting
    available_discounts = []
    for discount in discounts:
        # Check tier targeting
        if discount["target_tiers"] and target_tier not in discount["target_tiers"]:
            continue
        
        # Check user targeting
        if discount["target_users"] and current_user.email not in discount["target_users"]:
            continue
        
        # Check usage limits
        user_usage = await db.discount_usage.count_documents({
            "discount_id": discount["discount_id"],
            "user_id": current_user.user_id
        })
        
        if user_usage >= discount["per_user_limit"]:
            continue
        
        if discount["usage_limit"] and discount["total_uses"] >= discount["usage_limit"]:
            continue
        
        available_discounts.append(discount)
    
    return {
        "discounts": available_discounts,
        "count": len(available_discounts)
    }

@router.post("/admin/discounts/{discount_id}/apply/{user_id}")
async def apply_discount_to_user(
    discount_id: str,
    user_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Apply discount to specific user (admin only)"""
    
    # Get discount details
    discount = await db.discounts.find_one({"discount_id": discount_id})
    if not discount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discount not found"
        )
    
    # Check if user exists
    target_user = await db.users.find_one({"user_id": user_id})
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Record discount application
    usage_record = {
        "usage_id": str(uuid.uuid4()),
        "discount_id": discount_id,
        "user_id": user_id,
        "applied_by": current_user.user_id,
        "applied_at": datetime.utcnow(),
        "discount_amount": discount["value"],
        "discount_type": discount["discount_type"]
    }
    
    await db.discount_usage.insert_one(usage_record)
    
    # Update discount usage statistics
    await db.discounts.update_one(
        {"discount_id": discount_id},
        {"$inc": {"total_uses": 1}}
    )
    
    return {
        "message": f"Discount applied to user {target_user['email']}",
        "usage_record": usage_record
    }

# Account Impersonation Endpoints
@router.post("/admin/impersonate", response_model=ImpersonationSession)
async def start_impersonation_session(
    impersonation_request: ImpersonationRequest,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Start impersonation session for customer support"""
    
    # Verify target user exists
    target_user = await db.users.find_one({"user_id": impersonation_request.target_user_id})
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target user not found"
        )
    
    # Prevent impersonating other admins (unless super admin)
    if (target_user["role"] in [UserRole.ADMIN, UserRole.SUPER_ADMIN] and 
        current_user.role != UserRole.SUPER_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot impersonate admin users"
        )
    
    session_id = str(uuid.uuid4())
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=impersonation_request.duration_minutes)
    
    session_doc = {
        "session_id": session_id,
        "admin_user_id": current_user.user_id,
        "target_user_id": impersonation_request.target_user_id,
        "reason": impersonation_request.reason,
        "start_time": start_time,
        "end_time": end_time,
        "is_active": True,
        "admin_actions": []
    }
    
    await db.impersonation_sessions.insert_one(session_doc)
    
    # Log the impersonation start
    await db.admin_audit_log.insert_one({
        "admin_user_id": current_user.user_id,
        "action": "impersonation_started",
        "target_user_id": impersonation_request.target_user_id,
        "session_id": session_id,
        "reason": impersonation_request.reason,
        "timestamp": start_time
    })
    
    return ImpersonationSession(**session_doc)

@router.post("/admin/impersonate/{session_id}/end")
async def end_impersonation_session(
    session_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """End impersonation session"""
    
    session = await db.impersonation_sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Impersonation session not found"
        )
    
    if session["admin_user_id"] != current_user.user_id and current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot end another admin's impersonation session"
        )
    
    # End the session
    await db.impersonation_sessions.update_one(
        {"session_id": session_id},
        {"$set": {"is_active": False, "actual_end_time": datetime.utcnow()}}
    )
    
    # Log the impersonation end
    await db.admin_audit_log.insert_one({
        "admin_user_id": current_user.user_id,
        "action": "impersonation_ended",
        "target_user_id": session["target_user_id"],
        "session_id": session_id,
        "timestamp": datetime.utcnow()
    })
    
    return {"message": "Impersonation session ended"}

@router.get("/admin/impersonation/active")
async def get_active_impersonation_sessions(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get active impersonation sessions"""
    
    query = {"is_active": True}
    if current_user.role != UserRole.SUPER_ADMIN:
        query["admin_user_id"] = current_user.user_id
    
    sessions = await db.impersonation_sessions.find(query).to_list(length=50)
    
    # Add target user info
    for session in sessions:
        target_user = await db.users.find_one(
            {"user_id": session["target_user_id"]},
            {"email": 1, "first_name": 1, "last_name": 1, "subscription_tier": 1}
        )
        session["target_user_info"] = target_user
    
    return {
        "sessions": sessions,
        "count": len(sessions)
    }

# Analytics Dashboard Endpoints
@router.get("/admin/analytics/dashboard")
async def get_admin_analytics_dashboard(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get comprehensive admin analytics dashboard"""
    
    # User statistics by tier
    pipeline = [
        {
            "$group": {
                "_id": "$subscription_tier",
                "count": {"$sum": 1},
                "active_count": {
                    "$sum": {"$cond": [{"$eq": ["$is_active", True]}, 1, 0]}
                }
            }
        }
    ]
    
    tier_stats = await db.users.aggregate(pipeline).to_list(length=10)
    
    # Historical user growth (last 12 months)
    monthly_growth = []
    for i in range(12):
        start_date = datetime.utcnow().replace(day=1) - timedelta(days=30 * i)
        end_date = start_date + timedelta(days=32)  # Ensure we get the full month
        
        monthly_users = await db.users.count_documents({
            "created_at": {
                "$gte": start_date,
                "$lt": end_date
            }
        })
        
        monthly_growth.insert(0, {
            "month": start_date.strftime("%Y-%m"),
            "new_users": monthly_users
        })
    
    # Cancellation statistics
    cancelled_users = await db.users.count_documents({"is_active": False})
    
    # Revenue analytics (mock data - integrate with Stripe in production)
    total_revenue = 0
    revenue_by_tier = {}
    
    for tier_stat in tier_stats:
        tier = tier_stat["_id"]
        count = tier_stat["active_count"]
        
        # Mock pricing for revenue calculation
        tier_prices = {
            SubscriptionTier.FREE: 0,
            SubscriptionTier.PROFESSIONAL: 299,
            SubscriptionTier.ENTERPRISE: 799
        }
        
        tier_revenue = count * tier_prices.get(tier, 0)
        revenue_by_tier[tier] = tier_revenue
        total_revenue += tier_revenue
    
    # Banner analytics
    banner_stats = await db.banners.aggregate([
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "total_views": {"$sum": "$views"},
                "total_clicks": {"$sum": "$clicks"}
            }
        }
    ]).to_list(length=10)
    
    # Discount analytics
    discount_stats = await db.discounts.aggregate([
        {
            "$group": {
                "_id": "$discount_type",
                "count": {"$sum": 1},
                "total_uses": {"$sum": "$total_uses"},
                "total_impact": {"$sum": "$total_revenue_impact"}
            }
        }
    ]).to_list(length=10)
    
    # Recent admin activities
    recent_activities = await db.admin_audit_log.find({}).sort("timestamp", -1).limit(20).to_list(length=20)
    
    return {
        "user_statistics": {
            "by_tier": tier_stats,
            "total_users": sum(stat["count"] for stat in tier_stats),
            "active_users": sum(stat["active_count"] for stat in tier_stats),
            "cancelled_users": cancelled_users,
            "monthly_growth": monthly_growth
        },
        "revenue_analytics": {
            "total_monthly_revenue": total_revenue,
            "revenue_by_tier": revenue_by_tier,
            "average_revenue_per_user": total_revenue / max(sum(stat["active_count"] for stat in tier_stats), 1)
        },
        "banner_analytics": {
            "by_status": banner_stats,
            "total_banners": sum(stat["count"] for stat in banner_stats),
            "total_engagement": sum(stat["total_views"] + stat["total_clicks"] for stat in banner_stats)
        },
        "discount_analytics": {
            "by_type": discount_stats,
            "total_discounts": sum(stat["count"] for stat in discount_stats),
            "total_uses": sum(stat["total_uses"] for stat in discount_stats)
        },
        "recent_activities": recent_activities,
        "generated_at": datetime.utcnow()
    }

@router.get("/admin/analytics/users")
async def get_user_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get detailed user analytics"""
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # User acquisition over time
    daily_signups = await db.users.aggregate([
        {
            "$match": {
                "created_at": {"$gte": start_date, "$lte": end_date}
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_at"
                    }
                },
                "signups": {"$sum": 1},
                "by_tier": {
                    "$push": "$subscription_tier"
                }
            }
        },
        {"$sort": {"_id": 1}}
    ]).to_list(length=100)
    
    # Churn analysis
    churn_data = await db.users.aggregate([
        {
            "$match": {
                "is_active": False,
                "deactivated_at": {"$gte": start_date, "$lte": end_date}
            }
        },
        {
            "$group": {
                "_id": "$subscription_tier",
                "churned_count": {"$sum": 1}
            }
        }
    ]).to_list(length=10)
    
    # Login frequency analysis
    login_frequency = await db.login_logs.aggregate([
        {
            "$match": {
                "login_time": {"$gte": start_date, "$lte": end_date},
                "success": True
            }
        },
        {
            "$group": {
                "_id": "$user_id",
                "login_count": {"$sum": 1},
                "last_login": {"$max": "$login_time"}
            }
        },
        {
            "$group": {
                "_id": {
                    "$switch": {
                        "branches": [
                            {"case": {"$gte": ["$login_count", 20]}, "then": "very_active"},
                            {"case": {"$gte": ["$login_count", 10]}, "then": "active"},
                            {"case": {"$gte": ["$login_count", 5]}, "then": "moderate"},
                            {"case": {"$gte": ["$login_count", 1]}, "then": "low"}
                        ],
                        "default": "inactive"
                    }
                },
                "user_count": {"$sum": 1}
            }
        }
    ]).to_list(length=10)
    
    return {
        "date_range": {
            "start_date": start_date,
            "end_date": end_date
        },
        "daily_signups": daily_signups,
        "churn_analysis": churn_data,
        "login_frequency": login_frequency,
        "generated_at": datetime.utcnow()
    }

# Export router
__all__ = ["router"]