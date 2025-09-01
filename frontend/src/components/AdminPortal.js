import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, Users, Megaphone, DollarSign, BarChart3, Settings, LogOut, Lock } from 'lucide-react';

const AdminPortal = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('users');
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [adminData, setAdminData] = useState(null);
  const [error, setError] = useState('');

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Admin authentication
      const response = await axios.post(`${backendUrl}/api/auth/login`, {
        email: credentials.email,
        password: credentials.password
      });

      if (response.data.access_token) {
        const token = response.data.access_token;
        
        // Verify admin role
        const profileResponse = await axios.get(`${backendUrl}/api/auth/profile`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (profileResponse.data.role === 'admin' || profileResponse.data.role === 'super_admin') {
          localStorage.setItem('admin_token', token);
          setIsAuthenticated(true);
          loadAdminData(token);
        } else {
          setError('Access denied. Admin privileges required.');
        }
      }
    } catch (error) {
      setError('Invalid admin credentials or access denied.');
    } finally {
      setLoading(false);
    }
  };

  const loadAdminData = async (token) => {
    try {
      const response = await axios.get(`${backendUrl}/api/admin/analytics/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAdminData(response.data);
    } catch (error) {
      console.error('Failed to load admin data:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    setIsAuthenticated(false);
    setAdminData(null);
    setCredentials({ email: '', password: '' });
  };

  // Check for existing admin session
  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      // Verify token is still valid
      axios.get(`${backendUrl}/api/auth/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(response => {
        if (response.data.role === 'admin' || response.data.role === 'super_admin') {
          setIsAuthenticated(true);
          loadAdminData(token);
        } else {
          localStorage.removeItem('admin_token');
        }
      }).catch(() => {
        localStorage.removeItem('admin_token');
      });
    }
  }, []);

  // Admin Login Form
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="max-w-md w-full mx-4">
          <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-xl p-8 shadow-2xl">
            {/* Header */}
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-red-600/20 rounded-full mb-4">
                <Shield className="w-8 h-8 text-red-400" />
              </div>
              <h1 className="text-2xl font-bold text-white mb-2">Admin Portal</h1>
              <p className="text-slate-400">Secure access for approved administrators only</p>
            </div>

            {/* Login Form */}
            <form onSubmit={handleAdminLogin} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Admin Email
                </label>
                <input
                  type="email"
                  value={credentials.email}
                  onChange={(e) => setCredentials({...credentials, email: e.target.value})}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="admin@customermindiq.com"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Admin Password
                </label>
                <input
                  type="password"
                  value={credentials.password}
                  onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="Enter admin password"
                  required
                />
              </div>

              {error && (
                <div className="p-3 bg-red-500/20 border border-red-500/30 rounded-lg">
                  <p className="text-red-400 text-sm">{error}</p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-red-600 to-red-700 text-white font-semibold py-3 px-4 rounded-lg hover:from-red-700 hover:to-red-800 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Authenticating...
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <Lock className="w-5 h-5 mr-2" />
                    Secure Admin Login
                  </div>
                )}
              </button>
            </form>

            {/* Security Notice */}
            <div className="mt-6 p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
              <p className="text-yellow-400 text-xs text-center">
                🔒 This portal is restricted to approved administrators only. All access attempts are logged and monitored.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Admin Dashboard
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
            <button
              onClick={handleLogout}
              className="flex items-center px-4 py-2 bg-red-600/20 text-red-400 rounded-lg hover:bg-red-600/30 transition-colors"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </button>
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
            <h2 className="text-xl font-bold text-white mb-4">Banner Management</h2>
            <p className="text-slate-400 mb-6">Create and manage system-wide announcements and banners.</p>
            <div className="text-center py-8">
              <p className="text-slate-400">Banner management interface coming soon...</p>
            </div>
          </div>
        )}

        {activeTab === 'discounts' && (
          <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Discount Management</h2>
            <p className="text-slate-400 mb-6">Create and manage discount codes and promotional offers.</p>
            <div className="text-center py-8">
              <p className="text-slate-400">Discount management interface coming soon...</p>
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
      </div>
    </div>
  );
};

export default AdminPortal;