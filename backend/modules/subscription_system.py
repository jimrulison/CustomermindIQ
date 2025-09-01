# Subscription Management System
import os
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

# Models
class SubscriptionUpdate(BaseModel):
    plan_type: str
    billing_cycle: str
    is_active: bool = True

class TrialRequest(BaseModel):
    user_email: str
    plan_type: str = "starter"

# Subscription Tiers and Features
SUBSCRIPTION_FEATURES = {
    "free": {
        "name": "Free Trial",
        "features": [
            "Basic analytics (7 days)",
            "Up to 100 contacts",
            "Limited AI insights"
        ],
        "growth_acceleration_access": False,
        "trial_days": 7
    },
    "starter": {
        "name": "Starter Plan",
        "features": [
            "Basic customer analytics",
            "Email marketing automation", 
            "Up to 1,000 contacts",
            "Standard support"
        ],
        "growth_acceleration_access": False,
        "monthly_price": 49,
        "annual_price": 399
    },
    "professional": {
        "name": "Professional Plan",
        "features": [
            "Advanced customer intelligence",
            "AI-powered insights",
            "Up to 10,000 contacts", 
            "A/B testing capabilities",
            "Priority support",
            "Growth Acceleration Engine (Annual Only)"
        ],
        "growth_acceleration_access": True,  # Only for annual
        "monthly_price": 99,
        "annual_price": 799
    },
    "enterprise": {
        "name": "Enterprise Plan",
        "features": [
            "Unlimited contacts",
            "Custom integrations",
            "Dedicated account manager",
            "White-label options",
            "Advanced analytics",
            "Growth Acceleration Engine (Annual Only)",
            "Custom AI models"
        ],
        "growth_acceleration_access": True,  # Only for annual
        "monthly_price": 199,
        "annual_price": 1599
    }
}

# Helper Functions
async def check_subscription_access(user_email: str, required_tier: str = None) -> dict:
    """Check user's subscription access and permissions"""
    user = await db.users.find_one({"email": user_email})
    
    if not user:
        return {"has_access": False, "reason": "User not found"}
    
    # Check if subscription is active
    subscription_end = user.get("subscription_end")
    is_active = user.get("is_active", False)
    
    if subscription_end and subscription_end < datetime.utcnow():
        is_active = False
    
    # Determine access level
    plan_type = user.get("plan_type", "free")
    billing_cycle = user.get("billing_cycle", "monthly")
    subscription_tier = user.get("subscription_tier", "monthly")
    
    # Growth Acceleration Engine access (Annual subscribers only)
    has_growth_acceleration = (
        is_active and 
        subscription_tier == "annual" and 
        plan_type in ["professional", "enterprise"]
    )
    
    return {
        "has_access": is_active,
        "plan_type": plan_type,
        "billing_cycle": billing_cycle,
        "subscription_tier": subscription_tier,
        "has_growth_acceleration": has_growth_acceleration,
        "subscription_end": subscription_end,
        "is_trial": user.get("is_trial", False),
        "features": SUBSCRIPTION_FEATURES.get(plan_type, {}).get("features", [])
    }

# Subscription Endpoints
@router.post("/start-trial")
async def start_free_trial(trial_request: TrialRequest):
    """Start free trial for new user"""
    try:
        user = await db.users.find_one({"email": trial_request.user_email})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user already had a trial
        if user.get("has_had_trial", False):
            raise HTTPException(status_code=400, detail="Free trial already used")
        
        # Set up 7-day free trial
        trial_end = datetime.utcnow() + timedelta(days=7)
        
        trial_data = {
            "plan_type": trial_request.plan_type,
            "billing_cycle": "trial",
            "subscription_tier": "trial",
            "subscription_start": datetime.utcnow(),
            "subscription_end": trial_end,
            "is_active": True,
            "is_trial": True,
            "has_had_trial": True,
            "updated_at": datetime.utcnow()
        }
        
        await db.users.update_one(
            {"email": trial_request.user_email},
            {"$set": trial_data}
        )
        
        return {
            "status": "success",
            "message": "Free trial activated",
            "trial_end": trial_end,
            "features": SUBSCRIPTION_FEATURES.get(trial_request.plan_type, {}).get("features", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trial activation failed: {str(e)}")

@router.get("/check-access/{user_email}")
async def check_user_access(user_email: str):
    """Check user's subscription access and permissions"""
    try:
        access_info = await check_subscription_access(user_email)
        
        return {
            "status": "success",
            "access": access_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Access check failed: {str(e)}")

@router.get("/check-growth-access/{user_email}")
async def check_growth_acceleration_access(user_email: str):
    """Specifically check Growth Acceleration Engine access"""
    try:
        access_info = await check_subscription_access(user_email)
        
        return {
            "status": "success",
            "has_growth_access": access_info.get("has_growth_acceleration", False),
            "subscription_tier": access_info.get("subscription_tier"),
            "plan_type": access_info.get("plan_type"),
            "message": "Growth Acceleration Engine is available for Annual Professional and Enterprise subscribers only"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Growth access check failed: {str(e)}")

@router.put("/update-subscription/{user_email}")
async def update_subscription(user_email: str, subscription: SubscriptionUpdate):
    """Update user's subscription"""
    try:
        user = await db.users.find_one({"email": user_email})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate subscription end date
        if subscription.billing_cycle == "annual":
            subscription_end = datetime.utcnow() + timedelta(days=365)
            subscription_tier = "annual"
        elif subscription.billing_cycle == "monthly":
            subscription_end = datetime.utcnow() + timedelta(days=30)
            subscription_tier = "monthly"
        else:
            raise HTTPException(status_code=400, detail="Invalid billing cycle")
        
        update_data = {
            "plan_type": subscription.plan_type,
            "billing_cycle": subscription.billing_cycle,
            "subscription_tier": subscription_tier,
            "subscription_end": subscription_end,
            "is_active": subscription.is_active,
            "is_trial": False,
            "updated_at": datetime.utcnow()
        }
        
        result = await db.users.update_one(
            {"email": user_email},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "status": "success",
            "message": "Subscription updated successfully",
            "subscription": update_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription update failed: {str(e)}")

@router.get("/plans")
async def get_subscription_plans():
    """Get available subscription plans with features"""
    return {
        "status": "success",
        "plans": SUBSCRIPTION_FEATURES
    }

@router.post("/cancel-subscription/{user_email}")
async def cancel_subscription(user_email: str):
    """Cancel user's subscription"""
    try:
        result = await db.users.update_one(
            {"email": user_email},
            {
                "$set": {
                    "is_active": False,
                    "subscription_tier": "cancelled",
                    "cancelled_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "status": "success",
            "message": "Subscription cancelled successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription cancellation failed: {str(e)}")

@router.get("/usage-stats/{user_email}")
async def get_usage_statistics(user_email: str):
    """Get user's usage statistics"""
    try:
        # Get basic user info
        user = await db.users.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate usage statistics
        total_contacts = await db.customers.count_documents({"user_email": user_email})
        total_campaigns = await db.campaigns.count_documents({"user_email": user_email})
        total_automations = await db.automation_workflows.count_documents({"user_email": user_email})
        
        # Get plan limits
        plan_type = user.get("plan_type", "free")
        plan_features = SUBSCRIPTION_FEATURES.get(plan_type, {})
        
        # Extract contact limit (basic parsing)
        contact_limit = 100  # Default for free
        if "1,000 contacts" in str(plan_features.get("features", [])):
            contact_limit = 1000
        elif "10,000 contacts" in str(plan_features.get("features", [])):
            contact_limit = 10000
        elif "Unlimited contacts" in str(plan_features.get("features", [])):
            contact_limit = float('inf')
        
        return {
            "status": "success",
            "usage": {
                "contacts": {
                    "used": total_contacts,
                    "limit": contact_limit,
                    "percentage": (total_contacts / contact_limit * 100) if contact_limit != float('inf') else 0
                },
                "campaigns": total_campaigns,
                "automations": total_automations,
                "plan_type": plan_type,
                "subscription_tier": user.get("subscription_tier", "monthly")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Usage statistics fetch failed: {str(e)}")