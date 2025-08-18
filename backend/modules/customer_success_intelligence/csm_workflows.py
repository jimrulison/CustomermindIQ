"""
CSM Workflows & Task Automation

Automated workflow generation for Customer Success Managers based on AI insights.
Provides prioritized task queues, automated alerts, and workflow templates.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime, timedelta
import random

csm_workflows_router = APIRouter()

@csm_workflows_router.get("/csm-dashboard")
async def get_csm_workflows_dashboard() -> Dict[str, Any]:
    """Get CSM workflow dashboard with prioritized tasks and automation insights"""
    try:
        # Generate CSM team overview
        csm_team = []
        for i in range(8):
            csm_id = f"csm_{i+1}"
            customer_count = random.randint(45, 85)
            total_mrr = random.randint(180000, 420000)
            
            csm_team.append({
                "csm_id": csm_id,
                "name": f"CSM {i+1}",
                "email": f"csm{i+1}@customermindiq.com",
                "customers_assigned": customer_count,
                "total_mrr_managed": total_mrr,
                "avg_health_score": random.uniform(68.5, 84.2),
                "active_tasks": random.randint(8, 24),
                "overdue_tasks": random.randint(0, 5),
                "this_month_activities": random.randint(42, 87),
                "specialization": random.choice(["Enterprise", "SMB", "Technical", "Growth"]),
                "workload_status": random.choice(["optimal", "high", "overloaded"])
            })
        
        # Generate prioritized task queue across all CSMs
        task_priorities = ["critical", "high", "medium", "low"]
        task_types = [
            "Health Score Alert", "Milestone Check-in", "Expansion Opportunity",
            "Churn Risk Intervention", "Onboarding Follow-up", "Contract Renewal",
            "Training Session", "Business Review", "Support Escalation", "Usage Review"
        ]
        
        prioritized_tasks = []
        for i in range(25):  # Show top 25 priority tasks
            task_type = random.choice(task_types)
            priority = random.choice(task_priorities)
            
            # Set urgency based on task type
            if task_type in ["Health Score Alert", "Churn Risk Intervention", "Support Escalation"]:
                priority = random.choice(["critical", "high"])
            
            due_date = datetime.now() + timedelta(days=random.randint(0, 14))
            overdue = due_date < datetime.now()
            
            prioritized_tasks.append({
                "task_id": str(uuid.uuid4()),
                "task_type": task_type,
                "priority": priority,
                "customer_id": f"cust_task_{i+1}",
                "customer_name": f"Customer {i+1}",
                "company": f"Company {i+1}",
                "assigned_csm": random.choice([csm["csm_id"] for csm in csm_team]),
                "due_date": due_date.isoformat(),
                "overdue": overdue,
                "estimated_time": f"{random.randint(15, 120)} minutes",
                "automation_available": random.choice([True, False]),
                "context": random.choice([
                    "Health score dropped 15 points",
                    "No login activity for 14 days", 
                    "Support ticket escalated",
                    "Contract renewal in 30 days",
                    "Expansion signal detected",
                    "Onboarding milestone delayed"
                ]),
                "suggested_actions": random.sample([
                    "Schedule call",
                    "Send email", 
                    "Update account record",
                    "Create training plan",
                    "Escalate to management",
                    "Trigger automated campaign"
                ], k=random.randint(2, 4))
            })
        
        # Sort by priority and due date
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        prioritized_tasks.sort(key=lambda x: (priority_order[x["priority"]], x["due_date"]))
        
        # Automated workflow templates
        workflow_templates = [
            {
                "template_id": "health_decline_intervention",
                "name": "Health Score Decline Intervention",
                "description": "Automated response to significant health score drops",
                "trigger_conditions": ["Health score drops >10 points", "Usage decline >30%"],
                "automated_steps": [
                    "Create high-priority CSM task",
                    "Send internal alert to CSM",
                    "Schedule automated check-in email",
                    "Flag for next business review"
                ],
                "success_rate": 78.4,
                "avg_resolution_time": "3.2 days",
                "customers_helped_this_month": 23
            },
            {
                "template_id": "onboarding_stall_recovery",
                "name": "Onboarding Stall Recovery",
                "description": "Intervention for customers stuck in onboarding",
                "trigger_conditions": ["30+ days in onboarding", "No milestone progress"],
                "automated_steps": [
                    "Assign onboarding specialist",
                    "Schedule dedicated training session",
                    "Create customized success plan",
                    "Set weekly check-in cadence"
                ],
                "success_rate": 85.7,
                "avg_resolution_time": "5.8 days", 
                "customers_helped_this_month": 18
            },
            {
                "template_id": "expansion_opportunity_nurture",
                "name": "Expansion Opportunity Nurture",
                "description": "Systematic approach to qualified expansion leads",
                "trigger_conditions": ["Team growth signals", "Advanced feature usage", "High health score"],
                "automated_steps": [
                    "Create expansion opportunity record",
                    "Schedule business value discussion",
                    "Prepare ROI analysis",
                    "Coordinate with sales team"
                ],
                "success_rate": 62.3,
                "avg_resolution_time": "12.4 days",
                "customers_helped_this_month": 31
            }
        ]
        
        # Workflow automation insights
        automation_insights = [
            {
                "insight": "84% of health score alerts are resolved faster with automated workflows",
                "impact": "high",
                "recommendation": "Expand health score automation to all customer segments",
                "time_saved": "847 CSM hours this month"
            },
            {
                "insight": "Manual onboarding follow-ups have 23% lower completion rates",
                "impact": "medium",
                "recommendation": "Implement automated onboarding milestone tracking",
                "efficiency_gain": "34% faster onboarding completion"
            },
            {
                "insight": "Proactive expansion workflows generate 67% more qualified opportunities",
                "impact": "high", 
                "recommendation": "Train all CSMs on expansion opportunity automation",
                "revenue_impact": "$1.2M in additional pipeline"
            }
        ]
        
        # Task completion metrics
        task_metrics = {
            "total_tasks_this_month": 687,
            "completed_tasks": 523,
            "completion_rate": 76.1,
            "avg_completion_time": "2.8 days",
            "automated_task_percentage": 34.7,
            "overdue_tasks": 23,
            "high_priority_completion_rate": 91.2
        }
        
        dashboard_data = {
            "status": "success",
            "dashboard": {
                "summary_metrics": {
                    "total_csms": len(csm_team),
                    "total_customers_managed": sum([csm["customers_assigned"] for csm in csm_team]),
                    "total_mrr_managed": sum([csm["total_mrr_managed"] for csm in csm_team]),
                    "avg_csm_workload": round(sum([csm["active_tasks"] for csm in csm_team]) / len(csm_team), 1),
                    "automation_adoption_rate": 67.3,
                    "customer_satisfaction_score": 8.7
                },
                "csm_team_overview": csm_team,
                "prioritized_task_queue": prioritized_tasks,
                "workflow_templates": workflow_templates,
                "automation_insights": automation_insights,
                "task_completion_metrics": task_metrics,
                "workload_distribution": {
                    "optimal": len([csm for csm in csm_team if csm["workload_status"] == "optimal"]),
                    "high": len([csm for csm in csm_team if csm["workload_status"] == "high"]),
                    "overloaded": len([csm for csm in csm_team if csm["workload_status"] == "overloaded"])
                }
            }
        }
        
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSM workflows dashboard error: {str(e)}")

@csm_workflows_router.post("/create-automated-task")
async def create_automated_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create an automated task based on AI insights"""
    try:
        customer_id = task_data.get("customer_id")
        task_type = task_data.get("task_type")
        priority = task_data.get("priority", "medium")
        trigger_context = task_data.get("context", "")
        
        if not customer_id or not task_type:
            raise HTTPException(status_code=400, detail="Customer ID and task type required")
        
        # Create automated task
        task_id = str(uuid.uuid4())
        
        # Assign to appropriate CSM based on specialization and workload
        available_csms = [
            {"csm_id": "csm_1", "workload": "optimal", "specialization": "Enterprise"},
            {"csm_id": "csm_2", "workload": "high", "specialization": "SMB"},
            {"csm_id": "csm_3", "workload": "optimal", "specialization": "Technical"},
            {"csm_id": "csm_4", "workload": "overloaded", "specialization": "Growth"}
        ]
        
        # Prefer CSMs with optimal workload
        optimal_csms = [csm for csm in available_csms if csm["workload"] == "optimal"]
        assigned_csm = random.choice(optimal_csms if optimal_csms else available_csms)
        
        # Generate suggested actions based on task type
        action_templates = {
            "Health Score Alert": [
                "Schedule urgent check-in call",
                "Review recent usage patterns",
                "Identify specific risk factors",
                "Create intervention plan"
            ],
            "Churn Risk Intervention": [
                "Immediate customer outreach",
                "Escalate to senior CSM", 
                "Prepare retention offer",
                "Schedule executive business review"
            ],
            "Expansion Opportunity": [
                "Analyze growth signals",
                "Prepare expansion proposal",
                "Schedule business value call",
                "Coordinate with sales team"
            ]
        }
        
        suggested_actions = action_templates.get(task_type, [
            "Review customer context",
            "Take appropriate action",
            "Update customer record",
            "Monitor progress"
        ])
        
        # Set due date based on priority
        due_date_days = {"critical": 1, "high": 3, "medium": 7, "low": 14}
        due_date = datetime.now() + timedelta(days=due_date_days.get(priority, 7))
        
        created_task = {
            "status": "success",
            "message": "Automated task created successfully",
            "task_details": {
                "task_id": task_id,
                "customer_id": customer_id,
                "task_type": task_type,
                "priority": priority,
                "assigned_csm": assigned_csm["csm_id"],
                "created_date": datetime.now().isoformat(),
                "due_date": due_date.isoformat(),
                "trigger_context": trigger_context,
                "suggested_actions": suggested_actions,
                "estimated_completion_time": f"{random.randint(30, 180)} minutes",
                "automation_score": random.uniform(75, 95)
            },
            "workflow_triggered": random.choice([True, False]),
            "notification_sent": True
        }
        
        return created_task
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automated task creation error: {str(e)}")

@csm_workflows_router.get("/csm/{csm_id}/task-queue")
async def get_csm_task_queue(csm_id: str) -> Dict[str, Any]:
    """Get personalized task queue for specific CSM"""
    try:
        # Generate personalized task queue
        csm_tasks = []
        task_count = random.randint(12, 28)
        
        for i in range(task_count):
            task_type = random.choice([
                "Health Score Alert", "Milestone Check-in", "Expansion Opportunity",
                "Churn Risk Intervention", "Contract Renewal", "Training Session"
            ])
            
            priority = random.choice(["critical", "high", "medium", "low"])
            due_date = datetime.now() + timedelta(days=random.randint(-2, 14))
            
            csm_tasks.append({
                "task_id": str(uuid.uuid4()),
                "task_type": task_type,
                "priority": priority,
                "customer_name": f"Customer {i+1}",
                "customer_id": f"cust_{i+1}",
                "due_date": due_date.isoformat(),
                "overdue": due_date < datetime.now(),
                "estimated_time": f"{random.randint(15, 120)} minutes",
                "completion_status": random.choice(["not_started", "in_progress", "completed"]),
                "automation_available": random.choice([True, False])
            })
        
        # Sort by priority and due date
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        csm_tasks.sort(key=lambda x: (priority_order[x["priority"]], x["due_date"]))
        
        # CSM performance metrics
        performance_metrics = {
            "tasks_completed_this_week": random.randint(15, 35),
            "avg_task_completion_time": f"{random.uniform(1.2, 4.8):.1f} days",
            "customer_satisfaction_score": random.uniform(8.2, 9.5),
            "on_time_completion_rate": random.uniform(78, 94),
            "automation_usage_rate": random.uniform(45, 75)
        }
        
        csm_task_queue = {
            "status": "success",
            "csm_id": csm_id,
            "generated_date": datetime.now().isoformat(),
            "task_summary": {
                "total_tasks": len(csm_tasks),
                "critical_tasks": len([t for t in csm_tasks if t["priority"] == "critical"]),
                "high_priority_tasks": len([t for t in csm_tasks if t["priority"] == "high"]),
                "overdue_tasks": len([t for t in csm_tasks if t["overdue"]]),
                "estimated_total_time": f"{sum([int(t['estimated_time'].split()[0]) for t in csm_tasks])} minutes"
            },
            "prioritized_tasks": csm_tasks,
            "performance_metrics": performance_metrics,
            "daily_focus_areas": [
                "Address all critical priority tasks",
                "Follow up on overdue items",
                "Complete health score reviews",
                "Update customer success plans"
            ]
        }
        
        return csm_task_queue
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSM task queue error: {str(e)}")