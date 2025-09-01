"""
Growth Acceleration Engine - Data Models
Comprehensive data models for growth opportunities, A/B testing, revenue leaks, and ROI tracking
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from enum import Enum
import uuid

# Enums for type safety
class OpportunityType(str, Enum):
    ACQUISITION = "acquisition"
    RETENTION = "retention" 
    EXPANSION = "expansion"

class TestStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class TestType(str, Enum):
    LANDING_PAGE = "landing_page"
    EMAIL_CAMPAIGN = "email_campaign"
    PRICING = "pricing"
    FEATURE_ADOPTION = "feature_adoption"
    ONBOARDING = "onboarding"

class ImplementationEffort(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Priority(str, Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class LeakType(str, Enum):
    CONVERSION_BOTTLENECK = "conversion_bottleneck"
    CHURN_SPIKE = "churn_spike"
    PRICING_ISSUE = "pricing_issue"
    ONBOARDING_DROPOUT = "onboarding_dropout"
    FEATURE_ABANDONMENT = "feature_abandonment"

# Core Models
class GrowthOpportunity(BaseModel):
    """AI-identified growth opportunity"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    type: OpportunityType
    title: str
    description: str
    projected_revenue_impact: float
    confidence_score: float = Field(ge=0, le=1)
    implementation_effort: ImplementationEffort
    priority: Priority
    status: str = "identified"
    ai_reasoning: str
    success_metrics: List[str] = Field(default_factory=list)
    action_steps: List[str] = Field(default_factory=list)
    kpi_tracking: List[str] = Field(default_factory=list)
    estimated_timeline_weeks: int
    market_validation_score: float = Field(ge=0, le=100)
    competitive_advantage: str
    risk_factors: List[str] = Field(default_factory=list)
    implementation_resources_needed: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TestVariant(BaseModel):
    """A/B test variant configuration"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    is_control: bool = False
    variant_data: Dict[str, Any] = Field(default_factory=dict)
    traffic_allocation: float = Field(ge=0, le=1)
    description: str
    hypothesis: str
    expected_improvement: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ABTest(BaseModel):
    """Automated A/B test configuration and results"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    opportunity_id: Optional[str] = None
    name: str
    hypothesis: str
    test_type: TestType
    status: TestStatus = TestStatus.DRAFT
    variants: List[TestVariant] = Field(default_factory=list)
    success_metric: str
    success_metric_description: str
    minimum_sample_size: int
    confidence_level: float = 0.95
    minimum_detectable_effect: float = 0.15
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_duration_days: int
    actual_duration_days: Optional[int] = None
    statistical_significance: Optional[float] = None
    winning_variant_id: Optional[str] = None
    improvement_percentage: Optional[float] = None
    ai_insights: List[str] = Field(default_factory=list)
    next_recommended_tests: List[str] = Field(default_factory=list)
    cost_per_conversion: Optional[float] = None
    roi_projection: Optional[float] = None
    auto_implement_winner: bool = False
    implementation_status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TestResult(BaseModel):
    """A/B test result data point"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    test_id: str
    variant_id: str
    metric_name: str
    metric_value: float
    sample_size: int
    conversion_rate: Optional[float] = None
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    recorded_date: date
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RevenueLeak(BaseModel):
    """Identified revenue leak in customer funnel"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    leak_type: LeakType
    location: str  # Where in the funnel
    title: str
    description: str
    monthly_impact: float  # Revenue impact per month
    annual_impact: float  # Revenue impact per year
    users_affected: int
    current_performance: float
    benchmark_performance: float
    improvement_potential: float
    suggested_fixes: List[Dict[str, Any]] = Field(default_factory=list)
    fix_effort: ImplementationEffort
    priority: Priority
    status: str = "active"
    ai_analysis: str
    root_cause_analysis: List[str] = Field(default_factory=list)
    quick_wins: List[str] = Field(default_factory=list)
    long_term_solutions: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)
    estimated_fix_timeline: int  # weeks
    confidence_score: float = Field(ge=0, le=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ROICalculation(BaseModel):
    """ROI calculation and tracking for initiatives"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    initiative_id: str  # References opportunity, test, or leak fix
    initiative_type: str  # "opportunity", "ab_test", "leak_fix"
    initiative_name: str
    projected_revenue: float
    actual_revenue: Optional[float] = None
    implementation_cost: float
    ongoing_monthly_cost: float
    opportunity_cost: float
    total_investment: float
    payback_period_months: Optional[int] = None
    roi_12_months: float
    roi_24_months: float
    net_present_value: float
    internal_rate_of_return: Optional[float] = None
    risk_adjusted_roi: float
    confidence_level: float = Field(ge=0, le=1)
    assumptions: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    sensitivity_analysis: Dict[str, float] = Field(default_factory=dict)
    status: str = "projected"  # projected, in_progress, completed
    variance_analysis: Optional[Dict[str, Any]] = None
    learning_insights: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FunnelStage(BaseModel):
    """Customer funnel stage data"""
    stage_name: str
    stage_order: int
    users_entering: int
    users_completing: int
    conversion_rate: float
    average_time_in_stage: float  # hours
    drop_off_rate: float
    benchmark_conversion_rate: Optional[float] = None

class CustomerJourney(BaseModel):
    """Customer journey analysis"""
    customer_id: str
    journey_stages: List[FunnelStage]
    total_journey_time: float  # hours
    overall_conversion_rate: float
    bottleneck_stages: List[str] = Field(default_factory=list)
    optimization_opportunities: List[str] = Field(default_factory=list)

class GrowthMetrics(BaseModel):
    """Key growth metrics for dashboard"""
    total_opportunities_identified: int
    total_projected_revenue: float
    active_tests_count: int
    revenue_leaks_fixed: int
    average_roi: float
    total_revenue_saved: float
    implementation_success_rate: float
    average_payback_period: float

class AIInsight(BaseModel):
    """AI-generated insight"""
    insight_type: str
    title: str
    description: str
    confidence_score: float = Field(ge=0, le=1)
    impact_level: str  # "high", "medium", "low"
    actionable: bool = True
    related_data: Dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class GrowthDashboard(BaseModel):
    """Comprehensive growth dashboard data"""
    customer_id: str
    metrics: GrowthMetrics
    top_opportunities: List[GrowthOpportunity]
    active_tests: List[ABTest]
    critical_leaks: List[RevenueLeak]
    ai_insights: List[AIInsight]
    roi_summary: Dict[str, float]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models
class CreateOpportunityRequest(BaseModel):
    customer_data: Dict[str, Any]
    focus_areas: Optional[List[str]] = None
    timeframe_months: int = 12

class CreateTestRequest(BaseModel):
    opportunity_id: Optional[str] = None
    test_name: str
    test_type: TestType
    hypothesis: str
    success_metric: str
    variants: List[Dict[str, Any]]
    minimum_detectable_effect: float = 0.15
    confidence_level: float = 0.95
    auto_implement_winner: bool = False

class UpdateActualMetricsRequest(BaseModel):
    actual_revenue: float
    actual_costs: float
    actual_timeline: int
    performance_notes: str
    lessons_learned: List[str] = Field(default_factory=list)

class LeakAnalysisRequest(BaseModel):
    customer_data: Dict[str, Any]
    funnel_data: List[Dict[str, Any]]
    focus_areas: Optional[List[str]] = None

# Dashboard Response Models
class OpportunityDashboardResponse(BaseModel):
    opportunities: List[GrowthOpportunity]
    total_count: int
    total_projected_impact: float
    priority_breakdown: Dict[str, int]
    type_breakdown: Dict[str, int]

class TestDashboardResponse(BaseModel):
    active_tests: List[ABTest]
    completed_tests: List[ABTest]
    test_results_summary: Dict[str, Any]
    success_rate: float
    average_improvement: float

class LeakDashboardResponse(BaseModel):
    active_leaks: List[RevenueLeak]
    fixed_leaks: List[RevenueLeak]
    total_monthly_impact: float
    total_annual_impact: float
    priority_breakdown: Dict[str, int]

class ROIDashboardResponse(BaseModel):
    roi_calculations: List[ROICalculation]
    portfolio_roi: float
    total_investment: float
    total_returns: float
    payback_summary: Dict[str, float]