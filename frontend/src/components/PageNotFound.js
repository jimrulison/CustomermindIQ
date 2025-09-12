import React from 'react';
import { Button } from './ui/button';
import { AlertTriangle, Home, ArrowLeft, Search } from 'lucide-react';

const PageNotFound = ({ onNavigate, onGoBack }) => {
  const suggestedPages = [
    { id: 'customer-analytics-dashboard', label: 'Customer Analytics', icon: Home },
    { id: 'website-analytics-dashboard', label: 'Website Analytics', icon: Search },
    { id: 'support', label: 'Support Center', icon: AlertTriangle },
    { id: 'training', label: 'Training & Documentation', icon: Home }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center">
        {/* Error Icon */}
        <div className="mb-8">
          <AlertTriangle className="w-24 h-24 mx-auto text-orange-500 mb-4" />
          <h1 className="text-6xl font-bold text-gray-900 mb-2">404</h1>
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Page Not Found</h2>
          <p className="text-gray-600 text-lg leading-relaxed">
            The page you're looking for doesn't exist or has been moved. 
            This could be due to a broken link or an outdated bookmark.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          {onGoBack && (
            <Button 
              onClick={onGoBack}
              variant="outline" 
              className="flex items-center min-h-[48px]"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Go Back
            </Button>
          )}
          <Button 
            onClick={() => onNavigate('customer-analytics-dashboard')}
            className="flex items-center min-h-[48px]"
          >
            <Home className="w-4 h-4 mr-2" />
            Go to Dashboard
          </Button>
        </div>

        {/* Suggested Pages */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Try visiting one of these pages instead:
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {suggestedPages.map((page) => {
              const Icon = page.icon;
              return (
                <Button
                  key={page.id}
                  onClick={() => onNavigate(page.id)}
                  variant="ghost"
                  className="flex items-center justify-start p-4 h-auto text-left min-h-[48px] hover:bg-gray-50"
                >
                  <Icon className="w-5 h-5 mr-3 text-blue-600" />
                  <span>{page.label}</span>
                </Button>
              );
            })}
          </div>
        </div>

        {/* Help Text */}
        <div className="mt-8 text-sm text-gray-500">
          <p>
            If you continue to experience issues, please{' '}
            <button 
              onClick={() => onNavigate('support')}
              className="text-blue-600 hover:text-blue-800 underline"
            >
              contact support
            </button>{' '}
            or visit our{' '}
            <button 
              onClick={() => onNavigate('training')}
              className="text-blue-600 hover:text-blue-800 underline"
            >
              help documentation
            </button>.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PageNotFound;