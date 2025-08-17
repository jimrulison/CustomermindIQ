#!/usr/bin/env python3

import requests
import json

def test_revenue_post_endpoints():
    """Test Revenue Analytics Suite POST endpoints"""
    base_url = "https://smart-customer-hub.preview.emergentagent.com"
    headers = {'Content-Type': 'application/json'}
    
    print("🎯 TESTING REVENUE ANALYTICS SUITE POST ENDPOINTS")
    print("=" * 60)
    
    # Test POST endpoints with sample data
    post_tests = [
        {
            "name": "Revenue Forecasting Scenario",
            "endpoint": "api/revenue/revenue-forecasting/scenario",
            "data": {
                "time_horizon": 12,
                "growth_rate": 15,
                "market_conditions": "optimistic"
            }
        },
        {
            "name": "Price Change Simulation",
            "endpoint": "api/revenue/price-optimization/simulate",
            "data": {
                "product_id": "test_product_123",
                "current_price": 100,
                "new_price": 115
            }
        },
        {
            "name": "Cost Reduction Simulation",
            "endpoint": "api/revenue/profit-margin-analysis/cost-simulation",
            "data": {
                "cost_reduction_percentage": 12,
                "categories": ["operations", "marketing"]
            }
        },
        {
            "name": "Customer Churn Prediction",
            "endpoint": "api/revenue/subscription-analytics/churn-prediction",
            "data": {
                "customer_id": "test_customer_456",
                "usage_score": 65,
                "satisfaction_score": 7.2,
                "support_tickets": 3,
                "subscription_length_months": 8
            }
        },
        {
            "name": "Custom Financial Report",
            "endpoint": "api/revenue/financial-reporting/custom-report",
            "data": {
                "report_type": "comprehensive",
                "date_range": "quarterly",
                "include_forecasts": True
            }
        }
    ]
    
    results = []
    
    for test in post_tests:
        url = f"{base_url}/{test['endpoint']}"
        print(f"\n💰 Testing: {test['name']}")
        print(f"   URL: {url}")
        print(f"   Data: {json.dumps(test['data'], indent=2)}")
        
        try:
            response = requests.post(url, json=test['data'], headers=headers, timeout=45)
            
            success = response.status_code == 200
            if success:
                print(f"✅ PASSED - Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Response preview: {str(data)[:150]}...")
                    results.append((test['name'], "PASSED", response.status_code))
                except:
                    results.append((test['name'], "PASSED", response.status_code))
            else:
                print(f"❌ FAILED - Status: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                results.append((test['name'], "FAILED", response.status_code))
                
        except requests.exceptions.Timeout:
            print(f"❌ FAILED - Timeout after 45 seconds")
            results.append((test['name'], "TIMEOUT", 0))
        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            results.append((test['name'], "ERROR", 0))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 REVENUE ANALYTICS SUITE POST ENDPOINTS SUMMARY")
    print(f"{'='*60}")
    
    passed = len([r for r in results if r[1] == "PASSED"])
    total = len(results)
    
    for name, status, code in results:
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {name}: {status} ({code})")
    
    print(f"\nOverall Results: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    
    return passed, total

if __name__ == "__main__":
    test_revenue_post_endpoints()