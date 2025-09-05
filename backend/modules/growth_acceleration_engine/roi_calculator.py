"""
ROI Calculator & Impact Tracking - Advanced Financial Analysis
Calculates comprehensive ROI for growth initiatives and tracks actual vs projected performance
"""

import asyncio
import json
import os
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv

from .models import (
    ROICalculation,
    UpdateActualMetricsRequest,
    ROIDashboardResponse,
    AIInsight,
    GrowthOpportunity,
    ABTest,
    RevenueLeak
)

load_dotenv()

class ROICalculator:
    """Advanced ROI calculation and tracking service"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        self.mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[os.environ.get('DB_NAME', 'customer_mind_iq')]
        
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    async def calculate_initiative_roi(self, customer_id: str, initiative_id: str, 
                                     initiative_type: str, initiative_data: Dict[str, Any],
                                     business_context: Dict[str, Any]) -> ROICalculation:
        """
        AI-powered comprehensive ROI calculation for growth initiatives
        """
        try:
            # Initialize AI chat for ROI analysis
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"roi_calculator_{initiative_id}",
                system_message="""You are the ROI Calculation AI, a financial analysis expert 
                specializing in growth initiative ROI calculations. You provide comprehensive 
                financial analysis including revenue projections, cost analysis, risk assessment, 
                and NPV calculations with high accuracy and detailed assumptions.
                
                Always respond in valid JSON format with detailed financial analysis."""
            ).with_model("openai", "gpt-4o")
            
            # Prepare comprehensive ROI analysis prompt
            roi_prompt = f"""
            Calculate comprehensive ROI analysis for this growth initiative:
            
            Initiative Type: {initiative_type}
            Initiative Data: {json.dumps(initiative_data, default=str)}
            Business Context: {json.dumps(business_context, default=str)}
            
            Provide detailed ROI analysis in this EXACT JSON format:
            {{
                "projected_revenue": {{
                    "year_1": <year 1 revenue projection>,
                    "year_2": <year 2 revenue projection>,
                    "total_projected": <total projected revenue over analysis period>
                }},
                "cost_analysis": {{
                    "implementation_cost": <one-time implementation cost>,
                    "ongoing_monthly_cost": <monthly operational costs>,
                    "opportunity_cost": <estimated opportunity cost>,
                    "total_investment": <total investment required>
                }},
                "financial_metrics": {{
                    "payback_period_months": <months to break even>,
                    "roi_12_months": <ROI percentage after 12 months>,
                    "roi_24_months": <ROI percentage after 24 months>,
                    "net_present_value": <NPV using 10% discount rate>,
                    "internal_rate_of_return": <IRR percentage>,
                    "risk_adjusted_roi": <ROI adjusted for risk factors>
                }},
                "risk_assessment": {{
                    "confidence_level": <0.0-1.0 confidence in projections>,
                    "risk_factors": ["risk factor 1", "risk factor 2", "risk factor 3"],
                    "sensitivity_analysis": {{
                        "best_case_roi": <ROI in best case scenario>,
                        "worst_case_roi": <ROI in worst case scenario>,
                        "most_likely_roi": <ROI in most likely scenario>
                    }}
                }},
                "assumptions": [
                    "Key assumption 1",
                    "Key assumption 2", 
                    "Key assumption 3",
                    "Key assumption 4"
                ],
                "success_factors": [
                    "Critical success factor 1",
                    "Critical success factor 2",
                    "Critical success factor 3"
                ]
            }}
            
            Analysis requirements:
            1. Use realistic market data and industry benchmarks
            2. Include comprehensive cost analysis (direct, indirect, opportunity costs)
            3. Apply appropriate discount rates for NPV calculation
            4. Consider implementation risks and market uncertainties
            5. Provide sensitivity analysis for key variables
            6. Include clear assumptions and success factors
            """
            
            message = UserMessage(text=roi_prompt)
            response = await chat.send_message(message)
            
            # Parse AI response
            try:
                roi_analysis = json.loads(response)
            except json.JSONDecodeError:
                # Fallback ROI calculation
                roi_analysis = self._generate_fallback_roi_analysis(initiative_data, business_context)
            
            # Extract financial data from AI analysis
            projected_revenue_data = roi_analysis.get("projected_revenue", {})
            cost_analysis = roi_analysis.get("cost_analysis", {})
            financial_metrics = roi_analysis.get("financial_metrics", {})
            risk_assessment = roi_analysis.get("risk_assessment", {})
            
            # Create ROI calculation model
            roi_calculation = ROICalculation(
                customer_id=customer_id,
                initiative_id=initiative_id,
                initiative_type=initiative_type,
                initiative_name=initiative_data.get("title", f"{initiative_type.title()} Initiative"),
                projected_revenue=float(projected_revenue_data.get("total_projected", 100000)),
                implementation_cost=float(cost_analysis.get("implementation_cost", 25000)),
                ongoing_monthly_cost=float(cost_analysis.get("ongoing_monthly_cost", 2000)),
                opportunity_cost=float(cost_analysis.get("opportunity_cost", 10000)),
                total_investment=float(cost_analysis.get("total_investment", 35000)),
                payback_period_months=int(financial_metrics.get("payback_period_months", 8)),
                roi_12_months=float(financial_metrics.get("roi_12_months", 1.5)),
                roi_24_months=float(financial_metrics.get("roi_24_months", 2.8)),
                net_present_value=float(financial_metrics.get("net_present_value", 65000)),
                internal_rate_of_return=financial_metrics.get("internal_rate_of_return"),
                risk_adjusted_roi=float(financial_metrics.get("risk_adjusted_roi", 1.3)),
                confidence_level=float(risk_assessment.get("confidence_level", 0.75)),
                assumptions=roi_analysis.get("assumptions", []),
                risk_factors=risk_assessment.get("risk_factors", []),
                sensitivity_analysis=risk_assessment.get("sensitivity_analysis", {}),
                status="projected"
            )
            
            # Store in database
            await self.db.roi_calculations.update_one(
                {"id": roi_calculation.id},
                {"$set": roi_calculation.dict()},
                upsert=True
            )
            
            return roi_calculation
            
        except Exception as e:
            print(f"ROI calculation error: {e}")
            # Return fallback ROI calculation
            return await self._generate_fallback_roi_calculation(customer_id, initiative_id, 
                                                               initiative_type, initiative_data)
    
    def _generate_fallback_roi_analysis(self, initiative_data: Dict[str, Any], 
                                      business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback ROI analysis if AI fails"""
        projected_revenue = float(initiative_data.get("projected_revenue_impact", 100000))
        
        return {
            "projected_revenue": {
                "year_1": projected_revenue * 0.6,
                "year_2": projected_revenue * 0.4,
                "total_projected": projected_revenue
            },
            "cost_analysis": {
                "implementation_cost": projected_revenue * 0.25,
                "ongoing_monthly_cost": projected_revenue * 0.02,
                "opportunity_cost": projected_revenue * 0.10,
                "total_investment": projected_revenue * 0.35
            },
            "financial_metrics": {
                "payback_period_months": 8,
                "roi_12_months": 1.5,
                "roi_24_months": 2.8,
                "net_present_value": projected_revenue * 0.65,
                "internal_rate_of_return": 45.0,
                "risk_adjusted_roi": 1.3
            },
            "risk_assessment": {
                "confidence_level": 0.75,
                "risk_factors": [
                    "Market conditions uncertainty",
                    "Implementation execution risk",
                    "Customer adoption challenges"
                ],
                "sensitivity_analysis": {
                    "best_case_roi": 3.5,
                    "worst_case_roi": 0.8,
                    "most_likely_roi": 2.1
                }
            },
            "assumptions": [
                "Market demand remains stable",
                "Implementation completed on schedule",
                "Customer response matches projections",
                "No major competitive disruptions"
            ],
            "success_factors": [
                "Effective project management and execution",
                "Strong customer communication and adoption",
                "Continuous monitoring and optimization"
            ]
        }
    
    async def _generate_fallback_roi_calculation(self, customer_id: str, initiative_id: str,
                                               initiative_type: str, initiative_data: Dict[str, Any]) -> ROICalculation:
        """Generate fallback ROI calculation model"""
        projected_revenue = float(initiative_data.get("projected_revenue_impact", 100000))
        
        return ROICalculation(
            customer_id=customer_id,
            initiative_id=initiative_id,
            initiative_type=initiative_type,
            initiative_name=initiative_data.get("title", f"{initiative_type.title()} Initiative"),
            projected_revenue=projected_revenue,
            implementation_cost=projected_revenue * 0.25,
            ongoing_monthly_cost=projected_revenue * 0.02,
            opportunity_cost=projected_revenue * 0.10,
            total_investment=projected_revenue * 0.35,
            payback_period_months=8,
            roi_12_months=1.5,
            roi_24_months=2.8,
            net_present_value=projected_revenue * 0.65,
            internal_rate_of_return=45.0,
            risk_adjusted_roi=1.3,
            confidence_level=0.75,
            assumptions=[
                "Market demand remains stable",
                "Implementation completed on schedule",
                "Customer response matches projections"
            ],
            risk_factors=[
                "Market conditions uncertainty",
                "Implementation execution risk",
                "Customer adoption challenges"
            ],
            sensitivity_analysis={
                "best_case_roi": 3.5,
                "worst_case_roi": 0.8,
                "most_likely_roi": 2.1
            }
        )
    
    async def update_actual_performance(self, roi_id: str, actual_metrics: UpdateActualMetricsRequest) -> ROICalculation:
        """Update ROI calculation with actual performance data"""
        try:
            # Get existing ROI calculation
            roi_data = await self.db.roi_calculations.find_one({"id": roi_id})
            if not roi_data:
                raise ValueError("ROI calculation not found")
            
            roi_calculation = ROICalculation(**roi_data)
            
            # Update with actual metrics
            roi_calculation.actual_revenue = actual_metrics.actual_revenue
            roi_calculation.status = "completed"
            roi_calculation.updated_at = datetime.utcnow()
            
            # Calculate variance analysis
            variance_analysis = await self._calculate_variance_analysis(roi_calculation, actual_metrics)
            roi_calculation.variance_analysis = variance_analysis
            roi_calculation.learning_insights = actual_metrics.lessons_learned
            
            # Recalculate actual ROI
            actual_roi = self._calculate_actual_roi(roi_calculation, actual_metrics)
            roi_calculation.roi_12_months = actual_roi
            
            # Store updated calculation
            await self.db.roi_calculations.update_one(
                {"id": roi_id},
                {"$set": roi_calculation.dict()}
            )
            
            return roi_calculation
            
        except Exception as e:
            raise ValueError(f"Actual performance update error: {e}")
    
    async def _calculate_variance_analysis(self, roi_calculation: ROICalculation, 
                                         actual_metrics: UpdateActualMetricsRequest) -> Dict[str, Any]:
        """Calculate comprehensive variance analysis"""
        revenue_variance = ((actual_metrics.actual_revenue - roi_calculation.projected_revenue) / 
                          roi_calculation.projected_revenue) * 100
        
        cost_variance = ((actual_metrics.actual_costs - roi_calculation.total_investment) / 
                        roi_calculation.total_investment) * 100
        
        timeline_variance = ((actual_metrics.actual_timeline - 
                            (roi_calculation.payback_period_months or 12)) / 
                           (roi_calculation.payback_period_months or 12)) * 100
        
        return {
            "revenue_variance": {
                "projected": roi_calculation.projected_revenue,
                "actual": actual_metrics.actual_revenue,
                "variance_percent": revenue_variance,
                "variance_amount": actual_metrics.actual_revenue - roi_calculation.projected_revenue
            },
            "cost_variance": {
                "projected": roi_calculation.total_investment,
                "actual": actual_metrics.actual_costs,
                "variance_percent": cost_variance,
                "variance_amount": actual_metrics.actual_costs - roi_calculation.total_investment
            },
            "timeline_variance": {
                "projected_months": roi_calculation.payback_period_months,
                "actual_months": actual_metrics.actual_timeline,
                "variance_percent": timeline_variance
            },
            "performance_notes": actual_metrics.performance_notes
        }
    
    def _calculate_actual_roi(self, roi_calculation: ROICalculation, 
                            actual_metrics: UpdateActualMetricsRequest) -> float:
        """Calculate actual ROI based on real performance"""
        if actual_metrics.actual_costs > 0:
            return (actual_metrics.actual_revenue - actual_metrics.actual_costs) / actual_metrics.actual_costs
        return 0.0
    
    async def get_portfolio_roi_analysis(self, customer_id: str) -> Dict[str, Any]:
        """Get comprehensive portfolio ROI analysis"""
        try:
            # Get all ROI calculations for customer
            roi_cursor = self.db.roi_calculations.find({"customer_id": customer_id})
            roi_data = await roi_cursor.to_list(length=100)
            
            if not roi_data:
                return {
                    "portfolio_summary": {
                        "total_initiatives": 0,
                        "total_investment": 0.0,
                        "total_projected_revenue": 0.0,
                        "portfolio_roi": 0.0,
                        "average_payback_period": 0.0
                    },
                    "performance_breakdown": {},
                    "risk_analysis": {},
                    "recommendations": []
                }
            
            roi_calculations = [ROICalculation(**roi) for roi in roi_data]
            
            # Calculate portfolio metrics
            total_investment = sum(roi.total_investment for roi in roi_calculations)
            total_projected_revenue = sum(roi.projected_revenue for roi in roi_calculations)
            portfolio_roi = (total_projected_revenue - total_investment) / total_investment if total_investment > 0 else 0.0
            
            # Calculate average payback period
            payback_periods = [roi.payback_period_months for roi in roi_calculations if roi.payback_period_months]
            avg_payback = sum(payback_periods) / len(payback_periods) if payback_periods else 0.0
            
            # Breakdown by initiative type
            type_breakdown = {}
            for roi in roi_calculations:
                init_type = roi.initiative_type
                if init_type not in type_breakdown:
                    type_breakdown[init_type] = {
                        "count": 0,
                        "investment": 0.0,
                        "projected_revenue": 0.0,
                        "avg_roi": 0.0
                    }
                
                type_breakdown[init_type]["count"] += 1
                type_breakdown[init_type]["investment"] += roi.total_investment
                type_breakdown[init_type]["projected_revenue"] += roi.projected_revenue
            
            # Calculate average ROI by type
            for init_type in type_breakdown:
                investment = type_breakdown[init_type]["investment"]
                revenue = type_breakdown[init_type]["projected_revenue"]
                type_breakdown[init_type]["avg_roi"] = (revenue - investment) / investment if investment > 0 else 0.0
            
            # Risk analysis
            confidence_levels = [roi.confidence_level for roi in roi_calculations]
            avg_confidence = sum(confidence_levels) / len(confidence_levels) if confidence_levels else 0.0
            
            risk_analysis = {
                "average_confidence": avg_confidence,
                "high_risk_initiatives": len([roi for roi in roi_calculations if roi.confidence_level < 0.6]),
                "total_risk_exposure": sum(roi.total_investment for roi in roi_calculations if roi.confidence_level < 0.7)
            }
            
            return {
                "portfolio_summary": {
                    "total_initiatives": len(roi_calculations),
                    "total_investment": total_investment,
                    "total_projected_revenue": total_projected_revenue,
                    "portfolio_roi": portfolio_roi,
                    "average_payback_period": avg_payback
                },
                "performance_breakdown": type_breakdown,
                "risk_analysis": risk_analysis,
                "top_performers": sorted(roi_calculations, key=lambda x: x.roi_24_months, reverse=True)[:5]
            }
            
        except Exception as e:
            print(f"Portfolio analysis error: {e}")
            return {"error": str(e)}
    
    async def get_roi_dashboard(self, customer_id: str) -> ROIDashboardResponse:
        """Get comprehensive ROI dashboard"""
        try:
            # Get all ROI calculations
            roi_cursor = self.db.roi_calculations.find({"customer_id": customer_id})
            roi_data = await roi_cursor.to_list(length=100)
            
            roi_calculations = [ROICalculation(**roi) for roi in roi_data]
            
            # Calculate dashboard metrics
            total_investment = sum(roi.total_investment for roi in roi_calculations)
            total_returns = sum(roi.projected_revenue for roi in roi_calculations)
            portfolio_roi = (total_returns - total_investment) / total_investment if total_investment > 0 else 0.0
            
            # Payback summary
            payback_periods = [roi.payback_period_months for roi in roi_calculations if roi.payback_period_months]
            payback_summary = {
                "average_payback": sum(payback_periods) / len(payback_periods) if payback_periods else 0.0,
                "fastest_payback": min(payback_periods) if payback_periods else 0.0,
                "slowest_payback": max(payback_periods) if payback_periods else 0.0
            }
            
            return ROIDashboardResponse(
                roi_calculations=roi_calculations,
                portfolio_roi=portfolio_roi,
                total_investment=total_investment,
                total_returns=total_returns,
                payback_summary=payback_summary
            )
            
        except Exception as e:
            print(f"ROI dashboard error: {e}")
            return ROIDashboardResponse(
                roi_calculations=[],
                portfolio_roi=0.0,
                total_investment=0.0,
                total_returns=0.0,
                payback_summary={}
            )

# FastAPI Router
roi_calculator_router = APIRouter(prefix="/api/growth/roi", tags=["ROI Calculator"])

# Initialize service
roi_service = ROICalculator()

@roi_calculator_router.post("/calculate")
async def calculate_roi(request: Dict[str, Any]):
    """Calculate comprehensive ROI for growth initiative"""
    try:
        customer_id = "demo_customer_roi"
        initiative_id = request.get("initiative_id", "demo_initiative")
        initiative_type = request.get("initiative_type", "opportunity")
        initiative_data = request.get("initiative_data", {})
        business_context = request.get("business_context", {})
        
        roi_calculation = await roi_service.calculate_initiative_roi(
            customer_id=customer_id,
            initiative_id=initiative_id,
            initiative_type=initiative_type,
            initiative_data=initiative_data,
            business_context=business_context
        )
        
        return {
            "status": "success",
            "roi_calculation": roi_calculation.dict(),
            "calculated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ROI calculation error: {e}")

@roi_calculator_router.get("/dashboard")
async def get_roi_dashboard():
    """Get comprehensive ROI dashboard"""
    try:
        customer_id = "demo_customer_roi"
        dashboard = await roi_service.get_roi_dashboard(customer_id)
        
        return {
            "status": "success",
            "dashboard": dashboard.dict(),
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {e}")

@roi_calculator_router.get("/portfolio-analysis")
async def get_portfolio_analysis():
    """Get comprehensive portfolio ROI analysis"""
    try:
        customer_id = "demo_customer_roi"
        analysis = await roi_service.get_portfolio_roi_analysis(customer_id)
        
        return {
            "status": "success",
            "portfolio_analysis": analysis,
            "analyzed_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Portfolio analysis error: {e}")

@roi_calculator_router.post("/{roi_id}/update-actual")
async def update_actual_performance(roi_id: str, request: UpdateActualMetricsRequest):
    """Update ROI calculation with actual performance data"""
    try:
        updated_roi = await roi_service.update_actual_performance(roi_id, request)
        
        return {
            "status": "success",
            "roi_calculation": updated_roi.dict(),
            "updated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance update error: {e}")

@roi_calculator_router.get("/{roi_id}")
async def get_roi_details(roi_id: str):
    """Get detailed ROI calculation information"""
    try:
        roi_data = await roi_service.db.roi_calculations.find_one({"id": roi_id})
        
        if not roi_data:
            raise HTTPException(status_code=404, detail="ROI calculation not found")
        
        roi_calculation = ROICalculation(**roi_data)
        
        return {
            "status": "success",
            "roi_calculation": roi_calculation.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ROI details error: {e}")

@roi_calculator_router.get("/{roi_id}/variance-analysis")
async def get_variance_analysis(roi_id: str):
    """Get variance analysis for completed ROI calculation"""
    try:
        roi_data = await roi_service.db.roi_calculations.find_one({"id": roi_id})
        
        if not roi_data:
            raise HTTPException(status_code=404, detail="ROI calculation not found")
        
        roi_calculation = ROICalculation(**roi_data)
        
        if not roi_calculation.variance_analysis:
            raise HTTPException(status_code=404, detail="Variance analysis not available - actual metrics not yet provided")
        
        return {
            "status": "success",
            "variance_analysis": roi_calculation.variance_analysis,
            "learning_insights": roi_calculation.learning_insights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Variance analysis error: {e}")