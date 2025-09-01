import requests
import sys
import json
from datetime import datetime
import time

class AuthAdminSubscriptionTester:
    def __init__(self, base_url="https://mind-iq-dashboard.preview.emergentagent.com"):
        self.base_url = base_url
        self.auth_tests = 0
        self.auth_passed = 0
        self.admin_tests = 0
        self.admin_passed = 0
        self.subscription_tests = 0
        self.subscription_passed = 0
        self.core_platform_tests = 0
        self.core_platform_passed = 0
        
        # Store authentication tokens
        self.access_token = None
        self.admin_token = None
        self.test_user_id = None
        self.test_admin_id = None

    def run_auth_test(self, name, method, endpoint, expected_status, data=None, headers=None, timeout=30):
        """Run an authentication API test"""
        url = f"{self.base_url}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)

        self.auth_tests += 1
        print(f"\n🔐 Testing Authentication: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.auth_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def run_admin_test(self, name, method, endpoint, expected_status, data=None, headers=None, timeout=30):
        """Run an admin system API test"""
        url = f"{self.base_url}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)

        self.admin_tests += 1
        print(f"\n👑 Testing Admin System: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.admin_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def run_subscription_test(self, name, method, endpoint, expected_status, data=None, headers=None, timeout=30):
        """Run a subscription system API test"""
        url = f"{self.base_url}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)

        self.subscription_tests += 1
        print(f"\n💳 Testing Subscription System: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.subscription_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def run_core_test(self, name, method, endpoint, expected_status, data=None, headers=None, timeout=30):
        """Run a core platform API test"""
        url = f"{self.base_url}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)

        self.core_platform_tests += 1
        print(f"\n🚀 Testing Core Platform: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.core_platform_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    # =====================================================
    # AUTHENTICATION ENDPOINTS TESTS (/api/auth/*)
    # =====================================================

    def test_auth_register(self):
        """Test user registration endpoint"""
        print("\n🔐 Testing User Registration...")
        
        register_data = {
            "email": f"testuser_{int(time.time())}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User",
            "role": "user"
        }
        
        success, response = self.run_auth_test(
            "User Registration",
            "POST",
            "api/auth/register",
            201,
            data=register_data
        )
        
        if success and response:
            self.test_user_id = response.get('user_id')
            print(f"   Registered user ID: {self.test_user_id}")
            print(f"   User role: {response.get('role', 'unknown')}")
        
        return success

    def test_auth_login_admin(self):
        """Test admin login with default credentials"""
        print("\n🔐 Testing Admin Login with Default Credentials...")
        
        login_data = {
            "email": "admin@customermindiq.com",
            "password": "CustomerMindIQ2025!"
        }
        
        success, response = self.run_auth_test(
            "Admin Login",
            "POST",
            "api/auth/login",
            200,
            data=login_data
        )
        
        if success and response:
            self.admin_token = response.get('access_token')
            self.test_admin_id = response.get('user_id')
            print(f"   Admin token obtained: {self.admin_token[:20]}..." if self.admin_token else "   No token received")
            print(f"   Admin user ID: {self.test_admin_id}")
            print(f"   Token type: {response.get('token_type', 'unknown')}")
            print(f"   User role: {response.get('role', 'unknown')}")
        
        return success

    def test_auth_login_invalid(self):
        """Test login with invalid credentials"""
        print("\n🔐 Testing Login with Invalid Credentials...")
        
        login_data = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        
        success, response = self.run_auth_test(
            "Invalid Login",
            "POST",
            "api/auth/login",
            401,
            data=login_data
        )
        
        return success

    def test_auth_profile_get(self):
        """Test getting user profile with authentication"""
        if not self.admin_token:
            print("❌ No admin token available for profile test")
            return False
            
        print("\n🔐 Testing Get User Profile...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_auth_test(
            "Get User Profile",
            "GET",
            "api/auth/profile",
            200,
            headers=headers
        )
        
        if success and response:
            print(f"   Profile email: {response.get('email', 'unknown')}")
            print(f"   Profile name: {response.get('full_name', 'unknown')}")
            print(f"   Profile role: {response.get('role', 'unknown')}")
        
        return success

    def test_auth_profile_update(self):
        """Test updating user profile"""
        if not self.admin_token:
            print("❌ No admin token available for profile update test")
            return False
            
        print("\n🔐 Testing Update User Profile...")
        
        update_data = {
            "full_name": "Updated Admin Name",
            "phone": "+1234567890"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_auth_test(
            "Update User Profile",
            "PUT",
            "api/auth/profile",
            200,
            data=update_data,
            headers=headers
        )
        
        return success

    def test_auth_change_password(self):
        """Test password change functionality"""
        if not self.admin_token:
            print("❌ No admin token available for password change test")
            return False
            
        print("\n🔐 Testing Password Change...")
        
        password_data = {
            "current_password": "CustomerMindIQ2025!",
            "new_password": "NewPassword123!",
            "confirm_password": "NewPassword123!"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_auth_test(
            "Change Password",
            "POST",
            "api/auth/change-password",
            200,
            data=password_data,
            headers=headers
        )
        
        return success

    def test_auth_token_validation(self):
        """Test JWT token validation"""
        if not self.admin_token:
            print("❌ No admin token available for token validation test")
            return False
            
        print("\n🔐 Testing JWT Token Validation...")
        
        # Test with invalid token
        invalid_headers = {"Authorization": "Bearer invalid_token_123"}
        
        success, response = self.run_auth_test(
            "Invalid Token Validation",
            "GET",
            "api/auth/profile",
            401,  # Should return 401 for invalid token
            headers=invalid_headers
        )
        
        return success

    # =====================================================
    # ADMIN SYSTEM ENDPOINTS TESTS (/api/admin/*, /api/support/admin/*)
    # =====================================================

    def test_admin_banner_create(self):
        """Test admin banner creation"""
        if not self.admin_token:
            print("❌ No admin token available for banner creation test")
            return False
            
        print("\n👑 Testing Admin Banner Creation...")
        
        banner_data = {
            "title": "System Maintenance Notice",
            "message": "Scheduled maintenance on Sunday 2AM-4AM EST",
            "banner_type": "info",
            "priority": 1,
            "target_users": "all",
            "target_tiers": ["starter", "professional"],
            "is_dismissible": True,
            "start_date": "2025-01-20T00:00:00Z",
            "end_date": "2025-01-21T00:00:00Z"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Create Admin Banner",
            "POST",
            "api/support/admin/banners",
            201,
            data=banner_data,
            headers=headers
        )
        
        if success and response:
            print(f"   Banner ID: {response.get('banner_id', 'unknown')}")
            print(f"   Banner title: {response.get('title', 'unknown')}")
            print(f"   Target users: {response.get('target_users', 'unknown')}")
        
        return success

    def test_admin_banners_list(self):
        """Test getting admin banners list"""
        if not self.admin_token:
            print("❌ No admin token available for banners list test")
            return False
            
        print("\n👑 Testing Admin Banners List...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Get Admin Banners",
            "GET",
            "api/support/admin/banners",
            200,
            headers=headers
        )
        
        if success and response:
            banners = response.get('banners', [])
            print(f"   Total banners: {len(banners)}")
            for banner in banners[:3]:  # Show first 3 banners
                print(f"   - {banner.get('title', 'Unknown')}: {banner.get('banner_type', 'unknown')} priority {banner.get('priority', 0)}")
        
        return success

    def test_admin_discount_create(self):
        """Test admin discount creation"""
        if not self.admin_token:
            print("❌ No admin token available for discount creation test")
            return False
            
        print("\n👑 Testing Admin Discount Creation...")
        
        discount_data = {
            "code": f"TEST{int(time.time())}",
            "discount_type": "percentage",
            "value": 20.0,
            "description": "Test discount for new users",
            "target_users": "new_users",
            "target_tiers": ["starter"],
            "usage_limit": 100,
            "start_date": "2025-01-15T00:00:00Z",
            "end_date": "2025-02-15T00:00:00Z"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Create Admin Discount",
            "POST",
            "api/support/admin/discounts",
            201,
            data=discount_data,
            headers=headers
        )
        
        if success and response:
            print(f"   Discount ID: {response.get('discount_id', 'unknown')}")
            print(f"   Discount code: {response.get('code', 'unknown')}")
            print(f"   Discount value: {response.get('value', 0)}%")
        
        return success

    def test_admin_discounts_list(self):
        """Test getting admin discounts list"""
        if not self.admin_token:
            print("❌ No admin token available for discounts list test")
            return False
            
        print("\n👑 Testing Admin Discounts List...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Get Admin Discounts",
            "GET",
            "api/support/admin/discounts",
            200,
            headers=headers
        )
        
        if success and response:
            discounts = response.get('discounts', [])
            print(f"   Total discounts: {len(discounts)}")
            for discount in discounts[:3]:  # Show first 3 discounts
                print(f"   - {discount.get('code', 'Unknown')}: {discount.get('value', 0)}% off for {discount.get('target_users', 'unknown')}")
        
        return success

    def test_admin_analytics_dashboard(self):
        """Test admin analytics dashboard"""
        if not self.admin_token:
            print("❌ No admin token available for analytics dashboard test")
            return False
            
        print("\n👑 Testing Admin Analytics Dashboard...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Admin Analytics Dashboard",
            "GET",
            "api/support/admin/analytics",
            200,
            headers=headers
        )
        
        if success and response:
            analytics = response.get('analytics', {})
            user_stats = analytics.get('user_statistics', {})
            revenue_stats = analytics.get('revenue_analytics', {})
            
            print(f"   Total users: {user_stats.get('total_users', 0)}")
            print(f"   Active users: {user_stats.get('active_users', 0)}")
            print(f"   Monthly revenue: ${revenue_stats.get('monthly_revenue', 0):,.2f}")
            print(f"   ARPU: ${revenue_stats.get('arpu', 0):,.2f}")
        
        return success

    def test_admin_user_management(self):
        """Test admin user management endpoints"""
        if not self.admin_token:
            print("❌ No admin token available for user management test")
            return False
            
        print("\n👑 Testing Admin User Management...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test getting users list
        success, response = self.run_admin_test(
            "Get Users List",
            "GET",
            "api/support/admin/users",
            200,
            headers=headers
        )
        
        if success and response:
            users = response.get('users', [])
            print(f"   Total users: {len(users)}")
            for user in users[:3]:  # Show first 3 users
                print(f"   - {user.get('email', 'Unknown')}: {user.get('role', 'unknown')} ({user.get('subscription_tier', 'no tier')})")
        
        return success

    # =====================================================
    # SUBSCRIPTION SYSTEM ENDPOINTS TESTS (/api/subscriptions/*)
    # =====================================================

    def test_subscription_tiers(self):
        """Test getting subscription tiers"""
        print("\n💳 Testing Subscription Tiers...")
        
        success, response = self.run_subscription_test(
            "Get Subscription Tiers",
            "GET",
            "api/subscriptions/tiers",
            200
        )
        
        if success and response:
            tiers = response.get('tiers', [])
            print(f"   Available tiers: {len(tiers)}")
            for tier in tiers:
                print(f"   - {tier.get('name', 'Unknown')}: ${tier.get('price', 0)}/month")
                features = tier.get('features', [])
                print(f"     Features: {len(features)} included")
        
        return success

    def test_subscription_trial_register(self):
        """Test 7-day free trial registration"""
        print("\n💳 Testing 7-Day Free Trial Registration...")
        
        trial_data = {
            "email": f"trial_{int(time.time())}@example.com",
            "full_name": "Trial User",
            "company_name": "Test Company"
        }
        
        success, response = self.run_subscription_test(
            "7-Day Free Trial Registration",
            "POST",
            "api/subscriptions/trial/register",
            201,
            data=trial_data
        )
        
        if success and response:
            print(f"   Trial user ID: {response.get('user_id', 'unknown')}")
            print(f"   Trial tier: {response.get('trial_tier', 'unknown')}")
            print(f"   Trial end date: {response.get('trial_end_date', 'unknown')}")
            print(f"   Days remaining: {response.get('days_remaining', 0)}")
        
        return success

    def test_subscription_user_subscription(self):
        """Test getting user subscription details"""
        if not self.admin_token:
            print("❌ No admin token available for subscription details test")
            return False
            
        print("\n💳 Testing User Subscription Details...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_subscription_test(
            "Get User Subscription",
            "GET",
            "api/subscriptions/user/subscription",
            200,
            headers=headers
        )
        
        if success and response:
            subscription = response.get('subscription', {})
            print(f"   Current tier: {subscription.get('tier', 'unknown')}")
            print(f"   Status: {subscription.get('status', 'unknown')}")
            print(f"   Next billing: {subscription.get('next_billing_date', 'unknown')}")
        
        return success

    def test_subscription_feature_usage(self):
        """Test feature usage tracking"""
        if not self.admin_token:
            print("❌ No admin token available for feature usage test")
            return False
            
        print("\n💳 Testing Feature Usage Tracking...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_subscription_test(
            "Get Feature Usage",
            "GET",
            "api/subscriptions/user/usage",
            200,
            headers=headers
        )
        
        if success and response:
            usage = response.get('usage', {})
            limits = response.get('limits', {})
            print(f"   API calls used: {usage.get('api_calls', 0)}/{limits.get('api_calls', 'unlimited')}")
            print(f"   Storage used: {usage.get('storage_gb', 0)}/{limits.get('storage_gb', 'unlimited')} GB")
            print(f"   Users: {usage.get('users', 0)}/{limits.get('users', 'unlimited')}")
        
        return success

    # =====================================================
    # CORE PLATFORM ENDPOINTS AND INTELLIGENCE MODULES
    # =====================================================

    def test_core_health_check(self):
        """Test API health check"""
        print("\n🚀 Testing Core Platform Health Check...")
        
        success, response = self.run_core_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )
        
        if success and response:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Version: {response.get('version', 'unknown')}")
        
        return success

    def test_core_customers(self):
        """Test core customers endpoint"""
        print("\n🚀 Testing Core Customers Endpoint...")
        
        success, response = self.run_core_test(
            "Get Customers",
            "GET",
            "api/customers",
            200,
            timeout=60  # May take time for ODOO integration
        )
        
        if success and response:
            customers = response if isinstance(response, list) else []
            print(f"   Total customers: {len(customers)}")
            for customer in customers[:3]:  # Show first 3 customers
                print(f"   - {customer.get('name', 'Unknown')}: ${customer.get('total_spent', 0):,.2f} spent")
        
        return success

    def test_core_analytics(self):
        """Test core analytics endpoint"""
        print("\n🚀 Testing Core Analytics Endpoint...")
        
        success, response = self.run_core_test(
            "Get Analytics",
            "GET",
            "api/analytics",
            200
        )
        
        if success and response:
            print(f"   Total customers: {response.get('total_customers', 0)}")
            print(f"   Total revenue: ${response.get('total_revenue', 0):,.2f}")
            
            top_products = response.get('top_products', [])
            print(f"   Top products: {len(top_products)}")
            
            conversion_metrics = response.get('conversion_metrics', {})
            print(f"   Email open rate: {conversion_metrics.get('email_open_rate', 0):.1%}")
            print(f"   Conversion rate: {conversion_metrics.get('conversion_rate', 0):.1%}")
        
        return success

    def test_intelligence_dashboard(self):
        """Test intelligence dashboard endpoint"""
        print("\n🚀 Testing Intelligence Dashboard...")
        
        success, response = self.run_core_test(
            "Intelligence Dashboard",
            "GET",
            "api/intelligence/dashboard",
            200,
            timeout=90  # AI processing takes time
        )
        
        if success and response:
            modules = response.get('modules', {})
            print(f"   AI modules: {len(modules)}")
            
            for module_name, module_data in modules.items():
                if isinstance(module_data, dict) and 'error' not in module_data:
                    print(f"   ✅ {module_name.replace('_', ' ').title()}: Working")
                else:
                    print(f"   ❌ {module_name.replace('_', ' ').title()}: Error")
        
        return success

    def run_comprehensive_test(self):
        """Run comprehensive test suite for authentication, admin, subscription, and core platform"""
        print("=" * 80)
        print("🔍 CUSTOMERMIND IQ BACKEND COMPREHENSIVE TEST SUITE")
        print("   Testing Authentication, Admin, Subscription & Core Platform APIs")
        print("   Backend URL:", self.base_url)
        print("=" * 80)

        # Test Authentication Endpoints
        print("\n" + "=" * 50)
        print("🔐 AUTHENTICATION ENDPOINTS TESTING")
        print("=" * 50)
        
        self.test_auth_register()
        self.test_auth_login_admin()
        self.test_auth_login_invalid()
        self.test_auth_profile_get()
        self.test_auth_profile_update()
        self.test_auth_change_password()
        self.test_auth_token_validation()

        # Test Admin System Endpoints
        print("\n" + "=" * 50)
        print("👑 ADMIN SYSTEM ENDPOINTS TESTING")
        print("=" * 50)
        
        self.test_admin_banner_create()
        self.test_admin_banners_list()
        self.test_admin_discount_create()
        self.test_admin_discounts_list()
        self.test_admin_analytics_dashboard()
        self.test_admin_user_management()

        # Test Subscription System Endpoints
        print("\n" + "=" * 50)
        print("💳 SUBSCRIPTION SYSTEM ENDPOINTS TESTING")
        print("=" * 50)
        
        self.test_subscription_tiers()
        self.test_subscription_trial_register()
        self.test_subscription_user_subscription()
        self.test_subscription_feature_usage()

        # Test Core Platform Endpoints
        print("\n" + "=" * 50)
        print("🚀 CORE PLATFORM ENDPOINTS TESTING")
        print("=" * 50)
        
        self.test_core_health_check()
        self.test_core_customers()
        self.test_core_analytics()
        self.test_intelligence_dashboard()

        # Print comprehensive results
        self.print_comprehensive_results()

    def print_comprehensive_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)

        total_tests = self.auth_tests + self.admin_tests + self.subscription_tests + self.core_platform_tests
        total_passed = self.auth_passed + self.admin_passed + self.subscription_passed + self.core_platform_passed
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        print(f"\n🔐 AUTHENTICATION ENDPOINTS:")
        print(f"   Tests Run: {self.auth_tests}")
        print(f"   Tests Passed: {self.auth_passed}")
        print(f"   Success Rate: {(self.auth_passed/self.auth_tests*100):.1f}%" if self.auth_tests > 0 else "   Success Rate: N/A")

        print(f"\n👑 ADMIN SYSTEM ENDPOINTS:")
        print(f"   Tests Run: {self.admin_tests}")
        print(f"   Tests Passed: {self.admin_passed}")
        print(f"   Success Rate: {(self.admin_passed/self.admin_tests*100):.1f}%" if self.admin_tests > 0 else "   Success Rate: N/A")

        print(f"\n💳 SUBSCRIPTION SYSTEM ENDPOINTS:")
        print(f"   Tests Run: {self.subscription_tests}")
        print(f"   Tests Passed: {self.subscription_passed}")
        print(f"   Success Rate: {(self.subscription_passed/self.subscription_tests*100):.1f}%" if self.subscription_tests > 0 else "   Success Rate: N/A")

        print(f"\n🚀 CORE PLATFORM ENDPOINTS:")
        print(f"   Tests Run: {self.core_platform_tests}")
        print(f"   Tests Passed: {self.core_platform_passed}")
        print(f"   Success Rate: {(self.core_platform_passed/self.core_platform_tests*100):.1f}%" if self.core_platform_tests > 0 else "   Success Rate: N/A")

        print(f"\n🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Total Passed: {total_passed}")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")

        if overall_success_rate >= 80:
            print(f"\n✅ EXCELLENT: Backend APIs are working well!")
        elif overall_success_rate >= 60:
            print(f"\n⚠️  GOOD: Most backend APIs are working, some issues found")
        else:
            print(f"\n❌ NEEDS ATTENTION: Multiple backend API issues detected")

        print("\n" + "=" * 80)

if __name__ == "__main__":
    tester = AuthAdminSubscriptionTester()
    tester.run_comprehensive_test()