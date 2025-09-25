#!/usr/bin/env python3
"""
Advanced Affiliate Tracking System Backend Test
Tests the newly implemented advanced multi-method affiliate tracking system
"""

import asyncio
import httpx
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customeriq-hub.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class AdvancedTrackingSystemTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.admin_token = None
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    async def setup(self):
        """Setup test environment"""
        print("🔧 Setting up Advanced Affiliate Tracking System Test Environment...")
        
        # Get admin authentication
        try:
            login_response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
            )
            
            if login_response.status_code == 200:
                login_data = login_response.json()
                self.admin_token = login_data.get("access_token")
                print(f"✅ Admin authentication successful")
            else:
                print(f"❌ Admin authentication failed: {login_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
            
        return True
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
    
    async def test_click_tracking(self):
        """Test advanced click tracking endpoint"""
        print("\n🎯 Testing Advanced Click Tracking...")
        
        try:
            # Test click tracking with fingerprint data
            click_data = {
                "affiliate_id": "test_affiliate_001",
                "site_id": "customermindiq",
                "campaign_id": "test_campaign_001",
                "fingerprint_data": {
                    "screen_resolution": "1920x1080",
                    "timezone": "America/New_York",
                    "language": "en-US",
                    "platform": "Win32",
                    "canvas_fingerprint": "test_canvas_hash",
                    "webgl_fingerprint": "test_webgl_hash"
                }
            }
            
            response = await self.client.post(
                f"{API_BASE}/v2/track/click",
                json=click_data,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "X-Forwarded-For": "203.0.113.1",
                    "Referer": "https://example.com/affiliate-link"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if (result.get("success") and 
                    result.get("tracking_id") and 
                    "fraud_score" in result and
                    result.get("pixel_url")):
                    self.log_test_result(
                        "Advanced Click Tracking",
                        True,
                        f"Tracking ID: {result.get('tracking_id')}, Fraud Score: {result.get('fraud_score')}",
                        result
                    )
                else:
                    self.log_test_result(
                        "Advanced Click Tracking",
                        False,
                        f"Missing required fields in response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Advanced Click Tracking",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Advanced Click Tracking", False, f"Exception: {str(e)}")
    
    async def test_conversion_tracking(self):
        """Test advanced conversion tracking with multi-method attribution"""
        print("\n💰 Testing Advanced Conversion Tracking...")
        
        try:
            conversion_data = {
                "affiliate_id": "test_affiliate_001",
                "site_id": "customermindiq",
                "customer_email": "test.customer@example.com",
                "customer_id": "cust_12345",
                "event_type": "sale",
                "conversion_value": 750.0,
                "currency": "USD",
                "product_id": "growth_plan",
                "product_name": "Growth Plan Annual",
                "order_id": "order_67890",
                "custom_data": {
                    "subscription_tier": "growth",
                    "payment_method": "stripe"
                }
            }
            
            response = await self.client.post(
                f"{API_BASE}/v2/track/conversion",
                json=conversion_data,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "X-Forwarded-For": "203.0.113.1"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if (result.get("success") and 
                    result.get("conversion_id") and 
                    "attribution_methods" in result and
                    "fraud_risk" in result):
                    self.log_test_result(
                        "Advanced Conversion Tracking",
                        True,
                        f"Conversion ID: {result.get('conversion_id')}, Attribution Methods: {len(result.get('attribution_methods', []))}, Fraud Risk: {result.get('fraud_risk')}",
                        result
                    )
                else:
                    self.log_test_result(
                        "Advanced Conversion Tracking",
                        False,
                        f"Missing required fields in response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Advanced Conversion Tracking",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Advanced Conversion Tracking", False, f"Exception: {str(e)}")
    
    async def test_pixel_tracking(self):
        """Test pixel tracking functionality"""
        print("\n🖼️ Testing Pixel Tracking...")
        
        try:
            # Use a test tracking ID
            tracking_id = "test_track_pixel_001"
            
            response = await self.client.get(
                f"{API_BASE}/v2/track/pixel/{tracking_id}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "X-Forwarded-For": "203.0.113.1"
                }
            )
            
            if response.status_code == 200:
                # Check if it's a valid image response
                content_type = response.headers.get("content-type", "")
                if "image/png" in content_type and len(response.content) > 0:
                    self.log_test_result(
                        "Pixel Tracking",
                        True,
                        f"Pixel returned successfully, Content-Type: {content_type}, Size: {len(response.content)} bytes"
                    )
                else:
                    self.log_test_result(
                        "Pixel Tracking",
                        False,
                        f"Invalid pixel response - Content-Type: {content_type}, Size: {len(response.content)}"
                    )
            else:
                self.log_test_result(
                    "Pixel Tracking",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Pixel Tracking", False, f"Exception: {str(e)}")
    
    async def test_email_open_tracking(self):
        """Test email open tracking"""
        print("\n📧 Testing Email Open Tracking...")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/v2/track/email/open",
                params={
                    "affiliate_id": "test_affiliate_001",
                    "customer_email": "test.customer@example.com",
                    "email_campaign_id": "campaign_001"
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "X-Forwarded-For": "203.0.113.1"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("tracked") == "email_open":
                    self.log_test_result(
                        "Email Open Tracking",
                        True,
                        "Email open tracked successfully",
                        result
                    )
                else:
                    self.log_test_result(
                        "Email Open Tracking",
                        False,
                        f"Unexpected response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Email Open Tracking",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Email Open Tracking", False, f"Exception: {str(e)}")
    
    async def test_email_click_tracking(self):
        """Test email click tracking"""
        print("\n🔗 Testing Email Click Tracking...")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/v2/track/email/click",
                params={
                    "affiliate_id": "test_affiliate_001",
                    "customer_email": "test.customer@example.com",
                    "email_campaign_id": "campaign_001",
                    "link_id": "cta_button_1"
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "X-Forwarded-For": "203.0.113.1"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("tracked") == "email_click":
                    self.log_test_result(
                        "Email Click Tracking",
                        True,
                        "Email click tracked successfully",
                        result
                    )
                else:
                    self.log_test_result(
                        "Email Click Tracking",
                        False,
                        f"Unexpected response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Email Click Tracking",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Email Click Tracking", False, f"Exception: {str(e)}")
    
    async def test_attribution_retrieval(self):
        """Test attribution data retrieval"""
        print("\n🔍 Testing Attribution Data Retrieval...")
        
        try:
            # Use email hash as customer identifier
            customer_identifier = "test_customer_hash_001"
            
            response = await self.client.get(
                f"{API_BASE}/v2/track/attribution/{customer_identifier}",
                params={"lookback_days": 30}
            )
            
            if response.status_code == 200:
                result = response.json()
                if (result.get("success") and 
                    "attribution_data" in result and
                    result.get("customer_identifier") == customer_identifier):
                    self.log_test_result(
                        "Attribution Data Retrieval",
                        True,
                        f"Attribution data retrieved for {customer_identifier}",
                        result
                    )
                else:
                    self.log_test_result(
                        "Attribution Data Retrieval",
                        False,
                        f"Missing required fields in response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Attribution Data Retrieval",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Attribution Data Retrieval", False, f"Exception: {str(e)}")
    
    async def test_fraud_detection_stats(self):
        """Test fraud detection statistics (Admin only)"""
        print("\n🛡️ Testing Fraud Detection Statistics...")
        
        if not self.admin_token:
            self.log_test_result("Fraud Detection Statistics", False, "No admin token available")
            return
        
        try:
            response = await self.client.get(
                f"{API_BASE}/v2/track/stats/fraud",
                params={
                    "affiliate_id": "test_affiliate_001",
                    "days_back": 7
                },
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if (result.get("success") and 
                    "fraud_stats" in result and
                    "total_clicks" in result["fraud_stats"]):
                    fraud_stats = result["fraud_stats"]
                    self.log_test_result(
                        "Fraud Detection Statistics",
                        True,
                        f"Total clicks: {fraud_stats.get('total_clicks')}, Fraud rate: {fraud_stats.get('fraud_rate', 0):.2%}",
                        result
                    )
                else:
                    self.log_test_result(
                        "Fraud Detection Statistics",
                        False,
                        f"Missing required fields in response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Fraud Detection Statistics",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Fraud Detection Statistics", False, f"Exception: {str(e)}")
    
    async def test_health_check(self):
        """Test tracking system health check"""
        print("\n❤️ Testing Tracking System Health Check...")
        
        try:
            response = await self.client.get(f"{API_BASE}/v2/track/health")
            
            if response.status_code == 200:
                result = response.json()
                if (result.get("status") in ["healthy", "degraded"] and 
                    "components" in result and
                    "tracking_methods" in result):
                    components = result["components"]
                    healthy_components = sum(1 for status in components.values() if status == "healthy")
                    total_components = len(components)
                    
                    self.log_test_result(
                        "Tracking System Health Check",
                        True,
                        f"Status: {result.get('status')}, Components: {healthy_components}/{total_components} healthy",
                        result
                    )
                else:
                    self.log_test_result(
                        "Tracking System Health Check",
                        False,
                        f"Missing required fields in response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Tracking System Health Check",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Tracking System Health Check", False, f"Exception: {str(e)}")
    
    async def test_v2_commission_creation(self):
        """Test V2 commission creation with tracking integration"""
        print("\n💳 Testing V2 Commission Creation with Tracking...")
        
        try:
            commission_data = {
                "affiliate_id": "test_affiliate_001",
                "customer_email": "test.customer@example.com",
                "plan_type": "growth",
                "commission_amount": 225.0,
                "tracking_id": "test_track_commission_001",
                "site_id": "customermindiq"
            }
            
            response = await self.client.post(
                f"{API_BASE}/affiliate/v2/commission/create",
                params=commission_data
            )
            
            if response.status_code == 200:
                result = response.json()
                if (result.get("success") and 
                    result.get("commission_id") and
                    "breakdown" in result and
                    "tracking_integration" in result):
                    breakdown = result["breakdown"]
                    self.log_test_result(
                        "V2 Commission Creation",
                        True,
                        f"Commission ID: {result.get('commission_id')}, Total: ${result.get('total_commission')}, Base: ${breakdown.get('base_commission')}",
                        result
                    )
                else:
                    self.log_test_result(
                        "V2 Commission Creation",
                        False,
                        f"Missing required fields in response: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "V2 Commission Creation",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("V2 Commission Creation", False, f"Exception: {str(e)}")
    
    async def test_tracking_integration_test(self):
        """Test tracking integration test endpoint"""
        print("\n🔧 Testing Tracking Integration Test...")
        
        try:
            response = await self.client.get(
                f"{API_BASE}/affiliate/v2/tracking/integration-test",
                params={
                    "affiliate_id": "test_affiliate_001",
                    "customer_email": "integration.test@example.com"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if (result.get("success") and 
                    result.get("integration_test") == "passed" and
                    result.get("test_tracking_id")):
                    self.log_test_result(
                        "Tracking Integration Test",
                        True,
                        f"Integration test passed, Test Tracking ID: {result.get('test_tracking_id')}",
                        result
                    )
                else:
                    self.log_test_result(
                        "Tracking Integration Test",
                        False,
                        f"Integration test failed or missing fields: {result}",
                        result
                    )
            else:
                self.log_test_result(
                    "Tracking Integration Test",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    response.text
                )
                
        except Exception as e:
            self.log_test_result("Tracking Integration Test", False, f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all advanced tracking system tests"""
        print("🚀 Starting Advanced Affiliate Tracking System Comprehensive Testing...")
        print(f"🌐 Backend URL: {BACKEND_URL}")
        print("=" * 80)
        
        # Setup
        if not await self.setup():
            print("❌ Setup failed, aborting tests")
            return
        
        # Run all tests
        await self.test_click_tracking()
        await self.test_conversion_tracking()
        await self.test_pixel_tracking()
        await self.test_email_open_tracking()
        await self.test_email_click_tracking()
        await self.test_attribution_retrieval()
        await self.test_fraud_detection_stats()
        await self.test_health_check()
        await self.test_v2_commission_creation()
        await self.test_tracking_integration_test()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("🎯 ADVANCED AFFILIATE TRACKING SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📊 Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.total_tests - self.passed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Advanced tracking system is working perfectly!")
        elif success_rate >= 70:
            print("✅ GOOD: Advanced tracking system is mostly functional with minor issues")
        elif success_rate >= 50:
            print("⚠️ MODERATE: Advanced tracking system has some significant issues")
        else:
            print("❌ CRITICAL: Advanced tracking system has major problems")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['details']}")
        
        # Show successful tests
        successful_tests = [result for result in self.test_results if result["success"]]
        if successful_tests:
            print("\n✅ SUCCESSFUL TESTS:")
            for test in successful_tests:
                print(f"   • {test['test']}: {test['details']}")
        
        print("\n" + "=" * 80)
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.client.aclose()

async def main():
    """Main test execution"""
    tester = AdvancedTrackingSystemTester()
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(main())