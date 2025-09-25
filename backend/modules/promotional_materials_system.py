# CustomerMindIQ Advanced Promotional Materials System
# Complete implementation of Banner Generator, SmartLinks, A/B Testing, and Coupon Management

import os
import uuid
import hashlib
import secrets
import json
import base64
import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional, Union
from urllib.parse import urlparse, parse_qs
import aiohttp
import geoip2.database
import user_agents
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import qrcode

from fastapi import APIRouter, HTTPException, Depends, Query, File, UploadFile, BackgroundTasks
from fastapi.responses import RedirectResponse, FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum
import redis.asyncio as redis
from dotenv import load_dotenv
import logging

# Import authentication
from auth.auth_system import get_current_user, UserProfile, require_role, UserRole

# =============================================================================
# Models and Enums
# =============================================================================

class BannerCategory(str, Enum):
    LEADERBOARD = "leaderboard"
    SQUARE = "square"
    SKYSCRAPER = "skyscraper"
    MOBILE = "mobile"
    SOCIAL = "social"
    EMAIL = "email"

class BannerDimensions(str, Enum):
    LEADERBOARD_728x90 = "728x90"
    LEADERBOARD_970x250 = "970x250"
    SQUARE_300x250 = "300x250"
    SQUARE_336x280 = "336x280"
    SKYSCRAPER_160x600 = "160x600"
    SKYSCRAPER_300x600 = "300x600"
    MOBILE_320x50 = "320x50"
    MOBILE_320x100 = "320x100"
    SOCIAL_1200x630 = "1200x630"
    EMAIL_600x200 = "600x200"

class CouponType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    FREE_TRIAL = "free_trial"
    BUNDLE_DISCOUNT = "bundle_discount"
    SHIPPING_FREE = "shipping_free"

class TestStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    DRAFT = "draft"

class TestMetric(str, Enum):
    CTR = "ctr"
    CONVERSION_RATE = "conversion_rate"
    REVENUE = "revenue"
    ENGAGEMENT = "engagement"

# Banner Models
class BannerTemplate(BaseModel):
    template_id: str = Field(default_factory=lambda: f"tpl_{uuid.uuid4().hex[:12]}")
    name: str
    category: BannerCategory
    dimensions: BannerDimensions
    template_data: Dict[str, Any] = {}  # Design elements, fonts, colors, layout
    performance_data: Dict[str, Any] = {}  # CTR, conversion rates, usage stats
    preview_url: Optional[str] = None
    is_premium: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AffiliateBanner(BaseModel):
    banner_id: str = Field(default_factory=lambda: f"ban_{uuid.uuid4().hex[:12]}")
    affiliate_id: str
    template_id: Optional[str] = None
    name: str
    custom_text: Dict[str, str] = {}  # headline, subtitle, cta, etc.
    custom_colors: Dict[str, str] = {}  # primary, secondary, accent, etc.
    custom_images: Dict[str, str] = {}  # logo, product, background
    banner_url: Optional[str] = None
    tracking_code: str
    click_count: int = 0
    impression_count: int = 0
    conversion_count: int = 0
    last_used: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# SmartLinks Models
class SmartLinkDestination(BaseModel):
    url: str
    weight: int = 100  # Traffic percentage
    geo_targets: List[str] = []  # Country codes
    device_targets: List[str] = []  # mobile, desktop, tablet
    time_targets: Dict[str, Any] = {}  # Time-based targeting
    conversion_rate: float = 0.0
    revenue_per_click: float = 0.0
    is_active: bool = True

class SmartLink(BaseModel):
    smart_link_id: str = Field(default_factory=lambda: f"sl_{uuid.uuid4().hex[:12]}")
    affiliate_id: str
    name: str
    short_code: str
    destinations: List[SmartLinkDestination] = []
    optimization_settings: Dict[str, Any] = {
        "geo_targeting": True,
        "device_optimization": True,
        "time_optimization": False,
        "learning_mode": True,
        "auto_pause_poor_performers": False
    }
    total_clicks: int = 0
    total_conversions: int = 0
    total_revenue: float = 0.0
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SmartLinkClick(BaseModel):
    click_id: str = Field(default_factory=lambda: f"clk_{uuid.uuid4().hex[:12]}")
    smart_link_id: str
    visitor_ip: str
    user_agent: str
    country_code: Optional[str] = None
    device_type: Optional[str] = None
    destination_chosen: str
    converted: bool = False
    conversion_value: float = 0.0
    clicked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# A/B Testing Models
class BannerTest(BaseModel):
    test_id: str = Field(default_factory=lambda: f"test_{uuid.uuid4().hex[:12]}")
    affiliate_id: str
    test_name: str
    control_banner_id: str
    test_banner_id: str
    traffic_split: int = 50  # Percentage for test variant
    success_metric: TestMetric = TestMetric.CTR
    status: TestStatus = TestStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_sample_size: int = 1000
    confidence_level: float = 0.95
    winner_declared: Optional[str] = None  # Banner ID that won
    statistical_significance: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BannerTestResult(BaseModel):
    result_id: str = Field(default_factory=lambda: f"res_{uuid.uuid4().hex[:12]}")
    test_id: str
    banner_id: str
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    ctr: float = 0.0
    conversion_rate: float = 0.0
    revenue_per_click: float = 0.0
    recorded_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))

# Coupon Models
class AffiliateCoupon(BaseModel):
    coupon_id: str = Field(default_factory=lambda: f"cpn_{uuid.uuid4().hex[:12]}")
    affiliate_id: str
    coupon_code: str
    coupon_type: CouponType
    discount_value: float
    minimum_order_value: Optional[float] = None
    maximum_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_count: int = 0
    customer_usage_limit: int = 1  # Per customer
    expires_at: Optional[datetime] = None
    is_active: bool = True
    auto_generated: bool = False
    generation_pattern: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CouponUsage(BaseModel):
    usage_id: str = Field(default_factory=lambda: f"use_{uuid.uuid4().hex[:12]}")
    coupon_id: str
    customer_email: str
    customer_ip: Optional[str] = None
    order_value: float
    discount_applied: float
    order_id: Optional[str] = None
    used_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Request/Response Models
class CreateBannerRequest(BaseModel):
    template_id: Optional[str] = None
    name: str
    custom_text: Dict[str, str] = {}
    custom_colors: Dict[str, str] = {}
    custom_images: Dict[str, str] = {}

class CreateSmartLinkRequest(BaseModel):
    name: str
    destinations: List[Dict[str, Any]]
    optimization_settings: Dict[str, Any] = {}

class CreateBannerTestRequest(BaseModel):
    test_name: str
    control_banner_id: str
    test_banner_id: str
    traffic_split: int = 50
    success_metric: TestMetric = TestMetric.CTR
    min_sample_size: int = 1000
    duration_days: Optional[int] = None

class CreateCouponRequest(BaseModel):
    coupon_type: CouponType
    discount_value: float
    usage_limit: Optional[int] = None
    expires_in_days: Optional[int] = None
    minimum_order_value: Optional[float] = None
    generation_pattern: str = "BRANDED"  # BRANDED, READABLE, CUSTOM

# =============================================================================
# Promotional Materials Engine
# =============================================================================

class PromotionalMaterialsEngine:
    def __init__(self):
        # Initialize database connections
        load_dotenv()
        MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
        
        client = AsyncIOMotorClient(MONGO_URL)
        self.db = client[DB_NAME]
        
        # Initialize Redis
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/4")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Initialize components
        self.banner_generator = BannerGenerator(self.db, self.redis_client)
        self.smart_links = SmartLinksManager(self.db, self.redis_client)
        self.ab_testing = ABTestingEngine(self.db, self.redis_client)
        self.coupon_manager = CouponManager(self.db, self.redis_client)
        
        # Initialize GeoIP
        self.geoip_reader = None
        try:
            import geoip2.database
            geoip_path = os.getenv("GEOIP_DATABASE_PATH", "GeoLite2-City.mmdb")
            if os.path.exists(geoip_path):
                self.geoip_reader = geoip2.database.Reader(geoip_path)
        except Exception as e:
            logging.warning(f"GeoIP database not available: {e}")

# =============================================================================
# Banner Generator System
# =============================================================================

class BannerGenerator:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client
        self.templates_collection = db.banner_templates
        self.banners_collection = db.affiliate_banners
        
    async def create_default_templates(self):
        """Create default high-converting banner templates"""
        
        default_templates = [
            {
                "name": "SaaS Professional",
                "category": BannerCategory.LEADERBOARD,
                "dimensions": BannerDimensions.LEADERBOARD_728x90,
                "template_data": {
                    "layout": "text_left_image_right",
                    "background_color": "#0066cc",
                    "text_color": "#ffffff",
                    "accent_color": "#ff6600",
                    "font_family": "Arial, sans-serif",
                    "elements": {
                        "headline": {"x": 20, "y": 20, "width": 400, "height": 30, "font_size": 24, "font_weight": "bold"},
                        "subtitle": {"x": 20, "y": 50, "width": 400, "height": 20, "font_size": 14},
                        "cta_button": {"x": 450, "y": 25, "width": 120, "height": 40, "font_size": 16, "font_weight": "bold"},
                        "logo_area": {"x": 600, "y": 10, "width": 120, "height": 70}
                    },
                    "default_text": {
                        "headline": "Boost Your Business Intelligence",
                        "subtitle": "Get 30% more insights with CustomerMindIQ",
                        "cta": "Start Free Trial"
                    }
                },
                "performance_data": {"avg_ctr": 2.1, "avg_conversion": 8.5, "usage_count": 0}
            },
            {
                "name": "Conversion Focused",
                "category": BannerCategory.SQUARE,
                "dimensions": BannerDimensions.SQUARE_300x250,
                "template_data": {
                    "layout": "centered_vertical",
                    "background_color": "#f8f9fa",
                    "text_color": "#212529",
                    "accent_color": "#28a745",
                    "font_family": "Georgia, serif",
                    "elements": {
                        "headline": {"x": 20, "y": 30, "width": 260, "height": 40, "font_size": 20, "font_weight": "bold"},
                        "subtitle": {"x": 20, "y": 80, "width": 260, "height": 60, "font_size": 14},
                        "cta_button": {"x": 75, "y": 160, "width": 150, "height": 50, "font_size": 18, "font_weight": "bold"},
                        "badge": {"x": 200, "y": 10, "width": 80, "height": 30, "font_size": 12}
                    },
                    "default_text": {
                        "headline": "Unlock Customer Insights",
                        "subtitle": "Discover what your customers really want with AI-powered analytics",
                        "cta": "Get Started",
                        "badge": "FREE TRIAL"
                    }
                },
                "performance_data": {"avg_ctr": 3.2, "avg_conversion": 12.1, "usage_count": 0}
            },
            {
                "name": "Mobile Optimized",
                "category": BannerCategory.MOBILE,
                "dimensions": BannerDimensions.MOBILE_320x100,
                "template_data": {
                    "layout": "horizontal_compact",
                    "background_color": "#6c5ce7",
                    "text_color": "#ffffff",
                    "accent_color": "#fdcb6e",
                    "font_family": "Roboto, sans-serif",
                    "elements": {
                        "headline": {"x": 10, "y": 15, "width": 200, "height": 25, "font_size": 16, "font_weight": "bold"},
                        "subtitle": {"x": 10, "y": 40, "width": 200, "height": 20, "font_size": 12},
                        "cta_button": {"x": 220, "y": 25, "width": 90, "height": 50, "font_size": 14, "font_weight": "bold"}
                    },
                    "default_text": {
                        "headline": "Customer Intelligence",
                        "subtitle": "30% Off Premium Plans",
                        "cta": "Claim Now"
                    }
                },
                "performance_data": {"avg_ctr": 4.1, "avg_conversion": 9.8, "usage_count": 0}
            }
        ]
        
        for template_data in default_templates:
            template = BannerTemplate(**template_data)
            
            # Check if template already exists
            existing = await self.templates_collection.find_one({"name": template.name})
            if not existing:
                await self.templates_collection.insert_one(template.dict())
                logging.info(f"Created default template: {template.name}")
    
    async def get_templates(self, category: Optional[BannerCategory] = None) -> List[BannerTemplate]:
        """Get available banner templates"""
        
        query = {"is_active": True}
        if category:
            query["category"] = category
            
        cursor = self.templates_collection.find(query).sort("performance_data.avg_ctr", -1)
        templates = await cursor.to_list(length=None)
        
        return [BannerTemplate(**template) for template in templates]
    
    async def create_banner(self, affiliate_id: str, banner_request: CreateBannerRequest) -> AffiliateBanner:
        """Create a customized banner for an affiliate"""
        
        # Generate tracking code
        tracking_code = f"BAN_{affiliate_id}_{secrets.token_hex(6).upper()}"
        
        # Create banner record
        banner = AffiliateBanner(
            affiliate_id=affiliate_id,
            template_id=banner_request.template_id,
            name=banner_request.name,
            custom_text=banner_request.custom_text,
            custom_colors=banner_request.custom_colors,
            custom_images=banner_request.custom_images,
            tracking_code=tracking_code
        )
        
        # Generate banner image
        banner_url = await self._generate_banner_image(banner)
        banner.banner_url = banner_url
        
        # Save to database
        await self.banners_collection.insert_one(banner.dict())
        
        return banner
    
    async def _generate_banner_image(self, banner: AffiliateBanner) -> str:
        """Generate the actual banner image using PIL"""
        
        try:
            # Get template if specified
            template = None
            if banner.template_id:
                template_data = await self.templates_collection.find_one({"template_id": banner.template_id})
                if template_data:
                    template = BannerTemplate(**template_data)
            
            if not template:
                # Use default template based on first custom dimension or default
                dimensions = list(BannerDimensions)
                default_dim = dimensions[0]
                width, height = map(int, default_dim.value.split('x'))
            else:
                width, height = map(int, template.dimensions.value.split('x'))
            
            # Create image
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Load fonts (use default if custom font not available)
            try:
                title_font = ImageFont.truetype("arial.ttf", 24)
                subtitle_font = ImageFont.truetype("arial.ttf", 14)
                cta_font = ImageFont.truetype("arial.ttf", 16)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                cta_font = ImageFont.load_default()
            
            # Apply template design or create basic design
            if template:
                bg_color = banner.custom_colors.get('background', template.template_data.get('background_color', '#0066cc'))
                text_color = banner.custom_colors.get('text', template.template_data.get('text_color', '#ffffff'))
                accent_color = banner.custom_colors.get('accent', template.template_data.get('accent_color', '#ff6600'))
            else:
                bg_color = banner.custom_colors.get('background', '#0066cc')
                text_color = banner.custom_colors.get('text', '#ffffff')
                accent_color = banner.custom_colors.get('accent', '#ff6600')
            
            # Fill background
            draw.rectangle([0, 0, width, height], fill=bg_color)
            
            # Add text elements
            headline = banner.custom_text.get('headline', 'CustomerMind IQ')
            subtitle = banner.custom_text.get('subtitle', 'AI-Powered Customer Intelligence')
            cta = banner.custom_text.get('cta', 'Learn More')
            
            # Calculate text positions (simplified layout)
            if width >= 600:  # Leaderboard layout
                draw.text((20, 20), headline, font=title_font, fill=text_color)
                draw.text((20, 50), subtitle, font=subtitle_font, fill=text_color)
                
                # CTA button
                cta_x, cta_y, cta_w, cta_h = width-150, 25, 120, 40
                draw.rectangle([cta_x, cta_y, cta_x+cta_w, cta_y+cta_h], fill=accent_color)
                
                # Center CTA text
                cta_text_width = draw.textlength(cta, font=cta_font)
                cta_text_x = cta_x + (cta_w - cta_text_width) // 2
                draw.text((cta_text_x, cta_y+10), cta, font=cta_font, fill='white')
                
            elif width >= 300:  # Square layout
                draw.text((20, 30), headline, font=title_font, fill=text_color)
                draw.text((20, 70), subtitle, font=subtitle_font, fill=text_color)
                
                # CTA button
                cta_x, cta_y, cta_w, cta_h = 75, height-80, 150, 40
                draw.rectangle([cta_x, cta_y, cta_x+cta_w, cta_y+cta_h], fill=accent_color)
                
                cta_text_width = draw.textlength(cta, font=cta_font)
                cta_text_x = cta_x + (cta_w - cta_text_width) // 2
                draw.text((cta_text_x, cta_y+10), cta, font=cta_font, fill='white')
                
            else:  # Mobile layout
                draw.text((10, 15), headline, font=subtitle_font, fill=text_color)
                draw.text((10, 40), subtitle, font=ImageFont.load_default(), fill=text_color)
                
                # CTA button
                cta_x, cta_y, cta_w, cta_h = width-100, 25, 80, 50
                draw.rectangle([cta_x, cta_y, cta_x+cta_w, cta_y+cta_h], fill=accent_color)
                
                cta_text_width = draw.textlength(cta, font=ImageFont.load_default())
                cta_text_x = cta_x + (cta_w - cta_text_width) // 2
                draw.text((cta_text_x, cta_y+15), cta, font=ImageFont.load_default(), fill='white')
            
            # Save image
            banner_filename = f"{banner.banner_id}.png"
            banner_path = f"/tmp/{banner_filename}"
            img.save(banner_path, "PNG")
            
            # In production, upload to CDN/S3 and return URL
            # For now, return a placeholder URL
            return f"/api/banners/image/{banner.banner_id}"
            
        except Exception as e:
            logging.error(f"Error generating banner image: {e}")
            return f"/api/banners/placeholder/{banner.banner_id}"
    
    async def get_affiliate_banners(self, affiliate_id: str) -> List[AffiliateBanner]:
        """Get all banners for an affiliate"""
        
        cursor = self.banners_collection.find({"affiliate_id": affiliate_id, "is_active": True}).sort("created_at", -1)
        banners = await cursor.to_list(length=None)
        
        return [AffiliateBanner(**banner) for banner in banners]
    
    async def update_banner_stats(self, banner_id: str, action: str):
        """Update banner performance statistics"""
        
        update_field = f"{action}_count"
        await self.banners_collection.update_one(
            {"banner_id": banner_id},
            {
                "$inc": {update_field: 1},
                "$set": {"last_used": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)}
            }
        )

# =============================================================================
# SmartLinks System
# =============================================================================

class SmartLinksManager:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client
        self.smart_links_collection = db.smart_links
        self.clicks_collection = db.smart_link_clicks
        
    async def create_smart_link(self, affiliate_id: str, request: CreateSmartLinkRequest) -> SmartLink:
        """Create a new SmartLink with optimization"""
        
        # Generate unique short code
        short_code = self._generate_short_code()
        while await self._short_code_exists(short_code):
            short_code = self._generate_short_code()
        
        # Process destinations
        destinations = [SmartLinkDestination(**dest) for dest in request.destinations]
        
        # Create SmartLink
        smart_link = SmartLink(
            affiliate_id=affiliate_id,
            name=request.name,
            short_code=short_code,
            destinations=destinations,
            optimization_settings=request.optimization_settings
        )
        
        # Save to database
        await self.smart_links_collection.insert_one(smart_link.dict())
        
        return smart_link
    
    def _generate_short_code(self) -> str:
        """Generate a short, URL-safe code"""
        return secrets.token_urlsafe(6)[:8].upper()
    
    async def _short_code_exists(self, short_code: str) -> bool:
        """Check if short code already exists"""
        existing = await self.smart_links_collection.find_one({"short_code": short_code})
        return existing is not None
    
    async def route_visitor(self, short_code: str, visitor_ip: str, user_agent: str) -> tuple[str, SmartLinkClick]:
        """Intelligent routing based on visitor characteristics"""
        
        # Get SmartLink
        smart_link_data = await self.smart_links_collection.find_one({"short_code": short_code, "is_active": True})
        if not smart_link_data:
            raise HTTPException(status_code=404, detail="SmartLink not found")
        
        smart_link = SmartLink(**smart_link_data)
        
        # Analyze visitor
        visitor_info = await self._analyze_visitor(visitor_ip, user_agent)
        
        # Select best destination
        best_destination = await self._select_best_destination(smart_link, visitor_info)
        
        # Log click
        click = SmartLinkClick(
            smart_link_id=smart_link.smart_link_id,
            visitor_ip=visitor_ip,
            user_agent=user_agent,
            country_code=visitor_info.get("country"),
            device_type=visitor_info.get("device_type"),
            destination_chosen=best_destination.url
        )
        
        await self.clicks_collection.insert_one(click.dict())
        
        # Update SmartLink statistics
        await self.smart_links_collection.update_one(
            {"smart_link_id": smart_link.smart_link_id},
            {
                "$inc": {"total_clicks": 1},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )
        
        return best_destination.url, click
    
    async def _analyze_visitor(self, visitor_ip: str, user_agent: str) -> Dict[str, Any]:
        """Analyze visitor characteristics for routing"""
        
        visitor_info = {}
        
        # Device detection
        try:
            ua = user_agents.parse(user_agent)
            if ua.is_mobile:
                visitor_info["device_type"] = "mobile"
            elif ua.is_tablet:
                visitor_info["device_type"] = "tablet"
            else:
                visitor_info["device_type"] = "desktop"
            
            visitor_info["browser"] = ua.browser.family
            visitor_info["os"] = ua.os.family
        except:
            visitor_info["device_type"] = "unknown"
        
        # Geographic detection (simplified - would use GeoIP in production)
        try:
            # Placeholder for GeoIP lookup
            visitor_info["country"] = "US"  # Default
            visitor_info["region"] = "Unknown"
        except:
            visitor_info["country"] = "Unknown"
        
        # Time-based info
        current_time = datetime.now(timezone.utc)
        visitor_info["hour"] = current_time.hour
        visitor_info["day_of_week"] = current_time.weekday()
        
        return visitor_info
    
    async def _select_best_destination(self, smart_link: SmartLink, visitor_info: Dict[str, Any]) -> SmartLinkDestination:
        """Select the best destination based on optimization rules and performance"""
        
        eligible_destinations = []
        
        for destination in smart_link.destinations:
            if not destination.is_active:
                continue
            
            # Check geographic targeting
            if destination.geo_targets and visitor_info.get("country") not in destination.geo_targets:
                continue
            
            # Check device targeting
            if destination.device_targets and visitor_info.get("device_type") not in destination.device_targets:
                continue
            
            # Check time targeting (simplified)
            # Add more complex time-based logic here
            
            eligible_destinations.append(destination)
        
        if not eligible_destinations:
            # Fallback to first available destination
            eligible_destinations = [dest for dest in smart_link.destinations if dest.is_active]
        
        if not eligible_destinations:
            raise HTTPException(status_code=503, detail="No available destinations")
        
        # Select based on performance and weights
        if smart_link.optimization_settings.get("learning_mode", True):
            # Use performance-based selection (simplified)
            best_destination = max(eligible_destinations, key=lambda d: d.conversion_rate * d.weight)
        else:
            # Use weighted random selection
            import random
            weights = [dest.weight for dest in eligible_destinations]
            best_destination = random.choices(eligible_destinations, weights=weights, k=1)[0]
        
        return best_destination
    
    async def update_conversion(self, click_id: str, conversion_value: float):
        """Update click with conversion data"""
        
        await self.clicks_collection.update_one(
            {"click_id": click_id},
            {
                "$set": {
                    "converted": True,
                    "conversion_value": conversion_value
                }
            }
        )
        
        # Update SmartLink statistics
        click_data = await self.clicks_collection.find_one({"click_id": click_id})
        if click_data:
            await self.smart_links_collection.update_one(
                {"smart_link_id": click_data["smart_link_id"]},
                {
                    "$inc": {
                        "total_conversions": 1,
                        "total_revenue": conversion_value
                    }
                }
            )
    
    async def get_affiliate_smart_links(self, affiliate_id: str) -> List[SmartLink]:
        """Get all SmartLinks for an affiliate"""
        
        cursor = self.smart_links_collection.find({"affiliate_id": affiliate_id, "is_active": True}).sort("created_at", -1)
        smart_links = await cursor.to_list(length=None)
        
        return [SmartLink(**link) for link in smart_links]

# =============================================================================
# A/B Testing Engine
# =============================================================================

class ABTestingEngine:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client
        self.tests_collection = db.banner_tests
        self.results_collection = db.banner_test_results
        
    async def create_banner_test(self, affiliate_id: str, request: CreateBannerTestRequest) -> BannerTest:
        """Create a new A/B test for banners"""
        
        # Validate banners exist
        banners_collection = self.db.affiliate_banners
        control_banner = await banners_collection.find_one({"banner_id": request.control_banner_id, "affiliate_id": affiliate_id})
        test_banner = await banners_collection.find_one({"banner_id": request.test_banner_id, "affiliate_id": affiliate_id})
        
        if not control_banner or not test_banner:
            raise HTTPException(status_code=404, detail="One or both banners not found")
        
        # Create test
        banner_test = BannerTest(
            affiliate_id=affiliate_id,
            test_name=request.test_name,
            control_banner_id=request.control_banner_id,
            test_banner_id=request.test_banner_id,
            traffic_split=request.traffic_split,
            success_metric=request.success_metric,
            min_sample_size=request.min_sample_size
        )
        
        # Set end date if duration specified
        if request.duration_days:
            banner_test.end_date = datetime.now(timezone.utc) + timedelta(days=request.duration_days)
        
        await self.tests_collection.insert_one(banner_test.dict())
        
        return banner_test
    
    async def start_test(self, test_id: str):
        """Start an A/B test"""
        
        await self.tests_collection.update_one(
            {"test_id": test_id},
            {
                "$set": {
                    "status": TestStatus.ACTIVE,
                    "start_date": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
    
    async def assign_banner_variant(self, test_id: str, session_id: str) -> str:
        """Assign a banner variant to a visitor"""
        
        test_data = await self.tests_collection.find_one({"test_id": test_id, "status": TestStatus.ACTIVE})
        if not test_data:
            raise HTTPException(status_code=404, detail="Active test not found")
        
        test = BannerTest(**test_data)
        
        # Consistent assignment based on session
        hash_input = f"{test_id}_{session_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        # Split traffic based on test settings
        if (hash_value % 100) < test.traffic_split:
            return test.test_banner_id
        else:
            return test.control_banner_id
    
    async def record_interaction(self, test_id: str, banner_id: str, interaction_type: str, value: float = 0.0):
        """Record banner interaction (impression, click, conversion)"""
        
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Get or create today's results record
        result_data = await self.results_collection.find_one({
            "test_id": test_id,
            "banner_id": banner_id,
            "recorded_date": today
        })
        
        if not result_data:
            result = BannerTestResult(
                test_id=test_id,
                banner_id=banner_id,
                recorded_date=today
            )
            await self.results_collection.insert_one(result.dict())
        
        # Update counts
        update_field = {}
        if interaction_type == "impression":
            update_field["impressions"] = 1
        elif interaction_type == "click":
            update_field["clicks"] = 1
        elif interaction_type == "conversion":
            update_field["conversions"] = 1
            update_field["revenue"] = value
        
        if update_field:
            await self.results_collection.update_one(
                {"test_id": test_id, "banner_id": banner_id, "recorded_date": today},
                {"$inc": update_field}
            )
            
            # Recalculate derived metrics
            await self._update_derived_metrics(test_id, banner_id, today)
    
    async def _update_derived_metrics(self, test_id: str, banner_id: str, date: datetime):
        """Update calculated metrics like CTR, conversion rate"""
        
        result_data = await self.results_collection.find_one({
            "test_id": test_id,
            "banner_id": banner_id,
            "recorded_date": date
        })
        
        if result_data:
            impressions = result_data.get("impressions", 0)
            clicks = result_data.get("clicks", 0)
            conversions = result_data.get("conversions", 0)
            revenue = result_data.get("revenue", 0.0)
            
            # Calculate metrics
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
            revenue_per_click = (revenue / clicks) if clicks > 0 else 0
            
            await self.results_collection.update_one(
                {"test_id": test_id, "banner_id": banner_id, "recorded_date": date},
                {
                    "$set": {
                        "ctr": ctr,
                        "conversion_rate": conversion_rate,
                        "revenue_per_click": revenue_per_click
                    }
                }
            )
    
    async def calculate_test_significance(self, test_id: str) -> Dict[str, Any]:
        """Calculate statistical significance of A/B test results"""
        
        test_data = await self.tests_collection.find_one({"test_id": test_id})
        if not test_data:
            raise HTTPException(status_code=404, detail="Test not found")
        
        test = BannerTest(**test_data)
        
        # Get aggregated results for both variants
        control_results = await self._get_aggregated_results(test_id, test.control_banner_id)
        test_results = await self._get_aggregated_results(test_id, test.test_banner_id)
        
        # Calculate significance (simplified z-test)
        significance_data = self._calculate_significance(
            control_results, test_results, test.success_metric
        )
        
        # Check if we should declare a winner
        if (significance_data["p_value"] < 0.05 and 
            min(control_results["sample_size"], test_results["sample_size"]) >= test.min_sample_size):
            
            winner_banner_id = test.test_banner_id if significance_data["test_is_better"] else test.control_banner_id
            
            await self.tests_collection.update_one(
                {"test_id": test_id},
                {
                    "$set": {
                        "winner_declared": winner_banner_id,
                        "statistical_significance": significance_data["confidence"],
                        "status": TestStatus.COMPLETED,
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
        
        return {
            "test_id": test_id,
            "control_results": control_results,
            "test_results": test_results,
            "significance": significance_data,
            "winner": test_data.get("winner_declared")
        }
    
    async def _get_aggregated_results(self, test_id: str, banner_id: str) -> Dict[str, Any]:
        """Get aggregated results for a banner variant"""
        
        cursor = self.results_collection.find({"test_id": test_id, "banner_id": banner_id})
        results = await cursor.to_list(length=None)
        
        total_impressions = sum(r.get("impressions", 0) for r in results)
        total_clicks = sum(r.get("clicks", 0) for r in results)
        total_conversions = sum(r.get("conversions", 0) for r in results)
        total_revenue = sum(r.get("revenue", 0.0) for r in results)
        
        return {
            "banner_id": banner_id,
            "sample_size": total_impressions,
            "clicks": total_clicks,
            "conversions": total_conversions,
            "revenue": total_revenue,
            "ctr": (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
            "conversion_rate": (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
            "revenue_per_click": (total_revenue / total_clicks) if total_clicks > 0 else 0
        }
    
    def _calculate_significance(self, control_data: Dict, test_data: Dict, metric: TestMetric) -> Dict[str, Any]:
        """Calculate statistical significance (simplified)"""
        
        # This is a simplified calculation. In production, use proper statistical libraries
        import math
        
        if metric == TestMetric.CTR:
            control_rate = control_data["ctr"] / 100
            test_rate = test_data["ctr"] / 100
            control_n = control_data["sample_size"]
            test_n = test_data["sample_size"]
        elif metric == TestMetric.CONVERSION_RATE:
            control_rate = control_data["conversion_rate"] / 100
            test_rate = test_data["conversion_rate"] / 100
            control_n = control_data["clicks"]
            test_n = test_data["clicks"]
        else:
            # Revenue per click
            control_rate = control_data["revenue_per_click"]
            test_rate = test_data["revenue_per_click"]
            control_n = control_data["clicks"]
            test_n = test_data["clicks"]
        
        if control_n == 0 or test_n == 0:
            return {
                "p_value": 1.0,
                "confidence": 0.0,
                "test_is_better": False,
                "improvement": 0.0
            }
        
        # Simple z-test calculation
        pooled_rate = (control_rate * control_n + test_rate * test_n) / (control_n + test_n)
        se = math.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_n + 1/test_n))
        
        if se == 0:
            z_score = 0
        else:
            z_score = abs(test_rate - control_rate) / se
        
        # Convert to p-value (simplified)
        p_value = 2 * (1 - 0.5 * (1 + math.erf(z_score / math.sqrt(2))))
        confidence = 1 - p_value
        
        improvement = ((test_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
        
        return {
            "p_value": p_value,
            "confidence": confidence,
            "test_is_better": test_rate > control_rate,
            "improvement": improvement,
            "z_score": z_score
        }
    
    async def get_affiliate_tests(self, affiliate_id: str) -> List[BannerTest]:
        """Get all A/B tests for an affiliate"""
        
        cursor = self.tests_collection.find({"affiliate_id": affiliate_id}).sort("created_at", -1)
        tests = await cursor.to_list(length=None)
        
        return [BannerTest(**test) for test in tests]

# =============================================================================
# Coupon Management System
# =============================================================================

class CouponManager:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client
        self.coupons_collection = db.affiliate_coupons
        self.usage_collection = db.coupon_usage
        
    async def create_coupon(self, affiliate_id: str, request: CreateCouponRequest) -> AffiliateCoupon:
        """Create a new coupon for an affiliate"""
        
        # Generate coupon code
        coupon_code = self._generate_coupon_code(affiliate_id, request.generation_pattern, request.coupon_type, request.discount_value)
        
        # Ensure uniqueness
        while await self._coupon_code_exists(coupon_code):
            coupon_code = self._generate_coupon_code(affiliate_id, request.generation_pattern, request.coupon_type, request.discount_value)
        
        # Set expiration
        expires_at = None
        if request.expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=request.expires_in_days)
        
        # Create coupon
        coupon = AffiliateCoupon(
            affiliate_id=affiliate_id,
            coupon_code=coupon_code,
            coupon_type=request.coupon_type,
            discount_value=request.discount_value,
            minimum_order_value=request.minimum_order_value,
            usage_limit=request.usage_limit,
            expires_at=expires_at,
            auto_generated=True,
            generation_pattern=request.generation_pattern
        )
        
        await self.coupons_collection.insert_one(coupon.dict())
        
        return coupon
    
    def _generate_coupon_code(self, affiliate_id: str, pattern: str, coupon_type: CouponType, discount_value: float) -> str:
        """Generate coupon code based on pattern"""
        
        if pattern == "BRANDED":
            # CMIQ-AFF123-20OFF
            suffix = f"{int(discount_value)}OFF" if coupon_type == CouponType.PERCENTAGE else f"{int(discount_value)}USD"
            return f"CMIQ-AFF{affiliate_id[-6:]}-{suffix}"
            
        elif pattern == "READABLE":
            # SAVE20NOW, TRIAL30FREE
            action_words = ["SAVE", "GET", "CLAIM", "USE"]
            urgency_words = ["NOW", "TODAY", "FAST", "LIMITED"]
            
            action = secrets.choice(action_words)
            urgency = secrets.choice(urgency_words)
            
            if coupon_type == CouponType.PERCENTAGE:
                return f"{action}{int(discount_value)}{urgency}"
            elif coupon_type == CouponType.FREE_TRIAL:
                return f"TRIAL{int(discount_value)}FREE"
            else:
                return f"{action}{int(discount_value)}USD{urgency}"
                
        elif pattern == "SIMPLE":
            # Simple alphanumeric code
            return f"SAVE{secrets.token_hex(4).upper()}"
            
        else:
            # Default random pattern
            return f"CMIQ{secrets.token_hex(6).upper()}"
    
    async def _coupon_code_exists(self, coupon_code: str) -> bool:
        """Check if coupon code already exists"""
        existing = await self.coupons_collection.find_one({"coupon_code": coupon_code})
        return existing is not None
    
    async def validate_coupon(self, coupon_code: str, customer_email: str, order_value: float) -> Dict[str, Any]:
        """Validate coupon and calculate discount"""
        
        # Get coupon
        coupon_data = await self.coupons_collection.find_one({"coupon_code": coupon_code, "is_active": True})
        if not coupon_data:
            return {"valid": False, "error": "Coupon not found"}
        
        coupon = AffiliateCoupon(**coupon_data)
        
        # Check expiration
        if coupon.expires_at and datetime.now(timezone.utc) > coupon.expires_at:
            return {"valid": False, "error": "Coupon has expired"}
        
        # Check usage limits
        if coupon.usage_limit and coupon.usage_count >= coupon.usage_limit:
            return {"valid": False, "error": "Coupon usage limit exceeded"}
        
        # Check customer usage
        customer_usage = await self.usage_collection.count_documents({
            "coupon_id": coupon.coupon_id,
            "customer_email": customer_email
        })
        
        if customer_usage >= coupon.customer_usage_limit:
            return {"valid": False, "error": "Customer usage limit exceeded"}
        
        # Check minimum order value
        if coupon.minimum_order_value and order_value < coupon.minimum_order_value:
            return {
                "valid": False, 
                "error": f"Minimum order value of ${coupon.minimum_order_value} required"
            }
        
        # Calculate discount
        discount_amount = self._calculate_discount(coupon, order_value)
        
        return {
            "valid": True,
            "coupon_id": coupon.coupon_id,
            "discount_amount": discount_amount,
            "coupon_type": coupon.coupon_type,
            "affiliate_id": coupon.affiliate_id
        }
    
    def _calculate_discount(self, coupon: AffiliateCoupon, order_value: float) -> float:
        """Calculate discount amount"""
        
        if coupon.coupon_type == CouponType.PERCENTAGE:
            discount = order_value * (coupon.discount_value / 100)
        elif coupon.coupon_type == CouponType.FIXED_AMOUNT:
            discount = coupon.discount_value
        elif coupon.coupon_type == CouponType.FREE_TRIAL:
            # For free trial, return the trial value
            discount = coupon.discount_value
        else:
            discount = 0.0
        
        # Apply maximum discount limit if set
        if coupon.maximum_discount_amount:
            discount = min(discount, coupon.maximum_discount_amount)
        
        # Discount cannot exceed order value
        discount = min(discount, order_value)
        
        return round(discount, 2)
    
    async def apply_coupon(self, coupon_id: str, customer_email: str, order_value: float, order_id: str = None, customer_ip: str = None) -> CouponUsage:
        """Apply coupon and record usage"""
        
        # Get coupon
        coupon_data = await self.coupons_collection.find_one({"coupon_id": coupon_id})
        if not coupon_data:
            raise HTTPException(status_code=404, detail="Coupon not found")
        
        coupon = AffiliateCoupon(**coupon_data)
        
        # Calculate discount
        discount_amount = self._calculate_discount(coupon, order_value)
        
        # Create usage record
        usage = CouponUsage(
            coupon_id=coupon_id,
            customer_email=customer_email,
            customer_ip=customer_ip,
            order_value=order_value,
            discount_applied=discount_amount,
            order_id=order_id
        )
        
        await self.usage_collection.insert_one(usage.dict())
        
        # Update coupon usage count
        await self.coupons_collection.update_one(
            {"coupon_id": coupon_id},
            {
                "$inc": {"usage_count": 1},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )
        
        return usage
    
    async def get_affiliate_coupons(self, affiliate_id: str, include_inactive: bool = False) -> List[AffiliateCoupon]:
        """Get all coupons for an affiliate"""
        
        query = {"affiliate_id": affiliate_id}
        if not include_inactive:
            query["is_active"] = True
            
        cursor = self.coupons_collection.find(query).sort("created_at", -1)
        coupons = await cursor.to_list(length=None)
        
        return [AffiliateCoupon(**coupon) for coupon in coupons]
    
    async def get_coupon_analytics(self, affiliate_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get coupon performance analytics"""
        
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        
        # Get affiliate's coupons
        coupons_cursor = self.coupons_collection.find({"affiliate_id": affiliate_id})
        coupons = await coupons_cursor.to_list(length=None)
        coupon_ids = [c["coupon_id"] for c in coupons]
        
        # Get usage data
        usage_cursor = self.usage_collection.find({
            "coupon_id": {"$in": coupon_ids},
            "used_at": {"$gte": cutoff_date}
        })
        usage_data = await usage_cursor.to_list(length=None)
        
        # Calculate analytics
        total_usage = len(usage_data)
        total_discount = sum(u["discount_applied"] for u in usage_data)
        total_order_value = sum(u["order_value"] for u in usage_data)
        
        # Coupon performance
        coupon_performance = {}
        for usage in usage_data:
            coupon_id = usage["coupon_id"]
            if coupon_id not in coupon_performance:
                coupon_performance[coupon_id] = {
                    "usage_count": 0,
                    "total_discount": 0.0,
                    "total_order_value": 0.0
                }
            
            coupon_performance[coupon_id]["usage_count"] += 1
            coupon_performance[coupon_id]["total_discount"] += usage["discount_applied"]
            coupon_performance[coupon_id]["total_order_value"] += usage["order_value"]
        
        return {
            "period_days": days_back,
            "total_coupons": len(coupons),
            "total_usage": total_usage,
            "total_discount_given": total_discount,
            "total_order_value": total_order_value,
            "average_discount_per_use": total_discount / total_usage if total_usage > 0 else 0,
            "coupon_performance": coupon_performance
        }

# Initialize the promotional materials engine
promo_engine = PromotionalMaterialsEngine()

# =============================================================================
# FastAPI Router
# =============================================================================

router = APIRouter(prefix="/api/promotional", tags=["Promotional Materials System"])

# =============================================================================
# Banner Generator Endpoints
# =============================================================================

@router.get("/banners/templates")
async def get_banner_templates(
    category: Optional[BannerCategory] = Query(None),
    current_user: UserProfile = Depends(get_current_user)
):
    """Get available banner templates"""
    try:
        templates = await promo_engine.banner_generator.get_templates(category)
        return {
            "success": True,
            "templates": [template.dict() for template in templates],
            "total_count": len(templates)
        }
    except Exception as e:
        logging.error(f"Error getting banner templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/banners/create")
async def create_banner(
    banner_request: CreateBannerRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create a custom banner for affiliate"""
    try:
        # Use user ID as affiliate ID for now
        affiliate_id = current_user.user_id
        
        banner = await promo_engine.banner_generator.create_banner(affiliate_id, banner_request)
        
        return {
            "success": True,
            "banner": banner.dict(),
            "message": f"Banner '{banner.name}' created successfully"
        }
    except Exception as e:
        logging.error(f"Error creating banner: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/banners/my-banners")
async def get_my_banners(current_user: UserProfile = Depends(get_current_user)):
    """Get all banners for current affiliate"""
    try:
        affiliate_id = current_user.user_id
        banners = await promo_engine.banner_generator.get_affiliate_banners(affiliate_id)
        
        return {
            "success": True,
            "banners": [banner.dict() for banner in banners],
            "total_count": len(banners)
        }
    except Exception as e:
        logging.error(f"Error getting affiliate banners: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/banners/image/{banner_id}")
async def get_banner_image(banner_id: str):
    """Serve banner image"""
    try:
        # In production, this would serve from CDN/S3
        # For now, return a placeholder response
        return {
            "success": True,
            "message": "Banner image endpoint",
            "banner_id": banner_id,
            "url": f"/static/banners/{banner_id}.png"
        }
    except Exception as e:
        logging.error(f"Error serving banner image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# SmartLinks Endpoints
# =============================================================================

@router.post("/smartlinks/create")
async def create_smart_link(
    request: CreateSmartLinkRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create a new SmartLink"""
    try:
        affiliate_id = current_user.user_id
        smart_link = await promo_engine.smart_links.create_smart_link(affiliate_id, request)
        
        return {
            "success": True,
            "smart_link": smart_link.dict(),
            "short_url": f"/api/sl/{smart_link.short_code}",
            "message": f"SmartLink '{smart_link.name}' created successfully"
        }
    except Exception as e:
        logging.error(f"Error creating SmartLink: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/smartlinks/my-links")
async def get_my_smart_links(current_user: UserProfile = Depends(get_current_user)):
    """Get all SmartLinks for current affiliate"""
    try:
        affiliate_id = current_user.user_id
        smart_links = await promo_engine.smart_links.get_affiliate_smart_links(affiliate_id)
        
        return {
            "success": True,
            "smart_links": [link.dict() for link in smart_links],
            "total_count": len(smart_links)
        }
    except Exception as e:
        logging.error(f"Error getting SmartLinks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sl/{short_code}")
async def redirect_smart_link(short_code: str, request):
    """SmartLink redirect endpoint"""
    try:
        visitor_ip = request.client.host if request.client else "127.0.0.1"
        user_agent = request.headers.get("user-agent", "")
        
        destination_url, click = await promo_engine.smart_links.route_visitor(short_code, visitor_ip, user_agent)
        
        return RedirectResponse(url=destination_url, status_code=302)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in SmartLink redirect: {e}")
        raise HTTPException(status_code=500, detail="SmartLink routing error")

@router.post("/smartlinks/conversion/{click_id}")
async def record_smartlink_conversion(
    click_id: str,
    conversion_value: float,
    current_user: UserProfile = Depends(get_current_user)
):
    """Record a conversion for a SmartLink click"""
    try:
        await promo_engine.smart_links.update_conversion(click_id, conversion_value)
        
        return {
            "success": True,
            "message": "Conversion recorded successfully",
            "click_id": click_id,
            "conversion_value": conversion_value
        }
    except Exception as e:
        logging.error(f"Error recording SmartLink conversion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# A/B Testing Endpoints
# =============================================================================

@router.post("/ab-testing/create")
async def create_banner_test(
    request: CreateBannerTestRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create a new A/B test for banners"""
    try:
        affiliate_id = current_user.user_id
        banner_test = await promo_engine.ab_testing.create_banner_test(affiliate_id, request)
        
        return {
            "success": True,
            "test": banner_test.dict(),
            "message": f"A/B test '{banner_test.test_name}' created successfully"
        }
    except Exception as e:
        logging.error(f"Error creating banner test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ab-testing/{test_id}/start")
async def start_banner_test(
    test_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Start an A/B test"""
    try:
        await promo_engine.ab_testing.start_test(test_id)
        
        return {
            "success": True,
            "message": f"A/B test {test_id} started successfully"
        }
    except Exception as e:
        logging.error(f"Error starting banner test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ab-testing/{test_id}/banner")
async def get_test_banner_variant(test_id: str, session_id: str = Query(...)):
    """Get banner variant for a visitor session"""
    try:
        banner_id = await promo_engine.ab_testing.assign_banner_variant(test_id, session_id)
        
        return {
            "success": True,
            "banner_id": banner_id,
            "test_id": test_id,
            "session_id": session_id
        }
    except Exception as e:
        logging.error(f"Error getting banner variant: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ab-testing/{test_id}/interaction")
async def record_banner_interaction(
    test_id: str,
    banner_id: str,
    interaction_type: str,
    value: float = 0.0
):
    """Record banner interaction (impression, click, conversion)"""
    try:
        await promo_engine.ab_testing.record_interaction(test_id, banner_id, interaction_type, value)
        
        return {
            "success": True,
            "message": f"Interaction '{interaction_type}' recorded successfully"
        }
    except Exception as e:
        logging.error(f"Error recording banner interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ab-testing/{test_id}/results")
async def get_test_results(
    test_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Get A/B test results and significance"""
    try:
        results = await promo_engine.ab_testing.calculate_test_significance(test_id)
        
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        logging.error(f"Error getting test results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ab-testing/my-tests")
async def get_my_tests(current_user: UserProfile = Depends(get_current_user)):
    """Get all A/B tests for current affiliate"""
    try:
        affiliate_id = current_user.user_id
        tests = await promo_engine.ab_testing.get_affiliate_tests(affiliate_id)
        
        return {
            "success": True,
            "tests": [test.dict() for test in tests],
            "total_count": len(tests)
        }
    except Exception as e:
        logging.error(f"Error getting affiliate tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# Coupon Management Endpoints
# =============================================================================

@router.post("/coupons/create")
async def create_coupon(
    request: CreateCouponRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create a new coupon for affiliate"""
    try:
        affiliate_id = current_user.user_id
        coupon = await promo_engine.coupon_manager.create_coupon(affiliate_id, request)
        
        return {
            "success": True,
            "coupon": coupon.dict(),
            "message": f"Coupon '{coupon.coupon_code}' created successfully"
        }
    except Exception as e:
        logging.error(f"Error creating coupon: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coupons/validate/{coupon_code}")
async def validate_coupon(
    coupon_code: str,
    customer_email: EmailStr,
    order_value: float
):
    """Validate a coupon code"""
    try:
        validation_result = await promo_engine.coupon_manager.validate_coupon(
            coupon_code, customer_email, order_value
        )
        
        return {
            "success": True,
            "validation": validation_result
        }
    except Exception as e:
        logging.error(f"Error validating coupon: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/coupons/apply")
async def apply_coupon(
    coupon_id: str,
    customer_email: EmailStr,
    order_value: float,
    order_id: Optional[str] = None,
    customer_ip: Optional[str] = None
):
    """Apply a coupon and record usage"""
    try:
        usage = await promo_engine.coupon_manager.apply_coupon(
            coupon_id, customer_email, order_value, order_id, customer_ip
        )
        
        return {
            "success": True,
            "usage": usage.dict(),
            "message": "Coupon applied successfully"
        }
    except Exception as e:
        logging.error(f"Error applying coupon: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coupons/my-coupons")
async def get_my_coupons(
    current_user: UserProfile = Depends(get_current_user),
    include_inactive: bool = Query(False)
):
    """Get all coupons for current affiliate"""
    try:
        affiliate_id = current_user.user_id
        coupons = await promo_engine.coupon_manager.get_affiliate_coupons(affiliate_id, include_inactive)
        
        return {
            "success": True,
            "coupons": [coupon.dict() for coupon in coupons],
            "total_count": len(coupons)
        }
    except Exception as e:
        logging.error(f"Error getting affiliate coupons: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coupons/analytics")
async def get_coupon_analytics(
    current_user: UserProfile = Depends(get_current_user),
    days_back: int = Query(30, ge=1, le=365)
):
    """Get coupon performance analytics"""
    try:
        affiliate_id = current_user.user_id
        analytics = await promo_engine.coupon_manager.get_coupon_analytics(affiliate_id, days_back)
        
        return {
            "success": True,
            "analytics": analytics
        }
    except Exception as e:
        logging.error(f"Error getting coupon analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# System Administration Endpoints
# =============================================================================

@router.post("/admin/initialize-templates")
async def initialize_default_templates(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Initialize default banner templates (Admin only)"""
    try:
        await promo_engine.banner_generator.create_default_templates()
        
        return {
            "success": True,
            "message": "Default banner templates initialized successfully"
        }
    except Exception as e:
        logging.error(f"Error initializing templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def promotional_health_check():
    """Health check for promotional materials system"""
    
    try:
        # Check MongoDB connection
        await promo_engine.db.command("ping")
        mongodb_status = "healthy"
    except:
        mongodb_status = "unhealthy"
    
    try:
        # Check Redis connection
        await promo_engine.redis_client.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy" if mongodb_status == "healthy" and redis_status == "healthy" else "degraded",
        "components": {
            "mongodb": mongodb_status,
            "redis": redis_status,
            "banner_generator": "healthy",
            "smart_links": "healthy",
            "ab_testing": "healthy",
            "coupon_manager": "healthy"
        },
        "features": [
            "banner_generator",
            "smart_links_optimization",
            "ab_testing_engine",
            "coupon_management",
            "fraud_prevention",
            "performance_analytics"
        ]
    }

# Initialize default templates on startup
async def initialize_system():
    """Initialize promotional materials system"""
    try:
        await promo_engine.banner_generator.create_default_templates()
        logging.info("✅ Promotional Materials System initialized successfully")
    except Exception as e:
        logging.error(f"❌ Failed to initialize promotional materials system: {e}")

# Run initialization
asyncio.create_task(initialize_system())