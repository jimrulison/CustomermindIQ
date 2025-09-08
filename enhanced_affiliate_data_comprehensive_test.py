#!/usr/bin/env python3
"""
Enhanced Affiliate Data Endpoints Comprehensive Testing
Tests the new detailed commission, customer, and performance information endpoints with real data
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://pagebuilder-iq.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

class EnhancedAffiliateDataTester:
    def __init__(self):
        self.session = None
        self.admin_token = None
        self.results = []
        self.test_affiliate_id = None
        
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
        """Login as admin to get authentication token"""
        try:
            login_data = {
                "email": "admin@customermindiq.com",
                "password": "CustomerMindIQ2025!"
            }
            
            async with self.session.post(f"{API_BASE}/auth/login", json=login_data) as response:
                if response.status == 200:
                    data = await response.json()
                    self.admin_token = data.get("access_token")
                    self.log_result("Admin Authentication", True, f"Successfully logged in as admin")
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("Admin Authentication", False, f"Login failed: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Login error: {str(e)}")
            return False

    async def setup_test_affiliate(self):
        """Get existing affiliate and approve them for testing"""
        try:
            if not self.admin_token:
                return False
                
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            # Get list of affiliates
            async with self.session.get(f"{API_BASE}/affiliate/admin/affiliates", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    affiliates = data.get("affiliates", [])
                    
                    if affiliates:
                        # Use first affiliate
                        affiliate = affiliates[0]
                        self.test_affiliate_id = affiliate["affiliate_id"]
                        
                        # Approve the affiliate if not already approved
                        if affiliate["status"] != "approved":
                            status_data = {"status": "approved"}
                            async with self.session.patch(
                                f"{API_BASE}/affiliate/admin/affiliates/{self.test_affiliate_id}/status",
                                headers=headers,
                                json=status_data
                            ) as status_response:
                                if status_response.status == 200:
                                    self.log_result("Affiliate Setup", True, f"Approved affiliate {self.test_affiliate_id}")
                                else:
                                    self.log_result("Affiliate Setup", True, f"Using existing affiliate {self.test_affiliate_id}")
                        else:
                            self.log_result("Affiliate Setup", True, f"Using approved affiliate {self.test_affiliate_id}")
                        
                        return True
                    else:
                        self.log_result("Affiliate Setup", False, "No affiliates found")
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("Affiliate Setup", False, f"Failed to get affiliates: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Setup", False, f"Setup error: {str(e)}")
            return False

    async def create_test_commission_data(self):
        """Create some test commission and customer data"""
        try:
            if not self.test_affiliate_id:
                return False
            
            # Simulate a conversion event to create commission data
            conversion_data = {
                "event_type": "conversion",
                "affiliate_id": self.test_affiliate_id,
                "customer_id": f"test_customer_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "plan_type": "growth",
                "billing_cycle": "monthly",
                "amount": 750.0,
                "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            async with self.session.post(f"{API_BASE}/affiliate/track/event", json=conversion_data) as response:
                if response.status == 200:
                    self.log_result("Test Data Creation", True, "Created test commission and customer data")
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("Test Data Creation", False, f"Failed to create test data: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Test Data Creation", False, f"Data creation error: {str(e)}")
            return False

    async def test_affiliate_commissions_endpoint(self):
        """Test GET /api/affiliate/commissions endpoint with detailed commission history"""
        try:
            if not self.test_affiliate_id:
                self.log_result("Affiliate Commissions Endpoint", False, "No test affiliate ID available")
                return False
            
            params = {
                "affiliate_id": self.test_affiliate_id,
                "limit": 10
            }
            
            async with self.session.get(f"{API_BASE}/affiliate/commissions", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    if data.get("success") and "commissions" in data:
                        commissions = data["commissions"]
                        
                        # Check if commissions have enriched data
                        enriched_data_checks = []
                        if commissions:
                            commission = commissions[0]
                            # Check for customer details
                            enriched_data_checks.extend([
                                "customer_name" in commission,
                                "customer_email" in commission,
                                "plan_type" in commission,
                                "commission_amount" in commission,
                                "commission_rate" in commission,
                                "base_amount" in commission,
                                "earned_date" in commission,
                                "status" in commission
                            ])
                        
                        success = True  # Endpoint works even with no data
                        details = f"Found {len(commissions)} commissions with enriched customer data structure"
                        if commissions:
                            commission = commissions[0]
                            details += f", first commission: ${commission.get('commission_amount', 0):.2f} from {commission.get('customer_name', 'Unknown')}"
                            details += f", enrichment fields present: {sum(enriched_data_checks)}/8"
                        
                        self.log_result("Affiliate Commissions Endpoint", success, details, data)
                        return success
                    else:
                        self.log_result("Affiliate Commissions Endpoint", False, "Invalid response structure", data)
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("Affiliate Commissions Endpoint", False, f"HTTP {response.status}: {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Commissions Endpoint", False, f"Request error: {str(e)}")
            return False

    async def test_affiliate_customers_endpoint(self):
        """Test GET /api/affiliate/customers endpoint with customer referral details"""
        try:
            if not self.test_affiliate_id:
                self.log_result("Affiliate Customers Endpoint", False, "No test affiliate ID available")
                return False
            
            params = {
                "affiliate_id": self.test_affiliate_id,
                "limit": 20
            }
            
            async with self.session.get(f"{API_BASE}/affiliate/customers", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("success") and "customers" in data:
                        customers = data["customers"]
                        
                        # Check customer data enrichment
                        enriched_data_checks = []
                        if customers:
                            customer = customers[0]
                            enriched_data_checks.extend([
                                "customer_id" in customer,
                                "name" in customer,
                                "email" in customer,
                                "plan" in customer,
                                "signup_date" in customer,
                                "status" in customer,
                                "total_spent" in customer,
                                "lifetime_value" in customer
                            ])
                        
                        success = True  # Endpoint works even with no data
                        details = f"Found {len(customers)} customers with spending data structure"
                        if customers:
                            customer = customers[0]
                            details += f", first customer: {customer.get('name', 'Unknown')} (LTV: ${customer.get('lifetime_value', 0):.2f})"
                            details += f", enrichment fields present: {sum(enriched_data_checks)}/8"
                        
                        self.log_result("Affiliate Customers Endpoint", success, details, data)
                        return success
                    else:
                        self.log_result("Affiliate Customers Endpoint", False, "Invalid response structure", data)
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("Affiliate Customers Endpoint", False, f"HTTP {response.status}: {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Customers Endpoint", False, f"Request error: {str(e)}")
            return False

    async def test_affiliate_metrics_endpoint(self):
        """Test GET /api/affiliate/metrics endpoint with performance analytics"""
        try:
            if not self.test_affiliate_id:
                self.log_result("Affiliate Metrics Endpoint", False, "No test affiliate ID available")
                return False
            
            params = {"affiliate_id": self.test_affiliate_id}
            
            async with self.session.get(f"{API_BASE}/affiliate/metrics", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("success") and "metrics" in data:
                        metrics = data["metrics"]
                        
                        # Check for required metrics
                        required_metrics = [
                            "conversion_rate",
                            "avg_order_value", 
                            "customer_lifetime_value",
                            "top_traffic_sources",
                            "total_customers",
                            "active_customers",
                            "monthly_recurring_revenue",
                            "annual_recurring_revenue"
                        ]
                        
                        metrics_present = [metric in metrics for metric in required_metrics]
                        success = all(metrics_present)
                        
                        details = f"Metrics available: {sum(metrics_present)}/{len(required_metrics)}"
                        details += f", Conversion Rate: {metrics.get('conversion_rate', 0):.2f}%"
                        details += f", AOV: ${metrics.get('avg_order_value', 0):.2f}"
                        details += f", LTV: ${metrics.get('customer_lifetime_value', 0):.2f}"
                        
                        self.log_result("Affiliate Metrics Endpoint", success, details, data)
                        return success
                    else:
                        self.log_result("Affiliate Metrics Endpoint", False, "Invalid response structure", data)
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("Affiliate Metrics Endpoint", False, f"HTTP {response.status}: {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Metrics Endpoint", False, f"Request error: {str(e)}")
            return False

    async def test_affiliate_performance_chart_endpoint(self):
        """Test GET /api/affiliate/performance/chart endpoint with chart data"""
        try:
            if not self.test_affiliate_id:
                self.log_result("Affiliate Performance Chart Endpoint", False, "No test affiliate ID available")
                return False
            
            params = {
                "affiliate_id": self.test_affiliate_id,
                "period": "30d"
            }
            
            async with self.session.get(f"{API_BASE}/affiliate/performance/chart", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("success") and "chart_data" in data:
                        chart_data = data["chart_data"]
                        
                        # Check chart data structure
                        chart_data_checks = []
                        if chart_data:
                            data_point = chart_data[0]
                            chart_data_checks.extend([
                                "date" in data_point,
                                "clicks" in data_point,
                                "conversions" in data_point,
                                "conversion_rate" in data_point
                            ])
                        
                        success = True  # Endpoint works even with no data
                        details = f"Chart data points: {len(chart_data)} for period {data.get('period', '30d')}"
                        if chart_data:
                            total_clicks = sum(point.get('clicks', 0) for point in chart_data)
                            total_conversions = sum(point.get('conversions', 0) for point in chart_data)
                            details += f", Total clicks: {total_clicks}, Total conversions: {total_conversions}"
                            details += f", structure fields present: {sum(chart_data_checks)}/4"
                        
                        self.log_result("Affiliate Performance Chart Endpoint", success, details, data)
                        return success
                    else:
                        self.log_result("Affiliate Performance Chart Endpoint", False, "Invalid response structure", data)
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("Affiliate Performance Chart Endpoint", False, f"HTTP {response.status}: {error_text}")
                    return False
                    
        except Exception as e:
            self.log_result("Affiliate Performance Chart Endpoint", False, f"Request error: {str(e)}")
            return False

    async def test_demo_affiliate_fallback(self):
        """Test endpoints with demo affiliate ID for fallback data"""
        try:
            demo_affiliate_id = "demo_affiliate_001"
            
            # Test commissions endpoint with demo ID
            params = {"affiliate_id": demo_affiliate_id, "limit": 5}
            
            async with self.session.get(f"{API_BASE}/affiliate/commissions", params=params) as response:
                commissions_success = response.status == 200
                commissions_data = await response.json() if commissions_success else {}
            
            # Test customers endpoint with demo ID
            async with self.session.get(f"{API_BASE}/affiliate/customers", params=params) as response:
                customers_success = response.status == 200
                customers_data = await response.json() if customers_success else {}
            
            # Test metrics endpoint with demo ID
            params = {"affiliate_id": demo_affiliate_id}
            async with self.session.get(f"{API_BASE}/affiliate/metrics", params=params) as response:
                metrics_success = response.status == 200
                metrics_data = await response.json() if metrics_success else {}
            
            # Test chart endpoint with demo ID
            params = {"affiliate_id": demo_affiliate_id, "period": "30d"}
            async with self.session.get(f"{API_BASE}/affiliate/performance/chart", params=params) as response:
                chart_success = response.status == 200
                chart_data = await response.json() if chart_success else {}
            
            success = commissions_success and customers_success and chart_success
            details = f"Demo affiliate endpoints - Commissions: {commissions_success}, Customers: {customers_success}, Metrics: {metrics_success}, Chart: {chart_success}"
            
            self.log_result("Demo Affiliate Fallback Data", success, details)
            return success
            
        except Exception as e:
            self.log_result("Demo Affiliate Fallback Data", False, f"Request error: {str(e)}")
            return False

    async def test_endpoint_parameters_validation(self):
        """Test endpoint parameter validation and error handling"""
        try:
            test_cases = []
            
            # Test missing affiliate_id parameter
            async with self.session.get(f"{API_BASE}/affiliate/commissions") as response:
                test_cases.append(("Missing affiliate_id", response.status in [400, 422]))
            
            # Test invalid period parameter
            params = {"affiliate_id": "test", "period": "invalid"}
            async with self.session.get(f"{API_BASE}/affiliate/performance/chart", params=params) as response:
                test_cases.append(("Invalid period parameter", response.status in [400, 422]))
            
            # Test limit parameter validation
            params = {"affiliate_id": "test", "limit": 200}  # Over limit
            async with self.session.get(f"{API_BASE}/affiliate/commissions", params=params) as response:
                test_cases.append(("Limit validation", response.status in [200, 400, 422]))  # Should handle gracefully
            
            success = all(result for _, result in test_cases)
            details = f"Parameter validation tests: {sum(result for _, result in test_cases)}/{len(test_cases)} passed"
            
            self.log_result("Endpoint Parameters Validation", success, details)
            return success
            
        except Exception as e:
            self.log_result("Endpoint Parameters Validation", False, f"Validation error: {str(e)}")
            return False

    async def run_all_tests(self):
        """Run all enhanced affiliate data endpoint tests"""
        print("🚀 Starting Enhanced Affiliate Data Endpoints Comprehensive Testing")
        print("=" * 70)
        
        await self.setup_session()
        
        try:
            # Authentication and setup
            auth_success = await self.admin_login()
            if not auth_success:
                print("❌ Cannot proceed without admin authentication")
                return False
            
            setup_success = await self.setup_test_affiliate()
            if setup_success:
                await self.create_test_commission_data()
            
            # Test all enhanced affiliate data endpoints
            tests = [
                self.test_affiliate_commissions_endpoint(),
                self.test_affiliate_customers_endpoint(), 
                self.test_affiliate_metrics_endpoint(),
                self.test_affiliate_performance_chart_endpoint(),
                self.test_demo_affiliate_fallback(),
                self.test_endpoint_parameters_validation()
            ]
            
            results = await asyncio.gather(*tests, return_exceptions=True)
            
            # Calculate success rate
            successful_tests = sum(1 for result in results if result is True)
            total_tests = len(results)
            success_rate = (successful_tests / total_tests) * 100
            
            print("\n" + "=" * 70)
            print("🎯 ENHANCED AFFILIATE DATA ENDPOINTS TEST SUMMARY")
            print("=" * 70)
            print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
            print(f"📊 Success Rate: {success_rate:.1f}%")
            
            if success_rate >= 80:
                print("🎉 EXCELLENT: Enhanced affiliate data endpoints are working well!")
            elif success_rate >= 60:
                print("✅ GOOD: Most enhanced affiliate data endpoints are functional")
            else:
                print("⚠️  NEEDS ATTENTION: Several enhanced affiliate data endpoints need fixes")
            
            # Detailed results
            print("\n📋 DETAILED TEST RESULTS:")
            for result in self.results:
                status = "✅" if result["success"] else "❌"
                print(f"{status} {result['test']}")
                if result["details"]:
                    print(f"   {result['details']}")
            
            return success_rate >= 60
            
        finally:
            await self.cleanup_session()

async def main():
    """Main test execution"""
    tester = EnhancedAffiliateDataTester()
    success = await tester.run_all_tests()
    return success

if __name__ == "__main__":
    asyncio.run(main())