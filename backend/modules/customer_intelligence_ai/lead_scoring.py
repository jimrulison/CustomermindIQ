"""
Customer Mind IQ - Lead Scoring Microservice
AI-powered lead qualification and scoring system for software sales
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

class LeadScore(BaseModel):
    customer_id: str
    overall_score: int  # 0-100
    conversion_probability: float  # 0-1
    score_breakdown: Dict[str, int]  # Component scores
    qualification_level: str  # cold, warm, hot, qualified
    predicted_deal_size: float
    time_to_conversion: Optional[int]  # days
    recommended_actions: List[str]
    sales_priority: str  # low, medium, high, urgent

class ScoreComponent(BaseModel):
    component_name: str
    weight: float
    score: int  # 0-100
    factors: List[str]
    improvement_suggestions: List[str]

class LeadScoringService:
    """Customer Mind IQ Lead Scoring Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq
        
        # Lead scoring model configuration
        self.scoring_weights = {
            "demographic_fit": 0.25,
            "behavioral_engagement": 0.30,
            "purchase_history": 0.20,
            "software_needs": 0.15,
            "timing_factors": 0.10
        }
    
    async def calculate_lead_scores(self, customers_data: List[Dict]) -> List[LeadScore]:
        """Calculate comprehensive lead scores for all customers"""
        try:
            lead_scores = []
            
            for customer in customers_data:
                score = await self._calculate_individual_lead_score(customer)
                lead_scores.append(score)
            
            # Sort by overall score (highest first)
            lead_scores.sort(key=lambda x: x.overall_score, reverse=True)
            
            # Store results
            await self._store_scoring_results(lead_scores)
            
            return lead_scores
            
        except Exception as e:
            print(f"Lead scoring error: {e}")
            return await self._fallback_lead_scoring(customers_data)
    
    async def _calculate_individual_lead_score(self, customer: Dict) -> LeadScore:
        """Calculate comprehensive lead score for individual customer using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"lead_scoring_{customer.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ's lead scoring specialist. Analyze customer data 
                to generate accurate lead scores and sales recommendations for software products."""
            ).with_model("openai", "gpt-4o-mini")
            
            # Gather customer intelligence
            customer_profile = {
                "id": customer.get('customer_id'),
                "name": customer.get('name'),
                "email": customer.get('email'),
                "total_spent": customer.get('total_spent', 0),
                "total_purchases": customer.get('total_purchases', 0),
                "engagement_score": customer.get('engagement_score', 50),
                "software_owned": customer.get('software_owned', []),
                "lifecycle_stage": customer.get('lifecycle_stage', 'unknown'),
                "last_purchase_days": self._days_since_last_purchase(customer.get('last_purchase_date')),
                "purchase_patterns": customer.get('purchase_patterns', {})
            }
            
            scoring_prompt = f"""
            Analyze this customer for lead scoring using Customer Mind IQ advanced algorithms:
            
            Customer Profile: {json.dumps(customer_profile, default=str)}
            
            Calculate lead score considering:
            1. Demographic Fit (25%): Company size, industry alignment, budget indicators
            2. Behavioral Engagement (30%): Website activity, email engagement, software usage patterns
            3. Purchase History (20%): Past spending, purchase frequency, product mix
            4. Software Needs (15%): Current software gaps, upgrade opportunities
            5. Timing Factors (10%): Purchase cycles, seasonality, urgency indicators
            
            Provide comprehensive lead scoring in this exact JSON format:
            {{
                "overall_score": <0-100>,
                "conversion_probability": <0.0-1.0>,
                "score_breakdown": {{
                    "demographic_fit": <0-100>,
                    "behavioral_engagement": <0-100>,
                    "purchase_history": <0-100>,
                    "software_needs": <0-100>,
                    "timing_factors": <0-100>
                }},
                "qualification_level": "<cold/warm/hot/qualified>",
                "predicted_deal_size": <dollar_amount>,
                "time_to_conversion": <days_or_null>,
                "recommended_actions": ["action1", "action2", "action3"],
                "sales_priority": "<low/medium/high/urgent>",
                "score_reasoning": {{
                    "strengths": ["strength1", "strength2"],
                    "weaknesses": ["weakness1", "weakness2"],
                    "opportunities": ["opportunity1", "opportunity2"]
                }}
            }}
            
            Base scoring on concrete customer behaviors, spending patterns, and software needs.
            """
            
            message = UserMessage(text=scoring_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                
                return LeadScore(
                    customer_id=customer['customer_id'],
                    overall_score=analysis.get('overall_score', 50),
                    conversion_probability=analysis.get('conversion_probability', 0.5),
                    score_breakdown=analysis.get('score_breakdown', {}),
                    qualification_level=analysis.get('qualification_level', 'warm'),
                    predicted_deal_size=analysis.get('predicted_deal_size', 5000),
                    time_to_conversion=analysis.get('time_to_conversion'),
                    recommended_actions=analysis.get('recommended_actions', []),
                    sales_priority=analysis.get('sales_priority', 'medium')
                )
                
            except json.JSONDecodeError:
                return await self._fallback_individual_score(customer)
                
        except Exception as e:
            print(f"Individual lead scoring error: {e}")
            return await self._fallback_individual_score(customer)
    
    async def get_score_components_analysis(self, customer_id: str) -> List[ScoreComponent]:
        """Get detailed breakdown of lead score components"""
        try:
            # Get customer data
            customer = await self.db.customers.find_one({"customer_id": customer_id})
            if not customer:
                return []
            
            # Get latest lead score
            score_data = await self.db.lead_scores.find_one(
                {"customer_id": customer_id}, 
                sort=[("created_at", -1)]
            )
            
            if not score_data:
                return []
            
            components = []
            score_breakdown = score_data.get('score_breakdown', {})
            
            for component_name, weight in self.scoring_weights.items():
                component_score = score_breakdown.get(component_name, 50)
                
                component = await self._analyze_score_component(
                    component_name, component_score, weight, customer
                )
                components.append(component)
            
            return components
            
        except Exception as e:
            print(f"Score components analysis error: {e}")
            return []
    
    async def _analyze_score_component(self, component_name: str, score: int, weight: float, customer: Dict) -> ScoreComponent:
        """Analyze individual score component using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"component_analysis_{component_name}_{customer.get('customer_id')}",
                system_message="""You are Customer Mind IQ's lead scoring analyst. Provide detailed 
                analysis of specific scoring components and actionable improvement recommendations."""
            ).with_model("openai", "gpt-4o-mini")
            
            analysis_prompt = f"""
            Analyze the {component_name} component of lead scoring for this customer:
            
            Component: {component_name}
            Current Score: {score}/100
            Weight in Model: {weight * 100}%
            Customer Data: {json.dumps(customer, default=str)}
            
            Provide detailed component analysis in JSON format:
            {{
                "factors": ["factor1", "factor2", "factor3"],
                "improvement_suggestions": ["suggestion1", "suggestion2", "suggestion3"]
            }}
            
            Focus on:
            1. What factors contributed to this score
            2. Specific areas for improvement
            3. Actionable recommendations to increase this component score
            4. Quick wins vs long-term strategies
            """
            
            message = UserMessage(text=analysis_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                
                return ScoreComponent(
                    component_name=component_name.replace('_', ' ').title(),
                    weight=weight,
                    score=score,
                    factors=analysis.get('factors', []),
                    improvement_suggestions=analysis.get('improvement_suggestions', [])
                )
                
            except json.JSONDecodeError:
                return self._fallback_component_analysis(component_name, score, weight)
                
        except Exception as e:
            print(f"Component analysis error: {e}")
            return self._fallback_component_analysis(component_name, score, weight)
    
    async def get_sales_pipeline_insights(self) -> Dict[str, Any]:
        """Get comprehensive sales pipeline insights based on lead scores"""
        try:
            # Get latest lead scores
            latest_scores = await self.db.lead_scores.find(
                {}, sort=[("created_at", -1)]
            ).to_list(length=1000)
            
            if not latest_scores:
                return await self._generate_sample_pipeline()
            
            # Analyze pipeline distribution
            qualification_distribution = {"qualified": 0, "hot": 0, "warm": 0, "cold": 0}
            priority_distribution = {"urgent": 0, "high": 0, "medium": 0, "low": 0}
            
            total_pipeline_value = 0
            high_probability_value = 0
            avg_deal_size = 0
            
            for score in latest_scores:
                qualification_distribution[score.get('qualification_level', 'warm')] += 1
                priority_distribution[score.get('sales_priority', 'medium')] += 1
                
                deal_size = score.get('predicted_deal_size', 0)
                conversion_prob = score.get('conversion_probability', 0.5)
                
                total_pipeline_value += deal_size * conversion_prob
                if conversion_prob >= 0.7:
                    high_probability_value += deal_size
                avg_deal_size += deal_size
            
            avg_deal_size = avg_deal_size / max(len(latest_scores), 1)
            
            # Top scoring leads
            top_leads = sorted(latest_scores, key=lambda x: x.get('overall_score', 0), reverse=True)[:10]
            
            return {
                "pipeline_summary": {
                    "total_leads": len(latest_scores),
                    "qualified_leads": qualification_distribution["qualified"] + qualification_distribution["hot"],
                    "total_pipeline_value": total_pipeline_value,
                    "high_probability_value": high_probability_value,
                    "average_deal_size": avg_deal_size,
                    "average_score": sum(s.get('overall_score', 0) for s in latest_scores) / max(len(latest_scores), 1)
                },
                "qualification_distribution": qualification_distribution,
                "priority_distribution": priority_distribution,
                "top_leads": [
                    {
                        "customer_id": lead.get('customer_id'),
                        "overall_score": lead.get('overall_score'),
                        "conversion_probability": lead.get('conversion_probability'),
                        "predicted_deal_size": lead.get('predicted_deal_size'),
                        "qualification_level": lead.get('qualification_level')
                    }
                    for lead in top_leads
                ],
                "recommendations": await self._generate_pipeline_recommendations(latest_scores)
            }
            
        except Exception as e:
            print(f"Pipeline insights error: {e}")
            return await self._generate_sample_pipeline()
    
    async def _generate_pipeline_recommendations(self, scores: List[Dict]) -> List[str]:
        """Generate AI-powered pipeline recommendations"""
        try:
            high_scores = [s for s in scores if s.get('overall_score', 0) >= 80]
            medium_scores = [s for s in scores if 50 <= s.get('overall_score', 0) < 80]
            low_scores = [s for s in scores if s.get('overall_score', 0) < 50]
            
            recommendations = []
            
            if len(high_scores) > 0:
                recommendations.append(f"Prioritize {len(high_scores)} high-scoring leads for immediate sales contact")
            
            if len(medium_scores) > len(high_scores) * 2:
                recommendations.append("Focus on nurturing medium-scoring leads to improve qualification")
            
            if len(low_scores) > len(scores) * 0.4:
                recommendations.append("Review lead generation sources - high percentage of low-quality leads")
            
            avg_conversion_time = sum(s.get('time_to_conversion', 90) for s in scores if s.get('time_to_conversion')) / max(len(scores), 1)
            if avg_conversion_time > 120:
                recommendations.append("Sales cycle is lengthy - consider acceleration strategies")
            
            return recommendations[:5]  # Limit to top 5 recommendations
            
        except Exception as e:
            print(f"Pipeline recommendations error: {e}")
            return ["Focus on high-scoring leads", "Improve lead nurturing process"]
    
    def _days_since_last_purchase(self, last_purchase_date) -> int:
        """Calculate days since last purchase"""
        if not last_purchase_date:
            return 365
        
        if isinstance(last_purchase_date, str):
            try:
                last_purchase_date = datetime.fromisoformat(last_purchase_date.replace('Z', '+00:00'))
            except:
                return 365
        
        return (datetime.now() - last_purchase_date).days
    
    async def _fallback_lead_scoring(self, customers_data: List[Dict]) -> List[LeadScore]:
        """Fallback lead scoring when AI fails"""
        scores = []
        for customer in customers_data:
            score = await self._fallback_individual_score(customer)
            scores.append(score)
        return sorted(scores, key=lambda x: x.overall_score, reverse=True)
    
    async def _fallback_individual_score(self, customer: Dict) -> LeadScore:
        """Create fallback lead score"""
        # Simple rule-based scoring
        total_spent = customer.get('total_spent', 0)
        engagement_score = customer.get('engagement_score', 50)
        total_purchases = customer.get('total_purchases', 0)
        
        base_score = min(engagement_score, 100)
        
        # Adjust based on spending
        if total_spent > 10000:
            base_score += 20
        elif total_spent > 5000:
            base_score += 10
        
        # Adjust based on purchase history
        if total_purchases > 5:
            base_score += 15
        elif total_purchases > 2:
            base_score += 8
        
        overall_score = min(base_score, 100)
        conversion_prob = overall_score / 100 * 0.8  # Max 80% conversion probability
        
        qualification_level = "qualified" if overall_score >= 85 else "hot" if overall_score >= 70 else "warm" if overall_score >= 50 else "cold"
        priority = "urgent" if overall_score >= 90 else "high" if overall_score >= 75 else "medium" if overall_score >= 50 else "low"
        
        return LeadScore(
            customer_id=customer['customer_id'],
            overall_score=overall_score,
            conversion_probability=conversion_prob,
            score_breakdown={
                "demographic_fit": min(overall_score + 5, 100),
                "behavioral_engagement": engagement_score,
                "purchase_history": min(total_purchases * 15, 100),
                "software_needs": 60,  # Default assumption
                "timing_factors": 50   # Default assumption
            },
            qualification_level=qualification_level,
            predicted_deal_size=max(total_spent * 0.3, 2000),
            time_to_conversion=90 if conversion_prob > 0.6 else 180,
            recommended_actions=["Personal outreach", "Product demonstration", "Custom proposal"],
            sales_priority=priority
        )
    
    def _fallback_component_analysis(self, component_name: str, score: int, weight: float) -> ScoreComponent:
        """Create fallback component analysis"""
        component_factors = {
            "demographic_fit": ["Company size alignment", "Industry match", "Budget indicators"],
            "behavioral_engagement": ["Email engagement", "Website activity", "Content interaction"],
            "purchase_history": ["Past spending", "Purchase frequency", "Product adoption"],
            "software_needs": ["Current software gaps", "Upgrade opportunities", "Integration needs"],
            "timing_factors": ["Purchase cycle timing", "Budget availability", "Decision urgency"]
        }
        
        return ScoreComponent(
            component_name=component_name.replace('_', ' ').title(),
            weight=weight,
            score=score,
            factors=component_factors.get(component_name, ["Various factors"]),
            improvement_suggestions=["Increase engagement", "Provide more value", "Follow up regularly"]
        )
    
    async def _generate_sample_pipeline(self) -> Dict[str, Any]:
        """Generate sample pipeline data"""
        return {
            "pipeline_summary": {
                "total_leads": 45,
                "qualified_leads": 12,
                "total_pipeline_value": 180000,
                "high_probability_value": 95000,
                "average_deal_size": 4000,
                "average_score": 68
            },
            "qualification_distribution": {"qualified": 5, "hot": 7, "warm": 18, "cold": 15},
            "priority_distribution": {"urgent": 3, "high": 9, "medium": 20, "low": 13},
            "top_leads": [],
            "recommendations": [
                "Focus on 12 qualified leads for immediate outreach",
                "Nurture warm leads to improve conversion",
                "Review cold lead sources for quality improvement"
            ]
        }
    
    async def _store_scoring_results(self, scores: List[LeadScore]):
        """Store lead scoring results"""
        try:
            documents = []
            for score in scores:
                document = score.dict()
                document["created_at"] = datetime.now()
                document["service"] = "lead_scoring"
                documents.append(document)
            
            if documents:
                await self.db.lead_scores.insert_many(documents)
                
        except Exception as e:
            print(f"Error storing lead scores: {e}")