#!/usr/bin/env python3

import requests
import json
from datetime import datetime

class AdvancedFeaturesExpansionTester:
    def __init__(self, base_url="https://portal-rescue.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run an Advanced Features Expansion API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🚀 Testing: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error text: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_behavioral_clustering_dashboard(self):
        """Test Behavioral Clustering Dashboard"""
        success, response = self.run_test(
            "Behavioral Clustering Dashboard",
            "GET",
            "api/advanced/behavioral-clustering",
            200,
            timeout=45
        )
        
        if success:
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Customers Analyzed: {summary.get('total_customers_analyzed', 0)}")
                print(f"   Clusters Identified: {summary.get('clusters_identified', 0)}")
                clusters = dashboard.get('customer_clusters', [])
                print(f"   Customer Clusters: {len(clusters)}")
        
        return success

    def test_churn_prevention_dashboard(self):
        """Test Churn Prevention AI Dashboard"""
        success, response = self.run_test(
            "Churn Prevention AI Dashboard",
            "GET",
            "api/advanced/churn-prevention",
            200,
            timeout=60
        )
        
        if success:
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Customers Monitored: {summary.get('total_customers_monitored', 0)}")
                print(f"   At-Risk Customers: {summary.get('at_risk_customers', 0)}")
        
        return success

    def test_cross_sell_intelligence_dashboard(self):
        """Test Cross-Sell Intelligence Dashboard"""
        success, response = self.run_test(
            "Cross-Sell Intelligence Dashboard",
            "GET",
            "api/advanced/cross-sell-intelligence",
            200,
            timeout=45
        )
        
        if success:
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Cross-Sell Opportunities: {summary.get('total_cross_sell_opportunities', 0)}")
                print(f"   Potential Revenue: ${summary.get('total_potential_revenue', 0):,}")
        
        return success

    def test_pricing_optimization_dashboard(self):
        """Test Advanced Pricing Optimization Dashboard"""
        success, response = self.run_test(
            "Advanced Pricing Optimization Dashboard",
            "GET",
            "api/advanced/pricing-optimization",
            200,
            timeout=45
        )
        
        if success:
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Customers Analyzed: {summary.get('total_customers_analyzed', 0)}")
                print(f"   Active Experiments: {summary.get('active_pricing_experiments', 0)}")
        
        return success

    def test_sentiment_analysis_dashboard(self):
        """Test Sentiment Analysis Dashboard"""
        success, response = self.run_test(
            "Sentiment Analysis Dashboard",
            "GET",
            "api/advanced/sentiment-analysis",
            200,
            timeout=45
        )
        
        if success:
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Communications Analyzed: {summary.get('total_communications_analyzed', 0)}")
                print(f"   Overall Sentiment: {summary.get('overall_sentiment_score', 0)}")
        
        return success

    def test_advanced_dashboard(self):
        """Test Advanced Features Expansion Dashboard"""
        success, response = self.run_test(
            "Advanced Features Expansion Dashboard",
            "GET",
            "api/advanced/dashboard",
            200,
            timeout=90
        )
        
        if success:
            modules = response.get('modules', {})
            print(f"   Integrated modules: {len(modules)}")
            for module_name, module_data in modules.items():
                if isinstance(module_data, dict) and 'error' not in module_data:
                    print(f"   ✅ {module_name.replace('_', ' ').title()}: Working")
                else:
                    print(f"   ❌ {module_name.replace('_', ' ').title()}: Error")
        
        return success

def main():
    print("🚀 ADVANCED FEATURES EXPANSION MODULE - FOCUSED TESTING")
    print("=" * 80)
    print("Testing 5 Advanced Features Expansion Microservices:")
    print("1. Behavioral Clustering - K-means clustering for customer segmentation")
    print("2. Churn Prevention AI - Predictive churn modeling with automated retention")
    print("3. Cross-Sell Intelligence - Product relationship analysis and recommendations")
    print("4. Advanced Pricing Optimization - AI-driven price sensitivity and dynamic pricing")
    print("5. Sentiment Analysis - NLP analysis of customer communications")
    print("=" * 80)
    
    tester = AdvancedFeaturesExpansionTester()
    
    # Test sequence
    tests = [
        ("Behavioral Clustering Dashboard", tester.test_behavioral_clustering_dashboard),
        ("Churn Prevention AI Dashboard", tester.test_churn_prevention_dashboard),
        ("Cross-Sell Intelligence Dashboard", tester.test_cross_sell_intelligence_dashboard),
        ("Advanced Pricing Optimization Dashboard", tester.test_pricing_optimization_dashboard),
        ("Sentiment Analysis Dashboard", tester.test_sentiment_analysis_dashboard),
        ("Advanced Features Dashboard", tester.test_advanced_dashboard),
    ]
    
    print(f"\n📋 Running {len(tests)} Advanced Features Expansion tests...")
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
    
    # Print final results
    print(f"\n{'='*80}")
    print(f"📊 ADVANCED FEATURES EXPANSION TEST RESULTS")
    print(f"{'='*80}")
    print(f"Total tests run: {tester.tests_run}")
    print(f"Total tests passed: {tester.tests_passed}")
    print(f"Success rate: {(tester.tests_passed/tester.tests_run*100):.1f}%" if tester.tests_run > 0 else "No tests run")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All Advanced Features Expansion tests passed!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    main()