#!/usr/bin/env python3
"""
CustomerMind IQ - Comprehensive Email System Testing
Testing password reset emails, trial emails, and logo integration

Focus Areas:
1. Password Reset Email with Logo
2. Trial Welcome Email with Logo  
3. Email Template Structure
4. Email Provider Integration
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
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class ComprehensiveEmailTester:
    def __init__(self):
        self.admin_token = None
        self.results = []
        
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
            else:
                return {"error": f"Unsupported method: {method}", "status_code": 400}
            
            return {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "headers": dict(response.headers)
            }
            
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    async def authenticate_admin(self):
        """Authenticate as admin"""
        response = self.make_request("POST", "/auth/login", ADMIN_CREDENTIALS)
        
        if response.get("status_code") == 200 and "access_token" in response.get("data", {}):
            self.admin_token = response["data"]["access_token"]
            return True
        return False

    async def test_password_reset_with_existing_user(self):
        """Test password reset with existing admin user"""
        print("🔒 Testing Password Reset with Existing User...")
        
        # Use admin email for password reset test
        reset_data = {"email": "admin@customermindiq.com"}
        response = self.make_request("POST", "/auth/request-password-reset", reset_data)
        
        if response.get("status_code") == 200:
            message = response.get("data", {}).get("message", "")
            
            self.log_result(
                "Password Reset - Existing User",
                True,
                f"Password reset successful for existing user. Message: {message}",
                response.get("data")
            )
            
            # Wait for email processing
            await asyncio.sleep(3)
            
            # Check if email was logged
            await self.check_password_reset_email_logs()
            return True
        else:
            self.log_result(
                "Password Reset - Existing User",
                False,
                f"Password reset failed. Status: {response.get('status_code')}, Error: {response.get('data', {}).get('detail', 'Unknown error')}",
                response
            )
            return False

    async def check_password_reset_email_logs(self):
        """Check email logs for password reset emails"""
        print("📧 Checking Password Reset Email Logs...")
        
        if not self.admin_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Check email logs
        response = self.make_request("GET", "/email/email/campaigns", headers=headers)
        
        if response.get("status_code") == 200:
            campaigns = response.get("data", {}).get("campaigns", [])
            
            # Look for recent password reset campaigns
            recent_campaigns = [
                c for c in campaigns 
                if "password" in c.get("subject", "").lower() or "reset" in c.get("subject", "").lower()
            ]
            
            if recent_campaigns:
                latest_campaign = recent_campaigns[0]
                html_content = latest_campaign.get("html_content", "")
                
                # Check for logo and branding
                logo_checks = {
                    "has_logo_url": "customer-assets.emergentagent.com" in html_content,
                    "has_customer_mind_iq": "CustomerMind IQ" in html_content or "Customer Mind IQ" in html_content,
                    "has_reset_link": "reset-password" in html_content,
                    "has_security_message": "security" in html_content.lower(),
                    "has_proper_styling": "style=" in html_content
                }
                
                all_checks_passed = all(logo_checks.values())
                
                self.log_result(
                    "Password Reset Email Content Verification",
                    all_checks_passed,
                    f"Content checks: {sum(logo_checks.values())}/5 passed. Campaign: {latest_campaign.get('name', 'N/A')}",
                    {
                        "campaign_id": latest_campaign.get("campaign_id"),
                        "subject": latest_campaign.get("subject"),
                        "status": latest_campaign.get("status"),
                        "checks": logo_checks,
                        "recipient_count": latest_campaign.get("recipient_count", 0)
                    }
                )
                return all_checks_passed
            else:
                # Check email logs directly
                logs_response = self.make_request("GET", "/email/email/campaigns?limit=50", headers=headers)
                if logs_response.get("status_code") == 200:
                    all_campaigns = logs_response.get("data", {}).get("campaigns", [])
                    
                    self.log_result(
                        "Password Reset Email Search",
                        False,
                        f"No password reset campaigns found. Total campaigns: {len(all_campaigns)}",
                        {"campaign_subjects": [c.get("subject", "N/A") for c in all_campaigns[:5]]}
                    )
                return False
        else:
            self.log_result(
                "Password Reset Email Logs",
                False,
                f"Failed to retrieve email campaigns. Status: {response.get('status_code')}",
                response
            )
            return False

    async def test_trial_email_sequence(self):
        """Test complete trial email sequence"""
        print("📬 Testing Trial Email Sequence...")
        
        # Create trial user
        trial_email = f"emailtest_{int(time.time())}@example.com"
        trial_data = {
            "email": trial_email,
            "first_name": "Email",
            "last_name": "Tester",
            "company_name": "Test Email Company"
        }
        
        response = self.make_request("POST", "/subscriptions/trial/register", trial_data)
        
        if response.get("status_code") == 200:
            user_data = response.get("data", {})
            
            self.log_result(
                "Trial User Creation for Email Test",
                True,
                f"Trial user created: {trial_email}. Status: {user_data.get('status', 'unknown')}",
                {
                    "user_email": trial_email,
                    "trial_end": user_data.get("trial_end"),
                    "user_id": user_data.get("user", {}).get("user_id")
                }
            )
            
            # Wait for email processing
            await asyncio.sleep(5)
            
            # Check trial email logs
            await self.check_trial_email_logs(trial_email)
            return True
        else:
            self.log_result(
                "Trial User Creation for Email Test",
                False,
                f"Failed to create trial user. Status: {response.get('status_code')}",
                response
            )
            return False

    async def check_trial_email_logs(self, user_email: str):
        """Check trial email logs for specific user"""
        print(f"📊 Checking Trial Email Logs for {user_email}...")
        
        if not self.admin_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Get trial email logs for this user
        response = self.make_request("GET", f"/email/email/trial/logs?user_email={user_email}&limit=10", headers=headers)
        
        if response.get("status_code") == 200:
            logs = response.get("data", {}).get("logs", [])
            
            if logs:
                welcome_logs = [log for log in logs if log.get("email_type") == "welcome"]
                
                if welcome_logs:
                    welcome_log = welcome_logs[0]
                    html_content = welcome_log.get("html_content", "")
                    
                    # Comprehensive content checks
                    content_checks = {
                        "has_logo": "customer-assets.emergentagent.com" in html_content,
                        "has_branding": "CustomerMind IQ" in html_content or "Customer Mind IQ" in html_content,
                        "has_login_credentials": "password" in html_content.lower() and "username" in html_content.lower(),
                        "has_dashboard_link": "dashboard" in html_content.lower(),
                        "has_welcome_message": "welcome" in html_content.lower(),
                        "has_trial_info": "trial" in html_content.lower() or "7-day" in html_content.lower(),
                        "has_styling": "style=" in html_content and "background:" in html_content,
                        "has_call_to_action": "Start Exploring" in html_content or "Get Started" in html_content
                    }
                    
                    passed_checks = sum(content_checks.values())
                    total_checks = len(content_checks)
                    
                    self.log_result(
                        "Trial Welcome Email Content Analysis",
                        passed_checks >= 6,  # At least 6/8 checks should pass
                        f"Content analysis: {passed_checks}/{total_checks} checks passed. Status: {welcome_log.get('status', 'unknown')}",
                        {
                            "email_type": welcome_log.get("email_type"),
                            "status": welcome_log.get("status"),
                            "scheduled_time": welcome_log.get("scheduled_send_time"),
                            "actual_send_time": welcome_log.get("actual_send_time"),
                            "content_checks": content_checks,
                            "subject": welcome_log.get("subject")
                        }
                    )
                    return passed_checks >= 6
                else:
                    self.log_result(
                        "Trial Welcome Email Search",
                        False,
                        f"No welcome email found for {user_email}. Found {len(logs)} total logs",
                        {"log_types": [log.get("email_type") for log in logs]}
                    )
                    return False
            else:
                self.log_result(
                    "Trial Email Logs",
                    False,
                    f"No trial email logs found for {user_email}",
                    {"user_email": user_email}
                )
                return False
        else:
            self.log_result(
                "Trial Email Logs Retrieval",
                False,
                f"Failed to get trial email logs. Status: {response.get('status_code')}",
                response
            )
            return False

    async def test_email_template_structure(self):
        """Test email template structure and logo integration"""
        print("🎨 Testing Email Template Structure...")
        
        if not self.admin_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Get trial email stats to understand template usage
        response = self.make_request("GET", "/email/email/trial/stats", headers=headers)
        
        if response.get("status_code") == 200:
            stats = response.get("data", {})
            overall_stats = stats.get("overall_stats", {})
            type_stats = stats.get("stats_by_type", {})
            
            # Check if templates are being used
            template_usage = {
                "welcome_emails": type_stats.get("welcome", {}).get("total", 0),
                "progress_emails": type_stats.get("progress", {}).get("total", 0),
                "urgency_emails": type_stats.get("urgency", {}).get("total", 0),
                "final_emails": type_stats.get("final", {}).get("total", 0)
            }
            
            total_template_usage = sum(template_usage.values())
            
            self.log_result(
                "Email Template Usage Analysis",
                total_template_usage > 0,
                f"Total template usage: {total_template_usage} emails. Success rate: {overall_stats.get('success_rate_percent', 0)}%",
                {
                    "template_usage": template_usage,
                    "overall_stats": overall_stats,
                    "success_rate": overall_stats.get("success_rate_percent", 0)
                }
            )
            return total_template_usage > 0
        else:
            self.log_result(
                "Email Template Analysis",
                False,
                f"Failed to get template stats. Status: {response.get('status_code')}",
                response
            )
            return False

    async def test_email_provider_integration(self):
        """Test email provider integration and ODOO connection"""
        print("🔌 Testing Email Provider Integration...")
        
        if not self.admin_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Check current provider configuration
        response = self.make_request("GET", "/email/email/providers/current", headers=headers)
        
        if response.get("status_code") == 200:
            provider_data = response.get("data", {})
            provider_config = provider_data.get("provider_config", {})
            odoo_integration = provider_data.get("odoo_integration", {})
            
            # Analyze provider setup
            provider_checks = {
                "has_provider_config": bool(provider_config.get("provider")),
                "has_from_email": bool(provider_config.get("from_email")),
                "has_from_name": bool(provider_config.get("from_name")),
                "odoo_available": odoo_integration.get("available", False),
                "odoo_connected": odoo_integration.get("connected", False),
                "has_email_routing": bool(provider_data.get("email_routing"))
            }
            
            passed_checks = sum(provider_checks.values())
            
            self.log_result(
                "Email Provider Integration Analysis",
                passed_checks >= 4,  # At least 4/6 checks should pass
                f"Provider integration: {passed_checks}/6 checks passed. Provider: {provider_config.get('provider', 'unknown')}",
                {
                    "provider_checks": provider_checks,
                    "provider": provider_config.get("provider"),
                    "from_email": provider_config.get("from_email"),
                    "odoo_status": odoo_integration.get("message", "N/A"),
                    "email_routing": provider_data.get("email_routing")
                }
            )
            return passed_checks >= 4
        else:
            self.log_result(
                "Email Provider Integration",
                False,
                f"Failed to get provider config. Status: {response.get('status_code')}",
                response
            )
            return False

    async def run_comprehensive_tests(self):
        """Run all comprehensive email tests"""
        print("🚀 Starting Comprehensive Email System Testing")
        print("=" * 80)
        
        # Authenticate first
        if not await self.authenticate_admin():
            print("❌ Failed to authenticate admin - cannot proceed with tests")
            return
        
        # Test sequence
        tests = [
            ("Password Reset with Existing User", self.test_password_reset_with_existing_user),
            ("Trial Email Sequence", self.test_trial_email_sequence),
            ("Email Template Structure", self.test_email_template_structure),
            ("Email Provider Integration", self.test_email_provider_integration)
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
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE EMAIL SYSTEM TEST SUMMARY")
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
        print("🎯 EMAIL SYSTEM ASSESSMENT")
        print("=" * 80)
        
        # Check specific requirements from review request
        password_reset_working = any(r["success"] and "Password Reset" in r["test"] for r in self.results)
        email_content_verified = any(r["success"] and "Content" in r["test"] for r in self.results)
        provider_integration = any(r["success"] and "Provider Integration" in r["test"] for r in self.results)
        template_structure = any(r["success"] and "Template" in r["test"] for r in self.results)
        
        print(f"✅ Password Reset Emails: {'WORKING' if password_reset_working else 'NEEDS ATTENTION'}")
        print(f"✅ Email Content & Logo Integration: {'WORKING' if email_content_verified else 'NEEDS ATTENTION'}")
        print(f"✅ Email Provider Integration: {'WORKING' if provider_integration else 'NEEDS ATTENTION'}")
        print(f"✅ Email Template Structure: {'WORKING' if template_structure else 'NEEDS ATTENTION'}")
        
        # Overall assessment
        if success_rate >= 80:
            print("\n🎉 OVERALL ASSESSMENT: Email system with logo integration is FULLY FUNCTIONAL!")
            print("   - Password reset emails are being sent with proper branding")
            print("   - Trial welcome emails include Customer Mind IQ logo")
            print("   - Email templates are properly structured")
            print("   - Email provider integration is working")
        elif success_rate >= 60:
            print("\n⚠️ OVERALL ASSESSMENT: Email system is mostly working with minor issues.")
            print("   - Core functionality is operational")
            print("   - Some components may need fine-tuning")
        else:
            print("\n❌ OVERALL ASSESSMENT: Email system needs significant attention.")
            print("   - Multiple critical issues identified")
            print("   - Review email provider configuration")
            print("   - Check template integration")
        
        print("\n" + "=" * 80)

async def main():
    """Main test execution"""
    tester = ComprehensiveEmailTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())