#!/usr/bin/env python3

import requests
import json

def test_additional_revenue_endpoints():
    """Test additional Revenue Analytics Suite GET endpoints"""
    base_url = "https://smart-customer-hub.preview.emergentagent.com"
    headers = {'Content-Type': 'application/json'}
    
    print("🎯 TESTING ADDITIONAL REVENUE ANALYTICS SUITE ENDPOINTS")
    print("=" * 70)
    
    # Test additional GET endpoints
    additional_endpoints = [
        ("Revenue Trends Analysis", "GET", "api/revenue/revenue-forecasting/trends"),
        ("Competitive Pricing Analysis", "GET", "api/revenue/price-optimization/competitive-analysis"),
        ("Industry Benchmarking", "GET", "api/revenue/profit-margin-analysis/benchmarking"),
        ("Subscription Revenue Optimization", "GET", "api/revenue/subscription-analytics/revenue-optimization"),
        ("Executive KPI Dashboard", "GET", "api/revenue/financial-reporting/kpi-dashboard"),
        ("Budget Variance Analysis", "GET", "api/revenue/financial-reporting/variance-analysis"),
    ]
    
    results = []
    
    for name, method, endpoint in additional_endpoints:
        url = f"{base_url}/{endpoint}"
        print(f"\n💰 Testing: {name}")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=45)
            
            success = response.status_code == 200
            if success:
                print(f"✅ PASSED - Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Response preview: {str(data)[:150]}...")
                    
                    # Show some key data points for verification
                    if 'trends' in data:
                        trends = data['trends']
                        print(f"   📊 Trends data: {len(trends)} trend categories")
                    elif 'competitive_landscape' in data:
                        landscape = data['competitive_landscape']
                        competitors = landscape.get('competitors', [])
                        print(f"   🏆 Competitors analyzed: {len(competitors)}")
                    elif 'benchmarking' in data:
                        benchmarking = data['benchmarking']
                        position = benchmarking.get('company_position', {})
                        print(f"   📈 Company position: {position.get('industry_ranking', 'unknown')}")
                    elif 'revenue_optimization' in data:
                        optimization = data['revenue_optimization']
                        strategies = optimization.get('optimization_strategies', [])
                        print(f"   💡 Optimization strategies: {len(strategies)}")
                    elif 'dashboard' in data:
                        dashboard = data['dashboard']
                        kpis = dashboard.get('executive_kpis', [])
                        print(f"   📊 Executive KPIs: {len(kpis)}")
                    elif 'variance_analysis' in data:
                        analysis = data['variance_analysis']
                        variances = analysis.get('category_variances', [])
                        print(f"   📊 Variance categories: {len(variances)}")
                    
                    results.append((name, "PASSED", response.status_code))
                except Exception as e:
                    print(f"   ⚠️ JSON parsing issue: {e}")
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
    print(f"\n{'='*70}")
    print("📊 ADDITIONAL REVENUE ANALYTICS ENDPOINTS SUMMARY")
    print(f"{'='*70}")
    
    passed = len([r for r in results if r[1] == "PASSED"])
    total = len(results)
    
    for name, status, code in results:
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {name}: {status} ({code})")
    
    print(f"\nOverall Results: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    
    return passed, total

if __name__ == "__main__":
    test_additional_revenue_endpoints()