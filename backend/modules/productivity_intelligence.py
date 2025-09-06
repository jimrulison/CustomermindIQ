"""
Daily Productivity Intelligence Module
AI-powered productivity and workflow optimization system for Customer Mind IQ
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import os
import uuid
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# LLM setup
EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

router = APIRouter()

# Pydantic Models
class ProductivityInsightRequest(BaseModel):
    prompt: str = Field(..., description="Productivity analysis prompt")
    context_type: str = Field(default="comprehensive", description="Type of data context to include")
    workflow_focus: str = Field(default="daily", description="Focus area for productivity analysis")

class ProductivityInsightResponse(BaseModel):
    insight_id: str
    prompt: str
    analysis: str
    data_summary: Dict[str, Any]
    recommendations: List[str]
    action_items: List[str]
    priority_level: str
    estimated_time_savings: str
    created_at: datetime
    processing_time: float

# Productivity Prompt Templates
PRODUCTIVITY_PROMPTS = {
    "getting_started": [
        "What data sources should I connect first for the biggest impact?",
        "Show me the 5 most important dashboards for my business type",
        "What baseline metrics should I establish before making changes?"
    ],
    "daily_monitoring": [
        "What needs my immediate attention today?",
        "Show me yesterday's performance against targets",
        "Which customers should I reach out to today?",
        "What patterns emerged in today's data?",
        "Set tomorrow's priorities based on today's data"
    ],
    "weekly_analysis": [
        "What should I focus on this week to move the needle?",
        "Show me last week's wins and areas needing attention",
        "Summarize this week's business performance trends",
        "What experiments should I run next week?"
    ],
    "monthly_strategic": [
        "What are the top 3 opportunities to grow revenue next month?",
        "Which initiatives from last month delivered the best ROI?",
        "What warning signs suggest I should change strategy?"
    ],
    "immediate_attention": [
        "Alert me to any data anomalies that could indicate serious problems",
        "Show me customers with sudden behavior changes",
        "What revenue-critical issues need fixing this week?",
        "Which customers are showing expansion signals right now?",
        "What quick wins could I implement today?"
    ],
    "workflow_optimization": [
        "Show me my most time-consuming data analysis tasks",
        "What routine decisions could CustomerMindIQ make automatically?",
        "Create my personalized daily dashboard",
        "How much time is CustomerMindIQ saving me versus manual analysis?",
        "What insights am I getting now that I couldn't see before?"
    ]
}

# Enhanced Data Context Builders
async def get_comprehensive_context() -> Dict[str, Any]:
    """Get comprehensive business context combining customer and website data"""
    try:
        # Customer data
        total_customers = await db.customers.count_documents({})
        customer_segments = await db.customers.aggregate([
            {"$group": {"_id": "$segment", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]).to_list(length=10)
        
        # High-risk customers
        high_risk_customers = await db.customers.find(
            {"churn_risk": {"$in": ["High", "Critical"]}},
            {"customer_id": 1, "name": 1, "churn_risk": 1, "total_spent": 1}
        ).limit(5).to_list(length=5)
        
        # Revenue data
        revenue_pipeline = await db.customers.aggregate([
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total_spent"}}},
        ]).to_list(length=1)
        total_revenue = revenue_pipeline[0]["total_revenue"] if revenue_pipeline else 0
        
        # Campaign data
        active_campaigns = await db.campaigns.count_documents({"status": "active"})
        campaign_performance = await db.campaigns.aggregate([
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]).to_list(length=5)
        
        # Recent activity (last 24 hours)
        yesterday = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        recent_activity = {
            "new_customers": await db.customers.count_documents({"created_at": {"$gte": yesterday}}),
            "support_tickets": await db.support_tickets.count_documents({"created_at": {"$gte": yesterday}}) if hasattr(db, 'support_tickets') else 0,
        }
        
        return {
            "customer_overview": {
                "total_customers": total_customers,
                "customer_segments": customer_segments,
                "high_risk_customers": high_risk_customers
            },
            "revenue_metrics": {
                "total_revenue": total_revenue,
                "avg_customer_value": total_revenue / total_customers if total_customers > 0 else 0
            },
            "marketing_status": {
                "active_campaigns": active_campaigns,
                "campaign_performance": campaign_performance
            },
            "daily_activity": recent_activity,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "context_type": "comprehensive"
        }
    except Exception as e:
        print(f"Error getting comprehensive context: {e}")
        return {
            "error": "Could not retrieve comprehensive data",
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }

async def get_priority_context() -> Dict[str, Any]:
    """Get high-priority items needing immediate attention"""
    try:
        # Critical customers
        critical_customers = await db.customers.find(
            {"churn_risk": "Critical"},
            {"customer_id": 1, "name": 1, "total_spent": 1, "last_activity": 1}
        ).limit(10).to_list(length=10)
        
        # Failed campaigns or low performing
        underperforming_campaigns = await db.campaigns.find(
            {"status": {"$in": ["failed", "low_performance"]}},
            {"name": 1, "status": 1, "target_segment": 1}
        ).limit(5).to_list(length=5)
        
        # Expansion opportunities (high-value, active customers)
        expansion_opportunities = await db.customers.find(
            {"$and": [
                {"total_spent": {"$gt": 1000}},
                {"churn_risk": {"$in": ["Low", "Medium"]}},
                {"engagement_score": {"$gt": 70}}
            ]},
            {"customer_id": 1, "name": 1, "total_spent": 1, "engagement_score": 1}
        ).limit(5).to_list(length=5)
        
        return {
            "urgent_attention": {
                "critical_customers": critical_customers,
                "underperforming_campaigns": underperforming_campaigns
            },
            "opportunities": {
                "expansion_candidates": expansion_opportunities
            },
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "context_type": "priority_focus"
        }
    except Exception as e:
        print(f"Error getting priority context: {e}")
        return {
            "error": "Could not retrieve priority data",
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }

async def build_productivity_context(context_type: str) -> Dict[str, Any]:
    """Build comprehensive context for productivity analysis"""
    if context_type == "comprehensive":
        return await get_comprehensive_context()
    elif context_type == "priority_focus":
        return await get_priority_context()
    elif context_type == "customer_data":
        # Reuse from ai_business_insights
        from modules.ai_business_insights import get_customer_context
        return {"customer_data": await get_customer_context()}
    elif context_type == "website_data":
        # Basic website data - can be enhanced later
        return {
            "website_data": {"placeholder": "Website analytics integration"},
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }
    else:
        return await get_comprehensive_context()

async def generate_productivity_analysis(prompt: str, context_data: Dict[str, Any], workflow_focus: str) -> Dict[str, Any]:
    """Generate AI-powered productivity analysis"""
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="AI service not configured")
    
    try:
        session_id = f"productivity_{uuid.uuid4().hex[:8]}"
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=f"""You are an expert business productivity consultant and data analyst specializing in workflow optimization and daily business intelligence.

Your role is to help business owners and managers maximize their productivity by providing:
1. Actionable daily/weekly/monthly recommendations
2. Priority-focused task lists based on data
3. Time-saving automation suggestions
4. Early warning alerts for business issues
5. Opportunity identification for growth

Focus Area: {workflow_focus}

When analyzing data, provide:
- Immediate action items (what to do today)
- Priority levels (Critical/High/Medium/Low)
- Estimated time savings from recommendations
- Specific next steps with clear timelines
- Resource requirements for implementation

Structure your response with:
- Executive Summary (2-3 sentences)
- Immediate Actions Required (top 3-5 items)
- Opportunities to Pursue (growth/efficiency)
- Early Warning Alerts (potential issues)
- Automation Recommendations
- Estimated Time Impact

Keep responses practical, actionable, and focused on maximizing business productivity."""
        ).with_model("openai", "gpt-4o-mini")
        
        # Build context-aware prompt
        context_summary = f"""
Business Productivity Analysis Request:
Workflow Focus: {workflow_focus}

Current Business Context:
{json.dumps(context_data, indent=2, default=str)}

Productivity Question: {prompt}

Please provide a comprehensive productivity analysis with specific action items, priorities, and time-saving recommendations based on this data.
"""
        
        user_message = UserMessage(text=context_summary)
        analysis_response = await chat.send_message(user_message)
        
        # Extract action items and priority level
        action_items = []
        priority_level = "Medium"
        
        lines = analysis_response.split('\n')
        in_actions = False
        
        for line in lines:
            line = line.strip()
            if 'action' in line.lower() or 'immediate' in line.lower():
                in_actions = True
            elif in_actions and line.startswith(('•', '-', '*', '1.', '2.', '3.')):
                clean_action = line.lstrip('•-*123456789. ').strip()
                if clean_action and len(clean_action) > 10:
                    action_items.append(clean_action)
            
            # Detect priority level
            if 'critical' in line.lower() or 'urgent' in line.lower():
                priority_level = "Critical"
            elif 'high priority' in line.lower() or 'important' in line.lower():
                priority_level = "High"
        
        # Extract recommendations (reuse logic from ai_business_insights)
        recommendations = []
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['should', 'recommend', 'consider', 'implement', 'focus on']):
                if len(line) > 20 and len(line) < 200:
                    recommendations.append(line)
        
        return {
            "analysis": analysis_response,
            "recommendations": recommendations[:5],
            "action_items": action_items[:7],
            "priority_level": priority_level,
            "estimated_time_savings": "2-5 hours/week",
            "context_used": context_data,
            "session_id": session_id
        }
        
    except Exception as e:
        print(f"Productivity analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Productivity analysis failed: {str(e)}")

# API Endpoints
@router.get("/prompts")
async def get_productivity_prompts():
    """Get categorized productivity prompt templates"""
    return {
        "status": "success",
        "prompt_categories": PRODUCTIVITY_PROMPTS,
        "total_prompts": sum(len(prompts) for prompts in PRODUCTIVITY_PROMPTS.values()),
        "focus_areas": list(PRODUCTIVITY_PROMPTS.keys())
    }

@router.post("/analyze", response_model=ProductivityInsightResponse)
async def analyze_productivity(request: ProductivityInsightRequest):
    """Generate AI-powered productivity insights"""
    start_time = datetime.now()
    
    try:
        # Build analysis context
        context_data = await build_productivity_context(request.context_type)
        
        # Generate AI analysis
        ai_result = await generate_productivity_analysis(
            request.prompt, 
            context_data, 
            request.workflow_focus
        )
        
        # Create insight record
        insight_id = f"productivity_{uuid.uuid4().hex[:12]}"
        processing_time = (datetime.now() - start_time).total_seconds()
        
        insight = ProductivityInsightResponse(
            insight_id=insight_id,
            prompt=request.prompt,
            analysis=ai_result["analysis"],
            data_summary=context_data,
            recommendations=ai_result["recommendations"],
            action_items=ai_result["action_items"],
            priority_level=ai_result["priority_level"],
            estimated_time_savings=ai_result["estimated_time_savings"],
            created_at=datetime.now(timezone.utc),
            processing_time=processing_time
        )
        
        return insight
        
    except Exception as e:
        print(f"Productivity analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Productivity analysis failed: {str(e)}")

@router.get("/daily-priorities")
async def get_daily_priorities():
    """Get daily priority items that need immediate attention"""
    try:
        priority_context = await get_priority_context()
        
        return {
            "status": "success",
            "daily_priorities": priority_context,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        print(f"Daily priorities error: {e}")
        return {
            "status": "error",
            "message": "Could not retrieve daily priorities",
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

@router.get("/workflow-suggestions")
async def get_workflow_suggestions():
    """Get personalized workflow optimization suggestions"""
    try:
        # This would be enhanced with user behavior tracking
        suggestions = [
            {
                "category": "Morning Routine",
                "suggestion": "Start with 'What needs my immediate attention today?' prompt",
                "time_savings": "15 minutes",
                "priority": "High"
            },
            {
                "category": "Weekly Planning",
                "suggestion": "Use Monday planning prompts to focus on high-impact activities",
                "time_savings": "2 hours/week",
                "priority": "Medium"
            },
            {
                "category": "Data Analysis",
                "suggestion": "Automate routine reporting with custom dashboards",
                "time_savings": "5 hours/week",
                "priority": "High"
            }
        ]
        
        return {
            "status": "success",
            "workflow_suggestions": suggestions,
            "total_potential_savings": "7+ hours/week"
        }
        
    except Exception as e:
        print(f"Workflow suggestions error: {e}")
        return {
            "status": "error",
            "message": "Could not generate workflow suggestions"
        }

# Export router
__all__ = ["router"]