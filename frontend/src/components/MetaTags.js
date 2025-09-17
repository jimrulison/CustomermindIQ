import React from 'react';
import { Helmet } from 'react-helmet-async';

// Component for specific page meta tags
export const PageMetaTags = ({ page }) => {
  const metaConfigs = {
    'customer-intelligence': {
      title: "Customer Intelligence Suite - AI-Powered Churn Prediction & Analytics | CustomerMind IQ",
      description: "Reduce customer churn by 30% with 91.8% accurate AI predictions. Advanced customer segmentation, behavioral analysis, and lifetime value optimization. Free trial available.",
      keywords: "customer intelligence, churn prediction, customer analytics, behavioral segmentation, customer lifetime value, AI customer insights, customer success platform",
      canonical: "https://customermindiq.com/customer-intelligence"
    },
    'revenue-analytics': {
      title: "Revenue Analytics Suite - 95% Accurate Revenue Forecasting | CustomerMind IQ", 
      description: "Achieve 95% accurate revenue forecasting 3-6 months in advance. Advanced pricing optimization, profit analysis, and subscription analytics. Boost revenue by 20%+.",
      keywords: "revenue forecasting, pricing optimization, profit margin analysis, subscription analytics, financial reporting, revenue prediction, business intelligence",
      canonical: "https://customermindiq.com/revenue-analytics"
    },
    'marketing-automation': {
      title: "Marketing Automation Pro - 40% Better ROI & Campaign Automation | CustomerMind IQ",
      description: "Increase marketing ROI by 40% with AI-powered automation. Multi-channel campaigns, A/B testing, lead scoring, and personalization. Automate 78.9% of marketing tasks.",
      keywords: "marketing automation, multi-channel marketing, A/B testing, lead scoring, campaign automation, marketing ROI, personalization engine, email marketing",
      canonical: "https://customermindiq.com/marketing-automation"
    },
    'website-intelligence': {
      title: "Website Intelligence Hub - SEO Analytics & Performance Optimization | CustomerMind IQ",
      description: "Optimize website performance and SEO with Core Web Vitals monitoring, keyword tracking, and content analytics. Increase organic traffic by 30%+.",
      keywords: "website analytics, SEO optimization, Core Web Vitals, website performance, keyword tracking, content analytics, organic traffic, technical SEO",
      canonical: "https://customermindiq.com/website-intelligence"
    },
    'product-intelligence': {
      title: "Product Intelligence Center - Feature Adoption & User Analytics | CustomerMind IQ",
      description: "Optimize product development with feature adoption tracking, user journey analysis, and product-market fit scoring. Increase retention by 30%+.",
      keywords: "product analytics, feature adoption, user journey analysis, product-market fit, user retention, product intelligence, user behavior analytics",
      canonical: "https://customermindiq.com/product-intelligence"
    },
    'ai-business-insights': {
      title: "AI Business Insights - 47 AI Models for Business Optimization | CustomerMind IQ",
      description: "Leverage 47 active AI models for predictive analytics, process automation, and intelligent decision-making. Save $67,800+ daily in operational costs.",
      keywords: "AI business insights, predictive analytics, business automation, machine learning, AI models, intelligent business decisions, process optimization",
      canonical: "https://customermindiq.com/ai-business-insights"
    },
    'integrations': {
      title: "50+ Business Integrations - CRM, Analytics & Marketing Tools | CustomerMind IQ",
      description: "Connect with 50+ popular tools including Salesforce, HubSpot, Google Analytics, Mailchimp. Real-time data sync and automated workflows.",
      keywords: "business integrations, CRM integration, analytics integration, marketing tool integration, data connectors, API integration, workflow automation",
      canonical: "https://customermindiq.com/integrations"
    },
    'compliance': {
      title: "Enterprise Compliance & Security - GDPR, HIPAA, SOX | CustomerMind IQ",
      description: "Enterprise-grade security with GDPR, HIPAA, SOX compliance. AES-256 encryption, audit management, and 60% reduction in compliance overhead.",
      keywords: "enterprise security, GDPR compliance, HIPAA compliance, SOX compliance, data security, audit management, regulatory compliance, data privacy",
      canonical: "https://customermindiq.com/compliance"
    },
    'training': {
      title: "Customer Intelligence Training & Certification | CustomerMind IQ",
      description: "Master customer intelligence with comprehensive training materials, certification programs, and expert guidance. Maximize your platform ROI.",
      keywords: "customer intelligence training, analytics certification, business intelligence training, platform training, user education, ROI optimization",
      canonical: "https://customermindiq.com/training"
    },
    'support': {
      title: "24/7 Customer Support - Multi-Tier Support System | CustomerMind IQ",
      description: "Get expert help with our multi-tier support system. Email, live chat, and phone support based on your plan. Professional services available.",
      keywords: "customer support, technical support, live chat support, phone support, customer success, platform help, expert assistance",
      canonical: "https://customermindiq.com/support"
    }
  };

  const config = metaConfigs[page];
  if (!config) return null;

  return (
    <Helmet>
      <title>{config.title}</title>
      <meta name="description" content={config.description} />
      <meta name="keywords" content={config.keywords} />
      <link rel="canonical" href={config.canonical} />
      
      {/* Open Graph */}
      <meta property="og:title" content={config.title} />
      <meta property="og:description" content={config.description} />
      <meta property="og:url" content={config.canonical} />
      
      {/* Twitter */}
      <meta name="twitter:title" content={config.title} />
      <meta name="twitter:description" content={config.description} />
    </Helmet>
  );
};

// SEO-optimized breadcrumb component
export const SEOBreadcrumbs = ({ breadcrumbs }) => {
  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": breadcrumbs.map((crumb, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "name": crumb.name,
      "item": crumb.url
    }))
  };

  return (
    <>
      <script type="application/ld+json">
        {JSON.stringify(breadcrumbSchema)}
      </script>
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <ol className="flex space-x-2 text-sm text-gray-600">
          {breadcrumbs.map((crumb, index) => (
            <li key={index} className="flex items-center">
              {index > 0 && <span className="mx-2">/</span>}
              {index === breadcrumbs.length - 1 ? (
                <span className="text-gray-900 font-medium">{crumb.name}</span>
              ) : (
                <a href={crumb.url} className="hover:text-blue-600">{crumb.name}</a>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
};

export default PageMetaTags;