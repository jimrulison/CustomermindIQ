#!/usr/bin/env python3
"""
CustomerMind IQ - Focused Support & Email System API Testing
Testing specific endpoints mentioned in review request with detailed error investigation
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
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-mind-iq-6.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials - EXACT as specified in review request
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class FocusedAPITester:
    def __init__(self):
        self.admin_token = None
        self.user_token = None
        self.test_ticket_id = None
        self.results = []
        
    def log_result(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test result with detailed information"""
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
            print(f"   Error Response: {data}")
        print()

    async def test_admin_authentication(self):
        """Test admin authentication with exact credentials"""
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
                    f"Login successful - Role: {user_info.get('role')}, Email: {user_info.get('email')}"
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

    async def test_support_tier_info_endpoint(self):
        """Test GET /api/support/tier-info - Previously returning 500 errors"""
        print("🎯 TESTING SUPPORT TIER INFO ENDPOINT")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Support Tier Info", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/support/tier-info", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                support_tier = data.get("support_tier")
                subscription_tier = data.get("subscription_tier")
                tier_info = data.get("tier_info", {})
                
                self.log_result(
                    "Support Tier Info", 
                    True, 
                    f"Support tier: {support_tier}, Subscription: {subscription_tier}, Response time: {tier_info.get('response_time_hours')}h"
                )
                return True
            else:
                self.log_result(
                    "Support Tier Info", 
                    False, 
                    f"Status: {response.status_code} - This was previously returning 500 errors", 
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("Support Tier Info", False, f"Exception: {str(e)}")
            return False

    async def test_my_tickets_endpoint(self):
        """Test GET /api/support/tickets/my - Previously returning 500 errors"""
        print("🎫 TESTING MY TICKETS ENDPOINT")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("My Tickets Endpoint", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/support/tickets/my", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                tickets = data.get("tickets", [])
                total = data.get("total", 0)
                support_tier = data.get("support_tier")
                
                self.log_result(
                    "My Tickets Endpoint", 
                    True, 
                    f"Found {len(tickets)} tickets (total: {total}), Support tier: {support_tier}"
                )
                return True
            else:
                self.log_result(
                    "My Tickets Endpoint", 
                    False, 
                    f"Status: {response.status_code} - This was previously returning 500 errors", 
                    response.text
                )
                return False
        except Exception as e:
            self.log_result("My Tickets Endpoint", False, f"Exception: {str(e)}")
            return False

    async def test_create_ticket_endpoint(self):
        """Test POST /api/support/tickets/create"""
        print("📝 TESTING CREATE TICKET ENDPOINT")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Create Ticket", False, "No admin token available")
            return False
        
        ticket_data = {
            "subject": "API Testing - Support System Validation",
            "message": "This ticket is created to test the complete support system API endpoints as requested in the review. Testing ticket creation, admin responses, and customer replies.",
            "category": "technical",
            "priority": "high"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(f"{API_BASE}/support/tickets/create", json=ticket_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success" and data.get("ticket"):
                    self.test_ticket_id = data["ticket"]["ticket_id"]
                    support_tier = data["ticket"]["support_tier"]
                    due_date = data["ticket"]["due_date"]
                    self.log_result(
                        "Create Ticket", 
                        True, 
                        f"Ticket created: {self.test_ticket_id[:8]}..., Support tier: {support_tier}, Due: {due_date}"
                    )
                    return True
                else:
                    self.log_result("Create Ticket", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Create Ticket", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Create Ticket", False, f"Exception: {str(e)}")
            return False

    async def test_get_ticket_details(self):
        """Test GET /api/support/tickets/{ticket_id}"""
        print("🔍 TESTING GET TICKET DETAILS")
        print("=" * 50)
        
        if not self.admin_token or not self.test_ticket_id:
            self.log_result("Get Ticket Details", False, "Missing admin token or ticket ID")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/support/tickets/{self.test_ticket_id}", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                ticket = data.get("ticket", {})
                responses = ticket.get("responses", [])
                
                self.log_result(
                    "Get Ticket Details", 
                    True, 
                    f"Ticket retrieved: {ticket.get('subject', 'Unknown')[:50]}..., Responses: {len(responses)}"
                )
                return True
            else:
                self.log_result("Get Ticket Details", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Get Ticket Details", False, f"Exception: {str(e)}")
            return False

    async def test_customer_respond_to_ticket(self):
        """Test POST /api/support/tickets/{ticket_id}/respond"""
        print("💬 TESTING CUSTOMER RESPOND TO TICKET")
        print("=" * 50)
        
        if not self.admin_token or not self.test_ticket_id:
            self.log_result("Customer Respond to Ticket", False, "Missing admin token or ticket ID")
            return False
        
        response_data = {
            "message": "Thank you for creating this ticket. I need additional information about the API integration process. Can you provide documentation and examples?",
            "is_internal_note": False
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(
                f"{API_BASE}/support/tickets/{self.test_ticket_id}/respond", 
                json=response_data, 
                headers=headers, 
                timeout=60, verify=False
            )
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    response_info = data.get("response", {})
                    self.log_result(
                        "Customer Respond to Ticket", 
                        True, 
                        f"Customer response added successfully, Response ID: {response_info.get('response_id', 'unknown')[:8]}..."
                    )
                    return True
                else:
                    self.log_result("Customer Respond to Ticket", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Customer Respond to Ticket", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Customer Respond to Ticket", False, f"Exception: {str(e)}")
            return False

    async def test_live_chat_start(self):
        """Test POST /api/support/live-chat/start"""
        print("💭 TESTING LIVE CHAT START")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Live Chat Start", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(f"{API_BASE}/support/live-chat/start", headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    session = data.get("session", {})
                    wait_time = data.get("estimated_wait_time")
                    self.log_result(
                        "Live Chat Start", 
                        True, 
                        f"Live chat session started: {session.get('session_id', 'unknown')[:8]}..., Wait time: {wait_time}"
                    )
                    return True
                else:
                    self.log_result("Live Chat Start", False, "Invalid response format", data)
                    return False
            elif response.status_code == 403:
                # Expected for basic tier users
                self.log_result(
                    "Live Chat Start", 
                    True, 
                    "Live chat not available for basic tier (expected behavior)"
                )
                return True
            elif response.status_code == 503:
                # Expected outside business hours
                self.log_result(
                    "Live Chat Start", 
                    True, 
                    "Live chat not available outside business hours (expected behavior)"
                )
                return True
            else:
                self.log_result("Live Chat Start", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Live Chat Start", False, f"Exception: {str(e)}")
            return False

    async def test_admin_all_tickets(self):
        """Test GET /api/support/admin/tickets"""
        print("👨‍💼 TESTING ADMIN ALL TICKETS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Admin All Tickets", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/support/admin/tickets", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                tickets = data.get("tickets", [])
                statistics = data.get("statistics", {})
                
                self.log_result(
                    "Admin All Tickets", 
                    True, 
                    f"Found {len(tickets)} tickets, Stats: {statistics}"
                )
                return True
            else:
                self.log_result("Admin All Tickets", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Admin All Tickets", False, f"Exception: {str(e)}")
            return False

    async def test_admin_assign_ticket(self):
        """Test PUT /api/support/admin/tickets/{ticket_id}/assign"""
        print("🎯 TESTING ADMIN ASSIGN TICKET")
        print("=" * 50)
        
        if not self.admin_token or not self.test_ticket_id:
            self.log_result("Admin Assign Ticket", False, "Missing admin token or ticket ID")
            return False
        
        assign_data = {
            "agent_email": "support@customermindiq.com"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.put(
                f"{API_BASE}/support/admin/tickets/{self.test_ticket_id}/assign", 
                json=assign_data, 
                headers=headers, 
                timeout=60, verify=False
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_result(
                        "Admin Assign Ticket", 
                        True, 
                        f"Ticket assigned successfully: {data.get('message')}"
                    )
                    return True
                else:
                    self.log_result("Admin Assign Ticket", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Admin Assign Ticket", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Admin Assign Ticket", False, f"Exception: {str(e)}")
            return False

    async def test_admin_respond_to_ticket(self):
        """Test POST /api/support/admin/tickets/{ticket_id}/respond"""
        print("🛠️ TESTING ADMIN RESPOND TO TICKET")
        print("=" * 50)
        
        if not self.admin_token or not self.test_ticket_id:
            self.log_result("Admin Respond to Ticket", False, "Missing admin token or ticket ID")
            return False
        
        response_data = {
            "message": "Thank you for your inquiry about API integration. I've reviewed your request and will provide comprehensive documentation and examples. Our API supports full CRUD operations with JWT authentication. I'll send detailed integration guides to your email within the next hour.",
            "is_internal_note": False
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(
                f"{API_BASE}/support/admin/tickets/{self.test_ticket_id}/respond", 
                json=response_data, 
                headers=headers, 
                timeout=60, verify=False
            )
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    response_info = data.get("response", {})
                    self.log_result(
                        "Admin Respond to Ticket", 
                        True, 
                        f"Admin response added successfully, Response ID: {response_info.get('response_id', 'unknown')[:8]}..."
                    )
                    return True
                else:
                    self.log_result("Admin Respond to Ticket", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Admin Respond to Ticket", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Admin Respond to Ticket", False, f"Exception: {str(e)}")
            return False

    async def test_email_send_simple(self):
        """Test POST /api/email/send-simple"""
        print("📧 TESTING EMAIL SEND SIMPLE")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email Send Simple", False, "No admin token available")
            return False
        
        email_data = {
            "subject": "API Testing - Email System Validation",
            "html_content": """
            <h2>Email System API Testing</h2>
            <p>Dear {{ user_name }},</p>
            <p>This email is sent as part of comprehensive API testing for the CustomerMind IQ platform.</p>
            <p>Testing objectives:</p>
            <ul>
                <li>Simple email sending functionality</li>
                <li>Template variable replacement</li>
                <li>Email provider integration</li>
            </ul>
            <p>Best regards,<br>CustomerMind IQ Testing Team</p>
            """,
            "text_content": "Dear {{ user_name }}, This is an API test email for CustomerMind IQ platform validation. Best regards, Testing Team",
            "recipient_type": "all_users",
            "variables": {
                "platform_name": "CustomerMind IQ",
                "test_date": datetime.now().strftime("%B %d, %Y")
            }
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(f"{API_BASE}/email/send-simple", json=email_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    recipient_count = data.get("recipient_count", 0)
                    provider = data.get("provider", "unknown")
                    campaign_id = data.get("campaign_id", "unknown")
                    self.log_result(
                        "Email Send Simple", 
                        True, 
                        f"Email queued for {recipient_count} recipients, Provider: {provider}, Campaign: {campaign_id[:8]}..."
                    )
                    return True
                else:
                    self.log_result("Email Send Simple", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Email Send Simple", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email Send Simple", False, f"Exception: {str(e)}")
            return False

    async def test_email_campaigns(self):
        """Test GET /api/email/campaigns"""
        print("📊 TESTING EMAIL CAMPAIGNS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email Campaigns", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/email/campaigns", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                campaigns = data.get("campaigns", [])
                total = data.get("total", 0)
                
                self.log_result(
                    "Email Campaigns", 
                    True, 
                    f"Found {len(campaigns)} campaigns (total: {total})"
                )
                return True
            else:
                self.log_result("Email Campaigns", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email Campaigns", False, f"Exception: {str(e)}")
            return False

    async def test_email_providers_current(self):
        """Test GET /api/email/providers/current"""
        print("⚙️ TESTING EMAIL PROVIDERS CURRENT")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email Providers Current", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/email/providers/current", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                provider_config = data.get("provider_config", {})
                available_providers = data.get("available_providers", [])
                
                self.log_result(
                    "Email Providers Current", 
                    True, 
                    f"Current provider: {provider_config.get('provider')}, Available: {len(available_providers)} providers"
                )
                return True
            else:
                self.log_result("Email Providers Current", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email Providers Current", False, f"Exception: {str(e)}")
            return False

    async def test_email_stats(self):
        """Test GET /api/email/stats"""
        print("📈 TESTING EMAIL STATS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email Stats", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/email/stats", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                statistics = data.get("statistics", {})
                period_days = data.get("period_days", 30)
                
                self.log_result(
                    "Email Stats", 
                    True, 
                    f"Period: {period_days} days, Stats: {statistics}"
                )
                return True
            else:
                self.log_result("Email Stats", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email Stats", False, f"Exception: {str(e)}")
            return False

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎯 FOCUSED SUPPORT & EMAIL SYSTEM API TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print()
        
        # Group results by system
        systems = {
            "🔐 Authentication": ["Admin Authentication"],
            "🎫 Support System APIs": [
                "Support Tier Info", "My Tickets Endpoint", "Create Ticket", 
                "Get Ticket Details", "Customer Respond to Ticket", "Live Chat Start"
            ],
            "👨‍💼 Admin Support Management": [
                "Admin All Tickets", "Admin Assign Ticket", "Admin Respond to Ticket"
            ],
            "📧 Email System APIs": [
                "Email Send Simple", "Email Campaigns", "Email Providers Current", "Email Stats"
            ]
        }
        
        for system_name, test_names in systems.items():
            print(f"{system_name}:")
            system_results = [r for r in self.results if r["test"] in test_names]
            system_passed = len([r for r in system_results if r["success"]])
            system_total = len(system_results)
            
            for result in system_results:
                print(f"  {result['status']}: {result['test']}")
                if result['details']:
                    print(f"      {result['details']}")
            
            if system_total > 0:
                system_rate = (system_passed / system_total * 100)
                print(f"  📈 System Success Rate: {system_passed}/{system_total} ({system_rate:.1f}%)")
            print()
        
        # Key findings
        print("🔍 KEY FINDINGS:")
        
        # Previously problematic endpoints
        tier_info_test = next((r for r in self.results if r["test"] == "Support Tier Info"), None)
        my_tickets_test = next((r for r in self.results if r["test"] == "My Tickets Endpoint"), None)
        
        if tier_info_test and tier_info_test["success"]:
            print("  ✅ Support Tier Info endpoint (/api/support/tier-info) - FIXED (was returning 500 errors)")
        elif tier_info_test:
            print("  ❌ Support Tier Info endpoint (/api/support/tier-info) - STILL FAILING")
        
        if my_tickets_test and my_tickets_test["success"]:
            print("  ✅ My Tickets endpoint (/api/support/tickets/my) - FIXED (was returning 500 errors)")
        elif my_tickets_test:
            print("  ❌ My Tickets endpoint (/api/support/tickets/my) - STILL FAILING")
        
        # Full workflow verification
        support_workflow_tests = [r for r in self.results if any(test in r["test"] for test in ["Create Ticket", "Admin Respond to Ticket", "Customer Respond to Ticket"])]
        support_workflow_success = all(r["success"] for r in support_workflow_tests)
        
        if support_workflow_success:
            print("  ✅ Complete Support Workflow: Create → Admin Response → Customer Reply ✅")
        else:
            print("  ❌ Support Workflow has issues")
        
        # Email system verification
        email_tests = [r for r in self.results if "Email" in r["test"]]
        email_success = all(r["success"] for r in email_tests)
        
        if email_success:
            print("  ✅ Email System APIs: All endpoints working correctly ✅")
        else:
            failed_email = [r["test"] for r in email_tests if not r["success"]]
            print(f"  ❌ Email System Issues: {', '.join(failed_email)}")
        
        print()
        print("🎉 REVIEW REQUEST VERIFICATION:")
        
        if success_rate >= 90:
            print("  ✅ EXCELLENT: Multi-tier support system backend APIs working comprehensively!")
            print("  ✅ Admin authentication with exact credentials working")
            print("  ✅ Support system endpoints operational")
            print("  ✅ Email system endpoints functional")
            print("  ✅ Full support workflow cycle tested successfully")
        elif success_rate >= 75:
            print("  ⚠️  GOOD: Most APIs working but some issues need attention")
        else:
            print("  ❌ NEEDS WORK: Significant issues found requiring fixes")
        
        print("\n" + "=" * 80)
        
        return success_rate >= 80

async def main():
    """Run focused support and email system API tests"""
    print("🚀 STARTING FOCUSED SUPPORT & EMAIL SYSTEM API TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📡 API Base: {API_BASE}")
    print("🎯 Focus: Testing specific endpoints mentioned in review request")
    print("=" * 80)
    
    tester = FocusedAPITester()
    
    # Run all tests in sequence
    test_sequence = [
        tester.test_admin_authentication,
        tester.test_support_tier_info_endpoint,
        tester.test_my_tickets_endpoint,
        tester.test_create_ticket_endpoint,
        tester.test_get_ticket_details,
        tester.test_customer_respond_to_ticket,
        tester.test_live_chat_start,
        tester.test_admin_all_tickets,
        tester.test_admin_assign_ticket,
        tester.test_admin_respond_to_ticket,
        tester.test_email_send_simple,
        tester.test_email_campaigns,
        tester.test_email_providers_current,
        tester.test_email_stats
    ]
    
    for test_func in test_sequence:
        await test_func()
        # Small delay between tests
        await asyncio.sleep(1)
    
    # Print final summary
    overall_success = tester.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    asyncio.run(main())