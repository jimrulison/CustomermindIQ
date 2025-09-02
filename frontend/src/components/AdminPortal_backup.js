import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, Users, Megaphone, DollarSign, BarChart3, Settings, LogOut, Lock, Plus, Edit, Trash2, Eye, Calendar, Target, CheckCircle, AlertCircle, X } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const AdminPortal = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('users');
  const [adminData, setAdminData] = useState(null);
  const [error, setError] = useState('');
  
  // Form states
  const [showBannerForm, setShowBannerForm] = useState(false);
  const [showDiscountForm, setShowDiscountForm] = useState(false);
  const [banners, setBanners] = useState([]);
  const [discounts, setDiscounts] = useState([]);
  const [editingItem, setEditingItem] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Check if user has admin access
  const hasAdminAccess = user && (user.role === 'admin' || user.role === 'super_admin');

  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    };
  };

  const loadAdminData = async () => {
    if (!hasAdminAccess) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`${backendUrl}/api/admin/analytics/dashboard`, {
        headers: getAuthHeaders()
      });
      if (response.data.status === 'success') {
        setAdminData(response.data.analytics);
      }
    } catch (error) {
      console.error('Failed to load admin data:', error);
      setError('Failed to load admin data');
    } finally {
      setLoading(false);
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

  useEffect(() => {
    if (hasAdminAccess) {
      loadAdminData();
      loadBanners();
      loadDiscounts();
    }
  }, [hasAdminAccess]);

  // Banner Management Component
  const BannerForm = ({ banner, onClose, onSuccess }) => {
    const [formData, setFormData] = useState({
      title: banner?.title || '',
      message: banner?.message || '',
      banner_type: banner?.banner_type || 'info',
      target_tiers: banner?.target_tiers || [],
      target_users: banner?.target_users?.join(', ') || '',
      start_date: banner?.start_date ? banner.start_date.slice(0, 16) : '',
      end_date: banner?.end_date ? banner.end_date.slice(0, 16) : '',
      is_dismissible: banner?.is_dismissible ?? true,
      priority: banner?.priority || 5,
      call_to_action: banner?.call_to_action || '',
      cta_url: banner?.cta_url || ''
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);

      try {
        const payload = {
          ...formData,
          target_users: formData.target_users.split(',').map(email => email.trim()).filter(email => email),
          start_date: formData.start_date ? new Date(formData.start_date).toISOString() : null,
          end_date: formData.end_date ? new Date(formData.end_date).toISOString() : null
        };

        if (banner) {
          await axios.put(`${backendUrl}/api/admin/banners/${banner.banner_id}`, payload, {
            headers: getAuthHeaders()
          });
        } else {
          await axios.post(`${backendUrl}/api/admin/banners`, payload, {
            headers: getAuthHeaders()
          });
        }

        onSuccess();
        onClose();
        loadBanners();
      } catch (error) {
        console.error('Failed to save banner:', error);
        setError('Failed to save banner');
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-white">
              {banner ? 'Edit Banner' : 'Create Banner'}
            </h3>
            <button onClick={onClose} className="text-slate-400 hover:text-white">
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Message</label>
              <textarea
                value={formData.message}
                onChange={(e) => setFormData({...formData, message: e.target.value})}
                rows={3}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Type</label>
                <select
                  value={formData.banner_type}
                  onChange={(e) => setFormData({...formData, banner_type: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="info">Info</option>
                  <option value="success">Success</option>
                  <option value="warning">Warning</option>
                  <option value="error">Error</option>
                  <option value="announcement">Announcement</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Priority (1-10)</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={formData.priority}
                  onChange={(e) => setFormData({...formData, priority: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Target Users (emails, comma-separated)</label>
              <input
                type="text"
                value={formData.target_users}
                onChange={(e) => setFormData({...formData, target_users: e.target.value})}
                placeholder="user1@example.com, user2@example.com"
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Start Date</label>
                <input
                  type="datetime-local"
                  value={formData.start_date}
                  onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">End Date</label>
                <input
                  type="datetime-local"
                  value={formData.end_date}
                  onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="dismissible"
                checked={formData.is_dismissible}
                onChange={(e) => setFormData({...formData, is_dismissible: e.target.checked})}
                className="mr-2"
              />
              <label htmlFor="dismissible" className="text-sm text-slate-300">Dismissible</label>
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-slate-300 hover:text-white"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Saving...' : (banner ? 'Update' : 'Create')}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  // Discount Management Component  
  const DiscountForm = ({ discount, onClose, onSuccess }) => {
    const [formData, setFormData] = useState({
      name: discount?.name || '',
      description: discount?.description || '',
      discount_type: discount?.discount_type || 'percentage',
      value: discount?.value || '',
      target_tiers: discount?.target_tiers || [],
      target_users: discount?.target_users?.join(', ') || '',
      start_date: discount?.start_date ? discount.start_date.slice(0, 16) : '',
      end_date: discount?.end_date ? discount.end_date.slice(0, 16) : '',
      usage_limit: discount?.usage_limit || '',
      per_user_limit: discount?.per_user_limit || 1,
      minimum_purchase: discount?.minimum_purchase || '',
      is_active: discount?.is_active ?? true
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);

      try {
        const payload = {
          ...formData,
          target_users: formData.target_users.split(',').map(email => email.trim()).filter(email => email),
          value: parseFloat(formData.value),
          usage_limit: formData.usage_limit ? parseInt(formData.usage_limit) : null,
          per_user_limit: parseInt(formData.per_user_limit),
          minimum_purchase: formData.minimum_purchase ? parseFloat(formData.minimum_purchase) : null,
          start_date: formData.start_date ? new Date(formData.start_date).toISOString() : null,
          end_date: formData.end_date ? new Date(formData.end_date).toISOString() : null
        };

        if (discount) {
          await axios.put(`${backendUrl}/api/admin/discounts/${discount.discount_id}`, payload, {
            headers: getAuthHeaders()
          });
        } else {
          await axios.post(`${backendUrl}/api/admin/discounts`, payload, {
            headers: getAuthHeaders()
          });
        }

        onSuccess();
        onClose();
        loadDiscounts();
      } catch (error) {
        console.error('Failed to save discount:', error);
        setError('Failed to save discount');
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-white">
              {discount ? 'Edit Discount' : 'Create Discount'}
            </h3>
            <button onClick={onClose} className="text-slate-400 hover:text-white">
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                rows={2}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Type</label>
                <select
                  value={formData.discount_type}
                  onChange={(e) => setFormData({...formData, discount_type: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="percentage">Percentage</option>
                  <option value="fixed_amount">Fixed Amount</option>
                  <option value="free_months">Free Months</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Value {formData.discount_type === 'percentage' ? '(%)' : formData.discount_type === 'fixed_amount' ? '($)' : '(months)'}
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.value}
                  onChange={(e) => setFormData({...formData, value: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Target Users (emails, comma-separated - leave empty for all users)</label>
              <input
                type="text"
                value={formData.target_users}
                onChange={(e) => setFormData({...formData, target_users: e.target.value})}
                placeholder="user1@example.com, user2@example.com or leave empty for all users"
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Usage Limit</label>
                <input
                  type="number"
                  value={formData.usage_limit}
                  onChange={(e) => setFormData({...formData, usage_limit: e.target.value})}
                  placeholder="Leave empty for unlimited"
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Per User Limit</label>
                <input
                  type="number"
                  value={formData.per_user_limit}
                  onChange={(e) => setFormData({...formData, per_user_limit: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Start Date</label>
                <input
                  type="datetime-local"
                  value={formData.start_date}
                  onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">End Date</label>
                <input
                  type="datetime-local"
                  value={formData.end_date}
                  onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="active"
                checked={formData.is_active}
                onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
                className="mr-2"
              />
              <label htmlFor="active" className="text-sm text-slate-300">Active</label>
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-slate-300 hover:text-white"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Saving...' : (discount ? 'Update' : 'Create')}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  // Access denied screen for non-admin users
  if (!hasAdminAccess) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="max-w-md w-full mx-4">
          <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-xl p-8 shadow-2xl text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-red-600/20 rounded-full mb-4">
              <Shield className="w-8 h-8 text-red-400" />
            </div>
            <h1 className="text-2xl font-bold text-white mb-2">Access Denied</h1>
            <p className="text-slate-400 mb-6">
              This admin portal is restricted to approved administrators only.
            </p>
            <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
              <p className="text-yellow-400 text-sm">
                🔒 Admin privileges required. Contact your system administrator for access.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Admin Dashboard - only shows if user has admin access
  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800/50 backdrop-blur-xl border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Shield className="w-8 h-8 text-red-400 mr-3" />
              <h1 className="text-2xl font-bold text-white">CustomerMind IQ Admin Portal</h1>
            </div>
            <div className="text-sm text-slate-300">
              Welcome, {user?.email} ({user?.role})
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="bg-slate-800/30 border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8 py-4">
            <button
              onClick={() => setActiveTab('users')}
              className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'users' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <Users className="w-4 h-4 mr-2" />
              User Management
            </button>
            <button
              onClick={() => setActiveTab('banners')}
              className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'banners' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <Megaphone className="w-4 h-4 mr-2" />
              Banner Management
            </button>
            <button
              onClick={() => setActiveTab('discounts')}
              className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'discounts' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <DollarSign className="w-4 h-4 mr-2" />
              Discount Management
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'analytics' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <BarChart3 className="w-4 h-4 mr-2" />
              Analytics
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'settings' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <Settings className="w-4 h-4 mr-2" />
              Settings
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'users' && (
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">User Management</h2>
            <p className="text-slate-400 mb-6">Manage user accounts, subscriptions, and permissions.</p>
            
            {adminData && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-slate-300">Total Users</h3>
                  <p className="text-2xl font-bold text-white">{adminData.user_stats?.total_users || 0}</p>
                </div>
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-slate-300">Active Users</h3>
                  <p className="text-2xl font-bold text-green-400">{adminData.user_stats?.active_users || 0}</p>
                </div>
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-slate-300">Annual Subscribers</h3>
                  <p className="text-2xl font-bold text-yellow-400">{adminData.user_stats?.annual_subscribers || 0}</p>
                </div>
              </div>
            )}
            
            <div className="text-center py-8">
              <p className="text-slate-400">User management interface coming soon...</p>
            </div>
          </div>
        )}

        {activeTab === 'banners' && (
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-xl font-bold text-white">Banner Management</h2>
                <p className="text-slate-400">Create and manage system-wide announcements and banners.</p>
              </div>
              <button
                onClick={() => setShowBannerForm(true)}
                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Banner
              </button>
            </div>

            <div className="space-y-4">
              {banners.length === 0 ? (
                <div className="text-center py-8">
                  <Megaphone className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                  <p className="text-slate-400">No banners created yet. Create your first banner!</p>
                </div>
              ) : (
                banners.map((banner) => (
                  <div key={banner.banner_id} className="bg-slate-700/50 rounded-lg p-4 border border-slate-600">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="font-semibold text-white">{banner.title}</h3>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            banner.status === 'active' ? 'bg-green-500/20 text-green-400' :
                            banner.status === 'scheduled' ? 'bg-yellow-500/20 text-yellow-400' :
                            banner.status === 'expired' ? 'bg-red-500/20 text-red-400' :
                            'bg-slate-500/20 text-slate-400'
                          }`}>
                            {banner.status}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            banner.banner_type === 'info' ? 'bg-blue-500/20 text-blue-400' :
                            banner.banner_type === 'success' ? 'bg-green-500/20 text-green-400' :
                            banner.banner_type === 'warning' ? 'bg-yellow-500/20 text-yellow-400' :
                            banner.banner_type === 'error' ? 'bg-red-500/20 text-red-400' :
                            'bg-purple-500/20 text-purple-400'
                          }`}>
                            {banner.banner_type}
                          </span>
                        </div>
                        <p className="text-slate-300 text-sm mb-2">{banner.message}</p>
                        <div className="flex items-center space-x-4 text-xs text-slate-500">
                          <span>Priority: {banner.priority}</span>
                          <span>Views: {banner.views}</span>
                          <span>Clicks: {banner.clicks}</span>
                          {banner.start_date && <span>Start: {new Date(banner.start_date).toLocaleDateString()}</span>}
                          {banner.end_date && <span>End: {new Date(banner.end_date).toLocaleDateString()}</span>}
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => {
                            setEditingItem(banner);
                            setShowBannerForm(true);
                          }}
                          className="p-2 text-slate-400 hover:text-blue-400 hover:bg-slate-600 rounded"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={async () => {
                            if (window.confirm('Are you sure you want to delete this banner?')) {
                              try {
                                await axios.delete(`${backendUrl}/api/admin/banners/${banner.banner_id}`, {
                                  headers: getAuthHeaders()
                                });
                                loadBanners();
                              } catch (error) {
                                console.error('Failed to delete banner:', error);
                              }
                            }
                          }}
                          className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-600 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'discounts' && (
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-xl font-bold text-white">Discount Management</h2>
                <p className="text-slate-400">Create and manage discount codes and promotional offers for all users.</p>
              </div>
              <button
                onClick={() => setShowDiscountForm(true)}
                className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Discount
              </button>
            </div>

            <div className="space-y-4">
              {discounts.length === 0 ? (
                <div className="text-center py-8">
                  <DollarSign className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                  <p className="text-slate-400">No discounts created yet. Create your first discount!</p>
                </div>
              ) : (
                discounts.map((discount) => (
                  <div key={discount.discount_id} className="bg-slate-700/50 rounded-lg p-4 border border-slate-600">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="font-semibold text-white">{discount.name}</h3>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            discount.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                          }`}>
                            {discount.is_active ? 'Active' : 'Inactive'}
                          </span>
                          <span className="px-2 py-1 rounded text-xs font-medium bg-blue-500/20 text-blue-400">
                            {discount.discount_type === 'percentage' ? `${discount.value}%` :
                             discount.discount_type === 'fixed_amount' ? `$${discount.value}` :
                             `${discount.value} months`}
                          </span>
                        </div>
                        <p className="text-slate-300 text-sm mb-2">{discount.description}</p>
                        <div className="flex items-center space-x-4 text-xs text-slate-500">
                          <span>Uses: {discount.total_uses}</span>
                          {discount.usage_limit && <span>Limit: {discount.usage_limit}</span>}
                          <span>Per User: {discount.per_user_limit}</span>
                          {discount.target_users?.length > 0 && <span>Targeted Users: {discount.target_users.length}</span>}
                          {discount.start_date && <span>Start: {new Date(discount.start_date).toLocaleDateString()}</span>}
                          {discount.end_date && <span>End: {new Date(discount.end_date).toLocaleDateString()}</span>}
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => {
                            setEditingItem(discount);
                            setShowDiscountForm(true);
                          }}
                          className="p-2 text-slate-400 hover:text-blue-400 hover:bg-slate-600 rounded"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={async () => {
                            if (window.confirm('Are you sure you want to delete this discount?')) {
                              try {
                                await axios.delete(`${backendUrl}/api/admin/discounts/${discount.discount_id}`, {
                                  headers: getAuthHeaders()
                                });
                                loadDiscounts();
                              } catch (error) {
                                console.error('Failed to delete discount:', error);
                              }
                            }
                          }}
                          className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-600 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Platform Analytics</h2>
            <p className="text-slate-400 mb-6">Comprehensive platform usage and business metrics.</p>
            
            {adminData && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-slate-300">Monthly Revenue</h3>
                  <p className="text-2xl font-bold text-green-400">
                    ${adminData.revenue_analytics?.monthly_revenue?.toLocaleString() || '0'}
                  </p>
                </div>
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-slate-300">ARPU</h3>
                  <p className="text-2xl font-bold text-blue-400">
                    ${adminData.revenue_analytics?.arpu?.toFixed(2) || '0.00'}
                  </p>
                </div>
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-slate-300">Active Banners</h3>
                  <p className="text-2xl font-bold text-yellow-400">{adminData.banner_analytics?.total_banners || 0}</p>
                </div>
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-slate-300">Discounts Created</h3>
                  <p className="text-2xl font-bold text-purple-400">{adminData.discount_analytics?.total_discounts || 0}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">System Settings</h2>
            <p className="text-slate-400 mb-6">Configure platform settings and preferences.</p>
            <div className="text-center py-8">
              <p className="text-slate-400">System settings interface coming soon...</p>
            </div>
          </div>
        )}

        {/* Show forms */}
        {showBannerForm && (
          <BannerForm
            banner={editingItem}
            onClose={() => {
              setShowBannerForm(false);
              setEditingItem(null);
            }}
            onSuccess={() => {
              setEditingItem(null);
            }}
          />
        )}

        {showDiscountForm && (
          <DiscountForm
            discount={editingItem}
            onClose={() => {
              setShowDiscountForm(false);
              setEditingItem(null);
            }}
            onSuccess={() => {
              setEditingItem(null);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default AdminPortal;