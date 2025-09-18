import React, { useState, useEffect, useRef } from 'react';
import { X, Settings, Shield, BarChart3, Target } from 'lucide-react';
import ScreenReaderAnnouncer, { useScreenReaderAnnouncer } from './ScreenReaderAnnouncer';

const CookieConsent = () => {
  const [showBanner, setShowBanner] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [consent, setConsent] = useState({
    essential: true, // Always true, can't be disabled
    analytics: false,
    marketing: false,
    preferences: false
  });

  const detailsRef = useRef(null);
  const { announce, announceSuccess, ScreenReaderAnnouncer: Announcer } = useScreenReaderAnnouncer();

  useEffect(() => {
    // Check if user has already given consent
    const savedConsent = localStorage.getItem('cookieConsent');
    if (!savedConsent) {
      setShowBanner(true);
    } else {
      setConsent(JSON.parse(savedConsent));
    }
  }, []);

  const handleAcceptAll = () => {
    const allConsent = {
      essential: true,
      analytics: true,
      marketing: true,
      preferences: true
    };
    setConsent(allConsent);
    localStorage.setItem('cookieConsent', JSON.stringify(allConsent));
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    setShowBanner(false);
    setShowDetails(false);
    
    // Initialize analytics if accepted
    if (allConsent.analytics) {
      initializeAnalytics();
    }
    
    announceSuccess('All cookies accepted. Your preferences have been saved.');
  };

  const handleRejectAll = () => {
    const essentialOnly = {
      essential: true,
      analytics: false,
      marketing: false,
      preferences: false
    };
    setConsent(essentialOnly);
    localStorage.setItem('cookieConsent', JSON.stringify(essentialOnly));
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    setShowBanner(false);
    setShowDetails(false);
    
    announceSuccess('Essential cookies only. Your preferences have been saved.');
  };

  const handleSavePreferences = () => {
    localStorage.setItem('cookieConsent', JSON.stringify(consent));
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    setShowBanner(false);
    setShowDetails(false);
    
    // Initialize analytics if accepted
    if (consent.analytics) {
      initializeAnalytics();
    }
    
    announceSuccess('Cookie preferences saved successfully.');
  };

  const handleShowDetails = () => {
    setShowDetails(true);
    announce('Cookie preferences dialog opened. Use Tab to navigate through options.');
    
    // Focus the details modal after it opens
    setTimeout(() => {
      if (detailsRef.current) {
        detailsRef.current.focus();
      }
    }, 100);
  };

  const handleHideDetails = () => {
    setShowDetails(false);
    announce('Cookie preferences dialog closed.');
  };

  const initializeAnalytics = () => {
    // Initialize Google Analytics or other analytics tools
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('consent', 'update', {
        'analytics_storage': 'granted',
        'ad_storage': consent.marketing ? 'granted' : 'denied'
      });
    }
  };

  const handleConsentChange = (category, value) => {
    if (category === 'essential') return; // Essential cookies can't be disabled
    setConsent(prev => ({
      ...prev,
      [category]: value
    }));
  };

  const cookieCategories = [
    {
      id: 'essential',
      name: 'Essential Cookies',
      description: 'These cookies are necessary for the website to function and cannot be switched off.',
      icon: Shield,
      examples: 'Session management, security tokens, login state',
      required: true
    },
    {
      id: 'analytics',
      name: 'Analytics Cookies',
      description: 'These cookies help us understand how visitors interact with our website.',
      icon: BarChart3,
      examples: 'Google Analytics, usage statistics, performance monitoring',
      required: false
    },
    {
      id: 'marketing',
      name: 'Marketing Cookies',
      description: 'These cookies are used to show you relevant advertisements.',
      icon: Target,
      examples: 'Ad targeting, conversion tracking, remarketing',
      required: false
    },
    {
      id: 'preferences',
      name: 'Preference Cookies',
      description: 'These cookies remember your preferences and settings.',
      icon: Settings,
      examples: 'Language settings, theme preferences, customization',
      required: false
    }
  ];

  if (!showBanner) return null;

  return (
    <>
      <Announcer />
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-25 z-40" 
        style={{ display: showDetails ? 'block' : 'none' }}
        aria-hidden={!showDetails}
      />
      
      {/* Cookie Banner */}
      <section 
        className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-2xl z-50 transform transition-transform duration-300"
        role="dialog"
        aria-modal={showDetails}
        aria-labelledby="cookie-banner-title"
        aria-describedby="cookie-banner-description"
      >
        {!showDetails ? (
          // Simple banner view
          <div className="max-w-7xl mx-auto px-4 py-6">
            <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <Shield className="h-5 w-5 text-blue-600" aria-hidden="true" />
                  <h3 id="cookie-banner-title" className="text-lg font-semibold text-gray-900">Cookie Preferences</h3>
                </div>
                <p id="cookie-banner-description" className="text-gray-600 text-sm">
                  We use cookies to enhance your experience, analyze site usage, and personalize content. 
                  Choose your cookie preferences or accept all to continue.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-3 min-w-max">
                <button
                  onClick={handleShowDetails}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  aria-describedby="cookie-banner-description"
                >
                  <Settings className="h-4 w-4 inline mr-2" aria-hidden="true" />
                  Customize
                </button>
                <button
                  onClick={handleRejectAll}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  aria-describedby="cookie-banner-description"
                >
                  Reject All
                </button>
                <button
                  onClick={handleAcceptAll}
                  className="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  aria-describedby="cookie-banner-description"
                >
                  Accept All
                </button>
              </div>
            </div>
          </div>
        ) : (
          // Detailed preferences view
          <div className="max-w-4xl mx-auto px-4 py-6 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Cookie Preferences</h3>
              <button
                onClick={() => setShowDetails(false)}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <p className="text-gray-600 mb-6">
              We respect your privacy. Please choose which types of cookies you want to allow. 
              These settings will only apply to this browser and device.
            </p>
            
            <div className="space-y-6">
              {cookieCategories.map((category) => {
                const Icon = category.icon;
                const isEnabled = consent[category.id];
                
                return (
                  <div key={category.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <Icon className="h-5 w-5 text-blue-600" />
                          <h4 className="font-medium text-gray-900">{category.name}</h4>
                          {category.required && (
                            <span className="px-2 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-full">
                              Required
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{category.description}</p>
                        <p className="text-xs text-gray-500">
                          <strong>Examples:</strong> {category.examples}
                        </p>
                      </div>
                      
                      <div className="ml-4">
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={isEnabled}
                            onChange={(e) => handleConsentChange(category.id, e.target.checked)}
                            disabled={category.required}
                            className="sr-only peer"
                          />
                          <div className={`relative w-11 h-6 rounded-full transition-colors ${
                            category.required 
                              ? 'bg-gray-300 cursor-not-allowed' 
                              : isEnabled 
                                ? 'bg-blue-600 peer-hover:bg-blue-700' 
                                : 'bg-gray-200 peer-hover:bg-gray-300'
                          }`}>
                            <div className={`absolute top-[2px] left-[2px] bg-white border border-gray-300 rounded-full h-5 w-5 transition-transform ${
                              isEnabled ? 'translate-x-5' : 'translate-x-0'
                            }`} />
                          </div>
                        </label>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
            
            <div className="flex flex-col sm:flex-row gap-3 mt-8 justify-end">
              <button
                onClick={handleRejectAll}
                className="px-6 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Reject All
              </button>
              <button
                onClick={handleSavePreferences}
                className="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Save Preferences
              </button>
            </div>
          </div>
        )}
      </section>
    </>
  );
};

export default CookieConsent;