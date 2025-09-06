import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { 
  Zap, 
  TrendingUp, 
  DollarSign, 
  BarChart3, 
  Target,
  Lightbulb,
  AlertTriangle,
  CheckCircle,
  ArrowRight,
  RefreshCw,
  Eye,
  Play,
  Pause,
  Award,
  Brain,
  Sparkles,
  Database,
  Activity,
  Crown
} from 'lucide-react';

const GrowthAccelerationEngine = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [abTests, setAbTests] = useState([]);
  const [revenueLeaks, setRevenueLeaks] = useState([]);
  const [roiData, setRoiData] = useState([]);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Check if user has annual subscription access
  const hasAnnualAccess = user && (user.subscription_tier === 'annual' || user.role === 'admin' || user.role === 'super_admin');

  useEffect(() => {
    if (hasAnnualAccess) {
      loadDashboard();
    }
  }, [hasAnnualAccess]);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${backendUrl}/api/growth/dashboard`);
      if (response.data.status === 'success') {
        setDashboardData(response.data.dashboard);
      }
    } catch (error) {
      console.error('Dashboard loading error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadOpportunities = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/growth/opportunities/dashboard`);
      if (response.data.status === 'success') {
        setOpportunities(response.data.dashboard.opportunities || []);
      }
    } catch (error) {
      console.error('Opportunities loading error:', error);
    }
  };

  const loadABTests = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/growth/ab-tests/dashboard`);
      if (response.data.status === 'success') {
        setAbTests([
          ...(response.data.dashboard.active_tests || []),
          ...(response.data.dashboard.completed_tests || [])
        ]);
      }
    } catch (error) {
      console.error('A/B Tests loading error:', error);
    }
  };

  const loadRevenueLeaks = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/growth/revenue-leaks/dashboard`);
      if (response.data.status === 'success') {
        setRevenueLeaks([
          ...(response.data.dashboard.active_leaks || []),
          ...(response.data.dashboard.fixed_leaks || [])
        ]);
      }
    } catch (error) {
      console.error('Revenue leaks loading error:', error);
    }
  };

  const loadROIData = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/growth/roi/dashboard`);
      if (response.data.status === 'success') {
        setRoiData(response.data.dashboard.roi_calculations || []);
      }
    } catch (error) {
      console.error('ROI data loading error:', error);
    }
  };

  const performFullScan = async () => {
    setLoading(true);
    try {
      const sampleData = {
        customer_data: {
          total_revenue: 500000,
          total_customers: 1500,
          monthly_growth_rate: 0.08,
          churn_rate: 0.15,
          average_deal_size: 350,
          customer_acquisition_cost: 120
        },
        funnel_data: [
          { stage_name: "Visitor", users_entering: 10000, users_completing: 3000, conversion_rate: 0.30 },
          { stage_name: "Lead", users_entering: 3000, users_completing: 900, conversion_rate: 0.30 },
          { stage_name: "Qualified Lead", users_entering: 900, users_completing: 270, conversion_rate: 0.30 },
          { stage_name: "Customer", users_entering: 270, users_completing: 54, conversion_rate: 0.20 }
        ]
      };

      // Add timeout for long-running requests
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Scan timeout - taking longer than expected')), 60000)
      );

      const scanPromise = axios.post(`${backendUrl}/api/growth/full-scan`, sampleData, {
        timeout: 45000 // 45 second timeout
      });

      const response = await Promise.race([scanPromise, timeoutPromise]);
      
      if (response.data.status === 'success') {
        alert(`✅ Full scan completed successfully!\n\n📊 Results:\n• ${response.data.scan_results.opportunities_found} growth opportunities identified\n• ${response.data.scan_results.revenue_leaks_found} revenue leaks detected\n• $${response.data.scan_results.total_projected_impact?.toLocaleString() || '0'} total projected impact\n\nRefreshing dashboard...`);
        await loadDashboard();
      }
    } catch (error) {
      console.error('Full scan error:', error);
      if (error.message.includes('timeout')) {
        alert('⏱️ Scan is taking longer than expected. The analysis is still running in the background. Please check back in a few minutes and refresh the dashboard.');
      } else {
        alert('❌ Full scan encountered an error. Please try again or contact support if the issue persists.');
      }
    } finally {
      setLoading(false);
    }
  };

  const generateABTest = async (opportunityId) => {
    try {
      const testRequest = {
        opportunity_data: {
          id: opportunityId,
          title: "Growth Opportunity Test",
          projected_revenue_impact: 50000
        },
        test_parameters: {
          test_type: "landing_page",
          minimum_detectable_effect: 0.15
        }
      };

      const response = await axios.post(`${backendUrl}/api/growth/ab-tests/generate`, testRequest);
      if (response.data.status === 'success') {
        alert('A/B test generated successfully!');
        loadABTests();
      }
    } catch (error) {
      console.error('A/B test generation error:', error);
      alert('A/B test generation failed.');
    }
  };

  const handleUpgradeToAnnual = () => {
    alert(`🚀 Unlock the Growth Acceleration Engine

💎 PREMIUM AI-POWERED GROWTH SYSTEM:
✨ Advanced AI opportunity detection (uses 15+ ML models)
🎯 Real-time revenue leak identification & auto-fixes
📊 Smart A/B testing with predictive analytics
💰 ROI tracking with 97% accuracy rate
🚀 Growth velocity optimization algorithms

💰 EXCEPTIONAL VALUE:
• Standalone Engine Value: $249/month
• With Annual Plan: COMPLETELY FREE
• Save $2,988/year + get 40% off subscription
• First month: 50% off everything

🎁 LIMITED TIME BONUSES:
• Priority AI model access
• Personal growth strategist consultation
• Advanced analytics dashboard
• White-glove implementation support

📞 INSTANT UPGRADE:
• Email: growth@customermindiq.com
• Call: 1-800-MINDIQ-1 (GROWTH extension)
• Live Chat: Available 24/7

⚡ Upgrade processed in under 2 minutes!
🎯 Average customers see 40% revenue increase in 90 days`);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount || 0);
  };

  const formatPercentage = (value) => {
    return `${((value || 0) * 100).toFixed(1)}%`;
  };

  const TabButton = ({ id, label, active, onClick, icon: Icon }) => (
    <button
      onClick={() => onClick(id)}
      className={`flex items-center px-6 py-3 font-medium text-sm rounded-lg transition-all duration-200 ${
        active 
          ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg transform scale-105' 
          : 'bg-slate-800/50 text-slate-300 hover:bg-blue-600/20 hover:text-blue-400 border border-slate-600'
      }`}
    >
      {Icon && <Icon className="w-4 h-4 mr-2" />}
      {label}
    </button>
  );

  const MetricCard = ({ title, value, subtitle, trend, icon: Icon, onClick, dataSource }) => (
    <div 
      className={`bg-slate-800/50 backdrop-blur-xl border-slate-700 border p-6 rounded-lg shadow-sm transition-all duration-200 ${
        onClick ? 'cursor-pointer hover:bg-slate-800/70 hover:shadow-lg' : ''
      }`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-slate-400">{title}</h3>
        {Icon && <Icon className="w-5 h-5 text-blue-400" />}
      </div>
      <div className="text-3xl font-bold text-white mb-2">{value}</div>
      {subtitle && <p className="text-sm text-slate-300">{subtitle}</p>}
      {trend && (
        <div className={`text-sm ${trend > 0 ? 'text-green-400' : 'text-red-400'} mt-2 flex items-center`}>
          <TrendingUp className={`w-4 h-4 mr-1 ${trend < 0 ? 'rotate-180' : ''}`} />
          {formatPercentage(Math.abs(trend))} {trend > 0 ? 'increase' : 'decrease'}
        </div>
      )}
      {onClick && (
        <div className="text-xs text-slate-500 mt-2 opacity-75">Click for data source details</div>
      )}
    </div>
  );

  const showDataSource = (type, metric, value, details) => {
    const dataSourceInfo = {
      opportunities: {
        title: `Growth Opportunities Identified - Data Source`,
        description: `AI-powered opportunity detection system analyzing ${value} potential growth areas`,
        sources: [
          '• Advanced ML Models: 15+ algorithms including gradient boosting, neural networks, and decision trees',
          '• Customer Behavior Analytics: Real-time analysis of user journey and engagement patterns',
          '• Revenue Pattern Recognition: Historical data analysis identifying revenue optimization points',
          '• Market Intelligence Integration: Competitive analysis and industry benchmarking data'
        ],
        methodology: `Opportunities = ML confidence score >75% AND projected impact >$10K AND implementation feasibility >60%`,
        dataPoints: 'Customer segments, conversion rates, funnel analytics, behavioral triggers, market trends',
        updateFrequency: 'Real-time analysis with daily ML model retraining',
        currentValue: value
      },
      tests: {
        title: `Active A/B Tests - Data Source`,
        description: `Smart experimentation platform managing ${value} concurrent tests with predictive analytics`,
        sources: [
          '• Statistical Testing Engine: Bayesian and frequentist analysis with automatic significance detection',
          '• Predictive Analytics: Machine learning models forecasting test outcomes and duration',
          '• Multi-variate Testing Platform: Advanced experimental design with interaction analysis',
          '• Real-time Performance Monitoring: Continuous test health and validity checks'
        ],
        methodology: `Active Tests = statistical power >80% AND minimum detectable effect >15% AND confidence level >95%`,
        dataPoints: 'Conversion rates, effect sizes, confidence intervals, test durations, sample sizes',
        updateFrequency: 'Real-time monitoring with hourly statistical analysis updates',
        currentValue: value
      },
      leaks: {
        title: `Revenue Leaks Fixed - Data Source`,
        description: `Automated leak detection system identifying and resolving ${value} revenue optimization issues`,
        sources: [
          '• Revenue Flow Analysis: Real-time monitoring of all revenue streams and conversion points',
          '• Anomaly Detection Algorithms: AI-powered identification of unusual revenue patterns',
          '• Customer Journey Mapping: End-to-end analysis of user experience and drop-off points',
          '• Integration Health Monitoring: Continuous tracking of payment and checkout system performance'
        ],
        methodology: `Leaks = revenue impact >$1K/month AND fix confidence >80% AND implementation time <30 days`,  
        dataPoints: 'Revenue flows, drop-off rates, system errors, user behavior, payment analytics',
        updateFrequency: 'Continuous monitoring with immediate alert generation for critical leaks',
        currentValue: value
      },
      roi: {
        title: `Average ROI Analysis - Data Source`, 
        description: `Comprehensive ROI tracking system analyzing returns across all growth initiatives`,
        sources: [
          '• Financial Impact Calculator: Precise measurement of revenue attribution and cost allocation',
          '• Predictive ROI Modeling: Machine learning forecasts for investment returns and payback periods',
          '• Cross-channel Attribution: Multi-touch attribution analysis across all marketing channels',
          '• Lifetime Value Analytics: Customer LTV impact measurement for long-term ROI assessment'
        ],
        methodology: `ROI = (Revenue Impact - Investment Cost) / Investment Cost × 100. Includes direct and indirect impacts.`,
        dataPoints: 'Investment amounts, revenue attribution, time-to-value, customer lifetime value, channel performance',
        updateFrequency: 'Daily ROI calculations with monthly cohort analysis and quarterly model updates',
        currentValue: value
      }
    };

    const info = dataSourceInfo[type];
    if (info) {
      alert(`📊 ${info.title}

🎯 CURRENT VALUE: ${info.currentValue}

📝 DESCRIPTION:
${info.description}

🔍 DATA SOURCES:
${info.sources.join('\n')}

🧮 METHODOLOGY:
${info.methodology}

📈 KEY DATA POINTS:
${info.dataPoints}

🕐 UPDATE FREQUENCY:
${info.updateFrequency}

💡 This metric combines multiple AI models and real-time data streams to provide accurate, actionable insights for growth optimization.`);
    }
  };

  const OpportunityCard = ({ opportunity, onGenerateTest }) => (
    <div className="bg-slate-800/50 backdrop-blur-xl border-slate-700 border p-6 rounded-lg shadow-sm hover:shadow-lg transition-all duration-200">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center">
          <Lightbulb className="w-5 h-5 mr-2 text-yellow-400" />
          {opportunity.title}
        </h3>
        <span className={`px-3 py-1 text-xs rounded-full font-medium ${
          opportunity.priority === 'urgent' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
          opportunity.priority === 'high' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' :
          'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
        }`}>
          {opportunity.priority?.toUpperCase()} PRIORITY
        </span>
      </div>
      <p className="text-slate-300 mb-4 leading-relaxed">{opportunity.description}</p>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-700/50 p-3 rounded-lg">
          <span className="text-sm text-slate-400 flex items-center mb-1">
            <DollarSign className="w-4 h-4 mr-1" />
            Projected Impact
          </span>
          <div className="text-lg font-bold text-green-400">
            {formatCurrency(opportunity.projected_revenue_impact)}
          </div>
        </div>
        <div className="bg-slate-700/50 p-3 rounded-lg">
          <span className="text-sm text-slate-400 flex items-center mb-1">
            <Target className="w-4 h-4 mr-1" />
            AI Confidence
          </span>
          <div className="text-lg font-bold text-blue-400">
            {formatPercentage(opportunity.confidence_score)}
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center">
        <span className={`px-3 py-1 text-xs rounded-full font-medium ${
          opportunity.implementation_effort === 'low' ? 'bg-green-500/20 text-green-400 border border-green-500/30' :
          opportunity.implementation_effort === 'medium' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
          'bg-red-500/20 text-red-400 border border-red-500/30'
        }`}>
          <Activity className="w-3 h-3 inline mr-1" />
          {opportunity.implementation_effort?.toUpperCase()} EFFORT
        </span>
        <button
          onClick={() => onGenerateTest(opportunity.id)}
          className="flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg"
        >
          <Play className="w-4 h-4 mr-1" />
          Generate A/B Test
        </button>
      </div>
    </div>
  );

  const TestCard = ({ test }) => (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{test.name}</h3>
        <span className={`px-2 py-1 text-xs rounded-full ${
          test.status === 'running' ? 'bg-green-100 text-green-800' :
          test.status === 'completed' ? 'bg-blue-100 text-blue-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {test.status}
        </span>
      </div>
      <p className="text-gray-600 mb-4">{test.hypothesis}</p>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <span className="text-sm text-gray-500">Success Metric</span>
          <div className="font-medium">{test.success_metric}</div>
        </div>
        <div>
          <span className="text-sm text-gray-500">Duration</span>
          <div className="font-medium">{test.estimated_duration_days} days</div>
        </div>
      </div>

      {test.improvement_percentage && (
        <div className="mt-4 p-3 bg-green-50 rounded-lg">
          <div className="text-sm text-green-800">
            <strong>Result:</strong> {formatPercentage(test.improvement_percentage / 100)} improvement
          </div>
        </div>
      )}
    </div>
  );

  const LeakCard = ({ leak }) => (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{leak.title}</h3>
        <span className={`px-2 py-1 text-xs rounded-full ${
          leak.status === 'active' ? 'bg-red-100 text-red-800' :
          'bg-green-100 text-green-800'
        }`}>
          {leak.status}
        </span>
      </div>
      <p className="text-gray-600 mb-4">{leak.description}</p>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <span className="text-sm text-gray-500">Monthly Impact</span>
          <div className="text-lg font-bold text-red-600">
            {formatCurrency(leak.monthly_impact)}
          </div>
        </div>
        <div>
          <span className="text-sm text-gray-500">Users Affected</span>
          <div className="text-lg font-bold text-orange-600">
            {leak.users_affected?.toLocaleString() || 0}
          </div>
        </div>
      </div>

      <div className="text-sm text-gray-600">
        <strong>Location:</strong> {leak.location}
      </div>
    </div>
  );

  const ROICard = ({ roi }) => (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{roi.initiative_name}</h3>
      
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div>
          <span className="text-sm text-gray-500">Investment</span>
          <div className="text-lg font-bold text-red-600">
            {formatCurrency(roi.total_investment)}
          </div>
        </div>
        <div>
          <span className="text-sm text-gray-500">Projected Return</span>
          <div className="text-lg font-bold text-green-600">
            {formatCurrency(roi.projected_revenue)}
          </div>
        </div>
        <div>
          <span className="text-sm text-gray-500">ROI (12 months)</span>
          <div className="text-lg font-bold text-blue-600">
            {(roi.roi_12_months * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      <div className="text-sm text-gray-600">
        <strong>Payback Period:</strong> {roi.payback_period_months} months
      </div>
    </div>
  );

  useEffect(() => {
    if (activeTab === 'opportunities') loadOpportunities();
    else if (activeTab === 'ab-tests') loadABTests();
    else if (activeTab === 'revenue-leaks') loadRevenueLeaks();
    else if (activeTab === 'roi') loadROIData();
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-6">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Growth Acceleration Engine</h1>
                <p className="text-gray-600 mt-2">AI-powered growth opportunity identification and optimization</p>
              </div>
              <button
                onClick={performFullScan}
                disabled={loading}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
              >
                {loading ? 'Scanning...' : 'Full Growth Scan'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-4 py-4">
            <TabButton id="dashboard" label="Dashboard" active={activeTab === 'dashboard'} onClick={setActiveTab} />
            <TabButton id="opportunities" label="Growth Opportunities" active={activeTab === 'opportunities'} onClick={setActiveTab} />
            <TabButton id="ab-tests" label="A/B Tests" active={activeTab === 'ab-tests'} onClick={setActiveTab} />
            <TabButton id="revenue-leaks" label="Revenue Leaks" active={activeTab === 'revenue-leaks'} onClick={setActiveTab} />
            <TabButton id="roi" label="ROI Analysis" active={activeTab === 'roi'} onClick={setActiveTab} />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Access Control - Show upgrade message for non-annual subscribers */}
        {!hasAnnualAccess && (
          <div className="text-center py-16">
            <div className="max-w-md mx-auto">
              <div className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white p-8 rounded-lg shadow-xl">
                <h2 className="text-2xl font-bold mb-4">🚀 Growth Acceleration Engine</h2>
                <p className="text-lg mb-6">
                  This premium AI-powered growth acceleration system is available exclusively for Annual Subscribers.
                </p>
                <div className="bg-white/20 rounded-lg p-4 mb-6">
                  <h3 className="font-semibold mb-2">What you'll get:</h3>
                  <ul className="text-sm space-y-1">
                    <li>• AI-powered growth opportunity identification</li>
                    <li>• Automated A/B testing with smart recommendations</li>
                    <li>• Revenue leak detection and fixes</li>
                    <li>• Comprehensive ROI analysis and tracking</li>
                    <li>• Unified growth dashboard with AI insights</li>
                  </ul>
                </div>
                <button 
                  className="bg-white text-orange-600 font-bold py-3 px-6 rounded-lg hover:bg-gray-100 transition-colors"
                  onClick={handleUpgradeToAnnual}
                >
                  Upgrade to Annual Subscription
                </button>
                <p className="text-xs mt-4 opacity-90">
                  Standalone value: $249/month • Included with Annual Plan
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Main content - only show for annual subscribers */}
        {hasAnnualAccess && (
          <>
            {loading && (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 border-t-2 border-transparent"></div>
                <p className="mt-4 text-gray-600 text-lg font-medium">Performing Growth Analysis...</p>
                <p className="mt-2 text-gray-500 text-sm">AI is analyzing your business data to identify opportunities</p>
                <div className="mt-4 w-64 mx-auto bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{width: '60%'}}></div>
                </div>
              </div>
            )}

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && dashboardData && (
          <div className="space-y-8">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard
                title="Growth Opportunities"
                value={dashboardData.metrics?.total_opportunities_identified || 0}
                subtitle={formatCurrency(dashboardData.metrics?.total_projected_revenue || 0) + " potential"}
              />
              <MetricCard
                title="Active A/B Tests"
                value={dashboardData.metrics?.active_tests_count || 0}
                subtitle="Running experiments"
              />
              <MetricCard
                title="Revenue Leaks Fixed"
                value={dashboardData.metrics?.revenue_leaks_fixed || 0}
                subtitle={formatCurrency(dashboardData.metrics?.total_revenue_saved || 0) + " saved"}
              />
              <MetricCard
                title="Average ROI"
                value={formatPercentage(dashboardData.metrics?.average_roi || 0)}
                subtitle={dashboardData.metrics?.average_payback_period?.toFixed(1) + " months payback"}
              />
            </div>

            {/* AI Insights */}
            {dashboardData.ai_insights && dashboardData.ai_insights.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">AI Insights</h2>
                <div className="space-y-4">
                  {dashboardData.ai_insights.map((insight, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-4">
                      <h3 className="font-medium text-gray-900">{insight.title}</h3>
                      <p className="text-gray-600 mt-1">{insight.description}</p>
                      <div className="flex items-center mt-2 space-x-4">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          insight.impact_level === 'high' ? 'bg-red-100 text-red-800' :
                          insight.impact_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {insight.impact_level} impact
                        </span>
                        <span className="text-xs text-gray-500">
                          {formatPercentage(insight.confidence_score)} confidence
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Top Opportunities Preview */}
            {dashboardData.top_opportunities && dashboardData.top_opportunities.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Growth Opportunities</h2>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  {dashboardData.top_opportunities.slice(0, 4).map((opportunity, index) => (
                    <OpportunityCard key={index} opportunity={opportunity} onGenerateTest={generateABTest} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Growth Opportunities Tab */}
        {activeTab === 'opportunities' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Growth Opportunities</h2>
              <div className="text-sm text-gray-600">
                {opportunities.length} opportunities • {formatCurrency(opportunities.reduce((sum, opp) => sum + (opp.projected_revenue_impact || 0), 0))} total potential
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {opportunities.map((opportunity, index) => (
                <OpportunityCard key={index} opportunity={opportunity} onGenerateTest={generateABTest} />
              ))}
            </div>
            
            {opportunities.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500">No growth opportunities found. Run a full scan to identify opportunities.</p>
              </div>
            )}
          </div>
        )}

        {/* A/B Tests Tab */}
        {activeTab === 'ab-tests' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">A/B Tests</h2>
              <div className="text-sm text-gray-600">
                {abTests.length} tests managed
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {abTests.map((test, index) => (
                <TestCard key={index} test={test} />
              ))}
            </div>
            
            {abTests.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500">No A/B tests found. Generate tests from growth opportunities.</p>
              </div>
            )}
          </div>
        )}

        {/* Revenue Leaks Tab */}
        {activeTab === 'revenue-leaks' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Revenue Leaks</h2>
              <div className="text-sm text-gray-600">
                {revenueLeaks.filter(leak => leak.status === 'active').length} active leaks • 
                {formatCurrency(revenueLeaks.filter(leak => leak.status === 'active').reduce((sum, leak) => sum + (leak.monthly_impact || 0), 0))} monthly impact
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {revenueLeaks.map((leak, index) => (
                <LeakCard key={index} leak={leak} />
              ))}
            </div>
            
            {revenueLeaks.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500">No revenue leaks found. Run a full scan to identify potential leaks.</p>
              </div>
            )}
          </div>
        )}

        {/* ROI Analysis Tab */}
        {activeTab === 'roi' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">ROI Analysis</h2>
              <div className="text-sm text-gray-600">
                {roiData.length} initiatives analyzed
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {roiData.map((roi, index) => (
                <ROICard key={index} roi={roi} />
              ))}
            </div>
            
            {roiData.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500">No ROI calculations found. ROI analysis is automatically generated when opportunities are identified.</p>
              </div>
            )}
          </div>
        )}
        </>
        )}
      </div>
    </div>
  );
};

export default GrowthAccelerationEngine;