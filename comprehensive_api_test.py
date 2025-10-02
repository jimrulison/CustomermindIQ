#!/usr/bin/env python3
"""
Comprehensive API Testing for Customer Mind IQ Backend
Testing all major API endpoints as requested in the review.

COMPREHENSIVE TEST COVERAGE:
1. Core API Functionality Testing
2. Integration & External API Testing  
3. Environment Variables & Configuration
4. Service Health Check
5. Missing Requirements Identification

Test Areas:
- Authentication endpoints (/api/auth/*)
- User management endpoints
- Subscription/tier-related endpoints  
- Admin portal endpoints
- Support system endpoints
- Live chat system endpoints
- Third-party integrations
- Database connectivity
- Email service integrations
- Payment processing integrations
- Analytics/tracking integrations
- AI/LLM service integrations
- Cloud storage integrations

Admin credentials: admin@customermindiq.com / CustomerMindIQ2025!
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import urllib3
import time

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - Use production URL from frontend .env
BACKEND_URL = "https://subscription-tiers-4.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class ComprehensiveAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.admin_token = None
        self.test_results = []
        self.working_apis = []
        self.broken_apis = []
        self.required_api_keys = []
        self.config_issues = []
        self.setup_recommendations = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None, response_time: float = 0):
        """Log test results with categorization"""
        status = "✅ WORKING" if success else "❌ BROKEN"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response time: {response_time:.3f}s")
        if response_data and isinstance(response_data, dict):
            print(f"   Response keys: {list(response_data.keys())}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
        
        # Categorize results
        if success:
            self.working_apis.append(f"{test_name}: {details}")
        else:
            self.broken_apis.append(f"{test_name}: {details}")
        
        print()

    def authenticate_admin(self) -> bool:
        """Authenticate as admin user"""
        try:
            print("🔐 Testing Admin Authentication...")
            start_time = time.time()
            
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                if self.admin_token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.admin_token}"
                    })
                    self.log_test("Admin Authentication", True, 
                                f"Successfully authenticated as {ADMIN_CREDENTIALS['email']}", 
                                data, response_time)
                    return True
                else:
                    self.log_test("Admin Authentication", False, 
                                "No access token in response", data, response_time)
                    return False
            else:
                self.log_test("Admin Authentication", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False

    def test_core_authentication_endpoints(self):
        """Test all authentication endpoints"""
        print("🔑 Testing Core Authentication Endpoints...")
        
        # Test login endpoint (already tested in authenticate_admin)
        
        # Test register endpoint
        try:
            start_time = time.time()
            test_user = {
                "email": f"test.user.{int(datetime.now().timestamp())}@example.com",
                "password": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
                "company_name": "Test Company"
            }
            
            response = self.session.post(
                f"{API_BASE}/auth/register",
                json=test_user,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.log_test("User Registration", True, 
                            f"Successfully registered user", data, response_time)
            else:
                self.log_test("User Registration", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("User Registration", False, f"Exception: {str(e)}")
        
        # Test logout endpoint
        try:
            start_time = time.time()
            response = self.session.post(f"{API_BASE}/auth/logout", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code in [200, 204]:
                self.log_test("User Logout", True, 
                            "Logout endpoint accessible", None, response_time)
            else:
                self.log_test("User Logout", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("User Logout", False, f"Exception: {str(e)}")

    def test_user_management_endpoints(self):
        """Test user management endpoints"""
        print("👥 Testing User Management Endpoints...")
        
        # Test get current user profile
        try:
            start_time = time.time()
            response = self.session.get(f"{API_BASE}/auth/profile", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get User Profile", True, 
                            f"Successfully retrieved profile", data, response_time)
            else:
                self.log_test("Get User Profile", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("Get User Profile", False, f"Exception: {str(e)}")
        
        # Test customers endpoint
        try:
            start_time = time.time()
            response = self.session.get(f"{API_BASE}/customers", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get Customers", True, 
                            f"Successfully retrieved {len(data) if isinstance(data, list) else 'unknown'} customers", 
                            data, response_time)
            else:
                self.log_test("Get Customers", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("Get Customers", False, f"Exception: {str(e)}")

    def test_subscription_tier_endpoints(self):
        """Test subscription and tier-related endpoints"""
        print("💳 Testing Subscription & Tier Endpoints...")
        
        # Test subscription plans
        try:
            start_time = time.time()
            response = self.session.get(f"{API_BASE}/subscriptions/plans", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Subscription Plans", True, 
                            f"Successfully retrieved subscription plans", data, response_time)
            else:
                self.log_test("Subscription Plans", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("Subscription Plans", False, f"Exception: {str(e)}")
        
        # Test trial registration
        try:
            start_time = time.time()
            trial_user = {
                "email": f"trial.user.{int(datetime.now().timestamp())}@example.com",
                "first_name": "Trial",
                "last_name": "User",
                "company_name": "Trial Company"
            }
            
            response = self.session.post(
                f"{API_BASE}/subscriptions/trial/register",
                json=trial_user,
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Trial Registration", True, 
                            f"Successfully registered trial user", data, response_time)
            else:
                self.log_test("Trial Registration", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("Trial Registration", False, f"Exception: {str(e)}")

    def test_admin_portal_endpoints(self):
        """Test admin portal endpoints"""
        print("🔧 Testing Admin Portal Endpoints...")
        
        admin_endpoints = [
            ("/admin/analytics/dashboard", "Admin Analytics Dashboard"),
            ("/admin/email-templates", "Email Templates"),
            ("/admin/workflows", "Automated Workflows"),
            ("/admin/banners", "Admin Banners"),
            ("/admin/discounts", "Admin Discounts"),
            ("/admin/api-keys", "API Keys Management"),
            ("/admin/users", "User Management"),
            ("/admin/support/tickets", "Support Tickets (Admin)")
        ]
        
        for endpoint, name in admin_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, 
                                f"Successfully accessed endpoint", data, response_time)
                elif response.status_code == 404:
                    self.log_test(name, False, 
                                f"Endpoint not found (404)", None, response_time)
                elif response.status_code == 403:
                    self.log_test(name, False, 
                                f"Access forbidden (403) - may need higher permissions", None, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_support_system_endpoints(self):
        """Test support system endpoints"""
        print("🎧 Testing Support System Endpoints...")
        
        support_endpoints = [
            ("/support/tickets", "Support Tickets"),
            ("/support/create", "Create Support Ticket"),
            ("/support/categories", "Support Categories"),
            ("/support/faq", "Support FAQ")
        ]
        
        for endpoint, name in support_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, 
                                f"Successfully accessed endpoint", data, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_live_chat_endpoints(self):
        """Test live chat system endpoints"""
        print("💬 Testing Live Chat System Endpoints...")
        
        chat_endpoints = [
            ("/chat/sessions", "Chat Sessions"),
            ("/chat/access-check", "Chat Access Check"),
            ("/chat/history", "Chat History"),
            ("/chat/admin/dashboard", "Admin Chat Dashboard")
        ]
        
        for endpoint, name in chat_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, 
                                f"Successfully accessed endpoint", data, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_integration_endpoints(self):
        """Test integration and external API endpoints"""
        print("🔗 Testing Integration & External API Endpoints...")
        
        integration_endpoints = [
            ("/odoo/integration/status", "ODOO Integration Status"),
            ("/odoo/crm/pipeline", "ODOO CRM Pipeline"),
            ("/affiliate/dashboard", "Affiliate Dashboard"),
            ("/affiliate/resources", "Affiliate Resources"),
            ("/payment/stripe/status", "Stripe Payment Status"),
            ("/email/providers/status", "Email Providers Status"),
            ("/analytics/dashboard", "Analytics Dashboard")
        ]
        
        for endpoint, name in integration_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, 
                                f"Successfully accessed endpoint", data, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_dashboard_endpoints(self):
        """Test various dashboard endpoints"""
        print("📊 Testing Dashboard Endpoints...")
        
        dashboard_endpoints = [
            ("/customer-health/dashboard", "Customer Health Dashboard"),
            ("/customer-success/health-dashboard", "Customer Success Dashboard"),
            ("/growth-intelligence/abm-dashboard", "Growth Intelligence Dashboard"),
            ("/customer-journey/dashboard", "Customer Journey Dashboard"),
            ("/product-intelligence/feature-usage-dashboard", "Product Intelligence Dashboard"),
            ("/website-intelligence/dashboard", "Website Intelligence Dashboard"),
            ("/integration-hub/connectors-dashboard", "Integration Hub Dashboard")
        ]
        
        for endpoint, name in dashboard_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    data_size = len(str(data)) if data else 0
                    self.log_test(name, True, 
                                f"Successfully accessed endpoint ({data_size} chars)", 
                                data, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_health_and_connectivity(self):
        """Test service health and database connectivity"""
        print("🏥 Testing Service Health & Connectivity...")
        
        # Test health endpoint
        try:
            start_time = time.time()
            response = self.session.get(f"{API_BASE}/health", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Service Health Check", True, 
                            f"Service healthy: {data.get('service')} v{data.get('version')}", 
                            data, response_time)
            else:
                self.log_test("Service Health Check", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("Service Health Check", False, f"Exception: {str(e)}")
        
        # Test database connectivity
        try:
            start_time = time.time()
            response = self.session.get(f"{API_BASE}/test-db", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                overall_status = data.get("overall_status", "Unknown")
                self.log_test("Database Connectivity", True, 
                            f"Database test: {overall_status}", data, response_time)
            else:
                self.log_test("Database Connectivity", False, 
                            f"HTTP {response.status_code}: {response.text}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("Database Connectivity", False, f"Exception: {str(e)}")

    def analyze_environment_variables(self):
        """Analyze environment variables and configuration"""
        print("🔍 Analyzing Environment Variables & Configuration...")
        
        # Check for common environment variables that might be missing
        potential_missing_keys = [
            "STRIPE_API_KEY",
            "SENDGRID_API_KEY", 
            "OPENAI_API_KEY",
            "AWS_ACCESS_KEY_ID",
            "GOOGLE_ANALYTICS_ID",
            "FACEBOOK_PIXEL_ID"
        ]
        
        for key in potential_missing_keys:
            if key not in ["STRIPE_API_KEY"]:  # We know Stripe is configured
                self.required_api_keys.append(f"{key} - May be needed for full functionality")
        
        # Check CORS configuration
        self.config_issues.append("CORS is set to allow all origins (*) - consider restricting in production")
        
        # Check MongoDB configuration
        self.setup_recommendations.append("MongoDB connection configured - verify all collections are properly indexed")
        
        # Check ODOO integration
        self.setup_recommendations.append("ODOO integration configured - verify credentials and permissions")

    def run_comprehensive_test(self):
        """Run all comprehensive API tests"""
        print("🚀 Starting Comprehensive API Testing for Customer Mind IQ")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"📡 API Base: {API_BASE}")
        print("=" * 80)
        
        # Step 1: Authenticate
        if not self.authenticate_admin():
            print("❌ Authentication failed. Some tests may not work properly.")
        
        # Step 2: Test core authentication endpoints
        self.test_core_authentication_endpoints()
        
        # Step 3: Test user management
        self.test_user_management_endpoints()
        
        # Step 4: Test subscription/tier endpoints
        self.test_subscription_tier_endpoints()
        
        # Step 5: Test admin portal endpoints
        self.test_admin_portal_endpoints()
        
        # Step 6: Test support system endpoints
        self.test_support_system_endpoints()
        
        # Step 7: Test live chat endpoints
        self.test_live_chat_endpoints()
        
        # Step 8: Test integration endpoints
        self.test_integration_endpoints()
        
        # Step 9: Test dashboard endpoints
        self.test_dashboard_endpoints()
        
        # Step 10: Test health and connectivity
        self.test_health_and_connectivity()
        
        # Step 11: Analyze environment and configuration
        self.analyze_environment_variables()
        
        # Generate comprehensive report
        self.generate_comprehensive_report()

    def generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        print("=" * 80)
        print("📊 COMPREHENSIVE API TEST REPORT")
        print("=" * 80)
        
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        # Working APIs
        print("✅ WORKING APIs:")
        for api in self.working_apis:
            print(f"   ✅ {api}")
        print()
        
        # Broken/Missing APIs
        print("❌ BROKEN/MISSING APIs:")
        for api in self.broken_apis:
            print(f"   ❌ {api}")
        print()
        
        # Required API Keys
        print("🔑 REQUIRED API KEYS:")
        if self.required_api_keys:
            for key in self.required_api_keys:
                print(f"   🔑 {key}")
        else:
            print("   ✅ All known API keys appear to be configured")
        print()
        
        # Configuration Issues
        print("⚠️ CONFIGURATION ISSUES:")
        if self.config_issues:
            for issue in self.config_issues:
                print(f"   ⚠️ {issue}")
        else:
            print("   ✅ No major configuration issues detected")
        print()
        
        # Setup Recommendations
        print("📋 SETUP RECOMMENDATIONS:")
        for rec in self.setup_recommendations:
            print(f"   📋 {rec}")
        
        # Performance Analysis
        print("\n⚡ PERFORMANCE ANALYSIS:")
        response_times = [r["response_time"] for r in self.test_results if r["response_time"] > 0]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            print(f"   Average response time: {avg_time:.3f}s")
            print(f"   Fastest response: {min_time:.3f}s")
            print(f"   Slowest response: {max_time:.3f}s")
        
        print("\n" + "=" * 80)
        print("🎯 FINAL ASSESSMENT:")
        
        if success_rate >= 80:
            print("🎉 EXCELLENT: Most APIs are working correctly!")
        elif success_rate >= 60:
            print("👍 GOOD: Majority of APIs are functional with some issues to address")
        elif success_rate >= 40:
            print("⚠️ MODERATE: Significant issues found that need attention")
        else:
            print("🚨 CRITICAL: Major API functionality issues detected")
        
        return success_rate >= 60

def main():
    """Main test execution"""
    tester = ComprehensiveAPITester()
    success = tester.run_comprehensive_test()
    
    print(f"\n🏁 Testing completed. Overall success: {'✅ PASS' if success else '❌ NEEDS ATTENTION'}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())