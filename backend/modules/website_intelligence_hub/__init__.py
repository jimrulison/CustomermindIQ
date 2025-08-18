"""
Website Intelligence Hub Module

Comprehensive website analysis and monitoring for users' own websites,
including SEO analysis, performance metrics, technical audits, and business intelligence.
"""

from fastapi import APIRouter
from .website_analyzer import analyzer_router
from .performance_monitor import performance_router
from .seo_intelligence import seo_router
from .membership_manager import membership_router

# Create main router for Website Intelligence Hub
website_intelligence_router = APIRouter(prefix="/api/website-intelligence", tags=["Website Intelligence Hub"])

# Include all sub-routers
website_intelligence_router.include_router(analyzer_router)
website_intelligence_router.include_router(performance_router)
website_intelligence_router.include_router(seo_router)
website_intelligence_router.include_router(membership_router)