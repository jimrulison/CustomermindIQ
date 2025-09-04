"""
Customer Mind IQ - Unified Email Manager
Manages multiple email providers with intelligent switching and optimization
"""

import asyncio
import os
from typing import Dict, List, Optional, Any, Type
from datetime import datetime
from enum import Enum
import logging

from .base_provider import BaseEmailProvider, Contact, EmailTemplate, Campaign, EmailAnalytics
from .constant_contact import ConstantContactProvider

logger = logging.getLogger(__name__)

class ProviderType(Enum):
    """Available email provider types"""
    CONSTANT_CONTACT = "constant_contact"
    HUBSPOT = "hubspot"
    BREVO = "brevo"
    MAILCHIMP = "mailchimp"
    ACTIVE_CAMPAIGN = "active_campaign"

class EmailManager:
    """
    Unified email manager that handles multiple providers
    with intelligent switching and optimization
    """
    
    def __init__(self):
        self.providers: Dict[str, BaseEmailProvider] = {}
        self.default_provider: Optional[str] = None
        self.provider_classes: Dict[ProviderType, Type[BaseEmailProvider]] = {
            ProviderType.CONSTANT_CONTACT: ConstantContactProvider,
            # Additional providers will be added here
        }
        
    async def register_provider(self, provider_type: ProviderType, config: Dict[str, Any], 
                              is_default: bool = False) -> bool:
        """Register an email provider"""
        try:
            provider_class = self.provider_classes.get(provider_type)
            if not provider_class:
                logger.error(f"Provider type {provider_type.value} not supported")
                return False
                
            provider = provider_class(config)
            
            # Test authentication
            if await provider.authenticate():
                self.providers[provider_type.value] = provider
                
                if is_default or not self.default_provider:
                    self.default_provider = provider_type.value
                    
                logger.info(f"Successfully registered provider: {provider_type.value}")
                return True
            else:
                logger.error(f"Authentication failed for provider: {provider_type.value}")
                return False
                
        except Exception as e:
            logger.error(f"Error registering provider {provider_type.value}: {str(e)}")
            return False
    
    def get_provider(self, provider_name: Optional[str] = None) -> Optional[BaseEmailProvider]:
        """Get provider instance"""
        if provider_name:
            return self.providers.get(provider_name)
        elif self.default_provider:
            return self.providers.get(self.default_provider)
        else:
            # Return first available provider
            return next(iter(self.providers.values())) if self.providers else None
    
    async def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all registered providers"""
        status = {
            'total_providers': len(self.providers),
            'default_provider': self.default_provider,
            'providers': {}
        }
        
        for name, provider in self.providers.items():
            try:
                test_result = await provider.test_connection()
                status['providers'][name] = {
                    'connected': test_result.get('connected', False),
                    'authenticated': provider.is_authenticated,
                    'info': provider.get_provider_info()
                }
            except Exception as e:
                status['providers'][name] = {
                    'connected': False,
                    'authenticated': False,
                    'error': str(e)
                }
                
        return status
    
    # Unified Contact Management
    async def create_contact(self, contact: Contact, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Create contact using specified or default provider"""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError("No email provider available")
        return await provider.create_contact(contact)
    
    async def update_contact(self, email: str, updates: Dict[str, Any], 
                           provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Update contact using specified or default provider"""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError("No email provider available")
        return await provider.update_contact(email, updates)
    
    async def get_contact(self, email: str, provider_name: Optional[str] = None) -> Optional[Contact]:
        """Get contact using specified or default provider"""
        provider = self.get_provider(provider_name)
        if not provider:
            return None
        return await provider.get_contact(email)
    
    async def sync_contact_across_providers(self, contact: Contact) -> Dict[str, bool]:
        """Sync contact across all registered providers"""
        results = {}
        
        for name, provider in self.providers.items():
            try:
                await provider.create_contact(contact)
                results[name] = True
            except Exception as e:
                logger.error(f"Failed to sync contact {contact.email} to {name}: {str(e)}")
                results[name] = False
                
        return results
    
    # Unified Campaign Management
    async def create_campaign(self, campaign: Campaign, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Create campaign using specified or default provider"""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError("No email provider available")
        return await provider.create_campaign(campaign)
    
    async def send_campaign(self, campaign_id: str, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Send campaign using specified or default provider"""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError("No email provider available")
        return await provider.send_campaign(campaign_id)
    
    async def get_campaign_analytics(self, campaign_id: str, 
                                   provider_name: Optional[str] = None) -> EmailAnalytics:
        """Get campaign analytics using specified or default provider"""
        provider = self.get_provider(provider_name)
        if not provider:
            return EmailAnalytics()
        return await provider.get_campaign_analytics(campaign_id)
    
    # Unified Transactional Email
    async def send_transactional(self, 
                               to_email: str,
                               subject: str,
                               html_content: str,
                               text_content: Optional[str] = None,
                               from_name: Optional[str] = None,
                               from_email: Optional[str] = None,
                               personalization: Optional[Dict[str, Any]] = None,
                               provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Send transactional email using specified or default provider"""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError("No email provider available")
            
        return await provider.send_transactional(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            from_name=from_name,
            from_email=from_email,
            personalization=personalization
        )
    
    # Multi-Provider Operations
    async def send_with_failover(self, 
                               to_email: str,
                               subject: str,
                               html_content: str,
                               text_content: Optional[str] = None,
                               from_name: Optional[str] = None,
                               from_email: Optional[str] = None,
                               provider_priority: Optional[List[str]] = None) -> Dict[str, Any]:
        """Send email with automatic failover between providers"""
        
        # Determine provider order
        if provider_priority:
            providers_to_try = [p for p in provider_priority if p in self.providers]
        else:
            providers_to_try = list(self.providers.keys())
            
        if self.default_provider and self.default_provider not in providers_to_try:
            providers_to_try.insert(0, self.default_provider)
        
        last_error = None
        
        for provider_name in providers_to_try:
            try:
                result = await self.send_transactional(
                    to_email=to_email,
                    subject=subject,
                    html_content=html_content,
                    text_content=text_content,
                    from_name=from_name,
                    from_email=from_email,
                    provider_name=provider_name
                )
                
                # Success - add provider info
                result['provider_used'] = provider_name
                logger.info(f"Email sent successfully via {provider_name}")
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"Failed to send via {provider_name}: {str(e)}")
                continue
        
        # All providers failed
        raise Exception(f"All providers failed. Last error: {str(last_error)}")
    
    async def get_aggregated_analytics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get aggregated analytics across all providers"""
        all_analytics = {}
        total_analytics = EmailAnalytics()
        
        for name, provider in self.providers.items():
            try:
                analytics = await provider.get_overall_analytics(start_date, end_date)
                all_analytics[name] = analytics
                
                # Aggregate totals
                total_analytics.total_sent += analytics.total_sent
                total_analytics.delivered += analytics.delivered
                total_analytics.bounced += analytics.bounced
                total_analytics.opened += analytics.opened
                total_analytics.clicked += analytics.clicked
                total_analytics.unsubscribed += analytics.unsubscribed
                total_analytics.complaints += analytics.complaints
                
            except Exception as e:
                logger.error(f"Failed to get analytics from {name}: {str(e)}")
                all_analytics[name] = EmailAnalytics()
        
        # Calculate aggregated rates
        if total_analytics.total_sent > 0:
            total_analytics.delivery_rate = total_analytics.delivered / total_analytics.total_sent
            total_analytics.open_rate = total_analytics.opened / total_analytics.total_sent
            total_analytics.click_rate = total_analytics.clicked / total_analytics.total_sent
            total_analytics.bounce_rate = total_analytics.bounced / total_analytics.total_sent
            total_analytics.unsubscribe_rate = total_analytics.unsubscribed / total_analytics.total_sent
        
        return {
            'aggregated': total_analytics,
            'by_provider': all_analytics,
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        }
    
    # Provider Health and Optimization
    async def health_check_all_providers(self) -> Dict[str, Dict[str, Any]]:
        """Perform health check on all providers"""
        results = {}
        
        for name, provider in self.providers.items():
            start_time = datetime.now()
            try:
                test_result = await provider.test_connection()
                response_time = (datetime.now() - start_time).total_seconds()
                
                results[name] = {
                    'healthy': test_result.get('connected', False),
                    'response_time': response_time,
                    'authenticated': provider.is_authenticated,
                    'details': test_result
                }
            except Exception as e:
                response_time = (datetime.now() - start_time).total_seconds()
                results[name] = {
                    'healthy': False,
                    'response_time': response_time,
                    'authenticated': False,
                    'error': str(e)
                }
        
        return results
    
    async def get_optimal_provider(self, criteria: str = 'health') -> Optional[str]:
        """Get optimal provider based on specified criteria"""
        if not self.providers:
            return None
            
        if criteria == 'health':
            health_results = await self.health_check_all_providers()
            
            # Find healthiest provider with fastest response time
            healthy_providers = {
                name: result for name, result in health_results.items() 
                if result['healthy']
            }
            
            if not healthy_providers:
                return None
                
            # Return provider with best response time
            optimal = min(healthy_providers.items(), key=lambda x: x[1]['response_time'])
            return optimal[0]
            
        elif criteria == 'default':
            return self.default_provider
            
        else:
            # Return first available
            return next(iter(self.providers.keys()))

# Global email manager instance
email_manager = EmailManager()