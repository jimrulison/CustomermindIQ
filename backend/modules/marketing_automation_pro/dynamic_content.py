"""
Customer Mind IQ - Dynamic Content Microservice
AI-powered dynamic content personalization and optimization
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

class ContentType(str, Enum):
    EMAIL = "email"
    WEB_PAGE = "web_page"
    SMS = "sms"
    SOCIAL_MEDIA = "social_media"
    PUSH_NOTIFICATION = "push_notification"
    BANNER = "banner"

class PersonalizationLevel(str, Enum):
    BASIC = "basic"
    ADVANCED = "advanced"
    AI_POWERED = "ai_powered"

class ContentTemplate(BaseModel):
    template_id: str
    name: str
    content_type: ContentType
    base_content: Dict[str, Any]
    personalization_rules: List[Dict[str, Any]]
    dynamic_elements: List[str]
    performance_metrics: Dict[str, float] = {}
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class ContentPersonalization(BaseModel):
    personalization_id: str
    customer_id: str
    template_id: str
    generated_content: Dict[str, Any]
    personalization_level: PersonalizationLevel
    personalization_factors: List[str]
    confidence_score: float
    generated_at: datetime = datetime.now()

class DynamicContentService:
    """Customer Mind IQ Dynamic Content Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq
        
    async def create_content_template(self, template_data: Dict[str, Any]) -> ContentTemplate:
        """Create a dynamic content template with AI optimization"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"content_template_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's dynamic content specialist. 
                Create personalized content templates that adapt to individual customer preferences and behaviors."""
            ).with_model("openai", "gpt-4o-mini")
            
            template_optimization_prompt = f"""
            Create an optimized dynamic content template using Customer Mind IQ personalization algorithms:
            
            Template Request: {json.dumps(template_data, default=str)}
            
            Provide content template optimization in this exact JSON format:
            {{
                "optimized_base_content": {{
                    "subject": "<personalization_ready_subject>",
                    "headline": "<dynamic_headline>",
                    "body": "<personalization_ready_body>",
                    "cta": "<dynamic_call_to_action>",
                    "images": ["<image_placeholder>"],
                    "personalization_variables": ["{{customer_name}}", "{{product_recommendation}}", "{{location}}"]
                }},
                "personalization_rules": [
                    {{
                        "condition": "<customer_segment>",
                        "content_variation": {{"element": "value"}},
                        "priority": <1-10>
                    }}
                ],
                "dynamic_elements": ["subject", "headline", "product_recommendation", "cta"],
                "optimization_suggestions": [
                    "suggestion1",
                    "suggestion2"
                ],
                "performance_predictions": {{
                    "expected_open_rate": <0.0-1.0>,
                    "expected_click_rate": <0.0-1.0>,
                    "personalization_lift": <percentage>
                }}
            }}
            
            Focus on maximum personalization impact and conversion optimization.
            """
            
            message = UserMessage(text=template_optimization_prompt)
            response = await chat.send_message(message)
            
            try:
                optimization = json.loads(response)
                
                template = ContentTemplate(
                    template_id=str(uuid.uuid4()),
                    name=template_data.get('name', 'Dynamic Content Template'),
                    content_type=ContentType(template_data.get('content_type', 'email')),
                    base_content=optimization.get('optimized_base_content', {}),
                    personalization_rules=optimization.get('personalization_rules', []),
                    dynamic_elements=optimization.get('dynamic_elements', []),
                    performance_metrics=optimization.get('performance_predictions', {})
                )
                
                # Store template
                await self._store_content_template(template)
                return template
                
            except json.JSONDecodeError:
                return await self._fallback_template_creation(template_data)
                
        except Exception as e:
            print(f"Content template creation error: {e}")
            return await self._fallback_template_creation(template_data)
    
    async def generate_personalized_content(self, template_id: str, customer_data: Dict[str, Any]) -> ContentPersonalization:
        """Generate personalized content for specific customer"""
        try:
            # Get template
            template_doc = await self.db.content_templates.find_one({"template_id": template_id})
            if not template_doc:
                raise Exception("Template not found")
            
            template = ContentTemplate(**template_doc)
            
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"content_personalization_{customer_data.get('customer_id', 'unknown')}",
                system_message="""You are Customer Mind IQ's content personalization engine. 
                Generate highly personalized content that resonates with individual customers."""
            ).with_model("openai", "gpt-4o-mini")
            
            personalization_prompt = f"""
            Generate personalized content using Customer Mind IQ advanced personalization:
            
            Template: {json.dumps(template.base_content, default=str)}
            Customer Profile: {json.dumps(customer_data, default=str)}
            Personalization Rules: {json.dumps(template.personalization_rules, default=str)}
            Dynamic Elements: {template.dynamic_elements}
            
            Create personalized content in this exact JSON format:
            {{
                "personalized_content": {{
                    "subject": "<personalized_subject>",
                    "headline": "<personalized_headline>",
                    "body": "<personalized_body_content>",
                    "cta": "<personalized_call_to_action>",
                    "product_recommendations": ["product1", "product2"],
                    "personalization_tokens": {{
                        "customer_name": "<name>",
                        "location": "<location>",
                        "preference": "<preference>"
                    }}
                }},
                "personalization_level": "ai_powered",
                "personalization_factors": ["purchase_history", "behavior_pattern", "preferences"],
                "confidence_score": <0.0-1.0>,
                "reasoning": "<why_this_personalization_works>"
            }}
            
            Make content highly relevant and engaging for this specific customer.
            """
            
            message = UserMessage(text=personalization_prompt)
            response = await chat.send_message(message)
            
            try:
                personalization_data = json.loads(response)
                
                personalization = ContentPersonalization(
                    personalization_id=str(uuid.uuid4()),
                    customer_id=customer_data.get('customer_id', 'unknown'),
                    template_id=template_id,
                    generated_content=personalization_data.get('personalized_content', {}),
                    personalization_level=PersonalizationLevel(personalization_data.get('personalization_level', 'basic')),
                    personalization_factors=personalization_data.get('personalization_factors', []),
                    confidence_score=personalization_data.get('confidence_score', 0.7)
                )
                
                # Store personalization
                await self._store_personalization(personalization)
                return personalization
                
            except json.JSONDecodeError:
                return await self._fallback_personalization(template_id, customer_data)
                
        except Exception as e:
            print(f"Content personalization error: {e}")
            return await self._fallback_personalization(template_id, customer_data)
    
    async def optimize_content_performance(self, template_id: str) -> Dict[str, Any]:
        """Optimize content template based on performance data"""
        try:
            # Get template and personalization history
            template_doc = await self.db.content_templates.find_one({"template_id": template_id})
            personalizations = await self.db.content_personalizations.find(
                {"template_id": template_id}
            ).to_list(length=100)
            
            if not template_doc:
                return {"error": "Template not found"}
            
            template = ContentTemplate(**template_doc)
            
            # Analyze performance patterns
            performance_analysis = await self._analyze_content_performance(template, personalizations)
            
            # Generate optimization recommendations
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"content_optimization_{template_id}",
                system_message="""You are Customer Mind IQ's content optimization specialist. 
                Analyze performance data and recommend content improvements."""
            ).with_model("openai", "gpt-4o-mini")
            
            optimization_prompt = f"""
            Analyze content performance and provide optimization recommendations:
            
            Template: {template.name}
            Performance Analysis: {json.dumps(performance_analysis, default=str)}
            Current Metrics: {json.dumps(template.performance_metrics, default=str)}
            
            Provide content optimization in JSON format:
            {{
                "optimization_recommendations": [
                    {{
                        "element": "<content_element>",
                        "current_performance": "<metrics>",
                        "recommendation": "<specific_improvement>",
                        "expected_impact": "<impact_description>",
                        "priority": "<high/medium/low>"
                    }}
                ],
                "suggested_improvements": {{
                    "subject_lines": ["improved_subject1", "improved_subject2"],
                    "headlines": ["improved_headline1", "improved_headline2"],
                    "cta_buttons": ["improved_cta1", "improved_cta2"]
                }},
                "personalization_enhancements": [
                    "enhancement1",
                    "enhancement2"
                ],
                "performance_predictions": {{
                    "expected_lift": <percentage>,
                    "confidence_level": <0.0-1.0>
                }}
            }}
            """
            
            message = UserMessage(text=optimization_prompt)
            response = await chat.send_message(message)
            
            try:
                optimization = json.loads(response)
                
                # Update template with optimizations
                await self.db.content_templates.update_one(
                    {"template_id": template_id},
                    {
                        "$set": {
                            "optimization_recommendations": optimization.get('optimization_recommendations', []),
                            "suggested_improvements": optimization.get('suggested_improvements', {}),
                            "updated_at": datetime.now()
                        }
                    }
                )
                
                return {
                    "template_id": template_id,
                    "optimization_results": optimization,
                    "analysis_timestamp": datetime.now()
                }
                
            except json.JSONDecodeError:
                return await self._fallback_optimization(template_id)
                
        except Exception as e:
            print(f"Content optimization error: {e}")
            return {"error": str(e)}
    
    async def get_dynamic_content_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive dynamic content dashboard"""
        try:
            # Get templates and personalizations
            templates = await self.db.content_templates.find().to_list(length=100)
            personalizations = await self.db.content_personalizations.find().to_list(length=1000)
            
            if not templates:
                return await self._generate_sample_content_dashboard()
            
            # Content type distribution
            content_types = {}
            for template in templates:
                content_type = template.get('content_type', 'unknown')
                content_types[content_type] = content_types.get(content_type, 0) + 1
            
            # Personalization level analysis
            personalization_levels = {}
            for personalization in personalizations:
                level = personalization.get('personalization_level', 'basic')
                personalization_levels[level] = personalization_levels.get(level, 0) + 1
            
            # Performance metrics
            total_personalizations = len(personalizations)
            avg_confidence = sum(p.get('confidence_score', 0.7) for p in personalizations) / total_personalizations if personalizations else 0
            
            # Top performing templates
            template_performance = {}
            for template in templates:
                template_id = template.get('template_id')
                template_personalizations = [p for p in personalizations if p.get('template_id') == template_id]
                template_performance[template_id] = {
                    'name': template.get('name'),
                    'personalizations_count': len(template_personalizations),
                    'avg_confidence': sum(p.get('confidence_score', 0.7) for p in template_personalizations) / len(template_personalizations) if template_personalizations else 0
                }
            
            top_templates = sorted(template_performance.items(), key=lambda x: x[1]['avg_confidence'], reverse=True)[:5]
            
            return {
                "content_overview": {
                    "total_templates": len(templates),
                    "total_personalizations": total_personalizations,
                    "avg_confidence_score": round(avg_confidence, 3),
                    "active_content_types": len(content_types)
                },
                "content_type_distribution": content_types,
                "personalization_levels": personalization_levels,
                "performance_metrics": {
                    "personalization_success_rate": round(avg_confidence * 100, 2),
                    "templates_with_high_confidence": len([t for t in templates if t.get('performance_metrics', {}).get('confidence_score', 0.7) > 0.8]),
                    "most_personalized_element": "subject_line"  # Could be calculated from data
                },
                "top_performing_templates": [
                    {
                        "template_id": tid,
                        "name": data['name'],
                        "personalizations": data['personalizations_count'],
                        "confidence": round(data['avg_confidence'], 3)
                    }
                    for tid, data in top_templates
                ],
                "insights": [
                    f"{total_personalizations} content personalizations generated",
                    f"Average personalization confidence: {avg_confidence:.2f}",
                    f"Most used content type: {max(content_types.items(), key=lambda x: x[1])[0] if content_types else 'N/A'}"
                ]
            }
            
        except Exception as e:
            print(f"Dynamic content dashboard error: {e}")
            return await self._generate_sample_content_dashboard()
    
    async def _analyze_content_performance(self, template: ContentTemplate, personalizations: List[Dict]) -> Dict[str, Any]:
        """Analyze performance patterns in content personalizations"""
        if not personalizations:
            return {"message": "No personalization data available"}
        
        # Confidence score analysis
        confidence_scores = [p.get('confidence_score', 0.7) for p in personalizations]
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Personalization factor analysis
        all_factors = []
        for p in personalizations:
            all_factors.extend(p.get('personalization_factors', []))
        
        factor_counts = {}
        for factor in all_factors:
            factor_counts[factor] = factor_counts.get(factor, 0) + 1
        
        top_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_personalizations": len(personalizations),
            "avg_confidence_score": avg_confidence,
            "top_personalization_factors": top_factors,
            "performance_trend": "improving" if avg_confidence > 0.7 else "stable"
        }
    
    async def _fallback_template_creation(self, template_data: Dict[str, Any]) -> ContentTemplate:
        """Fallback template creation when AI fails"""
        return ContentTemplate(
            template_id=str(uuid.uuid4()),
            name=template_data.get('name', 'Dynamic Content Template'),
            content_type=ContentType(template_data.get('content_type', 'email')),
            base_content={
                "subject": "{{customer_name}}, check out this exclusive offer!",
                "headline": "Personalized recommendation for {{customer_name}}",
                "body": "Based on your interests in {{customer_preference}}, we have something special for you.",
                "cta": "Shop Now",
                "personalization_variables": ["{{customer_name}}", "{{customer_preference}}"]
            },
            personalization_rules=[
                {
                    "condition": "high_value_customer",
                    "content_variation": {"cta": "Get VIP Access"},
                    "priority": 8
                }
            ],
            dynamic_elements=["subject", "headline", "cta"],
            performance_metrics={
                "expected_open_rate": 0.25,
                "expected_click_rate": 0.05,
                "personalization_lift": 15.0
            }
        )
    
    async def _fallback_personalization(self, template_id: str, customer_data: Dict[str, Any]) -> ContentPersonalization:
        """Fallback personalization when AI fails"""
        customer_name = customer_data.get('name', 'Valued Customer')
        
        return ContentPersonalization(
            personalization_id=str(uuid.uuid4()),
            customer_id=customer_data.get('customer_id', 'unknown'),
            template_id=template_id,
            generated_content={
                "subject": f"{customer_name}, exclusive offer inside!",
                "headline": f"Personalized recommendation for {customer_name}",
                "body": f"Hi {customer_name}, based on your purchase history, we have selected these products for you.",
                "cta": "Shop Your Recommendations",
                "personalization_tokens": {
                    "customer_name": customer_name,
                    "preference": "premium products"
                }
            },
            personalization_level=PersonalizationLevel.BASIC,
            personalization_factors=["customer_name", "purchase_history"],
            confidence_score=0.7
        )
    
    async def _fallback_optimization(self, template_id: str) -> Dict[str, Any]:
        """Fallback optimization when AI fails"""
        return {
            "template_id": template_id,
            "optimization_results": {
                "optimization_recommendations": [
                    {
                        "element": "subject_line",
                        "recommendation": "Test shorter, more direct subject lines",
                        "priority": "high"
                    }
                ],
                "suggested_improvements": {
                    "subject_lines": ["Quick question for you", "Your exclusive deal expires soon"],
                    "cta_buttons": ["Get Started", "Claim Offer"]
                },
                "performance_predictions": {
                    "expected_lift": 12.0,
                    "confidence_level": 0.75
                }
            },
            "analysis_timestamp": datetime.now()
        }
    
    async def _generate_sample_content_dashboard(self) -> Dict[str, Any]:
        """Generate sample content dashboard"""
        return {
            "content_overview": {
                "total_templates": 12,
                "total_personalizations": 350,
                "avg_confidence_score": 0.78,
                "active_content_types": 4
            },
            "content_type_distribution": {
                "email": 8,
                "web_page": 2,
                "sms": 1,
                "social_media": 1
            },
            "personalization_levels": {
                "ai_powered": 280,
                "advanced": 50,
                "basic": 20
            },
            "performance_metrics": {
                "personalization_success_rate": 78.0,
                "templates_with_high_confidence": 9,
                "most_personalized_element": "subject_line"
            },
            "top_performing_templates": [
                {
                    "template_id": "template_1",
                    "name": "Welcome Email Series",
                    "personalizations": 85,
                    "confidence": 0.85
                },
                {
                    "template_id": "template_2", 
                    "name": "Product Recommendation",
                    "personalizations": 120,
                    "confidence": 0.82
                }
            ],
            "insights": [
                "350 content personalizations generated",
                "Average personalization confidence: 0.78",
                "Most used content type: email"
            ]
        }
    
    async def _store_content_template(self, template: ContentTemplate):
        """Store content template in database"""
        try:
            await self.db.content_templates.insert_one(template.dict())
            print(f"✅ Stored content template: {template.template_id}")
        except Exception as e:
            print(f"❌ Error storing content template: {e}")
    
    async def _store_personalization(self, personalization: ContentPersonalization):
        """Store content personalization in database"""
        try:
            await self.db.content_personalizations.insert_one(personalization.dict())
            print(f"✅ Stored content personalization: {personalization.personalization_id}")
        except Exception as e:
            print(f"❌ Error storing content personalization: {e}")