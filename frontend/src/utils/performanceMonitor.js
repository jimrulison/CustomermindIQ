// Performance monitoring utilities for CustomerMind IQ
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.observers = {};
    this.init();
  }

  init() {
    // Initialize performance observers if supported
    if ('PerformanceObserver' in window) {
      this.initLargestContentfulPaint();
      this.initFirstInputDelay();
      this.initCumulativeLayoutShift();
      this.initLongTasks();
    }

    // Monitor page load metrics
    this.initPageLoadMetrics();
    
    // Monitor user interactions
    this.initUserInteractionMetrics();
  }

  // Core Web Vitals monitoring
  initLargestContentfulPaint() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        this.metrics.lcp = Math.round(lastEntry.startTime);
        this.reportMetric('lcp', this.metrics.lcp);
      });
      observer.observe({ type: 'largest-contentful-paint', buffered: true });
      this.observers.lcp = observer;
    } catch (error) {
      console.warn('LCP monitoring not supported:', error);
    }
  }

  initFirstInputDelay() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          this.metrics.fid = Math.round(entry.processingStart - entry.startTime);
          this.reportMetric('fid', this.metrics.fid);
        });
      });
      observer.observe({ type: 'first-input', buffered: true });
      this.observers.fid = observer;
    } catch (error) {
      console.warn('FID monitoring not supported:', error);
    }
  }

  initCumulativeLayoutShift() {
    try {
      let clsValue = 0;
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        }
        this.metrics.cls = Math.round(clsValue * 1000) / 1000;
        this.reportMetric('cls', this.metrics.cls);
      });
      observer.observe({ type: 'layout-shift', buffered: true });
      this.observers.cls = observer;
    } catch (error) {
      console.warn('CLS monitoring not supported:', error);
    }
  }

  initLongTasks() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.duration > 50) {
            this.metrics.longTasks = (this.metrics.longTasks || 0) + 1;
            this.reportMetric('longTask', {
              duration: Math.round(entry.duration),
              startTime: Math.round(entry.startTime)
            });
          }
        });
      });
      observer.observe({ type: 'longtask', buffered: true });
      this.observers.longTasks = observer;
    } catch (error) {
      console.warn('Long tasks monitoring not supported:', error);
    }
  }

  initPageLoadMetrics() {
    window.addEventListener('load', () => {
      setTimeout(() => {
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
          this.metrics.pageLoad = {
            domContentLoaded: Math.round(navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart),
            loadComplete: Math.round(navigation.loadEventEnd - navigation.loadEventStart),
            totalTime: Math.round(navigation.loadEventEnd - navigation.fetchStart),
            dnsLookup: Math.round(navigation.domainLookupEnd - navigation.domainLookupStart),
            tcpConnect: Math.round(navigation.connectEnd - navigation.connectStart),
            serverResponse: Math.round(navigation.responseEnd - navigation.requestStart),
            domProcessing: Math.round(navigation.domComplete - navigation.domLoading)
          };
          this.reportMetric('pageLoad', this.metrics.pageLoad);
        }
      }, 0);
    });
  }

  initUserInteractionMetrics() {
    let interactionCount = 0;
    let totalDelay = 0;

    const trackInteraction = (event) => {
      const startTime = performance.now();
      
      // Use requestIdleCallback to measure interaction delay
      if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
          const delay = performance.now() - startTime;
          if (delay > 100) { // Only track significant delays
            interactionCount++;
            totalDelay += delay;
            this.metrics.avgInteractionDelay = Math.round(totalDelay / interactionCount);
            this.reportMetric('interactionDelay', {
              event: event.type,
              delay: Math.round(delay),
              average: this.metrics.avgInteractionDelay
            });
          }
        });
      }
    };

    ['click', 'touchstart', 'keydown'].forEach(eventType => {
      document.addEventListener(eventType, trackInteraction, { passive: true });
    });
  }

  // Memory usage monitoring
  getMemoryUsage() {
    if ('memory' in performance) {
      return {
        used: Math.round(performance.memory.usedJSHeapSize / 1048576), // MB
        total: Math.round(performance.memory.totalJSHeapSize / 1048576), // MB
        limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576) // MB
      };
    }
    return null;
  }

  // Resource loading monitoring
  getResourceMetrics() {
    const resources = performance.getEntriesByType('resource');
    const metrics = {
      totalResources: resources.length,
      slowResources: resources.filter(r => r.duration > 1000).length,
      largeResources: resources.filter(r => r.transferSize > 500000).length, // >500KB
      averageLoadTime: Math.round(resources.reduce((sum, r) => sum + r.duration, 0) / resources.length),
      cacheHitRate: Math.round((resources.filter(r => r.transferSize === 0).length / resources.length) * 100)
    };
    
    return metrics;
  }

  // Bundle size analysis
  getBundleMetrics() {
    const entries = performance.getEntriesByType('navigation');
    if (entries.length > 0) {
      const navigation = entries[0];
      return {
        transferSize: Math.round(navigation.transferSize / 1024), // KB
        encodedBodySize: Math.round(navigation.encodedBodySize / 1024), // KB
        decodedBodySize: Math.round(navigation.decodedBodySize / 1024), // KB
        compressionRatio: Math.round((1 - navigation.encodedBodySize / navigation.decodedBodySize) * 100) // %
      };
    }
    return null;
  }

  // Report metrics (can be extended to send to analytics)
  reportMetric(name, value) {
    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[Performance] ${name}:`, value);
    }

    // In production, you could send this to your analytics service
    // Example: analytics.track('performance_metric', { name, value });
    
    // Store locally for debugging
    if (!window.customerMindIQMetrics) {
      window.customerMindIQMetrics = {};
    }
    window.customerMindIQMetrics[name] = value;
  }

  // Get all current metrics
  getAllMetrics() {
    return {
      coreWebVitals: {
        lcp: this.metrics.lcp,
        fid: this.metrics.fid,
        cls: this.metrics.cls
      },
      pageLoad: this.metrics.pageLoad,
      memory: this.getMemoryUsage(),
      resources: this.getResourceMetrics(),
      bundle: this.getBundleMetrics(),
      interactions: {
        avgDelay: this.metrics.avgInteractionDelay,
        longTasks: this.metrics.longTasks || 0
      }
    };
  }

  // Clean up observers
  disconnect() {
    Object.values(this.observers).forEach(observer => {
      if (observer && observer.disconnect) {
        observer.disconnect();
      }
    });
  }

  // Performance recommendations based on metrics
  getRecommendations() {
    const recommendations = [];
    const metrics = this.getAllMetrics();

    // LCP recommendations
    if (metrics.coreWebVitals.lcp > 2500) {
      recommendations.push({
        type: 'warning',
        metric: 'LCP',
        issue: 'Largest Contentful Paint is slower than recommended (>2.5s)',
        suggestions: [
          'Optimize images and use modern formats (WebP, AVIF)',
          'Implement lazy loading for below-the-fold content',
          'Reduce server response times',
          'Use a CDN for static assets'
        ]
      });
    }

    // FID recommendations
    if (metrics.coreWebVitals.fid > 100) {
      recommendations.push({
        type: 'warning',
        metric: 'FID',
        issue: 'First Input Delay is higher than recommended (>100ms)',
        suggestions: [
          'Reduce JavaScript execution time',
          'Code split and lazy load non-critical JavaScript',
          'Use web workers for heavy computations',
          'Optimize third-party scripts'
        ]
      });
    }

    // CLS recommendations
    if (metrics.coreWebVitals.cls > 0.1) {
      recommendations.push({
        type: 'warning',
        metric: 'CLS',
        issue: 'Cumulative Layout Shift is higher than recommended (>0.1)',
        suggestions: [
          'Set size attributes on images and videos',
          'Reserve space for dynamically loaded content',
          'Avoid inserting content above existing content',
          'Use CSS aspect-ratio for responsive media'
        ]
      });
    }

    // Memory recommendations
    if (metrics.memory && metrics.memory.used > metrics.memory.limit * 0.8) {
      recommendations.push({
        type: 'error',
        metric: 'Memory',
        issue: 'High memory usage detected',
        suggestions: [
          'Check for memory leaks',
          'Optimize large data structures',
          'Implement pagination for large lists',
          'Use React.memo and useMemo for expensive operations'
        ]
      });
    }

    return recommendations;
  }
}

// Create singleton instance
const performanceMonitor = new PerformanceMonitor();

// Export monitoring functions
export const startPerformanceMonitoring = () => {
  // Already started in constructor
  return performanceMonitor;
};

export const getPerformanceMetrics = () => {
  return performanceMonitor.getAllMetrics();
};

export const getPerformanceRecommendations = () => {
  return performanceMonitor.getRecommendations();
};

export const stopPerformanceMonitoring = () => {
  performanceMonitor.disconnect();
};

// Auto-start monitoring
if (typeof window !== 'undefined') {
  startPerformanceMonitoring();
}

export default performanceMonitor;