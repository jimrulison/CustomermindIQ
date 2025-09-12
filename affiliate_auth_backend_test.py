#!/usr/bin/env python3
"""
Affiliate Authentication System Backend Testing
Tests the independent affiliate authentication system that works without main platform access
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://websiteintel-hub.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

class AffiliateAuthTester:
    def __init__(self):
        self.session = None
        self.affiliate_token = None
        self.test_affiliate_id = None
        self.results = []
        
    async def setup_session(self):
        """Setup HTTP session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    def log_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        if response_data and isinstance(response_data, dict):
            if "error" in response_data:
                print(f"   Error: {response_data['error']}")
        
        self.results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data
        })
        
    async def test_affiliate_registration_independent(self):
        """Test affiliate registration without main platform login"""
        try:
            # Test data from review request
            registration_data = {
                "first_name": "Jane",
                "last_name": "Affiliate", 
                "email": "jane.affiliate@example.com",
                "phone": "+1-555-987-6543",
                "website": "https://janemarketing.com",
                "promotion_method": "social",
                "password": "SecurePass123!",
                "address": {
                    "street": "456 Marketing Ave",
                    "city": "San Francisco", 
                    "state": "CA",
                    "zip_code": "94105",
                    "country": "US"
                },
                "payment_method": "paypal",
                "payment_details": {
                    "paypal_email": "jane.affiliate@paypal.com"
                }
            }
            
            # Test registration WITHOUT any authentication headers
            async with self.session.post(f"{API_BASE}/affiliate/auth/register", json=registration_data) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    self.test_affiliate_id = data.get("affiliate_id")
                    self.log_result(
                        "Affiliate Registration (Independent)", 
                        True, 
                        f"Registration successful without main platform auth. Affiliate ID: {self.test_affiliate_id}",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Affiliate Registration (Independent)", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Registration (Independent)", False, f"Exception: {str(e)}")
            return False
            
    async def test_affiliate_login_independent(self):
        """Test affiliate login authentication without main platform"""
        try:
            login_data = {
                "email": "jane.affiliate@example.com",
                "password": "SecurePass123!"
            }
            
            # Test login WITHOUT any main platform authentication
            async with self.session.post(f"{API_BASE}/affiliate/auth/login", json=login_data) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    self.affiliate_token = data.get("token")
                    self.log_result(
                        "Affiliate Login (Independent)", 
                        True, 
                        f"Login successful with affiliate-specific JWT token",
                        {"affiliate_info": data.get("affiliate")}
                    )
                    return True
                elif response.status == 403 and "pending approval" in data.get("detail", "").lower():
                    # Account pending approval is expected for new registrations
                    self.log_result(
                        "Affiliate Login (Independent)", 
                        True, 
                        "Account pending approval (expected for new registrations)",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Affiliate Login (Independent)", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Login (Independent)", False, f"Exception: {str(e)}")
            return False
            
    async def test_affiliate_dashboard_with_id(self):
        """Test affiliate dashboard access with affiliate_id parameter"""
        try:
            # Use test affiliate ID from registration or a test ID
            test_id = self.test_affiliate_id or "test_id"
            
            # Test dashboard access WITHOUT main platform authentication
            async with self.session.get(f"{API_BASE}/affiliate/dashboard?affiliate_id={test_id}") as response:
                data = await response.json()
                
                if response.status == 200:
                    # Check if response has expected structure
                    has_affiliate = "affiliate" in data
                    has_stats = "stats" in data
                    has_activity = "recent_activity" in data
                    
                    if has_affiliate and has_stats and has_activity:
                        self.log_result(
                            "Affiliate Dashboard Access", 
                            True, 
                            f"Dashboard accessible with affiliate_id parameter, no main platform auth required",
                            {"affiliate_id": data.get("affiliate", {}).get("affiliate_id")}
                        )
                        return True
                    else:
                        self.log_result(
                            "Affiliate Dashboard Access", 
                            False, 
                            f"Missing expected fields: affiliate={has_affiliate}, stats={has_stats}, activity={has_activity}",
                            data
                        )
                        return False
                elif response.status == 404:
                    self.log_result(
                        "Affiliate Dashboard Access", 
                        True, 
                        "Affiliate not found (expected for test ID) - endpoint accessible without main platform auth",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Affiliate Dashboard Access", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Dashboard Access", False, f"Exception: {str(e)}")
            return False
            
    async def test_generate_link_independent(self):
        """Test affiliate link generation without main platform auth"""
        try:
            test_id = self.test_affiliate_id or "test_id"
            
            link_data = {
                "campaign_name": "independent_test_campaign",
                "link_type": "trial",
                "custom_params": {
                    "utm_source": "affiliate",
                    "utm_medium": "social",
                    "utm_campaign": "independent_test"
                }
            }
            
            # Test link generation WITHOUT main platform authentication
            async with self.session.post(
                f"{API_BASE}/affiliate/generate-link?affiliate_id={test_id}", 
                json=link_data
            ) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    has_tracking_url = "tracking_url" in data
                    has_short_url = "short_url" in data
                    
                    if has_tracking_url and has_short_url:
                        self.log_result(
                            "Affiliate Link Generation", 
                            True, 
                            f"Link generation works independently without main platform auth",
                            {
                                "tracking_url": data.get("tracking_url"),
                                "short_url": data.get("short_url")
                            }
                        )
                        return True
                    else:
                        self.log_result(
                            "Affiliate Link Generation", 
                            False, 
                            f"Missing URLs: tracking={has_tracking_url}, short={has_short_url}",
                            data
                        )
                        return False
                else:
                    self.log_result(
                        "Affiliate Link Generation", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Link Generation", False, f"Exception: {str(e)}")
            return False
            
    async def test_event_tracking_no_auth(self):
        """Test event tracking without any authentication (should work)"""
        try:
            event_data = {
                "event_type": "click",
                "affiliate_id": self.test_affiliate_id or "test_id",
                "campaign": "independent_test_campaign",
                "ip": "192.168.1.100",
                "user_agent": "Mozilla/5.0 Independent Test Browser",
                "referrer": "https://janemarketing.com",
                "landing_page": "https://customermindiq.com/trial",
                "utm_source": "affiliate",
                "utm_medium": "social",
                "utm_campaign": "independent_test",
                "session_id": "independent_session_456"
            }
            
            # Test event tracking WITHOUT any authentication
            async with self.session.post(f"{API_BASE}/affiliate/track/event", json=event_data) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    self.log_result(
                        "Event Tracking (No Auth)", 
                        True, 
                        f"Event tracking works without any authentication as expected",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Event Tracking (No Auth)", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Event Tracking (No Auth)", False, f"Exception: {str(e)}")
            return False
            
    async def test_main_platform_separation(self):
        """Test that affiliate system is separate from main platform authentication"""
        try:
            # Try to access main platform endpoint without main platform auth
            async with self.session.get(f"{API_BASE}/customers") as response:
                main_platform_blocked = response.status == 401
                
            # Try to access affiliate endpoint without main platform auth
            test_id = self.test_affiliate_id or "test_id"
            async with self.session.get(f"{API_BASE}/affiliate/dashboard?affiliate_id={test_id}") as response:
                affiliate_accessible = response.status in [200, 404]  # 404 is OK for test ID
                
            if main_platform_blocked and affiliate_accessible:
                self.log_result(
                    "Platform Separation", 
                    True, 
                    "Affiliate system properly separated from main platform authentication",
                    {
                        "main_platform_blocked": main_platform_blocked,
                        "affiliate_accessible": affiliate_accessible
                    }
                )
                return True
            else:
                self.log_result(
                    "Platform Separation", 
                    False, 
                    f"Platform separation issue: main_blocked={main_platform_blocked}, affiliate_accessible={affiliate_accessible}",
                    {}
                )
                return False
                
        except Exception as e:
            self.log_result("Platform Separation", False, f"Exception: {str(e)}")
            return False
            
    async def run_all_tests(self):
        """Run all affiliate authentication independence tests"""
        print("🚀 Starting Affiliate Authentication Independence Testing")
        print("=" * 70)
        print("Testing affiliate system independence from main platform authentication")
        print("=" * 70)
        
        await self.setup_session()
        
        try:
            # Test independent affiliate functionality
            await self.test_affiliate_registration_independent()
            await self.test_affiliate_login_independent()
            await self.test_affiliate_dashboard_with_id()
            await self.test_generate_link_independent()
            await self.test_event_tracking_no_auth()
            await self.test_main_platform_separation()
            
        finally:
            await self.cleanup_session()
            
        # Print summary
        print("\n" + "=" * 70)
        print("📊 AFFILIATE AUTHENTICATION INDEPENDENCE TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.results:
                if not result["success"]:
                    print(f"   • {result['test']}: {result['details']}")
        
        print(f"\n🎯 AFFILIATE AUTHENTICATION INDEPENDENCE: {'✅ WORKING' if success_rate >= 80 else '❌ NEEDS ATTENTION'}")
        
        return success_rate >= 80

async def main():
    """Main test execution"""
    tester = AffiliateAuthTester()
    success = await tester.run_all_tests()
    return success

if __name__ == "__main__":
    asyncio.run(main())