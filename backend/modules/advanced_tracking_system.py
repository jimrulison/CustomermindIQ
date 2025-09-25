# Advanced Multi-Method Tracking System
# Ensures no lost conversions through multiple tracking methods

from fastapi import APIRouter, Request, Response, HTTPException, Header, Depends
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Dict, List, Any, Union
import httpx
import hashlib
import hmac
import json
import asyncio
import uuid
import ipaddress
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, parse_qs
import user_agents
import asyncpg
import redis.asyncio as redis
from cryptography.fernet import Fernet
import base64
import os
from enum import Enum
import logging
from motor.motor_asyncio import AsyncIOMotorClient

# Import existing auth system
from auth.auth_system import get_current_user, UserProfile, require_role, UserRole

# =============================================================================
# Configuration and Models
# =============================================================================

class TrackingMethod(str, Enum):
    COOKIE = "cookie"
    IP_TRACKING = "ip_tracking"  
    EMAIL_TRACKING = "email_tracking"
    FINGERPRINT = "fingerprint"
    DIRECT_LINK = "direct_link"
    POSTBACK_URL = "postback_url"
    SERVER_TO_SERVER = "s2s"
    PIXEL_TRACKING = "pixel"

class TrackingEvent(str, Enum):
    CLICK = "click"
    VIEW = "view" 
    LEAD = "lead"
    SALE = "sale"
    EMAIL_OPEN = "email_open"
    EMAIL_CLICK = "email_click"

class FraudRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"

class TrackingData(BaseModel):
    tracking_id: str
    affiliate_id: str
    site_id: str
    customer_id: Optional[str] = None
    session_id: str
    ip_address: str
    user_agent: str
    referrer: Optional[str] = None
    
    # Browser fingerprint data
    screen_resolution: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    platform: Optional[str] = None
    
    # Attribution data
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    
    # Geolocation
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    
    # Fraud detection
    fraud_score: float = 0.0
    fraud_flags: List[str] = []
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @validator('ip_address')
    def validate_ip(cls, v):
        try:
            ipaddress.ip_address(v)
            return v
        except ValueError:
            raise ValueError('Invalid IP address')

class ConversionData(BaseModel):
    conversion_id: str
    tracking_id: Optional[str] = None
    affiliate_id: str
    site_id: str
    customer_email: Optional[EmailStr] = None
    customer_id: Optional[str] = None
    
    # Conversion details
    event_type: TrackingEvent
    conversion_value: float = 0.0
    currency: str = "USD"
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    order_id: Optional[str] = None
    
    # Attribution chain
    attribution_methods: List[TrackingMethod] = []
    attribution_data: Dict[str, Any] = {}
    first_click_data: Optional[Dict] = None
    last_click_data: Optional[Dict] = None
    
    # Timing
    time_to_conversion: Optional[int] = None  # seconds
    conversion_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Fraud assessment
    fraud_risk: FraudRiskLevel = FraudRiskLevel.LOW
    fraud_details: Dict[str, Any] = {}

class BrowserFingerprint(BaseModel):
    fingerprint_hash: str
    screen_resolution: str
    timezone: str
    language: str
    platform: str
    user_agent: str
    canvas_fingerprint: Optional[str] = None
    webgl_fingerprint: Optional[str] = None
    audio_fingerprint: Optional[str] = None
    
    @classmethod
    def generate_fingerprint(cls, data: Dict[str, Any]) -> str:
        """Generate unique browser fingerprint hash"""
        fingerprint_string = f"{data.get('screen_resolution', '')}" \
                           f"{data.get('timezone', '')}" \
                           f"{data.get('language', '')}" \
                           f"{data.get('platform', '')}" \
                           f"{data.get('user_agent', '')}" \
                           f"{data.get('canvas_fingerprint', '')}" \
                           f"{data.get('webgl_fingerprint', '')}"
        
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()

# Request/Response Models
class TrackClickRequest(BaseModel):
    affiliate_id: str
    site_id: str = "main_site"
    campaign_id: Optional[str] = None
    fingerprint_data: Optional[Dict[str, Any]] = {}

class TrackConversionRequest(BaseModel):
    affiliate_id: str
    site_id: str = "main_site"
    customer_email: Optional[EmailStr] = None
    customer_id: Optional[str] = None
    event_type: TrackingEvent = TrackingEvent.SALE
    conversion_value: float = 0.0
    currency: str = "USD"
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    order_id: Optional[str] = None
    custom_data: Dict[str, Any] = {}

# =============================================================================
# Advanced Tracking Engine
# =============================================================================

class AdvancedTrackingEngine:
    def __init__(self):
        # Use existing MongoDB connection
        from dotenv import load_dotenv
        load_dotenv()
        
        MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
        
        client = AsyncIOMotorClient(MONGO_URL)
        self.db = client[DB_NAME]
        
        # Initialize Redis
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Initialize fraud detection
        self.fraud_detector = FraudDetectionEngine(self.redis_client, self.db)
        
        # GeoIP reader (optional)
        self.geoip_reader = None
        try:
            import geoip2.database
            geoip_path = os.getenv("GEOIP_DATABASE_PATH", "GeoLite2-City.mmdb")
            if os.path.exists(geoip_path):
                self.geoip_reader = geoip2.database.Reader(geoip_path)
        except Exception as e:
            logging.warning(f"GeoIP database not available: {e}")
    
    async def track_click(self, request: Request, track_data: TrackClickRequest) -> TrackingData:
        """Advanced click tracking with multiple methods"""
        
        # Generate unique tracking ID
        tracking_id = f"track_{uuid.uuid4().hex[:16]}"
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        
        # Extract request data
        ip_address = self._get_real_ip(request)
        user_agent = request.headers.get("user-agent", "")
        referrer = request.headers.get("referer")
        
        # Parse UTM parameters from request URL
        utm_params = self._extract_utm_params(str(request.url.query))
        
        # Get geolocation
        geo_data = await self._get_geolocation(ip_address)
        
        # Process browser fingerprint
        fingerprint_data = track_data.fingerprint_data or {}
        
        # Create tracking data
        tracking_data = TrackingData(
            tracking_id=tracking_id,
            affiliate_id=track_data.affiliate_id,
            site_id=track_data.site_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            # Browser fingerprint
            screen_resolution=fingerprint_data.get('screen_resolution'),
            timezone=fingerprint_data.get('timezone'),
            language=fingerprint_data.get('language'),
            platform=fingerprint_data.get('platform'),
            # UTM data
            **utm_params,
            # Geo data
            **geo_data
        )
        
        # Store multiple tracking methods
        await self._store_cookie_tracking(tracking_data)
        await self._store_ip_tracking(tracking_data)
        await self._store_session_tracking(tracking_data)
        await self._store_fingerprint_tracking(tracking_data, fingerprint_data)
        
        # Fraud detection
        fraud_score, fraud_flags = await self.fraud_detector.assess_click(tracking_data)
        tracking_data.fraud_score = fraud_score
        tracking_data.fraud_flags = fraud_flags
        
        # Store in database
        await self._save_tracking_data(tracking_data)
        
        return tracking_data
    
    async def track_conversion(self, request: Request, conversion_request: TrackConversionRequest) -> ConversionData:
        """Advanced conversion tracking with attribution"""
        
        conversion_id = f"conv_{uuid.uuid4().hex[:16]}"
        ip_address = self._get_real_ip(request)
        user_agent = request.headers.get("user-agent", "")
        
        # Create conversion data
        conversion_data = ConversionData(
            conversion_id=conversion_id,
            affiliate_id=conversion_request.affiliate_id,
            site_id=conversion_request.site_id,
            customer_email=conversion_request.customer_email,
            customer_id=conversion_request.customer_id,
            event_type=conversion_request.event_type,
            conversion_value=conversion_request.conversion_value,
            currency=conversion_request.currency,
            product_id=conversion_request.product_id,
            product_name=conversion_request.product_name,
            order_id=conversion_request.order_id
        )
        
        # Multi-method attribution
        attribution_results = await self._perform_attribution(
            conversion_data, ip_address, user_agent
        )
        
        # Update conversion with attribution data
        conversion_data.tracking_id = attribution_results.get("tracking_id")
        conversion_data.attribution_methods = attribution_results["methods"]
        conversion_data.attribution_data = attribution_results["data"]
        conversion_data.first_click_data = attribution_results.get("first_click")
        conversion_data.last_click_data = attribution_results.get("last_click")
        
        # Calculate time to conversion
        if conversion_data.first_click_data and conversion_data.first_click_data.get("timestamp"):
            first_click_time = datetime.fromisoformat(
                conversion_data.first_click_data["timestamp"].replace('Z', '+00:00')
            )
            conversion_data.time_to_conversion = int(
                (conversion_data.conversion_timestamp - first_click_time).total_seconds()
            )
        
        # Fraud assessment for conversion
        fraud_risk, fraud_details = await self.fraud_detector.assess_conversion(
            conversion_data, request
        )
        conversion_data.fraud_risk = fraud_risk
        conversion_data.fraud_details = fraud_details
        
        # Store conversion
        await self._save_conversion_data(conversion_data)
        
        return conversion_data
    
    async def _perform_attribution(self, conversion_data: ConversionData, 
                                 ip_address: str, user_agent: str) -> Dict[str, Any]:
        """Multi-method attribution to find the source affiliate"""
        
        attribution_methods = []
        attribution_data = {}
        
        # Method 1: Email-based attribution (if customer email provided)
        if conversion_data.customer_email:
            email_data = await self._check_email_attribution(conversion_data.customer_email)
            if email_data:
                attribution_methods.append(TrackingMethod.EMAIL_TRACKING)
                attribution_data["email_tracking"] = email_data
        
        # Method 2: IP-based attribution (for same IP within timeframe)
        ip_data = await self._check_ip_attribution(ip_address, hours_back=72)
        if ip_data:
            attribution_methods.append(TrackingMethod.IP_TRACKING)
            attribution_data["ip_tracking"] = ip_data
        
        # Method 3: Browser fingerprint attribution
        fingerprint_data = await self._check_fingerprint_attribution(user_agent, ip_address)
        if fingerprint_data:
            attribution_methods.append(TrackingMethod.FINGERPRINT)
            attribution_data["fingerprint"] = fingerprint_data
        
        # Method 4: Session-based attribution
        session_data = await self._check_session_attribution(ip_address, user_agent)
        if session_data:
            attribution_methods.append(TrackingMethod.COOKIE)
            attribution_data["session"] = session_data
        
        # Determine best attribution (priority order)
        best_attribution = self._determine_best_attribution(attribution_data)
        
        return {
            "methods": attribution_methods,
            "data": attribution_data,
            "best_attribution": best_attribution,
            "tracking_id": best_attribution.get("data", {}).get("tracking_id"),
            "first_click": best_attribution.get("data", {}),
            "last_click": best_attribution.get("data", {})
        }
    
    def _determine_best_attribution(self, attribution_data: Dict) -> Dict:
        """Determine the most reliable attribution method"""
        
        # Priority order (most to least reliable)
        priority_methods = ["email_tracking", "session", "fingerprint", "ip_tracking"]
        
        for method in priority_methods:
            if method in attribution_data:
                return {
                    "method": method,
                    "data": attribution_data[method],
                    "confidence": self._get_confidence_score(method, attribution_data[method])
                }
        
        return {"method": "unknown", "data": {}, "confidence": 0.0}
    
    def _get_confidence_score(self, method: str, data: Dict) -> float:
        """Calculate confidence score for attribution method"""
        base_scores = {
            "email_tracking": 0.95,
            "session": 0.90,
            "fingerprint": 0.80,
            "ip_tracking": 0.60
        }
        
        base_score = base_scores.get(method, 0.5)
        
        # Adjust based on data quality
        if data.get("timestamp"):
            try:
                timestamp = datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
                time_diff = (datetime.now(timezone.utc) - timestamp).days
                if time_diff > 30:  # Older than 30 days
                    base_score *= 0.8
            except:
                pass
        
        return min(base_score, 1.0)
    
    # Storage methods for different tracking approaches
    async def _store_cookie_tracking(self, tracking_data: TrackingData):
        """Store data for cookie-based tracking"""
        cookie_key = f"cookie:{tracking_data.tracking_id}"
        await self.redis_client.setex(
            cookie_key, 
            int(timedelta(days=90).total_seconds()),  # 90-day cookie
            json.dumps({
                "tracking_id": tracking_data.tracking_id,
                "affiliate_id": tracking_data.affiliate_id,
                "site_id": tracking_data.site_id,
                "timestamp": tracking_data.created_at.isoformat(),
                "utm_data": {
                    "source": tracking_data.utm_source,
                    "medium": tracking_data.utm_medium,
                    "campaign": tracking_data.utm_campaign
                }
            })
        )
    
    async def _store_ip_tracking(self, tracking_data: TrackingData):
        """Store IP-based tracking data"""
        ip_key = f"ip:{hashlib.md5(tracking_data.ip_address.encode()).hexdigest()}"
        
        # Store recent clicks for this IP
        existing_data = await self.redis_client.get(ip_key)
        if existing_data:
            clicks = json.loads(existing_data)
        else:
            clicks = []
        
        clicks.append({
            "tracking_id": tracking_data.tracking_id,
            "affiliate_id": tracking_data.affiliate_id,
            "site_id": tracking_data.site_id,
            "timestamp": tracking_data.created_at.isoformat(),
            "user_agent": tracking_data.user_agent
        })
        
        # Keep only last 10 clicks per IP
        clicks = clicks[-10:]
        
        await self.redis_client.setex(
            ip_key,
            int(timedelta(days=7).total_seconds()),  # 7-day IP tracking
            json.dumps(clicks)
        )
    
    async def _store_session_tracking(self, tracking_data: TrackingData):
        """Store session-based tracking"""
        session_key = f"session:{tracking_data.session_id}"
        await self.redis_client.setex(
            session_key,
            int(timedelta(hours=24).total_seconds()),  # 24-hour session
            json.dumps({
                "tracking_id": tracking_data.tracking_id,
                "affiliate_id": tracking_data.affiliate_id,
                "site_id": tracking_data.site_id,
                "ip_address": tracking_data.ip_address,
                "user_agent": tracking_data.user_agent,
                "timestamp": tracking_data.created_at.isoformat()
            })
        )
    
    async def _store_fingerprint_tracking(self, tracking_data: TrackingData, fingerprint_data: Dict):
        """Store browser fingerprint tracking"""
        if fingerprint_data:
            fingerprint_hash = BrowserFingerprint.generate_fingerprint(fingerprint_data)
            fingerprint_key = f"fingerprint:{fingerprint_hash}"
            
            await self.redis_client.setex(
                fingerprint_key,
                int(timedelta(days=30).total_seconds()),  # 30-day fingerprint
                json.dumps({
                    "tracking_id": tracking_data.tracking_id,
                    "affiliate_id": tracking_data.affiliate_id,
                    "site_id": tracking_data.site_id,
                    "timestamp": tracking_data.created_at.isoformat(),
                    "fingerprint_data": fingerprint_data
                })
            )
    
    # Attribution check methods
    async def _check_email_attribution(self, customer_email: str) -> Optional[Dict]:
        """Check for email-based attribution"""
        email_key = f"email:{hashlib.md5(customer_email.encode()).hexdigest()}"
        data = await self.redis_client.get(email_key)
        
        if data:
            return json.loads(data)
        
        return None
    
    async def _check_ip_attribution(self, ip_address: str, hours_back: int = 72) -> Optional[Dict]:
        """Check for IP-based attribution within timeframe"""
        ip_key = f"ip:{hashlib.md5(ip_address.encode()).hexdigest()}"
        data = await self.redis_client.get(ip_key)
        
        if data:
            clicks = json.loads(data)
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
            
            # Find clicks within timeframe
            valid_clicks = [
                click for click in clicks 
                if datetime.fromisoformat(click["timestamp"].replace('Z', '+00:00')) > cutoff_time
            ]
            
            if valid_clicks:
                # Return most recent click
                return valid_clicks[-1]
        
        return None
    
    async def _check_fingerprint_attribution(self, user_agent: str, ip_address: str) -> Optional[Dict]:
        """Check for browser fingerprint attribution"""
        # Simple fingerprint based on user agent + IP
        fingerprint = hashlib.sha256(f"{user_agent}{ip_address}".encode()).hexdigest()
        fingerprint_key = f"fingerprint:{fingerprint}"
        
        data = await self.redis_client.get(fingerprint_key)
        if data:
            return json.loads(data)
        
        return None
    
    async def _check_session_attribution(self, ip_address: str, user_agent: str) -> Optional[Dict]:
        """Check for session-based attribution"""
        # Look for recent sessions from same IP/UA
        session_pattern = f"session:*"
        sessions = await self.redis_client.keys(session_pattern)
        
        for session_key in sessions:
            session_data = await self.redis_client.get(session_key)
            if session_data:
                data = json.loads(session_data)
                if (data.get("ip_address") == ip_address and 
                    data.get("user_agent") == user_agent):
                    return data
        
        return None
    
    # Utility methods
    def _get_real_ip(self, request: Request) -> str:
        """Extract real IP address considering proxies"""
        # Check for forwarded headers
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
            
        return request.client.host if request.client else "127.0.0.1"
    
    def _extract_utm_params(self, query_string: str) -> Dict[str, Optional[str]]:
        """Extract UTM parameters from query string"""
        try:
            params = parse_qs(query_string)
            return {
                "utm_source": params.get("utm_source", [None])[0],
                "utm_medium": params.get("utm_medium", [None])[0], 
                "utm_campaign": params.get("utm_campaign", [None])[0],
                "utm_content": params.get("utm_content", [None])[0],
                "utm_term": params.get("utm_term", [None])[0]
            }
        except:
            return {
                "utm_source": None,
                "utm_medium": None,
                "utm_campaign": None,
                "utm_content": None,
                "utm_term": None
            }
    
    async def _get_geolocation(self, ip_address: str) -> Dict[str, Optional[str]]:
        """Get geolocation data for IP address"""
        if not self.geoip_reader:
            return {"country": None, "region": None, "city": None}
        
        try:
            response = self.geoip_reader.city(ip_address)
            return {
                "country": response.country.name,
                "region": response.subdivisions.most_specific.name,
                "city": response.city.name
            }
        except:
            return {"country": None, "region": None, "city": None}
    
    # Database operations
    async def _save_tracking_data(self, tracking_data: TrackingData):
        """Save tracking data to database"""
        try:
            await self.db.advanced_tracking_events.insert_one(tracking_data.dict())
            logging.info(f"Saved tracking data: {tracking_data.tracking_id}")
        except Exception as e:
            logging.error(f"Failed to save tracking data: {e}")
    
    async def _save_conversion_data(self, conversion_data: ConversionData):
        """Save conversion data to database"""
        try:
            await self.db.advanced_conversion_events.insert_one(conversion_data.dict())
            logging.info(f"Saved conversion data: {conversion_data.conversion_id}")
        except Exception as e:
            logging.error(f"Failed to save conversion data: {e}")

# =============================================================================
# Fraud Detection Engine
# =============================================================================

class FraudDetectionEngine:
    def __init__(self, redis_client, db):
        self.redis_client = redis_client
        self.db = db
    
    async def assess_click(self, tracking_data: TrackingData) -> tuple[float, List[str]]:
        """Assess fraud risk for click events"""
        fraud_score = 0.0
        fraud_flags = []
        
        # Check for suspicious IP patterns
        ip_flags = await self._check_ip_fraud(tracking_data.ip_address)
        fraud_flags.extend(ip_flags)
        fraud_score += len(ip_flags) * 0.1
        
        # Check for bot user agents
        if self._is_bot_user_agent(tracking_data.user_agent):
            fraud_flags.append("bot_user_agent")
            fraud_score += 0.3
        
        # Check for click velocity (too many clicks too fast)
        velocity_score = await self._check_click_velocity(
            tracking_data.affiliate_id, tracking_data.ip_address
        )
        if velocity_score > 0.5:
            fraud_flags.append("high_velocity")
            fraud_score += velocity_score
        
        return min(fraud_score, 1.0), fraud_flags
    
    async def assess_conversion(self, conversion_data: ConversionData, 
                              request: Request) -> tuple[FraudRiskLevel, Dict]:
        """Assess fraud risk for conversion events"""
        fraud_details = {}
        total_score = 0.0
        
        # Check conversion velocity
        ip_address = self._get_real_ip(request)
        velocity_score = await self._check_conversion_velocity(
            conversion_data.affiliate_id, 
            ip_address
        )
        fraud_details["velocity_score"] = velocity_score
        total_score += velocity_score
        
        # Check for duplicate conversions
        duplicate_score = await self._check_duplicate_conversion(conversion_data)
        fraud_details["duplicate_score"] = duplicate_score
        total_score += duplicate_score
        
        # Check conversion value anomalies
        value_score = await self._check_value_anomaly(conversion_data)
        fraud_details["value_score"] = value_score
        total_score += value_score
        
        # Determine risk level
        if total_score >= 0.8:
            return FraudRiskLevel.BLOCKED, fraud_details
        elif total_score >= 0.5:
            return FraudRiskLevel.HIGH, fraud_details
        elif total_score >= 0.3:
            return FraudRiskLevel.MEDIUM, fraud_details
        else:
            return FraudRiskLevel.LOW, fraud_details
    
    async def _check_ip_fraud(self, ip_address: str) -> List[str]:
        """Check IP address for fraud indicators"""
        flags = []
        
        # Check against known proxy/VPN ranges (simplified)
        if self._is_datacenter_ip(ip_address):
            flags.append("datacenter_ip")
        
        # Check for IP reputation
        if await self._is_blacklisted_ip(ip_address):
            flags.append("blacklisted_ip")
        
        return flags
    
    def _is_bot_user_agent(self, user_agent: str) -> bool:
        """Check if user agent appears to be a bot"""
        bot_indicators = [
            "bot", "crawler", "spider", "scraper", "curl", "wget", 
            "python", "java", "phantom", "headless"
        ]
        
        user_agent_lower = user_agent.lower()
        return any(indicator in user_agent_lower for indicator in bot_indicators)
    
    def _is_datacenter_ip(self, ip_address: str) -> bool:
        """Check if IP is from a datacenter (simplified check)"""
        # This would typically use a commercial IP intelligence service
        datacenter_ranges = [
            "52.", "54.", "23.", "107.",  # AWS ranges (simplified)
        ]
        
        return any(ip_address.startswith(range_prefix) for range_prefix in datacenter_ranges)
    
    async def _is_blacklisted_ip(self, ip_address: str) -> bool:
        """Check if IP is blacklisted"""
        blacklist_key = f"blacklist:ip:{ip_address}"
        return bool(await self.redis_client.get(blacklist_key))
    
    async def _check_click_velocity(self, affiliate_id: str, ip_address: str) -> float:
        """Check for suspicious click velocity"""
        # Count clicks from this IP for this affiliate in last hour
        velocity_key = f"velocity:click:{affiliate_id}:{hashlib.md5(ip_address.encode()).hexdigest()}"
        
        # Increment counter
        await self.redis_client.incr(velocity_key)
        await self.redis_client.expire(velocity_key, 3600)  # 1 hour expiry
        
        # Get current count
        click_count = int(await self.redis_client.get(velocity_key) or 0)
        
        # Normal: 1-10 clicks/hour, Suspicious: 10-50, Fraud: 50+
        if click_count > 50:
            return 1.0
        elif click_count > 10:
            return min((click_count - 10) / 40, 0.8)
        else:
            return 0.0
    
    async def _check_conversion_velocity(self, affiliate_id: str, ip_address: str) -> float:
        """Check for suspicious conversion velocity"""
        velocity_key = f"velocity:conversion:{affiliate_id}:{hashlib.md5(ip_address.encode()).hexdigest()}"
        
        await self.redis_client.incr(velocity_key)
        await self.redis_client.expire(velocity_key, 86400)  # 24 hour expiry
        
        conversion_count = int(await self.redis_client.get(velocity_key) or 0)
        
        # Normal: 1-2 conversions/day, Suspicious: 3-10, Fraud: 10+
        if conversion_count > 10:
            return 1.0
        elif conversion_count > 2:
            return min((conversion_count - 2) / 8, 0.8)
        else:
            return 0.0
    
    async def _check_duplicate_conversion(self, conversion_data: ConversionData) -> float:
        """Check for duplicate conversions"""
        if not conversion_data.customer_email:
            return 0.0
        
        # Check for same email/product/value in last 24 hours
        dup_key = f"dup:{hashlib.md5(f'{conversion_data.customer_email}{conversion_data.product_id}{conversion_data.conversion_value}'.encode()).hexdigest()}"
        
        if await self.redis_client.get(dup_key):
            return 0.9  # High fraud score for exact duplicate
        
        # Set key to prevent duplicates
        await self.redis_client.setex(dup_key, 86400, "1")
        
        return 0.0
    
    async def _check_value_anomaly(self, conversion_data: ConversionData) -> float:
        """Check for suspicious conversion values"""
        value = conversion_data.conversion_value
        
        # Check for round numbers (often fake)
        if value > 0 and value % 100 == 0:
            return 0.2
        
        # Check for extremely high values
        if value > 10000:
            return 0.5
        
        # Check for zero value conversions
        if value == 0 and conversion_data.event_type == TrackingEvent.SALE:
            return 0.3
        
        return 0.0
    
    def _get_real_ip(self, request: Request) -> str:
        """Extract real IP from request"""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "127.0.0.1"

# Initialize the tracking engine
tracking_engine = AdvancedTrackingEngine()

# =============================================================================
# FastAPI Router
# =============================================================================

router = APIRouter(prefix="/api/v2/track", tags=["Advanced Tracking System"])

@router.post("/click")
async def track_click(
    request: Request,
    track_data: TrackClickRequest
):
    """Advanced click tracking endpoint"""
    try:
        tracking_data = await tracking_engine.track_click(request, track_data)
        
        return {
            "success": True,
            "tracking_id": tracking_data.tracking_id,
            "fraud_score": tracking_data.fraud_score,
            "fraud_flags": tracking_data.fraud_flags,
            "attribution_cookie": tracking_data.tracking_id,  # For browser cookie
            "pixel_url": f"/api/v2/track/pixel/{tracking_data.tracking_id}"
        }
        
    except Exception as e:
        logging.error(f"Track click error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversion") 
async def track_conversion(
    request: Request,
    conversion_data: TrackConversionRequest
):
    """Advanced conversion tracking with multi-method attribution"""
    try:
        result = await tracking_engine.track_conversion(request, conversion_data)
        
        return {
            "success": True,
            "conversion_id": result.conversion_id,
            "tracking_id": result.tracking_id,
            "attribution_methods": result.attribution_methods,
            "best_attribution": result.attribution_data,
            "fraud_risk": result.fraud_risk,
            "fraud_details": result.fraud_details,
            "time_to_conversion": result.time_to_conversion
        }
        
    except Exception as e:
        logging.error(f"Track conversion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pixel/{tracking_id}")
async def tracking_pixel(tracking_id: str, request: Request):
    """1x1 tracking pixel for additional attribution"""
    
    try:
        # Log pixel impression
        ip_address = tracking_engine._get_real_ip(request)
        user_agent = request.headers.get("user-agent", "")
        
        # Store pixel hit data
        pixel_key = f"pixel:{tracking_id}"
        await tracking_engine.redis_client.setex(
            pixel_key,
            int(timedelta(days=30).total_seconds()),
            json.dumps({
                "ip_address": ip_address,
                "user_agent": user_agent,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "hit_count": 1
            })
        )
        
        # Return 1x1 transparent pixel
        pixel_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
        
        return Response(
            content=pixel_data,
            media_type="image/png",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    except Exception as e:
        logging.error(f"Pixel tracking error: {e}")
        # Return pixel anyway to not break page loading
        pixel_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
        return Response(content=pixel_data, media_type="image/png")

@router.post("/email/open")
async def track_email_open(
    request: Request,
    affiliate_id: str,
    customer_email: EmailStr,
    email_campaign_id: str
):
    """Track email opens for attribution"""
    
    try:
        # Create email tracking entry
        email_key = f"email:{hashlib.md5(customer_email.encode()).hexdigest()}"
        await tracking_engine.redis_client.setex(
            email_key,
            int(timedelta(days=30).total_seconds()),
            json.dumps({
                "affiliate_id": affiliate_id,
                "customer_email": customer_email,
                "campaign_id": email_campaign_id,
                "event": "open",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ip_address": tracking_engine._get_real_ip(request)
            })
        )
        
        return {"success": True, "tracked": "email_open"}
        
    except Exception as e:
        logging.error(f"Email open tracking error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/email/click")
async def track_email_click(
    request: Request,
    affiliate_id: str,
    customer_email: EmailStr,
    email_campaign_id: str,
    link_id: Optional[str] = None
):
    """Track email link clicks for attribution"""
    
    try:
        # Store email click data
        click_key = f"email_click:{affiliate_id}:{hashlib.md5(customer_email.encode()).hexdigest()}"
        await tracking_engine.redis_client.setex(
            click_key,
            int(timedelta(days=30).total_seconds()),
            json.dumps({
                "affiliate_id": affiliate_id,
                "customer_email": customer_email,
                "campaign_id": email_campaign_id,
                "link_id": link_id,
                "event": "click",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ip_address": tracking_engine._get_real_ip(request),
                "user_agent": request.headers.get("user-agent", "")
            })
        )
        
        return {"success": True, "tracked": "email_click"}
        
    except Exception as e:
        logging.error(f"Email click tracking error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/attribution/{customer_identifier}")
async def get_attribution(
    customer_identifier: str,  # email hash or customer ID
    lookback_days: int = 30
):
    """Get attribution data for a customer"""
    
    try:
        # Search for attribution data
        attribution_data = {}
        
        # Check email attribution
        email_key = f"email:{customer_identifier}"
        email_data = await tracking_engine.redis_client.get(email_key)
        if email_data:
            attribution_data["email"] = json.loads(email_data)
        
        # Check IP attribution (would need more complex search in production)
        
        return {
            "success": True,
            "customer_identifier": customer_identifier,
            "attribution_data": attribution_data,
            "lookback_days": lookback_days
        }
        
    except Exception as e:
        logging.error(f"Get attribution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/fraud")
async def get_fraud_stats(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN])),
    affiliate_id: Optional[str] = None,
    site_id: Optional[str] = None,
    days_back: int = 7
):
    """Get fraud detection statistics (Admin only)"""
    
    try:
        # Get fraud statistics from database
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        
        # Count total clicks and fraud flags
        total_clicks_cursor = tracking_engine.db.advanced_tracking_events.find({
            "created_at": {"$gte": cutoff_date}
        })
        
        total_clicks = 0
        fraudulent_clicks = 0
        fraud_types = {}
        
        async for click in total_clicks_cursor:
            total_clicks += 1
            if click.get("fraud_score", 0) > 0.5 or click.get("fraud_flags"):
                fraudulent_clicks += 1
                for flag in click.get("fraud_flags", []):
                    fraud_types[flag] = fraud_types.get(flag, 0) + 1
        
        fraud_rate = fraudulent_clicks / total_clicks if total_clicks > 0 else 0
        
        return {
            "success": True,
            "fraud_stats": {
                "total_clicks": total_clicks,
                "fraudulent_clicks": fraudulent_clicks,
                "fraud_rate": fraud_rate,
                "top_fraud_types": [
                    {"type": fraud_type, "count": count}
                    for fraud_type, count in sorted(fraud_types.items(), key=lambda x: x[1], reverse=True)
                ][:5]
            },
            "period": f"Last {days_back} days"
        }
        
    except Exception as e:
        logging.error(f"Get fraud stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check for tracking system"""
    
    # Check Redis connection
    try:
        await tracking_engine.redis_client.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"
    
    # Check MongoDB connection
    try:
        await tracking_engine.db.command("ping")
        mongodb_status = "healthy"
    except:
        mongodb_status = "unhealthy"
    
    return {
        "status": "healthy" if redis_status == "healthy" and mongodb_status == "healthy" else "degraded",
        "components": {
            "redis": redis_status,
            "mongodb": mongodb_status,
            "geoip": "healthy" if tracking_engine.geoip_reader else "disabled",
            "fraud_detection": "healthy"
        },
        "tracking_methods": [
            "cookie", "ip_tracking", "email_tracking", 
            "fingerprint", "session", "pixel"
        ]
    }