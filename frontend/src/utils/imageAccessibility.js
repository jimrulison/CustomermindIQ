/**
 * Image Accessibility Utilities
 * Provides consistent alt text and accessibility improvements for images
 */

// Alt text templates for common image types
export const altTextTemplates = {
  // Logo images
  logo: (brandName = "CustomerMind IQ") => `${brandName} company logo`,
  logoIcon: (brandName = "CustomerMind IQ") => `${brandName} brand icon`,
  
  // Decorative images
  decorative: "", // Empty alt for purely decorative images
  
  // Functional images
  avatar: (name) => `Profile picture of ${name}`,
  thumbnail: (title) => `Thumbnail image for ${title}`,
  screenshot: (description) => `Screenshot showing ${description}`,
  
  // Charts and graphs
  chart: (type, description) => `${type} chart showing ${description}`,
  graph: (description) => `Graph displaying ${description}`,
  
  // UI elements
  icon: (action, description) => `${action} icon - ${description}`,
  button: (action) => `${action} button`,
  
  // Product/feature images
  feature: (featureName, description) => `${featureName} feature: ${description}`,
  product: (productName, description) => `${productName} product image: ${description}`,
  
  // Training/educational content
  video: (title) => `Video thumbnail: ${title}`,
  tutorial: (title) => `Tutorial preview: ${title}`,
  
  // Dashboard/analytics
  dashboard: (dashboardType) => `${dashboardType} dashboard interface`,
  analytics: (metricType) => `${metricType} analytics visualization`,
  
  // Certificate/badge images
  certificate: (certType) => `${certType} certification badge`,
  badge: (achievement) => `Achievement badge: ${achievement}`
};

// Function to generate contextual alt text
export const generateAltText = (imageType, context = {}) => {
  const template = altTextTemplates[imageType];
  
  if (typeof template === 'function') {
    return template(context.name || context.description || context.title);
  }
  
  return template || `Image related to ${context.description || 'content'}`;
};

// Accessibility validation function
export const validateImageAccessibility = (imageElement) => {
  const issues = [];
  
  if (!imageElement.alt && imageElement.alt !== "") {
    issues.push("Missing alt attribute");
  }
  
  if (imageElement.alt && imageElement.alt.length > 125) {
    issues.push("Alt text too long (should be under 125 characters)");
  }
  
  if (imageElement.alt && imageElement.alt.toLowerCase().includes('image of')) {
    issues.push("Alt text contains redundant 'image of' phrase");
  }
  
  return issues;
};

// Common alt text improvements
export const improvedAltText = {
  // Main brand logo
  mainLogo: "CustomerMind IQ - AI-powered customer intelligence platform logo",
  
  // Dashboard screenshots
  websiteAnalytics: "Website analytics dashboard showing traffic, conversions, and user behavior metrics",
  customerAnalytics: "Customer analytics interface displaying segmentation, journey mapping, and retention data",
  productIntelligence: "Product intelligence hub with user engagement, feature adoption, and product-market fit metrics",
  
  // Feature illustrations
  aiInsights: "AI-powered business insights visualization with predictive analytics and recommendations",
  realTimeHealth: "Real-time business health monitoring dashboard with key performance indicators",
  competitiveIntel: "Competitive intelligence analysis showing market positioning and competitor insights",
  
  // Training and support images
  trainingVideo: "CustomerMind IQ training video thumbnail with play button overlay",
  supportChat: "Live chat support interface for customer assistance",
  knowledgeBase: "Knowledge base article preview with search functionality",
  
  // Affiliate and partnership images
  affiliatePortal: "Affiliate partner portal interface showing commission tracking and marketing materials",
  partnerBadge: "Certified CustomerMind IQ partner badge indicating authorized reseller status"
};

export default {
  altTextTemplates,
  generateAltText,
  validateImageAccessibility,
  improvedAltText
};