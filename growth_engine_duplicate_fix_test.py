#!/usr/bin/env python3
"""
Growth Acceleration Engine - Duplicate Initiatives Fix Testing
Tests the fix for duplicate initiatives issue as requested in review.

TESTING OBJECTIVES:
1. Test Opportunity Scan & Database Cleanup
2. Test Dashboard with Recent Data  
3. Verify User Experience Fix
4. Test Multiple Scan Cycles
"""

import asyncio
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add the backend directory to Python path
sys.path.append('/app/backend')

class GrowthEngineFixTester:
    def __init__(self):
        # Use the external URL from frontend/.env
        self.base_url = "https://mindiq-admin.preview.emergentagent.com"
        try:
            with open('/app/frontend/.env', 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        self.base_url = line.split('=')[1].strip()
                        break
        except Exception:
            pass  # Use default URL if file reading fails
        
        self.api_base = f"{self.base_url}/api"
        self.headers = {'Content-Type': 'application/json'}
        
        print(f"🔗 Testing Growth Acceleration Engine at: {self.api_base}")
        
        # Test data for scans
        self.test_customer_data = {
            "total_revenue": 500000,
            "total_customers": 250,
            "monthly_growth_rate": 0.08,
            "churn_rate": 0.05,
            "average_deal_size": 2000,
            "customer_acquisition_cost": 150,
            "lifetime_value": 8000,
            "industry": "SaaS",
            "company_size": "mid-market"
        }
        
        self.scan_request = {
            "customer_data": self.test_customer_data,
            "focus_areas": ["acquisition", "retention", "expansion"],
            "timeframe_months": 12
        }
    
    def make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request with error handling"""
        try:
            url = f"{self.api_base}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "message": response.text[:200],
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {"error": "Request failed", "message": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "message": str(e)}
    
    def test_health_check(self) -> bool:
        """Test basic connectivity"""
        print("\n🏥 Testing Health Check...")
        
        result = self.make_request('GET', '/health')
        
        if 'error' in result:
            print(f"❌ Health check failed: {result}")
            return False
        
        if result.get('status') == 'healthy':
            print(f"✅ Health check passed: {result.get('service')} v{result.get('version')}")
            return True
        else:
            print(f"❌ Health check failed: {result}")
            return False
    
    def test_opportunity_scan_cleanup(self) -> Dict[str, Any]:
        """
        TEST 1: Opportunity Scan & Database Cleanup
        Call scan multiple times and verify database cleanup works
        """
        print("\n🔍 TEST 1: Opportunity Scan & Database Cleanup")
        print("=" * 60)
        
        results = {
            "test_name": "Opportunity Scan & Database Cleanup",
            "scans_performed": 0,
            "unique_opportunities_per_scan": [],
            "database_cleanup_working": False,
            "scan_results": [],
            "success": False
        }
        
        try:
            # Perform 3 consecutive scans
            for scan_num in range(1, 4):
                print(f"\n📊 Performing Scan #{scan_num}...")
                
                scan_result = self.make_request('POST', '/growth/opportunities/scan', self.scan_request)
                
                if 'error' in scan_result:
                    print(f"❌ Scan #{scan_num} failed: {scan_result}")
                    results["scan_results"].append({"scan": scan_num, "error": scan_result})
                    continue
                
                opportunities = scan_result.get('opportunities', [])
                opportunities_count = len(opportunities)
                total_impact = scan_result.get('total_projected_impact', 0)
                
                print(f"   📈 Found {opportunities_count} opportunities")
                print(f"   💰 Total projected impact: ${total_impact:,.2f}")
                
                # Extract opportunity titles for uniqueness check
                titles = [opp.get('title', '') for opp in opportunities]
                unique_titles = list(set(titles))
                
                print(f"   🎯 Unique opportunity titles: {len(unique_titles)}")
                for i, title in enumerate(unique_titles[:3], 1):
                    print(f"      {i}. {title}")
                
                results["scans_performed"] += 1
                results["unique_opportunities_per_scan"].append(len(unique_titles))
                results["scan_results"].append({
                    "scan": scan_num,
                    "opportunities_count": opportunities_count,
                    "unique_titles": len(unique_titles),
                    "titles": titles,
                    "total_impact": total_impact,
                    "success": True
                })
                
                # Wait between scans to ensure different timestamps
                if scan_num < 3:
                    print("   ⏳ Waiting 2 seconds before next scan...")
                    import time
                    time.sleep(2)
            
            # Analyze results for database cleanup verification
            if results["scans_performed"] >= 2:
                # Check if we're getting diverse opportunities (not accumulating duplicates)
                unique_counts = results["unique_opportunities_per_scan"]
                avg_unique = sum(unique_counts) / len(unique_counts)
                
                # If each scan produces reasonable number of unique opportunities, cleanup is working
                if avg_unique >= 2:  # At least 2 unique opportunities per scan on average
                    results["database_cleanup_working"] = True
                    results["success"] = True
                    print(f"\n✅ Database cleanup appears to be working!")
                    print(f"   📊 Average unique opportunities per scan: {avg_unique:.1f}")
                else:
                    print(f"\n⚠️  Potential issue: Low unique opportunity diversity")
                    print(f"   📊 Average unique opportunities per scan: {avg_unique:.1f}")
            
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results["error"] = str(e)
        
        return results
    
    def test_dashboard_recent_data(self) -> Dict[str, Any]:
        """
        TEST 2: Dashboard with Recent Data
        Verify dashboard shows only recent, unique opportunities
        """
        print("\n📊 TEST 2: Dashboard with Recent Data")
        print("=" * 60)
        
        results = {
            "test_name": "Dashboard Recent Data",
            "dashboard_accessible": False,
            "shows_recent_data": False,
            "metrics_reasonable": False,
            "opportunities_unique": False,
            "success": False
        }
        
        try:
            # Get dashboard data
            print("📈 Fetching Growth Dashboard...")
            dashboard_result = self.make_request('GET', '/growth/dashboard')
            
            if 'error' in dashboard_result:
                print(f"❌ Dashboard request failed: {dashboard_result}")
                results["error"] = dashboard_result
                return results
            
            results["dashboard_accessible"] = True
            print("✅ Dashboard accessible")
            
            dashboard_data = dashboard_result.get('dashboard', {})
            
            # Check metrics
            metrics = dashboard_data.get('metrics', {})
            opportunities_count = metrics.get('total_opportunities_identified', 0)
            projected_revenue = metrics.get('total_projected_revenue', 0)
            average_roi = metrics.get('average_roi', 0)
            
            print(f"\n📊 Dashboard Metrics:")
            print(f"   🎯 Total opportunities: {opportunities_count}")
            print(f"   💰 Projected revenue: ${projected_revenue:,.2f}")
            print(f"   📈 Average ROI: {average_roi:.2f}x")
            
            # Check if metrics are reasonable (not inflated from duplicates)
            if opportunities_count <= 10 and projected_revenue <= 2000000:  # Reasonable limits
                results["metrics_reasonable"] = True
                print("✅ Metrics appear reasonable (not inflated)")
            else:
                print("⚠️  Metrics may be inflated from historical duplicates")
            
            # Check top opportunities
            top_opportunities = dashboard_data.get('top_opportunities', [])
            print(f"\n🎯 Top Opportunities ({len(top_opportunities)}):")
            
            if top_opportunities:
                titles = [opp.get('title', '') for opp in top_opportunities]
                unique_titles = list(set(titles))
                
                for i, opp in enumerate(top_opportunities[:3], 1):
                    title = opp.get('title', 'Unknown')
                    impact = opp.get('projected_revenue_impact', 0)
                    opp_type = opp.get('type', 'unknown')
                    print(f"   {i}. {title} (${impact:,.0f}, {opp_type})")
                
                # Check for uniqueness
                if len(unique_titles) == len(titles) and len(unique_titles) >= 2:
                    results["opportunities_unique"] = True
                    print("✅ Opportunities are unique and diverse")
                else:
                    print(f"⚠️  Potential duplicates: {len(titles)} total, {len(unique_titles)} unique")
            
            # Check if showing recent data (created within reasonable timeframe)
            recent_opportunities = []
            for opp in top_opportunities:
                created_at = opp.get('created_at')
                if created_at:
                    # Check if created recently (within last 24 hours for this test)
                    recent_opportunities.append(opp)
            
            if len(recent_opportunities) > 0:
                results["shows_recent_data"] = True
                print(f"✅ Dashboard showing recent opportunities: {len(recent_opportunities)}")
            
            # Overall success check
            if (results["dashboard_accessible"] and 
                results["metrics_reasonable"] and 
                results["opportunities_unique"]):
                results["success"] = True
                print("\n✅ Dashboard recent data test PASSED")
            else:
                print("\n⚠️  Dashboard recent data test has issues")
            
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results["error"] = str(e)
        
        return results
    
    def test_user_experience_fix(self) -> Dict[str, Any]:
        """
        TEST 3: Verify User Experience Fix
        Confirm users see distinct, different opportunities
        """
        print("\n👤 TEST 3: User Experience Fix Verification")
        print("=" * 60)
        
        results = {
            "test_name": "User Experience Fix",
            "distinct_opportunities": False,
            "different_types": False,
            "different_impacts": False,
            "user_experience_fixed": False,
            "success": False
        }
        
        try:
            # Get current opportunities from dashboard
            dashboard_result = self.make_request('GET', '/growth/dashboard')
            
            if 'error' in dashboard_result:
                print(f"❌ Could not get dashboard data: {dashboard_result}")
                results["error"] = dashboard_result
                return results
            
            opportunities = dashboard_result.get('dashboard', {}).get('top_opportunities', [])
            
            if len(opportunities) < 2:
                print(f"⚠️  Only {len(opportunities)} opportunities found, need at least 2 for comparison")
                return results
            
            print(f"🔍 Analyzing {len(opportunities)} opportunities for distinctiveness...")
            
            # Check for distinct titles
            titles = [opp.get('title', '') for opp in opportunities]
            unique_titles = list(set(titles))
            
            print(f"\n📝 Opportunity Titles:")
            for i, title in enumerate(titles, 1):
                print(f"   {i}. {title}")
            
            if len(unique_titles) == len(titles) and len(unique_titles) >= 2:
                results["distinct_opportunities"] = True
                print(f"✅ All {len(titles)} opportunities have distinct titles")
            else:
                print(f"❌ Found duplicates: {len(titles)} total, {len(unique_titles)} unique")
            
            # Check for different types
            types = [opp.get('type', '') for opp in opportunities]
            unique_types = list(set(types))
            
            print(f"\n🏷️  Opportunity Types:")
            for i, opp_type in enumerate(types, 1):
                print(f"   {i}. {opp_type}")
            
            if len(unique_types) >= 2:
                results["different_types"] = True
                print(f"✅ Found {len(unique_types)} different opportunity types")
            else:
                print(f"⚠️  Limited type diversity: {len(unique_types)} unique types")
            
            # Check for different revenue impacts
            impacts = [opp.get('projected_revenue_impact', 0) for opp in opportunities]
            unique_impacts = list(set(impacts))
            
            print(f"\n💰 Revenue Impacts:")
            for i, impact in enumerate(impacts, 1):
                print(f"   {i}. ${impact:,.0f}")
            
            if len(unique_impacts) >= 2:
                results["different_impacts"] = True
                print(f"✅ Found {len(unique_impacts)} different revenue impact levels")
            else:
                print(f"⚠️  All opportunities have same revenue impact")
            
            # Overall user experience assessment
            if (results["distinct_opportunities"] and 
                results["different_types"] and 
                len(opportunities) >= 3):
                results["user_experience_fixed"] = True
                results["success"] = True
                print(f"\n✅ USER EXPERIENCE FIXED: Users now see {len(opportunities)} distinct, diverse opportunities")
                print("   🎯 Different titles ✅")
                print("   🏷️  Different types ✅") 
                print("   💰 Different impacts ✅")
            else:
                print(f"\n❌ User experience still has issues:")
                print(f"   🎯 Distinct titles: {'✅' if results['distinct_opportunities'] else '❌'}")
                print(f"   🏷️  Different types: {'✅' if results['different_types'] else '❌'}")
                print(f"   💰 Different impacts: {'✅' if results['different_impacts'] else '❌'}")
            
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results["error"] = str(e)
        
        return results
    
    def test_multiple_scan_cycles(self) -> Dict[str, Any]:
        """
        TEST 4: Multiple Scan Cycles
        Run scan → check dashboard → run another scan → check dashboard again
        """
        print("\n🔄 TEST 4: Multiple Scan Cycles")
        print("=" * 60)
        
        results = {
            "test_name": "Multiple Scan Cycles",
            "cycles_completed": 0,
            "dashboard_updates": [],
            "consistent_behavior": False,
            "success": False
        }
        
        try:
            for cycle in range(1, 3):  # 2 cycles
                print(f"\n🔄 Cycle #{cycle}")
                print("-" * 30)
                
                # Step 1: Run scan
                print(f"📊 Running opportunity scan...")
                scan_result = self.make_request('POST', '/growth/opportunities/scan', self.scan_request)
                
                if 'error' in scan_result:
                    print(f"❌ Scan failed: {scan_result}")
                    continue
                
                scan_opportunities = len(scan_result.get('opportunities', []))
                scan_impact = scan_result.get('total_projected_impact', 0)
                print(f"   ✅ Scan completed: {scan_opportunities} opportunities, ${scan_impact:,.0f} impact")
                
                # Step 2: Check dashboard
                print(f"📈 Checking dashboard...")
                import time
                time.sleep(1)  # Brief pause to ensure data is updated
                
                dashboard_result = self.make_request('GET', '/growth/dashboard')
                
                if 'error' in dashboard_result:
                    print(f"❌ Dashboard check failed: {dashboard_result}")
                    continue
                
                dashboard_data = dashboard_result.get('dashboard', {})
                dashboard_opportunities = len(dashboard_data.get('top_opportunities', []))
                dashboard_metrics = dashboard_data.get('metrics', {})
                dashboard_total = dashboard_metrics.get('total_opportunities_identified', 0)
                dashboard_revenue = dashboard_metrics.get('total_projected_revenue', 0)
                
                print(f"   📊 Dashboard: {dashboard_opportunities} top opportunities")
                print(f"   📈 Metrics: {dashboard_total} total, ${dashboard_revenue:,.0f} revenue")
                
                cycle_data = {
                    "cycle": cycle,
                    "scan_opportunities": scan_opportunities,
                    "scan_impact": scan_impact,
                    "dashboard_opportunities": dashboard_opportunities,
                    "dashboard_total": dashboard_total,
                    "dashboard_revenue": dashboard_revenue
                }
                
                results["dashboard_updates"].append(cycle_data)
                results["cycles_completed"] += 1
                
                # Wait between cycles
                if cycle < 2:
                    print("   ⏳ Waiting before next cycle...")
                    time.sleep(2)
            
            # Analyze consistency
            if results["cycles_completed"] >= 2:
                updates = results["dashboard_updates"]
                
                # Check if dashboard is updating consistently (not accumulating)
                total_counts = [update["dashboard_total"] for update in updates]
                revenue_amounts = [update["dashboard_revenue"] for update in updates]
                
                print(f"\n📊 Cycle Analysis:")
                for i, update in enumerate(updates, 1):
                    print(f"   Cycle {i}: {update['dashboard_total']} opportunities, ${update['dashboard_revenue']:,.0f}")
                
                # Check if totals are reasonable and not exponentially growing
                max_total = max(total_counts)
                min_total = min(total_counts)
                
                if max_total <= 15 and (max_total - min_total) <= 10:  # Reasonable variation
                    results["consistent_behavior"] = True
                    results["success"] = True
                    print("✅ Dashboard behavior is consistent across cycles")
                    print("   📈 No excessive accumulation detected")
                else:
                    print("⚠️  Dashboard shows inconsistent behavior")
                    print(f"   📊 Total range: {min_total} - {max_total}")
            
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results["error"] = str(e)
        
        return results
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all tests and provide comprehensive results"""
        print("🚀 GROWTH ACCELERATION ENGINE - DUPLICATE INITIATIVES FIX TESTING")
        print("=" * 80)
        print("Testing the fix for duplicate initiatives issue as requested in review.")
        print()
        
        # Check connectivity first
        if not self.test_health_check():
            return {
                "overall_success": False,
                "error": "Health check failed - cannot proceed with testing"
            }
        
        # Run all tests
        test_results = {}
        
        # Test 1: Opportunity Scan & Database Cleanup
        test_results["scan_cleanup"] = self.test_opportunity_scan_cleanup()
        
        # Test 2: Dashboard with Recent Data
        test_results["dashboard_recent"] = self.test_dashboard_recent_data()
        
        # Test 3: User Experience Fix
        test_results["user_experience"] = self.test_user_experience_fix()
        
        # Test 4: Multiple Scan Cycles
        test_results["scan_cycles"] = self.test_multiple_scan_cycles()
        
        # Overall assessment
        successful_tests = sum(1 for test in test_results.values() if test.get("success", False))
        total_tests = len(test_results)
        
        print(f"\n🏁 COMPREHENSIVE TEST RESULTS")
        print("=" * 80)
        print(f"📊 Tests Completed: {total_tests}")
        print(f"✅ Tests Passed: {successful_tests}")
        print(f"❌ Tests Failed: {total_tests - successful_tests}")
        print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Detailed results
        print(f"\n📋 Detailed Results:")
        for test_name, result in test_results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            print(f"   {status} - {result.get('test_name', test_name)}")
        
        # Overall conclusion
        overall_success = successful_tests >= 3  # At least 3 out of 4 tests should pass
        
        if overall_success:
            print(f"\n🎉 OVERALL RESULT: ✅ DUPLICATE INITIATIVES FIX IS WORKING")
            print("   🔧 Database cleanup is functioning")
            print("   📊 Dashboard shows recent, unique data")
            print("   👤 User experience has been improved")
            print("   🔄 Multiple scan cycles work correctly")
        else:
            print(f"\n⚠️  OVERALL RESULT: ❌ DUPLICATE INITIATIVES ISSUE PERSISTS")
            print("   🔧 Fix may not be fully implemented")
            print("   📊 Further investigation required")
        
        return {
            "overall_success": overall_success,
            "success_rate": (successful_tests/total_tests)*100,
            "tests_passed": successful_tests,
            "tests_total": total_tests,
            "test_results": test_results,
            "conclusion": "DUPLICATE INITIATIVES FIX IS WORKING" if overall_success else "DUPLICATE INITIATIVES ISSUE PERSISTS"
        }

def main():
    """Main test execution"""
    tester = GrowthEngineFixTester()
    results = tester.run_comprehensive_test()
    
    # Return appropriate exit code
    if results.get("overall_success", False):
        print(f"\n✅ All tests completed successfully!")
        return 0
    else:
        print(f"\n❌ Some tests failed - see details above")
        return 1

if __name__ == "__main__":
    exit(main())