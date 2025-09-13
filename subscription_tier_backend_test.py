#!/usr/bin/env python3
"""
Subscription Tier System and Live Chat Access Controls Backend Testing
Testing the updated subscription tier system with proper access controls
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime
from typing import Dict, Any, List

# Add the backend directory to Python path
sys.path.append('/app/backend')

# Test Configuration
BACKEND_URL = "https://customeriq-admin.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class SubscriptionTierTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {details}")
        
    def authenticate_admin(self) -> bool:
        """Authenticate as admin user"""
        try:
            response = self.session.post(f"{BACKEND_URL}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
                self.log_test("Admin Authentication", True, f"Successfully authenticated as {ADMIN_EMAIL}")
                return True
            else:
                self.log_test("Admin Authentication", False, f"Failed with status {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def create_test_user(self, email: str, subscription_tier: str) -> Dict[str, Any]:
        """Create a test user with specific subscription tier"""
        try:
            # First check if user already exists
            existing_user = self.session.get(f"{BACKEND_URL}/admin/users/search", params={"email": email})
            
            user_data = {
                "email": email,
                "password": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
                "company_name": f"Test Company {subscription_tier.title()}",
                "subscription_tier": subscription_tier,
                "is_active": True,
                "email_verified": True
            }
            
            # Try to create user via admin endpoint
            response = self.session.post(f"{BACKEND_URL}/admin/users/create", json=user_data)
            
            if response.status_code in [200, 201]:
                user_info = response.json()
                self.log_test(f"Create Test User ({subscription_tier})", True, 
                            f"Created user {email} with {subscription_tier} tier")
                return user_info
            else:
                # If creation fails, try to update existing user
                update_response = self.session.put(f"{BACKEND_URL}/admin/users/update", json={
                    "email": email,
                    "subscription_tier": subscription_tier,
                    "is_active": True
                })
                
                if update_response.status_code == 200:
                    self.log_test(f"Update Test User ({subscription_tier})", True, 
                                f"Updated existing user {email} to {subscription_tier} tier")
                    return update_response.json()
                else:
                    self.log_test(f"Create/Update Test User ({subscription_tier})", False, 
                                f"Failed to create/update user: {response.text}")
                    return {}
                    
        except Exception as e:
            self.log_test(f"Create Test User ({subscription_tier})", False, f"Exception: {str(e)}")
            return {}
    
    def login_as_user(self, email: str, password: str = "TestPassword123!") -> str:
        """Login as a specific user and return token"""
        try:
            response = self.session.post(f"{BACKEND_URL}/auth/login", json={
                "email": email,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                self.log_test(f"User Login ({email})", True, "Successfully logged in")
                return token
            else:
                self.log_test(f"User Login ({email})", False, f"Login failed: {response.text}")
                return ""
                
        except Exception as e:
            self.log_test(f"User Login ({email})", False, f"Exception: {str(e)}")
            return ""
    
    def test_live_chat_access_control(self):
        """Test live chat access control for different subscription tiers"""
        print("\n🔒 TESTING LIVE CHAT ACCESS CONTROL")
        print("=" * 60)
        
        # Test data: tier -> should_have_access
        tier_access_map = {
            "launch": False,      # Launch tier should NOT have access
            "growth": True,       # Growth tier should have access
            "scale": True,        # Scale tier should have access
            "white_label": True,  # White Label tier should have access
            "custom": True        # Custom tier should have access
        }
        
        for tier, should_have_access in tier_access_map.items():
            email = f"test.{tier}@example.com"
            
            # Create test user with specific tier
            user_info = self.create_test_user(email, tier)
            if not user_info:
                continue
                
            # Login as the test user
            user_token = self.login_as_user(email)
            if not user_token:
                continue
                
            # Test chat access check endpoint
            try:
                headers = {"Authorization": f"Bearer {user_token}"}
                response = self.session.get(f"{BACKEND_URL}/chat/access-check", headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    has_access = data.get("has_access", False)
                    subscription_tier = data.get("subscription_tier", "")
                    message = data.get("message", "")
                    
                    # Verify access matches expectation
                    access_correct = has_access == should_have_access
                    
                    if access_correct:
                        self.log_test(f"Chat Access Check ({tier} tier)", True, 
                                    f"Correct access: {has_access}, Message: {message}")
                    else:
                        self.log_test(f"Chat Access Check ({tier} tier)", False, 
                                    f"Expected access: {should_have_access}, Got: {has_access}")
                        
                    # Test error message for Launch tier
                    if tier == "launch" and not has_access:
                        expected_keywords = ["upgrade", "growth", "scale", "white label", "custom"]
                        message_lower = message.lower()
                        has_upgrade_message = any(keyword in message_lower for keyword in expected_keywords)
                        
                        self.log_test(f"Launch Tier Error Message", has_upgrade_message,
                                    f"Error message contains upgrade info: {message}")
                        
                else:
                    self.log_test(f"Chat Access Check ({tier} tier)", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"Chat Access Check ({tier} tier)", False, f"Exception: {str(e)}")
        
        # Test starting chat session for different tiers
        print("\n🚀 Testing Chat Session Creation")
        
        for tier, should_have_access in tier_access_map.items():
            email = f"test.{tier}@example.com"
            user_token = self.login_as_user(email)
            
            if not user_token:
                continue
                
            try:
                headers = {"Authorization": f"Bearer {user_token}"}
                response = self.session.post(f"{BACKEND_URL}/chat/start-session", 
                                           headers=headers,
                                           json={"initial_message": f"Test message from {tier} tier user"})
                
                if should_have_access:
                    # Should succeed for premium tiers
                    if response.status_code == 200:
                        data = response.json()
                        session_id = data.get("session_id")
                        self.log_test(f"Start Chat Session ({tier} tier)", True, 
                                    f"Successfully started session: {session_id}")
                    else:
                        self.log_test(f"Start Chat Session ({tier} tier)", False, 
                                    f"Expected success but got {response.status_code}: {response.text}")
                else:
                    # Should fail for Launch tier
                    if response.status_code == 403:
                        error_data = response.json()
                        error_detail = error_data.get("detail", "")
                        
                        # Check if error message mentions correct tier names
                        expected_tiers = ["growth", "scale", "white label", "custom"]
                        error_lower = error_detail.lower()
                        has_correct_tiers = any(tier_name in error_lower for tier_name in expected_tiers)
                        
                        self.log_test(f"Start Chat Session ({tier} tier)", True, 
                                    f"Correctly blocked with 403: {error_detail}")
                        
                        self.log_test(f"Launch Tier Block Message", has_correct_tiers,
                                    f"Error mentions correct tier names: {error_detail}")
                    else:
                        self.log_test(f"Start Chat Session ({tier} tier)", False, 
                                    f"Expected 403 but got {response.status_code}: {response.text}")
                        
            except Exception as e:
                self.log_test(f"Start Chat Session ({tier} tier)", False, f"Exception: {str(e)}")
    
    def test_support_tier_mapping(self):
        """Test the support tier mapping system"""
        print("\n🎯 TESTING SUPPORT TIER MAPPING")
        print("=" * 60)
        
        # Expected mapping: subscription_tier -> support_tier
        tier_mapping = {
            "launch": "basic",      # Launch -> basic support (24hr email)
            "growth": "growth",     # Growth -> growth support (12hr + live chat)
            "scale": "scale",       # Scale -> scale support (4hr + live chat + phone)
            "white_label": "scale", # White Label -> scale support
            "custom": "scale"       # Custom -> scale support
        }
        
        for subscription_tier, expected_support_tier in tier_mapping.items():
            email = f"test.{subscription_tier}@example.com"
            
            # Create/update test user
            user_info = self.create_test_user(email, subscription_tier)
            if not user_info:
                continue
                
            # Login as user
            user_token = self.login_as_user(email)
            if not user_token:
                continue
                
            # Test support tier info endpoint
            try:
                headers = {"Authorization": f"Bearer {user_token}"}
                response = self.session.get(f"{BACKEND_URL}/support/tier-info", headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    support_tier = data.get("support_tier", "")
                    subscription_tier_returned = data.get("subscription_tier", "")
                    tier_info = data.get("tier_info", {})
                    
                    # Verify mapping is correct
                    mapping_correct = support_tier == expected_support_tier
                    
                    if mapping_correct:
                        self.log_test(f"Support Tier Mapping ({subscription_tier})", True, 
                                    f"Correctly mapped to {support_tier}")
                        
                        # Verify tier info contains expected features
                        response_time = tier_info.get("response_time_hours", 0)
                        live_chat = tier_info.get("live_chat", False)
                        phone_support = tier_info.get("phone_support", False)
                        
                        # Verify features match expected support tier
                        if expected_support_tier == "basic":
                            expected_response_time = 24
                            expected_live_chat = False
                            expected_phone = False
                        elif expected_support_tier == "growth":
                            expected_response_time = 12
                            expected_live_chat = True
                            expected_phone = False
                        elif expected_support_tier == "scale":
                            expected_response_time = 4
                            expected_live_chat = True
                            expected_phone = True
                        
                        features_correct = (
                            response_time == expected_response_time and
                            live_chat == expected_live_chat and
                            phone_support == expected_phone
                        )
                        
                        self.log_test(f"Support Features ({subscription_tier})", features_correct,
                                    f"Response: {response_time}h, Chat: {live_chat}, Phone: {phone_support}")
                        
                    else:
                        self.log_test(f"Support Tier Mapping ({subscription_tier})", False, 
                                    f"Expected {expected_support_tier}, got {support_tier}")
                        
                else:
                    self.log_test(f"Support Tier Mapping ({subscription_tier})", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"Support Tier Mapping ({subscription_tier})", False, f"Exception: {str(e)}")
    
    def test_admin_chat_dashboard(self):
        """Test admin chat dashboard tier badge display"""
        print("\n👑 TESTING ADMIN CHAT DASHBOARD")
        print("=" * 60)
        
        # Ensure we're authenticated as admin
        if not self.admin_token:
            if not self.authenticate_admin():
                return
        
        # Test getting chat sessions with tier information
        try:
            response = self.session.get(f"{BACKEND_URL}/admin/chat/sessions")
            
            if response.status_code == 200:
                data = response.json()
                sessions = data.get("sessions", [])
                
                self.log_test("Admin Chat Sessions Endpoint", True, 
                            f"Retrieved {len(sessions)} chat sessions")
                
                # Check if sessions contain tier information
                if sessions:
                    for session in sessions[:3]:  # Check first 3 sessions
                        session_id = session.get("session_id", "")
                        user_tier = session.get("user_subscription_tier", "")
                        user_name = session.get("user_name", "")
                        
                        has_tier_info = bool(user_tier)
                        self.log_test(f"Session Tier Info ({session_id[:8]})", has_tier_info,
                                    f"User: {user_name}, Tier: {user_tier}")
                else:
                    self.log_test("Admin Chat Sessions Content", True, 
                                "No active sessions found (expected for test environment)")
                    
            else:
                self.log_test("Admin Chat Sessions Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Chat Sessions Endpoint", False, f"Exception: {str(e)}")
        
        # Test creating a chat session and verifying tier display
        print("\n📊 Testing Tier Badge Display Logic")
        
        # Create a test chat session for each tier
        test_tiers = ["launch", "growth", "scale", "white_label", "custom"]
        
        for tier in test_tiers:
            email = f"test.{tier}@example.com"
            user_token = self.login_as_user(email)
            
            if not user_token and tier in ["growth", "scale", "white_label", "custom"]:
                continue
                
            # Only test chat creation for tiers that should have access
            if tier in ["growth", "scale", "white_label", "custom"]:
                try:
                    headers = {"Authorization": f"Bearer {user_token}"}
                    response = self.session.post(f"{BACKEND_URL}/chat/start-session", 
                                               headers=headers,
                                               json={"initial_message": f"Test from {tier} tier"})
                    
                    if response.status_code == 200:
                        session_data = response.json()
                        session_id = session_data.get("session_id", "")
                        
                        # Now check if admin can see this session with correct tier
                        admin_response = self.session.get(f"{BACKEND_URL}/admin/chat/sessions")
                        
                        if admin_response.status_code == 200:
                            admin_data = admin_response.json()
                            sessions = admin_data.get("sessions", [])
                            
                            # Find our session
                            our_session = None
                            for session in sessions:
                                if session.get("session_id") == session_id:
                                    our_session = session
                                    break
                            
                            if our_session:
                                displayed_tier = our_session.get("user_subscription_tier", "")
                                tier_correct = displayed_tier.lower() == tier.lower()
                                
                                self.log_test(f"Admin Dashboard Tier Display ({tier})", tier_correct,
                                            f"Session shows tier: {displayed_tier}")
                            else:
                                self.log_test(f"Admin Dashboard Session Visibility ({tier})", False,
                                            "Session not found in admin dashboard")
                        
                    else:
                        self.log_test(f"Test Session Creation ({tier})", False, 
                                    f"Failed to create session: {response.text}")
                        
                except Exception as e:
                    self.log_test(f"Test Session Creation ({tier})", False, f"Exception: {str(e)}")
    
    def test_tier_name_consistency(self):
        """Test that tier names are displayed correctly throughout the system"""
        print("\n🏷️  TESTING TIER NAME CONSISTENCY")
        print("=" * 60)
        
        # Test that error messages use correct tier names
        launch_user_token = self.login_as_user("test.launch@example.com")
        
        if launch_user_token:
            try:
                headers = {"Authorization": f"Bearer {launch_user_token}"}
                
                # Test chat access error message
                response = self.session.get(f"{BACKEND_URL}/chat/access-check", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    message = data.get("message", "").lower()
                    
                    # Check for correct tier names in message
                    correct_tier_names = ["growth", "scale", "white label", "custom"]
                    incorrect_tier_names = ["professional", "enterprise", "premium"]
                    
                    has_correct_names = any(name in message for name in correct_tier_names)
                    has_incorrect_names = any(name in message for name in incorrect_tier_names)
                    
                    name_consistency = has_correct_names and not has_incorrect_names
                    
                    self.log_test("Tier Name Consistency (Access Check)", name_consistency,
                                f"Message uses correct tier names: {data.get('message', '')}")
                
                # Test chat session creation error message
                response = self.session.post(f"{BACKEND_URL}/chat/start-session", 
                                           headers=headers,
                                           json={"initial_message": "Test"})
                
                if response.status_code == 403:
                    error_data = response.json()
                    error_detail = error_data.get("detail", "").lower()
                    
                    # Check for correct tier names in error
                    correct_tier_names = ["growth", "scale", "white label", "custom"]
                    incorrect_tier_names = ["professional", "enterprise", "premium"]
                    
                    has_correct_names = any(name in error_detail for name in correct_tier_names)
                    has_incorrect_names = any(name in error_detail for name in incorrect_tier_names)
                    
                    error_consistency = has_correct_names and not has_incorrect_names
                    
                    self.log_test("Tier Name Consistency (Error Message)", error_consistency,
                                f"Error uses correct tier names: {error_data.get('detail', '')}")
                
            except Exception as e:
                self.log_test("Tier Name Consistency", False, f"Exception: {str(e)}")
    
    def run_comprehensive_tests(self):
        """Run all subscription tier and live chat tests"""
        print("🚀 STARTING SUBSCRIPTION TIER SYSTEM & LIVE CHAT ACCESS TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Authenticate as admin first
        if not self.authenticate_admin():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Run all test suites
        self.test_live_chat_access_control()
        self.test_support_tier_mapping()
        self.test_admin_chat_dashboard()
        self.test_tier_name_consistency()
        
        # Generate summary
        self.generate_test_summary()
    
    def generate_test_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 SUBSCRIPTION TIER SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS ({failed_tests}):")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")
        
        print(f"\n✅ PASSED TESTS ({passed_tests}):")
        for result in self.test_results:
            if result["success"]:
                print(f"  • {result['test']}")
        
        # Key findings
        print(f"\n🔍 KEY FINDINGS:")
        
        # Live Chat Access Control
        chat_access_tests = [r for r in self.test_results if "Chat Access Check" in r["test"]]
        chat_access_passed = sum(1 for r in chat_access_tests if r["success"])
        print(f"  • Live Chat Access Control: {chat_access_passed}/{len(chat_access_tests)} tiers correctly configured")
        
        # Support Tier Mapping
        mapping_tests = [r for r in self.test_results if "Support Tier Mapping" in r["test"]]
        mapping_passed = sum(1 for r in mapping_tests if r["success"])
        print(f"  • Support Tier Mapping: {mapping_passed}/{len(mapping_tests)} tiers correctly mapped")
        
        # Admin Dashboard
        dashboard_tests = [r for r in self.test_results if "Admin" in r["test"] and "Dashboard" in r["test"]]
        dashboard_passed = sum(1 for r in dashboard_tests if r["success"])
        print(f"  • Admin Dashboard: {dashboard_passed}/{len(dashboard_tests)} dashboard features working")
        
        # Tier Name Consistency
        consistency_tests = [r for r in self.test_results if "Consistency" in r["test"]]
        consistency_passed = sum(1 for r in consistency_tests if r["success"])
        print(f"  • Tier Name Consistency: {consistency_passed}/{len(consistency_tests)} naming checks passed")
        
        print("\n" + "=" * 80)
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Subscription tier system is working correctly!")
        elif success_rate >= 75:
            print("✅ GOOD: Most features working, minor issues to address")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Several issues need attention")
        else:
            print("❌ CRITICAL: Major issues with subscription tier system")
        
        print("=" * 80)

def main():
    """Main test execution"""
    tester = SubscriptionTierTester()
    tester.run_comprehensive_tests()

if __name__ == "__main__":
    main()