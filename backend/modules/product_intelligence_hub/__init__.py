"""
Product Intelligence Hub Module

Advanced product usage analytics, feature adoption tracking, onboarding optimization,
and product-market fit indicators. Essential for product-led growth strategies.
"""

from fastapi import APIRouter
from .feature_usage_analytics import feature_usage_router
from .onboarding_optimization import onboarding_router
from .product_market_fit import pmf_router
from .user_journey_analytics import user_journey_router

# Create main router for Product Intelligence Hub
product_intelligence_router = APIRouter(prefix="/api/product-intelligence", tags=["Product Intelligence Hub"])

# Include all sub-routers
product_intelligence_router.include_router(feature_usage_router)
product_intelligence_router.include_router(onboarding_router)
product_intelligence_router.include_router(pmf_router)
product_intelligence_router.include_router(user_journey_router)