"""
Customer Success Intelligence Module

Advanced customer health scoring, success milestone tracking, and CSM workflow automation.
Combines insights from existing modules (churn prevention, behavioral clustering, sentiment analysis) 
into actionable customer success intelligence.
"""

from fastapi import APIRouter
from .health_score_engine import health_score_router
from .success_milestones import success_milestones_router
from .csm_workflows import csm_workflows_router
from .expansion_opportunities import expansion_opportunities_router

# Create main router for Customer Success Intelligence
customer_success_router = APIRouter(prefix="/api/customer-success", tags=["Customer Success Intelligence"])

# Include all sub-routers
customer_success_router.include_router(health_score_router)
customer_success_router.include_router(success_milestones_router)  
customer_success_router.include_router(csm_workflows_router)
customer_success_router.include_router(expansion_opportunities_router)