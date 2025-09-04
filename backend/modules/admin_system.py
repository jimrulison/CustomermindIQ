"""
Customer Mind IQ - Advanced Admin System
Banner management, discount system, account impersonation, and analytics dashboard
"""

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Query, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Optional, List, Union, Any
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import os
import csv
import io
import uuid
import re
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from auth.auth_system import get_current_user, require_role, UserRole, UserProfile, SubscriptionTier

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

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

# New Enhanced Models

class DiscountCode(BaseModel):
    code_id: str
    discount_id: str
    code: str
    is_active: bool
    usage_count: int
    max_uses: Optional[int] = None
    created_at: datetime
    expires_at: Optional[datetime] = None

class UserSearchFilter(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None
    subscription_tier: Optional[SubscriptionTier] = None
    registration_date_from: Optional[datetime] = None
    registration_date_to: Optional[datetime] = None
    is_active: Optional[bool] = None
    has_subscription: Optional[bool] = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)

class BulkDiscountApplication(BaseModel):
    discount_id: str
    target_criteria: Dict[str, Any]  # Filtering criteria for users
    notify_users: bool = Field(default=True)
    reason: str

class DiscountRule(BaseModel):
    rule_id: str
    name: str
    description: str
    trigger_conditions: Dict[str, Any]
    discount_config: Dict[str, Any]
    is_active: bool
    created_at: datetime
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0

class UserCohort(BaseModel):
    cohort_id: str
    name: str
    definition: Dict[str, Any]
    user_count: int
    created_at: datetime
    metrics: Dict[str, Any]

class EmailTemplate(BaseModel):
    template_id: str
    name: str
    subject: str
    html_content: str
    text_content: str
    template_type: str  # discount_applied, banner_notification, etc.
    variables: List[str]  # Available template variables
    is_active: bool
    created_at: datetime
    last_modified: datetime

class APIKeyConfig(BaseModel):
    key_id: str
    service_name: str
    key_value: str
    description: str
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime] = None
    usage_count: int = 0

class WorkflowStep(BaseModel):
    step_id: str
    step_type: str  # condition, action, delay
    config: Dict[str, Any]
    order: int

class AutomatedWorkflow(BaseModel):
    workflow_id: str
    name: str
    description: str
    trigger_event: str
    steps: List[WorkflowStep]
    is_active: bool
    created_at: datetime
    execution_count: int = 0
    last_executed: Optional[datetime] = None

class ExportRequest(BaseModel):
    export_type: str  # users, discounts, banners, analytics
    filters: Dict[str, Any]
    format: str = Field(default="csv")  # csv, json, xlsx
    date_range: Optional[Dict[str, datetime]] = None

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
    
    # Convert ObjectId to string for JSON serialization
    for banner in banners:
        if "_id" in banner:
            del banner["_id"]  # Remove MongoDB ObjectId
    
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
        # Remove ObjectId
        if "_id" in banner:
            del banner["_id"]
            
        # Check if banner targets this user specifically
        if banner.get("target_users") and current_user.email not in banner["target_users"]:
            continue
        
        # Check if banner targets this user's tier
        if banner.get("target_tiers") and current_user.subscription_tier not in banner["target_tiers"]:
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

# Announcements endpoints (alias for banners with announcement type)
@router.get("/admin/announcements")
async def get_announcements(
    active_only: bool = Query(False),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all announcements (banners with announcement type)"""
    try:
        # Build query for announcement banners
        query = {"banner_type": "announcement"}
        if active_only:
            query["status"] = "active"
        
        # Get announcements from database
        announcements_cursor = db.banners.find(query).sort("created_at", -1)
        announcements = await announcements_cursor.to_list(length=100)
        
        # Convert ObjectId to string for JSON serialization
        for announcement in announcements:
            announcement["_id"] = str(announcement["_id"])
            if "created_at" in announcement and isinstance(announcement["created_at"], datetime):
                announcement["created_at"] = announcement["created_at"].isoformat()
            if "updated_at" in announcement and isinstance(announcement["updated_at"], datetime):
                announcement["updated_at"] = announcement["updated_at"].isoformat()
        
        return {
            "status": "success",
            "announcements": announcements,
            "total_count": len(announcements)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch announcements: {str(e)}")

@router.post("/admin/announcements")
async def create_announcement(
    title: str,
    message: str,
    priority: int = 1,
    target_roles: Optional[List[str]] = None,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new announcement"""
    try:
        announcement_data = {
            "banner_id": str(uuid.uuid4()),
            "title": title,
            "message": message,
            "banner_type": "announcement",
            "status": "active",
            "priority": priority,
            "target_roles": target_roles or ["user"],
            "created_by": current_user.user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.banners.insert_one(announcement_data)
        
        return {
            "status": "success",
            "message": "Announcement created successfully",
            "announcement_id": announcement_data["banner_id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create announcement: {str(e)}")

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
    
    # Convert ObjectId to string for JSON serialization
    for discount in discounts:
        if "_id" in discount:
            del discount["_id"]  # Remove MongoDB ObjectId
    
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

# ===== BULK DISCOUNT APPLICATION =====

@router.post("/admin/discounts/{discount_id}/bulk-apply")
async def bulk_apply_discount(
    discount_id: str,
    bulk_request: BulkDiscountApplication,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Apply discount to multiple users based on criteria"""
    
    # Verify discount exists
    discount = await db.discounts.find_one({"discount_id": discount_id})
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    
    # Build user query from criteria
    user_query = {}
    criteria = bulk_request.target_criteria
    
    if criteria.get("subscription_tier"):
        user_query["subscription_tier"] = criteria["subscription_tier"]
    
    if criteria.get("registration_date_from"):
        user_query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(criteria["registration_date_from"])
    
    if criteria.get("registration_date_to"):
        user_query.setdefault("created_at", {})["$lte"] = datetime.fromisoformat(criteria["registration_date_to"])
        
    if criteria.get("is_active") is not None:
        user_query["is_active"] = criteria["is_active"]
    
    if criteria.get("email_contains"):
        user_query["email"] = {"$regex": criteria["email_contains"], "$options": "i"}
    
    # Get matching users
    users = await db.users.find(user_query).to_list(length=10000)
    
    if not users:
        return {"message": "No users match the specified criteria", "applied_count": 0}
    
    # Apply discount to each user
    applied_count = 0
    failed_applications = []
    
    for user in users:
        try:
            # Check if user already has this discount
            existing_usage = await db.discount_usage.find_one({
                "user_id": user["user_id"],
                "discount_id": discount_id
            })
            
            if existing_usage:
                continue  # Skip if already applied
            
            # Apply discount
            usage_record = {
                "usage_id": str(uuid.uuid4()),
                "discount_id": discount_id,
                "user_id": user["user_id"],
                "applied_by": current_user.user_id,
                "applied_at": datetime.utcnow(),
                "discount_amount": discount["value"],
                "discount_type": discount["discount_type"],
                "application_reason": bulk_request.reason,
                "is_bulk_applied": True
            }
            
            await db.discount_usage.insert_one(usage_record)
            applied_count += 1
            
            # Send notification if requested
            if bulk_request.notify_users:
                # Add to notification queue (simplified)
                await db.notification_queue.insert_one({
                    "user_id": user["user_id"],
                    "type": "discount_applied",
                    "message": f"You've received a {discount['name']} discount!",
                    "discount_id": discount_id,
                    "created_at": datetime.utcnow(),
                    "status": "pending"
                })
            
        except Exception as e:
            failed_applications.append({
                "user_id": user["user_id"],
                "error": str(e)
            })
    
    # Update discount usage statistics
    await db.discounts.update_one(
        {"discount_id": discount_id},
        {"$inc": {"total_uses": applied_count}}
    )
    
    return {
        "message": f"Discount applied to {applied_count} users",
        "applied_count": applied_count,
        "total_eligible": len(users),
        "failed_applications": failed_applications
    }

# ===== DISCOUNT PERFORMANCE ANALYTICS =====

@router.get("/admin/discounts/{discount_id}/analytics")
async def get_discount_analytics(
    discount_id: str,
    days: int = Query(30, ge=1, le=365),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get detailed analytics for a specific discount"""
    
    # Verify discount exists
    discount = await db.discounts.find_one({"discount_id": discount_id})
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Get usage data
    usage_data = await db.discount_usage.find({
        "discount_id": discount_id,
        "applied_at": {"$gte": date_from}
    }).to_list(length=10000)
    
    # Calculate metrics
    total_uses = len(usage_data)
    unique_users = len(set(usage["user_id"] for usage in usage_data))
    
    # Revenue impact calculation
    revenue_impact = 0.0
    for usage in usage_data:
        if discount["discount_type"] == "percentage":
            # Estimate based on average order value (simplified)
            estimated_order_value = 149.0  # Default monthly subscription
            revenue_impact += (estimated_order_value * discount["value"] / 100)
        elif discount["discount_type"] == "fixed_amount":
            revenue_impact += discount["value"]
        elif discount["discount_type"] == "free_months":
            revenue_impact += (149.0 * discount["value"])  # Monthly value * free months
    
    # Usage over time (daily breakdown)
    usage_by_day = {}
    for usage in usage_data:
        day = usage["applied_at"].strftime("%Y-%m-%d")
        usage_by_day[day] = usage_by_day.get(day, 0) + 1
    
    # Get code-specific analytics if codes exist
    codes_data = await db.discount_codes.find({"discount_id": discount_id}).to_list(length=1000)
    
    return {
        "discount_info": {
            "discount_id": discount_id,
            "name": discount["name"],
            "type": discount["discount_type"],
            "value": discount["value"],
            "created_at": discount["created_at"]
        },
        "usage_metrics": {
            "total_uses": total_uses,
            "unique_users": unique_users,
            "usage_rate": round(total_uses / max(unique_users, 1), 2),
            "revenue_impact": round(revenue_impact, 2)
        },
        "usage_timeline": usage_by_day,
        "codes_metrics": {
            "total_codes_generated": len(codes_data),
            "active_codes": sum(1 for code in codes_data if code["is_active"]),
            "total_code_redemptions": sum(code.get("usage_count", 0) for code in codes_data)
        },
        "period": f"Last {days} days"
    }

# ===== USER COHORT ANALYSIS =====

@router.post("/admin/cohorts/create")
async def create_user_cohort(
    name: str,
    definition: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a user cohort based on specific criteria"""
    
    cohort_id = str(uuid.uuid4())
    
    # Build query from definition
    query = {}
    if definition.get("subscription_tier"):
        query["subscription_tier"] = definition["subscription_tier"]
    
    if definition.get("registration_period"):
        period = definition["registration_period"]
        if period["from"]:
            query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(period["from"])
        if period["to"]:
            query.setdefault("created_at", {})["$lte"] = datetime.fromisoformat(period["to"])
    
    # Get users matching criteria
    users = await db.users.find(query).to_list(length=50000)
    user_count = len(users)
    
    # Calculate cohort metrics
    total_revenue = sum(
        user.get("total_paid", 0) for user in users
    )
    
    avg_revenue_per_user = total_revenue / user_count if user_count > 0 else 0
    
    # Retention analysis (simplified)
    active_users = sum(1 for user in users if user.get("is_active", True))
    retention_rate = (active_users / user_count) * 100 if user_count > 0 else 0
    
    cohort_doc = {
        "cohort_id": cohort_id,
        "name": name,
        "definition": definition,
        "user_count": user_count,
        "created_at": datetime.utcnow(),
        "created_by": current_user.user_id,
        "metrics": {
            "total_revenue": total_revenue,
            "avg_revenue_per_user": round(avg_revenue_per_user, 2),
            "retention_rate": round(retention_rate, 2),
            "active_users": active_users
        }
    }
    
    await db.user_cohorts.insert_one(cohort_doc)
    
    # Remove ObjectId for response
    del cohort_doc["_id"]
    
    return cohort_doc

@router.get("/admin/cohorts")
async def get_user_cohorts(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all user cohorts"""
    
    cohorts = await db.user_cohorts.find({}).sort("created_at", -1).to_list(length=100)
    
    # Remove ObjectIds
    for cohort in cohorts:
        if "_id" in cohort:
            del cohort["_id"]
    
    return {
        "cohorts": cohorts,
        "total": len(cohorts)
    }

@router.get("/admin/cohorts/{cohort_id}/analytics")
async def get_cohort_analytics(
    cohort_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get detailed analytics for a specific cohort"""
    
    cohort = await db.user_cohorts.find_one({"cohort_id": cohort_id})
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    # Recalculate current metrics
    definition = cohort["definition"]
    query = {}
    
    if definition.get("subscription_tier"):
        query["subscription_tier"] = definition["subscription_tier"]
    
    if definition.get("registration_period"):
        period = definition["registration_period"]
        if period.get("from"):
            query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(period["from"])
        if period.get("to"):
            query.setdefault("created_at", {})["$lte"] = datetime.fromisoformat(period["to"])
    
    users = await db.users.find(query).to_list(length=50000)
    
    # Calculate current metrics
    current_metrics = {
        "total_users": len(users),
        "active_users": sum(1 for user in users if user.get("is_active", True)),
        "subscription_distribution": {},
        "revenue_metrics": {}
    }
    
    # Subscription distribution
    for user in users:
        tier = user.get("subscription_tier", "unknown")
        current_metrics["subscription_distribution"][tier] = \
            current_metrics["subscription_distribution"].get(tier, 0) + 1
    
    return {
        "cohort_info": cohort,
        "current_metrics": current_metrics,
        "growth_since_creation": {
            "user_count_change": current_metrics["total_users"] - cohort["user_count"],
            "retention_analysis": "Updated metrics vs original cohort"
        }
    }

# ===== DISCOUNT ROI TRACKING =====

@router.get("/admin/discounts/roi-tracking")
async def get_discount_roi_tracking(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get ROI tracking for all discounts"""
    
    # Set default date range (last 90 days)
    if not date_from:
        date_from = (datetime.utcnow() - timedelta(days=90)).isoformat()
    if not date_to:
        date_to = datetime.utcnow().isoformat()
    
    date_filter = {
        "applied_at": {
            "$gte": datetime.fromisoformat(date_from.replace('Z', '+00:00')),
            "$lte": datetime.fromisoformat(date_to.replace('Z', '+00:00'))
        }
    }
    
    # Get all discount usage in period
    usage_data = await db.discount_usage.find(date_filter).to_list(length=50000)
    
    # Group by discount
    discount_roi = {}
    for usage in usage_data:
        discount_id = usage["discount_id"]
        if discount_id not in discount_roi:
            discount_roi[discount_id] = {
                "discount_id": discount_id,
                "total_uses": 0,
                "revenue_impact": 0.0,
                "users_acquired": set(),
                "conversion_rate": 0.0
            }
        
        discount_roi[discount_id]["total_uses"] += 1
        discount_roi[discount_id]["users_acquired"].add(usage["user_id"])
        
        # Calculate revenue impact
        if usage["discount_type"] == "percentage":
            estimated_value = 149.0 * (usage["discount_amount"] / 100)
        elif usage["discount_type"] == "fixed_amount":
            estimated_value = usage["discount_amount"]
        else:  # free_months
            estimated_value = 149.0 * usage["discount_amount"]
        
        discount_roi[discount_id]["revenue_impact"] += estimated_value
    
    # Get discount details and calculate final metrics
    roi_results = []
    for discount_id, data in discount_roi.items():
        discount = await db.discounts.find_one({"discount_id": discount_id})
        if discount:
            unique_users = len(data["users_acquired"])
            
            # Calculate estimated acquisition cost (simplified)
            estimated_cost = data["revenue_impact"] * 0.3  # Assume 30% cost ratio
            roi_percentage = ((data["revenue_impact"] - estimated_cost) / estimated_cost * 100) if estimated_cost > 0 else 0
            
            roi_results.append({
                "discount_name": discount["name"],
                "discount_id": discount_id,
                "total_uses": data["total_uses"],
                "unique_users": unique_users,
                "revenue_impact": round(data["revenue_impact"], 2),
                "estimated_cost": round(estimated_cost, 2),
                "roi_percentage": round(roi_percentage, 2),
                "cost_per_acquisition": round(estimated_cost / unique_users, 2) if unique_users > 0 else 0
            })
    
    # Sort by ROI percentage
    roi_results.sort(key=lambda x: x["roi_percentage"], reverse=True)
    
    return {
        "roi_tracking": roi_results,
        "period": f"{date_from} to {date_to}",
        "total_discounts_analyzed": len(roi_results)
    }

# ===== EXPORT CAPABILITIES =====

@router.post("/admin/export")
async def export_admin_data(
    export_request: ExportRequest,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Export admin data in various formats"""
    
    export_type = export_request.export_type
    filters = export_request.filters
    format_type = export_request.format
    
    # Build query based on filters
    query = {}
    if filters.get("date_range"):
        date_range = filters["date_range"]
        if date_range.get("from"):
            query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(date_range["from"])
        if date_range.get("to"):
            query.setdefault("created_at", {})["$lte"] = datetime.fromisoformat(date_range["to"])
    
    # Export users data
    if export_type == "users":
        if filters.get("subscription_tier"):
            query["subscription_tier"] = filters["subscription_tier"]
        if filters.get("is_active") is not None:
            query["is_active"] = filters["is_active"]
        
        users = await db.users.find(query).to_list(length=100000)
        
        # Remove sensitive data
        for user in users:
            user.pop("password_hash", None)
            user.pop("_id", None)
        
        if format_type == "csv":
            return _export_to_csv(users, "users_export")
        else:
            return {"data": users, "count": len(users)}
    
    # Export discounts data
    elif export_type == "discounts":
        discounts = await db.discounts.find(query).to_list(length=10000)
        
        # Get usage statistics for each discount
        for discount in discounts:
            discount.pop("_id", None)
            usage_count = await db.discount_usage.count_documents({"discount_id": discount["discount_id"]})
            discount["actual_usage_count"] = usage_count
        
        if format_type == "csv":
            return _export_to_csv(discounts, "discounts_export")
        else:
            return {"data": discounts, "count": len(discounts)}
    
    # Export analytics data
    elif export_type == "analytics":
        # Get comprehensive analytics
        total_users = await db.users.count_documents({})
        total_discounts = await db.discounts.count_documents({})
        total_banners = await db.banners.count_documents({})
        
        analytics_data = [{
            "metric": "Total Users",
            "value": total_users,
            "export_timestamp": datetime.utcnow().isoformat()
        }, {
            "metric": "Total Discounts",
            "value": total_discounts,
            "export_timestamp": datetime.utcnow().isoformat()
        }, {
            "metric": "Total Banners", 
            "value": total_banners,
            "export_timestamp": datetime.utcnow().isoformat()
        }]
        
        if format_type == "csv":
            return _export_to_csv(analytics_data, "analytics_export")
        else:
            return {"data": analytics_data, "count": len(analytics_data)}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid export type")

def _export_to_csv(data, filename):
    """Helper function to export data as CSV"""
    if not data:
        raise HTTPException(status_code=400, detail="No data to export")
    
    # Create CSV content
    output = io.StringIO()
    
    # Get field names from first record
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in data:
        # Convert datetime objects to strings
        cleaned_row = {}
        for key, value in row.items():
            if isinstance(value, datetime):
                cleaned_row[key] = value.isoformat()
            elif isinstance(value, list):
                cleaned_row[key] = ", ".join(str(item) for item in value)
            else:
                cleaned_row[key] = value
        writer.writerow(cleaned_row)
    
    # Create response
    csv_content = output.getvalue()
    output.close()
    
    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"}
    )

# ===== AUTOMATED DISCOUNT RULES =====

@router.post("/admin/discount-rules")
async def create_discount_rule(
    name: str,
    description: str,
    trigger_conditions: Dict[str, Any],
    discount_config: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create automated discount rule"""
    
    rule_id = str(uuid.uuid4())
    
    rule_doc = {
        "rule_id": rule_id,
        "name": name,
        "description": description,
        "trigger_conditions": trigger_conditions,
        "discount_config": discount_config,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "created_by": current_user.user_id,
        "last_triggered": None,  
        "trigger_count": 0
    }
    
    await db.discount_rules.insert_one(rule_doc)
    
    # Remove ObjectId for response
    del rule_doc["_id"]
    
    return rule_doc

@router.get("/admin/discount-rules")
async def get_discount_rules(
    is_active: Optional[bool] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all discount rules"""
    
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    rules = await db.discount_rules.find(query).sort("created_at", -1).to_list(length=100)
    
    # Remove ObjectIds
    for rule in rules:
        if "_id" in rule:
            del rule["_id"]
    
    return {
        "rules": rules,
        "total": len(rules)
    }

# ===== EMAIL TEMPLATES MANAGEMENT =====

@router.post("/admin/email-templates")
async def create_email_template(
    template_data: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new email template"""
    
    template_id = str(uuid.uuid4())
    
    template_doc = {
        "template_id": template_id,
        "name": template_data.get("name", ""),
        "subject": template_data.get("subject", ""),
        "html_content": template_data.get("html_content", ""),
        "text_content": template_data.get("text_content", ""),
        "template_type": template_data.get("template_type", "general"),
        "variables": template_data.get("variables", []),
        "is_active": template_data.get("is_active", True),
        "created_at": datetime.utcnow(),
        "last_modified": datetime.utcnow(),
        "created_by": current_user.user_id
    }
    
    await db.email_templates.insert_one(template_doc)
    
    # Remove ObjectId for response
    del template_doc["_id"]
    
    return template_doc

@router.get("/admin/email-templates")
async def get_email_templates(
    template_type: Optional[str] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all email templates"""
    
    query = {}
    if template_type:
        query["template_type"] = template_type
    
    templates = await db.email_templates.find(query).sort("created_at", -1).to_list(length=100)
    
    # Remove ObjectIds
    for template in templates:
        if "_id" in template:
            del template["_id"]
    
    return {
        "templates": templates,
        "total": len(templates)
    }

# ===== API KEYS MANAGEMENT =====

@router.post("/admin/api-keys")
async def create_api_key(
    service_name: str,
    key_value: str,
    description: str,
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))  # Super admin only
):
    """Create a new API key configuration"""
    
    key_id = str(uuid.uuid4())
    
    key_doc = {
        "key_id": key_id,
        "service_name": service_name,
        "key_value": key_value,  # In production, this should be encrypted
        "description": description,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "created_by": current_user.user_id,
        "last_used": None,
        "usage_count": 0
    }
    
    await db.api_keys.insert_one(key_doc)
    
    # Remove sensitive data and ObjectId for response
    response_data = key_doc.copy()
    response_data["key_value"] = "***HIDDEN***"  # Hide actual key value
    del response_data["_id"]
    
    return response_data

@router.get("/admin/api-keys")
async def get_api_keys(
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Get all API keys (super admin only)"""
    
    keys = await db.api_keys.find({}).sort("created_at", -1).to_list(length=100)
    
    # Remove sensitive data and ObjectIds
    for key in keys:
        key["key_value"] = "***HIDDEN***"
        if "_id" in key:
            del key["_id"]
    
    return {
        "api_keys": keys,
        "total": len(keys)
    }

# ===== AUTOMATED WORKFLOWS =====

@router.post("/admin/workflows")
async def create_automated_workflow(
    workflow_data: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new automated workflow"""
    
    workflow_id = str(uuid.uuid4())
    
    # Convert steps to WorkflowStep objects
    workflow_steps = []
    steps = workflow_data.get("steps", [])
    for i, step in enumerate(steps):
        workflow_steps.append({
            "step_id": str(uuid.uuid4()),
            "step_type": step.get("step_type", "action"),
            "config": step.get("config", {}),
            "order": i
        })
    
    workflow_doc = {
        "workflow_id": workflow_id,
        "name": workflow_data.get("name", ""),
        "description": workflow_data.get("description", ""),
        "trigger_event": workflow_data.get("trigger_event", "manual"),
        "steps": workflow_steps,
        "is_active": workflow_data.get("is_active", True),
        "created_at": datetime.utcnow(),
        "created_by": current_user.user_id,
        "execution_count": 0,
        "last_executed": None
    }
    
    await db.automated_workflows.insert_one(workflow_doc)
    
    # Remove ObjectId for response
    del workflow_doc["_id"]
    
    return workflow_doc

@router.get("/admin/workflows")
async def get_automated_workflows(
    is_active: Optional[bool] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all automated workflows"""
    
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    workflows = await db.automated_workflows.find(query).sort("created_at", -1).to_list(length=100)
    
    # Remove ObjectIds
    for workflow in workflows:
        if "_id" in workflow:
            del workflow["_id"]
    
    return {
        "workflows": workflows,
        "total": len(workflows)
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
    
    return {"message": "Impersonation session ended successfully"}

# ===== ENHANCED USER MANAGEMENT ENDPOINTS =====

# Simple users list endpoint that frontend expects
@router.get("/admin/users")
async def get_all_users(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all users - simplified endpoint for admin portal"""
    try:
        # Get users from database
        users_cursor = db.users.find({}).skip(offset).limit(limit)
        users = await users_cursor.to_list(length=limit)
        
        # Convert ObjectId to string and format response
        for user in users:
            user["_id"] = str(user["_id"])
            if "created_at" in user and isinstance(user["created_at"], datetime):
                user["created_at"] = user["created_at"].isoformat()
        
        return {
            "status": "success",
            "users": users,
            "total_count": await db.users.count_documents({}),
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

# Simple customers endpoint (alias for users)
@router.get("/admin/customers")
async def get_all_customers(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all customers - alias for users endpoint"""
    return await get_all_users(limit, offset, current_user)

@router.get("/admin/users/search")
async def search_users(
    email: Optional[str] = Query(None),
    role: Optional[UserRole] = Query(None),
    subscription_tier: Optional[SubscriptionTier] = Query(None),
    registration_from: Optional[str] = Query(None),
    registration_to: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    has_subscription: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Advanced user search and filtering"""
    
    # Build query
    query = {}
    
    if email:
        query["email"] = {"$regex": email, "$options": "i"}
    
    if role:
        query["role"] = role
    
    if subscription_tier:
        query["subscription_tier"] = subscription_tier
    
    if is_active is not None:
        query["is_active"] = is_active
    
    if has_subscription is not None:
        if has_subscription:
            query["subscription_tier"] = {"$in": [SubscriptionTier.MONTHLY, SubscriptionTier.ANNUAL]}
        else:
            query["subscription_tier"] = SubscriptionTier.FREE_TRIAL
            
    # Date range filtering
    if registration_from or registration_to:
        date_query = {}
        if registration_from:
            date_query["$gte"] = datetime.fromisoformat(registration_from.replace('Z', '+00:00'))
        if registration_to:
            date_query["$lte"] = datetime.fromisoformat(registration_to.replace('Z', '+00:00'))
        query["created_at"] = date_query
    
    # Execute search with pagination
    cursor = db.users.find(query).sort("created_at", -1).skip(offset).limit(limit)
    users = await cursor.to_list(length=limit)
    
    # Get total count for pagination
    total_count = await db.users.count_documents(query)
    
    # Remove sensitive data and ObjectIds
    for user in users:
        if "_id" in user:
            del user["_id"]
        if "password_hash" in user:
            del user["password_hash"]
    
    return {
        "users": users,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "has_more": total_count > (offset + limit)
    }

@router.get("/admin/users/{user_id}/analytics")
async def get_user_analytics(
    user_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get detailed analytics for a specific user"""
    
    # Verify user exists
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate user metrics with proper error handling
    try:
        user_analytics = {
            "user_profile": {
                "user_id": user["user_id"],
                "email": user["email"],
                "role": user.get("role", "user"),
                "subscription_tier": user.get("subscription_tier", "free_trial"),
                "created_at": user.get("created_at"),
                "is_active": user.get("is_active", True)
            },
            "activity_metrics": {
                "total_logins": 0,
                "last_login": None,
                "session_count_30d": 0,
                "features_used": []
            },
            "subscription_metrics": {
                "subscription_start": user.get("subscription_start"),
                "subscription_end": user.get("subscription_end"),
                "payments_made": 0,
                "total_revenue": 0.0,
                "discounts_used": []
            },
            "support_metrics": {
                "support_tickets": 0,
                "last_support_contact": None,
                "impersonation_sessions": 0
            }
        }
        
        # Try to get activity data (handle if collections don't exist)
        try:
            user_analytics["activity_metrics"]["total_logins"] = await db.user_activities.count_documents({"user_id": user_id, "activity_type": "login"})
        except:
            pass
            
        # Try to get last login
        try:
            last_login = await db.user_activities.find_one(
                {"user_id": user_id, "activity_type": "login"},
                sort=[("timestamp", -1)]
            )
            if last_login:
                user_analytics["activity_metrics"]["last_login"] = last_login["timestamp"]
        except:
            pass
        
        # Try to get session count (last 30 days)
        try:
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            user_analytics["activity_metrics"]["session_count_30d"] = await db.user_activities.count_documents({
                "user_id": user_id,
                "activity_type": "login",
                "timestamp": {"$gte": thirty_days_ago}
            })
        except:
            pass
        
        # Try to get payment information
        try:
            payments = await db.payments.find({"user_id": user_id}).to_list(length=100)
            user_analytics["subscription_metrics"]["payments_made"] = len(payments)
            user_analytics["subscription_metrics"]["total_revenue"] = sum(p.get("amount", 0) for p in payments)
        except:
            pass
        
        # Try to get discount usage
        try:
            discount_usage = await db.discount_usage.find({"user_id": user_id}).to_list(length=50)
            user_analytics["subscription_metrics"]["discounts_used"] = discount_usage[:5]  # Limit to 5 for response size
        except:
            pass
        
        # Try to get impersonation sessions
        try:
            user_analytics["support_metrics"]["impersonation_sessions"] = await db.impersonation_sessions.count_documents({
                "target_user_id": user_id
            })
        except:
            pass
        
        return user_analytics
        
    except Exception as e:
        # Return basic analytics if detailed fails
        return {
            "user_profile": {
                "user_id": user["user_id"],
                "email": user["email"],
                "role": user.get("role", "user"),
                "subscription_tier": user.get("subscription_tier", "free_trial"),
                "created_at": user.get("created_at"),
                "is_active": user.get("is_active", True)
            },
            "activity_metrics": {
                "total_logins": 0,
                "last_login": None,
                "session_count_30d": 0,
                "features_used": []
            },
            "subscription_metrics": {
                "subscription_start": user.get("subscription_start"),
                "subscription_end": user.get("subscription_end"),
                "payments_made": 0,
                "total_revenue": 0.0,
                "discounts_used": []
            },
            "support_metrics": {
                "support_tickets": 0,
                "last_support_contact": None,
                "impersonation_sessions": 0
            },
            "error": "Some analytics data could not be retrieved"
        }

# ===== DISCOUNT CODES SYSTEM =====

@router.post("/admin/discounts/{discount_id}/codes/generate")
async def generate_discount_codes(
    discount_id: str,
    count: int = Query(1, ge=1, le=1000),
    max_uses_per_code: Optional[int] = Query(None),
    expires_in_days: Optional[int] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Generate discount codes for a discount"""
    
    # Verify discount exists
    discount = await db.discounts.find_one({"discount_id": discount_id})
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    
    codes = []
    for _ in range(count):
        code_id = str(uuid.uuid4())
        code = f"CM{uuid.uuid4().hex[:8].upper()}"
        
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        code_doc = {
            "code_id": code_id,
            "discount_id": discount_id,
            "code": code,
            "is_active": True,
            "usage_count": 0,
            "max_uses": max_uses_per_code,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "created_by": current_user.user_id
        }
        
        await db.discount_codes.insert_one(code_doc)
        
        # Remove ObjectId for response
        del code_doc["_id"]
        codes.append(code_doc)
    
    return {
        "message": f"Generated {count} discount codes",
        "codes": codes
    }

@router.get("/admin/discounts/{discount_id}/codes")
async def get_discount_codes(
    discount_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get all codes for a discount"""
    
    codes = await db.discount_codes.find({"discount_id": discount_id}).sort("created_at", -1).to_list(length=500)
    
    # Remove ObjectIds
    for code in codes:
        if "_id" in code:
            del code["_id"]
    
    return {
        "codes": codes,
        "total": len(codes)
    }

@router.post("/discounts/redeem/{code}")
async def redeem_discount_code(
    code: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Redeem a discount code"""
    
    # Find the code
    code_doc = await db.discount_codes.find_one({"code": code})
    if not code_doc:
        raise HTTPException(status_code=404, detail="Invalid discount code")
    
    # Check if code is active and not expired
    if not code_doc["is_active"]:
        raise HTTPException(status_code=400, detail="Discount code is no longer active")
    
    if code_doc["expires_at"] and datetime.utcnow() > code_doc["expires_at"]:
        raise HTTPException(status_code=400, detail="Discount code has expired")
    
    # Check usage limits
    if code_doc["max_uses"] and code_doc["usage_count"] >= code_doc["max_uses"]:
        raise HTTPException(status_code=400, detail="Discount code usage limit reached")
    
    # Check if user already used this code
    existing_usage = await db.discount_usage.find_one({
        "user_id": current_user.user_id,
        "discount_code": code
    })
    if existing_usage:
        raise HTTPException(status_code=400, detail="You have already used this discount code")
    
    # Get discount details
    discount = await db.discounts.find_one({"discount_id": code_doc["discount_id"]})
    if not discount:
        raise HTTPException(status_code=404, detail="Associated discount not found")
    
    # Apply the discount
    usage_record = {
        "usage_id": str(uuid.uuid4()),
        "discount_id": discount["discount_id"],
        "discount_code": code,
        "user_id": current_user.user_id,
        "applied_at": datetime.utcnow(),
        "discount_amount": discount["value"],
        "discount_type": discount["discount_type"]
    }
    
    await db.discount_usage.insert_one(usage_record)
    
    # Update usage statistics
    await db.discount_codes.update_one(
        {"code": code},
        {"$inc": {"usage_count": 1}}
    )
    
    await db.discounts.update_one(
        {"discount_id": discount["discount_id"]},
        {"$inc": {"total_uses": 1}}
    )
    
    return {
        "message": "Discount code redeemed successfully",
        "discount": {
            "name": discount["name"],
            "type": discount["discount_type"],
            "value": discount["value"]
        },
        "usage_record": usage_record
    }

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
            SubscriptionTier.LAUNCH: 49,
            SubscriptionTier.GROWTH: 75,
            SubscriptionTier.SCALE: 199,
            SubscriptionTier.WHITE_LABEL: 299,
            SubscriptionTier.CUSTOM: 499
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

# ==============================================================================
# TRIAL EMAIL AUTOMATION ADMIN ENDPOINTS
# ==============================================================================

@router.get("/admin/trial-emails/logs")
async def get_admin_trial_email_logs(
    user_email: Optional[str] = Query(None, description="Filter by user email"),
    email_type: Optional[str] = Query(None, description="Filter by email type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200, description="Number of logs to return"),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN]))
):
    """Get all trial email logs for admin dashboard"""
    try:
        # Build query
        query = {}
        if user_email:
            query["user_email"] = {"$regex": user_email, "$options": "i"}
        if email_type:
            query["email_type"] = email_type
        if status:
            query["status"] = status
        
        # Get logs
        logs = await db.trial_email_logs.find(query).sort("created_at", -1).limit(limit).to_list(length=None)
        total_count = await db.trial_email_logs.count_documents(query)
        
        # Convert ObjectId to string and format dates
        for log in logs:
            log["_id"] = str(log["_id"])
            # Format dates for better display
            if "scheduled_send_time" in log:
                log["scheduled_send_time_formatted"] = log["scheduled_send_time"].strftime("%Y-%m-%d %H:%M:%S")
            if "actual_send_time" in log and log["actual_send_time"]:
                log["actual_send_time_formatted"] = log["actual_send_time"].strftime("%Y-%m-%d %H:%M:%S")
            if "created_at" in log:
                log["created_at_formatted"] = log["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "status": "success",
            "total_count": total_count,
            "returned_count": len(logs),
            "logs": logs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trial email logs: {str(e)}")

@router.get("/admin/trial-emails/stats")
async def get_admin_trial_email_stats(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN]))
):
    """Get comprehensive trial email statistics for admin dashboard"""
    try:
        # Overall stats
        total_logs = await db.trial_email_logs.count_documents({})
        sent_count = await db.trial_email_logs.count_documents({"status": "sent"})
        failed_count = await db.trial_email_logs.count_documents({"status": "failed"})
        scheduled_count = await db.trial_email_logs.count_documents({"status": "scheduled"})
        skipped_count = await db.trial_email_logs.count_documents({"status": "skipped"})
        
        # Stats by email type
        email_types = ["welcome", "progress", "urgency", "final"]
        type_stats = {}
        
        for email_type in email_types:
            type_total = await db.trial_email_logs.count_documents({"email_type": email_type})
            type_sent = await db.trial_email_logs.count_documents({
                "email_type": email_type,
                "status": "sent"
            })
            type_failed = await db.trial_email_logs.count_documents({
                "email_type": email_type,
                "status": "failed"
            })
            
            type_stats[email_type] = {
                "total": type_total,
                "sent": type_sent,
                "failed": type_failed,
                "success_rate": round((type_sent / type_total * 100) if type_total > 0 else 0, 2)
            }
        
        # Recent activity (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_activity = await db.trial_email_logs.aggregate([
            {
                "$match": {
                    "created_at": {"$gte": seven_days_ago}
                }
            },
            {
                "$group": {
                    "_id": {
                        "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                        "type": "$email_type"
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id.date": 1}}
        ]).to_list(length=None)
        
        # Trial users with email activity
        trial_users_with_emails = await db.trial_email_logs.aggregate([
            {
                "$group": {
                    "_id": "$user_email",
                    "total_emails": {"$sum": 1},
                    "sent_emails": {
                        "$sum": {"$cond": [{"$eq": ["$status", "sent"]}, 1, 0]}
                    },
                    "first_name": {"$first": "$first_name"},
                    "trial_start": {"$first": "$trial_start_date"},
                    "trial_end": {"$first": "$trial_end_date"}
                }
            },
            {"$sort": {"trial_start": -1}},
            {"$limit": 20}
        ]).to_list(length=None)
        
        # Calculate overall success rate
        success_rate = round((sent_count / total_logs * 100) if total_logs > 0 else 0, 2)
        
        return {
            "status": "success",
            "overall_stats": {
                "total_emails": total_logs,
                "sent": sent_count,
                "failed": failed_count,
                "scheduled": scheduled_count,
                "skipped": skipped_count,
                "success_rate_percent": success_rate
            },
            "stats_by_email_type": type_stats,
            "recent_activity": recent_activity,
            "trial_users_with_emails": trial_users_with_emails,
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trial email stats: {str(e)}")

@router.post("/admin/trial-emails/send-now/{log_id}")
async def admin_send_trial_email_now(
    log_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN]))
):
    """Admin endpoint to manually send a trial email immediately"""
    try:
        # Import the send function from email system
        from email_system import send_trial_email_now
        
        result = await send_trial_email_now(log_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send trial email: {str(e)}")

@router.post("/admin/trial-emails/process-scheduled")
async def admin_process_scheduled_trial_emails(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN]))
):
    """Admin endpoint to manually process all scheduled trial emails"""
    try:
        # Import the process function from email system
        from email_system import process_scheduled_trial_emails
        
        await process_scheduled_trial_emails()
        return {"status": "success", "message": "All scheduled trial emails processed"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process scheduled emails: {str(e)}")

@router.get("/admin/trial-emails/user/{user_email}")
async def get_trial_emails_for_user(
    user_email: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN]))
):
    """Get all trial emails for a specific user"""
    try:
        # Get user's trial emails
        emails = await db.trial_email_logs.find(
            {"user_email": user_email}
        ).sort("scheduled_send_time", 1).to_list(length=None)
        
        # Get user info
        user = await db.users.find_one({"email": user_email})
        
        # Format data
        for email in emails:
            email["_id"] = str(email["_id"])
            email["scheduled_send_time_formatted"] = email["scheduled_send_time"].strftime("%Y-%m-%d %H:%M:%S")
            if email.get("actual_send_time"):
                email["actual_send_time_formatted"] = email["actual_send_time"].strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "status": "success",
            "user_email": user_email,
            "user_name": f"{user.get('first_name', '')} {user.get('last_name', '')}" if user else "Unknown",
            "trial_status": "active" if user and user.get("is_trial") else "expired/converted",
            "emails": emails,
            "total_emails": len(emails)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user trial emails: {str(e)}")

# Export router
__all__ = ["router"]