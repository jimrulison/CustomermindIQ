"""
Customer Mind IQ - Email Provider Base Interface
Unified interface for all email service providers
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EmailStatus(Enum):
    """Email delivery status enumeration"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    BOUNCED = "bounced"
    FAILED = "failed"
    UNSUBSCRIBED = "unsubscribed"

class CampaignStatus(Enum):
    """Campaign status enumeration"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Contact:
    """Universal contact data structure"""
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    subscribed: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class EmailTemplate:
    """Universal email template structure"""
    template_id: Optional[str] = None
    name: str = ""
    subject: str = ""
    html_content: str = ""
    text_content: Optional[str] = None
    preview_text: Optional[str] = None
    from_name: str = "Customer Mind IQ"
    from_email: str = "hello@customermindiq.com"
    reply_to: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Campaign:
    """Universal campaign structure"""
    campaign_id: Optional[str] = None
    name: str = ""
    template_id: Optional[str] = None
    subject: str = ""
    html_content: str = ""
    text_content: Optional[str] = None
    from_name: str = "Customer Mind IQ"
    from_email: str = "hello@customermindiq.com"
    reply_to: Optional[str] = None
    recipient_list: Optional[List[str]] = None
    schedule_time: Optional[datetime] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class EmailAnalytics:
    """Universal email analytics structure"""
    total_sent: int = 0
    delivered: int = 0
    bounced: int = 0
    opened: int = 0
    clicked: int = 0
    unsubscribed: int = 0
    complaints: int = 0
    open_rate: float = 0.0
    click_rate: float = 0.0
    bounce_rate: float = 0.0
    unsubscribe_rate: float = 0.0
    delivery_rate: float = 0.0

class BaseEmailProvider(ABC):
    """
    Abstract base class for all email service providers
    Defines the unified interface that all providers must implement
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize provider with configuration"""
        self.config = config
        self.provider_name = self.__class__.__name__.replace('Provider', '').lower()
        self.is_authenticated = False
        
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the email provider"""
        pass
        
    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection and return provider status"""
        pass
    
    # Contact Management
    @abstractmethod
    async def create_contact(self, contact: Contact) -> Dict[str, Any]:
        """Create a new contact"""
        pass
        
    @abstractmethod
    async def update_contact(self, email: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing contact"""
        pass
        
    @abstractmethod
    async def get_contact(self, email: str) -> Optional[Contact]:
        """Retrieve contact by email"""
        pass
        
    @abstractmethod
    async def delete_contact(self, email: str) -> bool:
        """Delete contact"""
        pass
        
    @abstractmethod
    async def get_contacts(self, limit: int = 100, offset: int = 0) -> List[Contact]:
        """Get list of contacts"""
        pass
    
    # List Management
    @abstractmethod
    async def create_list(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create email list"""
        pass
        
    @abstractmethod
    async def add_contact_to_list(self, list_id: str, email: str) -> bool:
        """Add contact to list"""
        pass
        
    @abstractmethod
    async def remove_contact_from_list(self, list_id: str, email: str) -> bool:
        """Remove contact from list"""
        pass
    
    # Template Management
    @abstractmethod
    async def create_template(self, template: EmailTemplate) -> Dict[str, Any]:
        """Create email template"""
        pass
        
    @abstractmethod
    async def update_template(self, template_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update email template"""
        pass
        
    @abstractmethod
    async def get_template(self, template_id: str) -> Optional[EmailTemplate]:
        """Get email template"""
        pass
        
    @abstractmethod
    async def delete_template(self, template_id: str) -> bool:
        """Delete email template"""
        pass
        
    @abstractmethod
    async def get_templates(self, limit: int = 50) -> List[EmailTemplate]:
        """Get list of templates"""
        pass
    
    # Campaign Management
    @abstractmethod
    async def create_campaign(self, campaign: Campaign) -> Dict[str, Any]:
        """Create email campaign"""
        pass
        
    @abstractmethod
    async def send_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Send campaign"""
        pass
        
    @abstractmethod
    async def schedule_campaign(self, campaign_id: str, schedule_time: datetime) -> Dict[str, Any]:
        """Schedule campaign for later sending"""
        pass
        
    @abstractmethod
    async def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause campaign"""
        pass
        
    @abstractmethod
    async def cancel_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Cancel campaign"""
        pass
        
    @abstractmethod
    async def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get campaign details"""
        pass
        
    @abstractmethod
    async def get_campaigns(self, limit: int = 50) -> List[Campaign]:
        """Get list of campaigns"""
        pass
    
    # Analytics
    @abstractmethod
    async def get_campaign_analytics(self, campaign_id: str) -> EmailAnalytics:
        """Get campaign analytics"""
        pass
        
    @abstractmethod
    async def get_overall_analytics(self, start_date: datetime, end_date: datetime) -> EmailAnalytics:
        """Get overall account analytics"""
        pass
    
    # Transactional Email
    @abstractmethod
    async def send_transactional(self, 
                               to_email: str,
                               subject: str,
                               html_content: str,
                               text_content: Optional[str] = None,
                               from_name: Optional[str] = None,
                               from_email: Optional[str] = None,
                               personalization: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send transactional email"""
        pass
    
    # Utility Methods
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            "name": self.provider_name,
            "authenticated": self.is_authenticated,
            "config_keys": list(self.config.keys()) if self.config else []
        }
        
    async def validate_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
        
    def normalize_analytics(self, provider_analytics: Dict[str, Any]) -> EmailAnalytics:
        """Normalize provider-specific analytics to standard format"""
        # This is a base implementation - providers should override as needed
        return EmailAnalytics(
            total_sent=provider_analytics.get('sent', 0),
            delivered=provider_analytics.get('delivered', 0),
            bounced=provider_analytics.get('bounced', 0),
            opened=provider_analytics.get('opened', 0),
            clicked=provider_analytics.get('clicked', 0),
            unsubscribed=provider_analytics.get('unsubscribed', 0),
            complaints=provider_analytics.get('complaints', 0)
        )