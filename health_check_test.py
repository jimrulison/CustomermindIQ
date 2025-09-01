#!/usr/bin/env python3
"""
Backend Health Check Test
Simple health check to verify backend server is running correctly after restructuring
"""

import requests
import sys
import json
from datetime import datetime
import time

class BackendHealthChecker:
    def __init__(self):
        # Use the actual backend URL from frontend .env
        self.base_url = "https://mind-iq-dashboard.preview.emergentagent.com"
        self.tests_run = 0
        self.tests_passed = 0
        
    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a basic API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test basic API health check"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Version: {response.get('version', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
        
        return success

    def test_basic_endpoints(self):
        """Test a few core endpoints to verify basic functionality"""
        endpoints_to_test = [
            ("Analytics Dashboard", "GET", "api/analytics", 200),
            ("Universal Dashboard", "GET", "api/universal/dashboard", 200),
            ("Connectors Status", "GET", "api/universal/connectors/status", 200),
        ]
        
        results = []
        for name, method, endpoint, expected_status in endpoints_to_test:
            success, response = self.run_test(name, method, endpoint, expected_status, timeout=45)
            results.append((name, success))
            
        return results

    def run_health_check(self):
        """Run comprehensive health check"""
        print("=" * 80)
        print("🏥 BACKEND HEALTH CHECK - Customer Mind IQ Platform")
        print("=" * 80)
        print(f"Backend URL: {self.base_url}")
        print(f"Test Time: {datetime.now()}")
        print("=" * 80)

        # Test 1: Basic Health Check
        print("\n📋 STEP 1: Basic Health Check")
        health_ok = self.test_health_check()
        
        if not health_ok:
            print("\n❌ CRITICAL: Health check failed - backend may not be running")
            return False

        # Test 2: Core Endpoints
        print("\n📋 STEP 2: Core Endpoints Verification")
        endpoint_results = self.test_basic_endpoints()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print("\n📋 Endpoint Results:")
        print(f"✅ Health Check: {'PASS' if health_ok else 'FAIL'}")
        for name, success in endpoint_results:
            print(f"{'✅' if success else '❌'} {name}: {'PASS' if success else 'FAIL'}")
        
        # Overall assessment
        overall_health = self.tests_passed >= (self.tests_run * 0.75)  # 75% pass rate
        
        print("\n" + "=" * 80)
        if overall_health:
            print("🎉 OVERALL HEALTH: GOOD - Backend is responding correctly")
            print("✅ Server is running and core APIs are accessible")
        else:
            print("⚠️  OVERALL HEALTH: ISSUES DETECTED")
            print("❌ Some core endpoints are not responding correctly")
        
        print("=" * 80)
        
        return overall_health

if __name__ == "__main__":
    checker = BackendHealthChecker()
    success = checker.run_health_check()
    sys.exit(0 if success else 1)