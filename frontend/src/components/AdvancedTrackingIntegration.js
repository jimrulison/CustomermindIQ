import React, { useEffect, useState } from 'react';

/**
 * Advanced Tracking Integration Component
 * Handles conversion tracking for the affiliate system
 */
const AdvancedTrackingIntegration = ({ 
    onConversionTracked = null,
    debug = false 
}) => {
    const [trackingStatus, setTrackingStatus] = useState('initializing');
    const [tracker, setTracker] = useState(null);
    const [helpers, setHelpers] = useState(null);

    useEffect(() => {
        // Initialize tracking when component mounts
        const initializeTracking = () => {
            if (window.AdvancedAffiliateTracker) {
                const trackerInstance = new window.AdvancedAffiliateTracker({
                    debug: debug,
                    enableFingerprinting: true,
                    enablePixelTracking: true
                });
                
                const helpersInstance = new window.AffiliateTrackingHelpers(trackerInstance);
                
                setTracker(trackerInstance);
                setHelpers(helpersInstance);
                setTrackingStatus('ready');

                if (debug) {
                    console.log('🚀 Advanced tracking initialized', { tracker: trackerInstance, helpers: helpersInstance });
                }

                // Listen for conversion events
                window.addEventListener('affiliate_conversion_tracked', (event) => {
                    console.log('✅ Conversion tracked:', event.detail);
                    if (onConversionTracked) {
                        onConversionTracked(event.detail);
                    }
                });

            } else {
                console.warn('⚠️ Advanced Affiliate Tracker not found. Please ensure the tracking script is loaded.');
                setTrackingStatus('error');
            }
        };

        // Check if script is already loaded
        if (window.AdvancedAffiliateTracker) {
            initializeTracking();
        } else {
            // Wait for script to load
            const checkInterval = setInterval(() => {
                if (window.AdvancedAffiliateTracker) {
                    clearInterval(checkInterval);
                    initializeTracking();
                }
            }, 100);

            // Clear interval after 5 seconds to prevent infinite checking
            setTimeout(() => {
                clearInterval(checkInterval);
                if (trackingStatus === 'initializing') {
                    setTrackingStatus('timeout');
                    console.error('❌ Tracking script failed to load within 5 seconds');
                }
            }, 5000);
        }
    }, [debug, onConversionTracked]);

    // Expose tracking functions globally for easy access
    useEffect(() => {
        if (tracker && helpers) {
            // Make tracking functions available globally
            window.trackAffiliatePurchase = (orderData) => {
                return helpers.trackPurchase(orderData);
            };

            window.trackAffiliateLead = (leadData) => {
                return helpers.trackLead(leadData);
            };

            window.trackAffiliateSubscription = (subscriptionData) => {
                return helpers.trackSubscription(subscriptionData);
            };

            window.trackAffiliateConversion = (conversionData) => {
                return tracker.trackConversion(conversionData);
            };

            window.getAffiliateTrackingData = () => {
                return tracker.getTrackingData();
            };

            window.hasAffiliateTracking = () => {
                return tracker.hasTrackingData();
            };

            // Set global flag that tracking is ready
            window._advancedTrackingReady = true;

            if (debug) {
                console.log('🌐 Global tracking functions exposed:', {
                    trackAffiliatePurchase: 'trackAffiliatePurchase(orderData)',
                    trackAffiliateLead: 'trackAffiliateLead(leadData)',
                    trackAffiliateSubscription: 'trackAffiliateSubscription(subscriptionData)',
                    trackAffiliateConversion: 'trackAffiliateConversion(conversionData)',
                    getAffiliateTrackingData: 'getAffiliateTrackingData()',
                    hasAffiliateTracking: 'hasAffiliateTracking()'
                });
            }
        }
    }, [tracker, helpers, debug]);

    if (debug) {
        return (
            <div style={{ 
                position: 'fixed', 
                top: '10px', 
                right: '10px', 
                background: '#000', 
                color: '#fff', 
                padding: '10px', 
                borderRadius: '5px',
                fontSize: '12px',
                zIndex: 9999,
                maxWidth: '300px'
            }}>
                <div><strong>🔍 Advanced Tracking Status</strong></div>
                <div>Status: {trackingStatus}</div>
                {tracker && (
                    <>
                        <div>Has Tracking: {tracker.hasTrackingData() ? '✅' : '❌'}</div>
                        {tracker.hasTrackingData() && (
                            <div>Tracking ID: {tracker.getTrackingData().trackingId}</div>
                        )}
                    </>
                )}
            </div>
        );
    }

    return null; // This component doesn't render anything visible in production
};

/**
 * Hook for using advanced tracking in React components
 */
export const useAdvancedTracking = (debug = false) => {
    const [isReady, setIsReady] = useState(false);
    const [trackingData, setTrackingData] = useState(null);

    useEffect(() => {
        const checkReady = () => {
            if (window._advancedTrackingReady) {
                setIsReady(true);
                if (window.getAffiliateTrackingData) {
                    setTrackingData(window.getAffiliateTrackingData());
                }
            }
        };

        // Check immediately
        checkReady();

        // Set up interval to check periodically
        const interval = setInterval(checkReady, 500);

        return () => clearInterval(interval);
    }, []);

    const trackPurchase = (orderData) => {
        if (window.trackAffiliatePurchase) {
            return window.trackAffiliatePurchase(orderData);
        }
        console.warn('Advanced tracking not ready for purchase tracking');
        return Promise.resolve(null);
    };

    const trackLead = (leadData) => {
        if (window.trackAffiliateLead) {
            return window.trackAffiliateLead(leadData);
        }
        console.warn('Advanced tracking not ready for lead tracking');
        return Promise.resolve(null);
    };

    const trackSubscription = (subscriptionData) => {
        if (window.trackAffiliateSubscription) {
            return window.trackAffiliateSubscription(subscriptionData);
        }
        console.warn('Advanced tracking not ready for subscription tracking');
        return Promise.resolve(null);
    };

    const trackConversion = (conversionData) => {
        if (window.trackAffiliateConversion) {
            return window.trackAffiliateConversion(conversionData);
        }
        console.warn('Advanced tracking not ready for conversion tracking');
        return Promise.resolve(null);
    };

    const hasTracking = () => {
        return window.hasAffiliateTracking ? window.hasAffiliateTracking() : false;
    };

    return {
        isReady,
        trackingData,
        trackPurchase,
        trackLead,
        trackSubscription,
        trackConversion,
        hasTracking
    };
};

/**
 * Trial Registration Tracking Component
 * Automatically tracks trial registrations as conversions
 */
export const TrialTrackingIntegration = () => {
    const { trackLead, isReady, hasTracking } = useAdvancedTracking();

    useEffect(() => {
        // Listen for trial registration events
        const handleTrialRegistration = (event) => {
            const { email, firstName, lastName, companyName } = event.detail || {};
            
            if (email && isReady && hasTracking()) {
                trackLead({
                    email: email,
                    customerId: email,
                    value: 0,
                    customData: {
                        eventType: 'trial_registration',
                        firstName: firstName,
                        lastName: lastName,
                        companyName: companyName,
                        source: 'trial_signup_form'
                    }
                });
                
                console.log('🎯 Trial registration tracked for affiliate:', email);
            }
        };

        // Listen for custom trial registration events
        window.addEventListener('trial_registered', handleTrialRegistration);
        
        return () => {
            window.removeEventListener('trial_registered', handleTrialRegistration);
        };
    }, [trackLead, isReady, hasTracking]);

    return null;
};

/**
 * Subscription Tracking Component
 * Automatically tracks subscription purchases as conversions
 */
export const SubscriptionTrackingIntegration = () => {
    const { trackSubscription, isReady, hasTracking } = useAdvancedTracking();

    useEffect(() => {
        // Listen for subscription events
        const handleSubscriptionPurchase = (event) => {
            const subscriptionData = event.detail || {};
            
            if (subscriptionData.email && isReady && hasTracking()) {
                trackSubscription({
                    email: subscriptionData.email,
                    customerId: subscriptionData.customerId || subscriptionData.email,
                    value: subscriptionData.monthlyValue || subscriptionData.annualValue || 0,
                    planId: subscriptionData.planId,
                    planName: subscriptionData.planName
                });
                
                console.log('💰 Subscription tracked for affiliate:', subscriptionData);
            }
        };

        // Listen for custom subscription events
        window.addEventListener('subscription_purchased', handleSubscriptionPurchase);
        
        return () => {
            window.removeEventListener('subscription_purchased', handleSubscriptionPurchase);
        };
    }, [trackSubscription, isReady, hasTracking]);

    return null;
};

export default AdvancedTrackingIntegration;