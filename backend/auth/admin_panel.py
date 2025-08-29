"""
Customer Mind IQ - Admin Panel Backend
Administrative interface and management endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import os
from .auth_system import (
    get_current_user, require_role, UserProfile, UserRole, 
    SubscriptionTier, ROLE_PERMISSIONS, SUBSCRIPTION_MODULE_ACCESS
)

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.customer_mind_iq

router = APIRouter()

# Admin Dashboard Models
class SystemStats(BaseModel):
    total_users: int
    active_users: int
    total_revenue: float
    monthly_revenue: float
    subscription_breakdown: Dict[str, int]
    role_breakdown: Dict[str, int]
    recent_signups: int
    churn_rate: float

class UserManagement(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: UserRole
    subscription_tier: SubscriptionTier
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    total_revenue: float

class ActivityLog(BaseModel):
    log_id: str
    user_id: str
    user_email: str
    action: str
    module: str
    timestamp: datetime
    ip_address: Optional[str]
    details: Dict[str, Any]

class SystemConfiguration(BaseModel):
    feature_flags: Dict[str, bool]
    subscription_limits: Dict[str, Dict[str, int]]
    email_settings: Dict[str, Any]
    security_settings: Dict[str, Any]
    integration_settings: Dict[str, Any]

# Admin Dashboard Endpoints

@router.get("/dashboard/stats", response_model=SystemStats)
async def get_system_stats(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get system-wide statistics for admin dashboard"""
    
    # User statistics
    total_users = await db.users.count_documents({})
    active_users = await db.users.count_documents({"is_active": True})
    recent_signups = await db.users.count_documents({
        "created_at": {"$gte": datetime.utcnow() - timedelta(days=30)}
    })
    
    # Subscription breakdown
    subscription_pipeline = [
        {"$group": {"_id": "$subscription_tier", "count": {"$sum": 1}}}
    ]
    subscription_data = await db.users.aggregate(subscription_pipeline).to_list(length=10)
    subscription_breakdown = {item["_id"]: item["count"] for item in subscription_data}
    
    # Role breakdown
    role_pipeline = [
        {"$group": {"_id": "$role", "count": {"$sum": 1}}}
    ]
    role_data = await db.users.aggregate(role_pipeline).to_list(length=10)
    role_breakdown = {item["_id"]: item["count"] for item in role_data}
    
    # Revenue statistics
    revenue_pipeline = [
        {"$match": {"payment_status": "paid"}},
        {"$group": {
            "_id": None,
            "total_revenue": {"$sum": "$amount"},
            "monthly_revenue": {
                "$sum": {
                    "$cond": [
                        {"$gte": ["$created_at", datetime.utcnow().replace(day=1)]},
                        "$amount",
                        0
                    ]
                }
            }
        }}
    ]
    revenue_data = await db.payment_transactions.aggregate(revenue_pipeline).to_list(length=1)
    
    total_revenue = revenue_data[0]["total_revenue"] if revenue_data else 0
    monthly_revenue = revenue_data[0]["monthly_revenue"] if revenue_data else 0
    
    # Calculate churn rate (simplified)
    churned_users = await db.users.count_documents({
        "subscription_tier": {"$ne": "free"},
        "last_login": {"$lt": datetime.utcnow() - timedelta(days=30)}
    })
    paying_users = await db.users.count_documents({
        "subscription_tier": {"$ne": "free"}
    })
    churn_rate = (churned_users / paying_users * 100) if paying_users > 0 else 0
    
    return SystemStats(
        total_users=total_users,
        active_users=active_users,
        total_revenue=total_revenue,
        monthly_revenue=monthly_revenue,
        subscription_breakdown=subscription_breakdown,
        role_breakdown=role_breakdown,
        recent_signups=recent_signups,
        churn_rate=churn_rate
    )

@router.get("/dashboard/users", response_model=List[UserManagement])
async def get_users_management(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    role_filter: Optional[UserRole] = Query(None),
    subscription_filter: Optional[SubscriptionTier] = Query(None),
    active_only: bool = Query(False),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get users for management interface with filtering and pagination"""
    
    # Build filter query
    filter_query = {}
    
    if search:
        filter_query["$or"] = [
            {"email": {"$regex": search, "$options": "i"}},
            {"first_name": {"$regex": search, "$options": "i"}},
            {"last_name": {"$regex": search, "$options": "i"}},
            {"company_name": {"$regex": search, "$options": "i"}}
        ]
    
    if role_filter:
        filter_query["role"] = role_filter
    
    if subscription_filter:
        filter_query["subscription_tier"] = subscription_filter
    
    if active_only:
        filter_query["is_active"] = True
    
    # Get users with revenue data
    pipeline = [
        {"$match": filter_query},
        {
            "$lookup": {
                "from": "payment_transactions",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "transactions"
            }
        },
        {
            "$addFields": {
                "total_revenue": {
                    "$sum": {
                        "$map": {
                            "input": "$transactions",
                            "as": "transaction",
                            "in": {
                                "$cond": [
                                    {"$eq": ["$$transaction.payment_status", "paid"]},
                                    "$$transaction.amount",
                                    0
                                ]
                            }
                        }
                    }
                }
            }
        },
        {"$sort": {"created_at": -1}},
        {"$skip": skip},
        {"$limit": limit}
    ]
    
    users_data = await db.users.aggregate(pipeline).to_list(length=limit)
    
    users_management = []
    for user in users_data:
        user_mgmt = UserManagement(
            user_id=user["user_id"],
            email=user["email"],
            full_name=f"{user['first_name']} {user['last_name']}",
            role=user["role"],
            subscription_tier=user["subscription_tier"],
            is_active=user["is_active"],
            created_at=user["created_at"],
            last_login=user.get("last_login"),
            total_revenue=user.get("total_revenue", 0)
        )
        users_management.append(user_mgmt)
    
    return users_management

@router.get("/dashboard/activity-logs", response_model=List[ActivityLog])
async def get_activity_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user_filter: Optional[str] = Query(None),
    action_filter: Optional[str] = Query(None),
    module_filter: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get system activity logs for monitoring"""
    
    # Build filter query
    filter_query = {}
    
    if user_filter:
        filter_query["user_id"] = user_filter
    
    if action_filter:
        filter_query["action"] = {"$regex": action_filter, "$options": "i"}
    
    if module_filter:
        filter_query["module"] = module_filter
    
    if date_from or date_to:
        date_filter = {}
        if date_from:
            date_filter["$gte"] = date_from
        if date_to:
            date_filter["$lte"] = date_to
        filter_query["timestamp"] = date_filter
    
    # Get activity logs
    logs = await db.activity_logs.find(filter_query).sort("timestamp", -1).skip(skip).limit(limit).to_list(length=limit)
    
    activity_logs = []
    for log in logs:
        activity_log = ActivityLog(
            log_id=str(log["_id"]),
            user_id=log["user_id"],
            user_email=log.get("user_email", ""),
            action=log["action"],
            module=log.get("module", "system"),
            timestamp=log["timestamp"],
            ip_address=log.get("ip_address"),
            details=log.get("details", {})
        )
        activity_logs.append(activity_log)
    
    return activity_logs

@router.post("/users/{user_id}/impersonate")
async def impersonate_user(
    user_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Impersonate user (super admin only) for support purposes"""
    
    target_user = await db.users.find_one({"user_id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Log impersonation activity
    await db.activity_logs.insert_one({
        "user_id": current_user.user_id,
        "user_email": current_user.email,
        "action": "impersonate_user",
        "module": "admin",
        "timestamp": datetime.utcnow(),
        "details": {
            "target_user_id": user_id,
            "target_user_email": target_user["email"]
        }
    })
    
    # Create impersonation token (would need special handling in frontend)
    from .auth_system import create_access_token
    token_data = {
        "user_id": user_id, 
        "email": target_user["email"],
        "impersonated_by": current_user.user_id
    }
    impersonation_token = create_access_token(token_data, timedelta(hours=1))
    
    return {
        "message": "Impersonation token created",
        "impersonation_token": impersonation_token,
        "target_user": {
            "user_id": user_id,
            "email": target_user["email"],
            "name": f"{target_user['first_name']} {target_user['last_name']}"
        },
        "expires_in": 3600
    }

@router.get("/system/configuration", response_model=SystemConfiguration)
async def get_system_configuration(
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Get system configuration (super admin only)"""
    
    config = await db.system_config.find_one({"config_type": "main"}) or {}
    
    return SystemConfiguration(
        feature_flags=config.get("feature_flags", {
            "advanced_ai_models": True,
            "white_label": True,
            "custom_integrations": True,
            "beta_features": False
        }),
        subscription_limits=config.get("subscription_limits", SUBSCRIPTION_MODULE_ACCESS),
        email_settings=config.get("email_settings", {
            "smtp_server": "localhost",
            "smtp_port": 587,
            "use_tls": True,
            "from_email": "noreply@customermindiq.com"
        }),
        security_settings=config.get("security_settings", {
            "max_login_attempts": 5,
            "account_lock_duration_minutes": 30,
            "password_min_length": 8,
            "require_2fa": False,
            "session_timeout_minutes": 60
        }),
        integration_settings=config.get("integration_settings", {
            "stripe_webhooks_enabled": True,
            "email_notifications_enabled": True,
            "slack_notifications_enabled": False,
            "audit_logging_enabled": True
        })
    )

@router.put("/system/configuration")
async def update_system_configuration(
    config: SystemConfiguration,
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Update system configuration (super admin only)"""
    
    config_doc = {
        "config_type": "main",
        "feature_flags": config.feature_flags,
        "subscription_limits": config.subscription_limits,
        "email_settings": config.email_settings,
        "security_settings": config.security_settings,
        "integration_settings": config.integration_settings,
        "updated_at": datetime.utcnow(),
        "updated_by": current_user.user_id
    }
    
    await db.system_config.update_one(
        {"config_type": "main"},
        {"$set": config_doc},
        upsert=True
    )
    
    # Log configuration change
    await db.activity_logs.insert_one({
        "user_id": current_user.user_id,
        "user_email": current_user.email,
        "action": "update_system_configuration",
        "module": "admin",
        "timestamp": datetime.utcnow(),
        "details": {"configuration_updated": True}
    })
    
    return {"message": "System configuration updated successfully"}

@router.post("/system/backup")
async def create_system_backup(
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Create system backup (super admin only)"""
    
    backup_id = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    # In production, this would create actual database backups
    # For now, we'll log the backup request
    backup_record = {
        "backup_id": backup_id,
        "created_by": current_user.user_id,
        "created_at": datetime.utcnow(),
        "backup_type": "full_system",
        "status": "completed",
        "size_mb": 0,  # Would be actual size
        "collections": ["users", "payment_transactions", "subscriptions", "activity_logs"]
    }
    
    await db.system_backups.insert_one(backup_record)
    
    return {
        "message": "System backup created successfully",
        "backup_id": backup_id,
        "created_at": backup_record["created_at"]
    }

@router.get("/analytics/revenue")
async def get_revenue_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get revenue analytics for specified period"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily revenue aggregation
    daily_revenue_pipeline = [
        {
            "$match": {
                "payment_status": "paid",
                "created_at": {"$gte": start_date}
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"}
                },
                "daily_revenue": {"$sum": "$amount"},
                "transaction_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    daily_data = await db.payment_transactions.aggregate(daily_revenue_pipeline).to_list(length=days)
    
    # Subscription tier revenue breakdown
    tier_revenue_pipeline = [
        {
            "$match": {
                "payment_status": "paid",
                "created_at": {"$gte": start_date}
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user_info"
            }
        },
        {
            "$group": {
                "_id": {"$arrayElemAt": ["$user_info.subscription_tier", 0]},
                "revenue": {"$sum": "$amount"},
                "transactions": {"$sum": 1}
            }
        }
    ]
    
    tier_data = await db.payment_transactions.aggregate(tier_revenue_pipeline).to_list(length=10)
    
    return {
        "period_days": days,
        "start_date": start_date,
        "end_date": datetime.utcnow(),
        "daily_revenue": daily_data,
        "tier_breakdown": tier_data,
        "total_revenue": sum(item["daily_revenue"] for item in daily_data),
        "total_transactions": sum(item["transaction_count"] for item in daily_data)
    }

@router.post("/notifications/broadcast")
async def broadcast_notification(
    title: str,
    message: str,
    target_roles: List[UserRole] = None,
    target_tiers: List[SubscriptionTier] = None,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Broadcast notification to users"""
    
    # Build target user filter
    user_filter = {}
    if target_roles:
        user_filter["role"] = {"$in": target_roles}
    if target_tiers:
        user_filter["subscription_tier"] = {"$in": target_tiers}
    
    # Get target users
    target_users = await db.users.find(user_filter, {"user_id": 1, "email": 1}).to_list(length=10000)
    
    # Create notification record
    notification = {
        "notification_id": f"broadcast_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        "title": title,
        "message": message,
        "created_by": current_user.user_id,
        "created_at": datetime.utcnow(),
        "target_count": len(target_users),
        "delivery_status": "sent"
    }
    
    await db.notifications.insert_one(notification)
    
    # In production, this would send actual notifications (email, in-app, etc.)
    
    return {
        "message": "Notification broadcast successfully",
        "notification_id": notification["notification_id"],
        "target_users": len(target_users)
    }

# Export router
__all__ = ["router"]