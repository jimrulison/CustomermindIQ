#!/usr/bin/env python3
"""
AI-Powered Analytics & Real-Time Reporting System Backend Test
Testing comprehensive AI analytics system with intelligent insights, real-time metrics, 
performance predictions, and advanced reporting for affiliate performance.
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Test Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customeriq-hub.preview.emergentagent.com")
BASE_URL = f"{BACKEND_URL}/api"

# Test Data
TEST_AFFILIATE_ID = "test_affiliate_analytics_001"
TEST_SITE_ID = "test_site_001"

class AIAnalyticsBackendTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    async def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        result = {
            "test": test_name,
            "status": "✅ PASS" if success else "❌ FAIL",
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        if response_data and isinstance(response_data, dict):
            result["response_size"] = len(str(response_data))
            
        self.test_results.append(result)
        print(f"{result['status']} {test_name}: {details}")
        
    async def test_ai_insights_generation(self):
        """Test AI-powered insights generation endpoint"""
        try:
            # Test with different timeframes
            timeframes = [1, 24, 168]  # 1h, 24h, 7d
            
            for timeframe in timeframes:
                url = f"{BASE_URL}/v3/analytics/insights/{TEST_AFFILIATE_ID}?timeframe_hours={timeframe}"
                response = await self.client.post(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate response structure
                    required_fields = ["success", "affiliate_id", "timeframe_hours", "insights_count", "insights"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        await self.log_test(
                            f"AI Insights Generation ({timeframe}h)",
                            False,
                            f"Missing fields: {missing_fields}"
                        )
                        continue
                    
                    # Validate insights structure
                    insights = data.get("insights", [])
                    if insights:
                        insight = insights[0]
                        insight_fields = ["insight_id", "affiliate_id", "insight_type", "severity", "title", "description", "confidence_score"]
                        missing_insight_fields = [field for field in insight_fields if field not in insight]
                        
                        if missing_insight_fields:
                            await self.log_test(
                                f"AI Insights Generation ({timeframe}h)",
                                False,
                                f"Missing insight fields: {missing_insight_fields}"
                            )
                            continue
                    
                    await self.log_test(
                        f"AI Insights Generation ({timeframe}h)",
                        True,
                        f"Generated {data['insights_count']} insights with proper structure",
                        data
                    )
                else:
                    await self.log_test(
                        f"AI Insights Generation ({timeframe}h)",
                        False,
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
        except Exception as e:
            await self.log_test("AI Insights Generation", False, f"Exception: {str(e)}")
    
    async def test_real_time_metrics(self):
        """Test real-time metrics retrieval"""
        try:
            # Test without site_id (all sites)
            url = f"{BASE_URL}/v3/analytics/real-time/{TEST_AFFILIATE_ID}"
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    await self.log_test(
                        "Real-Time Metrics (All Sites)",
                        True,
                        f"Retrieved metrics: {len(data.get('metrics', {}))} sites",
                        data
                    )
                else:
                    await self.log_test(
                        "Real-Time Metrics (All Sites)",
                        False,
                        f"API returned success=false: {data}"
                    )
            else:
                await self.log_test(
                    "Real-Time Metrics (All Sites)",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
            
            # Test with specific site_id
            url = f"{BASE_URL}/v3/analytics/real-time/{TEST_AFFILIATE_ID}?site_id={TEST_SITE_ID}"
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    await self.log_test(
                        "Real-Time Metrics (Specific Site)",
                        True,
                        f"Retrieved site-specific metrics",
                        data
                    )
                else:
                    await self.log_test(
                        "Real-Time Metrics (Specific Site)",
                        False,
                        f"API returned success=false: {data}"
                    )
            else:
                await self.log_test(
                    "Real-Time Metrics (Specific Site)",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            await self.log_test("Real-Time Metrics", False, f"Exception: {str(e)}")
    
    async def test_event_tracking(self):
        """Test analytics event tracking"""
        try:
            # Test click event - using query parameters as expected by API
            url = f"{BASE_URL}/v3/analytics/event?affiliate_id={TEST_AFFILIATE_ID}&site_id={TEST_SITE_ID}&event_type=click"
            event_data = {
                "source": "test",
                "campaign": "analytics_test",
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.client.post(url, json=event_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    await self.log_test(
                        "Event Tracking (Click)",
                        True,
                        f"Click event tracked successfully",
                        data
                    )
                else:
                    await self.log_test(
                        "Event Tracking (Click)",
                        False,
                        f"API returned success=false: {data}"
                    )
            else:
                await self.log_test(
                    "Event Tracking (Click)",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
            
            # Wait a moment for processing
            await asyncio.sleep(1)
            
            # Test conversion event
            url = f"{BASE_URL}/v3/analytics/event?affiliate_id={TEST_AFFILIATE_ID}&site_id={TEST_SITE_ID}&event_type=conversion"
            conversion_data = {
                "value": 99.99,
                "order_id": "test_order_001",
                "customer_id": "test_customer_001",
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.client.post(url, json=conversion_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    await self.log_test(
                        "Event Tracking (Conversion)",
                        True,
                        f"Conversion event tracked successfully",
                        data
                    )
                else:
                    await self.log_test(
                        "Event Tracking (Conversion)",
                        False,
                        f"API returned success=false: {data}"
                    )
            else:
                await self.log_test(
                    "Event Tracking (Conversion)",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
            
            # Test email open event
            email_data = {
                "affiliate_id": TEST_AFFILIATE_ID,
                "site_id": TEST_SITE_ID,
                "event_type": "email_open",
                "event_data": {
                    "email": "test@example.com",
                    "campaign_id": "email_campaign_001",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            response = await self.client.post(url, json=email_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    await self.log_test(
                        "Event Tracking (Email Open)",
                        True,
                        f"Email open event tracked successfully",
                        data
                    )
                else:
                    await self.log_test(
                        "Event Tracking (Email Open)",
                        False,
                        f"API returned success=false: {data}"
                    )
            else:
                await self.log_test(
                    "Event Tracking (Email Open)",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            await self.log_test("Event Tracking", False, f"Exception: {str(e)}")
    
    async def test_performance_predictions(self):
        """Test performance predictions endpoint"""
        try:
            # Test with different forecast periods
            forecast_periods = [7, 14, 30]
            
            for days in forecast_periods:
                url = f"{BASE_URL}/v3/analytics/predictions/{TEST_AFFILIATE_ID}?forecast_days={days}"
                response = await self.client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        # Validate prediction structure
                        predictions = data.get("predictions", [])
                        summary = data.get("summary", {})
                        
                        required_summary_fields = ["total_predicted_revenue", "total_predicted_conversions", "average_daily_revenue"]
                        missing_summary_fields = [field for field in required_summary_fields if field not in summary]
                        
                        if missing_summary_fields:
                            await self.log_test(
                                f"Performance Predictions ({days}d)",
                                False,
                                f"Missing summary fields: {missing_summary_fields}"
                            )
                            continue
                        
                        if predictions:
                            prediction = predictions[0]
                            prediction_fields = ["prediction_id", "affiliate_id", "forecast_date", "predicted_clicks", "predicted_conversions", "predicted_revenue"]
                            missing_prediction_fields = [field for field in prediction_fields if field not in prediction]
                            
                            if missing_prediction_fields:
                                await self.log_test(
                                    f"Performance Predictions ({days}d)",
                                    False,
                                    f"Missing prediction fields: {missing_prediction_fields}"
                                )
                                continue
                        
                        await self.log_test(
                            f"Performance Predictions ({days}d)",
                            True,
                            f"Generated {len(predictions)} predictions, total predicted revenue: ${summary.get('total_predicted_revenue', 0):.2f}",
                            data
                        )
                    else:
                        await self.log_test(
                            f"Performance Predictions ({days}d)",
                            False,
                            f"API returned success=false: {data.get('error', 'Unknown error')}"
                        )
                else:
                    await self.log_test(
                        f"Performance Predictions ({days}d)",
                        False,
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
        except Exception as e:
            await self.log_test("Performance Predictions", False, f"Exception: {str(e)}")
    
    async def test_alerts_system(self):
        """Test real-time alerts retrieval"""
        try:
            # Test with different time ranges
            time_ranges = [1, 24, 168]  # 1h, 24h, 7d
            
            for hours in time_ranges:
                url = f"{BASE_URL}/v3/analytics/alerts/{TEST_AFFILIATE_ID}?hours_back={hours}"
                response = await self.client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        # Validate alerts structure
                        alerts = data.get("alerts", [])
                        alerts_count = data.get("alerts_count", 0)
                        
                        await self.log_test(
                            f"Recent Alerts ({hours}h)",
                            True,
                            f"Retrieved {alerts_count} alerts",
                            data
                        )
                    else:
                        await self.log_test(
                            f"Recent Alerts ({hours}h)",
                            False,
                            f"API returned success=false: {data}"
                        )
                else:
                    await self.log_test(
                        f"Recent Alerts ({hours}h)",
                        False,
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
        except Exception as e:
            await self.log_test("Recent Alerts", False, f"Exception: {str(e)}")
    
    async def test_dashboard_integration(self):
        """Test comprehensive dashboard API"""
        try:
            # Test with different timeframes
            timeframes = ["1h", "1d", "7d", "30d"]
            
            for timeframe in timeframes:
                url = f"{BASE_URL}/v3/analytics/dashboard/{TEST_AFFILIATE_ID}?timeframe={timeframe}"
                response = await self.client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        dashboard = data.get("dashboard", {})
                        
                        # Validate dashboard structure
                        required_sections = ["real_time_summary", "insights_summary", "alerts_summary", "performance_indicators"]
                        missing_sections = [section for section in required_sections if section not in dashboard]
                        
                        if missing_sections:
                            await self.log_test(
                                f"Dashboard Integration ({timeframe})",
                                False,
                                f"Missing dashboard sections: {missing_sections}"
                            )
                            continue
                        
                        # Validate real-time summary
                        rt_summary = dashboard.get("real_time_summary", {})
                        rt_fields = ["total_sites", "total_clicks_24h", "total_conversions_24h", "total_revenue_24h"]
                        missing_rt_fields = [field for field in rt_fields if field not in rt_summary]
                        
                        if missing_rt_fields:
                            await self.log_test(
                                f"Dashboard Integration ({timeframe})",
                                False,
                                f"Missing real-time summary fields: {missing_rt_fields}"
                            )
                            continue
                        
                        await self.log_test(
                            f"Dashboard Integration ({timeframe})",
                            True,
                            f"Dashboard loaded with {rt_summary.get('total_sites', 0)} sites, "
                            f"{rt_summary.get('total_clicks_24h', 0)} clicks, "
                            f"${rt_summary.get('total_revenue_24h', 0):.2f} revenue",
                            data
                        )
                    else:
                        await self.log_test(
                            f"Dashboard Integration ({timeframe})",
                            False,
                            f"API returned success=false: {data}"
                        )
                else:
                    await self.log_test(
                        f"Dashboard Integration ({timeframe})",
                        False,
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
        except Exception as e:
            await self.log_test("Dashboard Integration", False, f"Exception: {str(e)}")
    
    async def test_system_health(self):
        """Test system health check"""
        try:
            url = f"{BASE_URL}/v3/analytics/health"
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate health check structure
                required_fields = ["status", "components", "features"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    await self.log_test(
                        "System Health Check",
                        False,
                        f"Missing health check fields: {missing_fields}"
                    )
                    return
                
                # Check components
                components = data.get("components", {})
                expected_components = ["redis", "mongodb", "ai_engine", "real_time_analytics"]
                missing_components = [comp for comp in expected_components if comp not in components]
                
                if missing_components:
                    await self.log_test(
                        "System Health Check",
                        False,
                        f"Missing components: {missing_components}"
                    )
                    return
                
                # Check features
                features = data.get("features", [])
                expected_features = ["ai_powered_insights", "real_time_metrics", "performance_predictions", "anomaly_detection"]
                missing_features = [feat for feat in expected_features if feat not in features]
                
                if missing_features:
                    await self.log_test(
                        "System Health Check",
                        False,
                        f"Missing features: {missing_features}"
                    )
                    return
                
                # Check overall status
                overall_status = data.get("status")
                healthy_components = sum(1 for status in components.values() if status == "healthy")
                
                await self.log_test(
                    "System Health Check",
                    True,
                    f"Status: {overall_status}, {healthy_components}/{len(components)} components healthy, {len(features)} features available",
                    data
                )
            else:
                await self.log_test(
                    "System Health Check",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            await self.log_test("System Health Check", False, f"Exception: {str(e)}")
    
    async def test_integration_with_tracking(self):
        """Test integration with advanced tracking system"""
        try:
            # First, create some tracking events to ensure integration
            tracking_url = f"{BASE_URL}/v2/track/click"
            tracking_data = {
                "affiliate_id": TEST_AFFILIATE_ID,
                "site_id": TEST_SITE_ID,
                "customer_identifier": "test_customer_analytics",
                "source_url": "https://test.example.com",
                "destination_url": "https://target.example.com",
                "campaign_id": "analytics_integration_test",
                "fingerprint_data": {
                    "screen_resolution": "1920x1080",
                    "timezone": "America/New_York",
                    "language": "en-US",
                    "platform": "Linux x86_64"
                }
            }
            
            # Create click event
            response = await self.client.post(tracking_url, json=tracking_data)
            
            if response.status_code == 200:
                click_data = response.json()
                tracking_id = click_data.get("tracking_id")
                
                if tracking_id:
                    # Wait for processing
                    await asyncio.sleep(2)
                    
                    # Check if analytics picked up the event
                    analytics_url = f"{BASE_URL}/v3/analytics/real-time/{TEST_AFFILIATE_ID}?site_id={TEST_SITE_ID}"
                    analytics_response = await self.client.get(analytics_url)
                    
                    if analytics_response.status_code == 200:
                        analytics_data = analytics_response.json()
                        
                        if analytics_data.get("success"):
                            metrics = analytics_data.get("metrics")
                            
                            # Check if metrics were updated
                            if metrics and (metrics.get("clicks_1h", 0) > 0 or metrics.get("clicks_24h", 0) > 0):
                                await self.log_test(
                                    "Integration with Tracking System",
                                    True,
                                    f"Tracking event successfully integrated into analytics (tracking_id: {tracking_id})",
                                    analytics_data
                                )
                            else:
                                await self.log_test(
                                    "Integration with Tracking System",
                                    False,
                                    f"Analytics did not reflect tracking event (tracking_id: {tracking_id})"
                                )
                        else:
                            await self.log_test(
                                "Integration with Tracking System",
                                False,
                                f"Analytics API returned success=false: {analytics_data}"
                            )
                    else:
                        await self.log_test(
                            "Integration with Tracking System",
                            False,
                            f"Analytics API error: HTTP {analytics_response.status_code}"
                        )
                else:
                    await self.log_test(
                        "Integration with Tracking System",
                        False,
                        f"Tracking API did not return tracking_id: {click_data}"
                    )
            else:
                await self.log_test(
                    "Integration with Tracking System",
                    False,
                    f"Tracking API error: HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            await self.log_test("Integration with Tracking System", False, f"Exception: {str(e)}")
    
    async def run_comprehensive_test(self):
        """Run all AI Analytics tests"""
        print("🚀 Starting AI-Powered Analytics & Real-Time Reporting System Backend Tests")
        print(f"🎯 Testing against: {BACKEND_URL}")
        print(f"📊 Test Affiliate ID: {TEST_AFFILIATE_ID}")
        print("=" * 80)
        
        # Run all test categories
        await self.test_system_health()
        await self.test_event_tracking()
        await self.test_real_time_metrics()
        await self.test_ai_insights_generation()
        await self.test_performance_predictions()
        await self.test_alerts_system()
        await self.test_dashboard_integration()
        await self.test_integration_with_tracking()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📋 AI ANALYTICS BACKEND TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"✅ Passed: {self.passed_tests}/{self.total_tests} ({success_rate:.1f}%)")
        print(f"❌ Failed: {self.total_tests - self.passed_tests}/{self.total_tests}")
        
        # Group results by category
        categories = {}
        for result in self.test_results:
            test_name = result["test"]
            category = test_name.split("(")[0].strip() if "(" in test_name else test_name
            
            if category not in categories:
                categories[category] = {"passed": 0, "total": 0, "tests": []}
            
            categories[category]["total"] += 1
            categories[category]["tests"].append(result)
            
            if result["status"] == "✅ PASS":
                categories[category]["passed"] += 1
        
        print("\n📊 DETAILED RESULTS BY CATEGORY:")
        for category, stats in categories.items():
            category_success_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"\n🔸 {category}: {stats['passed']}/{stats['total']} ({category_success_rate:.1f}%)")
            
            for test in stats["tests"]:
                print(f"   {test['status']} {test['test']}: {test['details']}")
        
        # Overall assessment
        print(f"\n🎯 OVERALL ASSESSMENT:")
        if success_rate >= 90:
            print("🟢 EXCELLENT: AI Analytics system is working perfectly")
        elif success_rate >= 75:
            print("🟡 GOOD: AI Analytics system is mostly functional with minor issues")
        elif success_rate >= 50:
            print("🟠 FAIR: AI Analytics system has significant issues that need attention")
        else:
            print("🔴 POOR: AI Analytics system has critical issues requiring immediate fixes")
        
        print(f"\n⏰ Test completed at: {datetime.now().isoformat()}")
        
        await self.client.aclose()
        
        return success_rate

async def main():
    """Main test execution"""
    tester = AIAnalyticsBackendTester()
    success_rate = await tester.run_comprehensive_test()
    
    # Exit with appropriate code
    exit_code = 0 if success_rate >= 75 else 1
    exit(exit_code)

if __name__ == "__main__":
    asyncio.run(main())