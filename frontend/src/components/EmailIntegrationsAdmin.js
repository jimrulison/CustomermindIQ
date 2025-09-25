import React, { useState, useEffect } from 'react';
import { 
    Settings, 
    Mail, 
    ExternalLink, 
    Plus, 
    Trash2, 
    TestTube, 
    Eye, 
    EyeOff, 
    CheckCircle, 
    XCircle, 
    AlertCircle,
    Zap,
    Activity,
    Clock,
    Filter,
    Download,
    RefreshCw
} from 'lucide-react';

const EmailIntegrationsAdmin = () => {
    const [integrations, setIntegrations] = useState([]);
    const [webhookLogs, setWebhookLogs] = useState([]);
    const [overview, setOverview] = useState({});
    const [loading, setLoading] = useState(true);
    const [showSetupModal, setShowSetupModal] = useState(false);
    const [selectedIntegration, setSelectedIntegration] = useState(null);
    const [showApiKey, setShowApiKey] = useState({});
    const [error, setError] = useState('');

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://seo-legal-update.preview.emergentagent.com';

    const platformInfo = {
        convertkit: {
            name: 'ConvertKit',
            description: 'Email marketing automation',
            color: 'bg-pink-100 text-pink-800',
            icon: Mail,
            setupFields: ['api_secret', 'tags']
        },
        getresponse: {
            name: 'GetResponse',
            description: 'Email marketing platform',
            color: 'bg-blue-100 text-blue-800',
            icon: Mail,
            setupFields: ['api_key', 'campaign_id', 'tags']
        },
        zapier: {
            name: 'Zapier',
            description: 'Automation workflows',
            color: 'bg-orange-100 text-orange-800',
            icon: Zap,
            setupFields: ['webhook_url']
        }
    };

    useEffect(() => {
        fetchOverview();
        fetchRecentLogs();
    }, []);

    const fetchOverview = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${backendUrl}/api/integrations/admin/overview`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setOverview(data);
            }
        } catch (err) {
            setError('Failed to load overview');
        } finally {
            setLoading(false);
        }
    };

    const fetchRecentLogs = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${backendUrl}/api/integrations/admin/logs?limit=20`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setWebhookLogs(data.logs || []);
            }
        } catch (err) {
            console.error('Failed to load logs:', err);
        }
    };

    const fetchAffiliateIntegrations = async (affiliateId) => {
        try {
            const response = await fetch(`${backendUrl}/api/integrations/${affiliateId}`);
            
            if (response.ok) {
                const data = await response.json();
                setIntegrations(data.integrations || []);
            }
        } catch (err) {
            setError('Failed to load affiliate integrations');
        }
    };

    const SetupModal = () => {
        const [formData, setFormData] = useState({
            affiliate_id: '',
            platform: 'convertkit',
            api_key: '',
            webhook_url: '',
            tags: ['affiliate', 'customer'],
            custom_fields: {}
        });
        const [submitting, setSubmitting] = useState(false);

        const handleSetup = async (e) => {
            e.preventDefault();
            setSubmitting(true);

            try {
                const response = await fetch(`${backendUrl}/api/integrations/setup`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();
                
                if (result.success) {
                    alert(`${formData.platform.toUpperCase()} integration setup successful!`);
                    setShowSetupModal(false);
                    if (formData.affiliate_id) {
                        fetchAffiliateIntegrations(formData.affiliate_id);
                    }
                    fetchOverview();
                } else {
                    alert(`Setup failed: ${result.error || 'Unknown error'}`);
                }
            } catch (err) {
                alert(`Setup error: ${err.message}`);
            } finally {
                setSubmitting(false);
            }
        };

        return (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-lg p-6 w-full max-w-md">
                    <h3 className="text-lg font-semibold mb-4">Setup Email Integration</h3>
                    
                    <form onSubmit={handleSetup} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Affiliate ID</label>
                            <input
                                type="text"
                                value={formData.affiliate_id}
                                onChange={(e) => setFormData({...formData, affiliate_id: e.target.value})}
                                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                                placeholder="Enter affiliate ID"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Platform</label>
                            <select
                                value={formData.platform}
                                onChange={(e) => setFormData({...formData, platform: e.target.value})}
                                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                            >
                                <option value="convertkit">ConvertKit</option>
                                <option value="getresponse">GetResponse</option>
                                <option value="zapier">Zapier</option>
                            </select>
                        </div>

                        {formData.platform === 'zapier' ? (
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Webhook URL</label>
                                <input
                                    type="url"
                                    value={formData.webhook_url}
                                    onChange={(e) => setFormData({...formData, webhook_url: e.target.value})}
                                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                                    placeholder="https://hooks.zapier.com/hooks/catch/..."
                                    required
                                />
                            </div>
                        ) : (
                            <div>
                                <label className="block text-sm font-medium text-gray-700">
                                    API {formData.platform === 'convertkit' ? 'Secret' : 'Key'}
                                </label>
                                <input
                                    type="password"
                                    value={formData.api_key}
                                    onChange={(e) => setFormData({...formData, api_key: e.target.value})}
                                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                                    placeholder={formData.platform === 'convertkit' ? 'Your ConvertKit API secret' : 'Your GetResponse API key'}
                                    required
                                />
                            </div>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Tags (comma-separated)</label>
                            <input
                                type="text"
                                value={formData.tags.join(', ')}
                                onChange={(e) => setFormData({...formData, tags: e.target.value.split(',').map(t => t.trim())})}
                                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                                placeholder="affiliate, customer, conversion"
                            />
                        </div>

                        <div className="flex justify-end space-x-3 pt-4">
                            <button
                                type="button"
                                onClick={() => setShowSetupModal(false)}
                                className="px-4 py-2 text-gray-600 hover:text-gray-800"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={submitting}
                                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
                            >
                                {submitting ? 'Setting up...' : 'Setup Integration'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        );
    };

    const testIntegration = async (affiliateId, platform) => {
        try {
            const response = await fetch(`${backendUrl}/api/integrations/test/${affiliateId}/${platform}`);
            const result = await response.json();
            
            if (result.success) {
                alert(`${platform.toUpperCase()} integration test successful!`);
                fetchAffiliateIntegrations(affiliateId);
            } else {
                alert(`Test failed: ${result.test_result?.status || 'Unknown error'}`);
            }
        } catch (err) {
            alert(`Test error: ${err.message}`);
        }
    };

    const deleteIntegration = async (integrationId) => {
        if (!confirm('Are you sure you want to delete this integration?')) return;

        try {
            const response = await fetch(`${backendUrl}/api/integrations/${integrationId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                alert('Integration deleted successfully');
                fetchOverview();
                if (selectedIntegration) {
                    fetchAffiliateIntegrations(selectedIntegration);
                }
            }
        } catch (err) {
            alert(`Delete error: ${err.message}`);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleString();
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'active': return 'text-green-600';
            case 'error': return 'text-red-600';
            case 'inactive': return 'text-gray-600';
            default: return 'text-gray-600';
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'active': return CheckCircle;
            case 'error': return XCircle;
            default: return AlertCircle;
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

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                
                {/* Header */}
                <div className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Email Platform Integrations</h1>
                        <p className="text-gray-600 mt-2">Manage ConvertKit, GetResponse, and Zapier integrations</p>
                    </div>
                    <button
                        onClick={() => setShowSetupModal(true)}
                        className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Setup Integration
                    </button>
                </div>

                {error && (
                    <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
                        <div className="flex items-center">
                            <AlertCircle className="h-5 w-5 text-red-600 mr-3" />
                            <p className="text-red-700">{error}</p>
                        </div>
                    </div>
                )}

                {/* Overview Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <Settings className="h-6 w-6 text-indigo-600" />
                                </div>
                                <div className="ml-5 w-0 flex-1">
                                    <dl>
                                        <dt className="text-sm font-medium text-gray-500 truncate">Total Integrations</dt>
                                        <dd className="text-lg font-medium text-gray-900">
                                            {overview.total_integrations || 0}
                                        </dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>

                    {overview.platform_stats?.map(stat => {
                        const platform = platformInfo[stat._id];
                        const Icon = platform?.icon || Mail;
                        
                        return (
                            <div key={stat._id} className="bg-white overflow-hidden shadow rounded-lg">
                                <div className="p-5">
                                    <div className="flex items-center">
                                        <div className="flex-shrink-0">
                                            <Icon className="h-6 w-6 text-indigo-600" />
                                        </div>
                                        <div className="ml-5 w-0 flex-1">
                                            <dl>
                                                <dt className="text-sm font-medium text-gray-500 truncate">
                                                    {platform?.name || stat._id}
                                                </dt>
                                                <dd className="text-lg font-medium text-gray-900">
                                                    {stat.active} / {stat.total}
                                                </dd>
                                            </dl>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* Affiliate Integration Lookup */}
                <div className="bg-white rounded-lg shadow p-6 mb-8">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Affiliate Integrations</h2>
                    <div className="flex gap-4 mb-4">
                        <input
                            type="text"
                            placeholder="Enter Affiliate ID"
                            value={selectedIntegration || ''}
                            onChange={(e) => setSelectedIntegration(e.target.value)}
                            className="flex-1 border border-gray-300 rounded-md px-3 py-2"
                        />
                        <button
                            onClick={() => selectedIntegration && fetchAffiliateIntegrations(selectedIntegration)}
                            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                        >
                            Load Integrations
                        </button>
                    </div>

                    {integrations.length > 0 && (
                        <div className="space-y-4">
                            {integrations.map(integration => {
                                const platform = platformInfo[integration.platform];
                                const StatusIcon = getStatusIcon(integration.status);
                                
                                return (
                                    <div key={integration.integration_id} className="border border-gray-200 rounded-lg p-4">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center space-x-4">
                                                <div className={`px-3 py-1 rounded-full text-xs font-medium ${platform?.color || 'bg-gray-100 text-gray-800'}`}>
                                                    {platform?.name || integration.platform}
                                                </div>
                                                <div className="flex items-center space-x-2">
                                                    <StatusIcon className={`w-4 h-4 ${getStatusColor(integration.status)}`} />
                                                    <span className={`text-sm ${getStatusColor(integration.status)}`}>
                                                        {integration.status}
                                                    </span>
                                                </div>
                                                <div className="text-sm text-gray-500">
                                                    Created: {formatDate(integration.created_at)}
                                                </div>
                                                {integration.last_sync && (
                                                    <div className="text-sm text-gray-500">
                                                        Last sync: {formatDate(integration.last_sync)}
                                                    </div>
                                                )}
                                            </div>
                                            
                                            <div className="flex items-center space-x-2">
                                                <button
                                                    onClick={() => testIntegration(integration.affiliate_id, integration.platform)}
                                                    className="p-2 text-gray-600 hover:text-indigo-600"
                                                    title="Test Integration"
                                                >
                                                    <TestTube className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => deleteIntegration(integration.integration_id)}
                                                    className="p-2 text-gray-600 hover:text-red-600"
                                                    title="Delete Integration"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </div>

                                        {/* Integration Details */}
                                        <div className="mt-3 text-sm text-gray-600">
                                            {integration.tags?.length > 0 && (
                                                <div className="mb-2">
                                                    <span className="font-medium">Tags: </span>
                                                    {integration.tags.join(', ')}
                                                </div>
                                            )}
                                            {integration.webhook_url && (
                                                <div className="mb-2">
                                                    <span className="font-medium">Webhook: </span>
                                                    <span className="font-mono text-xs">{integration.webhook_url}</span>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>

                {/* Recent Webhook Logs */}
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold text-gray-900">Recent Webhook Activity</h2>
                        <button
                            onClick={fetchRecentLogs}
                            className="flex items-center px-3 py-1 text-sm text-gray-600 hover:text-indigo-600"
                        >
                            <RefreshCw className="w-4 h-4 mr-1" />
                            Refresh
                        </button>
                    </div>

                    {webhookLogs.length === 0 ? (
                        <p className="text-gray-500 text-center py-8">No recent webhook activity</p>
                    ) : (
                        <div className="space-y-3">
                            {webhookLogs.slice(0, 10).map(log => {
                                const platform = platformInfo[log.platform];
                                
                                return (
                                    <div key={log.log_id} className="border border-gray-200 rounded p-3">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center space-x-3">
                                                <div className={`px-2 py-1 rounded text-xs font-medium ${platform?.color || 'bg-gray-100 text-gray-800'}`}>
                                                    {platform?.name || log.platform}
                                                </div>
                                                <span className="text-sm text-gray-600">{log.event_type}</span>
                                                <span className="text-xs text-gray-500">{log.affiliate_id}</span>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                <div className={`w-2 h-2 rounded-full ${log.processed ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
                                                <span className="text-xs text-gray-500">{formatDate(log.created_at)}</span>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>

                {/* Setup Modal */}
                {showSetupModal && <SetupModal />}
            </div>
        </div>
    );
};

export default EmailIntegrationsAdmin;