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