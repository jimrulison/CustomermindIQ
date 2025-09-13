#!/usr/bin/env python3
"""
Admin Portal Backend Testing - Focused on User-Reported Issues

This script tests the specific Admin Portal backend endpoints that were reported as problematic:

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. **Advanced Analytics Dashboard API** - Test `/api/admin/analytics/dashboard` endpoint
2. **Email Templates API** - Test email templates related endpoints  
3. **Automated Workflows API** - Test workflows endpoints
4. **Authentication Validation** - Test admin authentication with admin@customermindiq.com / CustomerMindIQ2025!

Focus: Verify that backend is responding correctly to support frontend fixes for refresh functionality and grey boxes.
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import urllib3
import time

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - Use production URL from frontend .env
BACKEND_URL = "https://customer-mind-iq-6.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AdminPortalTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None, response_time: float = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        time_info = f" ({response_time:.3f}s)" if response_time else ""
        print(f"{status} {test_name}{time_info}")
        if details:
            print(f"   Details: {details}")
        if response_data and isinstance(response_data, dict):
            data_size = len(str(response_data))
            print(f"   Response: {data_size} chars, keys: {list(response_data.keys())}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
        print()

    def authenticate_admin(self) -> bool:
        """Authenticate as admin user"""
        try:
            print("🔐 Authenticating as admin...")
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
                                response_time=response_time)
                    return True
                else:
                    self.log_test("Admin Authentication", False, "No access token in response", response_time=response_time)
                    return False
            else:
                self.log_test("Admin Authentication", False, 
                            f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False

    def test_advanced_analytics_dashboard(self) -> bool:
        """Test Advanced Analytics Dashboard API - Main focus of user complaint"""
        try:
            print("📊 Testing Advanced Analytics Dashboard API...")
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/admin/analytics/dashboard",
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for essential analytics data structure
                expected_fields = ["total_users", "active_users", "monthly_revenue", "total_revenue"]
                missing_fields = [field for field in expected_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Advanced Analytics Dashboard - Data Structure", False, 
                                f"Missing critical fields: {missing_fields}", data, response_time)
                    return False
                
                # Check for numeric values (not null/empty)
                numeric_fields = ["total_users", "active_users", "monthly_revenue"]
                invalid_numeric = []
                for field in numeric_fields:
                    value = data.get(field)
                    if not isinstance(value, (int, float)) or value < 0:
                        invalid_numeric.append(f"{field}={value}")
                
                if invalid_numeric:
                    self.log_test("Advanced Analytics Dashboard - Data Validation", False, 
                                f"Invalid numeric values: {invalid_numeric}", data, response_time)
                    return False
                
                # Success - dashboard returns proper data for refresh functionality
                self.log_test("Advanced Analytics Dashboard API", True, 
                            f"Dashboard data loaded successfully with all required fields", data, response_time)
                return True
                
            elif response.status_code == 401:
                self.log_test("Advanced Analytics Dashboard API", False, 
                            "Authentication failed - admin token may be invalid", response_time=response_time)
                return False
            elif response.status_code == 403:
                self.log_test("Advanced Analytics Dashboard API", False, 
                            "Access forbidden - insufficient permissions", response_time=response_time)
                return False
            else:
                self.log_test("Advanced Analytics Dashboard API", False, 
                            f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Advanced Analytics Dashboard API", False, f"Exception: {str(e)}")
            return False

    def test_email_templates_api(self) -> bool:
        """Test Email Templates API - User reported grey boxes issue"""
        try:
            print("📧 Testing Email Templates API...")
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/admin/email-templates",
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we get templates data (not empty/null)
                if isinstance(data, list):
                    if len(data) > 0:
                        # Check template structure
                        template = data[0]
                        required_fields = ["id", "name", "subject"]
                        missing_fields = [field for field in required_fields if field not in template]
                        
                        if missing_fields:
                            self.log_test("Email Templates API - Template Structure", False, 
                                        f"Template missing fields: {missing_fields}", data, response_time)
                            return False
                        
                        self.log_test("Email Templates API", True, 
                                    f"Successfully loaded {len(data)} email templates", data, response_time)
                        return True
                    else:
                        self.log_test("Email Templates API", True, 
                                    "No email templates found (empty list - valid response)", data, response_time)
                        return True
                        
                elif isinstance(data, dict):
                    # Check if it's a proper response object
                    if "templates" in data or "success" in data:
                        templates = data.get("templates", [])
                        self.log_test("Email Templates API", True, 
                                    f"Successfully loaded templates object with {len(templates)} templates", 
                                    data, response_time)
                        return True
                    else:
                        self.log_test("Email Templates API", False, 
                                    "Response object missing expected fields", data, response_time)
                        return False
                else:
                    self.log_test("Email Templates API", False, 
                                f"Unexpected response type: {type(data)}", data, response_time)
                    return False
                    
            elif response.status_code == 404:
                self.log_test("Email Templates API", False, 
                            "Endpoint not found - may not be implemented", response_time=response_time)
                return False
            elif response.status_code == 401:
                self.log_test("Email Templates API", False, 
                            "Authentication failed", response_time=response_time)
                return False
            else:
                self.log_test("Email Templates API", False, 
                            f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Email Templates API", False, f"Exception: {str(e)}")
            return False

    def test_automated_workflows_api(self) -> bool:
        """Test Automated Workflows API - User reported data loading issues"""
        try:
            print("⚙️ Testing Automated Workflows API...")
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/admin/workflows",
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we get workflows data
                if isinstance(data, list):
                    self.log_test("Automated Workflows API", True, 
                                f"Successfully loaded {len(data)} workflows", data, response_time)
                    return True
                        
                elif isinstance(data, dict):
                    # Check if it's a proper response object
                    if "workflows" in data or "success" in data:
                        workflows = data.get("workflows", [])
                        self.log_test("Automated Workflows API", True, 
                                    f"Successfully loaded workflows object with {len(workflows)} workflows", 
                                    data, response_time)
                        return True
                    else:
                        self.log_test("Automated Workflows API", False, 
                                    "Response object missing expected fields", data, response_time)
                        return False
                else:
                    self.log_test("Automated Workflows API", False, 
                                f"Unexpected response type: {type(data)}", data, response_time)
                    return False
                    
            elif response.status_code == 404:
                self.log_test("Automated Workflows API", False, 
                            "Endpoint not found - may not be implemented", response_time=response_time)
                return False
            elif response.status_code == 401:
                self.log_test("Automated Workflows API", False, 
                            "Authentication failed", response_time=response_time)
                return False
            else:
                self.log_test("Automated Workflows API", False, 
                            f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Automated Workflows API", False, f"Exception: {str(e)}")
            return False

    def test_health_check(self) -> bool:
        """Test basic health check to verify backend connectivity"""
        try:
            print("🔍 Testing backend health check...")
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/health",
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check health response structure
                required_fields = ["status", "service"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Health Check Structure", False, 
                                f"Missing fields: {missing_fields}", data, response_time)
                    return False
                
                if data.get("status") == "healthy":
                    self.log_test("Backend Health Check", True, 
                                f"Service healthy: {data.get('service')}", data, response_time)
                    return True
                else:
                    self.log_test("Backend Health Check", False, 
                                f"Service not healthy: {data.get('status')}", data, response_time)
                    return False
                
            else:
                self.log_test("Backend Health Check", False, 
                            f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Backend Health Check", False, f"Exception: {str(e)}")
            return False

    def test_admin_banners_api(self) -> bool:
        """Test Admin Banners API - Additional admin endpoint"""
        try:
            print("🏷️ Testing Admin Banners API...")
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/admin/banners",
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Admin Banners API", True, 
                            "Successfully accessed banners endpoint", data, response_time)
                return True
            elif response.status_code == 404:
                self.log_test("Admin Banners API", False, 
                            "Endpoint not found", response_time=response_time)
                return False
            elif response.status_code == 500:
                self.log_test("Admin Banners API", False, 
                            "Internal server error - may be MongoDB serialization issue", response_time=response_time)
                return False
            else:
                self.log_test("Admin Banners API", False, 
                            f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Admin Banners API", False, f"Exception: {str(e)}")
            return False

    def test_admin_discounts_api(self) -> bool:
        """Test Admin Discounts API - Additional admin endpoint"""
        try:
            print("💰 Testing Admin Discounts API...")
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/admin/discounts",
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Admin Discounts API", True, 
                            "Successfully accessed discounts endpoint", data, response_time)
                return True
            elif response.status_code == 404:
                self.log_test("Admin Discounts API", False, 
                            "Endpoint not found", response_time=response_time)
                return False
            elif response.status_code == 500:
                self.log_test("Admin Discounts API", False, 
                            "Internal server error - may be MongoDB serialization issue", response_time=response_time)
                return False
            else:
                self.log_test("Admin Discounts API", False, 
                            f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Admin Discounts API", False, f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all admin portal tests focusing on user-reported issues"""
        print("🚀 Starting Admin Portal Backend Testing - User Issue Focus")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"📡 API Base: {API_BASE}")
        print("🎯 Focus: Advanced Analytics Dashboard, Email Templates, Automated Workflows")
        print("=" * 80)
        
        # Step 1: Test basic connectivity
        health_test_passed = self.test_health_check()
        
        # Step 2: Authenticate as admin
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with admin endpoint tests.")
            return False
        
        # Step 3: Test the MAIN user-reported issues
        analytics_test_passed = self.test_advanced_analytics_dashboard()
        email_templates_test_passed = self.test_email_templates_api()
        workflows_test_passed = self.test_automated_workflows_api()
        
        # Step 4: Test additional admin endpoints
        banners_test_passed = self.test_admin_banners_api()
        discounts_test_passed = self.test_admin_discounts_api()
        
        # Summary
        print("=" * 80)
        print("📊 ADMIN PORTAL TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        # Critical test results (user-reported issues)
        critical_tests = [
            ("Backend Health Check", health_test_passed),
            ("Admin Authentication", self.admin_token is not None),
            ("Advanced Analytics Dashboard API", analytics_test_passed),
            ("Email Templates API", email_templates_test_passed),
            ("Automated Workflows API", workflows_test_passed)
        ]
        
        # Additional tests
        additional_tests = [
            ("Admin Banners API", banners_test_passed),
            ("Admin Discounts API", discounts_test_passed)
        ]
        
        critical_passed = sum(1 for _, passed in critical_tests if passed)
        critical_total = len(critical_tests)
        
        print(f"\n🎯 CRITICAL TESTS (User-Reported Issues): {critical_passed}/{critical_total}")
        for test_name, passed in critical_tests:
            status = "✅" if passed else "❌"
            print(f"   {status} {test_name}")
        
        print(f"\n🔧 ADDITIONAL ADMIN TESTS:")
        for test_name, passed in additional_tests:
            status = "✅" if passed else "❌"
            print(f"   {status} {test_name}")
        
        # Performance analysis
        response_times = [r["response_time"] for r in self.test_results if r["response_time"]]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"   Average response time: {avg_time:.3f}s")
            print(f"   Fastest response: {min_time:.3f}s")
            print(f"   Slowest response: {max_time:.3f}s")
        
        print("\n📋 Detailed Test Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            time_info = f" ({result['response_time']:.3f}s)" if result['response_time'] else ""
            print(f"{status} {result['test']}{time_info}: {result['details']}")
        
        # Determine overall success based on critical tests
        all_critical_passed = all(passed for _, passed in critical_tests)
        
        return all_critical_passed, critical_passed, critical_total

def main():
    """Main test execution"""
    tester = AdminPortalTester()
    success, critical_passed, critical_total = tester.run_comprehensive_test()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 CONCLUSION: All critical admin portal endpoints are working!")
        print("   ✅ Advanced Analytics Dashboard API - Ready for refresh functionality")
        print("   ✅ Email Templates API - Data loading properly (no grey boxes)")
        print("   ✅ Automated Workflows API - Data loading correctly")
        print("   ✅ Admin Authentication - Working with provided credentials")
        print("\n💡 RECOMMENDATION: Frontend fixes should resolve user-reported issues")
        sys.exit(0)
    else:
        print("💥 CONCLUSION: Some critical admin portal tests failed!")
        print(f"   📊 Critical Tests: {critical_passed}/{critical_total} passed")
        print("\n🔍 ISSUES FOUND:")
        
        failed_tests = [r for r in tester.test_results if not r["success"]]
        for result in failed_tests:
            print(f"   ❌ {result['test']}: {result['details']}")
        
        print("\n💡 RECOMMENDATION: Backend issues need to be resolved before frontend can work properly")
        sys.exit(1)

if __name__ == "__main__":
    main()