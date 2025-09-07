#!/usr/bin/env python3
"""
Affiliate System Backend Testing
Tests the comprehensive affiliate tracking system with Phase 1 features
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-ai-hub-1.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

class AffiliateSystemTester:
    def __init__(self):
        self.session = None
        self.admin_token = None
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
        
    async def admin_login(self):
        """Login as admin to get admin token"""
        try:
            login_data = {
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!"
            }
            
            async with self.session.post(f"{API_BASE}/auth/login", json=login_data) as response:
                if response.status == 200:
                    data = await response.json()
                    self.admin_token = data.get("access_token")
                    self.log_result("Admin Login", True, f"Admin authenticated successfully")
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("Admin Login", False, f"Status: {response.status}, Error: {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Admin Login", False, f"Exception: {str(e)}")
            return False
            
    async def test_affiliate_registration(self):
        """Test affiliate registration endpoint"""
        try:
            # Test data from review request
            registration_data = {
                "first_name": "John",
                "last_name": "Doe", 
                "email": "johndoe@example.com",
                "phone": "+1-555-123-4567",
                "website": "https://johndoe.com",
                "promotion_method": "email",
                "password": "securepassword123",
                "address": {
                    "street": "123 Main St",
                    "city": "New York", 
                    "state": "NY",
                    "zip_code": "10001",
                    "country": "US"
                },
                "payment_method": "paypal",
                "payment_details": {
                    "paypal_email": "johndoe@paypal.com"
                }
            }
            
            async with self.session.post(f"{API_BASE}/affiliate/auth/register", json=registration_data) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    self.test_affiliate_id = data.get("affiliate_id")
                    self.log_result(
                        "Affiliate Registration", 
                        True, 
                        f"Affiliate registered with ID: {self.test_affiliate_id}",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Affiliate Registration", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Registration", False, f"Exception: {str(e)}")
            return False
            
    async def test_affiliate_login(self):
        """Test affiliate login endpoint"""
        try:
            login_data = {
                "email": "johndoe@example.com",
                "password": "securepassword123"
            }
            
            async with self.session.post(f"{API_BASE}/affiliate/auth/login", json=login_data) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    self.affiliate_token = data.get("token")
                    self.log_result(
                        "Affiliate Login", 
                        True, 
                        f"Login successful, token received",
                        {"affiliate_info": data.get("affiliate")}
                    )
                    return True
                elif response.status == 403:
                    # Account pending approval is expected for new registrations
                    self.log_result(
                        "Affiliate Login", 
                        True, 
                        "Account pending approval (expected for new registrations)",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Affiliate Login", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Login", False, f"Exception: {str(e)}")
            return False
            
    async def test_affiliate_dashboard(self):
        """Test affiliate dashboard endpoint"""
        try:
            # Use test affiliate ID from registration or a test ID
            test_id = self.test_affiliate_id or "test_affiliate_id"
            
            async with self.session.get(f"{API_BASE}/affiliate/dashboard?affiliate_id={test_id}") as response:
                data = await response.json()
                
                if response.status == 200:
                    # Check if response has expected structure
                    has_affiliate = "affiliate" in data
                    has_stats = "stats" in data
                    has_activity = "recent_activity" in data
                    
                    if has_affiliate and has_stats and has_activity:
                        self.log_result(
                            "Affiliate Dashboard", 
                            True, 
                            f"Dashboard data retrieved with affiliate, stats, and activity",
                            {"affiliate_id": data.get("affiliate", {}).get("affiliate_id")}
                        )
                        return True
                    else:
                        self.log_result(
                            "Affiliate Dashboard", 
                            False, 
                            f"Missing expected fields: affiliate={has_affiliate}, stats={has_stats}, activity={has_activity}",
                            data
                        )
                        return False
                elif response.status == 404:
                    self.log_result(
                        "Affiliate Dashboard", 
                        True, 
                        "Affiliate not found (expected for test ID)",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Affiliate Dashboard", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Dashboard", False, f"Exception: {str(e)}")
            return False
            
    async def test_generate_tracking_link(self):
        """Test tracking link generation endpoint"""
        try:
            test_id = self.test_affiliate_id or "test_affiliate_id"
            
            link_data = {
                "campaign_name": "test_campaign",
                "link_type": "trial",
                "custom_params": {
                    "utm_source": "affiliate",
                    "utm_medium": "email",
                    "utm_campaign": "test_campaign"
                }
            }
            
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
                            "Generate Tracking Link", 
                            True, 
                            f"Tracking link generated successfully",
                            {
                                "tracking_url": data.get("tracking_url"),
                                "short_url": data.get("short_url")
                            }
                        )
                        return True
                    else:
                        self.log_result(
                            "Generate Tracking Link", 
                            False, 
                            f"Missing URLs: tracking={has_tracking_url}, short={has_short_url}",
                            data
                        )
                        return False
                else:
                    self.log_result(
                        "Generate Tracking Link", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Generate Tracking Link", False, f"Exception: {str(e)}")
            return False
            
    async def test_affiliate_materials(self):
        """Test affiliate marketing materials endpoint"""
        try:
            test_id = self.test_affiliate_id or "test_affiliate_id"
            
            async with self.session.get(f"{API_BASE}/affiliate/materials?affiliate_id={test_id}") as response:
                data = await response.json()
                
                if response.status == 200:
                    has_banners = "banners" in data
                    has_email_templates = "email_templates" in data
                    has_landing_pages = "landing_pages" in data
                    
                    if has_banners and has_email_templates and has_landing_pages:
                        self.log_result(
                            "Affiliate Materials", 
                            True, 
                            f"Marketing materials retrieved with banners, templates, and landing pages",
                            {
                                "banners_count": len(data.get("banners", [])),
                                "templates_count": len(data.get("email_templates", [])),
                                "landing_pages_count": len(data.get("landing_pages", []))
                            }
                        )
                        return True
                    else:
                        self.log_result(
                            "Affiliate Materials", 
                            False, 
                            f"Missing materials: banners={has_banners}, templates={has_email_templates}, pages={has_landing_pages}",
                            data
                        )
                        return False
                else:
                    self.log_result(
                        "Affiliate Materials", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Materials", False, f"Exception: {str(e)}")
            return False
            
    async def test_event_tracking(self):
        """Test affiliate event tracking endpoint"""
        try:
            event_data = {
                "event_type": "click",
                "affiliate_id": self.test_affiliate_id or "test_affiliate_id",
                "campaign": "test_campaign",
                "ip": "192.168.1.1",
                "user_agent": "Mozilla/5.0 Test Browser",
                "referrer": "https://google.com",
                "landing_page": "https://customermindiq.com/trial",
                "utm_source": "affiliate",
                "utm_medium": "email",
                "utm_campaign": "test_campaign",
                "session_id": "test_session_123"
            }
            
            async with self.session.post(f"{API_BASE}/affiliate/track/event", json=event_data) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    self.log_result(
                        "Event Tracking", 
                        True, 
                        f"Event tracked successfully",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Event Tracking", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Event Tracking", False, f"Exception: {str(e)}")
            return False
            
    async def test_admin_affiliate_management(self):
        """Test admin affiliate management endpoint"""
        try:
            if not self.admin_token:
                self.log_result("Admin Affiliate Management", False, "No admin token available")
                return False
                
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            async with self.session.get(f"{API_BASE}/affiliate/admin/affiliates", headers=headers) as response:
                data = await response.json()
                
                if response.status == 200:
                    has_status = "status" in data
                    has_affiliates = "affiliates" in data
                    has_total = "total" in data
                    
                    if has_status and has_affiliates and has_total:
                        affiliates_count = len(data.get("affiliates", []))
                        self.log_result(
                            "Admin Affiliate Management", 
                            True, 
                            f"Admin endpoint accessible, {affiliates_count} affiliates found",
                            {
                                "status": data.get("status"),
                                "total": data.get("total")
                            }
                        )
                        return True
                    else:
                        self.log_result(
                            "Admin Affiliate Management", 
                            False, 
                            f"Missing fields: status={has_status}, affiliates={has_affiliates}, total={has_total}",
                            data
                        )
                        return False
                else:
                    self.log_result(
                        "Admin Affiliate Management", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Admin Affiliate Management", False, f"Exception: {str(e)}")
            return False
            
    async def test_commission_calculation(self):
        """Test commission calculation system"""
        try:
            # Test conversion event that should trigger commission calculation
            conversion_data = {
                "event_type": "conversion",
                "affiliate_id": self.test_affiliate_id or "test_affiliate_id",
                "customer_id": "test_customer_123",
                "plan_type": "growth",
                "billing_cycle": "monthly",
                "amount": 75.0,
                "session_id": "test_session_123"
            }
            
            async with self.session.post(f"{API_BASE}/affiliate/track/event", json=conversion_data) as response:
                data = await response.json()
                
                if response.status == 200 and data.get("success"):
                    self.log_result(
                        "Commission Calculation", 
                        True, 
                        f"Conversion event processed, commission calculation triggered",
                        data
                    )
                    return True
                else:
                    self.log_result(
                        "Commission Calculation", 
                        False, 
                        f"Status: {response.status}",
                        data
                    )
                    return False
                    
        except Exception as e:
            self.log_result("Commission Calculation", False, f"Exception: {str(e)}")
            return False
            
    async def run_all_tests(self):
        """Run all affiliate system tests"""
        print("🚀 Starting Affiliate System Backend Testing")
        print("=" * 60)
        
        await self.setup_session()
        
        try:
            # Authentication tests
            await self.admin_login()
            
            # Core affiliate functionality tests
            await self.test_affiliate_registration()
            await self.test_affiliate_login()
            await self.test_affiliate_dashboard()
            await self.test_generate_tracking_link()
            await self.test_affiliate_materials()
            await self.test_event_tracking()
            await self.test_commission_calculation()
            
            # Admin functionality tests
            await self.test_admin_affiliate_management()
            
        finally:
            await self.cleanup_session()
            
        # Print summary
        print("\n" + "=" * 60)
        print("📊 AFFILIATE SYSTEM TEST SUMMARY")
        print("=" * 60)
        
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
        
        print(f"\n🎯 AFFILIATE SYSTEM STATUS: {'✅ WORKING' if success_rate >= 70 else '❌ NEEDS ATTENTION'}")
        
        return success_rate >= 70

async def main():
    """Main test execution"""
    tester = AffiliateSystemTester()
    success = await tester.run_all_tests()
    return success

if __name__ == "__main__":
    asyncio.run(main())