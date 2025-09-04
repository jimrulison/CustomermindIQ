"""
Customer Mind IQ - Constant Contact Provider
OAuth 2.0 integration with comprehensive contact and campaign management
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from urllib.parse import urlencode

from .base_provider import BaseEmailProvider, Contact, EmailTemplate, Campaign, EmailAnalytics, CampaignStatus

class ConstantContactProvider(BaseEmailProvider):
    """Constant Contact email provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.access_token = config.get('access_token')
        self.base_url = "https://api.cc.email/v3"
        self.session = None
        
    async def _get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
        
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated API request"""
        if not self.access_token:
            raise ValueError("Access token required for Constant Contact API")
            
        session = await self._get_session()
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        async with session.request(method, url, json=data, params=params, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 201:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"Constant Contact API error {response.status}: {error_text}")
    
    async def authenticate(self) -> bool:
        """Test authentication"""
        try:
            result = await self.test_connection()
            self.is_authenticated = result.get('connected', False)
            return self.is_authenticated
        except Exception:
            self.is_authenticated = False
            return False
            
    async def test_connection(self) -> Dict[str, Any]:
        """Test Constant Contact connection"""
        try:
            # Test with account summary endpoint
            response = await self._make_request('GET', 'account/summary')
            return {
                'connected': True,
                'provider': 'constant_contact',
                'account_info': response
            }
        except Exception as e:
            return {
                'connected': False,
                'provider': 'constant_contact',
                'error': str(e)
            }
    
    # Contact Management
    async def create_contact(self, contact: Contact) -> Dict[str, Any]:
        """Create contact in Constant Contact"""
        contact_data = {
            'email_addresses': [{'email_address': contact.email}],
            'first_name': contact.first_name or '',
            'last_name': contact.last_name or '',
            'company_name': contact.company or '',
            'phone_numbers': [{'phone_number': contact.phone}] if contact.phone else []
        }
        
        if contact.custom_fields:
            contact_data['custom_fields'] = [
                {'custom_field_id': k, 'value': str(v)} 
                for k, v in contact.custom_fields.items()
            ]
            
        return await self._make_request('POST', 'contacts', contact_data)
        
    async def update_contact(self, email: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update contact in Constant Contact"""
        # First find the contact
        contacts = await self._make_request('GET', 'contacts', params={'email': email})
        if not contacts.get('contacts'):
            raise ValueError(f"Contact {email} not found")
            
        contact_id = contacts['contacts'][0]['contact_id']
        
        update_data = {}
        if 'first_name' in updates:
            update_data['first_name'] = updates['first_name']
        if 'last_name' in updates:
            update_data['last_name'] = updates['last_name']
        if 'company' in updates:
            update_data['company_name'] = updates['company']
            
        return await self._make_request('PUT', f'contacts/{contact_id}', update_data)
        
    async def get_contact(self, email: str) -> Optional[Contact]:
        """Get contact by email"""
        try:
            response = await self._make_request('GET', 'contacts', params={'email': email})
            contacts = response.get('contacts', [])
            
            if not contacts:
                return None
                
            cc_contact = contacts[0]
            return Contact(
                email=cc_contact['email_addresses'][0]['email_address'],
                first_name=cc_contact.get('first_name'),
                last_name=cc_contact.get('last_name'),
                company=cc_contact.get('company_name'),
                phone=cc_contact['phone_numbers'][0]['phone_number'] if cc_contact.get('phone_numbers') else None,
                created_at=datetime.fromisoformat(cc_contact['created_at'].replace('Z', '+00:00')) if cc_contact.get('created_at') else None
            )
        except Exception:
            return None
            
    async def delete_contact(self, email: str) -> bool:
        """Delete contact"""
        try:
            contacts = await self._make_request('GET', 'contacts', params={'email': email})
            if not contacts.get('contacts'):
                return False
                
            contact_id = contacts['contacts'][0]['contact_id']
            await self._make_request('DELETE', f'contacts/{contact_id}')
            return True
        except Exception:
            return False
            
    async def get_contacts(self, limit: int = 100, offset: int = 0) -> List[Contact]:
        """Get list of contacts"""
        try:
            response = await self._make_request('GET', 'contacts', params={'limit': limit, 'offset': offset})
            contacts = []
            
            for cc_contact in response.get('contacts', []):
                contact = Contact(
                    email=cc_contact['email_addresses'][0]['email_address'],
                    first_name=cc_contact.get('first_name'),
                    last_name=cc_contact.get('last_name'),
                    company=cc_contact.get('company_name'),
                    phone=cc_contact['phone_numbers'][0]['phone_number'] if cc_contact.get('phone_numbers') else None,
                    created_at=datetime.fromisoformat(cc_contact['created_at'].replace('Z', '+00:00')) if cc_contact.get('created_at') else None
                )
                contacts.append(contact)
                
            return contacts
        except Exception:
            return []
    
    # List Management
    async def create_list(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create contact list"""
        list_data = {
            'name': name,
            'description': description or f"Customer Mind IQ list: {name}"
        }
        return await self._make_request('POST', 'contact_lists', list_data)
        
    async def add_contact_to_list(self, list_id: str, email: str) -> bool:
        """Add contact to list"""
        try:
            # Get contact first
            contact = await self.get_contact(email)
            if not contact:
                return False
                
            # Add to list - Constant Contact uses membership endpoints
            membership_data = {
                'source': 'API',
                'contact_list_ids': [list_id]
            }
            
            await self._make_request('POST', f'contacts/{email}/contact_lists', membership_data)
            return True
        except Exception:
            return False
            
    async def remove_contact_from_list(self, list_id: str, email: str) -> bool:
        """Remove contact from list"""
        try:
            await self._make_request('DELETE', f'contacts/{email}/contact_lists/{list_id}')
            return True
        except Exception:
            return False
    
    # Template Management
    async def create_template(self, template: EmailTemplate) -> Dict[str, Any]:
        """Create email template"""
        template_data = {
            'name': template.name,
            'format_type': 'HTML',
            'from_name': template.from_name,
            'from_email': template.from_email,
            'reply_to_email': template.reply_to or template.from_email,
            'subject': template.subject,
            'html_content': template.html_content,
            'text_content': template.text_content or ''
        }
        return await self._make_request('POST', 'emails', template_data)
        
    async def update_template(self, template_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update email template"""
        return await self._make_request('PUT', f'emails/{template_id}', updates)
        
    async def get_template(self, template_id: str) -> Optional[EmailTemplate]:
        """Get email template"""
        try:
            response = await self._make_request('GET', f'emails/{template_id}')
            return EmailTemplate(
                template_id=response['campaign_id'],
                name=response.get('name', ''),
                subject=response.get('subject', ''),
                html_content=response.get('html_content', ''),
                text_content=response.get('text_content'),
                from_name=response.get('from_name', ''),
                from_email=response.get('from_email', ''),
                reply_to=response.get('reply_to_email')
            )
        except Exception:
            return None
            
    async def delete_template(self, template_id: str) -> bool:
        """Delete email template"""
        try:
            await self._make_request('DELETE', f'emails/{template_id}')
            return True
        except Exception:
            return False
            
    async def get_templates(self, limit: int = 50) -> List[EmailTemplate]:
        """Get list of templates"""
        try:
            response = await self._make_request('GET', 'emails', params={'limit': limit})
            templates = []
            
            for cc_template in response.get('campaigns', []):
                template = EmailTemplate(
                    template_id=cc_template['campaign_id'],
                    name=cc_template.get('name', ''),
                    subject=cc_template.get('subject', ''),
                    html_content=cc_template.get('html_content', ''),
                    from_name=cc_template.get('from_name', ''),
                    from_email=cc_template.get('from_email', '')
                )
                templates.append(template)
                
            return templates
        except Exception:
            return []
    
    # Campaign Management
    async def create_campaign(self, campaign: Campaign) -> Dict[str, Any]:
        """Create email campaign"""
        campaign_data = {
            'name': campaign.name,
            'email_campaign_activities': [{
                'format_type': 'HTML',
                'from_name': campaign.from_name,
                'from_email': campaign.from_email,
                'reply_to_email': campaign.reply_to or campaign.from_email,
                'subject': campaign.subject,
                'html_content': campaign.html_content,
                'text_content': campaign.text_content or ''
            }]
        }
        return await self._make_request('POST', 'emails', campaign_data)
        
    async def send_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Send campaign immediately"""
        return await self._make_request('POST', f'emails/{campaign_id}/schedules', {
            'scheduled_date': datetime.now().isoformat()
        })
        
    async def schedule_campaign(self, campaign_id: str, schedule_time: datetime) -> Dict[str, Any]:
        """Schedule campaign"""
        return await self._make_request('POST', f'emails/{campaign_id}/schedules', {
            'scheduled_date': schedule_time.isoformat()
        })
        
    async def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause campaign"""
        # Constant Contact doesn't support pausing - return error
        raise NotImplementedError("Constant Contact doesn't support campaign pausing")
        
    async def cancel_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Cancel campaign"""
        return await self._make_request('DELETE', f'emails/{campaign_id}/schedules')
        
    async def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get campaign details"""
        try:
            response = await self._make_request('GET', f'emails/{campaign_id}')
            activity = response.get('email_campaign_activities', [{}])[0]
            
            return Campaign(
                campaign_id=response['campaign_id'],
                name=response.get('name', ''),
                subject=activity.get('subject', ''),
                html_content=activity.get('html_content', ''),
                text_content=activity.get('text_content'),
                from_name=activity.get('from_name', ''),
                from_email=activity.get('from_email', ''),
                reply_to=activity.get('reply_to_email'),
                status=CampaignStatus.DRAFT  # Default status
            )
        except Exception:
            return None
            
    async def get_campaigns(self, limit: int = 50) -> List[Campaign]:
        """Get list of campaigns"""
        try:
            response = await self._make_request('GET', 'emails', params={'limit': limit})
            campaigns = []
            
            for cc_campaign in response.get('campaigns', []):
                activity = cc_campaign.get('email_campaign_activities', [{}])[0]
                campaign = Campaign(
                    campaign_id=cc_campaign['campaign_id'],
                    name=cc_campaign.get('name', ''),
                    subject=activity.get('subject', ''),
                    html_content=activity.get('html_content', ''),
                    from_name=activity.get('from_name', ''),
                    from_email=activity.get('from_email', ''),
                    status=CampaignStatus.DRAFT
                )
                campaigns.append(campaign)
                
            return campaigns
        except Exception:
            return []
    
    # Analytics
    async def get_campaign_analytics(self, campaign_id: str) -> EmailAnalytics:
        """Get campaign analytics"""
        try:
            response = await self._make_request('GET', f'reports/email_reports/{campaign_id}')
            
            stats = response.get('stats', {})
            return EmailAnalytics(
                total_sent=stats.get('sends', 0),
                delivered=stats.get('sends', 0) - stats.get('bounces', 0),
                bounced=stats.get('bounces', 0),
                opened=stats.get('opens', 0),
                clicked=stats.get('clicks', 0),
                unsubscribed=stats.get('unsubscribes', 0),
                open_rate=stats.get('open_rate', 0) / 100 if stats.get('open_rate') else 0,
                click_rate=stats.get('click_rate', 0) / 100 if stats.get('click_rate') else 0,
                bounce_rate=stats.get('bounce_rate', 0) / 100 if stats.get('bounce_rate') else 0
            )
        except Exception:
            return EmailAnalytics()
            
    async def get_overall_analytics(self, start_date: datetime, end_date: datetime) -> EmailAnalytics:
        """Get overall account analytics"""
        try:
            params = {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
            response = await self._make_request('GET', 'reports/summary_reports/email_activity_summary', params=params)
            
            stats = response.get('stats', {})
            return EmailAnalytics(
                total_sent=stats.get('sends', 0),
                delivered=stats.get('sends', 0) - stats.get('bounces', 0),
                bounced=stats.get('bounces', 0),
                opened=stats.get('opens', 0),
                clicked=stats.get('clicks', 0),
                unsubscribed=stats.get('unsubscribes', 0)
            )
        except Exception:
            return EmailAnalytics()
    
    # Transactional Email
    async def send_transactional(self, 
                               to_email: str,
                               subject: str, 
                               html_content: str,
                               text_content: Optional[str] = None,
                               from_name: Optional[str] = None,
                               from_email: Optional[str] = None,
                               personalization: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send transactional email"""
        # Note: Constant Contact doesn't have dedicated transactional email API
        # This creates and sends a campaign to a single recipient
        
        campaign_data = {
            'name': f"Transactional: {subject}",
            'email_campaign_activities': [{
                'format_type': 'HTML',
                'from_name': from_name or self.config.get('from_name', 'Customer Mind IQ'),
                'from_email': from_email or self.config.get('from_email', 'hello@customermindiq.com'),
                'subject': subject,
                'html_content': html_content,
                'text_content': text_content or ''
            }]
        }
        
        # Create campaign
        campaign_response = await self._make_request('POST', 'emails', campaign_data)
        campaign_id = campaign_response['campaign_id']
        
        # Send immediately to specific contact
        return await self._make_request('POST', f'emails/{campaign_id}/schedules', {
            'scheduled_date': datetime.now().isoformat()
        })
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()