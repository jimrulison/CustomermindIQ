"""
ROI Calculator - Growth Investment Analysis
Simplified standalone version for Growth Acceleration Engine
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel
import logging

from .auth import get_current_user

logger = logging.getLogger(__name__)

# Router
roi_calculator_router = APIRouter()

# Pydantic models
class ROICalculationRequest(BaseModel):
    investment_amount: float
    implementation_months: int
    current_metrics: Dict[str, float]
    expected_improvements: Dict[str, float]
    industry: Optional[str] = "general"

class ROIResult(BaseModel):
    id: str
    investment_amount: float
    projected_roi: float
    payback_period_months: float
    net_present_value: float
    break_even_point: datetime
    annual_savings: float
    confidence_level: float
    created_at: datetime

class ROIBreakdown(BaseModel):
    month: int
    cumulative_investment: float
    cumulative_returns: float
    net_benefit: float

class ROIResponse(BaseModel):
    result: ROIResult
    breakdown: List[ROIBreakdown]
    recommendations: List[str]

class ROICalculatorService:
    """Service for calculating ROI on growth investments"""
    
    def calculate_roi(self, request: ROICalculationRequest) -> ROIResponse:
        """Calculate ROI based on investment and expected improvements"""
        
        # Basic ROI calculation logic
        monthly_investment = request.investment_amount / request.implementation_months
        
        # Calculate projected returns based on improvements
        base_revenue = request.current_metrics.get("monthly_revenue", 10000)
        base_customers = request.current_metrics.get("monthly_customers", 100)
        
        # Apply expected improvements
        revenue_improvement = request.expected_improvements.get("revenue_increase", 0.2)
        customer_improvement = request.expected_improvements.get("customer_increase", 0.15)
        
        projected_monthly_increase = (base_revenue * revenue_improvement) + \
                                   (base_customers * customer_improvement * 100)  # Assume $100 per customer
        
        # Calculate ROI metrics
        annual_savings = projected_monthly_increase * 12
        roi_percentage = (annual_savings - request.investment_amount) / request.investment_amount * 100
        payback_months = request.investment_amount / projected_monthly_increase if projected_monthly_increase > 0 else 999
        npv = annual_savings - request.investment_amount  # Simplified NPV
        
        # Generate breakdown
        breakdown = []
        for month in range(1, 13):
            cumulative_investment = min(request.investment_amount, monthly_investment * month)
            cumulative_returns = projected_monthly_increase * month if month > request.implementation_months else 0
            net_benefit = cumulative_returns - cumulative_investment
            
            breakdown.append(ROIBreakdown(
                month=month,
                cumulative_investment=cumulative_investment,
                cumulative_returns=cumulative_returns,
                net_benefit=net_benefit
            ))
        
        # Create result
        result = ROIResult(
            id=f"roi_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            investment_amount=request.investment_amount,
            projected_roi=roi_percentage,
            payback_period_months=payback_months,
            net_present_value=npv,
            break_even_point=datetime.now(timezone.utc).replace(month=int(payback_months) + 1) if payback_months < 12 else datetime.now(timezone.utc).replace(year=datetime.now().year + 1),
            annual_savings=annual_savings,
            confidence_level=0.85,  # Default confidence
            created_at=datetime.now(timezone.utc)
        )
        
        # Generate recommendations
        recommendations = []
        if roi_percentage > 200:
            recommendations.append("Excellent ROI potential - prioritize this investment")
        elif roi_percentage > 100:
            recommendations.append("Good ROI potential - consider implementing")
        elif roi_percentage > 50:
            recommendations.append("Moderate ROI - evaluate against other priorities")
        else:
            recommendations.append("Low ROI - consider alternative strategies")
        
        if payback_months < 6:
            recommendations.append("Quick payback period - low financial risk")
        elif payback_months > 18:
            recommendations.append("Long payback period - ensure sustained commitment")
        
        return ROIResponse(
            result=result,
            breakdown=breakdown,
            recommendations=recommendations
        )

# Service instance
roi_service = ROICalculatorService()

# API Endpoints
@roi_calculator_router.post("/calculate", response_model=ROIResponse)
async def calculate_roi(
    request_data: ROICalculationRequest,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Calculate ROI for growth investment"""
    
    try:
        # Calculate ROI
        roi_response = roi_service.calculate_roi(request_data)
        
        # Store calculation in database
        db = request.state.db
        calculation_dict = roi_response.result.dict()
        calculation_dict["user_email"] = current_user["email"]
        calculation_dict["user_id"] = current_user["id"]
        calculation_dict["request_data"] = request_data.dict()
        
        await db.roi_calculations.insert_one(calculation_dict)
        
        return roi_response
        
    except Exception as e:
        logger.error(f"Error calculating ROI: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate ROI"
        )

@roi_calculator_router.get("/history", response_model=List[ROIResult])
async def get_roi_history(
    request: Request,
    current_user: dict = Depends(get_current_user),
    limit: int = 20
):
    """Get user's ROI calculation history"""
    
    db = request.state.db
    
    cursor = db.roi_calculations.find(
        {"user_email": current_user["email"]}
    ).sort("created_at", -1).limit(limit)
    
    calculations = await cursor.to_list(length=None)
    
    result = []
    for calc in calculations:
        calc["id"] = str(calc["_id"])
        del calc["_id"]
        del calc["user_email"]
        del calc["user_id"]
        del calc["request_data"]
        result.append(ROIResult(**calc))
    
    return result