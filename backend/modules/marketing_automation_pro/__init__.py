"""
Customer Mind IQ - Marketing Automation Pro Module
Advanced AI-powered marketing automation and campaign orchestration suite
"""

from .multi_channel_orchestration import MultiChannelOrchestrationService, Campaign, CampaignExecution
from .ab_testing import ABTestingService, ABTest, TestVariant, TestResults
from .dynamic_content import DynamicContentService, ContentTemplate, ContentPersonalization
from .cross_sell_intelligence import CrossSellIntelligenceService, CrossSellOpportunity, ProductRecommendation
from .referral_program import ReferralProgramService, ReferralCampaign, ReferralTracking

__all__ = [
    # Services
    'MultiChannelOrchestrationService',
    'ABTestingService',
    'DynamicContentService', 
    'CrossSellIntelligenceService',
    'ReferralProgramService',
    
    # Models
    'Campaign',
    'CampaignExecution',
    'ABTest',
    'TestVariant',
    'TestResults',
    'ContentTemplate',
    'ContentPersonalization',
    'CrossSellOpportunity',
    'ProductRecommendation',
    'ReferralCampaign',
    'ReferralTracking'
]