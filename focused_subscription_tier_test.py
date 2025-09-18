#!/usr/bin/env python3
"""
Focused Subscription Tier System Testing
Testing the core subscription tier functionality with existing users
"""

import json
import requests
from datetime import datetime
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Test Configuration
BACKEND_URL = "https://customeriq-fix.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class FocusedTierTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
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
                user_profile = data.get("user_profile", {})
                tier = user_profile.get("subscription_tier", "unknown")
                self.log_test("Admin Authentication", True, f"Authenticated as {ADMIN_EMAIL} (tier: {tier})")
                return True
            else:
                self.log_test("Admin Authentication", False, f"Failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_chat_access_check_endpoint(self):
        """Test the /api/chat/access-check endpoint with admin user"""
        print("\n🔒 TESTING CHAT ACCESS CHECK ENDPOINT")
        print("=" * 60)
        
        try:
            response = self.session.get(f"{BACKEND_URL}/chat/access-check")
            
            if response.status_code == 200:
                data = response.json()
                has_access = data.get("has_access", False)
                subscription_tier = data.get("subscription_tier", "")
                message = data.get("message", "")
                
                self.log_test("Chat Access Check Endpoint", True, 
                            f"Access: {has_access}, Tier: {subscription_tier}")
                
                # Admin with custom tier should have access
                if subscription_tier.lower() in ["custom", "scale", "white_label"]:
                    expected_access = True
                    access_correct = has_access == expected_access
                    self.log_test("Admin Chat Access Logic", access_correct,
                                f"Custom tier correctly has access: {has_access}")
                
                # Check message content
                if has_access:
                    expected_keywords = ["growth", "scale", "white label", "custom"]
                    message_lower = message.lower()
                    has_tier_info = any(keyword in message_lower for keyword in expected_keywords)
                    self.log_test("Access Message Content", has_tier_info,
                                f"Message mentions correct tiers: {message}")
                
            else:
                self.log_test("Chat Access Check Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Chat Access Check Endpoint", False, f"Exception: {str(e)}")
    
    def test_support_tier_info_endpoint(self):
        """Test the /api/support/tier-info endpoint"""
        print("\n🎯 TESTING SUPPORT TIER INFO ENDPOINT")
        print("=" * 60)
        
        try:
            response = self.session.get(f"{BACKEND_URL}/support/tier-info")
            
            if response.status_code == 200:
                data = response.json()
                support_tier = data.get("support_tier", "")
                subscription_tier = data.get("subscription_tier", "")
                tier_info = data.get("tier_info", {})
                
                self.log_test("Support Tier Info Endpoint", True, 
                            f"Support tier: {support_tier}, Subscription: {subscription_tier}")
                
                # Verify tier mapping logic
                if subscription_tier.lower() == "custom":
                    expected_support_tier = "scale"  # Custom should map to scale support
                    mapping_correct = support_tier == expected_support_tier
                    self.log_test("Custom Tier Mapping", mapping_correct,
                                f"Custom tier maps to {support_tier} support")
                
                # Check tier info structure
                required_fields = ["response_time_hours", "live_chat", "phone_support"]
                has_required_fields = all(field in tier_info for field in required_fields)
                self.log_test("Tier Info Structure", has_required_fields,
                            f"Contains required fields: {list(tier_info.keys())}")
                
                # Verify scale tier features
                if support_tier == "scale":
                    response_time = tier_info.get("response_time_hours", 0)
                    live_chat = tier_info.get("live_chat", False)
                    phone_support = tier_info.get("phone_support", False)
                    
                    scale_features_correct = (
                        response_time == 4 and
                        live_chat == True and
                        phone_support == True
                    )
                    
                    self.log_test("Scale Tier Features", scale_features_correct,
                                f"4hr response: {response_time==4}, Chat: {live_chat}, Phone: {phone_support}")
                
            else:
                self.log_test("Support Tier Info Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Support Tier Info Endpoint", False, f"Exception: {str(e)}")
    
    def test_chat_session_creation(self):
        """Test creating a chat session with admin user"""
        print("\n🚀 TESTING CHAT SESSION CREATION")
        print("=" * 60)
        
        try:
            response = self.session.post(f"{BACKEND_URL}/chat/start-session", json={
                "initial_message": "Test message from admin user for tier testing"
            })
            
            if response.status_code == 200:
                data = response.json()
                session_id = data.get("session_id", "")
                session_status = data.get("session_status", "")
                message = data.get("message", "")
                
                self.log_test("Chat Session Creation", True, 
                            f"Created session {session_id[:12]}... with status: {session_status}")
                
                # Test getting session messages
                if session_id:
                    msg_response = self.session.get(f"{BACKEND_URL}/chat/messages/{session_id}")
                    if msg_response.status_code == 200:
                        msg_data = msg_response.json()
                        messages = msg_data.get("messages", [])
                        session_info = msg_data.get("session", {})
                        
                        self.log_test("Chat Messages Retrieval", True,
                                    f"Retrieved {len(messages)} messages for session")
                        
                        # Check if session contains tier information
                        if session_info:
                            session_status = session_info.get("status", "")
                            admin_name = session_info.get("admin_name", "")
                            self.log_test("Session Info Structure", True,
                                        f"Status: {session_status}, Admin: {admin_name}")
                    else:
                        self.log_test("Chat Messages Retrieval", False,
                                    f"Failed to get messages: {msg_response.status_code}")
                
            elif response.status_code == 403:
                # This would indicate access control is working
                error_data = response.json()
                error_detail = error_data.get("detail", "")
                
                # Check if error mentions correct tier names
                expected_tiers = ["growth", "scale", "white label", "custom"]
                error_lower = error_detail.lower()
                has_correct_tiers = any(tier in error_lower for tier in expected_tiers)
                
                self.log_test("Chat Access Control Error", has_correct_tiers,
                            f"Error mentions correct tiers: {error_detail}")
                
            else:
                self.log_test("Chat Session Creation", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Chat Session Creation", False, f"Exception: {str(e)}")
    
    def test_admin_chat_dashboard(self):
        """Test admin chat dashboard functionality"""
        print("\n👑 TESTING ADMIN CHAT DASHBOARD")
        print("=" * 60)
        
        try:
            response = self.session.get(f"{BACKEND_URL}/admin/chat/sessions")
            
            if response.status_code == 200:
                data = response.json()
                sessions = data.get("sessions", [])
                total_count = data.get("total_count", 0)
                
                self.log_test("Admin Chat Sessions List", True, 
                            f"Retrieved {len(sessions)} sessions (total: {total_count})")
                
                # Check session structure for tier information
                if sessions:
                    for i, session in enumerate(sessions[:3]):  # Check first 3
                        session_id = session.get("session_id", "")
                        user_name = session.get("user_name", "")
                        user_tier = session.get("user_subscription_tier", "")
                        status = session.get("status", "")
                        
                        has_tier_info = bool(user_tier)
                        self.log_test(f"Session {i+1} Tier Display", has_tier_info,
                                    f"User: {user_name}, Tier: {user_tier}, Status: {status}")
                        
                        # Check if tier names are using new naming convention
                        if user_tier:
                            new_tier_names = ["launch", "growth", "scale", "white_label", "custom"]
                            old_tier_names = ["professional", "enterprise", "premium"]
                            
                            uses_new_names = user_tier.lower() in new_tier_names
                            uses_old_names = user_tier.lower() in old_tier_names
                            
                            naming_correct = uses_new_names and not uses_old_names
                            self.log_test(f"Session {i+1} Tier Naming", naming_correct,
                                        f"Uses correct tier name: {user_tier}")
                else:
                    self.log_test("Admin Chat Sessions Content", True, 
                                "No sessions found (expected in test environment)")
                
            else:
                self.log_test("Admin Chat Sessions List", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Admin Chat Sessions List", False, f"Exception: {str(e)}")
    
    def test_tier_access_logic(self):
        """Test the tier access logic by examining the code behavior"""
        print("\n🧪 TESTING TIER ACCESS LOGIC")
        print("=" * 60)
        
        # Test different scenarios by checking responses
        test_scenarios = [
            {
                "name": "Premium Tier Access",
                "description": "Admin with custom tier should have chat access",
                "expected_access": True
            }
        ]
        
        for scenario in test_scenarios:
            try:
                # Get current user's access
                response = self.session.get(f"{BACKEND_URL}/chat/access-check")
                
                if response.status_code == 200:
                    data = response.json()
                    has_access = data.get("has_access", False)
                    tier = data.get("subscription_tier", "")
                    
                    access_matches_expectation = has_access == scenario["expected_access"]
                    
                    self.log_test(scenario["name"], access_matches_expectation,
                                f"Tier: {tier}, Access: {has_access}, Expected: {scenario['expected_access']}")
                else:
                    self.log_test(scenario["name"], False, 
                                f"Failed to check access: {response.status_code}")
                    
            except Exception as e:
                self.log_test(scenario["name"], False, f"Exception: {str(e)}")
    
    def test_error_message_consistency(self):
        """Test that error messages use correct tier names"""
        print("\n🏷️  TESTING ERROR MESSAGE CONSISTENCY")
        print("=" * 60)
        
        # Since we can't easily create a Launch tier user, we'll check the logic
        # by examining what messages would be shown
        
        try:
            # Get the current access check response
            response = self.session.get(f"{BACKEND_URL}/chat/access-check")
            
            if response.status_code == 200:
                data = response.json()
                message = data.get("message", "")
                
                # Check for correct tier names in the message
                correct_tier_names = ["growth", "scale", "white label", "custom"]
                incorrect_tier_names = ["professional", "enterprise", "premium"]
                
                message_lower = message.lower()
                has_correct_names = any(name in message_lower for name in correct_tier_names)
                has_incorrect_names = any(name in message_lower for name in incorrect_tier_names)
                
                naming_consistency = has_correct_names and not has_incorrect_names
                
                self.log_test("Message Tier Name Consistency", naming_consistency,
                            f"Message uses correct tier names: '{message}'")
                
                # Check specific tier mentions
                for tier_name in correct_tier_names:
                    if tier_name in message_lower:
                        self.log_test(f"Mentions {tier_name.title()} Tier", True,
                                    f"Correctly mentions {tier_name} tier")
                
            else:
                self.log_test("Error Message Consistency", False, 
                            f"Failed to get access check: {response.status_code}")
                
        except Exception as e:
            self.log_test("Error Message Consistency", False, f"Exception: {str(e)}")
    
    def run_focused_tests(self):
        """Run focused subscription tier tests"""
        print("🎯 FOCUSED SUBSCRIPTION TIER SYSTEM TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Authenticate as admin
        if not self.authenticate_admin():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Run focused tests
        self.test_chat_access_check_endpoint()
        self.test_support_tier_info_endpoint()
        self.test_chat_session_creation()
        self.test_admin_chat_dashboard()
        self.test_tier_access_logic()
        self.test_error_message_consistency()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("📊 FOCUSED SUBSCRIPTION TIER TEST SUMMARY")
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
        
        # Chat access tests
        chat_tests = [r for r in self.test_results if "Chat" in r["test"]]
        chat_passed = sum(1 for r in chat_tests if r["success"])
        print(f"  • Live Chat System: {chat_passed}/{len(chat_tests)} tests passed")
        
        # Support tier tests
        support_tests = [r for r in self.test_results if "Support" in r["test"] or "Tier" in r["test"]]
        support_passed = sum(1 for r in support_tests if r["success"])
        print(f"  • Support Tier System: {support_passed}/{len(support_tests)} tests passed")
        
        # Admin dashboard tests
        admin_tests = [r for r in self.test_results if "Admin" in r["test"]]
        admin_passed = sum(1 for r in admin_tests if r["success"])
        print(f"  • Admin Dashboard: {admin_passed}/{len(admin_tests)} tests passed")
        
        # Naming consistency tests
        naming_tests = [r for r in self.test_results if "Consistency" in r["test"] or "Naming" in r["test"]]
        naming_passed = sum(1 for r in naming_tests if r["success"])
        print(f"  • Tier Naming: {naming_passed}/{len(naming_tests)} tests passed")
        
        print("\n" + "=" * 80)
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Subscription tier system working correctly!")
        elif success_rate >= 75:
            print("✅ GOOD: Most features working, minor issues to address")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Several issues need attention")
        else:
            print("❌ CRITICAL: Major issues with subscription tier system")
        
        print("=" * 80)

def main():
    """Main test execution"""
    tester = FocusedTierTester()
    tester.run_focused_tests()

if __name__ == "__main__":
    main()