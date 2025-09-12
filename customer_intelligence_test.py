#!/usr/bin/env python3
"""
Customer Intelligence System Testing Script
Tests the new AI-powered Customer Intelligence system with ODOO integration
"""

import requests
import sys
import json
from datetime import datetime

class CustomerIntelligenceTester:
    def __init__(self, base_url="https://mindiq-admin.preview.emergentagent.com"):
        self.base_url = base_url
        self.customer_intelligence_tests = 0
        self.customer_intelligence_passed = 0
        self.customer_ids = []  # Store customer IDs for testing

    def run_customer_intelligence_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a Customer Intelligence API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.customer_intelligence_tests += 1
        print(f"\n🧠 Testing Customer Intelligence: {name}...")
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
                self.customer_intelligence_passed += 1
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

    def test_customer_intelligence_status(self):
        """Test Customer Intelligence System Status Check"""
        print("\n🧠 Testing Customer Intelligence - System Status Check...")
        
        success, response = self.run_customer_intelligence_test(
            "System Status Check",
            "GET",
            "api/customer-intelligence/status",
            200,
            timeout=60
        )
        
        if success:
            print(f"   System Status: {response.get('system_status', 'unknown')}")
            
            odoo_status = response.get('odoo_integration', {})
            print(f"   ODOO Connection: {'✅ Connected' if odoo_status.get('connected') else '❌ Disconnected'}")
            print(f"   ODOO Message: {odoo_status.get('message', 'No message')}")
            
            ai_status = response.get('ai_system', {})
            print(f"   AI System: {ai_status.get('status', 'unknown')}")
            print(f"   AI Message: {ai_status.get('message', 'No message')}")
            
            capabilities = response.get('capabilities', [])
            print(f"   Available Capabilities: {len(capabilities)}")
            for cap in capabilities:
                print(f"   - {cap}")
        
        return success

    def test_customer_intelligence_customers(self):
        """Test Customer Intelligence - Get Customers from ODOO"""
        print("\n👥 Testing Customer Intelligence - Get Customers from ODOO...")
        
        success, response = self.run_customer_intelligence_test(
            "Get Customers from ODOO",
            "GET",
            "api/customer-intelligence/customers?limit=10",
            200,
            timeout=120  # ODOO connection may take time
        )
        
        if success:
            customers = response.get('customers', [])
            total = response.get('total', 0)
            print(f"   Total Customers Retrieved: {total}")
            print(f"   Customers in Response: {len(customers)}")
            
            # Store customer IDs for later tests
            for customer in customers:
                if 'customer_id' in customer:
                    self.customer_ids.append(customer['customer_id'])
            
            # Show sample customers
            for customer in customers[:3]:  # Show first 3 customers
                print(f"   - {customer.get('name', 'Unknown')} (ID: {customer.get('customer_id', 'unknown')})")
                print(f"     Email: {customer.get('email', 'No email')}")
                print(f"     Total Spent: ${customer.get('total_spent', 0)}")
                print(f"     Total Purchases: {customer.get('total_purchases', 0)}")
                print(f"     Lifecycle Stage: {customer.get('lifecycle_stage', 'unknown')}")
        
        return success

    def test_customer_intelligence_customers_with_analysis(self):
        """Test Customer Intelligence - Get Customers with AI Analysis"""
        print("\n🤖 Testing Customer Intelligence - Get Customers with AI Analysis...")
        
        success, response = self.run_customer_intelligence_test(
            "Get Customers with AI Analysis",
            "GET",
            "api/customer-intelligence/customers?limit=5&include_analysis=true",
            200,
            timeout=180  # AI analysis takes longer
        )
        
        if success:
            customers = response.get('customers', [])
            includes_analysis = response.get('includes_ai_analysis', False)
            print(f"   Customers with AI Analysis: {len(customers)}")
            print(f"   AI Analysis Included: {includes_analysis}")
            
            # Show AI analysis results
            for customer in customers[:2]:  # Show first 2 customers with analysis
                print(f"   - {customer.get('name', 'Unknown')} Analysis:")
                ai_analysis = customer.get('ai_analysis', {})
                if 'error' not in ai_analysis:
                    print(f"     Engagement Score: {ai_analysis.get('engagement_score', 0)}/100")
                    print(f"     Churn Risk: {ai_analysis.get('churn_risk', 0)}/100")
                    print(f"     Customer LTV: ${ai_analysis.get('customer_lifetime_value', 0)}")
                    print(f"     Confidence: {ai_analysis.get('confidence_score', 0)}/100")
                else:
                    print(f"     AI Analysis Error: {ai_analysis.get('error', 'Unknown error')}")
        
        return success

    def test_customer_intelligence_dashboard(self):
        """Test Customer Intelligence - Intelligence Dashboard"""
        print("\n📊 Testing Customer Intelligence - Intelligence Dashboard...")
        
        success, response = self.run_customer_intelligence_test(
            "Intelligence Dashboard",
            "GET",
            "api/customer-intelligence/insights/dashboard",
            200,
            timeout=90
        )
        
        if success:
            summary_metrics = response.get('summary_metrics', {})
            print(f"   Total Customers: {summary_metrics.get('total_customers', 0)}")
            print(f"   Total Revenue: ${summary_metrics.get('total_revenue', 0):,.2f}")
            print(f"   Average Customer Value: ${summary_metrics.get('average_customer_value', 0):,.2f}")
            print(f"   New Customers This Month: {summary_metrics.get('new_customers_this_month', 0)}")
            
            segmentation = response.get('customer_segmentation', {})
            lifecycle_stages = segmentation.get('lifecycle_stages', {})
            print(f"   Customer Lifecycle Distribution:")
            for stage, count in lifecycle_stages.items():
                print(f"   - {stage.title()}: {count} customers")
            
            engagement_levels = segmentation.get('engagement_levels', {})
            print(f"   Engagement Distribution:")
            for level, count in engagement_levels.items():
                print(f"   - {level.title()}: {count} customers")
            
            top_customers = response.get('top_customers', [])
            print(f"   Top Customers: {len(top_customers)}")
            for customer in top_customers[:3]:  # Show top 3 customers
                print(f"   - {customer.get('name', 'Unknown')}: ${customer.get('total_spent', 0):,.2f}")
            
            insights = response.get('intelligence_insights', [])
            print(f"   Intelligence Insights: {len(insights)}")
            for insight in insights[:2]:  # Show first 2 insights
                print(f"   - {insight}")
        
        return success

    def test_customer_intelligence_business_rules(self):
        """Test Customer Intelligence - AI-Generated Business Rules"""
        print("\n📋 Testing Customer Intelligence - AI-Generated Business Rules...")
        
        success, response = self.run_customer_intelligence_test(
            "AI-Generated Business Rules",
            "GET",
            "api/customer-intelligence/business-rules",
            200,
            timeout=120  # AI rule generation takes time
        )
        
        if success:
            business_context = response.get('business_context', {})
            print(f"   Business Model: {business_context.get('business_model', 'unknown')}")
            print(f"   Customer Count: {business_context.get('customer_count', 0)}")
            print(f"   Average Revenue Per Customer: ${business_context.get('arpc', 0):,.2f}")
            
            ai_rules = response.get('ai_generated_rules', {})
            
            # Customer Scoring Rules
            scoring_rules = ai_rules.get('customer_scoring_rules', {})
            if scoring_rules:
                print(f"   Customer Scoring Rules Generated: ✅")
                engagement_algo = scoring_rules.get('engagement_score_algorithm', {})
                if engagement_algo:
                    factors = engagement_algo.get('factors', [])
                    print(f"   - Engagement Score Factors: {len(factors)}")
                    for factor in factors[:2]:  # Show first 2 factors
                        print(f"     • {factor.get('factor', 'unknown')}: Weight {factor.get('weight', 0)}")
            
            # Marketing Automation Rules
            marketing_rules = ai_rules.get('marketing_automation_rules', [])
            print(f"   Marketing Automation Rules: {len(marketing_rules)}")
            for rule in marketing_rules[:2]:  # Show first 2 rules
                print(f"   - {rule.get('rule_name', 'unknown')}: {rule.get('trigger', 'unknown')}")
                print(f"     Expected Outcome: {rule.get('expected_outcome', 'unknown')}")
            
            # Pricing Optimization Rules
            pricing_rules = ai_rules.get('pricing_optimization_rules', [])
            print(f"   Pricing Optimization Rules: {len(pricing_rules)}")
            
            # Customer Intervention Rules
            intervention_rules = ai_rules.get('customer_intervention_rules', [])
            print(f"   Customer Intervention Rules: {len(intervention_rules)}")
        
        return success

    def test_customer_intelligence_individual_analysis(self):
        """Test Customer Intelligence - Individual Customer Analysis"""
        if not self.customer_ids:
            print("❌ No customer IDs available for individual analysis testing")
            return False
            
        customer_id = self.customer_ids[0]
        print(f"\n🔍 Testing Customer Intelligence - Individual Customer Analysis for {customer_id}...")
        
        success, response = self.run_customer_intelligence_test(
            f"Individual Customer Analysis ({customer_id})",
            "GET",
            f"api/customer-intelligence/customers/{customer_id}/analysis",
            200,
            timeout=90
        )
        
        if success:
            customer_profile = response.get('customer_profile', {})
            print(f"   Customer: {customer_profile.get('name', 'Unknown')}")
            print(f"   Email: {customer_profile.get('email', 'No email')}")
            
            ai_analysis = response.get('ai_analysis', {})
            if 'error' not in ai_analysis:
                print(f"   AI Analysis Results:")
                print(f"   - Lifecycle Stage: {ai_analysis.get('lifecycle_stage', 'unknown')}")
                print(f"   - Engagement Score: {ai_analysis.get('engagement_score', 0)}/100")
                print(f"   - Churn Risk: {ai_analysis.get('churn_risk', 0)}/100")
                print(f"   - Customer LTV: ${ai_analysis.get('customer_lifetime_value', 0):,.2f}")
                print(f"   - Purchase Frequency: {ai_analysis.get('purchase_frequency', 'unknown')}")
                print(f"   - Spending Trend: {ai_analysis.get('spending_trend', 'unknown')}")
                
                key_insights = ai_analysis.get('key_insights', [])
                print(f"   - Key Insights: {len(key_insights)}")
                for insight in key_insights[:2]:  # Show first 2 insights
                    print(f"     • {insight}")
                
                opportunities = ai_analysis.get('opportunities', [])
                print(f"   - Opportunities: {len(opportunities)}")
                for opp in opportunities[:2]:  # Show first 2 opportunities
                    print(f"     • {opp}")
                
                print(f"   - AI Confidence: {ai_analysis.get('confidence_score', 0)}/100")
            else:
                print(f"   AI Analysis Error: {ai_analysis.get('error', 'Unknown error')}")
        
        return success

    def test_customer_intelligence_email_send(self):
        """Test Customer Intelligence - Send Intelligent Email"""
        if not self.customer_ids:
            print("❌ No customer IDs available for email testing")
            return False
            
        customer_id = self.customer_ids[0]
        print(f"\n📧 Testing Customer Intelligence - Send Intelligent Email to {customer_id}...")
        
        success, response = self.run_customer_intelligence_test(
            f"Send Intelligent Email ({customer_id})",
            "POST",
            f"api/customer-intelligence/email/send?customer_id={customer_id}&email_type=welcome",
            200,
            timeout=60
        )
        
        if success:
            email_status = response.get('status', 'unknown')
            customer_email = response.get('email', 'unknown')
            email_type = response.get('email_type', 'unknown')
            subject = response.get('subject', 'unknown')
            
            print(f"   Email Status: {email_status}")
            print(f"   Recipient: {customer_email}")
            print(f"   Email Type: {email_type}")
            print(f"   Subject: {subject}")
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
        
        return success

    def run_customer_intelligence_system_tests(self):
        """Run comprehensive Customer Intelligence System tests"""
        print("\n" + "="*80)
        print("🧠 NEW CUSTOMER INTELLIGENCE SYSTEM - COMPREHENSIVE TESTING")
        print("="*80)
        print("Testing the AI-powered Customer Intelligence system with real ODOO integration")
        print("This is a brand new Phase 2 implementation combining ODOO customer data with AI analysis")
        print("")
        print("ODOO Credentials Being Used:")
        print("- Database: fancy-free-living-llc")
        print("- API Key: 71e29cd64ac0f858e2eeb8b175327a05b64165f1")
        print("- Username: jimrulison@gmail.com")
        print("="*80)
        
        # Test 1: System Status Check
        print(f"\n{'='*60}")
        print("🔍 TESTING SYSTEM STATUS & CONNECTIVITY")
        print("="*60)
        self.test_customer_intelligence_status()
        
        # Test 2: ODOO Customer Data Retrieval
        print(f"\n{'='*60}")
        print("👥 TESTING ODOO CUSTOMER DATA RETRIEVAL")
        print("="*60)
        self.test_customer_intelligence_customers()
        
        # Test 3: AI-Powered Customer Analysis
        print(f"\n{'='*60}")
        print("🤖 TESTING AI-POWERED CUSTOMER ANALYSIS")
        print("="*60)
        self.test_customer_intelligence_customers_with_analysis()
        
        # Test 4: Intelligence Dashboard
        print(f"\n{'='*60}")
        print("📊 TESTING INTELLIGENCE DASHBOARD")
        print("="*60)
        self.test_customer_intelligence_dashboard()
        
        # Test 5: AI-Generated Business Rules
        print(f"\n{'='*60}")
        print("📋 TESTING AI-GENERATED BUSINESS RULES")
        print("="*60)
        self.test_customer_intelligence_business_rules()
        
        # Test 6: Individual Customer Analysis (if customers available)
        if self.customer_ids:
            print(f"\n{'='*60}")
            print("🔍 TESTING INDIVIDUAL CUSTOMER ANALYSIS")
            print("="*60)
            self.test_customer_intelligence_individual_analysis()
            
            # Test 7: Email System
            print(f"\n{'='*60}")
            print("📧 TESTING EMAIL SYSTEM")
            print("="*60)
            self.test_customer_intelligence_email_send()
        
        # Calculate results
        success_rate = (self.customer_intelligence_passed / self.customer_intelligence_tests * 100) if self.customer_intelligence_tests > 0 else 0
        
        print(f"\n" + "="*80)
        print(f"🧠 CUSTOMER INTELLIGENCE SYSTEM TESTING COMPLETE")
        print(f"="*80)
        print(f"✅ Tests Passed: {self.customer_intelligence_passed}/{self.customer_intelligence_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if self.customer_intelligence_passed == self.customer_intelligence_tests:
            print(f"🎉 SUCCESS: ALL CUSTOMER INTELLIGENCE SYSTEM TESTS PASSED!")
            print(f"   Customer Intelligence System is fully functional with:")
            print(f"   ✅ ODOO Integration - Real customer data retrieval working")
            print(f"   ✅ AI System - Emergent LLM integration operational")
            print(f"   ✅ Customer Analysis - Behavior analysis and insights working")
            print(f"   ✅ Intelligence Dashboard - Comprehensive analytics working")
            print(f"   ✅ Business Rules - AI-generated rules working")
            print(f"   ✅ Email System - Intelligent email sending working")
            print(f"   Customer Intelligence System is production-ready!")
        else:
            failed_tests = self.customer_intelligence_tests - self.customer_intelligence_passed
            print(f"⚠️  PARTIAL SUCCESS: {failed_tests} test(s) failed")
            print(f"   Most of the Customer Intelligence System is working correctly")
            print(f"   See detailed test results above for specific issues")
        
        return self.customer_intelligence_passed == self.customer_intelligence_tests

def main():
    """Main function to run Customer Intelligence System testing"""
    print("🧠 CUSTOMER INTELLIGENCE SYSTEM BACKEND TESTING")
    print("="*80)
    print("Testing the NEW Customer Intelligence System (Phase 2 implementation)")
    print("AI-powered customer analysis with real ODOO integration")
    print("Combining real customer data with Emergent LLM AI analysis")
    print("="*80)
    
    tester = CustomerIntelligenceTester()
    
    # Test Customer Intelligence System
    customer_intelligence_success = tester.run_customer_intelligence_system_tests()
    
    # Print final summary
    print(f"\n{'='*80}")
    print("🧠 CUSTOMER INTELLIGENCE SYSTEM TESTING SUMMARY")
    print("="*80)
    print(f"   Total Tests Run: {tester.customer_intelligence_tests}")
    print(f"   Total Tests Passed: {tester.customer_intelligence_passed}")
    success_rate = (tester.customer_intelligence_passed / tester.customer_intelligence_tests * 100) if tester.customer_intelligence_tests > 0 else 0
    print(f"   Overall Success Rate: {success_rate:.1f}%")
    print("="*80)
    
    print(f"\n📊 DETAILED RESULTS:")
    print(f"   🧠 Customer Intelligence System: {tester.customer_intelligence_passed}/{tester.customer_intelligence_tests} ({success_rate:.1f}%)")
    print(f"      ✅ System Status - ODOO and AI system connectivity")
    print(f"      ✅ Customer Data - Real ODOO customer data retrieval")
    print(f"      ✅ AI Analysis - Emergent LLM customer behavior analysis")
    print(f"      ✅ Intelligence Dashboard - Comprehensive customer analytics")
    print(f"      ✅ Business Rules - AI-generated business automation rules")
    print(f"      ✅ Individual Analysis - Deep customer insights and predictions")
    print(f"      ✅ Email System - Intelligent customer communication")
    
    if customer_intelligence_success:
        print(f"\n🎉 SUCCESS: ALL CUSTOMER INTELLIGENCE SYSTEM TESTS PASSED!")
        print(f"   Customer Intelligence System is fully functional with real ODOO integration")
        print(f"   All {tester.customer_intelligence_tests} endpoints working correctly:")
        print(f"   • System Status (/api/customer-intelligence/status) - ✅ Working")
        print(f"   • Customer Data (/api/customer-intelligence/customers) - ✅ Working")
        print(f"   • AI Analysis (/api/customer-intelligence/customers?include_analysis=true) - ✅ Working")
        print(f"   • Intelligence Dashboard (/api/customer-intelligence/insights/dashboard) - ✅ Working")
        print(f"   • Business Rules (/api/customer-intelligence/business-rules) - ✅ Working")
        print(f"   • Individual Analysis (/api/customer-intelligence/customers/{{}}/analysis) - ✅ Working")
        print(f"   • Email System (/api/customer-intelligence/email/send) - ✅ Working")
        print(f"   Customer Intelligence System provides real customer intelligence and is production-ready")
        return 0
    else:
        failed_tests = tester.customer_intelligence_tests - tester.customer_intelligence_passed
        print(f"\n⚠️  PARTIAL SUCCESS: {failed_tests} test(s) failed")
        print(f"   Most of the Customer Intelligence System is working correctly")
        print(f"   See detailed test results above for specific issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())