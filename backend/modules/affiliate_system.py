# Multi-Site Affiliate System with Advanced Tracking Integration
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
from urllib.parse import urlencode
import json

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

router = APIRouter(prefix="/api/affiliate", tags=["Multi-Site Affiliate System"])

# ========== MULTI-SITE MODELS ==========

class Site(BaseModel):
    site_id: str = Field(primary_key=True)
    name: str
    domain: str
    logo_url: Optional[str] = None
    primary_color: str = "#3B82F6"
    commission_multiplier: float = 1.0
    status: str = "active"  # active, inactive, maintenance
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    custom_commission_rates: Optional[Dict] = None

class SiteAffiliateRelationship(BaseModel):
    site_id: str
    affiliate_id: str
    join_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "active"  # active, inactive, pending
    site_specific_rate_override: Optional[float] = None

class EnhancedCommissionRecord(BaseModel):
    commission_id: str = Field(primary_key=True)
    affiliate_id: str
    customer_id: str
    site_id: str  # NEW: Which site generated this
    plan_type: str
    commission_amount: float
    commission_rate: float
    base_amount: float
    status: str
    earned_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    paid_date: Optional[datetime] = None
    
    # Multi-site enhancements
    cross_site_bonus: float = 0.0
    combo_discount_applied: bool = False
    attributed_sites: List[str] = []
    bonus_details: Dict = {}

class ComboDiscountRule(BaseModel):
    rule_id: str = Field(primary_key=True)
    name: str
    description: str
    sites_required: List[str]  # Which sites need conversions
    timeframe_days: int = 30
    bonus_percentage: float  # e.g., 0.15 for 15% bonus
    min_conversions_per_site: int = 1
    min_total_value: float = 0.0
    status: str = "active"  # active, inactive
    valid_from: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: Optional[datetime] = None

class ComboDiscountTracking(BaseModel):
    tracking_id: str = Field(primary_key=True)
    affiliate_id: str
    rule_id: str
    customer_id: str
    sites_involved: List[str]
    total_bonus_amount: float
    applied_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    commission_ids: List[str]

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
    HELD = "held"
    RELEASED = "released"
    CANCELLED = "cancelled"

class LinkType(str, Enum):
    TRIAL = "trial"
    LANDING = "landing"
    DEMO = "demo"
    PRICING = "pricing"

# Enhanced affiliate registration for multi-site
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
    terms_accepted: bool = Field(..., description="Must accept terms and conditions")
    # Multi-site preferences
    interested_sites: List[str] = []  # Sites they want to promote

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('terms_accepted')
    def validate_terms(cls, v):
        if not v:
            raise ValueError('You must accept the terms and conditions')
        return v

# ========== CONFIGURATION ==========

# Site configurations - 10 sites as specified
SITES_CONFIG = {
    "customermindiq": {
        "name": "CustomerMindIQ.com",
        "domain": "customermindiq.com",
        "logo_url": "/logos/customermindiq.png"
    },
    "postvelocity": {
        "name": "PostVelocity.com", 
        "domain": "postvelocity.com",
        "logo_url": "/logos/postvelocity.png"
    },
    "connectmycustomer": {
        "name": "ConnectMyCustomer.com",
        "domain": "connectmycustomer.com", 
        "logo_url": "/logos/connectmycustomer.png"
    },
    "usethissearch": {
        "name": "UseThisSearch.com",
        "domain": "usethissearch.com",
        "logo_url": "/logos/usethissearch.png"
    },
    "groupkeywords": {
        "name": "GroupKeywords.com",
        "domain": "groupkeywords.com",
        "logo_url": "/logos/groupkeywords.png"
    },
    "trainercreator": {
        "name": "TrainerCreator.com",
        "domain": "trainercreator.com",
        "logo_url": "/logos/trainercreator.png"
    },
    "cleancutvideos": {
        "name": "CleanCutVideos.com",
        "domain": "cleancutvideos.com",
        "logo_url": "/logos/cleancutvideos.png"
    },
    "seegrabpost": {
        "name": "SeeGrabPost.com",
        "domain": "seegrabpost.com",
        "logo_url": "/logos/seegrabpost.png"
    },
    "backlinkdigger": {
        "name": "BacklinkDigger.com",
        "domain": "backlinkdigger.com",
        "logo_url": "/logos/backlinkdigger.png"
    },
    "site_10": {
        "name": "Site 10 - TBD",
        "domain": "site10.com",
        "logo_url": "/logos/site10.png"
    }
}

# Multi-Site Commission Structure (EASILY ADJUSTABLE)
MULTI_SITE_COMMISSION_RATES = {
    "launch": {
        "base_rates": {
            "initial": 0.30, 
            "recurring": [0.20] * 11 + [0.10] * 12
        },
        "multi_site_bonuses": {
            2: 0.05,   # 5% bonus for 2+ sites
            3: 0.10,   # 10% bonus for 3+ sites
            5: 0.15,   # 15% bonus for 5+ sites
            10: 0.20   # 20% bonus for all sites
        }
    },
    "growth": {
        "base_rates": {
            "initial": 0.40, 
            "recurring": [0.20] * 11 + [0.10] * 12
        },
        "multi_site_bonuses": {
            2: 0.05,
            3: 0.12,
            5: 0.18,
            10: 0.25
        }
    },
    "scale": {
        "base_rates": {
            "initial": 0.50, 
            "recurring": [0.20] * 11 + [0.10] * 12
        },
        "multi_site_bonuses": {
            2: 0.05,
            3: 0.15,
            5: 0.20,
            10: 0.30
        }
    }
}

# Default Combo Discount Rules (EASILY ADJUSTABLE)
DEFAULT_COMBO_RULES = [
    {
        "name": "Cross-Site Customer Journey",
        "description": "Purchase from 3+ sites within 30 days = 15% bonus",
        "sites_required": ["customermindiq", "postvelocity", "connectmycustomer"],
        "timeframe_days": 30,
        "bonus_percentage": 0.15,
        "min_conversions_per_site": 1,
        "min_total_value": 0.0
    },
    {
        "name": "Black Friday Special",
        "description": "Conversions across 5+ sites in November = 25% bonus", 
        "sites_required": ["customermindiq", "postvelocity", "connectmycustomer", "usethissearch", "groupkeywords"],
        "timeframe_days": 30,
        "bonus_percentage": 0.25,
        "min_conversions_per_site": 1,
        "min_total_value": 100.0
    }
]

# New models for enhanced affiliate system
class HoldbackSettings(BaseModel):
    percentage: float = Field(default=20.0, ge=0, le=100, description="Percentage to hold back")
    hold_days: int = Field(default=30, ge=0, description="Days to hold funds")
    custom_settings: bool = Field(default=False, description="Whether custom settings are applied")
    admin_notes: Optional[str] = Field(None, description="Admin notes about holdback settings")

class RefundTracking(BaseModel):
    customer_id: str
    affiliate_id: str
    order_id: str
    refund_amount: float
    refund_date: datetime
    original_commission: float
    commission_clawed_back: float
    reason: Optional[str] = None

class EarningsHoldback(BaseModel):
    id: str
    affiliate_id: str
    commission_id: str
    original_amount: float
    held_amount: float
    held_date: datetime
    release_date: datetime
    status: str  # "held", "released", "cancelled"
    admin_modified: bool = Field(default=False)
    admin_notes: Optional[str] = None

class AffiliateMonitoring(BaseModel):
    affiliate_id: str
    refund_rate_90d: float = Field(default=0.0, description="90-day refund rate percentage")
    total_revenue_90d: float = Field(default=0.0, description="90-day total revenue generated")
    refunded_revenue_90d: float = Field(default=0.0, description="90-day refunded revenue")
    flagged_high_refund: bool = Field(default=False, description="Flagged for >15% refund rate")
    account_paused: bool = Field(default=False, description="Account paused by admin")
    pause_reason: Optional[str] = None
    last_calculated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    custom_holdback: Optional[HoldbackSettings] = None

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
    available_commissions: float = 0.0  # Immediately available (80% of earnings)
    held_commissions: float = 0.0       # Currently held (20% for 30 days)
    pending_release: float = 0.0        # Held funds ready for next payment
    paid_commissions: float = 0.0
    refund_rate_90d: float = 0.0
    account_paused: bool = False
    created_at: datetime
    approved_at: Optional[datetime]
    last_login: Optional[datetime]
    terms_accepted: bool = True
    terms_accepted_at: Optional[datetime]

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

# ========== MULTI-SITE FUNCTIONS ==========

async def get_affiliate_active_sites(affiliate_id: str) -> List[str]:
    """Get all active sites for an affiliate"""
    relationships = await db.site_affiliate_relationships.find({
        "affiliate_id": affiliate_id,
        "status": "active"
    }).to_list(length=None)
    
    return [rel["site_id"] for rel in relationships]

async def get_site_config(site_id: str) -> Dict:
    """Get site configuration"""
    site = await db.sites.find_one({"site_id": site_id})
    if site:
        return site
    
    # Fallback to default config
    return SITES_CONFIG.get(site_id, {
        "name": f"Site {site_id}",
        "domain": f"{site_id}.com",
        "logo_url": f"/logos/{site_id}.png"
    })

def calculate_multi_site_bonus(site_count: int, plan_type: str, base_commission: float) -> float:
    """Calculate bonus based on number of active sites"""
    if site_count < 2:
        return 0.0
    
    bonus_rates = MULTI_SITE_COMMISSION_RATES[plan_type]["multi_site_bonuses"]
    
    # Find the highest applicable bonus rate
    applicable_bonus = 0.0
    for required_sites, bonus_rate in sorted(bonus_rates.items()):
        if site_count >= required_sites:
            applicable_bonus = bonus_rate
    
    return base_commission * applicable_bonus

async def check_combo_discount_eligibility(
    affiliate_id: str,
    customer_id: str,
    current_site_id: str,
    current_amount: float
) -> float:
    """Check if customer qualifies for combo discounts"""
    
    # Get active combo rules
    active_rules = await db.combo_discount_rules.find({"status": "active"}).to_list(length=None)
    
    total_bonus = 0.0
    
    for rule in active_rules:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=rule["timeframe_days"])
        
        # Check if customer has recent conversions on required sites
        recent_conversions = await db.enhanced_commission_records.find({
            "customer_id": customer_id,
            "site_id": {"$in": rule["sites_required"]},
            "earned_date": {"$gte": cutoff_date}
        }).to_list(length=None)
        
        # Group by site
        sites_with_conversions = {}
        for conv in recent_conversions:
            if conv["site_id"] not in sites_with_conversions:
                sites_with_conversions[conv["site_id"]] = []
            sites_with_conversions[conv["site_id"]].append(conv)
        
        # Add current site if it's in required sites
        if current_site_id in rule["sites_required"]:
            if current_site_id not in sites_with_conversions:
                sites_with_conversions[current_site_id] = []
        
        # Check if rule requirements are met
        if len(sites_with_conversions) >= len(rule["sites_required"]):
            # Calculate total value across sites
            total_value = sum(conv["base_amount"] for convs in sites_with_conversions.values() for conv in convs)
            total_value += current_amount  # Include current purchase
            
            if total_value >= rule["min_total_value"]:
                # Apply bonus
                bonus_amount = total_value * rule["bonus_percentage"]
                total_bonus += bonus_amount
                
                # Log combo discount application
                await db.combo_discount_tracking.insert_one({
                    "tracking_id": str(uuid.uuid4()),
                    "affiliate_id": affiliate_id,
                    "rule_id": rule["rule_id"],
                    "customer_id": customer_id,
                    "sites_involved": list(sites_with_conversions.keys()) + [current_site_id],
                    "total_bonus_amount": bonus_amount,
                    "applied_date": datetime.now(timezone.utc),
                    "commission_ids": []
                })
    
    return total_bonus

async def calculate_multisite_commission(
    affiliate_id: str,
    customer_id: str,
    site_id: str,
    plan_type: str,
    amount: float,
    billing_cycle: str = "monthly"
) -> Dict:
    """Calculate commission with multi-site bonuses and combo discounts"""
    
    # Get base commission
    base_rate = MULTI_SITE_COMMISSION_RATES[plan_type]["base_rates"]["initial"]
    base_commission = amount * base_rate
    
    # Get affiliate's active sites for multi-site bonus
    active_sites = await get_affiliate_active_sites(affiliate_id)
    multi_site_bonus = calculate_multi_site_bonus(
        len(active_sites), 
        plan_type, 
        base_commission
    )
    
    # Check for combo discount eligibility
    combo_bonus = await check_combo_discount_eligibility(
        affiliate_id,
        customer_id,
        site_id,
        amount
    )
    
    # Calculate total commission
    total_commission = base_commission + multi_site_bonus + combo_bonus
    
    return {
        "base_commission": base_commission,
        "multi_site_bonus": multi_site_bonus,
        "combo_bonus": combo_bonus,
        "total_commission": total_commission,
        "bonus_details": {
            "active_sites_count": len(active_sites),
            "combo_rules_applied": combo_bonus > 0,
            "site_id": site_id
        }
    }

# ========== MULTI-SITE TRACKING LINKS ==========

async def generate_multisite_tracking_link(
    link_data: Dict,
    affiliate_id: str,
    site_id: str,
    campaign_name: Optional[str] = None
) -> Dict:
    """Generate tracking links with multi-site support"""
    
    # Get site configuration
    site_config = await get_site_config(site_id)
    base_url = f"https://{site_config['domain']}"
    
    # Generate enhanced UTM parameters
    utm_params = {
        "utm_source": f"affiliate_{affiliate_id}",
        "utm_medium": "affiliate",
        "utm_campaign": campaign_name or f"general_{site_id}",
        "utm_content": f"site_{site_id}",
        "utm_term": f"multisite_{len(await get_affiliate_active_sites(affiliate_id))}",
        "ref": affiliate_id,
        "site_id": site_id,
        "ms_track": "1",  # Multi-site tracking flag
        "aff_tier": await get_affiliate_tier(affiliate_id)
    }
    
    # Build tracking URL
    path = link_data.get("path", "")
    tracking_url = f"{base_url}{path}?" + urlencode(utm_params)
    
    # Generate short URL
    short_url = f"https://cmiq.ly/{secrets.token_urlsafe(6)}"
    
    # Store for analytics
    await db.multisite_tracking_links.insert_one({
        "id": str(uuid.uuid4()),
        "affiliate_id": affiliate_id,
        "site_id": site_id,
        "url": tracking_url,
        "short_url": short_url,
        "utm_params": utm_params,
        "campaign_name": campaign_name,
        "clicks": 0,
        "conversions": 0,
        "created_at": datetime.now(timezone.utc)
    })
    
    return {
        "tracking_url": tracking_url,
        "short_url": short_url,
        "utm_params": utm_params,
        "site_name": site_config["name"],
        "expected_commission_rate": await get_expected_commission_rate(affiliate_id, site_id)
    }

async def get_affiliate_tier(affiliate_id: str) -> str:
    """Get affiliate tier based on performance"""
    active_sites = await get_affiliate_active_sites(affiliate_id)
    site_count = len(active_sites)
    
    if site_count >= 10:
        return "platinum"
    elif site_count >= 5:
        return "gold"
    elif site_count >= 2:
        return "silver"
    else:
        return "bronze"

async def get_expected_commission_rate(affiliate_id: str, site_id: str) -> float:
    """Calculate expected commission rate for affiliate on specific site"""
    # This would be based on average plan type conversions, etc.
    return 0.40  # Default to growth plan rate

# Commission calculation rates
COMMISSION_RATES = {
    "launch": {"initial": 0.30, "trailing_2_12": 0.20, "trailing_13_24": 0.10},
    "growth": {"initial": 0.40, "trailing_2_12": 0.20, "trailing_13_24": 0.10},
    "scale": {"initial": 0.50, "trailing_2_12": 0.20, "trailing_13_24": 0.10}
}

# ========== HOLDBACK SYSTEM FUNCTIONS ==========

async def get_affiliate_holdback_settings(affiliate_id: str) -> HoldbackSettings:
    """Get holdback settings for affiliate (default or custom)"""
    monitoring = await db.affiliate_monitoring.find_one({"affiliate_id": affiliate_id})
    if monitoring and monitoring.get("custom_holdback"):
        return HoldbackSettings(**monitoring["custom_holdback"])
    return HoldbackSettings()  # Default 20% for 30 days

async def apply_holdback_to_commission(affiliate_id: str, commission_amount: float, commission_id: str) -> dict:
    """Apply holdback to commission and return split amounts"""
    settings = await get_affiliate_holdback_settings(affiliate_id)
    
    held_amount = commission_amount * (settings.percentage / 100)
    available_amount = commission_amount - held_amount
    
    # Create holdback record
    holdback_record = {
        "id": str(uuid.uuid4()),
        "affiliate_id": affiliate_id,
        "commission_id": commission_id,
        "original_amount": commission_amount,
        "held_amount": held_amount,
        "held_date": datetime.now(timezone.utc),
        "release_date": datetime.now(timezone.utc) + timedelta(days=settings.hold_days),
        "status": "held",
        "admin_modified": settings.custom_settings,
        "admin_notes": settings.admin_notes
    }
    
    await db.earnings_holdback.insert_one(holdback_record)
    
    return {
        "available_amount": available_amount,
        "held_amount": held_amount,
        "holdback_id": holdback_record["id"]
    }

async def calculate_refund_rate(affiliate_id: str, days: int = 90) -> dict:
    """Calculate refund rate for affiliate over specified days"""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Get total revenue generated by affiliate in period
    total_revenue_cursor = db.affiliate_commissions.aggregate([
        {
            "$match": {
                "affiliate_id": affiliate_id,
                "created_at": {"$gte": cutoff_date},
                "status": {"$ne": "cancelled"}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_revenue": {"$sum": "$original_amount"}
            }
        }
    ])
    total_revenue_result = await total_revenue_cursor.to_list(length=1)
    total_revenue = total_revenue_result[0]["total_revenue"] if total_revenue_result else 0
    
    # Get refunded revenue in period
    refunded_revenue_cursor = db.refund_tracking.aggregate([
        {
            "$match": {
                "affiliate_id": affiliate_id,
                "refund_date": {"$gte": cutoff_date}
            }
        },
        {
            "$group": {
                "_id": None,
                "refunded_revenue": {"$sum": "$refund_amount"}
            }
        }
    ])
    refunded_revenue_result = await refunded_revenue_cursor.to_list(length=1)
    refunded_revenue = refunded_revenue_result[0]["refunded_revenue"] if refunded_revenue_result else 0
    
    # Calculate refund rate
    refund_rate = (refunded_revenue / total_revenue * 100) if total_revenue > 0 else 0
    
    return {
        "refund_rate": refund_rate,
        "total_revenue": total_revenue,
        "refunded_revenue": refunded_revenue,
        "flagged": refund_rate > 15.0
    }

async def update_affiliate_monitoring(affiliate_id: str):
    """Update affiliate monitoring data with latest refund rate"""
    refund_data = await calculate_refund_rate(affiliate_id)
    
    monitoring_update = {
        "affiliate_id": affiliate_id,
        "refund_rate_90d": refund_data["refund_rate"],
        "total_revenue_90d": refund_data["total_revenue"],
        "refunded_revenue_90d": refund_data["refunded_revenue"],
        "flagged_high_refund": refund_data["flagged"],
        "last_calculated": datetime.now(timezone.utc)
    }
    
    await db.affiliate_monitoring.update_one(
        {"affiliate_id": affiliate_id},
        {"$set": monitoring_update},
        upsert=True
    )
    
    return monitoring_update

async def process_monthly_holdback_releases():
    """Process monthly releases of held funds (run as scheduled job)"""
    current_date = datetime.now(timezone.utc)
    
    # Find all held funds ready for release
    ready_for_release = await db.earnings_holdback.find({
        "status": "held",
        "release_date": {"$lte": current_date}
    }).to_list(length=None)
    
    released_count = 0
    total_released = 0
    
    for holdback in ready_for_release:
        # Update holdback status
        await db.earnings_holdback.update_one(
            {"id": holdback["id"]},
            {"$set": {"status": "released", "released_date": current_date}}
        )
        
        # Add to affiliate's available balance
        await db.affiliates.update_one(
            {"affiliate_id": holdback["affiliate_id"]},
            {"$inc": {"available_commissions": holdback["held_amount"]}}
        )
        
        released_count += 1
        total_released += holdback["held_amount"]
    
    return {
        "released_count": released_count,
        "total_released": total_released,
        "processed_at": current_date
    }

# ========== AUTHENTICATION ENDPOINTS ==========

@router.post("/auth/register")
async def register_affiliate(registration: AffiliateRegistration):
    """Register new affiliate with multi-site preferences"""
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
        current_time = datetime.now(timezone.utc)
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
            # Multi-site enhancements
            "interested_sites": registration.interested_sites,
            "active_sites": [],  # Will be populated after approval
            # Existing fields
            "total_clicks": 0,
            "total_conversions": 0,
            "total_commissions": 0.0,
            "available_commissions": 0.0,
            "held_commissions": 0.0,
            "pending_release": 0.0,
            "paid_commissions": 0.0,
            "refund_rate_90d": 0.0,
            "account_paused": False,
            "terms_accepted": registration.terms_accepted,
            "terms_accepted_at": current_time if registration.terms_accepted else None,
            "created_at": current_time,
            "updated_at": current_time,
            "approved_at": None,
            "last_login": None,
            "email_verified": False,
            "verification_token": secrets.token_urlsafe(32)
        }
        
        # Insert affiliate
        result = await db.affiliates.insert_one(affiliate_data)
        
        # Initialize monitoring record
        await db.affiliate_monitoring.insert_one({
            "affiliate_id": affiliate_id,
            "refund_rate_90d": 0.0,
            "total_revenue_90d": 0.0,
            "refunded_revenue_90d": 0.0,
            "flagged_high_refund": False,
            "account_paused": False,
            "pause_reason": None,
            "last_calculated": current_time,
            "custom_holdback": None
        })
        
        # Create site relationships for interested sites
        for site_id in registration.interested_sites:
            await db.site_affiliate_relationships.insert_one({
                "site_id": site_id,
                "affiliate_id": affiliate_id,
                "join_date": current_time,
                "status": "pending"  # Will be activated after approval
            })
        
        return {
            "success": True,
            "affiliate_id": affiliate_id,
            "message": "Registration successful. Please verify your email.",
            "verification_email_sent": True,
            "sites_applied_for": len(registration.interested_sites)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/auth/login")
async def login_affiliate(login_data: AffiliateLogin):
    """Affiliate login with multi-site information"""
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
        
        # Get active sites count and tier
        active_sites = await get_affiliate_active_sites(affiliate["affiliate_id"])
        tier = await get_affiliate_tier(affiliate["affiliate_id"])
        
        return {
            "success": True,
            "token": token,
            "affiliate": {
                "id": affiliate["affiliate_id"],
                "name": f"{affiliate['first_name']} {affiliate['last_name']}",
                "status": affiliate["status"],
                "total_commissions": affiliate["total_commissions"],
                "active_sites_count": len(active_sites),
                "tier": tier,
                "multi_site_enabled": True
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/multisite-dashboard")
async def get_multisite_dashboard(
    affiliate_id: str = Query(...),
    site_ids: Optional[List[str]] = Query(None)
):
    """Get multi-site affiliate dashboard data"""
    try:
        # Get affiliate data
        affiliate = await db.affiliates.find_one({"affiliate_id": affiliate_id})
        if not affiliate:
            raise HTTPException(status_code=404, detail="Affiliate not found")
        
        # Get affiliate's sites if none specified
        if not site_ids:
            site_ids = await get_affiliate_active_sites(affiliate_id)
        
        dashboard_data = {}
        total_stats = {
            "total_earnings": 0,
            "total_clicks": 0,
            "total_conversions": 0,
            "multi_site_bonuses": 0,
            "combo_bonuses": 0
        }
        
        # Get performance data for each site
        for site_id in site_ids:
            site_data = await get_site_performance_data(affiliate_id, site_id)
            dashboard_data[site_id] = site_data
            
            # Aggregate totals
            total_stats["total_earnings"] += site_data.get("earnings", 0)
            total_stats["total_clicks"] += site_data.get("clicks", 0)
            total_stats["total_conversions"] += site_data.get("conversions", 0)
            total_stats["multi_site_bonuses"] += site_data.get("multi_site_bonuses", 0)
            total_stats["combo_bonuses"] += site_data.get("combo_bonuses", 0)
        
        # Get combo discount opportunities
        combo_opportunities = await get_combo_discount_opportunities(affiliate_id)
        
        return {
            "sites_data": dashboard_data,
            "aggregated_stats": total_stats,
            "combo_opportunities": combo_opportunities,
            "affiliate_tier": await get_affiliate_tier(affiliate_id),
            "next_tier_requirements": await get_next_tier_requirements(affiliate_id),
            "available_sites": [
                {
                    "site_id": site_id,
                    "name": config["name"],
                    "domain": config["domain"],
                    "logo_url": config["logo_url"]
                }
                for site_id, config in SITES_CONFIG.items()
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

async def get_site_performance_data(affiliate_id: str, site_id: str) -> Dict:
    """Get performance data for a specific site"""
    
    # Get site clicks from multisite tracking links
    site_clicks = await db.multisite_tracking_links.aggregate([
        {"$match": {"affiliate_id": affiliate_id, "site_id": site_id}},
        {"$group": {"_id": None, "total_clicks": {"$sum": "$clicks"}}}
    ]).to_list(length=1)
    
    clicks = site_clicks[0]["total_clicks"] if site_clicks else 0
    
    # Get site commissions and earnings
    site_commissions = await db.enhanced_commission_records.find({
        "affiliate_id": affiliate_id,
        "site_id": site_id
    }).to_list(length=None)
    
    earnings = sum(commission.get("commission_amount", 0) for commission in site_commissions)
    conversions = len(site_commissions)
    multi_site_bonuses = sum(commission.get("cross_site_bonus", 0) for commission in site_commissions)
    combo_bonuses = sum(commission.get("bonus_details", {}).get("combo_bonus", 0) for commission in site_commissions)
    
    return {
        "earnings": earnings,
        "clicks": clicks,
        "conversions": conversions,
        "multi_site_bonuses": multi_site_bonuses,
        "combo_bonuses": combo_bonuses,
        "conversion_rate": (conversions / clicks * 100) if clicks > 0 else 0
    }

async def get_combo_discount_opportunities(affiliate_id: str) -> List[Dict]:
    """Get available combo discount opportunities for affiliate"""
    
    active_rules = await db.combo_discount_rules.find({"status": "active"}).to_list(length=None)
    opportunities = []
    
    for rule in active_rules:
        # Check progress towards rule requirements
        affiliate_sites = await get_affiliate_active_sites(affiliate_id)
        required_sites = set(rule["sites_required"])
        active_required_sites = set(affiliate_sites).intersection(required_sites)
        
        progress = len(active_required_sites) / len(required_sites) * 100
        
        opportunities.append({
            "rule_id": rule["rule_id"],
            "name": rule["name"],
            "description": rule["description"],
            "bonus_percentage": rule["bonus_percentage"] * 100,
            "progress": progress,
            "sites_needed": list(required_sites - active_required_sites),
            "eligible": progress >= 100
        })
    
    return opportunities

async def get_next_tier_requirements(affiliate_id: str) -> Dict:
    """Get requirements for next affiliate tier"""
    active_sites = await get_affiliate_active_sites(affiliate_id)
    current_count = len(active_sites)
    
    if current_count >= 10:
        return {"current_tier": "platinum", "next_tier": None}
    elif current_count >= 5:
        return {"current_tier": "gold", "next_tier": "platinum", "sites_needed": 10 - current_count}
    elif current_count >= 2:
        return {"current_tier": "silver", "next_tier": "gold", "sites_needed": 5 - current_count}
    else:
        return {"current_tier": "bronze", "next_tier": "silver", "sites_needed": 2 - current_count}

@router.get("/dashboard")
async def get_affiliate_dashboard_legacy(affiliate_id: str = Query(...)):
    """Legacy dashboard endpoint - redirects to multi-site dashboard"""
    return await get_multisite_dashboard(affiliate_id=affiliate_id)

@router.post("/generate-link")
async def generate_tracking_link_legacy(
    link_data: Dict[str, Any],
    affiliate_id: str = Query(...)
):
    """Legacy link generation - defaults to main site for compatibility"""
    try:
        # Default to main site for legacy compatibility
        result = await generate_multisite_tracking_link(
            link_data=link_data,
            affiliate_id=affiliate_id,
            site_id="customermindiq",
            campaign_name=link_data.get("campaign_name")
        )
        
        return {
            "success": True,
            "tracking_url": result["tracking_url"],
            "short_url": result["short_url"],
            "qr_code": f"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."  # Placeholder
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Link generation failed: {str(e)}")

@router.post("/track/event")
async def track_affiliate_event(event_data: Dict[str, Any]):
    """Enhanced event tracking with multi-site support"""
    try:
        event_type = event_data.get("event_type")
        affiliate_id = event_data.get("affiliate_id")
        site_id = event_data.get("site_id", "customermindiq")  # Default to main site
        
        if not affiliate_id:
            return {"success": True}  # Silent fail for missing affiliate ID
        
        # Record the tracking event with site information
        tracking_record = {
            "id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "site_id": site_id,  # Multi-site enhancement
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
        
        # Store in both legacy and new collections for compatibility
        await db.click_tracking.insert_one(tracking_record)  # Legacy
        await db.multisite_click_tracking.insert_one(tracking_record)  # New
        
        # Update affiliate click count
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {"$inc": {"total_clicks": 1}}
        )
        
        # Handle specific event types
        if event_type == "conversion":
            await handle_multisite_conversion_event(event_data)
        
        return {"success": True, "site_id": site_id}
        
    except Exception as e:
        print(f"Tracking error: {e}")
        return {"success": False, "error": str(e)}

async def handle_multisite_conversion_event(event_data: Dict[str, Any]):
    """Handle conversion events with multi-site commission calculation"""
    try:
        affiliate_id = event_data.get("affiliate_id")
        customer_id = event_data.get("customer_id")
        site_id = event_data.get("site_id", "customermindiq")
        plan_type = event_data.get("plan_type", "launch")
        billing_cycle = event_data.get("billing_cycle", "monthly")
        amount = float(event_data.get("amount", 0))
        
        # Update conversion tracking in both collections
        update_data = {
            "$set": {
                "converted": True,
                "conversion_date": datetime.now(timezone.utc)
            }
        }
        
        await db.click_tracking.update_one(
            {
                "affiliate_id": affiliate_id,
                "session_id": event_data.get("session_id")
            },
            update_data
        )
        
        await db.multisite_click_tracking.update_one(
            {
                "affiliate_id": affiliate_id,
                "session_id": event_data.get("session_id"),
                "site_id": site_id
            },
            update_data
        )
        
        # Create multi-site commission record
        await create_multisite_commission_record(
            affiliate_id, customer_id, site_id, plan_type, amount, billing_cycle
        )
        
        # Update affiliate conversion stats
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {"$inc": {"total_conversions": 1}}
        )
        
    except Exception as e:
        print(f"Multi-site conversion handling error: {e}")

@router.get("/materials")
async def get_affiliate_materials(affiliate_id: str = Query(...)):
    """Enhanced affiliate marketing materials with multi-site support"""
    try:
        active_sites = await get_affiliate_active_sites(affiliate_id)
        
        # If no active sites, default to main site for compatibility
        if not active_sites:
            active_sites = ["customermindiq"]
        
        materials = {
            "banners": [],
            "email_templates": [],
            "landing_pages": [],
            "social_media": []
        }
        
        # Generate materials for each active site
        for site_id in active_sites:
            site_config = await get_site_config(site_id)
            site_name = site_config["name"]
            
            # Banners
            materials["banners"].append({
                "site_id": site_id,
                "site_name": site_name,
                "name": f"{site_name} - Email Header Banner",
                "size": "600x200",
                "url": f"https://cdn.customermindiq.com/banners/{site_id}-email-header.png",
                "tracking_url": (await generate_multisite_tracking_link(
                    {"path": "/trial"}, affiliate_id, site_id, "email-banner"
                ))["tracking_url"]
            })
            
            # Email templates
            materials["email_templates"].append({
                "site_id": site_id,
                "site_name": site_name,
                "name": f"{site_name} - Educational Template",
                "subject": f"Discover the power of {site_name}",
                "content": f"Experience the benefits of {site_name}...",
                "tracking_url": (await generate_multisite_tracking_link(
                    {"path": "/trial"}, affiliate_id, site_id, "email-template"
                ))["tracking_url"]
            })
            
            # Landing pages
            materials["landing_pages"].append({
                "site_id": site_id,
                "site_name": site_name,
                "name": f"{site_name} - Main Landing Page",
                "url": f"https://{site_config['domain']}/affiliate/{affiliate_id}",
                "description": f"Personalized landing page for {site_name}"
            })
        
        return {
            "success": True,
            "materials": materials,
            "active_sites_count": len(active_sites),
            "total_materials": sum(len(materials[key]) for key in materials),
            "multi_site_enabled": len(active_sites) > 1
        }
        
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
        
        # Create commission records with holdback processing
        await create_commission_records_with_holdback(affiliate_id, customer_id, plan_type, billing_cycle, amount)
        
        # Update affiliate stats with holdback split
        commission_amount = await calculate_initial_commission(plan_type, billing_cycle, amount)
        settings = await get_affiliate_holdback_settings(affiliate_id)
        
        available_amount = commission_amount * (1 - settings.percentage / 100)
        held_amount = commission_amount * (settings.percentage / 100)
        
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {
                "$inc": {
                    "total_conversions": 1,
                    "total_commissions": commission_amount,
                    "available_commissions": available_amount,
                    "held_commissions": held_amount
                }
            }
        )
        
        # Update affiliate monitoring
        await update_affiliate_monitoring(affiliate_id)
        
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

async def create_commission_records_with_holdback(affiliate_id: str, customer_id: str, plan_type: str, billing_cycle: str, amount: float):
    """Create commission records with holdback system integration"""
    try:
        rates = COMMISSION_RATES.get(plan_type, COMMISSION_RATES["launch"])
        current_time = datetime.now(timezone.utc)
        
        if billing_cycle == "annual":
            # Annual payment: commission on full amount
            initial_commission = amount * rates["initial"]
            commission_id = str(uuid.uuid4())
            
            # Apply holdback to initial commission
            holdback_result = await apply_holdback_to_commission(affiliate_id, initial_commission, commission_id)
            
            # Create initial commission with holdback tracking
            await db.commissions.insert_one({
                "id": commission_id,
                "affiliate_id": affiliate_id,
                "customer_id": customer_id,
                "commission_type": CommissionType.INITIAL.value,
                "plan_type": plan_type,
                "billing_cycle": billing_cycle,
                "commission_rate": rates["initial"] * 100,
                "base_amount": amount,
                "commission_amount": initial_commission,
                "available_amount": holdback_result["available_amount"],
                "held_amount": holdback_result["held_amount"],
                "holdback_id": holdback_result["holdback_id"],
                "status": CommissionStatus.APPROVED.value,  # Immediately approved, but held
                "earned_date": current_time,
                "due_date": current_time + timedelta(days=30),
                "paid_date": None,
                "billing_month": 1
            })
            
            # Create second year commission (also with holdback)
            second_year_commission_id = str(uuid.uuid4())
            second_year_commission = amount * rates["trailing_13_24"]
            second_year_holdback = await apply_holdback_to_commission(affiliate_id, second_year_commission, second_year_commission_id)
            
            await db.commissions.insert_one({
                "id": second_year_commission_id,
                "affiliate_id": affiliate_id,
                "customer_id": customer_id,
                "commission_type": CommissionType.TRAILING_13_24.value,
                "plan_type": plan_type,
                "billing_cycle": billing_cycle,
                "commission_rate": rates["trailing_13_24"] * 100,
                "base_amount": amount,
                "commission_amount": second_year_commission,
                "available_amount": second_year_holdback["available_amount"],
                "held_amount": second_year_holdback["held_amount"],
                "holdback_id": second_year_holdback["holdback_id"],
                "status": CommissionStatus.PENDING.value,
                "earned_date": current_time + timedelta(days=365),
                "due_date": current_time + timedelta(days=395),
                "paid_date": None,
                "billing_month": 13
            })
        else:
            # Monthly subscriptions: create 24 commission records with holdback
            initial_commission = amount * rates["initial"]
            initial_commission_id = str(uuid.uuid4())
            
            # Apply holdback to initial commission
            initial_holdback = await apply_holdback_to_commission(affiliate_id, initial_commission, initial_commission_id)
            
            # Initial commission (month 1)
            await db.commissions.insert_one({
                "id": initial_commission_id,
                "affiliate_id": affiliate_id,
                "customer_id": customer_id,
                "commission_type": CommissionType.INITIAL.value,
                "plan_type": plan_type,
                "billing_cycle": billing_cycle,
                "commission_rate": rates["initial"] * 100,
                "base_amount": amount,
                "commission_amount": initial_commission,
                "available_amount": initial_holdback["available_amount"],
                "held_amount": initial_holdback["held_amount"],
                "holdback_id": initial_holdback["holdback_id"],
                "status": CommissionStatus.APPROVED.value,
                "earned_date": current_time,
                "due_date": current_time + timedelta(days=30),
                "paid_date": None,
                "billing_month": 1
            })
            
            # Trailing commissions months 2-12 (20%)
            for month in range(2, 13):
                trailing_commission = amount * rates["trailing_2_12"]
                trailing_commission_id = str(uuid.uuid4())
                trailing_holdback = await apply_holdback_to_commission(affiliate_id, trailing_commission, trailing_commission_id)
                
                await db.commissions.insert_one({
                    "id": trailing_commission_id,
                    "affiliate_id": affiliate_id,
                    "customer_id": customer_id,
                    "commission_type": CommissionType.TRAILING_2_12.value,
                    "plan_type": plan_type,
                    "billing_cycle": billing_cycle,
                    "commission_rate": rates["trailing_2_12"] * 100,
                    "base_amount": amount,
                    "commission_amount": trailing_commission,
                    "available_amount": trailing_holdback["available_amount"],
                    "held_amount": trailing_holdback["held_amount"],
                    "holdback_id": trailing_holdback["holdback_id"],
                    "status": CommissionStatus.PENDING.value,
                    "earned_date": current_time + timedelta(days=30*month),
                    "due_date": current_time + timedelta(days=30*month + 30),
                    "paid_date": None,
                    "billing_month": month
                })
            
            # Trailing commissions months 13-24 (10%)
            for month in range(13, 25):
                trailing_commission = amount * rates["trailing_13_24"]
                trailing_commission_id = str(uuid.uuid4())
                trailing_holdback = await apply_holdback_to_commission(affiliate_id, trailing_commission, trailing_commission_id)
                
                await db.commissions.insert_one({
                    "id": trailing_commission_id,
                    "affiliate_id": affiliate_id,
                    "customer_id": customer_id,
                    "commission_type": CommissionType.TRAILING_13_24.value,
                    "plan_type": plan_type,
                    "billing_cycle": billing_cycle,
                    "commission_rate": rates["trailing_13_24"] * 100,
                    "base_amount": amount,
                    "commission_amount": trailing_commission,
                    "available_amount": trailing_holdback["available_amount"],
                    "held_amount": trailing_holdback["held_amount"],
                    "holdback_id": trailing_holdback["holdback_id"],
                    "status": CommissionStatus.PENDING.value,
                    "earned_date": current_time + timedelta(days=30*month),
                    "due_date": current_time + timedelta(days=30*month + 30),
                    "paid_date": None,
                    "billing_month": month
                })
        
    except Exception as e:
        print(f"Commission creation with holdback error: {e}")

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

@router.post("/multisite-links/generate")
async def generate_multisite_links(
    affiliate_id: str = Query(...),
    site_ids: List[str] = Query(...),
    campaign_name: Optional[str] = None,
    link_paths: List[str] = Query(default=["/"])
):
    """Generate tracking links for multiple sites at once"""
    try:
        all_links = {}
        
        for site_id in site_ids:
            site_links = {}
            for path in link_paths:
                link_data = await generate_multisite_tracking_link(
                    link_data={"path": path},
                    affiliate_id=affiliate_id,
                    site_id=site_id,
                    campaign_name=campaign_name
                )
                site_links[path] = link_data
            all_links[site_id] = site_links
        
        return {
            "success": True,
            "tracking_links": all_links,
            "campaign_name": campaign_name,
            "generated_at": datetime.now(timezone.utc),
            "total_sites": len(site_ids)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Link generation failed: {str(e)}")

@router.post("/commission/create")
async def create_multisite_commission_record(
    affiliate_id: str,
    customer_id: str,
    site_id: str,
    plan_type: str,
    amount: float,
    billing_cycle: str = "monthly"
):
    """Create commission record with multi-site bonuses"""
    try:
        # Calculate commission with bonuses
        commission_data = await calculate_multisite_commission(
            affiliate_id, customer_id, site_id, plan_type, amount, billing_cycle
        )
        
        # Create commission record (avoid ObjectId issues by using string IDs)
        commission_record = {
            "commission_id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "customer_id": customer_id,
            "site_id": site_id,
            "plan_type": plan_type,
            "commission_amount": commission_data["total_commission"],
            "commission_rate": commission_data["total_commission"] / amount,
            "base_amount": amount,
            "status": "pending",
            "earned_date": datetime.now(timezone.utc).isoformat(),  # Convert to string
            "cross_site_bonus": commission_data["multi_site_bonus"] + commission_data["combo_bonus"],
            "combo_discount_applied": commission_data["combo_bonus"] > 0,
            "attributed_sites": await get_affiliate_active_sites(affiliate_id),
            "bonus_details": commission_data["bonus_details"]
        }
        
        # Apply holdback (existing logic)
        settings = await get_affiliate_holdback_settings(affiliate_id)
        held_amount = commission_data["total_commission"] * (settings.percentage / 100)
        available_amount = commission_data["total_commission"] - held_amount
        
        holdback_record = {
            "id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "commission_id": commission_record["commission_id"],
            "original_amount": commission_data["total_commission"],
            "held_amount": held_amount,
            "held_date": datetime.now(timezone.utc).isoformat(),  # Convert to string
            "release_date": (datetime.now(timezone.utc) + timedelta(days=settings.hold_days)).isoformat(),
            "status": "held"
        }
        
        # Store records
        await db.enhanced_commission_records.insert_one(commission_record)
        await db.earnings_holdback.insert_one(holdback_record)
        
        # Update affiliate totals
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {
                "$inc": {
                    "total_commissions": commission_data["total_commission"],
                    "available_commissions": available_amount,
                    "held_commissions": held_amount
                }
            }
        )
        
        return {
            "success": True,
            "commission_record": commission_record,
            "breakdown": commission_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Commission creation failed: {str(e)}")

@router.post("/admin/initialize-sites")
async def initialize_sites(current_user: UserProfile = Depends(require_role(UserRole.SUPER_ADMIN))):
    """Initialize sites configuration (Admin only)"""
    try:
        sites_created = 0
        
        for site_id, config in SITES_CONFIG.items():
            existing_site = await db.sites.find_one({"site_id": site_id})
            if not existing_site:
                site_data = {
                    "site_id": site_id,
                    "name": config["name"],
                    "domain": config["domain"],
                    "logo_url": config.get("logo_url"),
                    "primary_color": "#3B82F6",
                    "commission_multiplier": 1.0,
                    "status": "active",
                    "created_date": datetime.now(timezone.utc)
                }
                
                await db.sites.insert_one(site_data)
                sites_created += 1
        
        # Initialize default combo rules
        rules_created = 0
        for rule_config in DEFAULT_COMBO_RULES:
            existing_rule = await db.combo_discount_rules.find_one({"name": rule_config["name"]})
            if not existing_rule:
                rule_data = {
                    "rule_id": str(uuid.uuid4()),
                    **rule_config,
                    "status": "active",
                    "valid_from": datetime.now(timezone.utc)
                }
                
                await db.combo_discount_rules.insert_one(rule_data)
                rules_created += 1
        
        return {
            "success": True,
            "sites_created": sites_created,
            "combo_rules_created": rules_created,
            "message": f"Initialized {sites_created} sites and {rules_created} combo rules"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")

# ========== AFFILIATE MANAGEMENT ENDPOINTS ==========

# ========== ENHANCED ADMIN ENDPOINTS ==========

@router.get("/admin/monitoring/high-refund")
async def get_high_refund_affiliates(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN])),
    limit: int = Query(default=50, le=100)
):
    """Get affiliates with high refund rates (>15%)"""
    try:
        # Get all flagged affiliates
        high_refund_affiliates = await db.affiliate_monitoring.find({
            "flagged_high_refund": True
        }).limit(limit).to_list(length=limit)
        
        # Enrich with affiliate details
        enriched_affiliates = []
        for monitoring in high_refund_affiliates:
            affiliate = await db.affiliates.find_one({"affiliate_id": monitoring["affiliate_id"]})
            if affiliate:
                enriched_affiliate = {
                    "affiliate_id": monitoring["affiliate_id"],
                    "name": f"{affiliate['first_name']} {affiliate['last_name']}",
                    "email": affiliate["email"],
                    "status": affiliate["status"],
                    "refund_rate_90d": monitoring["refund_rate_90d"],
                    "total_revenue_90d": monitoring["total_revenue_90d"],
                    "refunded_revenue_90d": monitoring["refunded_revenue_90d"],
                    "account_paused": monitoring.get("account_paused", False),
                    "pause_reason": monitoring.get("pause_reason"),
                    "last_calculated": monitoring["last_calculated"],
                    "custom_holdback": monitoring.get("custom_holdback"),
                    "created_at": affiliate["created_at"]
                }
                enriched_affiliates.append(enriched_affiliate)
        
        return {
            "success": True,
            "high_refund_affiliates": enriched_affiliates,
            "total_flagged": len(enriched_affiliates)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching high refund affiliates: {str(e)}")

@router.post("/admin/affiliates/{affiliate_id}/pause")
async def pause_affiliate_account(
    affiliate_id: str,
    pause_data: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Pause affiliate account with reason"""
    try:
        reason = pause_data.get("reason", "High refund rate - under review")
        
        # Update affiliate status
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {"$set": {"account_paused": True, "status": "suspended"}}
        )
        
        # Update monitoring record
        await db.affiliate_monitoring.update_one(
            {"affiliate_id": affiliate_id},
            {
                "$set": {
                    "account_paused": True,
                    "pause_reason": reason,
                    "paused_at": datetime.now(timezone.utc),
                    "paused_by": current_user.user_id
                }
            }
        )
        
        return {
            "success": True,
            "message": f"Affiliate account paused: {reason}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error pausing affiliate: {str(e)}")

@router.post("/admin/affiliates/{affiliate_id}/resume")
async def resume_affiliate_account(
    affiliate_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Resume paused affiliate account"""
    try:
        # Update affiliate status
        await db.affiliates.update_one(
            {"affiliate_id": affiliate_id},
            {"$set": {"account_paused": False, "status": "active"}}
        )
        
        # Update monitoring record
        await db.affiliate_monitoring.update_one(
            {"affiliate_id": affiliate_id},
            {
                "$set": {
                    "account_paused": False,
                    "pause_reason": None,
                    "resumed_at": datetime.now(timezone.utc),
                    "resumed_by": current_user.user_id
                }
            }
        )
        
        return {
            "success": True,
            "message": "Affiliate account resumed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resuming affiliate: {str(e)}")

@router.post("/admin/affiliates/{affiliate_id}/holdback-settings")
async def update_holdback_settings(
    affiliate_id: str,
    settings_data: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Update custom holdback settings for affiliate"""
    try:
        percentage = float(settings_data.get("percentage", 20.0))
        hold_days = int(settings_data.get("hold_days", 30))
        admin_notes = settings_data.get("admin_notes", "")
        
        if percentage < 0 or percentage > 100:
            raise HTTPException(status_code=400, detail="Holdback percentage must be between 0 and 100")
        
        if hold_days < 0:
            raise HTTPException(status_code=400, detail="Hold days must be non-negative")
        
        custom_holdback = {
            "percentage": percentage,
            "hold_days": hold_days,
            "custom_settings": True,
            "admin_notes": admin_notes
        }
        
        # Update monitoring record with custom holdback
        await db.affiliate_monitoring.update_one(
            {"affiliate_id": affiliate_id},
            {
                "$set": {
                    "custom_holdback": custom_holdback,
                    "updated_at": datetime.now(timezone.utc),
                    "updated_by": current_user.user_id
                }
            },
            upsert=True
        )
        
        return {
            "success": True,
            "message": f"Custom holdback settings updated: {percentage}% for {hold_days} days",
            "settings": custom_holdback
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid percentage or hold days value")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating holdback settings: {str(e)}")

@router.post("/admin/monitoring/refresh")
async def refresh_affiliate_monitoring(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN])),
    affiliate_id: Optional[str] = None
):
    """Refresh monitoring data for all affiliates or specific affiliate"""
    try:
        if affiliate_id:
            # Update specific affiliate
            result = await update_affiliate_monitoring(affiliate_id)
            return {
                "success": True,
                "message": f"Monitoring data refreshed for {affiliate_id}",
                "data": result
            }
        else:
            # Update all affiliates
            affiliates = await db.affiliates.find({"status": {"$in": ["active", "approved"]}}).to_list(length=None)
            updated_count = 0
            
            for affiliate in affiliates:
                try:
                    await update_affiliate_monitoring(affiliate["affiliate_id"])
                    updated_count += 1
                except Exception as e:
                    print(f"Error updating monitoring for {affiliate['affiliate_id']}: {e}")
            
            return {
                "success": True,
                "message": f"Monitoring data refreshed for {updated_count} affiliates",
                "updated_count": updated_count
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing monitoring data: {str(e)}")

@router.post("/admin/refunds/track")
async def track_refund(
    refund_data: Dict[str, Any],
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Track a refund and update affiliate metrics"""
    try:
        customer_id = refund_data.get("customer_id")
        order_id = refund_data.get("order_id")
        refund_amount = float(refund_data.get("refund_amount", 0))
        reason = refund_data.get("reason", "Customer refund")
        
        # Find the affiliate who referred this customer
        customer = await db.customers.find_one({"customer_id": customer_id})
        if not customer or not customer.get("referred_by_affiliate"):
            return {"success": True, "message": "No affiliate associated with this customer"}
        
        affiliate_id = customer["referred_by_affiliate"]
        
        # Find original commission for this customer
        commission = await db.commissions.find_one({
            "affiliate_id": affiliate_id,
            "customer_id": customer_id,
            "commission_type": "initial"
        })
        
        original_commission = commission.get("commission_amount", 0) if commission else 0
        commission_clawed_back = min(original_commission, refund_amount * 0.3)  # Example: claw back 30% of refund
        
        # Record the refund
        refund_record = {
            "customer_id": customer_id,
            "affiliate_id": affiliate_id,
            "order_id": order_id,
            "refund_amount": refund_amount,
            "refund_date": datetime.now(timezone.utc),
            "original_commission": original_commission,
            "commission_clawed_back": commission_clawed_back,
            "reason": reason,
            "tracked_by": current_user.user_id
        }
        
        await db.refund_tracking.insert_one(refund_record)
        
        # Update affiliate's available balance (claw back commission)
        if commission_clawed_back > 0:
            await db.affiliates.update_one(
                {"affiliate_id": affiliate_id},
                {"$inc": {"available_commissions": -commission_clawed_back}}
            )
        
        # Refresh monitoring data for this affiliate
        await update_affiliate_monitoring(affiliate_id)
        
        return {
            "success": True,
            "message": "Refund tracked successfully",
            "refund_tracked": refund_record,
            "commission_clawed_back": commission_clawed_back
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking refund: {str(e)}")

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