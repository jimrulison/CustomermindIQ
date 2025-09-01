import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  Users, 
  TrendingUp, 
  Target, 
  Zap, 
  ArrowRight,
  DollarSign,
  BarChart3,
  Eye,
  Shield,
  Sword,
  Trophy,
  AlertTriangle,
  CheckCircle2,
  RefreshCw,
  Download,
  Plus,
  Minus,
  TrendingDown,
  Award,
  Star,
  Clock,
  PieChart,
  Activity,
  FileText,
  Search,
  Filter
} from 'lucide-react';

const CompetitiveIntelligenceDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [competitiveData, setCompetitiveData] = useState(null);
  const [competitorAnalysis, setCompetitorAnalysis] = useState(null);
  const [winLossInsights, setWinLossInsights] = useState(null);
  const [pricingAnalysis, setPricingAnalysis] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedTimePeriod, setSelectedTimePeriod] = useState('90_days');

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Load competitive intelligence data
  const loadCompetitiveData = async () => {
    try {
      setLoading(true);
      
      // Load dashboard data
      const dashboardResponse = await fetch(`${backendUrl}/api/competitive-intelligence/dashboard`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (dashboardResponse.ok) {
        const dashboardResult = await dashboardResponse.json();
        setCompetitiveData(dashboardResult.data);
      }

      // Load competitor analysis
      const analysisResponse = await fetch(`${backendUrl}/api/competitive-intelligence/competitor-analysis`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (analysisResponse.ok) {
        const analysisResult = await analysisResponse.json();
        setCompetitorAnalysis(analysisResult.data);
      }

      // Load win/loss insights
      const winLossResponse = await fetch(`${backendUrl}/api/competitive-intelligence/win-loss-insights?time_period=${selectedTimePeriod}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (winLossResponse.ok) {
        const winLossResult = await winLossResponse.json();
        setWinLossInsights(winLossResult.data);
      }

      // Load pricing analysis
      const pricingResponse = await fetch(`${backendUrl}/api/competitive-intelligence/pricing-analysis`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (pricingResponse.ok) {
        const pricingResult = await pricingResponse.json();
        setPricingAnalysis(pricingResult.data);
      }

    } catch (error) {
      console.error('Error loading competitive data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Refresh data
  const refreshData = async () => {
    setRefreshing(true);
    await loadCompetitiveData();
    setTimeout(() => setRefreshing(false), 1000);
  };

  useEffect(() => {
    loadCompetitiveData();
  }, [selectedTimePeriod]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600 mx-auto"></div>
          <p className="text-gray-600 mt-2">Loading Competitive Intelligence...</p>
        </div>
      </div>
    );
  }

  const getThreatColor = (level) => {
    switch (level.toLowerCase()) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getPricingTierColor = (tier) => {
    switch (tier.toLowerCase()) {
      case 'premium': return 'text-purple-600 bg-purple-100';
      case 'competitive': return 'text-blue-600 bg-blue-100';
      case 'value': return 'text-green-600 bg-green-100';
      case 'disruptive': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Sword className="text-red-600" />
            Competitive Customer Intelligence
          </h1>
          <p className="text-gray-600 mt-1">
            AI-powered competitive analysis, win/loss intelligence, and market positioning insights
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={selectedTimePeriod}
            onChange={(e) => setSelectedTimePeriod(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            <option value="30_days">Last 30 Days</option>
            <option value="90_days">Last 90 Days</option>
            <option value="1_year">Last Year</option>
          </select>
          <button
            onClick={refreshData}
            disabled={refreshing}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh Data
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      {competitiveData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Win Rate</p>
                <p className="text-2xl font-bold text-gray-900">
                  {competitiveData.overview.overall_win_rate || 0}%
                </p>
              </div>
              <Trophy className="h-8 w-8 text-red-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-green-600">Above Industry Average</span>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Competitors Tracked</p>
                <p className="text-2xl font-bold text-gray-900">
                  {competitiveData.overview.total_competitors_tracked || 0}
                </p>
              </div>
              <Shield className="h-8 w-8 text-red-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-blue-600">Active Monitoring</span>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Won Deal Value</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${(competitiveData.overview.won_deal_value || 0).toLocaleString()}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-red-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-emerald-600">Revenue Generated</span>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">High Threats</p>
                <p className="text-2xl font-bold text-gray-900">
                  {competitiveData.overview.competitive_threats || 0}
                </p>
              </div>
              <AlertTriangle className="h-8 w-8 text-red-600" />
            </div>
            <div className="mt-2">
              <span className="text-sm text-red-600">Requiring Attention</span>
            </div>
          </div>
        </div>
      )}

      {/* AI Insights Banner */}
      {competitiveData?.ai_insights && (
        <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-xl p-6 border border-red-200">
          <div className="flex items-start gap-4">
            <Brain className="h-6 w-6 text-red-600 mt-1 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Competitive Intelligence</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-red-900 mb-1">Strategic Threats</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    {competitiveData.ai_insights.strategic_threats?.slice(0, 2).map((threat, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <AlertTriangle className="h-3 w-3 text-red-600" />
                        {threat}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-red-900 mb-1">Strategic Opportunities</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    {competitiveData.ai_insights.strategic_opportunities?.slice(0, 2).map((opportunity, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <Target className="h-3 w-3 text-red-600" />
                        {opportunity}
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
            { id: 'overview', name: 'Competitive Overview', icon: BarChart3 },
            { id: 'competitors', name: 'Competitor Analysis', icon: Shield },
            { id: 'win-loss', name: 'Win/Loss Intelligence', icon: Trophy },
            { id: 'pricing', name: 'Pricing Analysis', icon: DollarSign },
            { id: 'intelligence', name: 'Market Intelligence', icon: Eye }
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'border-red-500 text-red-600'
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
      {activeTab === 'overview' && competitiveData && (
        <div className="space-y-6">
          {/* Market Positioning */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Target className="h-5 w-5 text-red-600" />
              Market Positioning & Competitive Landscape
            </h3>
            
            {competitorAnalysis && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Our Position</h4>
                  <p className="text-sm text-blue-800">{competitorAnalysis.competitive_positioning?.our_position}</p>
                  <div className="mt-3">
                    <p className="text-xs text-blue-600 font-medium">Key Differentiators:</p>
                    <ul className="text-xs text-blue-700 mt-1">
                      {competitorAnalysis.competitive_positioning?.key_differentiators?.slice(0, 3).map((diff, index) => (
                        <li key={index} className="flex items-center gap-1">
                          <CheckCircle2 className="h-3 w-3" />
                          {diff}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
                
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg">
                  <h4 className="font-semibold text-orange-900 mb-2">Market Dynamics</h4>
                  <p className="text-sm text-orange-800">{competitorAnalysis.landscape_analysis?.market_dynamics}</p>
                  <div className="mt-3">
                    <div className="flex justify-between text-xs">
                      <span className="text-orange-600">Competitive Intensity:</span>
                      <span className="font-medium text-orange-800">{competitorAnalysis.landscape_analysis?.competitive_intensity}</span>
                    </div>
                    <div className="flex justify-between text-xs mt-1">
                      <span className="text-orange-600">Market Growth:</span>
                      <span className="font-medium text-orange-800">{competitorAnalysis.landscape_analysis?.market_growth_rate}%</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Competitors Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {competitiveData.competitors?.slice(0, 6).map((competitor) => (
                <div key={competitor.competitor_id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-gray-900">{competitor.name}</h4>
                    <span className={`text-xs px-2 py-1 rounded-full ${getThreatColor(competitor.threat_level)}`}>
                      {competitor.threat_level} Threat
                    </span>
                  </div>
                  
                  <div className="space-y-2 mb-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Market Share</span>
                      <span className="font-medium">{competitor.market_share}%</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Pricing Tier</span>
                      <span className={`text-xs px-2 py-1 rounded ${getPricingTierColor(competitor.pricing_tier)}`}>
                        {competitor.pricing_tier}
                      </span>
                    </div>
                  </div>
                  
                  <div className="text-xs text-gray-600">
                    <div className="mb-1">
                      <strong>Strengths:</strong> {competitor.strength_areas?.slice(0, 2).join(', ')}
                    </div>
                    <div>
                      <strong>Weaknesses:</strong> {competitor.weakness_areas?.slice(0, 2).join(', ')}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Win/Loss Summary */}
          {competitiveData.win_loss_analysis && (
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Trophy className="h-5 w-5 text-red-600" />
                Win/Loss Performance Summary
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-green-900 mb-3">Top Win Reasons</h4>
                  <div className="space-y-2">
                    {Object.entries(competitiveData.win_loss_analysis.win_reasons).map(([reason, percentage]) => (
                      <div key={reason} className="flex items-center justify-between">
                        <span className="text-sm text-gray-700">{reason}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-green-500 h-2 rounded-full" 
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium text-green-600">{percentage}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-red-900 mb-3">Top Loss Reasons</h4>
                  <div className="space-y-2">
                    {Object.entries(competitiveData.win_loss_analysis.loss_reasons).map(([reason, percentage]) => (
                      <div key={reason} className="flex items-center justify-between">
                        <span className="text-sm text-gray-700">{reason}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-red-500 h-2 rounded-full" 
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium text-red-600">{percentage}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Competitors Tab */}
      {activeTab === 'competitors' && competitiveData && (
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Shield className="h-5 w-5 text-red-600" />
            Detailed Competitor Analysis
          </h3>
          
          <div className="space-y-6">
            {competitiveData.competitors?.map((competitor) => (
              <div key={competitor.competitor_id} className="border rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <h4 className="text-lg font-semibold text-gray-900">{competitor.name}</h4>
                    <span className={`text-xs px-3 py-1 rounded-full ${getThreatColor(competitor.threat_level)}`}>
                      {competitor.threat_level} Threat
                    </span>
                    <span className={`text-xs px-3 py-1 rounded ${getPricingTierColor(competitor.pricing_tier)}`}>
                      {competitor.pricing_tier}
                    </span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Market Share</p>
                    <p className="text-xl font-bold text-gray-900">{competitor.market_share}%</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <h5 className="font-medium text-gray-900 mb-2">Market Segment</h5>
                    <p className="text-sm text-gray-700">{competitor.market_segment}</p>
                  </div>
                  
                  <div>
                    <h5 className="font-medium text-green-900 mb-2">Strengths</h5>
                    <ul className="text-sm text-gray-700 space-y-1">
                      {competitor.strength_areas?.map((strength, index) => (
                        <li key={index} className="flex items-center gap-2">
                          <CheckCircle2 className="h-3 w-3 text-green-600" />
                          {strength}
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <div>
                    <h5 className="font-medium text-red-900 mb-2">Weaknesses</h5>
                    <ul className="text-sm text-gray-700 space-y-1">
                      {competitor.weakness_areas?.map((weakness, index) => (
                        <li key={index} className="flex items-center gap-2">
                          <Minus className="h-3 w-3 text-red-600" />
                          {weakness}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Win Rate vs This Competitor */}
                {competitiveData.win_loss_analysis?.competitor_win_rates && (
                  <div className="mt-4 pt-4 border-t">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Win Rate vs {competitor.name}</span>
                      <span className="text-lg font-semibold text-blue-600">
                        {competitiveData.win_loss_analysis.competitor_win_rates[`vs ${competitor.name}`] || 'N/A'}%
                      </span>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Win/Loss Tab */}
      {activeTab === 'win-loss' && winLossInsights && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Trophy className="h-5 w-5 text-red-600" />
              Win/Loss Intelligence Analysis
            </h3>
            
            {/* Summary Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-green-600">Win Rate</p>
                    <p className="text-2xl font-bold text-green-900">{winLossInsights.summary_metrics?.win_rate}%</p>
                  </div>
                  <Trophy className="h-6 w-6 text-green-600" />
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-red-50 to-red-100 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-red-600">Loss Rate</p>
                    <p className="text-2xl font-bold text-red-900">{winLossInsights.summary_metrics?.loss_rate}%</p>
                  </div>
                  <TrendingDown className="h-6 w-6 text-red-600" />
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-blue-600">Total Opportunities</p>
                    <p className="text-2xl font-bold text-blue-900">{winLossInsights.summary_metrics?.total_opportunities}</p>
                  </div>
                  <Target className="h-6 w-6 text-blue-600" />
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-yellow-600">No Decision</p>
                    <p className="text-2xl font-bold text-yellow-900">{winLossInsights.summary_metrics?.no_decision_rate}%</p>
                  </div>
                  <Clock className="h-6 w-6 text-yellow-600" />
                </div>
              </div>
            </div>

            {/* Detailed Analysis */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-green-900 mb-3">Win Analysis</h4>
                <div className="space-y-3">
                  {winLossInsights.win_analysis?.top_win_factors?.map((factor, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <span className="text-sm text-gray-700">{factor.factor}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-500 h-2 rounded-full" 
                            style={{ width: `${factor.percentage}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-green-600">{factor.percentage}%</span>
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="mt-4">
                  <h5 className="font-medium text-gray-900 mb-2">Win Patterns</h5>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {winLossInsights.win_analysis?.win_patterns?.map((pattern, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <CheckCircle2 className="h-3 w-3 text-green-600" />
                        {pattern}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold text-red-900 mb-3">Loss Analysis</h4>
                <div className="space-y-3">
                  {winLossInsights.loss_analysis?.top_loss_factors?.map((factor, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <span className="text-sm text-gray-700">{factor.factor}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-red-500 h-2 rounded-full" 
                            style={{ width: `${factor.percentage}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-red-600">{factor.percentage}%</span>
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="mt-4">
                  <h5 className="font-medium text-gray-900 mb-2">Loss Patterns</h5>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {winLossInsights.loss_analysis?.loss_patterns?.map((pattern, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <AlertTriangle className="h-3 w-3 text-red-600" />
                        {pattern}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Segment Analysis */}
          {winLossInsights.segment_analysis && (
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Performance by Segment</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(winLossInsights.segment_analysis).map(([segment, data]) => (
                  <div key={segment} className="border rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-2">{segment}</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Win Rate</span>
                        <span className="text-sm font-medium text-green-600">{data.win_rate}%</span>
                      </div>
                      <div>
                        <span className="text-xs text-gray-600">Primary Challenge:</span>
                        <p className="text-sm text-gray-800">{data.primary_challenge}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Pricing Tab */}
      {activeTab === 'pricing' && pricingAnalysis && (
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <DollarSign className="h-5 w-5 text-red-600" />
            Competitive Pricing Analysis
          </h3>
          
          {/* Pricing Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
              <p className="text-sm text-green-600">Price Advantage</p>
              <p className="text-2xl font-bold text-green-900">{pricingAnalysis.pricing_overview?.avg_price_advantage}%</p>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
              <p className="text-sm text-blue-600">Market Position</p>
              <p className="text-lg font-bold text-blue-900">{pricingAnalysis.pricing_overview?.market_position}</p>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
              <p className="text-sm text-purple-600">Products Analyzed</p>
              <p className="text-2xl font-bold text-purple-900">{pricingAnalysis.pricing_overview?.products_analyzed}</p>
            </div>
            <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg">
              <p className="text-sm text-orange-600">Strategy</p>
              <p className="text-sm font-bold text-orange-900">{pricingAnalysis.pricing_overview?.pricing_strategy}</p>
            </div>
          </div>

          {/* Product Pricing Comparison */}
          <div className="space-y-4">
            {pricingAnalysis.product_pricing?.map((product, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-gray-900">{product.product_name}</h4>
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-bold text-blue-600">${product.our_price}</span>
                    <span className={`text-xs px-2 py-1 rounded ${getPricingTierColor(product.market_position)}`}>
                      {product.market_position}
                    </span>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(product.competitor_prices).map(([competitor, price]) => (
                    <div key={competitor} className="text-center">
                      <p className="text-xs text-gray-600">{competitor}</p>
                      <p className="text-sm font-medium text-gray-900">${price}</p>
                      <p className={`text-xs ${price > product.our_price ? 'text-red-600' : 'text-green-600'}`}>
                        {price > product.our_price ? '+' : ''}
                        {(((price - product.our_price) / product.our_price) * 100).toFixed(1)}%
                      </p>
                    </div>
                  ))}
                </div>
                
                <div className="mt-3 pt-3 border-t">
                  <h5 className="text-sm font-medium text-gray-900 mb-1">Recommendations:</h5>
                  <ul className="text-sm text-gray-600">
                    {product.recommendations?.map((rec, idx) => (
                      <li key={idx} className="flex items-center gap-2">
                        <Target className="h-3 w-3 text-blue-600" />
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Market Intelligence Tab */}
      {activeTab === 'intelligence' && competitiveData && (
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Eye className="h-5 w-5 text-red-600" />
            Market Intelligence Updates
          </h3>
          
          <div className="space-y-4">
            {competitiveData.market_intelligence?.map((intel) => (
              <div key={intel.intelligence_id} className="border-l-4 border-blue-500 bg-blue-50 p-4 rounded-r-lg">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <h4 className="font-semibold text-gray-900">{intel.competitor_name}</h4>
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      {intel.intelligence_type}
                    </span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      intel.impact_level === 'high' ? 'bg-red-100 text-red-800' :
                      intel.impact_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {intel.impact_level} impact
                    </span>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-600">Confidence: {(intel.confidence_score * 100).toFixed(0)}%</p>
                    <p className="text-xs text-gray-500">{intel.source_type}</p>
                  </div>
                </div>
                <p className="text-sm text-gray-700">{intel.summary}</p>
                <p className="text-xs text-gray-500 mt-2">
                  {new Date(intel.date_collected).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button className="flex items-center justify-center gap-3 p-4 bg-gradient-to-r from-red-50 to-red-100 border border-red-200 rounded-xl hover:shadow-md transition-shadow">
          <Plus className="h-5 w-5 text-red-600" />
          <div className="text-left">
            <p className="font-medium text-red-900">Add Competitor</p>
            <p className="text-sm text-red-600">Track new competitor</p>
          </div>
        </button>
        
        <button className="flex items-center justify-center gap-3 p-4 bg-gradient-to-r from-blue-50 to-blue-100 border border-blue-200 rounded-xl hover:shadow-md transition-shadow">
          <FileText className="h-5 w-5 text-blue-600" />
          <div className="text-left">
            <p className="font-medium text-blue-900">Record Win/Loss</p>
            <p className="text-sm text-blue-600">Log opportunity outcome</p>
          </div>
        </button>
        
        <button className="flex items-center justify-center gap-3 p-4 bg-gradient-to-r from-emerald-50 to-emerald-100 border border-emerald-200 rounded-xl hover:shadow-md transition-shadow">
          <Download className="h-5 w-5 text-emerald-600" />
          <div className="text-left">
            <p className="font-medium text-emerald-900">Export Analysis</p>
            <p className="text-sm text-emerald-600">Download competitive report</p>
          </div>
        </button>
      </div>
    </div>
  );
};

export default CompetitiveIntelligenceDashboard;