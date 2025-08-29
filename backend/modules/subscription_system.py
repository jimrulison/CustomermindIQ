"""
Customer Mind IQ - Updated Subscription System
New 4-tier pricing structure with 7-day free trial system
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

# Updated Subscription Tiers (New 4-tier structure)
class NewSubscriptionTier(str, Enum):
    STARTER = "starter"      # $99/month
    PROFESSIONAL = "professional"  # $299/month  
    ENTERPRISE = "enterprise"     # $799/month
    CUSTOM = "custom"           # Contact for pricing

class TrialStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CONVERTED = "converted"
    CANCELLED = "cancelled"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    TRIAL = "trial"
    ON_HOLD = "on_hold"

# Pricing Configuration
TIER_PRICING = {
    NewSubscriptionTier.STARTER: {
        "monthly_price": 99.00,
        "annual_price": 990.00,  # 2 months free
        "features": {
            "websites_monitored": 3,
            "keywords_tracked": 50,
            "customer_journeys": 10,
            "data_connectors": 2,
            "team_members": 2,
            "monthly_page_views": 10000,
            "support_level": "email"
        }
    },
    NewSubscriptionTier.PROFESSIONAL: {
        "monthly_price": 299.00,
        "annual_price": 2990.00,  # 2 months free
        "features": {
            "websites_monitored": 10,
            "keywords_tracked": 200,
            "customer_journeys": 50,
            "data_connectors": 10,
            "team_members": 10,
            "monthly_page_views": 100000,
            "support_level": "email_chat",
            "product_intelligence": True,
            "feature_usage_analytics": 20,
            "revenue_attribution": "500k_tracking"
        }
    },
    NewSubscriptionTier.ENTERPRISE: {
        "monthly_price": 799.00,
        "annual_price": 7990.00,  # 2 months free
        "features": {
            "websites_monitored": "unlimited",
            "keywords_tracked": "500+",
            "customer_journeys": "unlimited",
            "data_connectors": "unlimited",
            "team_members": "unlimited",
            "monthly_page_views": "500k+",
            "support_level": "phone_sla",
            "product_intelligence": True,
            "compliance_monitoring": True,
            "ai_command_center": "limited",
            "white_label": "addon",
            "custom_integrations": True
        }
    },
    NewSubscriptionTier.CUSTOM: {
        "monthly_price": "contact",
        "annual_price": "contact",
        "features": {
            "everything_enterprise": True,
            "ai_command_center": "unlimited",
            "on_premise_deployment": True,
            "custom_ml_models": True,
            "dedicated_support": True,
            "multi_tenant_architecture": True,
            "advanced_security": True
        }
    }
}

# Pydantic Models
class TrialRegistration(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    company_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = None
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None

class TrialInfo(BaseModel):
    trial_id: str
    user_id: str
    email: str
    trial_tier: NewSubscriptionTier = NewSubscriptionTier.STARTER
    start_date: datetime
    end_date: datetime
    status: TrialStatus
    days_remaining: int
    has_credit_card: bool = False
    conversion_attempted: bool = False
    
class SubscriptionInfo(BaseModel):
    subscription_id: str
    user_id: str
    tier: NewSubscriptionTier
    status: SubscriptionStatus
    billing_cycle: str  # "monthly" or "annual"
    current_price: float
    next_billing_date: Optional[datetime]
    created_at: datetime
    trial_info: Optional[TrialInfo] = None
    feature_usage: Dict[str, Any] = Field(default_factory=dict)
    
class SubscriptionUpgrade(BaseModel):
    target_tier: NewSubscriptionTier
    billing_cycle: str = Field(default="monthly", pattern="^(monthly|annual)$")
    promo_code: Optional[str] = None
    
class FeatureUsage(BaseModel):
    feature_name: str
    usage_count: int
    limit: Optional[int] = None
    last_reset: datetime
    
# Trial Management Endpoints
@router.post("/trial/register")
async def register_for_trial(trial_data: TrialRegistration):
    """Register for 7-day free trial (no credit card required)"""
    
    # Check if email already exists
    existing_user = await db.users.find_one({"email": trial_data.email})
    if existing_user:
        # Check if they already have an active trial
        existing_trial = await db.trials.find_one({
            "email": trial_data.email,
            "status": {"$in": [TrialStatus.ACTIVE, TrialStatus.CONVERTED]}
        })
        if existing_trial:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has an active trial or subscription"
            )
    
    # Create user account for trial
    user_id = str(uuid.uuid4())
    trial_id = str(uuid.uuid4())
    
    now = datetime.utcnow()
    trial_end = now + timedelta(days=7)
    
    # Create user with trial status
    user_doc = {
        "user_id": user_id,
        "email": trial_data.email,
        "first_name": trial_data.first_name,
        "last_name": trial_data.last_name,
        "company_name": trial_data.company_name,
        "phone": trial_data.phone,
        "role": UserRole.USER,
        "subscription_tier": NewSubscriptionTier.STARTER,  # Trial gets Starter features
        "subscription_status": SubscriptionStatus.TRIAL,
        "is_active": True,
        "email_verified": False,
        "created_at": now,
        "trial_user": True,
        "utm_source": trial_data.utm_source,
        "utm_campaign": trial_data.utm_campaign
    }
    
    # Create trial record
    trial_doc = {
        "trial_id": trial_id,
        "user_id": user_id,
        "email": trial_data.email,
        "trial_tier": NewSubscriptionTier.STARTER,
        "start_date": now,
        "end_date": trial_end,
        "status": TrialStatus.ACTIVE,
        "has_credit_card": False,
        "conversion_attempted": False,
        "utm_source": trial_data.utm_source,
        "utm_campaign": trial_data.utm_campaign,
        "created_at": now
    }
    
    # Insert both documents
    await db.users.insert_one(user_doc)
    await db.trials.insert_one(trial_doc)
    
    # Calculate days remaining
    days_remaining = (trial_end - now).days
    
    trial_info = TrialInfo(
        trial_id=trial_id,
        user_id=user_id,
        email=trial_data.email,
        trial_tier=NewSubscriptionTier.STARTER,
        start_date=now,
        end_date=trial_end,
        status=TrialStatus.ACTIVE,
        days_remaining=days_remaining,
        has_credit_card=False
    )
    
    return {
        "message": "7-day free trial started successfully",
        "trial_info": trial_info,
        "access_features": TIER_PRICING[NewSubscriptionTier.STARTER]["features"],
        "next_steps": {
            "1": "Explore all Starter tier features",
            "2": "Connect your data sources",
            "3": "Set up your first customer intelligence dashboard",
            "4": "Upgrade before trial expires to continue access"
        }
    }

@router.get("/trial/status")
async def get_trial_status(current_user: UserProfile = Depends(get_current_user)):
    """Get current user's trial status"""
    
    trial = await db.trials.find_one({"user_id": current_user.user_id})
    
    if not trial:
        return {"has_trial": False, "message": "No trial found for user"}
    
    now = datetime.utcnow()
    days_remaining = max(0, (trial["end_date"] - now).days)
    
    # Update trial status if expired
    if days_remaining == 0 and trial["status"] == TrialStatus.ACTIVE:
        await db.trials.update_one(
            {"trial_id": trial["trial_id"]},
            {"$set": {"status": TrialStatus.EXPIRED}}
        )
        
        # Put user account on hold
        await db.users.update_one(
            {"user_id": current_user.user_id},
            {"$set": {"subscription_status": SubscriptionStatus.ON_HOLD}}
        )
        
        trial["status"] = TrialStatus.EXPIRED
    
    trial_info = TrialInfo(
        trial_id=trial["trial_id"],
        user_id=trial["user_id"],
        email=trial["email"],
        trial_tier=trial["trial_tier"],
        start_date=trial["start_date"],
        end_date=trial["end_date"],
        status=trial["status"],
        days_remaining=days_remaining,
        has_credit_card=trial.get("has_credit_card", False),
        conversion_attempted=trial.get("conversion_attempted", False)
    )
    
    return {
        "has_trial": True,
        "trial_info": trial_info,
        "is_expired": days_remaining == 0,
        "upgrade_urgency": "high" if days_remaining <= 1 else "medium" if days_remaining <= 3 else "low"
    }

@router.post("/trial/extend")
async def extend_trial(
    target_user_id: str,
    days: int,
    reason: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Extend trial period (admin only)"""
    
    # Validate inputs
    if days < 1 or days > 14:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days must be between 1 and 14"
        )
    
    if len(reason) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reason must be less than 500 characters"
        )
    
    # Get the trial to extend
    trial = await db.trials.find_one({"user_id": target_user_id})
    
    if not trial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No trial found for user"
        )
    
    new_end_date = trial["end_date"] + timedelta(days=days)
    
    await db.trials.update_one(
        {"trial_id": trial["trial_id"]},
        {
            "$set": {
                "end_date": new_end_date,
                "extended_by": current_user.user_id,
                "extension_reason": reason,
                "extended_at": datetime.utcnow()
            }
        }
    )
    
    return {
        "message": f"Trial extended by {days} days",
        "new_end_date": new_end_date
    }

# Subscription Management Endpoints
@router.get("/subscriptions/tiers")
async def get_subscription_tiers():
    """Get all available subscription tiers with pricing and features"""
    
    return {
        "tiers": TIER_PRICING,
        "add_ons": {
            "extra_websites": {"price_per_month": 25, "description": "Additional website monitoring"},
            "additional_keywords": {"price_per_keyword": 0.50, "description": "Extra keyword tracking"},
            "extra_team_members": {"price_per_month": 25, "description": "Additional team member access"},
            "white_label_reporting": {"price_per_month": 200, "description": "White-label reports"},
            "api_rate_increase": {"price_per_month": 100, "description": "Higher API rate limits"}
        },
        "professional_services": {
            "implementation_setup": {"price": 2500, "type": "one_time"},
            "data_migration": {"price": 1500, "type": "one_time"},
            "custom_dashboard": {"price": 500, "type": "per_dashboard"},
            "advanced_training": {"price": 250, "type": "per_hour"}
        }
    }

@router.get("/subscriptions/current")
async def get_current_subscription(current_user: UserProfile = Depends(get_current_user)):
    """Get current user's subscription details"""
    
    # Get subscription info
    subscription = await db.subscriptions.find_one({"user_id": current_user.user_id})
    
    if not subscription:
        # Check if user is on trial
        trial_status = await get_trial_status(current_user)
        if trial_status["has_trial"]:
            return {
                "has_subscription": False,
                "on_trial": True,
                "trial_info": trial_status["trial_info"],
                "message": "User is currently on free trial"
            }
        else:
            return {
                "has_subscription": False,
                "on_trial": False,
                "message": "No active subscription found"
            }
    
    # Get feature usage statistics
    feature_usage = await db.feature_usage.find({"user_id": current_user.user_id}).to_list(length=50)
    
    # Calculate usage against limits
    current_tier_features = TIER_PRICING[subscription["tier"]]["features"]
    usage_summary = {}
    
    for usage in feature_usage:
        feature_name = usage["feature_name"]
        limit = current_tier_features.get(feature_name)
        
        usage_summary[feature_name] = {
            "current_usage": usage["usage_count"],
            "limit": limit,
            "percentage_used": (usage["usage_count"] / limit * 100) if isinstance(limit, (int, float)) else 0,
            "last_reset": usage["last_reset"]
        }
    
    subscription_info = SubscriptionInfo(
        subscription_id=subscription["subscription_id"],
        user_id=subscription["user_id"],
        tier=subscription["tier"],
        status=subscription["status"],
        billing_cycle=subscription["billing_cycle"],
        current_price=subscription["current_price"],
        next_billing_date=subscription.get("next_billing_date"),
        created_at=subscription["created_at"],
        feature_usage=usage_summary
    )
    
    return {
        "has_subscription": True,
        "subscription_info": subscription_info,
        "tier_features": current_tier_features,
        "upgrade_benefits": get_upgrade_benefits(subscription["tier"])
    }

def get_upgrade_benefits(current_tier: NewSubscriptionTier) -> Dict[str, Any]:
    """Calculate benefits of upgrading to higher tiers"""
    
    tier_order = [NewSubscriptionTier.STARTER, NewSubscriptionTier.PROFESSIONAL, NewSubscriptionTier.ENTERPRISE, NewSubscriptionTier.CUSTOM]
    current_index = tier_order.index(current_tier)
    
    if current_index >= len(tier_order) - 1:
        return {"message": "Already on highest tier"}
    
    benefits = {}
    current_features = TIER_PRICING[current_tier]["features"]
    
    for higher_tier in tier_order[current_index + 1:]:
        higher_features = TIER_PRICING[higher_tier]["features"]
        tier_benefits = {}
        
        for feature, value in higher_features.items():
            current_value = current_features.get(feature)
            if current_value != value:
                tier_benefits[feature] = {
                    "current": current_value,
                    "upgraded": value
                }
        
        benefits[higher_tier] = {
            "monthly_price": TIER_PRICING[higher_tier]["monthly_price"],
            "new_features": tier_benefits,
            "price_difference": TIER_PRICING[higher_tier]["monthly_price"] - TIER_PRICING[current_tier]["monthly_price"] if isinstance(TIER_PRICING[higher_tier]["monthly_price"], (int, float)) else "Contact for pricing"
        }
    
    return benefits

@router.post("/subscriptions/upgrade")
async def upgrade_subscription(
    upgrade_data: SubscriptionUpgrade,
    current_user: UserProfile = Depends(get_current_user)
):
    """Upgrade subscription to higher tier"""
    
    # Get current subscription or trial
    current_subscription = await db.subscriptions.find_one({"user_id": current_user.user_id})
    trial = await db.trials.find_one({"user_id": current_user.user_id})
    
    if not current_subscription and not trial:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No subscription or trial found to upgrade"
        )
    
    # Validate target tier
    if upgrade_data.target_tier == NewSubscriptionTier.CUSTOM:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Custom tier requires direct contact with sales team"
        )
    
    # Calculate pricing
    tier_pricing = TIER_PRICING[upgrade_data.target_tier]
    price = tier_pricing["annual_price"] if upgrade_data.billing_cycle == "annual" else tier_pricing["monthly_price"]
    
    # Apply promo code discount if provided
    if upgrade_data.promo_code:
        discount = await db.discounts.find_one({
            "name": upgrade_data.promo_code,
            "is_active": True
        })
        if discount:
            # Apply discount logic here
            pass
    
    subscription_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    # Create or update subscription
    subscription_doc = {
        "subscription_id": subscription_id,
        "user_id": current_user.user_id,
        "tier": upgrade_data.target_tier,
        "status": SubscriptionStatus.ACTIVE,
        "billing_cycle": upgrade_data.billing_cycle,
        "current_price": price,
        "next_billing_date": now + timedelta(days=30 if upgrade_data.billing_cycle == "monthly" else 365),
        "created_at": now,
        "upgraded_from": current_subscription["tier"] if current_subscription else "trial",
        "upgrade_date": now
    }
    
    if current_subscription:
        # Update existing subscription
        await db.subscriptions.update_one(
            {"user_id": current_user.user_id},
            {"$set": subscription_doc}
        )
    else:
        # Create new subscription from trial
        await db.subscriptions.insert_one(subscription_doc)
        
        # Mark trial as converted
        if trial:
            await db.trials.update_one(
                {"user_id": current_user.user_id},
                {"$set": {"status": TrialStatus.CONVERTED, "converted_at": now}}
            )
    
    # Update user subscription tier
    await db.users.update_one(
        {"user_id": current_user.user_id},
        {
            "$set": {
                "subscription_tier": upgrade_data.target_tier,
                "subscription_status": SubscriptionStatus.ACTIVE
            }
        }
    )
    
    # Initialize feature usage tracking for new tier
    tier_features = TIER_PRICING[upgrade_data.target_tier]["features"]
    for feature_name, limit in tier_features.items():
        if isinstance(limit, (int, float)):
            await db.feature_usage.update_one(
                {"user_id": current_user.user_id, "feature_name": feature_name},
                {
                    "$set": {
                        "usage_count": 0,
                        "limit": limit,
                        "last_reset": now
                    }
                },
                upsert=True
            )
    
    return {
        "message": f"Successfully upgraded to {upgrade_data.target_tier}",
        "subscription_id": subscription_id,
        "new_features": tier_features,
        "next_billing_date": subscription_doc["next_billing_date"],
        "price": price,
        "billing_cycle": upgrade_data.billing_cycle
    }

@router.post("/subscriptions/cancel")
async def cancel_subscription(
    cancel_data: dict,
    current_user: UserProfile = Depends(get_current_user)
):
    """Cancel subscription (keeps access until end of billing period)"""
    
    reason = cancel_data.get("reason", "No reason provided")
    if len(reason) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reason must be less than 500 characters"
        )
    
    subscription = await db.subscriptions.find_one({"user_id": current_user.user_id})
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    if subscription["status"] == SubscriptionStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscription is already cancelled"
        )
    
    # Mark subscription as cancelled but keep active until billing period ends
    cancellation_date = datetime.utcnow()
    access_end_date = subscription.get("next_billing_date", cancellation_date)
    
    await db.subscriptions.update_one(
        {"user_id": current_user.user_id},
        {
            "$set": {
                "status": SubscriptionStatus.CANCELLED,
                "cancelled_at": cancellation_date,
                "cancellation_reason": reason,
                "access_ends_at": access_end_date
            }
        }
    )
    
    # Log cancellation for analytics
    await db.subscription_events.insert_one({
        "event_id": str(uuid.uuid4()),
        "user_id": current_user.user_id,
        "event_type": "cancellation",
        "tier": subscription["tier"],
        "reason": reason,
        "timestamp": cancellation_date,
        "revenue_impact": -subscription["current_price"]
    })
    
    return {
        "message": "Subscription cancelled successfully",
        "access_ends_at": access_end_date,
        "days_remaining": (access_end_date - cancellation_date).days,
        "offer": "We'd love to win you back! Contact support for special offers."
    }

# Feature Usage Tracking
@router.post("/usage/track/{feature_name}")
async def track_feature_usage(
    feature_name: str,
    usage_amount: int = 1,
    current_user: UserProfile = Depends(get_current_user)
):
    """Track feature usage for current user"""
    
    # Get current usage
    usage_record = await db.feature_usage.find_one({
        "user_id": current_user.user_id,
        "feature_name": feature_name
    })
    
    if not usage_record:
        # Initialize usage tracking
        tier_features = TIER_PRICING.get(current_user.subscription_tier, {}).get("features", {})
        limit = tier_features.get(feature_name)
        
        usage_record = {
            "user_id": current_user.user_id,
            "feature_name": feature_name,
            "usage_count": 0,
            "limit": limit,
            "last_reset": datetime.utcnow()
        }
        await db.feature_usage.insert_one(usage_record)
    
    # Update usage
    new_usage = usage_record["usage_count"] + usage_amount
    
    await db.feature_usage.update_one(
        {"user_id": current_user.user_id, "feature_name": feature_name},
        {
            "$set": {
                "usage_count": new_usage,
                "last_updated": datetime.utcnow()
            }
        }
    )
    
    # Check if limit exceeded
    limit = usage_record.get("limit")
    limit_exceeded = False
    
    if isinstance(limit, (int, float)) and new_usage > limit:
        limit_exceeded = True
    
    return {
        "feature_name": feature_name,
        "current_usage": new_usage,
        "limit": limit,
        "limit_exceeded": limit_exceeded,
        "upgrade_recommended": limit_exceeded
    }

@router.get("/usage/summary")
async def get_usage_summary(current_user: UserProfile = Depends(get_current_user)):
    """Get feature usage summary for current user"""
    
    usage_records = await db.feature_usage.find({"user_id": current_user.user_id}).to_list(length=50)
    
    tier_features = TIER_PRICING.get(current_user.subscription_tier, {}).get("features", {})
    
    usage_summary = {}
    approaching_limits = []
    exceeded_limits = []
    
    for record in usage_records:
        feature_name = record["feature_name"]
        usage_count = record["usage_count"]
        limit = record.get("limit")
        
        usage_summary[feature_name] = {
            "usage_count": usage_count,
            "limit": limit,
            "percentage_used": (usage_count / limit * 100) if isinstance(limit, (int, float)) else 0,
            "last_reset": record["last_reset"]
        }
        
        if isinstance(limit, (int, float)):
            percentage = usage_count / limit * 100
            
            if percentage >= 100:
                exceeded_limits.append(feature_name)
            elif percentage >= 80:
                approaching_limits.append(feature_name)
    
    return {
        "current_tier": current_user.subscription_tier,
        "tier_features": tier_features,
        "usage_summary": usage_summary,
        "approaching_limits": approaching_limits,
        "exceeded_limits": exceeded_limits,
        "upgrade_recommended": len(exceeded_limits) > 0 or len(approaching_limits) > 2
    }

# Admin endpoints for subscription management
@router.get("/admin/subscriptions/analytics")
async def get_subscription_analytics(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get subscription analytics dashboard (admin only)"""
    
    # Subscription distribution by tier
    tier_distribution = await db.subscriptions.aggregate([
        {
            "$group": {
                "_id": "$tier",
                "count": {"$sum": 1},
                "total_revenue": {"$sum": "$current_price"}
            }
        }
    ]).to_list(length=10)
    
    # Trial conversion rates
    total_trials = await db.trials.count_documents({})
    converted_trials = await db.trials.count_documents({"status": TrialStatus.CONVERTED})
    conversion_rate = (converted_trials / total_trials * 100) if total_trials > 0 else 0
    
    # Churn analysis
    cancelled_subscriptions = await db.subscriptions.count_documents({"status": SubscriptionStatus.CANCELLED})
    total_subscriptions = await db.subscriptions.count_documents({})
    churn_rate = (cancelled_subscriptions / total_subscriptions * 100) if total_subscriptions > 0 else 0
    
    # Monthly recurring revenue
    mrr = sum(tier["total_revenue"] for tier in tier_distribution)
    
    # Recent subscription events
    recent_events = await db.subscription_events.find({}).sort("timestamp", -1).limit(20).to_list(length=20)
    
    return {
        "tier_distribution": tier_distribution,
        "total_subscriptions": total_subscriptions,
        "mrr": mrr,
        "arr": mrr * 12,  # Annual recurring revenue
        "trial_analytics": {
            "total_trials": total_trials,
            "converted_trials": converted_trials,
            "conversion_rate": conversion_rate
        },
        "churn_analytics": {
            "cancelled_subscriptions": cancelled_subscriptions,
            "churn_rate": churn_rate
        },
        "recent_events": recent_events,
        "generated_at": datetime.utcnow()
    }

# Export router
__all__ = ["router", "NewSubscriptionTier", "TIER_PRICING"]