import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Globe, 
  TrendingUp, 
  Zap, 
  Shield, 
  Search,
  BarChart3,
  Settings,
  CheckCircle,
  AlertTriangle,
  Clock,
  Plus,
  RefreshCw,
  Eye,
  Target,
  Crown,
  CreditCard
} from 'lucide-react';

const WebsiteIntelligenceHub = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [websiteData, setWebsiteData] = useState(null);
  const [membershipData, setMembershipData] = useState(null);
  const [performanceData, setPerformanceData] = useState(null);
  const [seoData, setSeoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    loadWebsiteIntelligenceData();
  }, []);

  const loadWebsiteIntelligenceData = async () => {
    try {
      setLoading(true);
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      
      const [website, membership, performance, seo] = await Promise.all([
        fetch(`${backendUrl}/api/website-intelligence/dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/website-intelligence/membership-status`).then(r => r.json()),
        fetch(`${backendUrl}/api/website-intelligence/performance-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/website-intelligence/seo-dashboard`).then(r => r.json())
      ]);
      
      setWebsiteData(website);
      setMembershipData(membership);
      setPerformanceData(performance);
      setSeoData(seo);
    } catch (error) {
      console.error('Error loading Website Intelligence data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateAll = async () => {
    try {
      setUpdating(true);
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      
      const response = await fetch(`${backendUrl}/api/website-intelligence/update-all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        // Simulate update progress
        setTimeout(() => {
          loadWebsiteIntelligenceData();
          setUpdating(false);
        }, 3000);
      }
    } catch (error) {
      console.error('Error updating websites:', error);
      setUpdating(false);
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'websites', name: 'My Websites', icon: Globe },
    { id: 'performance', name: 'Performance', icon: Zap },
    { id: 'seo', name: 'SEO Intelligence', icon: Search },
    { id: 'membership', name: 'Membership', icon: Crown }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Website Intelligence Hub</h1>
          <p className="text-slate-400 mt-2">Comprehensive analysis and monitoring for your websites</p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={handleUpdateAll}
            disabled={updating}
            className={`flex items-center px-4 py-2 rounded-lg font-medium transition-all ${
              updating 
                ? 'bg-blue-600/50 text-blue-300 cursor-not-allowed' 
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${updating ? 'animate-spin' : ''}`} />
            {updating ? 'Updating...' : 'Update All'}
          </button>
          <Badge className="bg-emerald-500/20 text-emerald-400">
            {membershipData?.membership_details?.current_tier || 'Unknown'} Plan
          </Badge>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Icon className="w-4 h-4 mr-2" />
              {tab.name}
            </button>
          );
        })}
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Globe className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {websiteData?.dashboard?.websites_overview?.total_websites || '0'}
                  </div>
                  <div className="text-xs text-blue-200">Websites Analyzed</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {websiteData?.dashboard?.websites_overview?.overall_health_score || '0'}
                  </div>
                  <div className="text-xs text-green-200">Health Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Search className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {seoData?.dashboard?.seo_overview?.overall_seo_score || '0'}
                  </div>
                  <div className="text-xs text-purple-200">SEO Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Zap className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {performanceData?.dashboard?.performance_overview?.overall_performance_score || '0'}
                  </div>
                  <div className="text-xs text-orange-200">Performance</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Key Insights */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Target className="w-5 h-5 mr-2 text-cyan-400" />
                  Business Opportunities
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {websiteData?.dashboard?.business_insights?.optimization_opportunities?.slice(0, 3).map((opportunity, index) => (
                  <Alert key={index} className="bg-blue-500/10 border-blue-500/20">
                    <TrendingUp className="h-4 w-4 text-blue-400" />
                    <AlertDescription className="text-blue-300 text-sm">
                      <div className="font-semibold">{opportunity.opportunity}</div>
                      <div className="text-slate-400 text-xs">
                        Impact: {opportunity.potential_impact} • Revenue: {opportunity.estimated_revenue_impact}
                      </div>
                    </AlertDescription>
                  </Alert>
                ))}
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2 text-orange-400" />
                  Action Items
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {websiteData?.dashboard?.action_items?.map((item, index) => (
                  <div key={index} className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="text-white font-semibold text-sm">{item.action}</div>
                      <div className="text-slate-400 text-xs">{item.impact}</div>
                    </div>
                    <Badge className={`text-xs ml-2 ${
                      item.priority === 'high'
                        ? 'bg-red-500/20 text-red-400'
                        : item.priority === 'medium'
                          ? 'bg-yellow-500/20 text-yellow-400'
                          : 'bg-blue-500/20 text-blue-400'
                    }`}>
                      {item.priority}
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* My Websites Tab */}
      {activeTab === 'websites' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold text-white">Your Websites</h2>
            <button className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all">
              <Plus className="w-4 h-4 mr-2" />
              Add Website
            </button>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {websiteData?.dashboard?.user_websites?.map((website, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:border-slate-600 transition-all">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span className="truncate">{website.domain}</span>
                    <Badge className={`text-xs ${
                      website.status === 'active'
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {website.status}
                    </Badge>
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    {website.website_name} • {website.website_type}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Health Score */}
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-400 mb-1">
                        {website.health_score}/100
                      </div>
                      <div className="text-xs text-slate-400">Overall Health</div>
                    </div>
                    
                    {/* Metrics Grid */}
                    <div className="grid grid-cols-2 gap-3">
                      <div className="text-center">
                        <div className="text-sm font-bold text-blue-400">
                          {website.seo_score}
                        </div>
                        <div className="text-xs text-slate-400">SEO</div>
                      </div>
                      <div className="text-center">
                        <div className="text-sm font-bold text-green-400">
                          {website.performance_score}
                        </div>
                        <div className="text-xs text-slate-400">Performance</div>
                      </div>
                      <div className="text-center">
                        <div className="text-sm font-bold text-purple-400">
                          {website.security_score}
                        </div>
                        <div className="text-xs text-slate-400">Security</div>
                      </div>
                      <div className="text-center">
                        <div className="text-sm font-bold text-orange-400">
                          {website.mobile_score}
                        </div>
                        <div className="text-xs text-slate-400">Mobile</div>
                      </div>
                    </div>
                    
                    {/* Stats */}
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      <div className="text-slate-300">
                        Visitors: {website.monthly_visitors?.toLocaleString()}
                      </div>
                      <div className="text-slate-300">
                        Conversion: {website.conversion_rate}%
                      </div>
                    </div>
                    
                    {/* Issues & Opportunities */}
                    <div className="flex justify-between text-xs">
                      <span className="text-red-400">
                        {website.issues_count} issues
                      </span>
                      <span className="text-green-400">
                        {website.opportunities_count} opportunities
                      </span>
                    </div>
                    
                    {/* Connected Services */}
                    <div className="flex flex-wrap gap-1">
                      {website.connected_services?.slice(0, 2).map((service, serviceIndex) => (
                        <Badge key={serviceIndex} className="bg-blue-500/10 text-blue-300 text-xs">
                          {service}
                        </Badge>
                      ))}
                      {website.connected_services?.length > 2 && (
                        <Badge className="bg-slate-600/50 text-slate-300 text-xs">
                          +{website.connected_services.length - 2}
                        </Badge>
                      )}
                    </div>
                    
                    <div className="text-xs text-slate-400">
                      Last analyzed: {new Date(website.last_analyzed).toLocaleDateString()}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Performance Tab */}
      {activeTab === 'performance' && (
        <div className="space-y-6">
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Zap className="w-5 h-5 mr-2 text-orange-400" />
                Core Web Vitals
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-3">
                {performanceData?.dashboard?.core_web_vitals?.vitals_by_website?.map((website, index) => (
                  <div key={index} className="border border-slate-600 rounded-lg p-4">
                    <h4 className="font-semibold text-white mb-2">{website.website}</h4>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-300">LCP</span>
                        <span className={`font-semibold ${
                          website.lcp <= 2.5 ? 'text-green-400' : website.lcp <= 4.0 ? 'text-yellow-400' : 'text-red-400'
                        }`}>
                          {website.lcp}s
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-slate-300">FID</span>
                        <span className={`font-semibold ${
                          website.fid <= 100 ? 'text-green-400' : website.fid <= 300 ? 'text-yellow-400' : 'text-red-400'
                        }`}>
                          {website.fid}ms
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-slate-300">CLS</span>
                        <span className={`font-semibold ${
                          website.cls <= 0.1 ? 'text-green-400' : website.cls <= 0.25 ? 'text-yellow-400' : 'text-red-400'
                        }`}>
                          {website.cls}
                        </span>
                      </div>
                      <div className="mt-3 pt-3 border-t border-slate-600">
                        <Badge className={`text-xs ${
                          website.overall_status === 'Good'
                            ? 'bg-green-500/20 text-green-400'
                            : website.overall_status === 'Needs Improvement'
                              ? 'bg-yellow-500/20 text-yellow-400'
                              : 'bg-red-500/20 text-red-400'
                        }`}>
                          {website.overall_status}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Performance Recommendations */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Target className="w-5 h-5 mr-2 text-cyan-400" />
                Optimization Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {performanceData?.dashboard?.optimization_recommendations?.map((rec, index) => (
                  <div key={index} className="border-l-4 border-orange-500 pl-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-semibold text-white">{rec.recommendation}</h4>
                        <p className="text-sm text-slate-400">{rec.potential_impact}</p>
                        <div className="flex items-center mt-2 space-x-2">
                          <Badge className={`text-xs ${
                            rec.priority === 'high'
                              ? 'bg-red-500/20 text-red-400'
                              : rec.priority === 'medium'
                                ? 'bg-yellow-500/20 text-yellow-400'
                                : 'bg-blue-500/20 text-blue-400'
                          }`}>
                            {rec.priority}
                          </Badge>
                          <span className="text-xs text-slate-400">
                            {rec.website} • {rec.estimated_effort}
                          </span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-green-400 font-semibold">
                          {rec.business_impact}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* SEO Intelligence Tab */}
      {activeTab === 'seo' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Keyword Rankings</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-4 gap-3 text-center">
                    <div>
                      <div className="text-lg font-bold text-green-400">
                        {seoData?.dashboard?.keyword_rankings?.ranking_distribution?.top_3 || 0}
                      </div>
                      <div className="text-xs text-slate-400">Top 3</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold text-blue-400">
                        {seoData?.dashboard?.keyword_rankings?.ranking_distribution?.top_10 || 0}
                      </div>
                      <div className="text-xs text-slate-400">Top 10</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold text-purple-400">
                        {seoData?.dashboard?.keyword_rankings?.ranking_distribution?.top_50 || 0}
                      </div>
                      <div className="text-xs text-slate-400">Top 50</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold text-orange-400">
                        {seoData?.dashboard?.keyword_rankings?.total_keywords || 0}
                      </div>
                      <div className="text-xs text-slate-400">Total</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    {seoData?.dashboard?.keyword_rankings?.keyword_performance?.slice(0, 3).map((keyword, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <div>
                          <div className="text-white font-medium text-sm">{keyword.keyword}</div>
                          <div className="text-slate-400 text-xs">{keyword.url}</div>
                        </div>
                        <div className="text-right">
                          <div className="flex items-center space-x-2">
                            <span className="text-white font-semibold">#{keyword.current_position}</span>
                            <span className={`text-xs ${
                              keyword.change?.startsWith('+') ? 'text-green-400' : 'text-red-400'
                            }`}>
                              {keyword.change}
                            </span>
                          </div>
                          <div className="text-xs text-slate-400">{keyword.traffic_value}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Organic Traffic</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-400">
                      {seoData?.dashboard?.organic_traffic?.current_month_sessions?.toLocaleString() || '0'}
                    </div>
                    <div className="text-slate-400">Sessions This Month</div>
                    <div className="text-green-400 text-sm font-semibold">
                      {seoData?.dashboard?.organic_traffic?.month_over_month_change || '0%'}
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    {seoData?.dashboard?.organic_traffic?.traffic_by_website?.map((website, index) => (
                      <div key={index} className="flex justify-between items-center">
                        <div>
                          <div className="text-white font-medium text-sm">{website.website}</div>
                          <div className="text-slate-400 text-xs">
                            Bounce: {website.bounce_rate} • Conv: {website.conversion_rate}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-white font-semibold">
                            {website.sessions?.toLocaleString()}
                          </div>
                          <div className={`text-xs ${
                            website.change?.startsWith('+') ? 'text-green-400' : 'text-red-400'
                          }`}>
                            {website.change}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* SEO Issues */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2 text-orange-400" />
                Technical SEO Issues
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {seoData?.dashboard?.technical_seo?.technical_issues?.map((issue, index) => (
                  <div key={index} className="flex justify-between items-center">
                    <div>
                      <div className="text-white font-medium">{issue.issue}</div>
                      <div className="text-slate-400 text-sm">
                        {issue.pages_affected} pages affected • {issue.websites?.join(', ')}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={`text-xs ${
                        issue.severity === 'high'
                          ? 'bg-red-500/20 text-red-400'
                          : issue.severity === 'medium'
                            ? 'bg-yellow-500/20 text-yellow-400'
                            : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {issue.severity}
                      </Badge>
                      <Badge className={`text-xs ${
                        issue.fix_priority === 'High'
                          ? 'bg-red-500/20 text-red-400'
                          : issue.fix_priority === 'Medium'
                            ? 'bg-yellow-500/20 text-yellow-400'
                            : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {issue.fix_priority}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Membership Tab */}
      {activeTab === 'membership' && (
        <div className="space-y-6">
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Crown className="w-5 h-5 mr-2 text-yellow-400" />
                Current Plan
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-2">
                <div>
                  <div className="text-2xl font-bold text-white mb-2">
                    {membershipData?.membership_details?.current_tier || 'Unknown'} Plan
                  </div>
                  <div className="text-slate-400 mb-4">
                    Status: {membershipData?.membership_details?.subscription_status || 'Unknown'}
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Billing Cycle:</span>
                      <span className="text-white">{membershipData?.membership_details?.billing_cycle || 'Unknown'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Next Billing:</span>
                      <span className="text-white">
                        {membershipData?.membership_details?.next_billing_date 
                          ? new Date(membershipData.membership_details.next_billing_date).toLocaleDateString()
                          : 'Unknown'
                        }
                      </span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <div className="text-lg font-semibold text-white mb-2">Website Usage</div>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">Websites Used:</span>
                      <span className="text-white font-semibold">
                        {membershipData?.website_limits?.websites_used || 0}/
                        {membershipData?.website_limits?.total_websites_allowed || 0}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                        style={{ 
                          width: `${((membershipData?.website_limits?.websites_used || 0) / 
                                   (membershipData?.website_limits?.total_websites_allowed || 1)) * 100}%` 
                        }}
                      ></div>
                    </div>
                    <div className="text-sm text-slate-400">
                      {membershipData?.website_limits?.websites_remaining || 0} websites remaining
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Plan Comparison */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Plan Comparison</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-3">
                {membershipData?.tier_comparison?.map((tier, index) => (
                  <div 
                    key={index} 
                    className={`border rounded-lg p-4 ${
                      tier.is_current 
                        ? 'border-blue-500 bg-blue-500/10' 
                        : 'border-slate-600 hover:border-slate-500'
                    } transition-all`}
                  >
                    <div className="text-center mb-4">
                      <h3 className="text-lg font-bold text-white">{tier.tier_name}</h3>
                      {tier.is_current && (
                        <Badge className="bg-blue-500/20 text-blue-400 mt-1">Current Plan</Badge>
                      )}
                    </div>
                    
                    <div className="text-center mb-4">
                      <div className="text-2xl font-bold text-white">
                        ${tier.monthly_price}
                      </div>
                      <div className="text-slate-400">per month</div>
                      <div className="text-sm text-green-400">
                        ${tier.yearly_price}/year (save ${tier.monthly_price * 12 - tier.yearly_price})
                      </div>
                    </div>
                    
                    <div className="space-y-2 mb-4">
                      <div className="text-center">
                        <span className="text-lg font-semibold text-blue-400">
                          {tier.websites_included}
                        </span>
                        <span className="text-slate-400"> websites</span>
                      </div>
                    </div>
                    
                    <div className="space-y-1 text-sm">
                      {tier.features?.slice(0, 3).map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center text-slate-300">
                          <CheckCircle className="w-3 h-3 text-green-400 mr-2 flex-shrink-0" />
                          {feature}
                        </div>
                      ))}
                      {tier.features?.length > 3 && (
                        <div className="text-slate-400 text-xs">
                          +{tier.features.length - 3} more features
                        </div>
                      )}
                    </div>
                    
                    {!tier.is_current && (
                      <button className="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all">
                        Upgrade to {tier.tier_name}
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Usage Analytics */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-purple-400" />
                Usage Analytics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-2">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Analyses This Month:</span>
                    <span className="text-white font-semibold">
                      {membershipData?.usage_analytics?.analyses_performed_this_month || 0}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Updates Triggered:</span>
                    <span className="text-white font-semibold">
                      {membershipData?.usage_analytics?.updates_triggered || 0}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Reports Generated:</span>
                    <span className="text-white font-semibold">
                      {membershipData?.usage_analytics?.reports_generated || 0}
                    </span>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-slate-300">API Calls:</span>
                      <span className="text-white font-semibold">
                        {membershipData?.usage_analytics?.api_calls_used || 0}/
                        {membershipData?.usage_analytics?.api_calls_limit || 0}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
                        style={{ 
                          width: `${((membershipData?.usage_analytics?.api_calls_used || 0) / 
                                   (membershipData?.usage_analytics?.api_calls_limit || 1)) * 100}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-slate-300">Storage:</span>
                      <span className="text-white font-semibold">
                        {membershipData?.usage_analytics?.storage_used_mb || 0}MB/
                        {membershipData?.usage_analytics?.storage_limit_mb || 0}MB
                      </span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                        style={{ 
                          width: `${((membershipData?.usage_analytics?.storage_used_mb || 0) / 
                                   (membershipData?.usage_analytics?.storage_limit_mb || 1)) * 100}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default WebsiteIntelligenceHub;