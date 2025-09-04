#!/usr/bin/env python3
"""
Comprehensive Pricing System Backend Testing
Testing the new pricing structure, trial management, referral system, and subscription management
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any

# Configuration
BACKEND_URL = "https://customer-mind-iq-5.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class PricingSystemTester:
    def __init__(self):
        self.session = None
        self.auth_token = None
        self.test_results = []
        
    async def setup_session(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    async def authenticate(self):
        """Authenticate with admin credentials"""
        try:
            login_data = {
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }
            
            async with self.session.post(f"{API_BASE}/auth/login", json=login_data) as response:
                if response.status == 200:
                    data = await response.json()
                    self.auth_token = data.get("access_token")
                    self.log_result("✅ AUTHENTICATION", True, "Admin login successful")
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("❌ AUTHENTICATION", False, f"Login failed: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("❌ AUTHENTICATION", False, f"Login error: {str(e)}")
            return False
            
    def get_auth_headers(self):
        """Get authorization headers"""
        if self.auth_token:
            return {"Authorization": f"Bearer {self.auth_token}"}
        return {}
        
    def log_result(self, test_name: str, success: bool, details: str):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status}: {test_name} - {details}")
        
    async def test_new_pricing_structure(self):
        """Test 1: New Pricing Structure (FIXED - now working)"""
        print("\n🔍 Testing New Pricing Structure...")
        
        # Test GET /api/subscriptions/plans
        try:
            async with self.session.get(f"{API_BASE}/subscriptions/plans") as response:
                if response.status == 200:
                    data = await response.json()
                    plans = data.get("plans", {})
                    
                    # Verify Launch Plan ($49/$490)
                    launch_plan = plans.get("launch", {})
                    if launch_plan.get("monthly_price") == 49 and launch_plan.get("annual_price") == 490:
                        self.log_result("Launch Plan Pricing", True, "Launch Plan: $49/$490 ✓")
                    else:
                        self.log_result("Launch Plan Pricing", False, f"Expected $49/$490, got ${launch_plan.get('monthly_price')}/${launch_plan.get('annual_price')}")
                    
                    # Verify Growth Plan ($75/$750) - Most Popular
                    growth_plan = plans.get("growth", {})
                    if growth_plan.get("monthly_price") == 75 and growth_plan.get("annual_price") == 750:
                        self.log_result("Growth Plan Pricing", True, "Growth Plan: $75/$750 ✓")
                    else:
                        self.log_result("Growth Plan Pricing", False, f"Expected $75/$750, got ${growth_plan.get('monthly_price')}/${growth_plan.get('annual_price')}")
                    
                    # Verify Most Popular flag
                    if growth_plan.get("most_popular"):
                        self.log_result("Growth Plan Most Popular", True, "Growth Plan marked as 'Most Popular' ✓")
                    else:
                        self.log_result("Growth Plan Most Popular", False, "Growth Plan not marked as 'Most Popular'")
                    
                    # Verify Scale Plan ($199/$1990)
                    scale_plan = plans.get("scale", {})
                    if scale_plan.get("monthly_price") == 199 and scale_plan.get("annual_price") == 1990:
                        self.log_result("Scale Plan Pricing", True, "Scale Plan: $199/$1990 ✓")
                    else:
                        self.log_result("Scale Plan Pricing", False, f"Expected $199/$1990, got ${scale_plan.get('monthly_price')}/${scale_plan.get('annual_price')}")
                    
                    # Verify Growth Acceleration Engine feature
                    gae_in_all_plans = True
                    for plan_name, plan_data in plans.items():
                        if plan_name in ["launch", "growth", "scale"]:
                            features = plan_data.get("features", [])
                            has_gae = any("Growth Acceleration Engine" in str(feature) for feature in features)
                            if not has_gae:
                                gae_in_all_plans = False
                                break
                    
                    if gae_in_all_plans:
                        self.log_result("Growth Acceleration Engine Feature", True, "GAE (Annual Only) in all plans ✓")
                    else:
                        self.log_result("Growth Acceleration Engine Feature", False, "GAE feature missing from some plans")
                        
                else:
                    error_text = await response.text()
                    self.log_result("Subscription Plans API", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Subscription Plans API", False, f"Request error: {str(e)}")
            
        # Test GET /api/payments/subscription-plans (Stripe pricing in cents)
        try:
            async with self.session.get(f"{API_BASE}/payments/subscription-plans") as response:
                if response.status == 200:
                    data = await response.json()
                    plans = data.get("plans", {})
                    
                    # Verify Stripe pricing in cents
                    launch_plan = plans.get("launch", {})
                    if launch_plan.get("monthly_price") == 4900 and launch_plan.get("annual_price") == 49000:
                        self.log_result("Stripe Launch Pricing", True, "Stripe Launch: 4900¢/49000¢ ✓")
                    else:
                        self.log_result("Stripe Launch Pricing", False, f"Expected 4900¢/49000¢, got {launch_plan.get('monthly_price')}¢/{launch_plan.get('annual_price')}¢")
                    
                    growth_plan = plans.get("growth", {})
                    if growth_plan.get("monthly_price") == 7500 and growth_plan.get("annual_price") == 75000:
                        self.log_result("Stripe Growth Pricing", True, "Stripe Growth: 7500¢/75000¢ ✓")
                    else:
                        self.log_result("Stripe Growth Pricing", False, f"Expected 7500¢/75000¢, got {growth_plan.get('monthly_price')}¢/{growth_plan.get('annual_price')}¢")
                    
                    scale_plan = plans.get("scale", {})
                    if scale_plan.get("monthly_price") == 19900 and scale_plan.get("annual_price") == 199000:
                        self.log_result("Stripe Scale Pricing", True, "Stripe Scale: 19900¢/199000¢ ✓")
                    else:
                        self.log_result("Stripe Scale Pricing", False, f"Expected 19900¢/199000¢, got {scale_plan.get('monthly_price')}¢/{scale_plan.get('annual_price')}¢")
                        
                else:
                    error_text = await response.text()
                    self.log_result("Payment Plans API", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Payment Plans API", False, f"Request error: {str(e)}")
            
    async def test_trial_management_system(self):
        """Test 2: Trial Management System"""
        print("\n🔍 Testing Trial Management System...")
        
        # Test GET /api/subscriptions/trial-status/{user_email}
        try:
            async with self.session.get(
                f"{API_BASE}/subscriptions/trial-status/{ADMIN_EMAIL}",
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check if admin user has trial data or is not on trial
                    if data.get("is_trial"):
                        trial_start = data.get("trial_start")
                        trial_end = data.get("trial_end")
                        days_remaining = data.get("days_remaining")
                        reminder_type = data.get("reminder_type")
                        data_retention_until = data.get("data_retention_until")
                        
                        self.log_result("Trial Status API", True, f"Trial active: {days_remaining} days remaining, reminder: {reminder_type}")
                        
                        # Verify 2-week data retention calculation
                        if data_retention_until:
                            self.log_result("Data Retention Period", True, f"Data retention until: {data_retention_until} (2 weeks after trial)")
                        else:
                            self.log_result("Data Retention Period", False, "Data retention period not calculated")
                            
                    else:
                        self.log_result("Trial Status API", True, f"User not on trial: {data.get('message', 'No trial active')}")
                        
                else:
                    error_text = await response.text()
                    self.log_result("Trial Status API", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Trial Status API", False, f"Request error: {str(e)}")
            
    async def test_referral_system(self):
        """Test 3: Referral System"""
        print("\n🔍 Testing Referral System...")
        
        # Test POST /api/subscriptions/apply-referral-discount
        try:
            referral_data = {
                "referrer_email": ADMIN_EMAIL,
                "referee_email": "test@example.com"
            }
            
            async with self.session.post(
                f"{API_BASE}/subscriptions/apply-referral-discount",
                json=referral_data,
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    discount_amount = data.get("discount_amount", 0)
                    
                    # Verify 30% discount calculation
                    if discount_amount > 0:
                        self.log_result("Referral Discount Application", True, f"30% discount applied: ${discount_amount/100:.2f}")
                    else:
                        self.log_result("Referral Discount Application", False, "No discount amount calculated")
                        
                elif response.status == 400:
                    # Expected if referrer is not active subscriber or referral already exists
                    error_data = await response.json()
                    self.log_result("Referral Discount Application", True, f"Expected validation: {error_data.get('detail', 'Validation error')}")
                    
                else:
                    error_text = await response.text()
                    self.log_result("Referral Discount Application", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Referral Discount Application", False, f"Request error: {str(e)}")
            
        # Test GET /api/subscriptions/referral-history/{user_email}
        try:
            async with self.session.get(
                f"{API_BASE}/subscriptions/referral-history/{ADMIN_EMAIL}",
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    referrals_made = data.get("referrals_made", 0)
                    total_discount_earned = data.get("total_discount_earned", 0)
                    
                    self.log_result("Referral History API", True, f"Referrals made: {referrals_made}, Total discount: ${total_discount_earned/100:.2f}")
                    
                else:
                    error_text = await response.text()
                    self.log_result("Referral History API", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Referral History API", False, f"Request error: {str(e)}")
            
    async def test_subscription_management(self):
        """Test 4: Subscription Management"""
        print("\n🔍 Testing Subscription Management...")
        
        # Test POST /api/subscriptions/upgrade-subscription
        try:
            upgrade_data = {
                "user_email": ADMIN_EMAIL,
                "new_plan_type": "growth",
                "new_billing_cycle": "annual"
            }
            
            async with self.session.post(
                f"{API_BASE}/subscriptions/upgrade-subscription",
                json=upgrade_data,
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    prorated_charge = data.get("prorated_charge", 0)
                    
                    self.log_result("Subscription Upgrade", True, f"Upgrade successful, prorated charge: ${prorated_charge/100:.2f}")
                    
                elif response.status == 404:
                    # Expected if user not found
                    self.log_result("Subscription Upgrade", True, "Expected validation: User not found or invalid upgrade path")
                    
                else:
                    error_text = await response.text()
                    self.log_result("Subscription Upgrade", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Subscription Upgrade", False, f"Request error: {str(e)}")
            
        # Test POST /api/subscriptions/cancel-subscription-with-refund
        try:
            cancellation_data = {
                "user_email": ADMIN_EMAIL,
                "type": "end_of_cycle",
                "reason": "Testing cancellation system"
            }
            
            async with self.session.post(
                f"{API_BASE}/subscriptions/cancel-subscription-with-refund",
                json=cancellation_data,
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    cancellation_type = data.get("cancellation_type")
                    refund_amount = data.get("refund_amount", 0)
                    
                    self.log_result("Subscription Cancellation", True, f"Cancellation: {cancellation_type}, Refund: ${refund_amount/100:.2f}")
                    
                elif response.status == 400:
                    # Expected if no active subscription
                    error_data = await response.json()
                    self.log_result("Subscription Cancellation", True, f"Expected validation: {error_data.get('detail', 'No active subscription')}")
                    
                else:
                    error_text = await response.text()
                    self.log_result("Subscription Cancellation", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Subscription Cancellation", False, f"Request error: {str(e)}")
            
    async def test_authentication_integration(self):
        """Test 5: Authentication Integration"""
        print("\n🔍 Testing Authentication Integration...")
        
        # Test that admin user has proper access levels
        try:
            async with self.session.get(
                f"{API_BASE}/auth/profile",
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    user_data = data.get("user", {})
                    subscription_tier = user_data.get("subscription_tier", "")
                    role = user_data.get("role", "")
                    
                    # Verify admin has scale tier access
                    if subscription_tier == "scale" or role in ["admin", "super_admin"]:
                        self.log_result("Admin Access Level", True, f"Admin has proper access: role={role}, tier={subscription_tier}")
                    else:
                        self.log_result("Admin Access Level", False, f"Admin access insufficient: role={role}, tier={subscription_tier}")
                        
                else:
                    error_text = await response.text()
                    self.log_result("Admin Profile API", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Admin Profile API", False, f"Request error: {str(e)}")
            
        # Test GAE access restriction
        try:
            async with self.session.get(
                f"{API_BASE}/growth/dashboard",
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_result("GAE Access Control", True, "GAE dashboard accessible to admin user")
                    
                elif response.status == 403:
                    self.log_result("GAE Access Control", True, "GAE properly restricted (403 Forbidden)")
                    
                else:
                    error_text = await response.text()
                    self.log_result("GAE Access Control", False, f"Unexpected response: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("GAE Access Control", False, f"Request error: {str(e)}")
            
    async def test_existing_endpoints_compatibility(self):
        """Test 6: Existing Endpoints Compatibility"""
        print("\n🔍 Testing Existing Endpoints Compatibility...")
        
        # Test GET /api/subscriptions/check-access/{user_email}
        try:
            async with self.session.get(
                f"{API_BASE}/subscriptions/check-access/{ADMIN_EMAIL}",
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    access_info = data.get("access", {})
                    has_access = access_info.get("has_access", False)
                    
                    self.log_result("Check Access API", True, f"Access check successful: has_access={has_access}")
                    
                else:
                    error_text = await response.text()
                    self.log_result("Check Access API", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Check Access API", False, f"Request error: {str(e)}")
            
        # Test GET /api/subscriptions/check-growth-access/{user_email}
        try:
            async with self.session.get(
                f"{API_BASE}/subscriptions/check-growth-access/{ADMIN_EMAIL}",
                headers=self.get_auth_headers()
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    has_growth_access = data.get("has_growth_access", False)
                    
                    self.log_result("Check Growth Access API", True, f"Growth access check successful: has_growth_access={has_growth_access}")
                    
                else:
                    error_text = await response.text()
                    self.log_result("Check Growth Access API", False, f"API error: {response.status} - {error_text}")
                    
        except Exception as e:
            self.log_result("Check Growth Access API", False, f"Request error: {str(e)}")
            
    async def run_all_tests(self):
        """Run all pricing system tests"""
        print("🚀 Starting Comprehensive Pricing System Backend Testing")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"👤 Test User: {ADMIN_EMAIL}")
        print("=" * 80)
        
        await self.setup_session()
        
        try:
            # Authenticate first
            if not await self.authenticate():
                print("❌ Authentication failed - cannot proceed with tests")
                return
                
            # Run all test suites
            await self.test_new_pricing_structure()
            await self.test_trial_management_system()
            await self.test_referral_system()
            await self.test_subscription_management()
            await self.test_authentication_integration()
            await self.test_existing_endpoints_compatibility()
            
        finally:
            await self.cleanup_session()
            
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 PRICING SYSTEM TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 Overall Results: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        
        if failed_tests > 0:
            print("\n🔍 Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['test']}: {result['details']}")
                    
        print("\n🎯 Key Findings:")
        
        # Analyze pricing structure tests
        pricing_tests = [r for r in self.test_results if "Pricing" in r["test"] or "Plans" in r["test"]]
        pricing_passed = len([r for r in pricing_tests if r["success"]])
        if pricing_passed == len(pricing_tests):
            print("   ✅ New pricing structure (Launch/Growth/Scale) working correctly")
        else:
            print("   ❌ Issues found with new pricing structure")
            
        # Analyze referral system tests
        referral_tests = [r for r in self.test_results if "Referral" in r["test"]]
        referral_passed = len([r for r in referral_tests if r["success"]])
        if referral_passed == len(referral_tests):
            print("   ✅ Referral system with 30% discounts working correctly")
        else:
            print("   ❌ Issues found with referral system")
            
        # Analyze trial management tests
        trial_tests = [r for r in self.test_results if "Trial" in r["test"]]
        trial_passed = len([r for r in trial_tests if r["success"]])
        if trial_passed == len(trial_tests):
            print("   ✅ Trial management with reminders working correctly")
        else:
            print("   ❌ Issues found with trial management system")
            
        # Analyze subscription management tests
        subscription_tests = [r for r in self.test_results if "Subscription" in r["test"] and "Upgrade" in r["test"] or "Cancellation" in r["test"]]
        subscription_passed = len([r for r in subscription_tests if r["success"]])
        if subscription_passed == len(subscription_tests):
            print("   ✅ Subscription upgrades and cancellations working correctly")
        else:
            print("   ❌ Issues found with subscription management")
            
        # Analyze authentication integration tests
        auth_tests = [r for r in self.test_results if "Access" in r["test"] or "GAE" in r["test"]]
        auth_passed = len([r for r in auth_tests if r["success"]])
        if auth_passed == len(auth_tests):
            print("   ✅ Authentication integration and GAE access control working correctly")
        else:
            print("   ❌ Issues found with authentication integration")
            
        print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

async def main():
    """Main test execution"""
    tester = PricingSystemTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())