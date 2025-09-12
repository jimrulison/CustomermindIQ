#!/usr/bin/env python3
"""
Focused Enhanced Affiliate System Holdback Testing
Testing the specific holdback functionality and admin monitoring endpoints
"""

import requests
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-iq-touch.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class HoldbackSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        
    def log_result(self, test_name, success, details="", error=""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")
        print()

    def admin_login(self):
        """Login as admin"""
        try:
            response = self.session.post(f"{API_BASE}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
                self.log_result("Admin Authentication", True, f"Successfully logged in as {ADMIN_EMAIL}")
                return True
            else:
                self.log_result("Admin Authentication", False, error=f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, error=str(e))
            return False

    def test_affiliate_registration_with_terms(self):
        """Test affiliate registration with terms_accepted requirement"""
        try:
            # Create unique email for this test
            unique_email = f"holdback.test.{int(time.time())}@example.com"
            
            registration_data = {
                "first_name": "Holdback",
                "last_name": "Tester",
                "email": unique_email,
                "phone": "+1234567890",
                "website": "https://holdbacktest.com",
                "promotion_method": "social",
                "password": "SecurePass123!",
                "address": {
                    "street": "123 Holdback St",
                    "city": "Test City",
                    "state": "TS",
                    "zip_code": "12345",
                    "country": "US"
                },
                "payment_method": "paypal",
                "payment_details": {
                    "paypal_email": "holdback@paypal.com"
                },
                "terms_accepted": True  # Required for enhanced system
            }
            
            response = self.session.post(f"{API_BASE}/affiliate/auth/register", json=registration_data)
            
            if response.status_code == 200:
                data = response.json()
                affiliate_id = data.get("affiliate_id")
                self.log_result("Enhanced Affiliate Registration with Terms", True, 
                               f"Successfully registered affiliate: {affiliate_id}")
                return affiliate_id
            else:
                self.log_result("Enhanced Affiliate Registration with Terms", False, 
                               error=f"Status: {response.status_code}, Response: {response.text}")
                return None
                
        except Exception as e:
            self.log_result("Enhanced Affiliate Registration with Terms", False, error=str(e))
            return None

    def test_high_refund_monitoring_endpoint(self):
        """Test GET /api/affiliate/admin/monitoring/high-refund"""
        try:
            if not self.admin_token:
                self.log_result("High Refund Monitoring Endpoint", False, error="No admin token")
                return False
            
            response = self.session.get(f"{API_BASE}/affiliate/admin/monitoring/high-refund")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                total_flagged = data.get("total_flagged", 0)
                high_refund_affiliates = data.get("high_refund_affiliates", [])
                
                self.log_result("High Refund Monitoring Endpoint", True, 
                               f"Successfully retrieved monitoring data - {total_flagged} affiliates flagged for high refund rates")
                
                # Check structure of returned data
                if high_refund_affiliates:
                    first_affiliate = high_refund_affiliates[0]
                    required_fields = ["affiliate_id", "name", "email", "refund_rate_90d", "total_revenue_90d", "account_paused"]
                    missing_fields = [field for field in required_fields if field not in first_affiliate]
                    
                    if not missing_fields:
                        self.log_result("High Refund Data Structure", True, 
                                       "All required fields present in monitoring data")
                    else:
                        self.log_result("High Refund Data Structure", False, 
                                       error=f"Missing fields: {missing_fields}")
                
                return True
            else:
                self.log_result("High Refund Monitoring Endpoint", False, 
                               error=f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("High Refund Monitoring Endpoint", False, error=str(e))
            return False

    def test_affiliate_pause_resume_endpoints(self):
        """Test affiliate pause and resume functionality"""
        try:
            if not self.admin_token:
                self.log_result("Affiliate Pause/Resume Endpoints", False, error="No admin token")
                return False
            
            # First, register a test affiliate for pause/resume testing
            test_affiliate_id = self.test_affiliate_registration_with_terms()
            
            if not test_affiliate_id:
                self.log_result("Affiliate Pause/Resume Endpoints", False, error="Could not create test affiliate")
                return False
            
            # Test pause endpoint
            pause_data = {
                "reason": "Testing holdback system pause functionality"
            }
            
            pause_response = self.session.post(
                f"{API_BASE}/affiliate/admin/affiliates/{test_affiliate_id}/pause",
                json=pause_data
            )
            
            if pause_response.status_code == 200:
                pause_result = pause_response.json()
                self.log_result("Affiliate Pause Endpoint", True, 
                               f"Successfully paused affiliate: {pause_result.get('message', '')}")
                
                # Test resume endpoint
                resume_response = self.session.post(
                    f"{API_BASE}/affiliate/admin/affiliates/{test_affiliate_id}/resume"
                )
                
                if resume_response.status_code == 200:
                    resume_result = resume_response.json()
                    self.log_result("Affiliate Resume Endpoint", True, 
                                   f"Successfully resumed affiliate: {resume_result.get('message', '')}")
                    return True
                else:
                    self.log_result("Affiliate Resume Endpoint", False, 
                                   error=f"Status: {resume_response.status_code}, Response: {resume_response.text}")
                    return False
            else:
                self.log_result("Affiliate Pause Endpoint", False, 
                               error=f"Status: {pause_response.status_code}, Response: {pause_response.text}")
                return False
                
        except Exception as e:
            self.log_result("Affiliate Pause/Resume Endpoints", False, error=str(e))
            return False

    def test_holdback_settings_endpoint(self):
        """Test custom holdback settings endpoint"""
        try:
            if not self.admin_token:
                self.log_result("Holdback Settings Endpoint", False, error="No admin token")
                return False
            
            # Register a test affiliate for holdback settings testing
            test_affiliate_id = self.test_affiliate_registration_with_terms()
            
            if not test_affiliate_id:
                self.log_result("Holdback Settings Endpoint", False, error="Could not create test affiliate")
                return False
            
            # Test custom holdback settings
            holdback_settings = {
                "percentage": 25.0,  # Custom 25% holdback (instead of default 20%)
                "hold_days": 60,     # Hold for 60 days (instead of default 30)
                "admin_notes": "Custom holdback settings for high-risk affiliate testing"
            }
            
            response = self.session.post(
                f"{API_BASE}/affiliate/admin/affiliates/{test_affiliate_id}/holdback-settings",
                json=holdback_settings
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                message = data.get("message", "")
                settings = data.get("settings", {})
                
                if success and settings.get("percentage") == 25.0 and settings.get("hold_days") == 60:
                    self.log_result("Custom Holdback Settings Endpoint", True, 
                                   f"Successfully set custom holdback: {message}")
                    return True
                else:
                    self.log_result("Custom Holdback Settings Endpoint", False, 
                                   error=f"Settings not applied correctly: {settings}")
                    return False
            else:
                self.log_result("Custom Holdback Settings Endpoint", False, 
                               error=f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Custom Holdback Settings Endpoint", False, error=str(e))
            return False

    def test_monitoring_refresh_endpoint(self):
        """Test monitoring refresh endpoint"""
        try:
            if not self.admin_token:
                self.log_result("Monitoring Refresh Endpoint", False, error="No admin token")
                return False
            
            # Test refresh all affiliates
            response = self.session.post(f"{API_BASE}/affiliate/admin/monitoring/refresh")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                message = data.get("message", "")
                updated_count = data.get("updated_count", 0)
                
                self.log_result("Monitoring Refresh Endpoint", True, 
                               f"Successfully refreshed monitoring for {updated_count} affiliates: {message}")
                return True
            else:
                self.log_result("Monitoring Refresh Endpoint", False, 
                               error=f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Monitoring Refresh Endpoint", False, error=str(e))
            return False

    def test_refund_rate_calculation_function(self):
        """Test the refund rate calculation logic"""
        try:
            if not self.admin_token:
                self.log_result("Refund Rate Calculation Function", False, error="No admin token")
                return False
            
            # Create a test affiliate and simulate refund tracking
            test_affiliate_id = self.test_affiliate_registration_with_terms()
            
            if not test_affiliate_id:
                self.log_result("Refund Rate Calculation Function", False, error="Could not create test affiliate")
                return False
            
            # Create a test customer linked to the affiliate
            customer_id = f"refund_test_customer_{int(time.time())}"
            customer_link_data = {
                "customer_id": customer_id,
                "affiliate_id": test_affiliate_id
            }
            
            link_response = self.session.post(f"{API_BASE}/affiliate/customer/link", json=customer_link_data)
            
            if link_response.status_code == 200:
                self.log_result("Customer-Affiliate Link for Refund Test", True, "Successfully linked customer to affiliate")
                
                # Track a refund
                refund_data = {
                    "customer_id": customer_id,
                    "order_id": f"refund_test_order_{int(time.time())}",
                    "refund_amount": 150.0,
                    "reason": "Testing refund rate calculation"
                }
                
                refund_response = self.session.post(f"{API_BASE}/affiliate/admin/refunds/track", json=refund_data)
                
                if refund_response.status_code == 200:
                    refund_result = refund_response.json()
                    self.log_result("Refund Tracking for Rate Calculation", True, 
                                   f"Successfully tracked refund: {refund_result.get('message', '')}")
                    
                    # Refresh monitoring to trigger refund rate calculation
                    refresh_response = self.session.post(
                        f"{API_BASE}/affiliate/admin/monitoring/refresh",
                        json={"affiliate_id": test_affiliate_id}
                    )
                    
                    if refresh_response.status_code == 200:
                        self.log_result("Refund Rate Calculation Trigger", True, 
                                       "Successfully triggered refund rate recalculation")
                        return True
                    else:
                        self.log_result("Refund Rate Calculation Trigger", False, 
                                       error=f"Could not trigger recalculation: {refresh_response.status_code}")
                        return False
                else:
                    self.log_result("Refund Tracking for Rate Calculation", False, 
                                   error=f"Status: {refund_response.status_code}, Response: {refund_response.text}")
                    return False
            else:
                self.log_result("Customer-Affiliate Link for Refund Test", False, 
                               error=f"Could not link customer: {link_response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Refund Rate Calculation Function", False, error=str(e))
            return False

    def run_all_tests(self):
        """Run all holdback system tests"""
        print("🚀 Starting Enhanced Affiliate System Holdback & Refund Monitoring Tests")
        print("=" * 80)
        
        # Admin authentication
        if not self.admin_login():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Test core holdback functionality
        self.test_high_refund_monitoring_endpoint()
        self.test_affiliate_pause_resume_endpoints()
        self.test_holdback_settings_endpoint()
        self.test_monitoring_refresh_endpoint()
        self.test_refund_rate_calculation_function()
        
        # Summary
        print("=" * 80)
        print("📊 HOLDBACK SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['error']}")
        
        print("\n🎉 Enhanced Affiliate System Holdback Testing Complete!")
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "results": self.test_results
        }

if __name__ == "__main__":
    tester = HoldbackSystemTester()
    results = tester.run_all_tests()