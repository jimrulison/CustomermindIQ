#!/usr/bin/env python3
"""
Phase 2 Enhanced CRM Features Backend Testing
Testing ODOO CRM integration endpoints for sales pipeline, analytics, forecasting, and customer management
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Test Configuration
BACKEND_URL = "https://reftrack-1.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@customermindiq.com"
ADMIN_PASSWORD = "CustomerMindIQ2025!"

class Phase2CRMTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.token = None
        self.test_results = []
        
    async def authenticate(self) -> bool:
        """Authenticate with admin credentials"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={
                        "email": ADMIN_EMAIL,
                        "password": ADMIN_PASSWORD
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get("access_token")
                    print(f"✅ Authentication successful - Token: {self.token[:20]}...")
                    return True
                else:
                    print(f"❌ Authentication failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def test_sales_pipeline(self) -> Dict[str, Any]:
        """Test /api/odoo/crm/pipeline endpoint"""
        print("\n📊 Testing Sales Pipeline Management...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/crm/pipeline",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "Sales Pipeline Management",
                    "endpoint": "/api/odoo/crm/pipeline",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    pipeline = data.get("pipeline", [])
                    result["pipeline_count"] = len(pipeline)
                    
                    print(f"✅ Sales Pipeline Retrieved: {len(pipeline)} opportunities found")
                    if pipeline:
                        print("   Pipeline Summary:")
                        for i, opp in enumerate(pipeline[:3]):  # Show first 3
                            print(f"   - {opp.get('name', 'Unnamed')}: ${opp.get('expected_revenue', 0)} ({opp.get('stage', 'Unknown')})")
                    else:
                        print("   No opportunities found in ODOO pipeline (expected for empty database)")
                else:
                    result["error"] = response.text
                    print(f"❌ Sales pipeline test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Sales Pipeline Management",
                "endpoint": "/api/odoo/crm/pipeline",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Sales pipeline test error: {e}")
            return result
    
    async def test_create_lead(self) -> Dict[str, Any]:
        """Test /api/odoo/crm/leads/create endpoint"""
        print("\n🎯 Testing Lead Creation...")
        
        try:
            # Test data for lead creation
            lead_data = {
                "name": "Customer Mind IQ Test Lead",
                "email": "testlead@example.com",
                "phone": "+1-555-0199",
                "company": "Test Company Ltd",
                "description": "This is a test lead created for Phase 2 CRM testing. Customer interested in AI-powered analytics platform.",
                "expected_revenue": 5000.0,
                "probability": 25,
                "source": "Website Contact Form"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/odoo/crm/leads/create",
                    headers=self.get_headers(),
                    json=lead_data
                )
                
                result = {
                    "test": "Lead/Opportunity Creation",
                    "endpoint": "/api/odoo/crm/leads/create",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    lead_id = data.get("lead_id")
                    result["lead_id"] = lead_id
                    
                    print(f"✅ Lead Created Successfully")
                    print(f"   Lead ID: {lead_id}")
                    print(f"   Name: {lead_data['name']}")
                    print(f"   Expected Revenue: ${lead_data['expected_revenue']}")
                    print(f"   Probability: {lead_data['probability']}%")
                else:
                    result["error"] = response.text
                    print(f"❌ Lead creation failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Lead/Opportunity Creation",
                "endpoint": "/api/odoo/crm/leads/create",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Lead creation test error: {e}")
            return result
    
    async def test_update_lead_stage(self, lead_id: int = None) -> Dict[str, Any]:
        """Test /api/odoo/crm/leads/{lead_id}/stage endpoint"""
        print("\n🔄 Testing Lead Stage Update...")
        
        # Use a test lead ID if none provided
        if lead_id is None:
            lead_id = 1  # Assume there's at least one lead for testing
        
        try:
            stage_data = {
                "stage_name": "Qualified"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.put(
                    f"{self.base_url}/odoo/crm/leads/{lead_id}/stage",
                    headers=self.get_headers(),
                    json=stage_data
                )
                
                result = {
                    "test": "Lead Stage Update",
                    "endpoint": f"/api/odoo/crm/leads/{lead_id}/stage",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    
                    print(f"✅ Lead Stage Updated Successfully")
                    print(f"   Lead ID: {lead_id}")
                    print(f"   New Stage: {stage_data['stage_name']}")
                    print(f"   Status: {data.get('message', 'Updated')}")
                elif response.status_code == 404:
                    result["warning"] = "Lead not found or stage not found"
                    print(f"⚠️ Lead stage update: {response.status_code} - Lead or stage not found (expected for empty database)")
                else:
                    result["error"] = response.text
                    print(f"❌ Lead stage update failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Lead Stage Update",
                "endpoint": f"/api/odoo/crm/leads/{lead_id}/stage",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Lead stage update test error: {e}")
            return result
    
    async def test_sales_analytics(self) -> Dict[str, Any]:
        """Test /api/odoo/crm/analytics endpoint"""
        print("\n📈 Testing Sales Analytics & Forecasting...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/crm/analytics?days=90",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "Sales Analytics & Forecasting",
                    "endpoint": "/api/odoo/crm/analytics",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    analytics = data.get("analytics", {})
                    
                    print(f"✅ Sales Analytics Retrieved")
                    print(f"   Total Opportunities: {analytics.get('total_opportunities', 0)}")
                    print(f"   Won Opportunities: {analytics.get('won_opportunities', 0)}")
                    print(f"   Total Revenue: ${analytics.get('total_revenue', 0)}")
                    print(f"   Conversion Rate: {analytics.get('conversion_rate', 0)}%")
                    print(f"   Average Deal Size: ${analytics.get('average_deal_size', 0)}")
                    print(f"   Pipeline Value: ${analytics.get('pipeline_value', 0)}")
                    print(f"   Analysis Period: {analytics.get('period_days', 90)} days")
                else:
                    result["error"] = response.text
                    print(f"❌ Sales analytics test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Sales Analytics & Forecasting",
                "endpoint": "/api/odoo/crm/analytics",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Sales analytics test error: {e}")
            return result
    
    async def test_sales_forecast(self) -> Dict[str, Any]:
        """Test /api/odoo/crm/forecast endpoint"""
        print("\n🔮 Testing Sales Forecasting...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/crm/forecast?months=6",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "Sales Forecasting",
                    "endpoint": "/api/odoo/crm/forecast",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    forecast = data.get("forecast", {})
                    
                    print(f"✅ Sales Forecast Generated")
                    print(f"   Forecast Period: {forecast.get('forecast_period_months', 6)} months")
                    print(f"   Total Opportunities: {forecast.get('total_opportunities', 0)}")
                    print(f"   Total Pipeline Value: ${forecast.get('total_pipeline_value', 0)}")
                    print(f"   Weighted Pipeline Value: ${forecast.get('weighted_pipeline_value', 0)}")
                    print(f"   Confidence Level: {forecast.get('confidence_level', 'unknown')}")
                    
                    monthly_forecast = forecast.get('monthly_forecast', {})
                    if monthly_forecast:
                        print("   Monthly Breakdown:")
                        for month, data in list(monthly_forecast.items())[:3]:  # Show first 3 months
                            print(f"   - {data.get('month', month)}: {data.get('opportunities', 0)} opps, ${data.get('weighted_value', 0):.2f}")
                else:
                    result["error"] = response.text
                    print(f"❌ Sales forecast test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Sales Forecasting",
                "endpoint": "/api/odoo/crm/forecast",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Sales forecast test error: {e}")
            return result
    
    async def test_customer_interactions(self) -> Dict[str, Any]:
        """Test /api/odoo/crm/customers/{customer_id}/interactions endpoint"""
        print("\n💬 Testing Customer Relationship Management...")
        
        # Use a test customer ID
        customer_id = 1  # Assume there's at least one customer for testing
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/crm/customers/{customer_id}/interactions",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "Customer Relationship Management",
                    "endpoint": f"/api/odoo/crm/customers/{customer_id}/interactions",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    interactions = data.get("interactions", [])
                    result["interaction_count"] = len(interactions)
                    
                    print(f"✅ Customer Interactions Retrieved")
                    print(f"   Customer ID: {customer_id}")
                    print(f"   Total Interactions: {len(interactions)}")
                    
                    if interactions:
                        print("   Recent Interactions:")
                        for i, interaction in enumerate(interactions[:3]):  # Show first 3
                            print(f"   - {interaction.get('type', 'unknown')}: {interaction.get('subject', 'No subject')} ({interaction.get('date', 'No date')})")
                    else:
                        print("   No interactions found (expected for new customer)")
                elif response.status_code == 404:
                    result["warning"] = "Customer not found"
                    print(f"⚠️ Customer interactions: Customer ID {customer_id} not found (expected for empty database)")
                else:
                    result["error"] = response.text
                    print(f"❌ Customer interactions test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Customer Relationship Management",
                "endpoint": f"/api/odoo/crm/customers/{customer_id}/interactions",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Customer interactions test error: {e}")
            return result
    
    async def test_customer_sync(self) -> Dict[str, Any]:
        """Test /api/odoo/crm/customers/sync endpoint"""
        print("\n🔄 Testing Customer Data Sync...")
        
        try:
            # Test data for customer sync
            customer_data = {
                "name": "Test Customer Sync",
                "email": "testsync@example.com",
                "phone": "+1-555-0188",
                "engagement_score": 85,
                "lifecycle_stage": "active"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/odoo/crm/customers/sync",
                    headers=self.get_headers(),
                    json=customer_data
                )
                
                result = {
                    "test": "Customer Data Sync",
                    "endpoint": "/api/odoo/crm/customers/sync",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    sync_result = data.get("sync_result", {})
                    
                    print(f"✅ Customer Data Sync Completed")
                    print(f"   Status: {data.get('status', 'unknown')}")
                    print(f"   Action: {sync_result.get('action', 'unknown')}")
                    print(f"   Partner ID: {sync_result.get('partner_id', 'N/A')}")
                    print(f"   Changes: {len(sync_result.get('changes', []))}")
                    
                    if sync_result.get('changes'):
                        print("   Sync Changes:")
                        for change in sync_result['changes'][:3]:  # Show first 3 changes
                            print(f"   - {change.get('field', 'unknown')}: {change.get('action', 'updated')}")
                else:
                    result["error"] = response.text
                    print(f"❌ Customer sync test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Customer Data Sync",
                "endpoint": "/api/odoo/crm/customers/sync",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Customer sync test error: {e}")
            return result
    
    async def test_crm_dashboard(self) -> Dict[str, Any]:
        """Test /api/odoo/crm/dashboard endpoint"""
        print("\n📋 Testing CRM Dashboard...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/crm/dashboard",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "CRM Dashboard",
                    "endpoint": "/api/odoo/crm/dashboard",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    dashboard = data.get("dashboard", {})
                    
                    print(f"✅ CRM Dashboard Retrieved")
                    
                    # Overview metrics
                    overview = dashboard.get("overview", {})
                    print(f"   📊 Overview:")
                    print(f"   - Total Opportunities: {overview.get('total_opportunities', 0)}")
                    print(f"   - Total Pipeline Value: ${overview.get('total_pipeline_value', 0)}")
                    print(f"   - Conversion Rate: {overview.get('conversion_rate', 0)}%")
                    print(f"   - Average Deal Size: ${overview.get('average_deal_size', 0)}")
                    
                    # Pipeline summary
                    pipeline_summary = dashboard.get("pipeline_summary", {})
                    stage_distribution = pipeline_summary.get("stage_distribution", {})
                    print(f"   🎯 Pipeline Summary:")
                    if stage_distribution:
                        for stage, count in stage_distribution.items():
                            print(f"   - {stage}: {count} opportunities")
                    else:
                        print("   - No pipeline stages found")
                    
                    # Analytics summary
                    analytics_summary = dashboard.get("analytics_summary", {})
                    forecast_summary = analytics_summary.get("forecast_summary", {})
                    print(f"   📈 Analytics Summary:")
                    print(f"   - Next 3 Months Forecast: ${forecast_summary.get('next_3_months', 0)}")
                    print(f"   - Forecast Confidence: {forecast_summary.get('confidence', 'unknown')}")
                    
                else:
                    result["error"] = response.text
                    print(f"❌ CRM dashboard test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "CRM Dashboard",
                "endpoint": "/api/odoo/crm/dashboard",
                "success": False,
                "error": str(e)
            }
            print(f"❌ CRM dashboard test error: {e}")
            return result
    
    async def test_integration_status_update(self) -> Dict[str, Any]:
        """Test /api/odoo/integration/status endpoint for Phase 2 features"""
        print("\n🔧 Testing Integration Status Update...")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/odoo/integration/status",
                    headers=self.get_headers()
                )
                
                result = {
                    "test": "Integration Status Update",
                    "endpoint": "/api/odoo/integration/status",
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    result["data"] = data
                    
                    connection = data.get("connection", {})
                    statistics = data.get("statistics", {})
                    features = data.get("features", {})
                    
                    print(f"✅ Integration Status Retrieved")
                    print(f"   🔗 Connection:")
                    print(f"   - Status: {connection.get('status', 'unknown')}")
                    print(f"   - Connected: {connection.get('connected', False)}")
                    print(f"   - Database: {connection.get('database', 'N/A')}")
                    
                    print(f"   📊 Statistics:")
                    print(f"   - Email Templates: {statistics.get('email_templates', 0)}")
                    print(f"   - Customers Available: {statistics.get('customers_available', 0)}")
                    print(f"   - Campaigns (30 days): {statistics.get('campaigns_last_30_days', 0)}")
                    
                    print(f"   🚀 Phase 2 Features:")
                    phase2_features = [
                        'sales_pipeline_management',
                        'sales_analytics_forecasting', 
                        'customer_relationship_management',
                        'crm_dashboard'
                    ]
                    
                    for feature in phase2_features:
                        status = features.get(feature, False)
                        print(f"   - {feature.replace('_', ' ').title()}: {'✅' if status else '❌'}")
                    
                    # Check if Phase 2 features are properly reported
                    phase2_count = sum(1 for f in phase2_features if features.get(f, False))
                    result["phase2_features_active"] = phase2_count
                    
                else:
                    result["error"] = response.text
                    print(f"❌ Integration status test failed: {response.status_code} - {response.text}")
                
                return result
                
        except Exception as e:
            result = {
                "test": "Integration Status Update",
                "endpoint": "/api/odoo/integration/status",
                "success": False,
                "error": str(e)
            }
            print(f"❌ Integration status test error: {e}")
            return result
    
    async def run_all_tests(self):
        """Run all Phase 2 Enhanced CRM tests"""
        print("🚀 Starting Phase 2 Enhanced CRM Features Backend Testing")
        print("=" * 70)
        
        # Authenticate first
        if not await self.authenticate():
            print("❌ Authentication failed - cannot proceed with tests")
            return
        
        # Run all CRM tests
        tests = [
            self.test_sales_pipeline(),
            self.test_create_lead(),
            self.test_update_lead_stage(),
            self.test_sales_analytics(),
            self.test_sales_forecast(),
            self.test_customer_interactions(),
            self.test_customer_sync(),
            self.test_crm_dashboard(),
            self.test_integration_status_update()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Process results
        successful_tests = 0
        total_tests = len(results)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.test_results.append({
                    "test": f"Test {i+1}",
                    "success": False,
                    "error": str(result)
                })
            else:
                self.test_results.append(result)
                if result.get("success", False):
                    successful_tests += 1
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 Phase 2 Enhanced CRM Testing Summary")
        print("=" * 70)
        
        success_rate = (successful_tests / total_tests) * 100
        print(f"✅ Tests Passed: {successful_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if successful_tests == total_tests:
            print("🎉 All Phase 2 CRM features are working perfectly!")
        elif successful_tests > total_tests * 0.7:
            print("⚠️ Most CRM features working - minor issues detected")
        else:
            print("❌ Multiple CRM feature failures - requires investigation")
        
        # Detailed results
        print("\n📋 Detailed Test Results:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅ PASS" if result.get("success") else "❌ FAIL"
            test_name = result.get("test", f"Test {i}")
            print(f"{i}. {status} - {test_name}")
            
            if not result.get("success") and result.get("error"):
                print(f"   Error: {result['error']}")
        
        # Key findings for Phase 2 CRM
        print("\n🔍 Phase 2 CRM Key Findings:")
        
        # Sales Pipeline Management
        pipeline_test = next((r for r in self.test_results if "Pipeline" in r.get("test", "")), None)
        if pipeline_test and pipeline_test.get("success"):
            pipeline_count = pipeline_test.get("pipeline_count", 0)
            print(f"✅ Sales Pipeline Management: {pipeline_count} opportunities retrieved")
        else:
            print("❌ Sales Pipeline Management has issues")
        
        # Lead Management
        lead_tests = [r for r in self.test_results if "Lead" in r.get("test", "")]
        lead_success = sum(1 for r in lead_tests if r.get("success"))
        if lead_success == len(lead_tests) and lead_tests:
            print("✅ Lead Management (Create/Update) fully functional")
        elif lead_success > 0:
            print("⚠️ Lead Management partially working")
        else:
            print("❌ Lead Management has issues")
        
        # Analytics & Forecasting
        analytics_tests = [r for r in self.test_results if "Analytics" in r.get("test", "") or "Forecast" in r.get("test", "")]
        analytics_success = sum(1 for r in analytics_tests if r.get("success"))
        if analytics_success == len(analytics_tests) and analytics_tests:
            print("✅ Sales Analytics & Forecasting fully operational")
        elif analytics_success > 0:
            print("⚠️ Sales Analytics & Forecasting partially working")
        else:
            print("❌ Sales Analytics & Forecasting has issues")
        
        # Customer Relationship Management
        crm_tests = [r for r in self.test_results if "Customer" in r.get("test", "") or "CRM" in r.get("test", "")]
        crm_success = sum(1 for r in crm_tests if r.get("success"))
        if crm_success == len(crm_tests) and crm_tests:
            print("✅ Customer Relationship Management fully functional")
        elif crm_success > 0:
            print("⚠️ Customer Relationship Management partially working")
        else:
            print("❌ Customer Relationship Management has issues")
        
        # Integration Status
        integration_test = next((r for r in self.test_results if "Integration" in r.get("test", "")), None)
        if integration_test and integration_test.get("success"):
            phase2_features = integration_test.get("phase2_features_active", 0)
            print(f"✅ Integration Status: {phase2_features}/4 Phase 2 features active")
        else:
            print("❌ Integration Status reporting has issues")
        
        print("\n" + "=" * 70)
        print("🏁 Phase 2 Enhanced CRM Testing Complete")
        print("=" * 70)

async def main():
    """Main test execution"""
    tester = Phase2CRMTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())