import React, { useState, useEffect } from 'react';
import { 
    Mail, 
    Zap, 
    Plus, 
    Settings, 
    CheckCircle, 
    XCircle, 
    ExternalLink, 
    TestTube,
    Eye,
    EyeOff,
    AlertCircle,
    ArrowLeft
} from 'lucide-react';

const AffiliateEmailIntegrations = ({ affiliateId, onBack }) => {
    const [integrations, setIntegrations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showSetupModal, setShowSetupModal] = useState(false);
    const [selectedPlatform, setSelectedPlatform] = useState(null);
    const [error, setError] = useState('');

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://seo-legal-update.preview.emergentagent.com';

    const platformInfo = {
        convertkit: {
            name: 'ConvertKit',
            description: 'Automatically tag customers in ConvertKit when they convert',
            color: 'bg-pink-100 text-pink-800 border-pink-200',
            icon: Mail,
            benefits: ['Automatic customer tagging', 'Conversion tracking', 'Email sequence triggers'],
            setupUrl: 'https://app.convertkit.com/account_settings/advanced_settings'
        },
        getresponse: {
            name: 'GetResponse',
            description: 'Sync conversions to GetResponse contacts and campaigns',
            color: 'bg-blue-100 text-blue-800 border-blue-200',
            icon: Mail,
            benefits: ['Contact synchronization', 'Campaign automation', 'Conversion analytics'],
            setupUrl: 'https://app.getresponse.com/manage_api.html'
        },
        zapier: {
            name: 'Zapier',
            description: 'Connect to 5,000+ apps with custom automation workflows',
            color: 'bg-orange-100 text-orange-800 border-orange-200',
            icon: Zap,
            benefits: ['Connect to any app', 'Custom workflows', 'Advanced automation'],
            setupUrl: 'https://zapier.com/app/editor'
        }
    };

    useEffect(() => {
        if (affiliateId) {
            fetchIntegrations();
        }
    }, [affiliateId]);

    const fetchIntegrations = async () => {
        try {
            setLoading(true);
            const response = await fetch(`${backendUrl}/api/integrations/${affiliateId}`);
            
            if (response.ok) {
                const data = await response.json();
                setIntegrations(data.integrations || []);
            } else {
                setError('Failed to load integrations');
            }
        } catch (err) {
            setError('Network error loading integrations');
        } finally {
            setLoading(false);
        }
    };

    const SetupModal = () => {
        const [formData, setFormData] = useState({
            api_key: '',
            webhook_url: '',
            tags: ['affiliate', 'conversion'],
            showApiKey: false
        });
        const [submitting, setSubmitting] = useState(false);

        const platform = platformInfo[selectedPlatform];

        const handleSetup = async (e) => {
            e.preventDefault();
            setSubmitting(true);

            try {
                const requestData = {
                    affiliate_id: affiliateId,
                    platform: selectedPlatform,
                    tags: formData.tags,
                    custom_fields: {
                        affiliate_source: 'multisite_dashboard',
                        setup_date: new Date().toISOString()
                    }
                };

                if (selectedPlatform === 'zapier') {
                    requestData.webhook_url = formData.webhook_url;
                    requestData.api_key = 'webhook'; // Placeholder for Zapier
                } else {
                    requestData.api_key = formData.api_key;
                }

                const response = await fetch(`${backendUrl}/api/integrations/setup`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });

                const result = await response.json();
                
                if (result.success) {
                    alert(`🎉 ${platform.name} integration setup successful! Your conversions will now sync automatically.`);
                    setShowSetupModal(false);
                    setSelectedPlatform(null);
                    fetchIntegrations();
                } else {
                    alert(`Setup failed: ${result.error || 'Please check your credentials and try again.'}`);
                }
            } catch (err) {
                alert(`Setup error: ${err.message}`);
            } finally {
                setSubmitting(false);
            }
        };

        return (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
                    <h3 className="text-xl font-semibold mb-4 flex items-center">
                        <platform.icon className="w-6 h-6 mr-2" />
                        Setup {platform.name} Integration
                    </h3>
                    
                    <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                        <p className="text-blue-800 text-sm">{platform.description}</p>
                        <ul className="mt-2 text-sm text-blue-700">
                            {platform.benefits.map((benefit, index) => (
                                <li key={index} className="flex items-center mt-1">
                                    <CheckCircle className="w-4 h-4 mr-2 text-blue-600" />
                                    {benefit}
                                </li>
                            ))}
                        </ul>
                    </div>
                    
                    <form onSubmit={handleSetup} className="space-y-4">
                        {selectedPlatform === 'zapier' ? (
                            <>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Zapier Webhook URL
                                    </label>
                                    <input
                                        type="url"
                                        value={formData.webhook_url}
                                        onChange={(e) => setFormData({...formData, webhook_url: e.target.value})}
                                        className="w-full border border-gray-300 rounded-md px-3 py-2"
                                        placeholder="https://hooks.zapier.com/hooks/catch/..."
                                        required
                                    />
                                    <p className="text-xs text-gray-500 mt-1">
                                        Create a "Catch Hook" trigger in Zapier to get this URL
                                    </p>
                                </div>
                                
                                <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
                                    <p className="text-sm text-yellow-800">
                                        <strong>Setup Instructions:</strong>
                                    </p>
                                    <ol className="text-sm text-yellow-700 mt-1 list-decimal list-inside space-y-1">
                                        <li>Create a new Zap in Zapier</li>
                                        <li>Choose "Webhooks by Zapier" as trigger</li>
                                        <li>Select "Catch Hook" event</li>
                                        <li>Copy the webhook URL here</li>
                                        <li>Complete setup to receive conversion data</li>
                                    </ol>
                                </div>
                            </>
                        ) : (
                            <>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        {selectedPlatform === 'convertkit' ? 'API Secret' : 'API Key'}
                                    </label>
                                    <div className="relative">
                                        <input
                                            type={formData.showApiKey ? 'text' : 'password'}
                                            value={formData.api_key}
                                            onChange={(e) => setFormData({...formData, api_key: e.target.value})}
                                            className="w-full border border-gray-300 rounded-md px-3 py-2 pr-10"
                                            placeholder={`Enter your ${platform.name} ${selectedPlatform === 'convertkit' ? 'API secret' : 'API key'}`}
                                            required
                                        />
                                        <button
                                            type="button"
                                            onClick={() => setFormData({...formData, showApiKey: !formData.showApiKey})}
                                            className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
                                        >
                                            {formData.showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                        </button>
                                    </div>
                                    <div className="mt-1 flex items-center">
                                        <a 
                                            href={platform.setupUrl}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-xs text-indigo-600 hover:text-indigo-700 flex items-center"
                                        >
                                            Get your API {selectedPlatform === 'convertkit' ? 'secret' : 'key'} here
                                            <ExternalLink className="w-3 h-3 ml-1" />
                                        </a>
                                    </div>
                                </div>
                            </>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Customer Tags (comma-separated)
                            </label>
                            <input
                                type="text"
                                value={formData.tags.join(', ')}
                                onChange={(e) => setFormData({...formData, tags: e.target.value.split(',').map(t => t.trim())})}
                                className="w-full border border-gray-300 rounded-md px-3 py-2"
                                placeholder="affiliate, conversion, premium"
                            />
                            <p className="text-xs text-gray-500 mt-1">
                                Tags will be automatically applied to customers when they convert
                            </p>
                        </div>

                        <div className="flex justify-end space-x-3 pt-4 border-t">
                            <button
                                type="button"
                                onClick={() => {
                                    setShowSetupModal(false);
                                    setSelectedPlatform(null);
                                }}
                                className="px-4 py-2 text-gray-600 hover:text-gray-800"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={submitting}
                                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
                            >
                                {submitting ? 'Setting up...' : 'Setup Integration'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        );
    };

    const testIntegration = async (platform) => {
        try {
            const response = await fetch(`${backendUrl}/api/integrations/test/${affiliateId}/${platform}`);
            const result = await response.json();
            
            if (result.success) {
                alert(`✅ ${platform.toUpperCase()} integration test successful! Your connection is working properly.`);
                fetchIntegrations();
            } else {
                alert(`❌ Test failed: Connection error. Please check your credentials.`);
            }
        } catch (err) {
            alert(`Test error: ${err.message}`);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'active': return 'text-green-600 bg-green-50 border-green-200';
            case 'error': return 'text-red-600 bg-red-50 border-red-200';
            default: return 'text-gray-600 bg-gray-50 border-gray-200';
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading email integrations...</p>
                </div>
            </div>
        );
    }

    const existingIntegrations = integrations.reduce((acc, int) => {
        acc[int.platform] = int;
        return acc;
    }, {});

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                
                {/* Header */}
                <div className="mb-8 flex items-center">
                    <button
                        onClick={onBack}
                        className="mr-4 p-2 text-gray-600 hover:text-gray-900"
                    >
                        <ArrowLeft className="w-5 h-5" />
                    </button>
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Email Integrations</h1>
                        <p className="text-gray-600 mt-2">
                            Automatically sync your conversions to email marketing platforms
                        </p>
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

                {/* Info Banner */}
                <div className="mb-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h2 className="text-lg font-semibold text-blue-900 mb-2">🚀 Supercharge Your Email Marketing</h2>
                    <p className="text-blue-800 mb-4">
                        Connect your email platforms to automatically tag customers, trigger sequences, and track conversions.
                        Perfect for building targeted email campaigns based on your affiliate conversions!
                    </p>
                    <ul className="text-sm text-blue-700 space-y-1">
                        <li>✓ Automatic customer tagging when they convert</li>
                        <li>✓ Trigger email sequences for different product purchases</li>
                        <li>✓ Track which affiliate promotions drive the best email subscribers</li>
                        <li>✓ Build custom audiences for retargeting campaigns</li>
                    </ul>
                </div>

                {/* Platform Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    {Object.entries(platformInfo).map(([platformId, platform]) => {
                        const integration = existingIntegrations[platformId];
                        const Icon = platform.icon;

                        return (
                            <div key={platformId} className={`bg-white border-2 rounded-lg p-6 ${integration ? platform.color : 'border-gray-200'}`}>
                                <div className="flex items-center justify-between mb-4">
                                    <div className="flex items-center">
                                        <Icon className="w-8 h-8 text-gray-700 mr-3" />
                                        <div>
                                            <h3 className="text-lg font-semibold text-gray-900">{platform.name}</h3>
                                            {integration && (
                                                <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(integration.status)}`}>
                                                    {integration.status === 'active' ? <CheckCircle className="w-3 h-3 mr-1" /> : <XCircle className="w-3 h-3 mr-1" />}
                                                    {integration.status}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                <p className="text-gray-600 text-sm mb-4">{platform.description}</p>

                                <ul className="text-sm text-gray-500 space-y-1 mb-6">
                                    {platform.benefits.map((benefit, index) => (
                                        <li key={index} className="flex items-center">
                                            <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full mr-2"></div>
                                            {benefit}
                                        </li>
                                    ))}
                                </ul>

                                {integration ? (
                                    <div className="space-y-3">
                                        <div className="text-sm text-gray-600">
                                            <div>Setup: {formatDate(integration.created_at)}</div>
                                            {integration.last_sync && (
                                                <div>Last sync: {formatDate(integration.last_sync)}</div>
                                            )}
                                            {integration.tags && integration.tags.length > 0 && (
                                                <div>Tags: {integration.tags.join(', ')}</div>
                                            )}
                                        </div>
                                        
                                        <button
                                            onClick={() => testIntegration(platformId)}
                                            className="w-full flex items-center justify-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
                                        >
                                            <TestTube className="w-4 h-4 mr-2" />
                                            Test Connection
                                        </button>
                                    </div>
                                ) : (
                                    <button
                                        onClick={() => {
                                            setSelectedPlatform(platformId);
                                            setShowSetupModal(true);
                                        }}
                                        className="w-full flex items-center justify-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                                    >
                                        <Plus className="w-4 h-4 mr-2" />
                                        Connect {platform.name}
                                    </button>
                                )}
                            </div>
                        );
                    })}
                </div>

                {/* Setup Modal */}
                {showSetupModal && selectedPlatform && <SetupModal />}
            </div>
        </div>
    );
};

export default AffiliateEmailIntegrations;