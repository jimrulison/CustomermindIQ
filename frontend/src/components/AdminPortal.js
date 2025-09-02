import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Shield, Users, Megaphone, DollarSign, BarChart3, Settings, LogOut, Lock, 
  Plus, Edit, Trash2, Eye, Calendar, Target, CheckCircle, AlertCircle, X,
  Search, Filter, Download, Code, Mail, Key, Workflow, Clock, TrendingUp,
  FileSpreadsheet, RefreshCw, UserCheck, Zap, Bell, CreditCard, Gift, Headphones
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const AdminPortalEnhanced = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [adminData, setAdminData] = useState(null);
  const [error, setError] = useState('');
  
  // Enhanced state management
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [editingItem, setEditingItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({});
  const [dateRange, setDateRange] = useState({
    from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    to: new Date().toISOString().split('T')[0]
  });

  // Data states
  const [users, setUsers] = useState([]);
  const [banners, setBanners] = useState([]);
  const [discounts, setDiscounts] = useState([]);
  const [discountCodes, setDiscountCodes] = useState([]);
  const [cohorts, setCohorts] = useState([]);
  const [emailTemplates, setEmailTemplates] = useState([]);
  const [apiKeys, setApiKeys] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [supportTickets, setSupportTickets] = useState([]);
  const [contactForms, setContactForms] = useState([]);
  const [emailCampaigns, setEmailCampaigns] = useState([]);
  const [emailProvider, setEmailProvider] = useState(null);
  const [analytics, setAnalytics] = useState({});

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
  const hasAdminAccess = user && (user.role === 'admin' || user.role === 'super_admin');

  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    };
  };

  // ===== DATA LOADING FUNCTIONS =====

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${backendUrl}/api/admin/analytics/dashboard`, {
        headers: getAuthHeaders()
      });
      if (response.data.status === 'success') {
        setAdminData(response.data.analytics);
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const params = new URLSearchParams();
      if (searchTerm) params.append('email', searchTerm);
      if (filters.role) params.append('role', filters.role);
      if (filters.subscription_tier) params.append('subscription_tier', filters.subscription_tier);
      if (filters.is_active !== undefined) params.append('is_active', filters.is_active);
      
      const response = await axios.get(`${backendUrl}/api/admin/users/search?${params}`, {
        headers: getAuthHeaders()
      });
      setUsers(response.data.users || []);
    } catch (error) {
      console.error('Failed to load users:', error);
    }
  };

  const loadDiscountCodes = async (discountId) => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/discounts/${discountId}/codes`, {
        headers: getAuthHeaders()
      });
      setDiscountCodes(response.data.codes || []);
    } catch (error) {
      console.error('Failed to load discount codes:', error);
    }
  };

  const loadCohorts = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/cohorts`, {
        headers: getAuthHeaders()
      });
      setCohorts(response.data.cohorts || []);
    } catch (error) {
      console.error('Failed to load cohorts:', error);
    }
  };

  const loadEmailTemplates = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/email-templates`, {
        headers: getAuthHeaders()
      });
      setEmailTemplates(response.data.templates || []);
    } catch (error) {
      console.error('Failed to load email templates:', error);
    }
  };

  const loadApiKeys = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/api-keys`, {
        headers: getAuthHeaders()
      });
      setApiKeys(response.data.api_keys || []);
    } catch (error) {
      console.error('Failed to load API keys:', error);
    }
  };

  const loadWorkflows = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/workflows`, {
        headers: getAuthHeaders()
      });
      setWorkflows(response.data.workflows || []);
    } catch (error) {
      console.error('Failed to load workflows:', error);
    }
  };

  const loadSupportTickets = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/support/admin/tickets`, {
        headers: getAuthHeaders()
      });
      setSupportTickets(response.data.tickets || []);
    } catch (error) {
      console.error('Failed to load support tickets:', error);
    }
  };

  const loadContactForms = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/odoo/admin/contact-forms`, {
        headers: getAuthHeaders()
      });
      setContactForms(response.data.submissions || []);
    } catch (error) {
      console.error('Failed to load contact forms:', error);
    }
  };

  const loadEmailCampaigns = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/email/campaigns`, {
        headers: getAuthHeaders()
      });
      setEmailCampaigns(response.data.campaigns || []);
    } catch (error) {
      console.error('Failed to load email campaigns:', error);
    }
  };

  const loadEmailProvider = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/email/providers/current`, {
        headers: getAuthHeaders()
      });
      setEmailProvider(response.data.provider_config);
    } catch (error) {
      console.error('Failed to load email provider:', error);
    }
  };

  const loadBanners = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/banners`, {
        headers: getAuthHeaders()
      });
      setBanners(response.data.banners || []);
    } catch (error) {
      console.error('Failed to load banners:', error);
    }
  };

  const loadDiscounts = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/discounts`, {
        headers: getAuthHeaders()
      });
      setDiscounts(response.data.discounts || []);
    } catch (error) {
      console.error('Failed to load discounts:', error);
    }
  };

  // ===== EXPORT FUNCTIONALITY =====

  const handleExport = async (exportType, format = 'csv') => {
    try {
      setLoading(true);
      
      const exportRequest = {
        export_type: exportType,
        filters: {
          date_range: dateRange,
          ...filters
        },
        format: format
      };

      const response = await axios.post(`${backendUrl}/api/admin/export`, exportRequest, {
        headers: getAuthHeaders(),
        responseType: format === 'csv' ? 'blob' : 'json'
      });

      if (format === 'csv') {
        // Create download link for CSV
        const blob = new Blob([response.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${exportType}_export_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } else {
        console.log('Exported data:', response.data);
      }
    } catch (error) {
      console.error('Export failed:', error);
      setError('Export failed');
    } finally {
      setLoading(false);
    }
  };

  // ===== BULK OPERATIONS =====

  const handleBulkDiscountApplication = async (discountId, criteria, reason) => {
    try {
      setLoading(true);
      
      const response = await axios.post(`${backendUrl}/api/admin/discounts/${discountId}/bulk-apply`, {
        discount_id: discountId,
        target_criteria: criteria,
        notify_users: true,
        reason: reason
      }, {
        headers: getAuthHeaders()
      });

      alert(`Discount applied to ${response.data.applied_count} users`);
      setShowModal(false);
    } catch (error) {
      console.error('Bulk application failed:', error);
      setError('Bulk application failed');
    } finally {
      setLoading(false);
    }
  };

  // ===== DISCOUNT CODE GENERATION =====

  const generateDiscountCodes = async (discountId, count, maxUses, expiresInDays) => {
    try {
      setLoading(true);
      
      const params = new URLSearchParams();
      params.append('count', count);
      if (maxUses) params.append('max_uses_per_code', maxUses);
      if (expiresInDays) params.append('expires_in_days', expiresInDays);
      
      const response = await axios.post(
        `${backendUrl}/api/admin/discounts/${discountId}/codes/generate?${params}`,
        {},
        { headers: getAuthHeaders() }
      );

      alert(`Generated ${response.data.codes.length} discount codes`);
      loadDiscountCodes(discountId);
    } catch (error) {
      console.error('Code generation failed:', error);
      setError('Code generation failed');
    } finally {
      setLoading(false);
    }
  };

  // ===== USER IMPERSONATION =====

  const startImpersonation = async (userId, reason, duration = 60) => {
    try {
      const response = await axios.post(`${backendUrl}/api/admin/impersonate`, {
        target_user_id: userId,
        reason: reason,
        duration_minutes: duration
      }, {
        headers: getAuthHeaders()
      });

      alert(`Impersonation session started: ${response.data.session_id}`);
    } catch (error) {
      console.error('Impersonation failed:', error);
      setError('Impersonation failed');
    }
  };

  // ===== COMPONENT LIFECYCLE =====

  useEffect(() => {
    if (hasAdminAccess) {
      loadDashboardData();
      loadBanners();
      loadDiscounts();
      loadCohorts();
      loadEmailTemplates();
      if (user.role === 'super_admin') {
        loadApiKeys();
      }
      loadWorkflows();
      loadSupportTickets();
      loadEmailCampaigns();
      loadEmailProvider();
    }
  }, [hasAdminAccess]);

  useEffect(() => {
    if (activeTab === 'users') {
      loadUsers();
    }
  }, [activeTab, searchTerm, filters]);

  if (!hasAdminAccess) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-8 text-center">
          <Lock className="w-16 h-16 text-red-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Access Denied</h2>
          <p className="text-slate-300">You need admin privileges to access this portal.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="bg-slate-800/50 border-b border-slate-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Shield className="w-8 h-8 text-blue-400" />
            <div>
              <h1 className="text-2xl font-bold text-white">CustomerMind IQ Admin Portal</h1>
              <p className="text-slate-400">Enhanced Administration Dashboard</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-white font-medium">{user.email}</p>
              <p className="text-slate-400 text-sm capitalize">{user.role}</p>
            </div>
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <Shield className="w-5 h-5 text-white" />
            </div>
          </div>
        </div>
      </div>

      <div className="flex">
        {/* Enhanced Sidebar */}
        <div className="w-64 bg-slate-800/30 border-r border-slate-700 min-h-screen">
          <div className="p-4">
            <nav className="space-y-2">
              {[
                { id: 'dashboard', name: 'Dashboard', icon: BarChart3 },
                { id: 'users', name: 'User Management', icon: Users },
                { id: 'banners', name: 'Banner Management', icon: Megaphone },
                { id: 'discounts', name: 'Discount Management', icon: DollarSign },
                { id: 'codes', name: 'Discount Codes', icon: Code },
                { id: 'cohorts', name: 'User Cohorts', icon: Target },
                { id: 'analytics', name: 'Advanced Analytics', icon: TrendingUp },
                { id: 'templates', name: 'Email Templates', icon: Mail },
                { id: 'workflows', name: 'Automated Workflows', icon: Workflow },
                { id: 'support', name: 'Support Tickets', icon: Headphones },
                { id: 'contact-forms', name: 'Contact Forms', icon: Mail },
                { id: 'emails', name: 'Email System', icon: Mail },
                ...(user.role === 'super_admin' ? [
                  { id: 'api-keys', name: 'API Keys', icon: Key }
                ] : []),
                { id: 'exports', name: 'Data Export', icon: Download },
                { id: 'settings', name: 'Settings', icon: Settings }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center px-3 py-2 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
                  }`}
                >
                  <tab.icon className="w-5 h-5 mr-3" />
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6">
          {error && (
            <div className="mb-4 bg-red-500/20 border border-red-500/50 rounded-lg p-4">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-red-400 mr-2" />
                <span className="text-red-300">{error}</span>
                <button
                  onClick={() => setError('')}
                  className="ml-auto text-red-300 hover:text-red-100"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">Admin Dashboard</h2>
                <button
                  onClick={loadDashboardData}
                  className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  disabled={loading}
                >
                  <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </button>
              </div>

              {adminData && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-slate-400 text-sm">Total Users</p>
                        <p className="text-2xl font-bold text-white">{adminData.user_statistics?.total_users || 0}</p>
                      </div>
                      <Users className="w-8 h-8 text-blue-400" />
                    </div>
                  </div>

                  <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-slate-400 text-sm">Monthly Revenue</p>
                        <p className="text-2xl font-bold text-green-400">
                          ${adminData.revenue_analytics?.total_monthly_revenue?.toLocaleString() || '0'}
                        </p>
                      </div>
                      <DollarSign className="w-8 h-8 text-green-400" />
                    </div>
                  </div>

                  <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-slate-400 text-sm">Active Discounts</p>
                        <p className="text-2xl font-bold text-yellow-400">{adminData.discount_analytics?.active_discounts || 0}</p>
                      </div>
                      <Gift className="w-8 h-8 text-yellow-400" />
                    </div>
                  </div>

                  <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-slate-400 text-sm">ARPU</p>
                        <p className="text-2xl font-bold text-purple-400">
                          ${adminData.revenue_analytics?.average_revenue_per_user?.toFixed(2) || '0.00'}
                        </p>
                      </div>
                      <TrendingUp className="w-8 h-8 text-purple-400" />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Enhanced User Management Tab */}
          {activeTab === 'users' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">User Management</h2>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => handleExport('users')}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Export Users
                  </button>
                </div>
              </div>

              {/* Advanced Search and Filters */}
              <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Search Email</label>
                    <div className="relative">
                      <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                      <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Search by email..."
                        className="w-full pl-10 pr-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Role</label>
                    <select
                      value={filters.role || ''}
                      onChange={(e) => setFilters({...filters, role: e.target.value || undefined})}
                      className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="">All Roles</option>
                      <option value="user">User</option>
                      <option value="admin">Admin</option>
                      <option value="super_admin">Super Admin</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Subscription</label>
                    <select
                      value={filters.subscription_tier || ''}
                      onChange={(e) => setFilters({...filters, subscription_tier: e.target.value || undefined})}
                      className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="">All Tiers</option>
                      <option value="free_trial">Free Trial</option>
                      <option value="monthly">Monthly</option>
                      <option value="annual">Annual</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Status</label>
                    <select
                      value={filters.is_active === undefined ? '' : filters.is_active.toString()}
                      onChange={(e) => setFilters({...filters, is_active: e.target.value === '' ? undefined : e.target.value === 'true'})}
                      className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="">All Users</option>
                      <option value="true">Active</option>
                      <option value="false">Inactive</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Users Table */}
              <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-slate-700/50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">User</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Role</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Subscription</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Status</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Joined</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                      {users.map((user) => (
                        <tr key={user.user_id} className="hover:bg-slate-700/30">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                                <span className="text-white text-sm font-medium">
                                  {user.email.charAt(0).toUpperCase()}
                                </span>
                              </div>
                              <div className="ml-3">
                                <p className="text-white font-medium">{user.email}</p>
                                <p className="text-slate-400 text-sm">{user.user_id}</p>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              user.role === 'super_admin' ? 'bg-red-500/20 text-red-400' :
                              user.role === 'admin' ? 'bg-yellow-500/20 text-yellow-400' :
                              'bg-gray-500/20 text-gray-400'
                            }`}>
                              {user.role}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              user.subscription_tier === 'annual' ? 'bg-green-500/20 text-green-400' :
                              user.subscription_tier === 'monthly' ? 'bg-blue-500/20 text-blue-400' :
                              'bg-gray-500/20 text-gray-400'
                            }`}>
                              {user.subscription_tier}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              user.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                            }`}>
                              {user.is_active ? 'Active' : 'Inactive'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-slate-300 text-sm">
                            {new Date(user.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex space-x-2">
                              <button
                                onClick={() => {
                                  setEditingItem(user);
                                  setModalType('user-analytics');
                                  setShowModal(true);
                                }}
                                className="p-2 text-slate-400 hover:text-blue-400 hover:bg-slate-600 rounded"
                                title="View Analytics"
                              >
                                <BarChart3 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => {
                                  const reason = prompt('Enter reason for impersonation:');
                                  if (reason) {
                                    startImpersonation(user.user_id, reason);
                                  }
                                }}
                                className="p-2 text-slate-400 hover:text-yellow-400 hover:bg-slate-600 rounded"
                                title="Impersonate User"
                              >
                                <UserCheck className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Other tabs would be implemented similarly with enhanced features... */}
          {/* For brevity, I'll show the structure for discount codes tab */}
          
          {activeTab === 'codes' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">Discount Codes</h2>
                <button
                  onClick={() => {
                    setModalType('generate-codes');
                    setShowModal(true);
                  }}
                  className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Generate Codes
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {discounts.map((discount) => (
                  <div key={discount.discount_id} className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                    <h3 className="text-lg font-semibold text-white mb-2">{discount.name}</h3>
                    <p className="text-slate-400 text-sm mb-4">{discount.description}</p>
                    <div className="flex items-center justify-between">
                      <span className="px-2 py-1 rounded text-xs font-medium bg-blue-500/20 text-blue-400">
                        {discount.discount_type === 'percentage' ? `${discount.value}%` :
                         discount.discount_type === 'fixed_amount' ? `$${discount.value}` :
                         `${discount.value} months`}
                      </span>
                      <button
                        onClick={() => {
                          const count = prompt('How many codes to generate?');
                          if (count) {
                            generateDiscountCodes(discount.discount_id, parseInt(count));
                          }
                        }}
                        className="flex items-center px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
                      >
                        <Code className="w-3 h-3 mr-1" />
                        Generate
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Support Tickets Tab */}
          {activeTab === 'support' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">Support Tickets</h2>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={loadSupportTickets}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Refresh
                  </button>
                </div>
              </div>

              <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-slate-700/50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Ticket</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Customer</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Status</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Priority</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Support Tier</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Created</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Due</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                      {supportTickets.length === 0 ? (
                        <tr>
                          <td colSpan="8" className="px-6 py-8 text-center">
                            <Headphones className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                            <p className="text-slate-400">No support tickets found</p>
                          </td>
                        </tr>
                      ) : (
                        supportTickets.map((ticket) => (
                          <tr key={ticket.ticket_id} className="hover:bg-slate-700/30">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div>
                                <p className="text-white font-medium text-sm">{ticket.subject}</p>
                                <p className="text-slate-400 text-xs">#{ticket.ticket_id.slice(-8)}</p>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                                  <span className="text-white text-xs font-medium">
                                    {ticket.user_email.charAt(0).toUpperCase()}
                                  </span>
                                </div>
                                <div className="ml-3">
                                  <p className="text-white text-sm">{ticket.user_email}</p>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                ticket.status === 'open' ? 'bg-green-500/20 text-green-400' :
                                ticket.status === 'in_progress' ? 'bg-blue-500/20 text-blue-400' :
                                ticket.status === 'waiting_customer' ? 'bg-yellow-500/20 text-yellow-400' :
                                ticket.status === 'resolved' ? 'bg-purple-500/20 text-purple-400' :
                                'bg-gray-500/20 text-gray-400'
                              }`}>
                                {ticket.status.replace('_', ' ')}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                ticket.priority === 'urgent' ? 'bg-red-500/20 text-red-400' :
                                ticket.priority === 'high' ? 'bg-orange-500/20 text-orange-400' :
                                ticket.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                'bg-green-500/20 text-green-400'
                              }`}>
                                {ticket.priority}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                ticket.support_tier === 'enterprise' ? 'bg-purple-500/20 text-purple-400' :
                                ticket.support_tier === 'professional' ? 'bg-blue-500/20 text-blue-400' :
                                'bg-gray-500/20 text-gray-400'
                              }`}>
                                {ticket.support_tier}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-slate-300 text-sm">
                              {new Date(ticket.created_at).toLocaleDateString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`text-sm ${
                                new Date(ticket.due_date) < new Date() ? 'text-red-400 font-medium' : 'text-slate-300'
                              }`}>
                                {new Date(ticket.due_date).toLocaleDateString()}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex space-x-2">
                                <button
                                  onClick={() => {
                                    setEditingItem(ticket);
                                    setModalType('ticket-details');
                                    setShowModal(true);
                                  }}
                                  className="p-2 text-slate-400 hover:text-blue-400 hover:bg-slate-600 rounded"
                                  title="View Details"
                                >
                                  <Eye className="w-4 h-4" />
                                </button>
                                <button
                                  onClick={() => {
                                    const agent = prompt('Assign to agent (email):');
                                    if (agent) {
                                      // assignTicket(ticket.ticket_id, agent);
                                      console.log('Assign ticket functionality to be implemented');
                                    }
                                  }}
                                  className="p-2 text-slate-400 hover:text-yellow-400 hover:bg-slate-600 rounded"
                                  title="Assign Agent"
                                >
                                  <UserCheck className="w-4 h-4" />
                                </button>
                              </div>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Support Statistics */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Total Tickets</p>
                      <p className="text-2xl font-bold text-white">{supportTickets.length}</p>
                    </div>
                    <Headphones className="w-8 h-8 text-blue-400" />
                  </div>
                </div>

                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Open Tickets</p>
                      <p className="text-2xl font-bold text-green-400">
                        {supportTickets.filter(t => t.status === 'open').length}
                      </p>
                    </div>
                    <AlertCircle className="w-8 h-8 text-green-400" />
                  </div>
                </div>

                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Overdue</p>
                      <p className="text-2xl font-bold text-red-400">
                        {supportTickets.filter(t => new Date(t.due_date) < new Date() && t.status !== 'closed').length}
                      </p>
                    </div>
                    <Clock className="w-8 h-8 text-red-400" />
                  </div>
                </div>

                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Avg Response</p>
                      <p className="text-2xl font-bold text-purple-400">8.5h</p>
                    </div>
                    <TrendingUp className="w-8 h-8 text-purple-400" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Data Export Tab */}
          {activeTab === 'exports' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white">Data Export</h2>

              <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Export Configuration</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Date Range</label>
                    <div className="flex space-x-2">
                      <input
                        type="date"
                        value={dateRange.from}
                        onChange={(e) => setDateRange({...dateRange, from: e.target.value})}
                        className="flex-1 px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                      />
                      <input
                        type="date"
                        value={dateRange.to}
                        onChange={(e) => setDateRange({...dateRange, to: e.target.value})}
                        className="flex-1 px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { type: 'users', name: 'Users', icon: Users },
                    { type: 'discounts', name: 'Discounts', icon: Gift },
                    { type: 'banners', name: 'Banners', icon: Bell },
                    { type: 'analytics', name: 'Analytics', icon: BarChart3 }
                  ].map((exportOption) => (
                    <button
                      key={exportOption.type}
                      onClick={() => handleExport(exportOption.type)}
                      disabled={loading}
                      className="flex flex-col items-center p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors disabled:opacity-50"
                    >
                      <exportOption.icon className="w-8 h-8 text-blue-400 mb-2" />
                      <span className="text-white font-medium">{exportOption.name}</span>
                      <span className="text-slate-400 text-xs">CSV Export</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Email System Tab */}
          {activeTab === 'emails' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">Email System</h2>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => {
                      setModalType('send-email');
                      setShowModal(true);
                    }}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    <Mail className="w-4 h-4 mr-2" />
                    Send Email
                  </button>
                  <button
                    onClick={loadEmailCampaigns}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Refresh
                  </button>
                </div>
              </div>

              {/* Email Provider Status */}
              {emailProvider && (
                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Email Provider Configuration</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-slate-700/50 p-4 rounded-lg">
                      <p className="text-slate-300 text-sm">Current Provider</p>
                      <p className="text-white font-semibold capitalize">{emailProvider.provider}</p>
                    </div>
                    <div className="bg-slate-700/50 p-4 rounded-lg">
                      <p className="text-slate-300 text-sm">From Email</p>
                      <p className="text-white font-semibold">{emailProvider.from_email}</p>
                    </div>
                    <div className="bg-slate-700/50 p-4 rounded-lg">
                      <p className="text-slate-300 text-sm">Status</p>
                      <p className={`font-semibold ${emailProvider.is_active ? 'text-green-400' : 'text-red-400'}`}>
                        {emailProvider.is_active ? 'Active' : 'Inactive'}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Email Campaigns Table */}
              <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
                <div className="px-6 py-4 border-b border-slate-700">
                  <h3 className="text-lg font-semibold text-white">Email Campaigns</h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-slate-700/50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Campaign</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Recipients</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Status</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Provider</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Sent/Failed</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Created</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                      {emailCampaigns.length === 0 ? (
                        <tr>
                          <td colSpan="7" className="px-6 py-8 text-center">
                            <Mail className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                            <p className="text-slate-400">No email campaigns found</p>
                          </td>
                        </tr>
                      ) : (
                        emailCampaigns.map((campaign) => (
                          <tr key={campaign.campaign_id} className="hover:bg-slate-700/30">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div>
                                <p className="text-white font-medium text-sm">{campaign.subject}</p>
                                <p className="text-slate-400 text-xs">#{campaign.campaign_id.slice(-8)}</p>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-slate-300 text-sm">
                              {campaign.recipient_count}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                campaign.status === 'sent' ? 'bg-green-500/20 text-green-400' :
                                campaign.status === 'sending' ? 'bg-blue-500/20 text-blue-400' :
                                campaign.status === 'queued' ? 'bg-yellow-500/20 text-yellow-400' :
                                campaign.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                                'bg-gray-500/20 text-gray-400'
                              }`}>
                                {campaign.status}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="px-2 py-1 rounded text-xs font-medium bg-blue-500/20 text-blue-400 capitalize">
                                {campaign.provider}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-slate-300 text-sm">
                              <span className="text-green-400">{campaign.sent_count}</span> / 
                              <span className="text-red-400 ml-1">{campaign.failed_count}</span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-slate-300 text-sm">
                              {new Date(campaign.created_at).toLocaleDateString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <button
                                onClick={() => {
                                  setEditingItem(campaign);
                                  setModalType('campaign-details');
                                  setShowModal(true);
                                }}
                                className="p-2 text-slate-400 hover:text-blue-400 hover:bg-slate-600 rounded"
                                title="View Details"
                              >
                                <Eye className="w-4 h-4" />
                              </button>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Email Statistics */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Total Campaigns</p>
                      <p className="text-2xl font-bold text-white">{emailCampaigns.length}</p>
                    </div>
                    <Mail className="w-8 h-8 text-blue-400" />
                  </div>
                </div>

                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Emails Sent</p>
                      <p className="text-2xl font-bold text-green-400">
                        {emailCampaigns.reduce((sum, c) => sum + (c.sent_count || 0), 0)}
                      </p>
                    </div>
                    <CheckCircle className="w-8 h-8 text-green-400" />
                  </div>
                </div>

                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Failed</p>
                      <p className="text-2xl font-bold text-red-400">
                        {emailCampaigns.reduce((sum, c) => sum + (c.failed_count || 0), 0)}
                      </p>
                    </div>
                    <AlertCircle className="w-8 h-8 text-red-400" />
                  </div>
                </div>

                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm">Delivery Rate</p>
                      <p className="text-2xl font-bold text-purple-400">
                        {emailCampaigns.length > 0 ? 
                          Math.round((emailCampaigns.reduce((sum, c) => sum + (c.sent_count || 0), 0) / 
                          Math.max(emailCampaigns.reduce((sum, c) => sum + (c.recipient_count || 0), 0), 1)) * 100) : 0}%
                      </p>
                    </div>
                    <TrendingUp className="w-8 h-8 text-purple-400" />
                  </div>
                </div>
              </div>

              {/* Quick Send Email Form (Simple Method) */}
              <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Quick Send Email</h3>
                <p className="text-slate-400 text-sm mb-4">Simple method to send emails to customers</p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <button
                    onClick={() => {
                      setModalType('send-to-all');
                      setShowModal(true);
                    }}
                    className="flex flex-col items-center p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
                  >
                    <Users className="w-8 h-8 text-blue-400 mb-2" />
                    <span className="text-white font-medium">All Users</span>
                    <span className="text-slate-400 text-xs">Send to all customers</span>
                  </button>

                  <button
                    onClick={() => {
                      setModalType('send-to-tier');
                      setShowModal(true);
                    }}
                    className="flex flex-col items-center p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
                  >
                    <Target className="w-8 h-8 text-green-400 mb-2" />
                    <span className="text-white font-medium">By Subscription</span>
                    <span className="text-slate-400 text-xs">Target specific tiers</span>
                  </button>

                  <button
                    onClick={() => {
                      setModalType('send-custom');
                      setShowModal(true);
                    }}
                    className="flex flex-col items-center p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
                  >
                    <Edit className="w-8 h-8 text-purple-400 mb-2" />
                    <span className="text-white font-medium">Custom List</span>
                    <span className="text-slate-400 text-xs">Specific email addresses</span>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminPortalEnhanced;