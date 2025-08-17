"""
Customer Mind IQ - Universal Intelligence Engine
Platform-agnostic customer intelligence that works with any business software
"""

from .universal_intelligence_service import UniversalIntelligenceService
from .customer_profile_manager import CustomerProfileManager
from .universal_models import UniversalCustomerProfile, CustomerInsight, BusinessIntelligence

__all__ = [
    'UniversalIntelligenceService',
    'CustomerProfileManager',
    'UniversalCustomerProfile',
    'CustomerInsight', 
    'BusinessIntelligence'
]