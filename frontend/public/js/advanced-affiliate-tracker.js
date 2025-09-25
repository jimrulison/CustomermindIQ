/**
 * Advanced Multi-Method Client-Side Tracking System
 * Works with the Python backend to ensure no lost conversions
 */

class AdvancedAffiliateTracker {
    constructor(config = {}) {
        this.config = {
            apiBaseUrl: config.apiBaseUrl || window.location.origin + '/api/v2/track',
            cookieDomain: config.cookieDomain || window.location.hostname,
            cookieExpireDays: config.cookieExpireDays || 90,
            debug: config.debug || false,
            enableFingerprinting: config.enableFingerprinting !== false,
            enablePixelTracking: config.enablePixelTracking !== false,
            ...config
        };
        
        this.trackingData = {};
        this.fingerprint = null;
        this.init();
    }
    
    async init() {
        if (this.config.debug) {
            console.log('🔍 Advanced Affiliate Tracker initialized', this.config);
        }
        
        // Generate browser fingerprint if enabled
        if (this.config.enableFingerprinting) {
            this.fingerprint = await this.generateFingerprint();
        }
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Load any existing tracking data from cookies/localStorage
        this.loadExistingTrackingData();
        
        // If we have affiliate parameters in URL, track the click
        this.checkForAffiliateClick();
    }
    
    /**
     * Generate unique browser fingerprint for cross-device tracking
     */
    async generateFingerprint() {
        const fingerprint = {
            screen_resolution: `${screen.width}x${screen.height}`,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            language: navigator.language,
            platform: navigator.platform,
            user_agent: navigator.userAgent,
            colorDepth: screen.colorDepth,
            pixelDepth: screen.pixelDepth,
            cookieEnabled: navigator.cookieEnabled,
            doNotTrack: navigator.doNotTrack,
            hardwareConcurrency: navigator.hardwareConcurrency || 'unknown'
        };
        
        // Canvas fingerprint (if available)
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('Advanced tracking fingerprint 🔍', 2, 2);
            fingerprint.canvas_fingerprint = canvas.toDataURL().slice(-50); // Last 50 chars
        } catch (e) {
            fingerprint.canvas_fingerprint = 'blocked';
        }
        
        // WebGL fingerprint (if available)
        try {
            const gl = document.createElement('canvas').getContext('webgl');
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            fingerprint.webgl_fingerprint = JSON.stringify({
                vendor: gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL),
                renderer: gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
            });
        } catch (e) {
            fingerprint.webgl_fingerprint = 'blocked';
        }
        
        // Generate hash from all fingerprint data
        const fingerprintString = JSON.stringify(fingerprint);
        const hash = await this.generateHash(fingerprintString);
        
        if (this.config.debug) {
            console.log('🖐️ Browser fingerprint generated:', hash);
        }
        
        return {
            data: fingerprint,
            hash: hash
        };
    }
    
    /**
     * Generate SHA-256 hash (Web Crypto API)
     */
    async generateHash(text) {
        if (!window.crypto || !window.crypto.subtle) {
            // Fallback for older browsers
            return this.simpleHash(text);
        }
        
        const encoder = new TextEncoder();
        const data = encoder.encode(text);
        const hashBuffer = await window.crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
    
    /**
     * Simple hash fallback for older browsers
     */
    simpleHash(text) {
        let hash = 0;
        for (let i = 0; i < text.length; i++) {
            const char = text.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return Math.abs(hash).toString(16);
    }
    
    /**
     * Set up event listeners for various tracking events
     */
    setupEventListeners() {
        // Track page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.trackEvent('page_visible');
            }
        });
        
        // Track clicks on affiliate links
        document.addEventListener('click', (event) => {
            const link = event.target.closest('a');
            if (link && this.isAffiliateLink(link.href)) {
                this.trackLinkClick(link);
            }
        });
        
        // Track form submissions (for lead tracking)
        document.addEventListener('submit', (event) => {
            if (this.hasTrackingData()) {
                this.trackFormSubmission(event.target);
            }
        });
        
        // Track scroll depth for engagement
        let maxScroll = 0;
        window.addEventListener('scroll', this.throttle(() => {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
                if (maxScroll % 25 === 0) { // Track at 25%, 50%, 75%, 100%
                    this.trackEvent('scroll_depth', { percent: maxScroll });
                }
            }
        }, 1000));
    }
    
    /**
     * Check URL parameters for affiliate tracking
     */
    checkForAffiliateClick() {
        const urlParams = new URLSearchParams(window.location.search);
        const affiliateId = urlParams.get('ref') || urlParams.get('affiliate') || urlParams.get('aff');
        const siteId = urlParams.get('site_id') || 'main_site';
        const campaignId = urlParams.get('campaign') || urlParams.get('utm_campaign');
        
        if (affiliateId) {
            this.trackClick(affiliateId, siteId, campaignId);
        }
    }
    
    /**
     * Track affiliate click with advanced attribution
     */
    async trackClick(affiliateId, siteId, campaignId = null) {
        try {
            const trackingPayload = {
                affiliate_id: affiliateId,
                site_id: siteId,
                campaign_id: campaignId,
                fingerprint_data: this.fingerprint ? this.fingerprint.data : {}
            };
            
            const response = await fetch(`${this.config.apiBaseUrl}/click`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(trackingPayload)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Store tracking data in multiple places
                this.storeTrackingData({
                    trackingId: result.tracking_id,
                    affiliateId: affiliateId,
                    siteId: siteId,
                    campaignId: campaignId,
                    timestamp: new Date().toISOString(),
                    fraudScore: result.fraud_score
                });
                
                // Load tracking pixel if enabled
                if (this.config.enablePixelTracking && result.pixel_url) {
                    this.loadTrackingPixel(result.pixel_url);
                }
                
                if (this.config.debug) {
                    console.log('🎯 Click tracked successfully:', result);
                }
                
                // Fire custom event for other scripts to listen to
                this.fireCustomEvent('affiliate_click_tracked', result);
                
                return result;
            }
        } catch (error) {
            console.error('❌ Failed to track click:', error);
        }
    }
    
    /**
     * Track conversion with multi-method attribution
     */
    async trackConversion(conversionData) {
        try {
            const trackingData = this.getTrackingData();
            
            const conversionPayload = {
                affiliate_id: trackingData.affiliateId || conversionData.affiliateId,
                site_id: trackingData.siteId || conversionData.siteId || 'main_site',
                customer_email: conversionData.customerEmail,
                customer_id: conversionData.customerId,
                event_type: conversionData.eventType || 'sale',
                conversion_value: conversionData.value || 0,
                currency: conversionData.currency || 'USD',
                product_id: conversionData.productId,
                product_name: conversionData.productName,
                order_id: conversionData.orderId,
                custom_data: {
                    fingerprint_hash: this.fingerprint ? this.fingerprint.hash : null,
                    page_url: window.location.href,
                    user_agent: navigator.userAgent,
                    timestamp: new Date().toISOString(),
                    ...conversionData.customData
                }
            };
            
            const response = await fetch(`${this.config.apiBaseUrl}/conversion`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(conversionPayload)
            });
            
            const result = await response.json();
            
            if (result.success) {
                if (this.config.debug) {
                    console.log('💰 Conversion tracked successfully:', result);
                }
                
                // Fire custom event
                this.fireCustomEvent('affiliate_conversion_tracked', result);
                
                // Clear tracking data after successful conversion
                this.clearTrackingData();
                
                return result;
            }
        } catch (error) {
            console.error('❌ Failed to track conversion:', error);
        }
    }
    
    /**
     * Track email opens (called from email tracking pixels)
     */
    async trackEmailOpen(affiliateId, customerEmail, campaignId) {
        try {
            const response = await fetch(`${this.config.apiBaseUrl}/email/open?affiliate_id=${encodeURIComponent(affiliateId)}&customer_email=${encodeURIComponent(customerEmail)}&email_campaign_id=${encodeURIComponent(campaignId)}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            return await response.json();
        } catch (error) {
            console.error('❌ Failed to track email open:', error);
        }
    }
    
    /**
     * Track email clicks
     */
    async trackEmailClick(affiliateId, customerEmail, campaignId, linkId = null) {
        try {
            const response = await fetch(`${this.config.apiBaseUrl}/email/click?affiliate_id=${encodeURIComponent(affiliateId)}&customer_email=${encodeURIComponent(customerEmail)}&email_campaign_id=${encodeURIComponent(campaignId)}${linkId ? '&link_id=' + encodeURIComponent(linkId) : ''}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            return await response.json();
        } catch (error) {
            console.error('❌ Failed to track email click:', error);
        }
    }
    
    /**
     * Store tracking data in multiple places for reliability
     */
    storeTrackingData(data) {
        this.trackingData = data;
        
        // Store in cookie (primary method)
        this.setCookie('_affiliate_tracking', JSON.stringify(data), this.config.cookieExpireDays);
        
        // Store in sessionStorage (backup)
        try {
            sessionStorage.setItem('_affiliate_tracking', JSON.stringify(data));
        } catch (e) {
            // Handle storage quota exceeded or disabled
        }
        
        // Store in localStorage (backup)
        try {
            localStorage.setItem('_affiliate_tracking', JSON.stringify(data));
        } catch (e) {
            // Handle storage quota exceeded or disabled
        }
        
        // Store in memory
        window._affiliateTrackingData = data;
        
        if (this.config.debug) {
            console.log('💾 Tracking data stored:', data);
        }
    }
    
    /**
     * Load existing tracking data from various sources
     */
    loadExistingTrackingData() {
        // Try to load from cookie first
        let data = this.getCookie('_affiliate_tracking');
        
        // Try sessionStorage if cookie not found
        if (!data) {
            try {
                data = sessionStorage.getItem('_affiliate_tracking');
            } catch (e) {
                // Storage disabled
            }
        }
        
        // Try localStorage if still not found
        if (!data) {
            try {
                data = localStorage.getItem('_affiliate_tracking');
            } catch (e) {
                // Storage disabled
            }
        }
        
        // Try memory if still not found
        if (!data && window._affiliateTrackingData) {
            data = JSON.stringify(window._affiliateTrackingData);
        }
        
        if (data) {
            try {
                this.trackingData = JSON.parse(data);
                if (this.config.debug) {
                    console.log('📂 Existing tracking data loaded:', this.trackingData);
                }
            } catch (e) {
                console.error('Failed to parse tracking data:', e);
            }
        }
    }
    
    /**
     * Get current tracking data
     */
    getTrackingData() {
        return this.trackingData;
    }
    
    /**
     * Check if we have tracking data
     */
    hasTrackingData() {
        return this.trackingData && this.trackingData.trackingId;
    }
    
    /**
     * Clear tracking data after conversion
     */
    clearTrackingData() {
        this.trackingData = {};
        this.deleteCookie('_affiliate_tracking');
        
        try {
            sessionStorage.removeItem('_affiliate_tracking');
            localStorage.removeItem('_affiliate_tracking');
        } catch (e) {
            // Storage disabled
        }
        
        delete window._affiliateTrackingData;
        
        if (this.config.debug) {
            console.log('🗑️ Tracking data cleared');
        }
    }
    
    /**
     * Load tracking pixel for additional attribution
     */
    loadTrackingPixel(pixelUrl) {
        const img = new Image();
        img.src = pixelUrl;
        img.style.display = 'none';
        img.onload = () => {
            if (this.config.debug) {
                console.log('📸 Tracking pixel loaded');
            }
        };
    }
    
    /**
     * Track custom events
     */
    async trackEvent(eventName, eventData = {}) {
        if (!this.hasTrackingData()) return;
        
        const trackingData = this.getTrackingData();
        
        try {
            // For now, just log the event. In production, you'd send to your analytics
            if (this.config.debug) {
                console.log(`📊 Event tracked: ${eventName}`, eventData);
            }
            
            // You could extend this to send events to your backend
            // await fetch(`${this.config.apiBaseUrl}/event`, { ... });
        } catch (error) {
            console.error('❌ Failed to track event:', error);
        }
    }
    
    /**
     * Track form submissions as leads
     */
    async trackFormSubmission(form) {
        const formData = new FormData(form);
        const email = formData.get('email') || formData.get('email_address');
        
        if (email && this.hasTrackingData()) {
            await this.trackConversion({
                eventType: 'lead',
                customerEmail: email,
                value: 0,
                customData: {
                    form_id: form.id,
                    form_action: form.action
                }
            });
        }
    }
    
    /**
     * Utility functions
     */
    isAffiliateLink(href) {
        return href && (
            href.includes('ref=') ||
            href.includes('affiliate=') ||
            href.includes('aff=') ||
            href.includes('utm_source=')
        );
    }
    
    trackLinkClick(link) {
        if (this.config.debug) {
            console.log('🔗 Affiliate link clicked:', link.href);
        }
        // Additional link tracking logic here
    }
    
    fireCustomEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        window.dispatchEvent(event);
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
    
    // Cookie utilities
    setCookie(name, value, days) {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = `${name}=${value}; expires=${expires}; path=/; domain=${this.config.cookieDomain}; SameSite=Lax`;
    }
    
    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
    
    deleteCookie(name) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${this.config.cookieDomain}`;
    }
}

/**
 * Easy-to-use tracking functions for common scenarios
 */
class AffiliateTrackingHelpers {
    constructor(tracker) {
        this.tracker = tracker;
    }
    
    /**
     * Simple conversion tracking for e-commerce
     */
    async trackPurchase(orderData) {
        return await this.tracker.trackConversion({
            eventType: 'sale',
            customerEmail: orderData.email,
            customerId: orderData.customerId,
            value: orderData.total,
            currency: orderData.currency || 'USD',
            orderId: orderData.orderId,
            productId: orderData.productId,
            productName: orderData.productName
        });
    }
    
    /**
     * Track lead generation (form submissions, signups)
     */
    async trackLead(leadData) {
        return await this.tracker.trackConversion({
            eventType: 'lead',
            customerEmail: leadData.email,
            customerId: leadData.customerId,
            value: leadData.value || 0,
            customData: leadData
        });
    }
    
    /**
     * Track subscription signups
     */
    async trackSubscription(subscriptionData) {
        return await this.tracker.trackConversion({
            eventType: 'sale',
            customerEmail: subscriptionData.email,
            customerId: subscriptionData.customerId,
            value: subscriptionData.monthlyValue || subscriptionData.value,
            productId: subscriptionData.planId,
            productName: subscriptionData.planName
        });
    }
    
    /**
     * Track app downloads
     */
    async trackAppDownload(downloadData) {
        return await this.tracker.trackConversion({
            eventType: 'lead',
            customerEmail: downloadData.email,
            value: 0,
            productId: downloadData.appId,
            productName: downloadData.appName,
            customData: {
                platform: downloadData.platform,
                version: downloadData.version
            }
        });
    }
}

/**
 * Initialize tracker when page loads
 */
(function() {
    // Auto-initialize if config is provided
    if (typeof window.affiliateTrackerConfig !== 'undefined') {
        window.affiliateTracker = new AdvancedAffiliateTracker(window.affiliateTrackerConfig);
        window.affiliateTrackingHelpers = new AffiliateTrackingHelpers(window.affiliateTracker);
        
        console.log('🚀 Advanced Affiliate Tracker auto-initialized');
    }
    
    // Make classes available globally
    window.AdvancedAffiliateTracker = AdvancedAffiliateTracker;
    window.AffiliateTrackingHelpers = AffiliateTrackingHelpers;
})();

/**
 * Usage Examples:
 * 
 * // Basic initialization
 * const tracker = new AdvancedAffiliateTracker({
 *     apiBaseUrl: '/api/v2/track',
 *     debug: true
 * });
 * 
 * // Track a purchase
 * tracker.trackConversion({
 *     eventType: 'sale',
 *     customerEmail: 'customer@example.com',
 *     value: 97.00,
 *     orderId: 'order_123'
 * });
 * 
 * // Using helpers
 * const helpers = new AffiliateTrackingHelpers(tracker);
 * helpers.trackPurchase({
 *     email: 'customer@example.com',
 *     total: 97.00,
 *     orderId: 'order_123'
 * });
 * 
 * // Listen for tracking events
 * window.addEventListener('affiliate_conversion_tracked', (event) => {
 *     console.log('Conversion tracked!', event.detail);
 * });
 */