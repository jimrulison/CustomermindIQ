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
  Route,
  X,
  Database,
  RefreshCw,
  Info,
  TrendingUp as TrendIcon,
  BarChart,
  PieChart
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
  const [showDataSourceModal, setShowDataSourceModal] = useState(false);
  const [selectedDataSource, setSelectedDataSource] = useState(null);

  // Data source drill-down handlers for all sections
  const showDataSource = (section, metricType, metricName, currentValue) => {
    const sourceDetails = {
      // FEATURE USAGE DATA SOURCES
      'features_total_features': {
        title: 'Total Features - Data Source',
        description: 'Complete inventory of product features and their tracking status',
        sources: [
          '• Product Analytics SDK: Real-time feature usage tracking',
          '• Application Database: Feature configuration and metadata',
          '• Event Logging System: User interaction capture',
          '• API Gateway: Feature access and utilization logs'
        ],
        methodology: 'Features identified through code analysis, SDK integration, and manual configuration. Active tracking covers user interactions, session data, and conversion events.',
        dataPoints: 'Click events, page views, feature activation, time spent, user flows, error rates',
        updateFrequency: 'Real-time with 5-minute aggregation intervals',
        currentValue: currentValue,
        icon: BarChart3,
        color: 'blue'
      },
      'features_avg_adoption_rate': {
        title: 'Average Adoption Rate - Data Source',
        description: 'Calculated adoption percentage across all tracked features',
        sources: [
          '• User Behavior Analytics: Individual user feature interactions',
          '• Cohort Analysis Engine: User segment adoption patterns',
          '• A/B Testing Platform: Feature rollout and adoption tracking',
          '• Customer Success Platform: Feature usage correlation with retention'
        ],
        methodology: 'Adoption rate = (Users who used feature in last 30 days / Total active users) × 100. Weighted by feature importance and user segment.',
        dataPoints: 'Unique users per feature, session frequency, feature depth usage, onboarding completion',
        updateFrequency: 'Updated daily at 3:00 AM UTC with rolling 30-day windows',
        currentValue: currentValue,
        icon: TrendingUp,
        color: 'green'
      },
      'features_power_users': {
        title: 'Power Users Percentage - Data Source',
        description: 'Users exhibiting high engagement across multiple features',
        sources: [
          '• User Engagement Scoring: Multi-feature usage patterns',
          '• Session Analytics: Deep usage behavior analysis',
          '• Product Intelligence ML: Usage pattern classification',
          '• Customer Health Scoring: Engagement correlation with success metrics'
        ],
        methodology: 'Power users defined as top 20% by engagement score: feature breadth (40%), usage frequency (35%), session depth (25%). ML algorithms identify patterns.',
        dataPoints: 'Features used per session, session duration, feature exploration rate, advanced feature adoption',
        updateFrequency: 'Recalculated weekly with daily incremental updates',
        currentValue: currentValue,
        icon: Users,
        color: 'purple'
      },
      'features_stickiness_score': {
        title: 'Feature Stickiness Score - Data Source',
        description: 'Measure of feature retention and habitual usage patterns',
        sources: [
          '• Retention Analytics Engine: User return behavior per feature',
          '• Usage Frequency Tracker: Daily/weekly/monthly usage patterns',
          '• Behavioral Cohort Analysis: Feature abandonment and adoption curves',
          '• Predictive Models: Churn risk based on feature usage decline'
        ],
        methodology: 'Stickiness = (DAU/MAU) × Feature Depth Factor × Retention Weight. Accounts for usage consistency, feature complexity, and user segment behavior.',
        dataPoints: 'Daily active users, monthly active users, feature session depth, return visit patterns, feature churn events',
        updateFrequency: 'Real-time computation with hourly rolling averages',
        currentValue: currentValue,
        icon: Activity,
        color: 'orange'
      },
      // ONBOARDING DATA SOURCES
      'onboarding_completion_rate': {
        title: 'Onboarding Completion Rate - Data Source',
        description: 'Percentage of users who complete the full onboarding process',
        sources: [
          '• Onboarding Analytics: Step-by-step completion tracking',
          '• User Journey Mapping: Flow progression analysis',
          '• Event Tracking: Milestone and checkpoint completion',
          '• Session Recording: User behavior during onboarding'
        ],
        methodology: 'Completion Rate = (Users completing all onboarding steps / Users starting onboarding) × 100. Tracks critical milestones and identifies drop-off points.',
        dataPoints: 'Step completion events, time per step, abandonment points, user segment performance',
        updateFrequency: 'Real-time tracking with hourly summary reports',
        currentValue: currentValue,
        icon: CheckCircle,
        color: 'green'
      },
      'onboarding_avg_time_to_complete': {
        title: 'Average Time to Complete - Data Source',
        description: 'Mean duration for users to complete onboarding process',
        sources: [
          '• Timing Analytics: Precise step duration measurement',
          '• User Session Data: Start/end timestamp tracking',
          '• Flow Analytics: Multi-session completion tracking',
          '• Behavioral Segmentation: Time variance by user type'
        ],
        methodology: 'Average calculated from first onboarding step to final completion, excluding inactive periods >24 hours. Segmented by user type and entry point.',
        dataPoints: 'Session timestamps, step durations, pause periods, completion paths',
        updateFrequency: 'Updated daily with rolling 30-day averages',
        currentValue: currentValue,
        icon: Clock,
        color: 'blue'
      },
      'onboarding_drop_off_rate': {
        title: 'Drop-off Rate - Data Source',
        description: 'Percentage of users who abandon onboarding before completion',
        sources: [
          '• Funnel Analytics: Step-by-step abandonment tracking',
          '• Exit Intent Detection: User departure behavior analysis',
          '• A/B Testing: Onboarding variant performance comparison',
          '• User Feedback: Exit surveys and abandonment reasons'
        ],
        methodology: 'Drop-off Rate = 100% - Completion Rate. Analyzed by step, user segment, traffic source, and device type to identify improvement opportunities.',
        dataPoints: 'Exit points, abandonment triggers, device data, referral sources, user demographics',
        updateFrequency: 'Real-time with daily trend analysis',
        currentValue: currentValue,
        icon: AlertCircle,
        color: 'red'
      },
      'onboarding_feature_discovery': {
        title: 'Feature Discovery Rate - Data Source',
        description: 'Percentage of users discovering key features during onboarding',
        sources: [
          '• Feature Interaction Tracking: Discovery event logging',
          '• Onboarding Progress Analytics: Feature exposure measurement',
          '• User Engagement Metrics: Post-onboarding feature adoption',
          '• Guided Tour Analytics: Tutorial completion and interaction'
        ],
        methodology: 'Discovery Rate = (Users interacting with key features during onboarding / Total users in onboarding) × 100. Weighted by feature importance and business impact.',
        dataPoints: 'Feature clicks, tutorial completions, help usage, feature adoption post-onboarding',
        updateFrequency: 'Real-time with weekly trend analysis',
        currentValue: currentValue,
        icon: Eye,
        color: 'cyan'
      },
      // PRODUCT-MARKET FIT DATA SOURCES
      'pmf_overall_score': {
        title: 'Overall PMF Score - Data Source',
        description: 'Comprehensive product-market fit assessment score',
        sources: [
          '• Customer Satisfaction Surveys: NPS and satisfaction metrics',
          '• Usage Analytics: Product engagement and retention data',
          '• Market Research: Competitive positioning analysis',
          '• Customer Success Data: Churn, expansion, and success metrics'
        ],
        methodology: 'PMF Score = weighted average of satisfaction (30%), retention (25%), growth (20%), competitive advantage (15%), market penetration (10%). Normalized to 0-100 scale.',
        dataPoints: 'NPS scores, churn rates, usage frequency, expansion revenue, market share data',
        updateFrequency: 'Monthly calculation with quarterly deep analysis',
        currentValue: currentValue,
        icon: Star,
        color: 'yellow'
      },
      'pmf_nps_score': {
        title: 'Net Promoter Score - Data Source',
        description: 'Customer loyalty and satisfaction measurement',
        sources: [
          '• Customer Surveys: In-app and email NPS surveys',
          '• Customer Success Platform: Relationship health tracking',
          '• Support Ticket Analysis: Sentiment analysis of interactions',
          '• Product Review Monitoring: External review aggregation'
        ],
        methodology: 'NPS = % Promoters (9-10) - % Detractors (0-6). Collected through systematic surveys with 90-day rotation and sentiment analysis of support interactions.',
        dataPoints: 'Survey responses, support sentiment, review scores, referral tracking',
        updateFrequency: 'Continuous collection with monthly NPS calculation',
        currentValue: currentValue,
        icon: TrendIcon,
        color: 'emerald'
      },
      'pmf_customer_satisfaction': {
        title: 'Customer Satisfaction - Data Source',
        description: 'Overall customer happiness and product satisfaction',
        sources: [
          '• CSAT Surveys: Post-interaction satisfaction measurement',
          '• Product Feedback: In-app rating and feedback collection',
          '• Customer Success Metrics: Health score and engagement tracking',
          '• Behavioral Analytics: Usage patterns indicating satisfaction'
        ],
        methodology: 'Satisfaction = average of CSAT surveys (40%), product ratings (30%), usage engagement (20%), support sentiment (10%). Scale normalized to percentage.',
        dataPoints: 'CSAT scores, product ratings, session duration, feature adoption, support interactions',
        updateFrequency: 'Real-time collection with weekly satisfaction calculation',
        currentValue: currentValue,
        icon: CheckCircle,
        color: 'green'
      },
      'pmf_market_penetration': {
        title: 'Market Penetration - Data Source',
        description: 'Market share and competitive positioning metrics',
        sources: [
          '• Market Research Data: Industry reports and competitive analysis',
          '• Customer Acquisition Analytics: Market share tracking',
          '• Competitive Intelligence: Feature comparison and positioning',
          '• Industry Benchmarking: Performance vs. market standards'
        ],
        methodology: 'Market Penetration = (Our customers / Total addressable market) × 100. Combined with competitive feature analysis and market positioning assessment.',
        dataPoints: 'Customer counts, market size estimates, competitive feature matrices, industry benchmarks',
        updateFrequency: 'Quarterly assessment with monthly trend tracking',
        currentValue: currentValue,
        icon: BarChart,
        color: 'indigo'
      },
      // USER JOURNEYS DATA SOURCES
      'journeys_total_paths': {
        title: 'Total Journey Paths - Data Source',
        description: 'Number of distinct user journey paths through the product',
        sources: [
          '• User Flow Analytics: Complete user journey mapping',
          '• Session Replay Data: Detailed interaction sequences',
          '• Event Stream Processing: Real-time journey construction',
          '• Machine Learning: Pattern recognition and path classification'
        ],
        methodology: 'Journey paths identified using ML clustering of user behavior sequences. Paths must have >10 users and >5% completion rate to be considered significant.',
        dataPoints: 'Page sequences, click paths, session flows, conversion funnels, abandonment points',
        updateFrequency: 'Daily path analysis with weekly pattern recognition',
        currentValue: currentValue,
        icon: Route,
        color: 'teal'
      },
      'journeys_avg_completion_rate': {
        title: 'Average Completion Rate - Data Source',
        description: 'Percentage of users completing their intended journeys',
        sources: [
          '• Goal Completion Tracking: Conversion and task completion',
          '• Funnel Analytics: Multi-step process completion',
          '• Intent Recognition: User goal identification and tracking',
          '• Behavioral Analytics: Success vs. abandonment patterns'
        ],
        methodology: 'Completion Rate = (Successful journey completions / Total journey attempts) × 100. Success defined by reaching conversion goals or key milestones.',
        dataPoints: 'Goal completions, funnel progression, task success, user intent signals',
        updateFrequency: 'Real-time tracking with daily completion analysis',
        currentValue: currentValue,
        icon: Target,
        color: 'green'
      },
      'journeys_avg_steps_to_conversion': {
        title: 'Average Steps to Conversion - Data Source',
        description: 'Mean number of interactions required to reach conversion goals',
        sources: [
          '• Conversion Funnel Analytics: Step-by-step progression tracking',
          '• User Path Analysis: Interaction sequence measurement',
          '• Goal Flow Reports: Conversion path optimization data',
          '• A/B Testing: Path efficiency comparison analysis'
        ],
        methodology: 'Steps to Conversion = average number of meaningful interactions from entry to goal completion. Excludes navigational and non-productive actions.',
        dataPoints: 'Click sequences, page views, form interactions, conversion events, path efficiency metrics',
        updateFrequency: 'Daily calculation with trend analysis',
        currentValue: currentValue,
        icon: Activity,
        color: 'blue'
      },
      'journeys_optimization_score': {
        title: 'Journey Optimization Score - Data Source',
        description: 'Efficiency and effectiveness rating of user journey design',
        sources: [
          '• UX Analytics: User experience and friction analysis',
          '• Performance Metrics: Journey speed and efficiency tracking',
          '• Conversion Optimization: A/B test results and improvements',
          '• User Feedback: Journey satisfaction and pain point identification'
        ],
        methodology: 'Optimization Score = weighted combination of completion rate (35%), steps efficiency (25%), time to conversion (20%), user satisfaction (20%). Normalized 0-100.',
        dataPoints: 'Completion rates, interaction efficiency, time metrics, satisfaction scores, friction points',
        updateFrequency: 'Weekly optimization analysis with continuous monitoring',
        currentValue: currentValue,
        icon: Zap,
        color: 'yellow'
      }
    };

    const key = `${section}_${metricType}`;
    const details = sourceDetails[key] || {
      title: `${metricName} - Data Source`,
      description: 'Data source information for this metric',
      sources: ['• Multiple data collection systems', '• Real-time analytics platforms', '• User behavior tracking', '• Performance monitoring'],
      methodology: 'Calculated using advanced analytics algorithms and machine learning models',
      dataPoints: 'User interactions, behavior patterns, performance metrics, and business outcomes',
      updateFrequency: 'Updated regularly based on data collection schedules',
      currentValue: currentValue,
      icon: Database,
      color: 'slate'
    };

    setSelectedDataSource(details);
    setShowDataSourceModal(true);
  };

  // Feature detail drill-down
  const showFeatureDetails = (feature) => {
    const featureDetails = {
      title: `Feature Analysis: ${feature.feature_name}`,
      description: `Comprehensive analytics and insights for ${feature.feature_name} feature usage`,
      icon: BarChart3,
      color: 'blue',
      currentValue: `${feature.adoption_rate}% adoption`,
      category: feature.category,
      usageData: {
        dailyActiveUsers: feature.daily_active_users?.toLocaleString() || 'N/A',
        adoptionRate: `${feature.adoption_rate || 'N/A'}% of total users`,
        stickiness: `${feature.feature_stickiness || 'N/A'}% (DAU/MAU ratio)`,
        powerUsers: `${feature.power_users || 'N/A'}% are heavy users`,
        avgSessions: feature.avg_sessions_per_user || 'N/A',
        retentionImpact: `${feature.retention_correlation || 'N/A'}% correlation`
      },
      dataSources: [
        'Event Tracking: User clicks, page views, interactions captured via analytics SDK',
        'Session Analytics: Usage duration, frequency patterns from behavioral tracking',
        'Cohort Analysis: User adoption and retention tracking through lifecycle management',
        'A/B Testing: Feature performance experiments and statistical analysis'
      ],
      insights: [
        feature.adoption_rate > 70 
          ? 'High adoption - consider expanding or creating similar features' 
          : 'Low adoption - investigate barriers: onboarding, UX, or feature discovery',
        feature.feature_stickiness > 60 
          ? 'Good retention - analyze success factors and apply to other features' 
          : 'Poor retention - improve UX, add tutorials, or consider redesign',
        feature.retention_correlation > 50 
          ? 'Strong retention driver - prioritize maintenance and enhancement' 
          : 'Weak retention impact - evaluate feature value or consider sunset'
      ],
      optimizations: [
        'Improve onboarding flow specifically for this feature',
        'Create contextual tutorials for advanced functionality',
        'Implement progressive disclosure for complex features',
        'Monitor usage patterns to identify optimization signals',
        'Set up automated alerts for usage anomalies'
      ]
    };

    setSelectedDataSource(featureDetails);
    setShowDataSourceModal(true);
  };

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
            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30 cursor-pointer hover:bg-blue-600/30 transition-all duration-200" onClick={() => showDataSource('features', 'total_features', 'Total Features', featureData?.dashboard?.summary_metrics?.total_features || 12)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <BarChart3 className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.total_features || 12}
                  </div>
                  <div className="text-xs text-blue-200">Total Features</div>
                  <div className="text-xs text-blue-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30 cursor-pointer hover:bg-green-600/30 transition-all duration-200" onClick={() => showDataSource('features', 'avg_adoption_rate', 'Average Adoption Rate', `${featureData?.dashboard?.summary_metrics?.avg_feature_adoption_rate || 63.2}%`)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.avg_feature_adoption_rate || 63.2}%
                  </div>
                  <div className="text-xs text-green-200">Avg Adoption Rate</div>
                  <div className="text-xs text-green-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30 cursor-pointer hover:bg-purple-600/30 transition-all duration-200" onClick={() => showDataSource('features', 'power_users', 'Power Users Percentage', `${featureData?.dashboard?.summary_metrics?.power_users_percentage || 35.8}%`)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Users className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.power_users_percentage || 35.8}%
                  </div>
                  <div className="text-xs text-purple-200">Power Users</div>
                  <div className="text-xs text-purple-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30 cursor-pointer hover:bg-orange-600/30 transition-all duration-200" onClick={() => showDataSource('features', 'stickiness_score', 'Feature Stickiness Score', featureData?.dashboard?.summary_metrics?.feature_stickiness_score || 68.9)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Activity className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {featureData?.dashboard?.summary_metrics?.feature_stickiness_score || 68.9}
                  </div>
                  <div className="text-xs text-orange-200">Stickiness Score</div>
                  <div className="text-xs text-orange-300 mt-1 opacity-75">Click for data source</div>
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
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg cursor-pointer hover:bg-slate-700/50 transition-all duration-200" onClick={() => showFeatureDetails(feature)}>
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
                        <div className="text-xs text-slate-400 ml-2">Click for details</div>
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
            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30 cursor-pointer hover:bg-green-600/30 transition-all duration-200" onClick={() => showDataSource('onboarding', 'completion_rate', 'Onboarding Completion Rate', `${onboardingData?.dashboard?.summary_metrics?.overall_completion_rate || 41.2}%`)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <CheckCircle className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.overall_completion_rate || 41.2}%
                  </div>
                  <div className="text-xs text-green-200">Completion Rate</div>
                  <div className="text-xs text-green-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30 cursor-pointer hover:bg-blue-600/30 transition-all duration-200" onClick={() => showDataSource('onboarding', 'avg_time_to_complete', 'Average Time to Complete', `${onboardingData?.dashboard?.summary_metrics?.avg_time_to_complete || 14.8}d`)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Clock className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.avg_time_to_complete || 14.8}d
                  </div>
                  <div className="text-xs text-blue-200">Avg Time to Complete</div>
                  <div className="text-xs text-blue-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30 cursor-pointer hover:bg-purple-600/30 transition-all duration-200" onClick={() => showDataSource('onboarding', 'drop_off_rate', 'Drop-off Rate', `${100 - (onboardingData?.dashboard?.summary_metrics?.overall_completion_rate || 41.2)}%`)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Star className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.user_satisfaction_score || 7.9}
                  </div>
                  <div className="text-xs text-purple-200">Satisfaction Score</div>
                  <div className="text-xs text-purple-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30 cursor-pointer hover:bg-orange-600/30 transition-all duration-200" onClick={() => showDataSource('onboarding', 'feature_discovery', 'Feature Discovery Rate', onboardingData?.dashboard?.summary_metrics?.month_over_month_improvement || '+8.4%')}>
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {onboardingData?.dashboard?.summary_metrics?.month_over_month_improvement || '+8.4%'}
                  </div>
                  <div className="text-xs text-orange-200">MoM Improvement</div>
                  <div className="text-xs text-orange-300 mt-1 opacity-75">Click for data source</div>
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
            <Card className="bg-gradient-to-br from-yellow-600/20 to-yellow-800/20 border-yellow-500/30 cursor-pointer hover:bg-yellow-600/30 transition-all duration-200" onClick={() => showDataSource('pmf', 'overall_score', 'Overall PMF Score', pmfData?.dashboard?.pmf_core_metrics?.overall_pmf_score || 78.4)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Star className="h-8 w-8 text-yellow-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.overall_pmf_score || 78.4}
                  </div>
                  <div className="text-xs text-yellow-200">PMF Score</div>
                  <div className="text-xs text-yellow-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30 cursor-pointer hover:bg-green-600/30 transition-all duration-200" onClick={() => showDataSource('pmf', 'nps_score', 'Net Promoter Score', pmfData?.dashboard?.pmf_core_metrics?.nps_score || 67)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.nps_score || 67}
                  </div>
                  <div className="text-xs text-green-200">NPS Score</div>
                  <div className="text-xs text-green-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30 cursor-pointer hover:bg-blue-600/30 transition-all duration-200" onClick={() => showDataSource('pmf', 'customer_satisfaction', 'Customer Satisfaction', `${(pmfData?.dashboard?.pmf_core_metrics?.product_stickiness || 0.87) * 100}%`)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Activity className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.product_stickiness || 0.87}
                  </div>
                  <div className="text-xs text-blue-200">Product Stickiness</div>
                  <div className="text-xs text-blue-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30 cursor-pointer hover:bg-purple-600/30 transition-all duration-200" onClick={() => showDataSource('pmf', 'market_penetration', 'Market Penetration', `${pmfData?.dashboard?.pmf_core_metrics?.time_to_value_avg || 8.7}d`)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Zap className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {pmfData?.dashboard?.pmf_core_metrics?.time_to_value_avg || 8.7}d
                  </div>
                  <div className="text-xs text-purple-200">Time to Value</div>
                  <div className="text-xs text-purple-300 mt-1 opacity-75">Click for data source</div>
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
            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30 cursor-pointer hover:bg-blue-600/30 transition-all duration-200" onClick={() => showDataSource('journeys', 'total_paths', 'Total Journey Paths', journeyData?.dashboard?.journey_health?.overall_journey_health_score || 72.8)}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Route className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {journeyData?.dashboard?.journey_health?.overall_journey_health_score || 72.8}
                  </div>
                  <div className="text-xs text-blue-200">Journey Health</div>
                  <div className="text-xs text-blue-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30 cursor-pointer hover:bg-green-600/30 transition-all duration-200" onClick={() => showDataSource('journeys', 'avg_completion_rate', 'Average Completion Rate', '+8.4%')}>
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    +8.4%
                  </div>
                  <div className="text-xs text-green-200">Velocity Improvement</div>
                  <div className="text-xs text-green-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30 cursor-pointer hover:bg-purple-600/30 transition-all duration-200" onClick={() => showDataSource('journeys', 'avg_steps_to_conversion', 'Average Steps to Conversion', '-12.7%')}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Target className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    -12.7%
                  </div>
                  <div className="text-xs text-purple-200">Drop-off Reduction</div>
                  <div className="text-xs text-purple-300 mt-1 opacity-75">Click for data source</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30 cursor-pointer hover:bg-orange-600/30 transition-all duration-200" onClick={() => showDataSource('journeys', 'optimization_score', 'Journey Optimization Score', '7.9')}>
              <CardContent className="p-4">
                <div className="text-center">
                  <Star className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    7.9
                  </div>
                  <div className="text-xs text-orange-200">Flow Satisfaction</div>
                  <div className="text-xs text-orange-300 mt-1 opacity-75">Click for data source</div>
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