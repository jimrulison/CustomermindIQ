import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { 
  TrendingUp, 
  DollarSign,
  Users,
  Target,
  AlertTriangle,
  CheckCircle,
  Brain,
  BarChart3,
  Activity,
  Zap,
  Eye,
  ArrowUp,
  ArrowDown,
  Calendar,
  Star
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const ExecutiveIntelligenceDashboard = () => {
  const [executiveData, setExecutiveData] = useState(null);
  const [kpiData, setKpiData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState('overview');

  useEffect(() => {
    loadExecutiveData();
  }, []);

  const loadExecutiveData = async () => {
    try {
      setLoading(true);
      
      const [dashboardRes, kpiRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/executive/dashboard`).catch(err => {
          console.error('Executive dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/executive/kpi-summary`).catch(err => {
          console.error('Executive KPI error:', err);
          return { data: {} };
        })
      ]);

      setExecutiveData(dashboardRes.data);
      setKpiData(kpiRes.data);
      
      console.log('Executive Intelligence data loaded successfully');
    } catch (error) {
      console.error('Error loading executive data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}K`;
    }
    return `$${value?.toLocaleString()}`;
  };

  const getAlertColor = (severity) => {
    const colors = {
      'high': 'bg-red-500/20 text-red-400 border-red-500/30',
      'medium': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      'low': 'bg-green-500/20 text-green-400 border-green-500/30'
    };
    return colors[severity] || 'bg-slate-500/20 text-slate-400 border-slate-500/30';
  };

  const getTrendIcon = (trend) => {
    if (trend === 'improving' || trend === 'strong_growth') {
      return <ArrowUp className="w-4 h-4 text-green-400" />;
    } else if (trend === 'declining') {
      return <ArrowDown className="w-4 h-4 text-red-400" />;
    }
    return <Activity className="w-4 h-4 text-blue-400" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading Executive Intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Executive Intelligence Dashboard</h1>
          <p className="text-slate-400 mt-2">Strategic insights and C-level analytics across all modules</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className="bg-gold-500/20 text-gold-400">C-Level Analytics</Badge>
          <Badge className="bg-purple-500/20 text-purple-400">Cross-Module Intelligence</Badge>
          <Badge className="bg-blue-500/20 text-blue-400">Board Ready</Badge>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
        {[
          { id: 'overview', label: 'Executive Overview', icon: BarChart3 },
          { id: 'kpis', label: 'Key Metrics', icon: Target },
          { id: 'modules', label: 'Module Performance', icon: Activity },
          { id: 'insights', label: 'AI Strategic Insights', icon: Brain }
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveView(tab.id)}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeView === tab.id
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Icon className="w-4 h-4 mr-2" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Executive Overview Tab */}
      {activeView === 'overview' && (
        <div className="space-y-6">
          {/* Executive KPI Summary */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <DollarSign className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {formatCurrency(executiveData?.dashboard?.executive_kpis?.revenue_metrics?.total_arr)}
                  </div>
                  <div className="text-xs text-green-200">Total ARR</div>
                  <div className="text-xs text-green-400 mt-1">
                    +{executiveData?.dashboard?.executive_kpis?.revenue_metrics?.arr_growth_rate}% YoY
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Users className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {executiveData?.dashboard?.executive_kpis?.customer_metrics?.total_customers?.toLocaleString()}
                  </div>
                  <div className="text-xs text-blue-200">Total Customers</div>
                  <div className="text-xs text-blue-400 mt-1">
                    +{executiveData?.dashboard?.executive_kpis?.customer_metrics?.customer_growth_rate}% Growth
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {executiveData?.dashboard?.executive_kpis?.revenue_metrics?.net_revenue_retention}%
                  </div>
                  <div className="text-xs text-purple-200">Net Revenue Retention</div>
                  <div className="text-xs text-purple-400 mt-1">Top 10% Industry</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Activity className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {executiveData?.dashboard?.platform_health?.overall_score}
                  </div>
                  <div className="text-xs text-orange-200">Platform Health</div>
                  <div className="text-xs text-orange-400 mt-1">Excellent Status</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Critical Alerts */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2 text-orange-400" />
                Critical Business Alerts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {executiveData?.dashboard?.critical_alerts?.map((alert, index) => (
                  <div key={index} className={`p-4 rounded-lg border ${getAlertColor(alert.severity)}`}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <h4 className="font-semibold">{alert.title}</h4>
                          <Badge className={`text-xs ${getAlertColor(alert.severity)}`}>
                            {alert.severity.toUpperCase()}
                          </Badge>
                        </div>
                        <p className="text-sm mb-2">{alert.description}</p>
                        <p className="text-xs opacity-75">
                          <strong>Impact:</strong> {alert.impact}
                        </p>
                        <p className="text-xs opacity-75">
                          <strong>Action Required:</strong> {alert.action_required}
                        </p>
                      </div>
                      <Button size="sm" className="bg-blue-600 hover:bg-blue-700 ml-4">
                        Address
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Board Summary */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Star className="w-5 h-5 mr-2 text-gold-400" />
                Board-Ready Summary
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-2">
                <div>
                  <h4 className="text-white font-semibold mb-3">Key Achievements</h4>
                  <ul className="space-y-2">
                    {executiveData?.dashboard?.board_summary?.key_achievements?.map((achievement, index) => (
                      <li key={index} className="flex items-center text-sm text-slate-300">
                        <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                        {achievement}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-3">Strategic Priorities</h4>
                  <ul className="space-y-2">
                    {executiveData?.dashboard?.board_summary?.strategic_priorities?.map((priority, index) => (
                      <li key={index} className="flex items-center text-sm text-slate-300">
                        <Target className="w-4 h-4 text-blue-400 mr-2" />
                        {priority}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Key Metrics Tab */}
      {activeView === 'kpis' && (
        <div className="space-y-6">
          {/* Headline KPIs */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {kpiData?.headline_kpis && Object.entries(kpiData.headline_kpis).map(([key, kpi]) => (
              <Card key={key} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader className="pb-3">
                  <CardTitle className="text-white text-sm capitalize">{key.replace('_', ' ')}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-white mb-1">
                      {key === 'arr' ? formatCurrency(kpi.value) : 
                       typeof kpi.value === 'number' ? kpi.value.toLocaleString() : kpi.value}
                    </div>
                    <div className="flex items-center justify-center space-x-1 text-xs">
                      {getTrendIcon(kpi.trend)}
                      <span className={`${
                        kpi.trend === 'improving' || kpi.trend === 'strong_growth' ? 'text-green-400' :
                        kpi.trend === 'declining' ? 'text-red-400' : 'text-blue-400'
                      }`}>
                        {kpi.vs_plan}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Quick Insights & Action Items */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Eye className="w-5 h-5 mr-2 text-blue-400" />
                  Quick Insights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {kpiData?.quick_insights?.map((insight, index) => (
                    <Alert key={index} className="bg-blue-500/10 border-blue-500/20">
                      <Brain className="h-4 w-4 text-blue-400" />
                      <AlertDescription className="text-blue-300 text-sm">
                        {insight}
                      </AlertDescription>
                    </Alert>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Calendar className="w-5 h-5 mr-2 text-orange-400" />
                  Executive Action Items
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {kpiData?.action_items?.map((action, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                      <span className="text-slate-300 text-sm">{action}</span>
                      <Badge className="bg-orange-500/20 text-orange-400">Priority</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Module Performance Tab */}
      {activeView === 'modules' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {executiveData?.dashboard?.module_performance?.map((module, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg">{module.module}</CardTitle>
                  <CardDescription>
                    <Badge className={`${
                      module.health_status === 'Excellent' ? 'bg-green-500/20 text-green-400' :
                      module.health_status === 'Good' ? 'bg-blue-500/20 text-blue-400' :
                      'bg-orange-500/20 text-orange-400'
                    }`}>
                      {module.health_status}
                    </Badge>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300 text-sm">{module.key_metric}</span>
                      <div className="flex items-center space-x-1">
                        <span className="text-white font-semibold">{module.metric_value}</span>
                        {getTrendIcon(module.trend)}
                      </div>
                    </div>
                    <p className="text-xs text-slate-400">{module.impact}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* AI Strategic Insights Tab */}
      {activeView === 'insights' && (
        <div className="space-y-6">
          {executiveData?.dashboard?.ai_strategic_insights?.map((insight, index) => (
            <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center justify-between">
                  <div className="flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-cyan-400" />
                    {insight.insight_category}
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge className={`${
                      insight.impact === 'Critical' ? 'bg-red-500/20 text-red-400' :
                      insight.impact === 'High' ? 'bg-orange-500/20 text-orange-400' :
                      'bg-blue-500/20 text-blue-400'
                    }`}>
                      {insight.impact} Impact
                    </Badge>
                    <Badge className="bg-green-500/20 text-green-400">
                      {insight.confidence}% Confidence
                    </Badge>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Alert className="bg-cyan-500/10 border-cyan-500/20">
                    <AlertDescription className="text-cyan-300">
                      <strong>Insight:</strong> {insight.insight}
                    </AlertDescription>
                  </Alert>
                  
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <h4 className="text-white font-semibold text-sm">Recommendation</h4>
                      <p className="text-slate-300 text-sm">{insight.recommendation}</p>
                    </div>
                    <div className="space-y-2">
                      <h4 className="text-white font-semibold text-sm">Expected Impact</h4>
                      <p className="text-green-400 text-sm font-medium">{insight.potential_impact}</p>
                      <p className="text-slate-400 text-xs">
                        Complexity: {insight.implementation_complexity} | 
                        Resources: {insight.required_resources}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex justify-end">
                    <Button className="bg-cyan-600 hover:bg-cyan-700">
                      Implement Strategy
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default ExecutiveIntelligenceDashboard;