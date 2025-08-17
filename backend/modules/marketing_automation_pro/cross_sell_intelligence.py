"""
Customer Mind IQ - Cross-Sell Intelligence Microservice
AI-powered cross-selling and upselling opportunity identification
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from enum import Enum
import uuid

class OpportunityType(str, Enum):
    CROSS_SELL = "cross_sell"
    UPSELL = "upsell"
    BUNDLE = "bundle"
    RENEWAL = "renewal"

class OpportunityPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ProductRecommendation(BaseModel):
    product_id: str
    product_name: str
    category: str
    price: float
    relevance_score: float
    reasoning: str
    expected_revenue: float

class CrossSellOpportunity(BaseModel):
    opportunity_id: str
    customer_id: str
    opportunity_type: OpportunityType
    priority: OpportunityPriority
    products_owned: List[str]
    recommended_products: List[ProductRecommendation]
    total_potential_revenue: float
    conversion_probability: float
    best_contact_time: str
    personalized_pitch: str
    objection_handlers: List[str]
    created_at: datetime = datetime.now()
    expires_at: Optional[datetime] = None

class CrossSellIntelligenceService:
    """Customer Mind IQ Cross-Sell Intelligence Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq
        
    async def identify_cross_sell_opportunities(self, customers_data: List[Dict]) -> List[CrossSellOpportunity]:
        """Identify cross-sell and upsell opportunities for all customers"""
        try:
            opportunities = []
            
            for customer in customers_data:
                customer_opportunities = await self._analyze_customer_opportunities(customer)
                opportunities.extend(customer_opportunities)
            
            # Sort by priority and potential revenue
            opportunities.sort(key=lambda x: (x.priority == OpportunityPriority.URGENT, x.total_potential_revenue), reverse=True)
            
            # Store opportunities
            await self._store_opportunities(opportunities)
            
            return opportunities
            
        except Exception as e:
            print(f"Cross-sell opportunity identification error: {e}")
            return await self._fallback_opportunities(customers_data)
    
    async def _analyze_customer_opportunities(self, customer: Dict) -> List[CrossSellOpportunity]:
        """Analyze cross-sell opportunities for individual customer using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"cross_sell_analysis_{customer.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ's cross-sell intelligence specialist. 
                Analyze customer profiles to identify high-potential cross-sell and upsell opportunities."""
            ).with_model("openai", "gpt-4o-mini")
            
            # Get available products for recommendations
            available_products = await self._get_available_products()
            
            opportunity_prompt = f"""
            Analyze cross-sell opportunities using Customer Mind IQ advanced algorithms:
            
            Customer Profile: {json.dumps(customer, default=str)}
            Available Products: {json.dumps(available_products[:10], default=str)}  # Limit for prompt size
            
            Identify cross-sell opportunities in this exact JSON format:
            {{
                "opportunities": [
                    {{
                        "opportunity_type": "<cross_sell/upsell/bundle/renewal>",
                        "priority": "<low/medium/high/urgent>",
                        "recommended_products": [
                            {{
                                "product_id": "<product_id>",
                                "product_name": "<product_name>",  
                                "category": "<category>",
                                "price": <price>,
                                "relevance_score": <0.0-1.0>,
                                "reasoning": "<why_this_product_fits>",
                                "expected_revenue": <revenue_potential>
                            }}
                        ],
                        "conversion_probability": <0.0-1.0>,
                        "best_contact_time": "<morning/afternoon/evening>",
                        "personalized_pitch": "<tailored_sales_pitch>", 
                        "objection_handlers": ["objection_response1", "objection_response2"]
                    }}
                ]
            }}
            
            Focus on:
            1. Customer's current product portfolio and usage patterns
            2. Natural product progression and complementary items
            3. Revenue maximization while maintaining customer satisfaction
            4. Realistic conversion probabilities based on customer behavior
            5. Personalized messaging that resonates with this customer
            """
            
            message = UserMessage(text=opportunity_prompt)
            response = await chat.send_message(message)
            
            try:
                analysis = json.loads(response)
                opportunities = []
                
                for opp_data in analysis.get('opportunities', []):
                    # Create product recommendations
                    product_recommendations = []
                    for prod_data in opp_data.get('recommended_products', []):
                        recommendation = ProductRecommendation(
                            product_id=prod_data.get('product_id', str(uuid.uuid4())),
                            product_name=prod_data.get('product_name', 'Product'),
                            category=prod_data.get('category', 'General'),
                            price=prod_data.get('price', 100.0),
                            relevance_score=prod_data.get('relevance_score', 0.7),
                            reasoning=prod_data.get('reasoning', 'Good fit for customer'),
                            expected_revenue=prod_data.get('expected_revenue', 100.0)
                        )
                        product_recommendations.append(recommendation)
                    
                    # Calculate total potential revenue
                    total_revenue = sum(rec.expected_revenue for rec in product_recommendations)
                    
                    # Set expiration date
                    expires_at = datetime.now() + timedelta(days=30)
                    
                    opportunity = CrossSellOpportunity(
                        opportunity_id=str(uuid.uuid4()),
                        customer_id=customer['customer_id'],
                        opportunity_type=OpportunityType(opp_data.get('opportunity_type', 'cross_sell')),
                        priority=OpportunityPriority(opp_data.get('priority', 'medium')),
                        products_owned=customer.get('software_owned', []),
                        recommended_products=product_recommendations,
                        total_potential_revenue=total_revenue,
                        conversion_probability=opp_data.get('conversion_probability', 0.5),
                        best_contact_time=opp_data.get('best_contact_time', 'morning'),
                        personalized_pitch=opp_data.get('personalized_pitch', 'We have some great recommendations for you!'),
                        objection_handlers=opp_data.get('objection_handlers', []),
                        expires_at=expires_at
                    )
                    opportunities.append(opportunity)
                
                return opportunities
                
            except json.JSONDecodeError:
                return await self._fallback_customer_opportunities(customer)
                
        except Exception as e:
            print(f"Customer opportunity analysis error: {e}")
            return await self._fallback_customer_opportunities(customer)
    
    async def generate_cross_sell_campaign(self, opportunity_ids: List[str]) -> Dict[str, Any]:
        """Generate targeted cross-sell campaign for specific opportunities"""
        try:
            # Get opportunities
            opportunities = []
            for opp_id in opportunity_ids:
                opp_doc = await self.db.cross_sell_opportunities.find_one({"opportunity_id": opp_id})
                if opp_doc:
                    opportunities.append(CrossSellOpportunity(**opp_doc))
            
            if not opportunities:
                return {"error": "No valid opportunities found"}
            
            # Group opportunities by type and priority
            campaign_groups = {}
            for opp in opportunities:
                key = f"{opp.opportunity_type}_{opp.priority}"
                if key not in campaign_groups:
                    campaign_groups[key] = []
                campaign_groups[key].append(opp)
            
            # Generate campaign strategy using AI
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"cross_sell_campaign_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's cross-sell campaign strategist. 
                Create targeted campaigns that maximize conversion while maintaining customer relationships."""
            ).with_model("openai", "gpt-4o-mini")
            
            campaign_data = {
                "total_opportunities": len(opportunities),
                "total_potential_revenue": sum(opp.total_potential_revenue for opp in opportunities),
                "avg_conversion_probability": sum(opp.conversion_probability for opp in opportunities) / len(opportunities),
                "opportunity_groups": list(campaign_groups.keys()),
                "priority_distribution": {
                    "urgent": len([o for o in opportunities if o.priority == OpportunityPriority.URGENT]),
                    "high": len([o for o in opportunities if o.priority == OpportunityPriority.HIGH]),
                    "medium": len([o for o in opportunities if o.priority == OpportunityPriority.MEDIUM]),
                    "low": len([o for o in opportunities if o.priority == OpportunityPriority.LOW])
                }
            }
            
            campaign_prompt = f"""
            Create a cross-sell campaign strategy using Customer Mind IQ optimization:
            
            Campaign Data: {json.dumps(campaign_data, default=str)}
            Sample Opportunities: {json.dumps([opp.dict() for opp in opportunities[:3]], default=str)}
            
            Generate campaign strategy in this JSON format:
            {{
                "campaign_name": "<descriptive_campaign_name>",
                "campaign_description": "<campaign_overview>",
                "target_segments": [
                    {{
                        "segment_name": "<segment>",
                        "opportunity_type": "<type>",
                        "priority": "<priority>",
                        "customer_count": <count>,
                        "messaging_strategy": "<messaging_approach>"
                    }}
                ],
                "channel_strategy": {{
                    "primary_channel": "<email/phone/in_app>",
                    "secondary_channels": ["channel1", "channel2"],
                    "timing_strategy": "<timing_approach>"
                }},
                "content_templates": {{
                    "email_subject": "<email_subject_template>",
                    "email_body": "<email_body_template>",
                    "phone_script": "<phone_script_template>"
                }},
                "success_metrics": {{
                    "target_conversion_rate": <target_rate>,
                    "expected_revenue": <expected_revenue>,
                    "campaign_duration_days": <duration>
                }},
                "implementation_steps": ["step1", "step2", "step3"]
            }}
            """
            
            message = UserMessage(text=campaign_prompt)
            response = await chat.send_message(message)
            
            try:
                campaign_strategy = json.loads(response)
                
                # Store campaign
                campaign_doc = {
                    "campaign_id": str(uuid.uuid4()),
                    "opportunity_ids": opportunity_ids,
                    "strategy": campaign_strategy,
                    "created_at": datetime.now(),
                    "status": "draft"
                }
                
                await self.db.cross_sell_campaigns.insert_one(campaign_doc)
                
                return {
                    "campaign_id": campaign_doc["campaign_id"],
                    "strategy": campaign_strategy,
                    "opportunities_included": len(opportunities),
                    "total_potential_revenue": sum(opp.total_potential_revenue for opp in opportunities)
                }
                
            except json.JSONDecodeError:
                return await self._fallback_campaign_generation(opportunities)
                
        except Exception as e:
            print(f"Cross-sell campaign generation error: {e}")
            return {"error": str(e)}
    
    async def get_cross_sell_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive cross-sell intelligence dashboard"""
        try:
            # Get opportunities and campaigns
            opportunities = await self.db.cross_sell_opportunities.find().to_list(length=1000)
            campaigns = await self.db.cross_sell_campaigns.find().to_list(length=100)
            
            if not opportunities:
                return await self._generate_sample_cross_sell_dashboard()
            
            # Opportunity analysis
            total_opportunities = len(opportunities)
            total_potential_revenue = sum(opp.get('total_potential_revenue', 0) for opp in opportunities)
            avg_conversion_probability = sum(opp.get('conversion_probability', 0.5) for opp in opportunities) / total_opportunities
            
            # Priority distribution
            priority_distribution = {}
            for opp in opportunities:
                priority = opp.get('priority', 'medium')
                priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
            
            # Opportunity type distribution
            type_distribution = {}
            for opp in opportunities:
                opp_type = opp.get('opportunity_type', 'cross_sell')
                type_distribution[opp_type] = type_distribution.get(opp_type, 0) + 1
            
            # Top opportunities by revenue potential
            opportunities_by_revenue = sorted(opportunities, key=lambda x: x.get('total_potential_revenue', 0), reverse=True)
            top_opportunities = [
                {
                    "opportunity_id": opp.get('opportunity_id'),
                    "customer_id": opp.get('customer_id'),
                    "type": opp.get('opportunity_type'),
                    "potential_revenue": opp.get('total_potential_revenue'),
                    "conversion_probability": opp.get('conversion_probability')
                }
                for opp in opportunities_by_revenue[:10]
            ]
            
            # Campaign performance
            active_campaigns = len([c for c in campaigns if c.get('status') != 'completed'])
            
            return {
                "opportunities_overview": {
                    "total_opportunities": total_opportunities,
                    "total_potential_revenue": total_potential_revenue,
                    "avg_conversion_probability": round(avg_conversion_probability, 3),
                    "high_priority_opportunities": priority_distribution.get('high', 0) + priority_distribution.get('urgent', 0)
                },
                "priority_distribution": priority_distribution,
                "type_distribution": type_distribution,
                "campaign_metrics": {
                    "total_campaigns": len(campaigns),
                    "active_campaigns": active_campaigns,
                    "campaigns_this_month": len([c for c in campaigns if c.get('created_at', datetime.min).month == datetime.now().month])
                },
                "top_opportunities": top_opportunities,
                "performance_insights": [
                    f"${total_potential_revenue:,.2f} in identified revenue opportunities",
                    f"{avg_conversion_probability:.1%} average conversion probability",
                    f"{priority_distribution.get('urgent', 0)} urgent opportunities requiring immediate attention",
                    f"Most common opportunity type: {max(type_distribution.items(), key=lambda x: x[1])[0] if type_distribution else 'N/A'}"
                ]
            }
            
        except Exception as e:
            print(f"Cross-sell dashboard error: {e}")
            return await self._generate_sample_cross_sell_dashboard()
    
    async def _get_available_products(self) -> List[Dict[str, Any]]:
        """Get available products for recommendations"""
        try:
            # Try to get from products database first
            products = await self.db.products.find().to_list(length=50)
            
            if products:
                return products
            
            # Fallback to sample products
            return [
                {"product_id": "prod_1", "name": "CRM Pro", "category": "CRM", "price": 299.0},
                {"product_id": "prod_2", "name": "Analytics Suite", "category": "Analytics", "price": 199.0},
                {"product_id": "prod_3", "name": "Email Marketing Pro", "category": "Marketing", "price": 149.0},
                {"product_id": "prod_4", "name": "Customer Support Premium", "category": "Support", "price": 99.0},
                {"product_id": "prod_5", "name": "Sales Automation", "category": "Sales", "price": 249.0}
            ]
            
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    async def _fallback_opportunities(self, customers_data: List[Dict]) -> List[CrossSellOpportunity]:
        """Fallback opportunities when AI fails"""
        opportunities = []
        for customer in customers_data[:5]:  # Limit to avoid too many fallback opportunities
            fallback_opps = await self._fallback_customer_opportunities(customer)
            opportunities.extend(fallback_opps)
        return opportunities
    
    async def _fallback_customer_opportunities(self, customer: Dict) -> List[CrossSellOpportunity]:
        """Fallback opportunities for individual customer"""
        total_spent = customer.get('total_spent', 0)
        
        # Simple rule-based opportunity identification
        if total_spent > 10000:
            priority = OpportunityPriority.HIGH
            products = [
                ProductRecommendation(
                    product_id="premium_addon",
                    product_name="Premium Add-on",
                    category="Premium",
                    price=500.0,
                    relevance_score=0.8,
                    reasoning="High-value customer ready for premium features",
                    expected_revenue=500.0
                )
            ]
        elif total_spent > 5000:
            priority = OpportunityPriority.MEDIUM
            products = [
                ProductRecommendation(
                    product_id="standard_upgrade",
                    product_name="Standard Upgrade",
                    category="Upgrade",
                    price=200.0,
                    relevance_score=0.6,
                    reasoning="Good candidate for feature upgrade",
                    expected_revenue=200.0
                )
            ]
        else:
            priority = OpportunityPriority.LOW
            products = [
                ProductRecommendation(
                    product_id="starter_addon",
                    product_name="Starter Add-on",
                    category="Basic",
                    price=50.0,
                    relevance_score=0.5,
                    reasoning="Entry-level customer with growth potential",
                    expected_revenue=50.0
                )
            ]
        
        opportunity = CrossSellOpportunity(
            opportunity_id=str(uuid.uuid4()),
            customer_id=customer['customer_id'],
            opportunity_type=OpportunityType.UPSELL,
            priority=priority,
            products_owned=customer.get('software_owned', []),
            recommended_products=products,
            total_potential_revenue=sum(p.expected_revenue for p in products),
            conversion_probability=0.4,
            best_contact_time="morning",
            personalized_pitch="Based on your usage, we recommend upgrading for enhanced features.",
            objection_handlers=["Highlight ROI benefits", "Offer trial period"],
            expires_at=datetime.now() + timedelta(days=30)
        )
        
        return [opportunity]
    
    async def _fallback_campaign_generation(self, opportunities: List[CrossSellOpportunity]) -> Dict[str, Any]:
        """Fallback campaign generation when AI fails"""
        return {
            "campaign_id": str(uuid.uuid4()),
            "strategy": {
                "campaign_name": "Cross-Sell Opportunity Campaign",
                "campaign_description": "Targeted campaign for identified cross-sell opportunities",
                "target_segments": [
                    {
                        "segment_name": "High Priority Customers",
                        "opportunity_type": "mixed",
                        "priority": "high",
                        "customer_count": len(opportunities),
                        "messaging_strategy": "Personalized value proposition"
                    }
                ],
                "channel_strategy": {
                    "primary_channel": "email",
                    "secondary_channels": ["phone"],
                    "timing_strategy": "Best customer contact time"
                },
                "success_metrics": {
                    "target_conversion_rate": 0.15,
                    "expected_revenue": sum(opp.total_potential_revenue for opp in opportunities) * 0.15,
                    "campaign_duration_days": 30
                }
            },
            "opportunities_included": len(opportunities),
            "total_potential_revenue": sum(opp.total_potential_revenue for opp in opportunities)
        }
    
    async def _generate_sample_cross_sell_dashboard(self) -> Dict[str, Any]:
        """Generate sample cross-sell dashboard"""
        return {
            "opportunities_overview": {
                "total_opportunities": 45,
                "total_potential_revenue": 125000.0,
                "avg_conversion_probability": 0.35,
                "high_priority_opportunities": 12
            },
            "priority_distribution": {
                "urgent": 3,
                "high": 9,
                "medium": 20,
                "low": 13
            },
            "type_distribution": {
                "cross_sell": 25,
                "upsell": 15,
                "bundle": 3,
                "renewal": 2
            },
            "campaign_metrics": {
                "total_campaigns": 6,
                "active_campaigns": 2,
                "campaigns_this_month": 3
            },
            "top_opportunities": [
                {
                    "opportunity_id": "opp_1",
                    "customer_id": "customer_1",
                    "type": "upsell",
                    "potential_revenue": 5000.0,
                    "conversion_probability": 0.8
                }
            ],
            "performance_insights": [
                "$125,000.00 in identified revenue opportunities",
                "35.0% average conversion probability",
                "3 urgent opportunities requiring immediate attention",
                "Most common opportunity type: cross_sell"
            ]
        }
    
    async def _store_opportunities(self, opportunities: List[CrossSellOpportunity]):
        """Store cross-sell opportunities in database"""
        try:
            documents = [opp.dict() for opp in opportunities]
            if documents:
                await self.db.cross_sell_opportunities.insert_many(documents)
                print(f"✅ Stored {len(documents)} cross-sell opportunities")
        except Exception as e:
            print(f"❌ Error storing cross-sell opportunities: {e}")