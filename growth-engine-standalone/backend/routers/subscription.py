"""
Subscription management router for Growth Acceleration Engine
Handles pricing plans, Stripe integration, and subscription status
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

class SubscriptionCreate(BaseModel):
    plan_id: str
    billing_cycle: str  # "monthly" or "annual"
    payment_method_id: str

class SubscriptionResponse(BaseModel):
    id: str
    plan_id: str
    plan_name: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    billing_cycle: str
    amount: int

# Pricing plans configuration
PRICING_PLANS = {
    "growth_starter": PricingPlan(
        id="growth_starter",
        name="Growth Starter",
        description="Perfect for small businesses starting their growth journey",
        monthly_price=9700,  # $97
        annual_price=97000,  # $970 (2 months free)
        features=[
            "Basic growth insights",
            "3 key metrics tracking",
            "Monthly reports",
            "Email support",
            "Growth opportunity scanner"
        ]
    ),
    "growth_professional": PricingPlan(
        id="growth_professional",
        name="Growth Professional",
        description="Complete growth acceleration suite for growing businesses",
        monthly_price=19700,  # $197
        annual_price=197000,  # $1,970 (2 months free)
        features=[
            "Full Growth Acceleration suite",
            "Unlimited metrics tracking",
            "Weekly AI insights",
            "Advanced predictions",
            "A/B testing automation",
            "Revenue leak detection",
            "ROI calculator",
            "Priority support"
        ],
        is_popular=True
    ),
    "growth_enterprise": PricingPlan(
        id="growth_enterprise",
        name="Growth Enterprise",
        description="Advanced growth optimization for scaling businesses",
        monthly_price=39700,  # $397
        annual_price=397000,  # $3,970 (2 months free)
        features=[
            "Everything in Professional",
            "Custom growth strategies",
            "Real-time optimization",
            "Dedicated account manager",
            "Custom integrations",
            "White-label options",
            "Phone + email support",
            "Custom reporting"
        ]
    )
}

# Subscription endpoints
@subscription_router.get("/plans", response_model=Dict[str, PricingPlan])
async def get_pricing_plans():
    """Get all available pricing plans"""
    return PRICING_PLANS

@subscription_router.get("/plans/{plan_id}", response_model=PricingPlan)
async def get_pricing_plan(plan_id: str):
    """Get specific pricing plan"""
    if plan_id not in PRICING_PLANS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing plan not found"
        )
    return PRICING_PLANS[plan_id]

@subscription_router.post("/create-subscription", response_model=Dict[str, str])
async def create_subscription(
    subscription_data: SubscriptionCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Create new subscription with Stripe"""
    db = request.state.db
    
    # Validate plan
    if subscription_data.plan_id not in PRICING_PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pricing plan"
        )
    
    plan = PRICING_PLANS[subscription_data.plan_id]
    
    # Calculate price based on billing cycle
    if subscription_data.billing_cycle == "monthly":
        amount = plan.monthly_price
        interval = "month"
    elif subscription_data.billing_cycle == "annual":
        amount = plan.annual_price
        interval = "year"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid billing cycle"
        )
    
    try:
        # Create or retrieve Stripe customer
        stripe_customer = None
        user_email = current_user["email"]
        
        # Check if customer already exists
        customers = stripe.Customer.list(email=user_email, limit=1)
        if customers.data:
            stripe_customer = customers.data[0]
        else:
            # Create new customer
            stripe_customer = stripe.Customer.create(
                email=user_email,
                name=current_user.get("full_name", ""),
                metadata={
                    "user_id": current_user["id"],
                    "company": current_user.get("company_name", "")
                }
            )
        
        # Create price object if not exists
        price_id = f"price_{subscription_data.plan_id}_{subscription_data.billing_cycle}"
        
        try:
            price = stripe.Price.retrieve(price_id)
        except stripe.error.InvalidRequestError:
            # Create price
            price = stripe.Price.create(
                unit_amount=amount,
                currency="usd",
                recurring={"interval": interval},
                product_data={
                    "name": plan.name,
                    "description": plan.description
                },
                metadata={"plan_id": subscription_data.plan_id}
            )
        
        # Create subscription
        stripe_subscription = stripe.Subscription.create(
            customer=stripe_customer.id,
            items=[{"price": price.id}],
            payment_behavior="default_incomplete",
            payment_settings={"save_default_payment_method": "on_subscription"},
            expand=["latest_invoice.payment_intent"],
            metadata={
                "user_id": current_user["id"],
                "plan_id": subscription_data.plan_id,
                "billing_cycle": subscription_data.billing_cycle
            }
        )
        
        # Update user subscription in database
        await db.users.update_one(
            {"email": user_email},
            {
                "$set": {
                    "subscription_status": "active",
                    "subscription_plan": subscription_data.plan_id,
                    "stripe_customer_id": stripe_customer.id,
                    "stripe_subscription_id": stripe_subscription.id,
                    "subscription_start": datetime.now(timezone.utc),
                    "subscription_end": datetime.now(timezone.utc) + timedelta(days=30 if interval == "month" else 365),
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        
        return {
            "subscription_id": stripe_subscription.id,
            "client_secret": stripe_subscription.latest_invoice.payment_intent.client_secret,
            "status": stripe_subscription.status
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment processing error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Subscription creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create subscription"
        )

@subscription_router.get("/current", response_model=Dict[str, Any])
async def get_current_subscription(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get current user's subscription details"""
    db = request.state.db
    
    user = await db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    subscription_info = {
        "status": user.get("subscription_status", "trial"),
        "plan": user.get("subscription_plan", "growth_professional"),
        "plan_name": PRICING_PLANS.get(user.get("subscription_plan", "growth_professional"), PRICING_PLANS["growth_professional"]).name,
        "subscription_start": user.get("subscription_start"),
        "subscription_end": user.get("subscription_end"),
        "trial_end_date": user.get("trial_end_date"),
        "stripe_customer_id": user.get("stripe_customer_id"),
        "stripe_subscription_id": user.get("stripe_subscription_id")
    }
    
    # If user has Stripe subscription, get latest info
    if user.get("stripe_subscription_id"):
        try:
            stripe_subscription = stripe.Subscription.retrieve(user["stripe_subscription_id"])
            subscription_info.update({
                "status": stripe_subscription.status,
                "current_period_start": datetime.fromtimestamp(stripe_subscription.current_period_start, tz=timezone.utc),
                "current_period_end": datetime.fromtimestamp(stripe_subscription.current_period_end, tz=timezone.utc),
                "amount": stripe_subscription.items.data[0].price.unit_amount if stripe_subscription.items.data else 0
            })
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve Stripe subscription: {e}")
    
    return subscription_info

@subscription_router.post("/cancel")
async def cancel_subscription(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Cancel current subscription"""
    db = request.state.db
    
    user = await db.users.find_one({"email": current_user["email"]})
    if not user or not user.get("stripe_subscription_id"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    try:
        # Cancel Stripe subscription at period end
        stripe.Subscription.modify(
            user["stripe_subscription_id"],
            cancel_at_period_end=True
        )
        
        # Update user record
        await db.users.update_one(
            {"email": current_user["email"]},
            {
                "$set": {
                    "subscription_status": "cancelled",
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        
        return {"message": "Subscription cancelled successfully"}
        
    except stripe.error.StripeError as e:
        logger.error(f"Failed to cancel subscription: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to cancel subscription: {str(e)}"
        )

@subscription_router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "invoice.payment_succeeded":
        # Payment succeeded
        subscription_id = event["data"]["object"]["subscription"]
        logger.info(f"Payment succeeded for subscription: {subscription_id}")
        
    elif event["type"] == "invoice.payment_failed":
        # Payment failed
        subscription_id = event["data"]["object"]["subscription"]
        logger.info(f"Payment failed for subscription: {subscription_id}")
        
    elif event["type"] == "customer.subscription.updated":
        # Subscription updated
        subscription = event["data"]["object"]
        logger.info(f"Subscription updated: {subscription['id']}")
        
    elif event["type"] == "customer.subscription.deleted":
        # Subscription cancelled
        subscription = event["data"]["object"]
        logger.info(f"Subscription cancelled: {subscription['id']}")
    
    return {"status": "success"}