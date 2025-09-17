import React from 'react';
import { Helmet } from 'react-helmet-async';

const SEOHead = ({ 
  title,
  description,
  keywords,
  canonicalUrl,
  imageUrl,
  pageType = 'website',
  structuredData
}) => {
  const siteUrl = process.env.REACT_APP_SITE_URL || 'https://customermindiq.com';
  const fullImageUrl = imageUrl ? `${siteUrl}${imageUrl}` : `${siteUrl}/images/customermind-iq-og-image.jpg`;
  
  return (
    <Helmet>
      {/* Primary Meta Tags */}
      <title>{title}</title>
      <meta name="title" content={title} />
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta name="robots" content="index, follow" />
      <meta name="language" content="English" />
      <meta name="revisit-after" content="1 days" />
      <meta name="author" content="CustomerMind IQ" />
      
      {/* Canonical URL */}
      <link rel="canonical" href={canonicalUrl || siteUrl} />
      
      {/* Open Graph / Facebook */}
      <meta property="og:type" content={pageType} />
      <meta property="og:url" content={canonicalUrl || siteUrl} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={fullImageUrl} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:site_name" content="CustomerMind IQ" />
      <meta property="og:locale" content="en_US" />
      
      {/* Twitter */}
      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={canonicalUrl || siteUrl} />
      <meta property="twitter:title" content={title} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content={fullImageUrl} />
      <meta property="twitter:creator" content="@CustomerMindIQ" />
      <meta property="twitter:site" content="@CustomerMindIQ" />
      
      {/* LinkedIn */}
      <meta property="article:author" content="CustomerMind IQ" />
      <meta property="article:publisher" content="CustomerMind IQ" />
      
      {/* Additional SEO Meta Tags */}
      <meta name="theme-color" content="#1e40af" />
      <meta name="msapplication-TileColor" content="#1e40af" />
      <meta name="application-name" content="CustomerMind IQ" />
      
      {/* Geographic Targeting */}
      <meta name="geo.region" content="US" />
      <meta name="geo.placename" content="United States" />
      <meta name="ICBM" content="39.8283, -98.5795" />
      
      {/* Structured Data */}
      {structuredData && (
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      )}
    </Helmet>
  );
};

export default SEOHead;