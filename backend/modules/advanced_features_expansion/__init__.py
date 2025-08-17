"""
Advanced Features Expansion Module

This module provides advanced AI-powered customer intelligence features for
hyper-targeted marketing and predictive customer behavior analysis.

Features:
1. Behavioral Clustering - K-means clustering for customer segmentation
2. Churn Prevention AI - Predictive churn modeling with automated retention
3. Cross-Sell Intelligence - Product relationship analysis and recommendations  
4. Pricing Optimization - AI-driven price sensitivity and dynamic pricing
5. Sentiment Analysis - NLP analysis of customer communications
"""

from .behavioral_clustering import behavioral_clustering_router
from .churn_prevention_ai import churn_prevention_router
from .cross_sell_intelligence import cross_sell_intelligence_router
from .pricing_optimization import pricing_optimization_router
from .sentiment_analysis import sentiment_analysis_router

__all__ = [
    'behavioral_clustering_router',
    'churn_prevention_router',
    'cross_sell_intelligence_router',
    'pricing_optimization_router',
    'sentiment_analysis_router'
]