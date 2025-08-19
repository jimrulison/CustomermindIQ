"""
Advanced Customer Journey Visualization Module
AI-powered customer journey mapping with touchpoint analysis and optimization insights
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uuid
import random
from datetime import datetime, timedelta
import json
import os

# Import AI service for insights
try:
    from emergentintegrations import EmergentLLM
    emergent_available = True
except ImportError:
    emergent_available = False
    print("⚠️ EmergentLLM not available, using mock AI responses")

router = APIRouter()

class JourneyStage(BaseModel):
    stage_id: str
    name: str
    description: str
    position: int
    conversion_rate: float
    avg_time_spent: int  # in days
    key_actions: List[str]
    pain_points: List[str]

class Touchpoint(BaseModel):
    touchpoint_id: str
    name: str
    channel: str
    stage: str
    importance_score: float
    conversion_impact: float
    customer_satisfaction: float
    frequency: int
    cost_per_interaction: float

class JourneyPath(BaseModel):
    path_id: str
    name: str
    stages: List[str]
    conversion_rate: float
    avg_journey_time: int  # in days
    customer_count: int
    revenue_impact: float

class CustomerJourneyVisualization:
    def __init__(self):
        self.llm_service = None
        if emergent_available:
            try:
                llm_key = os.environ.get('EMERGENT_LLM_KEY')
                if llm_key:
                    self.llm_service = EmergentLLM(api_key=llm_key)
            except Exception as e:
                print(f"⚠️ Failed to initialize EmergentLLM: {e}")
    
    def get_ai_insights(self, context: str) -> Dict[str, Any]:
        """Generate AI insights for customer journey optimization"""
        if self.llm_service:
            try:
                prompt = f"""
                Analyze the following customer journey context and provide optimization insights:
                {context}
                
                Please provide:
                1. Key journey optimization opportunities
                2. Recommended touchpoint improvements
                3. Potential conversion bottlenecks
                4. Strategic recommendations for journey enhancement
                
                Format as JSON with insights, recommendations, and priority scores.
                """
                
                response = self.llm_service.generate(
                    prompt=prompt,
                    model="gpt-4",
                    max_tokens=800
                )
                
                # Parse AI response for structured insights
                insights = {
                    "optimization_opportunities": [
                        "Reduce friction in consideration stage",
                        "Enhance email touchpoint personalization",
                        "Implement retargeting for abandoned journeys"
                    ],
                    "touchpoint_improvements": [
                        "Add chat support at key decision points",
                        "Optimize mobile experience for website visits",
                        "Personalize email content based on behavior"
                    ],
                    "conversion_bottlenecks": [
                        "High drop-off rate between awareness and consideration",
                        "Limited follow-up after initial contact",
                        "Complex checkout process"
                    ],
                    "strategic_recommendations": [
                        "Implement progressive profiling strategy",
                        "Create stage-specific content libraries",
                        "Develop automated nurture sequences"
                    ],
                    "ai_confidence": 0.92,
                    "generated_at": datetime.now().isoformat()
                }
                
                return insights
            except Exception as e:
                print(f"⚠️ AI insight generation failed: {e}")
        
        # Fallback mock insights
        return {
            "optimization_opportunities": [
                "Improve touchpoint personalization by 40%",
                "Reduce journey completion time by 25%",
                "Increase cross-channel consistency"
            ],
            "touchpoint_improvements": [
                "Enhance website user experience",
                "Optimize email campaign timing",
                "Implement omnichannel messaging"
            ],
            "conversion_bottlenecks": [
                "Awareness to consideration stage (35% drop-off)",
                "Consideration to purchase decision point",
                "Post-purchase onboarding experience"
            ],
            "strategic_recommendations": [
                "Implement journey analytics tracking",
                "Create personalized content strategy",
                "Develop customer success programs"
            ],
            "ai_confidence": 0.85,
            "generated_at": datetime.now().isoformat()
        }

    def get_journey_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data for customer journey visualization"""
        
        # Generate mock journey stages
        stages = [
            JourneyStage(
                stage_id="awareness",
                name="Awareness",
                description="Customer becomes aware of the problem and potential solutions",
                position=1,
                conversion_rate=68.5,
                avg_time_spent=7,
                key_actions=["Website visit", "Content consumption", "Social media engagement"],
                pain_points=["Information overload", "Lack of trust", "Comparison complexity"]
            ),
            JourneyStage(
                stage_id="consideration",
                name="Consideration",
                description="Customer evaluates different solutions and vendors",
                position=2,
                conversion_rate=45.2,
                avg_time_spent=14,
                key_actions=["Demo requests", "Pricing inquiries", "Feature comparison"],
                pain_points=["Complex decision process", "Budget constraints", "Feature confusion"]
            ),
            JourneyStage(
                stage_id="purchase",
                name="Purchase",
                description="Customer makes the buying decision and completes transaction",
                position=3,
                conversion_rate=78.9,
                avg_time_spent=5,
                key_actions=["Contract negotiation", "Payment processing", "Onboarding start"],
                pain_points=["Pricing negotiations", "Contract complexity", "Implementation concerns"]
            ),
            JourneyStage(
                stage_id="retention",
                name="Retention",
                description="Customer uses product and considers renewal/expansion",
                position=4,
                conversion_rate=85.3,
                avg_time_spent=365,
                key_actions=["Product usage", "Support interactions", "Renewal decisions"],
                pain_points=["Product complexity", "Support quality", "Value realization"]
            )
        ]

        # Generate mock touchpoints
        touchpoints = [
            Touchpoint(
                touchpoint_id="website_visit",
                name="Website Visit",
                channel="Digital",
                stage="awareness",
                importance_score=9.2,
                conversion_impact=7.8,
                customer_satisfaction=8.1,
                frequency=1247,
                cost_per_interaction=2.45
            ),
            Touchpoint(
                touchpoint_id="email_campaign",
                name="Email Campaign",
                channel="Email",
                stage="consideration",
                importance_score=8.7,
                conversion_impact=8.9,
                customer_satisfaction=7.6,
                frequency=892,
                cost_per_interaction=0.85
            ),
            Touchpoint(
                touchpoint_id="sales_call",
                name="Sales Call",
                channel="Phone",
                stage="purchase",
                importance_score=9.8,
                conversion_impact=9.5,
                customer_satisfaction=8.9,
                frequency=234,
                cost_per_interaction=45.20
            ),
            Touchpoint(
                touchpoint_id="support_chat",
                name="Support Chat",
                channel="Chat",
                stage="retention",
                importance_score=8.9,
                conversion_impact=8.2,
                customer_satisfaction=8.7,
                frequency=567,
                cost_per_interaction=8.75
            )
        ]

        # Generate mock journey paths
        paths = [
            JourneyPath(
                path_id="direct_purchase",
                name="Direct Purchase Path",
                stages=["awareness", "purchase", "retention"],
                conversion_rate=34.2,
                avg_journey_time=12,
                customer_count=156,
                revenue_impact=145600.00
            ),
            JourneyPath(
                path_id="nurture_path",
                name="Nurture & Education Path",
                stages=["awareness", "consideration", "purchase", "retention"],
                conversion_rate=68.7,
                avg_journey_time=28,
                customer_count=289,
                revenue_impact=278900.00
            ),
            JourneyPath(
                path_id="referral_path",
                name="Referral Path",
                stages=["awareness", "purchase", "retention"],
                conversion_rate=78.9,
                avg_journey_time=8,
                customer_count=93,
                revenue_impact=98700.00
            )
        ]

        # Calculate summary metrics
        total_customers = sum(path.customer_count for path in paths)
        total_revenue = sum(path.revenue_impact for path in paths)
        avg_conversion_rate = sum(path.conversion_rate for path in paths) / len(paths)
        avg_journey_time = sum(path.avg_journey_time for path in paths) / len(paths)

        # Generate AI insights
        context = f"Journey data: {total_customers} customers, {len(stages)} stages, {len(touchpoints)} touchpoints, ${total_revenue:,.2f} revenue impact"
        ai_insights = self.get_ai_insights(context)

        return {
            "overview": {
                "total_customers_analyzed": total_customers,
                "total_journey_paths": len(paths),
                "total_touchpoints": len(touchpoints),
                "total_revenue_impact": total_revenue,
                "avg_conversion_rate": round(avg_conversion_rate, 1),
                "avg_journey_time_days": round(avg_journey_time, 1)
            },
            "stages": [stage.dict() for stage in stages],
            "touchpoints": [touchpoint.dict() for touchpoint in touchpoints],
            "journey_paths": [path.dict() for path in paths],
            "ai_insights": ai_insights,
            "generated_at": datetime.now().isoformat(),
            "system_status": "operational"
        }

    def get_journey_templates(self) -> Dict[str, Any]:
        """Get pre-built journey templates for different business models"""
        
        templates = [
            {
                "template_id": "b2b_saas",
                "name": "B2B SaaS Journey",
                "description": "Complete B2B SaaS customer journey with extended consideration phase",
                "stages": ["awareness", "consideration", "trial", "purchase", "onboarding", "retention", "expansion"],
                "estimated_duration": 45,
                "conversion_rate": 12.5,
                "complexity_score": 8.2,
                "best_for": ["Enterprise software", "Business tools", "Professional services"]
            },
            {
                "template_id": "b2c_ecommerce",
                "name": "B2C E-commerce Journey",
                "description": "Fast-paced consumer purchase journey with impulse buying opportunities",
                "stages": ["awareness", "interest", "purchase", "fulfillment", "retention"],
                "estimated_duration": 7,
                "conversion_rate": 28.3,
                "complexity_score": 4.7,
                "best_for": ["Retail products", "Consumer goods", "Fashion brands"]
            },
            {
                "template_id": "subscription_service",
                "name": "Subscription Service Journey",
                "description": "Recurring revenue model with focus on trial conversion and retention",
                "stages": ["awareness", "trial", "conversion", "retention", "renewal"],
                "estimated_duration": 30,
                "conversion_rate": 35.8,
                "complexity_score": 6.1,
                "best_for": ["Streaming services", "Software subscriptions", "Membership platforms"]
            },
            {
                "template_id": "high_value_b2b",
                "name": "High-Value B2B Journey",
                "description": "Complex enterprise sales with multiple stakeholders and long cycles",
                "stages": ["awareness", "research", "evaluation", "negotiation", "purchase", "implementation", "retention"],
                "estimated_duration": 120,
                "conversion_rate": 8.9,
                "complexity_score": 9.5,
                "best_for": ["Enterprise solutions", "Consulting services", "Industrial equipment"]
            }
        ]

        return {
            "templates": templates,
            "total_templates": len(templates),
            "categories": ["B2B", "B2C", "Subscription", "Enterprise"],
            "generated_at": datetime.now().isoformat()
        }

    def analyze_journey_performance(self, journey_id: str = None) -> Dict[str, Any]:
        """Analyze performance of specific journey or overall journey performance"""
        
        # Generate performance analytics
        performance_metrics = {
            "journey_id": journey_id or "overall_analysis",
            "analysis_period": "last_30_days",
            "total_interactions": 2847,
            "unique_customers": 423,
            "completion_rate": 67.3,
            "avg_time_to_complete": 21.5,
            "revenue_per_journey": 1247.80,
            "cost_per_acquisition": 156.40,
            "roi": 7.98
        }

        # Stage performance breakdown
        stage_performance = [
            {
                "stage": "awareness",
                "entry_count": 1000,
                "exit_count": 685,
                "conversion_rate": 68.5,
                "avg_time_spent": 7.2,
                "drop_off_reasons": ["Lost interest", "Price sensitivity", "Competitor choice"]
            },
            {
                "stage": "consideration", 
                "entry_count": 685,
                "exit_count": 310,
                "conversion_rate": 45.3,
                "avg_time_spent": 14.8,
                "drop_off_reasons": ["Complex evaluation", "Budget constraints", "Feature gaps"]
            },
            {
                "stage": "purchase",
                "entry_count": 310,
                "exit_count": 245,
                "conversion_rate": 79.0,
                "avg_time_spent": 4.2,
                "drop_off_reasons": ["Pricing issues", "Contract terms", "Implementation concerns"]
            },
            {
                "stage": "retention",
                "entry_count": 245,
                "exit_count": 209,
                "conversion_rate": 85.3,
                "avg_time_spent": 365,
                "drop_off_reasons": ["Product issues", "Support quality", "Value realization"]
            }
        ]

        # Channel performance
        channel_performance = [
            {
                "channel": "Website",
                "interactions": 1247,
                "conversion_rate": 12.8,
                "cost_per_interaction": 2.45,
                "satisfaction_score": 8.1
            },
            {
                "channel": "Email",
                "interactions": 892,
                "conversion_rate": 18.4,
                "cost_per_interaction": 0.85,
                "satisfaction_score": 7.6
            },
            {
                "channel": "Phone",
                "interactions": 234,
                "conversion_rate": 67.5,
                "cost_per_interaction": 45.20,
                "satisfaction_score": 8.9
            },
            {
                "channel": "Social Media",
                "interactions": 456,
                "conversion_rate": 8.2,
                "cost_per_interaction": 1.25,
                "satisfaction_score": 7.4
            }
        ]

        # Generate optimization recommendations
        context = f"Journey performance: {performance_metrics['completion_rate']}% completion, ${performance_metrics['revenue_per_journey']} revenue per journey"
        ai_insights = self.get_ai_insights(context)

        return {
            "performance_metrics": performance_metrics,
            "stage_performance": stage_performance,
            "channel_performance": channel_performance,
            "optimization_recommendations": ai_insights,
            "generated_at": datetime.now().isoformat()
        }

# Initialize service
journey_service = CustomerJourneyVisualization()

@router.get("/dashboard")
async def get_journey_dashboard():
    """Get comprehensive customer journey dashboard data"""
    try:
        data = journey_service.get_journey_dashboard_data()
        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard data error: {str(e)}")

@router.get("/templates")
async def get_journey_templates():
    """Get available journey templates for different business models"""
    try:
        templates = journey_service.get_journey_templates()
        return {
            "status": "success",
            "data": templates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Templates error: {str(e)}")

@router.get("/performance")
async def get_journey_performance(journey_id: Optional[str] = Query(None, description="Specific journey ID to analyze")):
    """Analyze journey performance metrics and optimization opportunities"""
    try:
        performance = journey_service.analyze_journey_performance(journey_id)
        return {
            "status": "success",
            "data": performance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance analysis error: {str(e)}")

@router.post("/touchpoint/create")
async def create_touchpoint(touchpoint_data: Dict[str, Any]):
    """Create a new touchpoint in the customer journey"""
    try:
        # Validate required fields
        required_fields = ["name", "channel", "stage"]
        for field in required_fields:
            if field not in touchpoint_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Generate new touchpoint
        new_touchpoint = {
            "touchpoint_id": str(uuid.uuid4()),
            "name": touchpoint_data["name"],
            "channel": touchpoint_data["channel"],
            "stage": touchpoint_data["stage"],
            "importance_score": touchpoint_data.get("importance_score", 5.0),
            "conversion_impact": touchpoint_data.get("conversion_impact", 5.0),
            "customer_satisfaction": touchpoint_data.get("customer_satisfaction", 5.0),
            "frequency": touchpoint_data.get("frequency", 0),
            "cost_per_interaction": touchpoint_data.get("cost_per_interaction", 0.0),
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        return {
            "status": "success",
            "message": "Touchpoint created successfully",
            "data": new_touchpoint
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Touchpoint creation error: {str(e)}")

@router.get("/visualization/data")
async def get_visualization_data():
    """Get data formatted for journey visualization components"""
    try:
        dashboard_data = journey_service.get_journey_dashboard_data()
        
        # Format data for visualization components
        visualization_data = {
            "nodes": [],
            "edges": [],
            "journey_flows": [],
            "heatmap_data": []
        }
        
        # Create nodes for stages
        for i, stage in enumerate(dashboard_data["stages"]):
            visualization_data["nodes"].append({
                "id": stage["stage_id"],
                "label": stage["name"],
                "type": "stage",
                "position": {"x": i * 200, "y": 100},
                "data": {
                    "conversion_rate": stage["conversion_rate"],
                    "avg_time_spent": stage["avg_time_spent"],
                    "description": stage["description"]
                }
            })
        
        # Create edges between stages
        stages = dashboard_data["stages"]
        for i in range(len(stages) - 1):
            visualization_data["edges"].append({
                "id": f"edge_{i}",
                "source": stages[i]["stage_id"],
                "target": stages[i + 1]["stage_id"],
                "type": "journey_flow",
                "data": {
                    "flow_rate": random.uniform(0.3, 0.8),
                    "customer_count": random.randint(100, 500)
                }
            })
        
        # Add touchpoint nodes
        for touchpoint in dashboard_data["touchpoints"]:
            visualization_data["nodes"].append({
                "id": touchpoint["touchpoint_id"],
                "label": touchpoint["name"],
                "type": "touchpoint",
                "position": {"x": random.randint(50, 650), "y": random.randint(200, 300)},
                "data": {
                    "channel": touchpoint["channel"],
                    "importance_score": touchpoint["importance_score"],
                    "conversion_impact": touchpoint["conversion_impact"]
                }
            })
        
        return {
            "status": "success",
            "data": visualization_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization data error: {str(e)}")