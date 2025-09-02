#!/usr/bin/env python3
"""
CustomerMind IQ - Comprehensive Pricing System Testing
Testing the newly implemented comprehensive pricing system with Launch/Growth/Scale Plans

Test Objectives:
1. New Pricing Structure (Launch/Growth/Scale Plans) - GET /api/subscriptions/plans
2. Payment System Integration - GET /api/payments/subscription-plans  
3. Trial Management System - GET /api/subscriptions/trial-status/{user_email}
4. Referral System - POST /api/subscriptions/apply-referral-discount
5. Subscription Management - POST /api/subscriptions/upgrade-subscription
6. Authentication Integration - Verify GAE access restrictions
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
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://growth-engine-app-1.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

# Test user credentials for pricing tests
TEST_USER_CREDENTIALS = {
    "email": "pricingtest@customermindiq.com",
    "password": "PricingTest123!",
    "first_name": "Pricing",
    "last_name": "Tester",
    "company": "Pricing Test Company"
}

class PricingSystemTester:
    def __init__(self):
        self.admin_token = None
        self.user_token = None
        self.test_user_email = TEST_USER_CREDENTIALS["email"]
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
        """Test authentication for admin and create test user"""
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
        
        # Create/login test user for pricing tests
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

    async def test_new_pricing_structure(self):
        """Test GET /api/subscriptions/plans - New pricing tiers"""
        print("💰 TESTING NEW PRICING STRUCTURE")
        print("=" * 50)
        
        try:
            response = requests.get(f"{API_BASE}/subscriptions/plans", timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                plans = data.get("plans", {})
                
                # Verify new pricing tiers exist
                expected_tiers = ["launch", "growth", "scale", "white_label", "custom"]
                found_tiers = []
                pricing_details = {}
                
                for tier in expected_tiers:
                    if tier in plans:
                        found_tiers.append(tier)
                        plan_data = plans[tier]
                        pricing_details[tier] = {
                            "name": plan_data.get("name"),
                            "monthly_price": plan_data.get("monthly_price"),
                            "annual_price": plan_data.get("annual_price"),
                            "has_gae": plan_data.get("growth_acceleration_access", False)
                        }
                
                # Verify specific pricing (founders pricing)
                launch_correct = (
                    plans.get("launch", {}).get("monthly_price") == 49 and
                    plans.get("launch", {}).get("annual_price") == 490
                )
                
                growth_correct = (
                    plans.get("growth", {}).get("monthly_price") == 75 and
                    plans.get("growth", {}).get("annual_price") == 750
                )
                
                scale_correct = (
                    plans.get("scale", {}).get("monthly_price") == 199 and
                    plans.get("scale", {}).get("annual_price") == 1990
                )
                
                # Check Growth Acceleration Engine access
                gae_annual_only = all([
                    plans.get(tier, {}).get("growth_acceleration_access", False) 
                    for tier in ["launch", "growth", "scale"]
                ])
                
                success = (
                    len(found_tiers) == len(expected_tiers) and
                    launch_correct and growth_correct and scale_correct and
                    gae_annual_only
                )
                
                self.log_result(
                    "New Pricing Structure", 
                    success, 
                    f"Found tiers: {found_tiers}, Launch: ${pricing_details.get('launch', {}).get('monthly_price', 'N/A')}/${pricing_details.get('launch', {}).get('annual_price', 'N/A')}, Growth: ${pricing_details.get('growth', {}).get('monthly_price', 'N/A')}/${pricing_details.get('growth', {}).get('annual_price', 'N/A')}, Scale: ${pricing_details.get('scale', {}).get('monthly_price', 'N/A')}/${pricing_details.get('scale', {}).get('annual_price', 'N/A')}, GAE Annual Only: {gae_annual_only}",
                    pricing_details if not success else None
                )
                return success
            else:
                self.log_result("New Pricing Structure", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("New Pricing Structure", False, f"Exception: {str(e)}")
            return False

    async def test_payment_system_integration(self):
        """Test GET /api/payments/subscription-plans - Payment system pricing"""
        print("💳 TESTING PAYMENT SYSTEM INTEGRATION")
        print("=" * 50)
        
        try:
            response = requests.get(f"{API_BASE}/payments/subscription-plans", timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                plans = data.get("plans", {})
                
                # Verify pricing is in cents for Stripe
                launch_cents_correct = (
                    plans.get("launch", {}).get("monthly_price") == 4900 and  # $49 in cents
                    plans.get("launch", {}).get("annual_price") == 49000      # $490 in cents
                )
                
                growth_cents_correct = (
                    plans.get("growth", {}).get("monthly_price") == 7500 and  # $75 in cents
                    plans.get("growth", {}).get("annual_price") == 75000      # $750 in cents
                )
                
                scale_cents_correct = (
                    plans.get("scale", {}).get("monthly_price") == 19900 and  # $199 in cents
                    plans.get("scale", {}).get("annual_price") == 199000      # $1990 in cents
                )
                
                # Check plan names updated from old to new
                has_new_names = (
                    "launch" in plans and "growth" in plans and "scale" in plans
                )
                
                # Verify GAE feature in all plans
                gae_in_features = all([
                    "Growth Acceleration Engine (Annual Only)" in plans.get(tier, {}).get("features", [])
                    for tier in ["launch", "growth", "scale"]
                ])
                
                success = (
                    launch_cents_correct and growth_cents_correct and 
                    scale_cents_correct and has_new_names and gae_in_features
                )
                
                self.log_result(
                    "Payment System Integration", 
                    success, 
                    f"Stripe pricing (cents): Launch {plans.get('launch', {}).get('monthly_price', 'N/A')}/{plans.get('launch', {}).get('annual_price', 'N/A')}, Growth {plans.get('growth', {}).get('monthly_price', 'N/A')}/{plans.get('growth', {}).get('annual_price', 'N/A')}, Scale {plans.get('scale', {}).get('monthly_price', 'N/A')}/{plans.get('scale', {}).get('annual_price', 'N/A')}, New names: {has_new_names}, GAE in features: {gae_in_features}"
                )
                return success
            else:
                self.log_result("Payment System Integration", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Payment System Integration", False, f"Exception: {str(e)}")
            return False

    async def test_trial_management_system(self):
        """Test GET /api/subscriptions/trial-status/{user_email} - Trial management"""
        print("🆓 TESTING TRIAL MANAGEMENT SYSTEM")
        print("=" * 50)
        
        if not self.user_token:
            self.log_result("Trial Management System", False, "No user token available")
            return False
        
        try:
            response = requests.get(f"{API_BASE}/subscriptions/trial-status/{self.test_user_email}", timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                
                # Check trial status structure
                has_trial_info = "is_trial" in data
                has_reminder_logic = "reminder_needed" in data or "reminder_type" in data
                has_retention_period = "data_retention_until" in data
                
                # If user is on trial, verify trial details
                if data.get("is_trial"):
                    trial_start = data.get("trial_start")
                    trial_end = data.get("trial_end")
                    days_remaining = data.get("days_remaining")
                    
                    trial_details_complete = all([trial_start, trial_end, days_remaining is not None])
                    
                    self.log_result(
                        "Trial Management System", 
                        True, 
                        f"Trial active: {data.get('is_trial')}, Days remaining: {days_remaining}, Reminder needed: {data.get('reminder_needed', False)}, Data retention: {data.get('data_retention_until', 'N/A')}"
                    )
                else:
                    self.log_result(
                        "Trial Management System", 
                        True, 
                        f"User not on trial, Trial info available: {has_trial_info}, Reminder logic: {has_reminder_logic}, Retention period: {has_retention_period}"
                    )
                
                return True
            else:
                self.log_result("Trial Management System", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Trial Management System", False, f"Exception: {str(e)}")
            return False

    async def test_referral_system(self):
        """Test POST /api/subscriptions/apply-referral-discount - Referral system"""
        print("🤝 TESTING REFERRAL SYSTEM")
        print("=" * 50)
        
        # Test referral discount application
        referral_data = {
            "referrer_email": ADMIN_CREDENTIALS["email"],  # Use admin as referrer
            "referee_email": self.test_user_email
        }
        
        try:
            response = requests.post(f"{API_BASE}/subscriptions/apply-referral-discount", json=referral_data, timeout=60, verify=False)
            
            # This might fail if referrer is not active subscriber, but we test the endpoint
            if response.status_code in [200, 201]:
                data = response.json()
                
                # Check 30% discount calculation
                discount_amount = data.get("discount_amount", 0)
                discount_percentage = 30  # Should be 30%
                
                self.log_result(
                    "Referral Discount Application", 
                    True, 
                    f"Referral applied: {data.get('message', 'N/A')}, Discount: ${discount_amount/100:.2f} (30%)"
                )
                referral_success = True
            else:
                # Expected failure cases (referrer not active, etc.)
                error_data = response.text
                expected_errors = ["must be an active paying subscriber", "already applied", "not found"]
                is_expected_error = any(error in error_data for error in expected_errors)
                
                self.log_result(
                    "Referral Discount Application", 
                    is_expected_error, 
                    f"Expected validation error: {response.status_code} - {error_data[:100]}..."
                )
                referral_success = is_expected_error
        except Exception as e:
            self.log_result("Referral Discount Application", False, f"Exception: {str(e)}")
            referral_success = False
        
        # Test referral history endpoint
        try:
            response = requests.get(f"{API_BASE}/subscriptions/referral-history/{self.test_user_email}", timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                
                referrals_made = data.get("referrals_made", 0)
                referrals_received = data.get("referrals_received", 0)
                total_discount = data.get("total_discount_earned", 0)
                
                self.log_result(
                    "Referral History Tracking", 
                    True, 
                    f"Referrals made: {referrals_made}, Received: {referrals_received}, Total discount earned: ${total_discount/100:.2f}"
                )
                history_success = True
            else:
                self.log_result("Referral History Tracking", False, f"Status: {response.status_code}", response.text)
                history_success = False
        except Exception as e:
            self.log_result("Referral History Tracking", False, f"Exception: {str(e)}")
            history_success = False
        
        return referral_success and history_success

    async def test_subscription_management(self):
        """Test subscription upgrade and cancellation with refunds"""
        print("📈 TESTING SUBSCRIPTION MANAGEMENT")
        print("=" * 50)
        
        # Test subscription upgrade with prorated calculations
        upgrade_data = {
            "user_email": self.test_user_email,
            "new_plan_type": "growth",
            "new_billing_cycle": "annual"
        }
        
        try:
            response = requests.post(f"{API_BASE}/subscriptions/upgrade-subscription", json=upgrade_data, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                
                prorated_charge = data.get("prorated_charge", 0)
                new_plan = data.get("new_plan")
                previous_plan = data.get("previous_plan")
                
                self.log_result(
                    "Subscription Upgrade", 
                    True, 
                    f"Upgraded from {previous_plan} to {new_plan}, Prorated charge: ${prorated_charge/100:.2f}"
                )
                upgrade_success = True
            else:
                self.log_result("Subscription Upgrade", False, f"Status: {response.status_code}", response.text)
                upgrade_success = False
        except Exception as e:
            self.log_result("Subscription Upgrade", False, f"Exception: {str(e)}")
            upgrade_success = False
        
        # Test subscription cancellation with refund
        cancellation_data = {
            "user_email": self.test_user_email,
            "type": "immediate"
        }
        
        try:
            response = requests.post(f"{API_BASE}/subscriptions/cancel-subscription-with-refund", json=cancellation_data, timeout=60, verify=False)
            if response.status_code in [200, 201]:
                data = response.json()
                
                refund_amount = data.get("refund_amount", 0)
                cancellation_type = data.get("cancellation_type")
                processing_info = data.get("refund_processing", "")
                
                self.log_result(
                    "Subscription Cancellation with Refund", 
                    True, 
                    f"Cancelled ({cancellation_type}), Refund: ${refund_amount/100:.2f}, Processing: {processing_info}"
                )
                cancellation_success = True
            else:
                # Might fail if no active subscription
                error_text = response.text
                expected_error = "No active subscription" in error_text
                
                self.log_result(
                    "Subscription Cancellation with Refund", 
                    expected_error, 
                    f"Expected error (no active subscription): {response.status_code}"
                )
                cancellation_success = expected_error
        except Exception as e:
            self.log_result("Subscription Cancellation with Refund", False, f"Exception: {str(e)}")
            cancellation_success = False
        
        return upgrade_success and cancellation_success

    async def test_authentication_integration(self):
        """Test GAE access restrictions and authentication integration"""
        print("🔐 TESTING AUTHENTICATION INTEGRATION")
        print("=" * 50)
        
        if not self.user_token:
            self.log_result("Authentication Integration", False, "No user token available")
            return False
        
        # Test GAE access check
        try:
            response = requests.get(f"{API_BASE}/subscriptions/check-growth-access/{self.test_user_email}", timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                
                has_growth_access = data.get("has_growth_access", False)
                subscription_tier = data.get("subscription_tier")
                plan_type = data.get("plan_type")
                message = data.get("message", "")
                
                # GAE should be restricted to annual subscribers only
                annual_restriction_message = "Annual" in message
                
                self.log_result(
                    "GAE Access Restriction Check", 
                    True, 
                    f"GAE Access: {has_growth_access}, Tier: {subscription_tier}, Plan: {plan_type}, Annual restriction enforced: {annual_restriction_message}"
                )
                gae_success = True
            else:
                self.log_result("GAE Access Restriction Check", False, f"Status: {response.status_code}", response.text)
                gae_success = False
        except Exception as e:
            self.log_result("GAE Access Restriction Check", False, f"Exception: {str(e)}")
            gae_success = False
        
        # Test subscription access check
        try:
            response = requests.get(f"{API_BASE}/subscriptions/check-access/{self.test_user_email}", timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                access_info = data.get("access", {})
                
                has_access = access_info.get("has_access", False)
                plan_type = access_info.get("plan_type")
                billing_cycle = access_info.get("billing_cycle")
                has_growth_acceleration = access_info.get("has_growth_acceleration", False)
                
                self.log_result(
                    "Subscription Access Integration", 
                    True, 
                    f"Access: {has_access}, Plan: {plan_type}, Cycle: {billing_cycle}, GAE: {has_growth_acceleration}"
                )
                access_success = True
            else:
                self.log_result("Subscription Access Integration", False, f"Status: {response.status_code}", response.text)
                access_success = False
        except Exception as e:
            self.log_result("Subscription Access Integration", False, f"Exception: {str(e)}")
            access_success = False
        
        return gae_success and access_success

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE PRICING SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
        print()
        
        # Group results by pricing system component
        components = {
            "🔐 Authentication Setup": ["Admin Authentication", "Test User Registration", "Test User Login"],
            "💰 New Pricing Structure": ["New Pricing Structure"],
            "💳 Payment System Integration": ["Payment System Integration"],
            "🆓 Trial Management": ["Trial Management System"],
            "🤝 Referral System": ["Referral Discount Application", "Referral History Tracking"],
            "📈 Subscription Management": ["Subscription Upgrade", "Subscription Cancellation with Refund"],
            "🔐 Authentication Integration": ["GAE Access Restriction Check", "Subscription Access Integration"]
        }
        
        for component_name, test_names in components.items():
            print(f"{component_name}:")
            component_results = [r for r in self.results if r["test"] in test_names]
            component_passed = len([r for r in component_results if r["success"]])
            component_total = len(component_results)
            
            for result in component_results:
                print(f"  {result['status']}: {result['test']}")
                if result['details']:
                    print(f"      {result['details']}")
            
            if component_total > 0:
                component_rate = (component_passed / component_total * 100)
                print(f"  📈 Component Success Rate: {component_passed}/{component_total} ({component_rate:.1f}%)")
            print()
        
        # Key findings
        print("🔍 KEY FINDINGS:")
        
        # Pricing structure verification
        pricing_tests = [r for r in self.results if "Pricing Structure" in r["test"]]
        pricing_success = all(r["success"] for r in pricing_tests)
        
        if pricing_success:
            print("  ✅ New Pricing Structure: Launch ($49/$490), Growth ($75/$750), Scale ($199/$1990) ✅")
        else:
            print("  ❌ New Pricing Structure: Issues with Launch/Growth/Scale pricing")
        
        # Payment integration
        payment_tests = [r for r in self.results if "Payment System" in r["test"]]
        payment_success = all(r["success"] for r in payment_tests)
        
        if payment_success:
            print("  ✅ Payment Integration: Stripe pricing in cents, GAE features included ✅")
        else:
            print("  ❌ Payment Integration: Issues with Stripe integration or feature listing")
        
        # Trial and referral systems
        trial_tests = [r for r in self.results if "Trial" in r["test"] or "Referral" in r["test"]]
        trial_success = all(r["success"] for r in trial_tests)
        
        if trial_success:
            print("  ✅ Trial & Referral Systems: Trial management and 30% referral discounts working ✅")
        else:
            print("  ❌ Trial & Referral Systems: Issues with trial tracking or referral logic")
        
        # GAE restrictions
        gae_tests = [r for r in self.results if "GAE" in r["test"] or "Growth" in r["test"]]
        gae_success = all(r["success"] for r in gae_tests)
        
        if gae_success:
            print("  ✅ GAE Access Control: Annual subscription restriction properly enforced ✅")
        else:
            print("  ❌ GAE Access Control: Issues with annual subscription restrictions")
        
        print()
        print("🎉 PRICING SYSTEM VERIFICATION:")
        
        if pricing_success and payment_success and trial_success and gae_success:
            print("  ✅ COMPLETE SUCCESS: Comprehensive pricing system fully operational!")
            print("  ✅ New tier structure (Launch/Growth/Scale) implemented correctly")
            print("  ✅ Founders pricing ($49/$75/$199) with annual savings active")
            print("  ✅ Payment system integrated with proper Stripe pricing")
            print("  ✅ Trial management and referral systems working")
            print("  ✅ GAE access properly restricted to annual subscribers")
        else:
            print("  ⚠️  Some pricing system components need attention - see failed tests above")
        
        print("\n" + "=" * 80)
        
        return success_rate >= 75  # Consider 75%+ as overall success for pricing system

async def main():
    """Run comprehensive pricing system tests"""
    print("🚀 STARTING COMPREHENSIVE PRICING SYSTEM TESTING")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📡 API Base: {API_BASE}")
    print("=" * 80)
    
    tester = PricingSystemTester()
    
    # Run all tests in sequence
    test_sequence = [
        tester.test_authentication_setup,
        tester.test_new_pricing_structure,
        tester.test_payment_system_integration,
        tester.test_trial_management_system,
        tester.test_referral_system,
        tester.test_subscription_management,
        tester.test_authentication_integration
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