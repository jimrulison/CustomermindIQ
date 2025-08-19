import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
import uuid
import re
from pymongo import MongoClient

# Load environment variables
load_dotenv()

class AICustomerIntelligence:
    """
    AI-powered customer behavior analysis and intelligence system
    Uses Emergent LLM integration for comprehensive customer analytics
    """
    
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
        
        # MongoDB connection for storing AI analysis results
        self.mongo_client = MongoClient(os.getenv('MONGO_URL'))
        self.db = self.mongo_client[os.getenv('DB_NAME', 'customer_intelligence')]
        
        # Initialize collections
        self.customer_analysis_collection = self.db.customer_analysis
        self.behavioral_patterns_collection = self.db.behavioral_patterns
        self.purchase_predictions_collection = self.db.purchase_predictions
        self.business_rules_collection = self.db.business_rules
        
        # AI Chat instances for different analysis types
        self.behavior_analyzer = None
        self.prediction_engine = None
        self.recommendation_engine = None
        self.business_rules_engine = None
        
    async def initialize_ai_engines(self):
        """Initialize AI chat engines for different analysis types"""
        
        # Customer Behavior Analyzer
        self.behavior_analyzer = LlmChat(
            api_key=self.api_key,
            session_id="customer_behavior_analysis",
            system_message="""You are an expert customer behavior analyst specializing in purchase pattern recognition and customer lifecycle analysis. 

Your expertise includes:
- Analyzing purchase history patterns and frequency
- Identifying customer lifecycle stages (new, active, at_risk, churned)
- Calculating customer lifetime value and engagement scores
- Detecting behavioral anomalies and churn risk signals
- Segmenting customers based on behavior patterns

Always provide structured JSON responses with specific metrics, confidence scores, and actionable insights. Focus on business-relevant patterns that drive revenue optimization and customer retention strategies."""
        ).with_model("openai", "gpt-4o-mini")
        
        # Purchase Prediction Engine
        self.prediction_engine = LlmChat(
            api_key=self.api_key,
            session_id="purchase_prediction",
            system_message="""You are an advanced predictive analytics specialist focused on customer purchase behavior and product recommendations.

Your capabilities include:
- Predicting next purchase probability and timing
- Identifying cross-sell and upsell opportunities
- Calculating purchase intent scores and conversion likelihood
- Analyzing product affinity and recommendation confidence
- Forecasting customer spending patterns and seasonal trends

Provide precise probability scores, confidence intervals, and specific product recommendations with detailed reasoning. Always include timing predictions and business impact assessments."""
        ).with_model("openai", "gpt-4o-mini")
        
        # Product Recommendation Engine
        self.recommendation_engine = LlmChat(
            api_key=self.api_key,
            session_id="product_recommendations",
            system_message="""You are an intelligent product recommendation system specializing in personalized customer experiences and revenue optimization.

Your focus areas:
- Generating personalized product recommendations based on purchase history
- Analyzing product affinity and cross-sell opportunities
- Calculating recommendation confidence and expected conversion rates
- Identifying optimal timing and channels for product suggestions
- Optimizing product bundles and pricing strategies

Always provide ranked recommendations with confidence scores, expected revenue impact, and personalization reasoning. Include implementation strategies and success metrics."""
        ).with_model("openai", "gpt-4o-mini")
        
        # Business Rules Engine
        self.business_rules_engine = LlmChat(
            api_key=self.api_key,
            session_id="business_rules_generation",
            system_message="""You are a business intelligence specialist focused on generating data-driven business rules and optimization strategies.

Your responsibilities:
- Creating intelligent business logic rules based on customer data patterns
- Defining automated triggers for marketing campaigns and interventions
- Establishing scoring algorithms and threshold values
- Generating dynamic pricing and promotion strategies
- Creating customer segmentation and targeting rules

Generate practical, implementable business rules with clear conditions, actions, and expected outcomes. Focus on automatable logic that drives measurable business results."""
        ).with_model("openai", "gpt-4o-mini")
    
    async def analyze_customer_behavior(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive AI analysis of individual customer behavior patterns
        """
        if not self.behavior_analyzer:
            await self.initialize_ai_engines()
        
        analysis_prompt = f"""
        Analyze this customer's behavior patterns and provide comprehensive insights:

        Customer Profile:
        - Name: {customer_data.get('name', 'Unknown')}
        - Email: {customer_data.get('email', 'Unknown')}
        - Registration Date: {customer_data.get('registration_date', 'Unknown')}
        - Total Purchases: {customer_data.get('total_purchases', 0)}
        - Total Spent: ${customer_data.get('total_spent', 0)}
        - Last Purchase: {customer_data.get('last_purchase_date', 'Unknown')}
        - Products Owned: {customer_data.get('products_owned', [])}
        - Communication History: {customer_data.get('communication_history', [])}
        - Support Tickets: {customer_data.get('support_tickets', 0)}

        Purchase History:
        {json.dumps(customer_data.get('purchase_history', []), indent=2)}

        Provide analysis in this exact JSON format:
        {{
            "customer_id": "{customer_data.get('customer_id', 'unknown')}",
            "analysis_timestamp": "{datetime.now().isoformat()}",
            "lifecycle_stage": "new|active|at_risk|churned",
            "engagement_score": 0-100,
            "churn_risk": 0-100,
            "customer_lifetime_value": 0.00,
            "purchase_frequency": "weekly|monthly|quarterly|irregular",
            "spending_trend": "increasing|stable|decreasing",
            "behavioral_segments": ["segment1", "segment2"],
            "key_insights": [
                "insight 1",
                "insight 2", 
                "insight 3"
            ],
            "risk_factors": [
                "risk factor 1",
                "risk factor 2"
            ],
            "opportunities": [
                "opportunity 1",
                "opportunity 2"
            ],
            "recommended_actions": [
                {{
                    "action": "specific action",
                    "priority": "high|medium|low",
                    "expected_impact": "description",
                    "timeline": "immediate|1-week|1-month"
                }}
            ],
            "confidence_score": 0-100
        }}
        """
        
        try:
            user_message = UserMessage(text=analysis_prompt)
            response = await self.behavior_analyzer.send_message(user_message)
            
            # Parse JSON response
            analysis_result = self._parse_json_response(response)
            
            # Store in database
            analysis_result['_id'] = str(uuid.uuid4())
            analysis_result['created_at'] = datetime.now()
            self.customer_analysis_collection.insert_one(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            print(f"Error in customer behavior analysis: {str(e)}")
            return self._generate_fallback_analysis(customer_data)
    
    async def predict_next_purchase(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered prediction of customer's next purchase behavior
        """
        if not self.prediction_engine:
            await self.initialize_ai_engines()
        
        prediction_prompt = f"""
        Analyze this customer's purchase history and predict their next purchase behavior:

        Customer Profile:
        - Current Lifecycle Stage: {customer_data.get('lifecycle_stage', 'unknown')}
        - Total Purchases: {customer_data.get('total_purchases', 0)}
        - Average Order Value: ${customer_data.get('average_order_value', 0)}
        - Days Since Last Purchase: {customer_data.get('days_since_last_purchase', 0)}
        - Purchase Frequency: {customer_data.get('purchase_frequency', 'unknown')}
        
        Recent Purchase Pattern:
        {json.dumps(customer_data.get('recent_purchases', []), indent=2)}
        
        Product Preferences:
        {json.dumps(customer_data.get('product_preferences', {}), indent=2)}

        Provide predictions in this exact JSON format:
        {{
            "customer_id": "{customer_data.get('customer_id', 'unknown')}",
            "prediction_timestamp": "{datetime.now().isoformat()}",
            "next_purchase_probability": 0-100,
            "predicted_purchase_date": "YYYY-MM-DD",
            "confidence_interval": "±X days",
            "predicted_order_value": 0.00,
            "likely_products": [
                {{
                    "product_name": "Product Name",
                    "probability": 0-100,
                    "confidence": 0-100,
                    "reasoning": "why this product"
                }}
            ],
            "purchase_triggers": [
                "trigger 1",
                "trigger 2"
            ],
            "optimal_contact_timing": {{
                "best_day": "Monday|Tuesday|...",
                "best_time": "morning|afternoon|evening",
                "preferred_channel": "email|phone|sms"
            }},
            "upsell_opportunities": [
                {{
                    "product": "Product Name",
                    "probability": 0-100,
                    "revenue_impact": 0.00
                }}
            ],
            "cross_sell_opportunities": [
                {{
                    "product": "Product Name", 
                    "probability": 0-100,
                    "revenue_impact": 0.00
                }}
            ],
            "prediction_confidence": 0-100
        }}
        """
        
        try:
            user_message = UserMessage(text=prediction_prompt)
            response = await self.prediction_engine.send_message(user_message)
            
            prediction_result = self._parse_json_response(response)
            
            # Store prediction in database
            prediction_result['_id'] = str(uuid.uuid4())
            prediction_result['created_at'] = datetime.now()
            self.purchase_predictions_collection.insert_one(prediction_result)
            
            return prediction_result
            
        except Exception as e:
            print(f"Error in purchase prediction: {str(e)}")
            return self._generate_fallback_prediction(customer_data)
    
    async def generate_product_recommendations(self, customer_data: Dict[str, Any], available_products: List[Dict]) -> Dict[str, Any]:
        """
        AI-powered personalized product recommendations
        """
        if not self.recommendation_engine:
            await self.initialize_ai_engines()
        
        recommendation_prompt = f"""
        Generate personalized product recommendations for this customer:

        Customer Profile:
        - Purchase History: {json.dumps(customer_data.get('purchase_history', []), indent=2)}
        - Products Owned: {customer_data.get('products_owned', [])}
        - Spending Behavior: {customer_data.get('spending_behavior', {})}
        - Preferences: {customer_data.get('preferences', {})}
        
        Available Products:
        {json.dumps(available_products, indent=2)}

        Generate recommendations in this exact JSON format:
        {{
            "customer_id": "{customer_data.get('customer_id', 'unknown')}",
            "recommendation_timestamp": "{datetime.now().isoformat()}",
            "recommendations": [
                {{
                    "product_id": "product_id",
                    "product_name": "Product Name",
                    "recommendation_type": "cross_sell|upsell|new_category|replenishment",
                    "confidence_score": 0-100,
                    "expected_conversion_rate": 0-100,
                    "revenue_potential": 0.00,
                    "reasoning": "detailed explanation for recommendation",
                    "personalization_factors": ["factor1", "factor2"],
                    "optimal_timing": "immediate|1-week|1-month",
                    "presentation_context": "email|website|phone|in-app"
                }}
            ],
            "recommendation_strategy": "strategy description",
            "total_revenue_potential": 0.00,
            "overall_confidence": 0-100
        }}
        """
        
        try:
            user_message = UserMessage(text=recommendation_prompt)
            response = await self.recommendation_engine.send_message(user_message)
            
            recommendations = self._parse_json_response(response)
            
            # Store recommendations
            recommendations['_id'] = str(uuid.uuid4())
            recommendations['created_at'] = datetime.now()
            # Note: You might want to create a separate collection for recommendations
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return self._generate_fallback_recommendations(customer_data)
    
    async def generate_business_rules(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-generated business logic rules based on customer data patterns
        """
        if not self.business_rules_engine:
            await self.initialize_ai_engines()
        
        rules_prompt = f"""
        Generate intelligent business rules based on this business context and customer data patterns:

        Business Context:
        - Industry: {business_context.get('industry', 'Unknown')}
        - Business Model: {business_context.get('business_model', 'Unknown')}
        - Customer Base Size: {business_context.get('customer_count', 0)}
        - Average Revenue Per Customer: ${business_context.get('arpc', 0)}
        - Customer Acquisition Cost: ${business_context.get('cac', 0)}
        - Churn Rate: {business_context.get('churn_rate', 0)}%
        
        Customer Patterns:
        {json.dumps(business_context.get('customer_patterns', {}), indent=2)}

        Generate business rules in this exact JSON format:
        {{
            "rules_timestamp": "{datetime.now().isoformat()}",
            "customer_scoring_rules": {{
                "engagement_score_algorithm": {{
                    "factors": [
                        {{"factor": "purchase_frequency", "weight": 0.3, "calculation": "description"}},
                        {{"factor": "recency", "weight": 0.25, "calculation": "description"}}
                    ],
                    "score_ranges": {{
                        "high": "80-100: description",
                        "medium": "50-79: description", 
                        "low": "0-49: description"
                    }}
                }},
                "churn_risk_indicators": [
                    {{"indicator": "no_purchase_X_days", "threshold": 60, "risk_level": "medium"}},
                    {{"indicator": "decreased_engagement", "threshold": "50%", "risk_level": "high"}}
                ]
            }},
            "marketing_automation_rules": [
                {{
                    "rule_name": "Welcome Series",
                    "trigger": "new_customer_registration",
                    "conditions": ["condition1", "condition2"],
                    "actions": ["send_welcome_email", "assign_to_nurture_sequence"],
                    "timing": "immediate",
                    "expected_outcome": "increase_engagement_by_X%"
                }}
            ],
            "pricing_optimization_rules": [
                {{
                    "rule_name": "Dynamic Discount",
                    "customer_segment": "at_risk_customers",
                    "discount_percentage": 15,
                    "conditions": ["no_purchase_30_days", "high_ltv"],
                    "expected_impact": "reduce_churn_by_X%"
                }}
            ],
            "product_recommendation_rules": [
                {{
                    "rule_name": "Cross-sell Engine",
                    "trigger": "product_purchase",
                    "logic": "customers_who_bought_X_also_bought_Y",
                    "confidence_threshold": 70,
                    "timing": "immediate_post_purchase"
                }}
            ],
            "customer_intervention_rules": [
                {{
                    "rule_name": "Churn Prevention",
                    "trigger": "churn_risk_score > 70",
                    "actions": ["personal_outreach", "retention_offer"],
                    "escalation_path": "csm -> sales_manager -> director",
                    "success_metrics": ["retention_rate", "satisfaction_score"]
                }}
            ],
            "segmentation_rules": {{
                "high_value": {{"criteria": ["ltv > $1000", "purchase_frequency > monthly"], "treatment": "VIP_service"}},
                "growth_potential": {{"criteria": ["engagement_score > 60", "ltv < $500"], "treatment": "upsell_campaign"}},
                "at_risk": {{"criteria": ["churn_score > 60"], "treatment": "retention_program"}}
            }},
            "implementation_priority": [
                {{"rule_category": "churn_prevention", "priority": 1, "impact": "high"}},
                {{"rule_category": "upsell_automation", "priority": 2, "impact": "medium"}}
            ]
        }}
        """
        
        try:
            user_message = UserMessage(text=rules_prompt)
            response = await self.business_rules_engine.send_message(user_message)
            
            business_rules = self._parse_json_response(response)
            
            # Store business rules
            business_rules['_id'] = str(uuid.uuid4())
            business_rules['created_at'] = datetime.now()
            self.business_rules_collection.insert_one(business_rules)
            
            return business_rules
            
        except Exception as e:
            print(f"Error generating business rules: {str(e)}")
            return self._generate_fallback_business_rules()
    
    async def analyze_customer_cohort(self, cohort_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        AI analysis of customer cohort behavior patterns
        """
        if not self.behavior_analyzer:
            await self.initialize_ai_engines()
        
        cohort_prompt = f"""
        Analyze this customer cohort and identify patterns, trends, and insights:

        Cohort Data:
        - Cohort Size: {len(cohort_data)}
        - Customers: {json.dumps(cohort_data[:10], indent=2)}  # First 10 for analysis
        
        Provide cohort analysis in this JSON format:
        {{
            "cohort_analysis_timestamp": "{datetime.now().isoformat()}",
            "cohort_size": {len(cohort_data)},
            "behavior_patterns": {{
                "common_purchase_patterns": ["pattern1", "pattern2"],
                "average_ltv": 0.00,
                "retention_rate": 0-100,
                "engagement_distribution": {{"high": 0.0, "medium": 0.0, "low": 0.0}}
            }},
            "segment_characteristics": [
                {{
                    "segment_name": "High Value Customers",
                    "percentage": 0.0,
                    "key_traits": ["trait1", "trait2"],
                    "revenue_contribution": 0.0
                }}
            ],
            "optimization_opportunities": [
                {{
                    "opportunity": "description",
                    "target_segment": "segment_name",
                    "expected_impact": "description",
                    "implementation": "how_to_implement"
                }}
            ],
            "predictive_insights": {{
                "churn_risk_distribution": {{"high": 0.0, "medium": 0.0, "low": 0.0}},
                "growth_potential": "description",
                "seasonal_patterns": ["pattern1", "pattern2"]
            }},
            "recommended_strategies": [
                {{
                    "strategy": "strategy_name",
                    "target": "target_segment",
                    "tactics": ["tactic1", "tactic2"],
                    "expected_roi": "X%"
                }}
            ]
        }}
        """
        
        try:
            user_message = UserMessage(text=cohort_prompt)
            response = await self.behavior_analyzer.send_message(user_message)
            
            cohort_analysis = self._parse_json_response(response)
            return cohort_analysis
            
        except Exception as e:
            print(f"Error in cohort analysis: {str(e)}")
            return {"error": "Cohort analysis failed", "details": str(e)}
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response, handling potential formatting issues"""
        try:
            # Clean the response - remove any markdown formatting
            cleaned_response = re.sub(r'```json\s*|\s*```', '', response.strip())
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response content: {response}")
            # Return a basic structure if parsing fails
            return {
                "error": "Failed to parse AI response",
                "raw_response": response,
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_fallback_analysis(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic analysis when AI fails"""
        return {
            "customer_id": customer_data.get('customer_id', 'unknown'),
            "analysis_timestamp": datetime.now().isoformat(),
            "lifecycle_stage": "active",
            "engagement_score": 50,
            "churn_risk": 30,
            "customer_lifetime_value": customer_data.get('total_spent', 0),
            "confidence_score": 25,
            "error": "AI analysis unavailable, using fallback method"
        }
    
    def _generate_fallback_prediction(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic prediction when AI fails"""
        return {
            "customer_id": customer_data.get('customer_id', 'unknown'),
            "prediction_timestamp": datetime.now().isoformat(),
            "next_purchase_probability": 50,
            "predicted_purchase_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "prediction_confidence": 25,
            "error": "AI prediction unavailable, using fallback method"
        }
    
    def _generate_fallback_recommendations(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic recommendations when AI fails"""
        return {
            "customer_id": customer_data.get('customer_id', 'unknown'),
            "recommendation_timestamp": datetime.now().isoformat(),
            "recommendations": [],
            "overall_confidence": 0,
            "error": "AI recommendations unavailable"
        }
    
    def _generate_fallback_business_rules(self) -> Dict[str, Any]:
        """Generate basic business rules when AI fails"""
        return {
            "rules_timestamp": datetime.now().isoformat(),
            "customer_scoring_rules": {},
            "marketing_automation_rules": [],
            "error": "AI business rules generation unavailable"
        }

# Initialize global instance
ai_customer_intelligence = AICustomerIntelligence()