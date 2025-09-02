#!/usr/bin/env python3
"""
CustomerMind IQ - Complete Customer Communication Workflow Testing
Testing Support Ticket System + Email System Integration

Test Objectives:
1. Complete Support Ticket Cycle (Create → Admin Response → Customer Reply)
2. Simple Email System Demonstration (All Users, Subscription Tier, Custom)
3. Integrated Communication Management (Admin Dashboard Integration)
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
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://mind-iq-dashboard.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

# Test user credentials (will create if needed)
TEST_USER_CREDENTIALS = {
    "email": "testcustomer@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "Customer",
    "company": "Test Company"
}

class CustomerCommunicationTester:
    def __init__(self):
        self.admin_token = None
        self.user_token = None
        self.test_ticket_id = None
        self.test_campaign_id = None
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
        """Test authentication for both admin and regular user"""
        print("🔐 TESTING AUTHENTICATION SETUP")
        print("=" * 50)
        
        # Test admin login
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
        
        # Test user registration/login
        try:
            # Try to register test user first
            response = requests.post(f"{API_BASE}/auth/register", json=TEST_USER_CREDENTIALS, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                self.user_token = data.get("access_token")
                self.log_result(
                    "Test User Registration", 
                    True, 
                    f"User registered successfully, tier: {data.get('user', {}).get('subscription_tier', 'unknown')}"
                )
            else:
                # User might already exist, try login
                login_data = {
                    "email": TEST_USER_CREDENTIALS["email"],
                    "password": TEST_USER_CREDENTIALS["password"]
                }
                response = requests.post(f"{API_BASE}/auth/login", json=login_data, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    self.user_token = data.get("access_token")
                    self.log_result(
                        "Test User Login", 
                        True, 
                        f"User login successful, tier: {data.get('user', {}).get('subscription_tier', 'unknown')}"
                    )
                else:
                    self.log_result(
                        "Test User Authentication", 
                        False, 
                        f"Registration failed ({response.status_code}), login also failed", 
                        response.text
                    )
                    return False
        except Exception as e:
            self.log_result("Test User Authentication", False, f"Exception: {str(e)}")
            return False
        
        return True

    async def test_support_ticket_creation(self):
        """Test customer creating support ticket"""
        print("🎫 TESTING SUPPORT TICKET CREATION")
        print("=" * 50)
        
        if not self.user_token:
            self.log_result("Support Ticket Creation", False, "No user token available")
            return False
        
        ticket_data = {
            "subject": "Test Support Request - Communication Workflow",
            "message": "This is a test support ticket to verify the complete customer communication workflow. Please respond to test the admin response functionality.",
            "category": "technical",
            "priority": "medium"
        }
        
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        try:
            response = requests.post(f"{API_BASE}/support/tickets/create", json=ticket_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success" and data.get("ticket"):
                    self.test_ticket_id = data["ticket"]["ticket_id"]
                    support_tier = data["ticket"]["support_tier"]
                    due_date = data["ticket"]["due_date"]
                    self.log_result(
                        "Support Ticket Creation", 
                        True, 
                        f"Ticket created: {self.test_ticket_id[:8]}..., Support tier: {support_tier}, Due: {due_date}"
                    )
                    return True
                else:
                    self.log_result("Support Ticket Creation", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Support Ticket Creation", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Support Ticket Creation", False, f"Exception: {str(e)}")
            return False

    async def test_admin_view_tickets(self):
        """Test admin viewing support tickets"""
        print("👨‍💼 TESTING ADMIN TICKET VIEWING")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Admin View Tickets", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/support/admin/tickets", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                tickets = data.get("tickets", [])
                stats = data.get("statistics", {})
                
                # Check if our test ticket is visible
                test_ticket_found = False
                if self.test_ticket_id:
                    for ticket in tickets:
                        if ticket.get("ticket_id") == self.test_ticket_id:
                            test_ticket_found = True
                            break
                
                self.log_result(
                    "Admin View Tickets", 
                    True, 
                    f"Found {len(tickets)} tickets, Test ticket visible: {test_ticket_found}, Stats: {stats}"
                )
                return True
            else:
                self.log_result("Admin View Tickets", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Admin View Tickets", False, f"Exception: {str(e)}")
            return False

    async def test_admin_respond_to_ticket(self):
        """Test admin responding to support ticket"""
        print("💬 TESTING ADMIN TICKET RESPONSE")
        print("=" * 50)
        
        if not self.admin_token or not self.test_ticket_id:
            self.log_result("Admin Ticket Response", False, "Missing admin token or ticket ID")
            return False
        
        response_data = {
            "message": "Thank you for contacting CustomerMind IQ support. We have received your technical inquiry and our team is reviewing it. We will provide a detailed solution within our SLA timeframe. This is a test response to verify the complete communication workflow.",
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
                        "Admin Ticket Response", 
                        True, 
                        f"Admin response added successfully, Response ID: {response_info.get('response_id', 'unknown')[:8]}..."
                    )
                    return True
                else:
                    self.log_result("Admin Ticket Response", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Admin Ticket Response", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Admin Ticket Response", False, f"Exception: {str(e)}")
            return False

    async def test_customer_reply_to_ticket(self):
        """Test customer replying to support ticket"""
        print("🔄 TESTING CUSTOMER TICKET REPLY")
        print("=" * 50)
        
        if not self.user_token or not self.test_ticket_id:
            self.log_result("Customer Ticket Reply", False, "Missing user token or ticket ID")
            return False
        
        reply_data = {
            "message": "Thank you for the quick response! I have a follow-up question: Can you provide more details about the advanced analytics features? Also, is there documentation available for the API integration? This reply tests the customer response functionality in the communication workflow.",
            "is_internal_note": False
        }
        
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        try:
            response = requests.post(
                f"{API_BASE}/support/tickets/{self.test_ticket_id}/respond", 
                json=reply_data, 
                headers=headers, 
                timeout=60, verify=False
            )
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    response_info = data.get("response", {})
                    self.log_result(
                        "Customer Ticket Reply", 
                        True, 
                        f"Customer reply added successfully, Response ID: {response_info.get('response_id', 'unknown')[:8]}..."
                    )
                    return True
                else:
                    self.log_result("Customer Ticket Reply", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Customer Ticket Reply", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Customer Ticket Reply", False, f"Exception: {str(e)}")
            return False

    async def test_ticket_conversation_history(self):
        """Test viewing complete ticket conversation"""
        print("📜 TESTING TICKET CONVERSATION HISTORY")
        print("=" * 50)
        
        if not self.user_token or not self.test_ticket_id:
            self.log_result("Ticket Conversation History", False, "Missing user token or ticket ID")
            return False
        
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/support/tickets/{self.test_ticket_id}", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                ticket = data.get("ticket", {})
                responses = ticket.get("responses", [])
                
                # Count different types of responses
                customer_responses = [r for r in responses if r.get("created_by_role") != "support_agent"]
                admin_responses = [r for r in responses if r.get("created_by_role") == "support_agent"]
                
                self.log_result(
                    "Ticket Conversation History", 
                    True, 
                    f"Conversation loaded: {len(responses)} total responses ({len(customer_responses)} customer, {len(admin_responses)} admin)"
                )
                return True
            else:
                self.log_result("Ticket Conversation History", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Ticket Conversation History", False, f"Exception: {str(e)}")
            return False

    async def test_email_to_all_users(self):
        """Test sending email to all users"""
        print("📧 TESTING EMAIL TO ALL USERS")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email to All Users", False, "No admin token available")
            return False
        
        email_data = {
            "subject": "CustomerMind IQ - Platform Update Notification",
            "html_content": """
            <h2>Important Platform Update</h2>
            <p>Dear {{ user_name }},</p>
            <p>We're excited to announce new features in CustomerMind IQ that will enhance your customer intelligence capabilities:</p>
            <ul>
                <li>Enhanced Support Ticket System with multi-tier support</li>
                <li>Improved Email Communication Tools</li>
                <li>Advanced Analytics Dashboard</li>
            </ul>
            <p>These updates are now live in your account. Log in to explore the new features!</p>
            <p>Best regards,<br>The CustomerMind IQ Team</p>
            """,
            "text_content": "Dear {{ user_name }}, We have exciting platform updates available. Log in to CustomerMind IQ to explore new features including enhanced support system and improved email tools. Best regards, CustomerMind IQ Team",
            "recipient_type": "all_users",
            "variables": {
                "platform_name": "CustomerMind IQ",
                "update_date": datetime.now().strftime("%B %d, %Y")
            }
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(f"{API_BASE}/email/email/send-simple", json=email_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    self.test_campaign_id = data.get("campaign_id")
                    recipient_count = data.get("recipient_count", 0)
                    provider = data.get("provider", "unknown")
                    self.log_result(
                        "Email to All Users", 
                        True, 
                        f"Email queued for {recipient_count} users, Provider: {provider}, Campaign ID: {self.test_campaign_id[:8] if self.test_campaign_id else 'unknown'}..."
                    )
                    return True
                else:
                    self.log_result("Email to All Users", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Email to All Users", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email to All Users", False, f"Exception: {str(e)}")
            return False

    async def test_email_to_subscription_tier(self):
        """Test sending email to specific subscription tier"""
        print("🎯 TESTING EMAIL TO SUBSCRIPTION TIER")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email to Subscription Tier", False, "No admin token available")
            return False
        
        email_data = {
            "subject": "Exclusive Professional Features - CustomerMind IQ",
            "html_content": """
            <h2>Exclusive Professional Features Available</h2>
            <p>Hello {{ user_name }},</p>
            <p>As a Professional tier customer, you now have access to exclusive features:</p>
            <ul>
                <li>Priority Support with 12-hour response time</li>
                <li>Live Chat Support during business hours</li>
                <li>Advanced Email Campaign Tools</li>
                <li>Enhanced Analytics and Reporting</li>
            </ul>
            <p>Upgrade to Enterprise for even more advanced features including 4-hour support and dedicated customer success manager.</p>
            <p>Thank you for choosing CustomerMind IQ Professional!</p>
            """,
            "text_content": "Hello {{ user_name }}, As a Professional customer, you have access to priority support, live chat, and advanced features. Consider upgrading to Enterprise for even more benefits. Thank you for choosing CustomerMind IQ!",
            "recipient_type": "subscription_tier",
            "subscription_tiers": ["professional"],
            "variables": {
                "tier_name": "Professional",
                "support_hours": "12 hours"
            }
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(f"{API_BASE}/email/email/send-simple", json=email_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    recipient_count = data.get("recipient_count", 0)
                    provider = data.get("provider", "unknown")
                    campaign_id = data.get("campaign_id", "unknown")
                    self.log_result(
                        "Email to Subscription Tier", 
                        True, 
                        f"Email queued for {recipient_count} Professional tier users, Provider: {provider}, Campaign: {campaign_id[:8]}..."
                    )
                    return True
                else:
                    self.log_result("Email to Subscription Tier", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Email to Subscription Tier", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email to Subscription Tier", False, f"Exception: {str(e)}")
            return False

    async def test_email_to_custom_list(self):
        """Test sending email to custom email list"""
        print("📋 TESTING EMAIL TO CUSTOM LIST")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email to Custom List", False, "No admin token available")
            return False
        
        email_data = {
            "subject": "CustomerMind IQ - Custom Communication Test",
            "html_content": """
            <h2>Custom Email Communication Test</h2>
            <p>Dear {{ user_name }},</p>
            <p>This is a test of our custom email list functionality. You're receiving this because your email was specifically selected for this communication.</p>
            <p>Key features being tested:</p>
            <ul>
                <li>Custom recipient targeting</li>
                <li>Personalized content delivery</li>
                <li>Email campaign tracking</li>
            </ul>
            <p>This demonstrates our flexible email system that can target specific users as needed.</p>
            <p>Best regards,<br>CustomerMind IQ Testing Team</p>
            """,
            "text_content": "Dear {{ user_name }}, This is a custom email list test. You're receiving this as part of our targeted communication testing. Best regards, CustomerMind IQ Testing Team",
            "recipient_type": "custom_list",
            "custom_emails": [
                TEST_USER_CREDENTIALS["email"],
                ADMIN_CREDENTIALS["email"]
            ],
            "variables": {
                "test_type": "Custom List",
                "feature": "Targeted Communication"
            }
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            response = requests.post(f"{API_BASE}/email/email/send-simple", json=email_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                if data.get("status") == "success":
                    recipient_count = data.get("recipient_count", 0)
                    provider = data.get("provider", "unknown")
                    campaign_id = data.get("campaign_id", "unknown")
                    self.log_result(
                        "Email to Custom List", 
                        True, 
                        f"Email queued for {recipient_count} custom recipients, Provider: {provider}, Campaign: {campaign_id[:8]}..."
                    )
                    return True
                else:
                    self.log_result("Email to Custom List", False, "Invalid response format", data)
                    return False
            else:
                self.log_result("Email to Custom List", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email to Custom List", False, f"Exception: {str(e)}")
            return False

    async def test_email_campaign_tracking(self):
        """Test email campaign tracking and statistics"""
        print("📊 TESTING EMAIL CAMPAIGN TRACKING")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email Campaign Tracking", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Get email campaigns
            response = requests.get(f"{API_BASE}/email/email/campaigns", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                campaigns = data.get("campaigns", [])
                total_campaigns = data.get("total", 0)
                
                # Get email statistics
                stats_response = requests.get(f"{API_BASE}/email/stats", headers=headers, timeout=60, verify=False)
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    statistics = stats_data.get("statistics", {})
                    
                    self.log_result(
                        "Email Campaign Tracking", 
                        True, 
                        f"Campaigns: {total_campaigns}, Recent campaigns: {len(campaigns)}, Stats: {statistics}"
                    )
                    return True
                else:
                    self.log_result("Email Campaign Tracking", False, f"Stats request failed: {stats_response.status_code}", stats_response.text)
                    return False
            else:
                self.log_result("Email Campaign Tracking", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Email Campaign Tracking", False, f"Exception: {str(e)}")
            return False

    async def test_admin_dashboard_integration(self):
        """Test admin dashboard shows both support and email systems"""
        print("🎛️ TESTING ADMIN DASHBOARD INTEGRATION")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Admin Dashboard Integration", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        try:
            # Test support tickets admin view
            support_response = requests.get(f"{API_BASE}/support/admin/tickets", headers=headers, timeout=60, verify=False)
            support_success = support_response.status_code == 200
            
            # Test email campaigns view
            email_response = requests.get(f"{API_BASE}/email/email/campaigns", headers=headers, timeout=60, verify=False)
            email_success = email_response.status_code == 200
            
            # Test email statistics
            stats_response = requests.get(f"{API_BASE}/email/stats", headers=headers, timeout=60, verify=False)
            stats_success = stats_response.status_code == 200
            
            if support_success and email_success and stats_success:
                support_data = support_response.json()
                email_data = email_response.json()
                stats_data = stats_response.json()
                
                support_stats = support_data.get("statistics", {})
                email_stats = stats_data.get("statistics", {})
                
                self.log_result(
                    "Admin Dashboard Integration", 
                    True, 
                    f"Support: {support_stats.get('total_tickets', 0)} tickets, Email: {email_stats.get('total_campaigns', 0)} campaigns, Both systems accessible"
                )
                return True
            else:
                failed_systems = []
                if not support_success:
                    failed_systems.append(f"Support ({support_response.status_code})")
                if not email_success:
                    failed_systems.append(f"Email ({email_response.status_code})")
                if not stats_success:
                    failed_systems.append(f"Stats ({stats_response.status_code})")
                
                self.log_result("Admin Dashboard Integration", False, f"Failed systems: {', '.join(failed_systems)}")
                return False
        except Exception as e:
            self.log_result("Admin Dashboard Integration", False, f"Exception: {str(e)}")
            return False

    async def test_support_tier_info(self):
        """Test support tier information endpoint"""
        print("ℹ️ TESTING SUPPORT TIER INFORMATION")
        print("=" * 50)
        
        if not self.user_token:
            self.log_result("Support Tier Information", False, "No user token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        try:
            response = requests.get(f"{API_BASE}/support/tier-info", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                support_tier = data.get("support_tier")
                subscription_tier = data.get("subscription_tier")
                tier_info = data.get("tier_info", {})
                
                self.log_result(
                    "Support Tier Information", 
                    True, 
                    f"Support tier: {support_tier}, Subscription: {subscription_tier}, Response time: {tier_info.get('response_time_hours', 'unknown')}h"
                )
                return True
            else:
                self.log_result("Support Tier Information", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Support Tier Information", False, f"Exception: {str(e)}")
            return False

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎯 CUSTOMER COMMUNICATION WORKFLOW TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print()
        
        # Group results by workflow
        workflows = {
            "🔐 Authentication Setup": ["Admin Authentication", "Test User Registration", "Test User Login"],
            "🎫 Support Ticket Workflow": [
                "Support Ticket Creation", "Admin View Tickets", "Admin Ticket Response", 
                "Customer Ticket Reply", "Ticket Conversation History", "Support Tier Information"
            ],
            "📧 Email System Workflow": [
                "Email to All Users", "Email to Subscription Tier", "Email to Custom List", "Email Campaign Tracking"
            ],
            "🎛️ Admin Integration": ["Admin Dashboard Integration"]
        }
        
        for workflow_name, test_names in workflows.items():
            print(f"{workflow_name}:")
            workflow_results = [r for r in self.results if r["test"] in test_names]
            workflow_passed = len([r for r in workflow_results if r["success"]])
            workflow_total = len(workflow_results)
            
            for result in workflow_results:
                print(f"  {result['status']}: {result['test']}")
                if result['details']:
                    print(f"      {result['details']}")
            
            if workflow_total > 0:
                workflow_rate = (workflow_passed / workflow_total * 100)
                print(f"  📈 Workflow Success Rate: {workflow_passed}/{workflow_total} ({workflow_rate:.1f}%)")
            print()
        
        # Key findings
        print("🔍 KEY FINDINGS:")
        
        # Support ticket workflow
        support_tests = [r for r in self.results if any(test in r["test"] for test in ["Support", "Ticket", "Admin View", "Admin Ticket Response", "Customer Ticket Reply"])]
        support_success = all(r["success"] for r in support_tests)
        
        if support_success:
            print("  ✅ Complete Support Ticket Cycle: Customer Create → Admin Response → Customer Reply ✅")
        else:
            failed_support = [r["test"] for r in support_tests if not r["success"]]
            print(f"  ❌ Support Ticket Cycle Issues: {', '.join(failed_support)}")
        
        # Email system workflow
        email_tests = [r for r in self.results if "Email" in r["test"]]
        email_success = all(r["success"] for r in email_tests)
        
        if email_success:
            print("  ✅ Simple Email System: All Users, Subscription Tier, Custom List ✅")
        else:
            failed_email = [r["test"] for r in email_tests if not r["success"]]
            print(f"  ❌ Email System Issues: {', '.join(failed_email)}")
        
        # Integration
        integration_tests = [r for r in self.results if "Integration" in r["test"] or "Dashboard" in r["test"]]
        integration_success = all(r["success"] for r in integration_tests)
        
        if integration_success:
            print("  ✅ Admin Dashboard Integration: Both Support & Email Systems Accessible ✅")
        else:
            print("  ❌ Admin Dashboard Integration Issues")
        
        print()
        print("🎉 WORKFLOW VERIFICATION:")
        
        if support_success and email_success and integration_success:
            print("  ✅ COMPLETE SUCCESS: All customer communication workflows operational!")
            print("  ✅ Admin has complete control over customer communications")
            print("  ✅ Multi-channel support (reactive tickets + proactive emails) working")
            print("  ✅ Simple email methods working as requested")
        else:
            print("  ⚠️  Some workflows need attention - see failed tests above")
        
        print("\n" + "=" * 80)
        
        return success_rate >= 80  # Consider 80%+ as overall success

async def main():
    """Run complete customer communication workflow tests"""
    print("🚀 STARTING CUSTOMER COMMUNICATION WORKFLOW TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📡 API Base: {API_BASE}")
    print("=" * 80)
    
    tester = CustomerCommunicationTester()
    
    # Run all tests in sequence
    test_sequence = [
        tester.test_authentication_setup,
        tester.test_support_ticket_creation,
        tester.test_admin_view_tickets,
        tester.test_admin_respond_to_ticket,
        tester.test_customer_reply_to_ticket,
        tester.test_ticket_conversation_history,
        tester.test_support_tier_info,
        tester.test_email_to_all_users,
        tester.test_email_to_subscription_tier,
        tester.test_email_to_custom_list,
        tester.test_email_campaign_tracking,
        tester.test_admin_dashboard_integration
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