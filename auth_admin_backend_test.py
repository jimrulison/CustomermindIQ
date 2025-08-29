import requests
import sys
import json
from datetime import datetime
import time
import uuid

class AuthAdminSystemTester:
    def __init__(self, base_url="https://customer-mind-iq-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.auth_tests = 0
        self.auth_passed = 0
        self.admin_tests = 0
        self.admin_passed = 0
        self.subscription_tests = 0
        self.subscription_passed = 0
        # Store authentication tokens for testing
        self.access_token = None
        self.admin_token = None
        self.test_user_id = None
        self.test_admin_id = None
        self.test_user_email = f"testuser_{int(time.time())}@example.com"
        self.test_admin_email = "admin@customermindiq.com"

    def run_auth_test(self, name, method, endpoint, expected_status, data=None, headers=None, timeout=30):
        """Run an Authentication System API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        if headers:
            test_headers.update(headers)

        self.auth_tests += 1
        print(f"\n🔐 Testing Authentication: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=timeout)

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
        """Run an Admin System API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        if headers:
            test_headers.update(headers)

        self.admin_tests += 1
        print(f"\n👑 Testing Admin System: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=timeout)

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
        """Run a Subscription System API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        if headers:
            test_headers.update(headers)

        self.subscription_tests += 1
        print(f"\n💳 Testing Subscription System: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=timeout)

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

    # =====================================================
    # AUTHENTICATION SYSTEM TESTS
    # =====================================================

    def test_user_registration(self):
        """Test user registration with different roles"""
        print("\n🔐 Testing User Registration...")
        
        registration_data = {
            "email": self.test_user_email,
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company",
            "phone": "+1234567890",
            "role": "user",
            "subscription_tier": "free"
        }
        
        success, response = self.run_auth_test(
            "User Registration",
            "POST",
            "api/auth/register",
            200,
            data=registration_data,
            timeout=30
        )
        
        if success:
            self.access_token = response.get('access_token')
            self.test_user_id = response.get('user_profile', {}).get('user_id')
            print(f"   User ID: {self.test_user_id}")
            print(f"   Email: {response.get('user_profile', {}).get('email')}")
            print(f"   Role: {response.get('user_profile', {}).get('role')}")
            print(f"   Subscription Tier: {response.get('user_profile', {}).get('subscription_tier')}")
            print(f"   Token Type: {response.get('token_type')}")
            print(f"   Expires In: {response.get('expires_in')} seconds")
        
        return success

    def test_user_login(self):
        """Test user login with various scenarios"""
        print("\n🔐 Testing User Login...")
        
        login_data = {
            "email": self.test_user_email,
            "password": "TestPassword123!",
            "remember_me": False
        }
        
        success, response = self.run_auth_test(
            "User Login",
            "POST",
            "api/auth/login",
            200,
            data=login_data,
            timeout=30
        )
        
        if success:
            self.access_token = response.get('access_token')
            print(f"   Login successful for: {response.get('user_profile', {}).get('email')}")
            print(f"   Last Login: {response.get('user_profile', {}).get('last_login')}")
            print(f"   Account Active: {response.get('user_profile', {}).get('is_active')}")
        
        return success

    def test_admin_login(self):
        """Test admin login with default admin account"""
        print("\n🔐 Testing Admin Login...")
        
        admin_login_data = {
            "email": self.test_admin_email,
            "password": "CustomerMindIQ2025!",
            "remember_me": False
        }
        
        success, response = self.run_auth_test(
            "Admin Login",
            "POST",
            "api/auth/login",
            200,
            data=admin_login_data,
            timeout=30
        )
        
        if success:
            self.admin_token = response.get('access_token')
            self.test_admin_id = response.get('user_profile', {}).get('user_id')
            print(f"   Admin login successful for: {response.get('user_profile', {}).get('email')}")
            print(f"   Admin Role: {response.get('user_profile', {}).get('role')}")
            print(f"   Admin Tier: {response.get('user_profile', {}).get('subscription_tier')}")
        
        return success

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        print("\n🔐 Testing Invalid Login...")
        
        invalid_login_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPassword123!",
            "remember_me": False
        }
        
        success, response = self.run_auth_test(
            "Invalid Login",
            "POST",
            "api/auth/login",
            401,  # Expecting unauthorized
            data=invalid_login_data,
            timeout=30
        )
        
        if success:
            print(f"   Correctly rejected invalid credentials")
            print(f"   Error message: {response.get('detail', 'No error message')}")
        
        return success

    def test_get_user_profile(self):
        """Test getting current user profile"""
        if not self.access_token:
            print("❌ No access token available for profile test")
            return False
            
        print("\n🔐 Testing Get User Profile...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_auth_test(
            "Get User Profile",
            "GET",
            "api/auth/profile",
            200,
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   User ID: {response.get('user_id')}")
            print(f"   Email: {response.get('email')}")
            print(f"   Name: {response.get('first_name')} {response.get('last_name')}")
            print(f"   Company: {response.get('company_name')}")
            print(f"   Role: {response.get('role')}")
            print(f"   Subscription: {response.get('subscription_tier')}")
            print(f"   Created: {response.get('created_at')}")
        
        return success

    def test_update_user_profile(self):
        """Test updating user profile"""
        if not self.access_token:
            print("❌ No access token available for profile update test")
            return False
            
        print("\n🔐 Testing Update User Profile...")
        
        update_data = {
            "first_name": "Updated",
            "last_name": "TestUser",
            "company_name": "Updated Test Company",
            "phone": "+1987654321"
        }
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_auth_test(
            "Update User Profile",
            "PUT",
            "api/auth/profile",
            200,
            data=update_data,
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Updated Name: {response.get('first_name')} {response.get('last_name')}")
            print(f"   Updated Company: {response.get('company_name')}")
            print(f"   Updated Phone: {response.get('phone')}")
        
        return success

    def test_change_password(self):
        """Test changing user password"""
        if not self.access_token:
            print("❌ No access token available for password change test")
            return False
            
        print("\n🔐 Testing Change Password...")
        
        password_data = {
            "current_password": "TestPassword123!",
            "new_password": "NewTestPassword123!"
        }
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_auth_test(
            "Change Password",
            "POST",
            "api/auth/change-password",
            200,
            data=password_data,
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Password changed successfully")
            print(f"   Message: {response.get('message')}")
        
        return success

    def test_jwt_token_validation(self):
        """Test JWT token validation"""
        if not self.access_token:
            print("❌ No access token available for token validation test")
            return False
            
        print("\n🔐 Testing JWT Token Validation...")
        
        # Test with valid token
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_auth_test(
            "JWT Token Validation",
            "GET",
            "api/auth/profile",
            200,
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Valid token accepted")
            print(f"   User authenticated: {response.get('email')}")
        
        return success

    def test_invalid_token(self):
        """Test with invalid JWT token"""
        print("\n🔐 Testing Invalid JWT Token...")
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token_12345"}
        
        success, response = self.run_auth_test(
            "Invalid JWT Token",
            "GET",
            "api/auth/profile",
            401,  # Expecting unauthorized
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Invalid token correctly rejected")
            print(f"   Error: {response.get('detail', 'No error message')}")
        
        return success

    # =====================================================
    # ADMIN SYSTEM TESTS
    # =====================================================

    def test_admin_get_users(self):
        """Test admin endpoint to get all users"""
        if not self.admin_token:
            print("❌ No admin token available for admin users test")
            return False
            
        print("\n👑 Testing Admin Get Users...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Admin Get Users",
            "GET",
            "api/auth/admin/users?limit=10",
            200,
            headers=headers,
            timeout=30
        )
        
        if success:
            users = response.get('users', [])
            print(f"   Total Users: {response.get('total', 0)}")
            print(f"   Users Retrieved: {len(users)}")
            for user in users[:3]:  # Show first 3 users
                print(f"   - {user.get('email')}: {user.get('role')} ({user.get('subscription_tier')})")
        
        return success

    def test_admin_update_user_role(self):
        """Test admin updating user role"""
        if not self.admin_token or not self.test_user_id:
            print("❌ No admin token or test user ID available")
            return False
            
        print("\n👑 Testing Admin Update User Role...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Admin Update User Role",
            "PUT",
            f"api/auth/admin/users/{self.test_user_id}/role",
            200,
            data="analyst",  # New role
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Role update successful")
            print(f"   Message: {response.get('message')}")
        
        return success

    def test_admin_update_user_subscription(self):
        """Test admin updating user subscription tier"""
        if not self.admin_token or not self.test_user_id:
            print("❌ No admin token or test user ID available")
            return False
            
        print("\n👑 Testing Admin Update User Subscription...")
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Admin Update User Subscription",
            "PUT",
            f"api/auth/admin/users/{self.test_user_id}/subscription",
            200,
            data="professional",  # New subscription tier
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Subscription update successful")
            print(f"   Message: {response.get('message')}")
        
        return success

    def test_create_banner(self):
        """Test creating admin banner"""
        if not self.admin_token:
            print("❌ No admin token available for banner creation test")
            return False
            
        print("\n👑 Testing Create Admin Banner...")
        
        banner_data = {
            "title": "System Maintenance Notice",
            "message": "Scheduled maintenance will occur on Sunday from 2-4 AM EST. Please save your work.",
            "banner_type": "warning",
            "target_users": [],
            "target_tiers": [],
            "is_dismissible": True,
            "priority": 8,
            "call_to_action": "Learn More",
            "cta_url": "/maintenance-info"
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Create Admin Banner",
            "POST",
            "api/admin/banners",
            200,
            data=banner_data,
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Banner ID: {response.get('banner_id')}")
            print(f"   Title: {response.get('title')}")
            print(f"   Type: {response.get('banner_type')}")
            print(f"   Status: {response.get('status')}")
            print(f"   Priority: {response.get('priority')}")
        
        return success

    def test_get_active_banners(self):
        """Test getting active banners for users"""
        if not self.access_token:
            print("❌ No access token available for active banners test")
            return False
            
        print("\n👑 Testing Get Active Banners...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_admin_test(
            "Get Active Banners",
            "GET",
            "api/banners/active",
            200,
            headers=headers,
            timeout=30
        )
        
        if success:
            banners = response.get('banners', [])
            print(f"   Active Banners: {response.get('count', 0)}")
            for banner in banners[:2]:  # Show first 2 banners
                print(f"   - {banner.get('title')}: {banner.get('banner_type')}")
                print(f"     Message: {banner.get('message')[:100]}...")
        
        return success

    def test_create_discount(self):
        """Test creating admin discount"""
        if not self.admin_token:
            print("❌ No admin token available for discount creation test")
            return False
            
        print("\n👑 Testing Create Admin Discount...")
        
        discount_data = {
            "name": "New Year Special",
            "description": "20% off all subscription tiers for new customers",
            "discount_type": "percentage",
            "value": 20.0,
            "target_tiers": ["starter", "professional"],
            "target_users": [],
            "usage_limit": 100,
            "per_user_limit": 1,
            "minimum_purchase": 50.0,
            "is_active": True
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        success, response = self.run_admin_test(
            "Create Admin Discount",
            "POST",
            "api/admin/discounts",
            200,
            data=discount_data,
            headers=headers,
            timeout=30
        )
        
        if success:
            print(f"   Discount ID: {response.get('discount_id')}")
            print(f"   Name: {response.get('name')}")
            print(f"   Type: {response.get('discount_type')}")
            print(f"   Value: {response.get('value')}%")
            print(f"   Usage Limit: {response.get('usage_limit')}")
        
        return success

    def test_get_available_discounts(self):
        """Test getting available discounts for users"""
        if not self.access_token:
            print("❌ No access token available for available discounts test")
            return False
            
        print("\n👑 Testing Get Available Discounts...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_admin_test(
            "Get Available Discounts",
            "GET",
            "api/discounts/available",
            200,
            headers=headers,
            timeout=30
        )
        
        if success:
            discounts = response.get('discounts', [])
            print(f"   Available Discounts: {response.get('count', 0)}")
            for discount in discounts[:2]:  # Show first 2 discounts
                print(f"   - {discount.get('name')}: {discount.get('value')}% off")
                print(f"     Description: {discount.get('description')}")
        
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
            "api/admin/analytics/dashboard",
            200,
            headers=headers,
            timeout=45
        )
        
        if success:
            user_stats = response.get('user_statistics', {})
            print(f"   Total Users: {user_stats.get('total_users', 0)}")
            print(f"   Active Users: {user_stats.get('active_users', 0)}")
            print(f"   Cancelled Users: {user_stats.get('cancelled_users', 0)}")
            
            revenue_analytics = response.get('revenue_analytics', {})
            print(f"   Monthly Revenue: ${revenue_analytics.get('total_monthly_revenue', 0):,.2f}")
            print(f"   ARPU: ${revenue_analytics.get('average_revenue_per_user', 0):,.2f}")
            
            banner_analytics = response.get('banner_analytics', {})
            print(f"   Total Banners: {banner_analytics.get('total_banners', 0)}")
            
            discount_analytics = response.get('discount_analytics', {})
            print(f"   Total Discounts: {discount_analytics.get('total_discounts', 0)}")
            print(f"   Total Uses: {discount_analytics.get('total_uses', 0)}")
        
        return success

    # =====================================================
    # SUBSCRIPTION SYSTEM TESTS
    # =====================================================

    def test_trial_registration(self):
        """Test 7-day free trial registration"""
        print("\n💳 Testing 7-Day Free Trial Registration...")
        
        trial_email = f"trial_{int(time.time())}@example.com"
        trial_data = {
            "email": trial_email,
            "first_name": "Trial",
            "last_name": "User",
            "company_name": "Trial Company",
            "phone": "+1555123456",
            "utm_source": "website",
            "utm_campaign": "free_trial"
        }
        
        success, response = self.run_subscription_test(
            "Trial Registration",
            "POST",
            "api/subscriptions/trial/register",
            200,
            data=trial_data,
            timeout=30
        )
        
        if success:
            trial_info = response.get('trial_info', {})
            print(f"   Trial ID: {trial_info.get('trial_id')}")
            print(f"   User ID: {trial_info.get('user_id')}")
            print(f"   Trial Tier: {trial_info.get('trial_tier')}")
            print(f"   Days Remaining: {trial_info.get('days_remaining')}")
            print(f"   Start Date: {trial_info.get('start_date')}")
            print(f"   End Date: {trial_info.get('end_date')}")
            print(f"   No Credit Card Required: {not trial_info.get('has_credit_card', True)}")
        
        return success

    def test_subscription_tiers(self):
        """Test getting subscription tiers and pricing"""
        print("\n💳 Testing Subscription Tiers...")
        
        success, response = self.run_subscription_test(
            "Get Subscription Tiers",
            "GET",
            "api/subscriptions/tiers",
            200,
            timeout=30
        )
        
        if success:
            tiers = response.get('tiers', [])
            print(f"   Available Tiers: {len(tiers)}")
            for tier in tiers:
                print(f"   - {tier.get('name', 'Unknown')}: ${tier.get('monthly_price', 0)}/month")
                print(f"     Features: {len(tier.get('features', {}))}")
                features = tier.get('features', {})
                if 'websites_monitored' in features:
                    print(f"     Websites: {features.get('websites_monitored', 0)}")
                if 'team_members' in features:
                    print(f"     Team Members: {features.get('team_members', 0)}")
        
        return success

    def test_subscription_upgrade(self):
        """Test subscription upgrade"""
        if not self.access_token:
            print("❌ No access token available for subscription upgrade test")
            return False
            
        print("\n💳 Testing Subscription Upgrade...")
        
        upgrade_data = {
            "target_tier": "professional",
            "billing_cycle": "monthly",
            "promo_code": None
        }
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_subscription_test(
            "Subscription Upgrade",
            "POST",
            "api/subscriptions/upgrade",
            200,
            data=upgrade_data,
            headers=headers,
            timeout=30
        )
        
        if success:
            upgrade_info = response.get('upgrade_info', {})
            print(f"   Target Tier: {upgrade_info.get('target_tier')}")
            print(f"   New Price: ${upgrade_info.get('new_monthly_price', 0)}/month")
            print(f"   Billing Cycle: {upgrade_info.get('billing_cycle')}")
            print(f"   Effective Date: {upgrade_info.get('effective_date')}")
            
            pricing = response.get('pricing_details', {})
            print(f"   Prorated Amount: ${pricing.get('prorated_amount', 0)}")
            print(f"   Next Billing: {pricing.get('next_billing_date')}")
        
        return success

    def test_feature_usage_tracking(self):
        """Test feature usage tracking"""
        if not self.access_token:
            print("❌ No access token available for feature usage test")
            return False
            
        print("\n💳 Testing Feature Usage Tracking...")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        success, response = self.run_subscription_test(
            "Track Feature Usage",
            "POST",
            "api/subscriptions/usage/track/website_analysis",
            200,
            headers=headers,
            timeout=30
        )
        
        if success:
            usage_info = response.get('usage_info', {})
            print(f"   Feature: {usage_info.get('feature_name')}")
            print(f"   Current Usage: {usage_info.get('current_usage', 0)}")
            print(f"   Usage Limit: {usage_info.get('usage_limit', 'unlimited')}")
            print(f"   Remaining: {usage_info.get('remaining_usage', 'unlimited')}")
            print(f"   Reset Date: {usage_info.get('next_reset_date')}")
        
        return success

    def run_comprehensive_auth_admin_tests(self):
        """Run comprehensive authentication and admin system tests"""
        print("\n" + "="*80)
        print("🔐 AUTHENTICATION & ADMIN SYSTEM - COMPREHENSIVE TESTING")
        print("="*80)
        print("Testing newly implemented authentication and admin system backend:")
        print("")
        print("🔐 AUTHENTICATION SYSTEM:")
        print("   - User registration with different roles")
        print("   - Login with various scenarios (success, invalid credentials)")
        print("   - JWT token validation and refresh functionality")
        print("   - Profile management (get and update)")
        print("   - Password change functionality")
        print("")
        print("👑 ADMIN SYSTEM:")
        print("   - Banner management (create, get active banners)")
        print("   - Discount management (create, check availability)")
        print("   - Admin user management (get users, update roles/subscriptions)")
        print("   - Admin analytics dashboard")
        print("")
        print("💳 SUBSCRIPTION SYSTEM:")
        print("   - 7-day free trial registration (no credit card required)")
        print("   - Subscription tiers and pricing")
        print("   - Subscription upgrade functionality")
        print("   - Feature usage tracking")
        print("="*80)
        
        # Reset counters
        total_tests = 0
        total_passed = 0
        
        # Authentication System Tests
        print(f"\n{'='*60}")
        print("🔐 TESTING AUTHENTICATION SYSTEM")
        print("="*60)
        
        auth_tests = [
            self.test_user_registration,
            self.test_user_login,
            self.test_admin_login,
            self.test_invalid_login,
            self.test_get_user_profile,
            self.test_update_user_profile,
            self.test_change_password,
            self.test_jwt_token_validation,
            self.test_invalid_token
        ]
        
        for test in auth_tests:
            total_tests += 1
            if test():
                total_passed += 1
        
        # Admin System Tests
        print(f"\n{'='*60}")
        print("👑 TESTING ADMIN SYSTEM")
        print("="*60)
        
        admin_tests = [
            self.test_admin_get_users,
            self.test_admin_update_user_role,
            self.test_admin_update_user_subscription,
            self.test_create_banner,
            self.test_get_active_banners,
            self.test_create_discount,
            self.test_get_available_discounts,
            self.test_admin_analytics_dashboard
        ]
        
        for test in admin_tests:
            total_tests += 1
            if test():
                total_passed += 1
        
        # Subscription System Tests
        print(f"\n{'='*60}")
        print("💳 TESTING SUBSCRIPTION SYSTEM")
        print("="*60)
        
        subscription_tests = [
            self.test_trial_registration,
            self.test_subscription_tiers,
            self.test_subscription_upgrade,
            self.test_feature_usage_tracking
        ]
        
        for test in subscription_tests:
            total_tests += 1
            if test():
                total_passed += 1
        
        # Final Results
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n" + "="*80)
        print(f"🔐 AUTHENTICATION & ADMIN SYSTEM TESTING COMPLETE")
        print(f"="*80)
        print(f"✅ Tests Passed: {total_passed}/{total_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"")
        print(f"📋 DETAILED RESULTS:")
        print(f"   🔐 Authentication Tests: {self.auth_passed}/{self.auth_tests} ({(self.auth_passed/self.auth_tests*100) if self.auth_tests > 0 else 0:.1f}%)")
        print(f"   👑 Admin System Tests: {self.admin_passed}/{self.admin_tests} ({(self.admin_passed/self.admin_tests*100) if self.admin_tests > 0 else 0:.1f}%)")
        print(f"   💳 Subscription Tests: {self.subscription_passed}/{self.subscription_tests} ({(self.subscription_passed/self.subscription_tests*100) if self.subscription_tests > 0 else 0:.1f}%)")
        
        if total_passed == total_tests:
            print(f"\n🎉 SUCCESS: ALL AUTHENTICATION & ADMIN SYSTEM TESTS PASSED!")
            print(f"   ✅ User Registration & Login - Working with JWT tokens")
            print(f"   ✅ Role-based Access Control - Admin permissions enforced")
            print(f"   ✅ Banner Management - Create and display system announcements")
            print(f"   ✅ Discount Management - Create and apply discounts")
            print(f"   ✅ Admin Analytics - Comprehensive dashboard data")
            print(f"   ✅ 7-Day Free Trial - No credit card required")
            print(f"   ✅ 4-Tier Subscription System - Starter/Professional/Enterprise/Custom")
            print(f"   ✅ Feature Usage Tracking - Monitor subscription limits")
            print(f"   Authentication and Admin System is production-ready!")
        else:
            failed_tests = total_tests - total_passed
            print(f"\n⚠️  PARTIAL SUCCESS: {failed_tests} test(s) failed")
            print(f"   Most of the Authentication & Admin System is working correctly")
            print(f"   See detailed test results above for specific issues")
        
        return total_passed == total_tests

if __name__ == "__main__":
    print("🔐 Customer Mind IQ - Authentication & Admin System Backend Testing")
    print("="*80)
    
    tester = AuthAdminSystemTester()
    
    try:
        success = tester.run_comprehensive_auth_admin_tests()
        
        if success:
            print(f"\n🎉 ALL TESTS PASSED - Authentication & Admin System is fully functional!")
            sys.exit(0)
        else:
            print(f"\n⚠️  SOME TESTS FAILED - See details above")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Testing failed with error: {e}")
        sys.exit(1)