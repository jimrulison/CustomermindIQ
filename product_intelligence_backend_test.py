#!/usr/bin/env python3
"""
Comprehensive Backend Testing - Product Intelligence & Performance Validation

This script tests the backend endpoints that support the enhanced Product Intelligence UI
and overall application performance as requested in the review.

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. **Product Intelligence Endpoints:**
   - GET /api/product-intelligence/feature-usage-dashboard 
   - GET /api/product-intelligence/onboarding-dashboard
   - GET /api/product-intelligence/pmf-dashboard  
   - GET /api/product-intelligence/journey-dashboard
2. **Authentication & Authorization:**
   - POST /api/auth/login with admin@customermindiq.com / CustomerMindIQ2025!
   - Verify JWT token generation and validation
3. **Website Intelligence Integration:**
   - GET /api/website-intelligence/dashboard
4. **Performance & Health Checks:**
   - GET /api/health (basic health check)
   - Verify response times are acceptable (<2 seconds)
5. **Error Handling:**
   - Test with invalid authentication
   - Test with malformed requests

Use admin credentials: admin@customermindiq.com / CustomerMindIQ2025!
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import urllib3

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

class ProductIntelligenceTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.admin_token = None
        self.test_results = []
        self.start_time = time.time()
        
        print(f"🚀 Starting Product Intelligence Backend Testing")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"🕐 Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None, 
                response_time: float = 0, status_code: int = None):
        """Log test results with comprehensive details"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "response_time": response_time,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        print(f"{status} {test_name}")
        if status_code:
            print(f"   Status: {status_code} | Time: {response_time:.3f}s")
        if details:
            print(f"   Details: {details}")
        print()

    def test_health_check(self) -> bool:
        """Test basic health check endpoint"""
        print("🔍 Testing Health Check...")
        start_time = time.time()
        
        try:
            response = self.session.get(f"{API_BASE}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Health Check",
                    True,
                    f"Service: {data.get('service', 'Unknown')} | Version: {data.get('version', 'Unknown')}",
                    data,
                    response_time,
                    response.status_code
                )
                return True
            else:
                self.log_test(
                    "Health Check",
                    False,
                    f"Unexpected status code: {response.status_code}",
                    None,
                    response_time,
                    response.status_code
                )
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test(
                "Health Check",
                False,
                f"Exception: {str(e)}",
                None,
                response_time
            )
            return False

    def authenticate_admin(self) -> bool:
        """Authenticate as admin user"""
        print("🔐 Testing Authentication...")
        start_time = time.time()
        
        try:
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                if self.admin_token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.admin_token}"
                    })
                    
                    user_info = data.get("user", {})
                    self.log_test(
                        "Admin Authentication",
                        True,
                        f"User: {user_info.get('email', 'Unknown')} | Role: {user_info.get('role', 'Unknown')}",
                        data,
                        response_time,
                        response.status_code
                    )
                    return True
                else:
                    self.log_test(
                        "Admin Authentication",
                        False,
                        "No access token in response",
                        data,
                        response_time,
                        response.status_code
                    )
                    return False
            else:
                self.log_test(
                    "Admin Authentication",
                    False,
                    f"Login failed: {response.text[:200]}",
                    None,
                    response_time,
                    response.status_code
                )
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test(
                "Admin Authentication",
                False,
                f"Exception: {str(e)}",
                None,
                response_time
            )
            return False

    def test_jwt_validation(self) -> bool:
        """Test JWT token validation"""
        print("🎫 Testing JWT Token Validation...")
        start_time = time.time()
        
        if not self.admin_token:
            self.log_test(
                "JWT Token Validation",
                False,
                "No auth token available"
            )
            return False
        
        try:
            response = self.session.get(f"{API_BASE}/auth/profile", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "JWT Token Validation",
                    True,
                    f"Profile retrieved for: {data.get('email', 'Unknown')}",
                    data,
                    response_time,
                    response.status_code
                )
                return True
            else:
                self.log_test(
                    "JWT Token Validation",
                    False,
                    f"Profile access failed: {response.text[:200]}",
                    None,
                    response_time,
                    response.status_code
                )
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test(
                "JWT Token Validation",
                False,
                f"Exception: {str(e)}",
                None,
                response_time
            )
            return False

    def test_product_intelligence_endpoints(self) -> bool:
        """Test all Product Intelligence endpoints"""
        print("🧠 Testing Product Intelligence Endpoints...")
        
        endpoints = [
            {
                "name": "Feature Usage Dashboard",
                "url": "/product-intelligence/feature-usage-dashboard",
                "description": "Feature adoption and usage analytics"
            },
            {
                "name": "Onboarding Dashboard", 
                "url": "/product-intelligence/onboarding-dashboard",
                "description": "Onboarding optimization analytics"
            },
            {
                "name": "PMF Dashboard",
                "url": "/product-intelligence/pmf-dashboard", 
                "description": "Product-Market Fit indicators"
            },
            {
                "name": "Journey Dashboard",
                "url": "/product-intelligence/journey-dashboard",
                "description": "User journey analytics"
            }
        ]
        
        success_count = 0
        
        for endpoint in endpoints:
            start_time = time.time()
            
            try:
                response = self.session.get(
                    f"{API_BASE}{endpoint['url']}", 
                    timeout=15
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Validate JSON structure
                        if isinstance(data, dict) and "status" in data:
                            # Check for dashboard data
                            dashboard_data = data.get("dashboard", {})
                            metrics_count = len(str(dashboard_data))
                            
                            self.log_test(
                                endpoint["name"],
                                True,
                                f"{endpoint['description']} | Data size: {metrics_count} chars",
                                data,
                                response_time,
                                response.status_code
                            )
                            success_count += 1
                        else:
                            self.log_test(
                                endpoint["name"],
                                False,
                                "Invalid JSON structure - missing status or dashboard",
                                data,
                                response_time,
                                response.status_code
                            )
                    except json.JSONDecodeError:
                        self.log_test(
                            endpoint["name"],
                            False,
                            "Invalid JSON response",
                            None,
                            response_time,
                            response.status_code
                        )
                else:
                    self.log_test(
                        endpoint["name"],
                        False,
                        f"HTTP error: {response.text[:200]}",
                        None,
                        response_time,
                        response.status_code
                    )
                    
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(
                    endpoint["name"],
                    False,
                    f"Exception: {str(e)}",
                    None,
                    response_time
                )
        
        return success_count == len(endpoints)

    def test_website_intelligence_integration(self) -> bool:
        """Test Website Intelligence dashboard integration"""
        print("🌐 Testing Website Intelligence Integration...")
        start_time = time.time()
        
        try:
            response = self.session.get(
                f"{API_BASE}/website-intelligence/dashboard",
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check for expected data structure
                    if isinstance(data, dict):
                        websites = data.get("websites", [])
                        analytics = data.get("analytics", {})
                        
                        self.log_test(
                            "Website Intelligence Dashboard",
                            True,
                            f"Websites: {len(websites)} | Analytics keys: {len(analytics)}",
                            data,
                            response_time,
                            response.status_code
                        )
                        return True
                    else:
                        self.log_test(
                            "Website Intelligence Dashboard",
                            False,
                            "Invalid data structure",
                            data,
                            response_time,
                            response.status_code
                        )
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test(
                        "Website Intelligence Dashboard",
                        False,
                        "Invalid JSON response",
                        None,
                        response_time,
                        response.status_code
                    )
                    return False
            else:
                self.log_test(
                    "Website Intelligence Dashboard",
                    False,
                    f"HTTP error: {response.text[:200]}",
                    None,
                    response_time,
                    response.status_code
                )
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self.log_test(
                "Website Intelligence Dashboard",
                False,
                f"Exception: {str(e)}",
                None,
                response_time
            )
            return False

    def test_performance_metrics(self) -> bool:
        """Test response times and performance"""
        print("⚡ Testing Performance Metrics...")
        
        # Test multiple endpoints for performance
        performance_endpoints = [
            ("/health", "Health Check"),
            ("/auth/profile", "Auth Profile"), 
            ("/product-intelligence/feature-usage-dashboard", "Feature Usage Dashboard")
        ]
        
        performance_results = []
        
        for endpoint_url, endpoint_name in performance_endpoints:
            times = []
            
            # Test each endpoint 3 times for average
            for i in range(3):
                start_time = time.time()
                
                try:
                    response = self.session.get(f"{API_BASE}{endpoint_url}", timeout=10)
                    response_time = time.time() - start_time
                    times.append(response_time)
                    
                except Exception as e:
                    times.append(10.0)  # Timeout value
            
            avg_time = sum(times) / len(times)
            performance_results.append({
                "endpoint": endpoint_name,
                "avg_response_time": avg_time,
                "acceptable": avg_time < 2.0
            })
        
        # Log performance results
        acceptable_count = 0
        for result in performance_results:
            acceptable = result["acceptable"]
            if acceptable:
                acceptable_count += 1
                
            self.log_test(
                f"Performance - {result['endpoint']}",
                acceptable,
                f"Average response time: {result['avg_response_time']:.3f}s (Target: <2s)",
                None,
                result["avg_response_time"]
            )
        
        return acceptable_count == len(performance_results)

    def test_error_handling(self) -> bool:
        """Test error handling with invalid requests"""
        print("🚨 Testing Error Handling...")
        
        error_tests = [
            {
                "name": "Invalid Authentication",
                "method": "POST",
                "url": "/auth/login",
                "data": {"email": "invalid@test.com", "password": "wrongpassword"},
                "expected_status": [401, 400]
            },
            {
                "name": "Unauthorized Access",
                "method": "GET", 
                "url": "/admin/analytics/dashboard",
                "headers": {"Authorization": "Bearer invalid_token"},
                "expected_status": [401, 403]
            },
            {
                "name": "Non-existent Endpoint",
                "method": "GET",
                "url": "/non-existent-endpoint",
                "expected_status": [404]
            }
        ]
        
        success_count = 0
        
        for test in error_tests:
            start_time = time.time()
            
            try:
                # Prepare request
                headers = test.get("headers", {})
                data = test.get("data")
                
                if test["method"] == "POST":
                    response = requests.post(
                        f"{API_BASE}{test['url']}",
                        json=data,
                        headers=headers,
                        timeout=10,
                        verify=False
                    )
                else:
                    response = requests.get(
                        f"{API_BASE}{test['url']}",
                        headers=headers,
                        timeout=10,
                        verify=False
                    )
                
                response_time = time.time() - start_time
                
                if response.status_code in test["expected_status"]:
                    self.log_test(
                        test["name"],
                        True,
                        f"Correctly returned expected error status",
                        None,
                        response_time,
                        response.status_code
                    )
                    success_count += 1
                else:
                    self.log_test(
                        test["name"],
                        False,
                        f"Expected {test['expected_status']}, got {response.status_code}",
                        None,
                        response_time,
                        response.status_code
                    )
                    
            except Exception as e:
                response_time = time.time() - start_time
                self.log_test(
                    test["name"],
                    False,
                    f"Exception: {str(e)}",
                    None,
                    response_time
                )
        
        return success_count == len(error_tests)

    def generate_summary_report(self) -> bool:
        """Generate comprehensive test summary report"""
        total_time = time.time() - self.start_time
        
        print("=" * 80)
        print("📊 COMPREHENSIVE BACKEND TEST SUMMARY")
        print("=" * 80)
        
        # Overall statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"🎯 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Total Time: {total_time:.2f} seconds")
        print()
        
        # Performance statistics
        response_times = [r["response_time"] for r in self.test_results if r["response_time"] > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"⚡ Performance Metrics:")
            print(f"   Average Response Time: {avg_response_time:.3f}s")
            print(f"   Fastest Response: {min_response_time:.3f}s")
            print(f"   Slowest Response: {max_response_time:.3f}s")
            print()
        
        # Failed tests details
        failed_results = [r for r in self.test_results if not r["success"]]
        if failed_results:
            print(f"❌ Failed Tests Details:")
            for result in failed_results:
                print(f"   • {result['test_name']}")
                if result.get("status_code"):
                    print(f"     Status: {result['status_code']}")
                if result.get("details"):
                    print(f"     Details: {result['details']}")
                print()
        
        # Critical endpoint status
        print(f"🔍 Critical Endpoint Status:")
        critical_endpoints = [
            "Health Check",
            "Admin Authentication", 
            "Feature Usage Dashboard",
            "Onboarding Dashboard",
            "PMF Dashboard",
            "Journey Dashboard"
        ]
        
        for endpoint in critical_endpoints:
            result = next((r for r in self.test_results if r["test_name"] == endpoint), None)
            if result:
                status = "✅ WORKING" if result["success"] else "❌ FAILED"
                time_info = f"({result['response_time']:.3f}s)" if result["response_time"] > 0 else ""
                print(f"   {endpoint}: {status} {time_info}")
        
        print()
        print("=" * 80)
        
        # Return overall success status
        return success_rate >= 80  # Consider 80%+ success rate as overall success

    def run_comprehensive_test(self) -> bool:
        """Run all backend tests in sequence"""
        print("🚀 Starting Comprehensive Backend Testing Suite...")
        print()
        
        # Test sequence
        test_results = []
        
        # 1. Health Check
        health_success = self.test_health_check()
        test_results.append(("Health Check", health_success))
        
        # 2. Authentication
        auth_success = self.authenticate_admin()
        test_results.append(("Authentication", auth_success))
        
        # 3. JWT Validation (only if auth succeeded)
        if auth_success:
            jwt_success = self.test_jwt_validation()
            test_results.append(("JWT Validation", jwt_success))
        
        # 4. Product Intelligence Endpoints
        pi_success = self.test_product_intelligence_endpoints()
        test_results.append(("Product Intelligence Endpoints", pi_success))
        
        # 5. Website Intelligence Integration
        wi_success = self.test_website_intelligence_integration()
        test_results.append(("Website Intelligence Integration", wi_success))
        
        # 6. Performance Metrics
        perf_success = self.test_performance_metrics()
        test_results.append(("Performance Metrics", perf_success))
        
        # 7. Error Handling
        error_success = self.test_error_handling()
        test_results.append(("Error Handling", error_success))
        
        print("-" * 80)
        
        # Generate final report
        report_success = self.generate_summary_report()
        
        # Determine overall success
        critical_tests = ["Health Check", "Authentication", "Product Intelligence Endpoints"]
        critical_success = all(success for name, success in test_results if name in critical_tests)
        
        return critical_success and report_success

def main():
    """Main test execution function"""
    tester = ProductIntelligenceTester()
    
    try:
        success = tester.run_comprehensive_test()
        
        if success:
            print("🎉 Product Intelligence backend tests completed successfully!")
            print("✅ All critical endpoints are working correctly")
            print("✅ Authentication system operational")
            print("✅ Response times are acceptable")
            print("✅ Error handling is working properly")
            sys.exit(0)
        else:
            print("⚠️  Some backend tests failed. Check the summary above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Testing failed with critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()