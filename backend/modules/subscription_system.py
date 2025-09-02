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

# Subscription Tiers and Features - Updated with New Pricing Structure
SUBSCRIPTION_FEATURES = {
    "free": {
        "name": "7-Day Free Trial",
        "features": [
            "Basic analytics (7 days)",
            "Up to 100 contacts",
            "Limited AI insights"
        ],
        "growth_acceleration_access": False,
        "trial_days": 7
    },
    "launch": {
        "name": "Launch Plan",
        "description": "Perfect for growing businesses getting started with customer intelligence",
        "features": [
            "5 websites",
            "50 keywords", 
            "Basic analytics",
            "Basic dashboard/reporting",
            "Basic customer intelligence (5 modules)",
            "Website analytics",
            "Email integration (1K contacts)",
            "2 users",
            "Email support (48hr)"
        ],
        "growth_acceleration_access": True,  # Only for annual subscribers
        "monthly_price": 49,  # Founders pricing
        "annual_price": 490,  # Founders pricing (2 FREE months)
        "regular_monthly_price": 99,
        "regular_annual_price": 990,
        "annual_savings_months": 2
    },
    "growth": {
        "name": "Growth Plan", 
        "description": "Most popular plan for businesses ready to scale their customer insights",
        "features": [
            "Everything in the Launch Plan",
            "Full Customer Intelligence (14 modules)",
            "Real-time Website Health Monitoring",
            "Marketing Automation",
            "10 websites",
            "200 keywords",
            "Full analytics",
            "10 users",
            "Live chat when available + email support (12hr)"
        ],
        "growth_acceleration_access": True,  # Only for annual subscribers
        "monthly_price": 75,  # Founders pricing
        "annual_price": 750,  # Founders pricing (2 FREE months)
        "regular_monthly_price": 149,
        "regular_annual_price": 1490,
        "annual_savings_months": 2,
        "most_popular": True
    },
    "scale": {
        "name": "Scale Plan",
        "description": "Enterprise-grade features for businesses scaling rapidly",
        "features": [
            "Everything in the Growth Plan",
            "AI Command Center",
            "Executive Dashboard", 
            "Unlimited Users",
            "Unlimited websites",
            "Advanced features",
            "Priority support - Live chat when available, 4hr support response time"
        ],
        "growth_acceleration_access": True,  # Only for annual subscribers
        "monthly_price": 199,  # Founders pricing
        "annual_price": 1990,  # Founders pricing (2 FREE months)
        "regular_monthly_price": 399,
        "regular_annual_price": 3990,
        "annual_savings_months": 2
    },
    "white_label": {
        "name": "White Label Plan",
        "description": "Custom white-label solution for agencies and resellers",
        "features": [
            "Everything in the Scale Plan",
            "White-label branding",
            "Custom domain support",
            "Reseller dashboard",
            "Custom pricing controls",
            "Dedicated account manager"
        ],
        "growth_acceleration_access": True,
        "monthly_price": "contact_sales",
        "annual_price": "contact_sales",
        "contact_required": True
    },
    "custom": {
        "name": "Custom Plan",
        "description": "Tailored solution built specifically for your unique business needs",
        "features": [
            "Custom feature development",
            "Dedicated IT support team",
            "Custom integrations",
            "Service level agreements",
            "Priority feature requests",
            "Custom pricing and terms"
        ],
        "growth_acceleration_access": True,
        "monthly_price": "contact_sales",
        "annual_price": "contact_sales", 
        "contact_required": True
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