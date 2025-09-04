# Subscription Management System
import os
import uuid
import bcrypt
from fastapi import APIRouter, HTTPException, Depends, Query
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import secrets
from dotenv import load_dotenv

# Import email system for trial automation
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from email_system import schedule_trial_email_sequence

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter(tags=["Subscriptions"])

# Models
class SubscriptionUpdate(BaseModel):
    plan_type: str
    billing_cycle: str
    is_active: bool = True

class TrialRequest(BaseModel):
    user_email: str
    plan_type: str = "starter"

class TrialRegistration(BaseModel):
    email: str
    first_name: str
    last_name: str
    company_name: Optional[str] = None

class RefundRequest(BaseModel):
    user_email: str
    refund_type: str  # "end_of_cycle" or "immediate"
    reason: Optional[str] = None
    admin_notes: Optional[str] = None

class UsageOverage(BaseModel):
    user_email: str
    resource_type: str  # "contacts", "websites", "keywords", "users", "api_calls"
    current_usage: int
    plan_limit: int
    overage_amount: int
    overage_cost: float

class PrepaidBalance(BaseModel):
    user_email: str
    balance_amount: float
    last_updated: datetime
    transaction_history: List[Dict[str, Any]] = []

# Usage Limits and Overage Pricing
USAGE_LIMITS = {
    "free": {
        "contacts": 100,
        "websites": 1,
        "keywords": 10,
        "users": 1,
        "api_calls_per_month": 1000,
        "email_sends_per_month": 100,
        "data_storage_gb": 1
    },
    "launch": {
        "contacts": 1000,
        "websites": 5,
        "keywords": 50,
        "users": 2,
        "api_calls_per_month": 10000,
        "email_sends_per_month": 1000,
        "data_storage_gb": 10
    },
    "growth": {
        "contacts": 10000,
        "websites": 10,
        "keywords": 200,
        "users": 10,
        "api_calls_per_month": 50000,
        "email_sends_per_month": 10000,
        "data_storage_gb": 50
    },
    "scale": {
        "contacts": float('inf'),  # Unlimited
        "websites": float('inf'),
        "keywords": float('inf'),
        "users": float('inf'),
        "api_calls_per_month": 200000,
        "email_sends_per_month": float('inf'),
        "data_storage_gb": 200
    }
}

# Overage Pricing (per unit when limits exceeded)
OVERAGE_PRICING = {
    "contacts": 0.01,           # $0.01 per extra contact per month
    "websites": 5.00,           # $5.00 per extra website per month
    "keywords": 0.50,           # $0.50 per extra keyword per month
    "users": 10.00,             # $10.00 per extra user per month
    "api_calls": 0.001,         # $0.001 per extra API call (1,000 calls = $1)
    "email_sends": 0.01,        # $0.01 per extra email sent
    "data_storage_gb": 2.00     # $2.00 per extra GB per month
}

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
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

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
        plan_type in ["launch", "growth", "scale", "white_label", "custom"]
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

@router.post("/trial/register")
async def register_trial_user(trial_data: TrialRegistration):
    """Register a new user with 7-day free trial"""
    try:
        # Check if user already exists
        existing_user = await db.users.find_one({"email": trial_data.email})
        
        if existing_user:
            if existing_user.get("has_had_trial", False):
                raise HTTPException(status_code=400, detail="Email already registered and trial used")
            else:
                # User exists but hasn't used trial, activate trial
                trial_end = datetime.utcnow() + timedelta(days=7)
                
                await db.users.update_one(
                    {"email": trial_data.email},
                    {"$set": {
                        "plan_type": "free",
                        "billing_cycle": "trial",
                        "subscription_tier": "free",
                        "subscription_start": datetime.utcnow(),
                        "subscription_end": trial_end,
                        "is_active": True,
                        "is_trial": True,
                        "has_had_trial": True,
                        "updated_at": datetime.utcnow()
                    }}
                )
                
                return {
                    "status": "success",
                    "message": "Trial activated for existing user",
                    "trial_end": trial_end,
                    "user": {
                        "email": trial_data.email,
                        "first_name": existing_user.get("first_name"),
                        "last_name": existing_user.get("last_name")
                    }
                }
        
        # Create new user with trial
        user_id = str(uuid.uuid4())
        trial_end = datetime.utcnow() + timedelta(days=7)
        
        # Generate random password and hash it properly
        temp_password = secrets.token_urlsafe(16)
        
        new_user = {
            "user_id": user_id,
            "email": trial_data.email,
            "first_name": trial_data.first_name,
            "last_name": trial_data.last_name,
            "company_name": trial_data.company_name,
            "phone": None,  # Required by UserProfile
            "password_hash": hash_password(temp_password),  # Store hashed password
            "role": "user",
            "plan_type": "free",
            "billing_cycle": "trial",
            "subscription_tier": "free",
            "subscription_start": datetime.utcnow(),
            "subscription_end": trial_end,
            "is_active": True,
            "is_trial": True,
            "has_had_trial": True,
            "email_verified": False,  # Required by UserProfile
            "last_login": None,  # Required by UserProfile
            "profile_picture": None,  # Required by UserProfile
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.users.insert_one(new_user)
        
        # Schedule trial email sequence
        try:
            await schedule_trial_email_sequence(
                user_email=trial_data.email,
                user_id=user_id,
                first_name=trial_data.first_name,
                trial_start_date=datetime.utcnow(),
                trial_end_date=trial_end,
                login_password=temp_password
            )
        except Exception as e:
            # Log email scheduling error but don't fail the registration
            print(f"WARNING: Failed to schedule trial emails for {trial_data.email}: {str(e)}")
        
        return {
            "status": "success",
            "message": "Trial user registered successfully",
            "trial_end": trial_end,
            "user": {
                "user_id": user_id,
                "email": trial_data.email,
                "first_name": trial_data.first_name,
                "last_name": trial_data.last_name,
                "company_name": trial_data.company_name,
                "password": temp_password  # Return temp password for auto-login
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trial registration failed: {str(e)}")

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
        if "1K contacts" in str(plan_features.get("features", [])):
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

# New endpoints for trial management and referral system

@router.get("/trial-status/{user_email}")
async def get_trial_status(user_email: str):
    """Get detailed trial status with reminder information"""
    try:
        user = await db.users.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        is_trial = user.get("is_trial", False)
        if not is_trial:
            return {
                "status": "success",
                "is_trial": False,
                "message": "User is not on trial"
            }
        
        trial_start = user.get("subscription_start")
        trial_end = user.get("subscription_end")
        
        if not trial_start or not trial_end:
            return {
                "status": "success", 
                "is_trial": False,
                "message": "Trial dates not found"
            }
        
        now = datetime.utcnow()
        days_remaining = (trial_end - now).days
        days_elapsed = (now - trial_start).days
        
        # Determine reminder status
        reminder_needed = False
        reminder_type = None
        
        if days_remaining <= 1:
            reminder_needed = True
            reminder_type = "trial_ending"
        elif days_remaining <= 2:
            reminder_needed = True
            reminder_type = "5_day_reminder"
        elif days_remaining <= 4:
            reminder_needed = True
            reminder_type = "3_day_reminder"
        
        return {
            "status": "success",
            "is_trial": True,
            "trial_start": trial_start,
            "trial_end": trial_end,
            "days_remaining": days_remaining,
            "days_elapsed": days_elapsed,
            "reminder_needed": reminder_needed,
            "reminder_type": reminder_type,
            "data_retention_until": trial_end + timedelta(days=14)  # 2 weeks after trial
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trial status check failed: {str(e)}")

@router.post("/apply-referral-discount")
async def apply_referral_discount(referral_data: dict):
    """Apply 30% referral discount to next billing cycle"""
    try:
        referrer_email = referral_data.get("referrer_email", "").lower()
        referee_email = referral_data.get("referee_email", "").lower()
        
        if not referrer_email or not referee_email:
            raise HTTPException(status_code=400, detail="Both referrer and referee emails required")
        
        # Check if referrer exists and is active subscriber
        referrer = await db.users.find_one({"email": referrer_email})
        if not referrer:
            raise HTTPException(status_code=404, detail="Referrer not found")
        
        if not referrer.get("is_active") or referrer.get("subscription_tier") == "trial":
            raise HTTPException(status_code=400, detail="Referrer must be an active paying subscriber")
        
        # Check if referee exists and is new subscriber
        referee = await db.users.find_one({"email": referee_email})
        if not referee:
            raise HTTPException(status_code=404, detail="Referee not found")
        
        # Check if referral already applied
        existing_referral = await db.referrals.find_one({
            "referrer_email": referrer_email,
            "referee_email": referee_email
        })
        
        if existing_referral:
            raise HTTPException(status_code=400, detail="Referral discount already applied")
        
        # Calculate discount amount (30% of next billing cycle)
        next_billing_amount = 0
        referrer_plan = referrer.get("plan_type", "launch")
        referrer_cycle = referrer.get("billing_cycle", "monthly")
        
        plan_data = SUBSCRIPTION_FEATURES.get(referrer_plan, {})
        if referrer_cycle == "annual":
            next_billing_amount = plan_data.get("annual_price", 0)
        else:
            next_billing_amount = plan_data.get("monthly_price", 0)
        
        discount_amount = int(next_billing_amount * 0.30)
        
        # Create referral record
        referral_record = {
            "id": secrets.token_urlsafe(16),
            "referrer_email": referrer_email,
            "referee_email": referee_email,
            "discount_percentage": 30,
            "discount_amount": discount_amount,
            "applied_date": datetime.utcnow(),
            "status": "pending",
            "referrer_billing_cycle": referrer_cycle,
            "next_billing_date": referrer.get("subscription_end"),
            "is_annual_subscriber": referrer.get("subscription_tier") == "annual"
        }
        
        await db.referrals.insert_one(referral_record)
        
        return {
            "status": "success",
            "message": f"30% referral discount applied to {referrer_email}",
            "discount_amount": discount_amount,
            "next_billing_discount": f"${discount_amount/100:.2f}",
            "applies_to": "next_billing_cycle" if referrer_cycle == "monthly" else "next_annual_renewal"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Referral discount application failed: {str(e)}")

@router.get("/referral-history/{user_email}")
async def get_referral_history(user_email: str):
    """Get user's referral history and available discounts"""
    try:
        # Get referrals where user is referrer
        referrals_made = await db.referrals.find({"referrer_email": user_email}).to_list(length=100)
        
        # Get referrals where user was referred
        referrals_received = await db.referrals.find({"referee_email": user_email}).to_list(length=100)
        
        # Calculate total discount earned
        total_discount_earned = sum([r.get("discount_amount", 0) for r in referrals_made])
        
        return {
            "status": "success",
            "referrals_made": len(referrals_made),
            "referrals_received": len(referrals_received),
            "total_discount_earned": total_discount_earned,
            "total_discount_formatted": f"${total_discount_earned/100:.2f}",
            "referral_details": {
                "made": referrals_made,
                "received": referrals_received
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Referral history fetch failed: {str(e)}")

@router.post("/upgrade-subscription")
async def upgrade_subscription(upgrade_data: dict):
    """Upgrade subscription with prorated billing"""
    try:
        user_email = upgrade_data.get("user_email")
        new_plan_type = upgrade_data.get("new_plan_type")
        new_billing_cycle = upgrade_data.get("new_billing_cycle", "monthly")
        
        if not user_email or not new_plan_type:
            raise HTTPException(status_code=400, detail="User email and new plan type required")
        
        user = await db.users.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_plan = user.get("plan_type", "launch")
        current_cycle = user.get("billing_cycle", "monthly")
        
        # Validate upgrade path
        plan_hierarchy = ["launch", "growth", "scale", "white_label", "custom"]
        current_idx = plan_hierarchy.index(current_plan) if current_plan in plan_hierarchy else 0
        new_idx = plan_hierarchy.index(new_plan_type) if new_plan_type in plan_hierarchy else 0
        
        # Calculate prorated amount
        current_plan_data = SUBSCRIPTION_FEATURES.get(current_plan, {})
        new_plan_data = SUBSCRIPTION_FEATURES.get(new_plan_type, {})
        
        current_price = current_plan_data.get(f"{current_cycle}_price", 0)
        new_price = new_plan_data.get(f"{new_billing_cycle}_price", 0)
        
        # Calculate remaining days in current cycle
        subscription_end = user.get("subscription_end")
        now = datetime.utcnow()
        
        if subscription_end and subscription_end > now:
            days_remaining = (subscription_end - now).days
            cycle_days = 365 if current_cycle == "annual" else 30
            
            # Calculate prorated refund for current plan
            unused_amount = (current_price * days_remaining) / cycle_days
            
            # Calculate prorated charge for new plan
            new_cycle_days = 365 if new_billing_cycle == "annual" else 30
            prorated_new_amount = (new_price * days_remaining) / new_cycle_days
            
            # Net amount to charge
            net_charge = max(0, prorated_new_amount - unused_amount)
        else:
            net_charge = new_price
        
        # Update subscription
        new_subscription_end = now + timedelta(days=365 if new_billing_cycle == "annual" else 30)
        
        update_data = {
            "plan_type": new_plan_type,
            "billing_cycle": new_billing_cycle,
            "subscription_tier": "annual" if new_billing_cycle == "annual" else "monthly",
            "subscription_end": new_subscription_end,
            "upgraded_at": now,
            "previous_plan": current_plan,
            "upgrade_prorated_charge": net_charge
        }
        
        await db.users.update_one(
            {"email": user_email},
            {"$set": update_data}
        )
        
        return {
            "status": "success",
            "message": "Subscription upgraded successfully",
            "previous_plan": current_plan,
            "new_plan": new_plan_type,
            "prorated_charge": net_charge,
            "prorated_charge_formatted": f"${net_charge/100:.2f}",
            "new_subscription_end": new_subscription_end
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription upgrade failed: {str(e)}")

@router.post("/cancel-subscription-with-refund")
async def cancel_subscription_with_refund(cancellation_data: dict):
    """Cancel subscription with refund options as per pricing policy"""
    try:
        user_email = cancellation_data.get("user_email")
        cancellation_type = cancellation_data.get("type", "immediate")  # "immediate" or "end_of_cycle"
        
        if not user_email:
            raise HTTPException(status_code=400, detail="User email required")
        
        user = await db.users.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        subscription_end = user.get("subscription_end")
        subscription_start = user.get("subscription_start")
        billing_cycle = user.get("billing_cycle", "monthly")
        plan_type = user.get("plan_type", "launch")
        
        if not user.get("is_active"):
            raise HTTPException(status_code=400, detail="No active subscription to cancel")
        
        now = datetime.utcnow()
        
        # Calculate refund amount based on cancellation type
        refund_amount = 0
        
        if cancellation_type == "immediate" and subscription_end and subscription_end > now:
            # Calculate prorated refund for remaining time
            days_remaining = (subscription_end - now).days
            cycle_days = 365 if billing_cycle == "annual" else 30
            
            plan_data = SUBSCRIPTION_FEATURES.get(plan_type, {})
            paid_amount = plan_data.get(f"{billing_cycle}_price", 0)
            
            refund_amount = (paid_amount * days_remaining) / cycle_days
        
        # Create cancellation record
        cancellation_record = {
            "id": secrets.token_urlsafe(16),
            "user_email": user_email,
            "plan_type": plan_type,
            "billing_cycle": billing_cycle,
            "cancellation_type": cancellation_type,
            "cancellation_date": now,
            "refund_amount": refund_amount,
            "refund_status": "pending",
            "original_subscription_end": subscription_end,
            "reason": cancellation_data.get("reason", ""),
            "processing_time": "within_48_hours"
        }
        
        await db.cancellations.insert_one(cancellation_record)
        
        # Update user subscription status
        if cancellation_type == "immediate":
            cancellation_effective_date = now
        else:
            cancellation_effective_date = subscription_end
        
        await db.users.update_one(
            {"email": user_email},
            {
                "$set": {
                    "is_active": False if cancellation_type == "immediate" else True,
                    "subscription_tier": "cancelled",
                    "cancellation_scheduled": cancellation_effective_date,
                    "cancelled_at": now,
                    "data_retention_until": cancellation_effective_date + timedelta(days=14)
                }
            }
        )
        
        return {
            "status": "success",
            "message": "Subscription cancelled successfully",
            "cancellation_type": cancellation_type,
            "effective_date": cancellation_effective_date,
            "refund_amount": refund_amount,
            "refund_formatted": f"${refund_amount/100:.2f}",
            "refund_processing": "Refunds processed within 1-2 business days",
            "data_retention": "Data will be retained for 2 weeks after cancellation"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription cancellation failed: {str(e)}")

# Legacy endpoint maintained for backward compatibility
@router.post("/cancel-subscription/{user_email}")
async def cancel_subscription(user_email: str):
    """Cancel user's subscription (legacy endpoint)"""
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

# ==============================================================================
# ENHANCED REFUND SYSTEM WITH PREPAID BALANCE SUPPORT
# ==============================================================================

@router.post("/admin/process-refund")
async def admin_process_refund(refund_request: RefundRequest):
    """Admin endpoint for processing refunds with prepaid balance support"""
    try:
        user = await db.users.find_one({"email": refund_request.user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get current subscription details
        subscription_end = user.get("subscription_end")
        subscription_start = user.get("subscription_start")
        billing_cycle = user.get("billing_cycle", "monthly")
        plan_type = user.get("plan_type", "launch")
        now = datetime.utcnow()
        
        # Get prepaid balance
        prepaid_balance = await db.prepaid_balances.find_one({"user_email": refund_request.user_email})
        prepaid_amount = prepaid_balance.get("balance_amount", 0) if prepaid_balance else 0
        
        # Calculate refunds based on refund type
        subscription_refund = 0
        
        if refund_request.refund_type == "immediate" and subscription_end and subscription_end > now:
            # Calculate prorated refund for remaining time
            days_remaining = (subscription_end - now).days
            cycle_days = 365 if billing_cycle == "annual" else 30
            
            plan_data = SUBSCRIPTION_FEATURES.get(plan_type, {})
            paid_amount = plan_data.get(f"{billing_cycle}_price", 0)
            
            # Prorated refund calculation
            subscription_refund = (paid_amount * days_remaining) / cycle_days
        
        # Total refund = subscription refund + prepaid balance
        total_refund = subscription_refund + prepaid_amount
        
        # Create refund record
        refund_record = {
            "refund_id": str(uuid.uuid4()),
            "user_email": refund_request.user_email,
            "refund_type": refund_request.refund_type,
            "subscription_refund": subscription_refund,
            "prepaid_refund": prepaid_amount,
            "total_refund": total_refund,
            "reason": refund_request.reason,
            "admin_notes": refund_request.admin_notes,
            "status": "pending",
            "created_at": now,
            "processed_at": None,
            "original_plan": plan_type,
            "original_billing_cycle": billing_cycle,
            "cancellation_effective_date": now if refund_request.refund_type == "immediate" else subscription_end
        }
        
        await db.refund_requests.insert_one(refund_record)
        
        # Update user status based on refund type
        if refund_request.refund_type == "immediate":
            # Immediate cancellation
            await db.users.update_one(
                {"email": refund_request.user_email},
                {"$set": {
                    "is_active": False,
                    "subscription_tier": "cancelled",
                    "cancelled_at": now,
                    "cancellation_type": "immediate_with_refund",
                    "data_retention_until": now + timedelta(days=14)
                }}
            )
            
            # Clear prepaid balance
            if prepaid_balance:
                await db.prepaid_balances.update_one(
                    {"user_email": refund_request.user_email},
                    {"$set": {"balance_amount": 0, "last_updated": now}}
                )
        else:
            # End of cycle cancellation - just refund prepaid balance
            await db.users.update_one(
                {"email": refund_request.user_email},
                {"$set": {
                    "cancellation_scheduled": subscription_end,
                    "cancellation_type": "end_of_cycle_with_prepaid_refund",
                    "prepaid_refund_processed": True
                }}
            )
            
            # Clear prepaid balance but keep subscription active until end
            if prepaid_balance:
                await db.prepaid_balances.update_one(
                    {"user_email": refund_request.user_email},
                    {"$set": {"balance_amount": 0, "last_updated": now}}
                )
        
        return {
            "status": "success",
            "message": "Refund processed successfully",
            "refund_details": {
                "refund_id": refund_record["refund_id"],
                "refund_type": refund_request.refund_type,
                "subscription_refund": f"${subscription_refund/100:.2f}",
                "prepaid_refund": f"${prepaid_amount/100:.2f}",
                "total_refund": f"${total_refund/100:.2f}",
                "effective_date": refund_record["cancellation_effective_date"],
                "processing_time": "1-2 business days"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refund processing failed: {str(e)}")

@router.get("/admin/refund-requests")
async def get_refund_requests(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200)
):
    """Get all refund requests for admin review"""
    try:
        query = {}
        if status:
            query["status"] = status
        
        requests = await db.refund_requests.find(query).sort("created_at", -1).limit(limit).to_list(length=None)
        
        # Format for display
        for request in requests:
            request["_id"] = str(request["_id"])
            request["created_at_formatted"] = request["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            if request.get("processed_at"):
                request["processed_at_formatted"] = request["processed_at"].strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "status": "success",
            "total_requests": len(requests),
            "refund_requests": requests
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch refund requests: {str(e)}")

# ==============================================================================
# USAGE TRACKING AND OVERAGE BILLING SYSTEM
# ==============================================================================

@router.get("/usage/{user_email}")
async def get_detailed_usage(user_email: str):
    """Get detailed usage statistics with overage calculations"""
    try:
        user = await db.users.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        plan_type = user.get("plan_type", "free")
        limits = USAGE_LIMITS.get(plan_type, USAGE_LIMITS["free"])
        
        # Get actual usage data (this would be populated by your various modules)
        current_usage = {
            "contacts": await db.customers.count_documents({"owner_email": user_email}),
            "websites": await db.websites.count_documents({"user_email": user_email}) if "websites" in await db.list_collection_names() else 0,
            "keywords": await db.keywords.count_documents({"user_email": user_email}) if "keywords" in await db.list_collection_names() else 0,
            "users": await db.team_members.count_documents({"team_owner": user_email}) if "team_members" in await db.list_collection_names() else 1,
            "api_calls_per_month": await get_monthly_api_calls(user_email),
            "email_sends_per_month": await get_monthly_email_sends(user_email),
            "data_storage_gb": await calculate_data_storage(user_email)
        }
        
        # Calculate overages and costs
        usage_details = {}
        total_overage_cost = 0
        
        for resource, current in current_usage.items():
            limit = limits.get(resource, 0)
            overage = max(0, current - limit) if limit != float('inf') else 0
            overage_cost = overage * OVERAGE_PRICING.get(resource, 0) if limit != float('inf') else 0
            total_overage_cost += overage_cost
            
            usage_details[resource] = {
                "current": current,
                "limit": limit if limit != float('inf') else "Unlimited",
                "overage": overage,
                "overage_cost": f"${overage_cost:.2f}",
                "percentage_used": round((current / limit * 100) if limit != float('inf') else 0, 1),
                "status": "over_limit" if overage > 0 else "within_limit"
            }
        
        return {
            "status": "success",
            "user_email": user_email,
            "plan_type": plan_type,
            "usage_details": usage_details,
            "total_overage_cost": f"${total_overage_cost:.2f}",
            "billing_note": "Overages will be charged on your next billing cycle" if total_overage_cost > 0 else "All usage within plan limits"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Usage calculation failed: {str(e)}")

@router.post("/admin/charge-overages")
async def charge_usage_overages():
    """Admin endpoint to process monthly overage charges for all users"""
    try:
        # Get all active users
        active_users = await db.users.find({"is_active": True}).to_list(length=None)
        
        overage_charges = []
        total_charges = 0
        
        for user in active_users:
            user_email = user["email"]
            plan_type = user.get("plan_type", "free")
            
            # Skip scale plan users (they have high limits)
            if plan_type == "scale":
                continue
            
            # Get usage and calculate overages
            usage_response = await get_detailed_usage(user_email)
            usage_details = usage_response["usage_details"]
            
            user_overage_cost = 0
            overage_items = []
            
            for resource, details in usage_details.items():
                if details["status"] == "over_limit":
                    overage_cost = float(details["overage_cost"].replace("$", ""))
                    if overage_cost > 0:
                        user_overage_cost += overage_cost
                        overage_items.append({
                            "resource": resource,
                            "overage_amount": details["overage"],
                            "cost": overage_cost
                        })
            
            if user_overage_cost > 0:
                # Create overage charge record
                overage_record = {
                    "charge_id": str(uuid.uuid4()),
                    "user_email": user_email,
                    "plan_type": plan_type,
                    "billing_period": datetime.utcnow().strftime("%Y-%m"),
                    "overage_items": overage_items,
                    "total_charge": user_overage_cost,
                    "status": "pending",
                    "created_at": datetime.utcnow()
                }
                
                await db.overage_charges.insert_one(overage_record)
                overage_charges.append(overage_record)
                total_charges += user_overage_cost
        
        return {
            "status": "success",
            "message": f"Processed overage charges for {len(overage_charges)} users",
            "total_charges": f"${total_charges:.2f}",
            "overage_charges": overage_charges
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Overage charging failed: {str(e)}")

# Helper functions for usage calculations
async def get_monthly_api_calls(user_email: str) -> int:
    """Get API calls for current month"""
    try:
        # This would track API calls - implement based on your API logging
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Placeholder - implement actual API call tracking
        api_logs = await db.api_logs.count_documents({
            "user_email": user_email,
            "timestamp": {"$gte": current_month_start}
        }) if "api_logs" in await db.list_collection_names() else 0
        
        return api_logs
    except:
        return 0

async def get_monthly_email_sends(user_email: str) -> int:
    """Get emails sent for current month"""
    try:
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Count from email campaigns and trial emails
        email_sends = await db.email_campaigns.aggregate([
            {"$match": {
                "user_email": user_email,
                "sent_at": {"$gte": current_month_start}
            }},
            {"$group": {"_id": None, "total": {"$sum": "$recipient_count"}}}
        ]).to_list(length=1)
        
        return email_sends[0]["total"] if email_sends else 0
    except:
        return 0

async def calculate_data_storage(user_email: str) -> float:
    """Calculate data storage usage in GB"""
    try:
        # This would calculate actual data storage - placeholder implementation
        # You'd need to track file uploads, database size per user, etc.
        
        # Estimate based on customer records and other data
        customer_count = await db.customers.count_documents({"owner_email": user_email})
        campaigns_count = await db.email_campaigns.count_documents({"user_email": user_email})
        
        # Rough estimate: each customer = 1KB, each campaign = 10KB
        estimated_gb = (customer_count * 0.001 + campaigns_count * 0.01) / 1024
        
        return round(estimated_gb, 2)
    except:
        return 0.1  # Minimum usage