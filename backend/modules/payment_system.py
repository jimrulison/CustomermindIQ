"""
Customer Mind IQ - Payment Processing System
Stripe integration for SaaS subscription management
"""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
import os
import uuid
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.customer_mind_iq

router = APIRouter()

# Subscription Plans Configuration (Server-side defined for security)
SUBSCRIPTION_PLANS = {
    "free": {
        "name": "Free Tier",
        "price": 0.0,
        "currency": "usd",
        "billing_cycle": "monthly",
        "features": [
            "Basic customer intelligence",
            "Up to 1,000 customer profiles",
            "5 AI insights per month",
            "Email support",
            "Basic dashboard"
        ],
        "limits": {
            "customer_profiles": 1000,
            "ai_insights": 5,
            "api_calls": 1000,
            "data_storage": 1,  # GB
            "support_channels": ["email"],
            "modules": ["basic_intelligence"]
        }
    },
    "professional": {
        "name": "Professional Tier",
        "price": 99.0,
        "currency": "usd",
        "billing_cycle": "monthly",
        "features": [
            "Full customer intelligence suite",
            "Up to 50,000 customer profiles",
            "Unlimited AI insights",
            "Marketing automation",
            "Revenue analytics",
            "Website intelligence",
            "Priority support",
            "Advanced dashboard",
            "API access"
        ],
        "limits": {
            "customer_profiles": 50000,
            "ai_insights": -1,  # Unlimited
            "api_calls": 10000,
            "data_storage": 50,  # GB
            "support_channels": ["email", "chat"],
            "modules": ["all"]
        }
    },
    "enterprise": {
        "name": "Enterprise Tier",
        "price": 299.0,
        "currency": "usd",
        "billing_cycle": "monthly",
        "features": [
            "Everything in Professional",
            "Unlimited customer profiles",
            "White-label options",
            "Custom integrations",
            "Dedicated account manager",
            "Phone support",
            "Custom onboarding",
            "SLA guarantees",
            "Advanced security",
            "Custom reporting"
        ],
        "limits": {
            "customer_profiles": -1,  # Unlimited
            "ai_insights": -1,  # Unlimited
            "api_calls": 100000,
            "data_storage": 500,  # GB
            "support_channels": ["email", "chat", "phone"],
            "modules": ["all", "white_label", "custom"]
        }
    }
}

# Pydantic Models
class SubscriptionRequest(BaseModel):
    plan_id: str = Field(..., description="Subscription plan ID (free, professional, enterprise)")
    origin_url: str = Field(..., description="Frontend origin URL for redirect URLs")
    metadata: Optional[Dict[str, str]] = Field(default_factory=dict, description="Additional metadata")

class PaymentTransaction(BaseModel):
    transaction_id: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    email: Optional[str] = None
    plan_id: str
    amount: float
    currency: str
    payment_status: str = "pending"
    checkout_status: str = "initiated"
    metadata: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None

class SubscriptionStatus(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    current_plan: str = "free"
    subscription_id: Optional[str] = None
    status: str = "active"
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    auto_renewal: bool = True
    usage_stats: Dict[str, int] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WebhookEvent(BaseModel):
    event_type: str
    event_id: str
    session_id: Optional[str] = None
    payment_status: str
    metadata: Dict[str, str] = Field(default_factory=dict)
    processed_at: datetime = Field(default_factory=datetime.utcnow)

# Initialize Stripe Checkout
def get_stripe_checkout(request: Request) -> StripeCheckout:
    """Initialize Stripe checkout with dynamic webhook URL"""
    api_key = os.getenv("STRIPE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Stripe API key not configured")
    
    # Use request base URL to construct webhook URL
    host_url = str(request.base_url).rstrip('/')
    webhook_url = f"{host_url}/api/webhook/stripe"
    
    return StripeCheckout(api_key=api_key, webhook_url=webhook_url)

# Payment Processing Endpoints

@router.post("/subscription/checkout")
async def create_subscription_checkout(
    request: SubscriptionRequest,
    http_request: Request,
    background_tasks: BackgroundTasks
):
    """Create a Stripe checkout session for subscription"""
    
    # Validate plan exists
    if request.plan_id not in SUBSCRIPTION_PLANS:
        raise HTTPException(status_code=400, detail="Invalid subscription plan")
    
    plan = SUBSCRIPTION_PLANS[request.plan_id]
    
    # Free tier doesn't require payment
    if request.plan_id == "free":
        # Create free subscription record
        subscription = SubscriptionStatus(
            current_plan="free",
            status="active"
        )
        
        result = await db.subscriptions.insert_one(subscription.dict())
        
        return {
            "success": True,
            "message": "Free subscription activated",
            "plan": plan,
            "subscription_id": str(result.inserted_id)
        }
    
    # For paid plans, create Stripe checkout
    try:
        stripe_checkout = get_stripe_checkout(http_request)
        
        # Generate transaction ID
        transaction_id = str(uuid.uuid4())
        
        # Construct success and cancel URLs
        origin_url = request.origin_url.rstrip('/')
        success_url = f"{origin_url}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{origin_url}/subscription/cancel"
        
        # Prepare metadata
        metadata = {
            "plan_id": request.plan_id,
            "transaction_id": transaction_id,
            "source": "subscription_checkout",
            **request.metadata
        }
        
        # Create checkout session
        checkout_request = CheckoutSessionRequest(
            amount=plan["price"],
            currency=plan["currency"],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata
        )
        
        session: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
        
        # Create payment transaction record
        transaction = PaymentTransaction(
            transaction_id=transaction_id,
            session_id=session.session_id,
            plan_id=request.plan_id,
            amount=plan["price"],
            currency=plan["currency"],
            payment_status="pending",
            checkout_status="initiated",
            metadata=metadata,
            success_url=success_url,
            cancel_url=cancel_url
        )
        
        # Store in database
        await db.payment_transactions.insert_one(transaction.dict())
        
        return {
            "success": True,
            "checkout_url": session.url,
            "session_id": session.session_id,
            "transaction_id": transaction_id,
            "plan": plan
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")

@router.get("/checkout/status/{session_id}")
async def get_checkout_status(session_id: str, http_request: Request):
    """Check the status of a checkout session and update database"""
    
    try:
        stripe_checkout = get_stripe_checkout(http_request)
        
        # Get status from Stripe
        checkout_status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
        
        # Find transaction in database
        transaction = await db.payment_transactions.find_one({"session_id": session_id})
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Check if already processed to prevent double processing
        if transaction.get("payment_status") == "paid" and checkout_status.payment_status == "paid":
            return {
                "success": True,
                "status": checkout_status.status,
                "payment_status": checkout_status.payment_status,
                "amount_total": checkout_status.amount_total,
                "currency": checkout_status.currency,
                "message": "Payment already processed"
            }
        
        # Update transaction status
        update_data = {
            "payment_status": checkout_status.payment_status,
            "checkout_status": checkout_status.status,
            "updated_at": datetime.utcnow()
        }
        
        await db.payment_transactions.update_one(
            {"session_id": session_id},
            {"$set": update_data}
        )
        
        # If payment successful, create/update subscription
        if checkout_status.payment_status == "paid" and transaction.get("payment_status") != "paid":
            await activate_subscription(transaction, checkout_status)
        
        return {
            "success": True,
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "amount_total": checkout_status.amount_total,
            "currency": checkout_status.currency,
            "transaction_id": transaction.get("transaction_id"),
            "plan_id": transaction.get("plan_id")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check checkout status: {str(e)}")

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle Stripe webhook events"""
    
    try:
        stripe_checkout = get_stripe_checkout(request)
        
        # Get request body and signature
        body = await request.body()
        signature = request.headers.get("Stripe-Signature")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing Stripe signature")
        
        # Handle webhook
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        # Log webhook event
        webhook_event = WebhookEvent(
            event_type=webhook_response.event_type,
            event_id=webhook_response.event_id,
            session_id=webhook_response.session_id,
            payment_status=webhook_response.payment_status,
            metadata=webhook_response.metadata
        )
        
        await db.webhook_events.insert_one(webhook_event.dict())
        
        # Process webhook based on event type
        if webhook_response.event_type == "checkout.session.completed":
            background_tasks.add_task(process_successful_payment, webhook_response)
        elif webhook_response.event_type == "invoice.payment_failed":
            background_tasks.add_task(process_failed_payment, webhook_response)
        
        return {"success": True, "event_processed": webhook_response.event_type}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

# Helper Functions

async def activate_subscription(transaction: dict, checkout_status: CheckoutStatusResponse):
    """Activate subscription after successful payment"""
    
    plan_id = transaction.get("plan_id")
    if not plan_id:
        return
    
    # Calculate subscription end date (monthly billing)
    end_date = datetime.utcnow() + timedelta(days=30)
    
    # Create or update subscription
    subscription_data = {
        "current_plan": plan_id,
        "subscription_id": checkout_status.metadata.get("transaction_id"),
        "status": "active",
        "start_date": datetime.utcnow(),
        "end_date": end_date,
        "auto_renewal": True,
        "usage_stats": {},
        "updated_at": datetime.utcnow()
    }
    
    # If user_id or email available, link subscription
    if transaction.get("email"):
        subscription_data["email"] = transaction.get("email")
    if transaction.get("user_id"):
        subscription_data["user_id"] = transaction.get("user_id")
    
    # Upsert subscription
    filter_query = {}
    if transaction.get("email"):
        filter_query["email"] = transaction.get("email")
    elif transaction.get("user_id"):
        filter_query["user_id"] = transaction.get("user_id")
    else:
        filter_query["subscription_id"] = checkout_status.metadata.get("transaction_id")
    
    await db.subscriptions.update_one(
        filter_query,
        {"$set": subscription_data},
        upsert=True
    )

async def process_successful_payment(webhook_response):
    """Background task to process successful payment"""
    
    if not webhook_response.session_id:
        return
    
    # Find and update transaction
    transaction = await db.payment_transactions.find_one({"session_id": webhook_response.session_id})
    
    if transaction and transaction.get("payment_status") != "paid":
        # Update payment status
        await db.payment_transactions.update_one(
            {"session_id": webhook_response.session_id},
            {"$set": {
                "payment_status": "paid",
                "updated_at": datetime.utcnow()
            }}
        )
        
        # Activate subscription
        checkout_status = CheckoutStatusResponse(
            status="complete",
            payment_status="paid",
            amount_total=int(transaction.get("amount", 0) * 100),  # Convert to cents
            currency=transaction.get("currency", "usd"),
            metadata=webhook_response.metadata
        )
        
        await activate_subscription(transaction, checkout_status)

async def process_failed_payment(webhook_response):
    """Background task to process failed payment"""
    
    if webhook_response.session_id:
        # Update transaction status
        await db.payment_transactions.update_one(
            {"session_id": webhook_response.session_id},
            {"$set": {
                "payment_status": "failed",
                "updated_at": datetime.utcnow()
            }}
        )

# Subscription Management Endpoints

@router.get("/subscription/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    
    return {
        "success": True,
        "plans": SUBSCRIPTION_PLANS
    }

@router.get("/subscription/current")
async def get_current_subscription(email: Optional[str] = None, user_id: Optional[str] = None):
    """Get current subscription status"""
    
    if not email and not user_id:
        raise HTTPException(status_code=400, detail="Email or user_id required")
    
    # Find subscription
    filter_query = {}
    if email:
        filter_query["email"] = email
    elif user_id:
        filter_query["user_id"] = user_id
    
    subscription = await db.subscriptions.find_one(filter_query)
    
    if not subscription:
        # Return default free subscription
        return {
            "success": True,
            "subscription": {
                "current_plan": "free",
                "status": "active",
                "features": SUBSCRIPTION_PLANS["free"]["features"],
                "limits": SUBSCRIPTION_PLANS["free"]["limits"]
            }
        }
    
    # Add plan details
    plan_id = subscription.get("current_plan", "free")
    plan_details = SUBSCRIPTION_PLANS.get(plan_id, SUBSCRIPTION_PLANS["free"])
    
    return {
        "success": True,
        "subscription": {
            **subscription,
            "features": plan_details["features"],
            "limits": plan_details["limits"],
            "_id": str(subscription.get("_id"))
        }
    }

@router.get("/transactions/history")
async def get_transaction_history(email: Optional[str] = None, user_id: Optional[str] = None, limit: int = 10):
    """Get payment transaction history"""
    
    filter_query = {}
    if email:
        filter_query["email"] = email
    elif user_id:
        filter_query["user_id"] = user_id
    
    transactions = await db.payment_transactions.find(filter_query).sort("created_at", -1).limit(limit).to_list(length=limit)
    
    # Convert ObjectId to string
    for transaction in transactions:
        transaction["_id"] = str(transaction.get("_id"))
    
    return {
        "success": True,
        "transactions": transactions,
        "total": len(transactions)
    }

@router.post("/subscription/cancel")
async def cancel_subscription(email: Optional[str] = None, user_id: Optional[str] = None):
    """Cancel current subscription"""
    
    if not email and not user_id:
        raise HTTPException(status_code=400, detail="Email or user_id required")
    
    filter_query = {}
    if email:
        filter_query["email"] = email
    elif user_id:
        filter_query["user_id"] = user_id
    
    # Update subscription to cancelled
    result = await db.subscriptions.update_one(
        filter_query,
        {"$set": {
            "status": "cancelled",
            "auto_renewal": False,
            "updated_at": datetime.utcnow()
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return {
        "success": True,
        "message": "Subscription cancelled successfully"
    }

# Analytics and Admin Endpoints

@router.get("/admin/dashboard")
async def get_admin_dashboard():
    """Get payment and subscription analytics dashboard"""
    
    try:
        # Payment statistics
        total_transactions = await db.payment_transactions.count_documents({})
        successful_payments = await db.payment_transactions.count_documents({"payment_status": "paid"})
        total_revenue = await db.payment_transactions.aggregate([
            {"$match": {"payment_status": "paid"}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]).to_list(length=1)
        
        # Subscription statistics
        active_subscriptions = await db.subscriptions.count_documents({"status": "active"})
        subscription_breakdown = await db.subscriptions.aggregate([
            {"$group": {"_id": "$current_plan", "count": {"$sum": 1}}}
        ]).to_list(length=10)
        
        # Recent transactions
        recent_transactions = await db.payment_transactions.find({}).sort("created_at", -1).limit(5).to_list(length=5)
        
        return {
            "success": True,
            "analytics": {
                "payments": {
                    "total_transactions": total_transactions,
                    "successful_payments": successful_payments,
                    "success_rate": successful_payments / total_transactions * 100 if total_transactions > 0 else 0,
                    "total_revenue": total_revenue[0]["total"] if total_revenue else 0
                },
                "subscriptions": {
                    "active_subscriptions": active_subscriptions,
                    "plan_breakdown": subscription_breakdown
                },
                "recent_transactions": recent_transactions
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard: {str(e)}")

# Export router
__all__ = ["router"]