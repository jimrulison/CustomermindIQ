"""
Integration & Data Management Hub Module

Comprehensive data integration platform for managing connectors, data flows,
synchronization, quality monitoring, and integration analytics.
"""

from fastapi import APIRouter
from .data_connectors import connectors_router
from .sync_management import sync_router
from .data_quality import quality_router
from .integration_analytics import analytics_router

# Create main router for Integration & Data Management Hub
integration_hub_router = APIRouter(prefix="/api/integration-hub", tags=["Integration & Data Management Hub"])

# Include all sub-routers
integration_hub_router.include_router(connectors_router)
integration_hub_router.include_router(sync_router)
integration_hub_router.include_router(quality_router)
integration_hub_router.include_router(analytics_router)