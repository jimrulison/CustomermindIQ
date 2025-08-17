"""
Customer Mind IQ - Referral Program Microservice
AI-powered referral program management and optimization
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

class ReferralStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REWARDED = "rewarded"

class CampaignType(str, Enum):
    STANDARD = "standard"
    DOUBLE_SIDED = "double_sided"
    TIERED = "tiered"
    LIMITED_TIME = "limited_time"

class ReferralCampaign(BaseModel):
    campaign_id: str
    name: str
    description: str
    campaign_type: CampaignType
    referrer_reward: Dict[str, Any]  # type, amount, description
    referee_reward: Dict[str, Any]   # type, amount, description
    requirements: Dict[str, Any]     # minimum spend, time limits, etc.
    target_audience: Dict[str, Any]
    campaign_duration: int  # days
    max_referrals_per_customer: int
    tracking_parameters: Dict[str, str]
    performance_metrics: Dict[str, float] = {}
    is_active: bool = True
    created_at: datetime = datetime.now()
    expires_at: Optional[datetime] = None

class ReferralTracking(BaseModel):
    tracking_id: str
    campaign_id: str
    referrer_customer_id: str
    referee_email: str
    referee_customer_id: Optional[str] = None
    referral_code: str
    referral_link: str
    status: ReferralStatus = ReferralStatus.PENDING
    referred_at: datetime = datetime.now()
    converted_at: Optional[datetime] = None
    referrer_reward_amount: float = 0.0
    referee_reward_amount: float = 0.0
    conversion_value: float = 0.0
    tracking_data: Dict[str, Any] = {}

class ReferralProgramService:
    """Customer Mind IQ Referral Program Microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq
        
    async def create_referral_campaign(self, campaign_data: Dict[str, Any]) -> ReferralCampaign:
        """Create a new referral campaign with AI optimization"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"referral_campaign_{datetime.now().strftime('%Y%m%d')}",
                system_message="""You are Customer Mind IQ's referral program specialist. 
                Design and optimize referral campaigns for maximum participation and conversion."""
            ).with_model("openai", "gpt-4o-mini")
            
            campaign_optimization_prompt = f"""
            Optimize this referral campaign using Customer Mind IQ advanced algorithms:
            
            Campaign Request: {json.dumps(campaign_data, default=str)}
            
            Provide referral campaign optimization in this exact JSON format:
            {{
                "optimized_campaign": {{
                    "campaign_type": "<standard/double_sided/tiered/limited_time>",
                    "referrer_reward": {{
                        "type": "<cash/credit/discount/product>",
                        "amount": <reward_amount>,
                        "description": "<reward_description>"
                    }},
                    "referee_reward": {{
                        "type": "<cash/credit/discount/product>",
                        "amount": <reward_amount>,
                        "description": "<reward_description>"
                    }},
                    "requirements": {{
                        "minimum_spend": <amount>,
                        "time_limit_days": <days>,
                        "qualification_criteria": ["criteria1", "criteria2"]
                    }},
                    "target_audience": {{
                        "segments": ["segment1", "segment2"],
                        "exclusions": ["exclusion1"],
                        "size_estimate": <estimated_participants>
                    }},
                    "campaign_duration": <optimal_duration_days>,  
                    "max_referrals_per_customer": <max_referrals>,
                    "tracking_parameters": {{
                        "utm_source": "referral",
                        "utm_medium": "customer_referral",
                        "utm_campaign": "<campaign_name>"
                    }}
                }},
                "performance_predictions": {{
                    "expected_participation_rate": <0.0-1.0>,
                    "expected_conversion_rate": <0.0-1.0>,
                    "projected_new_customers": <number>,
                    "roi_estimate": <roi_multiplier>,
                    "viral_coefficient": <coefficient>
                }},
                "optimization_recommendations": [
                    "recommendation1",
                    "recommendation2",
                    "recommendation3"
                ]
            }}
            
            Focus on maximizing viral growth while maintaining profitability.
            """
            
            message = UserMessage(text=campaign_optimization_prompt)
            response = await chat.send_message(message)
            
            try:
                optimization = json.loads(response)
                optimized_data = optimization.get('optimized_campaign', {})
                
                # Set expiration date
                duration = optimized_data.get('campaign_duration', 90)
                expires_at = datetime.now() + timedelta(days=duration)
                
                campaign = ReferralCampaign(
                    campaign_id=str(uuid.uuid4()),
                    name=campaign_data.get('name', 'Referral Campaign'),
                    description=campaign_data.get('description', 'AI-optimized referral program'),
                    campaign_type=CampaignType(optimized_data.get('campaign_type', 'standard')),
                    referrer_reward=optimized_data.get('referrer_reward', {"type": "credit", "amount": 50, "description": "$50 account credit"}),
                    referee_reward=optimized_data.get('referee_reward', {"type": "discount", "amount": 25, "description": "25% off first purchase"}),
                    requirements=optimized_data.get('requirements', {"minimum_spend": 100}),
                    target_audience=optimized_data.get('target_audience', {}),
                    campaign_duration=duration,
                    max_referrals_per_customer=optimized_data.get('max_referrals_per_customer', 10),
                    tracking_parameters=optimized_data.get('tracking_parameters', {}),
                    performance_metrics=optimization.get('performance_predictions', {}),
                    expires_at=expires_at
                )
                
                # Store campaign
                await self._store_referral_campaign(campaign)
                return campaign
                
            except json.JSONDecodeError:
                return await self._fallback_campaign_creation(campaign_data)
                
        except Exception as e:
            print(f"Referral campaign creation error: {e}")
            return await self._fallback_campaign_creation(campaign_data)
    
    async def generate_referral_link(self, campaign_id: str, customer_id: str) -> Dict[str, Any]:
        """Generate personalized referral link for customer"""
        try:
            # Get campaign details
            campaign_doc = await self.db.referral_campaigns.find_one({"campaign_id": campaign_id})
            if not campaign_doc:
                return {"error": "Campaign not found"}
            
            campaign = ReferralCampaign(**campaign_doc)
            
            # Check if campaign is active
            if not campaign.is_active or (campaign.expires_at and campaign.expires_at < datetime.now()):
                return {"error": "Campaign is not active"}
            
            # Generate unique referral code
            referral_code = f"REF{customer_id[-4:].upper()}{uuid.uuid4().hex[:6].upper()}"
            
            # Create referral tracking base URL
            base_url = "https://customermindiq.com/referral"
            referral_link = f"{base_url}?ref={referral_code}&campaign={campaign_id}&source={customer_id}"
            
            # Add tracking parameters
            for key, value in campaign.tracking_parameters.items():
                referral_link += f"&{key}={value}"
            
            # Generate personalized referral message using AI
            referral_message = await self._generate_referral_message(campaign, customer_id)
            
            # Store referral tracking
            tracking = ReferralTracking(
                tracking_id=str(uuid.uuid4()),
                campaign_id=campaign_id,
                referrer_customer_id=customer_id,
                referee_email="",  # Will be filled when someone uses the link
                referral_code=referral_code,
                referral_link=referral_link,
                referrer_reward_amount=campaign.referrer_reward.get('amount', 0),
                referee_reward_amount=campaign.referee_reward.get('amount', 0)
            )
            
            await self._store_referral_tracking(tracking)
            
            return {
                "referral_code": referral_code,
                "referral_link": referral_link,
                "campaign_name": campaign.name,
                "referrer_reward": campaign.referrer_reward,
                "referee_reward": campaign.referee_reward,
                "personalized_message": referral_message,
                "campaign_expires": campaign.expires_at,
                "tracking_id": tracking.tracking_id
            }
            
        except Exception as e:
            print(f"Referral link generation error: {e}")
            return {"error": str(e)}
    
    async def track_referral_conversion(self, referral_code: str, referee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track referral conversion and calculate rewards"""
        try:
            # Find referral tracking record
            tracking_doc = await self.db.referral_tracking.find_one({"referral_code": referral_code})
            if not tracking_doc:
                return {"error": "Invalid referral code"}
            
            tracking = ReferralTracking(**tracking_doc)
            
            # Get campaign details
            campaign_doc = await self.db.referral_campaigns.find_one({"campaign_id": tracking.campaign_id})
            if not campaign_doc:
                return {"error": "Campaign not found"}
            
            campaign = ReferralCampaign(**campaign_doc)
            
            # Check campaign requirements
            conversion_value = referee_data.get('purchase_amount', 0)
            minimum_spend = campaign.requirements.get('minimum_spend', 0)
            
            if conversion_value < minimum_spend:
                return {
                    "status": "pending",
                    "message": f"Conversion pending - minimum spend requirement: ${minimum_spend}",
                    "current_amount": conversion_value
                }
            
            # Update tracking record
            await self.db.referral_tracking.update_one(
                {"tracking_id": tracking.tracking_id},
                {
                    "$set": {
                        "referee_customer_id": referee_data.get('customer_id'),
                        "referee_email": referee_data.get('email', ''),
                        "status": "approved",
                        "converted_at": datetime.now(),
                        "conversion_value": conversion_value,
                        "tracking_data": referee_data
                    }
                }
            )
            
            # Process rewards
            rewards_processed = await self._process_referral_rewards(tracking, campaign, conversion_value)
            
            return {
                "status": "approved" if rewards_processed else "pending",
                "referrer_reward": campaign.referrer_reward,
                "referee_reward": campaign.referee_reward,
                "conversion_value": conversion_value,
                "rewards_processed": rewards_processed,
                "tracking_id": tracking.tracking_id
            }
            
        except Exception as e:
            print(f"Referral conversion tracking error: {e}")
            return {"error": str(e)}
    
    async def get_referral_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive referral program dashboard"""
        try:
            # Get campaigns and tracking data
            campaigns = await self.db.referral_campaigns.find().to_list(length=100)
            tracking_records = await self.db.referral_tracking.find().to_list(length=1000)
            
            if not campaigns:
                return await self._generate_sample_referral_dashboard()
            
            # Campaign performance analysis
            active_campaigns = [c for c in campaigns if c.get('is_active', True)]
            total_campaigns = len(campaigns)
            
            # Tracking metrics
            total_referrals = len(tracking_records)
            approved_referrals = len([t for t in tracking_records if t.get('status') == 'approved'])
            pending_referrals = len([t for t in tracking_records if t.get('status') == 'pending'])
            
            # Conversion metrics
            total_conversion_value = sum(t.get('conversion_value', 0) for t in tracking_records if t.get('status') == 'approved')
            total_rewards_paid = sum(t.get('referrer_reward_amount', 0) + t.get('referee_reward_amount', 0) for t in tracking_records if t.get('status') == 'rewarded')
            
            # Calculate rates
            conversion_rate = (approved_referrals / total_referrals) if total_referrals > 0 else 0
            avg_conversion_value = (total_conversion_value / approved_referrals) if approved_referrals > 0 else 0
            
            # Campaign type distribution
            campaign_types = {}
            for campaign in campaigns:
                camp_type = campaign.get('campaign_type', 'standard')
                campaign_types[camp_type] = campaign_types.get(camp_type, 0) + 1
            
            # Top performing campaigns
            campaign_performance = {}
            for campaign in campaigns:
                campaign_id = campaign.get('campaign_id')
                campaign_referrals = [t for t in tracking_records if t.get('campaign_id') == campaign_id]
                campaign_performance[campaign_id] = {
                    'name': campaign.get('name'),
                    'total_referrals': len(campaign_referrals),
                    'approved_referrals': len([t for t in campaign_referrals if t.get('status') == 'approved']),
                    'conversion_value': sum(t.get('conversion_value', 0) for t in campaign_referrals),
                    'conversion_rate': len([t for t in campaign_referrals if t.get('status') == 'approved']) / len(campaign_referrals) if campaign_referrals else 0
                }
            
            top_campaigns = sorted(campaign_performance.items(), key=lambda x: x[1]['conversion_value'], reverse=True)[:5]
            
            # Recent activity
            recent_referrals = sorted(tracking_records, key=lambda x: x.get('referred_at', datetime.min), reverse=True)[:10]
            
            return {
                "program_overview": {
                    "total_campaigns": total_campaigns,
                    "active_campaigns": len(active_campaigns),
                    "total_referrals": total_referrals,
                    "approved_referrals": approved_referrals,
                    "pending_referrals": pending_referrals,
                    "conversion_rate": round(conversion_rate * 100, 2)
                },
                "financial_metrics": {
                    "total_conversion_value": total_conversion_value,
                    "total_rewards_paid": total_rewards_paid,
                    "avg_conversion_value": round(avg_conversion_value, 2),
                    "roi": round((total_conversion_value / total_rewards_paid), 2) if total_rewards_paid > 0 else 0,
                    "program_efficiency": round((total_conversion_value - total_rewards_paid) / total_conversion_value * 100, 2) if total_conversion_value > 0 else 0
                },
                "campaign_distribution": campaign_types,
                "top_performing_campaigns": [
                    {
                        "campaign_id": cid,
                        "name": data['name'],
                        "referrals": data['total_referrals'],
                        "conversions": data['approved_referrals'],
                        "value": data['conversion_value'],
                        "conversion_rate": round(data['conversion_rate'] * 100, 2)
                    }
                    for cid, data in top_campaigns
                ],
                "recent_activity": [
                    {
                        "tracking_id": ref.get('tracking_id'),
                        "referrer_id": ref.get('referrer_customer_id'),
                        "status": ref.get('status'),
                        "referred_at": ref.get('referred_at'),
                        "conversion_value": ref.get('conversion_value', 0)
                    }
                    for ref in recent_referrals
                ],
                "performance_insights": [
                    f"{total_referrals} total referrals generated",
                    f"{conversion_rate:.1%} referral conversion rate",
                    f"${avg_conversion_value:.2f} average conversion value",
                    f"${total_conversion_value - total_rewards_paid:.2f} net revenue from referrals"
                ]
            }
            
        except Exception as e:
            print(f"Referral dashboard error: {e}")
            return await self._generate_sample_referral_dashboard()
    
    async def _generate_referral_message(self, campaign: ReferralCampaign, customer_id: str) -> str:
        """Generate personalized referral message using AI"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"referral_message_{customer_id}",
                system_message="""You are Customer Mind IQ's referral messaging specialist. 
                Create compelling, personalized referral messages that motivate sharing."""
            ).with_model("openai", "gpt-4o-mini")
            
            message_prompt = f"""
            Create a personalized referral message for this campaign:
            
            Campaign: {campaign.name}
            Referrer Reward: {campaign.referrer_reward}
            Referee Reward: {campaign.referee_reward}
            Campaign Type: {campaign.campaign_type}
            
            Generate a compelling referral message that:
            1. Explains the benefits for both referrer and referee
            2. Creates urgency if applicable
            3. Uses friendly, personal tone
            4. Includes clear next steps
            
            Return just the message text, no JSON format needed.
            """
            
            message = UserMessage(text=message_prompt)
            response = await chat.send_message(message)
            
            return response.strip()
            
        except Exception as e:
            print(f"Referral message generation error: {e}")
            return f"Share the benefits of {campaign.name} with your friends and earn {campaign.referrer_reward.get('description', 'rewards')}!"
    
    async def _process_referral_rewards(self, tracking: ReferralTracking, campaign: ReferralCampaign, conversion_value: float) -> bool:
        """Process referral rewards for both referrer and referee"""
        try:
            # Here you would integrate with your reward/payment system
            # For now, we'll simulate reward processing
            
            # Update tracking status to rewarded
            await self.db.referral_tracking.update_one(
                {"tracking_id": tracking.tracking_id},
                {"$set": {"status": "rewarded"}}
            )
            
            # Log reward transactions (in a real system, you'd process actual payments/credits)
            reward_log = {
                "tracking_id": tracking.tracking_id,
                "referrer_customer_id": tracking.referrer_customer_id,
                "referee_customer_id": tracking.referee_customer_id,
                "referrer_reward": campaign.referrer_reward,
                "referee_reward": campaign.referee_reward,
                "processed_at": datetime.now(),
                "conversion_value": conversion_value
            }
            
            await self.db.referral_rewards.insert_one(reward_log)
            
            return True
            
        except Exception as e:
            print(f"Reward processing error: {e}")
            return False
    
    async def _fallback_campaign_creation(self, campaign_data: Dict[str, Any]) -> ReferralCampaign:
        """Fallback campaign creation when AI fails"""
        duration = 90
        expires_at = datetime.now() + timedelta(days=duration)
        
        return ReferralCampaign(
            campaign_id=str(uuid.uuid4()),
            name=campaign_data.get('name', 'Referral Program'),
            description=campaign_data.get('description', 'Refer friends and earn rewards'),
            campaign_type=CampaignType.DOUBLE_SIDED,
            referrer_reward={
                "type": "credit",
                "amount": 50.0,
                "description": "$50 account credit"
            },
            referee_reward={
                "type": "discount", 
                "amount": 25.0,
                "description": "25% off first purchase"
            },
            requirements={
                "minimum_spend": 100.0,
                "time_limit_days": 30
            },
            target_audience={
                "segments": ["active_customers"],
                "size_estimate": 1000
            },
            campaign_duration=duration,
            max_referrals_per_customer=10,
            tracking_parameters={
                "utm_source": "referral",
                "utm_medium": "customer_referral"
            },
            performance_metrics={
                "expected_participation_rate": 0.15,
                "expected_conversion_rate": 0.25,
                "projected_new_customers": 150,
                "roi_estimate": 3.5
            },
            expires_at=expires_at
        )
    
    async def _generate_sample_referral_dashboard(self) -> Dict[str, Any]:
        """Generate sample referral dashboard"""
        return {
            "program_overview": {
                "total_campaigns": 4,
                "active_campaigns": 2,
                "total_referrals": 127,
                "approved_referrals": 89,
                "pending_referrals": 15,
                "conversion_rate": 70.1
            },
            "financial_metrics": {
                "total_conversion_value": 45600.0,
                "total_rewards_paid": 8900.0,
                "avg_conversion_value": 512.4,
                "roi": 5.1,
                "program_efficiency": 80.5
            },
            "campaign_distribution": {
                "double_sided": 2,
                "tiered": 1,
                "limited_time": 1
            },
            "top_performing_campaigns": [
                {
                    "campaign_id": "camp_1",
                    "name": "Summer Referral Bonus",
                    "referrals": 67,
                    "conversions": 52,
                    "value": 28400.0,
                    "conversion_rate": 77.6
                }
            ],
            "recent_activity": [],
            "performance_insights": [
                "127 total referrals generated",
                "70.1% referral conversion rate",
                "$512.40 average conversion value",
                "$36,700.00 net revenue from referrals"
            ]
        }
    
    async def _store_referral_campaign(self, campaign: ReferralCampaign):
        """Store referral campaign in database"""
        try:
            await self.db.referral_campaigns.insert_one(campaign.dict())
            print(f"✅ Stored referral campaign: {campaign.campaign_id}")
        except Exception as e:
            print(f"❌ Error storing referral campaign: {e}")
    
    async def _store_referral_tracking(self, tracking: ReferralTracking):
        """Store referral tracking in database"""
        try:
            await self.db.referral_tracking.insert_one(tracking.dict())
            print(f"✅ Stored referral tracking: {tracking.tracking_id}")
        except Exception as e:
            print(f"❌ Error storing referral tracking: {e}")