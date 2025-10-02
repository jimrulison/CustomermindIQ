#!/usr/bin/env python3
"""
CustomerMind IQ - Comprehensive Link Testing Suite

This script performs comprehensive link testing for the CustomerMind IQ application as requested:

1. Internal API Endpoint Testing - all API routes, authentication, admin portal, dashboard modules, file downloads
2. Static File Accessibility - training docs, affiliate pages, sitemap, robots.txt, manifest, favicon  
3. Route Validation - React router paths, hash navigation, protected routes, 404 handling
4. External Link Testing - API integrations, CDN links, external resources
5. SEO URL Structure - canonical URLs, sitemap validation, structured data, robots.txt
6. Link Consistency - broken links, navigation consistency, breadcrumbs, header/footer links

BACKEND URL: https://subscription-tiers-4.preview.emergentagent.com
ADMIN CREDENTIALS: admin@customermindiq.com / CustomerMindIQ2025!
"""

import asyncio
import json
import os
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import urllib3
import re
from urllib.parse import urljoin, urlparse

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - Use production URL from frontend .env
BACKEND_URL = "https://subscription-tiers-4.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class ComprehensiveLinkTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.session.timeout = 30
        self.jwt_token = None
        self.test_results = {
            "api_endpoints": [],
            "static_files": [],
            "route_validation": [],
            "external_links": [],
            "seo_structure": [],
            "link_consistency": [],
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            }
        }
        
    def log_result(self, category: str, test_name: str, status: str, url: str, details: str = "", response_time: float = 0):
        """Log test result"""
        result = {
            "test_name": test_name,
            "status": status,  # "✅ PASS", "❌ FAIL", "⚠️ WARN"
            "url": url,
            "details": details,
            "response_time": f"{response_time:.3f}s" if response_time > 0 else "N/A",
            "timestamp": datetime.now().isoformat()
        }
        
        self.test_results[category].append(result)
        self.test_results["summary"]["total_tests"] += 1
        
        if status.startswith("✅"):
            self.test_results["summary"]["passed"] += 1
        elif status.startswith("❌"):
            self.test_results["summary"]["failed"] += 1
        elif status.startswith("⚠️"):
            self.test_results["summary"]["warnings"] += 1
            
        print(f"{status} {test_name}: {url}")
        if details:
            print(f"   Details: {details}")
            
    async def authenticate_admin(self) -> bool:
        """Authenticate as admin and get JWT token"""
        try:
            print("\n🔐 ADMIN AUTHENTICATION")
            print("=" * 50)
            
            login_url = f"{API_BASE}/auth/login"
            login_data = {
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }
            
            start_time = datetime.now()
            response = self.session.post(login_url, json=login_data)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.jwt_token = data["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.jwt_token}"})
                    self.log_result("api_endpoints", "Admin Authentication", "✅ PASS", login_url, 
                                  f"Successfully authenticated admin user", response_time)
                    return True
                else:
                    self.log_result("api_endpoints", "Admin Authentication", "❌ FAIL", login_url,
                                  f"No access_token in response: {data}", response_time)
                    return False
            else:
                self.log_result("api_endpoints", "Admin Authentication", "❌ FAIL", login_url,
                              f"HTTP {response.status_code}: {response.text}", response_time)
                return False
                
        except Exception as e:
            self.log_result("api_endpoints", "Admin Authentication", "❌ FAIL", login_url,
                          f"Exception: {str(e)}", 0)
            return False

    async def test_api_endpoints(self):
        """Test all internal API endpoints"""
        print("\n🔗 INTERNAL API ENDPOINT TESTING")
        print("=" * 50)
        
        # Core API endpoints to test
        api_endpoints = [
            # Health and basic endpoints
            ("Health Check", "GET", "/health", False),
            ("Database Test", "GET", "/test-db", False),
            
            # Authentication endpoints
            ("Auth Login", "POST", "/auth/login", False),
            ("Auth Register", "POST", "/auth/register", False),
            
            # Admin portal endpoints
            ("Admin Analytics Dashboard", "GET", "/admin/analytics/dashboard", True),
            ("Admin Email Templates", "GET", "/admin/email-templates", True),
            ("Admin Automated Workflows", "GET", "/admin/workflows", True),
            ("Admin Banners", "GET", "/admin/banners", True),
            ("Admin Discounts", "GET", "/admin/discounts", True),
            ("Admin API Keys", "GET", "/admin/api-keys", True),
            ("Admin Users", "GET", "/admin/users", True),
            ("Admin API Documentation", "GET", "/admin/api-documentation", True),
            
            # Dashboard module endpoints
            ("Customer Health Dashboard", "GET", "/customer-health/dashboard", True),
            ("Customer Success Health Dashboard", "GET", "/customer-success/health-dashboard", True),
            ("Growth Intelligence ABM Dashboard", "GET", "/growth-intelligence/abm-dashboard", True),
            ("Customer Journey Dashboard", "GET", "/customer-journey/dashboard", True),
            ("Product Intelligence Feature Usage", "GET", "/product-intelligence/feature-usage-dashboard", True),
            ("Product Intelligence Onboarding", "GET", "/product-intelligence/onboarding-dashboard", True),
            ("Product Intelligence PMF", "GET", "/product-intelligence/pmf-dashboard", True),
            ("Product Intelligence Journey", "GET", "/product-intelligence/journey-dashboard", True),
            ("Website Intelligence Dashboard", "GET", "/website-intelligence/dashboard", True),
            ("Website Intelligence Performance", "GET", "/website-intelligence/performance-dashboard", True),
            ("Website Intelligence SEO", "GET", "/website-intelligence/seo-dashboard", True),
            ("Website Intelligence Membership", "GET", "/website-intelligence/membership-status", True),
            ("Integration Hub Connectors", "GET", "/integration-hub/connectors-dashboard", True),
            ("Integration Hub Sync", "GET", "/integration-hub/sync-dashboard", True),
            ("Integration Hub Quality", "GET", "/integration-hub/quality-dashboard", True),
            ("Integration Hub Analytics", "GET", "/integration-hub/analytics-dashboard", True),
            
            # Subscription and payment endpoints
            ("Subscription Plans", "GET", "/subscriptions/plans", False),
            ("Trial Registration", "POST", "/subscriptions/trial/register", False),
            
            # Affiliate system endpoints
            ("Affiliate Resources", "GET", "/affiliate/resources", False),
            ("Affiliate Dashboard", "GET", "/affiliate/dashboard", False),
            ("Affiliate Generate Link", "POST", "/affiliate/generate-link", False),
            
            # Support system endpoints
            ("Support Tickets", "GET", "/support/tickets", True),
            ("Support Admin Tickets", "GET", "/admin/support/tickets", True),
            
            # Live chat endpoints
            ("Chat Access Check", "GET", "/chat/access-check", True),
            ("Chat Sessions", "GET", "/chat/sessions", True),
            
            # Customer and analytics endpoints
            ("Customers", "GET", "/customers", True),
            ("Analytics", "GET", "/analytics", True),
            ("Campaigns", "GET", "/campaigns", True),
        ]
        
        # File download endpoints
        download_endpoints = [
            ("Quick Start Guide Download", "GET", "/download/quick-start-guide", False),
            ("Complete Training Manual Download", "GET", "/download/complete-training-manual", False),
            ("Admin Training Manual Download", "GET", "/download/admin-training-manual", False),
            ("Training Portal Download", "GET", "/download/training-portal", False),
            ("Quick Reference Guide Download", "GET", "/download/quick-reference-guide", False),
        ]
        
        # Test all API endpoints
        for name, method, endpoint, requires_auth in api_endpoints + download_endpoints:
            await self.test_single_api_endpoint(name, method, endpoint, requires_auth)
            
    async def test_single_api_endpoint(self, name: str, method: str, endpoint: str, requires_auth: bool):
        """Test a single API endpoint"""
        try:
            url = f"{API_BASE}{endpoint}"
            
            # Skip auth-required endpoints if we don't have token
            if requires_auth and not self.jwt_token:
                self.log_result("api_endpoints", name, "⚠️ WARN", url, "Skipped - no auth token")
                return
                
            start_time = datetime.now()
            
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                # Use sample data for POST requests
                if "login" in endpoint:
                    data = {"email": "test@example.com", "password": "testpass"}
                elif "register" in endpoint:
                    data = {"email": "test@example.com", "password": "testpass", "first_name": "Test", "last_name": "User"}
                elif "trial" in endpoint:
                    data = {"email": "trial@example.com", "first_name": "Trial", "last_name": "User", "company_name": "Test Company"}
                elif "generate-link" in endpoint:
                    data = {"campaign": "test", "landing_page": "home"}
                else:
                    data = {}
                response = self.session.post(url, json=data)
            else:
                response = self.session.request(method, url)
                
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Evaluate response
            if response.status_code == 200:
                try:
                    data = response.json()
                    data_size = len(json.dumps(data))
                    self.log_result("api_endpoints", name, "✅ PASS", url, 
                                  f"HTTP 200, {data_size} chars response", response_time)
                except:
                    # HTML or other content
                    content_size = len(response.content)
                    self.log_result("api_endpoints", name, "✅ PASS", url,
                                  f"HTTP 200, {content_size} bytes content", response_time)
            elif response.status_code == 401 and requires_auth:
                self.log_result("api_endpoints", name, "⚠️ WARN", url,
                              f"HTTP 401 - Authentication required (expected)", response_time)
            elif response.status_code == 404:
                self.log_result("api_endpoints", name, "❌ FAIL", url,
                              f"HTTP 404 - Endpoint not found", response_time)
            elif response.status_code >= 500:
                self.log_result("api_endpoints", name, "❌ FAIL", url,
                              f"HTTP {response.status_code} - Server error", response_time)
            else:
                self.log_result("api_endpoints", name, "⚠️ WARN", url,
                              f"HTTP {response.status_code}", response_time)
                
        except Exception as e:
            self.log_result("api_endpoints", name, "❌ FAIL", url, f"Exception: {str(e)}", 0)

    async def test_static_files(self):
        """Test static file accessibility"""
        print("\n📁 STATIC FILE ACCESSIBILITY TESTING")
        print("=" * 50)
        
        # Static files to test
        static_files = [
            # Training documentation files
            ("Admin Training Manual Direct", "/download-admin-manual-direct"),
            ("Admin Training Manual Static", "/admin-training-manual.html"),
            ("Training Test Page", "/training-test"),
            ("Training Portal", "/training"),
            ("Training Portal Alt", "/training/portal"),
            
            # Affiliate system pages
            ("Affiliate Resources Page", "/affiliate-resources.html"),
            ("Affiliate Banners Page", "/affiliate-banners.html"),
            ("Affiliate Materials Page", "/affiliate-materials.html"),
            
            # SEO and meta files
            ("Sitemap XML", "/sitemap.xml"),
            ("Robots TXT", "/robots.txt"),
            ("Manifest JSON", "/manifest.json"),
            ("Favicon ICO", "/favicon.ico"),
            ("Favicon PNG", "/favicon.png"),
            
            # Public directory files
            ("Index HTML", "/index.html"),
            ("Logo Files", "/logo192.png"),
            ("Logo Files Large", "/logo512.png"),
        ]
        
        for name, path in static_files:
            await self.test_static_file(name, path)
            
    async def test_static_file(self, name: str, path: str):
        """Test a single static file"""
        try:
            url = f"{BACKEND_URL}{path}"
            
            start_time = datetime.now()
            response = self.session.get(url)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'unknown')
                content_size = len(response.content)
                self.log_result("static_files", name, "✅ PASS", url,
                              f"HTTP 200, {content_size} bytes, {content_type}", response_time)
            elif response.status_code == 404:
                self.log_result("static_files", name, "❌ FAIL", url,
                              f"HTTP 404 - File not found", response_time)
            else:
                self.log_result("static_files", name, "⚠️ WARN", url,
                              f"HTTP {response.status_code}", response_time)
                
        except Exception as e:
            self.log_result("static_files", name, "❌ FAIL", url, f"Exception: {str(e)}", 0)

    async def test_route_validation(self):
        """Test React router paths and navigation"""
        print("\n🛣️ ROUTE VALIDATION TESTING")
        print("=" * 50)
        
        # React routes to test (these should return the main React app)
        react_routes = [
            ("Home Route", "/"),
            ("Dashboard Route", "/#dashboard"),
            ("Admin Route", "/#admin"),
            ("Analytics Route", "/#analytics"),
            ("Customers Route", "/#customers"),
            ("Campaigns Route", "/#campaigns"),
            ("Settings Route", "/#settings"),
            ("Profile Route", "/#profile"),
            ("Subscription Route", "/#subscription"),
            ("Support Route", "/#support"),
            ("Training Route", "/#training"),
            ("Affiliate Route", "/#affiliate"),
            
            # Hash-based navigation
            ("Dashboard Hash", "#dashboard"),
            ("Admin Hash", "#admin"),
            ("Analytics Hash", "#analytics"),
            
            # Invalid routes (should handle gracefully)
            ("Invalid Route 1", "/nonexistent-page"),
            ("Invalid Route 2", "/invalid/deep/route"),
            ("Invalid Hash", "/#invalid-section"),
        ]
        
        for name, route in react_routes:
            await self.test_route(name, route)
            
    async def test_route(self, name: str, route: str):
        """Test a single route"""
        try:
            # For hash routes, test the base URL since hash is client-side
            if route.startswith("#"):
                url = f"{BACKEND_URL}/{route}"
            else:
                url = f"{BACKEND_URL}{route}"
                
            start_time = datetime.now()
            response = self.session.get(url)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                # Check if it's the React app (should contain React-related content)
                content = response.text.lower()
                if 'react' in content or 'app' in content or 'root' in content:
                    self.log_result("route_validation", name, "✅ PASS", url,
                                  f"HTTP 200, React app loaded", response_time)
                else:
                    self.log_result("route_validation", name, "⚠️ WARN", url,
                                  f"HTTP 200, but may not be React app", response_time)
            elif response.status_code == 404:
                if "invalid" in name.lower() or "nonexistent" in name.lower():
                    self.log_result("route_validation", name, "✅ PASS", url,
                                  f"HTTP 404 - Correctly handled invalid route", response_time)
                else:
                    self.log_result("route_validation", name, "❌ FAIL", url,
                                  f"HTTP 404 - Route not found", response_time)
            else:
                self.log_result("route_validation", name, "⚠️ WARN", url,
                              f"HTTP {response.status_code}", response_time)
                
        except Exception as e:
            self.log_result("route_validation", name, "❌ FAIL", url, f"Exception: {str(e)}", 0)

    async def test_external_links(self):
        """Test external API integrations and CDN links"""
        print("\n🌐 EXTERNAL LINK TESTING")
        print("=" * 50)
        
        # External resources to test
        external_links = [
            # CDN and external assets
            ("Customer Assets CDN", "https://customer-assets.emergentagent.com/"),
            ("Emergent Agent Main", "https://emergentagent.com/"),
            
            # API integrations (test connectivity, not actual API calls)
            ("MongoDB Atlas Connectivity", "https://cluster0.iw5g77.mongodb.net/"),
            
            # Social media and documentation (if any)
            ("GitHub Repository", "https://github.com/"),
            ("Documentation Site", "https://docs.emergentagent.com/"),
        ]
        
        for name, url in external_links:
            await self.test_external_link(name, url)
            
    async def test_external_link(self, name: str, url: str):
        """Test a single external link"""
        try:
            start_time = datetime.now()
            response = self.session.get(url, timeout=10)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                self.log_result("external_links", name, "✅ PASS", url,
                              f"HTTP 200, external resource accessible", response_time)
            elif response.status_code in [301, 302, 307, 308]:
                self.log_result("external_links", name, "⚠️ WARN", url,
                              f"HTTP {response.status_code} - Redirect", response_time)
            else:
                self.log_result("external_links", name, "❌ FAIL", url,
                              f"HTTP {response.status_code}", response_time)
                
        except requests.exceptions.Timeout:
            self.log_result("external_links", name, "⚠️ WARN", url, "Timeout - may be slow", 10.0)
        except Exception as e:
            self.log_result("external_links", name, "❌ FAIL", url, f"Exception: {str(e)}", 0)

    async def test_seo_structure(self):
        """Test SEO URL structure and meta files"""
        print("\n🔍 SEO URL STRUCTURE TESTING")
        print("=" * 50)
        
        # Test sitemap.xml
        await self.test_sitemap_xml()
        
        # Test robots.txt
        await self.test_robots_txt()
        
        # Test canonical URLs and meta tags
        await self.test_canonical_urls()
        
    async def test_sitemap_xml(self):
        """Test sitemap.xml validity and content"""
        try:
            url = f"{BACKEND_URL}/sitemap.xml"
            response = self.session.get(url)
            
            if response.status_code == 200:
                try:
                    # Parse XML
                    root = ET.fromstring(response.content)
                    
                    # Count URLs in sitemap
                    urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
                    url_count = len(urls)
                    
                    if url_count > 0:
                        self.log_result("seo_structure", "Sitemap XML Validation", "✅ PASS", url,
                                      f"Valid XML with {url_count} URLs")
                        
                        # Test a few URLs from sitemap
                        for i, url_elem in enumerate(urls[:5]):  # Test first 5 URLs
                            loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                            if loc_elem is not None:
                                sitemap_url = loc_elem.text
                                await self.test_sitemap_url(f"Sitemap URL {i+1}", sitemap_url)
                    else:
                        self.log_result("seo_structure", "Sitemap XML Validation", "⚠️ WARN", url,
                                      "Valid XML but no URLs found")
                        
                except ET.ParseError as e:
                    self.log_result("seo_structure", "Sitemap XML Validation", "❌ FAIL", url,
                                  f"Invalid XML: {str(e)}")
            else:
                self.log_result("seo_structure", "Sitemap XML Validation", "❌ FAIL", url,
                              f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("seo_structure", "Sitemap XML Validation", "❌ FAIL", url,
                          f"Exception: {str(e)}")
            
    async def test_sitemap_url(self, name: str, url: str):
        """Test a URL from sitemap"""
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                self.log_result("seo_structure", name, "✅ PASS", url, "Sitemap URL accessible")
            else:
                self.log_result("seo_structure", name, "❌ FAIL", url,
                              f"HTTP {response.status_code} - Sitemap URL broken")
        except Exception as e:
            self.log_result("seo_structure", name, "❌ FAIL", url, f"Sitemap URL error: {str(e)}")

    async def test_robots_txt(self):
        """Test robots.txt validity and directives"""
        try:
            url = f"{BACKEND_URL}/robots.txt"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for basic robots.txt directives
                has_user_agent = "User-agent:" in content
                has_sitemap = "Sitemap:" in content
                has_directives = "Allow:" in content or "Disallow:" in content
                
                details = []
                if has_user_agent:
                    details.append("User-agent directive found")
                if has_sitemap:
                    details.append("Sitemap reference found")
                if has_directives:
                    details.append("Allow/Disallow directives found")
                    
                if has_user_agent and (has_sitemap or has_directives):
                    self.log_result("seo_structure", "Robots TXT Validation", "✅ PASS", url,
                                  f"Valid robots.txt: {', '.join(details)}")
                else:
                    self.log_result("seo_structure", "Robots TXT Validation", "⚠️ WARN", url,
                                  f"Basic robots.txt: {', '.join(details) if details else 'minimal content'}")
            else:
                self.log_result("seo_structure", "Robots TXT Validation", "❌ FAIL", url,
                              f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("seo_structure", "Robots TXT Validation", "❌ FAIL", url,
                          f"Exception: {str(e)}")

    async def test_canonical_urls(self):
        """Test canonical URLs and meta tags on main pages"""
        try:
            url = f"{BACKEND_URL}/"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for canonical URL
                has_canonical = 'rel="canonical"' in content
                
                # Check for basic meta tags
                has_title = '<title>' in content
                has_description = 'name="description"' in content
                has_og_tags = 'property="og:' in content
                has_twitter_tags = 'name="twitter:' in content
                
                details = []
                if has_canonical:
                    details.append("canonical URL")
                if has_title:
                    details.append("title tag")
                if has_description:
                    details.append("meta description")
                if has_og_tags:
                    details.append("Open Graph tags")
                if has_twitter_tags:
                    details.append("Twitter Card tags")
                    
                if len(details) >= 3:
                    self.log_result("seo_structure", "Canonical URLs & Meta Tags", "✅ PASS", url,
                                  f"Good SEO structure: {', '.join(details)}")
                elif len(details) >= 1:
                    self.log_result("seo_structure", "Canonical URLs & Meta Tags", "⚠️ WARN", url,
                                  f"Basic SEO structure: {', '.join(details)}")
                else:
                    self.log_result("seo_structure", "Canonical URLs & Meta Tags", "❌ FAIL", url,
                                  "No SEO meta tags found")
            else:
                self.log_result("seo_structure", "Canonical URLs & Meta Tags", "❌ FAIL", url,
                              f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("seo_structure", "Canonical URLs & Meta Tags", "❌ FAIL", url,
                          f"Exception: {str(e)}")

    async def test_link_consistency(self):
        """Test link consistency across components"""
        print("\n🔗 LINK CONSISTENCY TESTING")
        print("=" * 50)
        
        # Test main navigation links
        await self.test_navigation_consistency()
        
        # Test footer links
        await self.test_footer_links()
        
        # Test breadcrumb navigation
        await self.test_breadcrumb_links()
        
    async def test_navigation_consistency(self):
        """Test main navigation links"""
        try:
            url = f"{BACKEND_URL}/"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text
                
                # Look for common navigation patterns
                nav_patterns = [
                    r'href=["\']#dashboard["\']',
                    r'href=["\']#admin["\']',
                    r'href=["\']#analytics["\']',
                    r'href=["\']#customers["\']',
                    r'href=["\']#campaigns["\']',
                    r'href=["\']#settings["\']',
                ]
                
                found_nav_links = []
                for pattern in nav_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        found_nav_links.append(pattern.split('#')[1].split('[')[0])
                        
                if len(found_nav_links) >= 3:
                    self.log_result("link_consistency", "Navigation Consistency", "✅ PASS", url,
                                  f"Found {len(found_nav_links)} navigation links: {', '.join(found_nav_links)}")
                elif len(found_nav_links) >= 1:
                    self.log_result("link_consistency", "Navigation Consistency", "⚠️ WARN", url,
                                  f"Limited navigation links: {', '.join(found_nav_links)}")
                else:
                    self.log_result("link_consistency", "Navigation Consistency", "❌ FAIL", url,
                                  "No navigation links found")
            else:
                self.log_result("link_consistency", "Navigation Consistency", "❌ FAIL", url,
                              f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("link_consistency", "Navigation Consistency", "❌ FAIL", url,
                          f"Exception: {str(e)}")

    async def test_footer_links(self):
        """Test footer links"""
        try:
            url = f"{BACKEND_URL}/"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Look for footer-related content
                has_footer = '<footer' in content or 'class="footer"' in content
                has_privacy = 'privacy' in content
                has_terms = 'terms' in content or 'tos' in content
                has_contact = 'contact' in content
                has_support = 'support' in content
                
                footer_elements = []
                if has_footer:
                    footer_elements.append("footer element")
                if has_privacy:
                    footer_elements.append("privacy link")
                if has_terms:
                    footer_elements.append("terms link")
                if has_contact:
                    footer_elements.append("contact link")
                if has_support:
                    footer_elements.append("support link")
                    
                if len(footer_elements) >= 3:
                    self.log_result("link_consistency", "Footer Links", "✅ PASS", url,
                                  f"Good footer structure: {', '.join(footer_elements)}")
                elif len(footer_elements) >= 1:
                    self.log_result("link_consistency", "Footer Links", "⚠️ WARN", url,
                                  f"Basic footer: {', '.join(footer_elements)}")
                else:
                    self.log_result("link_consistency", "Footer Links", "❌ FAIL", url,
                                  "No footer elements found")
            else:
                self.log_result("link_consistency", "Footer Links", "❌ FAIL", url,
                              f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("link_consistency", "Footer Links", "❌ FAIL", url,
                          f"Exception: {str(e)}")

    async def test_breadcrumb_links(self):
        """Test breadcrumb navigation"""
        try:
            # Test a deep route that might have breadcrumbs
            url = f"{BACKEND_URL}/#admin"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Look for breadcrumb patterns
                has_breadcrumb = 'breadcrumb' in content or 'nav-breadcrumb' in content
                has_nav_trail = '>' in content and ('home' in content or 'dashboard' in content)
                
                if has_breadcrumb:
                    self.log_result("link_consistency", "Breadcrumb Links", "✅ PASS", url,
                                  "Breadcrumb navigation found")
                elif has_nav_trail:
                    self.log_result("link_consistency", "Breadcrumb Links", "⚠️ WARN", url,
                                  "Navigation trail found (may be breadcrumbs)")
                else:
                    self.log_result("link_consistency", "Breadcrumb Links", "⚠️ WARN", url,
                                  "No breadcrumb navigation detected")
            else:
                self.log_result("link_consistency", "Breadcrumb Links", "❌ FAIL", url,
                              f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("link_consistency", "Breadcrumb Links", "❌ FAIL", url,
                          f"Exception: {str(e)}")

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE LINK TESTING REPORT")
        print("=" * 80)
        
        # Summary
        summary = self.test_results["summary"]
        total = summary["total_tests"]
        passed = summary["passed"]
        failed = summary["failed"]
        warnings = summary["warnings"]
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n📊 OVERALL SUMMARY:")
        print(f"   Total Tests: {total}")
        print(f"   ✅ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"   ❌ Failed: {failed} ({failed/total*100:.1f}%)")
        print(f"   ⚠️ Warnings: {warnings} ({warnings/total*100:.1f}%)")
        print(f"   🎯 Success Rate: {success_rate:.1f}%")
        
        # Detailed results by category
        categories = [
            ("🔗 API ENDPOINTS", "api_endpoints"),
            ("📁 STATIC FILES", "static_files"),
            ("🛣️ ROUTE VALIDATION", "route_validation"),
            ("🌐 EXTERNAL LINKS", "external_links"),
            ("🔍 SEO STRUCTURE", "seo_structure"),
            ("🔗 LINK CONSISTENCY", "link_consistency")
        ]
        
        for category_name, category_key in categories:
            results = self.test_results[category_key]
            if results:
                print(f"\n{category_name}:")
                
                # Count by status
                category_passed = len([r for r in results if r["status"].startswith("✅")])
                category_failed = len([r for r in results if r["status"].startswith("❌")])
                category_warnings = len([r for r in results if r["status"].startswith("⚠️")])
                category_total = len(results)
                
                print(f"   Summary: {category_passed}✅ {category_failed}❌ {category_warnings}⚠️ ({category_total} total)")
                
                # Show failed tests first
                failed_tests = [r for r in results if r["status"].startswith("❌")]
                if failed_tests:
                    print(f"   ❌ FAILED TESTS:")
                    for result in failed_tests:
                        print(f"      • {result['test_name']}: {result['url']}")
                        if result['details']:
                            print(f"        Details: {result['details']}")
                
                # Show warnings
                warning_tests = [r for r in results if r["status"].startswith("⚠️")]
                if warning_tests:
                    print(f"   ⚠️ WARNINGS:")
                    for result in warning_tests[:3]:  # Show first 3 warnings
                        print(f"      • {result['test_name']}: {result['details']}")
                    if len(warning_tests) > 3:
                        print(f"      ... and {len(warning_tests) - 3} more warnings")
                
                # Show some successful tests
                passed_tests = [r for r in results if r["status"].startswith("✅")]
                if passed_tests:
                    print(f"   ✅ WORKING ({len(passed_tests)} tests passed)")
                    for result in passed_tests[:2]:  # Show first 2 successful tests
                        print(f"      • {result['test_name']}: {result['response_time']}")
                    if len(passed_tests) > 2:
                        print(f"      ... and {len(passed_tests) - 2} more successful tests")
        
        # Recommendations
        print(f"\n🔧 RECOMMENDATIONS:")
        
        if failed > 0:
            print(f"   • Fix {failed} failed tests - these are critical issues")
            
        if warnings > 0:
            print(f"   • Review {warnings} warnings - these may need attention")
            
        if success_rate >= 90:
            print(f"   • Excellent link health! {success_rate:.1f}% success rate")
        elif success_rate >= 75:
            print(f"   • Good link health with room for improvement")
        else:
            print(f"   • Link health needs attention - {success_rate:.1f}% success rate")
            
        # Critical issues
        critical_failures = []
        for category_key in ["api_endpoints", "static_files"]:
            failed_in_category = [r for r in self.test_results[category_key] if r["status"].startswith("❌")]
            critical_failures.extend(failed_in_category)
            
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES REQUIRING IMMEDIATE ATTENTION:")
            for failure in critical_failures[:5]:  # Show top 5 critical issues
                print(f"   • {failure['test_name']}: {failure['details']}")
                
        print(f"\n" + "=" * 80)
        print(f"Report generated at: {datetime.now().isoformat()}")
        print(f"Backend URL tested: {BACKEND_URL}")
        print("=" * 80)

async def main():
    """Main test execution"""
    print("🚀 CustomerMind IQ - Comprehensive Link Testing Suite")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Start Time: {datetime.now().isoformat()}")
    print("=" * 80)
    
    tester = ComprehensiveLinkTester()
    
    try:
        # Step 1: Authenticate as admin
        auth_success = await tester.authenticate_admin()
        
        # Step 2: Test all categories
        await tester.test_api_endpoints()
        await tester.test_static_files()
        await tester.test_route_validation()
        await tester.test_external_links()
        await tester.test_seo_structure()
        await tester.test_link_consistency()
        
        # Step 3: Generate comprehensive report
        tester.generate_report()
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical testing error: {e}")
    finally:
        print(f"\n🏁 Testing completed at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    asyncio.run(main())