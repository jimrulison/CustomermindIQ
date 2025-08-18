"""
Compliance & Governance Suite Module

Enterprise-grade compliance management, data governance, audit trails,
regulatory reporting, and policy enforcement for customer intelligence platforms.
"""

from fastapi import APIRouter
from .compliance_monitoring import compliance_router
from .audit_management import audit_router
from .data_governance import governance_router
from .regulatory_reporting import reporting_router

# Create main router for Compliance & Governance Suite
compliance_governance_router = APIRouter(prefix="/api/compliance-governance", tags=["Compliance & Governance Suite"])

# Include all sub-routers
compliance_governance_router.include_router(compliance_router)
compliance_governance_router.include_router(audit_router)
compliance_governance_router.include_router(governance_router)
compliance_governance_router.include_router(reporting_router)