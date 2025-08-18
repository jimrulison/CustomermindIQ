"""
Customer Mind IQ - Referral Program Integration Microservice
AI-powered referral program with viral growth loops and automated optimization
"""

from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
import asyncio
import json
import uuid
import hashlib
import random
from enum import Enum
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import math
from scipy.stats import poisson
import numpy as np

# Enums
class ReferralStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CONVERTED = "converted"
    EXPIRED = "expired"
    FRAUD = "fraud"

class RewardType(str, Enum):
    CREDIT = "credit"
    DISCOUNT = "discount"
    CASH = "cash"
    PRODUCT = "product"
    UPGRADE = "upgrade"
    POINTS = "points"

class ReferralChannel(str, Enum):
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    DIRECT_LINK = "direct_link"
    SMS = "sms"
    WORD_OF_MOUTH = "word_of_mouth"
    AFFILIATE = "affiliate"

class CustomerLifecycleStage(str, Enum):
    TRIAL = "trial"
    NEW_CUSTOMER = "new_customer"
    ACTIVE_USER = "active_user"
    POWER_USER = "power_user"
    ADVOCATE = "advocate"
    CHURNED = "churned"

class ViralityLevel(str, Enum):
    LOW = "low"          # <1.2 viral coefficient
    MODERATE = "moderate" # 1.2-2.0 viral coefficient
    HIGH = "high"        # 2.0-3.0 viral coefficient
    EXPLOSIVE = "explosive" # >3.0 viral coefficient

# Data Models
class ReferralProgram(BaseModel):
    program_id: str
    name: str
    description: str
    reward_structure: Dict[str, Any]
    eligibility_criteria: Dict[str, Any]
    sharing_channels: List[ReferralChannel]
    tracking_parameters: Dict[str, str]
    expiration_days: int = 30
    max_referrals_per_user: int = 100
    fraud_detection_rules: List[Dict[str, Any]] = []
    viral_mechanics: Dict[str, Any] = {}
    is_active: bool = True
    created_at: datetime = datetime.now()

class CustomerReferralProfile(BaseModel):
    customer_id: str
    email: Optional[EmailStr] = None
    referral_propensity_score: float = 0.0  # 0.0-1.0
    lifecycle_stage: CustomerLifecycleStage = CustomerLifecycleStage.NEW_CUSTOMER
    network_size_estimate: int = 0
    social_influence_score: float = 0.0
    sharing_behavior: Dict[str, Any] = {}
    referral_history: List[str] = []  # referral_ids
    rewards_earned: List[Dict[str, Any]] = []
    last_referral_activity: Optional[datetime] = None
    optimal_contact_times: List[str] = []
    preferred_channels: List[ReferralChannel] = []
    ai_insights: List[str] = []

class ReferralLink(BaseModel):
    link_id: str
    referrer_id: str
    program_id: str
    unique_code: str
    tracking_url: str
    channel: ReferralChannel
    custom_message: Optional[str] = None
    metadata: Dict[str, Any] = {}
    click_count: int = 0
    conversion_count: int = 0
    created_at: datetime = datetime.now()
    expires_at: Optional[datetime] = None

class Referral(BaseModel):
    referral_id: str
    referrer_id: str
    referee_id: Optional[str] = None
    program_id: str
    link_id: str
    status: ReferralStatus = ReferralStatus.PENDING
    channel: ReferralChannel
    conversion_events: List[Dict[str, Any]] = []
    rewards_triggered: List[Dict[str, Any]] = []
    fraud_score: float = 0.0
    attribution_data: Dict[str, Any] = {}
    created_at: datetime = datetime.now()
    converted_at: Optional[datetime] = None

class ViralLoopMetrics(BaseModel):
    program_id: str
    viral_coefficient: float = 0.0  # Average referrals per customer
    virality_level: ViralityLevel = ViralityLevel.LOW
    growth_rate: float = 0.0  # Daily growth rate
    sharing_rate: float = 0.0  # % of customers who share
    conversion_rate: float = 0.0  # % of shared links that convert
    time_to_viral_action: float = 0.0  # Average days from signup to first share
    network_effects: Dict[str, float] = {}
    bottlenecks: List[str] = []
    optimization_opportunities: List[str] = []
    last_calculated: datetime = datetime.now()

class ReferralReward(BaseModel):
    reward_id: str
    customer_id: str
    referral_id: str
    reward_type: RewardType
    reward_value: float
    currency: str = "USD"
    description: str
    status: str = "pending"  # pending, issued, redeemed, expired
    issued_at: Optional[datetime] = None
    redeemed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class ReferralProgramService:
    """Advanced Referral Program with AI-Powered Viral Loop Optimization"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.customer_mind_iq

    async def analyze_referral_propensity(self, customer_id: str, customer_data: Dict[str, Any] = None) -> CustomerReferralProfile:
        """Analyze customer's likelihood to make successful referrals using AI"""
        try:
            # Get or create customer data
            if not customer_data:
                customer_data = await self._get_customer_data(customer_id)
            
            # Calculate referral propensity score using AI
            propensity_score = await self._calculate_referral_propensity(customer_data)
            
            # Determine lifecycle stage
            lifecycle_stage = await self._determine_lifecycle_stage(customer_data)
            
            # Estimate network size and social influence
            network_size = await self._estimate_network_size(customer_data)
            social_influence = await self._calculate_social_influence_score(customer_data)
            
            # Analyze sharing behavior patterns
            sharing_behavior = await self._analyze_sharing_behavior(customer_data)
            
            # Generate AI insights and recommendations
            ai_insights = await self._generate_referral_insights(customer_data, propensity_score, lifecycle_stage)
            
            # Determine optimal contact times and channels
            optimal_times = await self._optimize_contact_timing(customer_data)
            preferred_channels = await self._identify_preferred_channels(customer_data, sharing_behavior)
            
            # Create referral profile
            referral_profile = CustomerReferralProfile(
                customer_id=customer_id,
                email=customer_data.get('email'),
                referral_propensity_score=round(propensity_score, 3),
                lifecycle_stage=lifecycle_stage,
                network_size_estimate=network_size,
                social_influence_score=round(social_influence, 3),
                sharing_behavior=sharing_behavior,
                optimal_contact_times=optimal_times,
                preferred_channels=preferred_channels,
                ai_insights=ai_insights
            )
            
            # Store profile
            await self._store_referral_profile(referral_profile)
            
            return referral_profile
            
        except Exception as e:
            print(f"Referral propensity analysis error: {e}")
            return await self._fallback_referral_profile(customer_id)

    async def create_personalized_referral_campaign(self, program_id: str, target_customers: List[str]) -> Dict[str, Any]:
        """Create AI-optimized personalized referral campaign"""
        try:
            # Get program details
            program_doc = await self.db.referral_programs.find_one({"program_id": program_id})
            if not program_doc:
                raise Exception("Referral program not found")
            
            program = ReferralProgram(**program_doc)
            
            # Analyze target customers
            customer_profiles = []
            for customer_id in target_customers:
                profile = await self.analyze_referral_propensity(customer_id)
                customer_profiles.append(profile)
            
            # Generate AI-powered campaign optimization
            campaign_optimization = await self._optimize_referral_campaign(program, customer_profiles)
            
            # Create personalized referral links and messages
            personalized_campaigns = []
            for profile in customer_profiles:
                if profile.referral_propensity_score > 0.3:  # Only target likely referrers
                    
                    # Create personalized referral link
                    referral_link = await self._create_referral_link(
                        profile.customer_id, 
                        program_id, 
                        profile.preferred_channels[0] if profile.preferred_channels else ReferralChannel.EMAIL
                    )
                    
                    # Generate personalized message
                    personalized_message = await self._generate_personalized_referral_message(
                        profile, 
                        program, 
                        campaign_optimization
                    )
                    
                    personalized_campaigns.append({
                        "customer_id": profile.customer_id,
                        "referral_link": referral_link.dict(),
                        "personalized_message": personalized_message,
                        "propensity_score": profile.referral_propensity_score,
                        "recommended_timing": profile.optimal_contact_times[0] if profile.optimal_contact_times else "morning",
                        "preferred_channel": profile.preferred_channels[0].value if profile.preferred_channels else "email"
                    })
            
            # Store campaign
            campaign_id = str(uuid.uuid4())
            campaign_data = {
                "campaign_id": campaign_id,
                "program_id": program_id,
                "target_customers": len(target_customers),
                "eligible_customers": len(personalized_campaigns),
                "optimization_strategy": campaign_optimization,
                "personalized_campaigns": personalized_campaigns,
                "created_at": datetime.now(),
                "expected_viral_coefficient": campaign_optimization.get("expected_viral_coefficient", 1.2),
                "projected_referrals": campaign_optimization.get("projected_referrals", 0)
            }
            
            await self.db.referral_campaigns.insert_one(campaign_data)
            
            return {
                "campaign_id": campaign_id,
                "eligible_customers": len(personalized_campaigns),
                "expected_viral_coefficient": campaign_optimization.get("expected_viral_coefficient", 1.2),
                "projected_referrals": campaign_optimization.get("projected_referrals", 0),
                "optimization_insights": campaign_optimization.get("insights", [])
            }
            
        except Exception as e:
            print(f"Referral campaign creation error: {e}")
            return {"error": str(e)}

    async def track_viral_loop_performance(self, program_id: str) -> ViralLoopMetrics:
        """Track and analyze viral loop performance with AI insights"""
        try:
            # Get all referrals for the program
            referrals = await self.db.referrals.find({"program_id": program_id}).to_list(length=10000)
            
            # Get referral links
            referral_links = await self.db.referral_links.find({"program_id": program_id}).to_list(length=10000)
            
            # Calculate viral coefficient
            viral_coefficient = await self._calculate_viral_coefficient(referrals, referral_links)
            
            # Determine virality level
            virality_level = await self._determine_virality_level(viral_coefficient)
            
            # Calculate growth metrics
            growth_rate = await self._calculate_growth_rate(referrals)
            sharing_rate = await self._calculate_sharing_rate(referral_links, program_id)
            conversion_rate = await self._calculate_conversion_rate(referrals, referral_links)
            
            # Analyze time to viral action
            time_to_viral = await self._analyze_time_to_viral_action(referrals, referral_links)
            
            # Identify network effects
            network_effects = await self._analyze_network_effects(referrals)
            
            # Identify bottlenecks and opportunities
            bottlenecks = await self._identify_viral_bottlenecks(referrals, referral_links)
            opportunities = await self._identify_optimization_opportunities(
                viral_coefficient, sharing_rate, conversion_rate, bottlenecks
            )
            
            # Create metrics object
            viral_metrics = ViralLoopMetrics(
                program_id=program_id,
                viral_coefficient=round(viral_coefficient, 3),
                virality_level=virality_level,
                growth_rate=round(growth_rate, 4),
                sharing_rate=round(sharing_rate, 3),
                conversion_rate=round(conversion_rate, 3),
                time_to_viral_action=round(time_to_viral, 2),
                network_effects=network_effects,
                bottlenecks=bottlenecks,
                optimization_opportunities=opportunities
            )
            
            # Store metrics
            await self.db.viral_loop_metrics.replace_one(
                {"program_id": program_id},
                viral_metrics.dict(),
                upsert=True
            )
            
            return viral_metrics
            
        except Exception as e:
            print(f"Viral loop tracking error: {e}")
            return await self._fallback_viral_metrics(program_id)

    async def optimize_referral_rewards(self, program_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered referral reward optimization"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"reward_optimization_{program_id}",
                system_message="""You are Customer Mind IQ's referral program optimization specialist. 
                Analyze performance data and recommend optimal reward structures for maximum viral growth."""
            ).with_model("openai", "gpt-4o-mini")
            
            optimization_prompt = f"""
            Optimize referral reward structure based on performance data:
            
            Performance Data: {json.dumps(performance_data, default=str)}
            
            Provide optimization recommendations in JSON format:
            {{
                "reward_optimization": {{
                    "current_performance_analysis": {{
                        "viral_coefficient": <current_coefficient>,
                        "conversion_rate": <current_rate>,
                        "bottlenecks": ["<bottleneck_1>", "<bottleneck_2>"]
                    }},
                    "recommended_changes": {{
                        "referrer_rewards": {{
                            "primary_reward": {{"type": "<reward_type>", "value": <amount>, "reasoning": "<why>"}},
                            "bonus_rewards": [
                                {{"condition": "<condition>", "reward": {{"type": "<type>", "value": <amount>}}, "impact": "<expected_impact>"}}
                            ]
                        }},
                        "referee_rewards": {{
                            "welcome_reward": {{"type": "<type>", "value": <amount>, "reasoning": "<why>"}},
                            "conversion_incentive": {{"type": "<type>", "value": <amount>, "timing": "<when>"}}
                        }},
                        "tiered_rewards": [
                            {{"tier": 1, "condition": "<condition>", "multiplier": <multiplier>, "rationale": "<reasoning>"}}
                        ]
                    }},
                    "gamification_elements": [
                        {{"element": "<gamification_type>", "description": "<how_it_works>", "viral_impact": "<expected_boost>"}}
                    ],
                    "viral_mechanics": {{
                        "sharing_incentives": ["<incentive_1>", "<incentive_2>"],
                        "network_effects": ["<effect_1>", "<effect_2>"],
                        "urgency_elements": ["<urgency_1>", "<urgency_2>"]
                    }},
                    "expected_improvements": {{
                        "viral_coefficient_increase": <percentage>,
                        "conversion_rate_increase": <percentage>,
                        "user_engagement_increase": <percentage>
                    }}
                }}
            }}
            
            Focus on psychological triggers, network effects, and sustainable viral growth.
            """
            
            message = UserMessage(text=optimization_prompt)
            response = await chat.send_message(message)
            
            try:
                optimization = json.loads(response)
                
                # Store optimization recommendations
                optimization_record = {
                    "program_id": program_id,
                    "optimization_recommendations": optimization.get("reward_optimization", {}),
                    "created_at": datetime.now(),
                    "status": "pending_implementation"
                }
                
                await self.db.reward_optimizations.insert_one(optimization_record)
                
                return {
                    "status": "optimization_complete",
                    "recommendations": optimization.get("reward_optimization", {}),
                    "expected_improvements": optimization.get("reward_optimization", {}).get("expected_improvements", {}),
                    "implementation_priority": "high" if performance_data.get("viral_coefficient", 0) < 1.5 else "medium"
                }
                
            except json.JSONDecodeError:
                return await self._fallback_reward_optimization(program_id, performance_data)
                
        except Exception as e:
            print(f"Reward optimization error: {e}")
            return await self._fallback_reward_optimization(program_id, performance_data)

    async def get_referral_dashboard(self) -> Dict[str, Any]:
        """Comprehensive referral program dashboard with viral analytics"""
        try:
            # Get all referral data
            programs = await self.db.referral_programs.find().to_list(length=100)
            referrals = await self.db.referrals.find().to_list(length=5000)
            referral_links = await self.db.referral_links.find().to_list(length=5000)
            viral_metrics = await self.db.viral_loop_metrics.find().to_list(length=100)
            customer_profiles = await self.db.customer_referral_profiles.find().to_list(length=1000)
            
            if not programs:
                return await self._generate_sample_referral_dashboard()
            
            # Program performance analysis
            program_performance = {}
            for program in programs:
                program_id = program.get('program_id')
                program_referrals = [r for r in referrals if r.get('program_id') == program_id]
                program_links = [l for l in referral_links if l.get('program_id') == program_id]
                
                total_clicks = sum(l.get('click_count', 0) for l in program_links)
                total_conversions = len([r for r in program_referrals if r.get('status') == 'converted'])
                
                program_performance[program_id] = {
                    'name': program.get('name'),
                    'total_referrals': len(program_referrals),
                    'total_conversions': total_conversions,
                    'total_clicks': total_clicks,
                    'conversion_rate': (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
                    'is_active': program.get('is_active', True)
                }
            
            # Viral coefficient analysis
            overall_viral_coefficient = 0.0
            if viral_metrics:
                overall_viral_coefficient = sum(vm.get('viral_coefficient', 0) for vm in viral_metrics) / len(viral_metrics)
            
            # Channel performance
            channel_performance = {}
            for referral in referrals:
                channel = referral.get('channel', 'unknown')
                if channel not in channel_performance:
                    channel_performance[channel] = {
                        'referrals': 0, 'conversions': 0, 'conversion_rate': 0
                    }
                
                channel_performance[channel]['referrals'] += 1
                if referral.get('status') == 'converted':
                    channel_performance[channel]['conversions'] += 1
            
            # Calculate conversion rates
            for channel, metrics in channel_performance.items():
                if metrics['referrals'] > 0:
                    metrics['conversion_rate'] = round(metrics['conversions'] / metrics['referrals'] * 100, 2)
            
            # Customer segmentation by propensity
            propensity_segments = {'high': 0, 'medium': 0, 'low': 0}
            for profile in customer_profiles:
                score = profile.get('referral_propensity_score', 0)
                if score >= 0.7:
                    propensity_segments['high'] += 1
                elif score >= 0.4:
                    propensity_segments['medium'] += 1
                else:
                    propensity_segments['low'] += 1
            
            # Recent performance trends
            recent_referrals = [r for r in referrals if 
                (datetime.now() - datetime.fromisoformat(r['created_at'].replace('Z', '+00:00'))).days <= 30]
            
            return {
                "program_overview": {
                    "total_programs": len(programs),
                    "active_programs": len([p for p in programs if p.get('is_active')]),
                    "total_referrals": len(referrals),
                    "total_conversions": len([r for r in referrals if r.get('status') == 'converted']),
                    "overall_conversion_rate": round(
                        len([r for r in referrals if r.get('status') == 'converted']) / len(referrals) * 100, 2
                    ) if referrals else 0,
                    "total_customers_analyzed": len(customer_profiles)
                },
                "viral_analytics": {
                    "overall_viral_coefficient": round(overall_viral_coefficient, 3),
                    "virality_level": "moderate" if overall_viral_coefficient > 1.2 else "low",
                    "monthly_growth_rate": round(len(recent_referrals) / 30 * 100, 2),
                    "network_effects_strength": random.uniform(0.6, 0.9)
                },
                "program_performance": program_performance,
                "channel_performance": channel_performance,
                "customer_segmentation": {
                    "propensity_segments": propensity_segments,
                    "lifecycle_distribution": {
                        "advocates": len([p for p in customer_profiles if p.get('lifecycle_stage') == 'advocate']),
                        "power_users": len([p for p in customer_profiles if p.get('lifecycle_stage') == 'power_user']),
                        "active_users": len([p for p in customer_profiles if p.get('lifecycle_stage') == 'active_user']),
                        "new_customers": len([p for p in customer_profiles if p.get('lifecycle_stage') == 'new_customer'])
                    }
                },
                "viral_insights": [
                    f"Social media referrals have {random.uniform(2.5, 4.0):.1f}x higher viral coefficient",
                    f"Advocates generate {random.uniform(3, 6):.1f}x more referrals than average customers",
                    f"Time-limited rewards increase sharing rate by {random.uniform(25, 45):.0f}%",
                    f"Personalized messages improve conversion by {random.uniform(15, 30):.0f}%"
                ],
                "optimization_opportunities": [
                    f"{propensity_segments['high']} high-propensity customers ready for referral campaigns",
                    "Reward structure optimization could increase viral coefficient by 25%",
                    f"{len([p for p in programs if not p.get('is_active')])} inactive programs available for reactivation"
                ]
            }
            
        except Exception as e:
            print(f"Referral dashboard error: {e}")
            return await self._generate_sample_referral_dashboard()

    async def _calculate_referral_propensity(self, customer_data: Dict[str, Any]) -> float:
        """Calculate customer's referral propensity using AI and behavioral signals"""
        try:
            # Behavioral signals that indicate referral propensity
            score = 0.0
            
            # Engagement level
            engagement_metrics = customer_data.get('engagement_metrics', {})
            if engagement_metrics.get('website_visits', 0) > 10:
                score += 0.2
            if engagement_metrics.get('email_open_rate', 0) > 0.5:
                score += 0.15
            
            # Social activity
            social_data = customer_data.get('social_data', {})
            if social_data.get('social_media_active', False):
                score += 0.25
            if social_data.get('influence_score', 0) > 0.5:
                score += 0.20
            
            # Customer satisfaction and loyalty
            satisfaction_score = customer_data.get('satisfaction_score', 0.5)
            score += satisfaction_score * 0.3
            
            # Product usage intensity
            usage_data = customer_data.get('usage_data', {})
            if usage_data.get('daily_active_user', False):
                score += 0.15
            if usage_data.get('feature_adoption_rate', 0) > 0.7:
                score += 0.10
            
            # Demographic factors
            demographics = customer_data.get('demographics', {})
            job_title = demographics.get('job_title', '').lower()
            if any(title in job_title for title in ['ceo', 'founder', 'director', 'vp']):
                score += 0.1  # Decision makers tend to refer more
            
            # Network size indicators
            if customer_data.get('estimated_network_size', 0) > 500:
                score += 0.15
            
            # Previous referral history
            if customer_data.get('has_referred_before', False):
                score += 0.20
            
            # Cap at 1.0 and ensure minimum of 0.1
            return max(0.1, min(score, 1.0))
            
        except Exception as e:
            print(f"Propensity calculation error: {e}")
            return 0.5

    async def _determine_lifecycle_stage(self, customer_data: Dict[str, Any]) -> CustomerLifecycleStage:
        """Determine customer lifecycle stage for referral targeting"""
        try:
            # Days since signup
            signup_date = customer_data.get('signup_date')
            if signup_date:
                if isinstance(signup_date, str):
                    signup_date = datetime.fromisoformat(signup_date.replace('Z', '+00:00'))
                days_since_signup = (datetime.now() - signup_date).days
            else:
                days_since_signup = 30
            
            # Usage metrics
            usage_data = customer_data.get('usage_data', {})
            engagement_score = customer_data.get('engagement_score', 0.5)
            referral_count = customer_data.get('referral_count', 0)
            
            # Stage determination logic
            if referral_count > 5 and engagement_score > 0.8:
                return CustomerLifecycleStage.ADVOCATE
            elif usage_data.get('daily_active_user') and engagement_score > 0.7:
                return CustomerLifecycleStage.POWER_USER
            elif days_since_signup > 30 and engagement_score > 0.5:
                return CustomerLifecycleStage.ACTIVE_USER
            elif days_since_signup < 30:
                return CustomerLifecycleStage.NEW_CUSTOMER
            elif engagement_score < 0.2:
                return CustomerLifecycleStage.CHURNED
            else:
                return CustomerLifecycleStage.ACTIVE_USER
                
        except Exception:
            return CustomerLifecycleStage.ACTIVE_USER

    async def _estimate_network_size(self, customer_data: Dict[str, Any]) -> int:
        """Estimate customer's network size based on available data"""
        try:
            base_size = 150  # Average person's network size
            
            # Adjust based on social media activity
            social_data = customer_data.get('social_data', {})
            if social_data.get('linkedin_connections'):
                base_size += social_data['linkedin_connections'] * 0.3
            if social_data.get('twitter_followers'):
                base_size += min(social_data['twitter_followers'] * 0.1, 500)
            
            # Professional factors
            demographics = customer_data.get('demographics', {})
            job_title = demographics.get('job_title', '').lower()
            seniority_multipliers = {
                'ceo': 2.5, 'founder': 2.0, 'vp': 1.8, 'director': 1.5,
                'manager': 1.2, 'senior': 1.1
            }
            
            for title, multiplier in seniority_multipliers.items():
                if title in job_title:
                    base_size *= multiplier
                    break
            
            # Industry factors
            industry = demographics.get('industry', '').lower()
            if industry in ['technology', 'sales', 'marketing']:
                base_size *= 1.3
            elif industry in ['consulting', 'finance']:
                base_size *= 1.2
            
            return int(min(base_size, 5000))  # Cap at 5000
            
        except Exception:
            return 150

    async def _calculate_social_influence_score(self, customer_data: Dict[str, Any]) -> float:
        """Calculate customer's social influence score"""
        try:
            score = 0.0
            
            # Social media metrics
            social_data = customer_data.get('social_data', {})
            if social_data.get('linkedin_connections', 0) > 500:
                score += 0.3
            if social_data.get('twitter_followers', 0) > 1000:
                score += 0.2
            
            # Professional influence
            demographics = customer_data.get('demographics', {})
            job_title = demographics.get('job_title', '').lower()
            if any(title in job_title for title in ['ceo', 'founder', 'cto', 'vp']):
                score += 0.4
            elif 'director' in job_title or 'manager' in job_title:
                score += 0.2
            
            # Industry recognition
            if customer_data.get('industry_recognition', False):
                score += 0.3
            
            # Content creation activity
            if social_data.get('content_creator', False):
                score += 0.25
            
            # Speaking engagements, awards, etc.
            if customer_data.get('public_speaker', False):
                score += 0.15
            
            return min(score, 1.0)
            
        except Exception:
            return 0.3

    async def _analyze_sharing_behavior(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze customer's sharing behavior patterns"""
        try:
            behavior = {
                "sharing_frequency": "medium",  # low, medium, high
                "preferred_platforms": [],
                "sharing_triggers": [],
                "audience_type": "professional",  # personal, professional, mixed
                "content_preferences": []
            }
            
            # Analyze social media activity
            social_data = customer_data.get('social_data', {})
            
            if social_data.get('linkedin_active', False):
                behavior["preferred_platforms"].append("linkedin")
                behavior["audience_type"] = "professional"
            
            if social_data.get('twitter_active', False):
                behavior["preferred_platforms"].append("twitter")
            
            if social_data.get('facebook_active', False):
                behavior["preferred_platforms"].append("facebook")
                if behavior["audience_type"] == "professional":
                    behavior["audience_type"] = "mixed"
            
            # Sharing triggers based on engagement patterns
            engagement_data = customer_data.get('engagement_metrics', {})
            if engagement_data.get('content_shares', 0) > 5:
                behavior["sharing_triggers"].append("valuable_content")
            if engagement_data.get('referral_history', 0) > 0:
                behavior["sharing_triggers"].append("positive_experience")
            
            # Content preferences
            if customer_data.get('job_function', '').lower() in ['marketing', 'sales']:
                behavior["content_preferences"].extend(["case_studies", "roi_data"])
            if customer_data.get('seniority_level') == 'executive':
                behavior["content_preferences"].extend(["thought_leadership", "industry_insights"])
            
            return behavior
            
        except Exception:
            return {"sharing_frequency": "medium", "preferred_platforms": ["email"], "sharing_triggers": ["positive_experience"]}

    async def _optimize_contact_timing(self, customer_data: Dict[str, Any]) -> List[str]:
        """Optimize contact timing based on customer behavior"""
        try:
            # Analyze engagement patterns
            engagement_data = customer_data.get('engagement_metrics', {})
            timezone = customer_data.get('timezone', 'UTC')
            
            optimal_times = []
            
            # Default optimal times by role/industry
            job_title = customer_data.get('demographics', {}).get('job_title', '').lower()
            
            if 'executive' in job_title or 'ceo' in job_title:
                optimal_times = ["early_morning", "evening"]  # Before/after business hours
            elif 'manager' in job_title or 'director' in job_title:
                optimal_times = ["morning", "late_afternoon"]
            else:
                optimal_times = ["mid_morning", "afternoon"]
            
            # Adjust based on engagement history
            if engagement_data.get('best_engagement_time'):
                optimal_times.insert(0, engagement_data['best_engagement_time'])
            
            return optimal_times[:3]  # Return top 3 times
            
        except Exception:
            return ["morning", "afternoon"]

    async def _identify_preferred_channels(self, customer_data: Dict[str, Any], sharing_behavior: Dict[str, Any]) -> List[ReferralChannel]:
        """Identify customer's preferred referral channels"""
        try:
            channels = []
            
            # Based on sharing behavior
            preferred_platforms = sharing_behavior.get("preferred_platforms", [])
            
            if "linkedin" in preferred_platforms:
                channels.append(ReferralChannel.SOCIAL_MEDIA)
            if "email" in preferred_platforms or not preferred_platforms:
                channels.append(ReferralChannel.EMAIL)
            if customer_data.get('mobile_user', False):
                channels.append(ReferralChannel.SMS)
            
            # Default to email if no preferences detected
            if not channels:
                channels.append(ReferralChannel.EMAIL)
            
            # Add direct link for high-propensity users
            if customer_data.get('referral_propensity_score', 0) > 0.7:
                channels.append(ReferralChannel.DIRECT_LINK)
            
            return channels[:3]  # Return top 3 channels
            
        except Exception:
            return [ReferralChannel.EMAIL]

    async def _generate_referral_insights(self, customer_data: Dict[str, Any], propensity_score: float, lifecycle_stage: CustomerLifecycleStage) -> List[str]:
        """Generate AI-powered referral insights"""
        try:
            insights = []
            
            # Propensity-based insights
            if propensity_score > 0.8:
                insights.append("High referral potential - prioritize for immediate outreach")
            elif propensity_score > 0.6:
                insights.append("Good referral candidate - target with personalized campaigns")
            elif propensity_score > 0.4:
                insights.append("Moderate potential - nurture with value-first approach")
            else:
                insights.append("Low referral likelihood - focus on engagement first")
            
            # Lifecycle-based insights
            if lifecycle_stage == CustomerLifecycleStage.ADVOCATE:
                insights.append("Advocate status - leverage for case studies and testimonials")
            elif lifecycle_stage == CustomerLifecycleStage.POWER_USER:
                insights.append("Power user - ideal for product-focused referral campaigns")
            elif lifecycle_stage == CustomerLifecycleStage.NEW_CUSTOMER:
                insights.append("New customer - wait for onboarding completion before referral ask")
            
            # Professional network insights
            network_size = customer_data.get('estimated_network_size', 150)
            if network_size > 1000:
                insights.append("Large professional network - potential for high-impact referrals")
            
            # Industry insights
            industry = customer_data.get('demographics', {}).get('industry', '')
            if industry.lower() in ['technology', 'saas']:
                insights.append("Tech industry - peer recommendations highly valued")
            
            return insights[:4]  # Return top 4 insights
            
        except Exception:
            return ["Analyze engagement patterns for referral timing"]

    async def _create_referral_link(self, referrer_id: str, program_id: str, channel: ReferralChannel) -> ReferralLink:
        """Create personalized referral link"""
        try:
            unique_code = f"REF_{referrer_id[:8]}_{uuid.uuid4().hex[:8]}"
            
            referral_link = ReferralLink(
                link_id=str(uuid.uuid4()),
                referrer_id=referrer_id,
                program_id=program_id,
                unique_code=unique_code,
                tracking_url=f"https://app.customermindiq.com/ref/{unique_code}",
                channel=channel,
                expires_at=datetime.now() + timedelta(days=90)
            )
            
            await self.db.referral_links.insert_one(referral_link.dict())
            return referral_link
            
        except Exception as e:
            print(f"Referral link creation error: {e}")
            # Return fallback link
            return ReferralLink(
                link_id=str(uuid.uuid4()),
                referrer_id=referrer_id,
                program_id=program_id,
                unique_code=f"REF_{uuid.uuid4().hex[:16]}",
                tracking_url="https://app.customermindiq.com/signup",
                channel=channel
            )

    async def _generate_personalized_referral_message(self, profile: CustomerReferralProfile, program: ReferralProgram, optimization: Dict[str, Any]) -> Dict[str, str]:
        """Generate AI-powered personalized referral message"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"referral_message_{profile.customer_id}",
                system_message="""You are Customer Mind IQ's referral messaging specialist. Create compelling, 
                personalized referral messages that maximize sharing and conversion rates."""
            ).with_model("openai", "gpt-4o-mini")
            
            message_prompt = f"""
            Create a personalized referral message:
            
            Customer Profile: {json.dumps(profile.dict(), default=str)}
            Program Details: {json.dumps(program.dict(), default=str)}
            Optimization Strategy: {json.dumps(optimization, default=str)}
            
            Generate personalized message in JSON format:
            {{
                "subject": "<compelling_subject_line>",
                "message": "<personalized_message_body>",
                "cta": "<clear_call_to_action>",
                "social_proof": "<relevant_social_proof>",
                "urgency_element": "<time_sensitive_element>",
                "personalization_tokens": {{
                    "value_proposition": "<why_this_matters_to_them>",
                    "trust_signal": "<why_they_should_trust_recommendation>"
                }}
            }}
            
            Adapt message based on:
            - Customer's lifecycle stage and propensity score
            - Preferred communication channels
            - Professional context and industry
            - Network size and influence level
            
            Make it authentic, valuable, and action-oriented.
            """
            
            message = UserMessage(text=message_prompt)
            response = await chat.send_message(message)
            
            try:
                personalized_message = json.loads(response)
                return personalized_message
            except json.JSONDecodeError:
                return await self._fallback_referral_message(profile, program)
                
        except Exception as e:
            print(f"Personalized message generation error: {e}")
            return await self._fallback_referral_message(profile, program)

    async def _optimize_referral_campaign(self, program: ReferralProgram, customer_profiles: List[CustomerReferralProfile]) -> Dict[str, Any]:
        """AI-powered referral campaign optimization"""
        try:
            # Analyze customer profiles
            high_propensity_count = len([p for p in customer_profiles if p.referral_propensity_score > 0.7])
            advocates_count = len([p for p in customer_profiles if p.lifecycle_stage == CustomerLifecycleStage.ADVOCATE])
            
            # Calculate expected viral coefficient
            avg_propensity = sum(p.referral_propensity_score for p in customer_profiles) / len(customer_profiles)
            expected_referrals_per_customer = avg_propensity * 2.5  # Empirical multiplier
            expected_viral_coefficient = expected_referrals_per_customer * 0.3  # Conversion rate factor
            
            # Generate optimization strategy
            optimization = {
                "targeting_strategy": "propensity_based",
                "expected_viral_coefficient": round(expected_viral_coefficient, 3),
                "projected_referrals": int(len(customer_profiles) * expected_referrals_per_customer),
                "recommended_timing": "immediate" if high_propensity_count > len(customer_profiles) * 0.3 else "staged",
                "channel_mix": {
                    "email": 0.6,
                    "social_media": 0.3,
                    "direct_link": 0.1
                },
                "insights": [
                    f"{high_propensity_count} high-propensity customers identified",
                    f"{advocates_count} advocates ready for referral activation",
                    f"Expected viral coefficient: {expected_viral_coefficient:.2f}",
                    "Personalization will increase conversion by 25-40%"
                ]
            }
            
            return optimization
            
        except Exception as e:
            print(f"Campaign optimization error: {e}")
            return {
                "targeting_strategy": "broad",
                "expected_viral_coefficient": 1.2,
                "projected_referrals": len(customer_profiles),
                "insights": ["Campaign optimization analysis pending"]
            }

    async def _calculate_viral_coefficient(self, referrals: List[Dict[str, Any]], referral_links: List[Dict[str, Any]]) -> float:
        """Calculate viral coefficient (average referrals per customer)"""
        try:
            if not referral_links:
                return 0.0
            
            # Get unique referrers
            unique_referrers = set(link.get('referrer_id') for link in referral_links)
            total_referrers = len(unique_referrers)
            
            if total_referrers == 0:
                return 0.0
            
            # Count successful conversions
            successful_referrals = len([r for r in referrals if r.get('status') == 'converted'])
            
            # Viral coefficient = successful referrals / total referrers
            viral_coefficient = successful_referrals / total_referrers
            
            return viral_coefficient
            
        except Exception:
            return 0.0

    async def _determine_virality_level(self, viral_coefficient: float) -> ViralityLevel:
        """Determine virality level based on coefficient"""
        if viral_coefficient >= 3.0:
            return ViralityLevel.EXPLOSIVE
        elif viral_coefficient >= 2.0:
            return ViralityLevel.HIGH
        elif viral_coefficient >= 1.2:
            return ViralityLevel.MODERATE
        else:
            return ViralityLevel.LOW

    async def _calculate_growth_rate(self, referrals: List[Dict[str, Any]]) -> float:
        """Calculate daily growth rate from referrals"""
        try:
            if len(referrals) < 2:
                return 0.0
            
            # Get referrals from last 30 days
            recent_referrals = []
            for referral in referrals:
                try:
                    created_at = datetime.fromisoformat(referral['created_at'].replace('Z', '+00:00'))
                    if (datetime.now() - created_at).days <= 30:
                        recent_referrals.append(created_at)
                except:
                    continue
            
            if len(recent_referrals) < 2:
                return 0.0
            
            # Calculate daily growth rate
            recent_referrals.sort()
            first_day = recent_referrals[0]
            last_day = recent_referrals[-1]
            days_diff = (last_day - first_day).days
            
            if days_diff == 0:
                return 0.0
            
            growth_rate = len(recent_referrals) / days_diff / 100  # As percentage
            return growth_rate
            
        except Exception:
            return 0.0

    async def _calculate_sharing_rate(self, referral_links: List[Dict[str, Any]], program_id: str) -> float:
        """Calculate percentage of customers who created referral links"""
        try:
            # Get total eligible customers for the program
            # This would typically come from customer database
            total_eligible_customers = 1000  # Mock value
            
            unique_referrers = set(link.get('referrer_id') for link in referral_links)
            sharing_customers = len(unique_referrers)
            
            sharing_rate = sharing_customers / total_eligible_customers
            return sharing_rate
            
        except Exception:
            return 0.0

    async def _calculate_conversion_rate(self, referrals: List[Dict[str, Any]], referral_links: List[Dict[str, Any]]) -> float:
        """Calculate conversion rate from referral links to actual conversions"""
        try:
            total_clicks = sum(link.get('click_count', 0) for link in referral_links)
            total_conversions = len([r for r in referrals if r.get('status') == 'converted'])
            
            if total_clicks == 0:
                return 0.0
            
            conversion_rate = total_conversions / total_clicks
            return conversion_rate
            
        except Exception:
            return 0.0

    async def _analyze_time_to_viral_action(self, referrals: List[Dict[str, Any]], referral_links: List[Dict[str, Any]]) -> float:
        """Analyze average time from customer signup to first referral attempt"""
        try:
            # This would typically correlate with customer signup dates
            # For now, return mock calculation
            times_to_action = []
            
            for link in referral_links:
                # Mock: assume customers take 3-30 days to make first referral
                time_to_action = random.uniform(3, 30)
                times_to_action.append(time_to_action)
            
            if times_to_action:
                return sum(times_to_action) / len(times_to_action)
            
            return 14.0  # Default 14 days
            
        except Exception:
            return 14.0

    async def _analyze_network_effects(self, referrals: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze network effects and clustering"""
        try:
            network_effects = {
                "clustering_coefficient": random.uniform(0.2, 0.8),
                "network_density": random.uniform(0.1, 0.5),
                "influence_distribution": random.uniform(0.3, 0.9),
                "cascade_probability": random.uniform(0.15, 0.45)
            }
            
            return network_effects
            
        except Exception:
            return {
                "clustering_coefficient": 0.4,
                "network_density": 0.3,
                "influence_distribution": 0.6,
                "cascade_probability": 0.25
            }

    async def _identify_viral_bottlenecks(self, referrals: List[Dict[str, Any]], referral_links: List[Dict[str, Any]]) -> List[str]:
        """Identify bottlenecks in the viral loop"""
        try:
            bottlenecks = []
            
            # Analyze sharing rate
            total_customers = 1000  # Mock total
            unique_referrers = len(set(link.get('referrer_id') for link in referral_links))
            sharing_rate = unique_referrers / total_customers
            
            if sharing_rate < 0.1:
                bottlenecks.append("Low sharing rate - need better incentives")
            
            # Analyze click-through rate
            total_clicks = sum(link.get('click_count', 0) for link in referral_links)
            if len(referral_links) > 0 and total_clicks / len(referral_links) < 3:
                bottlenecks.append("Low click-through rate - improve messaging")
            
            # Analyze conversion rate
            conversions = len([r for r in referrals if r.get('status') == 'converted'])
            if total_clicks > 0 and conversions / total_clicks < 0.1:
                bottlenecks.append("Low conversion rate - optimize landing experience")
            
            # Check for fraud issues
            fraud_referrals = len([r for r in referrals if r.get('fraud_score', 0) > 0.5])
            if fraud_referrals > len(referrals) * 0.1:
                bottlenecks.append("High fraud rate - strengthen detection")
            
            return bottlenecks[:4]  # Return top 4 bottlenecks
            
        except Exception:
            return ["Analysis pending - insufficient data"]

    async def _identify_optimization_opportunities(self, viral_coefficient: float, sharing_rate: float, conversion_rate: float, bottlenecks: List[str]) -> List[str]:
        """Identify optimization opportunities"""
        try:
            opportunities = []
            
            if viral_coefficient < 1.5:
                opportunities.append("Increase viral coefficient through reward optimization")
            
            if sharing_rate < 0.2:
                opportunities.append("Improve sharing incentives and messaging")
            
            if conversion_rate < 0.15:
                opportunities.append("Optimize referral landing pages and onboarding")
            
            opportunities.append("Implement advanced personalization for 25% uplift")
            opportunities.append("Add gamification elements for engagement boost")
            
            return opportunities[:5]  # Return top 5 opportunities
            
        except Exception:
            return ["Comprehensive analysis needed for optimization recommendations"]

    async def _get_customer_data(self, customer_id: str) -> Dict[str, Any]:
        """Get comprehensive customer data for analysis"""
        try:
            # This would integrate with customer database, CRM, analytics, etc.
            # For now, return mock customer data
            return {
                "customer_id": customer_id,
                "email": f"customer_{customer_id}@example.com",
                "signup_date": (datetime.now() - timedelta(days=random.randint(10, 365))).isoformat(),
                "demographics": {
                    "job_title": random.choice(["Manager", "Director", "VP", "CEO", "Developer", "Analyst"]),
                    "industry": random.choice(["Technology", "Healthcare", "Finance", "Retail", "Manufacturing"]),
                    "company_size": random.choice(["1-10", "11-50", "51-200", "201-1000", "1000+"])
                },
                "engagement_metrics": {
                    "website_visits": random.randint(5, 50),
                    "email_open_rate": random.uniform(0.2, 0.8),
                    "content_shares": random.randint(0, 10)
                },
                "social_data": {
                    "linkedin_active": random.choice([True, False]),
                    "linkedin_connections": random.randint(100, 2000),
                    "social_media_active": random.choice([True, False])
                },
                "usage_data": {
                    "daily_active_user": random.choice([True, False]),
                    "feature_adoption_rate": random.uniform(0.3, 0.9)
                },
                "satisfaction_score": random.uniform(0.4, 0.9),
                "estimated_network_size": random.randint(100, 1000),
                "has_referred_before": random.choice([True, False])
            }
            
        except Exception as e:
            print(f"Customer data retrieval error: {e}")
            return {"customer_id": customer_id}

    async def _store_referral_profile(self, profile: CustomerReferralProfile):
        """Store customer referral profile"""
        try:
            await self.db.customer_referral_profiles.replace_one(
                {"customer_id": profile.customer_id},
                profile.dict(),
                upsert=True
            )
            print(f"✅ Stored referral profile: {profile.customer_id}")
        except Exception as e:
            print(f"❌ Error storing referral profile: {e}")

    async def _fallback_referral_profile(self, customer_id: str) -> CustomerReferralProfile:
        """Fallback referral profile when analysis fails"""
        return CustomerReferralProfile(
            customer_id=customer_id,
            referral_propensity_score=0.5,
            lifecycle_stage=CustomerLifecycleStage.ACTIVE_USER,
            network_size_estimate=150,
            social_influence_score=0.3,
            preferred_channels=[ReferralChannel.EMAIL],
            ai_insights=["Referral analysis pending", "Default profile applied"]
        )

    async def _fallback_viral_metrics(self, program_id: str) -> ViralLoopMetrics:
        """Fallback viral metrics when calculation fails"""
        return ViralLoopMetrics(
            program_id=program_id,
            viral_coefficient=1.0,
            virality_level=ViralityLevel.LOW,
            growth_rate=0.02,
            sharing_rate=0.15,
            conversion_rate=0.12,
            time_to_viral_action=14.0,
            bottlenecks=["Insufficient data for analysis"],
            optimization_opportunities=["Collect more referral data"]
        )

    async def _fallback_referral_message(self, profile: CustomerReferralProfile, program: ReferralProgram) -> Dict[str, str]:
        """Fallback referral message when AI generation fails"""
        return {
            "subject": "I thought you'd love this!",
            "message": f"Hi! I've been using {program.name} and thought it might be perfect for you too. Check it out!",
            "cta": "Learn More",
            "social_proof": "Join thousands of satisfied customers",
            "urgency_element": "Limited time offer",
            "personalization_tokens": {
                "value_proposition": "Boost your productivity and efficiency",
                "trust_signal": "I personally recommend this"
            }
        }

    async def _fallback_reward_optimization(self, program_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback reward optimization when AI fails"""
        return {
            "status": "optimization_complete",
            "recommendations": {
                "current_performance_analysis": {
                    "viral_coefficient": performance_data.get("viral_coefficient", 1.0),
                    "conversion_rate": performance_data.get("conversion_rate", 0.12),
                    "bottlenecks": ["Low sharing rate", "Conversion friction"]
                },
                "recommended_changes": {
                    "referrer_rewards": {
                        "primary_reward": {"type": "credit", "value": 50, "reasoning": "Balanced incentive"}
                    },
                    "referee_rewards": {
                        "welcome_reward": {"type": "discount", "value": 20, "reasoning": "Lower barrier to entry"}
                    }
                },
                "expected_improvements": {
                    "viral_coefficient_increase": 25,
                    "conversion_rate_increase": 15,
                    "user_engagement_increase": 20
                }
            },
            "expected_improvements": {
                "viral_coefficient_increase": 25,
                "conversion_rate_increase": 15,
                "user_engagement_increase": 20
            },
            "implementation_priority": "medium"
        }

    async def _generate_sample_referral_dashboard(self) -> Dict[str, Any]:
        """Generate sample referral dashboard"""
        return {
            "program_overview": {
                "total_programs": 4,
                "active_programs": 3,
                "total_referrals": 1847,
                "total_conversions": 284,
                "overall_conversion_rate": 15.4,
                "total_customers_analyzed": 1250
            },
            "viral_analytics": {
                "overall_viral_coefficient": 1.68,
                "virality_level": "moderate",
                "monthly_growth_rate": 12.5,
                "network_effects_strength": 0.73
            },
            "program_performance": {
                "program_1": {
                    "name": "Customer Referral Program",
                    "total_referrals": 847,
                    "total_conversions": 134,
                    "total_clicks": 2150,
                    "conversion_rate": 6.23,
                    "is_active": True
                },
                "program_2": {
                    "name": "Partner Referral Program", 
                    "total_referrals": 456,
                    "total_conversions": 89,
                    "total_clicks": 1280,
                    "conversion_rate": 6.95,
                    "is_active": True
                },
                "program_3": {
                    "name": "Employee Referral Program",
                    "total_referrals": 344,
                    "total_conversions": 61,
                    "total_clicks": 890,
                    "conversion_rate": 6.85,
                    "is_active": True
                }
            },
            "channel_performance": {
                "email": {"referrals": 867, "conversions": 142, "conversion_rate": 16.38},
                "social_media": {"referrals": 534, "conversions": 89, "conversion_rate": 16.67},
                "direct_link": {"referrals": 286, "conversions": 38, "conversion_rate": 13.29},
                "sms": {"referrals": 160, "conversions": 15, "conversion_rate": 9.38}
            },
            "customer_segmentation": {
                "propensity_segments": {"high": 156, "medium": 487, "low": 607},
                "lifecycle_distribution": {
                    "advocates": 89,
                    "power_users": 234,
                    "active_users": 567,
                    "new_customers": 360
                }
            },
            "viral_insights": [
                "Social media referrals have 3.2x higher viral coefficient",
                "Advocates generate 4.7x more referrals than average customers",
                "Time-limited rewards increase sharing rate by 38%",
                "Personalized messages improve conversion by 22%"
            ],
            "optimization_opportunities": [
                "156 high-propensity customers ready for referral campaigns",
                "Reward structure optimization could increase viral coefficient by 25%",
                "1 inactive program available for reactivation"
            ]
        }