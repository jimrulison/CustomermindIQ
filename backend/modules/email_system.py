"""
CustomerMind IQ - Simple Email System for Customer Communications
With API hookup capabilities for external email services
"""

import asyncio
import json
import os
import uuid
import smtplib
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum
import base64
from dotenv import load_dotenv

# Import auth dependencies
from auth.auth_system import get_current_user, require_role, UserRole, UserProfile, SubscriptionTier

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

router = APIRouter(tags=["Email System"])

# Enums
class EmailStatus(str, Enum):
    DRAFT = "draft"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"

class EmailProvider(str, Enum):
    ODOO = "odoo"                   # ODOO Email Integration (Preferred)
    INTERNAL = "internal"           # Simple SMTP
    SENDGRID = "sendgrid"
    MAILGUN = "mailgun"
    RESEND = "resend"
    POSTMARK = "postmark"
    SES = "aws_ses"
    CUSTOM_API = "custom_api"

class RecipientType(str, Enum):
    ALL_USERS = "all_users"
    SUBSCRIPTION_TIER = "subscription_tier"
    CUSTOM_LIST = "custom_list"
    SINGLE_USER = "single_user"

# Models
class EmailTemplate(BaseModel):
    template_id: str
    name: str
    subject: str
    html_content: str
    text_content: str
    variables: List[str] = []  # Available variables like {{user_name}}, {{company}}
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

class EmailRecipient(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    user_id: Optional[str] = None
    variables: Dict[str, str] = {}  # Personalization variables

class SimpleBulkEmail(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    html_content: str = Field(..., min_length=10)
    text_content: Optional[str] = None
    recipient_type: RecipientType
    subscription_tiers: Optional[List[SubscriptionTier]] = None  # For subscription_tier type
    custom_emails: Optional[List[EmailStr]] = None  # For custom_list type
    single_email: Optional[EmailStr] = None  # For single_user type
    schedule_at: Optional[datetime] = None  # For scheduling
    template_id: Optional[str] = None  # Use existing template
    variables: Dict[str, str] = {}  # Global variables for all recipients

class EmailProviderConfig(BaseModel):
    provider: EmailProvider
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    domain: Optional[str] = None  # For Mailgun
    webhook_url: Optional[str] = None
    from_email: str = "noreply@customermindiq.com"
    from_name: str = "CustomerMind IQ"
    is_active: bool = True

class EmailCampaign(BaseModel):
    campaign_id: str
    name: str
    subject: str
    html_content: str
    text_content: Optional[str] = None
    recipient_count: int
    sent_count: int = 0
    delivered_count: int = 0
    opened_count: int = 0
    clicked_count: int = 0
    failed_count: int = 0
    status: EmailStatus
    provider: EmailProvider
    created_at: datetime
    sent_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None

# Trial Email Automation Models
class TrialEmailType(str, Enum):
    WELCOME = "welcome"           # Immediate
    PROGRESS_CHECK = "progress"   # Day 3
    URGENCY = "urgency"          # Day 5 (2 days before expiration)
    FINAL_NOTICE = "final"       # Day 7 (expiration day)

class TrialEmailStatus(str, Enum):
    SCHEDULED = "scheduled"
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"  # User converted before email sent

class TrialEmailLog(BaseModel):
    log_id: str
    user_email: str
    user_id: str
    first_name: str
    trial_start_date: datetime
    trial_end_date: datetime
    email_type: TrialEmailType
    subject: str
    html_content: str
    scheduled_send_time: datetime
    actual_send_time: Optional[datetime] = None
    status: TrialEmailStatus
    error_message: Optional[str] = None
    provider_used: EmailProvider
    created_at: datetime
    updated_at: datetime

# Email Provider Configurations
DEFAULT_EMAIL_PROVIDERS = {
    EmailProvider.SENDGRID: {
        "api_url": "https://api.sendgrid.com/v3/mail/send",
        "headers": {"Content-Type": "application/json"},
        "auth_header": "Authorization"
    },
    EmailProvider.MAILGUN: {
        "api_url": "https://api.mailgun.net/v3/{domain}/messages",
        "auth_type": "basic"
    },
    EmailProvider.RESEND: {
        "api_url": "https://api.resend.com/emails",
        "headers": {"Content-Type": "application/json"},
        "auth_header": "Authorization"
    },
    EmailProvider.POSTMARK: {
        "api_url": "https://api.postmarkapp.com/email",
        "headers": {"Content-Type": "application/json"},
        "auth_header": "X-Postmark-Server-Token"
    }
}

# Helper Functions
async def get_email_provider_config() -> EmailProviderConfig:
    """Get active email provider configuration"""
    config = await db.email_provider_config.find_one({"is_active": True})
    if config:
        del config["_id"]
        return EmailProviderConfig(**config)
    
    # Return default internal SMTP config
    return EmailProviderConfig(
        provider=EmailProvider.INTERNAL,
        from_email="noreply@customermindiq.com",
        from_name="CustomerMind IQ"
    )

async def get_recipients_by_type(recipient_type: RecipientType, **kwargs) -> List[EmailRecipient]:
    """Get recipients based on type"""
    recipients = []
    
    if recipient_type == RecipientType.ALL_USERS:
        # Get all active users
        users = await db.users.find({"is_active": True}).to_list(length=10000)
        for user in users:
            recipients.append(EmailRecipient(
                email=user["email"],
                name=user.get("first_name", ""),
                user_id=user["user_id"]
            ))
    
    elif recipient_type == RecipientType.SUBSCRIPTION_TIER:
        subscription_tiers = kwargs.get("subscription_tiers", [])
        if subscription_tiers:
            users = await db.users.find({
                "subscription_tier": {"$in": subscription_tiers},
                "is_active": True
            }).to_list(length=10000)
            for user in users:
                recipients.append(EmailRecipient(
                    email=user["email"], 
                    name=user.get("first_name", ""),
                    user_id=user["user_id"]
                ))
    
    elif recipient_type == RecipientType.CUSTOM_LIST:
        custom_emails = kwargs.get("custom_emails", [])
        for email in custom_emails:
            # Try to find user info
            user = await db.users.find_one({"email": email})
            recipients.append(EmailRecipient(
                email=email,
                name=user.get("first_name", "") if user else "",
                user_id=user.get("user_id") if user else None
            ))
    
    elif recipient_type == RecipientType.SINGLE_USER:
        single_email = kwargs.get("single_email")
        if single_email:
            user = await db.users.find_one({"email": single_email})
            recipients.append(EmailRecipient(
                email=single_email,
                name=user.get("first_name", "") if user else "",
                user_id=user.get("user_id") if user else None
            ))
    
    return recipients

def personalize_content(content: str, variables: Dict[str, str]) -> str:
    """Replace variables in content with actual values"""
    for key, value in variables.items():
        placeholder = f"{{{{ {key} }}}}"  # {{user_name}} format
        content = content.replace(placeholder, str(value))
    return content

async def send_via_provider(provider_config: EmailProviderConfig, to_email: str, subject: str, 
                           html_content: str, text_content: str = None) -> Dict[str, Any]:
    """Send email via configured provider"""
    
    # Check if ODOO integration is available and preferred
    try:
        from modules.odoo_integration import odoo_integration
        
        # Test if ODOO is connected and working
        if odoo_integration.connected or odoo_integration._connect():
            logger.info(f"Routing email to {to_email} through ODOO")
            success = odoo_integration.send_email(to_email, subject, html_content)
            return {
                "success": success,
                "provider_response": "odoo_integration",
                "provider": "odoo"
            }
    except Exception as odoo_error:
        logger.warning(f"ODOO email failed, falling back to configured provider: {str(odoo_error)}")
    
    # Fallback to configured provider
    if provider_config.provider == EmailProvider.SENDGRID:
        return await send_via_sendgrid(provider_config, to_email, subject, html_content, text_content)
    elif provider_config.provider == EmailProvider.MAILGUN:
        return await send_via_mailgun(provider_config, to_email, subject, html_content, text_content)
    elif provider_config.provider == EmailProvider.RESEND:
        return await send_via_resend(provider_config, to_email, subject, html_content, text_content)
    elif provider_config.provider == EmailProvider.POSTMARK:
        return await send_via_postmark(provider_config, to_email, subject, html_content, text_content)
    elif provider_config.provider == EmailProvider.INTERNAL:
        return await send_via_smtp(provider_config, to_email, subject, html_content, text_content)
    elif provider_config.provider == EmailProvider.CUSTOM_API:
        return await send_via_custom_api(provider_config, to_email, subject, html_content, text_content)
    else:
        return {"success": False, "error": f"Unsupported provider: {provider_config.provider}"}

async def send_via_sendgrid(config: EmailProviderConfig, to_email: str, subject: str, 
                           html_content: str, text_content: str = None) -> Dict[str, Any]:
    """Send email via SendGrid API"""
    try:
        payload = {
            "personalizations": [{
                "to": [{"email": to_email}],
                "subject": subject
            }],
            "from": {
                "email": config.from_email,
                "name": config.from_name
            },
            "content": [
                {"type": "text/html", "value": html_content}
            ]
        }
        
        if text_content:
            payload["content"].insert(0, {"type": "text/plain", "value": text_content})
        
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 202:
            return {"success": True, "provider_response": response.headers.get("X-Message-Id")}
        else:
            return {"success": False, "error": f"SendGrid error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": f"SendGrid exception: {str(e)}"}

async def send_via_mailgun(config: EmailProviderConfig, to_email: str, subject: str, 
                          html_content: str, text_content: str = None) -> Dict[str, Any]:
    """Send email via Mailgun API"""
    try:
        data = {
            "from": f"{config.from_name} <{config.from_email}>",
            "to": to_email,
            "subject": subject,
            "html": html_content
        }
        
        if text_content:
            data["text"] = text_content
        
        response = requests.post(
            f"https://api.mailgun.net/v3/{config.domain}/messages",
            auth=("api", config.api_key),
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {"success": True, "provider_response": result.get("id")}
        else:
            return {"success": False, "error": f"Mailgun error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": f"Mailgun exception: {str(e)}"}

async def send_via_resend(config: EmailProviderConfig, to_email: str, subject: str, 
                         html_content: str, text_content: str = None) -> Dict[str, Any]:
    """Send email via Resend API"""
    try:
        payload = {
            "from": f"{config.from_name} <{config.from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html_content
        }
        
        if text_content:
            payload["text"] = text_content
        
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.resend.com/emails",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {"success": True, "provider_response": result.get("id")}
        else:
            return {"success": False, "error": f"Resend error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": f"Resend exception: {str(e)}"}

async def send_via_postmark(config: EmailProviderConfig, to_email: str, subject: str, 
                           html_content: str, text_content: str = None) -> Dict[str, Any]:
    """Send email via Postmark API"""
    try:
        payload = {
            "From": f"{config.from_name} <{config.from_email}>",
            "To": to_email,
            "Subject": subject,
            "HtmlBody": html_content
        }
        
        if text_content:
            payload["TextBody"] = text_content
        
        headers = {
            "X-Postmark-Server-Token": config.api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.postmarkapp.com/email",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {"success": True, "provider_response": result.get("MessageID")}
        else:
            return {"success": False, "error": f"Postmark error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": f"Postmark exception: {str(e)}"}

async def send_via_custom_api(config: EmailProviderConfig, to_email: str, subject: str, 
                             html_content: str, text_content: str = None) -> Dict[str, Any]:
    """Send email via custom API endpoint"""
    try:
        # This allows integration with any custom email API
        payload = {
            "to": to_email,
            "from": config.from_email,
            "from_name": config.from_name,
            "subject": subject,
            "html_content": html_content,
            "text_content": text_content
        }
        
        headers = {"Content-Type": "application/json"}
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"
        
        # Use webhook_url as the custom API endpoint
        response = requests.post(
            config.webhook_url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code in [200, 201, 202]:
            return {"success": True, "provider_response": response.text}
        else:
            return {"success": False, "error": f"Custom API error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": f"Custom API exception: {str(e)}"}

async def send_via_smtp(config: EmailProviderConfig, to_email: str, subject: str, 
                       html_content: str, text_content: str = None) -> Dict[str, Any]:
    """Send email via internal SMTP (fallback)"""
    try:
        # For now, just log the email (in production, configure SMTP)
        email_log = {
            "to": to_email,
            "from": config.from_email,
            "subject": subject,
            "html_content": html_content,
            "text_content": text_content,
            "sent_at": datetime.utcnow(),
            "method": "smtp_fallback"
        }
        
        await db.email_logs.insert_one(email_log)
        return {"success": True, "provider_response": "logged_for_smtp"}
        
    except Exception as e:
        return {"success": False, "error": f"SMTP fallback exception: {str(e)}"}

# API Endpoints

@router.post("/email/send-simple")
async def send_simple_email(
    email_data: SimpleBulkEmail,
    background_tasks: BackgroundTasks,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Send simple email to customers - Easy method for admins"""
    
    campaign_id = str(uuid.uuid4())
    
    try:
        # Get email provider configuration
        provider_config = await get_email_provider_config()
        
        # Get recipients based on type
        recipients = await get_recipients_by_type(
            email_data.recipient_type,
            subscription_tiers=email_data.subscription_tiers,
            custom_emails=email_data.custom_emails,
            single_email=email_data.single_email
        )
        
        if not recipients:
            raise HTTPException(status_code=400, detail="No recipients found for the specified criteria")
        
        # Create campaign record
        campaign = {
            "campaign_id": campaign_id,
            "name": f"Simple Email - {email_data.subject[:50]}",
            "subject": email_data.subject,
            "html_content": email_data.html_content,
            "text_content": email_data.text_content,
            "recipient_count": len(recipients),
            "sent_count": 0,
            "delivered_count": 0,
            "opened_count": 0,
            "clicked_count": 0,
            "failed_count": 0,
            "status": EmailStatus.QUEUED,
            "provider": provider_config.provider,
            "created_at": datetime.utcnow(),
            "created_by": current_user.user_id,
            "scheduled_at": email_data.schedule_at
        }
        
        await db.email_campaigns.insert_one(campaign)
        
        # Queue emails for sending
        if email_data.schedule_at and email_data.schedule_at > datetime.utcnow():
            # Schedule for later
            return {
                "status": "success",
                "message": f"Email scheduled for {len(recipients)} recipients",
                "campaign_id": campaign_id,
                "recipient_count": len(recipients),
                "scheduled_at": email_data.schedule_at
            }
        else:
            # Send immediately in background
            background_tasks.add_task(
                process_email_campaign,
                campaign_id,
                recipients,
                email_data,
                provider_config
            )
            
            return {
                "status": "success", 
                "message": f"Email queued for {len(recipients)} recipients",
                "campaign_id": campaign_id,
                "recipient_count": len(recipients),
                "provider": provider_config.provider
            }
    
    except Exception as e:
        await db.email_campaigns.update_one(
            {"campaign_id": campaign_id},
            {"$set": {"status": EmailStatus.FAILED, "error": str(e)}}
        )
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

async def process_email_campaign(campaign_id: str, recipients: List[EmailRecipient], 
                                email_data: SimpleBulkEmail, provider_config: EmailProviderConfig):
    """Process email campaign sending (background task)"""
    
    sent_count = 0
    failed_count = 0
    
    # Update campaign status
    await db.email_campaigns.update_one(
        {"campaign_id": campaign_id},
        {"$set": {"status": EmailStatus.SENDING, "sent_at": datetime.utcnow()}}
    )
    
    for recipient in recipients:
        try:
            # Personalize content
            html_content = personalize_content(email_data.html_content, {
                "user_name": recipient.name or recipient.email.split("@")[0],
                "user_email": recipient.email,
                **email_data.variables,
                **recipient.variables
            })
            
            text_content = None
            if email_data.text_content:
                text_content = personalize_content(email_data.text_content, {
                    "user_name": recipient.name or recipient.email.split("@")[0],
                    "user_email": recipient.email,
                    **email_data.variables,
                    **recipient.variables
                })
            
            # Send email
            result = await send_via_provider(
                provider_config,
                recipient.email,
                email_data.subject,
                html_content,
                text_content
            )
            
            # Log email result
            email_log = {
                "campaign_id": campaign_id,
                "recipient_email": recipient.email,
                "subject": email_data.subject,
                "status": EmailStatus.SENT if result["success"] else EmailStatus.FAILED,
                "provider": provider_config.provider,
                "provider_response": result.get("provider_response"),
                "error": result.get("error"),
                "sent_at": datetime.utcnow()
            }
            
            await db.email_logs.insert_one(email_log)
            
            if result["success"]:
                sent_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            failed_count += 1
            # Log failed email
            await db.email_logs.insert_one({
                "campaign_id": campaign_id,
                "recipient_email": recipient.email,
                "status": EmailStatus.FAILED,
                "error": str(e),
                "sent_at": datetime.utcnow()
            })
    
    # Update campaign final status
    final_status = EmailStatus.SENT if sent_count > 0 else EmailStatus.FAILED
    await db.email_campaigns.update_one(
        {"campaign_id": campaign_id},
        {
            "$set": {
                "status": final_status,
                "sent_count": sent_count,
                "failed_count": failed_count
            }
        }
    )

@router.get("/email/campaigns")
async def get_email_campaigns(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get email campaigns history"""
    
    campaigns = await db.email_campaigns.find({}).sort("created_at", -1).skip(offset).limit(limit).to_list(length=limit)
    total_count = await db.email_campaigns.count_documents({})
    
    # Remove ObjectIds
    for campaign in campaigns:
        if "_id" in campaign:
            del campaign["_id"]
    
    return {
        "campaigns": campaigns,
        "total": total_count,
        "limit": limit,
        "offset": offset
    }

@router.get("/email/campaigns/{campaign_id}")
async def get_campaign_details(
    campaign_id: str,
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get detailed campaign information"""
    
    campaign = await db.email_campaigns.find_one({"campaign_id": campaign_id})
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get email logs for this campaign
    email_logs = await db.email_logs.find({"campaign_id": campaign_id}).sort("sent_at", -1).to_list(length=1000)
    
    # Remove ObjectIds
    del campaign["_id"]
    for log in email_logs:
        if "_id" in log:
            del log["_id"]
    
    return {
        "campaign": campaign,
        "email_logs": email_logs,
        "total_logs": len(email_logs)
    }

@router.post("/email/providers/configure")
async def configure_email_provider(
    provider_config: EmailProviderConfig,
    current_user: UserProfile = Depends(require_role([UserRole.SUPER_ADMIN]))
):
    """Configure email provider (super admin only)"""
    
    # Deactivate all existing providers
    await db.email_provider_config.update_many({}, {"$set": {"is_active": False}})
    
    # Insert new active provider
    config_doc = provider_config.dict()
    config_doc["created_at"] = datetime.utcnow()
    config_doc["created_by"] = current_user.user_id
    
    await db.email_provider_config.insert_one(config_doc)
    
    return {
        "status": "success",
        "message": f"Email provider configured: {provider_config.provider}",
        "provider": provider_config.provider
    }

@router.get("/email/providers/current")
async def get_current_email_provider(
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get current email provider configuration"""
    
    config = await get_email_provider_config()
    
    # Check ODOO integration status
    odoo_status = {"available": False, "connected": False}
    try:
        from modules.odoo_integration import odoo_integration
        odoo_status["available"] = True
        odoo_status["connected"] = odoo_integration.connected or odoo_integration._connect()
        if odoo_status["connected"]:
            odoo_status["message"] = "ODOO email integration active"
        else:
            odoo_status["message"] = "ODOO connection failed"
    except Exception as e:
        odoo_status["message"] = f"ODOO integration error: {str(e)}"
    
    # Hide sensitive information
    config_dict = config.dict()
    if config_dict.get("api_key"):
        config_dict["api_key"] = "***HIDDEN***"
    if config_dict.get("api_secret"):
        config_dict["api_secret"] = "***HIDDEN***"
    
    return {
        "provider_config": config_dict,
        "available_providers": [provider.value for provider in EmailProvider],
        "odoo_integration": odoo_status,
        "email_routing": "ODOO (preferred) -> Configured Provider (fallback)" if odoo_status["connected"] else "Configured Provider Only"
    }

@router.get("/email/stats")
async def get_email_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user: UserProfile = Depends(require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Get email statistics"""
    
    date_from = datetime.utcnow() - timedelta(days=days)
    
    # Get campaign statistics
    total_campaigns = await db.email_campaigns.count_documents({"created_at": {"$gte": date_from}})
    
    # Get email log statistics
    total_sent = await db.email_logs.count_documents({
        "sent_at": {"$gte": date_from},
        "status": EmailStatus.SENT
    })
    
    total_failed = await db.email_logs.count_documents({
        "sent_at": {"$gte": date_from},
        "status": EmailStatus.FAILED
    })
    
    # Calculate delivery rate
    delivery_rate = (total_sent / (total_sent + total_failed) * 100) if (total_sent + total_failed) > 0 else 0
    
    return {
        "period_days": days,
        "statistics": {
            "total_campaigns": total_campaigns,
            "total_emails_sent": total_sent,
            "total_emails_failed": total_failed,
            "delivery_rate_percent": round(delivery_rate, 2)
        }
    }

# ==============================================================================
# TRIAL EMAIL AUTOMATION SYSTEM
# ==============================================================================

# Email Templates for Trial Automation
TRIAL_EMAIL_TEMPLATES = {
    TrialEmailType.WELCOME: {
        "subject": "Your CustomerMindIQ trial is active - Start here (5 minutes to first insights)",
        "html_template": """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <img src="https://customer-assets.emergentagent.com/job_customer-mind-iq-4/artifacts/pntu3yqm_Customer%20Mind%20IQ%20logo.png" 
                     alt="Customer Mind IQ" 
                     style="height: 80px; width: auto; margin-bottom: 20px; object-fit: contain;" />
                <h1 style="color: white; margin: 0; font-size: 28px;">Welcome to CustomerMind IQ!</h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin: 10px 0 0 0;">Your 7-day free trial just started</p>
            </div>
            
            <div style="padding: 30px; background: white;">
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-bottom: 20px;">Hi <strong>{first_name}</strong>,</p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    Welcome to CustomerMindIQ! Your 7-day free trial just started, and I want to make sure you get maximum value from every single day.
                </p>
                
                <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #1976d2; margin: 0 0 10px 0;">🔑 Your login details:</h3>
                    <p style="margin: 5px 0; color: #333;"><strong>Dashboard:</strong> CustomerMindIQ.com/dashboard</p>
                    <p style="margin: 5px 0; color: #333;"><strong>Username:</strong> {email}</p>
                    <p style="margin: 5px 0; color: #333;"><strong>Password:</strong> {password}</p>
                </div>
                
                <h3 style="color: #333; margin: 25px 0 15px 0;">🚀 Here's exactly what to do in your first 10 minutes:</h3>
                <ol style="font-size: 16px; line-height: 1.6; color: #333; padding-left: 20px;">
                    <li><strong>Connect your first data source</strong> (Google Analytics, your CRM, or email platform)</li>
                    <li><strong>Check the Customer Health Dashboard</strong> - see which customers might be at risk</li>
                    <li><strong>Run the Revenue Leak Detection</strong> - find money you're losing right now</li>
                </ol>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin: 20px 0;">
                    I built CustomerMindIQ because I was drowning in spreadsheets and couldn't see the big picture of my business. Within your first hour, you should start seeing patterns in your data that weren't visible before.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://customermindiq.com/dashboard" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                        🚀 Start Exploring Your Dashboard
                    </a>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    <strong>Need help?</strong> Reply to this email or use the chat support in your dashboard. I personally read every message and often respond myself.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    <strong>A quick promise:</strong> No credit card charges until you specifically choose to continue. No fake urgency tactics. Just honest software that either proves its value or it doesn't.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    Your trial clock started when you signed up, so don't wait - dive in and start exploring.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-top: 30px;">
                    <strong>Questions about anything?</strong> Just hit reply.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-top: 20px;">
                    Best,<br>
                    <strong>Jim</strong><br>
                    Founder, CustomerMindIQ
                </p>
                
                <p style="font-size: 14px; line-height: 1.5; color: #666; margin-top: 20px; font-style: italic;">
                    P.S. If you run into any bugs or have suggestions, please tell me immediately. We fix issues fast and actually listen to user feedback.
                </p>
            </div>
        </div>
        """
    },
    
    TrialEmailType.PROGRESS_CHECK: {
        "subject": "How's your CustomerMindIQ trial going? (Plus a quick favor)",
        "html_template": """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                <img src="https://customer-assets.emergentagent.com/job_customer-mind-iq-4/artifacts/pntu3yqm_Customer%20Mind%20IQ%20logo.png" 
                     alt="Customer Mind IQ" 
                     style="height: 80px; width: auto; margin-bottom: 20px; object-fit: contain;" />
                <h1 style="color: white; margin: 0; font-size: 28px;">How's your trial going?</h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin: 10px 0 0 0;">You're halfway through!</p>
            </div>
            
            <div style="padding: 30px; background: white;">
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-bottom: 20px;">Hi <strong>{first_name}</strong>,</p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    You're halfway through your CustomerMindIQ trial - how's it going so far?
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    I'm hoping you've had a chance to connect some data sources and explore the dashboards. If you haven't yet, you're missing out on the best part of your trial.
                </p>
                
                <div style="background: #fff3e0; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #f57c00; margin: 0 0 15px 0;">🎯 Quick check: Have you tried these game-changing features yet?</h3>
                    <ul style="font-size: 16px; line-height: 1.8; color: #333; margin: 0; padding-left: 20px;">
                        <li><strong>Churn Prediction</strong> - See which customers need attention before they leave</li>
                        <li><strong>Revenue Forecasting</strong> - Get surprisingly accurate predictions 3-6 months out</li>
                        <li><strong>Marketing Automation</strong> - Set up campaigns that run themselves</li>
                        <li><strong>Competitive Intelligence</strong> - See what your competitors are doing</li>
                    </ul>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong>💡 The most successful trial users spend 20-30 minutes exploring these features.</strong> The insights usually pay for the subscription in the first month.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    <strong>Here's my quick favor:</strong> If you've found something valuable (or confusing) in CustomerMindIQ, would you mind replying to tell me about it? I read every response and use feedback to improve the platform.
                </p>
                
                <div style="background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #7b1fa2; margin: 0 0 10px 0;">🆘 Still have questions?</h3>
                    <ul style="font-size: 16px; line-height: 1.6; color: #333; margin: 0; padding-left: 20px;">
                        <li>Reply to this email (I actually respond)</li>
                        <li>Use in-app chat for immediate help</li>
                        <li>Book a 15-minute walkthrough if you want personalized guidance</li>
                    </ul>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; text-align: center; background: #ffebee; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    ⏰ <strong>You have 4 days left in your trial. Make them count.</strong>
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-top: 30px;">
                    Best,<br>
                    <strong>Jim</strong><br>
                    Founder, CustomerMindIQ
                </p>
                
                <p style="font-size: 14px; line-height: 1.5; color: #666; margin-top: 20px; font-style: italic;">
                    P.S. Annual subscribers get our Growth Acceleration Engine (normally $249/month) completely free with ALL plans - even Launch. Just saying.
                </p>
            </div>
        </div>
        """
    },
    
    TrialEmailType.URGENCY: {
        "subject": "Your CustomerMindIQ trial expires in 48 hours - Don't lose your data",
        "html_template": """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa;">
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px;">⏰ 48 Hours Left!</h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin: 10px 0 0 0;">Don't lose your progress</p>
            </div>
            
            <div style="padding: 30px; background: white;">
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-bottom: 20px;">Hi <strong>{first_name}</strong>,</p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    Your CustomerMindIQ trial expires in 48 hours, and I don't want you to lose access to all the insights you've been building.
                </p>
                
                <div style="background: #ffebee; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f44336;">
                    <h3 style="color: #d32f2f; margin: 0 0 15px 0;">⚠️ Here's what happens when your trial ends:</h3>
                    <ul style="font-size: 16px; line-height: 1.6; color: #333; margin: 0; padding-left: 20px;">
                        <li>Your dashboards become view-only</li>
                        <li>Data connections stop syncing</li>
                        <li>You lose access to AI recommendations</li>
                        <li>All your configured alerts and automations pause</li>
                    </ul>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    <strong>But here's what I really don't want you to lose:</strong> The revenue opportunities CustomerMindIQ has identified for your business.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong>Quick question:</strong> Have you discovered any potential revenue leaks or growth opportunities during your trial? Most users find $5,000-$50,000 in previously hidden opportunities in their first week.
                </p>
                
                <h3 style="color: #333; margin: 25px 0 15px 0;">💰 If CustomerMindIQ has shown you something valuable, here's how to continue:</h3>
                
                <div style="display: grid; gap: 15px; margin: 20px 0;">
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #1976d2; margin: 0 0 10px 0;">📈 Monthly Plans:</h4>
                        <ul style="margin: 0; padding-left: 20px; font-size: 15px; line-height: 1.5;">
                            <li>Launch: $49/month (normally $99)</li>
                            <li>Growth: $75/month (normally $149)</li>
                            <li>Scale: $199/month (normally $399)</li>
                        </ul>
                    </div>
                    
                    <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; border: 2px solid #4caf50;">
                        <h4 style="color: #2e7d32; margin: 0 0 10px 0;">🎁 Annual Plans (Best Value - 12 months for the price of 10):</h4>
                        <ul style="margin: 0; padding-left: 20px; font-size: 15px; line-height: 1.5;">
                            <li><strong>Launch Annual:</strong> $49/month → $41/month + <span style="color: #ff6b6b;"><strong>$3,000 Growth Engine bonus</strong></span></li>
                            <li><strong>Growth Annual:</strong> $75/month → $62.50/month + <span style="color: #ff6b6b;"><strong>$3,000 Growth Engine bonus</strong></span></li>
                            <li><strong>Scale Annual:</strong> $199/month → $166/month + <span style="color: #ff6b6b;"><strong>$3,000 Growth Engine bonus</strong></span></li>
                        </ul>
                    </div>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong>💡 The Growth Acceleration Engine</strong> (included free with ALL annual plans) typically finds 15-25% additional revenue opportunities within the first 6 months.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://customermindiq.com/dashboard" style="background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); color: white; padding: 18px 40px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block; font-size: 18px;">
                        🚀 Continue Your Subscription
                    </a>
                    <p style="font-size: 14px; color: #666; margin: 10px 0 0 0;">Log in to your dashboard and click "Upgrade Account" - it takes 2 minutes</p>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    <strong>Still have questions?</strong> Reply to this email or schedule a quick call to discuss which plan fits your business best.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; text-align: center; background: #ffebee; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    ⚡ <strong>Don't let 48 hours of momentum go to waste.</strong>
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-top: 30px;">
                    Best,<br>
                    <strong>Jim</strong><br>
                    Founder, CustomerMindIQ
                </p>
                
                <p style="font-size: 14px; line-height: 1.5; color: #666; margin-top: 20px; font-style: italic;">
                    P.S. We're still brand new, so you're getting founder's pricing that won't be available much longer. Lock it in now.
                </p>
            </div>
        </div>
        """
    },
    
    TrialEmailType.FINAL_NOTICE: {
        "subject": "FINAL NOTICE: Your CustomerMindIQ trial expires today",
        "html_template": """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa;">
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px;">🚨 FINAL NOTICE</h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin: 10px 0 0 0;">Your trial expires today</p>
            </div>
            
            <div style="padding: 30px; background: white;">
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-bottom: 20px;">Hi <strong>{first_name}</strong>,</p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    Your CustomerMindIQ trial expires today at midnight, and I wanted to reach out personally one last time.
                </p>
                
                <div style="background: #ffebee; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f44336;">
                    <h3 style="color: #d32f2f; margin: 0 0 15px 0;">💔 Here's what you're about to lose access to:</h3>
                    <ul style="font-size: 16px; line-height: 1.6; color: #333; margin: 0; padding-left: 20px;">
                        <li>All the customer insights you've been building</li>
                        <li>Revenue leak detection that could be saving you thousands monthly</li>
                        <li>Churn prediction alerts for at-risk customers</li>
                        <li>Marketing automation workflows you've set up</li>
                        <li>Real-time business intelligence that gives you a competitive edge</li>
                    </ul>
                </div>
                
                <h3 style="color: #333; margin: 25px 0 15px 0;">🚀 But more importantly, here's what you'll miss out on going forward:</h3>
                
                <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="font-size: 16px; line-height: 1.6; color: #333; margin: 0 0 15px 0;"><strong>If you continue with CustomerMindIQ, you'll have:</strong></p>
                    <ul style="font-size: 16px; line-height: 1.8; color: #333; margin: 0; padding-left: 20px;">
                        <li>✓ A unified view of your entire business (no more tool-switching)</li>
                        <li>✓ AI that gets smarter about your business every month</li>
                        <li>✓ Predictive insights that help you stay ahead of problems</li>
                        <li>✓ Automated systems that save 20+ hours weekly</li>
                        <li>✓ Growth opportunities identified before your competition finds them</li>
                    </ul>
                </div>
                
                <div style="background: #fff3e0; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #ff9800;">
                    <h3 style="color: #f57c00; margin: 0 0 15px 0;">🎁 Plus, if you choose an annual plan today, you get:</h3>
                    <ul style="font-size: 16px; line-height: 1.8; color: #333; margin: 0; padding-left: 20px;">
                        <li>✓ <strong>$3,000 Growth Acceleration Engine</strong> - completely free with ANY plan (Launch, Growth, or Scale)</li>
                        <li>✓ <strong>12 months for the price of 10</strong> (2 months free)</li>
                        <li>✓ <strong>Locked-in founder's pricing</strong> (prices increase as we scale)</li>
                        <li>✓ <strong>Priority support</strong> and feature requests</li>
                    </ul>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong>💰 The Growth Acceleration Engine alone typically pays for your entire annual subscription</strong> within 3-4 months through the revenue opportunities it identifies.
                </p>
                
                <div style="background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #7b1fa2; margin: 0 0 15px 0;">⚡ Continue your subscription in 2 minutes:</h3>
                    <ol style="font-size: 16px; line-height: 1.6; color: #333; margin: 0; padding-left: 20px;">
                        <li>Log in to CustomerMindIQ.com/dashboard</li>
                        <li>Click "Upgrade Account"</li>
                        <li>Choose your plan and enter payment details</li>
                        <li>Keep all your data and momentum</li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://customermindiq.com/upgrade" style="background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); color: white; padding: 20px 50px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block; font-size: 20px;">
                        🎯 Upgrade Now - Keep Growing!
                    </a>
                </div>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    <strong>Or, if CustomerMindIQ isn't the right fit,</strong> that's okay too. Thanks for giving us a fair trial. Your account will automatically close at midnight with no charges.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    <strong>Last chance questions?</strong> Reply to this email - I'm personally monitoring responses today.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-top: 30px;">
                    Thanks for trying CustomerMindIQ. Whether you continue or not, I appreciate the opportunity to show you what we've built.
                </p>
                
                <p style="font-size: 16px; line-height: 1.6; color: #333; margin-top: 20px;">
                    Best,<br>
                    <strong>Jim</strong><br>
                    Founder, CustomerMindIQ
                </p>
                
                <p style="font-size: 14px; line-height: 1.5; color: #666; margin-top: 20px; font-style: italic;">
                    P.S. This is genuinely your last email from me unless you choose to continue. No annoying follow-ups or win-back campaigns. Just honest communication, which is how we do business.
                </p>
            </div>
        </div>
        """
    }
}

async def schedule_trial_email_sequence(user_email: str, user_id: str, first_name: str, trial_start_date: datetime, trial_end_date: datetime, login_password: Optional[str] = None):
    """Schedule the complete 4-email trial sequence for a new trial user"""
    try:
        logger.info(f"Scheduling trial email sequence for user: {user_email}")
        
        # Email scheduling timeline
        email_schedule = {
            TrialEmailType.WELCOME: trial_start_date,  # Immediate
            TrialEmailType.PROGRESS_CHECK: trial_start_date + timedelta(days=3),  # Day 3
            TrialEmailType.URGENCY: trial_start_date + timedelta(days=5),  # Day 5 (2 days before expiration)
            TrialEmailType.FINAL_NOTICE: trial_end_date  # Day 7 (expiration day)
        }
        
        # Create email log entries for each email in the sequence
        for email_type, send_time in email_schedule.items():
            template = TRIAL_EMAIL_TEMPLATES[email_type]
            
            # Personalize the email content
            html_content = template["html_template"].format(
                first_name=first_name,
                email=user_email,
                password=login_password or "[Set in your account]",
                trial_start_date=trial_start_date.strftime("%B %d, %Y"),
                trial_end_date=trial_end_date.strftime("%B %d, %Y")
            )
            
            email_log = {
                "log_id": str(uuid.uuid4()),
                "user_email": user_email,
                "user_id": user_id,
                "first_name": first_name,
                "trial_start_date": trial_start_date,
                "trial_end_date": trial_end_date,
                "email_type": email_type.value,
                "subject": template["subject"],
                "html_content": html_content,
                "scheduled_send_time": send_time,
                "actual_send_time": None,
                "status": TrialEmailStatus.SCHEDULED.value,
                "error_message": None,
                "provider_used": EmailProvider.INTERNAL.value,  # Will be updated when sent
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Store in database
            await db.trial_email_logs.insert_one(email_log)
            
            # Send welcome email immediately
            if email_type == TrialEmailType.WELCOME:
                await send_trial_email_now(email_log["log_id"])
        
        logger.info(f"Trial email sequence scheduled successfully for {user_email}")
        return {"status": "success", "message": f"Trial email sequence scheduled for {user_email}"}
        
    except Exception as e:
        logger.error(f"Error scheduling trial email sequence for {user_email}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to schedule trial emails: {str(e)}")

async def send_trial_email_now(log_id: str):
    """Send a specific trial email immediately"""
    try:
        # Get the email log
        email_log = await db.trial_email_logs.find_one({"log_id": log_id})
        if not email_log:
            raise HTTPException(status_code=404, detail="Email log not found")
        
        # Check if already sent
        if email_log["status"] == TrialEmailStatus.SENT.value:
            return {"status": "already_sent", "message": "Email already sent"}
        
        # Prepare email data
        email_data = {
            "subject": email_log["subject"],
            "html_content": email_log["html_content"],
            "text_content": "Please view this email in HTML format.",
            "recipient_type": RecipientType.SINGLE_USER,
            "single_email": email_log["user_email"],
            "schedule_at": None,  # Send immediately
            "variables": {}
        }
        
        # Send the email using existing send system
        result = await send_simple_email(SimpleBulkEmail(**email_data), background_tasks=None, current_user=None)
        
        # Update the log
        update_data = {
            "actual_send_time": datetime.utcnow(),
            "status": TrialEmailStatus.SENT.value if result["status"] == "success" else TrialEmailStatus.FAILED.value,
            "error_message": result.get("error") if result["status"] != "success" else None,
            "updated_at": datetime.utcnow()
        }
        
        await db.trial_email_logs.update_one(
            {"log_id": log_id},
            {"$set": update_data}
        )
        
        logger.info(f"Trial email sent successfully: {log_id}")
        return {"status": "success", "message": "Trial email sent successfully"}
        
    except Exception as e:
        logger.error(f"Error sending trial email {log_id}: {str(e)}")
        # Update log with error
        await db.trial_email_logs.update_one(
            {"log_id": log_id},
            {"$set": {
                "status": TrialEmailStatus.FAILED.value,
                "error_message": str(e),
                "updated_at": datetime.utcnow()
            }}
        )
        raise HTTPException(status_code=500, detail=f"Failed to send trial email: {str(e)}")

# Background task to process scheduled trial emails
async def process_scheduled_trial_emails():
    """Background task to send scheduled trial emails"""
    try:
        current_time = datetime.utcnow()
        
        # Find emails that are scheduled to be sent now or in the past
        scheduled_emails = await db.trial_email_logs.find({
            "status": TrialEmailStatus.SCHEDULED.value,
            "scheduled_send_time": {"$lte": current_time}
        }).to_list(length=None)
        
        for email_log in scheduled_emails:
            # Check if user has already converted (skip remaining emails)
            user = await db.users.find_one({"email": email_log["user_email"]})
            if user and not user.get("is_trial", True):  # User is no longer on trial
                # Mark remaining emails as skipped
                await db.trial_email_logs.update_one(
                    {"log_id": email_log["log_id"]},
                    {"$set": {
                        "status": TrialEmailStatus.SKIPPED.value,
                        "error_message": "User converted before email was sent",
                        "updated_at": datetime.utcnow()
                    }}
                )
                logger.info(f"Skipped trial email for converted user: {email_log['user_email']}")
                continue
            
            # Send the email
            try:
                await send_trial_email_now(email_log["log_id"])
                logger.info(f"Processed scheduled trial email: {email_log['log_id']}")
            except Exception as e:
                logger.error(f"Failed to process trial email {email_log['log_id']}: {str(e)}")
        
        logger.info(f"Processed {len(scheduled_emails)} scheduled trial emails")
        
    except Exception as e:
        logger.error(f"Error processing scheduled trial emails: {str(e)}")

# ==============================================================================
# TRIAL EMAIL AUTOMATION API ENDPOINTS
# ==============================================================================

@router.post("/email/trial/schedule")
async def api_schedule_trial_email_sequence(
    user_email: str,
    user_id: str,
    first_name: str,
    trial_start_date: datetime,
    trial_end_date: datetime,
    login_password: Optional[str] = None
):
    """API endpoint to schedule trial email sequence"""
    return await schedule_trial_email_sequence(
        user_email, user_id, first_name, trial_start_date, trial_end_date, login_password
    )

@router.post("/email/trial/send/{log_id}")
async def api_send_trial_email_now(log_id: str):
    """API endpoint to send a trial email immediately"""
    return await send_trial_email_now(log_id)

@router.get("/email/trial/logs")
async def get_trial_email_logs(
    user_email: Optional[str] = Query(None),
    email_type: Optional[TrialEmailType] = Query(None),
    status: Optional[TrialEmailStatus] = Query(None),
    limit: int = Query(50, ge=1, le=200)
):
    """Get trial email logs - Admin can see all emails sent"""
    try:
        # Build query
        query = {}
        if user_email:
            query["user_email"] = user_email
        if email_type:
            query["email_type"] = email_type.value
        if status:
            query["status"] = status.value
        
        # Get logs
        logs = await db.trial_email_logs.find(query).sort("created_at", -1).limit(limit).to_list(length=None)
        
        # Convert ObjectId to string for JSON serialization
        for log in logs:
            log["_id"] = str(log["_id"])
        
        return {
            "status": "success",
            "total": len(logs),
            "logs": logs
        }
        
    except Exception as e:
        logger.error(f"Error fetching trial email logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch trial email logs: {str(e)}")

@router.get("/email/trial/stats")
async def get_trial_email_stats():
    """Get trial email statistics for admin dashboard"""
    try:
        # Get overall stats
        total_logs = await db.trial_email_logs.count_documents({})
        sent_count = await db.trial_email_logs.count_documents({"status": TrialEmailStatus.SENT.value})
        failed_count = await db.trial_email_logs.count_documents({"status": TrialEmailStatus.FAILED.value})
        scheduled_count = await db.trial_email_logs.count_documents({"status": TrialEmailStatus.SCHEDULED.value})
        skipped_count = await db.trial_email_logs.count_documents({"status": TrialEmailStatus.SKIPPED.value})
        
        # Get stats by email type
        type_stats = {}
        for email_type in TrialEmailType:
            type_count = await db.trial_email_logs.count_documents({"email_type": email_type.value})
            type_sent = await db.trial_email_logs.count_documents({
                "email_type": email_type.value,
                "status": TrialEmailStatus.SENT.value
            })
            type_stats[email_type.value] = {
                "total": type_count,
                "sent": type_sent,
                "success_rate": round((type_sent / type_count * 100) if type_count > 0 else 0, 2)
            }
        
        # Calculate overall success rate
        success_rate = round((sent_count / total_logs * 100) if total_logs > 0 else 0, 2)
        
        return {
            "status": "success",
            "overall_stats": {
                "total_emails": total_logs,
                "sent": sent_count,
                "failed": failed_count,
                "scheduled": scheduled_count,
                "skipped": skipped_count,
                "success_rate_percent": success_rate
            },
            "stats_by_type": type_stats
        }
        
    except Exception as e:
        logger.error(f"Error fetching trial email stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch trial email stats: {str(e)}")

@router.post("/email/trial/process-scheduled")
async def api_process_scheduled_trial_emails():
    """Manual trigger to process scheduled trial emails (for testing/admin use)"""
    try:
        await process_scheduled_trial_emails()
        return {"status": "success", "message": "Scheduled trial emails processed"}
    except Exception as e:
        logger.error(f"Error processing scheduled emails: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process scheduled emails: {str(e)}")