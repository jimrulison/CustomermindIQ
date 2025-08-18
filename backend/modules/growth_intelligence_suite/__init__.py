"""
Growth Intelligence Suite Module

Enhanced marketing automation with ABM, intent data, and product-led growth tracking.
Builds upon existing Marketing Automation Pro with advanced growth intelligence capabilities.
"""

from fastapi import APIRouter
from .abm_intelligence import abm_intelligence_router
from .intent_data_analytics import intent_data_router
from .product_led_growth import plg_router

# Create main router for Growth Intelligence Suite
growth_intelligence_router = APIRouter(prefix="/api/growth-intelligence", tags=["Growth Intelligence Suite"])

# Include all sub-routers
growth_intelligence_router.include_router(abm_intelligence_router)
growth_intelligence_router.include_router(intent_data_router)
growth_intelligence_router.include_router(plg_router)