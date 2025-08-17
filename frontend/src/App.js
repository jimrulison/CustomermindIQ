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
  CheckCircle
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
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      console.log('Starting to load data from:', API_BASE_URL);
      
      // Configure axios with longer timeout for AI processing
      const axiosConfig = { timeout: 60000 }; // 60 seconds timeout
      
      const [customersRes, campaignsRes, analyticsRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/customers`, axiosConfig),
        axios.get(`${API_BASE_URL}/api/campaigns`, axiosConfig),
        axios.get(`${API_BASE_URL}/api/analytics`, axiosConfig)
      ]);
      
      console.log('Data loaded successfully');
      setCustomers(customersRes.data);
      setCampaigns(campaignsRes.data);
      setAnalytics(analyticsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
      console.error('Error details:', error.response?.data || error.message);
    } finally {
      setLoading(false);
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
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur-xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Brain className="h-8 w-8 text-purple-400" />
              <h1 className="text-2xl font-bold text-white">Software Analytics Hub</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-400 border-green-400">
                AI-Powered
              </Badge>
              <Badge variant="outline" className="text-blue-400 border-blue-400">
                {customers.length} Customers
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-slate-800/50 backdrop-blur-xl">
            <TabsTrigger value="dashboard" className="text-white data-[state=active]:bg-purple-600">
              <BarChart3 className="w-4 h-4 mr-2" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="customers" className="text-white data-[state=active]:bg-purple-600">
              <Users className="w-4 h-4 mr-2" />
              Customers
            </TabsTrigger>  
            <TabsTrigger value="campaigns" className="text-white data-[state=active]:bg-purple-600">
              <Mail className="w-4 h-4 mr-2" />
              Campaigns
            </TabsTrigger>
            <TabsTrigger value="create" className="text-white data-[state=active]:bg-purple-600">
              <Zap className="w-4 h-4 mr-2" />
              Create Campaign
            </TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            {analytics && (
              <>
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">Total Customers</CardTitle>
                      <Users className="h-4 w-4 text-purple-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-white">{analytics.total_customers}</div>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">Total Revenue</CardTitle>
                      <DollarSign className="h-4 w-4 text-green-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-white">
                        ${analytics.total_revenue.toLocaleString()}
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">Conversion Rate</CardTitle>
                      <Target className="h-4 w-4 text-blue-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-white">
                        {(analytics.conversion_metrics.conversion_rate * 100).toFixed(1)}%
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium text-slate-300">Avg Deal Size</CardTitle>
                      <ShoppingCart className="h-4 w-4 text-yellow-400" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-white">
                        ${analytics.conversion_metrics.average_deal_size.toLocaleString()}
                      </div>
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
                          <span className="text-slate-300">Current Rate</span>
                          <span className="text-white font-medium">
                            {(analytics.conversion_metrics.email_open_rate * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress 
                          value={analytics.conversion_metrics.email_open_rate * 100} 
                          className="h-2"
                        />
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
                          <span className="text-slate-300">Current Rate</span>
                          <span className="text-white font-medium">
                            {(analytics.conversion_metrics.click_through_rate * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress 
                          value={analytics.conversion_metrics.click_through_rate * 100} 
                          className="h-2"
                        />
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardHeader>
                      <CardTitle className="text-white flex items-center">
                        <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                        Conversion Rate
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-slate-300">Current Rate</span>
                          <span className="text-white font-medium">
                            {(analytics.conversion_metrics.conversion_rate * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress 
                          value={analytics.conversion_metrics.conversion_rate * 100} 
                          className="h-2"
                        />
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Top Products */}
                <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white">Top Performing Software</CardTitle>
                    <CardDescription className="text-slate-400">
                      Most purchased software by customer count
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {analytics.top_products.map((product, index) => (
                        <div key={index} className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg">
                          <div>
                            <h3 className="font-semibold text-white">{product.name}</h3>
                            <p className="text-sm text-slate-400">{product.customers} customers</p>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-bold text-green-400">
                              ${product.revenue.toLocaleString()}
                            </div>
                            <div className="text-sm text-slate-400">Revenue</div>
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
                    <CardTitle className="text-white">Customer Analytics</CardTitle>
                    <CardDescription className="text-slate-400">
                      AI-powered insights into customer behavior and purchase patterns
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {customers.map((customer) => (
                        <div 
                          key={customer.customer_id} 
                          className={`p-4 bg-slate-700/50 rounded-lg cursor-pointer transition-all hover:bg-slate-700/70 ${
                            selectedCustomer?.customer_id === customer.customer_id ? 'ring-2 ring-purple-400' : ''
                          }`}
                          onClick={() => {
                            setSelectedCustomer(customer);
                            loadCustomerRecommendations(customer.customer_id);
                          }}
                        >
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-semibold text-white">{customer.name}</h3>
                            <Badge className={getLifecycleColor(customer.lifecycle_stage)}>
                              {customer.lifecycle_stage}
                            </Badge>
                          </div>
                          
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm text-slate-400">{customer.email}</span>
                            <span className="text-sm font-medium text-green-400">
                              ${customer.total_spent.toLocaleString()}
                            </span>
                          </div>

                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-slate-400">Engagement Score</span>
                            <span className="text-sm font-medium text-white">
                              {customer.engagement_score}/100
                            </span>
                          </div>
                          
                          <Progress 
                            value={customer.engagement_score} 
                            className="h-2 mb-3"
                          />

                          <div className="flex flex-wrap gap-1">
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
                        For {selectedCustomer.name}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {recommendations.map((rec, index) => (
                          <div key={index} className="p-3 bg-slate-700/50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="font-medium text-white">{rec.product_name}</h4>
                              <Badge className="bg-green-500/20 text-green-400">
                                {rec.confidence_score.toFixed(0)}% match
                              </Badge>
                            </div>
                            <p className="text-sm text-slate-400 mb-2">{rec.reason}</p>
                            <div className="flex items-center justify-between">
                              <span className="text-xs text-slate-500">Conversion Probability</span>
                              <span className="text-xs font-medium text-purple-400">
                                {(rec.estimated_conversion_probability * 100).toFixed(0)}%
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ) : (
                  <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                    <CardContent className="flex items-center justify-center h-48">
                      <div className="text-center">
                        <Brain className="w-12 h-12 text-slate-600 mx-auto mb-2" />
                        <p className="text-slate-400">Select a customer to view AI recommendations</p>
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
                <CardTitle className="text-white">Email Campaigns</CardTitle>
                <CardDescription className="text-slate-400">
                  Manage your automated email marketing campaigns
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {campaigns.map((campaign, index) => (
                    <div key={index} className="p-4 bg-slate-700/50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-white">{campaign.name}</h3>
                        <Badge className={
                          campaign.status === 'sent' ? 'bg-green-500/20 text-green-400' :
                          campaign.status === 'draft' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-red-500/20 text-red-400'
                        }>
                          {campaign.status}
                        </Badge>
                      </div>
                      
                      <p className="text-sm text-slate-400 mb-2">{campaign.subject}</p>
                      
                      <div className="flex items-center justify-between text-xs text-slate-500">
                        <span>Target: {campaign.target_segment}</span>
                        <span>{campaign.target_customers.length} customers</span>
                        <span>{campaign.recommended_products.length} recommendations</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Create Campaign Tab */}
          <TabsContent value="create" className="space-y-6">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Zap className="w-5 h-5 mr-2 text-purple-400" />
                  Create AI-Powered Campaign
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Generate targeted email campaigns with AI-powered product recommendations
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Campaign Name
                  </label>
                  <Input
                    value={newCampaign.name}
                    onChange={(e) => setNewCampaign({...newCampaign, name: e.target.value})}
                    placeholder="e.g., Q4 Software Upgrade Campaign"
                    className="bg-slate-700/50 border-slate-600 text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Target Segment
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
                    Email Subject
                  </label>
                  <Input
                    value={newCampaign.subject}
                    onChange={(e) => setNewCampaign({...newCampaign, subject: e.target.value})}
                    placeholder="AI will enhance this based on customer data"
                    className="bg-slate-700/50 border-slate-600 text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Schedule Date (Optional)
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
                    AI will automatically generate personalized content and product recommendations for each customer segment.
                  </AlertDescription>
                </Alert>

                <Button 
                  onClick={createCampaign}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                  disabled={!newCampaign.name || !newCampaign.subject}
                >
                  <Send className="w-4 h-4 mr-2" />
                  Create AI-Powered Campaign
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