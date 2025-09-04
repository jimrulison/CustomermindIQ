"""
Customer Mind IQ - Email Provider API Routes
FastAPI routes for unified email management
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

from .email_manager import email_manager, ProviderType
from .base_provider import Contact, EmailTemplate, Campaign, EmailAnalytics
from auth.auth_system import require_role, UserProfile

router = APIRouter(prefix="/api/email-providers", tags=["Email Providers"])

# Pydantic Models for API
class ContactCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

class TemplateCreate(BaseModel):
    name: str
    subject: str
    html_content: str
    text_content: Optional[str] = None
    from_name: str = "Customer Mind IQ"
    from_email: str = "hello@customermindiq.com"
    reply_to: Optional[str] = None

class CampaignCreate(BaseModel):
    name: str
    template_id: Optional[str] = None
    subject: str
    html_content: str
    text_content: Optional[str] = None
    from_name: str = "Customer Mind IQ"
    from_email: str = "hello@customermindiq.com"
    reply_to: Optional[str] = None
    recipient_list: Optional[List[str]] = None
    schedule_time: Optional[datetime] = None

class TransactionalEmail(BaseModel):
    to_email: EmailStr
    subject: str
    html_content: str
    text_content: Optional[str] = None
    from_name: Optional[str] = None
    from_email: Optional[str] = None
    personalization: Optional[Dict[str, Any]] = None
    provider_name: Optional[str] = None

class ProviderConfig(BaseModel):
    provider_type: str
    config: Dict[str, Any]
    is_default: bool = False

# Provider Management Routes
@router.post("/providers/register")
async def register_provider(
    provider_config: ProviderConfig,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Register a new email provider"""
    try:
        provider_type = ProviderType(provider_config.provider_type)
        success = await email_manager.register_provider(
            provider_type=provider_type,
            config=provider_config.config,
            is_default=provider_config.is_default
        )
        
        if success:
            return {"status": "success", "message": f"Provider {provider_config.provider_type} registered successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to register provider")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid provider type: {provider_config.provider_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers/status")
async def get_provider_status(
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Get status of all registered providers"""
    try:
        return await email_manager.get_provider_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers/health-check")
async def health_check_providers(
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Perform health check on all providers"""
    try:
        return await email_manager.health_check_all_providers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers/optimal")
async def get_optimal_provider(
    criteria: str = "health",
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Get optimal provider based on criteria"""
    try:
        optimal_provider = await email_manager.get_optimal_provider(criteria)
        return {"optimal_provider": optimal_provider}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact Management Routes
@router.post("/contacts")
async def create_contact(
    contact: ContactCreate,
    provider_name: Optional[str] = None,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Create a new contact"""
    try:
        contact_obj = Contact(
            email=contact.email,
            first_name=contact.first_name,
            last_name=contact.last_name,
            company=contact.company,
            phone=contact.phone,
            custom_fields=contact.custom_fields,
            tags=contact.tags
        )
        
        result = await email_manager.create_contact(contact_obj, provider_name)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/contacts/{email}")
async def update_contact(
    email: str,
    updates: ContactUpdate,
    provider_name: Optional[str] = None,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Update existing contact"""
    try:
        update_dict = {k: v for k, v in updates.dict().items() if v is not None}
        result = await email_manager.update_contact(email, update_dict, provider_name)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contacts/{email}")
async def get_contact(
    email: str,
    provider_name: Optional[str] = None,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Get contact by email"""
    try:
        contact = await email_manager.get_contact(email, provider_name)
        if contact:
            return {"status": "success", "data": contact}
        else:
            raise HTTPException(status_code=404, detail="Contact not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/contacts/{email}/sync")
async def sync_contact_across_providers(
    email: str,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Sync contact across all providers"""
    try:
        # First get the contact
        contact = await email_manager.get_contact(email)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
            
        results = await email_manager.sync_contact_across_providers(contact)
        return {"status": "success", "sync_results": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Transactional Email Routes
@router.post("/send-transactional")
async def send_transactional_email(
    email_data: TransactionalEmail,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Send transactional email"""
    try:
        result = await email_manager.send_transactional(
            to_email=email_data.to_email,
            subject=email_data.subject,
            html_content=email_data.html_content,
            text_content=email_data.text_content,
            from_name=email_data.from_name,
            from_email=email_data.from_email,
            personalization=email_data.personalization,
            provider_name=email_data.provider_name
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-with-failover")
async def send_with_failover(
    email_data: TransactionalEmail,
    provider_priority: Optional[List[str]] = None,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Send email with automatic failover between providers"""
    try:
        result = await email_manager.send_with_failover(
            to_email=email_data.to_email,
            subject=email_data.subject,
            html_content=email_data.html_content,
            text_content=email_data.text_content,
            from_name=email_data.from_name,
            from_email=email_data.from_email,
            provider_priority=provider_priority
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics Routes
@router.get("/analytics/campaign/{campaign_id}")
async def get_campaign_analytics(
    campaign_id: str,
    provider_name: Optional[str] = None,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Get campaign analytics"""
    try:
        analytics = await email_manager.get_campaign_analytics(campaign_id, provider_name)
        return {"status": "success", "data": analytics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/aggregated")
async def get_aggregated_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Get aggregated analytics across all providers"""
    try:
        # Default to last 30 days if no dates provided
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = end_date - timedelta(days=30)
            
        analytics = await email_manager.get_aggregated_analytics(start_date, end_date)
        return {"status": "success", "data": analytics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test Routes
@router.post("/test/send-test-email")
async def send_test_email(
    to_email: EmailStr,
    provider_name: Optional[str] = None,
    current_user: UserProfile = Depends(require_role(['admin', 'super_admin']))
):
    """Send test email to verify provider functionality"""
    try:
        html_content = """
        <html>
        <body>
            <h2>Customer Mind IQ Email Provider Test</h2>
            <p>This is a test email to verify email provider functionality.</p>
            <p>Provider: <strong>{provider}</strong></p>
            <p>Timestamp: <strong>{timestamp}</strong></p>
            <p>If you received this email, the provider is working correctly!</p>
        </body>
        </html>
        """.format(
            provider=provider_name or "Default",
            timestamp=datetime.now().isoformat()
        )
        
        result = await email_manager.send_transactional(
            to_email=to_email,
            subject="Customer Mind IQ - Email Provider Test",
            html_content=html_content,
            text_content="Customer Mind IQ Email Provider Test - If you received this email, the provider is working correctly!",
            provider_name=provider_name
        )
        
        return {"status": "success", "message": "Test email sent successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))