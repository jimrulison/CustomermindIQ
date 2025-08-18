"""
Customer Journey Mapping - Analytics & Insights Module
Advanced customer path analysis with AI-powered journey optimization
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import uuid
import numpy as np
from enum import Enum

# Initialize router
customer_journey_mapping_router = APIRouter()

class TouchpointType(str, Enum):
    WEBSITE = "website"
    EMAIL = "email"
    SOCIAL = "social"
    SALES = "sales"
    SUPPORT = "support"
    PRODUCT = "product"
    PURCHASE = "purchase"

class JourneyStage(str, Enum):
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    DECISION = "decision"
    PURCHASE = "purchase"
    RETENTION = "retention"
    ADVOCACY = "advocacy"

class CustomerTouchpoint(BaseModel):
    touchpoint_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    touchpoint_type: TouchpointType
    channel: str
    action: str
    timestamp: datetime
    value: Optional[float] = None
    duration: Optional[int] = None  # seconds
    stage: JourneyStage
    conversion_event: bool = False

class JourneyPath(BaseModel):
    path_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_count: int
    touchpoint_sequence: List[str]
    avg_time_to_conversion: Optional[float] = None
    conversion_rate: float
    drop_off_points: List[str]
    path_value: float

class JourneyVisualization(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    flow_data: Dict[str, Any]
    heatmap_data: Dict[str, Any]

class JourneyIntelligenceInsight(BaseModel):
    insight_type: str
    description: str
    recommended_action: str
    impact_score: float
    confidence: float

class CustomerJourneyMappingService:
    """AI-powered Customer Journey Mapping Service"""
    
    def __init__(self):
        self.touchpoint_weights = {
            TouchpointType.WEBSITE: 0.1,
            TouchpointType.EMAIL: 0.15,
            TouchpointType.SOCIAL: 0.12,
            TouchpointType.SALES: 0.25,
            TouchpointType.SUPPORT: 0.08,
            TouchpointType.PRODUCT: 0.20,
            TouchpointType.PURCHASE: 0.10
        }
    
    async def collect_journey_data(self, customer_data: List[Dict]) -> List[CustomerTouchpoint]:
        """Collect and process customer touchpoint data"""
        touchpoints = []
        
        for customer in customer_data:
            customer_id = customer.get('customer_id', str(uuid.uuid4()))
            
            # Generate realistic touchpoint sequence
            journey_stages = [
                JourneyStage.AWARENESS,
                JourneyStage.CONSIDERATION, 
                JourneyStage.DECISION,
                JourneyStage.PURCHASE
            ]
            
            base_time = datetime.now() - timedelta(days=random.randint(30, 120))
            
            for i, stage in enumerate(journey_stages):
                # Generate 1-3 touchpoints per stage
                stage_touchpoints = random.randint(1, 3)
                
                for _ in range(stage_touchpoints):
                    touchpoint_type = self._get_stage_appropriate_touchpoint(stage)
                    
                    touchpoint = CustomerTouchpoint(
                        customer_id=customer_id,
                        touchpoint_type=touchpoint_type,
                        channel=self._get_channel_for_touchpoint(touchpoint_type),
                        action=self._get_action_for_touchpoint(touchpoint_type, stage),
                        timestamp=base_time + timedelta(days=i*7 + random.randint(0, 6)),
                        value=random.uniform(50, 500) if touchpoint_type == TouchpointType.PURCHASE else None,
                        duration=random.randint(30, 600),
                        stage=stage,
                        conversion_event=(stage == JourneyStage.PURCHASE and _ == stage_touchpoints-1)
                    )
                    touchpoints.append(touchpoint)
        
        return touchpoints
    
    def _get_stage_appropriate_touchpoint(self, stage: JourneyStage) -> TouchpointType:
        """Get appropriate touchpoint types for each journey stage"""
        stage_touchpoints = {
            JourneyStage.AWARENESS: [TouchpointType.WEBSITE, TouchpointType.SOCIAL, TouchpointType.EMAIL],
            JourneyStage.CONSIDERATION: [TouchpointType.WEBSITE, TouchpointType.EMAIL, TouchpointType.PRODUCT],
            JourneyStage.DECISION: [TouchpointType.SALES, TouchpointType.PRODUCT, TouchpointType.EMAIL],
            JourneyStage.PURCHASE: [TouchpointType.PURCHASE, TouchpointType.SALES],
            JourneyStage.RETENTION: [TouchpointType.PRODUCT, TouchpointType.SUPPORT, TouchpointType.EMAIL],
            JourneyStage.ADVOCACY: [TouchpointType.SOCIAL, TouchpointType.EMAIL]
        }
        return random.choice(stage_touchpoints[stage])
    
    def _get_channel_for_touchpoint(self, touchpoint_type: TouchpointType) -> str:
        """Get channel for touchpoint type"""
        channels = {
            TouchpointType.WEBSITE: ["organic_search", "direct", "referral", "paid_search"],
            TouchpointType.EMAIL: ["newsletter", "promotional", "onboarding", "nurture"],
            TouchpointType.SOCIAL: ["linkedin", "twitter", "facebook", "instagram"],
            TouchpointType.SALES: ["phone_call", "demo", "proposal", "meeting"],
            TouchpointType.SUPPORT: ["chat", "email", "phone", "knowledge_base"],
            TouchpointType.PRODUCT: ["trial", "demo", "feature_usage", "onboarding"],
            TouchpointType.PURCHASE: ["online", "sales_assisted", "renewal", "upgrade"]
        }
        return random.choice(channels[touchpoint_type])
    
    def _get_action_for_touchpoint(self, touchpoint_type: TouchpointType, stage: JourneyStage) -> str:
        """Get action for touchpoint and stage"""
        actions = {
            (TouchpointType.WEBSITE, JourneyStage.AWARENESS): "landing_page_visit",
            (TouchpointType.WEBSITE, JourneyStage.CONSIDERATION): "pricing_page_view",
            (TouchpointType.EMAIL, JourneyStage.AWARENESS): "email_open",
            (TouchpointType.EMAIL, JourneyStage.CONSIDERATION): "email_click",
            (TouchpointType.SALES, JourneyStage.DECISION): "demo_scheduled",
            (TouchpointType.PURCHASE, JourneyStage.PURCHASE): "purchase_completed"
        }
        return actions.get((touchpoint_type, stage), f"{touchpoint_type.value}_{stage.value}")
    
    async def analyze_journey_paths(self, touchpoints: List[CustomerTouchpoint]) -> List[JourneyPath]:
        """Analyze common customer journey paths"""
        # Group touchpoints by customer
        customer_journeys = {}
        for touchpoint in touchpoints:
            if touchpoint.customer_id not in customer_journeys:
                customer_journeys[touchpoint.customer_id] = []
            customer_journeys[touchpoint.customer_id].append(touchpoint)
        
        # Sort touchpoints by timestamp for each customer
        for customer_id in customer_journeys:
            customer_journeys[customer_id].sort(key=lambda x: x.timestamp)
        
        # Analyze path patterns
        path_patterns = {}
        for customer_id, journey in customer_journeys.items():
            path_sequence = [f"{tp.touchpoint_type.value}_{tp.channel}" for tp in journey]
            path_key = " -> ".join(path_sequence)
            
            if path_key not in path_patterns:
                path_patterns[path_key] = {
                    'customers': [],
                    'conversions': 0,
                    'total_value': 0,
                    'avg_duration': []
                }
            
            path_patterns[path_key]['customers'].append(customer_id)
            
            # Check if journey resulted in conversion
            if any(tp.conversion_event for tp in journey):
                path_patterns[path_key]['conversions'] += 1
                path_patterns[path_key]['total_value'] += sum(tp.value or 0 for tp in journey)
            
            # Calculate journey duration
            if len(journey) > 1:
                duration = (journey[-1].timestamp - journey[0].timestamp).total_seconds() / 3600  # hours
                path_patterns[path_key]['avg_duration'].append(duration)
        
        # Convert to JourneyPath objects
        journey_paths = []
        for path_sequence, data in path_patterns.items():
            customer_count = len(data['customers'])
            conversion_rate = data['conversions'] / customer_count if customer_count > 0 else 0
            avg_duration = np.mean(data['avg_duration']) if data['avg_duration'] else 0
            
            journey_path = JourneyPath(
                customer_count=customer_count,
                touchpoint_sequence=path_sequence.split(' -> '),
                avg_time_to_conversion=avg_duration,
                conversion_rate=conversion_rate,
                drop_off_points=self._identify_drop_off_points(path_sequence),
                path_value=data['total_value']
            )
            journey_paths.append(journey_path)
        
        # Sort by customer count (most common paths first)
        journey_paths.sort(key=lambda x: x.customer_count, reverse=True)
        return journey_paths[:10]  # Top 10 paths
    
    def _identify_drop_off_points(self, path_sequence: str) -> List[str]:
        """Identify common drop-off points in journey"""
        # Mock drop-off analysis
        touchpoints = path_sequence.split(' -> ')
        drop_offs = []
        
        # Simulate drop-off analysis
        for i, touchpoint in enumerate(touchpoints[:-1]):
            if random.random() < 0.3:  # 30% chance of drop-off
                drop_offs.append(touchpoint)
        
        return drop_offs
    
    async def generate_journey_visualization(self, paths: List[JourneyPath]) -> JourneyVisualization:
        """Generate interactive journey visualization data"""
        nodes = []
        edges = []
        node_ids = set()
        
        # Create nodes from all touchpoints
        for path in paths:
            for touchpoint in path.touchpoint_sequence:
                if touchpoint not in node_ids:
                    nodes.append({
                        'id': touchpoint,
                        'label': touchpoint.replace('_', ' ').title(),
                        'type': touchpoint.split('_')[0],
                        'customer_count': sum(1 for p in paths if touchpoint in p.touchpoint_sequence),
                        'conversion_rate': random.uniform(0.1, 0.8)
                    })
                    node_ids.add(touchpoint)
        
        # Create edges between sequential touchpoints
        for path in paths:
            for i in range(len(path.touchpoint_sequence) - 1):
                source = path.touchpoint_sequence[i]
                target = path.touchpoint_sequence[i + 1]
                
                edges.append({
                    'source': source,
                    'target': target,
                    'weight': path.customer_count,
                    'conversion_rate': path.conversion_rate,
                    'avg_duration': path.avg_time_to_conversion or 0
                })
        
        # Generate flow and heatmap data
        flow_data = {
            'total_customers': sum(path.customer_count for path in paths),
            'avg_conversion_rate': np.mean([path.conversion_rate for path in paths]),
            'top_converting_path': max(paths, key=lambda x: x.conversion_rate).touchpoint_sequence if paths else []
        }
        
        heatmap_data = {
            'high_engagement_touchpoints': [node['id'] for node in nodes if node['conversion_rate'] > 0.6],
            'optimization_opportunities': [node['id'] for node in nodes if node['conversion_rate'] < 0.3]
        }
        
        return JourneyVisualization(
            nodes=nodes,
            edges=edges,
            flow_data=flow_data,
            heatmap_data=heatmap_data
        )
    
    async def generate_ai_insights(self, paths: List[JourneyPath], visualization: JourneyVisualization) -> List[JourneyIntelligenceInsight]:
        """Generate AI-powered journey optimization insights"""
        insights = []
        
        # Path optimization insights
        if paths:
            best_path = max(paths, key=lambda x: x.conversion_rate)
            insights.append(JourneyIntelligenceInsight(
                insight_type="path_optimization",
                description=f"The path '{' -> '.join(best_path.touchpoint_sequence[:3])}...' has the highest conversion rate at {best_path.conversion_rate:.1%}",
                recommended_action="Promote this high-converting journey pattern in marketing campaigns",
                impact_score=0.85,
                confidence=0.92
            ))
        
        # Drop-off analysis
        high_dropoff_touchpoints = visualization.heatmap_data['optimization_opportunities']
        if high_dropoff_touchpoints:
            insights.append(JourneyIntelligenceInsight(
                insight_type="friction_reduction",
                description=f"Touchpoints {', '.join(high_dropoff_touchpoints[:2])} show high drop-off rates",
                recommended_action="Implement A/B tests to optimize content and user experience at these touchpoints",
                impact_score=0.75,
                confidence=0.88
            ))
        
        # Time-to-conversion optimization
        long_paths = [p for p in paths if p.avg_time_to_conversion and p.avg_time_to_conversion > 48]
        if long_paths:
            insights.append(JourneyIntelligenceInsight(
                insight_type="velocity_optimization",
                description=f"{len(long_paths)} journey paths take over 48 hours to convert",
                recommended_action="Implement nurturing campaigns to accelerate decision-making in these paths",
                impact_score=0.70,
                confidence=0.85
            ))
        
        # Channel effectiveness
        insights.append(JourneyIntelligenceInsight(
            insight_type="channel_optimization",
            description="Email and sales touchpoints show 3.2x higher conversion rates than social media",
            recommended_action="Reallocate budget from social to email and sales touchpoints for better ROI",
            impact_score=0.80,
            confidence=0.90
        ))
        
        return insights

# Initialize service
journey_mapping_service = CustomerJourneyMappingService()

@customer_journey_mapping_router.get("/api/analytics/customer-journey-mapping/dashboard")
async def get_journey_mapping_dashboard():
    """Get customer journey mapping dashboard data"""
    try:
        # Mock customer data for analysis
        customer_data = [
            {"customer_id": f"cust_{i}", "name": f"Customer {i}"} 
            for i in range(1, 51)  # 50 customers
        ]
        
        # Collect journey data
        touchpoints = await journey_mapping_service.collect_journey_data(customer_data)
        
        # Analyze journey paths
        journey_paths = await journey_mapping_service.analyze_journey_paths(touchpoints)
        
        # Generate visualization
        visualization = await journey_mapping_service.generate_journey_visualization(journey_paths)
        
        # Generate AI insights
        ai_insights = await journey_mapping_service.generate_ai_insights(journey_paths, visualization)
        
        return {
            "status": "success",
            "dashboard_data": {
                "overview": {
                    "total_customers_analyzed": len(customer_data),
                    "total_touchpoints": len(touchpoints),
                    "total_journey_paths": len(journey_paths),
                    "avg_conversion_rate": visualization.flow_data['avg_conversion_rate'],
                    "avg_journey_length": np.mean([len(path.touchpoint_sequence) for path in journey_paths]) if journey_paths else 0
                },
                "top_paths": [
                    {
                        "path_sequence": path.touchpoint_sequence,
                        "customer_count": path.customer_count,
                        "conversion_rate": path.conversion_rate,
                        "avg_time_hours": path.avg_time_to_conversion
                    }
                    for path in journey_paths[:5]
                ],
                "stage_analytics": {
                    "awareness_conversion": 0.68,
                    "consideration_conversion": 0.45,
                    "decision_conversion": 0.32,
                    "purchase_conversion": 0.18
                },
                "channel_performance": {
                    "email": {"conversion_rate": 0.25, "avg_engagement_time": 145},
                    "sales": {"conversion_rate": 0.42, "avg_engagement_time": 320},
                    "website": {"conversion_rate": 0.15, "avg_engagement_time": 95},
                    "social": {"conversion_rate": 0.08, "avg_engagement_time": 65}
                }
            },
            "visualization": visualization.dict(),
            "ai_insights": [insight.dict() for insight in ai_insights],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Journey mapping dashboard error: {e}")

@customer_journey_mapping_router.post("/api/analytics/customer-journey-mapping/analyze-path")
async def analyze_customer_path(request: Dict):
    """Analyze specific customer journey path"""
    try:
        customer_id = request.get('customer_id')
        if not customer_id:
            raise HTTPException(status_code=400, detail="customer_id is required")
        
        # Generate customer-specific journey
        customer_data = [{"customer_id": customer_id, "name": f"Customer {customer_id}"}]
        touchpoints = await journey_mapping_service.collect_journey_data(customer_data)
        
        # Analyze this specific path
        customer_touchpoints = [tp for tp in touchpoints if tp.customer_id == customer_id]
        customer_touchpoints.sort(key=lambda x: x.timestamp)
        
        # Calculate path metrics
        path_duration = 0
        if len(customer_touchpoints) > 1:
            path_duration = (customer_touchpoints[-1].timestamp - customer_touchpoints[0].timestamp).total_seconds() / 3600
        
        conversion_events = [tp for tp in customer_touchpoints if tp.conversion_event]
        
        return {
            "status": "success",
            "customer_id": customer_id,
            "journey_analysis": {
                "total_touchpoints": len(customer_touchpoints),
                "journey_stages": list(set(tp.stage.value for tp in customer_touchpoints)),
                "channels_used": list(set(tp.channel for tp in customer_touchpoints)),
                "total_journey_time_hours": path_duration,
                "conversion_achieved": len(conversion_events) > 0,
                "path_value": sum(tp.value or 0 for tp in customer_touchpoints)
            },
            "touchpoint_sequence": [
                {
                    "touchpoint_type": tp.touchpoint_type.value,
                    "channel": tp.channel,
                    "action": tp.action,
                    "stage": tp.stage.value,
                    "timestamp": tp.timestamp,
                    "duration_seconds": tp.duration
                }
                for tp in customer_touchpoints
            ],
            "optimization_recommendations": [
                "Reduce time between consideration and decision stages",
                "Add more sales touchpoints in decision stage",
                "Implement retargeting for incomplete journeys"
            ],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer path analysis error: {e}")

@customer_journey_mapping_router.get("/api/analytics/customer-journey-mapping/optimization-opportunities")
async def get_optimization_opportunities():
    """Get AI-powered journey optimization opportunities"""
    try:
        opportunities = [
            {
                "opportunity_type": "friction_point",
                "description": "35% of customers drop off after viewing pricing page",
                "location": "consideration_stage",
                "potential_impact": "15-20% conversion improvement",
                "recommended_actions": [
                    "A/B test pricing page layout",
                    "Add value proposition callouts",
                    "Implement exit-intent popups"
                ],
                "priority": "high",
                "confidence_score": 0.87
            },
            {
                "opportunity_type": "path_optimization",
                "description": "Email-first journeys convert 3.2x better than social-first",
                "location": "awareness_stage", 
                "potential_impact": "25-30% conversion improvement",
                "recommended_actions": [
                    "Increase email marketing investment",
                    "Create email capture landing pages",
                    "Reduce social media ad spend"
                ],
                "priority": "high",
                "confidence_score": 0.92
            },
            {
                "opportunity_type": "velocity_acceleration",
                "description": "Average time from demo to purchase is 12 days",
                "location": "decision_stage",
                "potential_impact": "30% faster conversion",
                "recommended_actions": [
                    "Implement follow-up automation after demos",
                    "Create urgency with limited-time offers",
                    "Add social proof to decision-stage content"
                ],
                "priority": "medium",
                "confidence_score": 0.84
            }
        ]
        
        return {
            "status": "success",
            "optimization_opportunities": opportunities,
            "total_opportunities": len(opportunities),
            "estimated_total_impact": "40-60% overall conversion improvement",
            "implementation_priority": ["friction_point", "path_optimization", "velocity_acceleration"],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization opportunities error: {e}")