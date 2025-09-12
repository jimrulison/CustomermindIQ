#!/usr/bin/env python3
"""
CustomerMind IQ - Affiliate Login Testing
Testing the affiliate login functionality specifically for admin@customermindiq.com

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. Check if the affiliate login endpoint /api/affiliate/auth/login is working
2. Test if admin@customermindiq.com exists in the affiliate system
3. Check if there are any CORS or network issues
4. Verify the affiliate authentication system is properly connected

The user is getting a "Network error. Please try again." when trying to log in through the affiliate portal.
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

# Configuration - Use localhost for testing (external URL returns 502)
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

AFFILIATE_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class AffiliateLoginTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.admin_token = None
        self.test_results = []
        
    def log_result(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   {message}")
        if details:
            print(f"   Details: {json.dumps(details, indent=2)}")
        print()

    def test_health_check(self):
        """Test basic connectivity to the backend"""
        try:
            response = self.session.get(f"{API_BASE}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Backend Health Check",
                    True,
                    f"Backend is healthy and accessible",
                    {"status_code": response.status_code, "response": data}
                )
                return True
            else:
                self.log_result(
                    "Backend Health Check",
                    False,
                    f"Backend returned status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Backend Health Check",
                False,
                f"Network error connecting to backend: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_admin_login(self):
        """Test admin login to get authentication token"""
        try:
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                self.log_result(
                    "Admin Authentication",
                    True,
                    "Admin login successful",
                    {"user_role": data.get("user", {}).get("role")}
                )
                return True
            else:
                self.log_result(
                    "Admin Authentication",
                    False,
                    f"Admin login failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Admin Authentication",
                False,
                f"Network error during admin login: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_affiliate_endpoint_accessibility(self):
        """Test if affiliate endpoints are accessible"""
        try:
            # Test affiliate dashboard endpoint (should return 400 without affiliate_id)
            response = self.session.get(f"{API_BASE}/affiliate/dashboard", timeout=10)
            
            # We expect a 422 (validation error) or 400 (missing affiliate_id) - this means endpoint is accessible
            if response.status_code in [400, 422]:
                self.log_result(
                    "Affiliate Endpoint Accessibility",
                    True,
                    "Affiliate endpoints are accessible (validation error expected without affiliate_id)",
                    {"status_code": response.status_code}
                )
                return True
            elif response.status_code == 404:
                self.log_result(
                    "Affiliate Endpoint Accessibility",
                    False,
                    "Affiliate endpoints not found - routing issue",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
            else:
                self.log_result(
                    "Affiliate Endpoint Accessibility",
                    False,
                    f"Unexpected response from affiliate endpoint: {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Affiliate Endpoint Accessibility",
                False,
                f"Network error accessing affiliate endpoints: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_affiliate_login_endpoint(self):
        """Test the affiliate login endpoint directly"""
        try:
            response = self.session.post(
                f"{API_BASE}/affiliate/auth/login",
                json=AFFILIATE_CREDENTIALS,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Affiliate Login Endpoint",
                    True,
                    "Affiliate login successful",
                    {"response": data}
                )
                return True
            elif response.status_code == 401:
                self.log_result(
                    "Affiliate Login Endpoint",
                    False,
                    "Affiliate login failed - Invalid credentials (admin@customermindiq.com not found in affiliate system)",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
            elif response.status_code == 403:
                data = response.json()
                self.log_result(
                    "Affiliate Login Endpoint",
                    False,
                    "Affiliate account exists but is pending approval",
                    {"status_code": response.status_code, "response": data}
                )
                return False
            elif response.status_code == 404:
                self.log_result(
                    "Affiliate Login Endpoint",
                    False,
                    "Affiliate login endpoint not found - routing issue",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
            else:
                self.log_result(
                    "Affiliate Login Endpoint",
                    False,
                    f"Affiliate login failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Affiliate Login Endpoint",
                False,
                f"Network error during affiliate login: {str(e)} - This matches the user's reported 'Network error. Please try again.'",
                {"error": str(e)}
            )
            return False

    def test_check_admin_affiliate_account(self):
        """Check if admin@customermindiq.com exists as an affiliate"""
        if not self.admin_token:
            self.log_result(
                "Check Admin Affiliate Account",
                False,
                "Cannot check affiliate account - admin authentication failed",
                {}
            )
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            # Try to get affiliate data using admin privileges
            # First, let's check if there's an admin endpoint to list affiliates
            response = self.session.get(
                f"{API_BASE}/admin/affiliates",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                affiliates = data.get("affiliates", [])
                admin_affiliate = None
                
                for affiliate in affiliates:
                    if affiliate.get("email") == "admin@customermindiq.com":
                        admin_affiliate = affiliate
                        break
                
                if admin_affiliate:
                    self.log_result(
                        "Check Admin Affiliate Account",
                        True,
                        f"Admin affiliate account found with status: {admin_affiliate.get('status')}",
                        {"affiliate": admin_affiliate}
                    )
                    return True
                else:
                    self.log_result(
                        "Check Admin Affiliate Account",
                        False,
                        "Admin affiliate account not found - admin@customermindiq.com is not registered as an affiliate",
                        {"total_affiliates": len(affiliates)}
                    )
                    return False
            else:
                self.log_result(
                    "Check Admin Affiliate Account",
                    False,
                    f"Cannot access affiliate list - status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Check Admin Affiliate Account",
                False,
                f"Network error checking affiliate account: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_cors_headers(self):
        """Test CORS headers on affiliate endpoints"""
        try:
            # Make an OPTIONS request to check CORS
            response = self.session.options(
                f"{API_BASE}/affiliate/auth/login",
                headers={
                    "Origin": "https://mindindata.preview.emergentagent.com",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                },
                timeout=10
            )
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
                "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials")
            }
            
            if response.status_code in [200, 204] and cors_headers["Access-Control-Allow-Origin"]:
                self.log_result(
                    "CORS Configuration",
                    True,
                    "CORS headers are properly configured",
                    {"cors_headers": cors_headers}
                )
                return True
            else:
                self.log_result(
                    "CORS Configuration",
                    False,
                    "CORS headers missing or misconfigured",
                    {"status_code": response.status_code, "cors_headers": cors_headers}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "CORS Configuration",
                False,
                f"Network error testing CORS: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_create_admin_affiliate_account(self):
        """Attempt to create an affiliate account for admin@customermindiq.com"""
        try:
            affiliate_registration = {
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!",
                "phone": "+1-555-0123",
                "company": "CustomerMind IQ",
                "website": "https://customermindiq.com",
                "promotion_method": "email",
                "address": {
                    "street": "123 Business St",
                    "city": "Business City",
                    "state": "CA",
                    "zip_code": "90210",
                    "country": "US"
                },
                "payment_method": "paypal",
                "payment_details": {
                    "paypal_email": "admin@customermindiq.com"
                }
            }
            
            response = self.session.post(
                f"{API_BASE}/affiliate/auth/register",
                json=affiliate_registration,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.log_result(
                    "Create Admin Affiliate Account",
                    True,
                    "Admin affiliate account created successfully",
                    {"response": data}
                )
                return True
            elif response.status_code == 400 and "already registered" in response.text.lower():
                self.log_result(
                    "Create Admin Affiliate Account",
                    True,
                    "Admin affiliate account already exists",
                    {"status_code": response.status_code, "response": response.text}
                )
                return True
            else:
                self.log_result(
                    "Create Admin Affiliate Account",
                    False,
                    f"Failed to create admin affiliate account - status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text}
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result(
                "Create Admin Affiliate Account",
                False,
                f"Network error creating affiliate account: {str(e)}",
                {"error": str(e)}
            )
            return False

    def run_all_tests(self):
        """Run all affiliate login tests"""
        print("🔍 AFFILIATE LOGIN TESTING - CustomerMind IQ")
        print("=" * 60)
        print(f"Testing affiliate login for: {AFFILIATE_CREDENTIALS['email']}")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 60)
        print()
        
        # Test sequence
        tests = [
            self.test_health_check,
            self.test_admin_login,
            self.test_affiliate_endpoint_accessibility,
            self.test_cors_headers,
            self.test_check_admin_affiliate_account,
            self.test_create_admin_affiliate_account,
            self.test_affiliate_login_endpoint,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                self.log_result(
                    test.__name__,
                    False,
                    f"Test failed with exception: {str(e)}",
                    {"error": str(e)}
                )
        
        # Summary
        print("=" * 60)
        print("🎯 AFFILIATE LOGIN TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Passed: {passed}/{total} ({(passed/total)*100:.1f}%)")
        print()
        
        # Detailed results
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        print()
        print("🔧 DIAGNOSIS AND RECOMMENDATIONS:")
        print("=" * 60)
        
        # Analyze results and provide recommendations
        health_ok = any(r["test"] == "Backend Health Check" and r["success"] for r in self.test_results)
        admin_auth_ok = any(r["test"] == "Admin Authentication" and r["success"] for r in self.test_results)
        affiliate_endpoint_ok = any(r["test"] == "Affiliate Endpoint Accessibility" and r["success"] for r in self.test_results)
        cors_ok = any(r["test"] == "CORS Configuration" and r["success"] for r in self.test_results)
        admin_affiliate_exists = any(r["test"] == "Check Admin Affiliate Account" and r["success"] for r in self.test_results)
        affiliate_login_ok = any(r["test"] == "Affiliate Login Endpoint" and r["success"] for r in self.test_results)
        
        if not health_ok:
            print("❌ CRITICAL: Backend is not accessible - network connectivity issue")
            print("   - Check if the backend service is running")
            print("   - Verify the URL: https://mindindata.preview.emergentagent.com")
            print("   - Check DNS resolution and firewall settings")
        
        elif not affiliate_endpoint_ok:
            print("❌ CRITICAL: Affiliate endpoints are not properly routed")
            print("   - Check FastAPI router configuration in server.py")
            print("   - Verify affiliate_system router is included with correct prefix")
        
        elif not admin_affiliate_exists:
            print("❌ ROOT CAUSE IDENTIFIED: admin@customermindiq.com is not registered as an affiliate")
            print("   - The admin user exists in the main authentication system")
            print("   - But there's no corresponding affiliate account")
            print("   - This explains the 'Network error' - it's actually an authentication error")
            print()
            print("🔧 SOLUTION:")
            print("   1. Register admin@customermindiq.com as an affiliate using the registration endpoint")
            print("   2. Or create the affiliate account directly in the database")
            print("   3. Ensure the affiliate account status is 'approved' or 'active'")
        
        elif not affiliate_login_ok:
            print("❌ ISSUE: Affiliate login endpoint has problems")
            print("   - Check password hashing compatibility")
            print("   - Verify affiliate account status (must be 'approved' or 'active')")
            print("   - Check JWT token generation")
        
        else:
            print("✅ All tests passed - affiliate login should be working")
        
        if not cors_ok:
            print("⚠️  WARNING: CORS configuration issues detected")
            print("   - This could cause 'Network error' messages in browsers")
            print("   - Check CORS middleware configuration in FastAPI")
        
        return passed, total

def main():
    """Main test execution"""
    tester = AffiliateLoginTester()
    passed, total = tester.run_all_tests()
    
    # Exit with appropriate code
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()