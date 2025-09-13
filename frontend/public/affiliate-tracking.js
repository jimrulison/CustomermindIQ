// Affiliate Tracking Script for CustomerMindIQ
class AffiliateTracker {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://customer-mind-iq-6.preview.emergentagent.com';
        this.trackPageView();
    }

    generateSessionId() {
        return 'sess_' + Math.random().toString(36).substr(2, 16);
    }

    getAffiliateParams() {
        const urlParams = new URLSearchParams(window.location.search);
        return {
            affiliateId: urlParams.get('ref'),
            campaign: urlParams.get('campaign'),
            utmSource: urlParams.get('utm_source'),
            utmMedium: urlParams.get('utm_medium'),
            utmCampaign: urlParams.get('utm_campaign')
        };
    }

    trackPageView() {
        const params = this.getAffiliateParams();
        if (params.affiliateId) {
            // Store in localStorage for session tracking
            localStorage.setItem('affiliate_data', JSON.stringify({
                ...params,
                sessionId: this.sessionId,
                timestamp: new Date().toISOString()
            }));

            // Send tracking data
            this.sendTrackingData('pageview', params);
        }
    }

    trackTrialSignup(customerData) {
        const affiliateData = JSON.parse(localStorage.getItem('affiliate_data') || '{}');
        if (affiliateData.affiliateId) {
            this.sendTrackingData('trial_signup', {
                ...affiliateData,
                customerEmail: customerData.email,
                customerName: customerData.name,
                sessionId: this.sessionId
            });
        }
    }

    trackConversion(customerData, planData) {
        const affiliateData = JSON.parse(localStorage.getItem('affiliate_data') || '{}');
        if (affiliateData.affiliateId) {
            this.sendTrackingData('conversion', {
                ...affiliateData,
                customerId: customerData.id,
                planType: planData.type,
                billingCycle: planData.cycle,
                amount: planData.amount,
                sessionId: this.sessionId
            });
        }
    }

    sendTrackingData(eventType, data) {
        const trackingData = {
            eventType,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            referrer: document.referrer,
            ip: null, // Will be captured server-side
            landing_page: window.location.href,
            ...data
        };

        fetch(`${this.backendUrl}/api/affiliate/track/event`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(trackingData)
        }).catch(err => console.warn('Affiliate tracking failed:', err));
    }

    // Get affiliate data for payment processing
    getAffiliateDataForPayment() {
        const affiliateData = JSON.parse(localStorage.getItem('affiliate_data') || '{}');
        return {
            affiliate_id: affiliateData.affiliateId,
            session_id: affiliateData.sessionId
        };
    }
}

// Initialize tracker
window.affiliateTracker = new AffiliateTracker();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AffiliateTracker;
}