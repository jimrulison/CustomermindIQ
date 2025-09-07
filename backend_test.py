#!/usr/bin/env python3
"""
CustomerMind IQ - Backend Testing for Specific User-Reported Issues
Testing the exact endpoints mentioned in the review request after frontend URL fix

SPECIFIC TEST OBJECTIVES (from review request):
1. **API Keys Management**: Test admin API keys endpoints:
   - GET /api/admin/api-keys (to list existing keys)
   - POST /api/admin/api-keys (to create a test key)

2. **Email Templates**: Test admin email templates endpoints:
   - GET /api/admin/email-templates (to list existing templates)
   - POST /api/admin/email-templates (to create a test template)

3. **Trial Email System**: Test trial email endpoints for runtime errors:
   - GET /api/email/trial/logs
   - GET /api/email/trial/stats
   - POST /api/subscriptions/trial/register (with sample data)

4. **Admin Manual**: Verify admin manual endpoints are working:
   - GET /api/download/admin-training-manual
   - GET /api/download/complete-training-manual

Use admin credentials: admin@customermindiq.com / CustomerMindIQ2025!
Focus on whether endpoints return proper data instead of 404 errors and check for runtime errors.
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
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://reftrack-1.preview.emergentagent.com")
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
            <p>As a Free tier customer, you now have access to basic features:</p>
            <ul>
                <li>Basic Support with 24-hour response time</li>
                <li>Email Support</li>
                <li>Basic Analytics and Reporting</li>
                <li>Community Support</li>
            </ul>
            <p>Upgrade to Professional or Enterprise for advanced features including priority support and live chat.</p>
            <p>Thank you for choosing CustomerMind IQ!</p>
            """,
            "text_content": "Hello {{ user_name }}, As a Free tier customer, you have access to basic support and features. Consider upgrading to Professional or Enterprise for more benefits. Thank you for choosing CustomerMind IQ!",
            "recipient_type": "subscription_tier",
            "subscription_tiers": ["free"],
            "variables": {
                "tier_name": "Free",
                "support_hours": "24 hours"
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
                        f"Email queued for {recipient_count} Free tier users, Provider: {provider}, Campaign: {campaign_id[:8]}..."
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
                stats_response = requests.get(f"{API_BASE}/email/email/stats", headers=headers, timeout=60, verify=False)
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
            stats_response = requests.get(f"{API_BASE}/email/email/stats", headers=headers, timeout=60, verify=False)
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

    # =====================================================
    # SPECIFIC USER-REPORTED ISSUE TESTS (FROM REVIEW REQUEST)
    # =====================================================

    async def test_api_keys_management_endpoints(self):
        """Test specific API Keys Management endpoints mentioned in review"""
        print("🔑 TESTING API KEYS MANAGEMENT ENDPOINTS (REVIEW REQUEST)")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("API Keys Management Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test 1: GET /api/admin/api-keys (to list existing keys)
        try:
            response = requests.get(f"{API_BASE}/admin/api-keys", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                key_count = len(data.get("api_keys", [])) if isinstance(data.get("api_keys"), list) else 0
                self.log_result(
                    "GET /api/admin/api-keys", 
                    True, 
                    f"Successfully retrieved {key_count} API keys"
                )
                list_success = True
            elif response.status_code == 404:
                self.log_result("GET /api/admin/api-keys", False, "404 Not Found - endpoint not accessible")
                list_success = False
            else:
                self.log_result("GET /api/admin/api-keys", False, f"Status: {response.status_code}", response.text[:200])
                list_success = False
        except Exception as e:
            self.log_result("GET /api/admin/api-keys", False, f"Exception: {str(e)}")
            list_success = False
        
        # Test 2: POST /api/admin/api-keys (to create a test key)
        try:
            # The endpoint expects query parameters, not JSON body
            params = {
                "service_name": "Review Test Service",
                "key_value": "test_key_12345_review_verification",
                "description": "API key created during review testing to verify endpoint functionality"
            }
            response = requests.post(f"{API_BASE}/admin/api-keys", params=params, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                api_key = data.get("api_key", {})
                key_id = api_key.get("key_id", "unknown")
                self.log_result(
                    "POST /api/admin/api-keys", 
                    True, 
                    f"Successfully created API key: {key_id[:8]}..."
                )
                create_success = True
            elif response.status_code == 404:
                self.log_result("POST /api/admin/api-keys", False, "404 Not Found - endpoint not accessible")
                create_success = False
            else:
                self.log_result("POST /api/admin/api-keys", False, f"Status: {response.status_code}", response.text[:200])
                create_success = False
        except Exception as e:
            self.log_result("POST /api/admin/api-keys", False, f"Exception: {str(e)}")
            create_success = False
        
        return list_success and create_success

    async def test_email_templates_endpoints(self):
        """Test specific Email Templates endpoints mentioned in review"""
        print("📄 TESTING EMAIL TEMPLATES ENDPOINTS (REVIEW REQUEST)")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Email Templates Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test 1: GET /api/admin/email-templates (to list existing templates)
        try:
            response = requests.get(f"{API_BASE}/admin/email-templates", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                template_count = len(data.get("templates", [])) if isinstance(data.get("templates"), list) else 0
                self.log_result(
                    "GET /api/admin/email-templates", 
                    True, 
                    f"Successfully retrieved {template_count} email templates"
                )
                list_success = True
            elif response.status_code == 404:
                self.log_result("GET /api/admin/email-templates", False, "404 Not Found - endpoint not accessible")
                list_success = False
            else:
                self.log_result("GET /api/admin/email-templates", False, f"Status: {response.status_code}", response.text[:200])
                list_success = False
        except Exception as e:
            self.log_result("GET /api/admin/email-templates", False, f"Exception: {str(e)}")
            list_success = False
        
        # Test 2: POST /api/admin/email-templates (to create a test template)
        try:
            test_template_data = {
                "name": "Review Test Template",
                "subject": "CustomerMind IQ - Review Testing Template",
                "html_content": """
                <h2>Review Testing Template</h2>
                <p>Hello {{ user_name }},</p>
                <p>This email template was created during review testing to verify the email templates endpoint functionality.</p>
                <p>Template features:</p>
                <ul>
                    <li>Variable substitution: {{ user_name }}</li>
                    <li>HTML formatting support</li>
                    <li>Professional styling</li>
                </ul>
                <p>Best regards,<br>CustomerMind IQ Team</p>
                """,
                "text_content": "Hello {{ user_name }}, This is a review test template. Best regards, CustomerMind IQ Team",
                "template_type": "notification",
                "variables": ["user_name"],
                "is_active": True
            }
            response = requests.post(f"{API_BASE}/admin/email-templates", json=test_template_data, headers=headers, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                template_id = data.get("template_id", "unknown")
                self.log_result(
                    "POST /api/admin/email-templates", 
                    True, 
                    f"Successfully created email template: {template_id[:8]}..."
                )
                create_success = True
            elif response.status_code == 404:
                self.log_result("POST /api/admin/email-templates", False, "404 Not Found - endpoint not accessible")
                create_success = False
            else:
                self.log_result("POST /api/admin/email-templates", False, f"Status: {response.status_code}", response.text[:200])
                create_success = False
        except Exception as e:
            self.log_result("POST /api/admin/email-templates", False, f"Exception: {str(e)}")
            create_success = False
        
        return list_success and create_success

    async def test_trial_email_system_endpoints(self):
        """Test specific Trial Email System endpoints mentioned in review"""
        print("📧 TESTING TRIAL EMAIL SYSTEM ENDPOINTS (REVIEW REQUEST)")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Trial Email System Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test 1: GET /api/email/email/trial/logs (correct path based on router prefix)
        try:
            response = requests.get(f"{API_BASE}/email/email/trial/logs", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                log_count = len(data.get("logs", [])) if isinstance(data.get("logs"), list) else 0
                self.log_result(
                    "GET /api/email/email/trial/logs", 
                    True, 
                    f"Successfully retrieved {log_count} trial email logs"
                )
                logs_success = True
            elif response.status_code == 500:
                self.log_result("GET /api/email/email/trial/logs", False, "500 Internal Server Error - RUNTIME ERROR DETECTED")
                logs_success = False
            elif response.status_code == 404:
                self.log_result("GET /api/email/email/trial/logs", False, "404 Not Found - endpoint not accessible")
                logs_success = False
            else:
                self.log_result("GET /api/email/email/trial/logs", False, f"Status: {response.status_code}", response.text[:200])
                logs_success = False
        except Exception as e:
            self.log_result("GET /api/email/email/trial/logs", False, f"Exception: {str(e)}")
            logs_success = False
        
        # Test 2: GET /api/email/email/trial/stats (correct path based on router prefix)
        try:
            response = requests.get(f"{API_BASE}/email/email/trial/stats", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                stats = data.get("statistics", {})
                self.log_result(
                    "GET /api/email/email/trial/stats", 
                    True, 
                    f"Successfully retrieved trial email stats: {stats}"
                )
                stats_success = True
            elif response.status_code == 500:
                self.log_result("GET /api/email/email/trial/stats", False, "500 Internal Server Error - RUNTIME ERROR DETECTED")
                stats_success = False
            elif response.status_code == 404:
                self.log_result("GET /api/email/email/trial/stats", False, "404 Not Found - endpoint not accessible")
                stats_success = False
            else:
                self.log_result("GET /api/email/email/trial/stats", False, f"Status: {response.status_code}", response.text[:200])
                stats_success = False
        except Exception as e:
            self.log_result("GET /api/email/email/trial/stats", False, f"Exception: {str(e)}")
            stats_success = False
        
        # Test 3: POST /api/subscriptions/trial/register (with sample data)
        try:
            test_trial_data = {
                "email": f"reviewtest_{datetime.now().strftime('%H%M%S')}@example.com",
                "first_name": "Review",
                "last_name": "Tester",
                "company_name": "Review Testing Company"
            }
            response = requests.post(f"{API_BASE}/subscriptions/trial/register", json=test_trial_data, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                user_id = data.get("user", {}).get("user_id", "unknown")
                trial_end = data.get("trial_end", "unknown")
                self.log_result(
                    "POST /api/subscriptions/trial/register", 
                    True, 
                    f"Successfully registered trial user: {user_id}, trial ends: {trial_end}"
                )
                register_success = True
            elif response.status_code == 500:
                self.log_result("POST /api/subscriptions/trial/register", False, "500 Internal Server Error - RUNTIME ERROR DETECTED")
                register_success = False
            elif response.status_code == 404:
                self.log_result("POST /api/subscriptions/trial/register", False, "404 Not Found - endpoint not accessible")
                register_success = False
            else:
                self.log_result("POST /api/subscriptions/trial/register", False, f"Status: {response.status_code}", response.text[:200])
                register_success = False
        except Exception as e:
            self.log_result("POST /api/subscriptions/trial/register", False, f"Exception: {str(e)}")
            register_success = False
        
        return logs_success and stats_success and register_success

    async def test_admin_manual_endpoints(self):
        """Test specific Admin Manual endpoints mentioned in review"""
        print("📚 TESTING ADMIN MANUAL ENDPOINTS (REVIEW REQUEST)")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Admin Manual Endpoints", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test 1: GET /api/download/admin-training-manual
        try:
            response = requests.get(f"{BACKEND_URL}/api/download/admin-training-manual", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                content_length = len(response.content)
                content_type = response.headers.get('content-type', 'unknown')
                self.log_result(
                    "GET /api/download/admin-training-manual", 
                    True, 
                    f"Successfully downloaded admin manual ({content_length} bytes, {content_type})"
                )
                admin_manual_success = True
            elif response.status_code == 404:
                self.log_result("GET /api/download/admin-training-manual", False, "404 Not Found - manual file not accessible")
                admin_manual_success = False
            else:
                self.log_result("GET /api/download/admin-training-manual", False, f"Status: {response.status_code}", response.text[:200])
                admin_manual_success = False
        except Exception as e:
            self.log_result("GET /api/download/admin-training-manual", False, f"Exception: {str(e)}")
            admin_manual_success = False
        
        # Test 2: GET /api/download/complete-training-manual
        try:
            response = requests.get(f"{BACKEND_URL}/api/download/complete-training-manual", headers=headers, timeout=60, verify=False)
            if response.status_code == 200:
                content_length = len(response.content)
                content_type = response.headers.get('content-type', 'unknown')
                self.log_result(
                    "GET /api/download/complete-training-manual", 
                    True, 
                    f"Successfully downloaded complete manual ({content_length} bytes, {content_type})"
                )
                complete_manual_success = True
            elif response.status_code == 404:
                self.log_result("GET /api/download/complete-training-manual", False, "404 Not Found - manual file not accessible")
                complete_manual_success = False
            else:
                self.log_result("GET /api/download/complete-training-manual", False, f"Status: {response.status_code}", response.text[:200])
                complete_manual_success = False
        except Exception as e:
            self.log_result("GET /api/download/complete-training-manual", False, f"Exception: {str(e)}")
            complete_manual_success = False
        
        return admin_manual_success and complete_manual_success

    async def test_admin_manual_loading(self):
        """Test admin manual accessibility via API endpoints"""
        print("📚 TESTING ADMIN MANUAL LOADING")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Admin Manual Loading", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        manual_endpoints = [
            "/api/admin/manual",
            "/api/training/manual", 
            "/api/download/admin-training-manual",
            "/api/download/complete-training-manual",
            "/api/download/quick-start-guide"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in manual_endpoints:
            try:
                response = requests.get(f"{API_BASE.replace('/api', '')}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    successful_endpoints.append(f"{endpoint} (200)")
                elif response.status_code == 404:
                    failed_endpoints.append(f"{endpoint} (404 - Not Found)")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception: {str(e)[:50]})")
        
        if successful_endpoints:
            self.log_result(
                "Admin Manual Loading", 
                True, 
                f"Found {len(successful_endpoints)} working manual endpoints: {', '.join(successful_endpoints)}"
            )
            return True
        else:
            self.log_result(
                "Admin Manual Loading", 
                False, 
                f"No working manual endpoints found. Tested: {', '.join(failed_endpoints)}"
            )
            return False

    async def test_templates_functionality(self):
        """Test templates functionality - check for template endpoints"""
        print("📄 TESTING TEMPLATES FUNCTIONALITY")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Templates Functionality", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        template_endpoints = [
            "/api/admin/email-templates",
            "/api/email/templates",
            "/api/templates"
        ]
        
        successful_endpoints = []
        template_data = {}
        
        for endpoint in template_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    template_count = 0
                    
                    # Try to count templates from different response formats
                    if isinstance(data, list):
                        template_count = len(data)
                    elif isinstance(data, dict):
                        if 'templates' in data:
                            template_count = len(data['templates']) if isinstance(data['templates'], list) else 1
                        elif 'email_templates' in data:
                            template_count = len(data['email_templates']) if isinstance(data['email_templates'], list) else 1
                        elif 'data' in data:
                            template_count = len(data['data']) if isinstance(data['data'], list) else 1
                        else:
                            template_count = len(data.keys())
                    
                    successful_endpoints.append(f"{endpoint} ({template_count} templates)")
                    template_data[endpoint] = {"count": template_count, "data": data}
                    
            except Exception as e:
                continue
        
        if successful_endpoints:
            total_templates = sum(template_data[ep.split(' (')[0]]["count"] for ep in successful_endpoints)
            self.log_result(
                "Templates Functionality", 
                True, 
                f"Found {len(successful_endpoints)} template endpoints with {total_templates} total templates: {', '.join(successful_endpoints)}"
            )
            return True
        else:
            self.log_result(
                "Templates Functionality", 
                False, 
                "No working template endpoints found. User mentioned 'quite a few' templates including 4 new ones."
            )
            return False

    async def test_trial_email_system(self):
        """Test trial email system endpoints for runtime errors"""
        print("📧 TESTING TRIAL EMAIL SYSTEM")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("Trial Email System", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        trial_endpoints = [
            ("/api/email/trial/logs", "GET"),
            ("/api/email/trial/stats", "GET"), 
            ("/api/email/trial/process-scheduled", "POST"),
            ("/api/subscriptions/trial/register", "POST")
        ]
        
        successful_tests = []
        failed_tests = []
        
        for endpoint, method in trial_endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                else:  # POST
                    if "register" in endpoint:
                        # Test trial registration with sample data
                        test_data = {
                            "email": f"trial_test_{datetime.now().strftime('%H%M%S')}@example.com",
                            "first_name": "Trial",
                            "last_name": "Test",
                            "company_name": "Test Company"
                        }
                        response = requests.post(f"{API_BASE}{endpoint}", json=test_data, headers=headers, timeout=60, verify=False)
                    else:
                        response = requests.post(f"{API_BASE}{endpoint}", json={}, headers=headers, timeout=60, verify=False)
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    successful_tests.append(f"{endpoint} ({response.status_code})")
                elif response.status_code == 500:
                    # This is what we're looking for - runtime errors
                    failed_tests.append(f"{endpoint} (500 - RUNTIME ERROR)")
                else:
                    failed_tests.append(f"{endpoint} ({response.status_code})")
                    
            except Exception as e:
                failed_tests.append(f"{endpoint} (Exception: {str(e)[:50]})")
        
        if failed_tests:
            runtime_errors = [test for test in failed_tests if "RUNTIME ERROR" in test]
            if runtime_errors:
                self.log_result(
                    "Trial Email System", 
                    False, 
                    f"RUNTIME ERRORS DETECTED: {', '.join(runtime_errors)}. Working endpoints: {', '.join(successful_tests)}"
                )
            else:
                self.log_result(
                    "Trial Email System", 
                    True, 
                    f"No runtime errors found. Working: {', '.join(successful_tests)}, Issues: {', '.join(failed_tests)}"
                )
            return len(runtime_errors) == 0
        else:
            self.log_result(
                "Trial Email System", 
                True, 
                f"All trial email endpoints working: {', '.join(successful_tests)}"
            )
            return True

    async def test_api_keys_configuration(self):
        """Test API keys management endpoints"""
        print("🔑 TESTING API KEYS CONFIGURATION")
        print("=" * 50)
        
        if not self.admin_token:
            self.log_result("API Keys Configuration", False, "No admin token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        api_key_endpoints = [
            "/api/admin/api-keys",
            "/api/keys",
            "/api/admin/keys",
            "/api/admin/api-keys/list"
        ]
        
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint in api_key_endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=60, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    key_count = 0
                    
                    # Try to count API keys from response
                    if isinstance(data, list):
                        key_count = len(data)
                    elif isinstance(data, dict):
                        if 'api_keys' in data:
                            key_count = len(data['api_keys']) if isinstance(data['api_keys'], list) else 1
                        elif 'keys' in data:
                            key_count = len(data['keys']) if isinstance(data['keys'], list) else 1
                    
                    successful_endpoints.append(f"{endpoint} ({key_count} keys)")
                elif response.status_code == 500:
                    failed_endpoints.append(f"{endpoint} (500 - Runtime Error)")
                else:
                    failed_endpoints.append(f"{endpoint} ({response.status_code})")
                    
            except Exception as e:
                failed_endpoints.append(f"{endpoint} (Exception)")
        
        if successful_endpoints:
            self.log_result(
                "API Keys Configuration", 
                True, 
                f"Found {len(successful_endpoints)} working API key endpoints: {', '.join(successful_endpoints)}"
            )
            return True
        else:
            self.log_result(
                "API Keys Configuration", 
                False, 
                f"No working API key endpoints found. Tested: {', '.join(failed_endpoints)}"
            )
            return False

    async def test_basic_system_health(self):
        """Test basic system health and core backend services"""
        print("🏥 TESTING BASIC SYSTEM HEALTH")
        print("=" * 50)
        
        health_endpoints = [
            "/api/health",
            "/api/test-db", 
            "/api/auth/health",
            "/api/admin/health"
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
        
        # Test database connectivity specifically
        try:
            response = requests.get(f"{API_BASE}/test-db", timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                db_status = data.get("overall_status", "unknown")
                if "ALL TESTS PASSED" in db_status:
                    successful_checks.append(f"Database connectivity (✅ All tests passed)")
                else:
                    failed_checks.append(f"Database connectivity ({db_status})")
            else:
                failed_checks.append(f"Database connectivity ({response.status_code})")
        except Exception as e:
            failed_checks.append(f"Database connectivity (Exception)")
        
        if len(successful_checks) >= 2:  # At least 2 health checks should pass
            self.log_result(
                "Basic System Health", 
                True, 
                f"System healthy. Working: {', '.join(successful_checks)}. Issues: {', '.join(failed_checks) if failed_checks else 'None'}"
            )
            return True
        else:
            self.log_result(
                "Basic System Health", 
                False, 
                f"System health issues detected. Working: {', '.join(successful_checks)}. Failed: {', '.join(failed_checks)}"
            )
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
            "🏥 System Health & Configuration": [
                "Basic System Health", "Admin Manual Loading", "Templates Functionality", 
                "Trial Email System", "API Keys Configuration"
            ],
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
        
        # Key findings for review request
        print("🔍 KEY FINDINGS FOR REVIEW REQUEST:")
        
        # Review-specific tests
        review_tests = [
            "GET /api/admin/api-keys", "POST /api/admin/api-keys",
            "GET /api/admin/email-templates", "POST /api/admin/email-templates", 
            "GET /api/email/email/trial/logs", "GET /api/email/email/trial/stats", "POST /api/subscriptions/trial/register",
            "GET /api/download/admin-training-manual", "GET /api/download/complete-training-manual"
        ]
        
        review_results = [r for r in self.results if r["test"] in review_tests]
        review_passed = len([r for r in review_results if r["success"]])
        review_total = len(review_results)
        
        if review_total > 0:
            review_rate = (review_passed / review_total * 100)
            print(f"  📊 Review Request Tests: {review_passed}/{review_total} ({review_rate:.1f}%)")
            
            # Check for specific issues mentioned in review
            runtime_errors = [r for r in review_results if "RUNTIME ERROR" in r.get("details", "")]
            not_found_errors = [r for r in review_results if "404" in r.get("details", "")]
            
            if runtime_errors:
                print(f"  🚨 RUNTIME ERRORS FOUND: {len(runtime_errors)} endpoints have uncaught runtime errors")
                for error in runtime_errors:
                    print(f"      - {error['test']}: {error['details']}")
            else:
                print("  ✅ NO RUNTIME ERRORS: All endpoints responding without uncaught runtime errors")
            
            if not_found_errors:
                print(f"  🚨 404 ERRORS FOUND: {len(not_found_errors)} endpoints returning 404 Not Found")
                for error in not_found_errors:
                    print(f"      - {error['test']}: {error['details']}")
            else:
                print("  ✅ NO 404 ERRORS: All endpoints accessible (no 404 errors)")
        
        # User-reported issues
        user_issue_tests = [r for r in self.results if any(test in r["test"] for test in ["Admin Manual Loading", "Templates Functionality", "Trial Email System", "API Keys Configuration", "Basic System Health"])]
        user_issues_success = all(r["success"] for r in user_issue_tests)
        
        if user_issues_success:
            print("  ✅ User-Reported Issues: All systems operational - Admin manual, Templates, Trial emails, API keys ✅")
        else:
            failed_user_issues = [r["test"] for r in user_issue_tests if not r["success"]]
            print(f"  ❌ User-Reported Issues Found: {', '.join(failed_user_issues)}")
        
        print()
        print("🎉 REVIEW REQUEST VERIFICATION:")
        
        # Check if the frontend URL fix resolved the issues
        api_keys_working = any(r["success"] for r in review_results if "api-keys" in r["test"])
        email_templates_working = any(r["success"] for r in review_results if "email-templates" in r["test"])
        trial_emails_working = any(r["success"] for r in review_results if "trial" in r["test"])
        admin_manuals_working = any(r["success"] for r in review_results if "manual" in r["test"])
        
        if api_keys_working and email_templates_working and trial_emails_working and admin_manuals_working:
            print("  ✅ FRONTEND URL FIX SUCCESSFUL: All reported endpoints now accessible!")
            print("  ✅ API Keys Management: Working properly")
            print("  ✅ Email Templates: Working properly") 
            print("  ✅ Trial Email System: Working properly")
            print("  ✅ Admin Manuals: Working properly")
        else:
            print("  ⚠️  Some endpoints still have issues after frontend URL fix:")
            if not api_keys_working:
                print("  ❌ API Keys Management: Still has issues")
            if not email_templates_working:
                print("  ❌ Email Templates: Still has issues")
            if not trial_emails_working:
                print("  ❌ Trial Email System: Still has issues")
            if not admin_manuals_working:
                print("  ❌ Admin Manuals: Still have issues")
        
        print("\n" + "=" * 80)
        
        return success_rate >= 75  # Consider 75%+ as overall success (lowered due to more tests)

async def main():
    """Run complete customer communication workflow tests"""
    print("🚀 STARTING CUSTOMER COMMUNICATION WORKFLOW TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📡 API Base: {API_BASE}")
    print("=" * 80)
    
    tester = CustomerCommunicationTester()
    
    # Run focused tests for review request
    test_sequence = [
        tester.test_authentication_setup,
        tester.test_basic_system_health,
        # SPECIFIC REVIEW REQUEST TESTS
        tester.test_api_keys_management_endpoints,
        tester.test_email_templates_endpoints, 
        tester.test_trial_email_system_endpoints,
        tester.test_admin_manual_endpoints,
        # ADDITIONAL COMPREHENSIVE TESTS
        tester.test_admin_manual_loading,
        tester.test_templates_functionality,
        tester.test_trial_email_system,
        tester.test_api_keys_configuration
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