import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Textarea } from './components/ui/textarea';
import { Badge } from './components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Alert, AlertDescription } from './components/ui/alert';
import { Progress } from './components/ui/progress';
import { 
  Users, 
  TrendingUp, 
  Mail, 
  Target, 
  BarChart3, 
  Brain, 
  Zap,
  DollarSign,
  ShoppingCart,
  Calendar,
  Send,
  Eye,
  MousePointer,
  CheckCircle,
  Megaphone,
  TestTube,
  Palette,
  TrendingDown,
  Gift,
  Settings,
  Activity,
  PieChart
} from 'lucide-react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [customers, setCustomers] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');

  // Marketing Automation Pro state
  const [marketingDashboard, setMarketingDashboard] = useState(null);
  const [multiChannelData, setMultiChannelData] = useState(null);
  const [abTestingData, setAbTestingData] = useState(null);
  const [dynamicContentData, setDynamicContentData] = useState(null);
  const [crossSellData, setCrossSellData] = useState(null);
  const [referralData, setReferralData] = useState(null);

  // Campaign creation state
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    target_segment: 'active',
    subject: '',
    content: '',
    scheduled_date: ''
  });

  useEffect(() => {
    loadData();
    
    // Fallback timeout to prevent infinite loading
    const timeoutId = setTimeout(() => {
      console.log('Customer Mind IQ: Timeout reached, forcing load completion');
      setLoading(false);
    }, 10000); // 10 second timeout
    
    return () => clearTimeout(timeoutId);
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      console.log('Loading Customer Mind IQ data...');
      
      const [customersRes, campaignsRes, analyticsRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/customers`).catch(err => {
          console.error('Customers API error:', err);
          return { data: [] };
        }),
        axios.get(`${API_BASE_URL}/api/campaigns`).catch(err => {
          console.error('Campaigns API error:', err);
          return { data: [] };
        }),
        axios.get(`${API_BASE_URL}/api/analytics`).catch(err => {
          console.error('Analytics API error:', err);
          return { data: { total_customers: 0, total_revenue: 0, top_products: [], conversion_metrics: {}, segment_distribution: {} } };
        })
      ]);
      
      setCustomers(customersRes.data);
      setCampaigns(campaignsRes.data);
      setAnalytics(analyticsRes.data);
      
      // Load Marketing Automation Pro data
      await loadMarketingData();
      
      console.log('Customer Mind IQ data loaded successfully');
    } catch (error) {
      console.error('Error loading data:', error);
      // Set default values to prevent hanging
      setCustomers([]);
      setCampaigns([]);
      setAnalytics({
        total_customers: 0,
        total_revenue: 0,
        top_products: [],
        conversion_metrics: {
          email_open_rate: 0.28,
          click_through_rate: 0.15,
          conversion_rate: 0.095,
          average_deal_size: 4200.0
        },
        segment_distribution: {}
      });
    } finally {
      setLoading(false);
      console.log('Customer Mind IQ loading complete');
    }
  };

  const loadMarketingData = async () => {
    try {
      console.log('Loading Marketing Automation Pro data...');
      
      const [
        marketingRes,
        multiChannelRes,
        abTestingRes,
        dynamicContentRes,
        crossSellRes,
        referralRes
      ] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/marketing/dashboard`).catch(err => {
          console.error('Marketing dashboard error:', err);
          return { data: { modules: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/marketing/multi-channel-orchestration`).catch(err => {
          console.error('Multi-channel error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/marketing/ab-testing`).catch(err => {
          console.error('A/B testing error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/marketing/dynamic-content`).catch(err => {
          console.error('Dynamic content error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/marketing/cross-sell-intelligence`).catch(err => {
          console.error('Cross-sell error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/marketing/referral-program`).catch(err => {
          console.error('Referral program error:', err);
          return { data: { dashboard: {} } };
        })
      ]);
      
      setMarketingDashboard(marketingRes.data);
      setMultiChannelData(multiChannelRes.data);
      setAbTestingData(abTestingRes.data);
      setDynamicContentData(dynamicContentRes.data);
      setCrossSellData(crossSellRes.data);
      setReferralData(referralRes.data);
      
      console.log('Marketing Automation Pro data loaded successfully');
    } catch (error) {
      console.error('Error loading marketing data:', error);
      // Set default values
      setMarketingDashboard({ modules: {} });
      setMultiChannelData({ dashboard: {} });
      setAbTestingData({ dashboard: {} });
      setDynamicContentData({ dashboard: {} });
      setCrossSellData({ dashboard: {} });
      setReferralData({ dashboard: {} });
    }
  };

  const loadCustomerRecommendations = async (customerId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/customers/${customerId}/recommendations`);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error loading recommendations:', error);
    }
  };

  const createCampaign = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/campaigns`, newCampaign);
      setCampaigns([...campaigns, response.data]);
      setNewCampaign({
        name: '',
        target_segment: 'active',
        subject: '',
        content: '',
        scheduled_date: ''
      });
      alert('Campaign created successfully!');
    } catch (error) {
      console.error('Error creating campaign:', error);
      alert('Error creating campaign');
    }
  };

  const getEngagementColor = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-blue-500';
    if (score >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getLifecycleColor = (stage) => {
    const colors = {
      'new': 'bg-blue-100 text-blue-800',
      'active': 'bg-green-100 text-green-800',
      'at_risk': 'bg-yellow-100 text-yellow-800',
      'churned': 'bg-red-100 text-red-800'
    };
    return colors[stage] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <img 
            src="https://customer-assets.emergentagent.com/job_upsell-tracker/artifacts/a451o37y_Customer%20Mind%20IQ%20logo.png" 
            alt="Customer Mind IQ Logo" 
            className="h-16 w-16 mx-auto mb-4 animate-pulse"
          />
          <div className="text-white text-xl mb-2">Customer Mind IQ</div>
          <div className="text-slate-300 text-sm">Loading AI Analytics Platform...</div>
          <div className="mt-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur-xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <img 
                src="https://customer-assets.emergentagent.com/job_upsell-tracker/artifacts/a451o37y_Customer%20Mind%20IQ%20logo.png" 
                alt="Customer Mind IQ Logo" 
                className="h-12 w-12 object-contain"
              />
              <div>
                <h1 className="text-2xl font-bold text-white">Customer Mind IQ</h1>
                <p className="text-sm text-slate-300">AI-Powered Purchase Analytics & Email Marketing</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-400 border-green-400">
                AI-Powered
              </Badge>
              <Badge variant="outline" className="text-blue-400 border-blue-400">
                {customers.length} Customers
              </Badge>
              <div className="text-xs text-slate-400">
                customermindai.com
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-slate-800/50 backdrop-blur-xl">
            <TabsTrigger value="dashboard" className="text-white data-[state=active]:bg-blue-600">
              <BarChart3 className="w-4 h-4 mr-2" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="customers" className="text-white data-[state=active]:bg-blue-600">
              <Users className="w-4 h-4 mr-2" />
              Customer Intelligence
            </TabsTrigger>  
            <TabsTrigger value="campaigns" className="text-white data-[state=active]:bg-blue-600">
              <Mail className="w-4 h-4 mr-2" />
              Email Campaigns
            </TabsTrigger>
            <TabsTrigger value="create" className="text-white data-[state=active]:bg-blue-600">
              <Zap className="w-4 h-4 mr-2" />
              Create Campaign
            </TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            {analytics && (
              <>
                {/* Welcome Section */}
                <Card className="bg-gradient-to-r from-blue-900/40 to-slate-800/40 backdrop-blur-xl border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-2xl text-white flex items-center">
                      <Brain className="w-8 h-8 mr-3 text-blue-400" />
                      Welcome to Customer Mind IQ
                    </CardTitle>
                    <CardDescription className="text-slate-300 text-lg">
                      Unlock customer insights with AI-powered analytics and targeted marketing automation
                    </CardDescription>
                  </CardHeader>
                </Card>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:bg-slate-800/70 transition-all">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">Total Customers</CardTitle>
                      <Users className="h-5 w-5 text-blue-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">{analytics.total_customers}</div>
                      <p className="text-xs text-slate-400 mt-1">Active customer base</p>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:bg-slate-800/70 transition-all">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">Total Revenue</CardTitle>
                      <DollarSign className="h-5 w-5 text-green-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">
                        ${analytics.total_revenue.toLocaleString()}
                      </div>
                      <p className="text-xs text-slate-400 mt-1">Lifetime customer value</p>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:bg-slate-800/70 transition-all">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">AI Conversion Rate</CardTitle>
                      <Target className="h-5 w-5 text-purple-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">
                        {(analytics.conversion_metrics.conversion_rate * 100).toFixed(1)}%
                      </div>
                      <p className="text-xs text-slate-400 mt-1">Email to purchase</p>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:bg-slate-800/70 transition-all">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">Avg Deal Size</CardTitle>
                      <ShoppingCart className="h-5 w-5 text-yellow-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-white">
                        ${analytics.conversion_metrics.average_deal_size.toLocaleString()}
                      </div>
                      <p className="text-xs text-slate-400 mt-1">Per customer transaction</p>
                    </CardContent>
                  </Card>
                </div>

                {/* Performance Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white flex items-center">
                        <Eye className="w-5 h-5 mr-2 text-blue-400" />
                        Email Open Rate
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-slate-300">Current Performance</span>
                          <span className="text-white font-medium">
                            {(analytics.conversion_metrics.email_open_rate * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress 
                          value={analytics.conversion_metrics.email_open_rate * 100} 
                          className="h-3"
                        />
                        <p className="text-xs text-slate-400">Industry avg: 22%</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white flex items-center">
                        <MousePointer className="w-5 h-5 mr-2 text-purple-400" />
                        Click Through Rate
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-slate-300">Current Performance</span>
                          <span className="text-white font-medium">
                            {(analytics.conversion_metrics.click_through_rate * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress 
                          value={analytics.conversion_metrics.click_through_rate * 100} 
                          className="h-3"
                        />
                        <p className="text-xs text-slate-400">Industry avg: 3.2%</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white flex items-center">
                        <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                        Purchase Conversion
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-slate-300">AI-Optimized Rate</span>
                          <span className="text-white font-medium">
                            {(analytics.conversion_metrics.conversion_rate * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress 
                          value={analytics.conversion_metrics.conversion_rate * 100} 
                          className="h-3"
                        />
                        <p className="text-xs text-slate-400">Industry avg: 2.1%</p>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Top Products */}
                <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <TrendingUp className="w-5 h-5 mr-2 text-green-400" />
                      Top Performing Software Products
                    </CardTitle>
                    <CardDescription className="text-slate-400">
                      Most purchased software by customer count and revenue impact
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {analytics.top_products.map((product, index) => (
                        <div key={index} className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700/70 transition-all">
                          <div className="flex items-center space-x-4">
                            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                              {index + 1}
                            </div>
                            <div>
                              <h3 className="font-semibold text-white">{product.name}</h3>
                              <p className="text-sm text-slate-400">{product.customers} customers • High conversion potential</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-bold text-green-400">
                              ${product.revenue.toLocaleString()}
                            </div>
                            <div className="text-sm text-slate-400">Revenue generated</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          {/* Customers Tab */}
          <TabsContent value="customers" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Customer List */}
              <div className="lg:col-span-2">
                <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <Brain className="w-6 h-6 mr-2 text-blue-400" />
                      Customer Intelligence Dashboard
                    </CardTitle>
                    <CardDescription className="text-slate-400">
                      AI-powered insights into customer behavior, purchase patterns, and growth opportunities
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {customers.map((customer) => (
                        <div 
                          key={customer.customer_id} 
                          className={`p-5 bg-slate-700/50 rounded-lg cursor-pointer transition-all hover:bg-slate-700/70 hover:scale-[1.02] ${
                            selectedCustomer?.customer_id === customer.customer_id ? 'ring-2 ring-blue-400 bg-slate-700/70' : ''
                          }`}
                          onClick={() => {
                            setSelectedCustomer(customer);
                            loadCustomerRecommendations(customer.customer_id);
                          }}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="font-semibold text-white text-lg">{customer.name}</h3>
                            <Badge className={getLifecycleColor(customer.lifecycle_stage)}>
                              {customer.lifecycle_stage.toUpperCase()}
                            </Badge>
                          </div>
                          
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm text-slate-400">{customer.email}</span>
                            <div className="text-right">
                              <div className="text-lg font-bold text-green-400">
                                ${customer.total_spent.toLocaleString()}
                              </div>
                              <div className="text-xs text-slate-400">{customer.total_purchases} purchases</div>
                            </div>
                          </div>

                          <div className="mb-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm text-slate-400">AI Engagement Score</span>
                              <span className="text-sm font-medium text-white">
                                {customer.engagement_score}/100
                              </span>
                            </div>
                            
                            <Progress 
                              value={customer.engagement_score} 
                              className="h-2 mb-1"
                            />
                            <p className="text-xs text-slate-500">
                              {customer.engagement_score >= 80 ? 'High value customer' :
                               customer.engagement_score >= 60 ? 'Engaged customer' :
                               customer.engagement_score >= 40 ? 'Moderate engagement' : 'Needs attention'}
                            </p>
                          </div>

                          <div className="flex flex-wrap gap-2">
                            {customer.software_owned.map((software, index) => (
                              <Badge key={index} variant="outline" className="text-xs text-blue-400 border-blue-400">
                                {software}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Customer Details & Recommendations */}
              <div>
                {selectedCustomer ? (
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white flex items-center">
                        <Target className="w-5 h-5 mr-2 text-purple-400" />
                        AI Recommendations
                      </CardTitle>
                      <CardDescription className="text-slate-400">
                        Personalized insights for {selectedCustomer.name}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <Alert className="bg-blue-500/10 border-blue-500/20">
                          <Brain className="h-4 w-4 text-blue-400" />
                          <AlertDescription className="text-blue-300">
                            AI Analysis: {selectedCustomer.engagement_score >= 70 ? 'High-value customer with strong upsell potential' : 
                                          selectedCustomer.engagement_score >= 50 ? 'Engaged customer ready for targeted offers' : 
                                          'Customer needs re-engagement strategy'}
                          </AlertDescription>
                        </Alert>
                        
                        {recommendations.map((rec, index) => (
                          <div key={index} className="p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700/70 transition-all">
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="font-medium text-white">{rec.product_name}</h4>
                              <Badge className="bg-green-500/20 text-green-400">
                                {rec.confidence_score.toFixed(0)}% match
                              </Badge>
                            </div>
                            <p className="text-sm text-slate-400 mb-3">{rec.reason}</p>
                            <div className="flex items-center justify-between">
                              <span className="text-xs text-slate-500">Conversion Probability</span>
                              <div className="flex items-center space-x-2">
                                <Progress value={rec.estimated_conversion_probability * 100} className="h-2 w-16" />
                                <span className="text-xs font-medium text-purple-400">
                                  {(rec.estimated_conversion_probability * 100).toFixed(0)}%
                                </span>
                              </div>
                            </div>
                          </div>
                        ))}
                        
                        {recommendations.length === 0 && (
                          <div className="text-center py-8">
                            <Brain className="w-12 h-12 text-slate-600 mx-auto mb-2" />
                            <p className="text-slate-400">Analyzing customer data...</p>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ) : (
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardContent className="flex items-center justify-center h-96">
                      <div className="text-center">
                        <img 
                          src="https://customer-assets.emergentagent.com/job_upsell-tracker/artifacts/a451o37y_Customer%20Mind%20IQ%20logo.png" 
                          alt="Customer Mind IQ" 
                          className="w-24 h-24 mx-auto mb-4 opacity-50"
                        />
                        <p className="text-slate-400 text-lg mb-2">Select a customer to view</p>
                        <p className="text-slate-500">AI-powered recommendations and insights</p>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </TabsContent>

          {/* Campaigns Tab */}
          <TabsContent value="campaigns" className="space-y-6">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Mail className="w-6 h-6 mr-2 text-blue-400" />
                  Email Marketing Campaigns
                </CardTitle>
                <CardDescription className="text-slate-400">
                  AI-powered email campaigns with personalized product recommendations
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {campaigns.map((campaign, index) => (
                    <div key={index} className="p-5 bg-slate-700/50 rounded-lg hover:bg-slate-700/70 transition-all">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-white text-lg">{campaign.name}</h3>
                        <Badge className={
                          campaign.status === 'sent' ? 'bg-green-500/20 text-green-400' :
                          campaign.status === 'draft' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-red-500/20 text-red-400'
                        }>
                          {campaign.status.toUpperCase()}
                        </Badge>
                      </div>
                      
                      <p className="text-slate-300 mb-3">{campaign.subject}</p>
                      
                      <div className="grid grid-cols-3 gap-4 text-xs text-slate-400">
                        <div className="text-center">
                          <div className="text-white font-medium">{campaign.target_segment}</div>
                          <div>Target Segment</div>
                        </div>
                        <div className="text-center">
                          <div className="text-white font-medium">{campaign.target_customers.length}</div>
                          <div>Recipients</div>
                        </div>
                        <div className="text-center">
                          <div className="text-white font-medium">{campaign.recommended_products.length}</div>
                          <div>AI Recommendations</div>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {campaigns.length === 0 && (
                    <div className="text-center py-12">
                      <Mail className="w-16 h-16 text-slate-600 mx-auto mb-4" />
                      <p className="text-slate-400 text-lg">No campaigns created yet</p>
                      <p className="text-slate-500">Create your first AI-powered campaign in the Create Campaign tab</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Create Campaign Tab */}
          <TabsContent value="create" className="space-y-6">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Zap className="w-6 h-6 mr-2 text-purple-400" />
                  Create AI-Powered Marketing Campaign
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Generate intelligent email campaigns with personalized product recommendations using Customer Mind IQ
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Campaign Name
                  </label>
                  <Input
                    value={newCampaign.name}
                    onChange={(e) => setNewCampaign({...newCampaign, name: e.target.value})}
                    placeholder="e.g., Q4 Software Upgrade Recommendations"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Target Customer Segment
                  </label>
                  <Select 
                    value={newCampaign.target_segment}
                    onValueChange={(value) => setNewCampaign({...newCampaign, target_segment: value})}
                  >
                    <SelectTrigger className="bg-slate-700/50 border-slate-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="new">New Customers</SelectItem>
                      <SelectItem value="active">Active Customers</SelectItem>
                      <SelectItem value="at_risk">At Risk Customers</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Email Subject Line
                  </label>
                  <Input
                    value={newCampaign.subject}
                    onChange={(e) => setNewCampaign({...newCampaign, subject: e.target.value})}
                    placeholder="AI will enhance this with personalization"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Schedule Campaign (Optional)
                  </label>
                  <Input
                    type="datetime-local"
                    value={newCampaign.scheduled_date}
                    onChange={(e) => setNewCampaign({...newCampaign, scheduled_date: e.target.value})}
                    className="bg-slate-700/50 border-slate-600 text-white"
                  />
                </div>

                <Alert className="bg-purple-500/10 border-purple-500/20">
                  <Brain className="h-4 w-4 text-purple-400" />
                  <AlertDescription className="text-purple-300">
                    <strong>Customer Mind IQ</strong> will automatically generate personalized email content and product recommendations for each customer segment using advanced AI analysis.
                  </AlertDescription>
                </Alert>

                <Button 
                  onClick={createCampaign}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium py-3"
                  disabled={!newCampaign.name || !newCampaign.subject}
                >
                  <Send className="w-5 h-5 mr-2" />
                  Launch AI-Powered Campaign
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

export default App;