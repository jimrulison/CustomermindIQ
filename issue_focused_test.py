#!/usr/bin/env python3
"""
Issue-Focused Backend Testing for Specific Endpoint Problems
Testing the specific endpoints that had issues in the previous comprehensive test:

1. Revenue Forecasting routing issues - 3 endpoints returning 404 errors
2. A/B Testing validation error - test_type field validation issue
3. Cross-Sell Intelligence recommendations endpoint - 404 error  
4. Pricing Optimization analysis endpoint - routing problem
5. Sentiment Analysis communication validation - text field requirement issue
"""

import requests
import json
from datetime import datetime
import time

class IssueFocusedTester:
    def __init__(self, base_url="https://marketai-pro-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.issues_found = []
        self.fixes_needed = []

    def test_endpoint(self, name, method, endpoint, expected_status=200, data=None, timeout=30):
        """Test a single endpoint and record detailed results"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        print(f"\n🔍 Testing Issue: {name}")
        print(f"   URL: {url}")
        print(f"   Method: {method}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)

            print(f"   Response Status: {response.status_code}")
            
            if response.status_code == expected_status:
                print(f"✅ ISSUE RESOLVED - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:300]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ ISSUE CONFIRMED - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', 'Unknown error')
                    print(f"   Error Detail: {error_detail}")
                    
                    # Record the issue for analysis
                    self.issues_found.append({
                        'name': name,
                        'endpoint': endpoint,
                        'method': method,
                        'expected_status': expected_status,
                        'actual_status': response.status_code,
                        'error_detail': error_detail,
                        'data_sent': data
                    })
                    
                    return False, error_data
                except:
                    error_text = response.text[:500]
                    print(f"   Error Text: {error_text}")
                    
                    self.issues_found.append({
                        'name': name,
                        'endpoint': endpoint,
                        'method': method,
                        'expected_status': expected_status,
                        'actual_status': response.status_code,
                        'error_detail': error_text,
                        'data_sent': data
                    })
                    
                    return False, {'error': error_text}

        except requests.exceptions.Timeout:
            print(f"❌ TIMEOUT - Request timed out after {timeout} seconds")
            self.issues_found.append({
                'name': name,
                'endpoint': endpoint,
                'method': method,
                'error_detail': f'Timeout after {timeout} seconds',
                'data_sent': data
            })
            return False, {'error': 'timeout'}
            
        except Exception as e:
            print(f"❌ EXCEPTION - {str(e)}")
            self.issues_found.append({
                'name': name,
                'endpoint': endpoint,
                'method': method,
                'error_detail': str(e),
                'data_sent': data
            })
            return False, {'error': str(e)}

    def test_revenue_forecasting_issues(self):
        """Test the 3 Revenue Forecasting endpoints that were returning 404 errors"""
        print("\n" + "="*80)
        print("🎯 TESTING REVENUE FORECASTING ROUTING ISSUES")
        print("="*80)
        
        # Test 1: Revenue Forecasting Dashboard
        self.test_endpoint(
            "Revenue Forecasting Dashboard",
            "GET",
            "api/revenue/forecasting"
        )
        
        # Test 2: Revenue Forecasting Scenario Creation
        scenario_data = {
            "name": "Q1 Growth Scenario",
            "growth_rate": 0.15,
            "market_conditions": "optimistic",
            "time_horizon": "quarterly"
        }
        self.test_endpoint(
            "Revenue Forecasting Scenario Creation",
            "POST",
            "api/revenue/forecasting/scenarios",
            data=scenario_data
        )
        
        # Test 3: Revenue Forecasting Trends Analysis
        self.test_endpoint(
            "Revenue Forecasting Trends Analysis",
            "GET",
            "api/revenue/forecasting/trends"
        )

    def test_ab_testing_validation_issue(self):
        """Test the A/B Testing validation error for test_type field"""
        print("\n" + "="*80)
        print("🎯 TESTING A/B TESTING VALIDATION ISSUE")
        print("="*80)
        
        # Test with various test_type values to identify the validation issue
        test_cases = [
            {
                "name": "A/B Test with 'email' test_type",
                "data": {
                    "name": "Email Subject Test",
                    "test_type": "email",
                    "variants": [
                        {"name": "Control", "content": "Original subject"},
                        {"name": "Variant A", "content": "New subject"}
                    ]
                }
            },
            {
                "name": "A/B Test with 'landing_page' test_type",
                "data": {
                    "name": "Landing Page Test",
                    "test_type": "landing_page",
                    "variants": [
                        {"name": "Control", "content": "Original page"},
                        {"name": "Variant A", "content": "New page"}
                    ]
                }
            },
            {
                "name": "A/B Test with 'campaign' test_type",
                "data": {
                    "name": "Campaign Test",
                    "test_type": "campaign",
                    "variants": [
                        {"name": "Control", "content": "Original campaign"},
                        {"name": "Variant A", "content": "New campaign"}
                    ]
                }
            }
        ]
        
        for test_case in test_cases:
            self.test_endpoint(
                test_case["name"],
                "POST",
                "api/marketing/ab-testing/tests",
                data=test_case["data"]
            )

    def test_cross_sell_intelligence_issue(self):
        """Test the Cross-Sell Intelligence recommendations endpoint 404 error"""
        print("\n" + "="*80)
        print("🎯 TESTING CROSS-SELL INTELLIGENCE ROUTING ISSUE")
        print("="*80)
        
        # Test the recommendations endpoint that was returning 404
        customer_id = "demo_customer_123"
        self.test_endpoint(
            "Cross-Sell Intelligence Customer Recommendations",
            "GET",
            f"api/advanced/cross-sell-intelligence/recommendations/{customer_id}"
        )
        
        # Also test the dashboard to see if the module is working
        self.test_endpoint(
            "Cross-Sell Intelligence Dashboard",
            "GET",
            "api/advanced/cross-sell-intelligence"
        )

    def test_pricing_optimization_routing_issue(self):
        """Test the Advanced Pricing Optimization analysis endpoint routing problem"""
        print("\n" + "="*80)
        print("🎯 TESTING PRICING OPTIMIZATION ROUTING ISSUE")
        print("="*80)
        
        # Test the analysis endpoint that had routing issues
        customer_data = {
            "customer_id": "demo_customer_123",
            "current_plan": "basic",
            "usage_metrics": {
                "monthly_usage": 1500,
                "feature_usage": ["analytics", "reporting"]
            }
        }
        
        self.test_endpoint(
            "Advanced Pricing Optimization Analysis",
            "POST",
            "api/advanced/pricing-optimization/analysis",
            data=customer_data
        )
        
        # Also test the dashboard
        self.test_endpoint(
            "Advanced Pricing Optimization Dashboard",
            "GET",
            "api/advanced/pricing-optimization"
        )

    def test_sentiment_analysis_validation_issue(self):
        """Test the Sentiment Analysis communication validation for text field requirement"""
        print("\n" + "="*80)
        print("🎯 TESTING SENTIMENT ANALYSIS VALIDATION ISSUE")
        print("="*80)
        
        # Test cases to identify the text field validation issue
        test_cases = [
            {
                "name": "Sentiment Analysis with missing text field",
                "data": {
                    "customer_id": "demo_customer_123",
                    "source": "email"
                }
            },
            {
                "name": "Sentiment Analysis with empty text field",
                "data": {
                    "customer_id": "demo_customer_123",
                    "text": "",
                    "source": "email"
                }
            },
            {
                "name": "Sentiment Analysis with valid text field",
                "data": {
                    "customer_id": "demo_customer_123",
                    "text": "I love this product! It has exceeded my expectations and the customer service is fantastic.",
                    "source": "email"
                }
            },
            {
                "name": "Sentiment Analysis with different source",
                "data": {
                    "customer_id": "demo_customer_123",
                    "text": "The software is okay but could use some improvements in the user interface.",
                    "source": "chat"
                }
            }
        ]
        
        for test_case in test_cases:
            self.test_endpoint(
                test_case["name"],
                "POST",
                "api/advanced/sentiment-analysis/communication",
                data=test_case["data"]
            )

    def run_all_issue_tests(self):
        """Run all issue-focused tests"""
        print("🚀 STARTING ISSUE-FOCUSED BACKEND TESTING")
        print(f"Base URL: {self.base_url}")
        print(f"Test Time: {datetime.now()}")
        
        # Test all the specific issues
        self.test_revenue_forecasting_issues()
        self.test_ab_testing_validation_issue()
        self.test_cross_sell_intelligence_issue()
        self.test_pricing_optimization_routing_issue()
        self.test_sentiment_analysis_validation_issue()
        
        # Generate summary report
        self.generate_issue_report()

    def generate_issue_report(self):
        """Generate a detailed report of all issues found"""
        print("\n" + "="*80)
        print("📋 ISSUE ANALYSIS REPORT")
        print("="*80)
        
        if not self.issues_found:
            print("✅ NO ISSUES FOUND - All endpoints are working correctly!")
            return
        
        print(f"❌ TOTAL ISSUES FOUND: {len(self.issues_found)}")
        
        for i, issue in enumerate(self.issues_found, 1):
            print(f"\n🔍 ISSUE #{i}: {issue['name']}")
            print(f"   Endpoint: {issue['endpoint']}")
            print(f"   Method: {issue['method']}")
            print(f"   Expected Status: {issue.get('expected_status', 'N/A')}")
            print(f"   Actual Status: {issue.get('actual_status', 'N/A')}")
            print(f"   Error Detail: {issue['error_detail']}")
            if issue.get('data_sent'):
                print(f"   Data Sent: {json.dumps(issue['data_sent'], indent=2)}")
            
            # Suggest potential fixes based on the error
            self.suggest_fix(issue)

    def suggest_fix(self, issue):
        """Suggest potential fixes based on the issue details"""
        print(f"   💡 SUGGESTED FIX:")
        
        if issue.get('actual_status') == 404:
            if 'forecasting' in issue['endpoint']:
                print(f"      - Check if Revenue Forecasting router is properly included in server.py")
                print(f"      - Verify the endpoint path matches the router definition")
            elif 'cross-sell-intelligence' in issue['endpoint']:
                print(f"      - Check if Cross-Sell Intelligence router is properly included")
                print(f"      - Verify the endpoint path and parameter handling")
            elif 'pricing-optimization' in issue['endpoint']:
                print(f"      - Check if Advanced Pricing Optimization router is properly included")
                print(f"      - Verify the endpoint path matches the router definition")
            else:
                print(f"      - Check if the router is properly included in server.py")
                print(f"      - Verify the endpoint path is correctly defined")
        
        elif issue.get('actual_status') == 422:
            if 'ab-testing' in issue['endpoint']:
                print(f"      - Check the test_type field validation in the Pydantic model")
                print(f"      - Verify allowed values for test_type field")
            elif 'sentiment-analysis' in issue['endpoint']:
                print(f"      - Check if 'text' field is required in the request model")
                print(f"      - Verify field validation rules for text input")
            else:
                print(f"      - Check request data validation in the Pydantic model")
                print(f"      - Verify required fields and data types")
        
        elif issue.get('actual_status') == 500:
            print(f"      - Check server logs for internal errors")
            print(f"      - Verify database connections and dependencies")
            print(f"      - Check for missing imports or service initialization")
        
        else:
            print(f"      - Review the endpoint implementation")
            print(f"      - Check server logs for more details")

if __name__ == "__main__":
    tester = IssueFocusedTester()
    tester.run_all_issue_tests()