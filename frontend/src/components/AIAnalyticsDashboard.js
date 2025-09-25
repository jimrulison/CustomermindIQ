import React, { useState, useEffect, useMemo } from 'react';
import { useAdvancedTracking } from './AdvancedTrackingIntegration';

/**
 * AI-Powered Analytics Dashboard Component
 * Displays real-time insights, predictions, and performance metrics
 */
const AIAnalyticsDashboard = ({ 
    affiliateId = null, 
    siteIds = null, 
    showRealTimeMetrics = true,
    showInsights = true,
    showPredictions = true,
    showAlerts = true,
    refreshInterval = 30000 // 30 seconds
}) => {
    const [dashboardData, setDashboardData] = useState(null);
    const [insights, setInsights] = useState([]);
    const [predictions, setPredictions] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [realTimeMetrics, setRealTimeMetrics] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedTimeframe, setSelectedTimeframe] = useState('24h');
    const [lastUpdated, setLastUpdated] = useState(null);
    const { isReady, trackingData } = useAdvancedTracking();

    // Use affiliate ID from tracking data if not provided
    const effectiveAffiliateId = affiliateId || trackingData?.affiliateId;

    // Fetch dashboard data
    const fetchDashboardData = async () => {
        if (!effectiveAffiliateId) return;

        try {
            setError(null);
            
            const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
            
            // Fetch main dashboard data
            const dashboardResponse = await fetch(
                `${backendUrl}/api/v3/analytics/dashboard/${effectiveAffiliateId}?timeframe=${selectedTimeframe}`,
                { method: 'GET', headers: { 'Content-Type': 'application/json' } }
            );
            
            if (dashboardResponse.ok) {
                const dashboardResult = await dashboardResponse.json();
                setDashboardData(dashboardResult.dashboard);
            }

            // Fetch detailed insights if enabled
            if (showInsights) {
                const insightsResponse = await fetch(
                    `${backendUrl}/api/v3/analytics/insights/${effectiveAffiliateId}?timeframe_hours=24`,
                    { method: 'POST', headers: { 'Content-Type': 'application/json' } }
                );
                
                if (insightsResponse.ok) {
                    const insightsResult = await insightsResponse.json();
                    setInsights(insightsResult.insights || []);
                }
            }

            // Fetch predictions if enabled
            if (showPredictions) {
                const predictionsResponse = await fetch(
                    `${backendUrl}/api/v3/analytics/predictions/${effectiveAffiliateId}?forecast_days=7`,
                    { method: 'GET', headers: { 'Content-Type': 'application/json' } }
                );
                
                if (predictionsResponse.ok) {
                    const predictionsResult = await predictionsResponse.json();
                    setPredictions(predictionsResult.predictions || []);
                }
            }

            // Fetch real-time metrics if enabled
            if (showRealTimeMetrics) {
                const metricsResponse = await fetch(
                    `${backendUrl}/api/v3/analytics/real-time/${effectiveAffiliateId}`,
                    { method: 'GET', headers: { 'Content-Type': 'application/json' } }
                );
                
                if (metricsResponse.ok) {
                    const metricsResult = await metricsResponse.json();
                    setRealTimeMetrics(metricsResult.metrics || {});
                }
            }

            // Fetch alerts if enabled
            if (showAlerts) {
                const alertsResponse = await fetch(
                    `${backendUrl}/api/v3/analytics/alerts/${effectiveAffiliateId}?hours_back=24`,
                    { method: 'GET', headers: { 'Content-Type': 'application/json' } }
                );
                
                if (alertsResponse.ok) {
                    const alertsResult = await alertsResponse.json();
                    setAlerts(alertsResult.alerts || []);
                }
            }

            setLastUpdated(new Date());
        } catch (err) {
            console.error('Failed to fetch analytics data:', err);
            setError('Failed to load analytics data');
        } finally {
            setLoading(false);
        }
    };

    // Initial data fetch and periodic refresh
    useEffect(() => {
        if (effectiveAffiliateId && isReady) {
            fetchDashboardData();

            const interval = setInterval(fetchDashboardData, refreshInterval);
            return () => clearInterval(interval);
        }
    }, [effectiveAffiliateId, isReady, selectedTimeframe, refreshInterval]);

    // Severity color mapping
    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'critical': return '#ef4444';
            case 'warning': return '#f97316';
            case 'opportunity': return '#10b981';
            case 'info': return '#3b82f6';
            default: return '#6b7280';
        }
    };

    // Insight icon mapping
    const getInsightIcon = (type) => {
        switch (type) {
            case 'anomaly_detection': return '🔍';
            case 'trend_analysis': return '📈';
            case 'optimization_suggestion': return '💡';
            case 'predictive_forecast': return '🔮';
            case 'performance_alert': return '⚠️';
            default: return '📊';
        }
    };

    // Performance health indicator
    const getHealthColor = (health) => {
        switch (health) {
            case 'excellent': return '#10b981';
            case 'good': return '#84cc16';
            case 'fair': return '#f97316';
            case 'needs_attention': return '#ef4444';
            default: return '#6b7280';
        }
    };

    // Memoized calculations
    const summaryMetrics = useMemo(() => {
        if (!dashboardData) return null;
        
        const summary = dashboardData.real_time_summary || {};
        return {
            totalRevenue: summary.total_revenue_24h || 0,
            totalClicks: summary.total_clicks_24h || 0,
            totalConversions: summary.total_conversions_24h || 0,
            conversionRate: summary.overall_conversion_rate_24h || 0,
            performanceScore: summary.avg_performance_score || 0,
            totalSites: summary.total_sites || 0
        };
    }, [dashboardData]);

    const topInsights = useMemo(() => {
        return insights
            .sort((a, b) => {
                // Sort by severity (critical > warning > opportunity > info)
                const severityOrder = { critical: 4, warning: 3, opportunity: 2, info: 1 };
                return (severityOrder[b.severity] || 0) - (severityOrder[a.severity] || 0);
            })
            .slice(0, 5);
    }, [insights]);

    if (!effectiveAffiliateId) {
        return (
            <div className="bg-white rounded-lg shadow p-6">
                <div className="text-center">
                    <div className="text-gray-400 mb-2">📊</div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Analytics Dashboard</h3>
                    <p className="text-gray-600">
                        No affiliate ID available. Make sure you have active tracking or provide an affiliate ID.
                    </p>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="bg-white rounded-lg shadow p-6">
                <div className="animate-pulse">
                    <div className="flex items-center justify-between mb-6">
                        <div className="h-6 bg-gray-200 rounded w-1/3"></div>
                        <div className="h-6 bg-gray-200 rounded w-1/4"></div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                        {[1,2,3,4].map(i => (
                            <div key={i} className="border rounded-lg p-4">
                                <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                                <div className="h-8 bg-gray-200 rounded w-3/4"></div>
                            </div>
                        ))}
                    </div>
                    <div className="space-y-4">
                        {[1,2,3].map(i => (
                            <div key={i} className="h-16 bg-gray-200 rounded"></div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-white rounded-lg shadow p-6">
                <div className="text-center">
                    <div className="text-red-400 mb-2">❌</div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Analytics</h3>
                    <p className="text-gray-600 mb-4">{error}</p>
                    <button
                        onClick={fetchDashboardData}
                        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                            🤖 AI Analytics Dashboard
                        </h2>
                        <p className="text-gray-600 mt-1">
                            Real-time insights and performance analytics for affiliate {effectiveAffiliateId}
                        </p>
                    </div>
                    <div className="flex items-center space-x-3">
                        <select
                            value={selectedTimeframe}
                            onChange={(e) => setSelectedTimeframe(e.target.value)}
                            className="border border-gray-300 rounded-md px-3 py-1 text-sm"
                        >
                            <option value="1h">Last Hour</option>
                            <option value="24h">Last 24 Hours</option>
                            <option value="7d">Last 7 Days</option>
                            <option value="30d">Last 30 Days</option>
                        </select>
                        {lastUpdated && (
                            <span className="text-xs text-gray-500">
                                Updated: {lastUpdated.toLocaleTimeString()}
                            </span>
                        )}
                    </div>
                </div>
            </div>

            {/* Summary Metrics */}
            {summaryMetrics && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-blue-100 rounded-lg">💰</div>
                            <div className="ml-4">
                                <p className="text-sm text-gray-600">Revenue (24h)</p>
                                <p className="text-2xl font-semibold text-gray-900">
                                    ${summaryMetrics.totalRevenue.toFixed(2)}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-green-100 rounded-lg">👆</div>
                            <div className="ml-4">
                                <p className="text-sm text-gray-600">Clicks (24h)</p>
                                <p className="text-2xl font-semibold text-gray-900">
                                    {summaryMetrics.totalClicks.toLocaleString()}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-purple-100 rounded-lg">🎯</div>
                            <div className="ml-4">
                                <p className="text-sm text-gray-600">Conversions (24h)</p>
                                <p className="text-2xl font-semibold text-gray-900">
                                    {summaryMetrics.totalConversions}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div 
                                className="p-2 rounded-lg"
                                style={{ backgroundColor: `${getHealthColor(dashboardData?.performance_indicators?.overall_health)}20` }}
                            >
                                📊
                            </div>
                            <div className="ml-4">
                                <p className="text-sm text-gray-600">Performance Score</p>
                                <p className="text-2xl font-semibold text-gray-900">
                                    {summaryMetrics.performanceScore.toFixed(1)}/100
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* AI Insights Section */}
            {showInsights && topInsights.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-900">🧠 AI-Powered Insights</h3>
                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                            {insights.length} total insights
                        </span>
                    </div>
                    <div className="space-y-4">
                        {topInsights.map((insight, index) => (
                            <div key={insight.insight_id || index} className="border-l-4 p-4 rounded-r-lg bg-gray-50"
                                 style={{ borderLeftColor: getSeverityColor(insight.severity) }}>
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center mb-2">
                                            <span className="mr-2">{getInsightIcon(insight.insight_type)}</span>
                                            <h4 className="font-medium text-gray-900">{insight.title}</h4>
                                            <span 
                                                className="ml-2 px-2 py-1 text-xs rounded-full"
                                                style={{ 
                                                    backgroundColor: `${getSeverityColor(insight.severity)}20`,
                                                    color: getSeverityColor(insight.severity)
                                                }}
                                            >
                                                {insight.severity}
                                            </span>
                                        </div>
                                        <p className="text-gray-700 text-sm mb-3">{insight.description}</p>
                                        
                                        {insight.recommended_actions && insight.recommended_actions.length > 0 && (
                                            <div>
                                                <p className="text-xs font-medium text-gray-600 mb-1">Recommended Actions:</p>
                                                <ul className="text-xs text-gray-600 space-y-1">
                                                    {insight.recommended_actions.slice(0, 3).map((action, actionIndex) => (
                                                        <li key={actionIndex} className="flex items-start">
                                                            <span className="mr-1">•</span>
                                                            {action}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                    <div className="ml-4 text-right">
                                        <div className="text-xs text-gray-500">
                                            Confidence: {(insight.confidence_score * 100).toFixed(0)}%
                                        </div>
                                        {insight.estimated_impact?.monthly_revenue_increase && (
                                            <div className="text-xs text-green-600 mt-1">
                                                +${insight.estimated_impact.monthly_revenue_increase.toFixed(0)}/mo
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Performance Predictions */}
            {showPredictions && predictions.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">🔮 7-Day Performance Forecast</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {predictions.slice(0, 7).map((prediction, index) => (
                            <div key={prediction.prediction_id || index} className="border rounded-lg p-4">
                                <div className="text-sm text-gray-600 mb-1">
                                    {new Date(prediction.forecast_date).toLocaleDateString()}
                                </div>
                                <div className="space-y-2">
                                    <div className="flex justify-between">
                                        <span className="text-sm">Revenue:</span>
                                        <span className="font-medium">${prediction.predicted_revenue.toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-sm">Conversions:</span>
                                        <span className="font-medium">{prediction.predicted_conversions.toFixed(0)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-sm">Clicks:</span>
                                        <span className="font-medium">{prediction.predicted_clicks.toFixed(0)}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Recent Alerts */}
            {showAlerts && alerts.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-900">🚨 Recent Alerts</h3>
                        <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full">
                            {alerts.length} alerts
                        </span>
                    </div>
                    <div className="space-y-3">
                        {alerts.slice(0, 5).map((alert, index) => (
                            <div key={index} className="flex items-start p-3 bg-gray-50 rounded-lg">
                                <div 
                                    className="w-2 h-2 rounded-full mt-2 mr-3"
                                    style={{ backgroundColor: getSeverityColor(alert.severity) }}
                                ></div>
                                <div className="flex-1">
                                    <div className="flex items-center justify-between">
                                        <span className="font-medium text-gray-900 capitalize">
                                            {alert.alert_type?.replace('_', ' ')}
                                        </span>
                                        <span className="text-xs text-gray-500">
                                            {new Date(alert.timestamp).toLocaleTimeString()}
                                        </span>
                                    </div>
                                    <p className="text-sm text-gray-700 mt-1">{alert.message}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">⚡ Quick Actions</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <button 
                        onClick={fetchDashboardData}
                        className="flex items-center justify-center p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                        <span className="mr-2">🔄</span>
                        <span className="text-sm">Refresh Data</span>
                    </button>
                    <button className="flex items-center justify-center p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                        <span className="mr-2">📊</span>
                        <span className="text-sm">Full Report</span>
                    </button>
                    <button className="flex items-center justify-center p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                        <span className="mr-2">⚙️</span>
                        <span className="text-sm">Settings</span>
                    </button>
                    <button className="flex items-center justify-center p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                        <span className="mr-2">📈</span>
                        <span className="text-sm">Export Data</span>
                    </button>
                </div>
            </div>

            {/* System Status */}
            <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between text-sm text-gray-600">
                    <div className="flex items-center space-x-4">
                        <span className="flex items-center">
                            <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                            Analytics Engine: Active
                        </span>
                        <span className="flex items-center">
                            <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                            Real-time Tracking: {isReady ? 'Connected' : 'Disconnected'}
                        </span>
                    </div>
                    <div>
                        Last updated: {lastUpdated ? lastUpdated.toLocaleString() : 'Never'}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AIAnalyticsDashboard;