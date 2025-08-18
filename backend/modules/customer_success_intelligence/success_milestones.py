"""
Success Milestones Tracking

Track customer journey milestones, onboarding progress, and success indicators.
Provides automated milestone detection and success playbook recommendations.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime, timedelta
import random

success_milestones_router = APIRouter()

@success_milestones_router.get("/milestones-dashboard")
async def get_success_milestones_dashboard() -> Dict[str, Any]:
    """Get success milestones tracking dashboard"""
    try:
        # Define standard success milestones
        milestone_definitions = [
            {
                "milestone_id": "onboarding_complete",
                "name": "Onboarding Complete",
                "description": "Customer has completed initial setup and training",
                "typical_timeframe": "0-30 days",
                "success_indicators": ["Account setup", "First feature use", "Training completion"],
                "completion_rate": 87.3,
                "avg_time_to_complete": 18.5
            },
            {
                "milestone_id": "first_value_realized", 
                "name": "First Value Realized",
                "description": "Customer has achieved their first meaningful outcome",
                "typical_timeframe": "30-60 days",
                "success_indicators": ["Core workflow active", "Positive feedback", "Regular usage"],
                "completion_rate": 74.2,
                "avg_time_to_complete": 42.3
            },
            {
                "milestone_id": "product_adoption",
                "name": "Product Adoption",
                "description": "Customer is actively using multiple features regularly",
                "typical_timeframe": "60-90 days", 
                "success_indicators": ["Multi-feature usage", "Daily active use", "Team adoption"],
                "completion_rate": 68.9,
                "avg_time_to_complete": 67.8
            },
            {
                "milestone_id": "expansion_ready",
                "name": "Expansion Ready",
                "description": "Customer is showing signs of growth and expansion potential",
                "typical_timeframe": "90-180 days",
                "success_indicators": ["Team growth", "Advanced features", "Integration usage"],
                "completion_rate": 45.7,
                "avg_time_to_complete": 124.2
            },
            {
                "milestone_id": "advocate_status",
                "name": "Customer Advocate",
                "description": "Customer is actively promoting and referring the product",
                "typical_timeframe": "180+ days",
                "success_indicators": ["Referrals made", "Case study", "Public testimonial"],
                "completion_rate": 23.4,
                "avg_time_to_complete": 287.6
            }
        ]
        
        # Generate customer milestone progress
        customers_by_milestone = {}
        total_customers = 1247
        
        for milestone in milestone_definitions:
            customers_at_milestone = int(total_customers * (milestone["completion_rate"] / 100))
            
            # Generate sample customers at this milestone
            customer_samples = []
            for i in range(min(10, customers_at_milestone)):  # Show top 10 per milestone
                days_in_milestone = random.randint(1, int(milestone["avg_time_to_complete"]))
                progress_percentage = min(100, (days_in_milestone / milestone["avg_time_to_complete"]) * 100)
                
                customer_samples.append({
                    "customer_id": f"cust_milestone_{milestone['milestone_id']}_{i+1}",
                    "customer_name": f"Customer {i+1}",
                    "company": f"Company {i+1}",
                    "days_in_milestone": days_in_milestone,
                    "progress_percentage": round(progress_percentage, 1),
                    "next_actions": random.sample([
                        "Schedule check-in call",
                        "Send training resources", 
                        "Introduce advanced features",
                        "Connect with success stories",
                        "Provide implementation support"
                    ], k=random.randint(1, 3)),
                    "risk_level": random.choice(["low", "medium", "high"]),
                    "csm_assigned": f"CSM {random.randint(1, 8)}",
                    "mrr": random.randint(299, 2999)
                })
            
            customers_by_milestone[milestone["milestone_id"]] = {
                "milestone_info": milestone,
                "total_customers": customers_at_milestone,
                "customer_samples": customer_samples
            }
        
        # Milestone performance trends
        milestone_trends = []
        for i in range(12, 0, -1):  # Last 12 months
            month_date = datetime.now() - timedelta(days=30*i)
            milestone_trends.append({
                "month": month_date.strftime("%Y-%m"),
                "onboarding_completion": random.uniform(82, 92),
                "first_value_time": random.uniform(38, 48),
                "adoption_rate": random.uniform(64, 74),
                "expansion_rate": random.uniform(40, 50)
            })
        
        # At-risk milestone analysis
        at_risk_customers = []
        for i in range(8):
            milestone_stuck = random.choice(milestone_definitions)
            days_stuck = random.randint(30, 120)
            expected_completion = milestone_stuck["avg_time_to_complete"]
            
            at_risk_customers.append({
                "customer_id": f"cust_risk_{i+1}",
                "customer_name": f"At-Risk Customer {i+1}",
                "stuck_at_milestone": milestone_stuck["name"],
                "days_stuck": days_stuck,
                "expected_completion_days": expected_completion,
                "delay_percentage": round(((days_stuck - expected_completion) / expected_completion) * 100, 1),
                "intervention_urgency": "high" if days_stuck > expected_completion * 1.5 else "medium",
                "potential_churn_risk": min(95, max(15, (days_stuck / expected_completion) * 45)),
                "recommended_intervention": random.choice([
                    "Immediate CSM outreach",
                    "Executive business review", 
                    "Technical implementation support",
                    "Custom training session",
                    "Product specialist consultation"
                ])
            })
        
        # Success playbook recommendations
        playbook_recommendations = [
            {
                "playbook_name": "Onboarding Acceleration",
                "target_milestone": "onboarding_complete",
                "trigger_conditions": ["7+ days in onboarding", "No recent activity"],
                "automated_actions": ["Send welcome email sequence", "Schedule onboarding call", "Assign CSM"],
                "success_rate": 89.2,
                "customers_eligible": 67
            },
            {
                "playbook_name": "Value Realization Boost",
                "target_milestone": "first_value_realized", 
                "trigger_conditions": ["30+ days without value milestone", "Low feature usage"],
                "automated_actions": ["Send use case examples", "Offer 1:1 training", "Share success stories"],
                "success_rate": 76.8,
                "customers_eligible": 89
            },
            {
                "playbook_name": "Adoption Acceleration",
                "target_milestone": "product_adoption",
                "trigger_conditions": ["Single feature usage only", "Team size = 1"],
                "automated_actions": ["Team invitation prompts", "Feature tour", "Integration setup"],
                "success_rate": 68.3,
                "customers_eligible": 124
            }
        ]
        
        dashboard_data = {
            "status": "success",
            "dashboard": {
                "summary_metrics": {
                    "total_customers_tracked": total_customers,
                    "avg_onboarding_time": 18.5,
                    "avg_time_to_value": 42.3,
                    "overall_milestone_completion_rate": 67.8,
                    "customers_at_risk": len(at_risk_customers),
                    "automated_interventions_active": 14
                },
                "milestone_definitions": milestone_definitions,
                "customers_by_milestone": customers_by_milestone,
                "milestone_trends": milestone_trends,
                "at_risk_analysis": at_risk_customers,
                "playbook_recommendations": playbook_recommendations,
                "success_metrics": {
                    "milestone_acceleration": "+12.3% this quarter",
                    "time_to_value_improvement": "-8.7 days average",
                    "completion_rate_trend": "+4.2% this month"
                }
            }
        }
        
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Success milestones dashboard error: {str(e)}")

@success_milestones_router.post("/trigger-playbook")
async def trigger_success_playbook(playbook_data: Dict[str, Any]) -> Dict[str, Any]:
    """Trigger a success playbook for specific customers"""
    try:
        playbook_name = playbook_data.get("playbook_name")
        customer_ids = playbook_data.get("customer_ids", [])
        
        if not playbook_name or not customer_ids:
            raise HTTPException(status_code=400, detail="Playbook name and customer IDs required")
        
        # Simulate playbook execution
        execution_results = []
        for customer_id in customer_ids:
            execution_results.append({
                "customer_id": customer_id,
                "status": random.choice(["initiated", "in_progress", "completed"]),
                "actions_triggered": random.randint(2, 5),
                "estimated_completion": random.choice(["2-3 days", "1 week", "2 weeks"]),
                "success_probability": random.uniform(65, 95)
            })
        
        playbook_result = {
            "status": "success",
            "message": f"Playbook '{playbook_name}' triggered for {len(customer_ids)} customers",
            "execution_id": str(uuid.uuid4()),
            "details": {
                "playbook_name": playbook_name,
                "customers_targeted": len(customer_ids),
                "execution_results": execution_results,
                "total_actions_triggered": sum([r["actions_triggered"] for r in execution_results]),
                "estimated_impact": f"+{random.randint(15, 35)}% milestone completion rate"
            },
            "tracking_url": f"/api/customer-success/playbook-tracking/{str(uuid.uuid4())}"
        }
        
        return playbook_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playbook trigger error: {str(e)}")

@success_milestones_router.get("/customer/{customer_id}/milestone-progress")
async def get_customer_milestone_progress(customer_id: str) -> Dict[str, Any]:
    """Get detailed milestone progress for specific customer"""
    try:
        # Generate customer milestone journey
        customer_milestones = []
        current_date = datetime.now()
        
        milestones = [
            ("onboarding_complete", "Onboarding Complete", 18),
            ("first_value_realized", "First Value Realized", 42),
            ("product_adoption", "Product Adoption", 68),
            ("expansion_ready", "Expansion Ready", 124),
            ("advocate_status", "Customer Advocate", 288)
        ]
        
        customer_start_date = current_date - timedelta(days=random.randint(30, 400))
        
        for i, (milestone_id, milestone_name, typical_days) in enumerate(milestones):
            milestone_date = customer_start_date + timedelta(days=typical_days + random.randint(-10, 20))
            days_from_start = (milestone_date - customer_start_date).days
            
            # Determine if milestone is completed, in progress, or upcoming
            if milestone_date <= current_date:
                status = "completed"
                completion_date = milestone_date.isoformat()
                progress = 100
            elif i == 0 or customer_milestones[i-1]["status"] == "completed":
                status = "in_progress"
                completion_date = None
                days_in_progress = (current_date - (customer_milestones[i-1]["completion_date"] if i > 0 else customer_start_date)).days
                progress = min(95, (days_in_progress / typical_days) * 100)
            else:
                status = "upcoming"
                completion_date = None
                progress = 0
            
            customer_milestones.append({
                "milestone_id": milestone_id,
                "milestone_name": milestone_name,
                "status": status,
                "progress_percentage": round(progress, 1),
                "completion_date": completion_date,
                "days_from_start": days_from_start,
                "typical_timeframe": f"{typical_days} days",
                "ahead_behind_schedule": random.randint(-15, 10) if status == "completed" else None
            })
        
        # Current focus and next steps
        current_milestone = next((m for m in customer_milestones if m["status"] == "in_progress"), None)
        if not current_milestone:
            current_milestone = next((m for m in customer_milestones if m["status"] == "upcoming"), customer_milestones[-1])
        
        customer_progress = {
            "status": "success",
            "customer_id": customer_id,
            "analysis_date": current_date.isoformat(),
            "customer_lifecycle": {
                "start_date": customer_start_date.isoformat(),
                "days_active": (current_date - customer_start_date).days,
                "current_stage": current_milestone["milestone_name"],
                "overall_progress": round(sum([m["progress_percentage"] for m in customer_milestones]) / len(customer_milestones), 1)
            },
            "milestone_progress": customer_milestones,
            "current_focus": {
                "milestone": current_milestone["milestone_name"],
                "progress": current_milestone["progress_percentage"],
                "next_actions": random.sample([
                    "Schedule progress review",
                    "Provide additional training",
                    "Introduce team members",
                    "Share best practices",
                    "Set up advanced features"
                ], k=3),
                "success_indicators_met": random.randint(1, 4),
                "success_indicators_total": 4
            },
            "recommendations": [
                {
                    "action": "Focus on feature adoption",
                    "priority": "high",
                    "expected_impact": "Accelerate milestone by 7-10 days"
                },
                {
                    "action": "Increase engagement touchpoints",
                    "priority": "medium", 
                    "expected_impact": "Improve overall progress by 15%"
                }
            ]
        }
        
        return customer_progress
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer milestone progress error: {str(e)}")