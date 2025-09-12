#!/usr/bin/env python3
"""
Enhanced Modal Systems Backend Validation Test

This script tests the backend endpoints that support the enhanced modal systems
for Analytics & Insights and Integration Data Hub as requested in the review.

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. **Product Intelligence Endpoints (already working):**
   - GET /api/product-intelligence/feature-usage-dashboard 
   - GET /api/product-intelligence/onboarding-dashboard
   - GET /api/product-intelligence/pmf-dashboard  
   - GET /api/product-intelligence/journey-dashboard

2. **Website Intelligence Endpoints:**
   - GET /api/website-intelligence/dashboard
   - GET /api/website-intelligence/performance-dashboard
   - GET /api/website-intelligence/seo-dashboard
   - GET /api/website-intelligence/membership-status

3. **Integration Data Hub Endpoints:**
   - GET /api/integration-hub/connectors-dashboard
   - GET /api/integration-hub/sync-dashboard
   - GET /api/integration-hub/quality-dashboard
   - GET /api/integration-hub/analytics-dashboard

4. **Authentication & Performance:**
   - POST /api/auth/login with admin credentials
   - Verify all endpoints return structured data for modal display
   - Test response times are acceptable for UI performance (<2 seconds)

Use admin credentials: admin@customermindiq.com / CustomerMindIQ2025!
"""

import asyncio
import json
import os
import sys
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - Use production URL from frontend .env
BACKEND_URL = "https://mindindata.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class EnhancedModalSystemsTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.admin_token = None
        self.test_results = []
        self.response_times = []
        
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
        
        if response_time:
            self.response_times.append(response_time)
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

    def test_product_intelligence_endpoints(self) -> bool:
        """Test Product Intelligence endpoints for modal data support"""
        try:
            print("🧠 Testing Product Intelligence endpoints...")
            
            endpoints = [
                ("feature-usage-dashboard", "Feature Usage Dashboard"),
                ("onboarding-dashboard", "Onboarding Dashboard"),
                ("pmf-dashboard", "Product-Market Fit Dashboard"),
                ("journey-dashboard", "Journey Dashboard")
            ]
            
            all_passed = True
            
            for endpoint, name in endpoints:
                try:
                    start_time = time.time()
                    response = self.session.get(
                        f"{API_BASE}/product-intelligence/{endpoint}",
                        timeout=30
                    )
                    response_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check if response has structured data for modals
                        if isinstance(data, dict) and len(data) > 0:
                            self.log_test(f"Product Intelligence - {name}", True, 
                                        f"HTTP 200 with structured data", data, response_time)
                        else:
                            self.log_test(f"Product Intelligence - {name}", False, 
                                        "Empty or invalid response structure", response_time=response_time)
                            all_passed = False
                    else:
                        self.log_test(f"Product Intelligence - {name}", False, 
                                    f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                        all_passed = False
                        
                except Exception as e:
                    self.log_test(f"Product Intelligence - {name}", False, f"Exception: {str(e)}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test("Product Intelligence Endpoints", False, f"Exception: {str(e)}")
            return False

    def test_website_intelligence_endpoints(self) -> bool:
        """Test Website Intelligence endpoints for modal data support"""
        try:
            print("🌐 Testing Website Intelligence endpoints...")
            
            endpoints = [
                ("dashboard", "Main Dashboard"),
                ("performance-dashboard", "Performance Dashboard"),
                ("seo-dashboard", "SEO Dashboard"),
                ("membership-status", "Membership Status")
            ]
            
            all_passed = True
            
            for endpoint, name in endpoints:
                try:
                    start_time = time.time()
                    response = self.session.get(
                        f"{API_BASE}/website-intelligence/{endpoint}",
                        timeout=30
                    )
                    response_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check if response has structured data for modals
                        if isinstance(data, dict) and len(data) > 0:
                            self.log_test(f"Website Intelligence - {name}", True, 
                                        f"HTTP 200 with structured data", data, response_time)
                        else:
                            self.log_test(f"Website Intelligence - {name}", False, 
                                        "Empty or invalid response structure", response_time=response_time)
                            all_passed = False
                    else:
                        self.log_test(f"Website Intelligence - {name}", False, 
                                    f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                        all_passed = False
                        
                except Exception as e:
                    self.log_test(f"Website Intelligence - {name}", False, f"Exception: {str(e)}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test("Website Intelligence Endpoints", False, f"Exception: {str(e)}")
            return False

    def test_integration_hub_endpoints(self) -> bool:
        """Test Integration Data Hub endpoints for modal data support"""
        try:
            print("🔗 Testing Integration Data Hub endpoints...")
            
            endpoints = [
                ("connectors-dashboard", "Connectors Dashboard"),
                ("sync-dashboard", "Sync Dashboard"),
                ("quality-dashboard", "Quality Dashboard"),
                ("analytics-dashboard", "Analytics Dashboard")
            ]
            
            all_passed = True
            
            for endpoint, name in endpoints:
                try:
                    start_time = time.time()
                    response = self.session.get(
                        f"{API_BASE}/integration-hub/{endpoint}",
                        timeout=30
                    )
                    response_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check if response has structured data for modals
                        if isinstance(data, dict) and len(data) > 0:
                            self.log_test(f"Integration Hub - {name}", True, 
                                        f"HTTP 200 with structured data", data, response_time)
                        else:
                            self.log_test(f"Integration Hub - {name}", False, 
                                        "Empty or invalid response structure", response_time=response_time)
                            all_passed = False
                    else:
                        self.log_test(f"Integration Hub - {name}", False, 
                                    f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                        all_passed = False
                        
                except Exception as e:
                    self.log_test(f"Integration Hub - {name}", False, f"Exception: {str(e)}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test("Integration Hub Endpoints", False, f"Exception: {str(e)}")
            return False

    def test_performance_requirements(self) -> bool:
        """Test that response times meet modal performance requirements (<2 seconds)"""
        try:
            print("⚡ Testing performance requirements...")
            
            if not self.response_times:
                self.log_test("Performance Requirements", False, "No response times recorded")
                return False
            
            avg_response_time = sum(self.response_times) / len(self.response_times)
            max_response_time = max(self.response_times)
            min_response_time = min(self.response_times)
            
            # Check if all responses are under 2 seconds (modal performance requirement)
            slow_responses = [t for t in self.response_times if t > 2.0]
            
            if len(slow_responses) == 0:
                self.log_test("Performance Requirements", True, 
                            f"All responses under 2s (avg: {avg_response_time:.3f}s, max: {max_response_time:.3f}s, min: {min_response_time:.3f}s)")
                return True
            else:
                self.log_test("Performance Requirements", False, 
                            f"{len(slow_responses)} responses over 2s (avg: {avg_response_time:.3f}s, max: {max_response_time:.3f}s)")
                return False
                
        except Exception as e:
            self.log_test("Performance Requirements", False, f"Exception: {str(e)}")
            return False

    def test_error_handling(self) -> bool:
        """Test error handling for invalid requests"""
        try:
            print("🚫 Testing error handling...")
            
            # Test with invalid authentication
            original_headers = self.session.headers.copy()
            self.session.headers.update({"Authorization": "Bearer invalid_token"})
            
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/product-intelligence/feature-usage-dashboard",
                timeout=30
            )
            response_time = time.time() - start_time
            
            # Restore original headers
            self.session.headers = original_headers
            
            if response.status_code == 401:
                self.log_test("Error Handling - Invalid Auth", True, 
                            "Correctly returned 401 for invalid token", response_time=response_time)
                return True
            else:
                self.log_test("Error Handling - Invalid Auth", False, 
                            f"Expected 401, got {response.status_code}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")
            return False

    def test_health_check(self) -> bool:
        """Test basic health check endpoint"""
        try:
            print("🔍 Testing health check...")
            start_time = time.time()
            response = self.session.get(
                f"{API_BASE}/health",
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Check health response structure
                required_fields = ["status", "service", "version", "timestamp"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Health Check", False, f"Missing fields: {missing_fields}", response_time=response_time)
                    return False
                
                if data.get("status") == "healthy":
                    self.log_test("Health Check", True, 
                                f"Service healthy: {data.get('service')} v{data.get('version')}", 
                                data, response_time)
                    return True
                else:
                    self.log_test("Health Check", False, f"Service not healthy: {data.get('status')}", response_time=response_time)
                    return False
                
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}", response_time=response_time)
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all enhanced modal systems tests"""
        print("🚀 Starting Enhanced Modal Systems Backend Validation")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"📡 API Base: {API_BASE}")
        print("=" * 80)
        
        # Step 1: Authenticate
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return False
        
        # Step 2: Test health check
        health_test_passed = self.test_health_check()
        
        # Step 3: Test Product Intelligence endpoints (already working according to test_result.md)
        product_intelligence_passed = self.test_product_intelligence_endpoints()
        
        # Step 4: Test Website Intelligence endpoints
        website_intelligence_passed = self.test_website_intelligence_endpoints()
        
        # Step 5: Test Integration Hub endpoints
        integration_hub_passed = self.test_integration_hub_endpoints()
        
        # Step 6: Test performance requirements
        performance_passed = self.test_performance_requirements()
        
        # Step 7: Test error handling
        error_handling_passed = self.test_error_handling()
        
        # Summary
        print("=" * 80)
        print("📊 ENHANCED MODAL SYSTEMS TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        # Performance summary
        if self.response_times:
            avg_time = sum(self.response_times) / len(self.response_times)
            max_time = max(self.response_times)
            print(f"⚡ Performance: avg {avg_time:.3f}s, max {max_time:.3f}s")
        
        # Critical test results
        critical_tests = [
            ("Authentication", self.admin_token is not None),
            ("Health Check", health_test_passed),
            ("Product Intelligence Endpoints", product_intelligence_passed),
            ("Website Intelligence Endpoints", website_intelligence_passed),
            ("Integration Hub Endpoints", integration_hub_passed),
            ("Performance Requirements", performance_passed),
            ("Error Handling", error_handling_passed)
        ]
        
        all_critical_passed = all(passed for _, passed in critical_tests)
        
        if all_critical_passed:
            print("🎉 ALL ENHANCED MODAL SYSTEMS TESTS PASSED!")
            print("✅ Authentication system working")
            print("✅ Product Intelligence endpoints returning structured data")
            print("✅ Website Intelligence endpoints operational")
            print("✅ Integration Hub endpoints functional")
            print("✅ Response times meet modal performance requirements (<2s)")
            print("✅ Error handling working correctly")
        else:
            print("⚠️  Some critical tests failed:")
            for test_name, passed in critical_tests:
                if not passed:
                    print(f"   ❌ {test_name}")
        
        print("\n📋 Detailed Test Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            time_info = f" ({result['response_time']:.3f}s)" if result.get('response_time') else ""
            print(f"{status} {result['test']}{time_info}: {result['details']}")
        
        return all_critical_passed

def main():
    """Main test execution"""
    tester = EnhancedModalSystemsTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 CONCLUSION: Enhanced Modal Systems backend support is working correctly!")
        print("   - All endpoints return structured data for modal display")
        print("   - Response times meet UI performance requirements")
        print("   - Authentication and error handling working properly")
        print("   - Product Intelligence, Website Intelligence, and Integration Hub ready for enhanced modals")
        sys.exit(0)
    else:
        print("\n💥 CONCLUSION: Some enhanced modal systems tests failed!")
        print("   - Check failed endpoints and fix backend issues")
        print("   - Ensure all endpoints return proper structured data")
        print("   - Verify response times are under 2 seconds for optimal modal loading")
        sys.exit(1)

if __name__ == "__main__":
    main()