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
  MessageSquare,
  AlertTriangle
} from 'lucide-react';
import axios from 'axios';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import SignIn from './components/SignIn';
import Header from './components/Header';
import CustomerAnalyticsDashboard from './components/CustomerAnalyticsDashboard';
import WebsiteAnalyticsDashboard from './components/WebsiteAnalyticsDashboard';
import RealTimeHealthDashboard from './components/RealTimeHealthDashboard';
import CustomerJourneyDashboard from './components/CustomerJourneyDashboard';
import CompetitiveIntelligenceDashboard from './components/CompetitiveIntelligenceDashboard';
import CreateCampaign from './components/CreateCampaign';
import CustomerSuccessIntelligence from './components/CustomerSuccessIntelligence';
import ExecutiveIntelligenceDashboard from './components/ExecutiveIntelligenceDashboard';
import GrowthAccelerationEngine from './components/GrowthAccelerationEngine';
import AdminPortal from './components/AdminPortal';
import GrowthIntelligenceSuite from './components/GrowthIntelligenceSuite';
import ProductIntelligenceHub from './components/ProductIntelligenceHub';
import IntegrationDataHub from './components/IntegrationDataHub';
import ComplianceGovernanceSuite from './components/ComplianceGovernanceSuite';
import AICommandCenter from './components/AICommandCenter';
import WebsiteIntelligenceHub from './components/WebsiteIntelligenceHub';
import Training from './components/Training';
import Support from './components/Support';
import KnowledgeBase from './components/KnowledgeBase';
import SubscriptionManager from './components/SubscriptionManager';
import LiveChatWidget from './components/LiveChatWidget';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function AppContent() {
  // Get authentication state from context
  const { user, isAuthenticated, logout, apiCall } = useAuth();

  // Application state
  const [currentPage, setCurrentPage] = useState('customer-analytics-dashboard');
  const [analyticsSection, setAnalyticsSection] = useState('customer'); // 'customer' or 'website'
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
  // State for announcements
  const [announcements, setAnnouncements] = useState([]);
  const [roiForecastingData, setRoiForecastingData] = useState(null);

  // Load announcements
  useEffect(() => {
    const loadAnnouncements = async () => {
      try {
        const response = await apiCall('/api/banners/active');
        const data = await response.json();
        setAnnouncements(data.banners || []);
      } catch (error) {
        console.error('Error loading announcements:', error);
        // Set demo announcement
        setAnnouncements([
          {
            id: 1,
            message: "🎓 New Training Session: Advanced SEO Strategies - December 20, 2PM EST. Register now!",
            banner_type: "info",
            is_active: true,
            is_dismissible: true
          }
        ]);
      }
    };
    
    if (isAuthenticated) {
      loadAnnouncements();
    }
  }, [isAuthenticated, apiCall]);

  const dismissAnnouncement = (id) => {
    setAnnouncements(prev => prev.filter(ann => ann.id !== id));
  };

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
    // The AuthContext will handle the authentication state
    setCurrentPage('customer-analytics-dashboard');
    setAnalyticsSection('customer');
  };

  const handleSignOut = async () => {
    try {
      await logout();
      setCurrentPage('customer-analytics-dashboard');
      setAnalyticsSection('customer');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  // Data loading on authentication
  useEffect(() => {
    if (isAuthenticated) {
      loadData();
    } else {
      // Set loading to false for unauthenticated users so SignIn page can show
      setLoading(false);
    }
  }, [isAuthenticated]);

  const loadData = async () => {
    try {
      setLoading(true);
      console.log('Loading Customer Mind IQ data...');
      
      // Load basic data first - essential for dashboard
      try {
        console.log('Loading basic dashboard data...');
        const basicDataPromise = Promise.all([
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
        
        // Add timeout for basic data (reduced to 10 seconds)
        const basicTimeout = new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Basic data timeout after 10 seconds')), 10000)
        );
        
        const [customersRes, campaignsRes, analyticsRes] = await Promise.race([basicDataPromise, basicTimeout]);
        
        setCustomers(customersRes.data);
        setCampaigns(campaignsRes.data);
        setAnalytics(analyticsRes.data);
        
        console.log('Basic data loaded successfully');
      } catch (error) {
        console.error('Basic data loading failed:', error);
        // Set fallback data for core functionality
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
      }
      
      // CRITICAL: Always set loading to false after basic data
      setLoading(false);
      console.log('Customer Mind IQ core data loaded successfully');
      
      // Load additional modules in background (non-blocking)
      // These failures won't prevent the dashboard from loading
      const loadModulesInBackground = async () => {
        const moduleTimeout = 5000; // 5 second timeout per module
        
        // Marketing Automation Pro
        try {
          console.log('Loading Marketing Automation Pro data...');
          const marketingTimeout = new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Marketing timeout')), moduleTimeout)
          );
          await Promise.race([loadMarketingData(), marketingTimeout]);
        } catch (err) {
          console.error('Marketing data load failed:', err);
          // Set default marketing data
          setMarketingDashboard({ modules: {} });
          setMultiChannelData({ dashboard: {} });
          setAbTestingData({ dashboard: {} });
          setDynamicContentData({ dashboard: {} });
          setLeadScoringData({ dashboard: {} });
          setReferralData({ dashboard: {} });
        }
        
        // Advanced Features
        try {
          console.log('Loading Advanced Features data...');
          const advancedTimeout = new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Advanced features timeout')), moduleTimeout)
          );
          await Promise.race([loadAdvancedFeaturesData(), advancedTimeout]);
        } catch (err) {
          console.error('Advanced features data load failed:', err);
          // Set default advanced data
          setAdvancedDashboard({ modules: {} });
          setBehavioralClusteringData({ dashboard: {} });
          setChurnPreventionData({ dashboard: {} });
          setCrossSellIntelligenceData({ dashboard: {} });
          setAdvancedPricingData({ dashboard: {} });
          setSentimentAnalysisData({ dashboard: {} });
        }
        
        // Revenue Analytics Suite
        try {
          console.log('Loading Revenue Analytics data...');
          const revenueTimeout = new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Revenue analytics timeout')), moduleTimeout)
          );
          await Promise.race([loadRevenueAnalyticsData(), revenueTimeout]);
        } catch (err) {
          console.error('Revenue analytics data load failed:', err);
          // Set default revenue data
          setRevenueDashboard({ modules: {} });
          setRevenueForecastingData({ dashboard: {} });
          setPriceOptimizationData({ dashboard: {} });
          setProfitMarginData({ dashboard: {} });
          setSubscriptionAnalyticsData({ dashboard: {} });
          setFinancialReportingData({ dashboard: {} });
        }
        
        // Analytics & Insights
        try {
          console.log('Loading Analytics & Insights data...');
          const analyticsTimeout = new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Analytics insights timeout')), moduleTimeout)
          );
          await Promise.race([loadAnalyticsInsightsData(), analyticsTimeout]);
        } catch (err) {
          console.error('Analytics insights data load failed:', err);
          // Set default analytics insights data
          setAnalyticsInsightsDashboard({ modules: {} });
          setCustomerJourneyData({ dashboard_data: {} });
          setRevenueAttributionData({ dashboard_data: {} });
          setCohortAnalysisData({ dashboard_data: {} });
          setCompetitiveIntelligenceData({ dashboard_data: {} });
          setRoiForecastingData({ dashboard_data: {} });
        }
        
        console.log('Background module loading completed');
      };
      
      // Start background loading but don't wait for it
      loadModulesInBackground();
      
      console.log('Customer Mind IQ core data loaded successfully');
    } catch (error) {
      console.error('Critical error loading data:', error);
      // Ensure we have minimum viable data
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
      // Always set loading to false to prevent hanging
      setLoading(false);
      console.log('Customer Mind IQ loading complete - dashboard ready');
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
        analyticsSection={analyticsSection}
      />
      
      {/* Announcement Banner */}
      {announcements.filter(ann => ann.active).map(announcement => (
        <div key={announcement.id} className={`${
          announcement.type === 'warning' ? 'bg-yellow-600/90' :
          announcement.type === 'error' ? 'bg-red-600/90' :
          'bg-blue-600/90'
        } text-white py-3 px-6 text-center relative`}>
          <div className="container mx-auto flex items-center justify-between">
            <div className="flex-1 text-sm">{announcement.message}</div>
            {announcement.dismissible && (
              <button
                onClick={() => dismissAnnouncement(announcement.id)}
                className="ml-4 text-white/80 hover:text-white text-lg leading-none"
              >
                ×
              </button>
            )}
          </div>
        </div>
      ))}
      
      <div className="container mx-auto px-6 py-8">
        {currentPage === 'customer-analytics-dashboard' && (
          <CustomerAnalyticsDashboard 
            dashboardData={analytics}
            customerData={{ dashboard_data: { total_customers: customers.length } }}
            marketingData={{ leadScoringData, campaigns_count: campaigns.length }}
            revenueAnalyticsData={{ revenueForecastingData, roi: 3.4 }}
            advancedFeaturesData={advancedDashboard}
            onNavigate={handleNavigate}
          />
        )}
        
        {currentPage === 'real-time-health' && (
          <RealTimeHealthDashboard 
            onNavigate={handleNavigate}
          />
        )}
        
        {currentPage === 'customer-journey' && (
          <CustomerJourneyDashboard 
            onNavigate={handleNavigate}
          />
        )}
        
        {currentPage === 'competitive-intelligence' && (
          <CompetitiveIntelligenceDashboard 
            onNavigate={handleNavigate}
          />
        )}
        
        {currentPage === 'website-analytics-dashboard' && (
          <WebsiteAnalyticsDashboard 
            analyticsInsightsDashboard={analyticsInsightsDashboard}
            onNavigate={handleNavigate}
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
        
        {/* Customer Success Intelligence Module */}
        {currentPage === 'customer-success' && (
          <CustomerSuccessIntelligence />
        )}
        
        {/* Executive Intelligence Dashboard Module */}
        {currentPage === 'executive' && (
          <ExecutiveIntelligenceDashboard />
        )}
        
        {/* Growth Acceleration Engine Module */}
        {currentPage === 'growth-acceleration' && (
          <GrowthAccelerationEngine />
        )}
        
        {/* Secure Admin Portal Module - Requires Admin Role */}
        {currentPage === 'admin-portal' && (
          <AdminPortal />
        )}
        
        {/* Growth Intelligence Suite Module */}
        {currentPage === 'growth' && (
          <GrowthIntelligenceSuite />
        )}
        
        {/* Product Intelligence Hub Module */}
        {currentPage === 'product' && (
          <ProductIntelligenceHub />
        )}
        
        {/* Integration & Data Management Hub Module */}
        {currentPage === 'integration' && (
          <IntegrationDataHub />
        )}
        
        {/* Compliance & Governance Suite Module */}
        {currentPage === 'compliance' && (
          <ComplianceGovernanceSuite />
        )}
        
        {/* AI Command Center Module */}
        {currentPage === 'ai-command' && (
          <AICommandCenter />
        )}
        
        {/* Website Intelligence Hub Module */}
        {currentPage === 'website-intelligence' && (
          <WebsiteIntelligenceHub />
        )}
        
        {/* Training Center Module */}
        {currentPage === 'training' && (
          <Training />
        )}
        
        {/* Knowledge Base Module */}
        {currentPage === 'knowledge-base' && (
          <KnowledgeBase />
        )}
        
        {/* Support Center Module */}
        {currentPage === 'support' && (
          <Support />
        )}
        
        {/* Subscription Manager Module */}
        {currentPage === 'subscription' && (
          <SubscriptionManager />
        )}
        
        {currentPage === 'create' && (
          <CreateCampaign 
            campaigns={campaigns}
            newCampaign={newCampaign}
            setNewCampaign={setNewCampaign}
            handleCreateCampaign={createCampaign}
          />
        )}
        
        {/* Marketing Automation Pro Module */}
        {currentPage === 'marketing' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white">Marketing Automation Pro</h1>
                <p className="text-slate-400 mt-2">AI-powered multi-channel marketing orchestration</p>
              </div>
              <div className="flex items-center space-x-2">
                <Badge className="bg-green-500/20 text-green-400">AI Powered</Badge>
                <Badge className="bg-blue-500/20 text-blue-400">5 Microservices</Badge>
              </div>
            </div>

            {/* Marketing Dashboard Summary */}
            <div className="grid gap-6 md:grid-cols-5">
              <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <Megaphone className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {multiChannelData?.dashboard?.campaigns_count || 15}
                    </div>
                    <div className="text-xs text-purple-200">Multi-Channel</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <TestTube className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {abTestingData?.dashboard?.active_tests || 8}
                    </div>
                    <div className="text-xs text-blue-200">A/B Tests</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <Palette className="h-8 w-8 text-green-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {dynamicContentData?.dashboard?.templates_count || 24}
                    </div>
                    <div className="text-xs text-green-200">Dynamic Content</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <Target className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {leadScoringData?.dashboard?.qualified_leads || 147}
                    </div>
                    <div className="text-xs text-orange-200">Lead Scoring</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-pink-600/20 to-pink-800/20 border-pink-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <Gift className="h-8 w-8 text-pink-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {referralData?.dashboard?.active_referrals || 89}
                    </div>
                    <div className="text-xs text-pink-200">Referral Program</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Marketing Microservices Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              
              {/* Multi-Channel Orchestration */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Megaphone className="w-5 h-5 mr-2 text-purple-400" />
                    Multi-Channel Orchestration
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Cross-channel campaign management
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Active Campaigns</span>
                      <span className="text-purple-400 font-semibold">
                        {multiChannelData?.dashboard?.campaigns_count || 15}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Channels</span>
                      <span className="text-green-400 font-semibold">
                        {multiChannelData?.dashboard?.channels_count || 5}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Avg Engagement</span>
                      <span className="text-blue-400 font-semibold">
                        {multiChannelData?.dashboard?.avg_engagement || '24.5%'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* A/B Testing */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <TestTube className="w-5 h-5 mr-2 text-blue-400" />
                    A/B Test Automation
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    AI-powered testing optimization
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Active Tests</span>
                      <span className="text-blue-400 font-semibold">
                        {abTestingData?.dashboard?.active_tests || 8}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Winning Variants</span>
                      <span className="text-green-400 font-semibold">
                        {abTestingData?.dashboard?.winning_variants || 12}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Uplift Rate</span>
                      <span className="text-green-400 font-semibold">
                        {abTestingData?.dashboard?.avg_uplift || '+18.3%'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Dynamic Content */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Palette className="w-5 h-5 mr-2 text-green-400" />
                    Dynamic Content
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Real-time personalization
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Templates</span>
                      <span className="text-green-400 font-semibold">
                        {dynamicContentData?.dashboard?.templates_count || 24}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Personalization</span>
                      <span className="text-purple-400 font-semibold">
                        {dynamicContentData?.dashboard?.personalization_rate || '87.5%'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Engagement</span>
                      <span className="text-blue-400 font-semibold">
                        {dynamicContentData?.dashboard?.engagement_uplift || '+32.1%'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Lead Scoring */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Target className="w-5 h-5 mr-2 text-orange-400" />
                    Lead Scoring Enhancement
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    AI-driven lead qualification
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Qualified Leads</span>
                      <span className="text-orange-400 font-semibold">
                        {leadScoringData?.dashboard?.qualified_leads || 147}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Avg Score</span>
                      <span className="text-blue-400 font-semibold">
                        {leadScoringData?.dashboard?.average_score || 78}/100
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Conversion Rate</span>
                      <span className="text-green-400 font-semibold">
                        {leadScoringData?.dashboard?.conversion_rate || '24.8%'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Referral Program */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Gift className="w-5 h-5 mr-2 text-pink-400" />
                    Referral Program
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Viral marketing optimization
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Active Referrals</span>
                      <span className="text-pink-400 font-semibold">
                        {referralData?.dashboard?.active_referrals || 89}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Viral Coefficient</span>
                      <span className="text-green-400 font-semibold">
                        {referralData?.dashboard?.viral_coefficient || '1.42'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Revenue Impact</span>
                      <span className="text-green-400 font-semibold">
                        ${(referralData?.dashboard?.revenue_impact || 24750).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* AI Insights */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-cyan-400" />
                    AI Marketing Insights
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Strategic recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <Alert className="bg-blue-500/10 border-blue-500/20">
                      <Brain className="h-4 w-4 text-blue-400" />
                      <AlertDescription className="text-blue-300 text-sm">
                        A/B test shows 23% higher engagement with personalized subject lines
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-green-500/10 border-green-500/20">
                      <TrendingUp className="h-4 w-4 text-green-400" />
                      <AlertDescription className="text-green-300 text-sm">
                        Multi-channel campaigns outperform single-channel by 47%
                      </AlertDescription>
                    </Alert>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
        
        {/* Revenue Analytics Suite Module */}
        {currentPage === 'revenue' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white">Revenue Analytics Suite</h1>
                <p className="text-slate-400 mt-2">Comprehensive revenue intelligence and forecasting</p>
              </div>
              <div className="flex items-center space-x-2">
                <Badge className="bg-green-500/20 text-green-400">Revenue Focus</Badge>
                <Badge className="bg-blue-500/20 text-blue-400">5 Analytics</Badge>
              </div>
            </div>

            {/* Revenue Analytics Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              
              {/* Revenue Forecasting */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-blue-400" />
                    Revenue Forecasting
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    AI-powered revenue predictions
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Forecast Accuracy</span>
                      <span className="text-green-400 font-semibold">
                        {revenueForecastingData?.dashboard?.accuracy || '88.7%'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Next Quarter</span>
                      <span className="text-blue-400 font-semibold">
                        ${(revenueForecastingData?.dashboard?.next_quarter || 542000).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Growth Rate</span>
                      <span className="text-green-400 font-semibold">
                        {revenueForecastingData?.dashboard?.growth_rate || '+24.1%'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Price Optimization */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <DollarSign className="w-5 h-5 mr-2 text-green-400" />
                    Price Optimization
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Dynamic pricing strategies
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Price Tests</span>
                      <span className="text-blue-400 font-semibold">
                        {priceOptimizationData?.dashboard?.active_tests || 12}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Revenue Uplift</span>
                      <span className="text-green-400 font-semibold">
                        {priceOptimizationData?.dashboard?.revenue_uplift || '+18.5%'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Optimal Prices</span>
                      <span className="text-purple-400 font-semibold">
                        {priceOptimizationData?.dashboard?.optimized_products || 47}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Profit Margin Analysis */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <PieChart className="w-5 h-5 mr-2 text-orange-400" />
                    Profit Margin Analysis
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Cost optimization insights
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Overall Margin</span>
                      <span className="text-orange-400 font-semibold">
                        {profitMarginData?.dashboard?.overall_margin || '55.1%'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Best Product</span>
                      <span className="text-green-400 font-semibold">
                        {profitMarginData?.dashboard?.best_margin || '72.3%'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Optimization</span>
                      <span className="text-blue-400 font-semibold">
                        {profitMarginData?.dashboard?.opportunities || 15} ops
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Subscription Analytics */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Activity className="w-5 h-5 mr-2 text-purple-400" />
                    Subscription Analytics
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    MRR and churn insights
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">MRR</span>
                      <span className="text-purple-400 font-semibold">
                        ${(subscriptionAnalyticsData?.dashboard?.mrr || 198000).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Churn Rate</span>
                      <span className="text-red-400 font-semibold">
                        {subscriptionAnalyticsData?.dashboard?.churn_rate || '3.2%'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">LTV</span>
                      <span className="text-green-400 font-semibold">
                        ${(subscriptionAnalyticsData?.dashboard?.ltv || 3240).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Financial Reporting */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <BarChart3 className="w-5 h-5 mr-2 text-cyan-400" />
                    Financial Reporting
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Executive dashboards & KPIs
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Health Score</span>
                      <span className="text-green-400 font-semibold">
                        {financialReportingData?.dashboard?.health_score || '85.6'}/100
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">YTD Revenue</span>
                      <span className="text-blue-400 font-semibold">
                        ${(financialReportingData?.dashboard?.ytd_revenue || 891000).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Budget Variance</span>
                      <span className="text-green-400 font-semibold">
                        {financialReportingData?.dashboard?.budget_variance?.overall_variance_score ? 
                          `${financialReportingData.dashboard.budget_variance.overall_variance_score}/100` : 
                          '85.2/100'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Revenue AI Insights */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-cyan-400" />
                    Revenue AI Insights
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Strategic revenue optimization
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <Alert className="bg-green-500/10 border-green-500/20">
                      <TrendingUp className="h-4 w-4 text-green-400" />
                      <AlertDescription className="text-green-300 text-sm">
                        Q4 revenue trending 24% above forecast
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-blue-500/10 border-blue-500/20">
                      <DollarSign className="h-4 w-4 text-blue-400" />
                      <AlertDescription className="text-blue-300 text-sm">
                        Price optimization identified $47K opportunity
                      </AlertDescription>
                    </Alert>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
        
        {/* Advanced Features Expansion Module */}
        {currentPage === 'advanced' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white">Advanced Features Expansion</h1>
                <p className="text-slate-400 mt-2">AI-driven customer intelligence and behavioral analysis</p>
              </div>
              <div className="flex items-center space-x-2">
                <Badge className="bg-orange-500/20 text-orange-400">Advanced AI</Badge>
                <Badge className="bg-blue-500/20 text-blue-400">5 Features</Badge>
              </div>
            </div>

            {/* Advanced Features Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              
              {/* Behavioral Clustering */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Users className="w-5 h-5 mr-2 text-blue-400" />
                    Behavioral Clustering
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    AI customer segmentation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Customers Analyzed</span>
                      <span className="text-blue-400 font-semibold">
                        {behavioralClusteringData?.dashboard?.summary_metrics?.total_customers_analyzed || 574}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Clusters Found</span>
                      <span className="text-green-400 font-semibold">
                        {behavioralClusteringData?.dashboard?.summary_metrics?.clusters_identified || 5}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Conversion Rate</span>
                      <span className="text-purple-400 font-semibold">
                        {behavioralClusteringData?.dashboard?.summary_metrics?.average_conversion_rate || '56.4'}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Churn Prevention AI */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <TrendingDown className="w-5 h-5 mr-2 text-red-400" />
                    Churn Prevention AI
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Predictive churn modeling
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">At-Risk Customers</span>
                      <span className="text-red-400 font-semibold">
                        {churnPreventionData?.dashboard?.summary_metrics?.at_risk_customers || 25}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Prevention Rate</span>
                      <span className="text-green-400 font-semibold">
                        {churnPreventionData?.dashboard?.success_metrics?.retention_success_rate || '78.4'}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Critical Cases</span>
                      <span className="text-orange-400 font-semibold">
                        {churnPreventionData?.dashboard?.summary_metrics?.critical_risk_count || 7}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Cross-Sell Intelligence */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <ShoppingCart className="w-5 h-5 mr-2 text-green-400" />
                    Cross-Sell Intelligence
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    AI product recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Opportunities</span>
                      <span className="text-green-400 font-semibold">
                        {crossSellIntelligenceData?.dashboard?.summary_metrics?.total_cross_sell_opportunities || 385}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Potential Revenue</span>
                      <span className="text-blue-400 font-semibold">
                        ${(crossSellIntelligenceData?.dashboard?.summary_metrics?.total_potential_revenue || 74575).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Conversion Rate</span>
                      <span className="text-purple-400 font-semibold">
                        {crossSellIntelligenceData?.dashboard?.summary_metrics?.avg_cross_sell_conversion_rate || '24.6'}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Advanced Pricing Optimization */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Settings className="w-5 h-5 mr-2 text-purple-400" />
                    Pricing Optimization
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    AI-driven price sensitivity
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Analyzed</span>
                      <span className="text-purple-400 font-semibold">
                        {advancedPricingData?.dashboard?.summary_metrics?.total_customers_analyzed || 684}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Experiments</span>
                      <span className="text-blue-400 font-semibold">
                        {advancedPricingData?.dashboard?.summary_metrics?.active_pricing_experiments || 2}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Revenue Boost</span>
                      <span className="text-green-400 font-semibold">
                        ${(advancedPricingData?.dashboard?.summary_metrics?.revenue_optimization_this_month || 47800).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Sentiment Analysis */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <MessageSquare className="w-5 h-5 mr-2 text-cyan-400" />
                    Sentiment Analysis
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    NLP communication analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Communications</span>
                      <span className="text-cyan-400 font-semibold">
                        {sentimentAnalysisData?.dashboard?.summary_metrics?.total_communications_analyzed || 568}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Positive Sentiment</span>
                      <span className="text-green-400 font-semibold">
                        {sentimentAnalysisData?.dashboard?.summary_metrics?.positive_sentiment_percentage || '41.2'}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Active Alerts</span>
                      <span className="text-orange-400 font-semibold">
                        {sentimentAnalysisData?.dashboard?.summary_metrics?.active_alerts || 4}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Advanced AI Insights */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-cyan-400" />
                    Advanced AI Insights
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Strategic behavioral recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <Alert className="bg-orange-500/10 border-orange-500/20">
                      <AlertTriangle className="h-4 w-4 text-orange-400" />
                      <AlertDescription className="text-orange-300 text-sm">
                        7 customers at high churn risk need immediate attention
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-green-500/10 border-green-500/20">
                      <TrendingUp className="h-4 w-4 text-green-400" />
                      <AlertDescription className="text-green-300 text-sm">
                        Cross-sell opportunities could generate $74K additional revenue
                      </AlertDescription>
                    </Alert>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
        
        {/* Analytics & Insights Module */}
        {currentPage === 'analytics' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white">Analytics & Insights</h1>
                <p className="text-slate-400 mt-2">Advanced analytics, attribution, and competitive intelligence</p>
              </div>  
              <div className="flex items-center space-x-2">
                <Badge className="bg-indigo-500/20 text-indigo-400">Advanced Analytics</Badge>
                <Badge className="bg-blue-500/20 text-blue-400">5 Modules</Badge>
              </div>
            </div>

            {/* Analytics & Insights Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              
              {/* Customer Journey Mapping */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <ArrowRightLeft className="w-5 h-5 mr-2 text-blue-400" />
                    Customer Journey Mapping
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    AI-powered journey visualization
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Customers Analyzed</span>
                      <span className="text-blue-400 font-semibold">
                        {customerJourneyData?.dashboard_data?.overview?.total_customers_analyzed || 50}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Journey Paths</span>
                      <span className="text-green-400 font-semibold">
                        {customerJourneyData?.dashboard_data?.overview?.total_journey_paths || 10}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Conversion Rate</span>
                      <span className="text-purple-400 font-semibold">
                        {((customerJourneyData?.dashboard_data?.overview?.avg_conversion_rate || 0.24) * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Revenue Attribution */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <DollarSign className="w-5 h-5 mr-2 text-green-400" />
                    Revenue Attribution
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Multi-touch attribution models
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Total Revenue</span>
                      <span className="text-green-400 font-semibold">
                        ${(revenueAttributionData?.dashboard_data?.overview?.total_revenue || 485000).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Overall ROI</span>
                      <span className="text-blue-400 font-semibold">
                        {(revenueAttributionData?.dashboard_data?.overview?.overall_roi || 2.88).toFixed(1)}x
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Avg LTV</span>
                      <span className="text-purple-400 font-semibold">
                        ${(revenueAttributionData?.dashboard_data?.overview?.average_ltv || 3240).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Cohort Analysis */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Users className="w-5 h-5 mr-2 text-orange-400" />
                    Cohort Analysis
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Retention forecasting & insights
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Customers Analyzed</span>
                      <span className="text-orange-400 font-semibold">
                        {cohortAnalysisData?.dashboard_data?.overview?.total_customers_analyzed || 400}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Cohorts</span>
                      <span className="text-blue-400 font-semibold">
                        {cohortAnalysisData?.dashboard_data?.overview?.total_cohorts || 12}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">1-Month Retention</span>
                      <span className="text-green-400 font-semibold">
                        {((cohortAnalysisData?.dashboard_data?.overview?.retention_1_month || 0.68) * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Competitive Intelligence */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Eye className="w-5 h-5 mr-2 text-purple-400" />
                    Competitive Intelligence
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Market monitoring & analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Competitors</span>
                      <span className="text-purple-400 font-semibold">
                        {competitiveIntelligenceData?.dashboard_data?.overview?.competitors_monitored || 5}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Data Points</span>
                      <span className="text-blue-400 font-semibold">
                        {competitiveIntelligenceData?.dashboard_data?.overview?.data_points_collected || 150}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Market Sentiment</span>
                      <span className="text-green-400 font-semibold">
                        {((competitiveIntelligenceData?.dashboard_data?.overview?.market_sentiment_score || 0.35) * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* ROI Forecasting */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-cyan-400" />
                    ROI Forecasting
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    ML-powered campaign predictions
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Planned Budget</span>
                      <span className="text-cyan-400 font-semibold">
                        ${(roiForecastingData?.dashboard_data?.overview?.total_planned_budget || 28000).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Predicted Revenue</span>
                      <span className="text-green-400 font-semibold">
                        ${(roiForecastingData?.dashboard_data?.overview?.total_predicted_revenue || 89600).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Portfolio ROI</span>
                      <span className="text-blue-400 font-semibold">
                        {(roiForecastingData?.dashboard_data?.overview?.portfolio_roi || 2.2).toFixed(1)}x
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Analytics AI Insights */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-cyan-400" />
                    Analytics AI Insights
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Strategic analytics recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <Alert className="bg-blue-500/10 border-blue-500/20">
                      <TrendingUp className="h-4 w-4 text-blue-400" />
                      <AlertDescription className="text-blue-300 text-sm">
                        Customer journey optimization could improve conversion by 24%
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-green-500/10 border-green-500/20">
                      <DollarSign className="h-4 w-4 text-green-400" />
                      <AlertDescription className="text-green-300 text-sm">
                        Attribution model shows email driving highest ROI at 4.4x
                      </AlertDescription>
                    </Alert>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>

      {/* Live Chat Widget - Always available for premium users */}
      {user && <LiveChatWidget />}
    </div>
  );
}

// Main App component wrapped with AuthProvider
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
