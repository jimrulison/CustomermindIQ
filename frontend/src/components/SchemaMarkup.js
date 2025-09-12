import React from 'react';

const SchemaMarkup = () => {
  // Organization Schema
  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://customermindiq.com/#organization",
    "name": "Customer Mind IQ",
    "alternateName": "CustomerMind IQ",
    "url": "https://customermindiq.com",
    "logo": {
      "@type": "ImageObject",
      "url": "https://customer-assets.emergentagent.com/job_mindiq-auth/artifacts/bi9l7mag_Customer%20Mind%20IQ%20logo.png",
      "width": 200,
      "height": 200
    },
    "description": "AI-powered customer intelligence platform helping businesses understand and optimize their customer relationships through advanced analytics, marketing automation, and predictive insights.",
    "foundingDate": "2024",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "San Francisco",
      "addressRegion": "CA",
      "addressCountry": "US"
    },
    "contactPoint": [
      {
        "@type": "ContactPoint",
        "telephone": "+1-800-MIND-IQ",
        "contactType": "customer service",
        "availableLanguage": ["English", "Spanish", "French", "German", "Italian"],
        "areaServed": "Worldwide"
      },
      {
        "@type": "ContactPoint",
        "email": "support@customermindiq.com",
        "contactType": "customer support",
        "availableLanguage": ["English", "Spanish", "French", "German", "Italian"],
        "areaServed": "Worldwide"
      },
      {
        "@type": "ContactPoint",
        "email": "sales@customermindiq.com",
        "contactType": "sales",
        "availableLanguage": ["English", "Spanish", "French", "German", "Italian"],
        "areaServed": "Worldwide"
      }
    ],
    "sameAs": [
      "https://www.linkedin.com/company/customermindiq",
      "https://twitter.com/customermindiq"
    ]
  };

  // Software Application Schema
  const softwareSchema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "@id": "https://customermindiq.com/#software",
    "name": "Customer Mind IQ Platform",
    "applicationCategory": "BusinessApplication",
    "applicationSubCategory": "Customer Analytics Software",
    "operatingSystem": "Web Browser",
    "description": "Comprehensive AI-powered customer intelligence platform with 14+ specialized analytics modules, marketing automation, revenue optimization, and growth acceleration tools.",
    "url": "https://customermindiq.com",
    "downloadUrl": "https://customermindiq.com/signup",
    "softwareVersion": "2.0",
    "releaseNotes": "Enhanced AI capabilities, improved user interface, and advanced automation features",
    "datePublished": "2024-01-01",
    "dateModified": "2024-12-01",
    "publisher": {
      "@id": "https://customermindiq.com/#organization"
    },
    "offers": [
      {
        "@type": "Offer",
        "@id": "https://customermindiq.com/#free-plan",
        "name": "Free Tier",
        "description": "Basic customer intelligence with up to 1,000 customer profiles",
        "price": "0",
        "priceCurrency": "USD",
        "priceValidUntil": "2025-12-31",
        "availability": "https://schema.org/InStock",
        "validFrom": "2024-01-01",
        "category": "Free Plan",
        "includedServices": [
          "Basic customer intelligence",
          "Up to 1,000 customer profiles",
          "5 AI insights per month",
          "Email support",
          "Basic dashboard"
        ]
      },
      {
        "@type": "Offer",
        "@id": "https://customermindiq.com/#professional-plan",
        "name": "Professional Plan",
        "description": "Full customer intelligence suite with unlimited AI insights",
        "price": "99",
        "priceCurrency": "USD",
        "billingPeriod": "Monthly",
        "priceValidUntil": "2025-12-31",
        "availability": "https://schema.org/InStock",
        "validFrom": "2024-01-01",
        "category": "Professional Plan",
        "includedServices": [
          "Full customer intelligence suite",
          "Up to 50,000 customer profiles",
          "Unlimited AI insights",
          "Marketing automation",
          "Revenue analytics",
          "Website intelligence",
          "Priority support"
        ]
      },
      {
        "@type": "Offer",
        "@id": "https://customermindiq.com/#enterprise-plan",
        "name": "Enterprise Plan", 
        "description": "Complete solution with unlimited profiles and white-label options",
        "price": "299",
        "priceCurrency": "USD",
        "billingPeriod": "Monthly",
        "priceValidUntil": "2025-12-31",
        "availability": "https://schema.org/InStock",
        "validFrom": "2024-01-01",
        "category": "Enterprise Plan",
        "includedServices": [
          "Everything in Professional",
          "Unlimited customer profiles",
          "White-label options",
          "Custom integrations",
          "Dedicated account manager",
          "Phone support",
          "SLA guarantees"
        ]
      }
    ],
    "featureList": [
      "AI-Powered Customer Intelligence",
      "Real-Time Health Monitoring",
      "Marketing Automation",
      "Revenue Analytics",
      "Website Intelligence Hub",
      "Growth Acceleration Engine",
      "Productivity Intelligence",
      "Customer Success Management",
      "Executive Dashboard",
      "Advanced Features Suite",
      "Knowledge Base",
      "Training & Support",
      "Affiliate Program",
      "API Integration"
    ],
    "screenshot": [
      "https://customermindiq.com/screenshots/dashboard.png",
      "https://customermindiq.com/screenshots/analytics.png",
      "https://customermindiq.com/screenshots/automation.png"
    ],
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "bestRating": "5",
      "worstRating": "1",
      "ratingCount": "247",
      "reviewCount": "156"
    }
  };

  // Product Schema
  const productSchema = {
    "@context": "https://schema.org",
    "@type": "Product",
    "@id": "https://customermindiq.com/#product",
    "name": "Customer Mind IQ",
    "brand": {
      "@id": "https://customermindiq.com/#organization"
    },
    "manufacturer": {
      "@id": "https://customermindiq.com/#organization"
    },
    "description": "Advanced AI-powered customer intelligence and marketing automation platform designed to help businesses understand, engage, and optimize their customer relationships for maximum growth and retention.",
    "category": "Software > Business Software > Customer Analytics",
    "audience": {
      "@type": "BusinessAudience",
      "audienceType": "Small to Enterprise Businesses"
    },
    "serviceType": "SaaS Platform",
    "provider": {
      "@id": "https://customermindiq.com/#organization"
    },
    "offers": {
      "@id": "https://customermindiq.com/#professional-plan"
    },
    "aggregateRating": {
      "@id": "https://customermindiq.com/#aggregate-rating"
    },
    "review": [
      {
        "@type": "Review",
        "@id": "https://customermindiq.com/#review-1",
        "author": {
          "@type": "Person",
          "name": "Sarah Johnson"
        },
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5",
          "bestRating": "5"
        },
        "reviewBody": "Customer Mind IQ has transformed how we understand our customers. The AI insights are incredibly accurate and have helped us increase our conversion rate by 40%.",
        "datePublished": "2024-10-15"
      },
      {
        "@type": "Review",
        "@id": "https://customermindiq.com/#review-2", 
        "author": {
          "@type": "Person",
          "name": "Michael Chen"
        },
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "5",
          "bestRating": "5"
        },
        "reviewBody": "The marketing automation features are outstanding. We've seen a 60% improvement in email engagement and our revenue has grown significantly.",
        "datePublished": "2024-11-02"
      },
      {
        "@type": "Review",
        "@id": "https://customermindiq.com/#review-3",
        "author": {
          "@type": "Person", 
          "name": "Emma Rodriguez"
        },
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": "4",
          "bestRating": "5"
        },
        "reviewBody": "Great platform with comprehensive analytics. The interface is intuitive and the support team is very responsive. Highly recommend for growing businesses.",
        "datePublished": "2024-11-18"
      }
    ]
  };

  // FAQ Schema
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "@id": "https://customermindiq.com/#faq",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What is Customer Mind IQ?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Customer Mind IQ is an AI-powered customer intelligence platform that helps businesses understand and optimize their customer relationships through advanced analytics, marketing automation, and predictive insights."
        }
      },
      {
        "@type": "Question",
        "name": "How does the AI analysis work?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Our AI analyzes customer behavior patterns, purchase history, engagement metrics, and other data points to provide actionable insights, predict future behavior, and recommend optimization strategies."
        }
      },
      {
        "@type": "Question",
        "name": "What integrations are available?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Customer Mind IQ integrates with popular CRM systems, email marketing platforms, e-commerce solutions, payment processors, and other business tools through our comprehensive API and pre-built connectors."
        }
      },
      {
        "@type": "Question",
        "name": "Is there a free trial available?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes, we offer a free 7-day trial with no credit card required. You can also use our Free Tier which includes basic customer intelligence features for up to 1,000 customer profiles."
        }
      },
      {
        "@type": "Question",
        "name": "What kind of support do you provide?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "We provide comprehensive support including email support for all plans, priority support for Professional plans, phone support for Enterprise plans, extensive documentation, training materials, and a knowledge base."
        }
      }
    ]
  };

  // Website Schema
  const websiteSchema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://customermindiq.com/#website",
    "url": "https://customermindiq.com",
    "name": "Customer Mind IQ",
    "publisher": {
      "@id": "https://customermindiq.com/#organization"
    },
    "potentialAction": {
      "@type": "SearchAction",
      "target": {
        "@type": "EntryPoint",
        "urlTemplate": "https://customermindiq.com/search?q={search_term_string}"
      },
      "query-input": "required name=search_term_string"
    }
  };

  // Service Schema
  const serviceSchema = {
    "@context": "https://schema.org",
    "@type": "Service",
    "@id": "https://customermindiq.com/#service",
    "name": "Customer Intelligence Analytics Service",
    "provider": {
      "@id": "https://customermindiq.com/#organization"
    },
    "serviceType": "Business Analytics and Intelligence",
    "description": "Comprehensive customer intelligence and analytics service powered by AI to help businesses optimize customer relationships, increase revenue, and improve marketing effectiveness.",
    "areaServed": "Worldwide",
    "availableChannel": {
      "@type": "ServiceChannel",
      "serviceUrl": "https://customermindiq.com",
      "servicePhone": "+1-800-MIND-IQ",
      "serviceSmsNumber": "+1-800-MIND-IQ"
    },
    "category": "Customer Analytics",
    "audience": {
      "@type": "BusinessAudience",
      "audienceType": "SMB to Enterprise"
    },
    "offers": [
      { "@id": "https://customermindiq.com/#free-plan" },
      { "@id": "https://customermindiq.com/#professional-plan" },
      { "@id": "https://customermindiq.com/#enterprise-plan" }
    ]
  };

  return (
    <>
      {/* Organization Schema */}
      <script 
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />
      
      {/* Software Application Schema */}
      <script 
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(softwareSchema) }}
      />
      
      {/* Product Schema */}
      <script 
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(productSchema) }}
      />
      
      {/* FAQ Schema */}
      <script 
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      
      {/* Website Schema */}
      <script 
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteSchema) }}
      />
      
      {/* Service Schema */}
      <script 
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(serviceSchema) }}
      />
    </>
  );
};

export default SchemaMarkup;