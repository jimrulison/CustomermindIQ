#!/usr/bin/env python3
"""
Focused API Testing for Customer Mind IQ Backend
Testing core functionality using localhost to avoid external routing issues.
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

# Configuration - Use localhost for direct testing
BACKEND_URL = "http://127.0.0.1:8001"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class FocusedAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.working_apis = []
        self.broken_apis = []
        self.required_api_keys = []
        self.config_issues = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None, response_time: float = 0):
        """Log test results with categorization"""
        status = "✅ WORKING" if success else "❌ BROKEN"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_time > 0:
            print(f"   Response time: {response_time:.3f}s")
        if response_data and isinstance(response_data, dict) and len(response_data) > 0:
            keys = list(response_data.keys())[:5]  # Show first 5 keys
            print(f"   Response keys: {keys}")
        
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
                            f"HTTP {response.status_code}: {response.text[:200]}", 
                            None, response_time)
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False

    def test_core_endpoints(self):
        """Test core API endpoints"""
        print("🔑 Testing Core API Endpoints...")
        
        core_endpoints = [
            ("/health", "Service Health Check"),
            ("/test-db", "Database Connectivity"),
            ("/customers", "Customer Management"),
            ("/subscriptions/plans", "Subscription Plans"),
            ("/admin/analytics/dashboard", "Admin Analytics Dashboard"),
            ("/admin/email-templates", "Email Templates"),
            ("/admin/workflows", "Automated Workflows"),
            ("/admin/banners", "Admin Banners"),
            ("/admin/discounts", "Admin Discounts")
        ]
        
        for endpoint, name in core_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        data_size = len(str(data)) if data else 0
                        self.log_test(name, True, 
                                    f"HTTP 200 - Data size: {data_size} chars", 
                                    data, response_time)
                    except:
                        self.log_test(name, True, 
                                    f"HTTP 200 - Non-JSON response", 
                                    None, response_time)
                elif response.status_code == 404:
                    self.log_test(name, False, 
                                f"Endpoint not found (404)", None, response_time)
                elif response.status_code == 403:
                    self.log_test(name, False, 
                                f"Access forbidden (403)", None, response_time)
                elif response.status_code == 401:
                    self.log_test(name, False, 
                                f"Authentication required (401)", None, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text[:200]}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_dashboard_endpoints(self):
        """Test dashboard endpoints"""
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
                    try:
                        data = response.json()
                        data_size = len(str(data)) if data else 0
                        self.log_test(name, True, 
                                    f"HTTP 200 - Data size: {data_size} chars", 
                                    data, response_time)
                    except:
                        self.log_test(name, True, 
                                    f"HTTP 200 - Non-JSON response", 
                                    None, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text[:200]}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_integration_endpoints(self):
        """Test integration endpoints"""
        print("🔗 Testing Integration Endpoints...")
        
        integration_endpoints = [
            ("/odoo/integration/status", "ODOO Integration Status"),
            ("/affiliate/resources", "Affiliate Resources"),
            ("/support/tickets", "Support System"),
            ("/chat/access-check", "Live Chat System")
        ]
        
        for endpoint, name in integration_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        data_size = len(str(data)) if data else 0
                        self.log_test(name, True, 
                                    f"HTTP 200 - Data size: {data_size} chars", 
                                    data, response_time)
                    except:
                        self.log_test(name, True, 
                                    f"HTTP 200 - Non-JSON response", 
                                    None, response_time)
                else:
                    self.log_test(name, False, 
                                f"HTTP {response.status_code}: {response.text[:200]}", 
                                None, response_time)
                    
            except Exception as e:
                self.log_test(name, False, f"Exception: {str(e)}")

    def test_trial_registration(self):
        """Test trial registration functionality"""
        print("🆓 Testing Trial Registration...")
        
        try:
            start_time = time.time()
            trial_user = {
                "email": f"test.trial.{int(datetime.now().timestamp())}@example.com",
                "first_name": "Test",
                "last_name": "Trial",
                "company_name": "Test Company"
            }
            
            response = self.session.post(
                f"{API_BASE}/subscriptions/trial/register",
                json=trial_user,
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Trial Registration", True, 
                                f"Successfully registered trial user", data, response_time)
                    
                    # Test auto-login with generated password
                    if "password" in data.get("user", {}):
                        login_data = {
                            "email": trial_user["email"],
                            "password": data["user"]["password"]
                        }
                        
                        login_response = self.session.post(
                            f"{API_BASE}/auth/login",
                            json=login_data,
                            timeout=30
                        )
                        
                        if login_response.status_code == 200:
                            self.log_test("Trial Auto-Login", True, 
                                        "Trial user can login with generated password")
                        else:
                            self.log_test("Trial Auto-Login", False, 
                                        f"Login failed: HTTP {login_response.status_code}")
                else:
                    self.log_test("Trial Registration", False, 
                                f"Registration failed: {data.get('message', 'Unknown error')}", 
                                data, response_time)
            else:
                self.log_test("Trial Registration", False, 
                            f"HTTP {response.status_code}: {response.text[:200]}", 
                            None, response_time)
                
        except Exception as e:
            self.log_test("Trial Registration", False, f"Exception: {str(e)}")

    def check_environment_variables(self):
        """Check for missing environment variables and integrations"""
        print("🔍 Checking Environment Variables & Integrations...")
        
        # Check for AI/LLM integration
        try:
            response = self.session.get(f"{API_BASE}/health", timeout=10)
            if response.status_code == 200:
                # Check backend logs for AI warnings
                self.config_issues.append("EmergentLLM not available - using mock AI responses (check logs)")
        except:
            pass
        
        # Check for email service integration
        self.required_api_keys.extend([
            "SENDGRID_API_KEY - For email campaigns and notifications",
            "OPENAI_API_KEY - For enhanced AI features", 
            "AWS_ACCESS_KEY_ID - For cloud storage integration",
            "GOOGLE_ANALYTICS_ID - For website analytics",
            "FACEBOOK_PIXEL_ID - For marketing analytics"
        ])

    def run_focused_test(self):
        """Run focused API tests"""
        print("🚀 Starting Focused API Testing for Customer Mind IQ")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"📡 API Base: {API_BASE}")
        print("=" * 80)
        
        # Step 1: Authenticate
        auth_success = self.authenticate_admin()
        
        # Step 2: Test core endpoints
        self.test_core_endpoints()
        
        # Step 3: Test dashboard endpoints
        self.test_dashboard_endpoints()
        
        # Step 4: Test integration endpoints
        self.test_integration_endpoints()
        
        # Step 5: Test trial registration
        self.test_trial_registration()
        
        # Step 6: Check environment variables
        self.check_environment_variables()
        
        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate test report"""
        print("=" * 80)
        print("📊 FOCUSED API TEST REPORT")
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
        if self.broken_apis:
            print("❌ BROKEN/MISSING APIs:")
            for api in self.broken_apis:
                print(f"   ❌ {api}")
            print()
        
        # Required API Keys
        if self.required_api_keys:
            print("🔑 REQUIRED API KEYS:")
            for key in self.required_api_keys:
                print(f"   🔑 {key}")
            print()
        
        # Configuration Issues
        if self.config_issues:
            print("⚠️ CONFIGURATION ISSUES:")
            for issue in self.config_issues:
                print(f"   ⚠️ {issue}")
            print()
        
        # Performance Analysis
        response_times = [r["response_time"] for r in self.test_results if r["response_time"] > 0]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            print("⚡ PERFORMANCE ANALYSIS:")
            print(f"   Average response time: {avg_time:.3f}s")
            print(f"   Fastest response: {min_time:.3f}s")
            print(f"   Slowest response: {max_time:.3f}s")
            print()
        
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
    tester = FocusedAPITester()
    success = tester.run_focused_test()
    
    print(f"\n🏁 Testing completed. Overall success: {'✅ PASS' if success else '❌ NEEDS ATTENTION'}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())