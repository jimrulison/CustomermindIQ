"""
Cohort Analysis - Analytics & Insights Module
Advanced customer cohort analysis and retention modeling
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, date
import random
import uuid
import numpy as np
import pandas as pd
from enum import Enum

# Initialize router
cohort_analysis_router = APIRouter()

class CohortType(str, Enum):
    ACQUISITION_DATE = "acquisition_date"
    CAMPAIGN = "campaign"
    PRODUCT_VERSION = "product_version"
    CHANNEL = "channel"
    GEOGRAPHIC = "geographic"
    BEHAVIORAL = "behavioral"

class CohortPeriod(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

class CohortCustomer(BaseModel):
    customer_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cohort_id: str
    acquisition_date: date
    first_purchase_amount: float
    channel: str
    campaign: Optional[str] = None
    geographic_region: str
    product_version: str

class CohortMetric(BaseModel):
    cohort_id: str
    period: int  # Period number (0 = acquisition period, 1 = first period after, etc.)
    retention_rate: float
    revenue_per_customer: float
    customer_count: int
    total_revenue: float
    churn_rate: float
    expansion_revenue: float

class CohortAnalysisResult(BaseModel):
    cohort_type: CohortType
    cohort_period: CohortPeriod
    cohorts: List[str]
    metrics: List[CohortMetric]
    retention_curves: Dict[str, List[float]]
    revenue_curves: Dict[str, List[float]]

class PredictiveCohortInsight(BaseModel):
    cohort_id: str
    predicted_ltv: float
    predicted_retention_12m: float
    early_health_indicators: List[str]
    risk_factors: List[str]
    intervention_recommendations: List[str]

class CohortAnalysisService:
    """Advanced Cohort Analysis Service"""
    
    def __init__(self):
        self.channels = ["organic_search", "paid_search", "email", "social_media", "referral", "direct"]
        self.campaigns = ["Brand Campaign Q4", "Product Launch", "Retention Campaign", "Acquisition Push", "Referral Program"]
        self.regions = ["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East"]
        self.product_versions = ["v1.0", "v1.1", "v1.2", "v2.0", "v2.1"]
    
    async def generate_cohort_data(self, num_customers: int = 500, months_back: int = 12) -> List[CohortCustomer]:
        """Generate realistic cohort customer data"""
        customers = []
        
        for i in range(num_customers):
            # Random acquisition date within the last months_back months
            days_back = random.randint(0, months_back * 30)
            acquisition_date = (datetime.now() - timedelta(days=days_back)).date()
            
            # Generate cohort assignment based on acquisition month
            cohort_id = f"cohort_{acquisition_date.year}_{acquisition_date.month:02d}"
            
            customer = CohortCustomer(
                cohort_id=cohort_id,
                acquisition_date=acquisition_date,
                first_purchase_amount=random.uniform(50, 2000),
                channel=random.choice(self.channels),
                campaign=random.choice(self.campaigns) if random.random() < 0.7 else None,
                geographic_region=random.choice(self.regions),
                product_version=random.choice(self.product_versions)
            )
            customers.append(customer)
        
        return customers
    
    async def calculate_cohort_metrics(self, customers: List[CohortCustomer], cohort_type: CohortType, cohort_period: CohortPeriod) -> CohortAnalysisResult:
        """Calculate comprehensive cohort metrics"""
        
        # Group customers by cohort
        cohorts = {}
        for customer in customers:
            cohort_key = self._get_cohort_key(customer, cohort_type)
            if cohort_key not in cohorts:
                cohorts[cohort_key] = []
            cohorts[cohort_key].append(customer)
        
        # Calculate metrics for each cohort and period
        all_metrics = []
        retention_curves = {}
        revenue_curves = {}
        
        for cohort_id, cohort_customers in cohorts.items():
            if len(cohort_customers) < 5:  # Skip small cohorts
                continue
                
            cohort_metrics, retention_curve, revenue_curve = await self._calculate_cohort_performance(
                cohort_id, cohort_customers, cohort_period
            )
            
            all_metrics.extend(cohort_metrics)
            retention_curves[cohort_id] = retention_curve
            revenue_curves[cohort_id] = revenue_curve
        
        return CohortAnalysisResult(
            cohort_type=cohort_type,
            cohort_period=cohort_period,
            cohorts=list(cohorts.keys()),
            metrics=all_metrics,
            retention_curves=retention_curves,
            revenue_curves=revenue_curves
        )
    
    def _get_cohort_key(self, customer: CohortCustomer, cohort_type: CohortType) -> str:
        """Get cohort key based on cohort type"""
        if cohort_type == CohortType.ACQUISITION_DATE:
            return customer.cohort_id
        elif cohort_type == CohortType.CAMPAIGN:
            return customer.campaign or "no_campaign"
        elif cohort_type == CohortType.PRODUCT_VERSION:
            return customer.product_version
        elif cohort_type == CohortType.CHANNEL:
            return customer.channel
        elif cohort_type == CohortType.GEOGRAPHIC:
            return customer.geographic_region
        else:
            return customer.cohort_id
    
    async def _calculate_cohort_performance(self, cohort_id: str, customers: List[CohortCustomer], period: CohortPeriod) -> tuple:
        """Calculate performance metrics for a specific cohort"""
        initial_count = len(customers)
        initial_revenue = sum(c.first_purchase_amount for c in customers)
        
        # Calculate periods to analyze (up to 12 periods)
        max_periods = 12
        period_length_days = {
            CohortPeriod.WEEKLY: 7,
            CohortPeriod.MONTHLY: 30,
            CohortPeriod.QUARTERLY: 90
        }[period]
        
        metrics = []
        retention_curve = []
        revenue_curve = []
        
        # Get the earliest acquisition date for this cohort
        min_acquisition_date = min(c.acquisition_date for c in customers)
        
        for period_num in range(max_periods):
            period_start = min_acquisition_date + timedelta(days=period_num * period_length_days)
            period_end = period_start + timedelta(days=period_length_days)
            
            # Simulate customer behavior for this period
            active_customers = self._simulate_customer_activity(customers, period_num, initial_count)
            
            if active_customers > 0:
                retention_rate = active_customers / initial_count
                revenue_per_customer = random.uniform(50, 300) * (0.9 ** period_num)  # Decreasing over time
                total_revenue = revenue_per_customer * active_customers
                churn_rate = 1 - retention_rate if period_num > 0 else 0
                expansion_revenue = random.uniform(0, 100) * active_customers if period_num > 2 else 0
                
                metric = CohortMetric(
                    cohort_id=cohort_id,
                    period=period_num,
                    retention_rate=retention_rate,
                    revenue_per_customer=revenue_per_customer,
                    customer_count=active_customers,
                    total_revenue=total_revenue,
                    churn_rate=churn_rate,
                    expansion_revenue=expansion_revenue
                )
                metrics.append(metric)
                retention_curve.append(retention_rate)
                revenue_curve.append(revenue_per_customer)
            else:
                retention_curve.append(0.0)
                revenue_curve.append(0.0)
        
        return metrics, retention_curve, revenue_curve
    
    def _simulate_customer_activity(self, customers: List[CohortCustomer], period_num: int, initial_count: int) -> int:
        """Simulate customer activity for a given period"""
        if period_num == 0:
            return initial_count
        
        # Simulate retention with realistic decay
        base_retention = 0.85  # 85% retention in first period
        decay_rate = 0.95  # 5% additional decay each period
        
        # Channel-based retention differences
        channel_retention_multipliers = {
            "organic_search": 1.1,
            "referral": 1.15,
            "direct": 1.2,
            "email": 1.05,
            "paid_search": 0.9,
            "social_media": 0.85
        }
        
        # Calculate weighted retention based on customer channels
        channel_weights = {}
        for customer in customers:
            channel = customer.channel
            if channel not in channel_weights:
                channel_weights[channel] = 0
            channel_weights[channel] += 1
        
        # Calculate average retention multiplier
        total_customers = len(customers)
        avg_multiplier = sum(
            (count / total_customers) * channel_retention_multipliers.get(channel, 1.0)
            for channel, count in channel_weights.items()
        )
        
        # Calculate retention for this period
        period_retention = base_retention * (decay_rate ** period_num) * avg_multiplier
        active_customers = int(initial_count * period_retention)
        
        return max(0, active_customers)
    
    async def generate_predictive_insights(self, cohort_results: CohortAnalysisResult) -> List[PredictiveCohortInsight]:
        """Generate AI-powered predictive insights for cohorts"""
        insights = []
        
        for cohort_id in cohort_results.cohorts:
            # Get cohort metrics
            cohort_metrics = [m for m in cohort_results.metrics if m.cohort_id == cohort_id]
            if not cohort_metrics:
                continue
            
            # Calculate predictive metrics
            retention_curve = cohort_results.retention_curves.get(cohort_id, [])
            revenue_curve = cohort_results.revenue_curves.get(cohort_id, [])
            
            # Predict 12-month retention
            if len(retention_curve) >= 3:
                # Simple exponential decay prediction
                recent_retention = retention_curve[:3]
                decay_rate = (recent_retention[0] / recent_retention[2]) ** (1/2) if recent_retention[2] > 0 else 0.9
                predicted_12m_retention = recent_retention[0] * (decay_rate ** 12)
            else:
                predicted_12m_retention = 0.5
            
            # Predict LTV
            if revenue_curve:
                avg_revenue_per_period = np.mean(revenue_curve[:6])  # First 6 periods
                predicted_ltv = avg_revenue_per_period * 12 * predicted_12m_retention
            else:
                predicted_ltv = 1000
            
            # Generate health indicators and recommendations
            early_indicators = []
            risk_factors = []
            recommendations = []
            
            # Analyze early retention (first 3 periods)
            if len(retention_curve) >= 3:
                first_period_retention = retention_curve[1] if len(retention_curve) > 1 else 0.8
                third_period_retention = retention_curve[2] if len(retention_curve) > 2 else 0.6
                
                if first_period_retention > 0.8:
                    early_indicators.append("Strong early engagement")
                if third_period_retention > 0.6:
                    early_indicators.append("Good mid-term retention")
                
                if first_period_retention < 0.6:
                    risk_factors.append("Poor initial retention")
                    recommendations.append("Implement onboarding improvement program")
                
                if len(retention_curve) > 1 and retention_curve[1] / retention_curve[0] < 0.7:
                    risk_factors.append("Steep retention drop-off")
                    recommendations.append("Add retention campaigns after first purchase")
            
            # Revenue-based insights
            if revenue_curve and len(revenue_curve) >= 2:
                if revenue_curve[1] > revenue_curve[0]:
                    early_indicators.append("Increasing customer value")
                elif revenue_curve[1] < revenue_curve[0] * 0.7:
                    risk_factors.append("Declining customer value")
                    recommendations.append("Focus on upselling and cross-selling")
            
            insight = PredictiveCohortInsight(
                cohort_id=cohort_id,
                predicted_ltv=predicted_ltv,
                predicted_retention_12m=predicted_12m_retention,
                early_health_indicators=early_indicators or ["Standard performance metrics"],
                risk_factors=risk_factors or ["No significant risk factors identified"],
                intervention_recommendations=recommendations or ["Continue monitoring performance"]
            )
            insights.append(insight)
        
        return insights
    
    async def compare_cohorts(self, cohort_results: CohortAnalysisResult) -> Dict[str, Any]:
        """Compare performance across different cohorts"""
        if len(cohort_results.cohorts) < 2:
            return {"message": "Need at least 2 cohorts for comparison"}
        
        # Calculate comparative metrics
        cohort_summary = {}
        for cohort_id in cohort_results.cohorts:
            cohort_metrics = [m for m in cohort_results.metrics if m.cohort_id == cohort_id]
            if not cohort_metrics:
                continue
            
            # Calculate summary metrics for this cohort
            total_customers = cohort_metrics[0].customer_count if cohort_metrics else 0
            avg_retention = np.mean([m.retention_rate for m in cohort_metrics[:6]])  # First 6 periods
            total_revenue = sum(m.total_revenue for m in cohort_metrics)
            avg_revenue_per_customer = total_revenue / total_customers if total_customers > 0 else 0
            
            cohort_summary[cohort_id] = {
                "total_customers": total_customers,
                "avg_retention_rate": avg_retention,
                "total_revenue": total_revenue,
                "revenue_per_customer": avg_revenue_per_customer,
                "retention_curve": cohort_results.retention_curves.get(cohort_id, [])[:6]
            }
        
        # Find best and worst performing cohorts
        best_retention = max(cohort_summary.items(), key=lambda x: x[1]['avg_retention_rate'])
        worst_retention = min(cohort_summary.items(), key=lambda x: x[1]['avg_retention_rate'])
        
        best_revenue = max(cohort_summary.items(), key=lambda x: x[1]['revenue_per_customer'])
        worst_revenue = min(cohort_summary.items(), key=lambda x: x[1]['revenue_per_customer'])
        
        # Calculate performance gaps
        retention_gap = best_retention[1]['avg_retention_rate'] - worst_retention[1]['avg_retention_rate']
        revenue_gap = best_revenue[1]['revenue_per_customer'] - worst_revenue[1]['revenue_per_customer']
        
        return {
            "cohort_summary": cohort_summary,
            "performance_leaders": {
                "best_retention": {
                    "cohort_id": best_retention[0],
                    "retention_rate": best_retention[1]['avg_retention_rate']
                },
                "best_revenue": {
                    "cohort_id": best_revenue[0],
                    "revenue_per_customer": best_revenue[1]['revenue_per_customer']
                }
            },
            "performance_gaps": {
                "retention_gap": retention_gap,
                "revenue_gap": revenue_gap,
                "improvement_potential": f"Bringing worst-performing cohorts to best-performer level could increase overall retention by {retention_gap:.1%}"
            },
            "cohort_trends": {
                "improving_cohorts": [
                    cohort_id for cohort_id, data in cohort_summary.items()
                    if len(data['retention_curve']) >= 3 and data['retention_curve'][2] > data['retention_curve'][1]
                ],
                "declining_cohorts": [
                    cohort_id for cohort_id, data in cohort_summary.items()
                    if len(data['retention_curve']) >= 3 and data['retention_curve'][2] < data['retention_curve'][1] * 0.8
                ]
            }
        }

# Initialize service
cohort_service = CohortAnalysisService()

@cohort_analysis_router.get("/api/analytics/cohort-analysis/dashboard")
async def get_cohort_dashboard():
    """Get cohort analysis dashboard data"""
    try:
        # Generate cohort data
        customers = await cohort_service.generate_cohort_data(400, 12)
        
        # Analyze acquisition date cohorts (monthly)
        cohort_results = await cohort_service.calculate_cohort_metrics(
            customers, CohortType.ACQUISITION_DATE, CohortPeriod.MONTHLY
        )
        
        # Generate predictive insights
        insights = await cohort_service.generate_predictive_insights(cohort_results)
        
        # Compare cohorts
        comparison = await cohort_service.compare_cohorts(cohort_results)
        
        # Calculate overall metrics
        total_customers = len(customers)
        total_cohorts = len(cohort_results.cohorts)
        
        # Calculate average metrics across all cohorts
        all_retention_rates = [m.retention_rate for m in cohort_results.metrics if m.period == 1]  # 1-month retention
        avg_retention = np.mean(all_retention_rates) if all_retention_rates else 0
        
        all_revenue_per_customer = [m.revenue_per_customer for m in cohort_results.metrics if m.period <= 3]
        avg_revenue_per_customer = np.mean(all_revenue_per_customer) if all_revenue_per_customer else 0
        
        return {
            "status": "success",
            "dashboard_data": {
                "overview": {
                    "total_customers_analyzed": total_customers,
                    "total_cohorts": total_cohorts,
                    "average_retention_rate_1m": avg_retention,
                    "average_revenue_per_customer": avg_revenue_per_customer,
                    "cohort_analysis_period": "12 months"
                },
                "cohort_performance": {
                    cohort_id: {
                        "customer_count": len([c for c in customers if cohort_service._get_cohort_key(c, CohortType.ACQUISITION_DATE) == cohort_id]),
                        "retention_curve": cohort_results.retention_curves.get(cohort_id, [])[:6],
                        "revenue_curve": cohort_results.revenue_curves.get(cohort_id, [])[:6],
                        "predicted_ltv": next((i.predicted_ltv for i in insights if i.cohort_id == cohort_id), 0)
                    }
                    for cohort_id in cohort_results.cohorts[:8]  # Show top 8 cohorts
                },
                "retention_heatmap": {
                    "cohorts": cohort_results.cohorts[:10],
                    "periods": list(range(6)),  # Show first 6 periods
                    "retention_matrix": [
                        cohort_results.retention_curves.get(cohort_id, [])[:6]
                        for cohort_id in cohort_results.cohorts[:10]
                    ]
                },
                "trend_analysis": {
                    "improving_cohorts_count": len(comparison.get("cohort_trends", {}).get("improving_cohorts", [])),
                    "declining_cohorts_count": len(comparison.get("cohort_trends", {}).get("declining_cohorts", [])),
                    "retention_improvement_potential": comparison.get("performance_gaps", {}).get("improvement_potential", "No data available")
                }
            },
            "predictive_insights": [
                {
                    "cohort_id": insight.cohort_id,
                    "predicted_ltv": insight.predicted_ltv,
                    "predicted_retention_12m": insight.predicted_retention_12m,
                    "health_score": "Healthy" if insight.predicted_retention_12m > 0.4 else "At Risk",
                    "key_recommendations": insight.intervention_recommendations[:2]
                }
                for insight in insights[:10]
            ],
            "comparison_insights": comparison,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cohort dashboard error: {e}")

@cohort_analysis_router.post("/api/analytics/cohort-analysis/custom-analysis")
async def perform_custom_cohort_analysis(request: Dict):
    """Perform custom cohort analysis with specific parameters"""
    try:
        cohort_type = CohortType(request.get('cohort_type', 'acquisition_date'))
        cohort_period = CohortPeriod(request.get('cohort_period', 'monthly'))
        months_back = request.get('months_back', 12)
        customer_count = request.get('customer_count', 300)
        
        # Generate cohort data
        customers = await cohort_service.generate_cohort_data(customer_count, months_back)
        
        # Perform analysis
        cohort_results = await cohort_service.calculate_cohort_metrics(customers, cohort_type, cohort_period)
        
        # Generate insights
        insights = await cohort_service.generate_predictive_insights(cohort_results)
        
        # Calculate custom metrics
        custom_metrics = {}
        
        if cohort_type == CohortType.CHANNEL:
            # Channel-specific analysis
            for cohort_id in cohort_results.cohorts:
                channel_customers = [c for c in customers if c.channel == cohort_id]
                if channel_customers:
                    avg_first_purchase = np.mean([c.first_purchase_amount for c in channel_customers])
                    custom_metrics[cohort_id] = {
                        "avg_first_purchase_amount": avg_first_purchase,
                        "customer_acquisition_cost": avg_first_purchase * 0.3,  # Assume 30% CAC
                        "channel_efficiency_score": avg_first_purchase / (avg_first_purchase * 0.3)
                    }
        
        elif cohort_type == CohortType.CAMPAIGN:
            # Campaign-specific analysis
            for cohort_id in cohort_results.cohorts:
                campaign_customers = [c for c in customers if c.campaign == cohort_id]
                if campaign_customers:
                    cohort_metrics = [m for m in cohort_results.metrics if m.cohort_id == cohort_id]
                    total_revenue = sum(m.total_revenue for m in cohort_metrics)
                    custom_metrics[cohort_id] = {
                        "total_campaign_revenue": total_revenue,
                        "customer_count": len(campaign_customers),
                        "revenue_per_customer": total_revenue / len(campaign_customers) if campaign_customers else 0
                    }
        
        return {
            "status": "success",
            "analysis_parameters": {
                "cohort_type": cohort_type.value,
                "cohort_period": cohort_period.value,
                "months_analyzed": months_back,
                "customers_analyzed": len(customers)
            },
            "cohort_results": {
                "cohorts": cohort_results.cohorts,
                "total_cohorts": len(cohort_results.cohorts),
                "retention_curves": cohort_results.retention_curves,
                "revenue_curves": cohort_results.revenue_curves
            },
            "custom_metrics": custom_metrics,
            "predictive_insights": [insight.dict() for insight in insights],
            "key_findings": [
                f"Analyzed {len(customers)} customers across {len(cohort_results.cohorts)} {cohort_type.value} cohorts",
                f"Average {cohort_period.value} retention varies from {min([min(curve) for curve in cohort_results.retention_curves.values()]):.1%} to {max([max(curve) for curve in cohort_results.retention_curves.values()]):.1%}",
                f"Best performing cohort: {max(cohort_results.retention_curves.items(), key=lambda x: max(x[1]))[0]}"
            ],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom cohort analysis error: {e}")

@cohort_analysis_router.get("/api/analytics/cohort-analysis/retention-forecast")
async def get_retention_forecast():
    """Get retention forecasting for existing cohorts"""
    try:
        # Generate data for forecasting
        customers = await cohort_service.generate_cohort_data(350, 6)  # 6 months of data
        
        # Analyze current cohorts
        cohort_results = await cohort_service.calculate_cohort_metrics(
            customers, CohortType.ACQUISITION_DATE, CohortPeriod.MONTHLY
        )
        
        # Generate forecasts for each cohort
        forecasts = {}
        
        for cohort_id in cohort_results.cohorts:
            retention_curve = cohort_results.retention_curves.get(cohort_id, [])
            
            if len(retention_curve) >= 3:
                # Simple exponential forecasting
                current_data = retention_curve[:6]  # Use first 6 months
                
                # Calculate trend
                if len(current_data) >= 2:
                    decay_rate = np.mean([current_data[i] / current_data[i-1] for i in range(1, len(current_data)) if current_data[i-1] > 0])
                    
                    # Forecast next 6 months
                    forecast_periods = 6
                    forecasted_retention = []
                    last_value = current_data[-1]
                    
                    for period in range(forecast_periods):
                        forecasted_value = last_value * (decay_rate ** (period + 1))
                        forecasted_retention.append(max(0.05, forecasted_value))  # Minimum 5% retention
                    
                    # Calculate forecast confidence (simulated)
                    confidence_score = max(0.6, 1.0 - (len(current_data) * 0.05))  # Decreases with more data points
                    
                    forecasts[cohort_id] = {
                        "current_retention_curve": current_data,
                        "forecasted_retention": forecasted_retention,
                        "forecast_confidence": confidence_score,
                        "predicted_12m_retention": forecasted_retention[-1] if forecasted_retention else 0.1,
                        "trend": "declining" if decay_rate < 0.95 else "stable" if decay_rate < 1.05 else "improving"
                    }
        
        # Calculate overall forecast metrics
        all_12m_predictions = [f["predicted_12m_retention"] for f in forecasts.values()]
        avg_12m_retention = np.mean(all_12m_predictions) if all_12m_predictions else 0
        
        # Identify cohorts needing intervention
        at_risk_cohorts = [
            cohort_id for cohort_id, forecast in forecasts.items()
            if forecast["predicted_12m_retention"] < 0.3
        ]
        
        return {
            "status": "success",
            "forecast_summary": {
                "cohorts_analyzed": len(forecasts),
                "average_predicted_12m_retention": avg_12m_retention,
                "at_risk_cohorts_count": len(at_risk_cohorts),
                "forecast_horizon_months": 6
            },
            "cohort_forecasts": forecasts,
            "intervention_recommendations": {
                "immediate_attention": at_risk_cohorts,
                "recommended_actions": [
                    "Implement retention campaigns for at-risk cohorts",
                    "A/B test onboarding improvements for new cohorts",
                    "Analyze successful cohorts to identify best practices"
                ],
                "budget_allocation": {
                    "retention_campaigns": "40% of marketing budget",
                    "acquisition_optimization": "35% of marketing budget", 
                    "product_improvements": "25% of marketing budget"
                }
            },
            "forecast_accuracy_note": "Forecasts based on exponential trend analysis. Actual results may vary due to external factors, product changes, and market conditions.",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retention forecast error: {e}")