#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_revenue_analytics_endpoints():
    """Test Revenue Analytics Suite endpoints specifically"""
    base_url = "https://smart-customer-hub.preview.emergentagent.com"
    headers = {'Content-Type': 'application/json'}
    
    print("🎯 FOCUSED REVENUE ANALYTICS SUITE TESTING")
    print("=" * 60)
    
    # Test endpoints
    endpoints = [
        ("Revenue Forecasting Dashboard", "GET", "api/revenue/revenue-forecasting"),
        ("Price Optimization Dashboard", "GET", "api/revenue/price-optimization"),
        ("Profit Margin Analysis Dashboard", "GET", "api/revenue/profit-margin-analysis"),
        ("Subscription Analytics Dashboard", "GET", "api/revenue/subscription-analytics"),
        ("Financial Reporting Dashboard", "GET", "api/revenue/financial-reporting"),
        ("Revenue Analytics Suite Dashboard", "GET", "api/revenue/dashboard"),
    ]
    
    results = []
    
    for name, method, endpoint in endpoints:
        url = f"{base_url}/{endpoint}"
        print(f"\n💰 Testing: {name}")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=45)
            
            success = response.status_code == 200
            if success:
                print(f"✅ PASSED - Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Response preview: {str(data)[:150]}...")
                    results.append((name, "PASSED", response.status_code))
                except:
                    results.append((name, "PASSED", response.status_code))
            else:
                print(f"❌ FAILED - Status: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                results.append((name, "FAILED", response.status_code))
                
        except requests.exceptions.Timeout:
            print(f"❌ FAILED - Timeout after 45 seconds")
            results.append((name, "TIMEOUT", 0))
        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            results.append((name, "ERROR", 0))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 REVENUE ANALYTICS SUITE TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = len([r for r in results if r[1] == "PASSED"])
    total = len(results)
    
    for name, status, code in results:
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {name}: {status} ({code})")
    
    print(f"\nOverall Results: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("🎉 All Revenue Analytics Suite endpoints are working!")
        return True
    else:
        print(f"⚠️ {total-passed} endpoint(s) failed")
        return False

if __name__ == "__main__":
    test_revenue_analytics_endpoints()