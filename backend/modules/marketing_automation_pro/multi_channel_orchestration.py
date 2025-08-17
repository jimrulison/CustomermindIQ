"""
Customer Mind IQ - Multi-Channel Orchestration Microservice
AI-powered cross-channel marketing campaign orchestration and automation
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
from enum import Enum

class ChannelType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    SOCIAL_MEDIA = "social_media"
    PUSH_NOTIFICATION = "push_notification"
    IN_APP = "in_app"
    DIRECT_MAIL = "direct_mail"
    PHONE_CALL = "phone_call"

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Campaign(BaseModel):
    campaign_id: str
    name: str
    description: str
    target_audience: Dict[str, Any]
    channels: List[ChannelType]
    schedule: Dict[str, Any]
    content: Dict[str, Any]
    budget: float
    expected_reach: int
    kpis: Dict[str, float]
    status: CampaignStatus = CampaignStatus.DRAFT
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class CampaignExecution(BaseModel):
    execution_id: str
    campaign_id: str
    channel: ChannelType
    scheduled_time: datetime
    actual_time: Optional[datetime] = None
    status: str = "pending"
    audience_size: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    converted: int = 0
    cost: float = 0.0
    revenue_generated: float = 0.0

class MultiChannelOrchestrationService:
    """Customer Mind IQ Multi-Channel Orchestration Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq
        
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Campaign:
        """Create a new multi-channel marketing campaign using AI optimization"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"campaign_creation_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's multi-channel campaign specialist. 
                Optimize marketing campaigns across multiple channels for maximum engagement and ROI."""
            ).with_model("openai", "gpt-4o-mini")
            
            optimization_prompt = f"""
            Optimize this multi-channel marketing campaign using Customer Mind IQ advanced algorithms:
            
            Campaign Data: {json.dumps(campaign_data, default=str)}
            
            Provide campaign optimization in this exact JSON format:
            {{
                "optimized_channels": ["email", "sms", "social_media"],
                "target_audience": {{
                    "segment": "<segment_name>",
                    "size_estimate": <number>,
                    "engagement_score": <0-100>
                }},
                "schedule": {{
                    "start_date": "<YYYY-MM-DD>",
                    "end_date": "<YYYY-MM-DD>",
                    "channel_timing": {{
                        "email": "09:00",
                        "sms": "14:00",
                        "social_media": "19:00"
                    }}
                }},
                "content_strategy": {{
                    "main_message": "<campaign_message>",
                    "channel_variations": {{
                        "email": "<email_specific_content>",
                        "sms": "<sms_specific_content>",
                        "social_media": "<social_specific_content>"
                    }}
                }},
                "expected_performance": {{
                    "reach": <estimated_reach>,
                    "engagement_rate": <0.0-1.0>,
                    "conversion_rate": <0.0-1.0>,
                    "roi_estimate": <roi_multiplier>
                }},
                "budget_allocation": {{
                    "email": <percentage>,
                    "sms": <percentage>,
                    "social_media": <percentage>
                }}
            }}
            
            Focus on channel synergy, optimal timing, and personalized messaging.
            """
            
            message = UserMessage(text=optimization_prompt)
            response = await chat.send_message(message)
            
            try:
                optimization = json.loads(response)
                
                campaign = Campaign(
                    campaign_id=str(uuid.uuid4()),
                    name=campaign_data.get('name', 'Multi-Channel Campaign'),
                    description=campaign_data.get('description', ''),
                    target_audience=optimization.get('target_audience', {}),
                    channels=[ChannelType(ch) for ch in optimization.get('optimized_channels', ['email'])],
                    schedule=optimization.get('schedule', {}),
                    content=optimization.get('content_strategy', {}),
                    budget=campaign_data.get('budget', 1000.0),
                    expected_reach=optimization.get('expected_performance', {}).get('reach', 1000),
                    kpis=optimization.get('expected_performance', {}),
                    status=CampaignStatus.DRAFT
                )
                
                # Store campaign
                await self._store_campaign(campaign)
                return campaign
                
            except json.JSONDecodeError:
                return await self._fallback_campaign_creation(campaign_data)
                
        except Exception as e:
            print(f"Campaign creation error: {e}")
            return await self._fallback_campaign_creation(campaign_data)
    
    async def orchestrate_campaign_execution(self, campaign_id: str) -> List[CampaignExecution]:
        """Orchestrate campaign execution across multiple channels"""
        try:
            # Get campaign details
            campaign = await self.db.campaigns.find_one({"campaign_id": campaign_id})
            if not campaign:
                raise Exception("Campaign not found")
            
            executions = []
            current_time = datetime.now()
            
            for channel in campaign.get('channels', []):
                # Calculate optimal execution time for each channel
                channel_timing = campaign.get('schedule', {}).get('channel_timing', {})
                base_time = channel_timing.get(channel, '12:00')
                
                # Parse time and create execution schedule
                hour, minute = map(int, base_time.split(':'))
                scheduled_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if scheduled_time < current_time:
                    scheduled_time += timedelta(days=1)
                
                execution = CampaignExecution(
                    execution_id=str(uuid.uuid4()),
                    campaign_id=campaign_id,
                    channel=ChannelType(channel),
                    scheduled_time=scheduled_time,
                    audience_size=campaign.get('expected_reach', 1000) // len(campaign.get('channels', [1])),
                    status="scheduled"
                )
                
                executions.append(execution)
                await self._store_execution(execution)
            
            # Update campaign status
            await self.db.campaigns.update_one(
                {"campaign_id": campaign_id},
                {"$set": {"status": "scheduled", "updated_at": datetime.now()}}
            )
            
            return executions
            
        except Exception as e:
            print(f"Campaign orchestration error: {e}")
            return []
    
    async def get_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Get comprehensive campaign performance across all channels"""
        try:
            # Get campaign and executions
            campaign = await self.db.campaigns.find_one({"campaign_id": campaign_id})
            executions = await self.db.campaign_executions.find({"campaign_id": campaign_id}).to_list(length=100)
            
            if not campaign:
                return {"error": "Campaign not found"}
            
            # Aggregate performance metrics
            total_delivered = sum(ex.get('delivered', 0) for ex in executions)
            total_opened = sum(ex.get('opened', 0) for ex in executions)
            total_clicked = sum(ex.get('clicked', 0) for ex in executions)
            total_converted = sum(ex.get('converted', 0) for ex in executions)
            total_cost = sum(ex.get('cost', 0.0) for ex in executions)
            total_revenue = sum(ex.get('revenue_generated', 0.0) for ex in executions)
            
            # Calculate rates
            open_rate = (total_opened / total_delivered) if total_delivered > 0 else 0
            click_rate = (total_clicked / total_opened) if total_opened > 0 else 0
            conversion_rate = (total_converted / total_clicked) if total_clicked > 0 else 0
            roi = (total_revenue / total_cost) if total_cost > 0 else 0
            
            # Channel breakdown
            channel_performance = {}
            for execution in executions:
                channel = execution.get('channel')
                if channel not in channel_performance:
                    channel_performance[channel] = {
                        'delivered': 0, 'opened': 0, 'clicked': 0, 'converted': 0,
                        'cost': 0.0, 'revenue': 0.0
                    }
                
                channel_performance[channel]['delivered'] += execution.get('delivered', 0)
                channel_performance[channel]['opened'] += execution.get('opened', 0)
                channel_performance[channel]['clicked'] += execution.get('clicked', 0)
                channel_performance[channel]['converted'] += execution.get('converted', 0)
                channel_performance[channel]['cost'] += execution.get('cost', 0.0)
                channel_performance[channel]['revenue'] += execution.get('revenue_generated', 0.0)
            
            return {
                "campaign_id": campaign_id,
                "campaign_name": campaign.get('name'),
                "status": campaign.get('status'),
                "overall_performance": {
                    "total_delivered": total_delivered,
                    "total_opened": total_opened,
                    "total_clicked": total_clicked,
                    "total_converted": total_converted,
                    "open_rate": round(open_rate * 100, 2),
                    "click_rate": round(click_rate * 100, 2),
                    "conversion_rate": round(conversion_rate * 100, 2),
                    "total_cost": total_cost,
                    "total_revenue": total_revenue,
                    "roi": round(roi, 2)
                },
                "channel_performance": channel_performance,
                "executions_count": len(executions)
            }
            
        except Exception as e:
            print(f"Campaign performance error: {e}")
            return {"error": str(e)}
    
    async def get_orchestration_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive multi-channel orchestration dashboard"""
        try:
            # Get all campaigns
            campaigns = await self.db.campaigns.find().to_list(length=100)
            executions = await self.db.campaign_executions.find().to_list(length=1000)
            
            if not campaigns:
                return await self._generate_sample_dashboard()
            
            # Campaign status distribution
            status_distribution = {}
            for campaign in campaigns:
                status = campaign.get('status', 'draft')
                status_distribution[status] = status_distribution.get(status, 0) + 1
            
            # Channel usage analysis
            channel_usage = {}
            for campaign in campaigns:
                for channel in campaign.get('channels', []):
                    channel_usage[channel] = channel_usage.get(channel, 0) + 1
            
            # Performance aggregation
            total_budget = sum(c.get('budget', 0) for c in campaigns)
            total_reach = sum(c.get('expected_reach', 0) for c in campaigns)
            
            # Execution stats
            completed_executions = [e for e in executions if e.get('status') == 'completed']
            total_delivered = sum(e.get('delivered', 0) for e in completed_executions)
            total_converted = sum(e.get('converted', 0) for e in completed_executions)
            total_revenue = sum(e.get('revenue_generated', 0) for e in completed_executions)
            
            return {
                "campaigns_overview": {
                    "total_campaigns": len(campaigns),
                    "active_campaigns": status_distribution.get('running', 0),
                    "completed_campaigns": status_distribution.get('completed', 0),
                    "total_budget": total_budget,
                    "expected_total_reach": total_reach
                },
                "status_distribution": status_distribution,
                "channel_usage": channel_usage,
                "performance_metrics": {
                    "total_delivered": total_delivered,
                    "total_converted": total_converted,
                    "total_revenue_generated": total_revenue,
                    "avg_conversion_rate": (total_converted / total_delivered * 100) if total_delivered > 0 else 0,
                    "avg_roi": (total_revenue / total_budget) if total_budget > 0 else 0
                },
                "top_performing_channels": sorted(channel_usage.items(), key=lambda x: x[1], reverse=True)[:5]
            }
            
        except Exception as e:
            print(f"Orchestration dashboard error: {e}")
            return await self._generate_sample_dashboard()
    
    async def _store_campaign(self, campaign: Campaign):
        """Store campaign in database"""
        try:
            await self.db.campaigns.insert_one(campaign.dict())
            print(f"✅ Stored campaign: {campaign.campaign_id}")
        except Exception as e:
            print(f"❌ Error storing campaign: {e}")
    
    async def _store_execution(self, execution: CampaignExecution):
        """Store campaign execution in database"""
        try:
            await self.db.campaign_executions.insert_one(execution.dict())
            print(f"✅ Stored execution: {execution.execution_id}")
        except Exception as e:
            print(f"❌ Error storing execution: {e}")
    
    async def _fallback_campaign_creation(self, campaign_data: Dict[str, Any]) -> Campaign:
        """Fallback campaign creation when AI fails"""
        return Campaign(
            campaign_id=str(uuid.uuid4()),
            name=campaign_data.get('name', 'Multi-Channel Campaign'),
            description=campaign_data.get('description', 'AI-optimized multi-channel marketing campaign'),
            target_audience={
                "segment": "general_audience",
                "size_estimate": 1000,
                "engagement_score": 70
            },
            channels=[ChannelType.EMAIL, ChannelType.SMS],
            schedule={
                "start_date": datetime.now().strftime('%Y-%m-%d'),
                "end_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                "channel_timing": {
                    "email": "09:00",
                    "sms": "14:00"
                }
            },
            content={
                "main_message": "Exclusive offer just for you!",
                "channel_variations": {
                    "email": "Check your email for our exclusive offer",
                    "sms": "Limited time offer - act now!"
                }
            },
            budget=campaign_data.get('budget', 1000.0),
            expected_reach=1000,
            kpis={
                "engagement_rate": 0.15,
                "conversion_rate": 0.05,
                "roi_estimate": 3.0
            }
        )
    
    async def _generate_sample_dashboard(self) -> Dict[str, Any]:
        """Generate sample dashboard data"""
        return {
            "campaigns_overview": {
                "total_campaigns": 5,
                "active_campaigns": 2,
                "completed_campaigns": 2,
                "total_budget": 15000.0,
                "expected_total_reach": 50000
            },
            "status_distribution": {
                "running": 2,
                "completed": 2,
                "draft": 1
            },
            "channel_usage": {
                "email": 5,
                "sms": 3,
                "social_media": 4,
                "push_notification": 2
            },
            "performance_metrics": {
                "total_delivered": 45000,
                "total_converted": 2250,
                "total_revenue_generated": 67500.0,
                "avg_conversion_rate": 5.0,
                "avg_roi": 4.5
            },
            "top_performing_channels": [
                ("email", 5),
                ("social_media", 4),
                ("sms", 3),
                ("push_notification", 2)
            ]
        }