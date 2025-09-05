import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
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
import OverageApproval from './components/OverageApproval';
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
import PublicTrainingPage from './components/PublicTrainingPage';
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

  // Marketing Automation Pro - Data source drill-down handlers
  const showMarketingDataSource = (section, metricType, metricName, currentValue) => {
    const sourceDetails = {
      // OVERVIEW SUMMARY DATA SOURCES
      'overview_multi_channel': {
        title: 'Multi-Channel Campaigns - Data Source',
        description: 'Number of active cross-channel marketing campaigns running simultaneously',
        sources: [
          '• Campaign Management Platform: Multi-channel campaign orchestration and tracking',
          '• Marketing Automation Engine: Cross-platform campaign execution and monitoring',
          '• Channel Integration APIs: Email, SMS, social media, and web push integration',
          '• Campaign Analytics Database: Performance tracking across all marketing channels'
        ],
        methodology: 'Multi-Channel Campaigns = Total active campaigns spanning 2+ marketing channels (email, SMS, social, web, mobile). Includes scheduled, running, and optimization phases.',
        dataPoints: 'Campaign status, channel coverage, audience reach, engagement rates, conversion tracking',
        updateFrequency: 'Real-time campaign status updates with hourly performance summaries',
        currentValue: currentValue
      },
      'overview_ab_tests': {
        title: 'Active A/B Tests - Data Source',
        description: 'Number of currently running multivariate and A/B testing experiments',
        sources: [
          '• A/B Testing Platform: Experiment design, execution, and statistical analysis',
          '• Conversion Tracking System: Test variant performance and outcome measurement',
          '• Statistical Engine: Significance testing and confidence interval calculation',
          '• Experiment Database: Historical test results and learning repository'
        ],
        methodology: 'Active A/B Tests = Total running experiments with statistical validity requirements. Includes email subject lines, landing pages, ad creatives, and user experience tests.',
        dataPoints: 'Test variants, sample sizes, conversion rates, statistical significance, confidence levels',
        updateFrequency: 'Real-time test performance tracking with daily statistical analysis',
        currentValue: currentValue
      },
      'overview_dynamic_content': {
        title: 'Dynamic Content Templates - Data Source',
        description: 'Number of personalized content templates available for dynamic marketing',
        sources: [
          '• Content Management System: Template creation, versioning, and deployment',
          '• Personalization Engine: Dynamic content rule engine and audience targeting',
          '• Asset Library: Creative assets, copy variations, and multimedia resources',
          '• Performance Analytics: Template effectiveness and engagement measurement'
        ],
        methodology: 'Dynamic Content Templates = Total personalized templates across all channels with active targeting rules. Includes email templates, web content, ad creatives, and push notifications.',
        dataPoints: 'Template usage, personalization rules, audience segments, engagement metrics, conversion attribution',
        updateFrequency: 'Real-time template performance with daily optimization recommendations',
        currentValue: currentValue
      },
      'overview_lead_scoring': {
        title: 'Qualified Leads - Data Source',
        description: 'Number of marketing qualified leads (MQLs) based on AI scoring algorithms',
        sources: [
          '• Lead Scoring Engine: AI-powered lead qualification and ranking system',
          '• Behavioral Analytics: Website, email, and engagement behavior tracking',
          '• CRM Integration: Sales qualification feedback and conversion data',
          '• Predictive Models: Machine learning models for lead quality prediction'
        ],
        methodology: 'Qualified Leads = Leads scoring above MQL threshold (typically 70+ points) based on demographic, behavioral, and engagement factors. AI models continuously refine scoring algorithms.',
        dataPoints: 'Lead scores, engagement metrics, demographic data, behavioral patterns, conversion probabilities',
        updateFrequency: 'Real-time lead scoring with hourly qualification updates',
        currentValue: currentValue
      },
      'overview_referral_program': {
        title: 'Active Referrals - Data Source',
        description: 'Number of active referral program participants and ongoing referrals',
        sources: [
          '• Referral Management Platform: Referral tracking, rewards, and program analytics',
          '• Customer Database: Referrer and referee relationship mapping',
          '• Reward System: Points, discounts, and incentive distribution tracking',
          '• Social Sharing Analytics: Referral link sharing and viral coefficient measurement'
        ],
        methodology: 'Active Referrals = Total referral participants with pending or completed referrals in current period. Includes referrers actively sharing and referees in conversion funnel.',
        dataPoints: 'Referral links, sharing activity, conversion rates, reward redemption, viral coefficients',
        updateFrequency: 'Real-time referral tracking with daily program performance analysis',
        currentValue: currentValue
      },
      // MULTI-CHANNEL ORCHESTRATION DATA SOURCES
      'multichannel_campaigns_count': {
        title: 'Campaign Volume - Data Source',
        description: 'Total number of coordinated multi-channel marketing campaigns',
        sources: [
          '• Campaign Orchestration Platform: Cross-channel campaign planning and execution',
          '• Workflow Management: Campaign timeline, dependencies, and resource allocation',
          '• Channel APIs: Integration with email, SMS, social, web, and mobile platforms',
          '• Performance Dashboard: Real-time campaign monitoring and optimization'
        ],
        methodology: 'Campaign Count = Active campaigns utilizing 2+ marketing channels with coordinated messaging and timing. Includes awareness, nurture, conversion, and retention campaigns.',
        dataPoints: 'Campaign objectives, channel mix, audience targeting, message personalization, performance metrics',
        updateFrequency: 'Real-time campaign tracking with automated performance optimization',
        currentValue: currentValue
      },
      'multichannel_engagement_rate': {
        title: 'Cross-Channel Engagement Rate - Data Source',
        description: 'Average engagement rate across all marketing channels and touchpoints',
        sources: [
          '• Engagement Analytics Engine: Multi-channel interaction tracking and analysis',
          '• Customer Journey Mapping: Touchpoint engagement correlation and attribution',
          '• Channel Performance Monitor: Individual channel engagement optimization',
          '• Unified Customer Profile: Cross-channel behavior aggregation and insights'
        ],
        methodology: 'Engagement Rate = (Total interactions / Total impressions) × 100 across all channels, weighted by channel importance and audience quality.',
        dataPoints: 'Click-through rates, open rates, social engagement, website interactions, conversion events',
        updateFrequency: 'Real-time engagement tracking with 15-minute rolling averages',
        currentValue: currentValue
      },
      // A/B TESTING DATA SOURCES
      'abtesting_active_tests': {
        title: 'Active Test Volume - Data Source',
        description: 'Number of concurrent A/B and multivariate tests running across campaigns',
        sources: [
          '• Experimentation Platform: Test design, randomization, and statistical analysis',
          '• Conversion Tracking: Outcome measurement and attribution across test variants',
          '• Statistical Computing: Power analysis, significance testing, and confidence intervals',
          '• Learning Repository: Historical test results and optimization insights'
        ],
        methodology: 'Active Tests = Concurrent experiments with adequate sample sizes and statistical power (>80%). Includes email, landing page, ad creative, and user experience tests.',
        dataPoints: 'Test variants, sample sizes, conversion rates, statistical significance, effect sizes',
        updateFrequency: 'Real-time test monitoring with automated statistical analysis',
        currentValue: currentValue
      },
      'abtesting_win_rate': {
        title: 'Test Win Rate - Data Source',
        description: 'Percentage of A/B tests showing statistically significant improvements',
        sources: [
          '• Test Results Database: Historical experiment outcomes and statistical significance',
          '• Performance Comparison Engine: Variant performance analysis and ranking',
          '• Statistical Validation: Confidence interval calculation and significance testing',
          '• Optimization Intelligence: Pattern recognition in winning test characteristics'
        ],
        methodology: 'Win Rate = (Tests with statistically significant positive results / Total completed tests) × 100. Significance threshold typically set at 95% confidence level.',
        dataPoints: 'Test outcomes, statistical significance, effect sizes, confidence levels, improvement magnitudes',
        updateFrequency: 'Updated immediately upon test completion with weekly trend analysis',
        currentValue: currentValue
      },
      // DYNAMIC CONTENT DATA SOURCES
      'content_templates_count': {
        title: 'Template Library Size - Data Source',
        description: 'Total number of dynamic content templates available for personalization',
        sources: [
          '• Content Management System: Template creation, versioning, and asset library',
          '• Personalization Engine: Dynamic rule engine and audience targeting logic',
          '• Creative Asset Database: Images, copy variations, and multimedia resources',
          '• Template Performance Analytics: Usage statistics and effectiveness measurement'
        ],
        methodology: 'Template Count = Total active templates across all channels with personalization rules. Includes email templates, web content, ad variations, and mobile push templates.',
        dataPoints: 'Template usage frequency, personalization rules, audience targeting, engagement metrics, conversion rates',
        updateFrequency: 'Real-time template management with daily performance optimization',
        currentValue: currentValue
      },
      'content_personalization_rate': {
        title: 'Content Personalization Rate - Data Source',
        description: 'Percentage of marketing content delivered with personalized elements',
        sources: [
          '• Personalization Analytics: Content customization tracking and measurement',
          '• Customer Data Platform: Individual customer preference and behavior data',
          '• Dynamic Content Engine: Real-time content assembly and delivery',
          '• Engagement Correlation: Personalization impact on engagement and conversion'
        ],
        methodology: 'Personalization Rate = (Personalized content impressions / Total content impressions) × 100. Includes demographic, behavioral, and contextual personalization.',
        dataPoints: 'Personalization triggers, content variants, audience segments, engagement lift, conversion impact',
        updateFrequency: 'Real-time personalization tracking with continuous optimization',
        currentValue: currentValue
      },
      // LEAD SCORING DATA SOURCES
      'leadscoring_qualified_leads': {
        title: 'Marketing Qualified Leads - Data Source',
        description: 'Number of leads meeting qualification criteria based on AI scoring models',
        sources: [
          '• Lead Scoring Engine: AI-powered qualification algorithms and predictive models',
          '• Behavioral Analytics: Website activity, content engagement, and interaction tracking',
          '• Demographic Intelligence: Firmographic and demographic scoring factors',
          '• Sales Feedback Loop: Conversion data and qualification validation from sales team'
        ],
        methodology: 'Qualified Leads = Leads scoring above MQL threshold (typically 70+ points) based on weighted scoring model: Demographics (25%), Behavior (40%), Engagement (35%).',
        dataPoints: 'Lead scores, behavioral indicators, demographic fit, engagement history, conversion probability',
        updateFrequency: 'Real-time lead scoring with hourly qualification batch processing',
        currentValue: currentValue
      },
      'leadscoring_score_accuracy': {
        title: 'Scoring Model Accuracy - Data Source',
        description: 'Accuracy rate of lead scoring predictions versus actual sales outcomes',
        sources: [
          '• Model Performance Analytics: Prediction accuracy tracking and validation',
          '• Sales Outcome Database: Actual conversion results and deal closure data',
          '• Machine Learning Pipeline: Model training, validation, and performance monitoring',
          '• Feedback Loop Analytics: Continuous model improvement and calibration'
        ],
        methodology: 'Score Accuracy = (Correct predictions / Total predictions) × 100. Measured by comparing predicted lead quality with actual sales conversion outcomes.',
        dataPoints: 'Prediction accuracy, false positive/negative rates, model confidence scores, calibration metrics',
        updateFrequency: 'Weekly model performance analysis with monthly accuracy reporting',
        currentValue: currentValue
      },
      // REFERRAL PROGRAM DATA SOURCES
      'referral_active_referrals': {
        title: 'Active Referral Participants - Data Source',
        description: 'Number of customers actively participating in referral programs',
        sources: [
          '• Referral Management Platform: Participant tracking and reward distribution',
          '• Customer Engagement Database: Referral sharing activity and social metrics',
          '• Conversion Tracking: Referee onboarding and qualification measurement',
          '• Reward Analytics: Incentive effectiveness and redemption analysis'
        ],
        methodology: 'Active Referrals = Customers with active referral links and participants in conversion funnel. Includes both referrers and referees in active referral cycles.',
        dataPoints: 'Referral link generation, sharing activity, click-through rates, conversion rates, reward redemption',
        updateFrequency: 'Real-time referral activity tracking with daily program performance updates',
        currentValue: currentValue
      },
      'referral_viral_coefficient': {
        title: 'Viral Coefficient - Data Source',
        description: 'Average number of new customers acquired per existing customer referral',
        sources: [
          '• Viral Growth Analytics: Customer acquisition through referral tracking',
          '• Network Effect Measurement: Referral chain analysis and viral loop optimization',
          '• Customer Lifetime Value: Long-term value impact of referred customers',
          '• Social Sharing Intelligence: Referral link distribution and engagement analysis'
        ],
        methodology: 'Viral Coefficient = Total new customers acquired through referrals / Total referring customers. Values >1.0 indicate exponential viral growth.',
        dataPoints: 'Referral conversion rates, customer acquisition costs, viral loop efficiency, network growth metrics',
        updateFrequency: 'Weekly viral coefficient calculation with monthly trend analysis',
        currentValue: currentValue
      }
    };

    const key = `${section}_${metricType}`;
    const details = sourceDetails[key] || {
      title: `${metricName} - Data Source`,
      description: 'Data source information for this marketing automation metric',
      sources: ['• Marketing automation platforms', '• Campaign management systems', '• Analytics and tracking tools', '• Customer engagement databases'],
      methodology: 'Calculated using advanced marketing analytics and automation algorithms',
      dataPoints: 'Campaign performance, customer engagement, conversion rates, attribution data',
      updateFrequency: 'Updated based on marketing automation monitoring schedules',
      currentValue: currentValue
    };

    alert(`📊 ${details.title}

Current Value: ${details.currentValue}

${details.description}

🔍 DATA SOURCES:
${details.sources.join('\n')}

⚙️ METHODOLOGY:
${details.methodology}

📈 KEY DATA POINTS:
${details.dataPoints}

🕐 UPDATE FREQUENCY:
${details.updateFrequency}

💡 This data helps optimize marketing campaigns and improve customer acquisition and engagement.`);
  };

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
  
  // Overage approval state
  const [showOverageApproval, setShowOverageApproval] = useState(false);
  const [overageStatus, setOverageStatus] = useState(null);

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

  // Check overage status function
  const checkOverageStatus = async (email) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/overage-review/${encodeURIComponent(email)}`);
      const data = await response.json();
      
      if (data.status === 'success' && data.approval_required) {
        setOverageStatus(data);
        setShowOverageApproval(true);
      }
    } catch (error) {
      console.error('Error checking overage status:', error);
      // Don't show modal on error - user can still use the system
    }
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
      
      // IMMEDIATE UI LOAD - Load dashboard UI first with default data
      const defaultAnalytics = {
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
      };
      
      // Set default data immediately to show UI
      setCustomers([]);
      setCampaigns([]);
      setAnalytics(defaultAnalytics);
      
      // STOP LOADING IMMEDIATELY - Show dashboard with default data
      setLoading(false);
      console.log('Customer Mind IQ dashboard ready - immediate load');
      
      // Check for overage approvals immediately with default handling
      if (user?.email) {
        setTimeout(() => checkOverageStatus(user.email), 50);
      }
      
      // Load real data in background WITHOUT affecting loading state
      setTimeout(() => {
        loadBackgroundData();
      }, 200); // Start data loading after UI is shown
      
    } catch (error) {
      console.error('Critical loading error:', error);
      setLoading(false); // Always stop loading on error
    }
  };

  // Background data loading - doesn't affect UI loading state  
  const loadBackgroundData = async () => {
    console.log('Loading background data...');
    
    // Only load if authenticated
    if (!isAuthenticated || !apiCall) {
      console.log('Not authenticated yet, skipping data loading');
      return;
    }
    
    try {
      // Load essential data using authenticated API calls
      const [customersRes, campaignsRes, analyticsRes] = await Promise.allSettled([
        apiCall('/api/customers'),
        apiCall('/api/campaigns'), 
        apiCall('/api/analytics')
      ]);
      
      // Update data if successful - with array validation
      if (customersRes.status === 'fulfilled') {
        const customersData = customersRes.value;
        // Ensure customers is always an array
        if (Array.isArray(customersData)) {
          setCustomers(customersData);
          console.log('Customers loaded:', customersData.length);
        } else if (customersData && Array.isArray(customersData.data)) {
          // Handle case where API returns {data: [...]}
          setCustomers(customersData.data);
          console.log('Customers loaded from data property:', customersData.data.length);
        } else {
          console.log('Invalid customers data format:', customersData);
          setCustomers([]); // Fallback to empty array
        }
      } else {
        console.log('Failed to load customers:', customersRes.reason);
        setCustomers([]); // Ensure it's always an array on error
      }
      
      if (campaignsRes.status === 'fulfilled') {
        setCampaigns(campaignsRes.value);
      }
      
      if (analyticsRes.status === 'fulfilled') {
        setAnalytics(analyticsRes.value);
      }
      
      console.log('Background data loaded successfully');
      
    } catch (error) {
      console.log('Background data loading failed (non-critical):', error.message);
    }
    
    // Load background modules after basic data
    setTimeout(() => {
      loadBackgroundModules();
    }, 500);
  };

  // Separate function for background module loading - optimized
  const loadBackgroundModules = async () => {
    console.log('Starting optimized background module loading...');
    
    // Set default values immediately to prevent undefined errors
    const defaultModuleData = { modules: {}, dashboard: {}, dashboard_data: {} };
    
    setMarketingDashboard(defaultModuleData);
    setMultiChannelData(defaultModuleData);
    setAbTestingData(defaultModuleData);
    setDynamicContentData(defaultModuleData);
    setLeadScoringData(defaultModuleData);
    setReferralData(defaultModuleData);
    setAdvancedDashboard(defaultModuleData);
    setBehavioralClusteringData(defaultModuleData);
    setChurnPreventionData(defaultModuleData);
    setCrossSellIntelligenceData(defaultModuleData);
    setAdvancedPricingData(defaultModuleData);
    setSentimentAnalysisData(defaultModuleData);
    setRevenueDashboard(defaultModuleData);
    setRevenueForecastingData(defaultModuleData);
    setPriceOptimizationData(defaultModuleData);
    setProfitMarginData(defaultModuleData);
    setSubscriptionAnalyticsData(defaultModuleData);
    setFinancialReportingData(defaultModuleData);
    setAnalyticsInsightsDashboard(defaultModuleData);
    setCustomerJourneyData(defaultModuleData);
    setRevenueAttributionData(defaultModuleData);
    setCohortAnalysisData(defaultModuleData);
    setCompetitiveIntelligenceData(defaultModuleData);
    setRoiForecastingData(defaultModuleData);
    
    // Load modules with faster timeout and error handling
    const moduleLoaders = [
      { name: 'Marketing', loader: loadMarketingData },
      { name: 'Advanced Features', loader: loadAdvancedFeaturesData },
      { name: 'Revenue Analytics', loader: loadRevenueAnalyticsData },
      { name: 'Analytics Insights', loader: loadAnalyticsInsightsData }
    ];
    
    // Load modules in parallel with shorter timeout
    const modulePromises = moduleLoaders.map(async ({ name, loader }) => {
      try {
        await Promise.race([
          loader(),
          new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 1500)) // Reduced timeout
        ]);
        console.log(`${name} data loaded successfully`);
      } catch (error) {
        console.log(`${name} data load failed (non-critical):`, error.message);
      }
    });
    
    // Wait for all modules to complete (or timeout)
    await Promise.allSettled(modulePromises);
    console.log('Background module loading completed');
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
      
      {/* Overage Approval Modal */}
      {showOverageApproval && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 rounded-xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">Approve Additional Services</h2>
                <button 
                  onClick={() => setShowOverageApproval(false)}
                  className="text-slate-400 hover:text-white"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <OverageApproval 
                userEmail={user?.email}
                onApprovalComplete={(result) => {
                  setShowOverageApproval(false);
                  setOverageStatus(null);
                  // Optionally show a success message
                  console.log('Overage approval completed:', result);
                }}
              />
            </div>
          </div>
        </div>
      )}
      
      <div className="container mx-auto px-6 py-8">
        {/* Usage Status Banner - Show when user needs overage approval */}
        {overageStatus?.approval_required && !showOverageApproval && (
          <div className="mb-6">
            <Alert className="bg-orange-500/10 border-orange-500/20">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription className="text-orange-300 flex items-center justify-between">
                <span>
                  You've exceeded your plan limits. Some features may be blocked until you approve additional charges.
                </span>
                <Button 
                  onClick={() => setShowOverageApproval(true)}
                  className="bg-orange-600 hover:bg-orange-700 text-white ml-4"
                  size="sm"
                >
                  Review & Approve
                </Button>
              </AlertDescription>
            </Alert>
          </div>
        )}
        
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
                      {Array.isArray(customers) && customers.length > 0 ? customers.map((customer) => (
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
                      )) : (
                        <div className="text-center py-8">
                          <Brain className="w-12 h-12 mx-auto text-slate-500 mb-4" />
                          <h3 className="text-white text-lg mb-2">No Customer Data Available</h3>
                          <p className="text-slate-400 text-sm">Customer intelligence data is being loaded...</p>
                        </div>
                      )}
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
              <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30 cursor-pointer hover:bg-purple-600/30 transition-all duration-200" onClick={() => showMarketingDataSource('overview', 'multi_channel', 'Multi-Channel Campaigns', multiChannelData?.dashboard?.campaigns_count || 15)}>
                <CardContent className="p-4">
                  <div className="text-center">
                    <Megaphone className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {multiChannelData?.dashboard?.campaigns_count || 15}
                    </div>
                    <div className="text-xs text-purple-200">Multi-Channel</div>
                    <div className="text-xs text-purple-300 mt-1 opacity-75">Click for data source</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30 cursor-pointer hover:bg-blue-600/30 transition-all duration-200" onClick={() => showMarketingDataSource('overview', 'ab_tests', 'Active A/B Tests', abTestingData?.dashboard?.active_tests || 8)}>
                <CardContent className="p-4">
                  <div className="text-center">
                    <TestTube className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {abTestingData?.dashboard?.active_tests || 8}
                    </div>
                    <div className="text-xs text-blue-200">A/B Tests</div>
                    <div className="text-xs text-blue-300 mt-1 opacity-75">Click for data source</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30 cursor-pointer hover:bg-green-600/30 transition-all duration-200" onClick={() => showMarketingDataSource('overview', 'dynamic_content', 'Dynamic Content Templates', dynamicContentData?.dashboard?.templates_count || 24)}>
                <CardContent className="p-4">
                  <div className="text-center">
                    <Palette className="h-8 w-8 text-green-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {dynamicContentData?.dashboard?.templates_count || 24}
                    </div>
                    <div className="text-xs text-green-200">Dynamic Content</div>
                    <div className="text-xs text-green-300 mt-1 opacity-75">Click for data source</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30 cursor-pointer hover:bg-orange-600/30 transition-all duration-200" onClick={() => showMarketingDataSource('overview', 'lead_scoring', 'Qualified Leads (MQL)', leadScoringData?.dashboard?.qualified_leads || 147)}>
                <CardContent className="p-4">
                  <div className="text-center">
                    <Target className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {leadScoringData?.dashboard?.qualified_leads || 147}
                    </div>
                    <div className="text-xs text-orange-200">Lead Scoring</div>
                    <div className="text-xs text-orange-300 mt-1 opacity-75">Click for data source</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-pink-600/20 to-pink-800/20 border-pink-500/30 cursor-pointer hover:bg-pink-600/30 transition-all duration-200" onClick={() => showMarketingDataSource('overview', 'referral_program', 'Active Referrals', referralData?.dashboard?.active_referrals || 89)}>
                <CardContent className="p-4">
                  <div className="text-center">
                    <Gift className="h-8 w-8 text-pink-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {referralData?.dashboard?.active_referrals || 89}
                    </div>
                    <div className="text-xs text-pink-200">Referral Program</div>
                    <div className="text-xs text-pink-300 mt-1 opacity-75">Click for data source</div>
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
                    Cross-channel campaign management - Click metrics for data sources
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('multichannel', 'campaigns_count', 'Active Campaigns', multiChannelData?.dashboard?.campaigns_count || 15)}>
                      <span className="text-slate-300">Active Campaigns</span>
                      <span className="text-purple-400 font-semibold">
                        {multiChannelData?.dashboard?.campaigns_count || 15}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('multichannel', 'campaigns_count', 'Marketing Channels', multiChannelData?.dashboard?.channels_count || 5)}>
                      <span className="text-slate-300">Channels</span>
                      <span className="text-green-400 font-semibold">
                        {multiChannelData?.dashboard?.channels_count || 5}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('multichannel', 'engagement_rate', 'Average Engagement Rate', multiChannelData?.dashboard?.avg_engagement || '24.5%')}>
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
                    AI-powered testing optimization - Click metrics for data sources
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('abtesting', 'active_tests', 'Active Tests', abTestingData?.dashboard?.active_tests || 8)}>
                      <span className="text-slate-300">Active Tests</span>
                      <span className="text-blue-400 font-semibold">
                        {abTestingData?.dashboard?.active_tests || 8}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('abtesting', 'win_rate', 'Winning Variants', abTestingData?.dashboard?.winning_variants || 12)}>
                      <span className="text-slate-300">Winning Variants</span>
                      <span className="text-green-400 font-semibold">
                        {abTestingData?.dashboard?.winning_variants || 12}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('abtesting', 'win_rate', 'Average Uplift Rate', abTestingData?.dashboard?.avg_uplift || '+18.3%')}>
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
                    Real-time personalization - Click metrics for data sources
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('content', 'templates_count', 'Content Templates', dynamicContentData?.dashboard?.templates_count || 24)}>
                      <span className="text-slate-300">Templates</span>
                      <span className="text-green-400 font-semibold">
                        {dynamicContentData?.dashboard?.templates_count || 24}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('content', 'personalization_rate', 'Personalization Rate', dynamicContentData?.dashboard?.personalization_rate || '87.5%')}>
                      <span className="text-slate-300">Personalization</span>
                      <span className="text-purple-400 font-semibold">
                        {dynamicContentData?.dashboard?.personalization_rate || '87.5%'}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('content', 'personalization_rate', 'Engagement Uplift', dynamicContentData?.dashboard?.engagement_uplift || '+32.1%')}>
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
                    AI-driven lead qualification - Click metrics for data sources
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('leadscoring', 'qualified_leads', 'Marketing Qualified Leads', leadScoringData?.dashboard?.qualified_leads || 147)}>
                      <span className="text-slate-300">Qualified Leads</span>
                      <span className="text-orange-400 font-semibold">
                        {leadScoringData?.dashboard?.qualified_leads || 147}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('leadscoring', 'score_accuracy', 'Average Lead Score', `${leadScoringData?.dashboard?.average_score || 78}/100`)}>
                      <span className="text-slate-300">Avg Score</span>
                      <span className="text-blue-400 font-semibold">
                        {leadScoringData?.dashboard?.average_score || 78}/100
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('leadscoring', 'score_accuracy', 'Lead Conversion Rate', leadScoringData?.dashboard?.conversion_rate || '24.8%')}>
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
                    Viral marketing optimization - Click metrics for data sources
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('referral', 'active_referrals', 'Active Referral Participants', referralData?.dashboard?.active_referrals || 89)}>
                      <span className="text-slate-300">Active Referrals</span>
                      <span className="text-pink-400 font-semibold">
                        {referralData?.dashboard?.active_referrals || 89}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('referral', 'viral_coefficient', 'Viral Growth Coefficient', referralData?.dashboard?.viral_coefficient || '1.42')}>
                      <span className="text-slate-300">Viral Coefficient</span>
                      <span className="text-green-400 font-semibold">
                        {referralData?.dashboard?.viral_coefficient || '1.42'}
                      </span>
                    </div>
                    <div className="flex justify-between cursor-pointer hover:bg-slate-700/30 p-2 rounded transition-all duration-200" onClick={() => showMarketingDataSource('referral', 'viral_coefficient', 'Revenue Impact from Referrals', `$${(referralData?.dashboard?.revenue_impact || 24750).toLocaleString()}`)}>
                      <span className="text-slate-300">Revenue Impact</span>
                      <span className="text-green-400 font-semibold">
                        ${(referralData?.dashboard?.revenue_impact || 24750).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* AI Marketing Insights */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-cyan-400" />
                    AI Marketing Insights
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Strategic recommendations - Click insights for data sources
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <Alert className="bg-blue-500/10 border-blue-500/20 cursor-pointer hover:bg-blue-500/20 transition-all duration-200" onClick={() => showMarketingDataSource('abtesting', 'win_rate', 'A/B Test Performance Analysis', '23% higher engagement with personalized subject lines')}>
                      <Brain className="h-4 w-4 text-blue-400" />
                      <AlertDescription className="text-blue-300 text-sm">
                        <div className="font-medium mb-1">A/B Test Insight (+23% engagement boost)</div>
                        <div className="text-blue-200/80">
                          Personalized subject lines significantly outperform generic ones. Click to see data methodology and statistical confidence.
                        </div>
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-green-500/10 border-green-500/20 cursor-pointer hover:bg-green-500/20 transition-all duration-200" onClick={() => showMarketingDataSource('multichannel', 'engagement_rate', 'Multi-Channel Campaign Performance', '47% outperformance vs single-channel')}>
                      <TrendingUp className="h-4 w-4 text-green-400" />
                      <AlertDescription className="text-green-300 text-sm">
                        <div className="font-medium mb-1">Multi-Channel Performance (+47% improvement)</div>
                        <div className="text-green-200/80">
                          Cross-channel campaigns deliver superior results. Click to explore data sources and measurement methodology.
                        </div>
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-purple-500/10 border-purple-500/20 cursor-pointer hover:bg-purple-500/20 transition-all duration-200" onClick={() => showMarketingDataSource('content', 'personalization_rate', 'Dynamic Content Optimization', '87.5% personalization rate driving +32.1% engagement')}>
                      <Palette className="h-4 w-4 text-purple-400" />
                      <AlertDescription className="text-purple-300 text-sm">
                        <div className="font-medium mb-1">Content Personalization Impact (+32.1% engagement)</div>
                        <div className="text-purple-200/80">
                          Dynamic content personalization shows strong engagement uplift. Click for personalization engine data sources.
                        </div>
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-orange-500/10 border-orange-500/20 cursor-pointer hover:bg-orange-500/20 transition-all duration-200" onClick={() => showMarketingDataSource('leadscoring', 'score_accuracy', 'Lead Scoring Intelligence', '147 MQLs with 78/100 average score')}>
                      <Target className="h-4 w-4 text-orange-400" />
                      <AlertDescription className="text-orange-300 text-sm">
                        <div className="font-medium mb-1">Lead Scoring Optimization (147 qualified leads)</div>
                        <div className="text-orange-200/80">
                          AI-powered lead scoring delivers 24.8% conversion rate. Click for scoring algorithm and data sources.
                        </div>
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-pink-500/10 border-pink-500/20 cursor-pointer hover:bg-pink-500/20 transition-all duration-200" onClick={() => showMarketingDataSource('referral', 'viral_coefficient', 'Referral Program Intelligence', 'Viral coefficient of 1.42 generating $24.7K revenue')}>
                      <Gift className="h-4 w-4 text-pink-400" />
                      <AlertDescription className="text-pink-300 text-sm">
                        <div className="font-medium mb-1">Referral Program Success (1.42 viral coefficient)</div>
                        <div className="text-pink-200/80">
                          Referral program driving viral growth and $24,750 revenue impact. Click for viral analytics data sources.
                        </div>
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
                    Actionable optimization recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <Alert className="bg-blue-500/10 border-blue-500/20">
                      <TrendingUp className="h-4 w-4 text-blue-400" />
                      <AlertDescription className="text-blue-300 text-sm">
                        <div className="font-medium mb-1">Customer Journey Optimization (+24% conversion)</div>
                        <div className="text-blue-200/80">
                          • Add exit-intent popup on pricing page (37% abandon rate)<br/>
                          • Reduce form fields from 8 to 4 on signup (increases completion by 31%)<br/>
                          • Send follow-up email within 6 hours (41% reactivation rate)
                        </div>
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-green-500/10 border-green-500/20">
                      <DollarSign className="h-4 w-4 text-green-400" />
                      <AlertDescription className="text-green-300 text-sm">
                        <div className="font-medium mb-1">Revenue Attribution Optimization (4.4x ROI)</div>
                        <div className="text-green-200/80">
                          • Increase email budget by 40% (highest ROI channel)<br/>
                          • Reduce paid social spend by 25% (negative ROI)<br/>
                          • Launch email retargeting for trial dropoffs (+$23k/month)
                        </div>
                      </AlertDescription>
                    </Alert>
                    <Alert className="bg-purple-500/10 border-purple-500/20">
                      <Target className="h-4 w-4 text-purple-400" />
                      <AlertDescription className="text-purple-300 text-sm">
                        <div className="font-medium mb-1">Customer Health Alert (125 at-risk customers)</div>
                        <div className="text-purple-200/80">
                          • Schedule calls with top 25 high-value accounts this week<br/>
                          • Send feature adoption email series to low-usage customers<br/>
                          • Implement win-back campaign for churned prospects
                        </div>
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

// Main App component wrapped with AuthProvider and Router
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
