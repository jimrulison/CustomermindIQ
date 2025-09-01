import React from 'react';
import { Button } from './ui/button';
import { 
  Brain, 
  Users, 
  Megaphone, 
  DollarSign, 
  Zap, 
  TrendingUp, 
  BarChart3,
  Target,
  LogOut,
  User,
  Activity,
  Database,
  Shield,
  Cpu,
  Globe,
  GraduationCap,
  HelpCircle,
  Heart,
  Settings,
  BookOpen
} from 'lucide-react';

const Header = ({ currentPage, onNavigate, onSignOut, user }) => {
  // Primary navigation - separated by analytics type
  const primaryNavigation = [
    {
      id: 'customer-analytics-dashboard',
      label: 'Customer Analytics',
      icon: Brain,
      color: 'hover:bg-blue-600/20 hover:text-blue-400',
      description: 'Customer behavior, marketing automation, revenue optimization'
    },
    {
      id: 'website-analytics-dashboard', 
      label: 'Website Analytics',
      icon: Globe,
      color: 'hover:bg-emerald-600/20 hover:text-emerald-400',
      description: 'Website performance, SEO, technical optimization'
    }
  ];

  // Customer Analytics modules
  const customerAnalyticsModules = [
    {
      id: 'customers',
      label: 'Customer Intelligence',
      icon: Users,
      color: 'hover:bg-blue-600/20 hover:text-blue-400'
    },
    {
      id: 'real-time-health',
      label: 'Real-Time Health',
      icon: Heart,
      color: 'hover:bg-red-600/20 hover:text-red-400'
    },
    {
      id: 'marketing',
      label: 'Marketing Automation',
      icon: Megaphone,
      color: 'hover:bg-purple-600/20 hover:text-purple-400'
    },
    {
      id: 'revenue',
      label: 'Revenue Analytics',
      icon: DollarSign,
      color: 'hover:bg-green-600/20 hover:text-green-400'
    },
    {
      id: 'advanced',
      label: 'Advanced Features',
      icon: Zap,
      color: 'hover:bg-orange-600/20 hover:text-orange-400'
    },
    {
      id: 'customer-success',
      label: 'Customer Success',
      icon: Target,
      color: 'hover:bg-cyan-600/20 hover:text-cyan-400'
    },
    {
      id: 'executive',
      label: 'Executive Dashboard',
      icon: BarChart3,
      color: 'hover:bg-indigo-600/20 hover:text-indigo-400'
    },
    {
      id: 'growth-acceleration',
      label: 'Growth Acceleration Engine',
      subtitle: 'Annual Subscribers Only',
      icon: Zap,
      color: 'hover:bg-yellow-600/20 hover:text-yellow-400',
      requiresAnnual: true
    },
    {
      id: 'growth',
      label: 'Growth Intelligence',
      icon: TrendingUp,
      color: 'hover:bg-emerald-600/20 hover:text-emerald-400'
    },
    {
      id: 'create',
      label: 'Create Campaign',
      icon: Cpu,
      color: 'hover:bg-yellow-600/20 hover:text-yellow-400'
    }
  ];

  // Website Analytics modules  
  const websiteAnalyticsModules = [
    {
      id: 'website-intelligence',
      label: 'Website Intelligence',
      icon: Globe,
      color: 'hover:bg-emerald-600/20 hover:text-emerald-400'
    },
    {
      id: 'analytics',
      label: 'Analytics & Insights',
      icon: TrendingUp,
      color: 'hover:bg-indigo-600/20 hover:text-indigo-400'
    },
    {
      id: 'product',
      label: 'Product Intelligence',
      icon: Activity,
      color: 'hover:bg-teal-600/20 hover:text-teal-400'
    },
    {
      id: 'integration',
      label: 'Integration & Data Hub',
      icon: Database,
      color: 'hover:bg-blue-600/20 hover:text-blue-400'
    },
    {
      id: 'compliance',
      label: 'Compliance & Governance',
      icon: Shield,
      color: 'hover:bg-purple-600/20 hover:text-purple-400'
    },
    {
      id: 'ai-command',
      label: 'AI Command Center',
      icon: Cpu,
      color: 'hover:bg-cyan-600/20 hover:text-cyan-400'
    }
  ];

  // Determine which modules to show based on current context
  const getActiveModules = () => {
    if (currentPage === 'customer-analytics-dashboard' || customerAnalyticsModules.some(m => m.id === currentPage)) {
      return customerAnalyticsModules;
    } else if (currentPage === 'website-analytics-dashboard' || websiteAnalyticsModules.some(m => m.id === currentPage)) {
      return websiteAnalyticsModules;
    }
    return customerAnalyticsModules; // Default to customer analytics
  };

  const activeModules = getActiveModules();

  return (
    <header className="bg-slate-900/95 backdrop-blur-xl border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo Section */}
          <div className="flex items-center">
            <img
              src="https://customer-assets.emergentagent.com/job_mindiq-auth/artifacts/bi9l7mag_Customer%20Mind%20IQ%20logo.png"
              alt="CustomerMind IQ Logo"
              className="w-8 h-8 mr-3"
            />
            <h1 className="text-xl font-bold text-white">CustomerMind IQ</h1>
          </div>

          {/* Primary Dashboard Selector - Center */}
          <div className="flex-1 flex justify-center">
            <div className="flex space-x-2">
              <button
                onClick={() => onNavigate('customer-analytics-dashboard')}
                className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-200 ${
                  currentPage === 'customer-analytics-dashboard' || customerAnalyticsModules.some(m => m.id === currentPage)
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-slate-800/50 text-slate-300 hover:bg-blue-600/20 hover:text-blue-400 border border-slate-600'
                }`}
              >
                <Brain className="w-4 h-4 inline mr-2" />
                CUSTOMER ANALYTICS
              </button>
              
              <button
                onClick={() => onNavigate('website-analytics-dashboard')}
                className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-200 ${
                  currentPage === 'website-analytics-dashboard' || websiteAnalyticsModules.some(m => m.id === currentPage)
                    ? 'bg-emerald-600 text-white shadow-lg'
                    : 'bg-slate-800/50 text-slate-300 hover:bg-emerald-600/20 hover:text-emerald-400 border border-slate-600'
                }`}
              >
                <Globe className="w-4 h-4 inline mr-2" />
                WEBSITE ANALYTICS
              </button>
            </div>
          </div>

          {/* User Info & Admin & Training & Support & Sign Out */}
          <div className="flex items-center space-x-4">
            {/* Admin Panel Button (only show for admin users) */}
            {user && (user.role === 'admin' || user.role === 'super_admin') && (
              <button
                onClick={() => onNavigate('admin')}
                className={`flex items-center px-3 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                  currentPage === 'admin'
                    ? 'bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg'
                    : 'bg-slate-800/50 text-slate-300 hover:bg-red-600/20 hover:text-red-400 border border-slate-600'
                }`}
              >
                <Settings className="w-4 h-4 mr-2" />
                Admin Panel
              </button>
            )}

            {/* Training Button */}
            <button
              onClick={() => onNavigate('training')}
              className={`flex items-center px-3 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                currentPage === 'training'
                  ? 'bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg'
                  : 'bg-slate-800/50 text-slate-300 hover:bg-green-600/20 hover:text-green-400 border border-slate-600'
              }`}
            >
              <GraduationCap className="w-4 h-4 mr-2" />
              Training
            </button>

            {/* Knowledge Base Button */}
            <button
              onClick={() => onNavigate('knowledge-base')}
              className={`flex items-center px-3 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                currentPage === 'knowledge-base'
                  ? 'bg-gradient-to-r from-purple-600 to-purple-700 text-white shadow-lg'
                  : 'bg-slate-800/50 text-slate-300 hover:bg-purple-600/20 hover:text-purple-400 border border-slate-600'
              }`}
            >
              <BookOpen className="w-4 h-4 mr-2" />
              Knowledge Base
            </button>

            {/* Support Button */}
            <button
              onClick={() => onNavigate('support')}
              className={`flex items-center px-3 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                currentPage === 'support'
                  ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg'
                  : 'bg-slate-800/50 text-slate-300 hover:bg-blue-600/20 hover:text-blue-400 border border-slate-600'
              }`}
            >
              <HelpCircle className="w-4 h-4 mr-2" />
              Support
            </button>
            
            <div className="hidden sm:flex items-center space-x-2 text-slate-300">
              <User className="w-4 h-4" />
              <span className="text-sm">{user?.name || 'Demo User'}</span>
            </div>
            <Button
              onClick={onSignOut}
              variant="ghost"
              size="sm"
              className="text-slate-400 hover:text-red-400 hover:bg-red-500/10"
            >
              <LogOut className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Navigation Buttons Row */}
        <div className="pb-4">
          <div className="flex flex-wrap gap-2 justify-center">
            {activeModules.map((button) => {
              const Icon = button.icon;
              const isActive = currentPage === button.id;
              const hasAnnualSubscription = user && (user.subscription_tier === 'annual' || user.role === 'admin' || user.role === 'super_admin');
              const canAccess = !button.requiresAnnual || hasAnnualSubscription;
              
              return (
                <button
                  key={button.id}
                  onClick={() => canAccess ? onNavigate(button.id) : alert('This feature is available for Annual Subscribers only. Upgrade your subscription to access the Growth Acceleration Engine.')}
                  className={`flex flex-col items-center px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg transform scale-105'
                      : `bg-slate-800/50 text-slate-300 border border-slate-600 ${canAccess ? button.color : 'opacity-75 cursor-not-allowed'}`
                  }`}
                  disabled={!canAccess}
                >
                  <div className="flex items-center">
                    <Icon className="w-4 h-4 mr-2" />
                    {button.label}
                  </div>
                  {button.requiresAnnual && (
                    <div className="text-xs text-red-400 mt-1 font-semibold">
                      {hasAnnualSubscription ? '✓ Annual Access' : 'Annual Subscribers Only'}
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;