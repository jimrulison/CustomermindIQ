#!/usr/bin/env python3

import requests
import json
from datetime import datetime

class AdvancedFeaturesDetailedTester:
    def __init__(self, base_url="https://subscription-tiers-4.preview.emergentagent.com"):
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

    def test_behavioral_clustering_analyze(self):
        """Test Customer Behavior Analysis"""
        customer_data = {
            "customer_id": "test_customer_123",
            "total_purchases": 5,
            "total_spent": 2500.0,
            "software_owned": ["CRM Pro", "Analytics Suite"],
            "engagement_score": 75,
            "last_purchase_date": "2024-01-15T10:00:00Z"
        }
        
        success, response = self.run_test(
            "Customer Behavior Analysis",
            "POST",
            "api/advanced/behavioral-clustering/analyze",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            cluster_assignment = response.get('cluster_assignment', {})
            if cluster_assignment:
                print(f"   Assigned Cluster: {cluster_assignment.get('cluster_name', 'unknown')}")
                print(f"   Confidence Score: {cluster_assignment.get('confidence_score', 0)}")
        
        return success

    def test_churn_prevention_predict(self):
        """Test Individual Customer Churn Prediction"""
        customer_data = {
            "customer_id": "test_customer_456",
            "days_since_last_login": 21,
            "usage_frequency_change": -25,
            "payment_delays": 1,
            "support_tickets_last_30d": 2,
            "feature_adoption_rate": 45,
            "email_engagement_rate": 15,
            "account_age_days": 180,
            "last_purchase_days_ago": 45,
            "subscription_value": 299
        }
        
        success, response = self.run_test(
            "Customer Churn Prediction",
            "POST",
            "api/advanced/churn-prevention/predict",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            prediction = response.get('churn_prediction', {})
            if prediction:
                print(f"   Churn Probability: {prediction.get('churn_probability', 0)}%")
                print(f"   Risk Level: {prediction.get('risk_level', 'unknown')}")
        
        return success

    def test_cross_sell_recommend(self):
        """Test Customer Cross-Sell Recommendations"""
        customer_data = {
            "customer_id": "test_customer_789",
            "current_products": ["CRM Pro"],
            "segment": "SMB",
            "purchase_history": [
                {"product": "CRM Pro", "date": "2024-01-15", "amount": 299}
            ],
            "usage_patterns": {
                "engagement_score": 85,
                "feature_utilization": 0.7
            }
        }
        
        success, response = self.run_test(
            "Customer Cross-Sell Recommendations",
            "POST",
            "api/advanced/cross-sell-intelligence/recommend",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            recommendations = response.get('recommendations', [])
            print(f"   Product Recommendations: {len(recommendations)}")
            for rec in recommendations[:2]:  # Show first 2 recommendations
                print(f"   - {rec.get('product_name', 'Unknown')}: ${rec.get('price', 0)}")
                print(f"     Confidence: {rec.get('confidence_score', 0)}%")
        
        return success

    def test_pricing_analyze_customer(self):
        """Test Customer Price Sensitivity Analysis"""
        customer_data = {
            "customer_id": "test_customer_pricing_001",
            "purchase_history": [
                {"product": "CRM Pro", "price": 299, "date": "2024-01-15"},
                {"product": "Analytics Suite", "price": 199, "date": "2024-02-20"}
            ],
            "avg_order_value": 249,
            "discount_response_history": [15, 20, 10],
            "time_between_purchases": 45,
            "price_comparison_behavior": "moderate",
            "customer_segment": "SMB",
            "geographic_region": "US",
            "company_size": "small",
            "industry": "technology"
        }
        
        success, response = self.run_test(
            "Customer Price Sensitivity Analysis",
            "POST",
            "api/advanced/pricing-optimization/analyze-customer",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            sensitivity_analysis = response.get('price_sensitivity_analysis', {})
            if sensitivity_analysis:
                print(f"   Sensitivity Score: {sensitivity_analysis.get('sensitivity_score', 0)}/100")
                print(f"   Sensitivity Category: {sensitivity_analysis.get('sensitivity_category', 'unknown')}")
        
        return success

    def test_sentiment_analyze(self):
        """Test Communication Sentiment Analysis"""
        communication_data = {
            "communication_id": "comm_test_001",
            "customer_id": "test_customer_sentiment_001",
            "text": "I love the new features in the CRM Pro! The customer support has been excellent and the product quality is amazing. Very satisfied with my purchase and would highly recommend to others.",
            "source": "email",
            "communication_type": "feedback"
        }
        
        success, response = self.run_test(
            "Communication Sentiment Analysis",
            "POST",
            "api/advanced/sentiment-analysis/analyze",
            200,
            data=communication_data,
            timeout=30
        )
        
        if success:
            sentiment_analysis = response.get('sentiment_analysis', {})
            if sentiment_analysis:
                print(f"   Sentiment Score: {sentiment_analysis.get('sentiment_score', 0)}")
                print(f"   Sentiment Category: {sentiment_analysis.get('sentiment_category', 'unknown')}")
        
        return success

def main():
    print("🚀 ADVANCED FEATURES EXPANSION - DETAILED ENDPOINT TESTING")
    print("=" * 80)
    print("Testing individual POST endpoints with realistic data:")
    print("1. Customer Behavior Analysis")
    print("2. Individual Churn Prediction")
    print("3. Cross-Sell Recommendations")
    print("4. Price Sensitivity Analysis")
    print("5. Sentiment Analysis")
    print("=" * 80)
    
    tester = AdvancedFeaturesDetailedTester()
    
    # Test sequence
    tests = [
        ("Customer Behavior Analysis", tester.test_behavioral_clustering_analyze),
        ("Individual Churn Prediction", tester.test_churn_prevention_predict),
        ("Cross-Sell Recommendations", tester.test_cross_sell_recommend),
        ("Price Sensitivity Analysis", tester.test_pricing_analyze_customer),
        ("Communication Sentiment Analysis", tester.test_sentiment_analyze),
    ]
    
    print(f"\n📋 Running {len(tests)} detailed endpoint tests...")
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
    
    # Print final results
    print(f"\n{'='*80}")
    print(f"📊 DETAILED ENDPOINT TEST RESULTS")
    print(f"{'='*80}")
    print(f"Total tests run: {tester.tests_run}")
    print(f"Total tests passed: {tester.tests_passed}")
    print(f"Success rate: {(tester.tests_passed/tester.tests_run*100):.1f}%" if tester.tests_run > 0 else "No tests run")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All detailed endpoint tests passed!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    main()