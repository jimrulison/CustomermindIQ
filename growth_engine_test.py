#!/usr/bin/env python3
"""
Growth Acceleration Engine Opportunity Scanner Test
Testing the fix for duplicate initiatives issue
"""

import requests
import json
import time
from datetime import datetime
import sys

class GrowthEngineOpportunityTester:
    def __init__(self, base_url="https://mindiq-portal.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.access_token = None
        
    def authenticate_admin(self):
        """Authenticate as admin user to get access token"""
        print("\n🔐 Authenticating as admin user...")
        
        login_data = {
            "email": "admin@customermindiq.com",
            "password": "CustomerMindIQ2025!"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                print(f"✅ Admin authentication successful")
                return True
            else:
                print(f"❌ Admin authentication failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Admin authentication error: {e}")
            return False
    
    def get_auth_headers(self):
        """Get headers with authentication token"""
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
    
    def run_test(self, name, method, endpoint, expected_status=200, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = self.get_auth_headers()
        
        self.tests_run += 1
        print(f"\n🧪 Test {self.tests_run}: {name}")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == expected_status:
                try:
                    response_data = response.json()
                    print(f"✅ {name} - SUCCESS")
                    self.tests_passed += 1
                    return True, response_data
                except json.JSONDecodeError:
                    print(f"❌ {name} - Invalid JSON response")
                    return False, {}
            else:
                print(f"❌ {name} - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:500]}")
                return False, {}
                
        except Exception as e:
            print(f"❌ {name} - Error: {str(e)}")
            return False, {}
    
    def test_opportunity_scan_diversity(self):
        """Test multiple opportunity scans to verify diversity (no duplicates)"""
        print("\n" + "="*80)
        print("🎯 TESTING OPPORTUNITY SCAN DIVERSITY")
        print("="*80)
        print("Testing multiple calls to /api/growth/opportunities/scan")
        print("Verifying that different opportunities are generated each time")
        
        all_opportunities = []
        scan_results = []
        
        # Sample customer data for the scan
        sample_customer_data = {
            "total_revenue": 500000,
            "total_customers": 250,
            "monthly_growth_rate": 0.15,
            "churn_rate": 0.05,
            "average_order_value": 2000,
            "customer_acquisition_cost": 150,
            "lifetime_value": 8000,
            "industry": "SaaS",
            "company_size": "mid-market"
        }
        
        scan_request_data = {
            "customer_data": sample_customer_data,
            "focus_areas": ["acquisition", "retention", "expansion"],
            "timeframe_months": 12
        }
        
        # Run 5 scans to test diversity
        for i in range(5):
            print(f"\n--- Scan {i+1}/5 ---")
            success, data = self.run_test(
                f"Opportunity Scan #{i+1}",
                "POST",
                "api/growth/opportunities/scan",
                data=scan_request_data
            )
            
            if success and data.get('status') == 'success':
                opportunities = data.get('opportunities', [])
                scan_results.append({
                    'scan_number': i+1,
                    'opportunities': opportunities,
                    'count': len(opportunities)
                })
                
                print(f"   Found {len(opportunities)} opportunities:")
                for j, opp in enumerate(opportunities, 1):
                    title = opp.get('title', 'No title')
                    opp_type = opp.get('type', 'No type')
                    revenue_impact = opp.get('projected_revenue_impact', 0)
                    print(f"   {j}. {title} ({opp_type}) - ${revenue_impact:,}")
                    
                    # Store for duplicate checking
                    all_opportunities.append({
                        'scan': i+1,
                        'title': title,
                        'type': opp_type,
                        'description': opp.get('description', ''),
                        'revenue_impact': revenue_impact
                    })
            else:
                print(f"   ❌ Scan {i+1} failed")
        
        # Analyze diversity
        print(f"\n📊 DIVERSITY ANALYSIS")
        print(f"Total opportunities collected: {len(all_opportunities)}")
        
        # Check for duplicate titles
        titles = [opp['title'] for opp in all_opportunities]
        unique_titles = set(titles)
        duplicate_titles = len(titles) - len(unique_titles)
        
        print(f"Unique titles: {len(unique_titles)}")
        print(f"Duplicate titles: {duplicate_titles}")
        
        # Check for duplicate descriptions
        descriptions = [opp['description'] for opp in all_opportunities]
        unique_descriptions = set(descriptions)
        duplicate_descriptions = len(descriptions) - len(unique_descriptions)
        
        print(f"Unique descriptions: {len(unique_descriptions)}")
        print(f"Duplicate descriptions: {duplicate_descriptions}")
        
        # Check type diversity
        types = [opp['type'] for opp in all_opportunities]
        unique_types = set(types)
        print(f"Opportunity types found: {list(unique_types)}")
        
        # Check revenue impact diversity
        revenue_impacts = [opp['revenue_impact'] for opp in all_opportunities]
        unique_revenue_impacts = set(revenue_impacts)
        print(f"Unique revenue impacts: {len(unique_revenue_impacts)}")
        
        # Determine if diversity test passes
        diversity_score = 0
        if duplicate_titles == 0:
            print("✅ No duplicate titles found")
            diversity_score += 1
        else:
            print(f"❌ Found {duplicate_titles} duplicate titles")
            
        if duplicate_descriptions == 0:
            print("✅ No duplicate descriptions found")
            diversity_score += 1
        else:
            print(f"❌ Found {duplicate_descriptions} duplicate descriptions")
            
        if len(unique_types) >= 2:
            print("✅ Multiple opportunity types found")
            diversity_score += 1
        else:
            print("❌ Limited opportunity type diversity")
            
        if len(unique_revenue_impacts) >= len(all_opportunities) * 0.7:  # At least 70% unique
            print("✅ Good revenue impact diversity")
            diversity_score += 1
        else:
            print("❌ Limited revenue impact diversity")
        
        print(f"\n🎯 DIVERSITY SCORE: {diversity_score}/4")
        
        if diversity_score >= 3:
            print("✅ DIVERSITY TEST PASSED - Opportunities are sufficiently diverse")
            return True
        else:
            print("❌ DIVERSITY TEST FAILED - Too many duplicates or insufficient diversity")
            return False
    
    def test_dashboard_endpoint(self):
        """Test the growth dashboard endpoint"""
        print("\n" + "="*80)
        print("📊 TESTING GROWTH DASHBOARD")
        print("="*80)
        
        success, data = self.run_test(
            "Growth Dashboard",
            "GET",
            "api/growth/dashboard"
        )
        
        if success and data.get('status') == 'success':
            dashboard = data.get('dashboard', {})
            metrics = dashboard.get('metrics', {})
            
            print(f"   Total opportunities: {metrics.get('total_opportunities_identified', 0)}")
            print(f"   Projected revenue: ${metrics.get('total_projected_revenue', 0):,}")
            print(f"   Active tests: {metrics.get('active_tests_count', 0)}")
            print(f"   Revenue leaks fixed: {metrics.get('revenue_leaks_fixed', 0)}")
            print(f"   Average ROI: {metrics.get('average_roi', 0):.2f}x")
            
            return True
        else:
            return False
    
    def test_opportunities_dashboard_endpoint(self):
        """Test the opportunities-specific dashboard endpoint"""
        print("\n" + "="*80)
        print("📈 TESTING OPPORTUNITIES DASHBOARD")
        print("="*80)
        
        success, data = self.run_test(
            "Opportunities Dashboard",
            "GET",
            "api/growth/opportunities/dashboard"
        )
        
        if success and data.get('status') == 'success':
            dashboard = data.get('dashboard', {})
            
            print(f"   Total opportunities: {dashboard.get('total_count', 0)}")
            print(f"   Total projected impact: ${dashboard.get('total_projected_impact', 0):,}")
            
            priority_breakdown = dashboard.get('priority_breakdown', {})
            type_breakdown = dashboard.get('type_breakdown', {})
            
            print(f"   Priority breakdown: {priority_breakdown}")
            print(f"   Type breakdown: {type_breakdown}")
            
            return True
        else:
            return False
    
    def test_full_scan_endpoint(self):
        """Test the full growth scan endpoint"""
        print("\n" + "="*80)
        print("🔍 TESTING FULL GROWTH SCAN")
        print("="*80)
        
        # Sample data for full scan
        full_scan_data = {
            "customer_data": {
                "total_revenue": 750000,
                "total_customers": 400,
                "monthly_growth_rate": 0.12,
                "churn_rate": 0.04,
                "average_order_value": 1875,
                "customer_acquisition_cost": 200,
                "lifetime_value": 9000,
                "industry": "SaaS",
                "company_size": "enterprise"
            },
            "funnel_data": [
                {"stage": "awareness", "users": 10000, "conversion_rate": 0.15},
                {"stage": "interest", "users": 1500, "conversion_rate": 0.25},
                {"stage": "consideration", "users": 375, "conversion_rate": 0.40},
                {"stage": "purchase", "users": 150, "conversion_rate": 1.0}
            ]
        }
        
        success, data = self.run_test(
            "Full Growth Scan",
            "POST",
            "api/growth/full-scan",
            data=full_scan_data
        )
        
        if success and data.get('status') == 'success':
            scan_results = data.get('scan_results', {})
            
            # Check opportunities
            opportunities = scan_results.get('opportunities', [])
            print(f"   Opportunities found: {len(opportunities)}")
            
            for i, opp in enumerate(opportunities, 1):
                title = opp.get('title', 'No title')
                opp_type = opp.get('type', 'No type')
                revenue_impact = opp.get('projected_revenue_impact', 0)
                print(f"   {i}. {title} ({opp_type}) - ${revenue_impact:,}")
            
            # Check revenue leaks
            revenue_leaks = scan_results.get('revenue_leaks', [])
            print(f"   Revenue leaks found: {len(revenue_leaks)}")
            
            # Check ROI calculations
            roi_calculations = scan_results.get('roi_calculations', [])
            print(f"   ROI calculations: {len(roi_calculations)}")
            
            return True
        else:
            return False
    
    def test_health_check(self):
        """Test basic health check"""
        print("\n" + "="*80)
        print("🏥 TESTING HEALTH CHECK")
        print("="*80)
        
        success, data = self.run_test(
            "Health Check",
            "GET",
            "api/health"
        )
        
        if success:
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            return True
        else:
            return False
    
    def run_all_tests(self):
        """Run all Growth Acceleration Engine tests"""
        print("🚀 GROWTH ACCELERATION ENGINE OPPORTUNITY SCANNER TESTING")
        print("="*80)
        print("Testing the fix for duplicate initiatives issue")
        print("Verifying that opportunity scans generate diverse, unique results")
        print("="*80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed - cannot proceed with tests")
            return False
        
        # Run health check
        health_ok = self.test_health_check()
        
        # Run main tests
        diversity_ok = self.test_opportunity_scan_diversity()
        dashboard_ok = self.test_dashboard_endpoint()
        opportunities_dashboard_ok = self.test_opportunities_dashboard_endpoint()
        full_scan_ok = self.test_full_scan_endpoint()
        
        # Summary
        print("\n" + "="*80)
        print("📋 TEST SUMMARY")
        print("="*80)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n🎯 KEY RESULTS:")
        print(f"   Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"   Opportunity Diversity: {'✅ PASS' if diversity_ok else '❌ FAIL'}")
        print(f"   Main Dashboard: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
        print(f"   Opportunities Dashboard: {'✅ PASS' if opportunities_dashboard_ok else '❌ FAIL'}")
        print(f"   Full Scan Endpoint: {'✅ PASS' if full_scan_ok else '❌ FAIL'}")
        
        # Overall assessment
        critical_tests_passed = diversity_ok and (dashboard_ok or opportunities_dashboard_ok)
        
        if critical_tests_passed:
            print(f"\n✅ OVERALL RESULT: SUCCESS")
            print(f"   The duplicate initiatives issue appears to be RESOLVED")
            print(f"   Opportunity scans are generating diverse, unique results")
            return True
        else:
            print(f"\n❌ OVERALL RESULT: ISSUES FOUND")
            print(f"   The duplicate initiatives issue may still exist")
            print(f"   Review the detailed test results above")
            return False

def main():
    """Main function to run Growth Acceleration Engine testing"""
    tester = GrowthEngineOpportunityTester()
    
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())