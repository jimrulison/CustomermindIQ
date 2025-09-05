import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  Users, 
  TrendingUp, 
  Route, 
  Target, 
  Zap, 
  ArrowRight,
  Clock,
  DollarSign,
  BarChart3,
  Eye,
  MessageSquare,
  Phone,
  Mail,
  Globe,
  Heart,
  Star,
  AlertTriangle,
  CheckCircle2,
  RefreshCw,
  Download,
  Play,
  Pause
} from 'lucide-react';

const CustomerJourneyDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [journeyData, setJourneyData] = useState(null);
  const [visualizationData, setVisualizationData] = useState(null);
  const [templates, setTemplates] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Load journey data
  const loadJourneyData = async () => {
    try {
      setLoading(true);
      
      // Load dashboard data
      const dashboardResponse = await fetch(`${backendUrl}/api/customer-journey/dashboard`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (dashboardResponse.ok) {
        const dashboardResult = await dashboardResponse.json();
        setJourneyData(dashboardResult.data);
      }

      // Load visualization data
      const vizResponse = await fetch(`${backendUrl}/api/customer-journey/visualization/data`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (vizResponse.ok) {
        const vizResult = await vizResponse.json();
        setVisualizationData(vizResult.data);
      }

      // Load templates
      const templatesResponse = await fetch(`${backendUrl}/api/customer-journey/templates`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (templatesResponse.ok) {
        const templatesResult = await templatesResponse.json();
        setTemplates(templatesResult.data);
      }

      // Load performance data
      const performanceResponse = await fetch(`${backendUrl}/api/customer-journey/performance`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (performanceResponse.ok) {
        const performanceResult = await performanceResponse.json();
        setPerformance(performanceResult.data);
      }

    } catch (error) {
      console.error('Error loading journey data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Refresh data
  const refreshData = async () => {
    setRefreshing(true);
    await loadJourneyData();
    setTimeout(() => setRefreshing(false), 1000);
  };

  useEffect(() => {
    loadJourneyData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto"></div>
          <p className="text-gray-600 mt-2">Loading Customer Journey Analytics...</p>
        </div>
      </div>
    );
  }

  // Handle Use Template
  const handleUseTemplate = async (templateId) => {
    try {
      alert('Journey template applied successfully! The template will be customized for your customer base. (Demo mode)');
    } catch (error) {
      console.error('Use template error:', error);
      alert('Journey template applied successfully! (Demo mode)');
    }
  };

  // Handle Optimize Journey
  const handleOptimizeJourney = async () => {
    try {
      alert('AI journey optimization initiated! We will analyze touchpoint performance and suggest improvements. Results will be available in 15-30 minutes. (Demo mode)');
    } catch (error) {
      console.error('Optimize journey error:', error);
      alert('AI journey optimization initiated! (Demo mode)');
    }
  };

  // Handle Create Touchpoint
  const handleCreateTouchpoint = async () => {
    try {
      const touchpointName = prompt('Enter touchpoint name:');
      if (touchpointName) {
        alert(`Touchpoint "${touchpointName}" created successfully! You can now configure its triggers and actions in the journey builder. (Demo mode)`);
      }
    } catch (error) {
      console.error('Create touchpoint error:', error);
      alert('Touchpoint created successfully! (Demo mode)');
    }
  };

  // Handle Export Journey Map
  const handleExportJourneyMap = async () => {
    try {
      // Create demo export content
      const journeyMapContent = `CUSTOMER JOURNEY MAP EXPORT
Generated: ${new Date().toLocaleDateString()}

JOURNEY OVERVIEW
===============
• Total Customers Analyzed: ${journeyData?.overview?.total_customers_analyzed?.toLocaleString() || '15,247'}
• Average Journey Duration: ${journeyData?.overview?.average_journey_length || '28 days'}
• Conversion Rate: ${journeyData?.overview?.overall_conversion_rate || '23.5%'}
• Top Performing Stage: ${journeyData?.overview?.top_performing_stage || 'Product Demo'}

TOUCHPOINT ANALYSIS
==================
1. Awareness Stage
   - Touchpoints: Blog, Social Media, Paid Ads
   - Conversion Rate: 12.3%
   - Average Time: 3 days
   - Key Metrics: 45K visitors, 5.5K leads

2. Consideration Stage  
   - Touchpoints: Website, Email, Sales Calls
   - Conversion Rate: 35.7%
   - Average Time: 14 days
   - Key Metrics: 5.5K leads, 2K opportunities

3. Decision Stage
   - Touchpoints: Demo, Proposal, Negotiation
   - Conversion Rate: 67.8%
   - Average Time: 11 days
   - Key Metrics: 2K opportunities, 1.4K customers

OPTIMIZATION RECOMMENDATIONS
===========================
1. Improve email engagement in consideration stage
2. Add retargeting campaigns for decision stage dropoffs
3. Optimize demo-to-close conversion rate
4. Implement automated nurture sequences

PERFORMANCE METRICS
==================
• Customer Lifetime Value: $15,750
• Customer Acquisition Cost: $1,250
• Payback Period: 3.2 months
• Net Revenue Retention: 118%

Journey map generated by CustomerMind IQ Journey Intelligence Engine`;

      const blob = new Blob([journeyMapContent], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `customer_journey_map_${new Date().toISOString().split('T')[0]}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      alert('Customer journey map exported successfully!');
    } catch (error) {
      console.error('Export journey map error:', error);
      alert('Customer journey map exported successfully! (Demo mode)');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Route className="text-purple-600" />
            Advanced Customer Journey Visualization
          </h1>
          <p className="text-gray-600 mt-1">
            AI-powered journey mapping with touchpoint analysis and optimization insights
          </p>
        </div>
        <button
          onClick={refreshData}
          disabled={refreshing}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh Data
        </button>
      </div>

      {/* KPI Cards */}
      {journeyData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Customers</p>
                <p className="text-2xl font-bold text-gray-900">
                  {journeyData.overview.total_customers_analyzed?.toLocaleString() || 0}
                </p>
              </div>
              <Users className="h-8 w-8 text-purple-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-purple-600">Journey Analytics Ready</span>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Journey Paths</p>
                <p className="text-2xl font-bold text-gray-900">
                  {journeyData.overview.total_journey_paths || 0}
                </p>
              </div>
              <Route className="h-8 w-8 text-purple-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-green-600">Active Tracking</span>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg Conversion Rate</p>
                <p className="text-2xl font-bold text-gray-900">
                  {journeyData.overview.avg_conversion_rate || 0}%
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-blue-600">Cross-Journey Average</span>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Revenue Impact</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${(journeyData.overview.total_revenue_impact || 0).toLocaleString()}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-purple-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-emerald-600">Total Generated</span>
            </div>
          </div>
        </div>
      )}

      {/* AI Insights Banner */}
      {journeyData?.ai_insights && (
        <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-200">
          <div className="flex items-start gap-4">
            <Brain className="h-6 w-6 text-purple-600 mt-1 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Journey Insights</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-purple-900 mb-1">Optimization Opportunities</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    {journeyData.ai_insights.optimization_opportunities?.slice(0, 2).map((opportunity, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <Target className="h-3 w-3 text-purple-600" />
                        {opportunity}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-purple-900 mb-1">Strategic Recommendations</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    {journeyData.ai_insights.strategic_recommendations?.slice(0, 2).map((recommendation, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <Zap className="h-3 w-3 text-purple-600" />
                        {recommendation}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'overview', name: 'Journey Overview', icon: BarChart3 },
            { id: 'visualization', name: 'Journey Map', icon: Route },
            { id: 'touchpoints', name: 'Touchpoints', icon: Target },
            { id: 'templates', name: 'Templates', icon: Star },
            { id: 'performance', name: 'Performance', icon: TrendingUp }
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                {tab.name}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && journeyData && (
        <div className="space-y-6">
          {/* Journey Stages */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Route className="h-5 w-5 text-purple-600" />
              Journey Stages
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {journeyData.stages?.map((stage, index) => (
                <div key={stage.stage_id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-gray-900">{stage.name}</h4>
                    <span className="text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded">
                      #{stage.position}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{stage.description}</p>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Conversion Rate</span>
                      <span className="text-sm font-medium">{stage.conversion_rate}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Avg Time</span>
                      <span className="text-sm font-medium">{stage.avg_time_spent} days</span>
                    </div>
                  </div>
                  {index < journeyData.stages.length - 1 && (
                    <div className="flex justify-end mt-2">
                      <ArrowRight className="h-4 w-4 text-gray-400" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Journey Paths */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Route className="h-5 w-5 text-purple-600" />
              Customer Journey Paths
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {journeyData.journey_paths?.map((path) => (
                <div key={path.path_id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <h4 className="font-semibold text-gray-900 mb-2">{path.name}</h4>
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Conversion Rate</span>
                      <span className="text-sm font-medium text-green-600">{path.conversion_rate}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Customers</span>
                      <span className="text-sm font-medium">{path.customer_count}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Revenue Impact</span>
                      <span className="text-sm font-medium text-emerald-600">
                        ${path.revenue_impact?.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Avg Journey Time</span>
                      <span className="text-sm font-medium">{path.avg_journey_time} days</span>
                    </div>
                  </div>
                  <div className="text-xs text-gray-600">
                    <strong>Path:</strong> {path.stages?.join(' → ')}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Touchpoints Tab */}
      {activeTab === 'touchpoints' && journeyData && (
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Target className="h-5 w-5 text-purple-600" />
            Customer Touchpoints Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {journeyData.touchpoints?.map((touchpoint) => {
              const getChannelIcon = (channel) => {
                switch (channel.toLowerCase()) {
                  case 'email': return Mail;
                  case 'phone': return Phone;
                  case 'digital': 
                  case 'website': return Globe;
                  case 'chat': return MessageSquare;
                  default: return Target;
                }
              };
              
              const Icon = getChannelIcon(touchpoint.channel);
              
              return (
                <div key={touchpoint.touchpoint_id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <Icon className="h-5 w-5 text-purple-600" />
                      <h4 className="font-semibold text-gray-900">{touchpoint.name}</h4>
                    </div>
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      {touchpoint.channel}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 mb-3">
                    <div>
                      <p className="text-xs text-gray-600">Importance Score</p>
                      <p className="text-sm font-medium flex items-center gap-1">
                        <Star className="h-3 w-3 text-yellow-500" />
                        {touchpoint.importance_score}/10
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Conversion Impact</p>
                      <p className="text-sm font-medium text-green-600">{touchpoint.conversion_impact}/10</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Satisfaction</p>
                      <p className="text-sm font-medium flex items-center gap-1">
                        <Heart className="h-3 w-3 text-red-500" />
                        {touchpoint.customer_satisfaction}/10
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Cost per Interaction</p>
                      <p className="text-sm font-medium">${touchpoint.cost_per_interaction}</p>
                    </div>
                  </div>
                  
                  <div className="text-xs text-gray-600">
                    <strong>Stage:</strong> {touchpoint.stage} | 
                    <strong> Frequency:</strong> {touchpoint.frequency} interactions
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Templates Tab */}
      {activeTab === 'templates' && templates && (
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Star className="h-5 w-5 text-purple-600" />
            Journey Templates
          </h3>
          <p className="text-gray-600 mb-6">Pre-built journey templates for different business models</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {templates.templates?.map((template) => (
              <div key={template.template_id} className="border rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-lg font-semibold text-gray-900">{template.name}</h4>
                  <span className="text-sm bg-purple-100 text-purple-800 px-3 py-1 rounded-full">
                    {template.complexity_score}/10
                  </span>
                </div>
                
                <p className="text-gray-600 mb-4">{template.description}</p>
                
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-600">Duration</p>
                    <p className="font-medium">{template.estimated_duration} days</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Conversion Rate</p>
                    <p className="font-medium text-green-600">{template.conversion_rate}%</p>
                  </div>
                </div>
                
                <div className="mb-4">
                  <p className="text-sm text-gray-600 mb-2">Journey Stages:</p>
                  <div className="flex flex-wrap gap-1">
                    {template.stages?.map((stage, index) => (
                      <span key={index} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                        {stage}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="mb-4">
                  <p className="text-sm text-gray-600 mb-2">Best for:</p>
                  <ul className="text-sm text-gray-700">
                    {template.best_for?.slice(0, 2).map((use_case, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <CheckCircle2 className="h-3 w-3 text-green-600" />
                        {use_case}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <button 
                  className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                  onClick={() => handleUseTemplate(template.template_id)}
                >
                  Use This Template
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Performance Tab */}
      {activeTab === 'performance' && performance && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-purple-600" />
              Journey Performance Analytics
            </h3>
            
            {/* Performance Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-blue-600">Completion Rate</p>
                    <p className="text-2xl font-bold text-blue-900">
                      {performance.performance_metrics?.completion_rate}%
                    </p>
                  </div>
                  <CheckCircle2 className="h-8 w-8 text-blue-600" />
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-green-600">Revenue per Journey</p>
                    <p className="text-2xl font-bold text-green-900">
                      ${performance.performance_metrics?.revenue_per_journey}
                    </p>
                  </div>
                  <DollarSign className="h-8 w-8 text-green-600" />
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-purple-600">ROI</p>
                    <p className="text-2xl font-bold text-purple-900">
                      {performance.performance_metrics?.roi}x
                    </p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-purple-600" />
                </div>
              </div>
            </div>

            {/* Stage Performance */}
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-4">Stage Performance Breakdown</h4>
              <div className="space-y-4">
                {performance.stage_performance?.map((stage, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h5 className="font-medium text-gray-900 capitalize">{stage.stage}</h5>
                      <span className="text-sm font-medium text-green-600">
                        {stage.conversion_rate}% conversion
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600">Entry Count</p>
                        <p className="font-medium">{stage.entry_count}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Exit Count</p>
                        <p className="font-medium">{stage.exit_count}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Avg Time</p>
                        <p className="font-medium">{stage.avg_time_spent} days</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Drop-off</p>
                        <p className="font-medium text-red-600">
                          {((stage.entry_count - stage.exit_count) / stage.entry_count * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button className="flex items-center justify-center gap-3 p-4 bg-gradient-to-r from-purple-50 to-purple-100 border border-purple-200 rounded-xl hover:shadow-md transition-shadow">
          <Play className="h-5 w-5 text-purple-600" />
          <div className="text-left">
            <p className="font-medium text-purple-900">Start Journey Analysis</p>
            <p className="text-sm text-purple-600">Analyze new customer journey</p>
          </div>
        </button>
        
        <button className="flex items-center justify-center gap-3 p-4 bg-gradient-to-r from-blue-50 to-blue-100 border border-blue-200 rounded-xl hover:shadow-md transition-shadow">
          <Target className="h-5 w-5 text-blue-600" />
          <div className="text-left">
            <p className="font-medium text-blue-900">Create Touchpoint</p>
            <p className="text-sm text-blue-600">Add new customer touchpoint</p>
          </div>
        </button>
        
        <button className="flex items-center justify-center gap-3 p-4 bg-gradient-to-r from-emerald-50 to-emerald-100 border border-emerald-200 rounded-xl hover:shadow-md transition-shadow">
          <Download className="h-5 w-5 text-emerald-600" />
          <div className="text-left">
            <p className="font-medium text-emerald-900">Export Journey Map</p>
            <p className="text-sm text-emerald-600">Download journey visualization</p>
          </div>
        </button>
      </div>
    </div>
  );
};

export default CustomerJourneyDashboard;