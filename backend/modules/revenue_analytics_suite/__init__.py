"""
Revenue Analytics Suite Module

This module provides comprehensive revenue intelligence and financial analytics
for the Customer Mind IQ Universal Intelligence Platform.

Microservices:
1. Revenue Forecasting - Predictive revenue analysis with AI-powered trends
2. Price Optimization - Dynamic pricing recommendations using market intelligence
3. Profit Margin Analysis - Cost analysis and margin optimization strategies
4. Subscription Analytics - Recurring revenue insights and churn impact analysis
5. Financial Reporting - Comprehensive financial dashboards and KPI tracking
"""

from .revenue_forecasting import revenue_forecasting_router
from .price_optimization import price_optimization_router
from .profit_margin_analysis import profit_margin_analysis_router
from .subscription_analytics import subscription_analytics_router
from .financial_reporting import financial_reporting_router

__all__ = [
    'revenue_forecasting_router',
    'price_optimization_router', 
    'profit_margin_analysis_router',
    'subscription_analytics_router',
    'financial_reporting_router'
]