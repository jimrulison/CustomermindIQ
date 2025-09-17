import React from 'react';
import { HelmetProvider } from 'react-helmet-async';
import SEOHead from './SEOHead';
import StructuredDataScript from './StructuredDataScript';
import { generateOrganizationSchema } from '../utils/seoData';

// Global SEO wrapper component
const SEOWrapper = ({ children }) => {
  // Global structured data that appears on every page
  const globalStructuredData = generateOrganizationSchema();

  return (
    <HelmetProvider>
      {/* Global SEO Tags */}
      <SEOHead
        title="CustomerMind IQ - AI-Powered Customer Intelligence Platform"
        description="Transform your business with AI-powered customer intelligence. 91.8% accurate churn prediction, 300-500% ROI, real-time analytics. Free 7-day trial."
        keywords="customer intelligence, AI analytics, churn prediction, business intelligence, customer success, marketing automation"
        canonicalUrl="https://customermindiq.com"
      />
      
      {/* Global Structured Data */}
      <StructuredDataScript data={globalStructuredData} />
      
      {/* Global Meta Tags */}
      {/* Preconnect to external domains for performance */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
      <link rel="preconnect" href="https://cdnjs.cloudflare.com" />
      
      {/* DNS Prefetch for external resources */}
      <link rel="dns-prefetch" href="//www.google-analytics.com" />
      <link rel="dns-prefetch" href="//www.googletagmanager.com" />
      
      {/* Favicon and icons */}
      <link rel="icon" href="/favicon.ico" />
      <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
      <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
      <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
      <link rel="manifest" href="/site.webmanifest" />
      
      {/* Security headers */}
      <meta httpEquiv="X-Content-Type-Options" content="nosniff" />
      <meta httpEquiv="X-Frame-Options" content="DENY" />
      <meta httpEquiv="X-XSS-Protection" content="1; mode=block" />
      <meta httpEquiv="Referrer-Policy" content="strict-origin-when-cross-origin" />
      
      {/* Performance hints */}
      <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
      
      {children}
    </HelmetProvider>
  );
};

// Enhanced page wrapper with dynamic SEO
export const PageSEOWrapper = ({ 
  children, 
  title, 
  description, 
  keywords, 
  canonicalUrl, 
  structuredData,
  breadcrumbs,
  noIndex = false,
  pageType = 'website'
}) => {
  return (
    <>
      <SEOHead
        title={title}
        description={description}
        keywords={keywords}
        canonicalUrl={canonicalUrl}
        pageType={pageType}
        structuredData={structuredData}
      />
      
      {/* Breadcrumb structured data */}
      {breadcrumbs && (
        <StructuredDataScript 
          data={{
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumbs.map((crumb, index) => ({
              "@type": "ListItem",
              "position": index + 1,
              "name": crumb.name,
              "item": crumb.url
            }))
          }}
        />
      )}
      
      {/* No index directive if needed */}
      {noIndex && <meta name="robots" content="noindex, nofollow" />}
      
      {children}
    </>
  );
};

export default SEOWrapper;