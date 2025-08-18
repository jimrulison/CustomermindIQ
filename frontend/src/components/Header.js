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
  User
} from 'lucide-react';

const Header = ({ currentPage, onNavigate, onSignOut, user }) => {
  const navigationButtons = [
    {
      id: 'customers',
      label: 'Customer Intelligence',
      icon: Users,
      color: 'hover:bg-blue-600/20 hover:text-blue-400'
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
      icon: Brain,
      color: 'hover:bg-orange-600/20 hover:text-orange-400'
    },
    {
      id: 'analytics',
      label: 'Analytics & Insights',
      icon: TrendingUp,
      color: 'hover:bg-indigo-600/20 hover:text-indigo-400'
    },
    {
      id: 'customer-success',
      label: 'Customer Success',
      icon: Target,
      color: 'hover:bg-cyan-600/20 hover:text-cyan-400'
    },
    {
      id: 'create',
      label: 'Create Campaign',
      icon: Zap,
      color: 'hover:bg-yellow-600/20 hover:text-yellow-400'
    }
  ];

  return (
    <header className="bg-slate-900/95 backdrop-blur-xl border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo Section */}
          <div className="flex items-center">
            <Brain className="w-8 h-8 text-blue-400 mr-3" />
            <h1 className="text-xl font-bold text-white">CustomerMind IQ</h1>
          </div>

          {/* Dashboard Button - Center */}
          <div className="flex-1 flex justify-center">
            <button
              onClick={() => onNavigate('dashboard')}
              className={`px-6 py-2 rounded-lg font-semibold text-sm transition-all duration-200 ${
                currentPage === 'dashboard'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-800/50 text-slate-300 hover:bg-blue-600/20 hover:text-blue-400 border border-slate-600'
              }`}
            >
              <BarChart3 className="w-4 h-4 inline mr-2" />
              DASHBOARD
            </button>
          </div>

          {/* User Info & Sign Out */}
          <div className="flex items-center space-x-4">
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
            {navigationButtons.map((button) => {
              const Icon = button.icon;
              const isActive = currentPage === button.id;
              
              return (
                <button
                  key={button.id}
                  onClick={() => onNavigate(button.id)}
                  className={`flex items-center px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg transform scale-105'
                      : `bg-slate-800/50 text-slate-300 border border-slate-600 ${button.color}`
                  }`}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {button.label}
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