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
  DollarSign,
  Trash2
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
  
  // Website details modal state
  const [showWebsiteDetails, setShowWebsiteDetails] = useState(false);
  const [selectedWebsite, setSelectedWebsite] = useState(null);
  const [detailView, setDetailView] = useState('overview'); // 'overview', 'issues', 'opportunities', 'seo', 'performance'
  
  // Track locally deleted websites (until backend delete endpoint is implemented)
  const [deletedWebsites, setDeletedWebsites] = useState([]);

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

      // Filter out locally deleted websites from the backend data
      const filteredDashboardData = {
        ...dashboardRes.data,
        dashboard: {
          ...dashboardRes.data.dashboard,
          user_websites: (dashboardRes.data.dashboard?.user_websites || []).filter(website => {
            return !deletedWebsites.some(deleted => 
              deleted.website_id === website.website_id ||
              deleted.domain === website.domain ||
              deleted.website_name === website.website_name
            );
          })
        }
      };

      setDashboardData(filteredDashboardData);
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

      console.log('Adding website with data:', websiteData);
      console.log('Auth headers:', getAuthHeaders());
      console.log('API URL:', `${API_BASE_URL}/api/website-intelligence/website/add`);
      console.log('Request config:', {
        method: 'POST',
        url: `${API_BASE_URL}/api/website-intelligence/website/add`,
        headers: getAuthHeaders(),
        data: websiteData
      });

      const response = await axios.post(`${API_BASE_URL}/api/website-intelligence/website/add`, websiteData, {
        headers: getAuthHeaders()
      });
      
      console.log('Website added successfully:', response.data);
      alert('Website added successfully!');
      
      // Reset form and close dialog
      setNewWebsite({ domain: '', name: '', type: 'E-commerce' });
      setShowAddWebsite(false);
      
      // Refresh data
      loadAllData();
      
    } catch (error) {
      console.error('Error adding website:', error);
      console.error('Error response:', error.response);
      console.error('Error status:', error.response?.status);
      console.error('Error data:', error.response?.data);
      
      if (error.response?.status === 403) {
        alert('Website limit reached for your current plan. Please upgrade to add more websites.');
      } else if (error.response?.status === 401) {
        alert('Authentication failed. Please log in again.');
      } else if (error.response?.status === 400) {
        const errorMsg = error.response?.data?.detail || 'Invalid website data provided.';
        alert(`Validation Error: ${errorMsg}`);
      } else if (error.response?.status === 500) {
        const errorMsg = error.response?.data?.detail || 'Server error occurred.';
        alert(`Server Error: ${errorMsg}`);
      } else if (error.code === 'NETWORK_ERROR' || !error.response) {
        alert('Network error: Unable to connect to server. Please check your connection.');
      } else {
        const statusCode = error.response?.status || 'Unknown';
        const errorDetail = error.response?.data?.detail || error.message || 'Unknown error';
        alert(`Error ${statusCode}: ${errorDetail}`);
      }
    }
  };

  const handleDeleteWebsite = async (website) => {
    if (!confirm(`Are you sure you want to delete "${website.website_name}" (${website.domain})? This action cannot be undone.`)) {
      return;
    }

    try {
      console.log('Deleting website:', website);
      
      // Add to deleted websites list to persist the deletion
      setDeletedWebsites(prev => [...prev, {
        website_id: website.website_id,
        domain: website.domain,
        website_name: website.website_name
      }]);
      
      // Remove from current state immediately
      if (dashboardData && dashboardData.dashboard && dashboardData.dashboard.user_websites) {
        const updatedWebsites = dashboardData.dashboard.user_websites.filter(
          site => site.website_id !== website.website_id && 
                  site.domain !== website.domain && 
                  site.website_name !== website.website_name
        );
        
        // Update the local state
        setDashboardData({
          ...dashboardData,
          dashboard: {
            ...dashboardData.dashboard,
            user_websites: updatedWebsites,
            websites_overview: {
              ...dashboardData.dashboard.websites_overview,
              total_websites: Math.max(0, (dashboardData.dashboard.websites_overview?.total_websites || 0) - 1),
              active_websites: Math.max(0, (dashboardData.dashboard.websites_overview?.active_websites || 0) - 1)
            }
          }
        });
        
        alert(`Website "${website.website_name}" has been removed from your account.`);
        console.log('Website removed and added to deleted list');
      }
      
      // TODO: When backend delete endpoint is implemented, add API call here:
      // await axios.delete(`${API_BASE_URL}/api/website-intelligence/website/${website.website_id}`, {
      //   headers: getAuthHeaders()
      // });
      
    } catch (error) {
      console.error('Error deleting website:', error);
      alert('Error deleting website. Please try again.');
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
                    <div className="flex items-center space-x-2">
                      <Badge className={`${
                        website.status === 'active' ? 'bg-green-500/20 text-green-400' : 
                        'bg-red-500/20 text-red-400'
                      }`}>
                        {website.status}
                      </Badge>
                      <button
                        onClick={() => handleDeleteWebsite(website)}
                        className="p-1 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors"
                        title="Delete website"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
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

                    {/* Metrics Grid - Now Clickable */}
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <button
                        onClick={() => {
                          setSelectedWebsite(website);
                          setDetailView('seo');
                          setShowWebsiteDetails(true);
                        }}
                        className="text-center p-2 bg-slate-700/30 rounded hover:bg-slate-600/30 transition-colors cursor-pointer"
                        title="Click to view SEO details"
                      >
                        <div className="text-blue-400 font-semibold">{website.seo_score?.toFixed(1)}</div>
                        <div className="text-slate-400 text-xs">SEO Score</div>
                      </button>
                      <button
                        onClick={() => {
                          setSelectedWebsite(website);
                          setDetailView('performance');
                          setShowWebsiteDetails(true);
                        }}
                        className="text-center p-2 bg-slate-700/30 rounded hover:bg-slate-600/30 transition-colors cursor-pointer"
                        title="Click to view performance details"
                      >
                        <div className="text-green-400 font-semibold">{website.performance_score?.toFixed(1)}</div>
                        <div className="text-slate-400 text-xs">Performance</div>
                      </button>
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

                    {/* Issues & Opportunities - Now Clickable */}
                    <div className="flex items-center justify-between text-xs">
                      <button
                        onClick={() => {
                          setSelectedWebsite(website);
                          setDetailView('issues');
                          setShowWebsiteDetails(true);
                        }}
                        className="flex items-center text-red-400 hover:text-red-300 hover:bg-red-500/10 px-2 py-1 rounded transition-colors cursor-pointer"
                        title="Click to view detailed issues"
                      >
                        <AlertTriangle className="w-3 h-3 mr-1" />
                        {website.issues_count || 0} Issues
                      </button>
                      <button
                        onClick={() => {
                          setSelectedWebsite(website);
                          setDetailView('opportunities');
                          setShowWebsiteDetails(true);
                        }}
                        className="flex items-center text-green-400 hover:text-green-300 hover:bg-green-500/10 px-2 py-1 rounded transition-colors cursor-pointer"
                        title="Click to view detailed opportunities"
                      >
                        <Lightbulb className="w-3 h-3 mr-1" />
                        {website.opportunities_count || 0} Opportunities
                      </button>
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

      {/* Website Details Modal */}
      {showWebsiteDetails && selectedWebsite && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-800 rounded-xl border border-slate-700 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b border-slate-700">
              <h3 className="text-xl font-semibold text-white">
                {selectedWebsite.website_name} - {detailView === 'issues' ? 'Issues' : 
                detailView === 'opportunities' ? 'Opportunities' :
                detailView === 'seo' ? 'SEO Analysis' :
                detailView === 'performance' ? 'Performance Analysis' : 'Overview'}
              </h3>
              <button
                onClick={() => {
                  setShowWebsiteDetails(false);
                  setSelectedWebsite(null);
                  setDetailView('overview');
                }}
                className="text-slate-400 hover:text-white"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="p-6">
              {/* Issues Detail View */}
              {detailView === 'issues' && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h4 className="text-lg font-semibold text-white">Website Issues</h4>
                    <Badge className="bg-red-500/20 text-red-400">
                      {selectedWebsite.issues_count || 0} Issues Found
                    </Badge>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5" />
                        <div>
                          <h5 className="font-medium text-white">Slow Page Load Speed</h5>
                          <p className="text-slate-400 text-sm mt-1">
                            Your homepage takes 4.2 seconds to load, which is above the recommended 2.5 seconds.
                          </p>
                          <div className="mt-2">
                            <span className="text-xs bg-red-500/20 text-red-400 px-2 py-1 rounded">High Priority</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <AlertTriangle className="w-5 h-5 text-yellow-400 mt-0.5" />
                        <div>
                          <h5 className="font-medium text-white">Missing Meta Descriptions</h5>
                          <p className="text-slate-400 text-sm mt-1">
                            15 pages are missing meta descriptions, which impacts SEO performance.
                          </p>
                          <div className="mt-2">
                            <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">Medium Priority</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <AlertTriangle className="w-5 h-5 text-orange-400 mt-0.5" />
                        <div>
                          <h5 className="font-medium text-white">Broken Internal Links</h5>
                          <p className="text-slate-400 text-sm mt-1">
                            3 internal links return 404 errors and need to be fixed.
                          </p>
                          <div className="mt-2">
                            <span className="text-xs bg-orange-500/20 text-orange-400 px-2 py-1 rounded">Low Priority</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-slate-700">
                    <h5 className="font-medium text-white mb-2">Recommended Actions</h5>
                    <ul className="space-y-2 text-sm text-slate-300">
                      <li className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                        <span>Optimize images and enable compression to improve load speed</span>
                      </li>
                      <li className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                        <span>Add meta descriptions to all pages using relevant keywords</span>
                      </li>
                      <li className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                        <span>Update or remove broken internal links</span>
                      </li>
                    </ul>
                  </div>
                </div>
              )}

              {/* Opportunities Detail View */}
              {detailView === 'opportunities' && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h4 className="text-lg font-semibold text-white">Growth Opportunities</h4>
                    <Badge className="bg-green-500/20 text-green-400">
                      {selectedWebsite.opportunities_count || 0} Opportunities
                    </Badge>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <Lightbulb className="w-5 h-5 text-green-400 mt-0.5" />
                        <div>
                          <h5 className="font-medium text-white">Add Schema Markup</h5>
                          <p className="text-slate-400 text-sm mt-1">
                            Implementing structured data could improve your search result appearance and increase click-through rates by 15-20%.
                          </p>
                          <div className="mt-2">
                            <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">High Impact</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <Lightbulb className="w-5 h-5 text-blue-400 mt-0.5" />
                        <div>
                          <h5 className="font-medium text-white">Mobile Optimization</h5>
                          <p className="text-slate-400 text-sm mt-1">
                            Your mobile page speed score is 65. Optimizing for mobile could increase conversions by 10-12%.
                          </p>
                          <div className="mt-2">
                            <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded">Medium Impact</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <Lightbulb className="w-5 h-5 text-purple-400 mt-0.5" />
                        <div>
                          <h5 className="font-medium text-white">Content Expansion</h5>
                          <p className="text-slate-400 text-sm mt-1">
                            Adding blog content targeting 5 identified keywords could drive 25% more organic traffic.
                          </p>
                          <div className="mt-2">
                            <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-1 rounded">Long-term</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <Lightbulb className="w-5 h-5 text-yellow-400 mt-0.5" />
                        <div>
                          <h5 className="font-medium text-white">Social Media Integration</h5>
                          <p className="text-slate-400 text-sm mt-1">
                            Adding social sharing buttons and Open Graph tags could increase referral traffic by 8-10%.
                          </p>
                          <div className="mt-2">
                            <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">Quick Win</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-slate-700">
                    <h5 className="font-medium text-white mb-2">Priority Recommendations</h5>
                    <ol className="space-y-2 text-sm text-slate-300">
                      <li className="flex items-center space-x-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-xs">1</span>
                        <span>Implement schema markup for products/services (High Impact)</span>
                      </li>
                      <li className="flex items-center space-x-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs">2</span>
                        <span>Optimize mobile performance and user experience</span>
                      </li>
                      <li className="flex items-center space-x-3">
                        <span className="flex-shrink-0 w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-xs">3</span>
                        <span>Create content strategy for identified keyword opportunities</span>
                      </li>
                    </ol>
                  </div>
                </div>
              )}

              {/* SEO Analysis Detail View */}
              {detailView === 'seo' && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h4 className="text-lg font-semibold text-white">SEO Analysis</h4>
                    <Badge className="bg-blue-500/20 text-blue-400">
                      Score: {selectedWebsite.seo_score?.toFixed(1) || 0}/100
                    </Badge>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <h5 className="font-medium text-white mb-2">On-Page SEO</h5>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Title Tags</span>
                          <span className="text-green-400">Good</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-300">Meta Descriptions</span>
                          <span className="text-yellow-400">Needs Work</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-300">Header Structure</span>
                          <span className="text-green-400">Good</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-300">Internal Linking</span>
                          <span className="text-red-400">Poor</span>
                        </div>
                      </div>
                    </div>

                    <div className="bg-slate-700/30 rounded-lg p-4">
                      <h5 className="font-medium text-white mb-2">Technical SEO</h5>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-slate-300">Site Speed</span>
                          <span className="text-yellow-400">Fair</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-300">Mobile Friendly</span>
                          <span className="text-green-400">Good</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-300">SSL Certificate</span>
                          <span className="text-green-400">Good</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-300">XML Sitemap</span>
                          <span className="text-green-400">Good</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-slate-700/30 rounded-lg p-4">
                    <h5 className="font-medium text-white mb-3">Top Keywords</h5>
                    <div className="flex flex-wrap gap-2">
                      {['ecommerce platform', 'online store', 'digital marketing', 'web development', 'seo services'].map((keyword, index) => (
                        <span key={index} className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Performance Analysis Detail View */}
              {detailView === 'performance' && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h4 className="text-lg font-semibold text-white">Performance Analysis</h4>
                    <Badge className="bg-green-500/20 text-green-400">
                      Score: {selectedWebsite.performance_score?.toFixed(1) || 0}/100
                    </Badge>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-slate-700/30 rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-blue-400 mb-1">2.1s</div>
                      <div className="text-slate-300 text-sm">First Contentful Paint</div>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-yellow-400 mb-1">4.2s</div>
                      <div className="text-slate-300 text-sm">Largest Contentful Paint</div>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-green-400 mb-1">0.1s</div>
                      <div className="text-slate-300 text-sm">Cumulative Layout Shift</div>
                    </div>
                  </div>

                  <div className="bg-slate-700/30 rounded-lg p-4">
                    <h5 className="font-medium text-white mb-3">Performance Recommendations</h5>
                    <ul className="space-y-2 text-sm text-slate-300">
                      <li className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                        <span>Compress and optimize images (potential 1.5s improvement)</span>
                      </li>
                      <li className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                        <span>Enable browser caching (potential 0.8s improvement)</span>
                      </li>
                      <li className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                        <span>Minify CSS and JavaScript (potential 0.3s improvement)</span>
                      </li>
                    </ul>
                  </div>
                </div>
              )}
            </div>

            <div className="flex justify-end space-x-3 p-6 border-t border-slate-700">
              <button
                onClick={() => {
                  setShowWebsiteDetails(false);
                  setSelectedWebsite(null);
                  setDetailView('overview');
                }}
                className="px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 transition-colors"
              >
                Close
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Export Report
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WebsiteIntelligenceHub;