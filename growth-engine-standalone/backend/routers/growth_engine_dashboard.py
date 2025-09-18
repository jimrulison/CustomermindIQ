"""
Growth Engine Dashboard - Main Dashboard Data
Simplified standalone version for Growth Acceleration Engine
"""

from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel
import logging

from .auth import get_current_user

logger = logging.getLogger(__name__)

# Router
growth_dashboard_router = APIRouter()

# Pydantic models
class DashboardMetrics(BaseModel):
    total_opportunities: int
    high_priority_opportunities: int
    total_estimated_impact: float
    active_ab_tests: int
    completed_ab_tests: int
    revenue_leaks_detected: int
    total_revenue_at_risk: float
    recovery_potential: float
    roi_calculations: int
    average_projected_roi: float

class RecentActivity(BaseModel):
    id: str
    type: str  # "opportunity", "ab_test", "revenue_leak", "roi_calculation"
    title: str
    description: str
    timestamp: datetime
    status: str

class DashboardResponse(BaseModel):
    metrics: DashboardMetrics
    recent_activities: List[RecentActivity]
    insights: List[str]
    recommendations: List[str]

class GrowthDashboardService:
    """Service for generating dashboard data"""
    
    async def get_dashboard_metrics(self, db, user_email: str) -> DashboardMetrics:
        """Calculate dashboard metrics from user data"""
        
        # Count opportunities
        opportunities_count = await db.growth_opportunities.count_documents({"user_email": user_email})
        high_priority_count = await db.growth_opportunities.count_documents({
            "user_email": user_email,
            "priority": {"$in": ["critical", "high"]}
        })
        
        # Count A/B tests
        active_tests = await db.ab_tests.count_documents({
            "user_email": user_email,
            "status": "running"
        })
        completed_tests = await db.ab_tests.count_documents({
            "user_email": user_email,
            "status": "completed"
        })
        
        # Count revenue leaks
        leaks_count = await db.revenue_leaks.count_documents({"user_email": user_email})
        
        # Calculate revenue at risk
        leaks_cursor = db.revenue_leaks.find({"user_email": user_email})
        leaks = await leaks_cursor.to_list(length=None)
        total_revenue_at_risk = sum(leak.get("estimated_monthly_loss", 0) for leak in leaks)
        recovery_potential = sum(leak.get("potential_recovery", 0) for leak in leaks)
        
        # ROI calculations
        roi_count = await db.roi_calculations.count_documents({"user_email": user_email})
        
        # Calculate average ROI
        roi_cursor = db.roi_calculations.find({"user_email": user_email})
        roi_calculations = await roi_cursor.to_list(length=None)
        avg_roi = sum(calc.get("projected_roi", 0) for calc in roi_calculations) / len(roi_calculations) if roi_calculations else 0
        
        return DashboardMetrics(
            total_opportunities=opportunities_count,
            high_priority_opportunities=high_priority_count,
            total_estimated_impact=25.5,  # Mock percentage
            active_ab_tests=active_tests,
            completed_ab_tests=completed_tests,
            revenue_leaks_detected=leaks_count,
            total_revenue_at_risk=round(total_revenue_at_risk, 2),
            recovery_potential=round(recovery_potential, 2),
            roi_calculations=roi_count,
            average_projected_roi=round(avg_roi, 2)
        )
    
    async def get_recent_activities(self, db, user_email: str, limit: int = 10) -> List[RecentActivity]:
        """Get recent user activities across all modules"""
        
        activities = []
        
        # Get recent opportunities
        cursor = db.growth_opportunities.find({"user_email": user_email}).sort("created_at", -1).limit(3)
        opportunities = await cursor.to_list(length=None)
        for opp in opportunities:
            activities.append(RecentActivity(
                id=str(opp["_id"]),
                type="opportunity",
                title=f"Growth Opportunity: {opp.get('title', 'Unknown')}",
                description=opp.get('description', '')[:100] + "..." if len(opp.get('description', '')) > 100 else opp.get('description', ''),
                timestamp=opp.get('created_at', datetime.now(timezone.utc)),
                status=opp.get('status', 'identified')
            ))
        
        # Get recent A/B tests
        cursor = db.ab_tests.find({"user_email": user_email}).sort("created_at", -1).limit(3)
        tests = await cursor.to_list(length=None)
        for test in tests:
            activities.append(RecentActivity(
                id=str(test["_id"]),
                type="ab_test",
                title=f"A/B Test: {test.get('name', 'Unknown')}",
                description=test.get('description', '')[:100] + "..." if len(test.get('description', '')) > 100 else test.get('description', ''),
                timestamp=test.get('created_at', datetime.now(timezone.utc)),
                status=test.get('status', 'draft')
            ))
        
        # Get recent revenue leaks
        cursor = db.revenue_leaks.find({"user_email": user_email}).sort("created_at", -1).limit(3)
        leaks = await cursor.to_list(length=None)
        for leak in leaks:
            activities.append(RecentActivity(
                id=str(leak["_id"]),
                type="revenue_leak",
                title=f"Revenue Leak: {leak.get('title', 'Unknown')}",
                description=leak.get('description', '')[:100] + "..." if len(leak.get('description', '')) > 100 else leak.get('description', ''),
                timestamp=leak.get('created_at', datetime.now(timezone.utc)),
                status=leak.get('status', 'detected')
            ))
        
        # Get recent ROI calculations
        cursor = db.roi_calculations.find({"user_email": user_email}).sort("created_at", -1).limit(2)
        calculations = await cursor.to_list(length=None)
        for calc in calculations:
            activities.append(RecentActivity(
                id=str(calc["_id"]),
                type="roi_calculation",
                title=f"ROI Calculation: {calc.get('projected_roi', 0):.1f}% ROI",
                description=f"Investment: ${calc.get('investment_amount', 0):,.0f}, Payback: {calc.get('payback_period_months', 0):.1f} months",
                timestamp=calc.get('created_at', datetime.now(timezone.utc)),
                status="completed"
            ))
        
        # Sort by timestamp and limit
        activities.sort(key=lambda x: x.timestamp, reverse=True)
        return activities[:limit]
    
    def generate_insights(self, metrics: DashboardMetrics) -> List[str]:
        """Generate AI insights based on dashboard metrics"""
        
        insights = []
        
        if metrics.high_priority_opportunities > 0:
            insights.append(f"You have {metrics.high_priority_opportunities} high-priority growth opportunities ready for implementation")
        
        if metrics.revenue_leaks_detected > 0:
            insights.append(f"${metrics.total_revenue_at_risk:,.0f} monthly revenue at risk - ${metrics.recovery_potential:,.0f} recoverable")
        
        if metrics.active_ab_tests > 0:
            insights.append(f"{metrics.active_ab_tests} A/B tests are currently running - monitor for statistical significance")
        
        if metrics.average_projected_roi > 100:
            insights.append(f"Your growth investments show strong ROI potential (avg {metrics.average_projected_roi:.1f}%)")
        
        if not insights:
            insights.append("Start by scanning for growth opportunities to identify areas for improvement")
        
        return insights[:4]  # Limit to 4 insights
    
    def generate_recommendations(self, metrics: DashboardMetrics) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        if metrics.high_priority_opportunities > 2:
            recommendations.append("Focus on implementing your top 2 high-priority opportunities first")
        
        if metrics.revenue_leaks_detected > 0 and metrics.recovery_potential > 1000:
            recommendations.append("Address revenue leaks immediately to recover lost revenue")
        
        if metrics.completed_ab_tests < 2:
            recommendations.append("Run A/B tests to validate growth strategies before full implementation")
        
        if metrics.roi_calculations == 0:
            recommendations.append("Calculate ROI for growth investments to prioritize resources effectively")
        
        recommendations.append("Regularly scan for new opportunities to maintain growth momentum")
        
        return recommendations[:4]  # Limit to 4 recommendations

# Service instance
dashboard_service = GrowthDashboardService()

# API Endpoints
@growth_dashboard_router.get("/overview", response_model=DashboardResponse)
async def get_dashboard_overview(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get complete dashboard overview"""
    
    try:
        db = request.state.db
        user_email = current_user["email"]
        
        # Get metrics
        metrics = await dashboard_service.get_dashboard_metrics(db, user_email)
        
        # Get recent activities
        recent_activities = await dashboard_service.get_recent_activities(db, user_email)
        
        # Generate insights and recommendations
        insights = dashboard_service.generate_insights(metrics)
        recommendations = dashboard_service.generate_recommendations(metrics)
        
        return DashboardResponse(
            metrics=metrics,
            recent_activities=recent_activities,
            insights=insights,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error getting dashboard overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load dashboard"
        )

@growth_dashboard_router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get dashboard metrics only"""
    
    try:
        db = request.state.db
        user_email = current_user["email"]
        
        metrics = await dashboard_service.get_dashboard_metrics(db, user_email)
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting dashboard metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load metrics"
        )