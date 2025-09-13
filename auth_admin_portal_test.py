#!/usr/bin/env python3
"""
Authentication & Admin Portal Access Testing

This script specifically tests the authentication system and admin portal access
as requested in the review to diagnose why the admin portal is not loading properly.

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. **Admin Authentication Test:**
   - Test admin login with credentials: admin@customermindiq.com / CustomerMindIQ2025!
   - Verify that the login returns a JWT token
   - Verify that the user profile includes the correct role (should be 'admin' or 'super_admin')
   - Check what role is returned in the user object

2. **Admin Portal Access Test:**
   - Test accessing admin endpoints that would be called by the AdminPortal component
   - Try to call /api/admin/analytics/dashboard to verify admin access
   - Test /api/admin/email-templates endpoint
   - Test /api/admin/workflows endpoint

3. **User Role Verification:**
   - After login, test the /api/auth/profile endpoint to see the exact user data being returned
   - Verify that the user role field is set correctly for admin access

The issue is that the admin portal is not loading properly - the user gets redirected 
to Customer Analytics instead of seeing the AdminPortal component.
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - Use production URL from frontend .env
BACKEND_URL = "https://admin-portal-fix-9.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AuthAdminPortalTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.jwt_token = None
        self.user_profile = None
        self.test_results = []
        self.start_time = datetime.now()
        
    def log_test(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        print(f"     Details: {details}")
        if response_data and isinstance(response_data, dict):
            if "role" in response_data:
                print(f"     User Role: {response_data.get('role', 'NOT_FOUND')}")
            if "subscription_tier" in response_data:
                print(f"     Subscription Tier: {response_data.get('subscription_tier', 'NOT_FOUND')}")
        print()

    def test_health_check(self) -> bool:
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{API_BASE}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Backend Health Check",
                    True,
                    f"Backend is healthy. Service: {data.get('service', 'Unknown')}",
                    data
                )
                return True
            else:
                self.log_test(
                    "Backend Health Check",
                    False,
                    f"Health check failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Backend Health Check",
                False,
                f"Health check error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_admin_login(self) -> bool:
        """Test admin login with specific credentials"""
        try:
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for JWT token
                if "access_token" in data:
                    self.jwt_token = data["access_token"]
                    
                    # Set authorization header for future requests
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.jwt_token}"
                    })
                    
                    # Check user data in login response
                    user_data = data.get("user", {})
                    role = user_data.get("role", "NOT_FOUND")
                    
                    self.log_test(
                        "Admin Login Authentication",
                        True,
                        f"Login successful. JWT token received. User role: {role}",
                        {
                            "has_token": True,
                            "token_length": len(self.jwt_token),
                            "role": role,
                            "user_data": user_data
                        }
                    )
                    return True
                else:
                    self.log_test(
                        "Admin Login Authentication",
                        False,
                        "Login response missing access_token",
                        data
                    )
                    return False
            else:
                self.log_test(
                    "Admin Login Authentication",
                    False,
                    f"Login failed with status {response.status_code}: {response.text[:200]}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Login Authentication",
                False,
                f"Login error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_user_profile(self) -> bool:
        """Test /api/auth/profile endpoint to get exact user data"""
        if not self.jwt_token:
            self.log_test(
                "User Profile Verification",
                False,
                "Cannot test profile - no JWT token available",
                None
            )
            return False
            
        try:
            response = self.session.get(f"{API_BASE}/auth/profile", timeout=10)
            
            if response.status_code == 200:
                self.user_profile = response.json()
                role = self.user_profile.get("role", "NOT_FOUND")
                subscription_tier = self.user_profile.get("subscription_tier", "NOT_FOUND")
                
                # Check if role is admin or super_admin
                is_admin_role = role in ["admin", "super_admin"]
                
                self.log_test(
                    "User Profile Verification",
                    True,
                    f"Profile retrieved. Role: {role}, Subscription: {subscription_tier}, Is Admin: {is_admin_role}",
                    {
                        "role": role,
                        "subscription_tier": subscription_tier,
                        "is_admin_role": is_admin_role,
                        "full_profile": self.user_profile
                    }
                )
                return True
            else:
                self.log_test(
                    "User Profile Verification",
                    False,
                    f"Profile request failed with status {response.status_code}: {response.text[:200]}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "User Profile Verification",
                False,
                f"Profile request error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_admin_analytics_dashboard(self) -> bool:
        """Test /api/admin/analytics/dashboard endpoint"""
        if not self.jwt_token:
            self.log_test(
                "Admin Analytics Dashboard Access",
                False,
                "Cannot test admin dashboard - no JWT token available",
                None
            )
            return False
            
        try:
            response = self.session.get(f"{API_BASE}/admin/analytics/dashboard", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Admin Analytics Dashboard Access",
                    True,
                    f"Admin dashboard accessible. Data keys: {list(data.keys()) if isinstance(data, dict) else 'Non-dict response'}",
                    {"status_code": 200, "data_keys": list(data.keys()) if isinstance(data, dict) else None}
                )
                return True
            elif response.status_code == 401:
                self.log_test(
                    "Admin Analytics Dashboard Access",
                    False,
                    "Admin dashboard returned 401 Unauthorized - authentication issue",
                    {"status_code": 401, "response": response.text[:200]}
                )
                return False
            elif response.status_code == 403:
                self.log_test(
                    "Admin Analytics Dashboard Access",
                    False,
                    "Admin dashboard returned 403 Forbidden - insufficient permissions",
                    {"status_code": 403, "response": response.text[:200]}
                )
                return False
            elif response.status_code == 404:
                self.log_test(
                    "Admin Analytics Dashboard Access",
                    False,
                    "Admin dashboard returned 404 Not Found - endpoint may not exist",
                    {"status_code": 404, "response": response.text[:200]}
                )
                return False
            else:
                self.log_test(
                    "Admin Analytics Dashboard Access",
                    False,
                    f"Admin dashboard failed with status {response.status_code}: {response.text[:200]}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Analytics Dashboard Access",
                False,
                f"Admin dashboard error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_admin_email_templates(self) -> bool:
        """Test /api/admin/email-templates endpoint"""
        if not self.jwt_token:
            self.log_test(
                "Admin Email Templates Access",
                False,
                "Cannot test email templates - no JWT token available",
                None
            )
            return False
            
        try:
            response = self.session.get(f"{API_BASE}/admin/email-templates", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Admin Email Templates Access",
                    True,
                    f"Email templates accessible. Response type: {type(data)}",
                    {"status_code": 200, "response_type": str(type(data))}
                )
                return True
            elif response.status_code == 401:
                self.log_test(
                    "Admin Email Templates Access",
                    False,
                    "Email templates returned 401 Unauthorized - authentication issue",
                    {"status_code": 401, "response": response.text[:200]}
                )
                return False
            elif response.status_code == 403:
                self.log_test(
                    "Admin Email Templates Access",
                    False,
                    "Email templates returned 403 Forbidden - insufficient permissions",
                    {"status_code": 403, "response": response.text[:200]}
                )
                return False
            elif response.status_code == 404:
                self.log_test(
                    "Admin Email Templates Access",
                    False,
                    "Email templates returned 404 Not Found - endpoint may not exist",
                    {"status_code": 404, "response": response.text[:200]}
                )
                return False
            else:
                self.log_test(
                    "Admin Email Templates Access",
                    False,
                    f"Email templates failed with status {response.status_code}: {response.text[:200]}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Email Templates Access",
                False,
                f"Email templates error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_admin_workflows(self) -> bool:
        """Test /api/admin/workflows endpoint"""
        if not self.jwt_token:
            self.log_test(
                "Admin Workflows Access",
                False,
                "Cannot test workflows - no JWT token available",
                None
            )
            return False
            
        try:
            response = self.session.get(f"{API_BASE}/admin/workflows", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Admin Workflows Access",
                    True,
                    f"Workflows accessible. Response type: {type(data)}",
                    {"status_code": 200, "response_type": str(type(data))}
                )
                return True
            elif response.status_code == 401:
                self.log_test(
                    "Admin Workflows Access",
                    False,
                    "Workflows returned 401 Unauthorized - authentication issue",
                    {"status_code": 401, "response": response.text[:200]}
                )
                return False
            elif response.status_code == 403:
                self.log_test(
                    "Admin Workflows Access",
                    False,
                    "Workflows returned 403 Forbidden - insufficient permissions",
                    {"status_code": 403, "response": response.text[:200]}
                )
                return False
            elif response.status_code == 404:
                self.log_test(
                    "Admin Workflows Access",
                    False,
                    "Workflows returned 404 Not Found - endpoint may not exist",
                    {"status_code": 404, "response": response.text[:200]}
                )
                return False
            else:
                self.log_test(
                    "Admin Workflows Access",
                    False,
                    f"Workflows failed with status {response.status_code}: {response.text[:200]}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Workflows Access",
                False,
                f"Workflows error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def run_comprehensive_test(self):
        """Run all authentication and admin portal tests"""
        print("🔐 AUTHENTICATION & ADMIN PORTAL ACCESS TESTING")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Credentials: {ADMIN_CREDENTIALS['email']}")
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Test sequence
        tests = [
            ("Backend Health Check", self.test_health_check),
            ("Admin Login Authentication", self.test_admin_login),
            ("User Profile Verification", self.test_user_profile),
            ("Admin Analytics Dashboard Access", self.test_admin_analytics_dashboard),
            ("Admin Email Templates Access", self.test_admin_email_templates),
            ("Admin Workflows Access", self.test_admin_workflows),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {str(e)}", {"error": str(e)})
        
        # Summary
        print("=" * 60)
        print("🎯 AUTHENTICATION & ADMIN PORTAL TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests} tests passed)")
        print()
        
        # Key findings
        print("🔍 KEY FINDINGS:")
        
        if self.user_profile:
            role = self.user_profile.get("role", "NOT_FOUND")
            print(f"• User Role: {role}")
            print(f"• Is Admin Role: {role in ['admin', 'super_admin']}")
            print(f"• Subscription Tier: {self.user_profile.get('subscription_tier', 'NOT_FOUND')}")
        else:
            print("• User Profile: NOT RETRIEVED")
            
        if self.jwt_token:
            print(f"• JWT Token: PRESENT (length: {len(self.jwt_token)})")
        else:
            print("• JWT Token: MISSING")
        
        print()
        
        # Diagnosis
        print("🩺 ADMIN PORTAL ISSUE DIAGNOSIS:")
        
        failed_tests = [result for result in self.test_results if not result["success"]]
        
        if not failed_tests:
            print("• All authentication and admin access tests passed")
            print("• The issue may be in the frontend routing or component logic")
        else:
            print("• Issues found in backend authentication/authorization:")
            for failed_test in failed_tests:
                print(f"  - {failed_test['test']}: {failed_test['details']}")
        
        print()
        print("📊 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        return success_rate >= 80  # Consider successful if 80% or more tests pass

def main():
    """Main test execution"""
    tester = AuthAdminPortalTester()
    
    try:
        success = tester.run_comprehensive_test()
        
        if success:
            print("\n🎉 AUTHENTICATION & ADMIN PORTAL TESTING COMPLETED SUCCESSFULLY")
            sys.exit(0)
        else:
            print("\n⚠️  AUTHENTICATION & ADMIN PORTAL TESTING COMPLETED WITH ISSUES")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()