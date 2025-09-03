#!/usr/bin/env python3
"""
Authentication Backend Testing for Customer Mind IQ
Focus: Admin login, JWT tokens, and basic API endpoints
"""

import requests
import json
import sys
from datetime import datetime

class AuthenticationTester:
    def __init__(self, base_url="https://customer-mind-iq-4.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.jwt_token = None
        self.admin_credentials = {
            "email": "admin@customermindiq.com",
            "password": "CustomerMindIQ2025!"
        }
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}: PASSED {details}")
        else:
            print(f"❌ {test_name}: FAILED {details}")
        
    def test_health_check(self):
        """Test basic health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            success = response.status_code == 200
            details = f"(Status: {response.status_code})"
            if success:
                data = response.json()
                details += f" Service: {data.get('service', 'Unknown')}"
            self.log_test("Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login(self):
        """Test admin login with correct credentials"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=self.admin_credentials,
                timeout=10
            )
            
            success = response.status_code == 200
            details = f"(Status: {response.status_code})"
            
            if success:
                data = response.json()
                if "access_token" in data:
                    self.jwt_token = data["access_token"]
                    details += f" Token received, User: {data.get('user', {}).get('email', 'Unknown')}"
                else:
                    success = False
                    details += " No access token in response"
            else:
                try:
                    error_data = response.json()
                    details += f" Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" Response: {response.text[:100]}"
                    
            self.log_test("Admin Login", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception: {str(e)}")
            return False
    
    def test_jwt_token_validation(self):
        """Test JWT token validation"""
        if not self.jwt_token:
            self.log_test("JWT Token Validation", False, "No token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.jwt_token}"}
            response = requests.get(
                f"{self.base_url}/api/auth/profile",
                headers=headers,
                timeout=10
            )
            
            success = response.status_code == 200
            details = f"(Status: {response.status_code})"
            
            if success:
                data = response.json()
                details += f" Profile: {data.get('email', 'Unknown')}, Role: {data.get('role', 'Unknown')}"
            else:
                try:
                    error_data = response.json()
                    details += f" Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" Response: {response.text[:100]}"
                    
            self.log_test("JWT Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("JWT Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_customers_endpoint(self):
        """Test /api/customers endpoint"""
        try:
            headers = {}
            if self.jwt_token:
                headers["Authorization"] = f"Bearer {self.jwt_token}"
                
            response = requests.get(
                f"{self.base_url}/api/customers",
                headers=headers,
                timeout=15
            )
            
            success = response.status_code == 200
            details = f"(Status: {response.status_code})"
            
            if success:
                data = response.json()
                if isinstance(data, list):
                    details += f" {len(data)} customers loaded"
                    if data:
                        sample_customer = data[0]
                        details += f", Sample: {sample_customer.get('name', 'Unknown')}"
                else:
                    details += " Invalid response format"
            else:
                try:
                    error_data = response.json()
                    details += f" Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" Response: {response.text[:100]}"
                    
            self.log_test("Customers Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Customers Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_campaigns_endpoint(self):
        """Test /api/campaigns endpoint"""
        try:
            headers = {}
            if self.jwt_token:
                headers["Authorization"] = f"Bearer {self.jwt_token}"
                
            response = requests.get(
                f"{self.base_url}/api/campaigns",
                headers=headers,
                timeout=10
            )
            
            success = response.status_code == 200
            details = f"(Status: {response.status_code})"
            
            if success:
                data = response.json()
                if isinstance(data, list):
                    details += f" {len(data)} campaigns found"
                else:
                    details += " Invalid response format"
            else:
                try:
                    error_data = response.json()
                    details += f" Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" Response: {response.text[:100]}"
                    
            self.log_test("Campaigns Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Campaigns Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_analytics_endpoint(self):
        """Test /api/analytics endpoint"""
        try:
            headers = {}
            if self.jwt_token:
                headers["Authorization"] = f"Bearer {self.jwt_token}"
                
            response = requests.get(
                f"{self.base_url}/api/analytics",
                headers=headers,
                timeout=15
            )
            
            success = response.status_code == 200
            details = f"(Status: {response.status_code})"
            
            if success:
                data = response.json()
                details += f" Customers: {data.get('total_customers', 0)}, Revenue: ${data.get('total_revenue', 0):,.2f}"
            else:
                try:
                    error_data = response.json()
                    details += f" Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" Response: {response.text[:100]}"
                    
            self.log_test("Analytics Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Analytics Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_endpoints_routing(self):
        """Test admin endpoints routing (previously reported as 404)"""
        if not self.jwt_token:
            self.log_test("Admin Endpoints Routing", False, "No admin token available")
            return False
            
        admin_endpoints = [
            "/api/admin/banners",
            "/api/admin/discounts", 
            "/api/admin/analytics/dashboard"
        ]
        
        headers = {"Authorization": f"Bearer {self.jwt_token}"}
        working_endpoints = 0
        
        for endpoint in admin_endpoints:
            try:
                response = requests.get(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code in [200, 401, 403]:  # Not 404
                    working_endpoints += 1
                    print(f"  ✓ {endpoint}: Status {response.status_code}")
                else:
                    print(f"  ✗ {endpoint}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"  ✗ {endpoint}: Exception {str(e)}")
        
        success = working_endpoints > 0
        details = f"({working_endpoints}/{len(admin_endpoints)} endpoints accessible)"
        self.log_test("Admin Endpoints Routing", success, details)
        return success
    
    def test_subscription_endpoints(self):
        """Test subscription system endpoints"""
        try:
            # Test subscription tiers endpoint
            response = requests.get(f"{self.base_url}/api/subscriptions/subscriptions/tiers", timeout=10)
            
            success = response.status_code == 200
            details = f"(Status: {response.status_code})"
            
            if success:
                data = response.json()
                if "tiers" in data:
                    tiers = data["tiers"]
                    details += f" {len(tiers)} tiers available"
                    tier_names = list(tiers.keys())
                    details += f" ({', '.join(tier_names)})"
                else:
                    details += " Invalid response format"
            else:
                try:
                    error_data = response.json()
                    details += f" Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" Response: {response.text[:100]}"
                    
            self.log_test("Subscription Tiers", success, details)
            return success
        except Exception as e:
            self.log_test("Subscription Tiers", False, f"Exception: {str(e)}")
            return False
    
    def run_authentication_tests(self):
        """Run comprehensive authentication testing"""
        print("🔐 AUTHENTICATION BACKEND TESTING")
        print("=" * 50)
        print(f"Testing backend: {self.base_url}")
        print(f"Admin credentials: {self.admin_credentials['email']}")
        print()
        
        # Core authentication flow
        print("📋 CORE AUTHENTICATION TESTS:")
        self.test_health_check()
        self.test_admin_login()
        self.test_jwt_token_validation()
        
        print("\n📋 BASIC API ENDPOINTS:")
        self.test_customers_endpoint()
        self.test_campaigns_endpoint() 
        self.test_analytics_endpoint()
        
        print("\n📋 ADMIN SYSTEM TESTS:")
        self.test_admin_endpoints_routing()
        
        print("\n📋 SUBSCRIPTION SYSTEM:")
        self.test_subscription_endpoints()
        
        # Summary
        print("\n" + "=" * 50)
        print("🎯 AUTHENTICATION TEST SUMMARY")
        print("=" * 50)
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("✅ AUTHENTICATION SYSTEM: WORKING")
        elif success_rate >= 60:
            print("⚠️  AUTHENTICATION SYSTEM: PARTIALLY WORKING")
        else:
            print("❌ AUTHENTICATION SYSTEM: CRITICAL ISSUES")
        
        return success_rate >= 60

if __name__ == "__main__":
    tester = AuthenticationTester()
    success = tester.run_authentication_tests()
    sys.exit(0 if success else 1)