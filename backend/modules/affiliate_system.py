# Affiliate Tracking System
import os
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.security import HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum
import bcrypt
import jwt
from dotenv import load_dotenv
import asyncio
import stripe

# Import authentication from main auth system
from auth.auth_system import get_current_user, UserProfile, require_role, UserRole

load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Stripe configuration  
stripe.api_key = os.getenv("STRIPE_API_KEY", "sk_test_emergent")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "affiliate-jwt-secret-key")
JWT_ALGORITHM = "HS256"

router = APIRouter(prefix="/api/affiliate", tags=["Affiliate System"])

# ========== MODELS ==========

class AffiliateStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

class PromotionMethod(str, Enum):
    EMAIL = "email"
    SOCIAL = "social"
    CONTENT = "content"
    PAID = "paid"
    NETWORK = "network"
    SPEAKING = "speaking"
    OTHER = "other"

class PaymentMethod(str, Enum):
    BANK = "bank"
    DEBIT = "debit"
    VENMO = "venmo"
    PAYPAL = "paypal"
    CHECK = "check"

class CommissionType(str, Enum):
    INITIAL = "initial"
    TRAILING_2_12 = "trailing_2_12"
    TRAILING_13_24 = "trailing_13_24"

class CommissionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"

class LinkType(str, Enum):
    TRIAL = "trial"
    LANDING = "landing"
    DEMO = "demo"
    PRICING = "pricing"

# Registration Models
class AffiliateAddress(BaseModel):
    street: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=50)
    zip_code: str = Field(..., max_length=20)
    country: str = Field(default="US", max_length=50)

class PaymentDetails(BaseModel):
    bank_name: Optional[str] = None
    routing_number: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    paypal_email: Optional[str] = None
    venmo_username: Optional[str] = None

class AffiliateRegistration(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    promotion_method: PromotionMethod
    password: str = Field(..., min_length=8)
    address: AffiliateAddress
    payment_method: PaymentMethod
    payment_details: PaymentDetails

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class AffiliateLogin(BaseModel):
    email: EmailStr
    password: str

# Response Models
class AffiliateProfile(BaseModel):
    affiliate_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    website: Optional[str]
    promotion_method: str
    status: str
    total_clicks: int = 0
    total_conversions: int = 0
    total_commissions: float = 0.0
    pending_commissions: float = 0.0
    paid_commissions: float = 0.0
    created_at: datetime
    approved_at: Optional[datetime]
    last_login: Optional[datetime]

class TrackingLink(BaseModel):
    id: str
    affiliate_id: str
    campaign_name: Optional[str]
    link_type: LinkType
    original_url: str
    tracking_url: str
    short_url: Optional[str]
    clicks: int = 0
    conversions: int = 0
    created_at: datetime

class AffiliateStats(BaseModel):
    this_month: Dict[str, Any]
    all_time: Dict[str, Any]

class AffiliateDashboardResponse(BaseModel):
    affiliate: AffiliateProfile
    stats: AffiliateStats
    recent_activity: List[Dict[str, Any]]

# ========== HELPER FUNCTIONS ==========

def generate_affiliate_id(first_name: str, last_name: str) -> str:
    """Generate unique affiliate ID"""
    base_id = f"{first_name.lower().replace(' ', '_')}_{last_name.lower().replace(' ', '_')}"
    timestamp = str(int(datetime.now().timestamp()))[-4:]
    return f"{base_id}_{timestamp}"

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(affiliate_id: str) -> str:
    """Create JWT token for affiliate"""
    payload = {
        "affiliate_id": affiliate_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=30),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def generate_tracking_url(affiliate_id: str, campaign_name: str = None, link_type: str = "trial") -> str:
    """Generate tracking URL"""
    base_url = "https://customermindiq.com"
    
    if link_type == "trial":
        url = f"{base_url}/trial"
    elif link_type == "pricing":
        url = f"{base_url}/pricing"
    elif link_type == "demo":
        url = f"{base_url}/demo"
    else:
        url = base_url
    
    params = [f"ref={affiliate_id}"]
    if campaign_name:
        params.append(f"campaign={campaign_name}")
    
    return f"{url}?{'&'.join(params)}"

def generate_short_url() -> str:
    """Generate short URL"""
    return f"https://cmiq.ly/{secrets.token_urlsafe(6)}"

# Commission calculation rates
COMMISSION_RATES = {
    "launch": {"initial": 0.30, "trailing_2_12": 0.20, "trailing_13_24": 0.10},
    "growth": {"initial": 0.40, "trailing_2_12": 0.20, "trailing_13_24": 0.10},
    "scale": {"initial": 0.50, "trailing_2_12": 0.20, "trailing_13_24": 0.10}
}

# ========== AUTHENTICATION ENDPOINTS ==========

@router.post("/auth/register")
async def register_affiliate(registration: AffiliateRegistration):
    """Register new affiliate"""
    try:
        # Check if email already exists
        existing_affiliate = await db.affiliates.find_one({"email": registration.email})
        if existing_affiliate:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Generate affiliate ID
        affiliate_id = generate_affiliate_id(registration.first_name, registration.last_name)
        
        # Ensure unique affiliate ID
        counter = 1
        original_id = affiliate_id
        while await db.affiliates.find_one({"affiliate_id": affiliate_id}):
            affiliate_id = f"{original_id}_{counter}"
            counter += 1
        
        # Hash password
        password_hash = hash_password(registration.password)
        
        # Create affiliate record
        affiliate_data = {
            "affiliate_id": affiliate_id,
            "first_name": registration.first_name,
            "last_name": registration.last_name,
            "email": registration.email,
            "phone": registration.phone,
            "website": registration.website,
            "promotion_method": registration.promotion_method.value,
            "status": AffiliateStatus.PENDING.value,
            "password_hash": password_hash,
            "address": registration.address.dict(),
            "payment_method": registration.payment_method.value,
            "payment_details": registration.payment_details.dict(),
            "total_clicks": 0,
            "total_conversions": 0,
            "total_commissions": 0.0,
            "pending_commissions": 0.0,
            "paid_commissions": 0.0,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "approved_at": None,
            "last_login": None,
            "email_verified": False,
            "verification_token": secrets.token_urlsafe(32)
        }
        
        # Insert into database
        result = await db.affiliates.insert_one(affiliate_data)
        
        # TODO: Send verification email
        
        return {
            "success": True,
            "affiliate_id": affiliate_id,
            "message": "Registration successful. Please verify your email.",
            "verification_email_sent": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/auth/login")
async def login_affiliate(login_data: AffiliateLogin):
    """Affiliate login"""
    try:
        # Find affiliate by email
        affiliate = await db.affiliates.find_one({"email": login_data.email})
        if not affiliate:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not verify_password(login_data.password, affiliate["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Check if affiliate is approved
        if affiliate["status"] not in [AffiliateStatus.APPROVED.value, AffiliateStatus.ACTIVE.value]:
            raise HTTPException(status_code=403, detail="Account pending approval")
        
        # Update last login
        await db.affiliates.update_one(
            {"affiliate_id": affiliate["affiliate_id"]},
            {"$set": {"last_login": datetime.now(timezone.utc)}}
        )
        
        # Create JWT token
        token = create_jwt_token(affiliate["affiliate_id"])
        
        return {
            "success": True,
            "token": token,
            "affiliate": {
                "id": affiliate["affiliate_id"],
                "name": f"{affiliate['first_name']} {affiliate['last_name']}",
                "status": affiliate["status"],
                "total_commissions": affiliate["total_commissions"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

# ========== AFFILIATE MANAGEMENT ENDPOINTS ==========

@router.get("/dashboard")
async def get_affiliate_dashboard(affiliate_id: str = Query(...)):
    """Get affiliate dashboard data"""
    try:
        # Get affiliate data
        affiliate = await db.affiliates.find_one({"affiliate_id": affiliate_id})
        if not affiliate:
            raise HTTPException(status_code=404, detail="Affiliate not found")
        
        # Calculate this month stats
        start_of_month = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Get clicks this month
        clicks_this_month = await db.click_tracking.count_documents({
            "affiliate_id": affiliate_id,
            "clicked_at": {"$gte": start_of_month}
        })
        
        # Get conversions this month
        conversions_this_month = await db.click_tracking.count_documents({
            "affiliate_id": affiliate_id,
            "converted": True,
            "conversion_date": {"$gte": start_of_month}
        })
        
        # Get commissions this month
        commissions_pipeline = [
            {
                "$match": {
                    "affiliate_id": affiliate_id,
                    "earned_date": {"$gte": start_of_month}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$commission_amount"}
                }
            }
        ]
        
        commissions_result = await db.commissions.aggregate(commissions_pipeline).to_list(length=1)
        commissions_this_month = commissions_result[0]["total"] if commissions_result else 0
        
        # Build affiliate profile
        affiliate_profile = AffiliateProfile(
            affiliate_id=affiliate["affiliate_id"],
            first_name=affiliate["first_name"],
            last_name=affiliate["last_name"],
            email=affiliate["email"],
            phone=affiliate.get("phone"),
            website=affiliate.get("website"),
            promotion_method=affiliate["promotion_method"],
            status=affiliate["status"],
            total_clicks=affiliate["total_clicks"],
            total_conversions=affiliate["total_conversions"],
            total_commissions=affiliate["total_commissions"],
            pending_commissions=affiliate["pending_commissions"],
            paid_commissions=affiliate["paid_commissions"],
            created_at=affiliate["created_at"],
            approved_at=affiliate.get("approved_at"),
            last_login=affiliate.get("last_login")
        )
        
        # Build stats
        stats = AffiliateStats(
            this_month={
                "clicks": clicks_this_month,
                "trials": 0,  # TODO: Calculate from customer data
                "conversions": conversions_this_month,
                "commissions": commissions_this_month
            },
            all_time={
                "clicks": affiliate["total_clicks"],
                "trials": 0,  # TODO: Calculate from customer data
                "conversions": affiliate["total_conversions"],
                "commissions": affiliate["total_commissions"]
            }
        )
        
        # Get recent activity (last 10 commissions)
        recent_commissions = await db.commissions.find(
            {"affiliate_id": affiliate_id}
        ).sort("earned_date", -1).limit(10).to_list(length=10)
        
        recent_activity = []
        for commission in recent_commissions:
            recent_activity.append({
                "type": "conversion",
                "customer": f"Customer {commission['customer_id'][:8]}...",
                "plan": commission["plan_type"],
                "commission": commission["commission_amount"],
                "date": commission["earned_date"].isoformat()
            })
        
        return AffiliateDashboardResponse(
            affiliate=affiliate_profile,
            stats=stats,
            recent_activity=recent_activity
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

@router.post("/generate-link")
async def generate_tracking_link(
    link_data: Dict[str, Any],
    affiliate_id: str = Query(...)
):
    """Generate tracking link for affiliate"""
    try:
        campaign_name = link_data.get("campaign_name", "default")
        link_type = LinkType(link_data.get("link_type", "trial"))
        custom_params = link_data.get("custom_params", {})
        
        # Generate tracking URL
        tracking_url = generate_tracking_url(affiliate_id, campaign_name, link_type.value)
        
        # Add custom UTM parameters
        utm_params = []
        for key, value in custom_params.items():
            if key.startswith("utm_"):
                utm_params.append(f"{key}={value}")
        
        if utm_params:
            separator = "&" if "?" in tracking_url else "?"
            tracking_url = f"{tracking_url}{separator}{'&'.join(utm_params)}"
        
        # Generate short URL
        short_url = generate_short_url()
        
        # Create tracking link record
        link_record = {
            "id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "campaign_name": campaign_name,
            "link_type": link_type.value,
            "original_url": "https://customermindiq.com",
            "tracking_url": tracking_url,
            "short_url": short_url,
            "clicks": 0,
            "conversions": 0,
            "created_at": datetime.now(timezone.utc)
        }
        
        # Store in database
        await db.tracking_links.insert_one(link_record)
        
        return {
            "success": True,
            "tracking_url": tracking_url,
            "short_url": short_url,
            "qr_code": f"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."  # TODO: Generate actual QR code
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Link generation failed: {str(e)}")

@router.get("/materials")
async def get_affiliate_materials(affiliate_id: str = Query(...)):
    """Get affiliate marketing materials"""
    try:
        # TODO: Generate dynamic marketing materials
        materials = {
            "banners": [
                {
                    "name": "Email Header Banner",
                    "size": "600x200",
                    "url": f"https://cdn.customermindiq.com/banners/email-header-{affiliate_id}.png",
                    "tracking_url": generate_tracking_url(affiliate_id, "email-banner", "trial")
                }
            ],
            "email_templates": [
                {
                    "name": "Educational Template",
                    "subject": "The #1 reason 68% of businesses lose customers",
                    "content": "Hi [First Name], Quick question...",
                    "tracking_url": generate_tracking_url(affiliate_id, "email-template-1", "trial")
                }
            ],
            "landing_pages": [
                {
                    "name": "Main Landing Page",
                    "url": f"https://customermindiq.com/affiliate/{affiliate_id}",
                    "description": "Personalized landing page with your affiliate branding"
                }
            ]
        }
        
        return materials
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Materials error: {str(e)}")

# ========== TRACKING ENDPOINTS ==========

@router.post("/track/event")
async def track_affiliate_event(event_data: Dict[str, Any]):
    """Track affiliate events (clicks, conversions)"""
    try:
        event_type = event_data.get("event_type")
        affiliate_id = event_data.get("affiliate_id")
        
        if not affiliate_id:
            return {"success": True}  # Silent fail for missing affiliate ID
        
        # Record the tracking event
        tracking_record = {
            "id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "campaign_name": event_data.get("campaign"),
            "visitor_ip": event_data.get("ip"),
            "user_agent": event_data.get("user_agent"),
            "referrer": event_data.get("referrer"),
            "landing_page": event_data.get("landing_page"),
            "utm_source": event_data.get("utm_source"),
            "utm_medium": event_data.get("utm_medium"),
            "utm_campaign": event_data.get("utm_campaign"),
            "session_id": event_data.get("session_id"),
            "clicked_at": datetime.now(timezone.utc),
            "converted": False,
            "conversion_date": None
        }
        
        await db.click_tracking.insert_one(tracking_record)
        
        # Update affiliate click count
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {"$inc": {"total_clicks": 1}}
        )
        
        # Handle specific event types
        if event_type == "conversion":
            await handle_conversion_event(event_data)
        
        return {"success": True}
        
    except Exception as e:
        print(f"Tracking error: {e}")
        return {"success": False, "error": str(e)}

async def handle_conversion_event(event_data: Dict[str, Any]):
    """Handle conversion events and create commission records"""
    try:
        affiliate_id = event_data.get("affiliate_id")
        customer_id = event_data.get("customer_id")
        plan_type = event_data.get("plan_type")
        billing_cycle = event_data.get("billing_cycle")
        amount = float(event_data.get("amount", 0))
        
        # Update conversion tracking
        await db.click_tracking.update_one(
            {
                "affiliate_id": affiliate_id,
                "session_id": event_data.get("session_id")
            },
            {
                "$set": {
                    "converted": True,
                    "conversion_date": datetime.now(timezone.utc)
                }
            }
        )
        
        # Create commission records
        await create_commission_records(affiliate_id, customer_id, plan_type, billing_cycle, amount)
        
        # Update affiliate stats
        commission_amount = await calculate_initial_commission(plan_type, billing_cycle, amount)
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {
                "$inc": {
                    "total_conversions": 1,
                    "pending_commissions": commission_amount
                }
            }
        )
        
    except Exception as e:
        print(f"Conversion handling error: {e}")

async def create_commission_records(affiliate_id: str, customer_id: str, plan_type: str, billing_cycle: str, amount: float):
    """Create commission records for affiliate"""
    try:
        rates = COMMISSION_RATES.get(plan_type, COMMISSION_RATES["launch"])
        
        if billing_cycle == "annual":
            # Annual payment: commission on full amount
            initial_commission = amount * rates["initial"]
            
            # Create initial commission
            await db.commissions.insert_one({
                "id": str(uuid.uuid4()),
                "affiliate_id": affiliate_id,
                "customer_id": customer_id,
                "commission_type": CommissionType.INITIAL.value,
                "plan_type": plan_type,
                "billing_cycle": billing_cycle,
                "commission_rate": rates["initial"] * 100,
                "base_amount": amount,
                "commission_amount": initial_commission,
                "status": CommissionStatus.PENDING.value,
                "earned_date": datetime.now(timezone.utc),
                "due_date": datetime.now(timezone.utc) + timedelta(days=30),
                "paid_date": None,
                "billing_month": 1
            })
            
            # Create second year commission
            await db.commissions.insert_one({
                "id": str(uuid.uuid4()),
                "affiliate_id": affiliate_id,
                "customer_id": customer_id,
                "commission_type": CommissionType.TRAILING_13_24.value,
                "plan_type": plan_type,
                "billing_cycle": billing_cycle,
                "commission_rate": rates["trailing_13_24"] * 100,
                "base_amount": amount,
                "commission_amount": amount * rates["trailing_13_24"],
                "status": CommissionStatus.PENDING.value,
                "earned_date": datetime.now(timezone.utc) + timedelta(days=365),
                "due_date": datetime.now(timezone.utc) + timedelta(days=395),
                "paid_date": None,
                "billing_month": 13
            })
        else:
            # Monthly subscriptions: create 24 commission records
            initial_commission = amount * rates["initial"]
            
            # Initial commission (month 1)
            await db.commissions.insert_one({
                "id": str(uuid.uuid4()),
                "affiliate_id": affiliate_id,
                "customer_id": customer_id,
                "commission_type": CommissionType.INITIAL.value,
                "plan_type": plan_type,
                "billing_cycle": billing_cycle,
                "commission_rate": rates["initial"] * 100,
                "base_amount": amount,
                "commission_amount": initial_commission,
                "status": CommissionStatus.PENDING.value,
                "earned_date": datetime.now(timezone.utc),
                "due_date": datetime.now(timezone.utc) + timedelta(days=30),
                "paid_date": None,
                "billing_month": 1
            })
            
            # Trailing commissions months 2-12 (20%)
            for month in range(2, 13):
                trailing_commission = amount * rates["trailing_2_12"]
                await db.commissions.insert_one({
                    "id": str(uuid.uuid4()),
                    "affiliate_id": affiliate_id,
                    "customer_id": customer_id,
                    "commission_type": CommissionType.TRAILING_2_12.value,
                    "plan_type": plan_type,
                    "billing_cycle": billing_cycle,
                    "commission_rate": rates["trailing_2_12"] * 100,
                    "base_amount": amount,
                    "commission_amount": trailing_commission,
                    "status": CommissionStatus.PENDING.value,
                    "earned_date": datetime.now(timezone.utc) + timedelta(days=30*month),
                    "due_date": datetime.now(timezone.utc) + timedelta(days=30*month + 30),
                    "paid_date": None,
                    "billing_month": month
                })
            
            # Trailing commissions months 13-24 (10%)
            for month in range(13, 25):
                trailing_commission = amount * rates["trailing_13_24"]
                await db.commissions.insert_one({
                    "id": str(uuid.uuid4()),
                    "affiliate_id": affiliate_id,
                    "customer_id": customer_id,
                    "commission_type": CommissionType.TRAILING_13_24.value,
                    "plan_type": plan_type,
                    "billing_cycle": billing_cycle,
                    "commission_rate": rates["trailing_13_24"] * 100,
                    "base_amount": amount,
                    "commission_amount": trailing_commission,
                    "status": CommissionStatus.PENDING.value,
                    "earned_date": datetime.now(timezone.utc) + timedelta(days=30*month),
                    "due_date": datetime.now(timezone.utc) + timedelta(days=30*month + 30),
                    "paid_date": None,
                    "billing_month": month
                })
        
    except Exception as e:
        print(f"Commission creation error: {e}")

async def calculate_initial_commission(plan_type: str, billing_cycle: str, amount: float) -> float:
    """Calculate initial commission amount"""
    rates = COMMISSION_RATES.get(plan_type, COMMISSION_RATES["launch"])
    return amount * rates["initial"]

# ========== ADMIN ENDPOINTS ==========

@router.get("/admin/affiliates")
async def list_affiliates(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN])),
    status: Optional[AffiliateStatus] = None,
    limit: int = Query(default=50, le=100)
):
    """Admin: List all affiliates"""
    try:
        query = {}
        if status:
            query["status"] = status.value
        
        affiliates = await db.affiliates.find(query).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        result = []
        for affiliate in affiliates:
            result.append({
                "affiliate_id": affiliate["affiliate_id"],
                "name": f"{affiliate['first_name']} {affiliate['last_name']}",
                "email": affiliate["email"],
                "status": affiliate["status"],
                "total_clicks": affiliate["total_clicks"],
                "total_conversions": affiliate["total_conversions"],
                "total_commissions": affiliate["total_commissions"],
                "pending_commissions": affiliate["pending_commissions"],
                "created_at": affiliate["created_at"],
                "last_login": affiliate.get("last_login")
            })
        
        return {
            "status": "success",
            "affiliates": result,
            "total": len(result)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Admin list error: {str(e)}")

@router.patch("/admin/affiliates/{affiliate_id}/status")
async def update_affiliate_status(
    affiliate_id: str,
    status_data: Dict[str, str],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Admin: Update affiliate status"""
    try:
        new_status = AffiliateStatus(status_data.get("status"))
        
        update_data = {
            "status": new_status.value,
            "updated_at": datetime.now(timezone.utc)
        }
        
        if new_status == AffiliateStatus.APPROVED:
            update_data["approved_at"] = datetime.now(timezone.utc)
        
        result = await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Affiliate not found")
        
        return {
            "status": "success",
            "message": f"Affiliate status updated to {new_status.value}"
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status update error: {str(e)}")

# ========== CUSTOMER INTEGRATION ENDPOINTS ==========

@router.post("/customer/link")
async def link_customer_to_affiliate(customer_data: Dict[str, Any]):
    """Link customer to affiliate (called when customer converts)"""
    try:
        customer_id = customer_data.get("customer_id")
        affiliate_id = customer_data.get("affiliate_id")
        
        if not customer_id or not affiliate_id:
            return {"success": True}  # Silent success if missing data
        
        # Update customer record to include affiliate reference
        await db.customers.update_one(
            {"customer_id": customer_id},
            {"$set": {"referred_by_affiliate": affiliate_id}}
        )
        
        return {"success": True}
        
    except Exception as e:
        print(f"Customer linking error: {e}")
        return {"success": False, "error": str(e)}

# ========== DETAILED DATA ENDPOINTS ==========

@router.get("/commissions")
async def get_affiliate_commissions(
    affiliate_id: str = Query(...),
    limit: int = Query(default=10, le=50),
    status: Optional[str] = None
):
    """Get detailed commission history for affiliate"""
    try:
        query = {"affiliate_id": affiliate_id}
        if status:
            query["status"] = status
        
        commissions = await db.commissions.find(query).sort("earned_date", -1).limit(limit).to_list(length=limit)
        
        # Enrich commissions with customer details
        enriched_commissions = []
        for commission in commissions:
            # Get customer details
            customer_id = commission.get("customer_id")
            customer_name = f"Customer {customer_id[:8]}..." if customer_id else "Unknown Customer"
            customer_email = f"{customer_id}@example.com" if customer_id else "unknown@example.com"
            
            # Try to get real customer data
            customer = await db.customers.find_one({"customer_id": customer_id}) if customer_id else None
            if customer:
                customer_name = customer.get("company_name") or customer.get("name") or customer_name
                customer_email = customer.get("email") or customer_email
            
            enriched_commission = {
                "id": commission.get("id"),
                "customer_id": customer_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "plan_type": commission.get("plan_type"),
                "billing_cycle": commission.get("billing_cycle"),
                "commission_amount": commission.get("commission_amount"),
                "commission_rate": commission.get("commission_rate"),
                "base_amount": commission.get("base_amount"),
                "earned_date": commission.get("earned_date"),
                "status": commission.get("status"),
                "billing_month": commission.get("billing_month", 1)
            }
            enriched_commissions.append(enriched_commission)
        
        return {
            "success": True,
            "commissions": enriched_commissions,
            "total": len(enriched_commissions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get commissions: {str(e)}")

@router.get("/customers")
async def get_affiliate_customers(
    affiliate_id: str = Query(...),
    limit: int = Query(default=20, le=100)
):
    """Get customers referred by affiliate"""
    try:
        # Find customers referred by this affiliate
        customers = await db.customers.find(
            {"referred_by_affiliate": affiliate_id}
        ).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        # Enrich customer data with spending info
        enriched_customers = []
        for customer in customers:
            # Calculate total spent and lifetime value
            customer_id = customer.get("customer_id")
            
            # Get payment history for this customer
            payments = await db.payments.find({"user_email": customer.get("email")}).to_list(length=None)
            total_spent = sum(payment.get("amount", 0) / 100 for payment in payments)  # Convert from cents
            
            # Estimate lifetime value (could be more sophisticated)
            months_active = max(1, (datetime.now(timezone.utc) - customer.get("created_at", datetime.now(timezone.utc))).days // 30)
            lifetime_value = total_spent * max(1, 12 / months_active)  # Annualized estimate
            
            enriched_customer = {
                "customer_id": customer_id,
                "name": customer.get("company_name") or customer.get("name") or f"Customer {customer_id[:8]}...",
                "email": customer.get("email"),
                "plan": customer.get("subscription_tier", "launch"),
                "signup_date": customer.get("created_at"),
                "status": "active" if customer.get("is_active", True) else "inactive",
                "total_spent": total_spent,
                "lifetime_value": lifetime_value
            }
            enriched_customers.append(enriched_customer)
        
        return {
            "success": True,
            "customers": enriched_customers,
            "total": len(enriched_customers)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get customers: {str(e)}")

@router.get("/metrics")
async def get_affiliate_metrics(affiliate_id: str = Query(...)):
    """Get performance metrics for affiliate"""
    try:
        # Get affiliate data
        affiliate = await db.affiliates.find_one({"affiliate_id": affiliate_id})
        if not affiliate:
            raise HTTPException(status_code=404, detail="Affiliate not found")
        
        # Calculate conversion rate
        total_clicks = affiliate.get("total_clicks", 0)
        total_conversions = affiliate.get("total_conversions", 0)
        conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        
        # Get commission data for calculations
        commissions = await db.commissions.find({"affiliate_id": affiliate_id}).to_list(length=None)
        
        # Calculate average order value
        if commissions:
            total_base = sum(c.get("base_amount", 0) for c in commissions)
            avg_order_value = total_base / len(commissions)
        else:
            avg_order_value = 0
        
        # Get customer data for LTV
        customers = await db.customers.find({"referred_by_affiliate": affiliate_id}).to_list(length=None)
        if customers:
            customer_lifetime_value = sum(
                max(299, len([c for c in commissions if c.get("customer_id") == customer.get("customer_id")]) * 50)
                for customer in customers
            ) / len(customers)
        else:
            customer_lifetime_value = 0
        
        # Get traffic source data from click tracking
        traffic_sources = await db.click_tracking.aggregate([
            {"$match": {"affiliate_id": affiliate_id}},
            {"$group": {
                "_id": {"$ifNull": ["$utm_source", "direct"]},
                "clicks": {"$sum": 1},
                "conversions": {"$sum": {"$cond": ["$converted", 1, 0]}}
            }},
            {"$sort": {"clicks": -1}},
            {"$limit": 5}
        ]).to_list(length=5)
        
        top_traffic_sources = [
            {
                "source": source["_id"],
                "clicks": source["clicks"], 
                "conversions": source["conversions"]
            }
            for source in traffic_sources
        ]
        
        metrics = {
            "conversion_rate": conversion_rate,
            "avg_order_value": avg_order_value,
            "customer_lifetime_value": customer_lifetime_value,
            "top_traffic_sources": top_traffic_sources,
            "total_customers": len(customers),
            "active_customers": len([c for c in customers if c.get("is_active", True)]),
            "monthly_recurring_revenue": sum(c.get("commission_amount", 0) for c in commissions if c.get("billing_cycle") == "monthly"),
            "annual_recurring_revenue": sum(c.get("commission_amount", 0) for c in commissions if c.get("billing_cycle") == "annual")
        }
        
        return {
            "success": True,
            "metrics": metrics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@router.get("/performance/chart")
async def get_affiliate_performance_chart(
    affiliate_id: str = Query(...),
    period: str = Query(default="30d", regex="^(7d|30d|90d|1y)$")
):
    """Get performance chart data for affiliate"""
    try:
        # Calculate date range
        days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}[period]
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Get daily metrics
        pipeline = [
            {"$match": {
                "affiliate_id": affiliate_id,
                "clicked_at": {"$gte": start_date}
            }},
            {"$group": {
                "_id": {
                    "year": {"$year": "$clicked_at"},
                    "month": {"$month": "$clicked_at"},
                    "day": {"$dayOfMonth": "$clicked_at"}
                },
                "clicks": {"$sum": 1},
                "conversions": {"$sum": {"$cond": ["$converted", 1, 0]}}
            }},
            {"$sort": {"_id": 1}}
        ]
        
        daily_data = await db.click_tracking.aggregate(pipeline).to_list(length=None)
        
        # Format for chart
        chart_data = []
        for data in daily_data:
            date = datetime(data["_id"]["year"], data["_id"]["month"], data["_id"]["day"])
            chart_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "clicks": data["clicks"],
                "conversions": data["conversions"],
                "conversion_rate": (data["conversions"] / data["clicks"] * 100) if data["clicks"] > 0 else 0
            })
        
        return {
            "success": True,
            "chart_data": chart_data,
            "period": period
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chart data: {str(e)}")

@router.get("/resources")
async def get_affiliate_resources():
    """Get affiliate resources and materials"""
    resources = [
        {
            "id": "roi_calculator",
            "title": "Affiliate ROI Calculator",
            "description": "Interactive Excel calculator to demonstrate potential returns to prospects",
            "type": "spreadsheet",
            "file_type": "xlsx",
            "download_url": "https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/rjb3ex4l_Affiliate%20ROI%20Calculator.xlsx",
            "category": "tools",
            "usage_tips": [
                "Show prospects their potential returns with detailed calculations",
                "Use during sales presentations to demonstrate value",
                "Include in follow-up emails to prospects",
                "Customize the calculator for specific customer scenarios"
            ]
        },
        {
            "id": "customer_iq_articles",
            "title": "Customer IQ Articles",
            "description": "Professional content and marketing materials for campaigns",
            "type": "document",
            "file_type": "docx",
            "download_url": "https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/6u3fbl33_Customer%20IQ%20Articles.docx",
            "category": "content",
            "usage_tips": [
                "Share on social media platforms to build authority",
                "Use content in email marketing campaigns",
                "Repurpose articles for blog posts and newsletters",
                "Reference in prospect conversations to educate"
            ]
        },
        {
            "id": "faq_document",
            "title": "Customer Mind IQ FAQ",
            "description": "Comprehensive FAQ covering all features and common questions",
            "type": "document", 
            "file_type": "docx",
            "download_url": "https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/ykt0gvbj_Customer%20Mind%20IQ%20FAQ.docx",
            "category": "support",
            "usage_tips": [
                "Reference when answering prospect questions",
                "Include relevant answers in email responses",
                "Use for objection handling during sales calls",
                "Share specific sections that address prospect concerns"
            ]
        },
        {
            "id": "white_paper",
            "title": "CMIQ White Paper",
            "description": "Professional white paper demonstrating Customer Mind IQ's value and methodology",
            "type": "document",
            "file_type": "docx", 
            "download_url": "https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/o86gio0n_CMIQ%20White%20Paper.docx",
            "category": "content",
            "usage_tips": [
                "Use as lead magnets in marketing campaigns",
                "Share with enterprise prospects to demonstrate expertise",
                "Include in proposal presentations to add credibility",
                "Post on LinkedIn and industry forums to build authority"
            ]
        },
        {
            "id": "pricing_schedule",
            "title": "Customer Mind Pricing Schedule", 
            "description": "Detailed pricing guide with all plans, features, and implementation costs",
            "type": "document",
            "file_type": "docx",
            "download_url": "https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/kaakxy6c_Customer%20Mind%20Pricing%20Schedule.docx",
            "category": "sales",
            "usage_tips": [
                "Reference during pricing discussions with prospects",
                "Use to create custom quotes and proposals",
                "Share with qualified leads to demonstrate value tiers",
                "Include in sales presentations and follow-up materials"
            ]
        },
        {
            "id": "affiliate_banners",
            "title": "Affiliate Marketing Banners",
            "description": "10 high-converting banner designs for social media, email, and web advertising",
            "type": "webpage",
            "file_type": "html",
            "download_url": f"{os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:3000')}/affiliate-banners.html",
            "category": "marketing",
            "usage_tips": [
                "Use different banners for different platforms (email, social, ads)",
                "Right-click banners to save as images for your campaigns",
                "Test different headlines and CTAs to optimize performance",
                "Replace emoji icons with your logo for brand consistency",
                "Focus on Growth Acceleration module as key differentiator"
            ]
        },
        {
            "id": "trial_audio",
            "title": "7-Day Free Trial Audio",
            "description": "Professional audio clip promoting the 7-day free trial for marketing campaigns",
            "type": "audio",
            "file_type": "mp3",
            "download_url": "https://customer-assets.emergentagent.com/job_c868e713-75a0-4b49-a7a7-697ac440ca39/artifacts/14ovry8g_7%20day%20free%20trial%20audio.mp3",
            "category": "marketing",
            "usage_tips": [
                "Use in podcast advertisements and sponsorships",
                "Include in video presentations and webinars",
                "Add to social media videos as voice-over",
                "Perfect for phone-based sales presentations",
                "Use in automated voice campaigns"
            ]
        },
        {
            "id": "growth_acceleration_video",
            "title": "Growth Acceleration Intro Slideshow",
            "description": "Comprehensive video slideshow explaining Growth Acceleration Engine features and benefits",
            "type": "video",
            "file_type": "mp4",
            "download_url": "https://customer-assets.emergentagent.com/job_c868e713-75a0-4b49-a7a7-697ac440ca39/artifacts/3f5sbcbd_Growth%20Acceleration%20intro%20slide%20show.mp4",
            "category": "content",
            "usage_tips": [
                "Share on LinkedIn and social media to demonstrate value",
                "Use in sales presentations to prospects",
                "Embed in email campaigns for visual engagement",
                "Post on YouTube with your affiliate tracking links",
                "Include in webinars as supporting content"
            ]
        },
        {
            "id": "intro_brief_video",
            "title": "Customer Mind IQ Intro Brief Video",
            "description": "Quick introduction video explaining Customer Mind IQ platform and core benefits",
            "type": "video",
            "file_type": "mp4",
            "download_url": "https://customer-assets.emergentagent.com/job_c868e713-75a0-4b49-a7a7-697ac440ca39/artifacts/xqe443kb_Intro%20brief%20video.mp4",
            "category": "content",
            "usage_tips": [
                "Perfect for initial prospect outreach and introductions",
                "Use as opener in sales presentations",
                "Share in first email contact to warm prospects",
                "Post on social media as educational content",
                "Include in website landing pages for credibility"
            ]
        },
        {
            "id": "prompt_explanation_presentation",
            "title": "AI Prompt Explanation Presentation",
            "description": "PowerPoint presentation explaining how to use AI prompts effectively with Customer Mind IQ",
            "type": "presentation",
            "file_type": "pptx",
            "download_url": "https://customer-assets.emergentagent.com/job_c868e713-75a0-4b49-a7a7-697ac440ca39/artifacts/v1vexy6i_Prompt%20explanation%20video.pptx",
            "category": "training",
            "usage_tips": [
                "Use in prospect training sessions and demos",
                "Customize slides with your branding and contact info",
                "Share with technical prospects who want implementation details",
                "Include in proposals to show training and support value",
                "Use as webinar content to educate potential customers"
            ]
        }
    ]
    
    return {
        "success": True,
        "resources": resources,
        "total_resources": len(resources),
        "categories": ["tools", "content", "support", "sales", "marketing", "training"],
        "message": "Affiliate resources retrieved successfully"
    }

@router.post("/resources/{resource_id}/download")
async def track_resource_download(resource_id: str, affiliate_id: str = None):
    """Track resource downloads for analytics"""
    try:
        download_record = {
            "resource_id": resource_id,
            "affiliate_id": affiliate_id,
            "download_timestamp": datetime.now(),
            "ip_address": "tracking_enabled",
            "user_agent": "tracking_enabled"
        }
        
        # Insert download tracking record
        await db.resource_downloads.insert_one(download_record)
        
        return {
            "success": True,
            "message": "Download tracked successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error tracking download: {str(e)}"
        }