"""
Analytics & Insights Module
Advanced analytics and insights for Universal Customer Intelligence SaaS Platform
"""

from .customer_journey_mapping import customer_journey_mapping_router
from .revenue_attribution import revenue_attribution_router  
from .cohort_analysis import cohort_analysis_router
from .competitive_intelligence import competitive_intelligence_router
from .roi_forecasting import roi_forecasting_router

__all__ = [
    'customer_journey_mapping_router',
    'revenue_attribution_router',
    'cohort_analysis_router', 
    'competitive_intelligence_router',
    'roi_forecasting_router'
]