#!/usr/bin/env python3
"""
Trial Registration Endpoint Testing
Testing the new trial registration endpoint at /api/subscriptions/trial/register
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get backend URL from environment
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-iq-touch.preview.emergentagent.com")

class TrialRegistrationTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session = None
        self.test_results = []
        self.test_email = None  # Store email for duplicate test
        
    async def setup_session(self):
        """Setup HTTP session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"Content-Type": "application/json"}
        )
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    def log_result(self, test_name: str, success: bool, details: str, response_data: dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
            
    async def test_trial_registration_new_user(self):
        """Test 1: POST /api/subscriptions/trial/register with new user"""
        test_name = "Trial Registration - New User"
        
        try:
            # Use realistic test data as requested - use timestamp to avoid duplicates
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.test_email = f"jane.smith.{timestamp}@testcompany.com"
            test_data = {
                "email": self.test_email,
                "first_name": "Jane",
                "last_name": "Smith",
                "company_name": "Test Company Inc"
            }
            
            url = f"{self.backend_url}/api/subscriptions/trial/register"
            
            async with self.session.post(url, json=test_data) as response:
                response_data = await response.json()
                
                if response.status == 200:
                    # Verify response structure
                    required_fields = ["status", "message", "trial_end", "user"]
                    missing_fields = [field for field in required_fields if field not in response_data]
                    
                    if missing_fields:
                        self.log_result(test_name, False, f"Missing required fields: {missing_fields}", response_data)
                        return None
                        
                    # Verify user object structure
                    user_data = response_data.get("user", {})
                    required_user_fields = ["email", "first_name", "last_name", "company_name", "password"]
                    missing_user_fields = [field for field in required_user_fields if field not in user_data]
                    
                    if missing_user_fields:
                        self.log_result(test_name, False, f"Missing user fields: {missing_user_fields}", response_data)
                        return None
                        
                    # Verify status is success
                    if response_data.get("status") != "success":
                        self.log_result(test_name, False, f"Status not success: {response_data.get('status')}", response_data)
                        return None
                        
                    self.log_result(test_name, True, f"Trial registered successfully for {user_data['email']}", response_data)
                    return user_data  # Return user data for login test
                    
                else:
                    self.log_result(test_name, False, f"HTTP {response.status}: {response_data.get('detail', 'Unknown error')}", response_data)
                    return None
                    
        except Exception as e:
            self.log_result(test_name, False, f"Exception: {str(e)}")
            return None
            
    async def test_duplicate_registration(self):
        """Test 2: Test duplicate registration with same email"""
        test_name = "Duplicate Registration Error Handling"
        
        try:
            # Use same email as first test
            test_data = {
                "email": self.test_email,
                "first_name": "Jane",
                "last_name": "Smith",
                "company_name": "Test Company Inc"
            }
            
            url = f"{self.backend_url}/api/subscriptions/trial/register"
            
            async with self.session.post(url, json=test_data) as response:
                response_data = await response.json()
                
                # Should return error for duplicate registration
                if response.status == 400:
                    error_message = response_data.get("detail", "")
                    if "already registered" in error_message.lower() or "trial used" in error_message.lower():
                        self.log_result(test_name, True, f"Correctly rejected duplicate registration: {error_message}")
                    else:
                        self.log_result(test_name, False, f"Unexpected error message: {error_message}", response_data)
                else:
                    self.log_result(test_name, False, f"Expected 400 error, got {response.status}", response_data)
                    
        except Exception as e:
            self.log_result(test_name, False, f"Exception: {str(e)}")
            
    async def test_auth_login(self, user_data):
        """Test 3: Test auth login with returned credentials"""
        test_name = "Auto-Login with Trial Credentials"
        
        if not user_data:
            self.log_result(test_name, False, "No user data available from registration test")
            return None
            
        try:
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"],
                "remember_me": False
            }
            
            url = f"{self.backend_url}/api/auth/login"
            
            async with self.session.post(url, json=login_data) as response:
                response_data = await response.json()
                
                if response.status == 200:
                    # Verify login response structure
                    required_fields = ["access_token", "refresh_token", "token_type", "user_profile"]
                    missing_fields = [field for field in required_fields if field not in response_data]
                    
                    if missing_fields:
                        self.log_result(test_name, False, f"Missing login response fields: {missing_fields}", response_data)
                        return None
                        
                    # Verify user profile
                    user_profile = response_data.get("user_profile", {})
                    if user_profile.get("email") != user_data["email"]:
                        self.log_result(test_name, False, f"Email mismatch in profile: {user_profile.get('email')} vs {user_data['email']}")
                        return None
                        
                    self.log_result(test_name, True, f"Successfully logged in with trial credentials for {user_profile.get('email')}")
                    return response_data.get("access_token")
                    
                else:
                    self.log_result(test_name, False, f"Login failed with HTTP {response.status}: {response_data.get('detail', 'Unknown error')}", response_data)
                    return None
                    
        except Exception as e:
            self.log_result(test_name, False, f"Exception: {str(e)}")
            return None
            
    async def test_dashboard_access(self, access_token):
        """Test 4: Verify dashboard access with trial token"""
        test_name = "Dashboard Access with Trial Token"
        
        if not access_token:
            self.log_result(test_name, False, "No access token available from login test")
            return
            
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Test profile endpoint to verify token works
            url = f"{self.backend_url}/api/auth/profile"
            
            async with self.session.get(url, headers=headers) as response:
                response_data = await response.json()
                
                if response.status == 200:
                    profile = response_data
                    
                    # Verify trial user properties
                    if profile.get("subscription_tier") == "free" and profile.get("is_active"):
                        self.log_result(test_name, True, f"Trial user can access dashboard with proper subscription tier: {profile.get('subscription_tier')}")
                    else:
                        self.log_result(test_name, False, f"Unexpected subscription tier or status: tier={profile.get('subscription_tier')}, active={profile.get('is_active')}", response_data)
                        
                else:
                    self.log_result(test_name, False, f"Profile access failed with HTTP {response.status}: {response_data.get('detail', 'Unknown error')}", response_data)
                    
        except Exception as e:
            self.log_result(test_name, False, f"Exception: {str(e)}")
            
    async def test_subscription_plans_endpoint(self):
        """Test 5: Verify subscription plans endpoint works"""
        test_name = "Subscription Plans Endpoint"
        
        try:
            url = f"{self.backend_url}/api/subscriptions/plans"
            
            async with self.session.get(url) as response:
                response_data = await response.json()
                
                if response.status == 200:
                    plans = response_data.get("plans", {})
                    
                    # Verify key plans exist
                    expected_plans = ["free", "launch", "growth", "scale"]
                    missing_plans = [plan for plan in expected_plans if plan not in plans]
                    
                    if missing_plans:
                        self.log_result(test_name, False, f"Missing subscription plans: {missing_plans}", response_data)
                    else:
                        # Verify free plan has trial info
                        free_plan = plans.get("free", {})
                        if free_plan.get("trial_days") == 7:
                            self.log_result(test_name, True, f"Subscription plans endpoint working with {len(plans)} plans including 7-day trial")
                        else:
                            self.log_result(test_name, False, f"Free plan missing trial_days or incorrect value: {free_plan.get('trial_days')}")
                            
                else:
                    self.log_result(test_name, False, f"Plans endpoint failed with HTTP {response.status}: {response_data.get('detail', 'Unknown error')}", response_data)
                    
        except Exception as e:
            self.log_result(test_name, False, f"Exception: {str(e)}")
            
    async def run_all_tests(self):
        """Run all trial registration tests"""
        print("🚀 Starting Trial Registration Endpoint Testing")
        print(f"Backend URL: {self.backend_url}")
        print("=" * 60)
        
        await self.setup_session()
        
        try:
            # Test 1: New user registration
            user_data = await self.test_trial_registration_new_user()
            
            # Test 2: Duplicate registration
            await self.test_duplicate_registration()
            
            # Test 3: Login with trial credentials
            access_token = await self.test_auth_login(user_data)
            
            # Test 4: Dashboard access
            await self.test_dashboard_access(access_token)
            
            # Test 5: Subscription plans
            await self.test_subscription_plans_endpoint()
            
        finally:
            await self.cleanup_session()
            
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
                    
        print("\n🎯 KEY FINDINGS:")
        
        # Check if the main issue is resolved
        trial_reg_success = any(r["success"] and "Trial Registration - New User" in r["test"] for r in self.test_results)
        login_success = any(r["success"] and "Auto-Login with Trial Credentials" in r["test"] for r in self.test_results)
        
        if trial_reg_success and login_success:
            print("✅ ISSUE RESOLVED: Users clicking '7-day free trial' can now register and auto-login successfully")
        elif trial_reg_success:
            print("⚠️  PARTIAL FIX: Trial registration works but auto-login may have issues")
        else:
            print("❌ ISSUE PERSISTS: Trial registration endpoint has problems")
            
        return passed_tests, failed_tests

async def main():
    """Main test execution"""
    tester = TrialRegistrationTester()
    passed, failed = await tester.run_all_tests()
    
    # Return appropriate exit code
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)