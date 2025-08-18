"""
Executive Intelligence Dashboard Module

Cross-module analytics and AI-generated executive insights.
Provides C-level dashboard views, automated reporting, and strategic recommendations.
"""

from fastapi import APIRouter
from .executive_dashboard import executive_dashboard_router
from .automated_reporting import automated_reporting_router
from .strategic_insights import strategic_insights_router

# Create main router for Executive Intelligence Dashboard
executive_intelligence_router = APIRouter(prefix="/api/executive", tags=["Executive Intelligence"])

# Include all sub-routers
executive_intelligence_router.include_router(executive_dashboard_router)
executive_intelligence_router.include_router(automated_reporting_router)
executive_intelligence_router.include_router(strategic_insights_router)