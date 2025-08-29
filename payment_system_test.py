#!/usr/bin/env python3
"""
Customer Mind IQ - Payment System Integration Testing
Comprehensive testing for Stripe checkout and subscription management
"""

import requests
import json
import time
from datetime import datetime
import uuid

class PaymentSystemTester:
    def __init__(self, base_url="https://customer-mind-iq-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.demo_email = "demo@customermindiq.com"
        self.demo_user_id = "demo_user_123"
        self.test_session_id = None
        self.test_transaction_id = None
        
    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=60):
        """Run a payment system API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PaymentSystemTester/1.0'
        }

        self.tests_run += 1
        print(f"\n💳 Testing Payment System: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout, verify=True)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout, verify=True)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=timeout, verify=True)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout, verify=True)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:300]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:300]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_subscription_plans(self):
        """Test subscription plans API endpoint"""
        print("\n🎯 Testing Subscription Plans API...")
        
        success, data = self.run_test(
            "Get Subscription Plans",
            "GET",
            "api/payments/subscription/plans",
            200
        )
        
        if success and data:
            plans = data.get('plans', {})
            print(f"   Plans available: {list(plans.keys())}")
            
            # Verify required plans exist
            required_plans = ['free', 'professional', 'enterprise']
            for plan_id in required_plans:
                if plan_id in plans:
                    plan = plans[plan_id]
                    print(f"   ✅ {plan_id.title()} Plan: ${plan.get('price', 0)}/month")
                    print(f"      Features: {len(plan.get('features', []))} features")
                    print(f"      Limits: {len(plan.get('limits', {}))} limit types")
                else:
                    print(f"   ❌ Missing required plan: {plan_id}")
                    return False
            
            # Verify pricing
            if plans.get('free', {}).get('price') == 0.0:
                print("   ✅ Free tier correctly priced at $0")
            if plans.get('professional', {}).get('price') == 99.0:
                print("   ✅ Professional tier correctly priced at $99")
            if plans.get('enterprise', {}).get('price') == 299.0:
                print("   ✅ Enterprise tier correctly priced at $299")
                
            return True
        
        return False

    def test_free_subscription_checkout(self):
        """Test free subscription checkout (no payment required)"""
        print("\n🆓 Testing Free Subscription Checkout...")
        
        checkout_data = {
            "plan_id": "free",
            "origin_url": "https://customermindiq.com",
            "metadata": {
                "user_email": self.demo_email,
                "source": "test_suite"
            }
        }
        
        success, data = self.run_test(
            "Free Subscription Checkout",
            "POST",
            "api/payments/subscription/checkout",
            200,
            data=checkout_data
        )
        
        if success and data:
            if data.get('success') and data.get('message') == "Free subscription activated":
                print("   ✅ Free subscription activated immediately")
                print(f"   Subscription ID: {data.get('subscription_id')}")
                return True
            else:
                print("   ❌ Free subscription not properly activated")
                return False
        
        return False

    def test_paid_subscription_checkout(self):
        """Test paid subscription checkout (Professional plan)"""
        print("\n💰 Testing Paid Subscription Checkout...")
        
        checkout_data = {
            "plan_id": "professional",
            "origin_url": "https://customermindiq.com",
            "metadata": {
                "user_email": self.demo_email,
                "user_id": self.demo_user_id,
                "source": "test_suite"
            }
        }
        
        success, data = self.run_test(
            "Professional Subscription Checkout",
            "POST",
            "api/payments/subscription/checkout",
            200,
            data=checkout_data
        )
        
        if success and data:
            if data.get('success') and data.get('checkout_url'):
                print("   ✅ Stripe checkout session created")
                print(f"   Checkout URL: {data.get('checkout_url')[:50]}...")
                print(f"   Session ID: {data.get('session_id')}")
                print(f"   Transaction ID: {data.get('transaction_id')}")
                
                # Store for later tests
                self.test_session_id = data.get('session_id')
                self.test_transaction_id = data.get('transaction_id')
                
                # Verify plan details
                plan = data.get('plan', {})
                if plan.get('price') == 99.0:
                    print("   ✅ Professional plan pricing correct ($99)")
                
                return True
            else:
                print("   ❌ Checkout session not created properly")
                return False
        
        return False

    def test_enterprise_subscription_checkout(self):
        """Test enterprise subscription checkout"""
        print("\n🏢 Testing Enterprise Subscription Checkout...")
        
        checkout_data = {
            "plan_id": "enterprise",
            "origin_url": "https://customermindiq.com",
            "metadata": {
                "user_email": self.demo_email,
                "user_id": self.demo_user_id,
                "source": "test_suite",
                "company": "Test Enterprise Corp"
            }
        }
        
        success, data = self.run_test(
            "Enterprise Subscription Checkout",
            "POST",
            "api/payments/subscription/checkout",
            200,
            data=checkout_data
        )
        
        if success and data:
            if data.get('success') and data.get('checkout_url'):
                print("   ✅ Enterprise checkout session created")
                print(f"   Session ID: {data.get('session_id')}")
                
                # Verify plan details
                plan = data.get('plan', {})
                if plan.get('price') == 299.0:
                    print("   ✅ Enterprise plan pricing correct ($299)")
                
                return True
            else:
                print("   ❌ Enterprise checkout session not created properly")
                return False
        
        return False

    def test_payment_status_check(self):
        """Test payment status check endpoint"""
        print("\n🔍 Testing Payment Status Check...")
        
        if not self.test_session_id:
            print("   ⚠️  No session ID available from previous tests, using mock session")
            test_session_id = "cs_test_mock_session_id_123"
        else:
            test_session_id = self.test_session_id
        
        success, data = self.run_test(
            "Payment Status Check",
            "GET",
            f"api/payments/checkout/status/{test_session_id}",
            200  # Expecting 200 even for mock session (should handle gracefully)
        )
        
        if success and data:
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Payment Status: {data.get('payment_status', 'unknown')}")
            if data.get('transaction_id'):
                print(f"   Transaction ID: {data.get('transaction_id')}")
            return True
        else:
            # Try with 404 status for non-existent session
            success, data = self.run_test(
                "Payment Status Check (Non-existent)",
                "GET",
                f"api/payments/checkout/status/{test_session_id}",
                404
            )
            if success:
                print("   ✅ Properly handles non-existent session with 404")
                return True
        
        return False

    def test_current_subscription_status(self):
        """Test current subscription status endpoint"""
        print("\n📊 Testing Current Subscription Status...")
        
        # Test with email parameter
        success, data = self.run_test(
            "Current Subscription Status (by email)",
            "GET",
            f"api/payments/subscription/current?email={self.demo_email}",
            200
        )
        
        if success and data:
            subscription = data.get('subscription', {})
            print(f"   Current Plan: {subscription.get('current_plan', 'unknown')}")
            print(f"   Status: {subscription.get('status', 'unknown')}")
            print(f"   Features: {len(subscription.get('features', []))} features")
            print(f"   Limits: {len(subscription.get('limits', {}))} limit types")
            
            # Test with user_id parameter
            success2, data2 = self.run_test(
                "Current Subscription Status (by user_id)",
                "GET",
                f"api/payments/subscription/current?user_id={self.demo_user_id}",
                200
            )
            
            return success2
        
        return False

    def test_transaction_history(self):
        """Test transaction history endpoint"""
        print("\n📜 Testing Transaction History...")
        
        # Test with email parameter
        success, data = self.run_test(
            "Transaction History (by email)",
            "GET",
            f"api/payments/transactions/history?email={self.demo_email}&limit=5",
            200
        )
        
        if success and data:
            transactions = data.get('transactions', [])
            total = data.get('total', 0)
            print(f"   Total transactions: {total}")
            print(f"   Transactions returned: {len(transactions)}")
            
            if transactions:
                for i, tx in enumerate(transactions[:3]):  # Show first 3
                    print(f"   Transaction {i+1}: {tx.get('plan_id', 'unknown')} - ${tx.get('amount', 0)} - {tx.get('payment_status', 'unknown')}")
            
            # Test with user_id parameter
            success2, data2 = self.run_test(
                "Transaction History (by user_id)",
                "GET",
                f"api/payments/transactions/history?user_id={self.demo_user_id}&limit=10",
                200
            )
            
            return success2
        
        return False

    def test_subscription_cancellation(self):
        """Test subscription cancellation endpoint"""
        print("\n❌ Testing Subscription Cancellation...")
        
        # Test cancellation with email
        success, data = self.run_test(
            "Cancel Subscription (by email)",
            "POST",
            f"api/payments/subscription/cancel?email={self.demo_email}",
            200  # Expecting success even if no subscription exists
        )
        
        if success and data:
            if data.get('success'):
                print("   ✅ Cancellation request processed successfully")
                print(f"   Message: {data.get('message', 'No message')}")
                return True
            else:
                print("   ❌ Cancellation request failed")
                return False
        else:
            # Try with 404 for non-existent subscription
            success, data = self.run_test(
                "Cancel Subscription (non-existent)",
                "POST",
                f"api/payments/subscription/cancel?email=nonexistent@test.com",
                404
            )
            if success:
                print("   ✅ Properly handles non-existent subscription with 404")
                return True
        
        return False

    def test_admin_dashboard(self):
        """Test admin dashboard endpoint"""
        print("\n📈 Testing Admin Dashboard...")
        
        success, data = self.run_test(
            "Admin Payment Dashboard",
            "GET",
            "api/payments/admin/dashboard",
            200
        )
        
        if success and data:
            analytics = data.get('analytics', {})
            payments = analytics.get('payments', {})
            subscriptions = analytics.get('subscriptions', {})
            
            print(f"   Total Transactions: {payments.get('total_transactions', 0)}")
            print(f"   Successful Payments: {payments.get('successful_payments', 0)}")
            print(f"   Success Rate: {payments.get('success_rate', 0):.1f}%")
            print(f"   Total Revenue: ${payments.get('total_revenue', 0)}")
            print(f"   Active Subscriptions: {subscriptions.get('active_subscriptions', 0)}")
            
            plan_breakdown = subscriptions.get('plan_breakdown', [])
            print(f"   Plan Breakdown: {len(plan_breakdown)} plan types")
            
            recent_transactions = analytics.get('recent_transactions', [])
            print(f"   Recent Transactions: {len(recent_transactions)} transactions")
            
            return True
        
        return False

    def test_invalid_plan_checkout(self):
        """Test checkout with invalid plan ID"""
        print("\n🚫 Testing Invalid Plan Checkout...")
        
        checkout_data = {
            "plan_id": "invalid_plan",
            "origin_url": "https://customermindiq.com",
            "metadata": {
                "user_email": self.demo_email,
                "source": "test_suite"
            }
        }
        
        success, data = self.run_test(
            "Invalid Plan Checkout",
            "POST",
            "api/payments/subscription/checkout",
            400,  # Expecting 400 Bad Request
            data=checkout_data
        )
        
        if success:
            print("   ✅ Properly rejects invalid plan with 400 error")
            return True
        
        return False

    def test_missing_parameters(self):
        """Test endpoints with missing required parameters"""
        print("\n⚠️  Testing Missing Parameters...")
        
        # Test current subscription without email or user_id
        success, data = self.run_test(
            "Current Subscription (no parameters)",
            "GET",
            "api/payments/subscription/current",
            400  # Expecting 400 Bad Request
        )
        
        if success:
            print("   ✅ Properly rejects missing parameters with 400 error")
            
            # Test subscription cancellation without parameters
            success2, data2 = self.run_test(
                "Cancel Subscription (no parameters)",
                "POST",
                "api/payments/subscription/cancel",
                400  # Expecting 400 Bad Request
            )
            
            return success2
        
        return False

    def run_all_tests(self):
        """Run all payment system tests"""
        print("🚀 Starting Payment System Integration Tests...")
        print(f"Backend URL: {self.base_url}")
        print(f"Demo Email: {self.demo_email}")
        print("=" * 80)
        
        # Core functionality tests
        test_results = []
        
        test_results.append(self.test_subscription_plans())
        test_results.append(self.test_free_subscription_checkout())
        test_results.append(self.test_paid_subscription_checkout())
        test_results.append(self.test_enterprise_subscription_checkout())
        test_results.append(self.test_payment_status_check())
        test_results.append(self.test_current_subscription_status())
        test_results.append(self.test_transaction_history())
        test_results.append(self.test_subscription_cancellation())
        test_results.append(self.test_admin_dashboard())
        
        # Error handling tests
        test_results.append(self.test_invalid_plan_checkout())
        test_results.append(self.test_missing_parameters())
        
        # Print summary
        print("\n" + "=" * 80)
        print("🎯 PAYMENT SYSTEM TESTING SUMMARY")
        print("=" * 80)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL PAYMENT SYSTEM TESTS PASSED!")
            print("✅ Stripe checkout integration working correctly")
            print("✅ Subscription management operational")
            print("✅ Payment processing functional")
            print("✅ Admin dashboard working")
            print("✅ Error handling proper")
            return True
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} TESTS FAILED")
            print("❌ Payment system has issues that need attention")
            return False

if __name__ == "__main__":
    tester = PaymentSystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Payment System is ready for production!")
    else:
        print("\n🔧 Payment System needs fixes before production")
    
    exit(0 if success else 1)