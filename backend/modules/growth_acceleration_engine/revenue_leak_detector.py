"""
Revenue Leak Detector - AI-Powered Funnel Analysis
Identifies and analyzes revenue leaks throughout the customer journey
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv

from .models import (
    RevenueLeak,
    LeakType,
    ImplementationEffort,
    Priority,
    FunnelStage,
    CustomerJourney,
    LeakAnalysisRequest,
    LeakDashboardResponse,
    AIInsight
)

load_dotenv()

class RevenueLeakDetector:
    """AI-powered revenue leak detection and analysis service"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        self.mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[os.environ.get('DB_NAME', 'customer_mind_iq')]
        
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    async def scan_revenue_leaks(self, customer_id: str, customer_data: Dict[str, Any], 
                               funnel_data: List[Dict[str, Any]], 
                               focus_areas: Optional[List[str]] = None) -> List[RevenueLeak]:
        """
        AI-powered comprehensive revenue leak detection
        """
        try:
            # Initialize AI chat for leak detection
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"leak_detector_{customer_id}",
                system_message="""You are the Revenue Leak Detection AI, an expert in identifying 
                revenue losses throughout customer funnels and business processes. You analyze conversion 
                data, customer behavior, and business metrics to pinpoint exactly where revenue is being 
                lost and provide actionable solutions.
                
                Always respond in valid JSON format with detailed analysis."""
            ).with_model("openai", "gpt-4o")
            
            # Prepare comprehensive leak analysis prompt
            analysis_prompt = f"""
            Analyze this business data and identify the top revenue leaks:
            
            Customer Data: {json.dumps(customer_data, default=str)}
            Funnel Data: {json.dumps(funnel_data, default=str)}
            Focus Areas: {focus_areas or 'All areas'}
            
            Identify and analyze revenue leaks in this EXACT JSON format:
            {{
                "revenue_leaks": [
                    {{
                        "leak_type": "conversion_bottleneck|churn_spike|pricing_issue|onboarding_dropout|feature_abandonment",
                        "location": "Specific location in funnel or process",
                        "title": "Clear, descriptive leak title",
                        "description": "Detailed description of the revenue leak",
                        "monthly_impact": <monthly revenue loss in dollars>,
                        "annual_impact": <annual revenue loss in dollars>,
                        "users_affected": <number of users affected>,
                        "current_performance": <current metric value>,
                        "benchmark_performance": <industry benchmark or target>,
                        "improvement_potential": <percentage improvement possible>,
                        "suggested_fixes": [
                            {{
                                "fix_title": "Quick win solution",
                                "fix_description": "Detailed implementation description",
                                "estimated_impact": "Expected revenue recovery",
                                "implementation_effort": "low|medium|high",
                                "timeline_weeks": 2
                            }}
                        ],
                        "fix_effort": "low|medium|high",
                        "priority": "urgent|high|medium|low",
                        "ai_analysis": "Detailed AI explanation of why this leak exists",
                        "root_cause_analysis": ["root cause 1", "root cause 2"],
                        "quick_wins": ["quick fix 1", "quick fix 2"],
                        "long_term_solutions": ["solution 1", "solution 2"],
                        "success_metrics": ["metric1", "metric2"],
                        "estimated_fix_timeline": <weeks to fix>,
                        "confidence_score": <0.0-1.0 confidence in analysis>
                    }}
                ]
            }}
            
            Focus on identifying:
            1. CONVERSION BOTTLENECKS (where users drop off in funnels)
            2. CHURN SPIKES (unexpected customer loss points)
            3. PRICING ISSUES (revenue optimization opportunities)
            4. ONBOARDING DROPOUTS (early user experience failures)
            5. FEATURE ABANDONMENT (underutilized revenue-generating features)
            
            Each leak must be:
            - Quantified with revenue impact
            - Specific and actionable
            - Prioritized by business impact
            - Include both quick wins and long-term solutions
            """
            
            message = UserMessage(text=analysis_prompt)
            response = await chat.send_message(message)
            
            # Parse AI response
            try:
                leak_analysis = json.loads(response)
                leaks_data = leak_analysis.get("revenue_leaks", [])
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                leaks_data = self._generate_fallback_leaks(customer_data, funnel_data)
            
            # Convert to RevenueLeak models
            revenue_leaks = []
            for leak_data in leaks_data[:10]:  # Top 10 leaks
                revenue_leak = RevenueLeak(
                    customer_id=customer_id,
                    leak_type=LeakType(leak_data.get("leak_type", "conversion_bottleneck")),
                    location=leak_data.get("location", "Customer funnel"),
                    title=leak_data.get("title", "Revenue Leak Identified"),
                    description=leak_data.get("description", "AI-identified revenue leak"),
                    monthly_impact=float(leak_data.get("monthly_impact", 10000)),
                    annual_impact=float(leak_data.get("annual_impact", 120000)),
                    users_affected=int(leak_data.get("users_affected", 100)),
                    current_performance=float(leak_data.get("current_performance", 0.12)),
                    benchmark_performance=float(leak_data.get("benchmark_performance", 0.18)),
                    improvement_potential=float(leak_data.get("improvement_potential", 25.0)),
                    suggested_fixes=leak_data.get("suggested_fixes", []),
                    fix_effort=ImplementationEffort(leak_data.get("fix_effort", "medium")),
                    priority=Priority(leak_data.get("priority", "high")),
                    ai_analysis=leak_data.get("ai_analysis", "AI-powered analysis identified this revenue leak"),
                    root_cause_analysis=leak_data.get("root_cause_analysis", []),
                    quick_wins=leak_data.get("quick_wins", []),
                    long_term_solutions=leak_data.get("long_term_solutions", []),
                    success_metrics=leak_data.get("success_metrics", []),
                    estimated_fix_timeline=int(leak_data.get("estimated_fix_timeline", 4)),
                    confidence_score=float(leak_data.get("confidence_score", 0.8))
                )
                revenue_leaks.append(revenue_leak)
            
            # Store leaks in database
            for leak in revenue_leaks:
                await self.db.revenue_leaks.update_one(
                    {"id": leak.id},
                    {"$set": leak.dict()},
                    upsert=True
                )
            
            return revenue_leaks
            
        except Exception as e:
            print(f"Revenue leak detection error: {e}")
            # Return fallback leaks on error
            return await self._generate_fallback_leak_models(customer_id, customer_data, funnel_data)
    
    def _generate_fallback_leaks(self, customer_data: Dict[str, Any], 
                                funnel_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate fallback leaks if AI analysis fails"""
        revenue = customer_data.get("total_revenue", 100000)
        customers = customer_data.get("total_customers", 1000)
        
        return [
            {
                "leak_type": "conversion_bottleneck",
                "location": "Checkout Process → Payment Completion",
                "title": "Cart Abandonment Revenue Loss",
                "description": "High abandonment rate at payment step causing significant revenue loss. Users add items to cart but fail to complete purchase.",
                "monthly_impact": revenue * 0.15,
                "annual_impact": revenue * 0.15 * 12,
                "users_affected": customers * 0.3,
                "current_performance": 0.65,
                "benchmark_performance": 0.82,
                "improvement_potential": 26.0,
                "suggested_fixes": [
                    {
                        "fix_title": "Simplify checkout flow",
                        "fix_description": "Remove unnecessary form fields and streamline payment process to reduce friction",
                        "estimated_impact": "$25,000 monthly recovery",
                        "implementation_effort": "low",
                        "timeline_weeks": 2
                    },
                    {
                        "fix_title": "Add payment options",
                        "fix_description": "Integrate multiple payment methods including digital wallets and buy-now-pay-later",
                        "estimated_impact": "$15,000 monthly recovery", 
                        "implementation_effort": "medium",
                        "timeline_weeks": 4
                    }
                ],
                "fix_effort": "medium",
                "priority": "urgent",
                "ai_analysis": "Checkout conversion rate of 65% is significantly below industry benchmark of 82%, representing major revenue leak in final funnel stage.",
                "root_cause_analysis": ["Complex checkout process", "Limited payment options", "Trust signals missing"],
                "quick_wins": ["Remove guest checkout barriers", "Add security badges", "Optimize mobile checkout"],
                "long_term_solutions": ["Implement one-click checkout", "Personalized payment recommendations", "AI-powered fraud prevention"],
                "success_metrics": ["Checkout conversion rate", "Cart abandonment rate", "Payment completion rate"],
                "estimated_fix_timeline": 4,
                "confidence_score": 0.92
            },
            {
                "leak_type": "churn_spike",
                "location": "Month 3-4 Customer Journey",
                "title": "Early Customer Churn Wave",
                "description": "Significant customer churn spike occurs at 3-4 month mark, indicating onboarding or value realization issues.",
                "monthly_impact": revenue * 0.12,
                "annual_impact": revenue * 0.12 * 12,
                "users_affected": customers * 0.2,
                "current_performance": 0.25,
                "benchmark_performance": 0.15,
                "improvement_potential": 40.0,
                "suggested_fixes": [
                    {
                        "fix_title": "Proactive customer success program",
                        "fix_description": "Implement automated check-ins and success milestones for months 1-6",
                        "estimated_impact": "$18,000 monthly recovery",
                        "implementation_effort": "medium",
                        "timeline_weeks": 6
                    }
                ],
                "fix_effort": "high",
                "priority": "high",
                "ai_analysis": "Churn rate of 25% at 3-4 months is 67% higher than industry benchmark, indicating critical value realization gap.",
                "root_cause_analysis": ["Lack of early value demonstration", "Insufficient onboarding support", "Feature adoption challenges"],
                "quick_wins": ["Create month 3 success checklist", "Automated success milestone emails", "Early warning system"],
                "long_term_solutions": ["Predictive churn modeling", "Personalized success paths", "Advanced customer health scoring"],
                "success_metrics": ["3-month retention rate", "Customer health score", "Time to first value"],
                "estimated_fix_timeline": 8,
                "confidence_score": 0.85
            },
            {
                "leak_type": "pricing_issue",
                "location": "Plan Upgrade Funnel",
                "title": "Undermonetized Customer Segments",
                "description": "Analysis reveals customer segments willing to pay more for premium features but not being offered appropriate upgrade paths.",
                "monthly_impact": revenue * 0.08,
                "annual_impact": revenue * 0.08 * 12,
                "users_affected": customers * 0.15,
                "current_performance": 0.08,
                "benchmark_performance": 0.15,
                "improvement_potential": 87.5,
                "suggested_fixes": [
                    {
                        "fix_title": "Usage-based upgrade triggers",
                        "fix_description": "Implement smart upgrade prompts based on feature usage patterns and limits",
                        "estimated_impact": "$12,000 monthly recovery",
                        "implementation_effort": "low",
                        "timeline_weeks": 3
                    }
                ],
                "fix_effort": "low",
                "priority": "medium",
                "ai_analysis": "Upgrade conversion rate of 8% is 47% below benchmark, with high-usage customers not being effectively monetized.",
                "root_cause_analysis": ["Poor upgrade visibility", "Unclear value proposition", "Timing issues"],
                "quick_wins": ["Add usage-based upgrade prompts", "Highlight premium features", "Improve upgrade flow"],
                "long_term_solutions": ["Dynamic pricing optimization", "Personalized plan recommendations", "Value-based pricing tiers"],
                "success_metrics": ["Upgrade conversion rate", "Average revenue per user", "Plan utilization rate"],
                "estimated_fix_timeline": 3,
                "confidence_score": 0.78
            }
        ]
    
    async def _generate_fallback_leak_models(self, customer_id: str, customer_data: Dict[str, Any], 
                                           funnel_data: List[Dict[str, Any]]) -> List[RevenueLeak]:
        """Generate fallback leak models"""
        fallback_data = self._generate_fallback_leaks(customer_data, funnel_data)
        leaks = []
        
        for leak_data in fallback_data:
            leak = RevenueLeak(
                customer_id=customer_id,
                leak_type=LeakType(leak_data["leak_type"]),
                location=leak_data["location"],
                title=leak_data["title"],
                description=leak_data["description"],
                monthly_impact=leak_data["monthly_impact"],
                annual_impact=leak_data["annual_impact"],
                users_affected=leak_data["users_affected"],
                current_performance=leak_data["current_performance"],
                benchmark_performance=leak_data["benchmark_performance"],
                improvement_potential=leak_data["improvement_potential"],
                suggested_fixes=leak_data["suggested_fixes"],
                fix_effort=ImplementationEffort(leak_data["fix_effort"]),
                priority=Priority(leak_data["priority"]),
                ai_analysis=leak_data["ai_analysis"],
                root_cause_analysis=leak_data["root_cause_analysis"],
                quick_wins=leak_data["quick_wins"],
                long_term_solutions=leak_data["long_term_solutions"],
                success_metrics=leak_data["success_metrics"],
                estimated_fix_timeline=leak_data["estimated_fix_timeline"],
                confidence_score=leak_data["confidence_score"]
            )
            leaks.append(leak)
        
        return leaks
    
    async def analyze_customer_journey(self, customer_id: str, journey_data: List[Dict[str, Any]]) -> CustomerJourney:
        """Analyze complete customer journey for leak points"""
        try:
            # Convert journey data to funnel stages
            funnel_stages = []
            for i, stage_data in enumerate(journey_data):
                stage = FunnelStage(
                    stage_name=stage_data.get("stage_name", f"Stage {i+1}"),
                    stage_order=i,
                    users_entering=int(stage_data.get("users_entering", 1000)),
                    users_completing=int(stage_data.get("users_completing", 800)),
                    conversion_rate=float(stage_data.get("conversion_rate", 0.8)),
                    average_time_in_stage=float(stage_data.get("average_time_in_stage", 24)),
                    drop_off_rate=1.0 - float(stage_data.get("conversion_rate", 0.8)),
                    benchmark_conversion_rate=float(stage_data.get("benchmark_conversion_rate", 0.85))
                )
                funnel_stages.append(stage)
            
            # Identify bottlenecks
            bottleneck_stages = []
            optimization_opportunities = []
            
            for stage in funnel_stages:
                if stage.benchmark_conversion_rate and stage.conversion_rate < stage.benchmark_conversion_rate * 0.9:
                    bottleneck_stages.append(stage.stage_name)
                    optimization_opportunities.append(f"Optimize {stage.stage_name} conversion rate")
            
            # Calculate overall metrics
            total_journey_time = sum(stage.average_time_in_stage for stage in funnel_stages)
            overall_conversion_rate = 1.0
            for stage in funnel_stages:
                overall_conversion_rate *= stage.conversion_rate
            
            customer_journey = CustomerJourney(
                customer_id=customer_id,
                journey_stages=funnel_stages,
                total_journey_time=total_journey_time,
                overall_conversion_rate=overall_conversion_rate,
                bottleneck_stages=bottleneck_stages,
                optimization_opportunities=optimization_opportunities
            )
            
            return customer_journey
            
        except Exception as e:
            print(f"Journey analysis error: {e}")
            # Return minimal journey
            return CustomerJourney(
                customer_id=customer_id,
                journey_stages=[],
                total_journey_time=0.0,
                overall_conversion_rate=0.0,
                bottleneck_stages=[],
                optimization_opportunities=[]
            )
    
    async def get_leak_dashboard(self, customer_id: str) -> LeakDashboardResponse:
        """Get comprehensive revenue leak dashboard"""
        try:
            # Get all leaks for customer
            leaks_cursor = self.db.revenue_leaks.find({"customer_id": customer_id})
            leaks_data = await leaks_cursor.to_list(length=100)
            
            active_leaks = []
            fixed_leaks = []
            
            for leak_data in leaks_data:
                leak = RevenueLeak(**leak_data)
                if leak.status == "active":
                    active_leaks.append(leak)
                elif leak.status == "fixed":
                    fixed_leaks.append(leak)
            
            # Calculate dashboard metrics
            total_monthly_impact = sum(leak.monthly_impact for leak in active_leaks)
            total_annual_impact = sum(leak.annual_impact for leak in active_leaks)
            
            priority_breakdown = {}
            for leak in active_leaks:
                priority_breakdown[leak.priority.value] = priority_breakdown.get(leak.priority.value, 0) + 1
            
            return LeakDashboardResponse(
                active_leaks=active_leaks,
                fixed_leaks=fixed_leaks,
                total_monthly_impact=total_monthly_impact,
                total_annual_impact=total_annual_impact,
                priority_breakdown=priority_breakdown
            )
            
        except Exception as e:
            print(f"Leak dashboard error: {e}")
            return LeakDashboardResponse(
                active_leaks=[],
                fixed_leaks=[],
                total_monthly_impact=0.0,
                total_annual_impact=0.0,
                priority_breakdown={}
            )
    
    async def generate_leak_insights(self, customer_id: str) -> List[AIInsight]:
        """Generate AI insights about revenue leaks"""
        try:
            # Get customer leaks
            leaks_cursor = self.db.revenue_leaks.find({"customer_id": customer_id})
            leaks_data = await leaks_cursor.to_list(length=50)
            
            if not leaks_data:
                return []
            
            # AI analysis of leak patterns
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"leak_insights_{customer_id}",
                system_message="You are an AI revenue optimization expert providing strategic insights about revenue leaks."
            ).with_model("openai", "gpt-4o-mini")
            
            insights_prompt = f"""
            Analyze these revenue leaks and provide strategic insights:
            
            Revenue Leaks: {json.dumps(leaks_data[:10], default=str)}
            
            Provide insights in this JSON format:
            {{
                "insights": [
                    {{
                        "insight_type": "strategic|operational|risk|opportunity",
                        "title": "Insight title",
                        "description": "Detailed insight description",
                        "confidence_score": 0.85,
                        "impact_level": "high|medium|low",
                        "actionable": true
                    }}
                ]
            }}
            """
            
            message = UserMessage(text=insights_prompt)
            response = await chat.send_message(message)
            
            try:
                insights_data = json.loads(response)
                insights = []
                
                for insight_data in insights_data.get("insights", []):
                    insight = AIInsight(
                        insight_type=insight_data.get("insight_type", "strategic"),
                        title=insight_data.get("title", "Revenue Insight"),
                        description=insight_data.get("description", "AI-generated insight"),
                        confidence_score=float(insight_data.get("confidence_score", 0.75)),
                        impact_level=insight_data.get("impact_level", "medium"),
                        actionable=insight_data.get("actionable", True)
                    )
                    insights.append(insight)
                
                return insights
                
            except json.JSONDecodeError:
                # Return fallback insights
                return [
                    AIInsight(
                        insight_type="strategic",
                        title="Funnel Optimization Priority",
                        description="Your revenue leaks are concentrated in conversion bottlenecks, suggesting immediate funnel optimization should be the top priority.",
                        confidence_score=0.88,
                        impact_level="high",
                        actionable=True
                    )
                ]
                
        except Exception as e:
            print(f"Leak insights generation error: {e}")
            return []

# FastAPI Router
revenue_leak_router = APIRouter(prefix="/api/growth/revenue-leaks", tags=["Revenue Leak Detection"])

# Initialize service
leak_detector_service = RevenueLeakDetector()

@revenue_leak_router.post("/scan")
async def scan_revenue_leaks(request: LeakAnalysisRequest):
    """Scan for revenue leaks using AI analysis"""
    try:
        customer_id = "demo_customer_leaks"
        
        revenue_leaks = await leak_detector_service.scan_revenue_leaks(
            customer_id=customer_id,
            customer_data=request.customer_data,
            funnel_data=request.funnel_data,
            focus_areas=request.focus_areas
        )
        
        total_monthly_impact = sum(leak.monthly_impact for leak in revenue_leaks)
        total_annual_impact = sum(leak.annual_impact for leak in revenue_leaks)
        
        return {
            "status": "success",
            "leaks_found": len(revenue_leaks),
            "revenue_leaks": [leak.dict() for leak in revenue_leaks],
            "total_monthly_impact": total_monthly_impact,
            "total_annual_impact": total_annual_impact,
            "scan_timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Revenue leak scanning error: {e}")

@revenue_leak_router.get("/dashboard")
async def get_leak_dashboard():
    """Get comprehensive revenue leak dashboard"""
    try:
        customer_id = "demo_customer_leaks"
        dashboard = await leak_detector_service.get_leak_dashboard(customer_id)
        
        return {
            "status": "success",
            "dashboard": dashboard.dict(),
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {e}")

@revenue_leak_router.get("/insights")
async def get_leak_insights():
    """Get AI-generated insights about revenue leaks"""
    try:
        customer_id = "demo_customer_leaks"
        insights = await leak_detector_service.generate_leak_insights(customer_id)
        
        return {
            "status": "success",
            "insights": [insight.dict() for insight in insights],
            "insights_count": len(insights),
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights error: {e}")

@revenue_leak_router.post("/journey-analysis")
async def analyze_customer_journey(request: Dict[str, Any]):
    """Analyze customer journey for leak points"""
    try:
        customer_id = "demo_customer_leaks"
        journey_data = request.get("journey_data", [])
        
        customer_journey = await leak_detector_service.analyze_customer_journey(customer_id, journey_data)
        
        return {
            "status": "success",
            "customer_journey": customer_journey.dict(),
            "analysis_timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Journey analysis error: {e}")

@revenue_leak_router.get("/{leak_id}")
async def get_leak_details(leak_id: str):
    """Get detailed information about a specific revenue leak"""
    try:
        leak_data = await leak_detector_service.db.revenue_leaks.find_one({"id": leak_id})
        
        if not leak_data:
            raise HTTPException(status_code=404, detail="Revenue leak not found")
        
        leak = RevenueLeak(**leak_data)
        
        return {
            "status": "success",
            "revenue_leak": leak.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Leak details error: {e}")

@revenue_leak_router.post("/{leak_id}/fix")
async def mark_leak_as_fixed(leak_id: str):
    """Mark revenue leak as fixed"""
    try:
        result = await leak_detector_service.db.revenue_leaks.update_one(
            {"id": leak_id},
            {"$set": {"status": "fixed", "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Revenue leak not found")
        
        return {
            "status": "success",
            "message": "Revenue leak marked as fixed",
            "leak_id": leak_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fix marking error: {e}")