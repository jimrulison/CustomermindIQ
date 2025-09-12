import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Alert, AlertDescription } from './ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Globe,
  BarChart3,
  Search,
  Zap,
  TrendingUp,
  TrendingDown,
  Monitor,
  Smartphone,
  Shield,
  RefreshCw,
  Plus,
  Eye,
  AlertTriangle,
  CheckCircle,
  Clock,
  Settings,
  Crown,
  Star,
  Target,
  Lightbulb,
  ExternalLink,
  ChevronRight,
  Activity,
  Users,
  DollarSign
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Authentication helper
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
};

const WebsiteIntelligenceHub = () => {
  // State management
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [dashboardData, setDashboardData] = useState(null);
  const [performanceData, setPerformanceData] = useState(null);
  const [seoData, setSeoData] = useState(null);
  const [membershipData, setMembershipData] = useState(null);
  const [updating, setUpdating] = useState(false);
  const [showAddWebsite, setShowAddWebsite] = useState(false);
  const [newWebsite, setNewWebsite] = useState({ domain: '', name: '', type: 'E-commerce' });

  // Load data on component mount
  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    try {
      setLoading(true);
      console.log('Loading Website Intelligence Hub data...');
      
      const axiosConfig = {
        timeout: 30000,
        headers: getAuthHeaders()
      };

      const [dashboardRes, performanceRes, seoRes, membershipRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/website-intelligence/dashboard`, axiosConfig).catch(err => {
          console.error('Website dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/website-intelligence/performance-dashboard`, axiosConfig).catch(err => {
          console.error('Performance dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/website-intelligence/seo-dashboard`, axiosConfig).catch(err => {
          console.error('SEO dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/website-intelligence/membership-status`, axiosConfig).catch(err => {
          console.error('Membership status error:', err);
          return { data: {} };
        })
      ]);

      setDashboardData(dashboardRes.data);
      setPerformanceData(performanceRes.data);
      setSeoData(seoRes.data);
      setMembershipData(membershipRes.data);
      
      console.log('Website Intelligence Hub data loaded successfully');
    } catch (error) {
      console.error('Error loading Website Intelligence data:', error);
      // Set fallback data
      setDashboardData({ dashboard: {} });
      setPerformanceData({ dashboard: {} });
      setSeoData({ dashboard: {} });
      setMembershipData({});
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateAll = async () => {
    try {
      setUpdating(true);
      const response = await axios.post(`${API_BASE_URL}/api/website-intelligence/update-all`, {}, {
        headers: getAuthHeaders()
      });
      console.log('Update initiated:', response.data);
      
      // Show update in progress and refresh data after a delay
      setTimeout(() => {
        loadAllData();
        setUpdating(false);
      }, 3000);
      
    } catch (error) {
      console.error('Error updating websites:', error);
      setUpdating(false);
    }
  };

  const handleAddWebsite = async () => {
    try {
      const websiteData = {
        domain: newWebsite.domain,
        name: newWebsite.name,
        type: newWebsite.type,
        membership_tier: membershipData?.membership_details?.current_tier?.toLowerCase() || 'basic',
        current_websites: dashboardData?.dashboard?.websites_overview?.total_websites || 0
      };

      const response = await axios.post(`${API_BASE_URL}/api/website-intelligence/website/add`, websiteData, {
        headers: getAuthHeaders()
      });
      console.log('Website added:', response.data);
      
      // Reset form and close dialog
      setNewWebsite({ domain: '', name: '', type: 'E-commerce' });
      setShowAddWebsite(false);
      
      // Refresh data
      loadAllData();
      
    } catch (error) {
      console.error('Error adding website:', error);
      if (error.response?.status === 403) {
        alert('Website limit reached for your current plan. Please upgrade to add more websites.');
      } else {
        alert('Error adding website. Please try again.');
      }
    }
  };

  const getTierColor = (tier) => {
    const colors = {
      'Basic': 'bg-blue-500/20 text-blue-400',
      'Professional': 'bg-purple-500/20 text-purple-400',
      'Enterprise': 'bg-gold-500/20 text-gold-400'
    };
    return colors[tier] || 'bg-gray-500/20 text-gray-400';
  };

  const getHealthColor = (score) => {
    if (score >= 90) return 'text-green-400';
    if (score >= 75) return 'text-blue-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getStatusColor = (status) => {
    if (status === 'Good' || status === 'online') return 'text-green-400';
    if (status === 'Needs Improvement') return 'text-yellow-400';
    return 'text-red-400';
  };

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="flex items-center justify-between">
          <div>
            <div className="h-8 bg-slate-700 rounded w-64 mb-2"></div>
            <div className="h-4 bg-slate-700 rounded w-96"></div>
          </div>
          <div className="h-10 bg-slate-700 rounded w-32"></div>
        </div>
        <div className="grid gap-6 md:grid-cols-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="bg-slate-800/50 rounded-lg p-6 h-32"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <Globe className="w-8 h-8 mr-3 text-blue-400" />
            Website Intelligence Hub
          </h1>
          <p className="text-slate-400 mt-2">
            Comprehensive analysis and monitoring for your websites
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge className={getTierColor(membershipData?.membership_details?.current_tier || 'Basic')}>
            <Crown className="w-4 h-4 mr-1" />
            {membershipData?.membership_details?.current_tier || 'Basic'} Plan
          </Badge>
          <Button
            onClick={handleUpdateAll}
            disabled={updating}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${updating ? 'animate-spin' : ''}`} />
            {updating ? 'Updating...' : 'Update All'}
          </Button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid gap-6 md:grid-cols-4">
        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {dashboardData?.dashboard?.websites_overview?.total_websites || 0}
                </div>
                <div className="text-xs text-blue-200">Websites Monitored</div>
              </div>
              <Globe className="h-8 w-8 text-blue-400" />
            </div>
            <div className="mt-2 text-xs text-slate-400">
              {membershipData?.website_limits?.websites_remaining || 0} slots remaining
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {dashboardData?.dashboard?.websites_overview?.overall_health_score?.toFixed(1) || '0.0'}%
                </div>
                <div className="text-xs text-green-200">Overall Health Score</div>
              </div>
              <Activity className="h-8 w-8 text-green-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {seoData?.dashboard?.seo_overview?.total_keywords_tracked || 0}
                </div>
                <div className="text-xs text-purple-200">Keywords Tracked</div>
              </div>
              <Search className="h-8 w-8 text-purple-400" />
            </div>
            <div className="mt-2 text-xs text-slate-400">
              {seoData?.dashboard?.seo_overview?.organic_traffic_change || '+0%'} this month
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {performanceData?.dashboard?.performance_overview?.overall_performance_score?.toFixed(1) || '0.0'}
                </div>
                <div className="text-xs text-orange-200">Performance Score</div>
              </div>
              <Zap className="h-8 w-8 text-orange-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-slate-800/50 p-1 h-auto">
          <TabsTrigger value="overview" className="flex items-center">
            <BarChart3 className="w-4 h-4 mr-2" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="websites" className="flex items-center">
            <Globe className="w-4 h-4 mr-2" />
            My Websites
          </TabsTrigger>
          <TabsTrigger value="performance" className="flex items-center">
            <Monitor className="w-4 h-4 mr-2" />
            Performance
          </TabsTrigger>
          <TabsTrigger value="seo" className="flex items-center">
            <Search className="w-4 h-4 mr-2" />
            SEO Intelligence
          </TabsTrigger>
          <TabsTrigger value="membership" className="flex items-center">
            <Crown className="w-4 h-4 mr-2" />
            Membership
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Analysis Summary */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-blue-400" />
                Analysis Summary
              </CardTitle>
              <CardDescription className="text-slate-400">
                Comprehensive overview of all your websites
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <div className="text-center p-4 bg-slate-700/50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-400">
                    {dashboardData?.dashboard?.analysis_summary?.total_pages_analyzed || 0}
                  </div>
                  <div className="text-sm text-slate-300">Pages Analyzed</div>
                </div>
                <div className="text-center p-4 bg-slate-700/50 rounded-lg">
                  <div className="text-2xl font-bold text-red-400">
                    {dashboardData?.dashboard?.analysis_summary?.total_issues_found || 0}
                  </div>
                  <div className="text-sm text-slate-300">Issues Found</div>
                </div>
                <div className="text-center p-4 bg-slate-700/50 rounded-lg">
                  <div className="text-2xl font-bold text-green-400">
                    {dashboardData?.dashboard?.analysis_summary?.opportunities_identified || 0}
                  </div>
                  <div className="text-sm text-slate-300">Opportunities</div>
                </div>
                <div className="text-center p-4 bg-slate-700/50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-400">
                    {dashboardData?.dashboard?.analysis_summary?.avg_seo_score?.toFixed(1) || '0.0'}%
                  </div>
                  <div className="text-sm text-slate-300">Avg SEO Score</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Key Insights */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Lightbulb className="w-5 h-5 mr-2 text-yellow-400" />
                Key Insights & Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {(dashboardData?.dashboard?.key_insights || []).map((insight, index) => (
                  <Alert key={index} className="bg-blue-500/10 border-blue-500/20">
                    <CheckCircle className="h-4 w-4 text-blue-400" />
                    <AlertDescription className="text-blue-300">
                      {insight}
                    </AlertDescription>
                  </Alert>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Action Items */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Target className="w-5 h-5 mr-2 text-orange-400" />
                Priority Action Items
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {(dashboardData?.dashboard?.action_items || []).map((item, index) => (
                  <div key={index} className="flex items-start space-x-4 p-4 bg-slate-700/30 rounded-lg">
                    <Badge 
                      className={`mt-1 ${
                        item.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                        item.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-green-500/20 text-green-400'
                      }`}
                    >
                      {item.priority?.toUpperCase()}
                    </Badge>
                    <div className="flex-1">
                      <h4 className="font-medium text-white mb-1">{item.action}</h4>
                      <p className="text-sm text-slate-400 mb-2">{item.impact}</p>
                      <div className="flex items-center text-xs text-slate-500">
                        <Clock className="w-3 h-3 mr-1" />
                        Effort: {item.effort}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* My Websites Tab */}
        <TabsContent value="websites" className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white">Your Websites</h2>
            <Dialog open={showAddWebsite} onOpenChange={setShowAddWebsite}>
              <DialogTrigger asChild>
                <Button className="bg-green-600 hover:bg-green-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Website
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-slate-800 border-slate-700">
                <DialogHeader>
                  <DialogTitle className="text-white">Add New Website</DialogTitle>
                  <DialogDescription className="text-slate-400">
                    Add a new website to monitor and analyze
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Domain</label>
                    <Input
                      placeholder="example.com"
                      value={newWebsite.domain}
                      onChange={(e) => setNewWebsite(prev => ({ ...prev, domain: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Website Name</label>
                    <Input
                      placeholder="My Awesome Website"
                      value={newWebsite.name}
                      onChange={(e) => setNewWebsite(prev => ({ ...prev, name: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Website Type</label>
                    <Select 
                      value={newWebsite.type} 
                      onValueChange={(value) => setNewWebsite(prev => ({ ...prev, type: value }))}
                    >
                      <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="E-commerce">E-commerce</SelectItem>
                        <SelectItem value="Blog/Content">Blog/Content</SelectItem>
                        <SelectItem value="Corporate">Corporate</SelectItem>
                        <SelectItem value="Portfolio">Portfolio</SelectItem>
                        <SelectItem value="Landing Page">Landing Page</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="flex justify-end space-x-2">
                  <Button variant="outline" onClick={() => setShowAddWebsite(false)}>
                    Cancel
                  </Button>
                  <Button onClick={handleAddWebsite} className="bg-green-600 hover:bg-green-700">
                    Add Website
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Websites Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {(dashboardData?.dashboard?.user_websites || []).map((website, index) => (
              <Card key={website.website_id || index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:border-slate-600 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-white text-lg">{website.website_name}</CardTitle>
                    <Badge className={`${
                      website.status === 'active' ? 'bg-green-500/20 text-green-400' : 
                      'bg-red-500/20 text-red-400'
                    }`}>
                      {website.status}
                    </Badge>
                  </div>
                  <CardDescription className="text-slate-400 flex items-center">
                    <ExternalLink className="w-4 h-4 mr-1" />
                    {website.domain}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Health Score */}
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-slate-300">Health Score</span>
                        <span className={`text-sm font-medium ${getHealthColor(website.health_score)}`}>
                          {website.health_score?.toFixed(1)}%
                        </span>
                      </div>
                      <Progress value={website.health_score} className="h-2" />
                    </div>

                    {/* Metrics Grid */}
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="text-center p-2 bg-slate-700/30 rounded">
                        <div className="text-blue-400 font-semibold">{website.seo_score?.toFixed(1)}</div>
                        <div className="text-slate-400 text-xs">SEO Score</div>
                      </div>
                      <div className="text-center p-2 bg-slate-700/30 rounded">
                        <div className="text-green-400 font-semibold">{website.performance_score?.toFixed(1)}</div>
                        <div className="text-slate-400 text-xs">Performance</div>
                      </div>
                    </div>

                    {/* Statistics */}
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      <div>
                        <div className="text-slate-300">Monthly Visitors</div>
                        <div className="text-white font-medium">
                          {website.monthly_visitors?.toLocaleString() || 0}
                        </div>
                      </div>
                      <div>
                        <div className="text-slate-300">Conversion Rate</div>
                        <div className="text-white font-medium">{website.conversion_rate || 0}%</div>
                      </div>
                    </div>

                    {/* Issues & Opportunities */}
                    <div className="flex items-center justify-between text-xs">
                      <div className="flex items-center text-red-400">
                        <AlertTriangle className="w-3 h-3 mr-1" />
                        {website.issues_count || 0} Issues
                      </div>
                      <div className="flex items-center text-green-400">
                        <Lightbulb className="w-3 h-3 mr-1" />
                        {website.opportunities_count || 0} Opportunities
                      </div>
                    </div>

                    {/* Connected Services */}
                    <div>
                      <div className="text-xs text-slate-400 mb-1">Connected Services</div>
                      <div className="flex flex-wrap gap-1">
                        {(website.connected_services || []).map((service, idx) => (
                          <Badge key={idx} variant="outline" className="text-xs text-slate-400 border-slate-600">
                            {service}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Last Updated */}
                    <div className="text-xs text-slate-500 flex items-center">
                      <Clock className="w-3 h-3 mr-1" />
                      Last updated: {website.last_analyzed ? new Date(website.last_analyzed).toLocaleDateString() : 'Never'}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Empty State */}
          {(!dashboardData?.dashboard?.user_websites?.length) && (
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardContent className="flex flex-col items-center justify-center py-16">
                <Globe className="w-16 h-16 text-slate-600 mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">No Websites Added</h3>
                <p className="text-slate-400 text-center mb-6 max-w-md">
                  Get started by adding your first website to monitor and analyze its performance, SEO, and technical health.
                </p>
                <Button 
                  onClick={() => setShowAddWebsite(true)}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Your First Website
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {/* Core Web Vitals */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Monitor className="w-5 h-5 mr-2 text-green-400" />
                  Core Web Vitals
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Essential performance metrics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300">Overall Status</span>
                    <Badge className={`${
                      performanceData?.dashboard?.core_web_vitals?.overall_status === 'Good' ?
                      'bg-green-500/20 text-green-400' : 
                      'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {performanceData?.dashboard?.core_web_vitals?.overall_status || 'Unknown'}
                    </Badge>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-300">LCP (Largest Contentful Paint)</span>
                      <span className="text-sm font-medium text-white">
                        {performanceData?.dashboard?.core_web_vitals?.lcp_average || 0}s
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-300">FID (First Input Delay)</span>
                      <span className="text-sm font-medium text-white">
                        {performanceData?.dashboard?.core_web_vitals?.fid_average || 0}ms
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-300">CLS (Cumulative Layout Shift)</span>
                      <span className="text-sm font-medium text-white">
                        {performanceData?.dashboard?.core_web_vitals?.cls_average || 0}
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Performance Score by Website */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <BarChart3 className="w-5 h-5 mr-2 text-blue-400" />
                  Performance by Website
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {(performanceData?.dashboard?.core_web_vitals?.vitals_by_website || []).map((website, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-300">{website.website}</span>
                        <Badge className={getStatusColor(website.overall_status)}>
                          {website.overall_status}
                        </Badge>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="bg-slate-700/30 p-2 rounded">
                          <div className="text-slate-400">Desktop</div>
                          <div className="text-white font-medium">{website.mobile_vs_desktop?.desktop_score || 0}</div>
                        </div>
                        <div className="bg-slate-700/30 p-2 rounded">
                          <div className="text-slate-400">Mobile</div>
                          <div className="text-white font-medium">{website.mobile_vs_desktop?.mobile_score || 0}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Optimization Recommendations */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Lightbulb className="w-5 h-5 mr-2 text-yellow-400" />
                Performance Optimization Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {(performanceData?.dashboard?.optimization_recommendations || []).map((rec, index) => (
                  <div key={index} className="p-4 bg-slate-700/30 rounded-lg">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <Badge className={`mr-2 ${
                            rec.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                            rec.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-green-500/20 text-green-400'
                          }`}>
                            {rec.priority?.toUpperCase()}
                          </Badge>
                          <h4 className="font-medium text-white">{rec.recommendation}</h4>
                        </div>
                        <p className="text-sm text-slate-400 mb-2">{rec.current_metric}</p>
                        <p className="text-sm text-green-300">{rec.potential_impact}</p>
                      </div>
                      <div className="text-right text-xs text-slate-500">
                        <div>{rec.estimated_effort}</div>
                        <div className="text-green-400">{rec.business_impact}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* SEO Intelligence Tab */}
        <TabsContent value="seo" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {/* SEO Overview */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Search className="w-5 h-5 mr-2 text-purple-400" />
                  SEO Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-400 mb-1">
                      {seoData?.dashboard?.seo_overview?.overall_seo_score?.toFixed(1) || '0.0'}
                    </div>
                    <div className="text-sm text-slate-400">Overall SEO Score</div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="text-center p-2 bg-slate-700/30 rounded">
                      <div className="text-green-400 font-semibold">
                        {seoData?.dashboard?.seo_overview?.total_keywords_tracked || 0}
                      </div>
                      <div className="text-slate-400 text-xs">Keywords Tracked</div>
                    </div>
                    <div className="text-center p-2 bg-slate-700/30 rounded">
                      <div className="text-blue-400 font-semibold">
                        {seoData?.dashboard?.seo_overview?.total_backlinks?.toLocaleString() || 0}
                      </div>
                      <div className="text-slate-400 text-xs">Total Backlinks</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Keyword Rankings */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-green-400" />
                  Keyword Rankings
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="grid grid-cols-4 gap-2 text-xs">
                    <div className="text-center p-2 bg-green-500/10 rounded">
                      <div className="text-green-400 font-semibold">
                        {seoData?.dashboard?.keyword_rankings?.ranking_distribution?.top_10 || 0}
                      </div>
                      <div className="text-slate-400">Top 10</div>
                    </div>
                    <div className="text-center p-2 bg-blue-500/10 rounded">
                      <div className="text-blue-400 font-semibold">
                        {seoData?.dashboard?.keyword_rankings?.ranking_distribution?.top_50 || 0}
                      </div>
                      <div className="text-slate-400">Top 50</div>
                    </div>
                    <div className="text-center p-2 bg-yellow-500/10 rounded">
                      <div className="text-yellow-400 font-semibold">
                        {seoData?.dashboard?.keyword_rankings?.ranking_distribution?.top_100 || 0}
                      </div>
                      <div className="text-slate-400">Top 100</div>
                    </div>
                    <div className="text-center p-2 bg-red-500/10 rounded">
                      <div className="text-red-400 font-semibold">
                        {seoData?.dashboard?.keyword_rankings?.ranking_distribution?.beyond_100 || 0}
                      </div>
                      <div className="text-slate-400">Beyond 100</div>
                    </div>
                  </div>
                  
                  <div className="text-center text-sm">
                    <span className="text-slate-400">Organic Traffic: </span>
                    <span className={`font-medium ${
                      seoData?.dashboard?.seo_overview?.organic_traffic_change?.startsWith('+') ? 
                      'text-green-400' : 'text-red-400'
                    }`}>
                      {seoData?.dashboard?.seo_overview?.organic_traffic_change || '+0%'}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* SEO Issues */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2 text-red-400" />
                SEO Issues & Opportunities
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {(seoData?.dashboard?.technical_seo?.technical_issues || []).map((issue, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center mb-1">
                        <Badge className={`mr-2 text-xs ${
                          issue.severity === 'high' ? 'bg-red-500/20 text-red-400' :
                          issue.severity === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-green-500/20 text-green-400'
                        }`}>
                          {issue.severity}
                        </Badge>
                        <span className="text-white font-medium">{issue.issue}</span>
                      </div>
                      <div className="text-sm text-slate-400">
                        {issue.pages_affected} pages affected • {issue.websites?.join(', ')}
                      </div>
                    </div>
                    <Badge className={`${
                      issue.fix_priority === 'High' ? 'bg-red-500/20 text-red-400' :
                      issue.fix_priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-green-500/20 text-green-400'
                    }`}>
                      {issue.fix_priority} Priority
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Membership Tab */}
        <TabsContent value="membership" className="space-y-6">
          {/* Current Plan */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Crown className="w-5 h-5 mr-2 text-gold-400" />
                Current Membership
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <div className="text-2xl font-bold text-white mb-1">
                    {membershipData?.membership_details?.current_tier || 'Basic'} Plan
                  </div>
                  <div className="text-slate-400">
                    {membershipData?.membership_details?.billing_cycle || 'monthly'} billing • 
                    Next billing: {membershipData?.membership_details?.next_billing_date ? 
                      new Date(membershipData.membership_details.next_billing_date).toLocaleDateString() : 'N/A'}
                  </div>
                </div>
                <Badge className={getTierColor(membershipData?.membership_details?.current_tier || 'Basic')}>
                  Active
                </Badge>
              </div>

              {/* Usage Statistics */}
              <div className="grid gap-4 md:grid-cols-3 mb-6">
                <div className="text-center p-4 bg-slate-700/30 rounded-lg">
                  <div className="text-2xl font-bold text-blue-400 mb-1">
                    {membershipData?.website_limits?.websites_used || 0} / {membershipData?.website_limits?.websites_included || 1}
                  </div>
                  <div className="text-sm text-slate-400">Websites Used</div>
                </div>
                <div className="text-center p-4 bg-slate-700/30 rounded-lg">
                  <div className="text-2xl font-bold text-green-400 mb-1">
                    {membershipData?.usage_analytics?.analyses_performed_this_month || 0}
                  </div>
                  <div className="text-sm text-slate-400">Analyses This Month</div>
                </div>
                <div className="text-center p-4 bg-slate-700/30 rounded-lg">
                  <div className="text-2xl font-bold text-purple-400 mb-1">
                    {((membershipData?.usage_analytics?.storage_used_mb || 0) / 1024).toFixed(1)} GB
                  </div>
                  <div className="text-sm text-slate-400">Storage Used</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Plan Comparison */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Star className="w-5 h-5 mr-2 text-yellow-400" />
                Plan Comparison
              </CardTitle>
              <CardDescription className="text-slate-400">
                Choose the perfect plan for your needs
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                {(membershipData?.tier_comparison || []).map((tier, index) => (
                  <div key={index} className={`p-4 rounded-lg border-2 ${
                    tier.is_current ? 'border-blue-500 bg-blue-500/5' : 'border-slate-600 bg-slate-700/30'
                  }`}>
                    <div className="text-center mb-4">
                      <div className="text-xl font-bold text-white mb-1">{tier.tier_name}</div>
                      <div className="text-2xl font-bold text-blue-400 mb-2">
                        ${tier.monthly_price}<span className="text-sm text-slate-400">/mo</span>
                      </div>
                      <div className="text-sm text-slate-400">
                        ${tier.yearly_price}/year (save ${tier.monthly_price * 12 - tier.yearly_price})
                      </div>
                    </div>
                    
                    <div className="space-y-2 mb-4">
                      {tier.features.map((feature, idx) => (
                        <div key={idx} className="flex items-center text-sm text-slate-300">
                          <CheckCircle className="w-4 h-4 text-green-400 mr-2 flex-shrink-0" />
                          {feature}
                        </div>
                      ))}
                    </div>

                    {tier.is_current ? (
                      <Badge className="w-full justify-center bg-blue-500/20 text-blue-400">
                        Current Plan
                      </Badge>
                    ) : (
                      <Button className="w-full bg-blue-600 hover:bg-blue-700">
                        {tier.tier_level > (membershipData?.membership_details?.tier_level || 1) ? 'Upgrade' : 'Downgrade'}
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default WebsiteIntelligenceHub;