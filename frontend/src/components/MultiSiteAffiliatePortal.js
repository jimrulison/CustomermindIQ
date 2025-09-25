import React, { useState, useEffect, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import AffiliateEmailIntegrations from './AffiliateEmailIntegrations';
import { 
    Users, 
    DollarSign, 
    TrendingUp, 
    Eye, 
    MousePointer, 
    Target, 
    Award, 
    Gift, 
    Star, 
    Globe,
    BarChart3,
    Calendar,
    Download,
    ExternalLink,
    ChevronRight,
    Plus,
    CheckCircle,
    AlertCircle,
    Zap,
    Settings
} from 'lucide-react';

const MultiSiteAffiliatePortal = () => {
    const { t } = useTranslation();
    const [selectedSites, setSelectedSites] = useState([]);
    const [dashboardData, setDashboardData] = useState({});
    const [comboEligibility, setComboEligibility] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [affiliateId, setAffiliateId] = useState('');
    const [showEmailIntegrations, setShowEmailIntegrations] = useState(false); // NEW

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://seo-legal-update.preview.emergentagent.com';

    useEffect(() => {
        // Get affiliate data from localStorage
        const affiliateData = localStorage.getItem('affiliate_data');
        if (affiliateData) {
            try {
                const data = JSON.parse(affiliateData);
                setAffiliateId(data.id);
                fetchDashboardData(data.id);
            } catch (error) {
                setError('Failed to load affiliate data');
            }
        }
    }, []);

    const fetchDashboardData = async (affId) => {
        try {
            setLoading(true);
            const response = await fetch(`${backendUrl}/api/affiliate/multisite-dashboard?affiliate_id=${affId}`);
            
            if (response.ok) {
                const data = await response.json();
                setDashboardData(data);
                setComboEligibility(data.combo_opportunities || []);
                
                // Auto-select first few sites if none selected
                if (selectedSites.length === 0 && data.available_sites) {
                    const autoSelect = data.available_sites.slice(0, 3).map(site => site.site_id);
                    setSelectedSites(autoSelect);
                }
            } else {
                setError('Failed to load dashboard data');
            }
        } catch (err) {
            setError('Network error loading dashboard');
        } finally {
            setLoading(false);
        }
    };

    // Aggregate data across selected sites
    const aggregatedStats = useMemo(() => {
        if (!dashboardData.sites_data) return {};
        
        return selectedSites.reduce((acc, siteId) => {
            const siteData = dashboardData.sites_data[siteId] || {};
            return {
                totalEarnings: (acc.totalEarnings || 0) + (siteData.earnings || 0),
                totalClicks: (acc.totalClicks || 0) + (siteData.clicks || 0),
                totalConversions: (acc.totalConversions || 0) + (siteData.conversions || 0),
                totalBonuses: (acc.totalBonuses || 0) + (siteData.multi_site_bonuses || 0),
                comboBonuses: (acc.comboBonuses || 0) + (siteData.combo_bonuses || 0)
            };
        }, {});
    }, [selectedSites, dashboardData]);

    const handleSiteChange = (siteId) => {
        setSelectedSites(prev => 
            prev.includes(siteId) 
                ? prev.filter(id => id !== siteId)
                : [...prev, siteId]
        );
    };

    const generateMultiSiteLinks = async () => {
        if (selectedSites.length === 0) {
            alert('Please select at least one site');
            return;
        }

        try {
            const params = new URLSearchParams({
                affiliate_id: affiliateId,
                campaign_name: 'dashboard_generated',
                site_ids: selectedSites,
                link_paths: ['/']
            });

            const response = await fetch(`${backendUrl}/api/affiliate/multisite-links/generate?${params}`, {
                method: 'POST'
            });

            if (response.ok) {
                const data = await response.json();
                alert(`Generated ${Object.keys(data.tracking_links).length} tracking link sets!`);
            }
        } catch (err) {
            alert('Failed to generate links');
        }
    };

    // Show Email Integrations component if requested
    if (showEmailIntegrations) {
        return (
            <AffiliateEmailIntegrations 
                affiliateId={affiliateId} 
                onBack={() => setShowEmailIntegrations(false)} 
            />
        );
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading multi-site dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Multi-Site Affiliate Dashboard</h1>
                    <div className="mt-2 flex items-center space-x-4">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                            <Star className="w-4 h-4 mr-1" />
                            {dashboardData.affiliate_tier} Tier
                        </span>
                        <span className="text-gray-500">
                            {selectedSites.length} of {dashboardData.available_sites?.length || 0} sites selected
                        </span>
                    </div>
                </div>

                {error && (
                    <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
                        <div className="flex items-center">
                            <AlertCircle className="h-5 w-5 text-red-600 mr-3" />
                            <p className="text-red-700">{error}</p>
                        </div>
                    </div>
                )}

                {/* Site Selector */}
                <div className="mb-8 bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                        <Globe className="w-5 h-5 mr-2" />
                        Select Sites to View
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                        {dashboardData.available_sites?.map(site => (
                            <div key={site.site_id} className="relative">
                                <label className="flex items-center p-3 border-2 rounded-lg cursor-pointer hover:border-indigo-200 transition-colors">
                                    <input
                                        type="checkbox"
                                        checked={selectedSites.includes(site.site_id)}
                                        onChange={() => handleSiteChange(site.site_id)}
                                        className="sr-only"
                                    />
                                    <div className={`flex-1 ${selectedSites.includes(site.site_id) ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200'} transition-colors`}>
                                        <div className="text-sm font-medium text-gray-900">{site.name}</div>
                                        <div className="text-xs text-gray-500">{site.domain}</div>
                                        {selectedSites.includes(site.site_id) && (
                                            <CheckCircle className="absolute top-2 right-2 w-5 h-5 text-indigo-600" />
                                        )}
                                    </div>
                                </label>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Stats Overview */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <DollarSign className="h-6 w-6 text-green-600" />
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">Total Earnings</dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            ${(aggregatedStats.totalEarnings || 0).toLocaleString()}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <Gift className="h-6 w-6 text-purple-600" />
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">Multi-Site Bonuses</dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            ${(aggregatedStats.totalBonuses || 0).toLocaleString()}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <Zap className="h-6 w-6 text-yellow-600" />
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">Combo Bonuses</dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            ${(aggregatedStats.comboBonuses || 0).toLocaleString()}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <MousePointer className="h-6 w-6 text-blue-600" />
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">Total Clicks</dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {(aggregatedStats.totalClicks || 0).toLocaleString()}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <Target className="h-6 w-6 text-indigo-600" />
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">Conversions</dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {(aggregatedStats.totalConversions || 0).toLocaleString()}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Combo Discount Opportunities */}
                {comboEligibility.length > 0 && (
                    <div className="mb-8 bg-white rounded-lg shadow p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                            <Gift className="w-5 h-5 mr-2" />
                            Combo Discount Opportunities
                        </h2>
                        <div className="space-y-4">
                            {comboEligibility.map((opportunity, index) => (
                                <div key={index} className={`p-4 border rounded-lg ${opportunity.eligible ? 'border-green-200 bg-green-50' : 'border-yellow-200 bg-yellow-50'}`}>
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <h3 className="font-medium text-gray-900">{opportunity.name}</h3>
                                            <p className="text-sm text-gray-600">{opportunity.description}</p>
                                            <div className="mt-2">
                                                <div className="flex items-center text-sm">
                                                    <span className="text-gray-500 mr-2">Progress:</span>
                                                    <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                                                        <div 
                                                            className={`h-2 rounded-full ${opportunity.eligible ? 'bg-green-500' : 'bg-yellow-500'}`}
                                                            style={{ width: `${Math.min(opportunity.progress, 100)}%` }}
                                                        ></div>
                                                    </div>
                                                    <span className="font-medium">{Math.round(opportunity.progress)}%</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-lg font-bold text-green-600">
                                                +{opportunity.bonus_percentage}%
                                            </div>
                                            {!opportunity.eligible && opportunity.sites_needed.length > 0 && (
                                                <div className="text-xs text-gray-500">
                                                    Need: {opportunity.sites_needed.slice(0, 2).join(', ')}
                                                    {opportunity.sites_needed.length > 2 && ` +${opportunity.sites_needed.length - 2} more`}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Action Buttons */}
                <div className="mb-8 bg-white rounded-lg shadow p-6">
                    <div className="flex flex-wrap gap-4">
                        <button 
                            onClick={generateMultiSiteLinks}
                            className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                            disabled={selectedSites.length === 0}
                        >
                            <Plus className="w-4 h-4 mr-2" />
                            Generate Multi-Site Links
                        </button>
                        
                        <button className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                            <Download className="w-4 h-4 mr-2" />
                            Export Report
                        </button>
                        
                        <button className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                            <BarChart3 className="w-4 h-4 mr-2" />
                            View Analytics
                        </button>

                        <button className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
                            <Settings className="w-4 h-4 mr-2" />
                            Email Integrations
                        </button>
                    </div>
                </div>

                {/* Individual Site Performance */}
                <div className="space-y-6">
                    <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                        <BarChart3 className="w-5 h-5 mr-2" />
                        Site Performance Breakdown
                    </h2>
                    
                    {selectedSites.map(siteId => {
                        const siteInfo = dashboardData.available_sites?.find(s => s.site_id === siteId);
                        const siteData = dashboardData.sites_data?.[siteId] || {};
                        
                        return (
                            <div key={siteId} className="bg-white rounded-lg shadow p-6">
                                <div className="flex items-center justify-between mb-4">
                                    <div>
                                        <h3 className="text-lg font-medium text-gray-900">{siteInfo?.name}</h3>
                                        <p className="text-sm text-gray-500">{siteInfo?.domain}</p>
                                    </div>
                                    <ExternalLink className="w-5 h-5 text-gray-400" />
                                </div>
                                
                                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-gray-900">
                                            ${(siteData.earnings || 0).toLocaleString()}
                                        </div>
                                        <div className="text-sm text-gray-500">Earnings</div>
                                    </div>
                                    
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-gray-900">
                                            {(siteData.clicks || 0).toLocaleString()}
                                        </div>
                                        <div className="text-sm text-gray-500">Clicks</div>
                                    </div>
                                    
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-gray-900">
                                            {(siteData.conversions || 0).toLocaleString()}
                                        </div>
                                        <div className="text-sm text-gray-500">Conversions</div>
                                    </div>
                                    
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-gray-900">
                                            {(siteData.conversion_rate || 0).toFixed(1)}%
                                        </div>
                                        <div className="text-sm text-gray-500">Conv. Rate</div>
                                    </div>
                                    
                                    <div className="text-center">
                                        <div className="text-2xl font-bold text-purple-600">
                                            ${(siteData.multi_site_bonuses || 0).toLocaleString()}
                                        </div>
                                        <div className="text-sm text-gray-500">Bonuses</div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* Tier Progress */}
                {dashboardData.next_tier_requirements && (
                    <div className="mt-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow p-6 text-white">
                        <h3 className="text-lg font-semibold mb-4">Tier Progress</h3>
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-indigo-100">Current: {dashboardData.next_tier_requirements.current_tier}</p>
                                {dashboardData.next_tier_requirements.next_tier && (
                                    <p className="text-sm">
                                        Next: {dashboardData.next_tier_requirements.next_tier} 
                                        ({dashboardData.next_tier_requirements.sites_needed} more sites needed)
                                    </p>
                                )}
                            </div>
                            <Award className="w-8 h-8 text-indigo-200" />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MultiSiteAffiliatePortal;