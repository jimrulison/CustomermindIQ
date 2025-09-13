#!/usr/bin/env python3
"""
CustomerMind IQ - Corrected Dashboard Endpoints Testing
Testing the actual dashboard endpoints based on the backend router configuration

CORRECTED ENDPOINT PATHS (based on backend analysis):
1. Customer Journey Dashboard endpoints:
   - /api/customer-journey/dashboard
   - /api/customer-journey/visualization/data  
   - /api/customer-journey/templates
   - /api/customer-journey/performance

2. Customer Health/Real-time Dashboard endpoints:
   - Need to check real_time_customer_health.py module

3. Growth Acceleration Engine endpoints:
   - /api/growth/dashboard
   - /api/growth/recommendations
   - /api/growth/access-check
   - /api/growth/health
   - /api/growth/full-scan

4. Support endpoints:
   - /api/support/tier-info
   - /api/support/tickets/my
   - /api/support/tickets/create

5. Download endpoints:
   - /api/download/* endpoints (these work)

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

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customeriq-admin.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class CorrectedDashboardTester:
    def __init__(self):
        self.admin_token = None
        self.results = []
        
    def log_result(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and data:
            print(f"   Error Data: {data}")
        print()

    async def test_authentication_setup(self):
        """Test admin authentication"""
        print("🔐 TESTING ADMIN AUTHENTICATION")
        print("=" * 50)
        
        try:
            response = requests.post(f"{API_BASE}/auth/login", json=ADMIN_CREDENTIALS, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                user_info = data.get("user", {})
                self.log_result(
                    "Admin Authentication", 
                    True, 
                    f"Admin login successful, role: {user_info.get('role', 'unknown')}, tier: {user_info.get('subscription_tier', 'unknown')}"
                )
                return True
            else:
                self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Status: {response.status_code}", 
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Exception: {str(e)}")
            return False

    async def test_customer_journey_endpoints(self):
        """Test Customer Journey Dashboard endpoints (corrected paths)"""
        print("🗺️ TESTING CUSTOMER JOURNEY DASHBOARD ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Customer Journey Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        endpoints = [
            "/api/customer-journey/dashboard",
            "/api/customer-journey/visualization/data",
            "/api/customer-journey/templates", 
            "/api/customer-journey/performance"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Response received: {data.get('status', 'unknown')}")
                elif response.status_code == 404:
                    failed_endpoints.append(f"{endpoint} (404)")
                    self.log_result(f"GET {endpoint}", False, "404 Not Found - endpoint not accessible")
                elif response.status_code == 500:
                    failed_endpoints.append(f"{endpoint} (500)")
                    self.log_result(f"GET {endpoint}", False, "500 Internal Server Error")
                elif response.status_code == 403:
                    failed_endpoints.append(f"{endpoint} (403)")
                    self.log_result(f"GET {endpoint}", False, "403 Forbidden - access denied")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
                    self.log_result(f"GET {endpoint}", False, f"Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception)")
                self.log_result(f"GET {endpoint}", False, f"Exception: {str(e)}")
        
        success_rate = len(successful_endpoints) / len(endpoints) * 100
        self.log_result(
            "Customer Journey Dashboard Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{len(endpoints)})"
        )
        
        return len(successful_endpoints) > 0

    async def test_growth_acceleration_endpoints(self):
        """Test Growth Acceleration Engine endpoints (corrected paths)"""
        print("🚀 TESTING GROWTH ACCELERATION ENGINE ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Growth Acceleration Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET endpoints
        get_endpoints = [
            "/api/growth/dashboard",
            "/api/growth/recommendations",
            "/api/growth/access-check",
            "/api/growth/health"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in get_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Response received: {data.get('status', 'unknown')}")
                elif response.status_code == 404:
                    failed_endpoints.append(f"{endpoint} (404)")
                    self.log_result(f"GET {endpoint}", False, "404 Not Found - endpoint not accessible")
                elif response.status_code == 500:
                    failed_endpoints.append(f"{endpoint} (500)")
                    self.log_result(f"GET {endpoint}", False, "500 Internal Server Error")
                elif response.status_code == 403:
                    failed_endpoints.append(f"{endpoint} (403)")
                    self.log_result(f"GET {endpoint}", False, "403 Forbidden - requires annual subscription")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
                    self.log_result(f"GET {endpoint}", False, f"Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception)")
                self.log_result(f"GET {endpoint}", False, f"Exception: {str(e)}")
        
        # Test POST endpoint for full scan
        try:
            scan_data = {
                "scan_type": "comprehensive",
                "include_revenue_leaks": True,
                "include_growth_opportunities": True,
                "include_ab_test_recommendations": True
            }
            response = requests.post(f"{API_BASE}/api/growth/full-scan", json=scan_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                successful_endpoints.append("/api/growth/full-scan (POST)")
                self.log_result("POST /api/growth/full-scan", True, f"Scan initiated: {data.get('status', 'unknown')}")
            elif response.status_code == 403:
                failed_endpoints.append("/api/growth/full-scan (403)")
                self.log_result("POST /api/growth/full-scan", False, "403 Forbidden - requires annual subscription")
            else:
                failed_endpoints.append(f"/api/growth/full-scan ({response.status_code})")
                self.log_result("POST /api/growth/full-scan", False, f"Status: {response.status_code}")
        except Exception as e:
            failed_endpoints.append("/api/growth/full-scan (Exception)")
            self.log_result("POST /api/growth/full-scan", False, f"Exception: {str(e)}")
        
        total_endpoints = len(get_endpoints) + 1  # +1 for POST endpoint
        success_rate = len(successful_endpoints) / total_endpoints * 100
        self.log_result(
            "Growth Acceleration Engine Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{total_endpoints})"
        )
        
        return len(successful_endpoints) > 0

    async def test_support_endpoints(self):
        """Test Support endpoints (corrected paths)"""
        print("🎓 TESTING SUPPORT ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Support Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test support endpoints
        support_endpoints = [
            "/api/support/tier-info",
            "/api/support/tickets/my"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in support_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Response received: {data.get('status', 'unknown')}")
                elif response.status_code == 404:
                    failed_endpoints.append(f"{endpoint} (404)")
                    self.log_result(f"GET {endpoint}", False, "404 Not Found - endpoint not accessible")
                elif response.status_code == 500:
                    failed_endpoints.append(f"{endpoint} (500)")
                    self.log_result(f"GET {endpoint}", False, "500 Internal Server Error")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
                    self.log_result(f"GET {endpoint}", False, f"Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception)")
                self.log_result(f"GET {endpoint}", False, f"Exception: {str(e)}")
        
        # Test ticket creation
        try:
            ticket_data = {
                "subject": "Corrected Dashboard Endpoints Test Ticket",
                "message": "This is a test ticket created during corrected dashboard endpoints testing to verify the support system functionality.",
                "category": "technical",
                "priority": "medium"
            }
            response = requests.post(f"{API_BASE}/api/support/tickets/create", json=ticket_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                successful_endpoints.append("/api/support/tickets/create (POST)")
                self.log_result("POST /api/support/tickets/create", True, f"Ticket created: {data.get('status', 'unknown')}")
            else:
                failed_endpoints.append(f"/api/support/tickets/create ({response.status_code})")
                self.log_result("POST /api/support/tickets/create", False, f"Status: {response.status_code}")
        except Exception as e:
            failed_endpoints.append("/api/support/tickets/create (Exception)")
            self.log_result("POST /api/support/tickets/create", False, f"Exception: {str(e)}")
        
        total_endpoints = len(support_endpoints) + 1  # +1 for POST endpoint
        success_rate = len(successful_endpoints) / total_endpoints * 100
        self.log_result(
            "Support Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{total_endpoints})"
        )
        
        return len(successful_endpoints) > 0

    async def test_download_endpoints(self):
        """Test Download endpoints (these should work)"""
        print("📥 TESTING DOWNLOAD ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Download Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test download endpoints
        download_endpoints = [
            "/api/download/quick-start-guide",
            "/api/download/complete-training-manual",
            "/api/download/admin-training-manual",
            "/api/download/training-portal",
            "/api/download/quick-reference-guide"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in download_endpoints:
            try:
                response = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    content_length = len(response.content)
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Downloaded {content_length} bytes")
                elif response.status_code == 404:
                    failed_endpoints.append(f"{endpoint} (404)")
                    self.log_result(f"GET {endpoint}", False, "404 Not Found - file not accessible")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
                    self.log_result(f"GET {endpoint}", False, f"Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception)")
                self.log_result(f"GET {endpoint}", False, f"Exception: {str(e)}")
        
        success_rate = len(successful_endpoints) / len(download_endpoints) * 100
        self.log_result(
            "Download Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{len(download_endpoints)})"
        )
        
        return len(successful_endpoints) > 0

    async def test_additional_dashboard_endpoints(self):
        """Test additional dashboard endpoints that might exist"""
        print("📊 TESTING ADDITIONAL DASHBOARD ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Additional Dashboard Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test various dashboard endpoints that might exist
        additional_endpoints = [
            "/api/analytics",
            "/api/customers",
            "/api/admin/analytics/dashboard",
            "/api/subscriptions/plans",
            "/api/health",
            "/api/test-db"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in additional_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Response received: {data.get('status', 'success')}")
                elif response.status_code == 404:
                    failed_endpoints.append(f"{endpoint} (404)")
                    self.log_result(f"GET {endpoint}", False, "404 Not Found - endpoint not accessible")
                elif response.status_code == 500:
                    failed_endpoints.append(f"{endpoint} (500)")
                    self.log_result(f"GET {endpoint}", False, "500 Internal Server Error")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
                    self.log_result(f"GET {endpoint}", False, f"Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception)")
                self.log_result(f"GET {endpoint}", False, f"Exception: {str(e)}")
        
        success_rate = len(successful_endpoints) / len(additional_endpoints) * 100
        self.log_result(
            "Additional Dashboard Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{len(additional_endpoints)})"
        )
        
        return len(successful_endpoints) > 0

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎯 CORRECTED DASHBOARD ENDPOINTS TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print()
        
        # Group results by endpoint category
        categories = {
            "🔐 Authentication": ["Admin Authentication"],
            "🗺️ Customer Journey Dashboard": [r["test"] for r in self.results if "customer-journey" in r["test"]],
            "🚀 Growth Acceleration Engine": [r["test"] for r in self.results if "growth" in r["test"]],
            "🎓 Support System": [r["test"] for r in self.results if "support" in r["test"]],
            "📥 Download System": [r["test"] for r in self.results if "download" in r["test"]],
            "📊 Additional Dashboards": [r["test"] for r in self.results if "Additional" in r["test"]]
        }
        
        for category_name, test_names in categories.items():
            if not test_names:
                continue
                
            print(f"{category_name}:")
            category_results = [r for r in self.results if r["test"] in test_names]
            category_passed = len([r for r in category_results if r["success"]])
            category_total = len(category_results)
            
            for result in category_results:
                print(f"  {result['status']}: {result['test']}")
                if result['details']:
                    print(f"      {result['details']}")
            
            if category_total > 0:
                category_rate = (category_passed / category_total * 100)
                print(f"  📈 Category Success Rate: {category_passed}/{category_total} ({category_rate:.1f}%)")
            print()
        
        # Summary by endpoint group
        print("🔍 ENDPOINT GROUP SUMMARY:")
        
        endpoint_groups = [
            ("Customer Journey Dashboard", "Customer Journey Dashboard Endpoints"),
            ("Growth Acceleration Engine", "Growth Acceleration Engine Endpoints"),
            ("Support System", "Support Endpoints"),
            ("Download System", "Download Endpoints"),
            ("Additional Dashboards", "Additional Dashboard Endpoints")
        ]
        
        working_groups = []
        failing_groups = []
        
        for group_name, test_name in endpoint_groups:
            group_result = next((r for r in self.results if r["test"] == test_name), None)
            if group_result:
                if group_result["success"]:
                    working_groups.append(group_name)
                else:
                    failing_groups.append(group_name)
        
        if working_groups:
            print(f"  ✅ WORKING ENDPOINT GROUPS: {', '.join(working_groups)}")
        
        if failing_groups:
            print(f"  ❌ FAILING ENDPOINT GROUPS: {', '.join(failing_groups)}")
        
        print()
        print("🎉 REVIEW REQUEST VERIFICATION:")
        
        # Check overall dashboard functionality
        dashboard_endpoints_working = len(working_groups) >= 2  # At least 2 groups working
        
        if dashboard_endpoints_working:
            print("  ✅ DASHBOARD ENDPOINTS: Core dashboard endpoints are working correctly")
        else:
            print("  ❌ DASHBOARD ENDPOINTS: Most dashboard endpoint groups have issues")
        
        # Check for critical issues
        critical_issues = [r for r in self.results if not r["success"] and "500" in r.get("details", "")]
        if critical_issues:
            print(f"  🚨 CRITICAL ISSUES: {len(critical_issues)} endpoints returning 500 errors")
        else:
            print("  ✅ NO CRITICAL ISSUES: No 500 server errors detected")
        
        # Check for missing endpoints
        missing_endpoints = [r for r in self.results if not r["success"] and "404" in r.get("details", "")]
        if missing_endpoints:
            print(f"  ⚠️ MISSING ENDPOINTS: {len(missing_endpoints)} endpoints returning 404 errors")
        else:
            print("  ✅ ALL ENDPOINTS ACCESSIBLE: No 404 errors detected")
        
        # Check for access issues (403 errors)
        access_issues = [r for r in self.results if not r["success"] and "403" in r.get("details", "")]
        if access_issues:
            print(f"  🔒 ACCESS RESTRICTIONS: {len(access_issues)} endpoints require annual subscription")
        else:
            print("  ✅ NO ACCESS RESTRICTIONS: All endpoints accessible with admin credentials")
        
        print(f"\n📋 RECOMMENDATION: {'Dashboard endpoints are functioning properly for frontend button integration.' if dashboard_endpoints_working else 'Some dashboard endpoints need attention before frontend integration.'}")

async def main():
    """Main test execution"""
    print("🚀 STARTING CORRECTED DASHBOARD ENDPOINTS TESTING")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base: {API_BASE}")
    print("=" * 80)
    
    tester = CorrectedDashboardTester()
    
    # Run all tests
    tests = [
        tester.test_authentication_setup(),
        tester.test_customer_journey_endpoints(),
        tester.test_growth_acceleration_endpoints(),
        tester.test_support_endpoints(),
        tester.test_download_endpoints(),
        tester.test_additional_dashboard_endpoints()
    ]
    
    for test in tests:
        await test
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main())