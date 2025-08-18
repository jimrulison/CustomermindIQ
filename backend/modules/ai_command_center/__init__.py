"""
AI Command Center Module

Centralized AI operations management, model orchestration, performance monitoring,
and intelligent automation control across all customer intelligence systems.
"""

from fastapi import APIRouter
from .ai_orchestration import orchestration_router
from .model_management import models_router
from .automation_control import automation_router
from .ai_insights_engine import insights_router

# Create main router for AI Command Center
ai_command_router = APIRouter(prefix="/api/ai-command", tags=["AI Command Center"])

# Include all sub-routers
ai_command_router.include_router(orchestration_router)
ai_command_router.include_router(models_router)
ai_command_router.include_router(automation_router)
ai_command_router.include_router(insights_router)