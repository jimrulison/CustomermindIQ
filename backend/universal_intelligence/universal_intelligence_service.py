"""
Customer Mind IQ - Universal Intelligence Service  
AI-powered customer intelligence that works with any business software
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from motor.motor_asyncio import AsyncIOMotorClient
from .universal_models import (
    UniversalCustomerProfile, CustomerInsight, BusinessIntelligence, 
    ActionRecommendation, UniversalAnalytics, UniversalReporting,
    CustomerValue, ChurnRisk, PurchaseIntent
)
from .customer_profile_manager import CustomerProfileManager
import uuid

class UniversalIntelligenceService:
    """
    Universal customer intelligence service that works with any business software.
    Provides AI-powered insights regardless of data source.
    """
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        db_name = os.getenv("DB_NAME", "customer_mind_iq")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        self.profile_manager = CustomerProfileManager()
        
    async def analyze_business_intelligence(self, profiles: List[UniversalCustomerProfile], business_name: str = "Your Business") -> BusinessIntelligence:
        """
        Generate comprehensive business intelligence from unified customer profiles
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"business_intelligence_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's universal business intelligence analyst. 
                Analyze customer data from any business software to provide actionable insights and recommendations."""
            ).with_model("openai", "gpt-4o-mini")
            
            # Prepare analysis data
            analysis_data = await self._prepare_business_analysis_data(profiles)
            
            intelligence_prompt = f"""
            Analyze this business's customer intelligence across all connected platforms:
            
            Business: {business_name}
            Analysis Data: {json.dumps(analysis_data, default=str)}
            
            Provide comprehensive business intelligence in this exact JSON format:
            {{
                "customer_segments": {{
                    "high_value_customers": <count>,
                    "growth_potential": <count>,
                    "at_risk_customers": <count>,
                    "new_customers": <count>
                }},
                "revenue_trend": "<increasing/stable/declining>",
                "top_customer_behaviors": ["behavior1", "behavior2", "behavior3"],
                "common_purchase_patterns": ["pattern1", "pattern2", "pattern3"],
                "seasonal_trends": ["trend1", "trend2"],
                "churn_predictions": ["prediction1", "prediction2", "prediction3"],
                "growth_opportunities": ["opportunity1", "opportunity2", "opportunity3"],
                "recommended_actions": ["action1", "action2", "action3", "action4", "action5"]
            }}
            
            Focus on:
            1. Customer behavior patterns across all platforms
            2. Revenue optimization opportunities  
            3. Churn prevention strategies
            4. Cross-selling and upselling potential
            5. Platform-specific insights
            """
            
            message = UserMessage(text=intelligence_prompt)
            response = await chat.send_message(message)
            
            try:
                ai_analysis = json.loads(response)
                
                # Calculate metrics
                total_customers = len(profiles)
                total_revenue = sum(p.total_spent_all_platforms for p in profiles)
                avg_order_value = total_revenue / sum(p.total_orders_all_platforms for p in profiles) if sum(p.total_orders_all_platforms for p in profiles) > 0 else 0
                
                # Platform revenue breakdown
                platform_revenue = {}
                for profile in profiles:
                    for platform, data in profile.platform_data.items():
                        platform_revenue[platform] = platform_revenue.get(platform, 0) + data.get('total_spent', 0)
                
                # Value distribution
                value_distribution = {
                    CustomerValue.VIP: len([p for p in profiles if p.customer_value_tier == CustomerValue.VIP]),
                    CustomerValue.HIGH: len([p for p in profiles if p.customer_value_tier == CustomerValue.HIGH]),
                    CustomerValue.MEDIUM: len([p for p in profiles if p.customer_value_tier == CustomerValue.MEDIUM]),
                    CustomerValue.LOW: len([p for p in profiles if p.customer_value_tier == CustomerValue.LOW])
                }
                
                # Churn risk distribution
                churn_distribution = {
                    ChurnRisk.CRITICAL: len([p for p in profiles if p.churn_risk_level == ChurnRisk.CRITICAL]),
                    ChurnRisk.HIGH: len([p for p in profiles if p.churn_risk_level == ChurnRisk.HIGH]),
                    ChurnRisk.MEDIUM: len([p for p in profiles if p.churn_risk_level == ChurnRisk.MEDIUM]),
                    ChurnRisk.LOW: len([p for p in profiles if p.churn_risk_level == ChurnRisk.LOW])
                }
                
                # Calculate additional metrics
                retention_rate = self._calculate_retention_rate(profiles)
                customer_lifetime_value = self._calculate_clv(profiles)
                
                business_intelligence = BusinessIntelligence(
                    analysis_id=str(uuid.uuid4()),
                    business_name=business_name,
                    platforms_analyzed=list(set().union(*[p.platforms_active for p in profiles])),
                    total_customers=total_customers,
                    analysis_period_days=90,
                    customer_segments=ai_analysis.get('customer_segments', {}),
                    value_distribution=value_distribution,
                    churn_risk_distribution=churn_distribution,
                    total_revenue=total_revenue,
                    average_order_value=avg_order_value,
                    revenue_by_platform=platform_revenue,
                    revenue_trend=ai_analysis.get('revenue_trend', 'stable'),
                    top_customer_behaviors=ai_analysis.get('top_customer_behaviors', []),
                    common_purchase_patterns=ai_analysis.get('common_purchase_patterns', []),
                    seasonal_trends=ai_analysis.get('seasonal_trends', []),
                    churn_predictions=ai_analysis.get('churn_predictions', []),
                    growth_opportunities=ai_analysis.get('growth_opportunities', []),
                    recommended_actions=ai_analysis.get('recommended_actions', []),
                    customer_lifetime_value=customer_lifetime_value,
                    retention_rate=retention_rate,
                    acquisition_cost_estimate=avg_order_value * 0.3  # Estimate
                )
                
                # Store analysis
                await self._store_business_intelligence(business_intelligence)
                
                return business_intelligence
                
            except json.JSONDecodeError:
                return await self._fallback_business_intelligence(profiles, business_name)
                
        except Exception as e:
            print(f"Business intelligence analysis error: {e}")
            return await self._fallback_business_intelligence(profiles, business_name)
    
    async def generate_customer_insights(self, profile: UniversalCustomerProfile) -> List[CustomerInsight]:
        """Generate AI-powered insights for individual customer"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"customer_insights_{profile.customer_id}",
                system_message="""You are Customer Mind IQ's customer insight specialist. 
                Analyze individual customer profiles to generate actionable, specific insights."""
            ).with_model("openai", "gpt-4o-mini")
            
            insight_prompt = f"""
            Generate specific insights for this customer:
            
            Customer Profile: {json.dumps(profile.dict(), default=str)}
            
            Generate 3-5 customer insights in this JSON format:
            {{
                "insights": [
                    {{
                        "insight_type": "<behavioral/predictive/prescriptive>",
                        "title": "<short_insight_title>",
                        "description": "<detailed_insight_description>",
                        "confidence_score": <0.0-1.0>,
                        "priority": "<low/medium/high/urgent>",
                        "recommended_actions": ["action1", "action2"],
                        "expected_impact": "<expected_business_impact>"
                    }}
                ]
            }}
            
            Focus on actionable insights that can drive revenue, prevent churn, or improve engagement.
            """
            
            message = UserMessage(text=insight_prompt)
            response = await chat.send_message(message)
            
            try:
                ai_insights = json.loads(response)
                insights = []
                
                for insight_data in ai_insights.get('insights', []):
                    insight = CustomerInsight(
                        insight_id=str(uuid.uuid4()),
                        customer_id=profile.customer_id,
                        insight_type=insight_data.get('insight_type', 'behavioral'),
                        title=insight_data.get('title', 'Customer Insight'),
                        description=insight_data.get('description', ''),
                        confidence_score=insight_data.get('confidence_score', 0.7),
                        priority=insight_data.get('priority', 'medium'),
                        recommended_actions=insight_data.get('recommended_actions', []),
                        expected_impact=insight_data.get('expected_impact')
                    )
                    insights.append(insight)
                
                return insights
                
            except json.JSONDecodeError:
                return await self._fallback_customer_insights(profile)
                
        except Exception as e:
            print(f"Customer insights error: {e}")
            return await self._fallback_customer_insights(profile)
    
    async def generate_action_recommendations(self, profiles: List[UniversalCustomerProfile]) -> List[ActionRecommendation]:
        """Generate AI-powered action recommendations"""
        try:
            high_priority_customers = [
                p for p in profiles 
                if p.churn_risk_level in [ChurnRisk.HIGH, ChurnRisk.CRITICAL] or 
                   p.purchase_intent in [PurchaseIntent.HOT, PurchaseIntent.READY]
            ]
            
            recommendations = []
            
            # Generate recommendations for high-priority customers
            for profile in high_priority_customers[:10]:  # Limit to top 10
                customer_recommendations = await self._generate_customer_specific_actions(profile)
                recommendations.extend(customer_recommendations)
            
            # Generate business-wide recommendations
            business_recommendations = await self._generate_business_wide_actions(profiles)
            recommendations.extend(business_recommendations)
            
            # Sort by priority and expected impact
            recommendations.sort(key=lambda x: (x.success_probability * x.estimated_revenue_impact), reverse=True)
            
            return recommendations[:20]  # Return top 20 recommendations
            
        except Exception as e:
            print(f"Action recommendations error: {e}")
            return []
    
    async def _generate_customer_specific_actions(self, profile: UniversalCustomerProfile) -> List[ActionRecommendation]:
        """Generate actions for specific customer"""
        actions = []
        
        # Churn prevention actions
        if profile.churn_risk_level in [ChurnRisk.HIGH, ChurnRisk.CRITICAL]:
            action = ActionRecommendation(
                action_id=str(uuid.uuid4()),
                customer_id=profile.customer_id,
                action_type="retention",
                priority="urgent" if profile.churn_risk_level == ChurnRisk.CRITICAL else "high",
                title=f"Urgent Retention Campaign for {profile.name or profile.email}",
                description=f"Customer at {profile.churn_risk_level.value} churn risk. Immediate intervention needed.",
                expected_outcome="Prevent customer churn and maintain revenue",
                success_probability=0.7,
                estimated_revenue_impact=profile.total_spent_all_platforms * 0.8,
                trigger_conditions=["High churn risk", "Declining engagement"]
            )
            actions.append(action)
        
        # Upsell actions
        if profile.purchase_intent in [PurchaseIntent.HOT, PurchaseIntent.READY] and profile.customer_value_tier in [CustomerValue.HIGH, CustomerValue.VIP]:
            action = ActionRecommendation(
                action_id=str(uuid.uuid4()),
                customer_id=profile.customer_id,
                action_type="upgrade",
                priority="high",
                title=f"Premium Upsell Opportunity for {profile.name or profile.email}",
                description=f"Customer shows {profile.purchase_intent.value} purchase intent and is {profile.customer_value_tier.value} value.",
                expected_outcome="Increase customer lifetime value",
                success_probability=0.8,
                estimated_revenue_impact=profile.total_spent_all_platforms * 0.3,
                trigger_conditions=["High purchase intent", "Value customer tier"]
            )
            actions.append(action)
        
        return actions
    
    async def _generate_business_wide_actions(self, profiles: List[UniversalCustomerProfile]) -> List[ActionRecommendation]:
        """Generate business-wide actions"""
        actions = []
        
        # Identify customers at critical churn risk
        critical_churn_customers = [p for p in profiles if p.churn_risk_level == ChurnRisk.CRITICAL]
        if len(critical_churn_customers) > 5:
            action = ActionRecommendation(
                action_id=str(uuid.uuid4()),
                action_type="email",
                priority="urgent",
                title="Mass Retention Campaign",
                description=f"Launch retention campaign for {len(critical_churn_customers)} customers at critical churn risk",
                expected_outcome="Reduce overall churn rate by 30%",
                success_probability=0.6,
                estimated_revenue_impact=sum(p.total_spent_all_platforms for p in critical_churn_customers) * 0.5,
                trigger_conditions=["Multiple customers at critical churn risk"]
            )
            actions.append(action)
        
        # Identify growth opportunities
        growth_customers = [p for p in profiles if p.customer_value_tier == CustomerValue.LOW and p.purchase_intent in [PurchaseIntent.WARM, PurchaseIntent.HOT]]
        if len(growth_customers) > 10:
            action = ActionRecommendation(
                action_id=str(uuid.uuid4()),
                action_type="email",
                priority="medium",
                title="Growth Opportunity Campaign",
                description=f"Target {len(growth_customers)} customers with growth potential for upselling",
                expected_outcome="Increase average customer value by 25%",
                success_probability=0.5,
                estimated_revenue_impact=len(growth_customers) * 500,  # Estimated increase per customer
                trigger_conditions=["Multiple low-value customers with purchase intent"]
            )
            actions.append(action)
        
        return actions
    
    async def get_universal_dashboard_data(self, profiles: List[UniversalCustomerProfile]) -> Dict[str, Any]:
        """Get comprehensive dashboard data for any business"""
        try:
            # Calculate key metrics
            total_customers = len(profiles)
            total_revenue = sum(p.total_spent_all_platforms for p in profiles)
            avg_customer_value = total_revenue / total_customers if total_customers > 0 else 0
            
            # Platform distribution
            platform_stats = {}
            for profile in profiles:
                for platform in profile.platforms_active:
                    platform_stats[platform] = platform_stats.get(platform, 0) + 1
            
            # Risk distribution
            risk_distribution = {
                'critical': len([p for p in profiles if p.churn_risk_level == ChurnRisk.CRITICAL]),
                'high': len([p for p in profiles if p.churn_risk_level == ChurnRisk.HIGH]), 
                'medium': len([p for p in profiles if p.churn_risk_level == ChurnRisk.MEDIUM]),
                'low': len([p for p in profiles if p.churn_risk_level == ChurnRisk.LOW])
            }
            
            # Value distribution
            value_distribution = {
                'vip': len([p for p in profiles if p.customer_value_tier == CustomerValue.VIP]),
                'high': len([p for p in profiles if p.customer_value_tier == CustomerValue.HIGH]),
                'medium': len([p for p in profiles if p.customer_value_tier == CustomerValue.MEDIUM]),
                'low': len([p for p in profiles if p.customer_value_tier == CustomerValue.LOW])
            }
            
            # Recent activity
            recent_customers = [p for p in profiles if p.last_activity_date and p.last_activity_date > datetime.now() - timedelta(days=30)]
            
            # Top insights
            top_insights = [
                f"{risk_distribution['critical']} customers at critical churn risk",
                f"{value_distribution['vip']} VIP customers generating premium revenue",
                f"{len(recent_customers)} customers active in last 30 days",
                f"Average customer value: ${avg_customer_value:.2f}"
            ]
            
            return {
                "overview": {
                    "total_customers": total_customers,
                    "total_revenue": total_revenue,
                    "average_customer_value": avg_customer_value,
                    "platforms_connected": len(platform_stats),
                    "active_customers_30d": len(recent_customers)
                },
                "platform_distribution": platform_stats,
                "risk_distribution": risk_distribution,
                "value_distribution": value_distribution,
                "top_insights": top_insights,
                "urgent_actions": risk_distribution['critical'] + risk_distribution['high'],
                "growth_opportunities": value_distribution['low'] + value_distribution['medium']
            }
            
        except Exception as e:
            print(f"Dashboard data error: {e}")
            return self._fallback_dashboard_data()
    
    def _calculate_retention_rate(self, profiles: List[UniversalCustomerProfile]) -> float:
        """Calculate customer retention rate"""
        if not profiles:
            return 0.0
        
        # Calculate based on customers who were active 3+ months ago and are still active
        three_months_ago = datetime.now() - timedelta(days=90)
        six_months_ago = datetime.now() - timedelta(days=180)
        
        old_customers = [
            p for p in profiles 
            if p.first_seen_date and p.first_seen_date < six_months_ago
        ]
        
        if not old_customers:
            return 1.0  # No historical data, assume 100%
        
        retained_customers = [
            p for p in old_customers
            if p.last_activity_date and p.last_activity_date > three_months_ago
        ]
        
        return len(retained_customers) / len(old_customers)
    
    def _calculate_clv(self, profiles: List[UniversalCustomerProfile]) -> float:
        """Calculate average customer lifetime value"""
        if not profiles:
            return 0.0
        
        total_clv = 0.0
        for profile in profiles:
            # Simple CLV calculation: (total spent / tenure in months) * estimated lifetime
            if profile.first_seen_date:
                tenure_days = (datetime.now() - profile.first_seen_date).days
                tenure_months = max(tenure_days / 30, 1)  # At least 1 month
                monthly_value = profile.total_spent_all_platforms / tenure_months
                estimated_lifetime_months = 24  # Assume 2 year average lifetime
                clv = monthly_value * estimated_lifetime_months
            else:
                clv = profile.total_spent_all_platforms * 2  # Simple multiplier
            
            total_clv += clv
        
        return total_clv / len(profiles)
    
    async def _prepare_business_analysis_data(self, profiles: List[UniversalCustomerProfile]) -> Dict[str, Any]:
        """Prepare data for business intelligence analysis"""
        return {
            "customer_count": len(profiles),
            "total_revenue": sum(p.total_spent_all_platforms for p in profiles),
            "platforms": list(set().union(*[p.platforms_active for p in profiles])),
            "value_tiers": {tier.value: len([p for p in profiles if p.customer_value_tier == tier]) for tier in CustomerValue},
            "churn_risks": {risk.value: len([p for p in profiles if p.churn_risk_level == risk]) for risk in ChurnRisk},
            "purchase_intents": {intent.value: len([p for p in profiles if p.purchase_intent == intent]) for intent in PurchaseIntent},
            "avg_engagement": sum(p.engagement_score for p in profiles) / len(profiles) if profiles else 0,
            "avg_loyalty": sum(p.loyalty_score for p in profiles) / len(profiles) if profiles else 0,
            "common_patterns": list(set().union(*[p.behavioral_patterns for p in profiles]))[:10]
        }
    
    async def _fallback_business_intelligence(self, profiles: List[UniversalCustomerProfile], business_name: str) -> BusinessIntelligence:
        """Fallback business intelligence when AI fails"""
        total_customers = len(profiles)
        total_revenue = sum(p.total_spent_all_platforms for p in profiles)
        
        return BusinessIntelligence(
            analysis_id=str(uuid.uuid4()),
            business_name=business_name,
            platforms_analyzed=list(set().union(*[p.platforms_active for p in profiles])) if profiles else [],
            total_customers=total_customers,
            analysis_period_days=90,
            customer_segments={
                "high_value_customers": len([p for p in profiles if p.customer_value_tier in [CustomerValue.HIGH, CustomerValue.VIP]]),
                "growth_potential": len([p for p in profiles if p.customer_value_tier == CustomerValue.MEDIUM]),
                "at_risk_customers": len([p for p in profiles if p.churn_risk_level in [ChurnRisk.HIGH, ChurnRisk.CRITICAL]]),
                "new_customers": len([p for p in profiles if p.first_seen_date and p.first_seen_date > datetime.now() - timedelta(days=30)])
            },
            value_distribution={tier: len([p for p in profiles if p.customer_value_tier == tier]) for tier in CustomerValue},
            churn_risk_distribution={risk: len([p for p in profiles if p.churn_risk_level == risk]) for risk in ChurnRisk},
            total_revenue=total_revenue,
            average_order_value=total_revenue / sum(p.total_orders_all_platforms for p in profiles) if sum(p.total_orders_all_platforms for p in profiles) > 0 else 0,
            revenue_by_platform={},
            revenue_trend="stable",
            top_customer_behaviors=["Regular purchaser", "Multi-platform user", "High engagement"],
            common_purchase_patterns=["Monthly recurring", "Seasonal purchases", "Bulk buying"],
            seasonal_trends=["Q4 increase", "Summer dip"],
            churn_predictions=["Customer engagement declining", "Payment issues increasing"],
            growth_opportunities=["Upsell opportunities", "Cross-platform expansion", "Feature adoption"],
            recommended_actions=["Focus on retention", "Implement loyalty program", "Improve onboarding"],
            customer_lifetime_value=self._calculate_clv(profiles),
            retention_rate=self._calculate_retention_rate(profiles),
            acquisition_cost_estimate=100.0
        )
    
    async def _fallback_customer_insights(self, profile: UniversalCustomerProfile) -> List[CustomerInsight]:
        """Fallback customer insights when AI fails"""
        insights = []
        
        # Churn risk insight
        if profile.churn_risk_level in [ChurnRisk.HIGH, ChurnRisk.CRITICAL]:
            insight = CustomerInsight(
                insight_id=str(uuid.uuid4()),
                customer_id=profile.customer_id,
                insight_type="predictive",
                title="Churn Risk Alert",
                description=f"Customer shows {profile.churn_risk_level.value} churn risk based on activity patterns",
                confidence_score=0.8,
                priority="urgent" if profile.churn_risk_level == ChurnRisk.CRITICAL else "high",
                recommended_actions=["Personal outreach", "Retention offer", "Account review"],
                expected_impact="Prevent customer churn and revenue loss"
            )
            insights.append(insight)
        
        # Value tier insight
        if profile.customer_value_tier in [CustomerValue.HIGH, CustomerValue.VIP]:
            insight = CustomerInsight(
                insight_id=str(uuid.uuid4()),
                customer_id=profile.customer_id,
                insight_type="behavioral",
                title="High-Value Customer",
                description=f"Customer is in {profile.customer_value_tier.value} value tier with strong purchase history",
                confidence_score=0.9,
                priority="medium",
                recommended_actions=["VIP treatment", "Exclusive offers", "Account management"],
                expected_impact="Increase customer lifetime value and loyalty"
            )
            insights.append(insight)
        
        return insights
    
    def _fallback_dashboard_data(self) -> Dict[str, Any]:
        """Fallback dashboard data"""
        return {
            "overview": {
                "total_customers": 0,
                "total_revenue": 0.0,
                "average_customer_value": 0.0,
                "platforms_connected": 0,
                "active_customers_30d": 0
            },
            "platform_distribution": {},
            "risk_distribution": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "value_distribution": {"vip": 0, "high": 0, "medium": 0, "low": 0},
            "top_insights": ["No data available"],
            "urgent_actions": 0,
            "growth_opportunities": 0
        }
    
    async def _store_business_intelligence(self, intelligence: BusinessIntelligence):
        """Store business intelligence analysis"""
        try:
            await self.db.business_intelligence.insert_one(intelligence.dict())
            print(f"✅ Stored business intelligence analysis: {intelligence.analysis_id}")
        except Exception as e:
            print(f"❌ Error storing business intelligence: {e}")