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
    BarChart3
} from 'lucide-react';
import AffiliateChatWidget from './AffiliateChatWidget';

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

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://customer-ai-hub-1.preview.emergentagent.com';

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
            {/* Welcome Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
                <h1 className="text-2xl font-bold">
                    Welcome back, {affiliateData.affiliate.first_name}! 👋
                </h1>
                <p className="mt-2 opacity-90">
                    Your affiliate ID: <span className="font-mono bg-white/20 px-2 py-1 rounded">{affiliateData.affiliate.affiliate_id}</span>
                </p>
                <p className="mt-1 text-sm opacity-75">
                    Status: <span className="capitalize font-semibold">{affiliateData.affiliate.status}</span>
                </p>
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

            {/* This Month vs All Time */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                        <Calendar className="h-5 w-5 mr-2 text-blue-600" />
                        This Month
                    </h3>
                    <div className="space-y-3">
                        <div className="flex justify-between">
                            <span className="text-gray-600">Clicks:</span>
                            <span className="font-semibold">{affiliateData.stats.this_month.clicks}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Trials:</span>
                            <span className="font-semibold">{affiliateData.stats.this_month.trials}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Conversions:</span>
                            <span className="font-semibold">{affiliateData.stats.this_month.conversions}</span>
                        </div>
                        <div className="flex justify-between border-t pt-2">
                            <span className="text-gray-600">Commissions:</span>
                            <span className="font-semibold text-green-600">
                                ${affiliateData.stats.this_month.commissions.toFixed(2)}
                            </span>
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-sm border">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                        <BarChart3 className="h-5 w-5 mr-2 text-purple-600" />
                        All Time
                    </h3>
                    <div className="space-y-3">
                        <div className="flex justify-between">
                            <span className="text-gray-600">Clicks:</span>
                            <span className="font-semibold">{affiliateData.stats.all_time.clicks}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Trials:</span>
                            <span className="font-semibold">{affiliateData.stats.all_time.trials}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Conversions:</span>
                            <span className="font-semibold">{affiliateData.stats.all_time.conversions}</span>
                        </div>
                        <div className="flex justify-between border-t pt-2">
                            <span className="text-gray-600">Commissions:</span>
                            <span className="font-semibold text-green-600">
                                ${affiliateData.stats.all_time.commissions.toFixed(2)}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-lg p-6 shadow-sm border">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <Award className="h-5 w-5 mr-2 text-green-600" />
                    Recent Activity
                </h3>
                <div className="space-y-3">
                    {affiliateData.recent_activity.map((activity, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <div>
                                <p className="font-medium">{activity.customer}</p>
                                <p className="text-sm text-gray-600">
                                    Upgraded to {activity.plan} plan
                                </p>
                            </div>
                            <div className="text-right">
                                <p className="font-semibold text-green-600">
                                    +${activity.commission.toFixed(2)}
                                </p>
                                <p className="text-xs text-gray-500">
                                    {new Date(activity.date).toLocaleDateString()}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
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
            </main>
        </div>
    );
};

export default AffiliatePortal;