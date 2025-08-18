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
  PieChart,
  ArrowRightLeft,
  MessageSquare
} from 'lucide-react';
import axios from 'axios';
import SignIn from './components/SignIn';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import CreateCampaign from './components/CreateCampaign';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('dashboard');
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
  const [leadScoringData, setLeadScoringData] = useState(null);
  const [referralData, setReferralData] = useState(null);

  // Advanced Features Expansion state
  const [advancedDashboard, setAdvancedDashboard] = useState(null);
  const [behavioralClusteringData, setBehavioralClusteringData] = useState(null);
  const [churnPreventionData, setChurnPreventionData] = useState(null);
  const [crossSellIntelligenceData, setCrossSellIntelligenceData] = useState(null);
  const [advancedPricingData, setAdvancedPricingData] = useState(null);
  const [sentimentAnalysisData, setSentimentAnalysisData] = useState(null);

  // Revenue Analytics Suite state
  const [revenueDashboard, setRevenueDashboard] = useState(null);
  const [revenueForecastingData, setRevenueForecastingData] = useState(null);
  const [priceOptimizationData, setPriceOptimizationData] = useState(null);
  const [profitMarginData, setProfitMarginData] = useState(null);
  const [subscriptionAnalyticsData, setSubscriptionAnalyticsData] = useState(null);
  const [financialReportingData, setFinancialReportingData] = useState(null);

  // Analytics & Insights state
  const [analyticsInsightsDashboard, setAnalyticsInsightsDashboard] = useState(null);
  const [customerJourneyData, setCustomerJourneyData] = useState(null);
  const [revenueAttributionData, setRevenueAttributionData] = useState(null);
  const [cohortAnalysisData, setCohortAnalysisData] = useState(null);
  const [competitiveIntelligenceData, setCompetitiveIntelligenceData] = useState(null);
  const [roiForecastingData, setRoiForecastingData] = useState(null);

  // Campaign creation state
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    target_segment: 'active',
    subject: '',
    content: '',
    scheduled_date: ''
  });

  // Authentication functions
  const handleSignIn = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
    setCurrentPage('dashboard');
  };

  const handleSignOut = () => {
    setUser(null);
    setIsAuthenticated(false);
    setCurrentPage('dashboard');
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  // Data loading on authentication
  useEffect(() => {
    if (isAuthenticated) {
      loadData();
    }
  }, [isAuthenticated]);

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
      
      // Load Advanced Features Expansion data
      await loadAdvancedFeaturesData();
      
      // Load Revenue Analytics Suite data
      await loadRevenueAnalyticsData();
      
      // Load Analytics & Insights data
      await loadAnalyticsInsightsData();
      
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
        leadScoringRes,
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
        axios.get(`${API_BASE_URL}/api/marketing/lead-scoring`).catch(err => {
          console.error('Lead scoring error:', err);
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
      setLeadScoringData(leadScoringRes.data);
      setReferralData(referralRes.data);
      
      console.log('Marketing Automation Pro data loaded successfully');
    } catch (error) {
      console.error('Error loading marketing data:', error);
      // Set default values
      setMarketingDashboard({ modules: {} });
      setMultiChannelData({ dashboard: {} });
      setAbTestingData({ dashboard: {} });
      setDynamicContentData({ dashboard: {} });
      setLeadScoringData({ dashboard: {} });
      setReferralData({ dashboard: {} });
    }
  };

  const loadAdvancedFeaturesData = async () => {
    try {
      console.log('Loading Advanced Features Expansion data...');
      
      const [
        advancedRes,
        behavioralRes,
        churnRes,
        crossSellAdvancedRes,
        pricingRes,
        sentimentRes
      ] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/advanced/dashboard`).catch(err => {
          console.error('Advanced dashboard error:', err);
          return { data: { modules: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/advanced/behavioral-clustering`).catch(err => {
          console.error('Behavioral clustering error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/advanced/churn-prevention`).catch(err => {
          console.error('Churn prevention error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/advanced/cross-sell-intelligence`).catch(err => {
          console.error('Cross-sell intelligence error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/advanced/pricing-optimization`).catch(err => {
          console.error('Advanced pricing error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/advanced/sentiment-analysis`).catch(err => {
          console.error('Sentiment analysis error:', err);
          return { data: { dashboard: {} } };
        })
      ]);
      
      setAdvancedDashboard(advancedRes.data);
      setBehavioralClusteringData(behavioralRes.data);
      setChurnPreventionData(churnRes.data);
      setCrossSellIntelligenceData(crossSellAdvancedRes.data);
      setAdvancedPricingData(pricingRes.data);
      setSentimentAnalysisData(sentimentRes.data);
      
      console.log('Advanced Features Expansion data loaded successfully');
    } catch (error) {
      console.error('Error loading advanced features data:', error);
      // Set default values
      setAdvancedDashboard({ modules: {} });
      setBehavioralClusteringData({ dashboard: {} });
      setChurnPreventionData({ dashboard: {} });
      setCrossSellIntelligenceData({ dashboard: {} });
      setAdvancedPricingData({ dashboard: {} });
      setSentimentAnalysisData({ dashboard: {} });
    }
  };

  const loadRevenueAnalyticsData = async () => {
    try {
      console.log('Loading Revenue Analytics Suite data...');
      
      const [
        revenueRes,
        forecastingRes,
        priceOptRes,
        profitMarginRes,
        subscriptionRes,
        financialRes
      ] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/revenue/dashboard`).catch(err => {
          console.error('Revenue dashboard error:', err);
          return { data: { modules: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/revenue/revenue-forecasting`).catch(err => {
          console.error('Revenue forecasting error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/revenue/price-optimization`).catch(err => {
          console.error('Price optimization error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/revenue/profit-margin-analysis`).catch(err => {
          console.error('Profit margin error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/revenue/subscription-analytics`).catch(err => {
          console.error('Subscription analytics error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/revenue/financial-reporting`).catch(err => {
          console.error('Financial reporting error:', err);
          return { data: { dashboard: {} } };
        })
      ]);
      
      setRevenueDashboard(revenueRes.data);
      setRevenueForecastingData(forecastingRes.data);
      setPriceOptimizationData(priceOptRes.data);
      setProfitMarginData(profitMarginRes.data);
      setSubscriptionAnalyticsData(subscriptionRes.data);
      setFinancialReportingData(financialRes.data);
      
      console.log('Revenue Analytics Suite data loaded successfully');
    } catch (error) {
      console.error('Error loading revenue analytics data:', error);
      // Set default values
      setRevenueDashboard({ modules: {} });
      setRevenueForecastingData({ dashboard: {} });
      setPriceOptimizationData({ dashboard: {} });
      setProfitMarginData({ dashboard: {} });
      setSubscriptionAnalyticsData({ dashboard: {} });
      setFinancialReportingData({ dashboard: {} });
    }
  };

  const loadAnalyticsInsightsData = async () => {
    try {
      console.log('Loading Analytics & Insights data...');
      
      const axiosConfig = {
        timeout: 60000, // 60 seconds timeout for comprehensive analytics
        headers: {
          'Content-Type': 'application/json'
        }
      };
      
      const [
        dashboardRes,
        journeyRes,
        attributionRes,
        cohortRes,
        competitiveRes,
        roiRes
      ] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/analytics/dashboard`, axiosConfig).catch(err => {
          console.error('Analytics dashboard error:', err);
          return { data: { modules: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/analytics/customer-journey-mapping/dashboard`, axiosConfig).catch(err => {
          console.error('Customer journey error:', err);
          return { data: { dashboard_data: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/analytics/revenue-attribution/dashboard`, axiosConfig).catch(err => {
          console.error('Revenue attribution error:', err);
          return { data: { dashboard_data: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/analytics/cohort-analysis/dashboard`, axiosConfig).catch(err => {
          console.error('Cohort analysis error:', err);
          return { data: { dashboard_data: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/analytics/competitive-intelligence/dashboard`, axiosConfig).catch(err => {
          console.error('Competitive intelligence error:', err);
          return { data: { dashboard_data: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/analytics/roi-forecasting/dashboard`, axiosConfig).catch(err => {
          console.error('ROI forecasting error:', err);
          return { data: { dashboard_data: {} } };
        })
      ]);
      
      console.log('Analytics dashboard response:', dashboardRes.data);
      console.log('Customer journey response:', journeyRes.data);
      console.log('Revenue attribution response:', attributionRes.data);
      console.log('Cohort analysis response:', cohortRes.data);
      console.log('Competitive intelligence response:', competitiveRes.data);
      console.log('ROI forecasting response:', roiRes.data);
      
      setAnalyticsInsightsDashboard(dashboardRes.data);
      setCustomerJourneyData(journeyRes.data);
      setRevenueAttributionData(attributionRes.data);
      setCohortAnalysisData(cohortRes.data);
      setCompetitiveIntelligenceData(competitiveRes.data);
      setRoiForecastingData(roiRes.data);
      
      console.log('Analytics & Insights data loaded successfully');
    } catch (error) {
      console.error('Error loading analytics insights data:', error);
      // Set default values
      setAnalyticsInsightsDashboard({ modules: {} });
      setCustomerJourneyData({ dashboard_data: {} });
      setRevenueAttributionData({ dashboard_data: {} });
      setCohortAnalysisData({ dashboard_data: {} });
      setCompetitiveIntelligenceData({ dashboard_data: {} });
      setRoiForecastingData({ dashboard_data: {} });
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

  // Show sign-in page if not authenticated
  if (!isAuthenticated) {
    return <SignIn onSignIn={handleSignIn} />;
  }

  // Show loading state
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

  // Render main application with header and current page
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <Header 
        currentPage={currentPage}
        onNavigate={handleNavigate}
        onSignOut={handleSignOut}
        user={user}
      />
      
      <div className="container mx-auto px-6 py-8">
        {currentPage === 'dashboard' && (
          <Dashboard 
            dashboardData={analytics}
            customerData={{ dashboard_data: { total_customers: customers.length } }}
            marketingData={{ leadScoringData, campaigns_count: campaigns.length }}
            advancedFeaturesData={advancedDashboard}
            revenueAnalyticsData={{ revenueForecastingData, roi: 3.4 }}
            analyticsInsightsDashboard={analyticsInsightsDashboard}
          />
        )}
        
        {currentPage === 'customers' && (
          <div className="space-y-6">
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
          </div>
        )}
        
        {currentPage === 'create' && (
          <CreateCampaign 
            campaigns={campaigns}
            newCampaign={newCampaign}
            setNewCampaign={setNewCampaign}
            handleCreateCampaign={createCampaign}
          />
        )}
        
        {/* Placeholder pages for other modules - these would be separate components */}
        {currentPage === 'marketing' && (
          <div className="space-y-6">
            <h1 className="text-3xl font-bold text-white">Marketing Automation</h1>
            <p className="text-slate-400">Marketing Automation Pro module coming soon...</p>
          </div>
        )}
        
        {currentPage === 'revenue' && (
          <div className="space-y-6">
            <h1 className="text-3xl font-bold text-white">Revenue Analytics</h1>
            <p className="text-slate-400">Revenue Analytics module coming soon...</p>
          </div>
        )}
        
        {currentPage === 'advanced' && (
          <div className="space-y-6">
            <h1 className="text-3xl font-bold text-white">Advanced Features</h1>
            <p className="text-slate-400">Advanced Features module coming soon...</p>
          </div>
        )}
        
        {currentPage === 'analytics' && (
          <div className="space-y-6">
            <h1 className="text-3xl font-bold text-white">Analytics & Insights</h1>
            <p className="text-slate-400">Analytics & Insights module coming soon...</p>
          </div>
        )}
      </div>
    </div>
  );
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
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
