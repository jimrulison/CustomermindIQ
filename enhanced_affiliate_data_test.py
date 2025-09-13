#!/usr/bin/env python3
"""
Enhanced Affiliate Data Endpoints Testing
Tests the new detailed commission, customer, and performance information endpoints
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://ai-mindiq.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

class EnhancedAffiliateDataTester:
    def __init__(self):
        self.session = None
        self.admin_token = None
        self.results = []
        
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

    async def test_affiliate_commissions_endpoint(self):
        """Test GET /api/affiliate/commissions endpoint with detailed commission history"""
        try:
            # Test with existing affiliate ID from previous tests
            test_affiliate_id = "jane_affiliate_2024"
            
            # Test endpoint with parameters
            params = {
                "affiliate_id": test_affiliate_id,
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
                        
                        success = len(enriched_data_checks) == 0 or all(enriched_data_checks)
                        details = f"Found {len(commissions)} commissions with enriched customer data"
                        if commissions:
                            details += f", first commission: ${commissions[0].get('commission_amount', 0):.2f} from {commissions[0].get('customer_name', 'Unknown')}"
                        
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
            # Test with existing affiliate ID
            test_affiliate_id = "jane_affiliate_2024"
            
            params = {
                "affiliate_id": test_affiliate_id,
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
                        
                        success = len(enriched_data_checks) == 0 or all(enriched_data_checks)
                        details = f"Found {len(customers)} customers with spending data"
                        if customers:
                            customer = customers[0]
                            details += f", first customer: {customer.get('name', 'Unknown')} (LTV: ${customer.get('lifetime_value', 0):.2f})"
                        
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
            # Test with existing affiliate ID
            test_affiliate_id = "jane_affiliate_2024"
            
            params = {"affiliate_id": test_affiliate_id}
            
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
            # Test with existing affiliate ID
            test_affiliate_id = "jane_affiliate_2024"
            
            params = {
                "affiliate_id": test_affiliate_id,
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
                        
                        success = len(chart_data_checks) == 0 or all(chart_data_checks)
                        details = f"Chart data points: {len(chart_data)} for period {data.get('period', '30d')}"
                        if chart_data:
                            total_clicks = sum(point.get('clicks', 0) for point in chart_data)
                            total_conversions = sum(point.get('conversions', 0) for point in chart_data)
                            details += f", Total clicks: {total_clicks}, Total conversions: {total_conversions}"
                        
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
            
            success = commissions_success or customers_success or metrics_success
            details = f"Demo affiliate endpoints - Commissions: {commissions_success}, Customers: {customers_success}, Metrics: {metrics_success}"
            
            self.log_result("Demo Affiliate Fallback Data", success, details)
            return success
            
        except Exception as e:
            self.log_result("Demo Affiliate Fallback Data", False, f"Request error: {str(e)}")
            return False

    async def test_data_quality_validation(self):
        """Test data quality and calculations in affiliate endpoints"""
        try:
            test_affiliate_id = "jane_affiliate_2024"
            
            # Get commissions data
            params = {"affiliate_id": test_affiliate_id, "limit": 10}
            async with self.session.get(f"{API_BASE}/affiliate/commissions", params=params) as response:
                commissions_data = await response.json() if response.status == 200 else {}
            
            # Get customers data  
            async with self.session.get(f"{API_BASE}/affiliate/customers", params=params) as response:
                customers_data = await response.json() if response.status == 200 else {}
            
            # Get metrics data
            params = {"affiliate_id": test_affiliate_id}
            async with self.session.get(f"{API_BASE}/affiliate/metrics", params=params) as response:
                metrics_data = await response.json() if response.status == 200 else {}
            
            quality_checks = []
            
            # Check commission calculations
            if commissions_data.get("success") and commissions_data.get("commissions"):
                commissions = commissions_data["commissions"]
                for commission in commissions[:3]:  # Check first 3
                    base_amount = commission.get("base_amount", 0)
                    commission_amount = commission.get("commission_amount", 0)
                    commission_rate = commission.get("commission_rate", 0)
                    
                    # Validate commission calculation
                    expected_commission = base_amount * (commission_rate / 100)
                    calculation_correct = abs(commission_amount - expected_commission) < 0.01
                    quality_checks.append(calculation_correct)
            
            # Check customer data completeness
            if customers_data.get("success") and customers_data.get("customers"):
                customers = customers_data["customers"]
                for customer in customers[:3]:  # Check first 3
                    has_required_fields = all([
                        customer.get("name"),
                        customer.get("email"),
                        "total_spent" in customer,
                        "lifetime_value" in customer
                    ])
                    quality_checks.append(has_required_fields)
            
            # Check metrics calculations
            if metrics_data.get("success") and metrics_data.get("metrics"):
                metrics = metrics_data["metrics"]
                # Conversion rate should be between 0 and 100
                conversion_rate = metrics.get("conversion_rate", 0)
                quality_checks.append(0 <= conversion_rate <= 100)
                
                # AOV and LTV should be positive or zero
                aov = metrics.get("avg_order_value", 0)
                ltv = metrics.get("customer_lifetime_value", 0)
                quality_checks.append(aov >= 0 and ltv >= 0)
            
            success = len(quality_checks) == 0 or all(quality_checks)
            details = f"Data quality checks passed: {sum(quality_checks)}/{len(quality_checks)}"
            
            self.log_result("Data Quality Validation", success, details)
            return success
            
        except Exception as e:
            self.log_result("Data Quality Validation", False, f"Validation error: {str(e)}")
            return False

    async def run_all_tests(self):
        """Run all enhanced affiliate data endpoint tests"""
        print("🚀 Starting Enhanced Affiliate Data Endpoints Testing")
        print("=" * 60)
        
        await self.setup_session()
        
        try:
            # Authentication (optional for affiliate endpoints)
            await self.admin_login()
            
            # Test all enhanced affiliate data endpoints
            tests = [
                self.test_affiliate_commissions_endpoint(),
                self.test_affiliate_customers_endpoint(), 
                self.test_affiliate_metrics_endpoint(),
                self.test_affiliate_performance_chart_endpoint(),
                self.test_demo_affiliate_fallback(),
                self.test_data_quality_validation()
            ]
            
            results = await asyncio.gather(*tests, return_exceptions=True)
            
            # Calculate success rate
            successful_tests = sum(1 for result in results if result is True)
            total_tests = len(results)
            success_rate = (successful_tests / total_tests) * 100
            
            print("\n" + "=" * 60)
            print("🎯 ENHANCED AFFILIATE DATA ENDPOINTS TEST SUMMARY")
            print("=" * 60)
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