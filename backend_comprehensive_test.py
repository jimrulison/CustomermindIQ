#!/usr/bin/env python3
"""
Backend Comprehensive Testing - Post Legal Pages Implementation

This script tests backend functionality after implementing new legal pages, 
contact page, 404 page, and cookie consent functionality to ensure all 
existing endpoints still work correctly.

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. Test existing backend endpoints to make sure they still work
2. Check if there are any backend endpoints related to contact form submission
3. Verify the general health and functionality of the backend API  
4. Test key endpoints like /api/health, /api/auth routes

Use admin credentials: admin@customermindiq.com / CustomerMindIQ2025!
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - Use production URL from frontend .env
BACKEND_URL = "https://customeriq-fix.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.auth_token = None
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_test(self, test_name: str, success: bool, details: str, response_time: float = 0):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "response_time": f"{response_time:.3f}s",
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {details} ({response_time:.3f}s)")
        
    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> tuple:
        """Make HTTP request and return response with timing"""
        url = f"{API_BASE}{endpoint}"
        request_headers = {"Content-Type": "application/json"}
        
        if headers:
            request_headers.update(headers)
            
        if self.auth_token:
            request_headers["Authorization"] = f"Bearer {self.auth_token}"
            
        start_time = datetime.now()
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=request_headers, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=request_headers, timeout=30)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=request_headers, timeout=30)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=request_headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response_time = (datetime.now() - start_time).total_seconds()
            return response, response_time
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return None, response_time
    
    async def test_health_endpoint(self):
        """Test 1: Health Check Endpoint"""
        print("\n🔍 Testing Health Check Endpoint...")
        
        response, response_time = self.make_request("GET", "/health")
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test(
                        "Health Check", 
                        True, 
                        f"Service healthy - {data.get('service', 'Unknown')} v{data.get('version', 'Unknown')}", 
                        response_time
                    )
                else:
                    self.log_test("Health Check", False, f"Unexpected health response: {data}", response_time)
            except json.JSONDecodeError:
                self.log_test("Health Check", False, f"Invalid JSON response: {response.text[:100]}", response_time)
        else:
            error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
            self.log_test("Health Check", False, error_msg, response_time)
    
    async def test_admin_authentication(self):
        """Test 2: Admin Authentication"""
        print("\n🔐 Testing Admin Authentication...")
        
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        response, response_time = self.make_request("POST", "/auth/login", login_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if "access_token" in data:
                    self.auth_token = data["access_token"]
                    self.log_test(
                        "Admin Authentication", 
                        True, 
                        f"Login successful, token received (length: {len(self.auth_token)})", 
                        response_time
                    )
                    return True
                else:
                    self.log_test("Admin Authentication", False, f"No access token in response: {data}", response_time)
            except json.JSONDecodeError:
                self.log_test("Admin Authentication", False, f"Invalid JSON response: {response.text[:100]}", response_time)
        else:
            error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('detail', 'Unknown error')}"
                except:
                    pass
            self.log_test("Admin Authentication", False, error_msg, response_time)
        
        return False
    
    async def test_auth_me_endpoint(self):
        """Test 3: Current User Info Endpoint"""
        print("\n👤 Testing Current User Info...")
        
        if not self.auth_token:
            self.log_test("Current User Info", False, "No auth token available", 0)
            return
            
        response, response_time = self.make_request("GET", "/auth/me")
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if "email" in data and data["email"] == ADMIN_EMAIL:
                    self.log_test(
                        "Current User Info", 
                        True, 
                        f"User info retrieved - Role: {data.get('role', 'Unknown')}, Tier: {data.get('subscription_tier', 'Unknown')}", 
                        response_time
                    )
                else:
                    self.log_test("Current User Info", False, f"Unexpected user data: {data}", response_time)
            except json.JSONDecodeError:
                self.log_test("Current User Info", False, f"Invalid JSON response: {response.text[:100]}", response_time)
        else:
            error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
            self.log_test("Current User Info", False, error_msg, response_time)
    
    async def test_contact_form_endpoints(self):
        """Test 4: Contact Form Related Endpoints"""
        print("\n📧 Testing Contact Form Endpoints...")
        
        # Test potential contact form submission endpoint
        contact_endpoints = [
            "/contact",
            "/contact/submit", 
            "/support/contact",
            "/admin/contact-forms",
            "/support/tickets"
        ]
        
        for endpoint in contact_endpoints:
            response, response_time = self.make_request("GET", endpoint)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.log_test(
                        f"Contact Endpoint {endpoint}", 
                        True, 
                        f"Endpoint accessible - Response size: {len(str(data))} chars", 
                        response_time
                    )
                except json.JSONDecodeError:
                    self.log_test(
                        f"Contact Endpoint {endpoint}", 
                        True, 
                        f"Endpoint accessible - HTML/Text response: {len(response.text)} chars", 
                        response_time
                    )
            elif response and response.status_code == 404:
                self.log_test(
                    f"Contact Endpoint {endpoint}", 
                    True, 
                    "Endpoint not found (expected for some endpoints)", 
                    response_time
                )
            else:
                error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
                self.log_test(f"Contact Endpoint {endpoint}", False, error_msg, response_time)
    
    async def test_core_api_endpoints(self):
        """Test 5: Core API Endpoints"""
        print("\n🔧 Testing Core API Endpoints...")
        
        core_endpoints = [
            ("/customers", "GET"),
            ("/analytics", "GET"), 
            ("/campaigns", "GET"),
            ("/admin/analytics/dashboard", "GET"),
            ("/subscriptions/plans", "GET")
        ]
        
        for endpoint, method in core_endpoints:
            response, response_time = self.make_request(method, endpoint)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.log_test(
                        f"Core API {method} {endpoint}", 
                        True, 
                        f"Endpoint working - Response size: {len(str(data))} chars", 
                        response_time
                    )
                except json.JSONDecodeError:
                    self.log_test(
                        f"Core API {method} {endpoint}", 
                        False, 
                        f"Invalid JSON response: {response.text[:100]}", 
                        response_time
                    )
            elif response and response.status_code in [401, 403]:
                self.log_test(
                    f"Core API {method} {endpoint}", 
                    True, 
                    f"Authentication required (HTTP {response.status_code}) - Expected behavior", 
                    response_time
                )
            else:
                error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
                if response:
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('detail', 'Unknown error')}"
                    except:
                        pass
                self.log_test(f"Core API {method} {endpoint}", False, error_msg, response_time)
    
    async def test_admin_endpoints(self):
        """Test 6: Admin-Specific Endpoints"""
        print("\n👑 Testing Admin Endpoints...")
        
        if not self.auth_token:
            self.log_test("Admin Endpoints", False, "No auth token available", 0)
            return
            
        admin_endpoints = [
            "/admin/banners",
            "/admin/discounts", 
            "/admin/email-templates",
            "/admin/workflows",
            "/admin/users"
        ]
        
        for endpoint in admin_endpoints:
            response, response_time = self.make_request("GET", endpoint)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    self.log_test(
                        f"Admin Endpoint {endpoint}", 
                        True, 
                        f"Endpoint accessible - Response size: {len(str(data))} chars", 
                        response_time
                    )
                except json.JSONDecodeError:
                    self.log_test(
                        f"Admin Endpoint {endpoint}", 
                        False, 
                        f"Invalid JSON response: {response.text[:100]}", 
                        response_time
                    )
            elif response and response.status_code == 404:
                self.log_test(
                    f"Admin Endpoint {endpoint}", 
                    False, 
                    "Endpoint not found - May indicate routing issues", 
                    response_time
                )
            elif response and response.status_code == 500:
                self.log_test(
                    f"Admin Endpoint {endpoint}", 
                    False, 
                    "Internal server error - Backend issue detected", 
                    response_time
                )
            else:
                error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
                self.log_test(f"Admin Endpoint {endpoint}", False, error_msg, response_time)
    
    async def test_trial_registration(self):
        """Test 7: Trial Registration Endpoint"""
        print("\n🆓 Testing Trial Registration...")
        
        trial_data = {
            "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company"
        }
        
        response, response_time = self.make_request("POST", "/subscriptions/trial/register", trial_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test(
                        "Trial Registration", 
                        True, 
                        f"Trial registration successful - User created with password", 
                        response_time
                    )
                else:
                    self.log_test("Trial Registration", False, f"Unexpected response: {data}", response_time)
            except json.JSONDecodeError:
                self.log_test("Trial Registration", False, f"Invalid JSON response: {response.text[:100]}", response_time)
        else:
            error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
            if response:
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('detail', 'Unknown error')}"
                except:
                    pass
            self.log_test("Trial Registration", False, error_msg, response_time)
    
    async def test_database_connectivity(self):
        """Test 8: Database Connectivity"""
        print("\n🗄️ Testing Database Connectivity...")
        
        response, response_time = self.make_request("GET", "/test-db")
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                overall_status = data.get("overall_status", "Unknown")
                if "ALL TESTS PASSED" in overall_status:
                    self.log_test(
                        "Database Connectivity", 
                        True, 
                        f"Database fully operational - {overall_status}", 
                        response_time
                    )
                else:
                    self.log_test(
                        "Database Connectivity", 
                        False, 
                        f"Database issues detected - {overall_status}", 
                        response_time
                    )
            except json.JSONDecodeError:
                self.log_test("Database Connectivity", False, f"Invalid JSON response: {response.text[:100]}", response_time)
        else:
            error_msg = f"HTTP {response.status_code}" if response else "Connection failed"
            self.log_test("Database Connectivity", False, error_msg, response_time)
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        duration = datetime.now() - self.start_time
        
        print(f"\n" + "="*80)
        print(f"🎯 BACKEND COMPREHENSIVE TESTING COMPLETE")
        print(f"="*80)
        print(f"📊 OVERALL RESULTS:")
        print(f"   • Total Tests: {total_tests}")
        print(f"   • Passed: {passed_tests}")
        print(f"   • Failed: {failed_tests}")
        print(f"   • Success Rate: {success_rate:.1f}%")
        print(f"   • Duration: {duration.total_seconds():.1f} seconds")
        print(f"   • Backend URL: {BACKEND_URL}")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   • {result['test']}: {result['details']}")
        
        print(f"\n✅ SUCCESSFUL TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"   • {result['test']}: {result['details']}")
        
        # Performance Analysis
        response_times = [float(result["response_time"].replace("s", "")) for result in self.test_results if result["response_time"] != "0.000s"]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"   • Average Response Time: {avg_response_time:.3f}s")
            print(f"   • Fastest Response: {min_response_time:.3f}s")
            print(f"   • Slowest Response: {max_response_time:.3f}s")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "duration": duration.total_seconds(),
            "test_results": self.test_results
        }

async def main():
    """Main test execution"""
    print("🚀 Starting Backend Comprehensive Testing...")
    print(f"🎯 Target: {BACKEND_URL}")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = BackendTester()
    
    # Execute all tests
    await tester.test_health_endpoint()
    await tester.test_admin_authentication()
    await tester.test_auth_me_endpoint()
    await tester.test_contact_form_endpoints()
    await tester.test_core_api_endpoints()
    await tester.test_admin_endpoints()
    await tester.test_trial_registration()
    await tester.test_database_connectivity()
    
    # Generate final summary
    summary = tester.generate_summary()
    
    return summary

if __name__ == "__main__":
    try:
        summary = asyncio.run(main())
        
        # Exit with appropriate code
        if summary["failed_tests"] == 0:
            print(f"\n🎉 ALL TESTS PASSED! Backend is fully operational.")
            sys.exit(0)
        else:
            print(f"\n⚠️  {summary['failed_tests']} tests failed. Backend needs attention.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Testing failed with error: {e}")
        sys.exit(1)