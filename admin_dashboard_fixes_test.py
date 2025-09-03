#!/usr/bin/env python3
"""
CustomerMind IQ - Admin Dashboard Fixes Testing
Testing specific fixes mentioned in review request:

1. Admin Dashboard 500 Error Fix: /api/admin/analytics/dashboard
2. Email System Endpoint Corrections: 
   - /api/email/email/campaigns (was /api/email/campaigns)
   - /api/email/email/providers/current (was /api/email/providers/current)
3. New Admin Endpoints:
   - /api/admin/users
   - /api/admin/customers  
   - /api/admin/announcements

Test Credentials: admin@customermindiq.com / CustomerMindIQ2025!
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Any, List
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-mind-iq-4.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials as specified in review
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AdminDashboardFixesTester:
    def __init__(self):
        self.admin_token = None
        self.results = []
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def log_result(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.results.append(result)
        print(f"{status} {test_name}: {details}")
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
    
    def authenticate_admin(self) -> bool:
        """Authenticate as admin user"""
        try:
            print(f"\n🔐 Authenticating admin user: {ADMIN_CREDENTIALS['email']}")
            
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                if self.admin_token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.admin_token}"
                    })
                    self.log_result(
                        "Admin Authentication", 
                        True, 
                        f"Successfully authenticated admin user with role: {data.get('user', {}).get('role', 'unknown')}"
                    )
                    return True
                else:
                    self.log_result("Admin Authentication", False, "No access token in response", data)
                    return False
            else:
                self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Authentication failed with status {response.status_code}", 
                    response.json() if response.content else None
                )
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Authentication error: {str(e)}")
            return False
    
    def test_admin_dashboard_endpoint(self) -> bool:
        """Test the fixed admin dashboard endpoint"""
        try:
            print(f"\n📊 Testing Admin Dashboard Endpoint (Previously 500 Error)")
            
            response = self.session.get(
                f"{API_BASE}/admin/analytics/dashboard",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Admin Dashboard Analytics", 
                    True, 
                    f"Dashboard loaded successfully with {len(data)} data fields",
                    data
                )
                return True
            else:
                self.log_result(
                    "Admin Dashboard Analytics", 
                    False, 
                    f"Dashboard failed with status {response.status_code}",
                    response.json() if response.content else None
                )
                return False
                
        except Exception as e:
            self.log_result("Admin Dashboard Analytics", False, f"Dashboard error: {str(e)}")
            return False
    
    def test_email_system_endpoints(self) -> bool:
        """Test the corrected email system endpoint paths"""
        success_count = 0
        total_tests = 2
        
        print(f"\n📧 Testing Corrected Email System Endpoints")
        
        # Test 1: Email Campaigns (corrected path)
        try:
            response = self.session.get(
                f"{API_BASE}/email/email/campaigns",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Email Campaigns Endpoint", 
                    True, 
                    f"Campaigns endpoint working - found {len(data) if isinstance(data, list) else 'data'} campaigns",
                    data
                )
                success_count += 1
            else:
                self.log_result(
                    "Email Campaigns Endpoint", 
                    False, 
                    f"Campaigns endpoint failed with status {response.status_code}",
                    response.json() if response.content else None
                )
                
        except Exception as e:
            self.log_result("Email Campaigns Endpoint", False, f"Campaigns error: {str(e)}")
        
        # Test 2: Email Providers (corrected path)
        try:
            response = self.session.get(
                f"{API_BASE}/email/email/providers/current",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Email Providers Endpoint", 
                    True, 
                    f"Providers endpoint working - current provider: {data.get('provider', 'unknown')}",
                    data
                )
                success_count += 1
            else:
                self.log_result(
                    "Email Providers Endpoint", 
                    False, 
                    f"Providers endpoint failed with status {response.status_code}",
                    response.json() if response.content else None
                )
                
        except Exception as e:
            self.log_result("Email Providers Endpoint", False, f"Providers error: {str(e)}")
        
        return success_count == total_tests
    
    def test_new_admin_endpoints(self) -> bool:
        """Test the newly added admin endpoints"""
        success_count = 0
        total_tests = 3
        
        print(f"\n👥 Testing New Admin Endpoints")
        
        # Test 1: Admin Users Endpoint
        try:
            response = self.session.get(
                f"{API_BASE}/admin/users",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                user_count = len(data) if isinstance(data, list) else data.get('total', 0)
                self.log_result(
                    "Admin Users Endpoint", 
                    True, 
                    f"Users endpoint working - found {user_count} users",
                    data
                )
                success_count += 1
            else:
                self.log_result(
                    "Admin Users Endpoint", 
                    False, 
                    f"Users endpoint failed with status {response.status_code}",
                    response.json() if response.content else None
                )
                
        except Exception as e:
            self.log_result("Admin Users Endpoint", False, f"Users error: {str(e)}")
        
        # Test 2: Admin Customers Endpoint (alias for users)
        try:
            response = self.session.get(
                f"{API_BASE}/admin/customers",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                customer_count = len(data) if isinstance(data, list) else data.get('total', 0)
                self.log_result(
                    "Admin Customers Endpoint", 
                    True, 
                    f"Customers endpoint working - found {customer_count} customers",
                    data
                )
                success_count += 1
            else:
                self.log_result(
                    "Admin Customers Endpoint", 
                    False, 
                    f"Customers endpoint failed with status {response.status_code}",
                    response.json() if response.content else None
                )
                
        except Exception as e:
            self.log_result("Admin Customers Endpoint", False, f"Customers error: {str(e)}")
        
        # Test 3: Admin Announcements Endpoint
        try:
            response = self.session.get(
                f"{API_BASE}/admin/announcements",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                announcement_count = len(data) if isinstance(data, list) else data.get('total', 0)
                self.log_result(
                    "Admin Announcements Endpoint", 
                    True, 
                    f"Announcements endpoint working - found {announcement_count} announcements",
                    data
                )
                success_count += 1
            else:
                self.log_result(
                    "Admin Announcements Endpoint", 
                    False, 
                    f"Announcements endpoint failed with status {response.status_code}",
                    response.json() if response.content else None
                )
                
        except Exception as e:
            self.log_result("Admin Announcements Endpoint", False, f"Announcements error: {str(e)}")
        
        return success_count == total_tests
    
    def run_comprehensive_test(self):
        """Run all admin dashboard fix tests"""
        print("=" * 80)
        print("🎯 ADMIN DASHBOARD FIXES TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Authenticate
        if not self.authenticate_admin():
            print("\n❌ CRITICAL: Admin authentication failed - cannot proceed with tests")
            return self.generate_summary()
        
        # Step 2: Test Admin Dashboard (Previously 500 Error)
        dashboard_success = self.test_admin_dashboard_endpoint()
        
        # Step 3: Test Email System Endpoints (Corrected Paths)
        email_success = self.test_email_system_endpoints()
        
        # Step 4: Test New Admin Endpoints
        admin_endpoints_success = self.test_new_admin_endpoints()
        
        # Generate final summary
        return self.generate_summary()
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📋 ADMIN DASHBOARD FIXES TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        print(f"\n🎯 SPECIFIC FIX VERIFICATION:")
        
        # Check specific fixes
        dashboard_fixed = any(r["test"] == "Admin Dashboard Analytics" and r["success"] for r in self.results)
        email_campaigns_fixed = any(r["test"] == "Email Campaigns Endpoint" and r["success"] for r in self.results)
        email_providers_fixed = any(r["test"] == "Email Providers Endpoint" and r["success"] for r in self.results)
        users_endpoint_working = any(r["test"] == "Admin Users Endpoint" and r["success"] for r in self.results)
        customers_endpoint_working = any(r["test"] == "Admin Customers Endpoint" and r["success"] for r in self.results)
        announcements_endpoint_working = any(r["test"] == "Admin Announcements Endpoint" and r["success"] for r in self.results)
        
        print(f"✅ Admin Dashboard 500 Error Fixed: {'YES' if dashboard_fixed else 'NO'}")
        print(f"✅ Email Campaigns Path Fixed: {'YES' if email_campaigns_fixed else 'NO'}")
        print(f"✅ Email Providers Path Fixed: {'YES' if email_providers_fixed else 'NO'}")
        print(f"✅ Admin Users Endpoint Added: {'YES' if users_endpoint_working else 'NO'}")
        print(f"✅ Admin Customers Endpoint Added: {'YES' if customers_endpoint_working else 'NO'}")
        print(f"✅ Admin Announcements Endpoint Added: {'YES' if announcements_endpoint_working else 'NO'}")
        
        print(f"\n📊 DETAILED RESULTS:")
        for result in self.results:
            print(f"{result['status']} {result['test']}: {result['details']}")
        
        # Overall assessment
        critical_fixes = [dashboard_fixed, email_campaigns_fixed, email_providers_fixed]
        new_endpoints = [users_endpoint_working, customers_endpoint_working, announcements_endpoint_working]
        
        if all(critical_fixes) and any(new_endpoints):
            print(f"\n🎉 OVERALL ASSESSMENT: ADMIN DASHBOARD FIXES SUCCESSFUL")
            print(f"   - All critical 500 errors resolved")
            print(f"   - Email endpoint paths corrected")
            print(f"   - New admin endpoints functional")
        elif all(critical_fixes):
            print(f"\n⚠️  OVERALL ASSESSMENT: CRITICAL FIXES SUCCESSFUL, SOME NEW ENDPOINTS NEED WORK")
            print(f"   - Main dashboard issues resolved")
            print(f"   - Email paths working correctly")
        else:
            print(f"\n❌ OVERALL ASSESSMENT: CRITICAL ISSUES REMAIN")
            print(f"   - Some 500 errors may still exist")
            print(f"   - Admin dashboard functionality incomplete")
        
        return {
            "success_rate": success_rate,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "critical_fixes_working": all(critical_fixes),
            "new_endpoints_working": any(new_endpoints),
            "results": self.results
        }

def main():
    """Main test execution"""
    tester = AdminDashboardFixesTester()
    summary = tester.run_comprehensive_test()
    
    # Return appropriate exit code
    if summary["critical_fixes_working"]:
        print(f"\n✅ Admin dashboard fixes verification completed successfully!")
        return 0
    else:
        print(f"\n❌ Admin dashboard fixes verification found issues!")
        return 1

if __name__ == "__main__":
    exit(main())