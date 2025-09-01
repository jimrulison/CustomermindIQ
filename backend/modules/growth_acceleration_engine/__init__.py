# Growth Acceleration Engine Module
# AI-powered growth opportunity identification, A/B testing, and revenue optimization

from .growth_opportunity_scanner import GrowthOpportunityScanner, growth_opportunity_router
from .automated_ab_testing import AutomatedABTestingService, ab_testing_router  
from .revenue_leak_detector import RevenueLeakDetector, revenue_leak_router
from .roi_calculator import ROICalculator, roi_calculator_router
from .models import *

__version__ = "1.0.0"
__author__ = "CustomerMind IQ"
__description__ = "AI-powered Growth Acceleration Engine for revenue optimization and customer insights"