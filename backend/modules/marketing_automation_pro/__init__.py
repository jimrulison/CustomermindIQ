"""
Customer Mind IQ - Marketing Automation Pro Module (Rebuilt)
Advanced AI-powered marketing automation with multi-channel orchestration,
A/B testing with bandit algorithms, dynamic content personalization,
multi-dimensional lead scoring, and viral referral programs
"""

from .multi_channel_orchestration import MultiChannelOrchestrationService
from .ab_testing import ABTestingService
from .dynamic_content import DynamicContentService
from .lead_scoring import LeadScoringService
from .referral_program import ReferralProgramService

__all__ = [
    # Advanced Marketing Automation Services
    'MultiChannelOrchestrationService',  # SMS, Push, Social Media Retargeting
    'ABTestingService',                  # AI-powered with multi-armed bandits
    'DynamicContentService',             # Real-time behavior-based personalization
    'LeadScoringService',               # Multi-dimensional AI scoring
    'ReferralProgramService'            # AI-powered viral loop optimization
]