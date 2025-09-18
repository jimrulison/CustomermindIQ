"""
Revenue Leak Detector - Identify Revenue Loss Opportunities
Simplified standalone version for Growth Acceleration Engine
"""

import random
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel
import logging

from .auth import get_current_user

logger = logging.getLogger(__name__)

# Router
revenue_leak_router = APIRouter()

# Pydantic models
class RevenueLeak(BaseModel):
    id: str
    title: str
    description: str
    leak_type: str
    severity: str
    estimated_monthly_loss: float
    potential_recovery: float
    confidence_score: float
    detection_method: str
    recommended_actions: List[str]
    created_at: datetime
    status: str = "detected"

class LeakScanRequest(BaseModel):
    business_metrics: Dict[str, Any]
    scan_period_months: int = 3
    focus_areas: Optional[List[str]] = None

class LeakScanResponse(BaseModel):
    leaks: List[RevenueLeak]
    total_estimated_loss: float
    recovery_potential: float
    priority_actions: List[str]
    scan_summary: Dict[str, Any]

# Mock leak detection templates
LEAK_TEMPLATES = [
    {
        "title": "High Cart Abandonment Rate",
        "description": "Customers are abandoning carts at checkout, resulting in lost revenue",
        "leak_type": "conversion",
        "severity": "high",
        "detection_method": "funnel_analysis",
        "recommended_actions": [
            "Simplify checkout process",
            "Add exit-intent popups with discounts",
            "Implement cart abandonment email campaigns",
            "Offer guest checkout option"
        ]
    },
    {
        "title": "Underutilized Upselling Opportunities",
        "description": "Missing revenue from existing customers who could purchase additional products",
        "leak_type": "expansion",
        "severity": "medium",
        "detection_method": "customer_behavior_analysis",
        "recommended_actions": [
            "Implement personalized product recommendations",
            "Create bundled offers for related products",
            "Train sales team on upselling techniques",
            "Add 'frequently bought together' suggestions"
        ]
    },
    {
        "title": "Pricing Strategy Misalignment",
        "description": "Current pricing may be too low compared to value delivered and market rates",
        "leak_type": "pricing",
        "severity": "high",
        "detection_method": "competitive_analysis",
        "recommended_actions": [
            "Conduct market pricing research",
            "Test price increases on new customers",
            "Implement value-based pricing tiers",
            "Analyze price sensitivity by customer segment"
        ]
    },
    {
        "title": "Customer Churn in High-Value Segments",
        "description": "Losing valuable customers who could be retained with proper intervention",
        "leak_type": "retention",
        "severity": "critical",
        "detection_method": "cohort_analysis",
        "recommended_actions": [
            "Implement proactive outreach for at-risk customers",
            "Create loyalty programs for high-value customers",
            "Improve customer success onboarding",
            "Regular check-ins and satisfaction surveys"
        ]
    },
    {
        "title": "Inefficient Marketing Spend",
        "description": "Marketing budget allocated to low-performing channels or campaigns",
        "leak_type": "acquisition",
        "severity": "medium",
        "detection_method": "attribution_analysis",
        "recommended_actions": [
            "Reallocate budget to high-performing channels",
            "Pause or optimize underperforming campaigns",
            "Implement better tracking and attribution",
            "A/B test different marketing messages"
        ]
    }
]

class RevenueLeakService:
    """Service for detecting and analyzing revenue leaks"""
    
    def detect_leaks(self, business_metrics: Dict[str, Any], scan_period_months: int) -> List[RevenueLeak]:
        """Detect revenue leaks based on business metrics"""
        
        # In a real implementation, this would analyze actual data
        # For now, we'll return relevant template leaks with calculated losses
        
        leaks = []
        base_revenue = business_metrics.get("monthly_revenue", 50000)
        
        # Select 2-4 relevant leaks
        selected_templates = random.sample(LEAK_TEMPLATES, random.randint(2, 4))
        
        for i, template in enumerate(selected_templates):
            # Calculate estimated loss based on leak type and severity
            if template["severity"] == "critical":
                loss_percentage = random.uniform(0.08, 0.15)  # 8-15% loss
            elif template["severity"] == "high":
                loss_percentage = random.uniform(0.05, 0.10)  # 5-10% loss
            else:
                loss_percentage = random.uniform(0.02, 0.06)  # 2-6% loss
            
            estimated_loss = base_revenue * loss_percentage
            recovery_potential = estimated_loss * random.uniform(0.6, 0.9)  # 60-90% recoverable
            
            leak = RevenueLeak(
                id=f"leak_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{i+1}",
                title=template["title"],
                description=template["description"],
                leak_type=template["leak_type"],
                severity=template["severity"],
                estimated_monthly_loss=round(estimated_loss, 2),
                potential_recovery=round(recovery_potential, 2),
                confidence_score=random.uniform(0.75, 0.95),
                detection_method=template["detection_method"],
                recommended_actions=template["recommended_actions"],
                created_at=datetime.now(timezone.utc),
                status="detected"
            )
            leaks.append(leak)
        
        # Sort by severity and estimated loss
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        leaks.sort(
            key=lambda x: (severity_order.get(x.severity, 0), x.estimated_monthly_loss),
            reverse=True
        )
        
        return leaks

# Service instance
leak_service = RevenueLeakService()

# API Endpoints
@revenue_leak_router.post("/scan", response_model=LeakScanResponse)
async def scan_revenue_leaks(
    request_data: LeakScanRequest,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Scan for revenue leaks based on business metrics"""
    
    try:
        # Detect leaks
        leaks = leak_service.detect_leaks(
            business_metrics=request_data.business_metrics,
            scan_period_months=request_data.scan_period_months
        )
        
        # Calculate totals
        total_loss = sum(leak.estimated_monthly_loss for leak in leaks)
        recovery_potential = sum(leak.potential_recovery for leak in leaks)
        
        # Generate priority actions
        priority_actions = []
        for leak in leaks[:2]:  # Top 2 leaks
            priority_actions.extend(leak.recommended_actions[:2])  # Top 2 actions each
        
        # Store leaks in database
        db = request.state.db
        for leak in leaks:
            leak_dict = leak.dict()
            leak_dict["user_email"] = current_user["email"]
            leak_dict["user_id"] = current_user["id"]
            
            await db.revenue_leaks.insert_one(leak_dict)
        
        # Generate scan summary
        scan_summary = {
            "total_leaks_detected": len(leaks),
            "critical_leaks": len([l for l in leaks if l.severity == "critical"]),
            "high_priority_leaks": len([l for l in leaks if l.severity in ["critical", "high"]]),
            "average_confidence": sum(l.confidence_score for l in leaks) / len(leaks) if leaks else 0,
            "scan_date": datetime.now(timezone.utc).isoformat(),
            "scan_period_months": request_data.scan_period_months
        }
        
        return LeakScanResponse(
            leaks=leaks,
            total_estimated_loss=total_loss,
            recovery_potential=recovery_potential,
            priority_actions=priority_actions,
            scan_summary=scan_summary
        )
        
    except Exception as e:
        logger.error(f"Error scanning revenue leaks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to scan revenue leaks"
        )

@revenue_leak_router.get("/leaks", response_model=List[RevenueLeak])
async def get_revenue_leaks(
    request: Request,
    current_user: dict = Depends(get_current_user),
    severity: Optional[str] = None,
    status_filter: Optional[str] = None,
    limit: int = 20
):
    """Get user's detected revenue leaks"""
    
    db = request.state.db
    
    # Build query
    query = {"user_email": current_user["email"]}
    if severity:
        query["severity"] = severity
    if status_filter:
        query["status"] = status_filter
    
    cursor = db.revenue_leaks.find(query).sort("created_at", -1).limit(limit)
    leaks = await cursor.to_list(length=None)
    
    result = []
    for leak in leaks:
        leak["id"] = str(leak["_id"])
        del leak["_id"]
        del leak["user_email"]
        del leak["user_id"]
        result.append(RevenueLeak(**leak))
    
    return result

@revenue_leak_router.put("/leaks/{leak_id}/status")
async def update_leak_status(
    leak_id: str,
    status: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Update revenue leak status"""
    
    db = request.state.db
    
    # Validate status
    valid_statuses = ["detected", "investigating", "fixing", "resolved", "dismissed"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    # Update leak
    result = await db.revenue_leaks.update_one(
        {
            "_id": leak_id,
            "user_email": current_user["email"]
        },
        {
            "$set": {
                "status": status,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revenue leak not found"
        )
    
    return {"message": "Revenue leak status updated successfully"}

@revenue_leak_router.get("/analytics", response_model=Dict[str, Any])
async def get_leak_analytics(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get revenue leak analytics summary"""
    
    db = request.state.db
    
    # Get all user's leaks
    cursor = db.revenue_leaks.find({"user_email": current_user["email"]})
    leaks = await cursor.to_list(length=None)
    
    if not leaks:
        return {
            "total_leaks": 0,
            "total_estimated_loss": 0,
            "total_recovery_potential": 0,
            "leaks_by_severity": {},
            "leaks_by_type": {},
            "leaks_by_status": {}
        }
    
    # Calculate analytics
    total_loss = sum(leak.get("estimated_monthly_loss", 0) for leak in leaks)
    total_recovery = sum(leak.get("potential_recovery", 0) for leak in leaks)
    
    # Group by categories
    by_severity = {}
    by_type = {}
    by_status = {}
    
    for leak in leaks:
        severity = leak.get("severity", "unknown")
        leak_type = leak.get("leak_type", "unknown")
        status = leak.get("status", "unknown")
        
        by_severity[severity] = by_severity.get(severity, 0) + 1
        by_type[leak_type] = by_type.get(leak_type, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
    
    return {
        "total_leaks": len(leaks),
        "total_estimated_loss": round(total_loss, 2),
        "total_recovery_potential": round(total_recovery, 2),
        "leaks_by_severity": by_severity,
        "leaks_by_type": by_type,
        "leaks_by_status": by_status,
        "last_scan_date": max(leak.get("created_at", datetime.now(timezone.utc)) for leak in leaks).isoformat() if leaks else None
    }