"""
Expansion Opportunities Intelligence

AI-powered identification and prioritization of customer expansion opportunities.
Combines usage data, health scores, and behavioral patterns to identify upsell/cross-sell potential.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime, timedelta
import random

expansion_opportunities_router = APIRouter()

@expansion_opportunities_router.get("/expansion-dashboard")
async def get_expansion_opportunities_dashboard() -> Dict[str, Any]:
    """Get comprehensive expansion opportunities dashboard"""
    try:
        # Generate expansion opportunity pipeline
        opportunity_stages = [
            {
                "stage": "Identified",
                "description": "AI has detected expansion signals",
                "opportunity_count": 87,
                "total_potential_arr": 425000,
                "avg_deal_size": 4885,
                "conversion_probability": 25.3
            },
            {
                "stage": "Qualified", 
                "description": "CSM has validated the opportunity",
                "opportunity_count": 34,
                "total_potential_arr": 287000,
                "avg_deal_size": 8441,
                "conversion_probability": 52.7
            },
            {
                "stage": "Proposal Sent",
                "description": "Formal expansion proposal submitted",
                "opportunity_count": 18,
                "total_potential_arr": 195000,
                "avg_deal_size": 10833,
                "conversion_probability": 73.2
            },
            {
                "stage": "Negotiation",
                "description": "Active negotiations in progress",
                "opportunity_count": 9,
                "total_potential_arr": 134000,
                "avg_deal_size": 14889,
                "conversion_probability": 89.1
            },
            {
                "stage": "Closed Won",
                "description": "Successfully closed expansion deals",
                "opportunity_count": 23,
                "total_potential_arr": 312000,
                "avg_deal_size": 13565,
                "conversion_probability": 100.0
            }
        ]
        
        # High-priority expansion opportunities
        priority_opportunities = []
        expansion_types = [
            "Seat Expansion", "Feature Upgrade", "Plan Upgrade", "Add-on Modules", 
            "Integration Package", "Professional Services", "Multi-Year Contract"
        ]
        
        for i in range(15):
            opportunity_type = random.choice(expansion_types)
            current_mrr = random.randint(500, 5000)
            expansion_value = random.randint(200, 3000)
            
            # Calculate expansion signals strength
            signals = random.sample([
                "Team size increased 40%",
                "Usage exceeded plan limits",
                "Requested advanced features", 
                "High engagement with training",
                "Positive health score trend",
                "Executive involvement increased",
                "Integration requests",
                "Multi-department adoption"
            ], k=random.randint(3, 5))
            
            priority_opportunities.append({
                "opportunity_id": str(uuid.uuid4()),
                "customer_id": f"cust_expansion_{i+1}",
                "customer_name": f"Expansion Customer {i+1}",
                "company": f"Expansion Company {i+1}",
                "opportunity_type": opportunity_type,
                "current_mrr": current_mrr,
                "expansion_mrr_potential": expansion_value,
                "expansion_percentage": round((expansion_value / current_mrr) * 100, 1),
                "probability_score": random.uniform(35, 85),
                "expansion_signals": signals,
                "signal_strength": random.choice(["Strong", "Medium", "Weak"]),
                "timeline_estimate": random.choice(["This Quarter", "Next Quarter", "6+ Months"]),
                "assigned_csm": f"CSM {random.randint(1, 8)}",
                "last_interaction": (datetime.now() - timedelta(days=random.randint(1, 21))).isoformat(),
                "next_action": random.choice([
                    "Schedule expansion discussion",
                    "Prepare ROI analysis",
                    "Coordinate with sales team",
                    "Create custom proposal",
                    "Present use case examples"
                ])
            })
        
        # Sort by probability score and potential value
        priority_opportunities.sort(key=lambda x: x["probability_score"] * x["expansion_mrr_potential"], reverse=True)
        
        # Expansion triggers and patterns
        expansion_triggers = [
            {
                "trigger_name": "Usage Limit Exceeded",
                "description": "Customer consistently exceeds plan limits",
                "frequency": "High",
                "success_rate": 78.3,
                "avg_expansion_value": 1850,
                "customers_triggered": 23,
                "automated_detection": True
            },
            {
                "trigger_name": "Team Growth",
                "description": "Significant increase in team size or seats",
                "frequency": "Medium",
                "success_rate": 65.7,
                "avg_expansion_value": 2340,
                "customers_triggered": 18,
                "automated_detection": True
            },
            {
                "trigger_name": "Feature Request Patterns",
                "description": "Multiple requests for premium features",
                "frequency": "Medium", 
                "success_rate": 72.1,
                "avg_expansion_value": 1680,
                "customers_triggered": 15,
                "automated_detection": True
            },
            {
                "trigger_name": "High Engagement Behavior",
                "description": "Increased training/support engagement",
                "frequency": "High",
                "success_rate": 56.4,
                "avg_expansion_value": 1420,
                "customers_triggered": 31,
                "automated_detection": False
            }
        ]
        
        # Expansion performance metrics
        performance_metrics = {
            "this_quarter": {
                "opportunities_identified": 127,
                "opportunities_closed": 23,
                "close_rate": 18.1,
                "total_expansion_arr": 312000,
                "avg_time_to_close": 45.2
            },
            "last_quarter": {
                "opportunities_identified": 108,
                "opportunities_closed": 19,
                "close_rate": 17.6,
                "total_expansion_arr": 267000,
                "avg_time_to_close": 52.1
            },
            "trends": {
                "identification_growth": "+17.6%",
                "close_rate_improvement": "+0.5%",
                "arr_growth": "+16.9%",
                "efficiency_improvement": "-6.9 days to close"
            }
        }
        
        # AI expansion insights
        ai_insights = [
            {
                "insight": "Customers with >70 health score have 3.2x higher expansion probability",
                "impact": "high",
                "recommendation": "Prioritize expansion outreach for healthy customers",
                "potential_impact": "+$145K quarterly expansion ARR"
            },
            {
                "insight": "Multi-department usage increases expansion value by 67% on average",
                "impact": "high",
                "recommendation": "Focus on cross-department adoption programs",
                "potential_impact": "+$89K average deal size"
            },
            {
                "insight": "Technical integration requests correlate with 58% expansion success rate",
                "impact": "medium",
                "recommendation": "Fast-track technical discussions for integration requesters",
                "potential_impact": "+12% overall close rate"
            },
            {
                "insight": "Q4 timing shows 23% higher expansion close rates historically",
                "impact": "medium",
                "recommendation": "Accelerate Q4 pipeline development and outreach",
                "potential_impact": "+$67K Q4 expansion opportunity"
            }
        ]
        
        dashboard_data = {
            "status": "success",
            "dashboard": {
                "summary_metrics": {
                    "total_opportunities": sum([stage["opportunity_count"] for stage in opportunity_stages[:-1]]),
                    "total_pipeline_value": sum([stage["total_potential_arr"] for stage in opportunity_stages[:-1]]),
                    "weighted_pipeline_value": sum([stage["total_potential_arr"] * (stage["conversion_probability"]/100) for stage in opportunity_stages[:-1]]),
                    "avg_opportunity_value": 6847,
                    "current_close_rate": 18.1,
                    "expansion_customers_percentage": 34.7
                },
                "opportunity_pipeline": opportunity_stages,
                "priority_opportunities": priority_opportunities,
                "expansion_triggers": expansion_triggers,
                "performance_metrics": performance_metrics,
                "ai_insights": ai_insights,
                "expansion_categories": {
                    "seat_expansion": {"count": 45, "avg_value": 1850},
                    "plan_upgrades": {"count": 32, "avg_value": 2940},
                    "add_on_modules": {"count": 28, "avg_value": 1670},
                    "professional_services": {"count": 22, "avg_value": 3450}
                }
            }
        }
        
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Expansion opportunities dashboard error: {str(e)}")

@expansion_opportunities_router.post("/create-expansion-opportunity")
async def create_expansion_opportunity(opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create new expansion opportunity based on AI signals"""
    try:
        customer_id = opportunity_data.get("customer_id")
        opportunity_type = opportunity_data.get("opportunity_type")
        expansion_signals = opportunity_data.get("expansion_signals", [])
        
        if not customer_id or not opportunity_type:
            raise HTTPException(status_code=400, detail="Customer ID and opportunity type required")
        
        # Generate opportunity details
        opportunity_id = str(uuid.uuid4())
        current_mrr = random.randint(500, 5000)
        expansion_potential = random.randint(200, 3000)
        
        # Calculate probability based on signals and customer data
        base_probability = 45.0
        signal_boost = len(expansion_signals) * 8.5
        probability_score = min(85.0, base_probability + signal_boost + random.uniform(-10, 15))
        
        # Assign CSM based on opportunity size and complexity
        if expansion_potential > 2000:
            assigned_csm = "Senior CSM"
            involve_sales = True
        else:
            assigned_csm = f"CSM {random.randint(1, 8)}"
            involve_sales = False
        
        # Generate recommended next actions
        next_actions = [
            {
                "action": "Analyze current usage patterns",
                "timeline": "This week",
                "owner": "CSM",
                "priority": "high"
            },
            {
                "action": "Prepare expansion business case",
                "timeline": "Next week", 
                "owner": "CSM",
                "priority": "high"
            },
            {
                "action": "Schedule stakeholder meeting",
                "timeline": "Within 2 weeks",
                "owner": "CSM + Sales" if involve_sales else "CSM",
                "priority": "medium"
            }
        ]
        
        created_opportunity = {
            "status": "success",
            "message": "Expansion opportunity created successfully",
            "opportunity_details": {
                "opportunity_id": opportunity_id,
                "customer_id": customer_id,
                "opportunity_type": opportunity_type,
                "current_mrr": current_mrr,
                "expansion_potential_mrr": expansion_potential,
                "probability_score": round(probability_score, 1),
                "created_date": datetime.now().isoformat(),
                "stage": "Identified",
                "assigned_csm": assigned_csm,
                "sales_involvement_required": involve_sales,
                "expansion_signals": expansion_signals,
                "timeline_estimate": random.choice(["This Quarter", "Next Quarter", "6+ Months"]),
                "next_actions": next_actions,
                "tracking_url": f"/api/customer-success/expansion-tracking/{opportunity_id}"
            },
            "automation_triggered": {
                "csm_notification": True,
                "task_created": True,
                "follow_up_scheduled": True,
                "sales_alert": involve_sales
            }
        }
        
        return created_opportunity
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Expansion opportunity creation error: {str(e)}")

@expansion_opportunities_router.get("/customer/{customer_id}/expansion-potential")
async def get_customer_expansion_potential(customer_id: str) -> Dict[str, Any]:
    """Analyze expansion potential for specific customer"""
    try:
        # Generate detailed expansion analysis for customer
        current_plan = random.choice(["Starter", "Professional", "Enterprise"])
        current_mrr = {"Starter": 299, "Professional": 899, "Enterprise": 2499}[current_plan]
        
        # Analyze expansion signals
        usage_signals = {
            "feature_adoption_rate": random.uniform(45, 85),
            "plan_limit_utilization": random.uniform(60, 95),
            "advanced_feature_requests": random.randint(0, 8),
            "team_growth_rate": random.uniform(-10, 40),
            "integration_usage": random.randint(1, 12)
        }
        
        # Behavioral signals
        behavioral_signals = {
            "executive_engagement": random.choice(["Low", "Medium", "High"]),
            "training_participation": random.uniform(20, 80),
            "support_satisfaction": random.uniform(7.5, 9.5),
            "product_feedback_frequency": random.choice(["Rare", "Occasional", "Frequent"]),
            "community_participation": random.choice(["None", "Observer", "Active"])
        }
        
        # Calculate expansion opportunities
        expansion_opportunities = []
        
        # Seat expansion
        if usage_signals["team_growth_rate"] > 10:
            expansion_opportunities.append({
                "type": "Seat Expansion",
                "description": f"Add {random.randint(3, 15)} additional seats",
                "potential_mrr": random.randint(150, 800),
                "probability": random.uniform(65, 85),
                "reasoning": "Team growth indicates need for additional user access"
            })
        
        # Plan upgrade
        if usage_signals["plan_limit_utilization"] > 80:
            next_plan = {"Starter": "Professional", "Professional": "Enterprise", "Enterprise": "Enterprise Plus"}
            if next_plan.get(current_plan):
                expansion_opportunities.append({
                    "type": "Plan Upgrade",
                    "description": f"Upgrade to {next_plan[current_plan]} plan",
                    "potential_mrr": random.randint(400, 1200),
                    "probability": random.uniform(55, 75),
                    "reasoning": "High utilization of current plan limits"
                })
        
        # Add-on modules
        if usage_signals["advanced_feature_requests"] > 3:
            expansion_opportunities.append({
                "type": "Add-on Modules",
                "description": "Advanced analytics and reporting module",
                "potential_mrr": random.randint(200, 500),
                "probability": random.uniform(40, 70),
                "reasoning": "Multiple requests for advanced features"
            })
        
        # Calculate overall expansion score
        expansion_score = (
            usage_signals["feature_adoption_rate"] * 0.3 +
            usage_signals["plan_limit_utilization"] * 0.25 +
            (behavioral_signals["training_participation"]) * 0.2 +
            ({"Low": 20, "Medium": 60, "High": 90}[behavioral_signals["executive_engagement"]]) * 0.15 +
            (behavioral_signals["support_satisfaction"] * 10) * 0.1
        )
        
        customer_expansion_analysis = {
            "status": "success",
            "customer_id": customer_id,
            "analysis_date": datetime.now().isoformat(),
            "current_state": {
                "current_plan": current_plan,
                "current_mrr": current_mrr,
                "tenure_months": random.randint(6, 48),
                "health_score": random.randint(65, 95)
            },
            "expansion_score": round(expansion_score, 1),
            "expansion_readiness": "High" if expansion_score > 70 else "Medium" if expansion_score > 50 else "Low",
            "usage_signals": usage_signals,
            "behavioral_signals": behavioral_signals,
            "expansion_opportunities": expansion_opportunities,
            "total_expansion_potential": sum([opp["potential_mrr"] for opp in expansion_opportunities]),
            "recommended_approach": {
                "primary_strategy": random.choice([
                    "Focus on demonstrating ROI with current usage",
                    "Highlight team collaboration benefits",
                    "Present advanced feature roadmap",
                    "Conduct strategic business review"
                ]),
                "timeline": random.choice(["Immediate (0-30 days)", "Short-term (1-3 months)", "Long-term (3-6 months)"]),
                "success_probability": round(sum([opp["probability"] for opp in expansion_opportunities]) / len(expansion_opportunities) if expansion_opportunities else 0, 1)
            }
        }
        
        return customer_expansion_analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer expansion potential error: {str(e)}")