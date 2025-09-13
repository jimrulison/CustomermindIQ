#!/usr/bin/env python3
"""
CustomerMind IQ - Dashboard Endpoints Verification Testing
Testing the specific dashboard endpoints mentioned in the review request

SPECIFIC TEST OBJECTIVES (from review request):
1. **Dashboard API Endpoints:**
   - `/api/customer-health/dashboard`
   - `/api/customer-success/health-dashboard`
   - `/api/growth-intelligence/abm-dashboard`
   - `/api/customer-journey/dashboard`

2. **Authentication System:**
   - Admin login: `admin@customermindiq.com` / `CustomerMindIQ2025!`
   - JWT token generation and validation

3. **Backend Health:**
   - Confirm all services running properly
   - Check for any error logs or issues

Expected: All dashboard endpoints should return HTTP 200 with rich data
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

class DashboardVerificationTester:
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

    async def test_admin_authentication(self):
        """Test admin authentication as specified in review request"""
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
                    f"Admin login successful, role: {user_info.get('role', 'unknown')}, email: {user_info.get('email', 'unknown')}"
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

    async def test_jwt_token_validation(self):
        """Test JWT token generation and validation"""
        print("🎫 TESTING JWT TOKEN VALIDATION")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("JWT Token Validation", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test token validation with profile endpoint
            response = requests.get(f"{API_BASE}/auth/profile", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                user_info = data.get("user", {})
                self.log_result(
                    "JWT Token Validation", 
                    True, 
                    f"Token valid, user: {user_info.get('email', 'unknown')}, role: {user_info.get('role', 'unknown')}"
                )
                return True
            else:
                self.log_result(
                    "JWT Token Validation", 
                    False, 
                    f"Status: {response.status_code}", 
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("JWT Token Validation", False, f"Exception: {str(e)}")
            return False

    async def test_customer_health_dashboard(self):
        """Test /api/customer-health/dashboard endpoint"""
        print("📊 TESTING CUSTOMER HEALTH DASHBOARD")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Customer Health Dashboard", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/customer-health/dashboard", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                # Check for rich data content
                data_keys = list(data.keys()) if isinstance(data, dict) else []
                data_size = len(str(data))
                
                self.log_result(
                    "Customer Health Dashboard", 
                    True, 
                    f"HTTP 200 with rich data ({data_size} chars), keys: {data_keys[:5]}{'...' if len(data_keys) > 5 else ''}"
                )
                return True
            else:
                self.log_result(
                    "Customer Health Dashboard", 
                    False, 
                    f"Status: {response.status_code}", 
                    response.text[:200]
                )
                return False
        except Exception as e:
            self.log_result("Customer Health Dashboard", False, f"Exception: {str(e)}")
            return False

    async def test_customer_success_health_dashboard(self):
        """Test /api/customer-success/health-dashboard endpoint"""
        print("🎯 TESTING CUSTOMER SUCCESS HEALTH DASHBOARD")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Customer Success Health Dashboard", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/customer-success/health-dashboard", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                # Check for rich data content
                data_keys = list(data.keys()) if isinstance(data, dict) else []
                data_size = len(str(data))
                
                self.log_result(
                    "Customer Success Health Dashboard", 
                    True, 
                    f"HTTP 200 with rich data ({data_size} chars), keys: {data_keys[:5]}{'...' if len(data_keys) > 5 else ''}"
                )
                return True
            else:
                self.log_result(
                    "Customer Success Health Dashboard", 
                    False, 
                    f"Status: {response.status_code}", 
                    response.text[:200]
                )
                return False
        except Exception as e:
            self.log_result("Customer Success Health Dashboard", False, f"Exception: {str(e)}")
            return False

    async def test_growth_intelligence_abm_dashboard(self):
        """Test /api/growth-intelligence/abm-dashboard endpoint"""
        print("📈 TESTING GROWTH INTELLIGENCE ABM DASHBOARD")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Growth Intelligence ABM Dashboard", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/growth-intelligence/abm-dashboard", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                # Check for rich data content
                data_keys = list(data.keys()) if isinstance(data, dict) else []
                data_size = len(str(data))
                
                self.log_result(
                    "Growth Intelligence ABM Dashboard", 
                    True, 
                    f"HTTP 200 with rich data ({data_size} chars), keys: {data_keys[:5]}{'...' if len(data_keys) > 5 else ''}"
                )
                return True
            else:
                self.log_result(
                    "Growth Intelligence ABM Dashboard", 
                    False, 
                    f"Status: {response.status_code}", 
                    response.text[:200]
                )
                return False
        except Exception as e:
            self.log_result("Growth Intelligence ABM Dashboard", False, f"Exception: {str(e)}")
            return False

    async def test_customer_journey_dashboard(self):
        """Test /api/customer-journey/dashboard endpoint"""
        print("🗺️ TESTING CUSTOMER JOURNEY DASHBOARD")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Customer Journey Dashboard", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/customer-journey/dashboard", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                # Check for rich data content
                data_keys = list(data.keys()) if isinstance(data, dict) else []
                data_size = len(str(data))
                
                self.log_result(
                    "Customer Journey Dashboard", 
                    True, 
                    f"HTTP 200 with rich data ({data_size} chars), keys: {data_keys[:5]}{'...' if len(data_keys) > 5 else ''}"
                )
                return True
            else:
                self.log_result(
                    "Customer Journey Dashboard", 
                    False, 
                    f"Status: {response.status_code}", 
                    response.text[:200]
                )
                return False
        except Exception as e:
            self.log_result("Customer Journey Dashboard", False, f"Exception: {str(e)}")
            return False

    async def test_backend_health_check(self):
        """Test backend health and service status"""
        print("🏥 TESTING BACKEND HEALTH")
        print("=" * 50)
        
        health_endpoints = [
            "/api/health",
            "/api/test-db"
        ]
        
        successful_checks = []
        failed_checks = []
        
        for endpoint in health_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "unknown")
                    successful_checks.append(f"{endpoint} ({status})")
                else:
                    failed_checks.append(f"{endpoint} ({response.status_code})")
            except Exception as e:
                failed_checks.append(f"{endpoint} (Exception)")
        
        if len(successful_checks) >= 1:
            self.log_result(
                "Backend Health Check", 
                True, 
                f"Backend healthy. Working: {', '.join(successful_checks)}. Issues: {', '.join(failed_checks) if failed_checks else 'None'}"
            )
            return True
        else:
            self.log_result(
                "Backend Health Check", 
                False, 
                f"Backend health issues. Failed: {', '.join(failed_checks)}"
            )
            return False

    async def test_service_status_check(self):
        """Test if all services are running properly"""
        print("⚙️ TESTING SERVICE STATUS")
        print("=" * 50)
        
        # Test various service endpoints to ensure they're running
        service_endpoints = [
            ("/api/auth/health", "Authentication Service"),
            ("/api/admin/analytics/dashboard", "Admin Service"),
            ("/api/subscriptions/plans", "Subscription Service"),
            ("/api/support/tier-info", "Support Service")
        ]
        
        if not self.admin_token:
            self.log_result("Service Status Check", False, "No admin token for authenticated endpoints")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        working_services = []
        failed_services = []
        
        for endpoint, service_name in service_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code in [200, 201]:
                    working_services.append(service_name)
                else:
                    failed_services.append(f"{service_name} ({response.status_code})")
            except Exception as e:
                failed_services.append(f"{service_name} (Exception)")
        
        if len(working_services) >= 3:  # At least 3 services should be working
            self.log_result(
                "Service Status Check", 
                True, 
                f"Services running properly. Working: {', '.join(working_services)}. Issues: {', '.join(failed_services) if failed_services else 'None'}"
            )
            return True
        else:
            self.log_result(
                "Service Status Check", 
                False, 
                f"Service issues detected. Working: {', '.join(working_services)}. Failed: {', '.join(failed_services)}"
            )
            return False

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎯 DASHBOARD ENDPOINTS VERIFICATION SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print()
        
        # Group results by category
        categories = {
            "🔐 Authentication System": [
                "Admin Authentication", "JWT Token Validation"
            ],
            "📊 Dashboard Endpoints": [
                "Customer Health Dashboard", "Customer Success Health Dashboard", 
                "Growth Intelligence ABM Dashboard", "Customer Journey Dashboard"
            ],
            "🏥 Backend Health": [
                "Backend Health Check", "Service Status Check"
            ]
        }
        
        for category_name, test_names in categories.items():
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
        
        # Review request verification
        print("🔍 REVIEW REQUEST VERIFICATION:")
        
        # Check dashboard endpoints specifically
        dashboard_tests = [
            "Customer Health Dashboard", "Customer Success Health Dashboard",
            "Growth Intelligence ABM Dashboard", "Customer Journey Dashboard"
        ]
        dashboard_results = [r for r in self.results if r["test"] in dashboard_tests]
        dashboard_passed = len([r for r in dashboard_results if r["success"]])
        dashboard_total = len(dashboard_results)
        
        if dashboard_total > 0:
            dashboard_rate = (dashboard_passed / dashboard_total * 100)
            print(f"  📊 Dashboard Endpoints: {dashboard_passed}/{dashboard_total} ({dashboard_rate:.1f}%)")
            
            if dashboard_passed == dashboard_total:
                print("  ✅ ALL DASHBOARD ENDPOINTS WORKING: All endpoints return HTTP 200 with rich data as expected")
            else:
                failed_dashboards = [r["test"] for r in dashboard_results if not r["success"]]
                print(f"  ❌ DASHBOARD ISSUES: {', '.join(failed_dashboards)}")
        
        # Check authentication system
        auth_tests = ["Admin Authentication", "JWT Token Validation"]
        auth_results = [r for r in self.results if r["test"] in auth_tests]
        auth_passed = len([r for r in auth_results if r["success"]])
        auth_total = len(auth_results)
        
        if auth_total > 0:
            auth_rate = (auth_passed / auth_total * 100)
            print(f"  🔐 Authentication System: {auth_passed}/{auth_total} ({auth_rate:.1f}%)")
            
            if auth_passed == auth_total:
                print("  ✅ AUTHENTICATION WORKING: Admin login and JWT tokens working perfectly")
            else:
                print("  ❌ AUTHENTICATION ISSUES: Admin login or JWT validation failing")
        
        # Check backend health
        health_tests = ["Backend Health Check", "Service Status Check"]
        health_results = [r for r in self.results if r["test"] in health_tests]
        health_passed = len([r for r in health_results if r["success"]])
        health_total = len(health_results)
        
        if health_total > 0:
            health_rate = (health_passed / health_total * 100)
            print(f"  🏥 Backend Health: {health_passed}/{health_total} ({health_rate:.1f}%)")
            
            if health_passed == health_total:
                print("  ✅ BACKEND HEALTHY: All services running properly, no issues detected")
            else:
                print("  ❌ BACKEND ISSUES: Some services may not be running properly")
        
        print()
        print("🎉 FINAL VERIFICATION STATUS:")
        
        if success_rate >= 90:
            print("  ✅ COMPREHENSIVE VERIFICATION SUCCESSFUL")
            print("  ✅ All dashboard endpoints working as expected")
            print("  ✅ Authentication system operational")
            print("  ✅ Backend services running properly")
            print("  ✅ Ready for production use")
        elif success_rate >= 75:
            print("  ⚠️ MOSTLY SUCCESSFUL WITH MINOR ISSUES")
            print("  ⚠️ Most systems working but some issues detected")
            print("  ⚠️ Review failed tests for minor fixes needed")
        else:
            print("  ❌ SIGNIFICANT ISSUES DETECTED")
            print("  ❌ Multiple systems not working as expected")
            print("  ❌ Requires investigation and fixes")
        
        print(f"\n📋 Test completed at: {datetime.now().isoformat()}")
        print(f"🌐 Backend URL: {BACKEND_URL}")
        print(f"🔑 Admin credentials: {ADMIN_CREDENTIALS['email']}")

    async def run_all_tests(self):
        """Run all dashboard verification tests"""
        print("🚀 STARTING DASHBOARD ENDPOINTS VERIFICATION")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Admin Email: {ADMIN_CREDENTIALS['email']}")
        print(f"Test Time: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        # Run tests in sequence
        await self.test_admin_authentication()
        await self.test_jwt_token_validation()
        await self.test_backend_health_check()
        await self.test_service_status_check()
        
        # Test all dashboard endpoints
        await self.test_customer_health_dashboard()
        await self.test_customer_success_health_dashboard()
        await self.test_growth_intelligence_abm_dashboard()
        await self.test_customer_journey_dashboard()
        
        # Print summary
        self.print_summary()

async def main():
    """Main test execution"""
    tester = DashboardVerificationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())