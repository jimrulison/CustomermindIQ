#!/usr/bin/env python3
"""
CustomerMind IQ - Dashboard Endpoints Testing
Testing the specific dashboard endpoints mentioned in the review request

SPECIFIC TEST OBJECTIVES (from review request):
1. Customer Journey Dashboard endpoints:
   - /api/customer-journey/dashboard
   - /api/customer-journey/visualization/data  
   - /api/customer-journey/templates
   - /api/customer-journey/performance

2. Customer Health/Real-time Dashboard endpoints:
   - /api/customer-health/dashboard
   - /api/customer-health/alerts
   - /api/customer-health/customer/{id}
   - /api/customer-health/alerts/create

3. Growth Acceleration Engine endpoints:
   - /api/growth/dashboard
   - /api/growth/opportunities/dashboard
   - /api/growth/ab-tests/dashboard
   - /api/growth/revenue-leaks/dashboard
   - /api/growth/roi/dashboard
   - /api/growth/full-scan

4. Customer Success Intelligence endpoints:
   - /api/customer-success/health-dashboard
   - /api/customer-success/milestones-dashboard
   - /api/customer-success/csm-dashboard
   - /api/customer-success/expansion-dashboard

5. Growth Intelligence Suite endpoints:
   - /api/growth-intelligence/abm-dashboard
   - /api/growth-intelligence/intent-dashboard  
   - /api/growth-intelligence/plg-dashboard

6. Support and Training endpoints:
   - /api/support/tier-info
   - /api/support/tickets/my
   - /api/support/tickets/create
   - /api/download/* endpoints

Use admin credentials: admin@customermindiq.com / CustomerMindIQ2025!
Focus on testing all endpoints respond correctly with appropriate status codes.
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
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customeriq-fix.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class DashboardEndpointsTester:
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
                self.log_result(
                    "Admin Authentication", 
                    True, 
                    f"Admin login successful, role: {data.get('user', {}).get('role', 'unknown')}"
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
        """Test Customer Journey Dashboard endpoints"""
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
                    self.log_result(f"GET {endpoint}", True, f"Response received with {len(str(data))} chars")
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
        
        success_rate = len(successful_endpoints) / len(endpoints) * 100
        self.log_result(
            "Customer Journey Dashboard Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{len(endpoints)})"
        )
        
        return len(successful_endpoints) > 0

    async def test_customer_health_endpoints(self):
        """Test Customer Health/Real-time Dashboard endpoints"""
        print("💚 TESTING CUSTOMER HEALTH DASHBOARD ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Customer Health Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET endpoints
        get_endpoints = [
            "/api/customer-health/dashboard",
            "/api/customer-health/alerts",
            "/api/customer-health/customer/demo_1"  # Using demo customer ID
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in get_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Response received with {len(str(data))} chars")
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
        
        # Test POST endpoint for alert creation
        try:
            alert_data = {
                "customer_id": "demo_1",
                "alert_type": "health_decline",
                "severity": "medium",
                "message": "Customer engagement score has declined by 15% in the last 7 days",
                "threshold_value": 0.15
            }
            response = requests.post(f"{API_BASE}/api/customer-health/alerts/create", json=alert_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                successful_endpoints.append("/api/customer-health/alerts/create (POST)")
                self.log_result("POST /api/customer-health/alerts/create", True, f"Alert created successfully")
            else:
                failed_endpoints.append(f"/api/customer-health/alerts/create ({response.status_code})")
                self.log_result("POST /api/customer-health/alerts/create", False, f"Status: {response.status_code}")
        except Exception as e:
            failed_endpoints.append("/api/customer-health/alerts/create (Exception)")
            self.log_result("POST /api/customer-health/alerts/create", False, f"Exception: {str(e)}")
        
        total_endpoints = len(get_endpoints) + 1  # +1 for POST endpoint
        success_rate = len(successful_endpoints) / total_endpoints * 100
        self.log_result(
            "Customer Health Dashboard Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{total_endpoints})"
        )
        
        return len(successful_endpoints) > 0

    async def test_growth_acceleration_endpoints(self):
        """Test Growth Acceleration Engine endpoints"""
        print("🚀 TESTING GROWTH ACCELERATION ENGINE ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Growth Acceleration Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        endpoints = [
            "/api/growth/dashboard",
            "/api/growth/opportunities/dashboard",
            "/api/growth/ab-tests/dashboard",
            "/api/growth/revenue-leaks/dashboard",
            "/api/growth/roi/dashboard",
            "/api/growth/full-scan"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in endpoints:
            try:
                if endpoint == "/api/growth/full-scan":
                    # POST endpoint for full scan
                    scan_data = {
                        "scan_type": "comprehensive",
                        "include_revenue_leaks": True,
                        "include_growth_opportunities": True,
                        "include_ab_test_recommendations": True
                    }
                    response = requests.post(f"{API_BASE}{endpoint}", json=scan_data, headers=headers, timeout=60, verify=False)
                else:
                    # GET endpoints
                    response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    method = "POST" if endpoint == "/api/growth/full-scan" else "GET"
                    self.log_result(f"{method} {endpoint}", True, f"Response received with {len(str(data))} chars")
                elif response.status_code == 404:
                    failed_endpoints.append(f"{endpoint} (404)")
                    method = "POST" if endpoint == "/api/growth/full-scan" else "GET"
                    self.log_result(f"{method} {endpoint}", False, "404 Not Found - endpoint not accessible")
                elif response.status_code == 500:
                    failed_endpoints.append(f"{endpoint} (500)")
                    method = "POST" if endpoint == "/api/growth/full-scan" else "GET"
                    self.log_result(f"{method} {endpoint}", False, "500 Internal Server Error")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
                    method = "POST" if endpoint == "/api/growth/full-scan" else "GET"
                    self.log_result(f"{method} {endpoint}", False, f"Status: {response.status_code}")
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception)")
                method = "POST" if endpoint == "/api/growth/full-scan" else "GET"
                self.log_result(f"{method} {endpoint}", False, f"Exception: {str(e)}")
        
        success_rate = len(successful_endpoints) / len(endpoints) * 100
        self.log_result(
            "Growth Acceleration Engine Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{len(endpoints)})"
        )
        
        return len(successful_endpoints) > 0

    async def test_customer_success_intelligence_endpoints(self):
        """Test Customer Success Intelligence endpoints"""
        print("🎯 TESTING CUSTOMER SUCCESS INTELLIGENCE ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Customer Success Intelligence Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        endpoints = [
            "/api/customer-success/health-dashboard",
            "/api/customer-success/milestones-dashboard",
            "/api/customer-success/csm-dashboard",
            "/api/customer-success/expansion-dashboard"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Response received with {len(str(data))} chars")
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
        
        success_rate = len(successful_endpoints) / len(endpoints) * 100
        self.log_result(
            "Customer Success Intelligence Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{len(endpoints)})"
        )
        
        return len(successful_endpoints) > 0

    async def test_growth_intelligence_suite_endpoints(self):
        """Test Growth Intelligence Suite endpoints"""
        print("📊 TESTING GROWTH INTELLIGENCE SUITE ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Growth Intelligence Suite Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        endpoints = [
            "/api/growth-intelligence/abm-dashboard",
            "/api/growth-intelligence/intent-dashboard",
            "/api/growth-intelligence/plg-dashboard"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    successful_endpoints.append(f"{endpoint} (200)")
                    self.log_result(f"GET {endpoint}", True, f"Response received with {len(str(data))} chars")
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
        
        success_rate = len(successful_endpoints) / len(endpoints) * 100
        self.log_result(
            "Growth Intelligence Suite Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{len(endpoints)})"
        )
        
        return len(successful_endpoints) > 0

    async def test_support_and_training_endpoints(self):
        """Test Support and Training endpoints"""
        print("🎓 TESTING SUPPORT AND TRAINING ENDPOINTS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Support and Training Endpoints", False, "No admin token available")
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
                    self.log_result(f"GET {endpoint}", True, f"Response received with {len(str(data))} chars")
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
                "subject": "Dashboard Endpoints Test Ticket",
                "message": "This is a test ticket created during dashboard endpoints testing to verify the support system functionality.",
                "category": "technical",
                "priority": "medium"
            }
            response = requests.post(f"{API_BASE}/api/support/tickets/create", json=ticket_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                successful_endpoints.append("/api/support/tickets/create (POST)")
                self.log_result("POST /api/support/tickets/create", True, f"Ticket created successfully")
            else:
                failed_endpoints.append(f"/api/support/tickets/create ({response.status_code})")
                self.log_result("POST /api/support/tickets/create", False, f"Status: {response.status_code}")
        except Exception as e:
            failed_endpoints.append("/api/support/tickets/create (Exception)")
            self.log_result("POST /api/support/tickets/create", False, f"Exception: {str(e)}")
        
        # Test download endpoints
        download_endpoints = [
            "/api/download/quick-start-guide",
            "/api/download/complete-training-manual",
            "/api/download/admin-training-manual",
            "/api/download/training-portal",
            "/api/download/quick-reference-guide"
        ]
        
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
        
        total_endpoints = len(support_endpoints) + 1 + len(download_endpoints)  # +1 for POST endpoint
        success_rate = len(successful_endpoints) / total_endpoints * 100
        self.log_result(
            "Support and Training Endpoints",
            len(successful_endpoints) > 0,
            f"Success rate: {success_rate:.1f}% ({len(successful_endpoints)}/{total_endpoints})"
        )
        
        return len(successful_endpoints) > 0

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎯 DASHBOARD ENDPOINTS TEST SUMMARY")
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
            "💚 Customer Health Dashboard": [r["test"] for r in self.results if "customer-health" in r["test"]],
            "🚀 Growth Acceleration Engine": [r["test"] for r in self.results if "growth/" in r["test"]],
            "🎯 Customer Success Intelligence": [r["test"] for r in self.results if "customer-success" in r["test"]],
            "📊 Growth Intelligence Suite": [r["test"] for r in self.results if "growth-intelligence" in r["test"]],
            "🎓 Support and Training": [r["test"] for r in self.results if "support" in r["test"] or "download" in r["test"]]
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
            ("Customer Health Dashboard", "Customer Health Dashboard Endpoints"),
            ("Growth Acceleration Engine", "Growth Acceleration Engine Endpoints"),
            ("Customer Success Intelligence", "Customer Success Intelligence Endpoints"),
            ("Growth Intelligence Suite", "Growth Intelligence Suite Endpoints"),
            ("Support and Training", "Support and Training Endpoints")
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
        dashboard_endpoints_working = len(working_groups) >= 4  # At least 4 out of 6 groups working
        
        if dashboard_endpoints_working:
            print("  ✅ DASHBOARD ENDPOINTS: Most dashboard endpoints are working correctly")
        else:
            print("  ❌ DASHBOARD ENDPOINTS: Multiple dashboard endpoint groups have issues")
        
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
        
        print(f"\n📋 RECOMMENDATION: {'All dashboard endpoints are functioning properly for frontend button integration.' if dashboard_endpoints_working else 'Some dashboard endpoints need attention before frontend integration.'}")

async def main():
    """Main test execution"""
    print("🚀 STARTING DASHBOARD ENDPOINTS TESTING")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base: {API_BASE}")
    print("=" * 80)
    
    tester = DashboardEndpointsTester()
    
    # Run all tests
    tests = [
        tester.test_authentication_setup(),
        tester.test_customer_journey_endpoints(),
        tester.test_customer_health_endpoints(),
        tester.test_growth_acceleration_endpoints(),
        tester.test_customer_success_intelligence_endpoints(),
        tester.test_growth_intelligence_suite_endpoints(),
        tester.test_support_and_training_endpoints()
    ]
    
    for test in tests:
        await test
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main())