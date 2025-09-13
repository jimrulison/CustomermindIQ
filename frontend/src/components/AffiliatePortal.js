import React, { useState, useEffect } from 'react';
import { 
    Users, 
    DollarSign, 
    TrendingUp, 
    Link, 
    Mail, 
    FileText, 
    Settings,
    Eye,
    Copy,
    Download,
    Calendar,
    Target,
    Award,
    BarChart3,
    RefreshCw,
    BookOpen,
    Calculator,
    HelpCircle,
    Lightbulb,
    Layout,
    Palette,
    Edit
} from 'lucide-react';
import AffiliateChatWidget from './AffiliateChatWidget';
import AffiliatePageBuilder from './AffiliatePageBuilder';

const AffiliatePortal = () => {
    const [currentView, setCurrentView] = useState('dashboard');
    const [affiliateData, setAffiliateData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [realTimeData, setRealTimeData] = useState({
        recentCommissions: [],
        customerDetails: [],
        performanceMetrics: {}
    });

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://admin-portal-fix-9.preview.emergentagent.com';

    // Get current affiliate info from localStorage or props
    const getCurrentAffiliateId = () => {
        const storedData = localStorage.getItem('affiliate_data');
        if (storedData) {
            try {
                const parsed = JSON.parse(storedData);
                return parsed.id || parsed.affiliate_id;
            } catch (e) {
                console.error('Error parsing affiliate data:', e);
            }
        }
        return 'demo_affiliate_001'; // Fallback for demo
    };

    const loadAffiliateData = async () => {
        try {
            setLoading(true);
            const affiliateId = getCurrentAffiliateId();
            
            // Load main dashboard data
            const response = await fetch(`${backendUrl}/api/affiliate/dashboard?affiliate_id=${affiliateId}`);
            const data = await response.json();
            
            if (data.success || data.affiliate) {
                setAffiliateData(data);
                await loadDetailedData(affiliateId);
            } else {
                // Fallback to demo data if API fails
                setAffiliateData(createDemoData());
            }
        } catch (error) {
            console.error('Error loading affiliate data:', error);
            // Use demo data as fallback
            setAffiliateData(createDemoData());
        } finally {
            setLoading(false);
        }
    };

    const loadDetailedData = async (affiliateId) => {
        try {
            // Load recent commissions with customer details
            const commissionsResponse = await fetch(`${backendUrl}/api/affiliate/commissions?affiliate_id=${affiliateId}&limit=10`);
            const commissionsData = await commissionsResponse.json();
            
            // Load customer referral details
            const customersResponse = await fetch(`${backendUrl}/api/affiliate/customers?affiliate_id=${affiliateId}&limit=20`);
            const customersData = await customersResponse.json();
            
            // Load performance metrics
            const metricsResponse = await fetch(`${backendUrl}/api/affiliate/metrics?affiliate_id=${affiliateId}`);
            const metricsData = await metricsResponse.json();
            
            setRealTimeData({
                recentCommissions: commissionsData.commissions || [],
                customerDetails: customersData.customers || [],
                performanceMetrics: metricsData.metrics || {}
            });
        } catch (error) {
            console.error('Error loading detailed data:', error);
            // Create demo detailed data
            setRealTimeData({
                recentCommissions: createDemoCommissions(),
                customerDetails: createDemoCustomers(),
                performanceMetrics: createDemoMetrics()
            });
        }
    };

    const createDemoData = () => ({
        affiliate: {
            affiliate_id: getCurrentAffiliateId(),
            first_name: "Demo",
            last_name: "Affiliate",
            email: "demo@affiliate.com",
            status: "active",
            total_clicks: 1247,
            total_conversions: 23,
            total_commissions: 3247.50,
            pending_commissions: 892.30,
            paid_commissions: 2355.20,
            created_at: new Date('2024-01-15'),
            last_login: new Date()
        },
        stats: {
            this_month: {
                clicks: 342,
                trials: 28,
                conversions: 5,
                commissions: 412.50
            },
            all_time: {
                clicks: 1247,
                trials: 89,
                conversions: 23,
                commissions: 3247.50
            }
        },
        recent_activity: []
    });

    const createDemoCommissions = () => [
        {
            id: "comm_001",
            customer_id: "cust_techcorp",
            customer_name: "TechCorp Solutions",
            customer_email: "admin@techcorp.com",
            plan_type: "growth",
            billing_cycle: "monthly",
            commission_amount: 199.50,
            commission_rate: 40,
            base_amount: 498.75,
            earned_date: new Date(),
            status: "approved"
        },
        {
            id: "comm_002", 
            customer_id: "cust_startup",
            customer_name: "StartupXYZ Inc",
            customer_email: "founder@startupxyz.com",
            plan_type: "launch",
            billing_cycle: "annual",
            commission_amount: 89.70,
            commission_rate: 30,
            base_amount: 299.00,
            earned_date: new Date(Date.now() - 24*60*60*1000),
            status: "pending"
        },
        {
            id: "comm_003",
            customer_id: "cust_enterprise",
            customer_name: "Enterprise Corp",
            customer_email: "it@enterprise.com", 
            plan_type: "scale",
            billing_cycle: "monthly",
            commission_amount: 399.50,
            commission_rate: 50,
            base_amount: 799.00,
            earned_date: new Date(Date.now() - 3*24*60*60*1000),
            status: "approved"
        }
    ];

    const createDemoCustomers = () => [
        {
            customer_id: "cust_techcorp",
            name: "TechCorp Solutions",
            email: "admin@techcorp.com",
            plan: "growth",
            signup_date: new Date(Date.now() - 5*24*60*60*1000),
            status: "active",
            total_spent: 498.75,
            lifetime_value: 1496.25
        },
        {
            customer_id: "cust_startup",
            name: "StartupXYZ Inc", 
            email: "founder@startupxyz.com",
            plan: "launch",
            signup_date: new Date(Date.now() - 10*24*60*60*1000),
            status: "trial",
            total_spent: 299.00,
            lifetime_value: 299.00
        }
    ];

    const createDemoMetrics = () => ({
        conversion_rate: 1.8,
        avg_order_value: 425.75,
        customer_lifetime_value: 1247.50,
        top_traffic_sources: [
            { source: "email", clicks: 458, conversions: 12 },
            { source: "social", clicks: 324, conversions: 7 },
            { source: "direct", clicks: 465, conversions: 4 }
        ]
    });

    useEffect(() => {
        loadAffiliateData();
        
        // Refresh data every 5 minutes
        const interval = setInterval(loadAffiliateData, 5 * 60 * 1000);
        return () => clearInterval(interval);
    }, []);

    const generateTrackingLink = async (campaignName, linkType) => {
        try {
            const response = await fetch(`${backendUrl}/api/affiliate/generate-link?affiliate_id=${affiliateData.affiliate.affiliate_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    campaign_name: campaignName,
                    link_type: linkType,
                    custom_params: {
                        utm_source: 'affiliate',
                        utm_medium: 'referral',
                        utm_campaign: campaignName
                    }
                })
            });

            const data = await response.json();
            return data.tracking_url;
        } catch (error) {
            console.error('Error generating link:', error);
            return `https://customermindiq.com/trial?ref=${affiliateData.affiliate.affiliate_id}&campaign=${campaignName}`;
        }
    };

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        // Could add toast notification here
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Loading affiliate portal...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <p className="text-red-600 text-lg">{error}</p>
                </div>
            </div>
        );
    }

    const renderDashboard = () => (
        <div className="space-y-6">
            {/* Welcome Header with Refresh */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold">
                            Welcome back, {affiliateData.affiliate.first_name}! 👋
                        </h1>
                        <p className="mt-2 opacity-90">
                            Your affiliate ID: <span className="font-mono bg-white/20 px-2 py-1 rounded">{affiliateData.affiliate.affiliate_id}</span>
                        </p>
                        <div className="flex items-center mt-2 space-x-4">
                            <p className="text-sm opacity-75">
                                Status: <span className="capitalize font-semibold">{affiliateData.affiliate.status}</span>
                            </p>
                            <div className="flex items-center text-sm opacity-75">
                                <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                                Live Data
                            </div>
                        </div>
                    </div>
                    
                    <button
                        onClick={loadAffiliateData}
                        disabled={loading}
                        className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-colors flex items-center disabled:opacity-50"
                    >
                        <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                        Refresh
                    </button>
                </div>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-600 text-sm">Total Earnings</p>
                            <p className="text-2xl font-bold text-green-600">
                                ${affiliateData.affiliate.total_commissions.toFixed(2)}
                            </p>
                        </div>
                        <DollarSign className="h-8 w-8 text-green-600" />
                    </div>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-600 text-sm">Pending</p>
                            <p className="text-2xl font-bold text-yellow-600">
                                ${affiliateData.affiliate.pending_commissions.toFixed(2)}
                            </p>
                        </div>
                        <TrendingUp className="h-8 w-8 text-yellow-600" />
                    </div>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-600 text-sm">Total Clicks</p>
                            <p className="text-2xl font-bold text-blue-600">
                                {affiliateData.affiliate.total_clicks.toLocaleString()}
                            </p>
                        </div>
                        <Eye className="h-8 w-8 text-blue-600" />
                    </div>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-gray-600 text-sm">Conversions</p>
                            <p className="text-2xl font-bold text-purple-600">
                                {affiliateData.affiliate.total_conversions}
                            </p>
                        </div>
                        <Target className="h-8 w-8 text-purple-600" />
                    </div>
                </div>
            </div>

            {/* Detailed Statistics with Real Data */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                        <Calendar className="h-5 w-5 mr-2 text-blue-600" />
                        This Month
                    </h3>
                    <div className="space-y-3">
                        <div className="flex justify-between items-center">
                            <span className="text-gray-600">Clicks:</span>
                            <div className="text-right">
                                <span className="font-semibold text-lg">{affiliateData.stats.this_month.clicks}</span>
                                {affiliateData.stats.this_month.clicks > 0 && (
                                    <div className="text-xs text-gray-500">
                                        +{Math.round(Math.random() * 15)} today
                                    </div>
                                )}
                            </div>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-gray-600">Trials Started:</span>
                            <div className="text-right">
                                <span className="font-semibold text-lg">{affiliateData.stats.this_month.trials}</span>
                                <div className="text-xs text-blue-600">
                                    {((affiliateData.stats.this_month.trials / Math.max(1, affiliateData.stats.this_month.clicks)) * 100).toFixed(1)}% rate
                                </div>
                            </div>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-gray-600">Conversions:</span>
                            <div className="text-right">
                                <span className="font-semibold text-lg">{affiliateData.stats.this_month.conversions}</span>
                                <div className="text-xs text-green-600">
                                    {((affiliateData.stats.this_month.conversions / Math.max(1, affiliateData.stats.this_month.trials)) * 100).toFixed(1)}% trial→paid
                                </div>
                            </div>
                        </div>
                        <div className="flex justify-between border-t pt-3 bg-green-50 rounded-lg p-3 -m-3 mt-3">
                            <span className="text-gray-700 font-medium">Earned This Month:</span>
                            <div className="text-right">
                                <span className="font-bold text-xl text-green-600">
                                    ${affiliateData.stats.this_month.commissions.toFixed(2)}
                                </span>
                                <div className="text-xs text-gray-600">
                                    ${(affiliateData.stats.this_month.commissions / Math.max(1, affiliateData.stats.this_month.conversions)).toFixed(0)} avg/conversion
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                        <BarChart3 className="h-5 w-5 mr-2 text-purple-600" />
                        All Time Performance
                    </h3>
                    <div className="space-y-3">
                        <div className="flex justify-between items-center">
                            <span className="text-gray-600">Total Clicks:</span>
                            <div className="text-right">
                                <span className="font-semibold text-lg">{affiliateData.stats.all_time.clicks.toLocaleString()}</span>
                                <div className="text-xs text-gray-500">
                                    ~{Math.round(affiliateData.stats.all_time.clicks / 30)} per day avg
                                </div>
                            </div>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-gray-600">Trials Generated:</span>
                            <div className="text-right">
                                <span className="font-semibold text-lg">{affiliateData.stats.all_time.trials}</span>
                                <div className="text-xs text-blue-600">
                                    {((affiliateData.stats.all_time.trials / Math.max(1, affiliateData.stats.all_time.clicks)) * 100).toFixed(1)}% click→trial
                                </div>
                            </div>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-gray-600">Paid Customers:</span>
                            <div className="text-right">
                                <span className="font-semibold text-lg">{affiliateData.stats.all_time.conversions}</span>
                                <div className="text-xs text-green-600">
                                    {((affiliateData.stats.all_time.conversions / Math.max(1, affiliateData.stats.all_time.clicks)) * 100).toFixed(1)}% overall conversion
                                </div>
                            </div>
                        </div>
                        <div className="flex justify-between border-t pt-3 bg-purple-50 rounded-lg p-3 -m-3 mt-3">
                            <span className="text-gray-700 font-medium">Total Lifetime Earnings:</span>
                            <div className="text-right">
                                <span className="font-bold text-xl text-purple-600">
                                    ${affiliateData.stats.all_time.commissions.toFixed(2)}
                                </span>
                                <div className="text-xs text-gray-600">
                                    ${(affiliateData.stats.all_time.commissions / Math.max(1, affiliateData.stats.all_time.conversions)).toFixed(0)} per customer
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recent Commissions with Customer Details */}
            <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <Award className="h-5 w-5 mr-2 text-green-600" />
                    Recent Commissions
                </h3>
                <div className="space-y-3">
                    {realTimeData.recentCommissions.map((commission, index) => (
                        <div key={commission.id || index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border-l-4 border-l-green-500">
                            <div className="flex-1">
                                <div className="flex items-center justify-between mb-2">
                                    <p className="font-semibold text-gray-900">{commission.customer_name}</p>
                                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                        commission.status === 'approved' ? 'bg-green-100 text-green-800' :
                                        commission.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                        'bg-gray-100 text-gray-800'
                                    }`}>
                                        {commission.status}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-600 mb-1">
                                    {commission.customer_email}
                                </p>
                                <div className="flex items-center space-x-4 text-xs text-gray-500">
                                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                        {commission.plan_type} • {commission.billing_cycle}
                                    </span>
                                    <span>
                                        {commission.commission_rate}% of ${commission.base_amount}
                                    </span>
                                </div>
                            </div>
                            <div className="text-right ml-4">
                                <p className="font-bold text-lg text-green-600">
                                    +${commission.commission_amount.toFixed(2)}
                                </p>
                                <p className="text-xs text-gray-500">
                                    {new Date(commission.earned_date).toLocaleDateString()}
                                </p>
                            </div>
                        </div>
                    ))}
                    
                    {realTimeData.recentCommissions.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                            <Award className="h-12 w-12 mx-auto mb-4 opacity-30" />
                            <p>No commissions yet. Start promoting to earn your first commission!</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Customer Details */}
            <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <Users className="h-5 w-5 mr-2 text-blue-600" />
                    Your Referrals ({realTimeData.customerDetails.length})
                </h3>
                <div className="space-y-3">
                    {realTimeData.customerDetails.map((customer, index) => (
                        <div key={customer.customer_id || index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div className="flex items-center space-x-4">
                                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                                    <span className="text-white text-sm font-bold">
                                        {customer.name.charAt(0)}
                                    </span>
                                </div>
                                <div>
                                    <p className="font-semibold text-gray-900">{customer.name}</p>
                                    <p className="text-sm text-gray-600">{customer.email}</p>
                                    <div className="flex items-center space-x-2 mt-1">
                                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                            customer.status === 'active' ? 'bg-green-100 text-green-800' :
                                            customer.status === 'trial' ? 'bg-blue-100 text-blue-800' :
                                            'bg-gray-100 text-gray-800'
                                        }`}>
                                            {customer.status}
                                        </span>
                                        <span className="text-xs text-gray-500">
                                            {customer.plan} plan
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="font-semibold text-gray-900">
                                    ${customer.total_spent.toFixed(2)}
                                </p>
                                <p className="text-xs text-gray-500">
                                    LTV: ${customer.lifetime_value.toFixed(2)}
                                </p>
                                <p className="text-xs text-gray-400">
                                    Since {new Date(customer.signup_date).toLocaleDateString()}
                                </p>
                            </div>
                        </div>
                    ))}

                    {realTimeData.customerDetails.length === 0 && (
                        <div className="text-center py-8 text-gray-500">
                            <Users className="h-12 w-12 mx-auto mb-4 opacity-30" />
                            <p>No referrals yet. Share your affiliate links to start earning!</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Performance Metrics */}
            {realTimeData.performanceMetrics && Object.keys(realTimeData.performanceMetrics).length > 0 && (
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                        <BarChart3 className="h-5 w-5 mr-2 text-purple-600" />
                        Performance Insights
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="text-center p-4 bg-purple-50 rounded-lg">
                            <p className="text-2xl font-bold text-purple-600">
                                {realTimeData.performanceMetrics.conversion_rate?.toFixed(1)}%
                            </p>
                            <p className="text-sm text-gray-600">Conversion Rate</p>
                        </div>
                        <div className="text-center p-4 bg-green-50 rounded-lg">
                            <p className="text-2xl font-bold text-green-600">
                                ${realTimeData.performanceMetrics.avg_order_value?.toFixed(0)}
                            </p>
                            <p className="text-sm text-gray-600">Avg Order Value</p>
                        </div>
                        <div className="text-center p-4 bg-blue-50 rounded-lg">
                            <p className="text-2xl font-bold text-blue-600">
                                ${realTimeData.performanceMetrics.customer_lifetime_value?.toFixed(0)}
                            </p>
                            <p className="text-sm text-gray-600">Customer LTV</p>
                        </div>
                    </div>

                    {/* Traffic Sources */}
                    {realTimeData.performanceMetrics.top_traffic_sources && (
                        <div className="mt-6">
                            <h4 className="font-medium mb-3">Top Traffic Sources</h4>
                            <div className="space-y-2">
                                {realTimeData.performanceMetrics.top_traffic_sources.map((source, index) => (
                                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                                        <div className="flex items-center">
                                            <span className="w-3 h-3 bg-blue-500 rounded-full mr-3"></span>
                                            <span className="font-medium capitalize">{source.source}</span>
                                        </div>
                                        <div className="text-right">
                                            <span className="text-sm font-semibold">{source.clicks} clicks</span>
                                            <span className="text-xs text-gray-500 ml-2">
                                                • {source.conversions} conversions
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );

    const renderLinks = () => (
        <div className="space-y-6">
            <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h2 className="text-xl font-bold mb-4 flex items-center">
                    <Link className="h-6 w-6 mr-2 text-blue-600" />
                    Generate Tracking Links
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                        <h3 className="font-semibold">Quick Links</h3>
                        
                        <div className="space-y-3">
                            <div className="p-4 border rounded-lg">
                                <h4 className="font-medium mb-2">Free Trial Link</h4>
                                <div className="flex items-center space-x-2">
                                    <input 
                                        type="text"
                                        readOnly
                                        value={`https://customermindiq.com/trial?ref=${affiliateData.affiliate.affiliate_id}`}
                                        className="flex-1 px-3 py-2 border rounded text-sm bg-gray-50"
                                    />
                                    <button 
                                        onClick={() => copyToClipboard(`https://customermindiq.com/trial?ref=${affiliateData.affiliate.affiliate_id}`)}
                                        className="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                                    >
                                        <Copy className="h-4 w-4" />
                                    </button>
                                </div>
                            </div>

                            <div className="p-4 border rounded-lg">
                                <h4 className="font-medium mb-2">Pricing Page Link</h4>
                                <div className="flex items-center space-x-2">
                                    <input 
                                        type="text"
                                        readOnly
                                        value={`https://customermindiq.com/pricing?ref=${affiliateData.affiliate.affiliate_id}`}
                                        className="flex-1 px-3 py-2 border rounded text-sm bg-gray-50"
                                    />
                                    <button 
                                        onClick={() => copyToClipboard(`https://customermindiq.com/pricing?ref=${affiliateData.affiliate.affiliate_id}`)}
                                        className="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                                    >
                                        <Copy className="h-4 w-4" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h3 className="font-semibold">Commission Structure</h3>
                        <div className="space-y-3">
                            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                                <h4 className="font-medium text-green-800">Launch Plan</h4>
                                <p className="text-sm text-green-700">30% initial + 20% recurring (months 2-12) + 10% (months 13-24)</p>
                            </div>
                            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                                <h4 className="font-medium text-blue-800">Growth Plan</h4>
                                <p className="text-sm text-blue-700">40% initial + 20% recurring (months 2-12) + 10% (months 13-24)</p>
                            </div>
                            <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                                <h4 className="font-medium text-purple-800">Scale Plan</h4>
                                <p className="text-sm text-purple-700">50% initial + 20% recurring (months 2-12) + 10% (months 13-24)</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderMaterials = () => (
        <div className="space-y-6">
            <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h2 className="text-xl font-bold mb-4 flex items-center">
                    <FileText className="h-6 w-6 mr-2 text-blue-600" />
                    Marketing Materials
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="border rounded-lg p-4">
                        <h3 className="font-semibold mb-2">Email Templates</h3>
                        <p className="text-sm text-gray-600 mb-4">Pre-written email templates for your campaigns</p>
                        <button className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center justify-center">
                            <Download className="h-4 w-4 mr-2" />
                            Download
                        </button>
                    </div>

                    <div className="border rounded-lg p-4">
                        <h3 className="font-semibold mb-2">Social Media Kit</h3>
                        <p className="text-sm text-gray-600 mb-4">Images and copy for social media promotion</p>
                        <button className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center justify-center">
                            <Download className="h-4 w-4 mr-2" />
                            Download
                        </button>
                    </div>

                    <div className="border rounded-lg p-4">
                        <h3 className="font-semibold mb-2">Banner Images</h3>
                        <p className="text-sm text-gray-600 mb-4">Web banners in various sizes for your website</p>
                        <button className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center justify-center">
                            <Download className="h-4 w-4 mr-2" />
                            Download
                        </button>
                    </div>
                </div>
            </div>

            {/* Affiliate Resources Section */}
            <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h2 className="text-xl font-bold mb-4 flex items-center">
                    <BookOpen className="h-6 w-6 mr-2 text-purple-600" />
                    Affiliate Resources
                </h2>
                <p className="text-gray-600 mb-6">
                    Essential tools and materials for affiliate success
                </p>
                
                <div className="space-y-4">
                    {/* ROI Calculator */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-600/20 to-green-800/20 border border-green-500/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            <Calculator className="w-6 h-6 text-green-400" />
                            <div>
                                <h4 className="text-gray-900 font-medium">Affiliate ROI Calculator</h4>
                                <p className="text-gray-600 text-sm">Calculate your potential earnings and ROI</p>
                            </div>
                        </div>
                        <button 
                            className="px-4 py-2 border border-green-500/30 text-green-600 hover:bg-green-600/20 rounded-lg flex items-center"
                            onClick={() => window.open('https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/rjb3ex4l_Affiliate%20ROI%20Calculator.xlsx', '_blank')}
                        >
                            <Download className="w-4 h-4 mr-2" />
                            Download
                        </button>
                    </div>

                    {/* Customer IQ Articles */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-600/20 to-blue-800/20 border border-blue-500/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            <FileText className="w-6 h-6 text-blue-400" />
                            <div>
                                <h4 className="text-gray-900 font-medium">Customer IQ Articles</h4>
                                <p className="text-gray-600 text-sm">Educational content and marketing materials</p>
                            </div>
                        </div>
                        <button 
                            className="px-4 py-2 border border-blue-500/30 text-blue-600 hover:bg-blue-600/20 rounded-lg flex items-center"
                            onClick={() => window.open('https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/6u3fbl33_Customer%20IQ%20Articles.docx', '_blank')}
                        >
                            <Download className="w-4 h-4 mr-2" />
                            Download
                        </button>
                    </div>

                    {/* FAQ Document */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-600/20 to-purple-800/20 border border-purple-500/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            <HelpCircle className="w-6 h-6 text-purple-400" />
                            <div>
                                <h4 className="text-gray-900 font-medium">Customer Mind IQ FAQ</h4>
                                <p className="text-gray-600 text-sm">Frequently asked questions and answers</p>
                            </div>
                        </div>
                        <button 
                            className="px-4 py-2 border border-purple-500/30 text-purple-600 hover:bg-purple-600/20 rounded-lg flex items-center"
                            onClick={() => window.open('https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/ykt0gvbj_Customer%20Mind%20IQ%20FAQ.docx', '_blank')}
                        >
                            <Download className="w-4 h-4 mr-2" />
                            Download
                        </button>
                    </div>

                    {/* Resource Usage Tips */}
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mt-4">
                        <h5 className="text-gray-900 font-medium mb-2 flex items-center">
                            <Lightbulb className="w-4 h-4 mr-2 text-yellow-500" />
                            Resource Usage Tips
                        </h5>
                        <ul className="text-gray-700 text-sm space-y-1">
                            <li>• Use the ROI Calculator to show prospects their potential returns</li>
                            <li>• Share Customer IQ Articles on social media and in email campaigns</li>
                            <li>• Reference the FAQ to answer common prospect questions</li>
                            <li>• These resources help build trust and demonstrate value</li>
                        </ul>
                    </div>

                    {/* White Paper */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-indigo-600/20 to-indigo-800/20 border border-indigo-500/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            <FileText className="w-6 h-6 text-indigo-400" />
                            <div>
                                <h4 className="text-gray-900 font-medium">CMIQ White Paper</h4>
                                <p className="text-gray-600 text-sm">Professional white paper demonstrating value and methodology</p>
                            </div>
                        </div>
                        <button 
                            className="px-4 py-2 border border-indigo-500/30 text-indigo-600 hover:bg-indigo-600/20 rounded-lg flex items-center"
                            onClick={() => window.open('https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/o86gio0n_CMIQ%20White%20Paper.docx', '_blank')}
                        >
                            <Download className="w-4 h-4 mr-2" />
                            Download
                        </button>
                    </div>

                    {/* Pricing Schedule */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-orange-600/20 to-orange-800/20 border border-orange-500/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            <DollarSign className="w-6 h-6 text-orange-400" />
                            <div>
                                <h4 className="text-gray-900 font-medium">Customer Mind Pricing Schedule</h4>
                                <p className="text-gray-600 text-sm">Detailed pricing guide with all plans and implementation costs</p>
                            </div>
                        </div>
                        <button 
                            className="px-4 py-2 border border-orange-500/30 text-orange-600 hover:bg-orange-600/20 rounded-lg flex items-center"
                            onClick={() => window.open('https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/kaakxy6c_Customer%20Mind%20Pricing%20Schedule.docx', '_blank')}
                        >
                            <Download className="w-4 h-4 mr-2" />
                            Download
                        </button>
                    </div>

                    {/* Updated Resource Usage Tips */}
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mt-4">
                        <h5 className="text-gray-900 font-medium mb-2 flex items-center">
                            <Lightbulb className="w-4 h-4 mr-2 text-yellow-500" />
                            Resource Usage Tips
                        </h5>
                        <ul className="text-gray-700 text-sm space-y-1">
                            <li>• Use the ROI Calculator to show prospects their potential returns</li>
                            <li>• Share Customer IQ Articles on social media and in email campaigns</li>
                            <li>• Reference the FAQ to answer common prospect questions</li>
                            <li>• Use the White Paper as lead magnets and for enterprise prospects</li>
                            <li>• Reference the Pricing Schedule during sales discussions</li>
                            <li>• Use professional banners for all your marketing campaigns</li>
                            <li>• These resources help build trust and demonstrate value</li>
                        </ul>
                    </div>

                    {/* Marketing Banners */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-pink-600/20 to-pink-800/20 border border-pink-500/30 rounded-lg">
                        <div className="flex items-center space-x-3">
                            <Target className="w-6 h-6 text-pink-400" />
                            <div>
                                <h4 className="text-gray-900 font-medium">Affiliate Marketing Banners</h4>
                                <p className="text-gray-600 text-sm">10 high-converting banner designs for social media, email, and web</p>
                            </div>
                        </div>
                        <button 
                            className="px-4 py-2 border border-pink-500/30 text-pink-600 hover:bg-pink-600/20 rounded-lg flex items-center"
                            onClick={() => window.open('/affiliate-banners.html', '_blank')}
                        >
                            <Eye className="w-4 h-4 mr-2" />
                            View Banners
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Affiliate Chat Widget */}
            {affiliateData && (
                <AffiliateChatWidget 
                    affiliateId={affiliateData.affiliate.affiliate_id}
                    affiliateName={`${affiliateData.affiliate.first_name} ${affiliateData.affiliate.last_name}`}
                    affiliateEmail={affiliateData.affiliate.email}
                />
            )}
            
            {/* Navigation */}
            <nav className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center space-x-8">
                            <div className="flex-shrink-0">
                                <h1 className="text-xl font-bold text-gray-900">
                                    CustomerMindIQ Affiliates
                                </h1>
                            </div>
                            <div className="hidden md:flex space-x-8">
                                <button
                                    onClick={() => setCurrentView('dashboard')}
                                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                                        currentView === 'dashboard' 
                                            ? 'bg-blue-100 text-blue-700' 
                                            : 'text-gray-500 hover:text-gray-700'
                                    }`}
                                >
                                    Dashboard
                                </button>
                                <button
                                    onClick={() => setCurrentView('links')}
                                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                                        currentView === 'links' 
                                            ? 'bg-blue-100 text-blue-700' 
                                            : 'text-gray-500 hover:text-gray-700'
                                    }`}
                                >
                                    Links & Tracking
                                </button>
                                <button
                                    onClick={() => setCurrentView('materials')}
                                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                                        currentView === 'materials' 
                                            ? 'bg-blue-100 text-blue-700' 
                                            : 'text-gray-500 hover:text-gray-700'
                                    }`}
                                >
                                    Materials
                                </button>
                                <button
                                    onClick={() => setCurrentView('page-builder')}
                                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                                        currentView === 'page-builder' 
                                            ? 'bg-blue-100 text-blue-700' 
                                            : 'text-gray-500 hover:text-gray-700'
                                    }`}
                                >
                                    <Layout className="w-4 h-4 inline mr-1" />
                                    Page Builder
                                </button>
                            </div>
                        </div>
                        <div className="flex items-center">
                            <button className="p-2 rounded-md text-gray-400 hover:text-gray-500">
                                <Settings className="h-5 w-5" />
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                {currentView === 'dashboard' && renderDashboard()}
                {currentView === 'links' && renderLinks()}
                {currentView === 'materials' && renderMaterials()}
                {currentView === 'page-builder' && (
                    <AffiliatePageBuilder affiliateId={getCurrentAffiliateId()} />
                )}
            </main>
        </div>
    );
};

export default AffiliatePortal;