#!/bin/bash

# Sitemap Ping Script for Customer Mind IQ
# This script notifies search engines about sitemap updates

SITEMAP_URL="https://customermindiq.com/sitemap.xml"

echo "🌐 Pinging Search Engines about Sitemap Update..."
echo "Sitemap URL: $SITEMAP_URL"
echo "Date: $(date)"
echo ""

# Ping Google
echo "📍 Pinging Google..."
GOOGLE_RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null "https://www.google.com/ping?sitemap=$SITEMAP_URL")
if [ "$GOOGLE_RESPONSE" = "200" ]; then
    echo "✅ Google: Successfully pinged"
else
    echo "❌ Google: Ping failed (HTTP $GOOGLE_RESPONSE)"
fi

# Ping Bing
echo "📍 Pinging Bing..."
BING_RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null "https://www.bing.com/ping?sitemap=$SITEMAP_URL")
if [ "$BING_RESPONSE" = "200" ]; then
    echo "✅ Bing: Successfully pinged"
else
    echo "❌ Bing: Ping failed (HTTP $BING_RESPONSE)"
fi

echo ""
echo "🔍 Verifying sitemap accessibility..."
SITEMAP_RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null "$SITEMAP_URL")
if [ "$SITEMAP_RESPONSE" = "200" ]; then
    echo "✅ Sitemap is accessible at $SITEMAP_URL"
else
    echo "❌ Sitemap not accessible (HTTP $SITEMAP_RESPONSE)"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Check Google Search Console for indexing status"
echo "2. Monitor Bing Webmaster Tools for crawl results"
echo "3. Verify new pages appear in search results within 1-2 weeks"
echo ""
echo "🔗 Manual Submission URLs:"
echo "Google: https://search.google.com/search-console/sitemaps"
echo "Bing: https://www.bing.com/webmasters/sitemaps"