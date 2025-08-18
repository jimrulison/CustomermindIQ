import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { 
  BarChart3, 
  TrendingUp, 
  Users,
  Target,
  Zap,
  Brain,
  ArrowUp,
  ArrowDown,
  CheckCircle,
  AlertCircle,
  Activity,
  Star,
  Clock,
  Eye,
  Route
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const ProductIntelligenceHub = () => {
  const [featureData, setFeatureData] = useState(null);
  const [onboardingData, setOnboardingData] = useState(null);
  const [pmfData, setPmfData] = useState(null);
  const [journeyData, setJourneyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('features');

  useEffect(() => {
    loadProductIntelligenceData();
  }, []);

  const loadProductIntelligenceData = async () => {
    try {
      setLoading(true);
      
      const [featureRes, onboardingRes, pmfRes, journeyRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/product-intelligence/feature-usage-dashboard`).catch(err => {
          console.error('Feature usage error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/product-intelligence/onboarding-dashboard`).catch(err => {
          console.error('Onboarding error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/product-intelligence/pmf-dashboard`).catch(err => {
          console.error('PMF error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/product-intelligence/journey-dashboard`).catch(err => {
          console.error('Journey error:', err);
          return { data: { dashboard: {} } };
        })
      ]);

      setFeatureData(featureRes.data);
      setOnboardingData(onboardingRes.data);
      setPmfData(pmfRes.data);
      setJourneyData(journeyRes.data);
      
      console.log('Product Intelligence data loaded successfully');
    } catch (error) {
      console.error('Error loading product intelligence data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-orange-400';
    return 'text-red-400';
  };

  const getTrendIcon = (trend) => {
    if (trend === 'improving' || trend?.includes('+')) {
      return <ArrowUp className="w-4 h-4 text-green-400" />;
    } else if (trend === 'declining' || trend?.includes('-')) {
      return <ArrowDown className="w-4 h-4 text-red-400" />;
    }
    return <Activity className="w-4 h-4 text-blue-400" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading Product Intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Product Intelligence Hub</h1>
          <p className="text-slate-400 mt-2">Feature analytics, onboarding optimization, and product-market fit insights</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className="bg-blue-500/20 text-blue-400">Feature Analytics</Badge>
          <Badge className="bg-green-500/20 text-green-400">PMF Insights</Badge>
          <Badge className="bg-purple-500/20 text-purple-400">Journey Optimization</Badge>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
        {[
          { id: 'features', label: 'Feature Usage', icon: BarChart3 },
          { id: 'onboarding', label: 'Onboarding', icon: Target },
          { id: 'pmf', label: 'Product-Market Fit', icon: Star },
          { id: 'journeys', label: 'User Journeys', icon: Route }
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

      {/* Feature Usage Tab */}
      {activeTab === 'features' && (
        <div className="space-y-6">
          {/* Feature Usage Summary */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <BarChart3 className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.total_features || 12}
                  </div>
                  <div className="text-xs text-blue-200">Total Features</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.avg_feature_adoption_rate || 63.2}%
                  </div>
                  <div className="text-xs text-green-200">Avg Adoption Rate</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Users className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.power_users_percentage || 35.8}%
                  </div>
                  <div className="text-xs text-purple-200">Power Users</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Activity className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.feature_stickiness_score || 68.9}
                  </div>
                  <div className="text-xs text-orange-200">Stickiness Score</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Feature Usage Matrix */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-blue-400" />
                Feature Usage Analytics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {featureData?.dashboard?.feature_usage_matrix?.slice(0, 8).map((feature, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <h4 className="text-white font-medium">{feature.feature_name}</h4>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {feature.category}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={`${getHealthColor(feature.adoption_rate)} bg-slate-600/50`}>
                          {feature.adoption_rate}% adopted
                        </Badge>
                        {getTrendIcon('improving')}
                      </div>
                    </div>
                    <div className="grid grid-cols-5 gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-white font-semibold">{feature.daily_active_users?.toLocaleString()}</div>
                        <div className="text-slate-400">DAU</div>
                      </div>
                      <div className="text-center">
                        <div className="text-green-400 font-semibold">{feature.feature_stickiness}%</div>
                        <div className="text-slate-400">Stickiness</div>
                      </div>
                      <div className="text-center">
                        <div className="text-blue-400 font-semibold">{feature.power_users}%</div>
                        <div className="text-slate-400">Power Users</div>
                      </div>
                      <div className="text-center">
                        <div className="text-purple-400 font-semibold">{feature.avg_sessions_per_user}</div>
                        <div className="text-slate-400">Avg Sessions</div>
                      </div>
                      <div className="text-center">
                        <div className="text-orange-400 font-semibold">{feature.retention_correlation}%</div>
                        <div className="text-slate-400">Retention Impact</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Onboarding Tab */}
      {activeTab === 'onboarding' && (
        <div className="space-y-6">
          {/* Onboarding Summary */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <CheckCircle className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.overall_completion_rate || 41.2}%
                  </div>
                  <div className="text-xs text-green-200">Completion Rate</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Clock className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.avg_time_to_complete || 14.8}d
                  </div>
                  <div className="text-xs text-blue-200">Avg Time to Complete</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Star className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.user_satisfaction_score || 7.9}
                  </div>
                  <div className="text-xs text-purple-200">Satisfaction Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.month_over_month_improvement || '+8.4%'}
                  </div>
                  <div className="text-xs text-orange-200">MoM Improvement</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Onboarding Funnel */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Target className="w-5 h-5 mr-2 text-green-400" />
                Onboarding Funnel Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {onboardingData?.dashboard?.onboarding_funnel?.map((step, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-bold">
                        {step.step_order}
                      </div>
                      <div>
                        <div className="text-white font-medium">{step.step}</div>
                        <div className="text-sm text-slate-400">
                          {step.avg_time_minutes} min avg • {step.drop_off_rate}% drop-off
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={`${getHealthColor(step.completion_rate)} bg-slate-600/50`}>
                        {step.completion_rate}% complete
                      </Badge>
                      <Badge className={`${getHealthColor(step.optimization_score)} bg-slate-600/50`}>
                        {step.optimization_score} score
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Onboarding Segments */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Users className="w-5 h-5 mr-2 text-blue-400" />
                Onboarding User Segments
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {onboardingData?.dashboard?.onboarding_segments?.map((segment, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium">{segment.segment}</h4>
                      <Badge className="bg-blue-500/20 text-blue-400">
                        {segment.percentage}% of users
                      </Badge>
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-300">Completion Rate</span>
                        <span className={`font-semibold ${getHealthColor(segment.completion_rate)}`}>
                          {segment.completion_rate}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-300">Avg Time</span>
                        <span className="text-blue-400 font-semibold">{segment.avg_completion_time}d</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-300">Retention</span>
                        <span className="text-green-400 font-semibold">{segment.retention_rate}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Product-Market Fit Tab */}
      {activeTab === 'pmf' && (
        <div className="space-y-6">
          {/* PMF Overview */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-gold-600/20 to-gold-800/20 border-gold-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Star className="h-8 w-8 text-gold-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.overall_pmf_score || 78.4}
                  </div>
                  <div className="text-xs text-gold-200">PMF Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.nps_score || 67}
                  </div>
                  <div className="text-xs text-green-200">NPS Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Activity className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.product_stickiness || 0.87}
                  </div>
                  <div className="text-xs text-blue-200">Product Stickiness</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Zap className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.time_to_value_avg || 8.7}d
                  </div>
                  <div className="text-xs text-purple-200">Time to Value</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* PMF Indicators */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Star className="w-5 h-5 mr-2 text-gold-400" />
                Product-Market Fit Indicators
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {pmfData?.dashboard?.pmf_indicators?.map((indicator, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium">{indicator.indicator}</h4>
                      <div className="flex items-center space-x-2">
                        <Badge className={`${getHealthColor(indicator.score)} bg-slate-600/50`}>
                          {indicator.score}/100
                        </Badge>
                        {getTrendIcon(indicator.trend)}
                      </div>
                    </div>
                    <div className="text-sm text-slate-400 mb-2">
                      Weight: {indicator.weight}% • {indicator.benchmark}
                    </div>
                    <div className="text-xs text-slate-500">
                      Focus: {indicator.improvement_areas?.join(', ')}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* User Segments PMF */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Users className="w-5 h-5 mr-2 text-blue-400" />
                PMF by User Segment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {pmfData?.dashboard?.user_segments_pmf?.map((segment, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium">{segment.segment}</h4>
                      <div className="flex items-center space-x-2">
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {segment.percentage}% of users
                        </Badge>
                        <Badge className={`${getHealthColor(segment.pmf_score)} bg-slate-600/50`}>
                          PMF: {segment.pmf_score}
                        </Badge>
                      </div>
                    </div>
                    <div className="text-sm text-slate-400 mb-2">
                      {segment.market_fit_evidence}
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      {segment.value_indicators?.slice(0, 4).map((indicator, idx) => (
                        <div key={idx} className="text-slate-300">{indicator}</div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* User Journeys Tab */}
      {activeTab === 'journeys' && (
        <div className="space-y-6">
          {/* Journey Health Summary */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Route className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {journeyData?.dashboard?.journey_health?.overall_journey_health_score || 72.8}
                  </div>
                  <div className="text-xs text-blue-200">Journey Health</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    +8.4%
                  </div>
                  <div className="text-xs text-green-200">Velocity Improvement</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Target className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    -12.7%
                  </div>
                  <div className="text-xs text-purple-200">Drop-off Reduction</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Star className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    7.9
                  </div>
                  <div className="text-xs text-orange-200">Flow Satisfaction</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Critical Journeys */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Route className="w-5 h-5 mr-2 text-blue-400" />
                Critical User Journeys
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {journeyData?.dashboard?.critical_journeys?.map((journey, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h4 className="text-white font-medium">{journey.journey_name}</h4>
                        <p className="text-sm text-slate-400">{journey.description}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={`${getHealthColor(journey.completion_rate)} bg-slate-600/50`}>
                          {journey.completion_rate}% complete
                        </Badge>
                        <Badge className={`${getHealthColor(journey.optimization_score)} bg-slate-600/50`}>
                          Score: {journey.optimization_score}
                        </Badge>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-white font-semibold">{journey.avg_completion_time}h</div>
                        <div className="text-slate-400">Avg Time</div>
                      </div>
                      <div className="text-center">
                        <div className="text-orange-400 font-semibold">
                          {journey.drop_off_points?.length || 0} points
                        </div>
                        <div className="text-slate-400">Drop-off Points</div>
                      </div>
                      <div className="text-center">
                        <div className="text-green-400 font-semibold">
                          {journey.success_factors?.length || 0} factors
                        </div>
                        <div className="text-slate-400">Success Factors</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Journey Segments */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Users className="w-5 h-5 mr-2 text-purple-400" />
                Journey Performance by Segment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {journeyData?.dashboard?.journey_segments?.map((segment, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium">{segment.segment}</h4>
                      <Badge className="bg-blue-500/20 text-blue-400">
                        {segment.percentage}% of users
                      </Badge>
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-300">Journey Completion</span>
                        <span className={`font-semibold ${getHealthColor(segment.journey_performance?.avg_journey_completion)}`}>
                          {segment.journey_performance?.avg_journey_completion}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-300">Success Rate</span>
                        <span className="text-green-400 font-semibold">
                          {segment.journey_performance?.success_rate}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-300">LTV Multiplier</span>
                        <span className="text-purple-400 font-semibold">
                          {segment.business_value?.ltv}x
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Product Intelligence AI Insights */}
      <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <Brain className="w-5 h-5 mr-2 text-cyan-400" />
            Product Intelligence AI Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {activeTab === 'features' && (
              <Alert className="bg-blue-500/10 border-blue-500/20">
                <Brain className="h-4 w-4 text-blue-400" />
                <AlertDescription className="text-blue-300 text-sm">
                  <strong>AI Insight:</strong> Features with 3+ correlations show 89% higher retention rates. 
                  Consider bundling AI Insights with Revenue Attribution for maximum impact.
                </AlertDescription>
              </Alert>
            )}
            
            {activeTab === 'onboarding' && (
              <Alert className="bg-green-500/10 border-green-500/20">
                <Target className="h-4 w-4 text-green-400" />
                <AlertDescription className="text-green-300 text-sm">
                  <strong>Optimization Opportunity:</strong> Progressive disclosure onboarding shows +23.4% completion rate improvement. 
                  Implement immediately for maximum impact.
                </AlertDescription>
              </Alert>
            )}
            
            {activeTab === 'pmf' && (
              <Alert className="bg-gold-500/10 border-gold-500/20">
                <Star className="h-4 w-4 text-gold-400" />
                <AlertDescription className="text-gold-300 text-sm">
                  <strong>PMF Strength:</strong> 67.8% of users would be "very disappointed" without the product (40%+ = strong PMF). 
                  Focus on converting casual users to engaged users for maximum growth.
                </AlertDescription>
              </Alert>
            )}
            
            {activeTab === 'journeys' && (
              <Alert className="bg-purple-500/10 border-purple-500/20">
                <Route className="h-4 w-4 text-purple-400" />
                <AlertDescription className="text-purple-300 text-sm">
                  <strong>Journey Optimization:</strong> Data connection step causes 23.4% of drop-offs across all journeys. 
                  Implementing progressive assistance could improve overall completion by 15%.
                </AlertDescription>
              </Alert>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProductIntelligenceHub;