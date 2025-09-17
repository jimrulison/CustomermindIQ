// SEO helper functions and configurations

// Generate page-specific canonical URLs
export const generateCanonicalUrl = (path = '') => {
  const baseUrl = process.env.REACT_APP_SITE_URL || 'https://customermindiq.com';
  return `${baseUrl}${path}`;
};

// Generate optimized meta descriptions based on features
export const generateMetaDescription = (features, benefits, cta = '') => {
  const featureText = features.join(', ');
  const benefitText = benefits.join(', ');
  const description = `${featureText}. ${benefitText}. ${cta}`;
  
  // Ensure description is within optimal length (150-160 characters)
  return description.length > 160 ? description.substring(0, 157) + '...' : description;
};

// Generate structured data for different content types
export const generateArticleSchema = (article) => ({
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": article.title,
  "description": article.description,
  "image": article.image,
  "author": {
    "@type": "Organization",
    "name": "CustomerMind IQ"
  },
  "publisher": {
    "@type": "Organization", 
    "name": "CustomerMind IQ",
    "logo": {
      "@type": "ImageObject",
      "url": "https://customermindiq.com/images/logo.png"
    }
  },
  "datePublished": article.publishDate,
  "dateModified": article.modifiedDate,
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": article.url
  }
});

export const generateVideoSchema = (video) => ({
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": video.title,
  "description": video.description,
  "thumbnailUrl": video.thumbnail,
  "uploadDate": video.uploadDate,
  "duration": video.duration,
  "contentUrl": video.url,
  "embedUrl": video.embedUrl,
  "publisher": {
    "@type": "Organization",
    "name": "CustomerMind IQ"
  }
});

export const generateHowToSchema = (howTo) => ({
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": howTo.title,
  "description": howTo.description,
  "image": howTo.image,
  "totalTime": howTo.totalTime,
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": howTo.cost
  },
  "supply": howTo.supplies?.map(supply => ({
    "@type": "HowToSupply",
    "name": supply
  })),
  "tool": howTo.tools?.map(tool => ({
    "@type": "HowToTool",
    "name": tool
  })),
  "step": howTo.steps?.map((step, index) => ({
    "@type": "HowToStep",
    "position": index + 1,
    "name": step.title,
    "text": step.description,
    "image": step.image
  }))
});

// SEO-optimized keywords for different business verticals
export const verticalKeywords = {
  saas: [
    'customer intelligence software',
    'SaaS analytics platform',
    'customer success software',
    'churn prediction SaaS',
    'subscription analytics',
    'customer behavior tracking',
    'SaaS business intelligence'
  ],
  ecommerce: [
    'ecommerce customer analytics',
    'online store intelligence',
    'customer segmentation ecommerce',
    'ecommerce churn prevention',
    'customer lifetime value ecommerce',
    'conversion optimization',
    'ecommerce business intelligence'
  ],
  agency: [
    'agency customer intelligence',
    'client analytics platform',
    'marketing agency tools',
    'client retention software',
    'agency business intelligence',
    'white label analytics',
    'client success platform'
  ],
  enterprise: [
    'enterprise customer intelligence',
    'large business analytics',
    'enterprise churn prediction',
    'corporate customer insights',
    'enterprise data platform',
    'business intelligence enterprise',
    'customer analytics enterprise'
  ]
};

// Long-tail keyword variations
export const longTailKeywords = [
  'how to reduce customer churn with AI',
  'best customer intelligence platform 2025',
  'AI powered customer behavior analysis',
  'customer lifetime value prediction software',
  'automated customer segmentation tools',
  'real time customer analytics dashboard',
  'predictive customer analytics platform',
  'customer success intelligence software',
  'behavioral customer clustering AI',
  'customer journey analytics tools'
];

// Local SEO keywords (if applicable)
export const localSEOKeywords = [
  'customer intelligence software USA',
  'American customer analytics platform',
  'US business intelligence software',
  'customer insights platform United States',
  'North American customer success tools'
];

// Competitor comparison keywords
export const competitorKeywords = [
  'better than HubSpot analytics',
  'Salesforce alternative customer intelligence',
  'Google Analytics customer insights alternative',
  'Mixpanel competitor customer analytics',
  'Segment alternative customer data platform'
];

// Feature-specific keyword clusters
export const featureKeywordClusters = {
  churnPrediction: [
    'customer churn prediction software',
    'AI churn prediction',
    'churn prevention tools',
    'customer retention software',
    'churn analysis platform'
  ],
  revenueForecasting: [
    'revenue forecasting software',
    'AI revenue prediction',
    'sales forecasting tools',
    'revenue analytics platform',
    'financial forecasting software'
  ],
  marketingAutomation: [
    'marketing automation platform',
    'AI marketing automation',
    'email marketing automation',
    'lead scoring software',
    'campaign automation tools'
  ],
  customerSegmentation: [
    'customer segmentation software',
    'behavioral segmentation tools',
    'AI customer clustering',
    'customer persona software',
    'audience segmentation platform'
  ]
};

// Generate semantic keywords for content optimization
export const generateSemanticKeywords = (primaryKeyword) => {
  const semanticMap = {
    'customer intelligence': [
      'customer insights', 'customer analytics', 'customer data analysis',
      'customer behavior understanding', 'customer knowledge platform',
      'customer information system', 'customer data intelligence'
    ],
    'churn prediction': [
      'customer attrition forecasting', 'retention modeling', 'customer loss prevention',
      'defection prediction', 'customer departure analysis', 'turnover forecasting'
    ],
    'revenue forecasting': [
      'sales prediction', 'income projection', 'financial forecasting',
      'earnings estimation', 'revenue modeling', 'profit prediction'
    ],
    'marketing automation': [
      'campaign automation', 'marketing workflow', 'automated marketing',
      'marketing process automation', 'digital marketing automation'
    ]
  };
  
  return semanticMap[primaryKeyword] || [];
};

// Title tag optimization helpers
export const optimizeTitle = (title, keywords) => {
  // Ensure title is 50-60 characters for optimal display
  const maxLength = 60;
  const primaryKeyword = keywords[0];
  
  // Include primary keyword near the beginning
  if (!title.toLowerCase().includes(primaryKeyword.toLowerCase())) {
    title = `${primaryKeyword} - ${title}`;
  }
  
  // Add brand name if space allows
  if (title.length + ' | CustomerMind IQ'.length <= maxLength) {
    title += ' | CustomerMind IQ';
  }
  
  return title.length > maxLength ? title.substring(0, maxLength - 3) + '...' : title;
};

// Meta description optimization
export const optimizeMetaDescription = (description, keywords) => {
  const maxLength = 160;
  const primaryKeyword = keywords[0];
  
  // Ensure primary keyword is included
  if (!description.toLowerCase().includes(primaryKeyword.toLowerCase())) {
    description = `${primaryKeyword}: ${description}`;
  }
  
  // Add call-to-action if space allows
  const cta = ' Try free for 7 days.';
  if (description.length + cta.length <= maxLength) {
    description += cta;
  }
  
  return description.length > maxLength ? description.substring(0, maxLength - 3) + '...' : description;
};

// Generate robots meta tag based on page type
export const generateRobotsTag = (pageType, isPublic = true) => {
  const configs = {
    'home': 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1',
    'product': 'index, follow, max-snippet:-1, max-image-preview:large',
    'blog': 'index, follow, max-snippet:160, max-image-preview:large',
    'login': 'noindex, nofollow',
    'admin': 'noindex, nofollow',
    'thank-you': 'noindex, follow',
    'privacy': 'index, nofollow',
    'terms': 'index, nofollow'
  };
  
  return isPublic ? (configs[pageType] || 'index, follow') : 'noindex, nofollow';
};

export default {
  generateCanonicalUrl,
  generateMetaDescription,
  verticalKeywords,
  longTailKeywords,
  featureKeywordClusters,
  generateSemanticKeywords,
  optimizeTitle,
  optimizeMetaDescription,
  generateRobotsTag
};