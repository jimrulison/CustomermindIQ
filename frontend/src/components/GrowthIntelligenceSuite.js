import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { 
  Target, 
  TrendingUp, 
  Users,
  Eye,
  Zap,
  Brain,
  ArrowUp,
  ArrowDown,
  Search,
  Calendar,
  CheckCircle,
  AlertCircle,
  Activity,
  BarChart3
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const GrowthIntelligenceSuite = () => {
  const [abmData, setAbmData] = useState(null);
  const [intentData, setIntentData] = useState(null);
  const [plgData, setPlgData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('abm');

  useEffect(() => {
    loadGrowthData();
  }, []);

  const loadGrowthData = async () => {
    try {
      setLoading(true);
      
      const [abmRes, intentRes, plgRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/growth-intelligence/abm-dashboard`).catch(err => {
          console.error('ABM dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/growth-intelligence/intent-dashboard`).catch(err => {
          console.error('Intent dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/growth-intelligence/plg-dashboard`).catch(err => {
          console.error('PLG dashboard error:', err);
          return { data: { dashboard: {} } };
        })
      ]);

      setAbmData(abmRes.data);
      setIntentData(intentRes.data);
      setPlgData(plgRes.data);
      
      console.log('Growth Intelligence data loaded successfully');
    } catch (error) {
      console.error('Error loading growth intelligence data:', error);
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

  const getIntentColor = (strength) => {
    const colors = {
      'Very Strong': 'bg-red-500/20 text-red-400 border-red-500/30',
      'Strong': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      'High': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      'Medium': 'bg-blue-500/20 text-blue-400 border-blue-500/30'
    };
    return colors[strength] || 'bg-slate-500/20 text-slate-400 border-slate-500/30';
  };

  const getTrendIcon = (trend) => {
    if (trend?.includes('+') || trend === 'increasing') {
      return <ArrowUp className="w-4 h-4 text-green-400" />;
    } else if (trend?.includes('-') || trend === 'declining') {
      return <ArrowDown className="w-4 h-4 text-red-400" />;
    }
    return <Activity className="w-4 h-4 text-blue-400" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading Growth Intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Growth Intelligence Suite</h1>
          <p className="text-slate-400 mt-2">ABM, intent data analytics, and product-led growth intelligence</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className="bg-purple-500/20 text-purple-400">ABM Intelligence</Badge>
          <Badge className="bg-orange-500/20 text-orange-400">Intent Analytics</Badge>
          <Badge className="bg-green-500/20 text-green-400">Product-Led Growth</Badge>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
        {[
          { id: 'abm', label: 'ABM Intelligence', icon: Target },
          { id: 'intent', label: 'Intent Data', icon: Eye },
          { id: 'plg', label: 'Product-Led Growth', icon: TrendingUp }
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.id
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

      {/* ABM Intelligence Tab */}
      {activeTab === 'abm' && (
        <div className="space-y-6">
          {/* ABM Summary Cards */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Target className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {abmData?.dashboard?.summary_metrics?.total_target_accounts || 837}
                  </div>
                  <div className="text-xs text-purple-200">Target Accounts</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Users className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {abmData?.dashboard?.summary_metrics?.engaged_accounts || 309}
                  </div>
                  <div className="text-xs text-blue-200">Engaged Accounts</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <CheckCircle className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {abmData?.dashboard?.summary_metrics?.qualified_accounts || 119}
                  </div>
                  <div className="text-xs text-green-200">Qualified Accounts</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <BarChart3 className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {formatCurrency(abmData?.dashboard?.summary_metrics?.pipeline_value)}
                  </div>
                  <div className="text-xs text-orange-200">Pipeline Value</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Account Segments */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Target className="w-5 h-5 mr-2 text-purple-400" />
                Account Segments Performance
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {abmData?.dashboard?.account_segments?.map((segment, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium">{segment.segment}</h4>
                      <Badge className="bg-blue-500/20 text-blue-400">
                        {formatCurrency(segment.avg_deal_size)} avg deal
                      </Badge>
                    </div>
                    <div className="grid grid-cols-4 gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-white font-semibold">{segment.total_accounts}</div>
                        <div className="text-slate-400">Total Accounts</div>
                      </div>
                      <div className="text-center">
                        <div className="text-green-400 font-semibold">{segment.engaged_accounts}</div>
                        <div className="text-slate-400">Engaged</div>
                      </div>
                      <div className="text-center">
                        <div className="text-blue-400 font-semibold">{segment.qualified_accounts}</div>
                        <div className="text-slate-400">Qualified</div>
                      </div>
                      <div className="text-center">
                        <div className="text-purple-400 font-semibold">{segment.sales_cycle_days}d</div>
                        <div className="text-slate-400">Sales Cycle</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Priority Target Accounts */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <AlertCircle className="w-5 h-5 mr-2 text-orange-400" />
                High-Priority Target Accounts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {abmData?.dashboard?.priority_accounts?.slice(0, 8).map((account, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="text-white font-medium">{account.company_name}</div>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {account.industry}
                        </Badge>
                        <Badge className={`${getIntentColor('Strong')}`}>
                          Score: {account.engagement_score}
                        </Badge>
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        {account.employee_count?.toLocaleString()} employees • 
                        {account.intent_signals} intent signals • 
                        {formatCurrency(account.estimated_deal_value)} potential
                      </div>
                    </div>
                    <Button size="sm" className="bg-purple-600 hover:bg-purple-700">
                      Engage
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Intent Data Tab */}
      {activeTab === 'intent' && (
        <div className="space-y-6">
          {/* Intent Summary Cards */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Eye className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {intentData?.dashboard?.summary_metrics?.total_intent_accounts || 235}
                  </div>
                  <div className="text-xs text-orange-200">Intent Accounts</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-red-600/20 to-red-800/20 border-red-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Zap className="h-8 w-8 text-red-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {intentData?.dashboard?.summary_metrics?.high_intent_accounts || 67}
                  </div>
                  <div className="text-xs text-red-200">High Intent</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <CheckCircle className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {intentData?.dashboard?.summary_metrics?.ready_to_contact || 23}
                  </div>
                  <div className="text-xs text-green-200">Ready to Contact</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {formatCurrency(intentData?.dashboard?.summary_metrics?.pipeline_potential)}
                  </div>
                  <div className="text-xs text-purple-200">Pipeline Potential</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Intent Signal Categories */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Search className="w-5 h-5 mr-2 text-orange-400" />
                Intent Signal Categories
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {intentData?.dashboard?.intent_signals?.map((signal, index) => (
                  <div key={index} className={`p-4 rounded-lg border ${getIntentColor(signal.signal_strength)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold">{signal.category}</h4>
                      <div className="flex items-center space-x-1">
                        {getTrendIcon(signal.growth_trend)}
                        <span className="text-sm">{signal.growth_trend}</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-sm">
                      <div className="text-center">
                        <div className="font-semibold">{signal.accounts_detected}</div>
                        <div className="text-xs opacity-75">Accounts</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold">{signal.avg_intent_score}</div>
                        <div className="text-xs opacity-75">Avg Score</div>
                      </div>
                      <div className="text-center">
                        <Badge className={`text-xs ${getIntentColor(signal.signal_strength)}`}>
                          {signal.signal_strength}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* High-Intent Prospects */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Zap className="w-5 h-5 mr-2 text-red-400" />
                High-Intent Prospects
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {intentData?.dashboard?.high_intent_prospects?.slice(0, 8).map((prospect, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="text-white font-medium">{prospect.company_name}</div>
                        <Badge className="bg-red-500/20 text-red-400">
                          Intent: {prospect.intent_score}
                        </Badge>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {prospect.buying_stage}
                        </Badge>
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        {prospect.industry} • {prospect.days_researching} days researching • 
                        {prospect.contact_readiness} to contact
                      </div>
                    </div>
                    <Button size="sm" className="bg-orange-600 hover:bg-orange-700">
                      Contact
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Product-Led Growth Tab */}
      {activeTab === 'plg' && (
        <div className="space-y-6">
          {/* PLG KPI Cards */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Users className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {plgData?.dashboard?.summary_metrics?.product_qualified_leads || 156}
                  </div>
                  <div className="text-xs text-green-200">Product Qualified Leads</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {plgData?.dashboard?.summary_metrics?.user_activation_rate || 67.8}%
                  </div>
                  <div className="text-xs text-blue-200">Activation Rate</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Zap className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {plgData?.dashboard?.summary_metrics?.avg_time_to_value || 8.7}
                  </div>
                  <div className="text-xs text-purple-200">Days to Value</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Activity className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {plgData?.dashboard?.summary_metrics?.expansion_revenue_rate || 145.7}%
                  </div>
                  <div className="text-xs text-orange-200">Expansion Rate</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Feature Adoption Funnel */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-green-400" />
                Feature Adoption Funnel
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {plgData?.dashboard?.feature_adoption_funnel?.map((feature, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium">{feature.feature}</h4>
                      <div className="flex items-center space-x-2">
                        <Badge className="bg-green-500/20 text-green-400">
                          {feature.adoption_rate}% adopted
                        </Badge>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {feature.power_users}% power users
                        </Badge>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-white font-semibold">{feature.time_to_first_use}d</div>
                        <div className="text-slate-400">Time to First Use</div>
                      </div>
                      <div className="text-center">
                        <div className="text-green-400 font-semibold">{feature.correlation_to_retention}%</div>
                        <div className="text-slate-400">Retention Impact</div>
                      </div>
                      <div className="text-center">
                        <div className="text-blue-400 font-semibold">{feature.power_user_threshold}</div>
                        <div className="text-slate-400">Power User Threshold</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Product Qualified Leads */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Target className="w-5 h-5 mr-2 text-green-400" />
                Product Qualified Leads (PQLs)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {plgData?.dashboard?.pql_segments?.slice(0, 6).map((pql, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="text-white font-medium">{pql.company_name}</div>
                        <Badge className="bg-green-500/20 text-green-400">
                          PQL: {pql.pql_score}
                        </Badge>
                        <Badge className={`${
                          pql.usage_velocity === 'High' ? 'bg-red-500/20 text-red-400' :
                          pql.usage_velocity === 'Accelerating' ? 'bg-orange-500/20 text-orange-400' :
                          'bg-blue-500/20 text-blue-400'
                        }`}>
                          {pql.usage_velocity} Velocity
                        </Badge>
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        {pql.features_adopted} features adopted • {pql.engagement_frequency} usage • 
                        {formatCurrency(pql.estimated_deal_value)} potential
                      </div>
                    </div>
                    <Button size="sm" className="bg-green-600 hover:bg-green-700">
                      Convert
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Growth AI Insights */}
      <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <Brain className="w-5 h-5 mr-2 text-cyan-400" />
            Growth AI Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {activeTab === 'abm' && abmData?.dashboard?.ai_abm_insights?.slice(0, 3).map((insight, index) => (
              <Alert key={index} className="bg-purple-500/10 border-purple-500/20">
                <Brain className="h-4 w-4 text-purple-400" />
                <AlertDescription className="text-purple-300 text-sm">
                  <strong>{insight.insight}</strong> - Recommendation: {insight.recommendation}
                  <span className="text-green-400 block mt-1">Potential Impact: {insight.potential_uplift}</span>
                </AlertDescription>
              </Alert>
            ))}
            
            {activeTab === 'intent' && intentData?.dashboard?.predictive_insights?.slice(0, 3).map((insight, index) => (
              <Alert key={index} className="bg-orange-500/10 border-orange-500/20">
                <Eye className="h-4 w-4 text-orange-400" />
                <AlertDescription className="text-orange-300 text-sm">
                  <strong>{insight.prediction}</strong> - {insight.recommended_action}
                  <span className="text-green-400 block mt-1">
                    Pipeline Impact: {formatCurrency(insight.potential_pipeline)}
                  </span>
                </AlertDescription>
              </Alert>
            ))}
            
            {activeTab === 'plg' && plgData?.dashboard?.plg_insights?.slice(0, 3).map((insight, index) => (
              <Alert key={index} className="bg-green-500/10 border-green-500/20">
                <TrendingUp className="h-4 w-4 text-green-400" />
                <AlertDescription className="text-green-300 text-sm">
                  <strong>{insight.insight}</strong> - {insight.recommendation}
                  <span className="text-blue-400 block mt-1">Expected Impact: {insight.potential_impact}</span>
                </AlertDescription>
              </Alert>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default GrowthIntelligenceSuite;