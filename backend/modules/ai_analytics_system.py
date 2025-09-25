# Phase 3: AI-Powered Analytics & Real-Time Reporting System
# Advanced analytics with machine learning insights and predictions

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Any, Union
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
import asyncio
import json
import logging
from enum import Enum
import uuid
from dataclasses import dataclass
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
import httpx
import os
from dotenv import load_dotenv

# Import authentication
from auth.auth_system import get_current_user, UserProfile, require_role, UserRole

# =============================================================================
# Analytics Models and Configuration
# =============================================================================

class AnalyticsTimeframe(str, Enum):
    HOUR = "1h"
    DAY = "1d" 
    WEEK = "7d"
    MONTH = "30d"
    QUARTER = "90d"
    YEAR = "365d"
    CUSTOM = "custom"

class MetricType(str, Enum):
    CLICKS = "clicks"
    CONVERSIONS = "conversions"
    REVENUE = "revenue"
    COMMISSIONS = "commissions"
    CONVERSION_RATE = "conversion_rate"
    AVERAGE_ORDER_VALUE = "aov"
    CUSTOMER_LIFETIME_VALUE = "clv"
    RETURN_ON_AD_SPEND = "roas"

class InsightType(str, Enum):
    PERFORMANCE_ALERT = "performance_alert"
    OPTIMIZATION_SUGGESTION = "optimization_suggestion"
    TREND_ANALYSIS = "trend_analysis"
    ANOMALY_DETECTION = "anomaly_detection"
    PREDICTIVE_FORECAST = "predictive_forecast"
    COMPETITIVE_ANALYSIS = "competitive_analysis"

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    OPPORTUNITY = "opportunity"

class RealTimeMetrics(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    affiliate_id: str
    site_id: str
    
    # Core metrics
    clicks_1h: int = 0
    clicks_24h: int = 0
    conversions_1h: int = 0
    conversions_24h: int = 0
    revenue_1h: float = 0.0
    revenue_24h: float = 0.0
    
    # Calculated metrics
    conversion_rate_1h: float = 0.0
    conversion_rate_24h: float = 0.0
    avg_order_value_24h: float = 0.0
    
    # Performance indicators
    performance_score: float = 0.0
    trend_direction: str = "stable"  # up, down, stable
    anomaly_score: float = 0.0

class AIInsight(BaseModel):
    insight_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    affiliate_id: str
    site_id: Optional[str] = None
    insight_type: InsightType
    severity: AlertSeverity
    title: str
    description: str
    
    # Data supporting the insight
    supporting_data: Dict[str, Any]
    confidence_score: float  # 0.0 to 1.0
    
    # Recommendations
    recommended_actions: List[str] = []
    estimated_impact: Dict[str, float] = {}  # revenue, conversions, etc.
    
    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    is_acknowledged: bool = False
    
class PerformancePrediction(BaseModel):
    prediction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    affiliate_id: str
    site_id: Optional[str] = None
    
    # Prediction timeframe
    forecast_date: datetime
    forecast_period_days: int
    
    # Predicted metrics
    predicted_clicks: float
    predicted_conversions: float
    predicted_revenue: float
    predicted_commissions: float
    
    # Confidence intervals
    clicks_confidence_interval: tuple
    revenue_confidence_interval: tuple
    
    # Model metadata
    model_accuracy: float
    model_version: str
    features_used: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# =============================================================================
# AI Analytics Engine
# =============================================================================

class AIAnalyticsEngine:
    """Advanced analytics engine with machine learning capabilities"""
    
    def __init__(self):
        # Initialize database connections
        load_dotenv()
        MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        DB_NAME = os.getenv("DB_NAME", "customer_mind_iq")
        
        client = AsyncIOMotorClient(MONGO_URL)
        self.db = client[DB_NAME]
        
        # Initialize Redis
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/3")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Initialize ML models (simplified versions without external dependencies)
        self.models_initialized = False
        self.initialize_simple_models()
    
    def initialize_simple_models(self):
        """Initialize simple statistical models without heavy ML dependencies"""
        try:
            # Simple statistical thresholds for anomaly detection
            self.anomaly_thresholds = {
                'conversion_rate_low': 0.01,  # 1%
                'conversion_rate_high': 0.15,  # 15%
                'revenue_spike_multiplier': 3.0,  # 3x average
                'traffic_spike_multiplier': 2.5   # 2.5x average
            }
            
            # Performance benchmarks
            self.benchmarks = {
                'conversion_rate': 0.035,  # 3.5%
                'avg_order_value': 75.0,
                'customer_lifetime_value': 250.0,
                'daily_revenue': 500.0
            }
            
            self.models_initialized = True
            logging.info("✅ Simple analytics models initialized successfully")
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize analytics models: {e}")
    
    async def generate_real_time_insights(self, affiliate_id: str, timeframe_hours: int = 24) -> List[AIInsight]:
        """Generate AI-powered insights for an affiliate"""
        
        insights = []
        
        try:
            # Get recent performance data
            performance_data = await self.get_performance_data(affiliate_id, timeframe_hours)
            
            if not performance_data or len(performance_data) == 0:
                # Generate insight about lack of data
                insight = AIInsight(
                    affiliate_id=affiliate_id,
                    insight_type=InsightType.PERFORMANCE_ALERT,
                    severity=AlertSeverity.WARNING,
                    title="Limited Performance Data",
                    description=f"No performance data found for the last {timeframe_hours} hours. This could indicate tracking issues or very low activity.",
                    supporting_data={"timeframe_hours": timeframe_hours, "data_points": 0},
                    confidence_score=0.9,
                    recommended_actions=[
                        "Check if tracking is properly implemented",
                        "Verify affiliate links are working",
                        "Review recent campaign activity",
                        "Contact support if issues persist"
                    ]
                )
                insights.append(insight)
                return insights
            
            # Anomaly detection
            anomaly_insights = await self.detect_performance_anomalies(affiliate_id, performance_data)
            insights.extend(anomaly_insights)
            
            # Trend analysis
            trend_insights = await self.analyze_performance_trends(affiliate_id, performance_data)
            insights.extend(trend_insights)
            
            # Optimization suggestions
            optimization_insights = await self.generate_optimization_suggestions(affiliate_id, performance_data)
            insights.extend(optimization_insights)
            
            # Predictive insights
            predictive_insights = await self.generate_predictive_insights(affiliate_id, performance_data)
            insights.extend(predictive_insights)
            
        except Exception as e:
            logging.error(f"Error generating insights for {affiliate_id}: {e}")
            # Generate error insight
            insights.append(AIInsight(
                affiliate_id=affiliate_id,
                insight_type=InsightType.PERFORMANCE_ALERT,
                severity=AlertSeverity.WARNING,
                title="Analytics Processing Error",
                description="There was an error processing your analytics data. Please try again later.",
                supporting_data={"error": str(e)},
                confidence_score=1.0,
                recommended_actions=["Refresh the page", "Contact support if the issue persists"]
            ))
        
        return insights
    
    async def detect_performance_anomalies(self, affiliate_id: str, data: List[Dict]) -> List[AIInsight]:
        """Detect anomalies in affiliate performance using statistical analysis"""
        
        insights = []
        
        try:
            if len(data) < 3:  # Need minimum data points
                return insights
            
            # Convert to simple analysis format
            conversion_rates = [d.get('conversion_rate', 0) for d in data]
            revenues = [d.get('revenue', 0) for d in data]
            clicks = [d.get('clicks', 0) for d in data]
            
            # Calculate basic statistics
            avg_cr = sum(conversion_rates) / len(conversion_rates) if conversion_rates else 0
            avg_revenue = sum(revenues) / len(revenues) if revenues else 0
            avg_clicks = sum(clicks) / len(clicks) if clicks else 0
            
            # Find recent performance (last entry)
            recent_data = data[-1] if data else {}
            recent_cr = recent_data.get('conversion_rate', 0)
            recent_revenue = recent_data.get('revenue', 0)
            recent_clicks = recent_data.get('clicks', 0)
            
            # Anomaly Detection: Low conversion rate
            if recent_cr < avg_cr * 0.5 and recent_cr < self.anomaly_thresholds['conversion_rate_low']:
                insight = AIInsight(
                    affiliate_id=affiliate_id,
                    insight_type=InsightType.ANOMALY_DETECTION,
                    severity=AlertSeverity.WARNING,
                    title="Low Conversion Rate Detected",
                    description=f"Recent conversion rate ({recent_cr:.2%}) is significantly below your average ({avg_cr:.2%}). "
                              f"This represents a {((avg_cr - recent_cr) / avg_cr * 100):.1f}% decline.",
                    supporting_data={
                        "current_rate": recent_cr,
                        "average_rate": avg_cr,
                        "decline_percentage": ((avg_cr - recent_cr) / avg_cr * 100) if avg_cr > 0 else 0,
                        "recent_clicks": recent_clicks
                    },
                    confidence_score=0.85,
                    recommended_actions=[
                        "Review recent traffic sources for quality issues",
                        "Check landing page performance and load times",
                        "Analyze user feedback for usability problems",
                        "Test different call-to-action messages",
                        "Verify tracking is working correctly"
                    ],
                    estimated_impact={
                        "potential_revenue_recovery": recent_clicks * avg_cr * (avg_revenue / max(avg_clicks, 1)) - recent_revenue
                    }
                )
                insights.append(insight)
            
            # Anomaly Detection: Revenue spike (opportunity)
            if recent_revenue > avg_revenue * self.anomaly_thresholds['revenue_spike_multiplier']:
                insight = AIInsight(
                    affiliate_id=affiliate_id,
                    insight_type=InsightType.ANOMALY_DETECTION,
                    severity=AlertSeverity.OPPORTUNITY,
                    title="Exceptional Revenue Performance",
                    description=f"Recent revenue (${recent_revenue:,.2f}) is {((recent_revenue - avg_revenue) / avg_revenue * 100):.1f}% "
                              f"above your average (${avg_revenue:,.2f}). Excellent performance!",
                    supporting_data={
                        "recent_revenue": recent_revenue,
                        "average_revenue": avg_revenue,
                        "performance_lift": ((recent_revenue - avg_revenue) / avg_revenue) if avg_revenue > 0 else 0
                    },
                    confidence_score=0.9,
                    recommended_actions=[
                        "Analyze what drove this exceptional performance",
                        "Document successful campaign elements for replication",
                        "Scale up similar campaign approaches",
                        "Share winning strategies across other campaigns",
                        "Consider increasing marketing budget for high-performing channels"
                    ],
                    estimated_impact={
                        "replication_potential": (recent_revenue - avg_revenue) * 30  # 30-day potential
                    }
                )
                insights.append(insight)
            
            # Anomaly Detection: Traffic spike without conversions
            if recent_clicks > avg_clicks * self.anomaly_thresholds['traffic_spike_multiplier'] and recent_cr < avg_cr * 0.7:
                insight = AIInsight(
                    affiliate_id=affiliate_id,
                    insight_type=InsightType.ANOMALY_DETECTION,
                    severity=AlertSeverity.WARNING,
                    title="Traffic Spike with Low Conversion Rate",
                    description=f"Traffic increased to {recent_clicks} clicks (vs {avg_clicks:.0f} average) but "
                              f"conversion rate dropped to {recent_cr:.2%}. This suggests potential traffic quality issues.",
                    supporting_data={
                        "recent_clicks": recent_clicks,
                        "average_clicks": avg_clicks,
                        "recent_conversion_rate": recent_cr,
                        "average_conversion_rate": avg_cr,
                        "traffic_increase": ((recent_clicks - avg_clicks) / avg_clicks) if avg_clicks > 0 else 0
                    },
                    confidence_score=0.8,
                    recommended_actions=[
                        "Investigate traffic sources for the spike period",
                        "Check for bot traffic or click fraud",
                        "Review ad targeting and audience quality",
                        "Analyze user behavior during high-traffic periods",
                        "Consider pausing underperforming traffic sources"
                    ],
                    estimated_impact={
                        "potential_wasted_spend": (recent_clicks - avg_clicks) * 0.50  # Assume $0.50 CPC
                    }
                )
                insights.append(insight)
        
        except Exception as e:
            logging.error(f"Error in anomaly detection for {affiliate_id}: {e}")
        
        return insights
    
    async def analyze_performance_trends(self, affiliate_id: str, data: List[Dict]) -> List[AIInsight]:
        """Analyze performance trends and generate insights"""
        
        insights = []
        
        try:
            if len(data) < 7:  # Need at least a week of data
                return insights
            
            # Split data into recent vs previous periods
            mid_point = len(data) // 2
            recent_period = data[mid_point:]
            previous_period = data[:mid_point]
            
            # Calculate averages for each period
            def calculate_averages(period_data):
                if not period_data:
                    return {'revenue': 0, 'conversion_rate': 0, 'clicks': 0}
                
                return {
                    'revenue': sum(d.get('revenue', 0) for d in period_data) / len(period_data),
                    'conversion_rate': sum(d.get('conversion_rate', 0) for d in period_data) / len(period_data),
                    'clicks': sum(d.get('clicks', 0) for d in period_data) / len(period_data)
                }
            
            recent_avg = calculate_averages(recent_period)
            previous_avg = calculate_averages(previous_period)
            
            # Revenue trend analysis
            if previous_avg['revenue'] > 0:
                revenue_change = (recent_avg['revenue'] - previous_avg['revenue']) / previous_avg['revenue']
                
                if abs(revenue_change) > 0.15:  # 15% change threshold
                    severity = AlertSeverity.OPPORTUNITY if revenue_change > 0 else AlertSeverity.WARNING
                    direction = "increased" if revenue_change > 0 else "decreased"
                    
                    insight = AIInsight(
                        affiliate_id=affiliate_id,
                        insight_type=InsightType.TREND_ANALYSIS,
                        severity=severity,
                        title=f"Revenue Trend: {direction.title()} {abs(revenue_change):.1%}",
                        description=f"Your average revenue has {direction} by {abs(revenue_change):.1%} "
                                  f"compared to the previous period (${recent_avg['revenue']:,.2f} vs ${previous_avg['revenue']:,.2f}).",
                        supporting_data={
                            "recent_avg_revenue": recent_avg['revenue'],
                            "previous_avg_revenue": previous_avg['revenue'],
                            "change_percentage": revenue_change,
                            "trend_direction": "up" if revenue_change > 0 else "down",
                            "period_length_days": len(recent_period)
                        },
                        confidence_score=min(abs(revenue_change) * 2, 0.95),
                        recommended_actions=[
                            "Analyze recent campaign changes and their impact" if revenue_change < 0 else "Scale successful recent campaigns",
                            "Review traffic source performance trends",
                            "Check for seasonal factors affecting performance",
                            "Compare with industry trends and competitor activity"
                        ],
                        estimated_impact={
                            "projected_monthly_impact": (recent_avg['revenue'] - previous_avg['revenue']) * 30
                        }
                    )
                    insights.append(insight)
            
            # Conversion rate trend analysis
            if previous_avg['conversion_rate'] > 0:
                cr_change = (recent_avg['conversion_rate'] - previous_avg['conversion_rate']) / previous_avg['conversion_rate']
                
                if abs(cr_change) > 0.10:  # 10% change threshold
                    severity = AlertSeverity.OPPORTUNITY if cr_change > 0 else AlertSeverity.WARNING
                    direction = "improved" if cr_change > 0 else "declined"
                    
                    insight = AIInsight(
                        affiliate_id=affiliate_id,
                        insight_type=InsightType.TREND_ANALYSIS,
                        severity=severity,
                        title=f"Conversion Rate {direction.title()} {abs(cr_change):.1%}",
                        description=f"Your conversion rate has {direction} by {abs(cr_change):.1%}, "
                                  f"from {previous_avg['conversion_rate']:.2%} to {recent_avg['conversion_rate']:.2%}.",
                        supporting_data={
                            "recent_conversion_rate": recent_avg['conversion_rate'],
                            "previous_conversion_rate": previous_avg['conversion_rate'],
                            "change_percentage": cr_change,
                            "recent_clicks": recent_avg['clicks'],
                            "previous_clicks": previous_avg['clicks']
                        },
                        confidence_score=min(abs(cr_change) * 3, 0.95),
                        recommended_actions=[
                            "Investigate recent landing page or checkout changes" if cr_change < 0 else "Document and replicate successful optimization strategies",
                            "Review traffic quality and source mix changes",
                            "Analyze customer journey and user experience data",
                            "Test and optimize key conversion elements"
                        ],
                        estimated_impact={
                            "monthly_conversion_impact": recent_avg['clicks'] * 30 * (recent_avg['conversion_rate'] - previous_avg['conversion_rate'])
                        }
                    )
                    insights.append(insight)
        
        except Exception as e:
            logging.error(f"Error in trend analysis for {affiliate_id}: {e}")
        
        return insights
    
    async def generate_optimization_suggestions(self, affiliate_id: str, data: List[Dict]) -> List[AIInsight]:
        """Generate AI-powered optimization suggestions"""
        
        insights = []
        
        try:
            if not data:
                return insights
            
            # Calculate current performance metrics
            revenues = [d.get('revenue', 0) for d in data]
            conversion_rates = [d.get('conversion_rate', 0) for d in data]
            clicks = [d.get('clicks', 0) for d in data]
            
            avg_cr = sum(conversion_rates) / len(conversion_rates) if conversion_rates else 0
            avg_revenue = sum(revenues) / len(revenues) if revenues else 0
            avg_clicks = sum(clicks) / len(clicks) if clicks else 0
            
            # Calculate AOV
            total_conversions = sum(d.get('conversions', 0) for d in data)
            total_revenue = sum(revenues)
            avg_aov = total_revenue / total_conversions if total_conversions > 0 else 0
            
            # Conversion rate optimization opportunity
            benchmark_cr = self.benchmarks['conversion_rate']
            if avg_cr < benchmark_cr and avg_cr > 0:
                potential_improvement = (benchmark_cr - avg_cr) / avg_cr
                
                insight = AIInsight(
                    affiliate_id=affiliate_id,
                    insight_type=InsightType.OPTIMIZATION_SUGGESTION,
                    severity=AlertSeverity.OPPORTUNITY,
                    title="Conversion Rate Optimization Opportunity",
                    description=f"Your conversion rate ({avg_cr:.2%}) is below industry benchmark "
                              f"({benchmark_cr:.2%}). Optimizing could increase revenue by "
                              f"{potential_improvement:.1%}.",
                    supporting_data={
                        "current_cr": avg_cr,
                        "benchmark_cr": benchmark_cr,
                        "improvement_potential": potential_improvement,
                        "current_avg_revenue": avg_revenue
                    },
                    confidence_score=0.8,
                    recommended_actions=[
                        "A/B test landing page headlines and call-to-action buttons",
                        "Optimize page loading speed (target under 3 seconds)",
                        "Add customer testimonials and trust signals",
                        "Simplify the checkout or signup process",
                        "Test different pricing strategies and offers",
                        "Improve mobile user experience"
                    ],
                    estimated_impact={
                        "monthly_revenue_increase": avg_revenue * 30 * potential_improvement,
                        "monthly_conversion_increase": avg_clicks * 30 * (benchmark_cr - avg_cr)
                    }
                )
                insights.append(insight)
            
            # Traffic quality analysis
            high_traffic_periods = [d for d in data if d.get('clicks', 0) > avg_clicks * 1.5]
            low_conversion_periods = [d for d in high_traffic_periods if d.get('conversion_rate', 0) < avg_cr * 0.6]
            
            if len(low_conversion_periods) > len(data) * 0.2:  # More than 20% of periods
                insight = AIInsight(
                    affiliate_id=affiliate_id,
                    insight_type=InsightType.OPTIMIZATION_SUGGESTION,
                    severity=AlertSeverity.WARNING,
                    title="Traffic Quality Optimization Needed",
                    description=f"Found {len(low_conversion_periods)} high-traffic periods with low conversions "
                              f"({len(low_conversion_periods)/len(data)*100:.1f}% of all periods). "
                              f"This suggests potential traffic quality issues.",
                    supporting_data={
                        "affected_periods": len(low_conversion_periods),
                        "total_periods": len(data),
                        "avg_clicks_in_affected_periods": sum(d.get('clicks', 0) for d in low_conversion_periods) / len(low_conversion_periods) if low_conversion_periods else 0,
                        "avg_cr_in_affected_periods": sum(d.get('conversion_rate', 0) for d in low_conversion_periods) / len(low_conversion_periods) if low_conversion_periods else 0
                    },
                    confidence_score=0.75,
                    recommended_actions=[
                        "Review and audit all traffic sources for quality",
                        "Implement bot detection and filtering",
                        "Analyze user behavior patterns during high-traffic periods",
                        "Consider pausing or optimizing underperforming traffic sources",
                        "Add traffic quality monitoring and alerts",
                        "Review and tighten targeting criteria"
                    ],
                    estimated_impact={
                        "potential_cost_savings": sum(d.get('clicks', 0) for d in low_conversion_periods) * 0.50,  # Assume $0.50 CPC
                        "conversion_improvement_potential": sum(d.get('clicks', 0) for d in low_conversion_periods) * (avg_cr - sum(d.get('conversion_rate', 0) for d in low_conversion_periods) / len(low_conversion_periods) if low_conversion_periods else 0)
                    }
                )
                insights.append(insight)
            
            # AOV optimization
            benchmark_aov = self.benchmarks['avg_order_value']
            if avg_aov > 0 and avg_aov < benchmark_aov:
                aov_improvement = (benchmark_aov - avg_aov) / avg_aov
                
                insight = AIInsight(
                    affiliate_id=affiliate_id,
                    insight_type=InsightType.OPTIMIZATION_SUGGESTION,
                    severity=AlertSeverity.OPPORTUNITY,
                    title="Average Order Value Optimization",
                    description=f"Your average order value (${avg_aov:.2f}) could be increased to the "
                              f"industry benchmark (${benchmark_aov:.2f}) for {aov_improvement:.1%} more revenue per conversion.",
                    supporting_data={
                        "current_aov": avg_aov,
                        "benchmark_aov": benchmark_aov,
                        "improvement_potential": aov_improvement,
                        "total_conversions": total_conversions
                    },
                    confidence_score=0.7,
                    recommended_actions=[
                        "Implement upselling and cross-selling strategies",
                        "Create product bundles and package deals",
                        "Test higher-value product recommendations",
                        "Optimize pricing strategy and discount structure",
                        "Improve product descriptions and value proposition",
                        "Add social proof and scarcity elements"
                    ],
                    estimated_impact={
                        "monthly_revenue_increase": total_conversions * 30 / len(data) * (benchmark_aov - avg_aov) if len(data) > 0 else 0
                    }
                )
                insights.append(insight)
        
        except Exception as e:
            logging.error(f"Error in optimization suggestions for {affiliate_id}: {e}")
        
        return insights
    
    async def generate_predictive_insights(self, affiliate_id: str, data: List[Dict]) -> List[AIInsight]:
        """Generate predictive insights using statistical analysis"""
        
        insights = []
        
        try:
            if len(data) < 14:  # Need at least 2 weeks of data
                return insights
            
            # Simple trend analysis for prediction
            revenues = [d.get('revenue', 0) for d in data]
            
            # Calculate simple moving average trend
            recent_7_days = revenues[-7:] if len(revenues) >= 7 else revenues
            previous_7_days = revenues[-14:-7] if len(revenues) >= 14 else revenues[:-7] if len(revenues) > 7 else []
            
            if not previous_7_days:
                return insights
            
            recent_avg = sum(recent_7_days) / len(recent_7_days)
            previous_avg = sum(previous_7_days) / len(previous_7_days)
            
            # Predict next week based on trend
            if previous_avg > 0:
                trend_rate = (recent_avg - previous_avg) / previous_avg
                predicted_next_week = recent_avg * (1 + trend_rate)
                
                # Only generate insight if significant change predicted
                if abs(trend_rate) > 0.1:  # 10% change threshold
                    severity = AlertSeverity.OPPORTUNITY if trend_rate > 0 else AlertSeverity.WARNING
                    direction = "increase" if trend_rate > 0 else "decrease"
                    
                    insight = AIInsight(
                        affiliate_id=affiliate_id,
                        insight_type=InsightType.PREDICTIVE_FORECAST,
                        severity=severity,
                        title=f"Predicted Revenue {direction.title()} Next Week",
                        description=f"Based on recent trends, revenue is predicted to {direction} by "
                                  f"{abs(trend_rate):.1%} next week. Predicted weekly revenue: "
                                  f"${predicted_next_week * 7:,.2f} vs current ${recent_avg * 7:,.2f}.",
                        supporting_data={
                            "predicted_daily_revenue": predicted_next_week,
                            "current_daily_revenue": recent_avg,
                            "predicted_weekly_revenue": predicted_next_week * 7,
                            "current_weekly_revenue": recent_avg * 7,
                            "trend_rate": trend_rate,
                            "prediction_confidence": min(0.7, abs(trend_rate) * 2)  # Higher confidence for stronger trends
                        },
                        confidence_score=0.6,  # Moderate confidence for simple predictions
                        recommended_actions=[
                            "Prepare marketing budget adjustments for predicted changes" if trend_rate > 0 else "Investigate factors causing predicted decline",
                            "Monitor key performance indicators closely",
                            "Adjust traffic acquisition strategies accordingly",
                            "Review and optimize conversion funnel",
                            "Plan inventory or capacity adjustments if applicable"
                        ],
                        estimated_impact={
                            "predicted_revenue_change": (predicted_next_week - recent_avg) * 7
                        }
                    )
                    insights.append(insight)
        
        except Exception as e:
            logging.error(f"Error in predictive insights for {affiliate_id}: {e}")
        
        return insights
    
    async def get_performance_data(self, affiliate_id: str, hours: int) -> List[Dict]:
        """Get performance data from tracking events and commissions"""
        
        try:
            # Calculate cutoff time - handle both timezone-aware and naive datetimes
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
            cutoff_time_naive = cutoff_time.replace(tzinfo=None)  # Also try without timezone
            
            # Get tracking events - temporarily skip date filtering due to MongoDB query issues
            # TODO: Fix date filtering issue with MongoDB
            tracking_cursor = self.db.advanced_tracking_events.find({
                "affiliate_id": affiliate_id
            }).sort("created_at", 1)
            
            tracking_events = await tracking_cursor.to_list(length=None)
            
            # Get conversion events - temporarily skip date filtering due to MongoDB query issues  
            # TODO: Fix date filtering issue with MongoDB
            conversion_cursor = self.db.advanced_conversion_events.find({
                "affiliate_id": affiliate_id
            }).sort("conversion_timestamp", 1)
            
            conversion_events = await conversion_cursor.to_list(length=None)
            
            # Filter events by date in Python since MongoDB query has issues
            if tracking_events:
                tracking_events = [
                    event for event in tracking_events 
                    if event.get('created_at') and (
                        event.get('created_at') >= cutoff_time_naive or 
                        (hasattr(event.get('created_at'), 'replace') and event.get('created_at').replace(tzinfo=timezone.utc) >= cutoff_time)
                    )
                ]
            
            if conversion_events:
                conversion_events = [
                    event for event in conversion_events 
                    if event.get('conversion_timestamp') and (
                        event.get('conversion_timestamp') >= cutoff_time_naive or 
                        (hasattr(event.get('conversion_timestamp'), 'replace') and event.get('conversion_timestamp').replace(tzinfo=timezone.utc) >= cutoff_time)
                    )
                ]
            
            # Aggregate data by hour or day
            time_buckets = {}
            
            # Process tracking events (clicks)
            for event in tracking_events:
                event_time = event.get('created_at')
                if not event_time:
                    continue
                
                # Round to nearest hour
                bucket_time = event_time.replace(minute=0, second=0, microsecond=0)
                bucket_key = bucket_time.isoformat()
                
                if bucket_key not in time_buckets:
                    time_buckets[bucket_key] = {
                        'date': bucket_time,
                        'clicks': 0,
                        'conversions': 0,
                        'revenue': 0.0
                    }
                
                time_buckets[bucket_key]['clicks'] += 1
            
            # Process conversion events
            for event in conversion_events:
                event_time = event.get('conversion_timestamp')
                if not event_time:
                    continue
                
                # Round to nearest hour
                bucket_time = event_time.replace(minute=0, second=0, microsecond=0)
                bucket_key = bucket_time.isoformat()
                
                if bucket_key not in time_buckets:
                    time_buckets[bucket_key] = {
                        'date': bucket_time,
                        'clicks': 0,
                        'conversions': 0,
                        'revenue': 0.0
                    }
                
                time_buckets[bucket_key]['conversions'] += 1
                time_buckets[bucket_key]['revenue'] += event.get('conversion_value', 0)
            
            # Convert to list and calculate derived metrics
            performance_data = []
            for bucket_data in time_buckets.values():
                clicks = bucket_data['clicks']
                conversions = bucket_data['conversions']
                revenue = bucket_data['revenue']
                
                # Calculate derived metrics
                conversion_rate = conversions / clicks if clicks > 0 else 0
                avg_order_value = revenue / conversions if conversions > 0 else 0
                
                performance_data.append({
                    'date': bucket_data['date'],
                    'clicks': clicks,
                    'conversions': conversions,
                    'revenue': revenue,
                    'conversion_rate': conversion_rate,
                    'avg_order_value': avg_order_value
                })
            
            # Sort by date
            performance_data.sort(key=lambda x: x['date'])
            
            return performance_data
            
        except Exception as e:
            logging.error(f"Error getting performance data for {affiliate_id}: {e}")
            return []

# =============================================================================
# Real-Time Analytics Manager
# =============================================================================

class RealTimeAnalyticsManager:
    """Manages real-time analytics and metric updates"""
    
    def __init__(self):
        # Initialize Redis connection
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/3")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Initialize AI engine
        self.ai_engine = AIAnalyticsEngine()
    
    async def update_real_time_metrics(self, affiliate_id: str, site_id: str, event_type: str, event_data: Dict):
        """Update real-time metrics when events occur"""
        
        try:
            # Get current metrics
            metrics_key = f"rt_metrics:{affiliate_id}:{site_id}"
            current_data = await self.redis_client.get(metrics_key)
            
            if current_data:
                try:
                    metrics_dict = json.loads(current_data)
                    metrics = RealTimeMetrics(**metrics_dict)
                except:
                    metrics = RealTimeMetrics(affiliate_id=affiliate_id, site_id=site_id)
            else:
                metrics = RealTimeMetrics(affiliate_id=affiliate_id, site_id=site_id)
            
            # Update based on event type
            if event_type == "click":
                metrics.clicks_1h += 1
                metrics.clicks_24h += 1
            
            elif event_type == "conversion":
                metrics.conversions_1h += 1
                metrics.conversions_24h += 1
                metrics.revenue_1h += event_data.get("value", 0)
                metrics.revenue_24h += event_data.get("value", 0)
                
                # Recalculate rates
                metrics.conversion_rate_1h = metrics.conversions_1h / max(metrics.clicks_1h, 1)
                metrics.conversion_rate_24h = metrics.conversions_24h / max(metrics.clicks_24h, 1)
                metrics.avg_order_value_24h = metrics.revenue_24h / max(metrics.conversions_24h, 1)
            
            # Update performance score
            metrics.performance_score = await self.calculate_performance_score(metrics)
            
            # Update timestamp
            metrics.timestamp = datetime.now(timezone.utc)
            
            # Store updated metrics
            await self.redis_client.setex(
                metrics_key, 
                86400,  # 24 hour expiry
                metrics.json()
            )
            
            # Trigger real-time insights if significant change
            await self.check_for_real_time_alerts(affiliate_id, site_id, metrics, event_type)
            
        except Exception as e:
            logging.error(f"Error updating real-time metrics: {e}")
    
    async def calculate_performance_score(self, metrics: RealTimeMetrics) -> float:
        """Calculate overall performance score (0-100)"""
        
        try:
            # Base score from conversion rate (0-40 points)
            cr_score = min(metrics.conversion_rate_24h * 1000, 40)  # 4% = 40 points
            
            # Revenue score (0-30 points)  
            revenue_score = min(metrics.revenue_24h / 50, 30)  # $1500/day = 30 points
            
            # Volume score (0-20 points)
            volume_score = min(metrics.clicks_24h / 100, 20)  # 2000 clicks = 20 points
            
            # AOV score (0-10 points)
            aov_score = min(metrics.avg_order_value_24h / 10, 10)  # $100 AOV = 10 points
            
            return cr_score + revenue_score + volume_score + aov_score
        except:
            return 0.0
    
    async def check_for_real_time_alerts(self, affiliate_id: str, site_id: str, metrics: RealTimeMetrics, event_type: str):
        """Check for conditions that should trigger immediate alerts"""
        
        try:
            alerts = []
            
            # Check for conversion rate drop
            if metrics.conversions_1h == 0 and metrics.clicks_1h > 20:
                alerts.append({
                    "type": "conversion_drop",
                    "message": f"No conversions in past hour despite {metrics.clicks_1h} clicks",
                    "severity": AlertSeverity.WARNING
                })
            
            # Check for traffic spike (need historical data to compare)
            if metrics.clicks_1h > 50:  # Simple threshold
                alerts.append({
                    "type": "traffic_spike",
                    "message": f"High traffic detected: {metrics.clicks_1h} clicks in past hour",
                    "severity": AlertSeverity.OPPORTUNITY
                })
            
            # Check for high-value conversion
            if event_type == "conversion" and metrics.avg_order_value_24h > 100:
                alerts.append({
                    "type": "high_value_conversion",
                    "message": f"High-value conversions detected: ${metrics.avg_order_value_24h:.2f} AOV",
                    "severity": AlertSeverity.OPPORTUNITY
                })
            
            # Send alerts
            for alert in alerts:
                await self.send_real_time_alert(affiliate_id, site_id, alert["type"], alert["message"], alert["severity"])
        
        except Exception as e:
            logging.error(f"Error in real-time alert checking: {e}")
    
    async def send_real_time_alert(self, affiliate_id: str, site_id: str, alert_type: str, message: str, severity: AlertSeverity):
        """Send real-time alert to affiliate"""
        
        try:
            alert_data = {
                "affiliate_id": affiliate_id,
                "site_id": site_id,
                "alert_type": alert_type,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Store alert for retrieval
            alert_key = f"rt_alert:{affiliate_id}:{datetime.now(timezone.utc).timestamp()}"
            await self.redis_client.setex(alert_key, 3600, json.dumps(alert_data))  # 1 hour expiry
            
            logging.info(f"Real-time alert sent: {alert_type} for {affiliate_id}")
        
        except Exception as e:
            logging.error(f"Failed to send real-time alert: {e}")

# =============================================================================
# Initialize managers
# =============================================================================

# Global instances
ai_engine = AIAnalyticsEngine()
rt_manager = RealTimeAnalyticsManager()

# =============================================================================
# FastAPI Router
# =============================================================================

router = APIRouter(prefix="/api/v3/analytics", tags=["AI Analytics & Real-Time Reporting"])

@router.post("/insights/{affiliate_id}")
async def get_ai_insights(
    affiliate_id: str,
    site_ids: List[str] = Query(None),
    timeframe_hours: int = Query(24, ge=1, le=168),  # 1 hour to 1 week
    insight_types: List[InsightType] = Query(None)
):
    """Get AI-powered insights for an affiliate"""
    
    try:
        insights = await ai_engine.generate_real_time_insights(affiliate_id, timeframe_hours)
        
        # Filter by site_ids if provided
        if site_ids:
            insights = [i for i in insights if i.site_id in site_ids or i.site_id is None]
        
        # Filter by insight types if provided
        if insight_types:
            insights = [i for i in insights if i.insight_type in insight_types]
        
        return {
            "success": True,
            "affiliate_id": affiliate_id,
            "timeframe_hours": timeframe_hours,
            "insights_count": len(insights),
            "insights": [insight.dict() for insight in insights],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    except Exception as e:
        logging.error(f"Error getting AI insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/real-time/{affiliate_id}")
async def get_real_time_metrics(
    affiliate_id: str,
    site_id: Optional[str] = Query(None)
):
    """Get real-time metrics for an affiliate"""
    
    try:
        if site_id:
            # Get metrics for specific site
            metrics_key = f"rt_metrics:{affiliate_id}:{site_id}"
            data = await rt_manager.redis_client.get(metrics_key)
            
            if data:
                metrics_dict = json.loads(data)
                return {"success": True, "metrics": metrics_dict}
            else:
                return {"success": True, "metrics": None, "message": "No real-time data available"}
        
        else:
            # Get metrics for all sites
            pattern = f"rt_metrics:{affiliate_id}:*"
            keys = await rt_manager.redis_client.keys(pattern)
            
            all_metrics = {}
            for key in keys:
                try:
                    site_id = key.split(":")[-1]
                    data = await rt_manager.redis_client.get(key)
                    if data:
                        all_metrics[site_id] = json.loads(data)
                except:
                    continue
            
            return {"success": True, "metrics": all_metrics}
    
    except Exception as e:
        logging.error(f"Error getting real-time metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/event")
async def track_analytics_event(
    affiliate_id: str,
    site_id: str,
    event_type: str,
    event_data: Dict[str, Any] = {}
):
    """Track analytics event for real-time processing"""
    
    try:
        await rt_manager.update_real_time_metrics(affiliate_id, site_id, event_type, event_data)
        
        return {
            "success": True,
            "message": f"Event {event_type} tracked for {affiliate_id}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    except Exception as e:
        logging.error(f"Error tracking analytics event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predictions/{affiliate_id}")
async def get_performance_predictions(
    affiliate_id: str,
    site_id: Optional[str] = Query(None),
    forecast_days: int = Query(7, ge=1, le=30)
):
    """Get AI-powered performance predictions"""
    
    try:
        # Get historical data
        historical_data = await ai_engine.get_performance_data(affiliate_id, hours=24*30)  # 30 days
        
        if len(historical_data) < 7:
            return {
                "success": False,
                "error": "Insufficient historical data for predictions",
                "minimum_days_required": 7,
                "current_data_points": len(historical_data)
            }
        
        # Simple trend-based predictions
        revenues = [d['revenue'] for d in historical_data]
        clicks = [d['clicks'] for d in historical_data]
        conversions = [d['conversions'] for d in historical_data]
        
        # Calculate recent trends
        recent_period = revenues[-7:] if len(revenues) >= 7 else revenues
        recent_avg_revenue = sum(recent_period) / len(recent_period)
        recent_avg_clicks = sum(clicks[-7:] if len(clicks) >= 7 else clicks) / len(clicks[-7:] if len(clicks) >= 7 else clicks)
        recent_avg_conversions = sum(conversions[-7:] if len(conversions) >= 7 else conversions) / len(conversions[-7:] if len(conversions) >= 7 else conversions)
        
        # Generate predictions
        predictions = []
        for i in range(forecast_days):
            prediction_date = datetime.now(timezone.utc) + timedelta(days=i+1)
            
            # Simple trend projection (could be enhanced with ML models)
            predicted_revenue = recent_avg_revenue * (1 + 0.01 * i)  # 1% daily growth assumption
            predicted_clicks = recent_avg_clicks * (1 + 0.005 * i)  # 0.5% daily growth
            predicted_conversions = recent_avg_conversions * (1 + 0.01 * i)
            
            prediction = PerformancePrediction(
                affiliate_id=affiliate_id,
                site_id=site_id,
                forecast_date=prediction_date,
                forecast_period_days=1,
                predicted_clicks=max(0, predicted_clicks),
                predicted_conversions=max(0, predicted_conversions),
                predicted_revenue=max(0, predicted_revenue),
                predicted_commissions=max(0, predicted_revenue * 0.1),  # Assume 10% commission
                clicks_confidence_interval=(max(0, predicted_clicks * 0.8), predicted_clicks * 1.2),
                revenue_confidence_interval=(max(0, predicted_revenue * 0.8), predicted_revenue * 1.2),
                model_accuracy=0.7,  # Conservative accuracy estimate
                model_version="v1.0_simple_trend",
                features_used=["historical_revenue", "historical_clicks", "time_trend"]
            )
            predictions.append(prediction)
        
        return {
            "success": True,
            "affiliate_id": affiliate_id,
            "forecast_period_days": forecast_days,
            "predictions": [p.dict() for p in predictions],
            "summary": {
                "total_predicted_revenue": sum(p.predicted_revenue for p in predictions),
                "total_predicted_conversions": sum(p.predicted_conversions for p in predictions),
                "average_daily_revenue": sum(p.predicted_revenue for p in predictions) / forecast_days,
                "model_confidence": "moderate",
                "based_on_days": len(historical_data)
            }
        }
    
    except Exception as e:
        logging.error(f"Error getting performance predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts/{affiliate_id}")
async def get_recent_alerts(
    affiliate_id: str,
    hours_back: int = Query(24, ge=1, le=168)
):
    """Get recent real-time alerts for an affiliate"""
    
    try:
        # Get alerts from Redis
        pattern = f"rt_alert:{affiliate_id}:*"
        keys = await rt_manager.redis_client.keys(pattern)
        
        alerts = []
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        
        for key in keys:
            try:
                # Extract timestamp from key
                timestamp_str = key.split(":")[-1]
                alert_time = datetime.fromtimestamp(float(timestamp_str))
                
                if alert_time > cutoff_time:
                    data = await rt_manager.redis_client.get(key)
                    if data:
                        alerts.append(json.loads(data))
            except:
                continue  # Skip invalid keys
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return {
            "success": True,
            "affiliate_id": affiliate_id,
            "alerts_count": len(alerts),
            "alerts": alerts,
            "timeframe_hours": hours_back
        }
    
    except Exception as e:
        logging.error(f"Error getting recent alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/{affiliate_id}")
async def get_analytics_dashboard(
    affiliate_id: str,
    site_ids: List[str] = Query(None),
    timeframe: AnalyticsTimeframe = Query(AnalyticsTimeframe.DAY)
):
    """Get comprehensive analytics dashboard data"""
    
    try:
        # Get real-time metrics
        rt_metrics_response = await get_real_time_metrics(affiliate_id)
        rt_metrics = rt_metrics_response.get("metrics", {})
        
        # Get AI insights
        insights_response = await get_ai_insights(affiliate_id, site_ids)
        insights = insights_response.get("insights", [])
        
        # Get recent alerts
        alerts_response = await get_recent_alerts(affiliate_id, 24)
        alerts = alerts_response.get("alerts", [])
        
        # Calculate summary metrics
        if isinstance(rt_metrics, dict) and rt_metrics:
            if len(rt_metrics) == 1 and 'clicks_24h' in list(rt_metrics.values())[0]:
                # Single site metrics
                single_metrics = list(rt_metrics.values())[0]
                total_clicks_24h = single_metrics.get("clicks_24h", 0)
                total_conversions_24h = single_metrics.get("conversions_24h", 0) 
                total_revenue_24h = single_metrics.get("revenue_24h", 0)
                avg_performance_score = single_metrics.get("performance_score", 0)
                total_sites = 1
            else:
                # Multiple sites
                total_clicks_24h = sum(m.get("clicks_24h", 0) for m in rt_metrics.values() if isinstance(m, dict))
                total_conversions_24h = sum(m.get("conversions_24h", 0) for m in rt_metrics.values() if isinstance(m, dict))
                total_revenue_24h = sum(m.get("revenue_24h", 0) for m in rt_metrics.values() if isinstance(m, dict))
                valid_scores = [m.get("performance_score", 0) for m in rt_metrics.values() if isinstance(m, dict) and m.get("performance_score", 0) > 0]
                avg_performance_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
                total_sites = len(rt_metrics)
        else:
            total_clicks_24h = 0
            total_conversions_24h = 0
            total_revenue_24h = 0
            avg_performance_score = 0
            total_sites = 0
        
        # Generate dashboard summary
        dashboard_data = {
            "affiliate_id": affiliate_id,
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "timeframe": timeframe,
            
            # Real-time metrics summary
            "real_time_summary": {
                "total_sites": total_sites,
                "total_clicks_24h": total_clicks_24h,
                "total_conversions_24h": total_conversions_24h,
                "total_revenue_24h": total_revenue_24h,
                "overall_conversion_rate_24h": (total_conversions_24h / total_clicks_24h) if total_clicks_24h > 0 else 0,
                "avg_performance_score": avg_performance_score
            },
            
            # Insights summary
            "insights_summary": {
                "total_insights": len(insights),
                "critical_insights": len([i for i in insights if i.get("severity") == "critical"]),
                "opportunities": len([i for i in insights if i.get("severity") == "opportunity"]),
                "warnings": len([i for i in insights if i.get("severity") == "warning"]),
                "info_insights": len([i for i in insights if i.get("severity") == "info"]),
                "top_insights": insights[:5]  # Top 5 insights
            },
            
            # Alerts summary
            "alerts_summary": {
                "total_alerts_24h": len(alerts),
                "recent_alerts": alerts[:5]  # Most recent 5 alerts
            },
            
            # Performance indicators
            "performance_indicators": {
                "overall_health": (
                    "excellent" if avg_performance_score > 80 else
                    "good" if avg_performance_score > 60 else
                    "fair" if avg_performance_score > 40 else
                    "needs_attention"
                ),
                "data_available": total_sites > 0,
                "has_recent_activity": total_clicks_24h > 0 or total_conversions_24h > 0
            }
        }
        
        return {
            "success": True,
            "dashboard": dashboard_data
        }
    
    except Exception as e:
        logging.error(f"Error getting analytics dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def analytics_health_check():
    """Health check for analytics system"""
    
    try:
        # Check Redis connection
        await rt_manager.redis_client.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"
    
    # Check MongoDB connection
    try:
        await ai_engine.db.command("ping")
        mongodb_status = "healthy"
    except:
        mongodb_status = "unhealthy"
    
    return {
        "status": "healthy" if redis_status == "healthy" and mongodb_status == "healthy" else "degraded",
        "components": {
            "redis": redis_status,
            "mongodb": mongodb_status,
            "ai_engine": "healthy",
            "real_time_analytics": "healthy"
        },
        "features": [
            "ai_powered_insights",
            "real_time_metrics", 
            "performance_predictions",
            "anomaly_detection",
            "trend_analysis",
            "optimization_suggestions",
            "real_time_alerts"
        ]
    }