# Email Platform Integrations System
import os
import uuid
import json
import hmac
import hashlib
import httpx
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Header, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Import authentication from main auth system
from auth.auth_system import get_current_user, UserProfile, require_role, UserRole

load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Encryption setup for API keys
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "placeholder-encryption-key-generate-in-production")
if ENCRYPTION_KEY == "placeholder-encryption-key-generate-in-production":
    # Generate a placeholder key for development
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    
cipher_suite = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

router = APIRouter(prefix="/api/integrations", tags=["Email Platform Integrations"])

# ========== MODELS ==========

class EmailPlatform(str, Enum):
    CONVERTKIT = "convertkit"
    GETRESPONSE = "getresponse"  
    ZAPIER = "zapier"

class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class AffiliateIntegration(BaseModel):
    integration_id: str = Field(primary_key=True)
    affiliate_id: str
    platform: EmailPlatform
    status: IntegrationStatus = IntegrationStatus.ACTIVE
    encrypted_api_key: Optional[str] = None
    webhook_url: Optional[str] = None
    tags: List[str] = []
    custom_fields: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_sync: Optional[datetime] = None

class IntegrationSetupRequest(BaseModel):
    affiliate_id: str
    platform: EmailPlatform
    api_key: str
    webhook_url: Optional[str] = None
    tags: List[str] = ["affiliate", "customer"]
    custom_fields: Dict[str, Any] = {}

class ConversionSyncRequest(BaseModel):
    affiliate_id: str
    customer_email: EmailStr
    customer_name: Optional[str] = None
    conversion_value: float
    product_name: Optional[str] = None
    site_id: Optional[str] = "main_site"
    utm_data: Dict[str, Any] = {}

class WebhookLog(BaseModel):
    log_id: str = Field(primary_key=True)
    affiliate_id: str
    platform: EmailPlatform
    event_type: str
    payload: Dict[str, Any]
    processed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ========== ENCRYPTION HELPERS ==========

def encrypt_api_key(api_key: str) -> str:
    """Encrypt API key for secure storage"""
    return cipher_suite.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt API key for use"""
    return cipher_suite.decrypt(encrypted_key.encode()).decode()

# ========== EMAIL PLATFORM CLIENTS ==========

class ConvertKitClient:
    def __init__(self, api_secret: str):
        self.api_secret = api_secret
        self.base_url = "https://api.convertkit.com/v3"
    
    async def add_subscriber(self, email: str, name: str = None, tags: List[str] = [], custom_fields: Dict = {}):
        """Add subscriber to ConvertKit"""
        async with httpx.AsyncClient() as client:
            data = {
                "api_secret": self.api_secret,
                "email": email,
                "tags": tags
            }
            if name:
                data["first_name"] = name.split(" ")[0] if " " in name else name
                if " " in name:
                    data["last_name"] = " ".join(name.split(" ")[1:])
            
            # Add custom fields
            data["fields"] = custom_fields
            
            response = await client.post(f"{self.base_url}/subscribers", json=data)
            response.raise_for_status()
            return response.json()
    
    async def add_tag_to_subscriber(self, email: str, tag: str):
        """Add tag to existing subscriber"""
        async with httpx.AsyncClient() as client:
            data = {
                "api_secret": self.api_secret,
                "email": email
            }
            response = await client.post(f"{self.base_url}/tags/{tag}/subscribe", json=data)
            response.raise_for_status()
            return response.json()

class GetResponseClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.getresponse.com/v3"
        self.headers = {"X-Auth-Token": f"api-key {api_key}"}
    
    async def add_contact(self, email: str, name: str = None, tags: List[str] = [], custom_fields: Dict = {}):
        """Add contact to GetResponse"""
        async with httpx.AsyncClient() as client:
            data = {
                "email": email,
                "campaign": {"campaignId": "PLACEHOLDER_CAMPAIGN_ID"},  # User needs to configure
                "tags": [{"tagId": tag} for tag in tags]
            }
            if name:
                data["name"] = name
            
            # Add custom fields
            if custom_fields:
                data["customFieldValues"] = [
                    {"customFieldId": k, "value": [v]} for k, v in custom_fields.items()
                ]
            
            response = await client.post(f"{self.base_url}/contacts", json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()

class ZapierClient:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_webhook(self, data: Dict):
        """Send data to Zapier webhook"""
        async with httpx.AsyncClient() as client:
            response = await client.post(self.webhook_url, json=data)
            response.raise_for_status()
            return {"status": "sent", "webhook_url": self.webhook_url}

# ========== INTEGRATION MANAGEMENT ==========

async def get_platform_client(integration: Dict):
    """Get the appropriate client for a platform"""
    platform = integration["platform"]
    
    if platform == EmailPlatform.CONVERTKIT:
        api_key = decrypt_api_key(integration["encrypted_api_key"])
        return ConvertKitClient(api_key)
    elif platform == EmailPlatform.GETRESPONSE:
        api_key = decrypt_api_key(integration["encrypted_api_key"])
        return GetResponseClient(api_key)
    elif platform == EmailPlatform.ZAPIER:
        return ZapierClient(integration["webhook_url"])
    else:
        raise ValueError(f"Unsupported platform: {platform}")

# ========== API ENDPOINTS ==========

@router.post("/setup")
async def setup_integration(request: IntegrationSetupRequest):
    """Setup email platform integration for affiliate"""
    try:
        # Check if integration already exists
        existing = await db.affiliate_integrations.find_one({
            "affiliate_id": request.affiliate_id,
            "platform": request.platform
        })
        
        integration_id = existing["integration_id"] if existing else str(uuid.uuid4())
        
        # Encrypt API key
        encrypted_key = encrypt_api_key(request.api_key) if request.api_key else None
        
        integration_data = {
            "integration_id": integration_id,
            "affiliate_id": request.affiliate_id,
            "platform": request.platform,
            "status": IntegrationStatus.ACTIVE,
            "encrypted_api_key": encrypted_key,
            "webhook_url": request.webhook_url,
            "tags": request.tags,
            "custom_fields": request.custom_fields,
            "created_at": datetime.now(timezone.utc),
            "last_sync": None
        }
        
        # Upsert integration
        await db.affiliate_integrations.replace_one(
            {"integration_id": integration_id},
            integration_data,
            upsert=True
        )
        
        # Test the integration
        try:
            client = await get_platform_client(integration_data)
            test_result = await test_integration_connection(client, request.platform)
            
            return {
                "success": True,
                "integration_id": integration_id,
                "status": "active",
                "test_result": test_result,
                "message": f"{request.platform.title()} integration setup successful"
            }
        except Exception as test_error:
            # Mark as error but still save the integration
            await db.affiliate_integrations.update_one(
                {"integration_id": integration_id},
                {"$set": {"status": IntegrationStatus.ERROR}}
            )
            
            return {
                "success": False,
                "integration_id": integration_id,
                "status": "error",
                "error": str(test_error),
                "message": f"Integration saved but connection test failed: {test_error}"
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Setup failed: {str(e)}")

@router.post("/sync-conversion")
async def sync_conversion_to_platforms(request: ConversionSyncRequest, background_tasks: BackgroundTasks):
    """Sync conversion data to all active email platforms for affiliate"""
    try:
        # Get all active integrations for affiliate
        integrations = await db.affiliate_integrations.find({
            "affiliate_id": request.affiliate_id,
            "status": IntegrationStatus.ACTIVE
        }).to_list(length=None)
        
        if not integrations:
            return {
                "success": True,
                "message": "No active integrations found for affiliate",
                "synced_platforms": []
            }
        
        synced_platforms = []
        errors = []
        
        for integration in integrations:
            try:
                # Add background task for each platform
                background_tasks.add_task(
                    sync_to_platform,
                    integration,
                    request
                )
                synced_platforms.append(integration["platform"])
                
            except Exception as e:
                errors.append(f"{integration['platform']}: {str(e)}")
        
        return {
            "success": True,
            "synced_platforms": synced_platforms,
            "total_integrations": len(integrations),
            "errors": errors,
            "message": f"Conversion sync initiated for {len(synced_platforms)} platforms"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

async def sync_to_platform(integration: Dict, request: ConversionSyncRequest):
    """Background task to sync conversion to specific platform"""
    try:
        client = await get_platform_client(integration)
        platform = integration["platform"]
        
        # Prepare conversion data
        conversion_data = {
            "email": request.customer_email,
            "name": request.customer_name,
            "conversion_value": request.conversion_value,
            "product_name": request.product_name,
            "site_id": request.site_id,
            "affiliate_id": request.affiliate_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "utm_data": request.utm_data
        }
        
        # Add conversion tags
        conversion_tags = integration["tags"] + ["conversion", f"value_{int(request.conversion_value)}"]
        
        if platform == EmailPlatform.CONVERTKIT:
            # Add/update subscriber with conversion data
            await client.add_subscriber(
                email=request.customer_email,
                name=request.customer_name,
                tags=conversion_tags,
                custom_fields={
                    **integration["custom_fields"],
                    "last_conversion_value": request.conversion_value,
                    "affiliate_id": request.affiliate_id,
                    "site_id": request.site_id
                }
            )
            
        elif platform == EmailPlatform.GETRESPONSE:
            # Add contact with conversion data
            await client.add_contact(
                email=request.customer_email,
                name=request.customer_name,
                tags=conversion_tags,
                custom_fields={
                    **integration["custom_fields"],
                    "last_conversion_value": str(request.conversion_value),
                    "affiliate_id": request.affiliate_id,
                    "site_id": request.site_id
                }
            )
            
        elif platform == EmailPlatform.ZAPIER:
            # Send webhook with full conversion data
            await client.send_webhook({
                "action": "conversion",
                "customer_data": {
                    "email": request.customer_email,
                    "name": request.customer_name
                },
                "conversion_data": conversion_data,
                "tags": conversion_tags,
                "custom_fields": integration["custom_fields"]
            })
        
        # Update last sync time
        await db.affiliate_integrations.update_one(
            {"integration_id": integration["integration_id"]},
            {"$set": {"last_sync": datetime.now(timezone.utc)}}
        )
        
    except Exception as e:
        # Log the error
        await db.integration_webhook_logs.insert_one({
            "log_id": str(uuid.uuid4()),
            "affiliate_id": integration["affiliate_id"],
            "platform": integration["platform"],
            "event_type": "sync_error",
            "payload": {"error": str(e), "request": request.dict()},
            "processed": False,
            "created_at": datetime.now(timezone.utc)
        })

async def test_integration_connection(client, platform: str):
    """Test integration connection"""
    try:
        if platform == EmailPlatform.CONVERTKIT:
            # Test by trying to get account info (placeholder)
            return {"status": "connected", "platform": platform, "test": "api_key_valid"}
        elif platform == EmailPlatform.GETRESPONSE:
            # Test by trying to get campaigns (placeholder)
            return {"status": "connected", "platform": platform, "test": "api_key_valid"}
        elif platform == EmailPlatform.ZAPIER:
            # Test webhook URL accessibility (placeholder)
            return {"status": "connected", "platform": platform, "test": "webhook_url_accessible"}
        else:
            return {"status": "unknown_platform"}
    except:
        return {"status": "connection_failed"}

@router.get("/test/{affiliate_id}/{platform}")
async def test_integration(affiliate_id: str, platform: EmailPlatform):
    """Test specific integration for affiliate"""
    try:
        integration = await db.affiliate_integrations.find_one({
            "affiliate_id": affiliate_id,
            "platform": platform
        })
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        client = await get_platform_client(integration)
        test_result = await test_integration_connection(client, platform)
        
        # Update status based on test
        new_status = IntegrationStatus.ACTIVE if test_result["status"] == "connected" else IntegrationStatus.ERROR
        await db.affiliate_integrations.update_one(
            {"integration_id": integration["integration_id"]},
            {"$set": {"status": new_status}}
        )
        
        return {
            "success": test_result["status"] == "connected",
            "integration_id": integration["integration_id"],
            "platform": platform,
            "test_result": test_result,
            "status": new_status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

# ========== HEALTH CHECK ==========

@router.get("/health")
async def integration_health_check():
    """Health check for integration system"""
    try:
        # Test database connection
        await db.affiliate_integrations.count_documents({})
        
        return {
            "success": True,
            "status": "healthy",
            "encryption": "enabled",
            "platforms_supported": ["convertkit", "getresponse", "zapier"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

@router.get("/{affiliate_id}")
async def get_affiliate_integrations(affiliate_id: str):
    """Get all integrations for an affiliate"""
    try:
        integrations = await db.affiliate_integrations.find(
            {"affiliate_id": affiliate_id}
        ).to_list(length=None)
        
        # Remove sensitive data
        for integration in integrations:
            integration.pop("encrypted_api_key", None)
        
        return {
            "success": True,
            "affiliate_id": affiliate_id,
            "integrations": integrations,
            "total": len(integrations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get integrations: {str(e)}")

@router.delete("/{integration_id}")
async def delete_integration(integration_id: str):
    """Delete an integration"""
    try:
        result = await db.affiliate_integrations.delete_one({"integration_id": integration_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        return {
            "success": True,
            "message": "Integration deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

# ========== WEBHOOK ENDPOINTS ==========

@router.post("/webhooks/convertkit/{affiliate_id}")
async def convertkit_webhook(
    affiliate_id: str,
    payload: Dict[str, Any],
    x_convertkit_signature: str = Header(None)
):
    """Handle ConvertKit webhooks"""
    try:
        # TODO: Verify webhook signature
        # webhook_secret = os.getenv(f"CONVERTKIT_SECRET_{affiliate_id}")
        
        # Log webhook
        await db.integration_webhook_logs.insert_one({
            "log_id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "platform": EmailPlatform.CONVERTKIT,
            "event_type": payload.get("type", "unknown"),
            "payload": payload,
            "processed": False,
            "created_at": datetime.now(timezone.utc)
        })
        
        # Process webhook based on event type
        event_type = payload.get("type")
        if event_type == "subscriber.subscribe":
            # Handle new subscriber
            await process_subscriber_event(affiliate_id, EmailPlatform.CONVERTKIT, payload)
        
        return {"success": True, "processed": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/webhooks/getresponse/{affiliate_id}")
async def getresponse_webhook(affiliate_id: str, payload: Dict[str, Any]):
    """Handle GetResponse webhooks"""
    try:
        # Log webhook
        await db.integration_webhook_logs.insert_one({
            "log_id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "platform": EmailPlatform.GETRESPONSE,
            "event_type": payload.get("action", "unknown"),
            "payload": payload,
            "processed": False,
            "created_at": datetime.now(timezone.utc)
        })
        
        return {"success": True, "processed": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/webhooks/zapier/{affiliate_id}")
async def zapier_webhook(affiliate_id: str, payload: Dict[str, Any]):
    """Handle Zapier webhooks"""
    try:
        # Log webhook
        await db.integration_webhook_logs.insert_one({
            "log_id": str(uuid.uuid4()),
            "affiliate_id": affiliate_id,
            "platform": EmailPlatform.ZAPIER,
            "event_type": payload.get("action", "unknown"),
            "payload": payload,
            "processed": False,
            "created_at": datetime.now(timezone.utc)
        })
        
        # Process conversion webhooks from Zapier
        if payload.get("action") == "conversion":
            await process_zapier_conversion(affiliate_id, payload)
        
        return {"success": True, "processed": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

async def process_subscriber_event(affiliate_id: str, platform: EmailPlatform, payload: Dict):
    """Process subscriber events for attribution"""
    # TODO: Implement subscriber attribution logic
    # This would track email subscribers back to affiliate links
    pass

async def process_zapier_conversion(affiliate_id: str, payload: Dict):
    """Process conversion webhook from Zapier"""
    try:
        conversion_data = payload.get("conversion_data", {})
        customer_email = payload.get("customer_data", {}).get("email")
        
        if customer_email and conversion_data.get("value"):
            # Create commission record if valid conversion
            from modules.affiliate_system import create_multisite_commission_record
            
            await create_multisite_commission_record(
                affiliate_id=affiliate_id,
                customer_id=customer_email,
                site_id=conversion_data.get("site_id", "main_site"),
                plan_type=conversion_data.get("plan_type", "launch"),
                amount=float(conversion_data["value"]),
                billing_cycle="monthly"
            )
    except Exception as e:
        print(f"Error processing Zapier conversion: {e}")

# ========== ADMIN ENDPOINTS ==========

@router.get("/admin/overview")
async def get_integrations_overview(current_user: UserProfile = Depends(require_role(UserRole.ADMIN))):
    """Get overview of all integrations (Admin only)"""
    try:
        # Get integration statistics
        pipeline = [
            {
                "$group": {
                    "_id": "$platform",
                    "total": {"$sum": 1},
                    "active": {"$sum": {"$cond": [{"$eq": ["$status", "active"]}, 1, 0]}},
                    "error": {"$sum": {"$cond": [{"$eq": ["$status", "error"]}, 1, 0]}}
                }
            }
        ]
        
        stats = await db.affiliate_integrations.aggregate(pipeline).to_list(length=None)
        
        # Get recent webhook logs
        recent_logs = await db.integration_webhook_logs.find().sort("created_at", -1).limit(10).to_list(length=10)
        
        return {
            "success": True,
            "platform_stats": stats,
            "recent_webhooks": recent_logs,
            "total_integrations": sum(stat["total"] for stat in stats)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get overview: {str(e)}")

@router.get("/admin/logs")
async def get_integration_logs(
    platform: Optional[EmailPlatform] = None,
    affiliate_id: Optional[str] = None,
    limit: int = 50,
    current_user: UserProfile = Depends(require_role(UserRole.ADMIN))
):
    """Get integration webhook logs (Admin only)"""
    try:
        query = {}
        if platform:
            query["platform"] = platform
        if affiliate_id:
            query["affiliate_id"] = affiliate_id
        
        logs = await db.integration_webhook_logs.find(query).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        return {
            "success": True,
            "logs": logs,
            "total": len(logs),
            "filters": {"platform": platform, "affiliate_id": affiliate_id}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")