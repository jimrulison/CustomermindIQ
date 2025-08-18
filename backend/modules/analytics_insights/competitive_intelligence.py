"""
Competitive Intelligence - Analytics & Insights Module
Market monitoring and competitive analysis with AI-powered insights
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import uuid
import numpy as np
from enum import Enum

# Initialize router
competitive_intelligence_router = APIRouter()

class CompetitorTier(str, Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    EMERGING = "emerging"

class DataSource(str, Enum):
    WEBSITE = "website"
    SOCIAL_MEDIA = "social_media"
    NEWS = "news"
    REVIEWS = "reviews"
    PATENTS = "patents"
    JOB_POSTINGS = "job_postings"
    PRICING = "pricing"

class MarketMovement(str, Enum):
    PRICE_CHANGE = "price_change"
    FEATURE_LAUNCH = "feature_launch"
    PARTNERSHIP = "partnership"
    FUNDING = "funding"
    ACQUISITION = "acquisition"
    LEADERSHIP_CHANGE = "leadership_change"

class Competitor(BaseModel):
    competitor_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    tier: CompetitorTier
    market_share: float
    website: str
    headquarters: str
    founded_year: int
    employee_count: int
    estimated_revenue: float

class CompetitiveIntelligenceData(BaseModel):
    data_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    competitor_id: str
    data_source: DataSource
    content: str
    timestamp: datetime
    sentiment_score: float
    relevance_score: float
    category: str

class MarketMovementEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    competitor_id: str
    movement_type: MarketMovement
    description: str
    impact_score: float
    timestamp: datetime
    detected_by: DataSource
    verified: bool = False

class CompetitiveAnalysis(BaseModel):
    competitor_name: str
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    market_position: str
    pricing_strategy: str
    recent_activities: List[str]

class MarketInsight(BaseModel):
    insight_type: str
    description: str
    confidence_score: float
    business_impact: str
    recommended_action: str
    urgency: str

class CompetitiveIntelligenceService:
    """AI-powered Competitive Intelligence Service"""
    
    def __init__(self):
        self.competitors_db = self._initialize_competitors()
        self.sentiment_keywords = {
            'positive': ['innovation', 'growth', 'success', 'breakthrough', 'launch', 'expansion'],
            'negative': ['decline', 'loss', 'failure', 'issue', 'problem', 'lawsuit'],
            'neutral': ['announcement', 'update', 'report', 'change', 'development']
        }
    
    def _initialize_competitors(self) -> List[Competitor]:
        """Initialize competitor database with mock data"""
        return [
            Competitor(
                name="TechRival Pro",
                tier=CompetitorTier.DIRECT,
                market_share=0.15,
                website="https://techrival.com",
                headquarters="San Francisco, CA",
                founded_year=2018,
                employee_count=150,
                estimated_revenue=25000000
            ),
            Competitor(
                name="DataMaster Solutions",
                tier=CompetitorTier.DIRECT,
                market_share=0.12,
                website="https://datamaster.com",
                headquarters="Austin, TX",
                founded_year=2016,
                employee_count=200,
                estimated_revenue=35000000
            ),
            Competitor(
                name="Analytics Edge",
                tier=CompetitorTier.INDIRECT,
                market_share=0.08,
                website="https://analyticsedge.com",
                headquarters="Seattle, WA",
                founded_year=2019,
                employee_count=75,
                estimated_revenue=12000000
            ),
            Competitor(
                name="InnovateCorp",
                tier=CompetitorTier.EMERGING,
                market_share=0.04,
                website="https://innovatecorp.com",
                headquarters="Boston, MA",
                founded_year=2021,
                employee_count=45,
                estimated_revenue=8000000
            ),
            Competitor(
                name="GlobalTech Systems",
                tier=CompetitorTier.DIRECT,
                market_share=0.18,
                website="https://globaltech.com",
                headquarters="New York, NY",
                founded_year=2015,
                employee_count=300,
                estimated_revenue=50000000
            )
        ]
    
    async def collect_competitive_data(self, days_back: int = 30) -> List[CompetitiveIntelligenceData]:
        """Simulate collection of competitive intelligence data"""
        data_points = []
        
        content_templates = {
            DataSource.WEBSITE: [
                "{} announces new product features focusing on AI automation",
                "{} updates pricing strategy with 15% increase across premium tiers",
                "{} launches integration with leading CRM platforms",
                "{} publishes case study showing 40% ROI improvement for enterprise clients"
            ],
            DataSource.SOCIAL_MEDIA: [
                "{} receives positive customer feedback on recent product updates",
                "{} trending on LinkedIn with thought leadership content",
                "{} announces partnership with major industry player",
                "{} CEO shares company milestone of reaching 10,000+ customers"
            ],
            DataSource.NEWS: [
                "{} raises $15M Series B funding round led by tier-1 VC firm",
                "{} acquires smaller competitor to expand market reach",
                "{} wins industry award for innovation in customer analytics",
                "{} announces expansion into European markets"
            ],
            DataSource.REVIEWS: [
                "{} receives 4.2/5 rating on G2 with praise for user experience",
                "Customer review highlights {}'s superior customer support",
                "{} faces criticism for complex onboarding process",
                "Users praise {}'s advanced reporting capabilities"
            ]
        }
        
        for competitor in self.competitors_db:
            # Generate 5-15 data points per competitor
            num_data_points = random.randint(5, 15)
            
            for _ in range(num_data_points):
                data_source = random.choice(list(DataSource))
                content_template = random.choice(content_templates.get(data_source, ["Generic update about {}"]))
                content = content_template.format(competitor.name)
                
                # Calculate sentiment score
                sentiment_score = self._calculate_sentiment(content)
                
                # Calculate relevance score (higher for direct competitors)
                relevance_base = {
                    CompetitorTier.DIRECT: 0.8,
                    CompetitorTier.INDIRECT: 0.6,
                    CompetitorTier.EMERGING: 0.4
                }[competitor.tier]
                relevance_score = relevance_base + random.uniform(-0.2, 0.2)
                
                timestamp = datetime.now() - timedelta(days=random.randint(0, days_back))
                
                data_point = CompetitiveIntelligenceData(
                    competitor_id=competitor.competitor_id,
                    data_source=data_source,
                    content=content,
                    timestamp=timestamp,
                    sentiment_score=sentiment_score,
                    relevance_score=max(0, min(1, relevance_score)),
                    category=self._categorize_content(content)
                )
                data_points.append(data_point)
        
        return data_points
    
    def _calculate_sentiment(self, content: str) -> float:
        """Calculate sentiment score for content"""
        content_lower = content.lower()
        
        positive_count = sum(1 for word in self.sentiment_keywords['positive'] if word in content_lower)
        negative_count = sum(1 for word in self.sentiment_keywords['negative'] if word in content_lower)
        
        if positive_count > negative_count:
            return random.uniform(0.6, 1.0)
        elif negative_count > positive_count:
            return random.uniform(-1.0, -0.6)
        else:
            return random.uniform(-0.3, 0.3)
    
    def _categorize_content(self, content: str) -> str:
        """Categorize content into relevant business categories"""
        categories = {
            'product': ['product', 'feature', 'launch', 'update', 'innovation'],
            'pricing': ['pricing', 'price', 'cost', 'subscription', 'plan'],
            'marketing': ['marketing', 'campaign', 'customer', 'client', 'case study'],
            'funding': ['funding', 'investment', 'raise', 'series', 'acquisition'],
            'partnerships': ['partnership', 'integration', 'collaboration', 'alliance'],
            'leadership': ['CEO', 'founder', 'executive', 'leadership', 'team'],
            'market': ['market', 'expansion', 'growth', 'share', 'competition']
        }
        
        content_lower = content.lower()
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return 'general'
    
    async def detect_market_movements(self, intelligence_data: List[CompetitiveIntelligenceData]) -> List[MarketMovementEvent]:
        """Detect significant market movements from intelligence data"""
        movements = []
        
        # Group data by competitor
        competitor_data = {}
        for data in intelligence_data:
            if data.competitor_id not in competitor_data:
                competitor_data[data.competitor_id] = []
            competitor_data[data.competitor_id].append(data)
        
        for competitor_id, data_points in competitor_data.items():
            competitor = next((c for c in self.competitors_db if c.competitor_id == competitor_id), None)
            if not competitor:
                continue
            
            # Detect different types of movements
            for data_point in data_points:
                movement_type = self._classify_movement(data_point.content)
                if movement_type:
                    impact_score = self._calculate_impact_score(movement_type, competitor.tier, data_point.relevance_score)
                    
                    movement = MarketMovementEvent(
                        competitor_id=competitor_id,
                        movement_type=movement_type,
                        description=data_point.content,
                        impact_score=impact_score,
                        timestamp=data_point.timestamp,
                        detected_by=data_point.data_source,
                        verified=random.random() > 0.3  # 70% verification rate
                    )
                    movements.append(movement)
        
        # Sort by impact score (highest first)
        movements.sort(key=lambda x: x.impact_score, reverse=True)
        return movements[:20]  # Return top 20 movements
    
    def _classify_movement(self, content: str) -> Optional[MarketMovement]:
        """Classify content into market movement types"""
        content_lower = content.lower()
        
        movement_keywords = {
            MarketMovement.PRICE_CHANGE: ['pricing', 'price', 'increase', 'decrease', 'discount'],
            MarketMovement.FEATURE_LAUNCH: ['launch', 'feature', 'product', 'new', 'announces'],
            MarketMovement.PARTNERSHIP: ['partnership', 'integration', 'collaboration', 'alliance'],
            MarketMovement.FUNDING: ['funding', 'raise', 'investment', 'series'],
            MarketMovement.ACQUISITION: ['acquisition', 'acquire', 'merger', 'buys'],
            MarketMovement.LEADERSHIP_CHANGE: ['CEO', 'executive', 'leadership', 'founder']
        }
        
        for movement_type, keywords in movement_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return movement_type
        
        return None
    
    def _calculate_impact_score(self, movement_type: MarketMovement, competitor_tier: CompetitorTier, relevance_score: float) -> float:
        """Calculate business impact score for market movements"""
        base_impact = {
            MarketMovement.PRICE_CHANGE: 0.8,
            MarketMovement.FEATURE_LAUNCH: 0.7,
            MarketMovement.PARTNERSHIP: 0.6,
            MarketMovement.FUNDING: 0.5,
            MarketMovement.ACQUISITION: 0.9,
            MarketMovement.LEADERSHIP_CHANGE: 0.4
        }[movement_type]
        
        tier_multiplier = {
            CompetitorTier.DIRECT: 1.0,
            CompetitorTier.INDIRECT: 0.7,
            CompetitorTier.EMERGING: 0.5
        }[competitor_tier]
        
        impact_score = base_impact * tier_multiplier * relevance_score
        return min(1.0, impact_score)
    
    async def generate_competitive_analysis(self, competitor_id: str, intelligence_data: List[CompetitiveIntelligenceData]) -> CompetitiveAnalysis:
        """Generate comprehensive competitive analysis for a specific competitor"""
        competitor = next((c for c in self.competitors_db if c.competitor_id == competitor_id), None)
        if not competitor:
            raise ValueError("Competitor not found")
        
        # Filter data for this competitor
        competitor_data = [d for d in intelligence_data if d.competitor_id == competitor_id]
        
        # Analyze recent activities
        recent_activities = []
        for data in competitor_data[-5:]:  # Last 5 data points
            recent_activities.append(data.content)
        
        # Generate SWOT analysis (simplified AI simulation)
        strengths = self._generate_strengths(competitor, competitor_data)
        weaknesses = self._generate_weaknesses(competitor, competitor_data)
        opportunities = self._generate_opportunities(competitor)
        threats = self._generate_threats(competitor, competitor_data)
        
        # Determine market position
        market_position = self._assess_market_position(competitor)
        
        # Analyze pricing strategy
        pricing_strategy = self._analyze_pricing_strategy(competitor_data)
        
        return CompetitiveAnalysis(
            competitor_name=competitor.name,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            market_position=market_position,
            pricing_strategy=pricing_strategy,
            recent_activities=recent_activities
        )
    
    def _generate_strengths(self, competitor: Competitor, data: List[CompetitiveIntelligenceData]) -> List[str]:
        """Generate competitor strengths based on data analysis"""
        strengths = []
        
        if competitor.market_share > 0.10:
            strengths.append("Strong market position with significant market share")
        
        if competitor.employee_count > 200:
            strengths.append("Large team enabling rapid development and support")
        
        positive_sentiment_data = [d for d in data if d.sentiment_score > 0.5]
        if len(positive_sentiment_data) > len(data) * 0.6:
            strengths.append("Strong positive market sentiment and customer satisfaction")
        
        if competitor.founded_year < 2018:
            strengths.append("Established market presence with proven track record")
        
        return strengths or ["Market presence in competitive landscape"]
    
    def _generate_weaknesses(self, competitor: Competitor, data: List[CompetitiveIntelligenceData]) -> List[str]:
        """Generate competitor weaknesses based on data analysis"""
        weaknesses = []
        
        if competitor.employee_count < 100:
            weaknesses.append("Limited team size may constrain growth and support capabilities")
        
        negative_sentiment_data = [d for d in data if d.sentiment_score < -0.3]
        if len(negative_sentiment_data) > len(data) * 0.3:
            weaknesses.append("Negative customer feedback in certain areas")
        
        if competitor.market_share < 0.05:
            weaknesses.append("Small market share indicates limited market penetration")
        
        if competitor.founded_year > 2020:
            weaknesses.append("Relatively new to market with limited proven track record")
        
        return weaknesses or ["Standard competitive challenges"]
    
    def _generate_opportunities(self, competitor: Competitor) -> List[str]:
        """Generate market opportunities for competitor"""
        opportunities = [
            "Growing demand for AI-powered analytics solutions",
            "Expansion into emerging markets and verticals",
            "Integration opportunities with major platforms",
            "Acquisition of smaller specialized competitors"
        ]
        return random.sample(opportunities, 3)
    
    def _generate_threats(self, competitor: Competitor, data: List[CompetitiveIntelligenceData]) -> List[str]:
        """Generate competitive threats"""
        threats = [
            "New entrants with innovative AI technologies",
            "Price competition from established players",
            "Economic downturn affecting customer spending",
            "Regulatory changes in data privacy and AI"
        ]
        return random.sample(threats, 2)
    
    def _assess_market_position(self, competitor: Competitor) -> str:
        """Assess competitor's market position"""
        if competitor.market_share > 0.15:
            return "Market Leader"
        elif competitor.market_share > 0.08:
            return "Strong Challenger"
        elif competitor.market_share > 0.03:
            return "Niche Player"
        else:
            return "Emerging Competitor"
    
    def _analyze_pricing_strategy(self, data: List[CompetitiveIntelligenceData]) -> str:
        """Analyze competitor's pricing strategy from data"""
        pricing_data = [d for d in data if 'pricing' in d.content.lower() or 'price' in d.content.lower()]
        
        if any('increase' in d.content.lower() for d in pricing_data):
            return "Premium Pricing Strategy"
        elif any('discount' in d.content.lower() or 'competitive' in d.content.lower() for d in pricing_data):
            return "Competitive Pricing Strategy"
        else:
            return "Value-Based Pricing Strategy"
    
    async def generate_market_insights(self, intelligence_data: List[CompetitiveIntelligenceData], movements: List[MarketMovementEvent]) -> List[MarketInsight]:
        """Generate AI-powered market insights"""
        insights = []
        
        # Analyze pricing trends
        pricing_movements = [m for m in movements if m.movement_type == MarketMovement.PRICE_CHANGE]
        if pricing_movements:
            insights.append(MarketInsight(
                insight_type="pricing_trend",
                description=f"{len(pricing_movements)} competitors have made pricing changes in the last 30 days",
                confidence_score=0.85,
                business_impact="May indicate market-wide pricing pressure or value repositioning",
                recommended_action="Review and potentially adjust pricing strategy to maintain competitiveness",
                urgency="medium"
            ))
        
        # Analyze feature launches
        feature_launches = [m for m in movements if m.movement_type == MarketMovement.FEATURE_LAUNCH]
        if len(feature_launches) >= 3:
            insights.append(MarketInsight(
                insight_type="innovation_trend",
                description="High level of product innovation activity across competitors",
                confidence_score=0.90,
                business_impact="Increased competition in product capabilities and features",
                recommended_action="Accelerate product roadmap and consider strategic feature development",
                urgency="high"
            ))
        
        # Analyze market sentiment
        avg_sentiment = np.mean([d.sentiment_score for d in intelligence_data])
        if avg_sentiment > 0.3:
            insights.append(MarketInsight(
                insight_type="market_sentiment",
                description="Overall positive market sentiment towards competitive landscape",
                confidence_score=0.75,
                business_impact="Growing market opportunity with increased customer confidence",
                recommended_action="Increase marketing investment to capture market growth",
                urgency="medium"
            ))
        
        # Analyze funding activity
        funding_movements = [m for m in movements if m.movement_type == MarketMovement.FUNDING]
        if funding_movements:
            insights.append(MarketInsight(
                insight_type="investment_activity",
                description=f"Recent funding activity indicates continued investor confidence in market",
                confidence_score=0.80,
                business_impact="Well-funded competitors may increase competitive pressure",
                recommended_action="Consider strategic partnerships or additional funding to compete effectively",
                urgency="medium"
            ))
        
        return insights

# Initialize service
competitive_service = CompetitiveIntelligenceService()

@competitive_intelligence_router.get("/api/analytics/competitive-intelligence/dashboard")
async def get_competitive_dashboard():
    """Get competitive intelligence dashboard data"""
    try:
        # Collect recent competitive data
        intelligence_data = await competitive_service.collect_competitive_data(30)
        
        # Detect market movements
        movements = await competitive_service.detect_market_movements(intelligence_data)
        
        # Generate market insights
        insights = await competitive_service.generate_market_insights(intelligence_data, movements)
        
        # Calculate dashboard metrics
        total_competitors = len(competitive_service.competitors_db)
        total_data_points = len(intelligence_data)
        high_impact_movements = len([m for m in movements if m.impact_score > 0.7])
        
        # Competitor performance summary
        competitor_summary = {}
        for competitor in competitive_service.competitors_db:
            competitor_data = [d for d in intelligence_data if d.competitor_id == competitor.competitor_id]
            avg_sentiment = np.mean([d.sentiment_score for d in competitor_data]) if competitor_data else 0
            
            competitor_summary[competitor.name] = {
                "tier": competitor.tier.value,
                "market_share": competitor.market_share,
                "data_points": len(competitor_data),
                "avg_sentiment": avg_sentiment,
                "recent_movements": len([m for m in movements if m.competitor_id == competitor.competitor_id]),
                "threat_level": "high" if competitor.tier == CompetitorTier.DIRECT and avg_sentiment > 0.5 else "medium" if competitor.tier == CompetitorTier.DIRECT else "low"
            }
        
        # Recent significant movements
        significant_movements = [
            {
                "competitor": next((c.name for c in competitive_service.competitors_db if c.competitor_id == m.competitor_id), "Unknown"),
                "movement_type": m.movement_type.value,
                "description": m.description,
                "impact_score": m.impact_score,
                "timestamp": m.timestamp
            }
            for m in movements[:10]
        ]
        
        return {
            "status": "success",
            "dashboard_data": {
                "overview": {
                    "total_competitors_monitored": total_competitors,
                    "total_data_points_collected": total_data_points,
                    "high_impact_movements": high_impact_movements,
                    "market_sentiment_score": np.mean([d.sentiment_score for d in intelligence_data]),
                    "monitoring_period_days": 30
                },
                "competitor_landscape": {
                    "direct_competitors": len([c for c in competitive_service.competitors_db if c.tier == CompetitorTier.DIRECT]),
                    "indirect_competitors": len([c for c in competitive_service.competitors_db if c.tier == CompetitorTier.INDIRECT]),
                    "emerging_competitors": len([c for c in competitive_service.competitors_db if c.tier == CompetitorTier.EMERGING]),
                    "total_market_share_monitored": sum(c.market_share for c in competitive_service.competitors_db)
                },
                "competitor_performance": competitor_summary,
                "recent_movements": significant_movements,
                "data_sources": {
                    source.value: len([d for d in intelligence_data if d.data_source == source])
                    for source in DataSource
                },
                "threat_analysis": {
                    "immediate_threats": [name for name, data in competitor_summary.items() if data["threat_level"] == "high"],
                    "emerging_threats": [name for name, data in competitor_summary.items() if data["threat_level"] == "medium"],
                    "competitive_pressure_score": min(100, sum(data["market_share"] * 100 for data in competitor_summary.values() if data["threat_level"] == "high"))
                }
            },
            "market_insights": [insight.dict() for insight in insights],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Competitive dashboard error: {e}")

@competitive_intelligence_router.post("/api/analytics/competitive-intelligence/competitor-analysis")
async def analyze_specific_competitor(request: Dict):
    """Perform detailed analysis of a specific competitor"""
    try:
        competitor_name = request.get('competitor_name')
        if not competitor_name:
            raise HTTPException(status_code=400, detail="competitor_name is required")
        
        # Find competitor
        competitor = next((c for c in competitive_service.competitors_db if c.name.lower() == competitor_name.lower()), None)
        if not competitor:
            raise HTTPException(status_code=404, detail="Competitor not found")
        
        # Collect intelligence data
        intelligence_data = await competitive_service.collect_competitive_data(60)  # 60 days
        
        # Generate comprehensive analysis
        analysis = await competitive_service.generate_competitive_analysis(competitor.competitor_id, intelligence_data)
        
        # Detect movements for this competitor
        movements = await competitive_service.detect_market_movements(intelligence_data)
        competitor_movements = [m for m in movements if m.competitor_id == competitor.competitor_id]
        
        # Calculate competitive metrics
        competitor_data = [d for d in intelligence_data if d.competitor_id == competitor.competitor_id]
        
        return {
            "status": "success",
            "competitor_profile": {
                "name": competitor.name,
                "tier": competitor.tier.value,
                "market_share": competitor.market_share,
                "headquarters": competitor.headquarters,
                "founded_year": competitor.founded_year,
                "employee_count": competitor.employee_count,
                "estimated_revenue": competitor.estimated_revenue
            },
            "competitive_analysis": analysis.dict(),
            "intelligence_summary": {
                "data_points_analyzed": len(competitor_data),
                "average_sentiment": np.mean([d.sentiment_score for d in competitor_data]) if competitor_data else 0,
                "relevance_score": np.mean([d.relevance_score for d in competitor_data]) if competitor_data else 0,
                "recent_movements": len(competitor_movements),
                "data_freshness": "Last 60 days"
            },
            "recent_movements": [
                {
                    "movement_type": m.movement_type.value,
                    "description": m.description,
                    "impact_score": m.impact_score,
                    "timestamp": m.timestamp,
                    "verified": m.verified
                }
                for m in competitor_movements[:10]
            ],
            "competitive_positioning": {
                "relative_market_position": analysis.market_position,
                "key_differentiators": analysis.strengths[:3],
                "vulnerability_areas": analysis.weaknesses[:3],
                "strategic_recommendations": [
                    "Monitor pricing strategy changes closely",
                    "Track product development announcements",
                    "Analyze customer sentiment trends",
                    "Watch for partnership opportunities or threats"
                ]
            },
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Competitor analysis error: {e}")

@competitive_intelligence_router.get("/api/analytics/competitive-intelligence/market-trends")
async def get_market_trends():
    """Get comprehensive market trend analysis"""
    try:
        # Collect extended data for trend analysis
        intelligence_data = await competitive_service.collect_competitive_data(90)  # 90 days
        movements = await competitive_service.detect_market_movements(intelligence_data)
        
        # Analyze trends by category
        trends = {
            "pricing_trends": [],
            "product_innovation_trends": [],
            "market_consolidation_trends": [],
            "investment_trends": []
        }
        
        # Pricing trends
        pricing_movements = [m for m in movements if m.movement_type == MarketMovement.PRICE_CHANGE]
        if pricing_movements:
            price_increases = len([m for m in pricing_movements if 'increase' in m.description.lower()])
            price_decreases = len([m for m in pricing_movements if 'decrease' in m.description.lower() or 'discount' in m.description.lower()])
            
            trends["pricing_trends"] = [
                {
                    "trend": "price_adjustments",
                    "description": f"{len(pricing_movements)} pricing changes detected in last 90 days",
                    "details": f"{price_increases} increases, {price_decreases} decreases/discounts",
                    "implication": "Market is actively testing price elasticity and value positioning"
                }
            ]
        
        # Product innovation trends
        feature_movements = [m for m in movements if m.movement_type == MarketMovement.FEATURE_LAUNCH]
        if feature_movements:
            trends["product_innovation_trends"] = [
                {
                    "trend": "accelerated_innovation",
                    "description": f"{len(feature_movements)} product launches/updates detected",
                    "details": "High frequency of feature releases across competitors",
                    "implication": "Competitive landscape driving rapid product evolution"
                }
            ]
        
        # Market consolidation trends
        acquisition_movements = [m for m in movements if m.movement_type == MarketMovement.ACQUISITION]
        partnership_movements = [m for m in movements if m.movement_type == MarketMovement.PARTNERSHIP]
        
        if acquisition_movements or partnership_movements:
            trends["market_consolidation_trends"] = [
                {
                    "trend": "strategic_partnerships",
                    "description": f"{len(partnership_movements)} partnerships, {len(acquisition_movements)} acquisitions",
                    "details": "Companies seeking strategic alliances and market consolidation",
                    "implication": "Market maturing with focus on strategic positioning"
                }
            ]
        
        # Investment trends
        funding_movements = [m for m in movements if m.movement_type == MarketMovement.FUNDING]
        if funding_movements:
            trends["investment_trends"] = [
                {
                    "trend": "continued_investment",
                    "description": f"{len(funding_movements)} funding events detected",
                    "details": "Sustained investor interest in market segment",
                    "implication": "Market growth expectations remain strong"
                }
            ]
        
        # Calculate market health indicators
        overall_sentiment = np.mean([d.sentiment_score for d in intelligence_data])
        activity_level = len(movements) / 90  # Movements per day
        
        market_health = {
            "overall_sentiment": overall_sentiment,
            "activity_level": activity_level,
            "health_score": min(100, (overall_sentiment + 1) * 50 + activity_level * 10),  # Normalized to 0-100
            "market_stage": "growth" if overall_sentiment > 0.2 and activity_level > 0.2 else "mature" if overall_sentiment > 0 else "declining"
        }
        
        return {
            "status": "success",
            "market_analysis": {
                "analysis_period": "90 days",
                "total_movements_tracked": len(movements),
                "competitors_monitored": len(competitive_service.competitors_db),
                "market_health": market_health
            },
            "trend_categories": trends,
            "strategic_insights": [
                {
                    "insight": "Market shows high innovation velocity",
                    "evidence": f"{len(feature_movements)} product launches in 90 days",
                    "recommendation": "Accelerate product development to maintain competitive position"
                },
                {
                    "insight": "Pricing strategies are being actively tested",
                    "evidence": f"{len(pricing_movements)} pricing changes detected",
                    "recommendation": "Monitor competitor pricing closely and prepare responsive strategies"
                },
                {
                    "insight": "Strategic partnerships are increasing",
                    "evidence": f"{len(partnership_movements)} partnerships announced",
                    "recommendation": "Evaluate potential strategic alliances and integration opportunities"
                }
            ],
            "market_predictions": {
                "next_30_days": "Continued high activity in product launches and pricing adjustments",
                "next_90_days": "Potential market consolidation through partnerships and acquisitions",
                "key_risks": ["Price wars", "New entrant disruption", "Economic downturn impact"],
                "key_opportunities": ["Partnership opportunities", "Market expansion", "Innovation leadership"]
            },
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market trends error: {e}")