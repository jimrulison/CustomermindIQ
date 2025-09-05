"""
Customer Mind IQ - Journey Mapping Microservice
AI-powered customer journey analysis and touchpoint optimization
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import uuid

class JourneyStage(BaseModel):
    stage_id: str
    stage_name: str
    stage_order: int
    customer_count: int
    avg_duration_days: int
    conversion_rate: float
    key_actions: List[str]
    pain_points: List[str]
    optimization_opportunities: List[str]

class CustomerJourney(BaseModel):
    customer_id: str
    current_stage: str
    journey_start_date: datetime
    stages_completed: List[str]
    total_journey_days: int
    touchpoints_engaged: List[str]
    conversion_probability: float
    next_best_action: str
    predicted_next_stage: str
    journey_health_score: int  # 0-100
    behavioral_patterns: Dict[str, Any]

class TouchpointAnalysis(BaseModel):
    touchpoint_id: str
    touchpoint_name: str
    stage: str
    engagement_rate: float
    conversion_impact: float
    customer_satisfaction: float
    optimization_score: int  # 0-100
    improvement_recommendations: List[str]

class JourneyMappingService:
    """Customer Mind IQ Journey Mapping Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[os.environ.get('DB_NAME', 'customer_mind_iq')]
        
        # Standard journey stages for software customers
        self.journey_stages = [
            "awareness", "consideration", "trial", "purchase", 
            "onboarding", "adoption", "expansion", "advocacy"
        ]
    
    async def analyze_customer_journeys(self, customers_data: List[Dict]) -> List[CustomerJourney]:
        """Analyze customer journeys using AI"""
        try:
            journey_maps = []
            
            for customer in customers_data:
                journey = await self._map_individual_journey(customer)
                journey_maps.append(journey)
            
            # Store results
            await self._store_journey_results(journey_maps)
            
            return journey_maps
            
        except Exception as e:
            print(f"Journey mapping error: {e}")
            return await self._fallback_journey_analysis(customers_data)
    
    async def _map_individual_journey(self, customer: Dict) -> CustomerJourney:
        """Map individual customer journey using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"journey_mapping_{customer.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ's customer journey specialist. Analyze customer data 
                to map their journey through software purchase and adoption stages."""
            ).with_model("openai", "gpt-4o-mini")
            
            # Calculate journey indicators
            journey_indicators = {
                "total_purchases": customer.get('total_purchases', 0),
                "total_spent": customer.get('total_spent', 0),
                "engagement_score": customer.get('engagement_score', 50),
                "software_portfolio": customer.get('software_owned', []),
                "lifecycle_stage": customer.get('lifecycle_stage', 'new'),
                "days_since_first_purchase": self._days_since_first_interaction(customer),
                "purchase_patterns": customer.get('purchase_patterns', {}),
                "last_activity_days": self._days_since_last_purchase(customer.get('last_purchase_date'))
            }
            
            journey_prompt = f"""
            Map customer journey using Customer Mind IQ advanced journey analytics:
            
            Customer Profile:
            - ID: {customer.get('customer_id')}
            - Name: {customer.get('name')}
            - Journey Indicators: {json.dumps(journey_indicators, default=str)}
            
            Journey Stages: {self.journey_stages}
            
            Analyze and map customer journey in this exact JSON format:
            {{
                "current_stage": "<awareness/consideration/trial/purchase/onboarding/adoption/expansion/advocacy>",
                "stages_completed": ["stage1", "stage2", "stage3"],
                "total_journey_days": <days_since_first_interaction>,
                "touchpoints_engaged": ["website", "email", "support", "product_demo", "purchase"],
                "conversion_probability": <0.0-1.0>,
                "next_best_action": "<specific_action_recommendation>",
                "predicted_next_stage": "<next_stage_name>",
                "journey_health_score": <0-100>,
                "behavioral_patterns": {{
                    "engagement_trend": "<increasing/stable/declining>",
                    "purchase_velocity": "<fast/normal/slow>",
                    "feature_adoption": "<high/medium/low>",
                    "support_dependency": "<high/medium/low>"
                }}
            }}
            
            Consider:
            1. Customer lifecycle position and progression
            2. Purchase history and spending patterns
            3. Engagement levels and interaction frequency
            4. Software adoption and usage indicators
            5. Time spent in each journey stage
            """
            
            message = UserMessage(text=journey_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                
                # Calculate journey start date
                journey_start = datetime.now() - timedelta(days=analysis.get('total_journey_days', 30))
                
                return CustomerJourney(
                    customer_id=customer['customer_id'],
                    current_stage=analysis.get('current_stage', 'consideration'),
                    journey_start_date=journey_start,
                    stages_completed=analysis.get('stages_completed', []),
                    total_journey_days=analysis.get('total_journey_days', 30),
                    touchpoints_engaged=analysis.get('touchpoints_engaged', []),
                    conversion_probability=analysis.get('conversion_probability', 0.5),
                    next_best_action=analysis.get('next_best_action', 'Personalized follow-up'),
                    predicted_next_stage=analysis.get('predicted_next_stage', 'purchase'),
                    journey_health_score=analysis.get('journey_health_score', 70),
                    behavioral_patterns=analysis.get('behavioral_patterns', {})
                )
                
            except json.JSONDecodeError:
                return await self._fallback_individual_journey(customer)
                
        except Exception as e:
            print(f"Individual journey mapping error: {e}")
            return await self._fallback_individual_journey(customer)
    
    async def analyze_journey_stages(self) -> List[JourneyStage]:
        """Analyze performance of each journey stage"""
        try:
            # Get latest journey data
            latest_journeys = await self.db.customer_journeys.find(
                {}, sort=[("created_at", -1)]
            ).to_list(length=1000)
            
            if not latest_journeys:
                return await self._generate_sample_stages()
            
            # Analyze each stage
            stage_analysis = {}
            for journey in latest_journeys:
                current_stage = journey.get('current_stage', 'consideration')
                
                if current_stage not in stage_analysis:
                    stage_analysis[current_stage] = {
                        "customers": [],
                        "durations": [],
                        "health_scores": [],
                        "conversion_probs": []
                    }
                
                stage_analysis[current_stage]["customers"].append(journey.get('customer_id'))
                stage_analysis[current_stage]["durations"].append(journey.get('total_journey_days', 30))
                stage_analysis[current_stage]["health_scores"].append(journey.get('journey_health_score', 70))
                stage_analysis[current_stage]["conversion_probs"].append(journey.get('conversion_probability', 0.5))
            
            # Generate AI insights for each stage
            stages = []
            for i, stage_name in enumerate(self.journey_stages):
                if stage_name in stage_analysis:
                    data = stage_analysis[stage_name]
                    stage = await self._analyze_stage_performance(stage_name, i, data)
                    stages.append(stage)
            
            return stages
            
        except Exception as e:
            print(f"Journey stage analysis error: {e}")
            return await self._generate_sample_stages()
    
    async def _analyze_stage_performance(self, stage_name: str, order: int, stage_data: Dict) -> JourneyStage:
        """Analyze performance of specific journey stage using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"stage_analysis_{stage_name}_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's journey optimization specialist. Analyze journey stage 
                performance and provide actionable optimization recommendations."""
            ).with_model("openai", "gpt-4o-mini")
            
            stage_metrics = {
                "customer_count": len(stage_data["customers"]),
                "avg_duration": sum(stage_data["durations"]) / len(stage_data["durations"]),
                "avg_health_score": sum(stage_data["health_scores"]) / len(stage_data["health_scores"]),
                "avg_conversion_prob": sum(stage_data["conversion_probs"]) / len(stage_data["conversion_probs"])
            }
            
            analysis_prompt = f"""
            Analyze journey stage performance for Customer Mind IQ optimization:
            
            Stage: {stage_name.title()}
            Stage Order: {order + 1} of {len(self.journey_stages)}
            Stage Metrics: {json.dumps(stage_metrics, default=str)}
            
            Provide stage optimization analysis in JSON format:
            {{
                "conversion_rate": <0.0-1.0>,
                "key_actions": ["action1", "action2", "action3"],
                "pain_points": ["pain1", "pain2", "pain3"],
                "optimization_opportunities": ["opportunity1", "opportunity2", "opportunity3"]
            }}
            
            Focus on:
            1. Stage-specific customer behaviors and patterns
            2. Common obstacles and friction points
            3. Conversion optimization opportunities
            4. Touchpoint effectiveness
            5. Duration optimization strategies
            """
            
            message = UserMessage(text=analysis_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                
                return JourneyStage(
                    stage_id=f"stage_{order}_{stage_name}",
                    stage_name=stage_name.title(),
                    stage_order=order,
                    customer_count=stage_metrics["customer_count"],
                    avg_duration_days=int(stage_metrics["avg_duration"]),
                    conversion_rate=analysis.get('conversion_rate', stage_metrics["avg_conversion_prob"]),
                    key_actions=analysis.get('key_actions', []),
                    pain_points=analysis.get('pain_points', []),
                    optimization_opportunities=analysis.get('optimization_opportunities', [])
                )
                
            except json.JSONDecodeError:
                return self._fallback_stage_analysis(stage_name, order, stage_metrics)
                
        except Exception as e:
            print(f"Stage analysis error: {e}")
            return self._fallback_stage_analysis(stage_name, order, stage_metrics)
    
    async def analyze_touchpoints(self) -> List[TouchpointAnalysis]:
        """Analyze touchpoint effectiveness across customer journeys"""
        try:
            # Get journey data
            latest_journeys = await self.db.customer_journeys.find(
                {}, sort=[("created_at", -1)]
            ).to_list(length=1000)
            
            if not latest_journeys:
                return await self._generate_sample_touchpoints()
            
            # Aggregate touchpoint data
            touchpoint_data = {}
            for journey in latest_journeys:
                for touchpoint in journey.get('touchpoints_engaged', []):
                    if touchpoint not in touchpoint_data:
                        touchpoint_data[touchpoint] = {
                            "customers": [],
                            "stages": [],
                            "health_scores": [],
                            "conversion_probs": []
                        }
                    
                    touchpoint_data[touchpoint]["customers"].append(journey.get('customer_id'))
                    touchpoint_data[touchpoint]["stages"].append(journey.get('current_stage'))
                    touchpoint_data[touchpoint]["health_scores"].append(journey.get('journey_health_score', 70))
                    touchpoint_data[touchpoint]["conversion_probs"].append(journey.get('conversion_probability', 0.5))
            
            # Analyze each touchpoint
            touchpoint_analyses = []
            for touchpoint_name, data in touchpoint_data.items():
                analysis = await self._analyze_individual_touchpoint(touchpoint_name, data)
                touchpoint_analyses.append(analysis)
            
            # Sort by optimization score
            touchpoint_analyses.sort(key=lambda x: x.optimization_score, reverse=True)
            
            return touchpoint_analyses
            
        except Exception as e:
            print(f"Touchpoint analysis error: {e}")
            return await self._generate_sample_touchpoints()
    
    async def _analyze_individual_touchpoint(self, touchpoint_name: str, data: Dict) -> TouchpointAnalysis:
        """Analyze individual touchpoint performance"""
        try:
            # Calculate basic metrics
            engagement_rate = len(data["customers"]) / 100  # Normalize based on customer base
            avg_health_score = sum(data["health_scores"]) / len(data["health_scores"])
            avg_conversion_prob = sum(data["conversion_probs"]) / len(data["conversion_probs"])
            
            # Determine primary stage
            stage_counts = {}
            for stage in data["stages"]:
                stage_counts[stage] = stage_counts.get(stage, 0) + 1
            primary_stage = max(stage_counts.items(), key=lambda x: x[1])[0] if stage_counts else "consideration"
            
            # Calculate optimization score (0-100)
            optimization_score = int(
                (engagement_rate * 0.4 + avg_conversion_prob * 0.4 + (avg_health_score / 100) * 0.2) * 100
            )
            
            # Generate improvement recommendations using AI
            recommendations = await self._generate_touchpoint_recommendations(
                touchpoint_name, engagement_rate, avg_conversion_prob, avg_health_score
            )
            
            return TouchpointAnalysis(
                touchpoint_id=str(uuid.uuid4()),
                touchpoint_name=touchpoint_name,
                stage=primary_stage,
                engagement_rate=engagement_rate,
                conversion_impact=avg_conversion_prob,
                customer_satisfaction=avg_health_score / 100,
                optimization_score=optimization_score,
                improvement_recommendations=recommendations
            )
            
        except Exception as e:
            print(f"Individual touchpoint analysis error: {e}")
            return TouchpointAnalysis(
                touchpoint_id=str(uuid.uuid4()),
                touchpoint_name=touchpoint_name,
                stage="consideration",
                engagement_rate=0.5,
                conversion_impact=0.5,
                customer_satisfaction=0.7,
                optimization_score=60,
                improvement_recommendations=["Improve engagement", "Optimize content", "Enhance user experience"]
            )
    
    async def _generate_touchpoint_recommendations(self, touchpoint: str, engagement: float, conversion: float, satisfaction: float) -> List[str]:
        """Generate AI-powered touchpoint recommendations"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"touchpoint_recommendations_{touchpoint}",
                system_message="""You are Customer Mind IQ's touchpoint optimization expert. Provide specific, 
                actionable recommendations to improve touchpoint performance."""
            ).with_model("openai", "gpt-4o-mini")
            
            recommendation_prompt = f"""
            Generate optimization recommendations for this touchpoint:
            
            Touchpoint: {touchpoint}
            Current Metrics:
            - Engagement Rate: {engagement:.2f}
            - Conversion Impact: {conversion:.2f}
            - Customer Satisfaction: {satisfaction:.2f}
            
            Provide 3-5 specific, actionable recommendations in JSON format:
            {{
                "recommendations": ["recommendation1", "recommendation2", "recommendation3"]
            }}
            
            Focus on practical improvements that can boost engagement, conversion, and satisfaction.
            """
            
            message = UserMessage(text=recommendation_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                return analysis.get('recommendations', ["Optimize content", "Improve user experience", "Enhance personalization"])
            except json.JSONDecodeError:
                return ["Optimize content", "Improve user experience", "Enhance personalization"]
                
        except Exception as e:
            print(f"Touchpoint recommendations error: {e}")
            return ["Optimize content", "Improve user experience", "Enhance personalization"]
    
    def _days_since_first_interaction(self, customer: Dict) -> int:
        """Calculate days since first customer interaction"""
        # Use last purchase date as proxy for first interaction
        last_purchase = customer.get('last_purchase_date')
        if not last_purchase:
            return 90  # Default assumption
        
        total_purchases = customer.get('total_purchases', 1)
        if total_purchases <= 1:
            return self._days_since_last_purchase(last_purchase)
        
        # Estimate first interaction based on purchase frequency
        avg_days_between_purchases = 60  # Assumption
        return self._days_since_last_purchase(last_purchase) + (total_purchases - 1) * avg_days_between_purchases
    
    def _days_since_last_purchase(self, last_purchase_date) -> int:
        """Calculate days since last purchase"""
        if not last_purchase_date:
            return 90
        
        if isinstance(last_purchase_date, str):
            try:
                last_purchase_date = datetime.fromisoformat(last_purchase_date.replace('Z', '+00:00'))
            except:
                return 90
        
        return (datetime.now() - last_purchase_date).days
    
    async def get_journey_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive journey mapping dashboard data"""
        try:
            # Get journey stages and touchpoints
            stages = await self.analyze_journey_stages()
            touchpoints = await self.analyze_touchpoints()
            
            # Get latest journeys
            latest_journeys = await self.db.customer_journeys.find(
                {}, sort=[("created_at", -1)]
            ).to_list(length=1000)
            
            if not latest_journeys:
                return await self._generate_sample_dashboard()
            
            # Calculate dashboard metrics
            total_customers = len(latest_journeys)
            avg_journey_health = sum(j.get('journey_health_score', 70) for j in latest_journeys) / total_customers
            avg_conversion_prob = sum(j.get('conversion_probability', 0.5) for j in latest_journeys) / total_customers
            
            # Stage distribution
            stage_distribution = {}
            for journey in latest_journeys:
                stage = journey.get('current_stage', 'consideration')
                stage_distribution[stage] = stage_distribution.get(stage, 0) + 1
            
            # Journey health distribution
            health_distribution = {"excellent": 0, "good": 0, "fair": 0, "poor": 0}
            for journey in latest_journeys:
                health_score = journey.get('journey_health_score', 70)
                if health_score >= 90:
                    health_distribution["excellent"] += 1
                elif health_score >= 75:
                    health_distribution["good"] += 1
                elif health_score >= 60:
                    health_distribution["fair"] += 1
                else:
                    health_distribution["poor"] += 1
            
            return {
                "journey_overview": {
                    "total_customers_mapped": total_customers,
                    "average_journey_health": avg_journey_health,
                    "average_conversion_probability": avg_conversion_prob,
                    "active_stages": len(stage_distribution),
                    "total_touchpoints": len(touchpoints)
                },
                "stage_distribution": stage_distribution,
                "health_distribution": health_distribution,
                "stage_performance": [
                    {
                        "stage_name": stage.stage_name,
                        "customer_count": stage.customer_count,
                        "avg_duration": stage.avg_duration_days,
                        "conversion_rate": stage.conversion_rate
                    }
                    for stage in stages[:5]  # Top 5 stages
                ],
                "top_touchpoints": [
                    {
                        "touchpoint_name": tp.touchpoint_name,
                        "optimization_score": tp.optimization_score,
                        "engagement_rate": tp.engagement_rate,
                        "conversion_impact": tp.conversion_impact
                    }
                    for tp in touchpoints[:5]  # Top 5 touchpoints
                ],
                "optimization_priorities": [
                    "Improve low-performing touchpoints",
                    "Accelerate slow journey stages",
                    "Enhance customer journey health scores"
                ]
            }
            
        except Exception as e:
            print(f"Journey dashboard error: {e}")
            return await self._generate_sample_dashboard()
    
    async def _fallback_journey_analysis(self, customers_data: List[Dict]) -> List[CustomerJourney]:
        """Fallback journey analysis when AI fails"""
        journeys = []
        for customer in customers_data:
            journey = await self._fallback_individual_journey(customer)
            journeys.append(journey)
        return journeys
    
    async def _fallback_individual_journey(self, customer: Dict) -> CustomerJourney:
        """Create fallback customer journey"""
        total_purchases = customer.get('total_purchases', 0)
        engagement_score = customer.get('engagement_score', 50)
        
        # Determine stage based on purchase history
        if total_purchases == 0:
            current_stage = "consideration"
            stages_completed = ["awareness"]
        elif total_purchases == 1:
            current_stage = "onboarding"
            stages_completed = ["awareness", "consideration", "purchase"]
        elif total_purchases < 5:
            current_stage = "adoption"
            stages_completed = ["awareness", "consideration", "purchase", "onboarding"]
        else:
            current_stage = "expansion"
            stages_completed = ["awareness", "consideration", "purchase", "onboarding", "adoption"]
        
        journey_days = max(30, total_purchases * 45)  # Rough estimate
        
        return CustomerJourney(
            customer_id=customer['customer_id'],
            current_stage=current_stage,
            journey_start_date=datetime.now() - timedelta(days=journey_days),
            stages_completed=stages_completed,
            total_journey_days=journey_days,
            touchpoints_engaged=["website", "email", "product"],
            conversion_probability=min(0.9, (engagement_score + total_purchases * 10) / 100),
            next_best_action="Personalized follow-up based on behavior",
            predicted_next_stage="expansion" if current_stage == "adoption" else "advocacy",
            journey_health_score=min(100, engagement_score + 20),
            behavioral_patterns={
                "engagement_trend": "stable" if engagement_score > 50 else "declining",
                "purchase_velocity": "normal",
                "feature_adoption": "medium",
                "support_dependency": "low"
            }
        )
    
    def _fallback_stage_analysis(self, stage_name: str, order: int, metrics: Dict) -> JourneyStage:
        """Create fallback stage analysis"""
        return JourneyStage(
            stage_id=f"stage_{order}_{stage_name}",
            stage_name=stage_name.title(),
            stage_order=order,
            customer_count=metrics.get("customer_count", 5),
            avg_duration_days=int(metrics.get("avg_duration", 30)),
            conversion_rate=metrics.get("avg_conversion_prob", 0.6),
            key_actions=["Engage customers", "Provide value", "Remove friction"],
            pain_points=["Long duration", "Low engagement", "Unclear next steps"],
            optimization_opportunities=["Streamline process", "Improve communication", "Add automation"]
        )
    
    async def _generate_sample_stages(self) -> List[JourneyStage]:
        """Generate sample journey stages"""
        sample_stages = []
        for i, stage_name in enumerate(self.journey_stages):
            stage = JourneyStage(
                stage_id=f"stage_{i}_{stage_name}",
                stage_name=stage_name.title(),
                stage_order=i,
                customer_count=max(1, 20 - i * 2),
                avg_duration_days=30 + i * 15,
                conversion_rate=max(0.3, 0.8 - i * 0.1),
                key_actions=["Engage", "Educate", "Convert"],
                pain_points=["Friction points", "Unclear value"],
                optimization_opportunities=["Improve experience", "Add automation"]
            )
            sample_stages.append(stage)
        return sample_stages
    
    async def _generate_sample_touchpoints(self) -> List[TouchpointAnalysis]:
        """Generate sample touchpoint analysis"""
        touchpoints = ["website", "email", "product_demo", "support", "onboarding"]
        sample_touchpoints = []
        
        for i, tp_name in enumerate(touchpoints):
            touchpoint = TouchpointAnalysis(
                touchpoint_id=str(uuid.uuid4()),
                touchpoint_name=tp_name,
                stage="consideration",
                engagement_rate=0.7 - i * 0.1,
                conversion_impact=0.6 - i * 0.05,
                customer_satisfaction=0.8 - i * 0.1,
                optimization_score=85 - i * 10,
                improvement_recommendations=["Optimize content", "Improve UX", "Personalize experience"]
            )
            sample_touchpoints.append(touchpoint)
        
        return sample_touchpoints
    
    async def _generate_sample_dashboard(self) -> Dict[str, Any]:
        """Generate sample dashboard data"""
        return {
            "journey_overview": {
                "total_customers_mapped": 50,
                "average_journey_health": 72,
                "average_conversion_probability": 0.65,
                "active_stages": 6,
                "total_touchpoints": 8
            },
            "stage_distribution": {
                "awareness": 5,
                "consideration": 12,
                "trial": 8,
                "purchase": 6,
                "onboarding": 7,
                "adoption": 8,
                "expansion": 3,
                "advocacy": 1
            },
            "health_distribution": {"excellent": 8, "good": 22, "fair": 15, "poor": 5},
            "stage_performance": [],
            "top_touchpoints": [],
            "optimization_priorities": [
                "Focus on trial to purchase conversion",
                "Improve onboarding experience",
                "Accelerate adoption timeline"
            ]
        }
    
    async def _store_journey_results(self, journeys: List[CustomerJourney]):
        """Store journey mapping results"""
        try:
            documents = []
            for journey in journeys:
                document = journey.dict()
                document["created_at"] = datetime.now()
                document["service"] = "journey_mapping"
                documents.append(document)
            
            if documents:
                await self.db.customer_journeys.insert_many(documents)
                
        except Exception as e:
            print(f"Error storing journey results: {e}")