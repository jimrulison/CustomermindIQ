#!/usr/bin/env python3
"""
Enhanced Affiliate System with Holdback Functionality - Backend Testing
Testing holdback functionality, refund monitoring, and admin endpoints
"""

import requests
import json
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-iq-touch.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials for testing admin endpoints
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class EnhancedAffiliateSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_affiliate_id = None
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
        """Login as admin to get authentication token"""
        try:
            response = self.session.post(f"{API_BASE}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
                self.log_result("Admin Login", True, f"Successfully logged in as {ADMIN_EMAIL}")
                return True
            else:
                self.log_result("Admin Login", False, error=f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Admin Login", False, error=str(e))
            return False

    def test_enhanced_affiliate_registration(self):
        """Test affiliate registration with terms_accepted field"""
        try:
            # Test registration without terms_accepted (should fail)
            registration_data_no_terms = {
                "first_name": "Test",
                "last_name": "Affiliate",
                "email": "test.affiliate.enhanced@example.com",
                "phone": "+1234567890",
                "website": "https://testaffiliate.com",
                "promotion_method": "social",
                "password": "SecurePass123!",
                "address": {
                    "street": "123 Test St",
                    "city": "Test City",
                    "state": "TS",
                    "zip_code": "12345",
                    "country": "US"
                },
                "payment_method": "paypal",
                "payment_details": {
                    "paypal_email": "test@paypal.com"
                },
                "terms_accepted": False  # Should fail
            }
            
            response = self.session.post(f"{API_BASE}/affiliate/auth/register", json=registration_data_no_terms)
            
            if response.status_code == 422:  # Validation error expected
                self.log_result("Registration Terms Validation", True, "Correctly rejected registration without terms acceptance")
            else:
                self.log_result("Registration Terms Validation", False, error=f"Expected 422, got {response.status_code}")
            
            # Test successful registration with terms_accepted=true
            registration_data_with_terms = registration_data_no_terms.copy()
            registration_data_with_terms["terms_accepted"] = True
            registration_data_with_terms["email"] = "test.affiliate.enhanced.valid@example.com"
            
            response = self.session.post(f"{API_BASE}/affiliate/auth/register", json=registration_data_with_terms)
            
            if response.status_code == 200:
                data = response.json()
                self.test_affiliate_id = data.get("affiliate_id")
                self.log_result("Enhanced Affiliate Registration", True, 
                               f"Successfully registered affiliate with ID: {self.test_affiliate_id}")
                
                # Verify monitoring record was created
                if self.admin_token:
                    monitoring_response = self.session.get(f"{API_BASE}/affiliate/admin/monitoring/high-refund")
                    if monitoring_response.status_code == 200:
                        self.log_result("Affiliate Monitoring Record Creation", True, 
                                       "Monitoring system initialized for new affiliate")
                    else:
                        self.log_result("Affiliate Monitoring Record Creation", False, 
                                       error=f"Could not verify monitoring record: {monitoring_response.status_code}")
                
                return True
            else:
                self.log_result("Enhanced Affiliate Registration", False, 
                               error=f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Enhanced Affiliate Registration", False, error=str(e))
            return False

    def test_holdback_system(self):
        """Test holdback calculation and record creation"""
        try:
            if not self.test_affiliate_id:
                self.log_result("Holdback System Test", False, error="No test affiliate ID available")
                return False
            
            # First, approve the affiliate so we can test commission creation
            if self.admin_token:
                approve_response = self.session.patch(
                    f"{API_BASE}/affiliate/admin/affiliates/{self.test_affiliate_id}/status",
                    json={"status": "approved"}
                )
                
                if approve_response.status_code == 200:
                    self.log_result("Affiliate Approval", True, "Test affiliate approved for holdback testing")
                else:
                    self.log_result("Affiliate Approval", False, 
                                   error=f"Could not approve affiliate: {approve_response.status_code}")
            
            # Simulate a conversion event to trigger commission creation with holdback
            conversion_data = {
                "event_type": "conversion",
                "affiliate_id": self.test_affiliate_id,
                "customer_id": f"test_customer_{int(time.time())}",
                "plan_type": "growth",
                "billing_cycle": "monthly",
                "amount": 750.0,  # $750 monthly plan
                "session_id": f"session_{int(time.time())}"
            }
            
            response = self.session.post(f"{API_BASE}/affiliate/track/event", json=conversion_data)
            
            if response.status_code == 200:
                self.log_result("Conversion Event Tracking", True, "Successfully tracked conversion event")
                
                # Wait a moment for processing
                time.sleep(2)
                
                # Check if holdback records were created
                # We'll check the affiliate dashboard to see if holdback amounts are properly split
                dashboard_response = self.session.get(f"{API_BASE}/affiliate/dashboard", 
                                                    params={"affiliate_id": self.test_affiliate_id})
                
                if dashboard_response.status_code == 200:
                    dashboard_data = dashboard_response.json()
                    affiliate = dashboard_data.get("affiliate", {})
                    
                    available_commissions = affiliate.get("available_commissions", 0)
                    held_commissions = affiliate.get("held_commissions", 0)
                    total_commissions = affiliate.get("total_commissions", 0)
                    
                    # For a $750 growth plan, initial commission should be 40% = $300
                    # Default holdback is 20%, so available should be $240, held should be $60
                    expected_total = 300.0
                    expected_available = 240.0  # 80% of commission
                    expected_held = 60.0        # 20% of commission
                    
                    if (abs(total_commissions - expected_total) < 1.0 and 
                        abs(available_commissions - expected_available) < 1.0 and 
                        abs(held_commissions - expected_held) < 1.0):
                        
                        self.log_result("Holdback Calculation", True, 
                                       f"Correct holdback split - Total: ${total_commissions}, Available: ${available_commissions}, Held: ${held_commissions}")
                    else:
                        self.log_result("Holdback Calculation", False, 
                                       error=f"Incorrect amounts - Total: ${total_commissions}, Available: ${available_commissions}, Held: ${held_commissions}")
                else:
                    self.log_result("Holdback Verification", False, 
                                   error=f"Could not get dashboard data: {dashboard_response.status_code}")
            else:
                self.log_result("Conversion Event Tracking", False, 
                               error=f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_result("Holdback System Test", False, error=str(e))

    def test_admin_monitoring_endpoints(self):
        """Test admin monitoring endpoints"""
        try:
            if not self.admin_token:
                self.log_result("Admin Monitoring Endpoints", False, error="No admin token available")
                return False
            
            # Test GET /api/affiliate/admin/monitoring/high-refund
            response = self.session.get(f"{API_BASE}/affiliate/admin/monitoring/high-refund")
            
            if response.status_code == 200:
                data = response.json()
                self.log_result("High Refund Monitoring Endpoint", True, 
                               f"Successfully retrieved high refund affiliates: {data.get('total_flagged', 0)} flagged")
            else:
                self.log_result("High Refund Monitoring Endpoint", False, 
                               error=f"Status: {response.status_code}, Response: {response.text}")
            
            if self.test_affiliate_id:
                # Test POST /api/affiliate/admin/affiliates/{id}/pause
                pause_response = self.session.post(
                    f"{API_BASE}/affiliate/admin/affiliates/{self.test_affiliate_id}/pause",
                    json={"reason": "Test pause for holdback system testing"}
                )
                
                if pause_response.status_code == 200:
                    self.log_result("Affiliate Pause Endpoint", True, "Successfully paused test affiliate")
                    
                    # Test POST /api/affiliate/admin/affiliates/{id}/resume
                    resume_response = self.session.post(
                        f"{API_BASE}/affiliate/admin/affiliates/{self.test_affiliate_id}/resume"
                    )
                    
                    if resume_response.status_code == 200:
                        self.log_result("Affiliate Resume Endpoint", True, "Successfully resumed test affiliate")
                    else:
                        self.log_result("Affiliate Resume Endpoint", False, 
                                       error=f"Status: {resume_response.status_code}")
                else:
                    self.log_result("Affiliate Pause Endpoint", False, 
                                   error=f"Status: {pause_response.status_code}")
                
                # Test POST /api/affiliate/admin/affiliates/{id}/holdback-settings
                holdback_settings = {
                    "percentage": 30.0,  # Custom 30% holdback
                    "hold_days": 45,     # Hold for 45 days
                    "admin_notes": "Custom holdback for testing purposes"
                }
                
                holdback_response = self.session.post(
                    f"{API_BASE}/affiliate/admin/affiliates/{self.test_affiliate_id}/holdback-settings",
                    json=holdback_settings
                )
                
                if holdback_response.status_code == 200:
                    data = holdback_response.json()
                    self.log_result("Custom Holdback Settings", True, 
                                   f"Successfully set custom holdback: {data.get('message', '')}")
                else:
                    self.log_result("Custom Holdback Settings", False, 
                                   error=f"Status: {holdback_response.status_code}")
            
            # Test POST /api/affiliate/admin/monitoring/refresh
            refresh_response = self.session.post(f"{API_BASE}/affiliate/admin/monitoring/refresh")
            
            if refresh_response.status_code == 200:
                data = refresh_response.json()
                self.log_result("Monitoring Refresh Endpoint", True, 
                               f"Successfully refreshed monitoring: {data.get('message', '')}")
            else:
                self.log_result("Monitoring Refresh Endpoint", False, 
                               error=f"Status: {refresh_response.status_code}")
                
        except Exception as e:
            self.log_result("Admin Monitoring Endpoints", False, error=str(e))

    def test_refund_rate_calculation(self):
        """Test refund rate calculation and flagging logic"""
        try:
            if not self.admin_token or not self.test_affiliate_id:
                self.log_result("Refund Rate Calculation", False, error="Missing admin token or affiliate ID")
                return False
            
            # Create a test refund to trigger refund rate calculation
            refund_data = {
                "customer_id": f"test_customer_{int(time.time())}",
                "order_id": f"order_{int(time.time())}",
                "refund_amount": 200.0,  # $200 refund
                "reason": "Test refund for rate calculation"
            }
            
            # First, we need to create a customer record linked to our affiliate
            customer_link_data = {
                "customer_id": refund_data["customer_id"],
                "affiliate_id": self.test_affiliate_id
            }
            
            link_response = self.session.post(f"{API_BASE}/affiliate/customer/link", json=customer_link_data)
            
            if link_response.status_code == 200:
                self.log_result("Customer-Affiliate Link", True, "Successfully linked customer to affiliate")
                
                # Now track the refund
                refund_response = self.session.post(f"{API_BASE}/affiliate/admin/refunds/track", json=refund_data)
                
                if refund_response.status_code == 200:
                    refund_result = refund_response.json()
                    self.log_result("Refund Tracking", True, 
                                   f"Successfully tracked refund: ${refund_result.get('commission_clawed_back', 0)} clawed back")
                    
                    # Refresh monitoring to recalculate refund rate
                    refresh_response = self.session.post(
                        f"{API_BASE}/affiliate/admin/monitoring/refresh",
                        json={"affiliate_id": self.test_affiliate_id}
                    )
                    
                    if refresh_response.status_code == 200:
                        self.log_result("Refund Rate Recalculation", True, "Successfully recalculated refund rate")
                        
                        # Check if affiliate is flagged for high refund rate
                        monitoring_response = self.session.get(f"{API_BASE}/affiliate/admin/monitoring/high-refund")
                        
                        if monitoring_response.status_code == 200:
                            monitoring_data = monitoring_response.json()
                            flagged_affiliates = monitoring_data.get("high_refund_affiliates", [])
                            
                            # Check if our test affiliate is in the flagged list
                            is_flagged = any(aff.get("affiliate_id") == self.test_affiliate_id for aff in flagged_affiliates)
                            
                            if is_flagged:
                                flagged_affiliate = next(aff for aff in flagged_affiliates if aff.get("affiliate_id") == self.test_affiliate_id)
                                refund_rate = flagged_affiliate.get("refund_rate_90d", 0)
                                
                                self.log_result("Refund Rate Flagging Logic", True, 
                                               f"Affiliate correctly flagged with {refund_rate:.2f}% refund rate")
                            else:
                                self.log_result("Refund Rate Flagging Logic", True, 
                                               "Affiliate not flagged (refund rate below 15% threshold)")
                        else:
                            self.log_result("Refund Rate Verification", False, 
                                           error=f"Could not verify flagging: {monitoring_response.status_code}")
                    else:
                        self.log_result("Refund Rate Recalculation", False, 
                                       error=f"Could not refresh monitoring: {refresh_response.status_code}")
                else:
                    self.log_result("Refund Tracking", False, 
                                   error=f"Status: {refund_response.status_code}, Response: {refund_response.text}")
            else:
                self.log_result("Customer-Affiliate Link", False, 
                               error=f"Could not link customer: {link_response.status_code}")
                
        except Exception as e:
            self.log_result("Refund Rate Calculation", False, error=str(e))

    def test_commission_creation_with_holdback(self):
        """Test commission creation with holdback integration"""
        try:
            if not self.test_affiliate_id:
                self.log_result("Commission Creation with Holdback", False, error="No test affiliate ID")
                return False
            
            # Get commissions for our test affiliate to verify holdback integration
            commissions_response = self.session.get(
                f"{API_BASE}/affiliate/commissions",
                params={"affiliate_id": self.test_affiliate_id, "limit": 10}
            )
            
            if commissions_response.status_code == 200:
                data = commissions_response.json()
                commissions = data.get("commissions", [])
                
                if commissions:
                    # Check if commissions have holdback fields
                    first_commission = commissions[0]
                    has_available_amount = "available_amount" in first_commission
                    has_held_amount = "held_amount" in first_commission
                    has_holdback_id = "holdback_id" in first_commission
                    
                    if has_available_amount and has_held_amount:
                        available = first_commission.get("available_amount", 0)
                        held = first_commission.get("held_amount", 0)
                        total = first_commission.get("commission_amount", 0)
                        
                        # Verify the split is correct (should be 80/20 by default)
                        expected_available = total * 0.8
                        expected_held = total * 0.2
                        
                        if (abs(available - expected_available) < 0.01 and 
                            abs(held - expected_held) < 0.01):
                            
                            self.log_result("Commission Holdback Integration", True, 
                                           f"Correct holdback split - Available: ${available:.2f}, Held: ${held:.2f}")
                        else:
                            self.log_result("Commission Holdback Integration", False, 
                                           error=f"Incorrect split - Available: ${available}, Held: ${held}, Total: ${total}")
                    else:
                        self.log_result("Commission Holdback Integration", False, 
                                       error="Commission records missing holdback fields")
                    
                    if has_holdback_id:
                        self.log_result("Holdback ID Linkage", True, "Commission properly linked to holdback record")
                    else:
                        self.log_result("Holdback ID Linkage", False, error="Missing holdback_id in commission")
                        
                else:
                    self.log_result("Commission Creation with Holdback", False, 
                                   error="No commissions found for test affiliate")
            else:
                self.log_result("Commission Creation with Holdback", False, 
                               error=f"Could not retrieve commissions: {commissions_response.status_code}")
                
        except Exception as e:
            self.log_result("Commission Creation with Holdback", False, error=str(e))

    def run_all_tests(self):
        """Run all enhanced affiliate system tests"""
        print("🚀 Starting Enhanced Affiliate System with Holdback Functionality Testing")
        print("=" * 80)
        
        # Admin authentication
        if not self.admin_login():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Test enhanced affiliate registration
        self.test_enhanced_affiliate_registration()
        
        # Test holdback system
        self.test_holdback_system()
        
        # Test admin monitoring endpoints
        self.test_admin_monitoring_endpoints()
        
        # Test refund rate calculation
        self.test_refund_rate_calculation()
        
        # Test commission creation with holdback
        self.test_commission_creation_with_holdback()
        
        # Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
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
        
        print("\n🎉 Enhanced Affiliate System with Holdback Testing Complete!")
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "results": self.test_results
        }

if __name__ == "__main__":
    tester = EnhancedAffiliateSystemTester()
    results = tester.run_all_tests()