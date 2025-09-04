#!/usr/bin/env python3
"""
CustomerMind IQ - Password Reset & Email Logo Integration Testing
Testing the updated functionality with logo integration and password reset

Test Objectives:
1. Password Reset Functionality - POST /api/auth/request-password-reset
2. Updated Email Templates - Verify logo integration in welcome emails
3. Email System Integration - Test email providers and logo embedding
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import urllib3
import time

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-mind-iq-4.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class PasswordResetEmailTester:
    def __init__(self):
        self.admin_token = None
        self.results = []
        self.test_email = "passwordreset@example.com"
        self.trial_email = "trialemail@example.com"
        
    def log_result(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        print(f"     Details: {details}")
        if response_data and not success:
            print(f"     Response: {json.dumps(response_data, indent=2)}")
        print()

    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        url = f"{API_BASE}{endpoint}"
        
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
            
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=default_headers, verify=False, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=default_headers, verify=False, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=default_headers, verify=False, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=default_headers, verify=False, timeout=30)
            else:
                return {"error": f"Unsupported method: {method}", "status_code": 400}
            
            return {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "headers": dict(response.headers)
            }
            
        except requests.exceptions.Timeout:
            return {"error": "Request timeout", "status_code": 408}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection error", "status_code": 503}
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    async def test_admin_authentication(self):
        """Test admin login for accessing admin endpoints"""
        print("🔐 Testing Admin Authentication...")
        
        response = self.make_request("POST", "/auth/login", ADMIN_CREDENTIALS)
        
        if response.get("status_code") == 200 and "access_token" in response.get("data", {}):
            self.admin_token = response["data"]["access_token"]
            user_profile = response["data"].get("user_profile", {})
            
            self.log_result(
                "Admin Authentication",
                True,
                f"Admin login successful. Role: {user_profile.get('role', 'unknown')}, Email: {user_profile.get('email', 'unknown')}",
                {"user_role": user_profile.get("role"), "subscription_tier": user_profile.get("subscription_tier")}
            )
            return True
        else:
            self.log_result(
                "Admin Authentication", 
                False,
                f"Admin login failed. Status: {response.get('status_code')}, Error: {response.get('data', {}).get('detail', 'Unknown error')}",
                response
            )
            return False

    async def test_password_reset_request(self):
        """Test password reset functionality"""
        print("🔒 Testing Password Reset Request...")
        
        # Test password reset request
        reset_data = {"email": self.test_email}
        response = self.make_request("POST", "/auth/request-password-reset", reset_data)
        
        if response.get("status_code") == 200:
            message = response.get("data", {}).get("message", "")
            
            self.log_result(
                "Password Reset Request",
                True,
                f"Password reset request successful. Message: {message}",
                response.get("data")
            )
            
            # Check if email was sent with logo
            await self.verify_password_reset_email_content()
            return True
        else:
            self.log_result(
                "Password Reset Request",
                False,
                f"Password reset failed. Status: {response.get('status_code')}, Error: {response.get('data', {}).get('detail', 'Unknown error')}",
                response
            )
            return False

    async def verify_password_reset_email_content(self):
        """Verify password reset email contains logo and proper branding"""
        print("📧 Verifying Password Reset Email Content...")
        
        # Check email logs to verify content
        if not self.admin_token:
            self.log_result(
                "Password Reset Email Verification",
                False,
                "Cannot verify email content - no admin token",
                None
            )
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.make_request("GET", "/email/email/campaigns", headers=headers)
        
        if response.get("status_code") == 200:
            campaigns = response.get("data", {}).get("campaigns", [])
            
            # Look for password reset emails
            password_reset_campaigns = [
                c for c in campaigns 
                if "password" in c.get("subject", "").lower() or "reset" in c.get("subject", "").lower()
            ]
            
            if password_reset_campaigns:
                latest_campaign = password_reset_campaigns[0]
                html_content = latest_campaign.get("html_content", "")
                
                # Check for logo URL in email content
                logo_url = "https://customer-assets.emergentagent.com/job_customer-mind-iq-4/artifacts/pntu3yqm_Customer%20Mind%20IQ%20logo.png"
                has_logo = logo_url in html_content
                has_branding = "CustomerMind IQ" in html_content or "Customer Mind IQ" in html_content
                
                self.log_result(
                    "Password Reset Email Logo Integration",
                    has_logo and has_branding,
                    f"Logo present: {has_logo}, Branding present: {has_branding}. Subject: {latest_campaign.get('subject', 'N/A')}",
                    {
                        "campaign_id": latest_campaign.get("campaign_id"),
                        "has_logo": has_logo,
                        "has_branding": has_branding,
                        "logo_url_found": logo_url in html_content
                    }
                )
                return has_logo and has_branding
            else:
                self.log_result(
                    "Password Reset Email Verification",
                    False,
                    "No password reset email campaigns found in recent history",
                    {"total_campaigns": len(campaigns)}
                )
                return False
        else:
            self.log_result(
                "Password Reset Email Verification",
                False,
                f"Failed to retrieve email campaigns. Status: {response.get('status_code')}",
                response
            )
            return False

    async def test_trial_user_creation_with_welcome_email(self):
        """Create a new trial user to trigger welcome email with logo"""
        print("👤 Testing Trial User Creation & Welcome Email...")
        
        # Create unique trial user
        trial_data = {
            "email": f"trial_{int(time.time())}@example.com",
            "first_name": "Trial",
            "last_name": "User",
            "company_name": "Test Company"
        }
        
        response = self.make_request("POST", "/subscriptions/trial/register", trial_data)
        
        if response.get("status_code") == 200:
            user_data = response.get("data", {})
            
            self.log_result(
                "Trial User Registration",
                True,
                f"Trial user created successfully. Email: {trial_data['email']}, Status: {user_data.get('status', 'unknown')}",
                {
                    "user_email": trial_data["email"],
                    "trial_end": user_data.get("trial_end"),
                    "auto_login_password": user_data.get("user", {}).get("password", "N/A")
                }
            )
            
            # Wait a moment for email to be processed
            await asyncio.sleep(2)
            
            # Verify welcome email was sent with logo
            await self.verify_trial_welcome_email(trial_data["email"])
            return True
        else:
            self.log_result(
                "Trial User Registration",
                False,
                f"Trial user creation failed. Status: {response.get('status_code')}, Error: {response.get('data', {}).get('detail', 'Unknown error')}",
                response
            )
            return False

    async def verify_trial_welcome_email(self, user_email: str):
        """Verify trial welcome email contains logo and proper content"""
        print("📬 Verifying Trial Welcome Email Content...")
        
        if not self.admin_token:
            self.log_result(
                "Trial Welcome Email Verification",
                False,
                "Cannot verify email content - no admin token",
                None
            )
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Check trial email logs
        response = self.make_request("GET", f"/email/email/trial/logs?user_email={user_email}", headers=headers)
        
        if response.get("status_code") == 200:
            logs = response.get("data", {}).get("logs", [])
            
            # Look for welcome email
            welcome_emails = [log for log in logs if log.get("email_type") == "welcome"]
            
            if welcome_emails:
                welcome_email = welcome_emails[0]
                html_content = welcome_email.get("html_content", "")
                
                # Check for logo and branding
                logo_url = "https://customer-assets.emergentagent.com/job_customer-mind-iq-4/artifacts/pntu3yqm_Customer%20Mind%20IQ%20logo.png"
                has_logo = logo_url in html_content
                has_welcome_branding = "CustomerMind IQ" in html_content or "Customer Mind IQ" in html_content
                has_login_credentials = "password" in html_content.lower()
                
                self.log_result(
                    "Trial Welcome Email Logo Integration",
                    has_logo and has_welcome_branding,
                    f"Logo: {has_logo}, Branding: {has_welcome_branding}, Login info: {has_login_credentials}. Status: {welcome_email.get('status', 'unknown')}",
                    {
                        "email_type": welcome_email.get("email_type"),
                        "status": welcome_email.get("status"),
                        "has_logo": has_logo,
                        "has_branding": has_welcome_branding,
                        "scheduled_time": welcome_email.get("scheduled_send_time"),
                        "actual_send_time": welcome_email.get("actual_send_time")
                    }
                )
                return has_logo and has_welcome_branding
            else:
                self.log_result(
                    "Trial Welcome Email Verification",
                    False,
                    f"No welcome email found for user {user_email}",
                    {"total_logs": len(logs), "log_types": [log.get("email_type") for log in logs]}
                )
                return False
        else:
            self.log_result(
                "Trial Welcome Email Verification",
                False,
                f"Failed to retrieve trial email logs. Status: {response.get('status_code')}",
                response
            )
            return False

    async def test_email_system_integration(self):
        """Test email system integration and provider configuration"""
        print("⚙️ Testing Email System Integration...")
        
        if not self.admin_token:
            self.log_result(
                "Email System Integration",
                False,
                "Cannot test email system - no admin token",
                None
            )
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Check current email provider
        response = self.make_request("GET", "/email/email/providers/current", headers=headers)
        
        if response.get("status_code") == 200:
            provider_data = response.get("data", {})
            provider_config = provider_data.get("provider_config", {})
            odoo_integration = provider_data.get("odoo_integration", {})
            
            self.log_result(
                "Email Provider Configuration",
                True,
                f"Provider: {provider_config.get('provider', 'unknown')}, ODOO available: {odoo_integration.get('available', False)}, ODOO connected: {odoo_integration.get('connected', False)}",
                {
                    "provider": provider_config.get("provider"),
                    "from_email": provider_config.get("from_email"),
                    "from_name": provider_config.get("from_name"),
                    "odoo_status": odoo_integration,
                    "email_routing": provider_data.get("email_routing")
                }
            )
            
            # Test email statistics
            await self.test_email_statistics()
            return True
        else:
            self.log_result(
                "Email Provider Configuration",
                False,
                f"Failed to get email provider config. Status: {response.get('status_code')}",
                response
            )
            return False

    async def test_email_statistics(self):
        """Test email statistics endpoint"""
        print("📊 Testing Email Statistics...")
        
        if not self.admin_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.make_request("GET", "/email/email/stats", headers=headers)
        
        if response.get("status_code") == 200:
            stats = response.get("data", {}).get("statistics", {})
            
            self.log_result(
                "Email Statistics",
                True,
                f"Campaigns: {stats.get('total_campaigns', 0)}, Sent: {stats.get('total_emails_sent', 0)}, Failed: {stats.get('total_emails_failed', 0)}, Delivery Rate: {stats.get('delivery_rate_percent', 0)}%",
                stats
            )
            return True
        else:
            self.log_result(
                "Email Statistics",
                False,
                f"Failed to get email statistics. Status: {response.get('status_code')}",
                response
            )
            return False

    async def test_trial_email_automation_stats(self):
        """Test trial email automation statistics"""
        print("🤖 Testing Trial Email Automation Stats...")
        
        if not self.admin_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.make_request("GET", "/email/email/trial/stats", headers=headers)
        
        if response.get("status_code") == 200:
            stats = response.get("data", {})
            overall_stats = stats.get("overall_stats", {})
            type_stats = stats.get("stats_by_type", {})
            
            self.log_result(
                "Trial Email Automation Stats",
                True,
                f"Total emails: {overall_stats.get('total_emails', 0)}, Sent: {overall_stats.get('sent', 0)}, Success rate: {overall_stats.get('success_rate_percent', 0)}%",
                {
                    "overall_stats": overall_stats,
                    "welcome_emails": type_stats.get("welcome", {}),
                    "progress_emails": type_stats.get("progress", {}),
                    "urgency_emails": type_stats.get("urgency", {}),
                    "final_emails": type_stats.get("final", {})
                }
            )
            return True
        else:
            self.log_result(
                "Trial Email Automation Stats",
                False,
                f"Failed to get trial email stats. Status: {response.get('status_code')}",
                response
            )
            return False

    async def run_all_tests(self):
        """Run all password reset and email integration tests"""
        print("🚀 Starting Password Reset & Email Logo Integration Testing")
        print("=" * 80)
        
        # Test sequence
        tests = [
            ("Admin Authentication", self.test_admin_authentication),
            ("Password Reset Request", self.test_password_reset_request),
            ("Trial User Creation & Welcome Email", self.test_trial_user_creation_with_welcome_email),
            ("Email System Integration", self.test_email_system_integration),
            ("Trial Email Automation Stats", self.test_trial_email_automation_stats)
        ]
        
        for test_name, test_func in tests:
            try:
                await test_func()
            except Exception as e:
                self.log_result(
                    test_name,
                    False,
                    f"Test failed with exception: {str(e)}",
                    {"exception": str(e)}
                )
        
        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("📋 TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Detailed results
        for result in self.results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        print("\n" + "=" * 80)
        print("🎯 KEY FINDINGS")
        print("=" * 80)
        
        # Check specific requirements
        password_reset_working = any(r["success"] and "Password Reset Request" in r["test"] for r in self.results)
        email_logo_integration = any(r["success"] and "Logo Integration" in r["test"] for r in self.results)
        email_system_working = any(r["success"] and "Email System Integration" in r["test"] for r in self.results)
        
        print(f"✅ Password Reset Functionality: {'WORKING' if password_reset_working else 'NEEDS ATTENTION'}")
        print(f"✅ Email Logo Integration: {'WORKING' if email_logo_integration else 'NEEDS ATTENTION'}")
        print(f"✅ Email System Integration: {'WORKING' if email_system_working else 'NEEDS ATTENTION'}")
        
        if success_rate >= 80:
            print("\n🎉 OVERALL STATUS: Password reset and email system with logo integration is WORKING WELL!")
        elif success_rate >= 60:
            print("\n⚠️ OVERALL STATUS: Password reset and email system mostly working, minor issues identified.")
        else:
            print("\n❌ OVERALL STATUS: Password reset and email system needs attention - multiple issues found.")
        
        print("\n" + "=" * 80)

async def main():
    """Main test execution"""
    tester = PasswordResetEmailTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())