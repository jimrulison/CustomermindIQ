import React from 'react';
import SEOHead from './SEOHead';
import StructuredDataScript from './StructuredDataScript';

// SEO component specifically for blog posts
const BlogSEO = ({ post }) => {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": post.title,
    "description": post.excerpt,
    "image": post.featuredImage || "https://customermindiq.com/images/blog-default.jpg",
    "author": {
      "@type": "Person",
      "name": post.author?.name || "CustomerMind IQ Team",
      "url": post.author?.url || "https://customermindiq.com/about"
    },
    "publisher": {
      "@type": "Organization",
      "name": "CustomerMind IQ",
      "logo": {
        "@type": "ImageObject",
        "url": "https://customermindiq.com/images/logo.png"
      }
    },
    "datePublished": post.publishedAt,
    "dateModified": post.updatedAt || post.publishedAt,
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": `https://customermindiq.com/blog/${post.slug}`
    },
    "wordCount": post.wordCount,
    "keywords": post.tags?.join(', '),
    "articleSection": post.category,
    "inLanguage": "en-US"
  };

  // Generate reading time estimate
  const readingTime = Math.ceil((post.wordCount || 1000) / 200);

  return (
    <>
      <SEOHead
        title={`${post.title} | CustomerMind IQ Blog`}
        description={post.excerpt}
        keywords={`${post.tags?.join(', ')}, customer intelligence, business analytics, customer success`}
        canonicalUrl={`https://customermindiq.com/blog/${post.slug}`}
        imageUrl={post.featuredImage}
        pageType="article"
      />
      
      <StructuredDataScript data={structuredData} />
      
      {/* Article-specific meta tags */}
      <meta property="article:published_time" content={post.publishedAt} />
      <meta property="article:modified_time" content={post.updatedAt || post.publishedAt} />
      <meta property="article:author" content={post.author?.name || "CustomerMind IQ Team"} />
      <meta property="article:section" content={post.category} />
      {post.tags?.map(tag => (
        <meta key={tag} property="article:tag" content={tag} />
      ))}
      
      {/* Reading time */}
      <meta name="twitter:label1" content="Reading time" />
      <meta name="twitter:data1" content={`${readingTime} min read`} />
    </>
  );
};

// Component for blog category pages
export const BlogCategorySEO = ({ category, posts }) => {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": `${category.name} - CustomerMind IQ Blog`,
    "description": category.description,
    "url": `https://customermindiq.com/blog/category/${category.slug}`,
    "mainEntity": {
      "@type": "ItemList",
      "itemListElement": posts?.slice(0, 10).map((post, index) => ({
        "@type": "BlogPosting",
        "position": index + 1,
        "headline": post.title,
        "url": `https://customermindiq.com/blog/${post.slug}`,
        "datePublished": post.publishedAt
      })) || []
    }
  };

  return (
    <>
      <SEOHead
        title={`${category.name} Articles | CustomerMind IQ Blog`}
        description={`Explore ${category.name.toLowerCase()} articles on customer intelligence, analytics, and business growth. Expert insights and best practices.`}
        keywords={`${category.name}, customer intelligence blog, ${category.keywords || ''}`}
        canonicalUrl={`https://customermindiq.com/blog/category/${category.slug}`}
      />
      
      <StructuredDataScript data={structuredData} />
    </>
  );
};

// Component for blog tag pages
export const BlogTagSEO = ({ tag, posts }) => {
  const structuredData = {
    "@context": "https://schema.org", 
    "@type": "CollectionPage",
    "name": `${tag} Articles - CustomerMind IQ Blog`,
    "description": `Articles tagged with ${tag}`,
    "url": `https://customermindiq.com/blog/tag/${tag}`,
    "mainEntity": {
      "@type": "ItemList",
      "itemListElement": posts?.slice(0, 10).map((post, index) => ({
        "@type": "BlogPosting",
        "position": index + 1,
        "headline": post.title,
        "url": `https://customermindiq.com/blog/${post.slug}`,
        "datePublished": post.publishedAt
      })) || []
    }
  };

  return (
    <>
      <SEOHead
        title={`${tag} | CustomerMind IQ Blog`}
        description={`Read articles about ${tag} and customer intelligence insights from CustomerMind IQ experts.`}
        keywords={`${tag}, customer intelligence, business analytics, customer success`}
        canonicalUrl={`https://customermindiq.com/blog/tag/${tag}`}
      />
      
      <StructuredDataScript data={structuredData} />
    </>
  );
};

export default BlogSEO;