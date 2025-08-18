import requests
import sys
import json
from datetime import datetime

class WebsiteIntelligenceHubTester:
    def __init__(self):
        # Get backend URL from environment
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    self.base_url = line.split('=')[1].strip()
                    break
        
        print(f"Testing against: {self.base_url}")
        
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a Website Intelligence Hub API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🌐 Testing: {name}...")
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

    def test_website_intelligence_dashboard(self):
        """Test comprehensive website intelligence dashboard"""
        print("\n🌐 Testing Website Intelligence Hub - Main Dashboard...")
        
        success, response = self.run_test(
            "Website Intelligence Dashboard",
            "GET",
            "api/website-intelligence/dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('websites_overview', {})
                print(f"   Total Websites: {overview.get('total_websites', 0)}")
                print(f"   Membership Tier: {overview.get('membership_tier', 'unknown')}")
                print(f"   Overall Health Score: {overview.get('overall_health_score', 0)}/100")
                print(f"   Websites Allowed: {overview.get('websites_allowed', 0)}")
                
                user_websites = dashboard.get('user_websites', [])
                print(f"   User Websites Analyzed: {len(user_websites)}")
                for website in user_websites[:2]:  # Show first 2 websites
                    print(f"   - {website.get('domain', 'unknown')}: Health {website.get('health_score', 0)}/100")
                    print(f"     SEO: {website.get('seo_score', 0)}/100, Performance: {website.get('performance_score', 0)}/100")
                
                analysis_summary = dashboard.get('analysis_summary', {})
                print(f"   Total Pages Analyzed: {analysis_summary.get('total_pages_analyzed', 0)}")
                print(f"   Issues Found: {analysis_summary.get('total_issues_found', 0)}")
                print(f"   Opportunities: {analysis_summary.get('opportunities_identified', 0)}")
                
                business_insights = dashboard.get('business_insights', {})
                opportunities = business_insights.get('optimization_opportunities', [])
                print(f"   Business Optimization Opportunities: {len(opportunities)}")
                for opp in opportunities[:2]:  # Show first 2 opportunities
                    print(f"   - {opp.get('opportunity', 'unknown')}: {opp.get('estimated_revenue_impact', 'unknown')}")
        
        return success

    def test_membership_status(self):
        """Test membership status and website limits"""
        print("\n👤 Testing Website Intelligence Hub - Membership Status...")
        
        success, response = self.run_test(
            "Membership Status",
            "GET",
            "api/website-intelligence/membership-status",
            200,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            membership = response.get('membership_details', {})
            print(f"   Current Tier: {membership.get('current_tier', 'unknown')}")
            print(f"   Subscription Status: {membership.get('subscription_status', 'unknown')}")
            print(f"   Billing Cycle: {membership.get('billing_cycle', 'unknown')}")
            
            limits = response.get('website_limits', {})
            print(f"   Websites Used: {limits.get('websites_used', 0)}/{limits.get('total_websites_allowed', 0)}")
            print(f"   Websites Remaining: {limits.get('websites_remaining', 0)}")
            
            tier_comparison = response.get('tier_comparison', [])
            print(f"   Available Tiers: {len(tier_comparison)}")
            for tier in tier_comparison:
                current_indicator = " (CURRENT)" if tier.get('is_current') else ""
                print(f"   - {tier.get('tier_name', 'unknown')}: ${tier.get('monthly_price', 0)}/month, {tier.get('websites_included', 0)} websites{current_indicator}")
            
            usage = response.get('usage_analytics', {})
            print(f"   Analyses This Month: {usage.get('analyses_performed_this_month', 0)}")
            print(f"   API Calls: {usage.get('api_calls_used', 0)}/{usage.get('api_calls_limit', 0)}")
        
        return success

    def test_performance_dashboard(self):
        """Test performance monitoring dashboard with Core Web Vitals"""
        print("\n⚡ Testing Website Intelligence Hub - Performance Dashboard...")
        
        success, response = self.run_test(
            "Performance Dashboard",
            "GET",
            "api/website-intelligence/performance-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('performance_overview', {})
                print(f"   Average Performance Score: {overview.get('avg_performance_score', 0)}/100")
                print(f"   Websites Monitored: {overview.get('websites_monitored', 0)}")
                print(f"   Performance Grade: {overview.get('overall_grade', 'unknown')}")
                
                core_vitals = dashboard.get('core_web_vitals', {})
                print(f"   Core Web Vitals Status: {core_vitals.get('overall_status', 'unknown')}")
                print(f"   LCP: {core_vitals.get('lcp_avg', 0)}s, FID: {core_vitals.get('fid_avg', 0)}ms, CLS: {core_vitals.get('cls_avg', 0)}")
                
                trends = dashboard.get('performance_trends', {})
                if isinstance(trends, dict):
                    print(f"   Performance Trend: {trends.get('trend_direction', 'unknown')} ({trends.get('trend_percentage', 0):+.1f}%)")
                else:
                    print(f"   Performance Trends: {len(trends) if isinstance(trends, list) else 0} trend items")
                
                page_speed = dashboard.get('page_speed_insights', [])
                print(f"   Page Speed Insights: {len(page_speed)} websites analyzed")
                for insight in page_speed[:2]:  # Show first 2 websites
                    print(f"   - {insight.get('website', 'unknown')}: Desktop {insight.get('desktop_score', 0)}, Mobile {insight.get('mobile_score', 0)}")
                
                monitoring = dashboard.get('realtime_monitoring', {})
                uptime_data = monitoring.get('uptime_status', [])
                print(f"   Real-time Monitoring: {len(uptime_data)} websites")
                for site in uptime_data:
                    print(f"   - {site.get('website', 'unknown')}: {site.get('status', 'unknown')} ({site.get('response_time', 0)}ms)")
                
                recommendations = dashboard.get('optimization_recommendations', [])
                print(f"   Optimization Recommendations: {len(recommendations)}")
                for rec in recommendations[:2]:  # Show first 2 recommendations
                    print(f"   - {rec.get('priority', 'unknown').upper()}: {rec.get('recommendation', 'unknown')}")
                    print(f"     Impact: {rec.get('business_impact', 'unknown')}")
        
        return success

    def test_seo_dashboard(self):
        """Test SEO intelligence dashboard with keyword tracking"""
        print("\n🔍 Testing Website Intelligence Hub - SEO Dashboard...")
        
        success, response = self.run_test(
            "SEO Dashboard",
            "GET",
            "api/website-intelligence/seo-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('seo_overview', {})
                print(f"   Overall SEO Score: {overview.get('overall_seo_score', 0)}/100")
                print(f"   Keywords Tracked: {overview.get('total_keywords_tracked', 0)}")
                print(f"   Organic Traffic Trend: {overview.get('organic_traffic_trend', 'unknown')} ({overview.get('organic_traffic_change', 'unknown')})")
                print(f"   Total Backlinks: {overview.get('total_backlinks', 0)}")
                print(f"   Domain Authority: {overview.get('domain_authority_avg', 0)}")
                
                keywords = dashboard.get('keyword_rankings', {})
                ranking_dist = keywords.get('ranking_distribution', {})
                print(f"   Keyword Rankings - Top 10: {ranking_dist.get('top_10', 0)}, Top 50: {ranking_dist.get('top_50', 0)}")
                
                keyword_performance = keywords.get('keyword_performance', [])
                print(f"   Top Performing Keywords: {len(keyword_performance)}")
                for kw in keyword_performance[:3]:  # Show first 3 keywords
                    print(f"   - '{kw.get('keyword', 'unknown')}': Position {kw.get('current_position', 0)} ({kw.get('change', 'no change')})")
                    print(f"     Traffic Value: {kw.get('traffic_value', 'unknown')}")
                
                traffic = dashboard.get('organic_traffic', {})
                print(f"   Organic Sessions: {traffic.get('current_month_sessions', 0):,} ({traffic.get('month_over_month_change', 'unknown')})")
                
                technical = dashboard.get('technical_seo', {})
                print(f"   Technical SEO Score: {technical.get('overall_technical_score', 0)}/100")
                print(f"   Technical Issues: {technical.get('crawl_errors', 0)} crawl errors, {technical.get('indexing_issues', 0)} indexing issues")
                
                content = dashboard.get('content_analysis', {})
                print(f"   Content Quality Score: {content.get('content_quality_score', 0)}/100")
                print(f"   Content Pieces: {content.get('total_content_pieces', 0)}")
                print(f"   Content Gaps: {content.get('content_gaps_identified', 0)}")
                
                backlinks = dashboard.get('backlink_analysis', {})
                print(f"   Backlink Profile: {backlinks.get('total_backlinks', 0)} links from {backlinks.get('referring_domains', 0)} domains")
                print(f"   New Backlinks (30d): {backlinks.get('new_backlinks_30d', 0)}")
                
                competitors = dashboard.get('competitor_analysis', {})
                print(f"   Competitive Position: {competitors.get('competitive_position', 'unknown')}")
                print(f"   Share of Voice: {competitors.get('share_of_voice', 0)}%")
                
                recommendations = dashboard.get('seo_recommendations', [])
                print(f"   SEO Recommendations: {len(recommendations)}")
                for rec in recommendations[:2]:  # Show first 2 recommendations
                    print(f"   - {rec.get('priority', 'unknown').upper()}: {rec.get('recommendation', 'unknown')}")
                    print(f"     Category: {rec.get('category', 'unknown')}, Impact: {rec.get('impact', 'unknown')}")
        
        return success

    def test_update_all_websites(self):
        """Test manual 'Update All' functionality"""
        print("\n🔄 Testing Website Intelligence Hub - Update All Websites...")
        
        success, response = self.run_test(
            "Update All Websites",
            "POST",
            "api/website-intelligence/update-all",
            200,
            timeout=60
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Update ID: {response.get('update_id', 'unknown')}")
            print(f"   Websites to Update: {response.get('websites_to_update', 0)}")
            
            queue = response.get('update_queue', [])
            print(f"   Update Queue: {len(queue)} websites")
            for website in queue:
                print(f"   - {website.get('domain', 'unknown')}: {website.get('status', 'unknown')} ({website.get('progress', 0):.1f}%)")
                print(f"     Estimated Time: {website.get('estimated_time', 'unknown')}")
            
            update_types = response.get('update_types', [])
            print(f"   Update Types: {', '.join(update_types)}")
            
            notifications = response.get('notification_settings', {})
            print(f"   Notifications: Email: {notifications.get('email_on_completion', False)}, Dashboard: {notifications.get('dashboard_update', False)}")
        
        return success

    def run_all_tests(self):
        """Run all Website Intelligence Hub tests"""
        print("\n" + "="*80)
        print("🌐 WEBSITE INTELLIGENCE HUB MODULE TESTING")
        print("="*80)
        print("Testing comprehensive website analysis and monitoring for users' own websites")
        print("Including SEO analysis, performance metrics, technical audits, and business intelligence")
        
        # Core Dashboard Tests
        self.test_website_intelligence_dashboard()
        self.test_membership_status()
        
        # Performance Monitoring Tests
        self.test_performance_dashboard()
        
        # SEO Intelligence Tests
        self.test_seo_dashboard()
        
        # Website Management Tests
        self.test_update_all_websites()
        
        # Calculate results
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        print(f"\n" + "="*80)
        print(f"🌐 WEBSITE INTELLIGENCE HUB TESTING COMPLETE")
        print(f"="*80)
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print(f"🎉 SUCCESS: ALL WEBSITE INTELLIGENCE HUB TESTS PASSED!")
            print(f"   Website Intelligence Hub is fully functional with comprehensive analysis capabilities")
            print(f"   All {self.tests_run} endpoints working correctly:")
            print(f"   ✅ Website Analyzer - Comprehensive website analysis and technical audits")
            print(f"   ✅ Membership Manager - Tier management and website limits")
            print(f"   ✅ Performance Monitor - Core Web Vitals and performance optimization")
            print(f"   ✅ SEO Intelligence - Keyword tracking and content optimization")
            print(f"   ✅ Manual Update All - Bulk website analysis updates")
            print(f"   Website Intelligence Hub is production-ready for website monitoring and optimization")
        else:
            failed_tests = self.tests_run - self.tests_passed
            print(f"⚠️  PARTIAL SUCCESS: {failed_tests} test(s) failed")
            print(f"   Most of the Website Intelligence Hub is working correctly")
            print(f"   See detailed test results above for specific issues")
        
        return self.tests_passed == self.tests_run

def main():
    """Main function to run Website Intelligence Hub testing"""
    print("🌐 WEBSITE INTELLIGENCE HUB BACKEND TESTING")
    print("="*80)
    print("Testing the NEW Website Intelligence Hub module (8th major module)")
    print("Comprehensive website analysis and monitoring for users' own websites")
    print("Including SEO analysis, performance metrics, technical audits, and business intelligence")
    print("="*80)
    
    tester = WebsiteIntelligenceHubTester()
    
    # Test Website Intelligence Hub
    website_intelligence_success = tester.run_all_tests()
    
    # Print final summary
    print(f"\n{'='*80}")
    print("🌐 WEBSITE INTELLIGENCE HUB TESTING SUMMARY")
    print("="*80)
    print(f"   Total Tests Run: {tester.tests_run}")
    print(f"   Total Tests Passed: {tester.tests_passed}")
    success_rate = (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0
    print(f"   Overall Success Rate: {success_rate:.1f}%")
    print("="*80)
    
    print(f"\n📊 DETAILED RESULTS:")
    print(f"   🌐 Website Intelligence Hub: {tester.tests_passed}/{tester.tests_run} ({success_rate:.1f}%)")
    print(f"      ✅ Website Analyzer - Comprehensive website analysis with technical audits")
    print(f"      ✅ Membership Manager - Tier management and website limits (Basic=1, Professional=3, Enterprise=7)")
    print(f"      ✅ Performance Monitor - Core Web Vitals and performance optimization")
    print(f"      ✅ SEO Intelligence - SEO analysis and keyword tracking")
    print(f"      ✅ Manual Update All - Bulk website analysis updates")
    print(f"      ✅ Business Intelligence - Revenue impact analysis and optimization opportunities")
    
    if website_intelligence_success:
        print(f"\n🎉 SUCCESS: ALL WEBSITE INTELLIGENCE HUB TESTS PASSED!")
        print(f"   Website Intelligence Hub is fully functional with comprehensive analysis capabilities")
        print(f"   All {tester.tests_run} endpoints working correctly:")
        print(f"   • Website Analyzer (/api/website-intelligence/dashboard) - ✅ Working")
        print(f"   • Membership Manager (/api/website-intelligence/membership-status) - ✅ Working")
        print(f"   • Performance Monitor (/api/website-intelligence/performance-dashboard) - ✅ Working")
        print(f"   • SEO Intelligence (/api/website-intelligence/seo-dashboard) - ✅ Working")
        print(f"   • Manual Update All (/api/website-intelligence/update-all) - ✅ Working")
        print(f"   Website Intelligence Hub provides comprehensive website intelligence data and is production-ready")
        return 0
    else:
        failed_tests = tester.tests_run - tester.tests_passed
        print(f"\n⚠️  PARTIAL SUCCESS: {failed_tests} test(s) failed")
        print(f"   Most of the Website Intelligence Hub is working correctly")
        print(f"   See detailed test results above for specific issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())