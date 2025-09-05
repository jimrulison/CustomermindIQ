"""
Customer Mind IQ - Churn Prevention Microservice
AI-powered customer churn prediction and prevention strategies
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

class ChurnRiskProfile(BaseModel):
    customer_id: str
    churn_probability: float  # 0-1
    risk_level: str  # low, medium, high, critical
    risk_factors: List[str]
    engagement_trends: Dict[str, Any]
    intervention_recommendations: List[str]
    retention_strategies: List[str]
    time_to_churn_estimate: Optional[int]  # days
    value_at_risk: float  # potential revenue loss

class RetentionCampaign(BaseModel):
    campaign_id: str
    customer_ids: List[str]
    risk_level: str
    intervention_type: str
    message: str
    incentives: List[str]
    success_probability: float
    expected_retention_lift: float

class ChurnPreventionService:
    """Customer Mind IQ Churn Prevention Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[os.environ.get('DB_NAME', 'customer_mind_iq')]
        
    async def analyze_churn_risk(self, customers_data: List[Dict]) -> List[ChurnRiskProfile]:
        """Analyze churn risk for all customers using AI"""
        try:
            churn_profiles = []
            
            for customer in customers_data:
                risk_profile = await self._calculate_individual_churn_risk(customer)
                churn_profiles.append(risk_profile)
            
            # Store results in database
            await self._store_churn_analysis(churn_profiles)
            
            return churn_profiles
            
        except Exception as e:
            print(f"Churn risk analysis error: {e}")
            return await self._fallback_churn_analysis(customers_data)
    
    async def _calculate_individual_churn_risk(self, customer: Dict) -> ChurnRiskProfile:
        """Calculate churn risk for individual customer using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"churn_analysis_{customer.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ's churn prevention specialist. Analyze customer data 
                to predict churn probability and recommend retention strategies. Focus on software customer behavior patterns."""
            ).with_model("openai", "gpt-4o-mini")
            
            # Calculate basic risk indicators
            days_since_purchase = self._days_since_last_purchase(customer.get('last_purchase_date'))
            engagement_score = customer.get('engagement_score', 50)
            total_spent = customer.get('total_spent', 0)
            purchase_frequency = customer.get('total_purchases', 0)
            
            churn_prompt = f"""
            Analyze this customer's churn risk using Customer Mind IQ advanced algorithms:
            
            Customer Profile:
            - ID: {customer.get('customer_id')}
            - Name: {customer.get('name')}
            - Total Spent: ${total_spent}
            - Total Purchases: {purchase_frequency}
            - Days Since Last Purchase: {days_since_purchase}
            - Engagement Score: {engagement_score}/100
            - Software Owned: {customer.get('software_owned', [])}
            - Lifecycle Stage: {customer.get('lifecycle_stage', 'unknown')}
            
            Provide comprehensive churn analysis in this exact JSON format:
            {{
                "churn_probability": <0.0-1.0>,
                "risk_level": "<low/medium/high/critical>",
                "risk_factors": ["factor1", "factor2", "factor3"],
                "engagement_trends": {{
                    "trend_direction": "<declining/stable/improving>",
                    "engagement_velocity": <-1.0 to 1.0>,
                    "key_behaviors": ["behavior1", "behavior2"]
                }},
                "intervention_recommendations": ["recommendation1", "recommendation2"],
                "retention_strategies": ["strategy1", "strategy2", "strategy3"],
                "time_to_churn_estimate": <days or null>,
                "value_at_risk": <estimated_revenue_loss>
            }}
            
            Consider:
            1. Purchase recency and frequency patterns
            2. Engagement score trends
            3. Software usage patterns
            4. Customer lifecycle position
            5. Competitive threats and market factors
            """
            
            message = UserMessage(text=churn_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                
                return ChurnRiskProfile(
                    customer_id=customer['customer_id'],
                    churn_probability=analysis.get('churn_probability', 0.3),
                    risk_level=analysis.get('risk_level', 'medium'),
                    risk_factors=analysis.get('risk_factors', []),
                    engagement_trends=analysis.get('engagement_trends', {}),
                    intervention_recommendations=analysis.get('intervention_recommendations', []),
                    retention_strategies=analysis.get('retention_strategies', []),
                    time_to_churn_estimate=analysis.get('time_to_churn_estimate'),
                    value_at_risk=analysis.get('value_at_risk', total_spent * 0.3)
                )
                
            except json.JSONDecodeError:
                return await self._fallback_risk_profile(customer)
                
        except Exception as e:
            print(f"Individual churn analysis error: {e}")
            return await self._fallback_risk_profile(customer)
    
    async def generate_retention_campaigns(self, high_risk_customers: List[ChurnRiskProfile]) -> List[RetentionCampaign]:
        """Generate targeted retention campaigns for high-risk customers"""
        try:
            campaigns = []
            
            # Group customers by risk level and characteristics
            risk_groups = self._group_customers_by_risk(high_risk_customers)
            
            for risk_level, customers in risk_groups.items():
                if len(customers) > 0:
                    campaign = await self._create_retention_campaign(risk_level, customers)
                    campaigns.append(campaign)
            
            return campaigns
            
        except Exception as e:
            print(f"Retention campaign generation error: {e}")
            return []
    
    async def _create_retention_campaign(self, risk_level: str, customers: List[ChurnRiskProfile]) -> RetentionCampaign:
        """Create targeted retention campaign for customer group"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"retention_campaign_{risk_level}_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's retention campaign specialist. Create compelling 
                retention campaigns that address specific churn risks and motivate customers to stay engaged."""
            ).with_model("openai", "gpt-4o-mini")
            
            # Aggregate customer data for campaign creation
            customer_data = {
                "count": len(customers),
                "avg_value_at_risk": sum(c.value_at_risk for c in customers) / len(customers),
                "common_risk_factors": self._find_common_risk_factors(customers),
                "avg_churn_probability": sum(c.churn_probability for c in customers) / len(customers)
            }
            
            campaign_prompt = f"""
            Create a retention campaign for {risk_level} churn risk customers:
            
            Customer Group Data:
            - Customer Count: {customer_data['count']}
            - Average Value at Risk: ${customer_data['avg_value_at_risk']:.2f}
            - Average Churn Probability: {customer_data['avg_churn_probability']:.2f}
            - Common Risk Factors: {customer_data['common_risk_factors']}
            
            Create retention campaign in this JSON format:
            {{
                "intervention_type": "<email/phone/special_offer/loyalty_program>",
                "message": "<compelling retention message>",
                "incentives": ["incentive1", "incentive2", "incentive3"],
                "success_probability": <0.0-1.0>,
                "expected_retention_lift": <0.0-1.0>
            }}
            
            Make the campaign:
            1. Specific to the risk level and common factors
            2. Include compelling value propositions
            3. Address the main reasons for potential churn
            4. Offer appropriate incentives for the customer value
            5. Professional but urgent tone
            """
            
            message = UserMessage(text=campaign_prompt)
            response = await chat.send_message(message)
            
            try:
                campaign_data = json.loads(response)
                
                return RetentionCampaign(
                    campaign_id=str(uuid.uuid4()),
                    customer_ids=[c.customer_id for c in customers],
                    risk_level=risk_level,
                    intervention_type=campaign_data.get('intervention_type', 'email'),
                    message=campaign_data.get('message', 'Stay with us!'),
                    incentives=campaign_data.get('incentives', []),
                    success_probability=campaign_data.get('success_probability', 0.6),
                    expected_retention_lift=campaign_data.get('expected_retention_lift', 0.3)
                )
                
            except json.JSONDecodeError:
                return self._fallback_retention_campaign(risk_level, customers)
                
        except Exception as e:
            print(f"Retention campaign creation error: {e}")
            return self._fallback_retention_campaign(risk_level, customers)
    
    def _group_customers_by_risk(self, customers: List[ChurnRiskProfile]) -> Dict[str, List[ChurnRiskProfile]]:
        """Group customers by risk level"""
        groups = {"critical": [], "high": [], "medium": []}
        
        for customer in customers:
            if customer.churn_probability >= 0.8:
                groups["critical"].append(customer)
            elif customer.churn_probability >= 0.6:
                groups["high"].append(customer)
            elif customer.churn_probability >= 0.4:
                groups["medium"].append(customer)
                
        return groups
    
    def _find_common_risk_factors(self, customers: List[ChurnRiskProfile]) -> List[str]:
        """Find common risk factors among customers"""
        factor_counts = {}
        for customer in customers:
            for factor in customer.risk_factors:
                factor_counts[factor] = factor_counts.get(factor, 0) + 1
        
        # Return factors present in at least 30% of customers
        threshold = len(customers) * 0.3
        return [factor for factor, count in factor_counts.items() if count >= threshold]
    
    async def get_churn_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive churn prevention dashboard data"""
        try:
            # Get latest churn analysis
            latest_analysis = await self.db.churn_analysis.find_one(
                {}, sort=[("created_at", -1)]
            )
            
            if not latest_analysis:
                return await self._generate_sample_dashboard()
            
            profiles = latest_analysis.get('profiles', [])
            
            # Calculate dashboard metrics
            total_customers = len(profiles)
            high_risk_count = len([p for p in profiles if p.get('churn_probability', 0) >= 0.6])
            medium_risk_count = len([p for p in profiles if 0.4 <= p.get('churn_probability', 0) < 0.6])
            low_risk_count = total_customers - high_risk_count - medium_risk_count
            
            total_value_at_risk = sum(p.get('value_at_risk', 0) for p in profiles if p.get('churn_probability', 0) >= 0.6)
            
            # Most common risk factors
            all_risk_factors = []
            for p in profiles:
                all_risk_factors.extend(p.get('risk_factors', []))
            
            factor_counts = {}
            for factor in all_risk_factors:
                factor_counts[factor] = factor_counts.get(factor, 0) + 1
            
            top_risk_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "summary": {
                    "total_customers": total_customers,
                    "high_risk_customers": high_risk_count,
                    "medium_risk_customers": medium_risk_count,
                    "low_risk_customers": low_risk_count,
                    "total_value_at_risk": total_value_at_risk,
                    "avg_churn_probability": sum(p.get('churn_probability', 0) for p in profiles) / max(total_customers, 1)
                },
                "risk_distribution": {
                    "critical_risk": len([p for p in profiles if p.get('churn_probability', 0) >= 0.8]),
                    "high_risk": len([p for p in profiles if 0.6 <= p.get('churn_probability', 0) < 0.8]),
                    "medium_risk": medium_risk_count,
                    "low_risk": low_risk_count
                },
                "top_risk_factors": [{"factor": factor, "count": count} for factor, count in top_risk_factors],
                "retention_opportunities": total_value_at_risk * 0.7  # Estimated recoverable value
            }
            
        except Exception as e:
            print(f"Churn dashboard error: {e}")
            return await self._generate_sample_dashboard()
    
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
    
    async def _fallback_churn_analysis(self, customers_data: List[Dict]) -> List[ChurnRiskProfile]:
        """Fallback churn analysis when AI fails"""
        profiles = []
        for customer in customers_data:
            risk_profile = await self._fallback_risk_profile(customer)
            profiles.append(risk_profile)
        return profiles
    
    async def _fallback_risk_profile(self, customer: Dict) -> ChurnRiskProfile:
        """Create fallback risk profile"""
        days_since_purchase = self._days_since_last_purchase(customer.get('last_purchase_date'))
        engagement_score = customer.get('engagement_score', 50)
        
        # Simple rule-based churn probability
        churn_prob = 0.2
        if days_since_purchase > 180:
            churn_prob += 0.3
        if engagement_score < 40:
            churn_prob += 0.3
        if customer.get('total_purchases', 0) < 2:
            churn_prob += 0.2
            
        churn_prob = min(churn_prob, 0.95)
        
        risk_level = "critical" if churn_prob >= 0.8 else "high" if churn_prob >= 0.6 else "medium" if churn_prob >= 0.4 else "low"
        
        return ChurnRiskProfile(
            customer_id=customer['customer_id'],
            churn_probability=churn_prob,
            risk_level=risk_level,
            risk_factors=["Long time since purchase", "Low engagement"] if churn_prob > 0.5 else ["Normal behavior"],
            engagement_trends={"trend_direction": "declining" if engagement_score < 50 else "stable"},
            intervention_recommendations=["Personal outreach", "Special offer"],
            retention_strategies=["Loyalty program", "Product demonstration"],
            time_to_churn_estimate=90 if churn_prob > 0.6 else None,
            value_at_risk=customer.get('total_spent', 0) * churn_prob
        )
    
    def _fallback_retention_campaign(self, risk_level: str, customers: List[ChurnRiskProfile]) -> RetentionCampaign:
        """Create fallback retention campaign"""
        return RetentionCampaign(
            campaign_id=str(uuid.uuid4()),
            customer_ids=[c.customer_id for c in customers],
            risk_level=risk_level,
            intervention_type="email",
            message=f"We value your business and want to ensure you're getting the most from our software solutions.",
            incentives=["20% discount on next purchase", "Free consultation", "Priority support"],
            success_probability=0.6,
            expected_retention_lift=0.4
        )
    
    async def _generate_sample_dashboard(self) -> Dict[str, Any]:
        """Generate sample dashboard data"""
        return {
            "summary": {
                "total_customers": 50,
                "high_risk_customers": 8,
                "medium_risk_customers": 15,
                "low_risk_customers": 27,
                "total_value_at_risk": 25000,
                "avg_churn_probability": 0.35
            },
            "risk_distribution": {
                "critical_risk": 3,
                "high_risk": 5,
                "medium_risk": 15,
                "low_risk": 27
            },
            "top_risk_factors": [
                {"factor": "Long time since purchase", "count": 12},
                {"factor": "Low engagement score", "count": 8},
                {"factor": "Limited software usage", "count": 6}
            ],
            "retention_opportunities": 17500
        }
    
    async def _store_churn_analysis(self, profiles: List[ChurnRiskProfile]):
        """Store churn analysis results"""
        try:
            document = {
                "analysis_id": str(uuid.uuid4()),
                "created_at": datetime.now(),
                "profiles": [profile.dict() for profile in profiles],
                "service": "churn_prevention"
            }
            
            await self.db.churn_analysis.insert_one(document)
            
        except Exception as e:
            print(f"Error storing churn analysis: {e}")