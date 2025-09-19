"""
Subscription management for Growth Acceleration Engine
Handles pricing plans, Stripe integration, and trial conversion
"""

import os
import stripe
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from .auth import get_current_user

logger = logging.getLogger(__name__)

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Router
subscription_router = APIRouter()

# Pydantic models
class PricingPlan(BaseModel):
    id: str
    name: str
    description: str
    monthly_price: int  # in cents
    annual_price: int   # in cents
    features: List[str]
    is_popular: bool = False
    founders_price_monthly: int  # in cents
    founders_price_annual: int   # in cents

class SubscriptionCreate(BaseModel):
    plan_id: str
    billing_cycle: str  # "monthly" or "annual"
    use_founders_pricing: bool = False

class TrialInfo(BaseModel):
    is_trial_active: bool
    trial_start_date: datetime
    trial_end_date: datetime
    days_remaining: int
    trial_plan: str

# Pricing plans with your structure
PRICING_PLANS = {
    "growth_starter": PricingPlan(
        id="growth_starter",
        name="Growth Starter",
        description="Perfect for small businesses starting their growth journey",
        monthly_price=13900,  # $139
        annual_price=139000,  # $1,390
        founders_price_monthly=11900,  # $119
        founders_price_annual=119000,  # $1,190
        features=[
            "Growth opportunity scanner",
            "Basic revenue leak detection",
            "3 key metrics tracking",
            "Monthly reports",
            "Email support",
            "7-day free trial"
        ]
    ),
    "growth_professional": PricingPlan(
        id="growth_professional",
        name="Growth Professional",
        description="Complete growth acceleration suite for growing businesses",
        monthly_price=24900,  # $249
        annual_price=247000,  # $2,470
        founders_price_monthly=12400,  # $124
        founders_price_annual=124000,  # $1,240
        features=[
            "Everything in Growth Starter",
            "Advanced A/B testing engine",
            "Complete revenue leak analysis",
            "ROI calculator & projections",
            "Unlimited metrics tracking",
            "Weekly AI insights",
            "Priority support",
            "7-day free trial"
        ],
        is_popular=True
    ),
    "growth_enterprise": PricingPlan(
        id="growth_enterprise",
        name="Growth Enterprise",
        description="Advanced growth optimization for scaling businesses",
        monthly_price=44900,  # $449
        annual_price=449000,  # $4,490
        founders_price_monthly=22400,  # $224
        founders_price_annual=224000,  # $2,240
        features=[
            "Everything in Professional",
            "Real-time growth optimization",
            "Custom growth strategies",
            "Dedicated account manager",
            "Advanced integrations",
            "White-label options",
            "Phone + email support",
            "7-day free trial"
        ]
    )
}

# Subscription endpoints
@subscription_router.get("/plans", response_model=Dict[str, PricingPlan])
async def get_pricing_plans():
    """Get all available pricing plans"""
    return PRICING_PLANS

@subscription_router.get("/trial-status", response_model=TrialInfo)
async def get_trial_status(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get current user's trial status"""
    trial_start = current_user.get("trial_start_date", datetime.now(timezone.utc))
    trial_end = current_user.get("trial_end_date", datetime.now(timezone.utc))
    is_trial_active = current_user.get("is_trial_active", False)
    days_remaining = current_user.get("trial_days_remaining", 0)
    
    return TrialInfo(
        is_trial_active=is_trial_active,
        trial_start_date=trial_start,
        trial_end_date=trial_end,
        days_remaining=days_remaining,
        trial_plan=current_user.get("subscription_plan", "growth_professional")
    )

@subscription_router.get("/founders-eligibility")
async def check_founders_eligibility(
    current_user: dict = Depends(get_current_user)
):
    """Check if user is eligible for founders pricing"""
    founders_eligible = current_user.get("founders_eligible", False)
    already_used = current_user.get("founders_pricing_used", False)
    
    return {
        "founders_eligible": founders_eligible and not already_used,
        "founders_pricing_used": already_used,
        "discount_percentage": 50,
        "message": "🎉 Founders Pricing: Get 50% off forever!" if founders_eligible and not already_used else "Founders pricing not available"
    }

@subscription_router.post("/create-subscription")
async def create_subscription(
    subscription_data: SubscriptionCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Create new subscription (convert from trial)"""
    db = request.state.db
    
    # Validate plan
    if subscription_data.plan_id not in PRICING_PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pricing plan"
        )
    
    plan = PRICING_PLANS[subscription_data.plan_id]
    
    # Determine pricing based on founders eligibility
    if subscription_data.use_founders_pricing and current_user.get("founders_eligible", False):
        if subscription_data.billing_cycle == "monthly":
            amount = plan.founders_price_monthly
        else:
            amount = plan.founders_price_annual
        plan_name = f"{plan.name} - Founders"
    else:
        if subscription_data.billing_cycle == "monthly":
            amount = plan.monthly_price
        else:
            amount = plan.annual_price
        plan_name = plan.name
    
    try:
        # Create Stripe customer
        stripe_customer = stripe.Customer.create(
            email=current_user["email"],
            name=current_user.get("full_name", ""),
            metadata={
                "user_id": current_user["id"],
                "company": current_user.get("company_name", ""),
                "founders_pricing": str(subscription_data.use_founders_pricing)
            }
        )
        
        # Create subscription (this would typically involve payment setup)
        # For now, we'll mark as active assuming payment succeeded
        
        # Update user subscription in database
        await db.users.update_one(
            {"email": current_user["email"]},
            {
                "$set": {
                    "subscription_status": "active",
                    "subscription_plan": subscription_data.plan_id,
                    "billing_cycle": subscription_data.billing_cycle,
                    "stripe_customer_id": stripe_customer.id,
                    "subscription_start": datetime.now(timezone.utc),
                    "is_trial_active": False,
                    "founders_pricing_used": subscription_data.use_founders_pricing,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        
        return {
            "message": "Subscription created successfully",
            "plan_name": plan_name,
            "amount": amount,
            "billing_cycle": subscription_data.billing_cycle,
            "founders_pricing": subscription_data.use_founders_pricing
        }
        
    except Exception as e:
        logger.error(f"Subscription creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create subscription"
        )

@subscription_router.get("/current")
async def get_current_subscription(current_user: dict = Depends(get_current_user)):
    """Get current user's subscription details"""
    return {
        "status": current_user.get("subscription_status", "trial"),
        "plan": current_user.get("subscription_plan", "growth_professional"),
        "plan_name": PRICING_PLANS.get(current_user.get("subscription_plan", "growth_professional")).name,
        "billing_cycle": current_user.get("billing_cycle", "monthly"),
        "trial_days_remaining": current_user.get("trial_days_remaining", 0),
        "is_trial_active": current_user.get("is_trial_active", False),
        "founders_eligible": current_user.get("founders_eligible", False),
        "founders_pricing_used": current_user.get("founders_pricing_used", False)
    }