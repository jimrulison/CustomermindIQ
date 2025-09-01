import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, Users, Megaphone, DollarSign, BarChart3, Settings, LogOut, Lock } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const AdminPortal = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('users');
  const [adminData, setAdminData] = useState(null);
  const [error, setError] = useState('');

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Check if user has admin access
  const hasAdminAccess = user && (user.role === 'admin' || user.role === 'super_admin');

  const loadAdminData = async () => {
    if (!hasAdminAccess) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`${backendUrl}/api/admin/analytics/overview`);
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

  useEffect(() => {
    if (hasAdminAccess) {
      loadAdminData();
    }
  }, [hasAdminAccess]);

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