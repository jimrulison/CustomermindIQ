import React from 'react';

const BreadcrumbSchema = ({ currentPage }) => {
  // Generate breadcrumb schema based on current page
  const getBreadcrumbSchema = () => {
    const baseUrl = "https://customermindiq.com";
    
    const breadcrumbMappings = {
      'customer-analytics-dashboard': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Customer Analytics", url: `${baseUrl}/#customer-analytics` }
        ]
      },
      'website-analytics-dashboard': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Website Analytics", url: `${baseUrl}/#website-analytics` }
        ]
      },
      'productivity': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Productivity Intelligence", url: `${baseUrl}/#productivity` }
        ]
      },
      'training': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Training & Documentation", url: `${baseUrl}/#training` }
        ]
      },
      'support': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Support Center", url: `${baseUrl}/#support` }
        ]
      },
      'knowledge-base': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Knowledge Base", url: `${baseUrl}/#knowledge-base` }
        ]
      },
      'subscription': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Subscription & Pricing", url: `${baseUrl}/#subscription` }
        ]
      },
      'affiliate-portal': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Affiliate Program", url: `${baseUrl}/affiliates` }
        ]
      },
      'website-intelligence': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Website Analytics", url: `${baseUrl}/#website-analytics` },
          { name: "Website Intelligence Hub", url: `${baseUrl}/#website-intelligence` }
        ]
      },
      'customers': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Customer Analytics", url: `${baseUrl}/#customer-analytics` },
          { name: "Customer Intelligence", url: `${baseUrl}/#customers` }
        ]
      },
      'marketing': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Customer Analytics", url: `${baseUrl}/#customer-analytics` },
          { name: "Marketing Automation", url: `${baseUrl}/#marketing` }
        ]
      },
      'revenue': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Customer Analytics", url: `${baseUrl}/#customer-analytics` },
          { name: "Revenue Analytics", url: `${baseUrl}/#revenue` }
        ]
      },
      'growth-acceleration': {
        items: [
          { name: "Home", url: baseUrl },
          { name: "Customer Analytics", url: `${baseUrl}/#customer-analytics` },
          { name: "Growth Acceleration Engine", url: `${baseUrl}/#growth-acceleration` }
        ]
      }
    };

    const breadcrumb = breadcrumbMappings[currentPage];
    if (!breadcrumb) {
      // Default breadcrumb for unknown pages
      return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": baseUrl
          }
        ]
      };
    }

    return {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": breadcrumb.items.map((item, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "name": item.name,
        "item": item.url
      }))
    };
  };

  const breadcrumbSchema = getBreadcrumbSchema();

  return (
    <script 
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
    />
  );
};

export default BreadcrumbSchema;