"""
AI Business Insights Module
Advanced AI-powered business analysis system for Customer Mind IQ
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
class BusinessInsightRequest(BaseModel):
    prompt: str = Field(..., description="Business analysis prompt")
    context_type: str = Field(default="customer_data", description="Type of data context to include")
    analysis_focus: str = Field(default="general", description="Focus area for analysis")

class BusinessInsightResponse(BaseModel):
    insight_id: str
    prompt: str
    analysis: str
    data_summary: Dict[str, Any]
    recommendations: List[str]
    created_at: datetime
    processing_time: float

class SavedInsight(BaseModel):
    insight_id: str
    user_id: str
    prompt: str
    analysis: str
    data_summary: Dict[str, Any]
    recommendations: List[str]
    created_at: datetime
    tags: List[str] = []

# Business Analysis Prompt Templates
BUSINESS_PROMPTS = {
    "customer_analysis": [
        "Analyze our customer churn patterns and suggest specific retention strategies based on our data",
        "What are the key characteristics of our most valuable customers and how can we attract more like them?",
        "Identify customer segments with the highest growth potential and recommend targeted strategies",
        "Analyze customer lifetime value trends and provide actionable insights for improvement",
        "What customer behavior patterns indicate expansion opportunities?"
    ],
    "revenue_optimization": [
        "Analyze our revenue streams and identify the top 3 optimization opportunities",
        "What pricing strategies would maximize our revenue based on customer behavior data?",
        "Identify seasonal revenue patterns and recommend strategies to capitalize on them",
        "Analyze our most profitable customer segments and suggest expansion strategies",
        "What are our biggest revenue leakage points and how can we address them?"
    ],
    "marketing_performance": [
        "Analyze our marketing campaign performance and identify the highest ROI channels",
        "What customer acquisition strategies are most effective based on our data?",
        "Identify content themes and messaging that drive the highest engagement",
        "Analyze our conversion funnel and recommend optimization strategies",
        "What marketing automation opportunities exist based on customer behavior?"
    ],
    "operational_insights": [
        "Analyze our support ticket data to identify common issues and improvement opportunities",
        "What operational bottlenecks are impacting customer satisfaction?",
        "Identify patterns in customer onboarding that affect long-term success",
        "Analyze usage patterns to recommend feature development priorities",
        "What process improvements would have the biggest impact on customer experience?"
    ],
    "competitive_analysis": [
        "Based on our performance data, where do we have competitive advantages?",
        "What market positioning would best leverage our customer success patterns?",
        "Analyze our pricing compared to value delivered and recommend adjustments",
        "Identify white space opportunities based on customer feedback and behavior",
        "What differentiation strategies align with our strongest customer segments?"
    ],
    "growth_strategies": [
        "Identify the top 5 growth levers based on our current business data",
        "What expansion strategies would maximize customer lifetime value?",
        "Analyze cross-sell and upsell opportunities within our customer base",
        "What market segments should we prioritize for expansion?",
        "Identify referral program opportunities based on customer satisfaction data"
    ]
}

# Data Context Builders
async def get_customer_context() -> Dict[str, Any]:
    """Get customer data context for AI analysis"""
    try:
        # Get customer overview
        total_customers = await db.customers.count_documents({})
        
        # Get customer segments
        pipeline = [
            {"$group": {"_id": "$segment", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        segments = await db.customers.aggregate(pipeline).to_list(length=10)
        
        # Get churn risk data
        churn_pipeline = [
            {"$group": {"_id": "$churn_risk", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        churn_data = await db.customers.aggregate(churn_pipeline).to_list(length=5)
        
        # Get recent customer activity
        recent_customers = await db.customers.find({}, {"customer_id": 1, "name": 1, "segment": 1, "total_spent": 1, "churn_risk": 1}).sort("created_at", -1).limit(10).to_list(length=10)
        
        return {
            "total_customers": total_customers,
            "customer_segments": segments,
            "churn_risk_distribution": churn_data,
            "recent_customers": recent_customers[:5],  # Limit for context
            "data_timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        print(f"Error getting customer context: {e}")
        return {"error": "Could not retrieve customer data", "total_customers": 0}

async def get_revenue_context() -> Dict[str, Any]:
    """Get revenue data context for AI analysis"""
    try:
        # Get total revenue from customers
        pipeline = [
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total_spent"}}},
        ]
        revenue_result = await db.customers.aggregate(pipeline).to_list(length=1)
        total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
        
        # Get revenue by segment
        segment_pipeline = [
            {"$group": {"_id": "$segment", "segment_revenue": {"$sum": "$total_spent"}, "customer_count": {"$sum": 1}}},
            {"$sort": {"segment_revenue": -1}}
        ]
        segment_revenue = await db.customers.aggregate(segment_pipeline).to_list(length=10)
        
        # Get high-value customers
        high_value = await db.customers.find({}).sort("total_spent", -1).limit(10).to_list(length=10)
        
        return {
            "total_revenue": total_revenue,
            "revenue_by_segment": segment_revenue,
            "top_customers_by_value": high_value[:5],  # Limit for context
            "data_timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        print(f"Error getting revenue context: {e}")
        return {"error": "Could not retrieve revenue data", "total_revenue": 0}

async def get_campaign_context() -> Dict[str, Any]:
    """Get marketing campaign context for AI analysis"""
    try:
        # Get campaign stats
        total_campaigns = await db.campaigns.count_documents({})
        
        # Get recent campaigns
        recent_campaigns = await db.campaigns.find({}, {"name": 1, "status": 1, "target_segment": 1, "created_at": 1}).sort("created_at", -1).limit(10).to_list(length=10)
        
        # Get campaign status distribution
        status_pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        status_data = await db.campaigns.aggregate(status_pipeline).to_list(length=5)
        
        return {
            "total_campaigns": total_campaigns,
            "recent_campaigns": recent_campaigns[:5],  # Limit for context
            "campaign_status_distribution": status_data,
            "data_timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        print(f"Error getting campaign context: {e}")
        return {"error": "Could not retrieve campaign data", "total_campaigns": 0}

async def build_analysis_context(context_type: str) -> Dict[str, Any]:
    """Build comprehensive context for AI analysis"""
    context = {
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        "context_type": context_type
    }
    
    if context_type == "customer_data" or context_type == "comprehensive":
        context["customer_data"] = await get_customer_context()
    
    if context_type == "revenue_data" or context_type == "comprehensive":
        context["revenue_data"] = await get_revenue_context()
    
    if context_type == "marketing_data" or context_type == "comprehensive":
        context["campaign_data"] = await get_campaign_context()
    
    return context

async def generate_ai_analysis(prompt: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate AI-powered business analysis"""
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="AI service not configured")
    
    try:
        # Initialize LLM chat
        session_id = f"business_insights_{uuid.uuid4().hex[:8]}"
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message="""You are a senior business analyst and data scientist specializing in customer intelligence and revenue optimization. 

Your role is to analyze business data and provide actionable insights that drive growth, improve customer satisfaction, and optimize revenue.

When analyzing data, focus on:
1. Actionable recommendations with specific next steps
2. Data-driven insights with clear evidence
3. Strategic implications and business impact
4. Risk identification and mitigation strategies
5. Growth opportunities and optimization potential

Always structure your response with:
- Executive Summary
- Key Findings
- Specific Recommendations
- Implementation Priorities
- Expected Impact/ROI

Keep your analysis professional, concise, and focused on business value."""
        ).with_model("openai", "gpt-4o-mini")
        
        # Build context-aware prompt
        context_summary = f"""
Business Context Data:
{json.dumps(context_data, indent=2, default=str)}

Analysis Request: {prompt}

Please provide a comprehensive business analysis based on this data, focusing on actionable insights and specific recommendations.
"""
        
        # Send message and get response
        user_message = UserMessage(text=context_summary)
        analysis_response = await chat.send_message(user_message)
        
        # Extract recommendations (simple parsing)
        recommendations = []
        lines = analysis_response.split('\n')
        in_recommendations = False
        
        for line in lines:
            line = line.strip()
            if 'recommendation' in line.lower() or 'action' in line.lower():
                in_recommendations = True
            elif in_recommendations and line.startswith(('•', '-', '*', '1.', '2.', '3.')):
                clean_rec = line.lstrip('•-*123456789. ').strip()
                if clean_rec and len(clean_rec) > 10:  # Filter out short/empty items
                    recommendations.append(clean_rec)
        
        # If no structured recommendations found, extract key actionable sentences
        if not recommendations:
            sentences = analysis_response.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in ['should', 'recommend', 'implement', 'focus on', 'consider', 'improve']):
                    if len(sentence) > 20 and len(sentence) < 200:
                        recommendations.append(sentence + '.')
        
        return {
            "analysis": analysis_response,
            "recommendations": recommendations[:5],  # Limit to top 5
            "context_used": context_data,
            "session_id": session_id
        }
        
    except Exception as e:
        print(f"AI analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

# API Endpoints

@router.get("/prompts")
async def get_business_prompts():
    """Get categorized business analysis prompt templates"""
    return {
        "status": "success",
        "prompt_categories": BUSINESS_PROMPTS,
        "total_prompts": sum(len(prompts) for prompts in BUSINESS_PROMPTS.values())
    }

@router.post("/analyze", response_model=BusinessInsightResponse)
async def analyze_business_data(request: BusinessInsightRequest):
    """Generate AI-powered business insights"""
    start_time = datetime.now()
    
    try:
        # Build analysis context
        context_data = await build_analysis_context(request.context_type)
        
        # Generate AI analysis
        ai_result = await generate_ai_analysis(request.prompt, context_data)
        
        # Create insight record
        insight_id = f"insight_{uuid.uuid4().hex[:12]}"
        processing_time = (datetime.now() - start_time).total_seconds()
        
        insight = BusinessInsightResponse(
            insight_id=insight_id,
            prompt=request.prompt,
            analysis=ai_result["analysis"],
            data_summary=context_data,
            recommendations=ai_result["recommendations"],
            created_at=datetime.now(timezone.utc),
            processing_time=processing_time
        )
        
        return insight
        
    except Exception as e:
        print(f"Business insight analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/save-insight")
async def save_business_insight(insight_data: dict):
    """Save business insight for future reference"""
    try:
        # Add metadata
        insight_data["saved_at"] = datetime.now(timezone.utc)
        insight_data["insight_id"] = insight_data.get("insight_id", f"saved_{uuid.uuid4().hex[:12]}")
        
        # Save to database
        await db.business_insights.insert_one(insight_data)
        
        return {
            "status": "success",
            "message": "Business insight saved successfully",
            "insight_id": insight_data["insight_id"]
        }
        
    except Exception as e:
        print(f"Save insight error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save insight")

@router.get("/history")
async def get_insight_history(limit: int = 10):
    """Get recent business insights history"""
    try:
        insights = await db.business_insights.find({}, {
            "insight_id": 1, 
            "prompt": 1, 
            "recommendations": 1, 
            "saved_at": 1
        }).sort("saved_at", -1).limit(limit).to_list(length=limit)
        
        return {
            "status": "success",
            "insights": insights,
            "total": len(insights)
        }
        
    except Exception as e:
        print(f"Get history error: {e}")
        return {
            "status": "success",
            "insights": [],
            "total": 0
        }

@router.get("/data-summary")
async def get_data_summary():
    """Get current business data summary for context"""
    try:
        summary = await build_analysis_context("comprehensive")
        
        return {
            "status": "success",
            "data_summary": summary,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        print(f"Data summary error: {e}")
        return {
            "status": "success", 
            "data_summary": {"error": "Could not retrieve data summary"},
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

# Export router
__all__ = ["router"]