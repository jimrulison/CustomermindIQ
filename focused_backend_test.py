#!/usr/bin/env python3
"""
Focused Backend API Testing for Universal Customer Intelligence SaaS Platform
Testing the specific modules mentioned in the review request:
1. Marketing Automation Pro endpoints (17 endpoints)
2. Advanced Features Expansion endpoints (13 endpoints) 
3. Revenue Analytics Suite endpoints (17 endpoints)
4. Universal Platform endpoints (7 endpoints)
5. Core Customer Intelligence endpoints
"""

import requests
import json
from datetime import datetime
import time

class FocusedBackendTester:
    def __init__(self, base_url="https://growth-engine-app-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.results = {
            'marketing_automation_pro': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'advanced_features': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'revenue_analytics': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'universal_platform': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'core_intelligence': {'total': 0, 'passed': 0, 'failed': 0, 'details': []}
        }

    def test_endpoint(self, module, name, method, endpoint, expected_status=200, data=None, timeout=30):
        """Test a single endpoint and record results"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.results[module]['total'] += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.results[module]['passed'] += 1
                print(f"✅ PASSED - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    # Show key metrics from response
                    if 'dashboard' in response_data:
                        dashboard = response_data['dashboard']
                        if isinstance(dashboard, dict):
                            for key, value in list(dashboard.items())[:3]:
                                if isinstance(value, dict) and 'total' in str(value):
                                    print(f"   📊 {key}: {value}")
                                elif isinstance(value, (int, float)):
                                    print(f"   📊 {key}: {value}")
                    elif 'status' in response_data:
                        print(f"   📊 Status: {response_data['status']}")
                    
                    self.results[module]['details'].append({
                        'name': name,
                        'status': 'PASSED',
                        'response_code': response.status_code,
                        'has_data': bool(response_data)
                    })
                    return True, response_data
                except:
                    self.results[module]['details'].append({
                        'name': name,
                        'status': 'PASSED',
                        'response_code': response.status_code,
                        'has_data': False
                    })
                    return True, {}
            else:
                self.results[module]['failed'] += 1
                print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                
                self.results[module]['details'].append({
                    'name': name,
                    'status': 'FAILED',
                    'response_code': response.status_code,
                    'error': response.text[:200]
                })
                return False, {}

        except requests.exceptions.Timeout:
            self.results[module]['failed'] += 1
            print(f"❌ FAILED - Request timed out after {timeout} seconds")
            self.results[module]['details'].append({
                'name': name,
                'status': 'TIMEOUT',
                'error': f'Timeout after {timeout}s'
            })
            return False, {}
        except Exception as e:
            self.results[module]['failed'] += 1
            print(f"❌ FAILED - Error: {str(e)}")
            self.results[module]['details'].append({
                'name': name,
                'status': 'ERROR',
                'error': str(e)
            })
            return False, {}

    def test_marketing_automation_pro(self):
        """Test Marketing Automation Pro endpoints (17 endpoints total)"""
        print("\n" + "="*80)
        print("🚀 TESTING MARKETING AUTOMATION PRO MODULE (17 ENDPOINTS)")
        print("="*80)
        
        # Multi-Channel Orchestration (4 endpoints)
        print("\n📢 Multi-Channel Orchestration (4 endpoints)")
        self.test_endpoint('marketing_automation_pro', 'Multi-Channel Dashboard', 'GET', 'api/marketing/multi-channel-orchestration')
        
        campaign_data = {
            "name": "Test Campaign",
            "target_audience": {"segment": "high_value"},
            "channels": ["email", "sms"],
            "budget": 1000
        }
        self.test_endpoint('marketing_automation_pro', 'Create Campaign', 'POST', 'api/marketing/multi-channel-orchestration/campaigns', data=campaign_data)
        self.test_endpoint('marketing_automation_pro', 'Execute Campaign', 'POST', 'api/marketing/multi-channel-orchestration/campaigns/test_123/execute')
        
        sms_data = {"customer_id": "test", "phone_number": "+1234567890", "message": "Test"}
        self.test_endpoint('marketing_automation_pro', 'Send SMS', 'POST', 'api/marketing/multi-channel-orchestration/sms', data=sms_data)
        
        # A/B Testing (4 endpoints)
        print("\n🧪 A/B Testing (4 endpoints)")
        self.test_endpoint('marketing_automation_pro', 'A/B Testing Dashboard', 'GET', 'api/marketing/ab-testing')
        
        ab_test_data = {
            "test_name": "Test AB",
            "test_type": "email",
            "variants": [{"name": "A", "content": "Version A"}],
            "use_multi_armed_bandit": True
        }
        self.test_endpoint('marketing_automation_pro', 'Create A/B Test', 'POST', 'api/marketing/ab-testing/tests', data=ab_test_data)
        self.test_endpoint('marketing_automation_pro', 'Get Optimal Variant', 'GET', 'api/marketing/ab-testing/tests/test_123/variant')
        
        event_data = {"variant_id": "v1", "event_type": "click", "value": 1.0}
        self.test_endpoint('marketing_automation_pro', 'Record Event', 'POST', 'api/marketing/ab-testing/tests/test_123/events', data=event_data)
        
        # Dynamic Content (4 endpoints)
        print("\n🎨 Dynamic Content (4 endpoints)")
        self.test_endpoint('marketing_automation_pro', 'Dynamic Content Dashboard', 'GET', 'api/marketing/dynamic-content')
        
        behavior_data = {"customer_id": "test", "event_type": "page_view", "page_url": "/test"}
        self.test_endpoint('marketing_automation_pro', 'Track Behavior', 'POST', 'api/marketing/dynamic-content/behavior/track', data=behavior_data)
        
        template_data = {"template_name": "Test Template", "template_type": "email", "base_content": "Hello {{name}}"}
        self.test_endpoint('marketing_automation_pro', 'Create Template', 'POST', 'api/marketing/dynamic-content/templates', data=template_data)
        self.test_endpoint('marketing_automation_pro', 'Get Recommendations', 'GET', 'api/marketing/dynamic-content/recommendations/test_customer')
        
        # Lead Scoring (3 endpoints)
        print("\n🎯 Lead Scoring (3 endpoints)")
        self.test_endpoint('marketing_automation_pro', 'Lead Scoring Dashboard', 'GET', 'api/marketing/lead-scoring')
        
        activity_data = {"lead_id": "test", "activity_type": "email_open", "details": {"campaign": "test"}}
        self.test_endpoint('marketing_automation_pro', 'Track Activity', 'POST', 'api/marketing/lead-scoring/activity/track', data=activity_data)
        
        lead_data = {"company_info": {"size": "50-200"}, "contact_info": {"title": "Manager"}}
        self.test_endpoint('marketing_automation_pro', 'Calculate Score', 'POST', 'api/marketing/lead-scoring/score/test_lead', data=lead_data)
        
        # Referral Program (4 endpoints)
        print("\n🤝 Referral Program (4 endpoints)")
        self.test_endpoint('marketing_automation_pro', 'Referral Dashboard', 'GET', 'api/marketing/referral-program')
        self.test_endpoint('marketing_automation_pro', 'Analyze Propensity', 'GET', 'api/marketing/referral-program/analyze/test_customer')
        
        campaign_data = {"name": "Test Referral", "reward_type": "discount", "reward_value": 20}
        self.test_endpoint('marketing_automation_pro', 'Create Referral Campaign', 'POST', 'api/marketing/referral-program/campaigns', data=campaign_data)
        self.test_endpoint('marketing_automation_pro', 'Get Viral Metrics', 'GET', 'api/marketing/referral-program/viral-metrics/test_program')
        
        # Marketing Dashboard (1 aggregation endpoint)
        print("\n📊 Marketing Dashboard (1 endpoint)")
        self.test_endpoint('marketing_automation_pro', 'Marketing Dashboard Aggregation', 'GET', 'api/marketing/dashboard')

    def test_advanced_features_expansion(self):
        """Test Advanced Features Expansion endpoints (13 endpoints total)"""
        print("\n" + "="*80)
        print("🧠 TESTING ADVANCED FEATURES EXPANSION MODULE (13 ENDPOINTS)")
        print("="*80)
        
        # Behavioral Clustering (2 endpoints)
        print("\n🎯 Behavioral Clustering (2 endpoints)")
        self.test_endpoint('advanced_features', 'Behavioral Clustering Dashboard', 'GET', 'api/advanced/behavioral-clustering')
        
        customer_data = {
            "customer_id": "test_customer",
            "purchase_history": [{"product": "Software A", "amount": 100}],
            "last_purchase_date": "2024-01-15"
        }
        self.test_endpoint('advanced_features', 'Analyze Customer Behavior', 'POST', 'api/advanced/behavioral-clustering/analyze', data=customer_data)
        
        # Churn Prevention AI (2 endpoints)
        print("\n🚨 Churn Prevention AI (2 endpoints)")
        self.test_endpoint('advanced_features', 'Churn Prevention Dashboard', 'GET', 'api/advanced/churn-prevention')
        
        churn_data = {
            "customer_id": "test_customer",
            "engagement_metrics": {"email_opens": 5, "last_login": "2024-01-10"},
            "usage_patterns": {"feature_usage": 0.3, "support_tickets": 2}
        }
        self.test_endpoint('advanced_features', 'Predict Churn', 'POST', 'api/advanced/churn-prevention/predict', data=churn_data)
        
        # Cross-Sell Intelligence (2 endpoints)
        print("\n💰 Cross-Sell Intelligence (2 endpoints)")
        self.test_endpoint('advanced_features', 'Cross-Sell Dashboard', 'GET', 'api/advanced/cross-sell-intelligence')
        
        cross_sell_data = {
            "customer_id": "test_customer",
            "current_products": ["Basic CRM"],
            "usage_data": {"monthly_usage": 150, "feature_adoption": 0.7}
        }
        self.test_endpoint('advanced_features', 'Get Recommendations', 'POST', 'api/advanced/cross-sell-intelligence/recommendations', data=cross_sell_data)
        
        # Advanced Pricing Optimization (2 endpoints)
        print("\n💲 Advanced Pricing Optimization (2 endpoints)")
        self.test_endpoint('advanced_features', 'Pricing Optimization Dashboard', 'GET', 'api/advanced/pricing-optimization')
        
        pricing_data = {
            "customer_id": "test_customer",
            "price_sensitivity_factors": {"budget": "medium", "competitor_prices": [99, 149, 199]},
            "purchase_history": {"avg_order_value": 150, "price_elasticity": 0.8}
        }
        self.test_endpoint('advanced_features', 'Analyze Price Sensitivity', 'POST', 'api/advanced/pricing-optimization/analyze', data=pricing_data)
        
        # Sentiment Analysis (2 endpoints)
        print("\n😊 Sentiment Analysis (2 endpoints)")
        self.test_endpoint('advanced_features', 'Sentiment Analysis Dashboard', 'GET', 'api/advanced/sentiment-analysis')
        
        sentiment_data = {
            "customer_id": "test_customer",
            "communication_text": "I love this software! It's amazing and the support team is fantastic. Very satisfied with my purchase.",
            "source": "email",
            "timestamp": datetime.now().isoformat()
        }
        self.test_endpoint('advanced_features', 'Analyze Communication', 'POST', 'api/advanced/sentiment-analysis/analyze', data=sentiment_data)
        
        # Advanced Dashboard (1 aggregation endpoint)
        print("\n📊 Advanced Dashboard (1 endpoint)")
        self.test_endpoint('advanced_features', 'Advanced Features Dashboard', 'GET', 'api/advanced/dashboard')

    def test_revenue_analytics_suite(self):
        """Test Revenue Analytics Suite endpoints (17 endpoints total)"""
        print("\n" + "="*80)
        print("💰 TESTING REVENUE ANALYTICS SUITE MODULE (17 ENDPOINTS)")
        print("="*80)
        
        # Revenue Forecasting (3 endpoints)
        print("\n📈 Revenue Forecasting (3 endpoints)")
        self.test_endpoint('revenue_analytics', 'Revenue Forecasting Dashboard', 'GET', 'api/revenue/forecasting')
        
        scenario_data = {
            "scenario_name": "Optimistic Growth",
            "assumptions": {"growth_rate": 0.15, "market_expansion": 0.1},
            "time_horizon": 12
        }
        self.test_endpoint('revenue_analytics', 'Create Scenario', 'POST', 'api/revenue/forecasting/scenarios', data=scenario_data)
        self.test_endpoint('revenue_analytics', 'Get Trends', 'GET', 'api/revenue/forecasting/trends')
        
        # Price Optimization (3 endpoints)
        print("\n💲 Price Optimization (3 endpoints)")
        self.test_endpoint('revenue_analytics', 'Price Optimization Dashboard', 'GET', 'api/revenue/price-optimization')
        
        simulation_data = {
            "product_id": "premium_software",
            "current_price": 199,
            "proposed_price": 249,
            "market_conditions": {"competition": "medium", "demand": "high"}
        }
        self.test_endpoint('revenue_analytics', 'Price Simulation', 'POST', 'api/revenue/price-optimization/simulate', data=simulation_data)
        self.test_endpoint('revenue_analytics', 'Competitive Analysis', 'GET', 'api/revenue/price-optimization/competitive-analysis')
        
        # Profit Margin Analysis (3 endpoints)
        print("\n📊 Profit Margin Analysis (3 endpoints)")
        self.test_endpoint('revenue_analytics', 'Profit Margin Dashboard', 'GET', 'api/revenue/profit-margin-analysis')
        
        cost_data = {
            "product_line": "enterprise_software",
            "cost_changes": {"development": -0.1, "marketing": 0.05, "support": 0.02}
        }
        self.test_endpoint('revenue_analytics', 'Cost Simulation', 'POST', 'api/revenue/profit-margin-analysis/cost-simulation', data=cost_data)
        self.test_endpoint('revenue_analytics', 'Industry Benchmarking', 'GET', 'api/revenue/profit-margin-analysis/benchmarking')
        
        # Subscription Analytics (3 endpoints)
        print("\n🔄 Subscription Analytics (3 endpoints)")
        self.test_endpoint('revenue_analytics', 'Subscription Dashboard', 'GET', 'api/revenue/subscription-analytics')
        
        churn_data = {"customer_id": "test_subscriber", "subscription_data": {"plan": "premium", "tenure": 12}}
        self.test_endpoint('revenue_analytics', 'Churn Prediction', 'POST', 'api/revenue/subscription-analytics/churn-prediction', data=churn_data)
        self.test_endpoint('revenue_analytics', 'Revenue Optimization', 'GET', 'api/revenue/subscription-analytics/revenue-optimization')
        
        # Financial Reporting (4 endpoints)
        print("\n📋 Financial Reporting (4 endpoints)")
        self.test_endpoint('revenue_analytics', 'Financial Dashboard', 'GET', 'api/revenue/financial-reporting')
        
        report_data = {
            "report_type": "monthly_summary",
            "date_range": {"start": "2024-01-01", "end": "2024-01-31"},
            "metrics": ["revenue", "costs", "profit"]
        }
        self.test_endpoint('revenue_analytics', 'Custom Report', 'POST', 'api/revenue/financial-reporting/custom-report', data=report_data)
        self.test_endpoint('revenue_analytics', 'KPI Dashboard', 'GET', 'api/revenue/financial-reporting/kpi-dashboard')
        self.test_endpoint('revenue_analytics', 'Variance Analysis', 'GET', 'api/revenue/financial-reporting/variance-analysis')
        
        # Revenue Dashboard (1 aggregation endpoint)
        print("\n📊 Revenue Dashboard (1 endpoint)")
        self.test_endpoint('revenue_analytics', 'Revenue Analytics Dashboard', 'GET', 'api/revenue/dashboard')

    def test_universal_platform(self):
        """Test Universal Platform endpoints (7 endpoints)"""
        print("\n" + "="*80)
        print("🌐 TESTING UNIVERSAL PLATFORM MODULE (7 ENDPOINTS)")
        print("="*80)
        
        self.test_endpoint('universal_platform', 'Connector Status', 'GET', 'api/universal/connectors/status')
        
        connector_data = {
            "platform_type": "stripe",
            "credentials": {"api_key": "sk_test_mock", "webhook_secret": "whsec_mock"}
        }
        self.test_endpoint('universal_platform', 'Add Connector', 'POST', 'api/universal/connectors/add', data=connector_data)
        self.test_endpoint('universal_platform', 'Sync Platforms', 'POST', 'api/universal/sync')
        self.test_endpoint('universal_platform', 'Unified Customers', 'GET', 'api/universal/customers')
        self.test_endpoint('universal_platform', 'Universal Intelligence', 'GET', 'api/universal/intelligence')
        self.test_endpoint('universal_platform', 'Universal Dashboard', 'GET', 'api/universal/dashboard')
        self.test_endpoint('universal_platform', 'Action Recommendations', 'GET', 'api/universal/recommendations')

    def test_core_intelligence(self):
        """Test Core Customer Intelligence endpoints"""
        print("\n" + "="*80)
        print("🧠 TESTING CORE CUSTOMER INTELLIGENCE MODULE")
        print("="*80)
        
        self.test_endpoint('core_intelligence', 'Health Check', 'GET', 'api/health')
        self.test_endpoint('core_intelligence', 'Get Customers', 'GET', 'api/customers', timeout=60)
        self.test_endpoint('core_intelligence', 'Customer Recommendations', 'GET', 'api/customers/demo_1/recommendations')
        self.test_endpoint('core_intelligence', 'Analytics Dashboard', 'GET', 'api/analytics')
        self.test_endpoint('core_intelligence', 'Get Campaigns', 'GET', 'api/campaigns')
        
        campaign_data = {
            "name": "Test Campaign",
            "target_segment": "active",
            "subject": "Test Subject",
            "content": "Test Content"
        }
        self.test_endpoint('core_intelligence', 'Create Campaign', 'POST', 'api/campaigns', data=campaign_data)

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE BACKEND API TEST SUMMARY")
        print("="*80)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for module, results in self.results.items():
            total_tests += results['total']
            total_passed += results['passed']
            total_failed += results['failed']
            
            if results['total'] > 0:
                success_rate = (results['passed'] / results['total']) * 100
                print(f"\n🔍 {module.upper().replace('_', ' ')}:")
                print(f"   Total: {results['total']} | Passed: {results['passed']} | Failed: {results['failed']}")
                print(f"   Success Rate: {success_rate:.1f}%")
                
                if results['failed'] > 0:
                    print(f"   ❌ Failed Tests:")
                    for detail in results['details']:
                        if detail['status'] in ['FAILED', 'TIMEOUT', 'ERROR']:
                            print(f"      - {detail['name']}: {detail['status']}")
        
        overall_success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n🎯 OVERALL RESULTS:")
        print(f"   Total Endpoints Tested: {total_tests}")
        print(f"   Endpoints Passed: {total_passed}")
        print(f"   Endpoints Failed: {total_failed}")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")
        
        if overall_success_rate >= 80:
            print(f"   ✅ EXCELLENT: Backend is production-ready!")
        elif overall_success_rate >= 60:
            print(f"   ⚠️  GOOD: Most endpoints working, minor issues to address")
        else:
            print(f"   ❌ NEEDS ATTENTION: Significant issues found")
        
        return {
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'success_rate': overall_success_rate,
            'module_results': self.results
        }

def main():
    print("🚀 UNIVERSAL CUSTOMER INTELLIGENCE SAAS PLATFORM - BACKEND API TESTING")
    print("="*80)
    print("Testing all modules mentioned in the review request:")
    print("1. Marketing Automation Pro endpoints (17 endpoints)")
    print("2. Advanced Features Expansion endpoints (13 endpoints)")
    print("3. Revenue Analytics Suite endpoints (17 endpoints)")
    print("4. Universal Platform endpoints (7 endpoints)")
    print("5. Core Customer Intelligence endpoints")
    print("="*80)
    
    tester = FocusedBackendTester()
    
    # Test all modules
    tester.test_marketing_automation_pro()
    tester.test_advanced_features_expansion()
    tester.test_revenue_analytics_suite()
    tester.test_universal_platform()
    tester.test_core_intelligence()
    
    # Print comprehensive summary
    results = tester.print_summary()
    
    return results

if __name__ == "__main__":
    main()