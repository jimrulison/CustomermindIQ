# Payment System with Stripe Integration
import os
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import stripe
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_API_KEY", "sk_test_emergent")

router = APIRouter(prefix="/api/payments", tags=["Payments"])

# Models
class PaymentRequest(BaseModel):
    plan_type: str  # 'starter', 'professional', 'enterprise'
    billing_cycle: str  # 'monthly', 'annual'
    discount_code: Optional[str] = None

class PaymentMethodRequest(BaseModel):
    payment_method_id: str
    customer_email: str

# Subscription Plans Configuration - Updated with New Pricing Structure
SUBSCRIPTION_PLANS = {
    "launch": {
        "name": "Launch Plan",
        "description": "Perfect for growing businesses getting started with customer intelligence",
        "monthly_price": 4900,  # $49 in cents (founders pricing)
        "annual_price": 49000,  # $490 in cents (founders pricing, 2 months free)
        "regular_monthly_price": 9900,  # $99 in cents (regular pricing)
        "regular_annual_price": 99000,  # $990 in cents (regular pricing)
        "features": [
            "5 websites",
            "50 keywords", 
            "Basic analytics",
            "Basic dashboard/reporting",
            "Basic customer intelligence (5 modules)",
            "Website analytics",
            "Email integration (1K contacts)",
            "2 users",
            "Email support (48hr)",
            "Growth Acceleration Engine (Annual Only)"
        ]
    },
    "growth": {
        "name": "Growth Plan", 
        "description": "Most popular plan for businesses ready to scale their customer insights",
        "monthly_price": 7500,  # $75 in cents (founders pricing)
        "annual_price": 75000,  # $750 in cents (founders pricing, 2 months free)
        "regular_monthly_price": 14900,  # $149 in cents (regular pricing)
        "regular_annual_price": 149000,  # $1490 in cents (regular pricing)
        "most_popular": True,
        "features": [
            "Everything in the Launch Plan",
            "Full Customer Intelligence (14 modules)",
            "Real-time Website Health Monitoring",
            "Marketing Automation",
            "10 websites",
            "200 keywords",
            "Full analytics",
            "10 users",
            "Live chat when available + email support (12hr)",
            "Growth Acceleration Engine (Annual Only)"
        ]
    },
    "scale": {
        "name": "Scale Plan",
        "description": "Enterprise-grade features for businesses scaling rapidly",
        "monthly_price": 19900,  # $199 in cents (founders pricing)
        "annual_price": 199000,  # $1990 in cents (founders pricing, 2 months free)
        "regular_monthly_price": 39900,  # $399 in cents (regular pricing)
        "regular_annual_price": 399000,  # $3990 in cents (regular pricing)
        "features": [
            "Everything in the Growth Plan",
            "AI Command Center",
            "Executive Dashboard", 
            "Unlimited Users",
            "Unlimited websites",
            "Advanced features",
            "Priority support - Live chat when available, 4hr support response time",
            "Growth Acceleration Engine (Annual Only)"
        ]
    },
    "white_label": {
        "name": "White Label Plan",
        "description": "Custom white-label solution for agencies and resellers",
        "monthly_price": "contact_sales",
        "annual_price": "contact_sales",
        "contact_required": True,
        "features": [
            "Everything in the Scale Plan",
            "White-label branding",
            "Custom domain support",
            "Reseller dashboard",
            "Custom pricing controls",
            "Dedicated account manager",
            "Growth Acceleration Engine (Annual Only)"
        ]
    },
    "custom": {
        "name": "Custom Plan",
        "description": "Tailored solution built specifically for your unique business needs",
        "monthly_price": "contact_sales",
        "annual_price": "contact_sales",
        "contact_required": True,
        "features": [
            "Custom feature development",
            "Dedicated IT support team",
            "Custom integrations",
            "Service level agreements",
            "Priority feature requests",
            "Custom pricing and terms",
            "Growth Acceleration Engine (Annual Only)"
        ]
    }
}

# Helper Functions
async def get_or_create_stripe_customer(email: str, name: str = None):
    """Get or create Stripe customer"""
    try:
        # Check if customer already exists in our database
        existing_customer = await db.stripe_customers.find_one({"email": email})
        if existing_customer:
            return existing_customer["stripe_customer_id"]
        
        # Create new Stripe customer
        customer_data = {"email": email}
        if name:
            customer_data["name"] = name
            
        stripe_customer = stripe.Customer.create(**customer_data)
        
        # Store in our database
        await db.stripe_customers.insert_one({
            "email": email,
            "stripe_customer_id": stripe_customer.id,
            "created_at": datetime.utcnow()
        })
        
        return stripe_customer.id
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer creation failed: {str(e)}")

async def apply_discount(amount: int, discount_code: str) -> tuple:
    """Apply discount code and return new amount and discount info"""
    if not discount_code:
        return amount, None
    
    # Get discount from database
    discount = await db.discounts.find_one({
        "code": discount_code.upper(),
        "is_active": True,
        "valid_until": {"$gte": datetime.utcnow()}
    })
    
    if not discount:
        raise HTTPException(status_code=400, detail="Invalid or expired discount code")
    
    if discount["current_uses"] >= discount["max_uses"]:
        raise HTTPException(status_code=400, detail="Discount code usage limit exceeded")
    
    # Calculate discounted amount
    discount_amount = int(amount * (discount["discount_percentage"] / 100))
    final_amount = amount - discount_amount
    
    return final_amount, discount

# Payment Endpoints
@router.post("/create-payment-intent")
async def create_payment_intent(payment_request: PaymentRequest):
    """Create Stripe payment intent"""
    try:
        plan = SUBSCRIPTION_PLANS.get(payment_request.plan_type)
        if not plan:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Get amount based on billing cycle
        if payment_request.billing_cycle == "monthly":
            amount = plan["monthly_price"]
        elif payment_request.billing_cycle == "annual":
            amount = plan["annual_price"]
        else:
            raise HTTPException(status_code=400, detail="Invalid billing cycle")
        
        # Apply discount if provided
        final_amount, discount_info = await apply_discount(amount, payment_request.discount_code)
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=final_amount,
            currency='usd',
            metadata={
                'plan_type': payment_request.plan_type,
                'billing_cycle': payment_request.billing_cycle,
                'original_amount': amount,
                'discount_code': payment_request.discount_code or '',
                'discount_applied': str(amount - final_amount) if discount_info else '0'
            }
        )
        
        return {
            "status": "success",
            "client_secret": intent.client_secret,
            "amount": final_amount,
            "original_amount": amount,
            "discount_applied": amount - final_amount if discount_info else 0,
            "plan_details": plan
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment intent creation failed: {str(e)}")

@router.post("/confirm-payment")
async def confirm_payment(payment_data: dict):
    """Confirm payment and activate subscription"""
    try:
        payment_intent_id = payment_data.get("payment_intent_id")
        user_email = payment_data.get("user_email")
        
        if not payment_intent_id or not user_email:
            raise HTTPException(status_code=400, detail="Missing required payment data")
        
        # Retrieve payment intent from Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status != "succeeded":
            raise HTTPException(status_code=400, detail="Payment not successful")
        
        # Extract metadata
        metadata = intent.metadata
        plan_type = metadata.get("plan_type")
        billing_cycle = metadata.get("billing_cycle")
        discount_code = metadata.get("discount_code")
        
        # Update user subscription in database
        subscription_data = {
            "plan_type": plan_type,
            "billing_cycle": billing_cycle,
            "subscription_tier": "annual" if billing_cycle == "annual" else "monthly",
            "payment_intent_id": payment_intent_id,
            "amount_paid": intent.amount,
            "subscription_start": datetime.utcnow(),
            "subscription_end": datetime.utcnow() + timedelta(
                days=365 if billing_cycle == "annual" else 30
            ),
            "is_active": True,
            "updated_at": datetime.utcnow()
        }
        
        # Update user record
        result = await db.users.update_one(
            {"email": user_email},
            {"$set": subscription_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update discount usage if applied
        if discount_code:
            await db.discounts.update_one(
                {"code": discount_code.upper()},
                {"$inc": {"current_uses": 1}}
            )
        
        # Record payment in payments collection
        payment_record = {
            "id": secrets.token_urlsafe(16),
            "user_email": user_email,
            "payment_intent_id": payment_intent_id,
            "plan_type": plan_type,
            "billing_cycle": billing_cycle,
            "amount": intent.amount,
            "currency": intent.currency,
            "discount_code": discount_code,
            "payment_date": datetime.utcnow(),
            "status": "completed"
        }
        
        await db.payments.insert_one(payment_record)
        
        return {
            "status": "success",
            "message": "Payment confirmed and subscription activated",
            "subscription": subscription_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment confirmation failed: {str(e)}")

@router.get("/subscription-plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    return {
        "status": "success",
        "plans": SUBSCRIPTION_PLANS
    }

@router.get("/user-subscription/{user_email}")
async def get_user_subscription(user_email: str):
    """Get user's current subscription"""
    try:
        user = await db.users.find_one(
            {"email": user_email},
            {
                "plan_type": 1,
                "billing_cycle": 1,
                "subscription_tier": 1,
                "subscription_start": 1,
                "subscription_end": 1,
                "is_active": 1
            }
        )
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "status": "success",
            "subscription": {
                "plan_type": user.get("plan_type"),
                "billing_cycle": user.get("billing_cycle"),
                "subscription_tier": user.get("subscription_tier"),
                "subscription_start": user.get("subscription_start"),
                "subscription_end": user.get("subscription_end"),
                "is_active": user.get("is_active", False),
                "has_annual_access": user.get("subscription_tier") == "annual"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription fetch failed: {str(e)}")

@router.post("/validate-discount")
async def validate_discount_code(discount_data: dict):
    """Validate discount code"""
    try:
        code = discount_data.get("code", "").upper()
        
        if not code:
            raise HTTPException(status_code=400, detail="Discount code required")
        
        discount = await db.discounts.find_one({
            "code": code,
            "is_active": True,
            "valid_until": {"$gte": datetime.utcnow()}
        })
        
        if not discount:
            return {"status": "error", "message": "Invalid or expired discount code"}
        
        if discount["current_uses"] >= discount["max_uses"]:
            return {"status": "error", "message": "Discount code usage limit exceeded"}
        
        return {
            "status": "success",
            "discount": {
                "code": discount["code"],
                "discount_percentage": discount["discount_percentage"],
                "remaining_uses": discount["max_uses"] - discount["current_uses"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discount validation failed: {str(e)}")