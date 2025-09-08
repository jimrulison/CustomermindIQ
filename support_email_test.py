#!/usr/bin/env python3
"""
CustomerMind IQ - Support System and Email System Testing
Testing the fixed multi-tier support system and simple email system
"""

import asyncio
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://mindiq-portal.preview.emergentagent.com"
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class SupportEmailSystemTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
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
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def authenticate_admin(self) -> bool:
        """Authenticate as admin user"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "email": ADMIN_EMAIL,
                    "password": ADMIN_PASSWORD
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                self.log_test("Admin Authentication", True, f"Successfully authenticated as {ADMIN_EMAIL}")
                return True
            else:
                self.log_test("Admin Authentication", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {"Authorization": f"Bearer {self.admin_token}"} if self.admin_token else {}

    # =====================================================
    # SUPPORT SYSTEM TESTS
    # =====================================================

    def test_support_tier_info(self):
        """Test support tier information endpoint"""
        try:
            response = requests.get(
                f"{self.base_url}/api/support/tier-info",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["support_tier", "subscription_tier", "tier_info"]
                if all(field in data for field in required_fields):
                    tier_info = data["tier_info"]
                    if "response_time_hours" in tier_info and "live_chat" in tier_info:
                        self.log_test("Support Tier Info", True, 
                                    f"Support tier: {data['support_tier']}, Response time: {tier_info['response_time_hours']}h")
                    else:
                        self.log_test("Support Tier Info", False, "Missing tier_info fields", data)
                else:
                    self.log_test("Support Tier Info", False, "Missing required fields", data)
            else:
                self.log_test("Support Tier Info", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Support Tier Info", False, f"Exception: {str(e)}")

    def test_create_support_ticket(self):
        """Test creating a support ticket"""
        try:
            ticket_data = {
                "subject": "Test Support Ticket - API Testing",
                "message": "This is a test support ticket created during API testing to verify the multi-tier support system functionality.",
                "category": "technical",
                "priority": "medium"
            }
            
            response = requests.post(
                f"{self.base_url}/api/support/tickets/create",
                json=ticket_data,
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success" and "ticket" in data:
                    ticket = data["ticket"]
                    ticket_id = ticket.get("ticket_id")
                    support_tier = ticket.get("support_tier")
                    
                    self.log_test("Create Support Ticket", True, 
                                f"Ticket created: {ticket_id}, Support tier: {support_tier}")
                    
                    # Store ticket ID for later tests
                    self.test_ticket_id = ticket_id
                else:
                    self.log_test("Create Support Ticket", False, "Invalid response structure", data)
            else:
                self.log_test("Create Support Ticket", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Create Support Ticket", False, f"Exception: {str(e)}")

    def test_get_user_tickets(self):
        """Test getting user's support tickets"""
        try:
            response = requests.get(
                f"{self.base_url}/api/support/tickets/my",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "tickets" in data and "total" in data:
                    tickets = data["tickets"]
                    total = data["total"]
                    support_tier = data.get("support_tier")
                    
                    self.log_test("Get User Tickets", True, 
                                f"Retrieved {len(tickets)} tickets (total: {total}), Support tier: {support_tier}")
                else:
                    self.log_test("Get User Tickets", False, "Invalid response structure", data)
            else:
                self.log_test("Get User Tickets", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Get User Tickets", False, f"Exception: {str(e)}")

    def test_admin_tickets_management(self):
        """Test admin ticket management"""
        try:
            response = requests.get(
                f"{self.base_url}/api/support/admin/tickets",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "tickets" in data and "statistics" in data:
                    tickets = data["tickets"]
                    stats = data["statistics"]
                    
                    total_tickets = stats.get("total_tickets", 0)
                    open_tickets = stats.get("open_tickets", 0)
                    
                    self.log_test("Admin Tickets Management", True, 
                                f"Admin view: {len(tickets)} tickets shown, {total_tickets} total, {open_tickets} open")
                else:
                    self.log_test("Admin Tickets Management", False, "Invalid response structure", data)
            else:
                self.log_test("Admin Tickets Management", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Admin Tickets Management", False, f"Exception: {str(e)}")

    # =====================================================
    # EMAIL SYSTEM TESTS
    # =====================================================

    def test_email_provider_current(self):
        """Test getting current email provider configuration"""
        try:
            response = requests.get(
                f"{self.base_url}/api/email/providers/current",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "provider_config" in data and "available_providers" in data:
                    provider_config = data["provider_config"]
                    provider = provider_config.get("provider")
                    from_email = provider_config.get("from_email")
                    
                    self.log_test("Email Provider Current", True, 
                                f"Provider: {provider}, From: {from_email}")
                else:
                    self.log_test("Email Provider Current", False, "Invalid response structure", data)
            else:
                self.log_test("Email Provider Current", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Email Provider Current", False, f"Exception: {str(e)}")

    def test_send_simple_email_all_users(self):
        """Test sending simple email to all users"""
        try:
            email_data = {
                "subject": "Test Email - All Users",
                "html_content": "<h1>Test Email</h1><p>This is a test email sent to all users via the CustomerMind IQ email system.</p>",
                "text_content": "Test Email - This is a test email sent to all users via the CustomerMind IQ email system.",
                "recipient_type": "all_users"
            }
            
            response = requests.post(
                f"{self.base_url}/api/email/send-simple",
                json=email_data,
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    campaign_id = data.get("campaign_id")
                    recipient_count = data.get("recipient_count")
                    provider = data.get("provider")
                    
                    self.log_test("Send Simple Email - All Users", True, 
                                f"Campaign: {campaign_id}, Recipients: {recipient_count}, Provider: {provider}")
                    
                    # Store campaign ID for later tests
                    self.test_campaign_id = campaign_id
                else:
                    self.log_test("Send Simple Email - All Users", False, "Email sending failed", data)
            else:
                self.log_test("Send Simple Email - All Users", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Send Simple Email - All Users", False, f"Exception: {str(e)}")

    def test_send_simple_email_professional_tier(self):
        """Test sending simple email to professional tier"""
        try:
            email_data = {
                "subject": "Test Email - Professional Tier",
                "html_content": "<h1>Professional Tier Email</h1><p>This email is targeted to professional tier subscribers.</p>",
                "recipient_type": "subscription_tier",
                "subscription_tiers": ["professional"]
            }
            
            response = requests.post(
                f"{self.base_url}/api/email/send-simple",
                json=email_data,
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    recipient_count = data.get("recipient_count")
                    self.log_test("Send Simple Email - Professional Tier", True, 
                                f"Professional tier email sent to {recipient_count} recipients")
                else:
                    self.log_test("Send Simple Email - Professional Tier", False, "Email sending failed", data)
            else:
                self.log_test("Send Simple Email - Professional Tier", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Send Simple Email - Professional Tier", False, f"Exception: {str(e)}")

    def test_send_simple_email_enterprise_tier(self):
        """Test sending simple email to enterprise tier"""
        try:
            email_data = {
                "subject": "Test Email - Enterprise Tier",
                "html_content": "<h1>Enterprise Tier Email</h1><p>This email is targeted to enterprise tier subscribers.</p>",
                "recipient_type": "subscription_tier",
                "subscription_tiers": ["enterprise"]
            }
            
            response = requests.post(
                f"{self.base_url}/api/email/send-simple",
                json=email_data,
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    recipient_count = data.get("recipient_count")
                    self.log_test("Send Simple Email - Enterprise Tier", True, 
                                f"Enterprise tier email sent to {recipient_count} recipients")
                else:
                    self.log_test("Send Simple Email - Enterprise Tier", False, "Email sending failed", data)
            else:
                self.log_test("Send Simple Email - Enterprise Tier", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Send Simple Email - Enterprise Tier", False, f"Exception: {str(e)}")

    def test_send_simple_email_custom_list(self):
        """Test sending simple email to custom list"""
        try:
            email_data = {
                "subject": "Test Email - Custom List",
                "html_content": "<h1>Custom List Email</h1><p>This email is sent to a custom list of recipients.</p>",
                "recipient_type": "custom_list",
                "custom_emails": ["admin@customermindiq.com", "test@example.com"]
            }
            
            response = requests.post(
                f"{self.base_url}/api/email/send-simple",
                json=email_data,
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    recipient_count = data.get("recipient_count")
                    self.log_test("Send Simple Email - Custom List", True, 
                                f"Custom list email sent to {recipient_count} recipients")
                else:
                    self.log_test("Send Simple Email - Custom List", False, "Email sending failed", data)
            else:
                self.log_test("Send Simple Email - Custom List", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Send Simple Email - Custom List", False, f"Exception: {str(e)}")

    def test_send_simple_email_single_user(self):
        """Test sending simple email to single user"""
        try:
            email_data = {
                "subject": "Test Email - Single User",
                "html_content": "<h1>Single User Email</h1><p>This email is sent to a single user.</p>",
                "recipient_type": "single_user",
                "single_email": "admin@customermindiq.com"
            }
            
            response = requests.post(
                f"{self.base_url}/api/email/send-simple",
                json=email_data,
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    recipient_count = data.get("recipient_count")
                    self.log_test("Send Simple Email - Single User", True, 
                                f"Single user email sent to {recipient_count} recipient")
                else:
                    self.log_test("Send Simple Email - Single User", False, "Email sending failed", data)
            else:
                self.log_test("Send Simple Email - Single User", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Send Simple Email - Single User", False, f"Exception: {str(e)}")

    def test_email_campaigns(self):
        """Test getting email campaigns"""
        try:
            response = requests.get(
                f"{self.base_url}/api/email/campaigns",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "campaigns" in data and "total" in data:
                    campaigns = data["campaigns"]
                    total = data["total"]
                    
                    self.log_test("Email Campaigns", True, 
                                f"Retrieved {len(campaigns)} campaigns (total: {total})")
                else:
                    self.log_test("Email Campaigns", False, "Invalid response structure", data)
            else:
                self.log_test("Email Campaigns", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Email Campaigns", False, f"Exception: {str(e)}")

    def test_email_stats(self):
        """Test getting email statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/api/email/stats",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "statistics" in data:
                    stats = data["statistics"]
                    total_campaigns = stats.get("total_campaigns", 0)
                    total_sent = stats.get("total_emails_sent", 0)
                    delivery_rate = stats.get("delivery_rate_percent", 0)
                    
                    self.log_test("Email Statistics", True, 
                                f"Campaigns: {total_campaigns}, Sent: {total_sent}, Delivery rate: {delivery_rate}%")
                else:
                    self.log_test("Email Statistics", False, "Invalid response structure", data)
            else:
                self.log_test("Email Statistics", False, f"Status: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Email Statistics", False, f"Exception: {str(e)}")

    # =====================================================
    # INTEGRATION TESTS
    # =====================================================

    def test_integration_admin_access(self):
        """Test that admin can access both support and email systems"""
        try:
            # Test support system access
            support_response = requests.get(
                f"{self.base_url}/api/support/admin/tickets",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            # Test email system access
            email_response = requests.get(
                f"{self.base_url}/api/email/campaigns",
                headers=self.get_auth_headers(),
                timeout=30
            )
            
            support_ok = support_response.status_code == 200
            email_ok = email_response.status_code == 200
            
            if support_ok and email_ok:
                self.log_test("Integration - Admin Access", True, 
                            "Admin can access both support and email systems")
            else:
                self.log_test("Integration - Admin Access", False, 
                            f"Support: {support_response.status_code}, Email: {email_response.status_code}")
                
        except Exception as e:
            self.log_test("Integration - Admin Access", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all support and email system tests"""
        print("🚀 STARTING SUPPORT SYSTEM AND EMAIL SYSTEM TESTING")
        print("=" * 60)
        print()
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ CRITICAL: Admin authentication failed. Cannot proceed with tests.")
            return
        
        print("📋 TESTING SUPPORT SYSTEM ENDPOINTS")
        print("-" * 40)
        
        # Support System Tests
        self.test_support_tier_info()
        self.test_create_support_ticket()
        self.test_get_user_tickets()
        self.test_admin_tickets_management()
        
        print("📧 TESTING EMAIL SYSTEM ENDPOINTS")
        print("-" * 40)
        
        # Email System Tests
        self.test_email_provider_current()
        self.test_send_simple_email_all_users()
        self.test_send_simple_email_professional_tier()
        self.test_send_simple_email_enterprise_tier()
        self.test_send_simple_email_custom_list()
        self.test_send_simple_email_single_user()
        self.test_email_campaigns()
        self.test_email_stats()
        
        print("🔗 TESTING INTEGRATION")
        print("-" * 40)
        
        # Integration Tests
        self.test_integration_admin_access()
        
        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate test summary"""
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results
        support_tests = [r for r in self.test_results if "Support" in r["test"] or "support" in r["test"].lower()]
        email_tests = [r for r in self.test_results if "Email" in r["test"] or "email" in r["test"].lower()]
        integration_tests = [r for r in self.test_results if "Integration" in r["test"]]
        
        print("📋 SUPPORT SYSTEM RESULTS:")
        support_passed = sum(1 for r in support_tests if r["success"])
        print(f"   {support_passed}/{len(support_tests)} tests passed ({support_passed/len(support_tests)*100:.1f}%)")
        
        print("📧 EMAIL SYSTEM RESULTS:")
        email_passed = sum(1 for r in email_tests if r["success"])
        print(f"   {email_passed}/{len(email_tests)} tests passed ({email_passed/len(email_tests)*100:.1f}%)")
        
        print("🔗 INTEGRATION RESULTS:")
        integration_passed = sum(1 for r in integration_tests if r["success"])
        print(f"   {integration_passed}/{len(integration_tests)} tests passed ({integration_passed/len(integration_tests)*100:.1f}%)")
        
        print()
        
        # Show failed tests
        failed_tests_list = [r for r in self.test_results if not r["success"]]
        if failed_tests_list:
            print("❌ FAILED TESTS:")
            for test in failed_tests_list:
                print(f"   - {test['test']}: {test['details']}")
        else:
            print("✅ ALL TESTS PASSED!")
        
        print()
        print("🎯 TESTING OBJECTIVES STATUS:")
        
        # Check specific objectives from review request
        objectives = {
            "Support tier mapping with correct enum values": any("Support Tier Info" in r["test"] and r["success"] for r in self.test_results),
            "Create support ticket functionality": any("Create Support Ticket" in r["test"] and r["success"] for r in self.test_results),
            "Get user tickets": any("Get User Tickets" in r["test"] and r["success"] for r in self.test_results),
            "Admin ticket management": any("Admin Tickets Management" in r["test"] and r["success"] for r in self.test_results),
            "Email provider configuration": any("Email Provider Current" in r["test"] and r["success"] for r in self.test_results),
            "Send simple email functionality": any("Send Simple Email" in r["test"] and r["success"] for r in self.test_results),
            "Email campaigns management": any("Email Campaigns" in r["test"] and r["success"] for r in self.test_results),
            "Email statistics": any("Email Statistics" in r["test"] and r["success"] for r in self.test_results),
            "Admin authentication for both systems": any("Integration - Admin Access" in r["test"] and r["success"] for r in self.test_results)
        }
        
        for objective, status in objectives.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {objective}")
        
        print()
        print("=" * 60)

if __name__ == "__main__":
    tester = SupportEmailSystemTester()
    tester.run_all_tests()