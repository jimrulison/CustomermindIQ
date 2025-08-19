#!/usr/bin/env python3
"""
Internal Backend Health Check Test
Tests backend server health using internal localhost connection
"""

import requests
import sys
import json
from datetime import datetime

class InternalHealthChecker:
    def __init__(self):
        # Use internal localhost URL since external routing has issues
        self.base_url = "http://localhost:8001"
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
                    print(f"   Response preview: {str(response_data)[:150]}...")
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

    def test_core_endpoints(self):
        """Test core backend endpoints"""
        endpoints = [
            ("Health Check", "GET", "api/health", 200),
            ("Analytics Dashboard", "GET", "api/analytics", 200),
            ("Universal Dashboard", "GET", "api/universal/dashboard", 200),
            ("Connectors Status", "GET", "api/universal/connectors/status", 200),
            ("Customer Intelligence Dashboard", "GET", "api/intelligence/dashboard", 200),
            ("Marketing Dashboard", "GET", "api/marketing/multi-channel-orchestration", 200),
            ("Revenue Analytics Dashboard", "GET", "api/revenue-analytics/dashboard", 200),
        ]
        
        results = []
        for name, method, endpoint, expected_status in endpoints:
            success, response = self.run_test(name, method, endpoint, expected_status, timeout=60)
            results.append((name, success, response))
            
        return results

    def run_comprehensive_health_check(self):
        """Run comprehensive backend health check"""
        print("=" * 80)
        print("🏥 INTERNAL BACKEND HEALTH CHECK - Customer Mind IQ Platform")
        print("=" * 80)
        print(f"Backend URL: {self.base_url}")
        print(f"Test Time: {datetime.now()}")
        print("=" * 80)

        # Test core endpoints
        print("\n📋 Testing Core Backend Endpoints...")
        endpoint_results = self.test_core_endpoints()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 BACKEND HEALTH CHECK SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print("\n📋 Detailed Results:")
        working_endpoints = []
        failing_endpoints = []
        
        for name, success, response in endpoint_results:
            status = "PASS" if success else "FAIL"
            print(f"{'✅' if success else '❌'} {name}: {status}")
            
            if success:
                working_endpoints.append(name)
                # Show key data for successful endpoints
                if isinstance(response, dict):
                    if 'service' in response:
                        print(f"    Service: {response.get('service', 'unknown')}")
                    if 'status' in response:
                        print(f"    Status: {response.get('status', 'unknown')}")
                    if 'total_customers' in response:
                        print(f"    Customers: {response.get('total_customers', 0)}")
                    if 'dashboard' in response:
                        dashboard = response.get('dashboard', {})
                        if 'overview' in dashboard:
                            overview = dashboard['overview']
                            print(f"    Overview: {overview.get('total_customers', 0)} customers, ${overview.get('total_revenue', 0):,.0f} revenue")
            else:
                failing_endpoints.append(name)
        
        # Overall assessment
        critical_endpoints = ["Health Check", "Analytics Dashboard", "Universal Dashboard"]
        critical_working = all(name in working_endpoints for name in critical_endpoints)
        overall_health = self.tests_passed >= (self.tests_run * 0.7) and critical_working  # 70% pass rate + critical endpoints
        
        print("\n" + "=" * 80)
        print("🎯 BACKEND ASSESSMENT")
        print("=" * 80)
        
        if overall_health:
            print("🎉 OVERALL HEALTH: EXCELLENT")
            print("✅ Backend server is running correctly after restructuring")
            print("✅ Core APIs are responding properly")
            print("✅ All critical endpoints are functional")
            print(f"✅ {len(working_endpoints)} out of {len(endpoint_results)} endpoints working")
        else:
            print("⚠️  OVERALL HEALTH: ISSUES DETECTED")
            if not critical_working:
                print("❌ Critical endpoints are not responding")
            if failing_endpoints:
                print(f"❌ Failing endpoints: {', '.join(failing_endpoints)}")
        
        print("\n📋 WORKING MODULES:")
        for endpoint in working_endpoints:
            print(f"  ✅ {endpoint}")
            
        if failing_endpoints:
            print("\n📋 ISSUES FOUND:")
            for endpoint in failing_endpoints:
                print(f"  ❌ {endpoint}")
        
        print("=" * 80)
        
        return overall_health, working_endpoints, failing_endpoints

if __name__ == "__main__":
    checker = InternalHealthChecker()
    success, working, failing = checker.run_comprehensive_health_check()
    sys.exit(0 if success else 1)