#!/usr/bin/env python3
"""
Website Intelligence Hub Backend Testing Suite

Tests all endpoints under the '/api/website-intelligence' prefix:
- Website Analyzer endpoints (5 endpoints)
- Performance Monitor endpoints (3 endpoints) 
- SEO Intelligence endpoints (3 endpoints)
- Membership Manager endpoints (5 endpoints)

Total: 16 endpoints to test
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Get backend URL from environment
import os
sys.path.append('/app/frontend')

try:
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                BACKEND_URL = line.split('=')[1].strip()
                break
        else:
            BACKEND_URL = "https://subscription-tiers-4.preview.emergentagent.com"
except:
    BACKEND_URL = "https://subscription-tiers-4.preview.emergentagent.com"

print(f"🔗 Testing Website Intelligence Hub Backend at: {BACKEND_URL}")

class WebsiteIntelligenceHubTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def test_endpoint(self, method: str, endpoint: str, data: Dict[str, Any] = None, 
                     expected_status: int = 200, test_name: str = "") -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        self.total_tests += 1
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Check status code
            status_ok = response.status_code == expected_status
            
            # Try to parse JSON response
            try:
                response_data = response.json()
                json_valid = True
            except:
                response_data = {"error": "Invalid JSON response", "text": response.text[:500]}
                json_valid = False
            
            # Determine if test passed
            test_passed = status_ok and json_valid
            if test_passed:
                self.passed_tests += 1
            
            result = {
                "test_name": test_name or f"{method} {endpoint}",
                "method": method.upper(),
                "endpoint": endpoint,
                "url": url,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "status_ok": status_ok,
                "json_valid": json_valid,
                "test_passed": test_passed,
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            
            # Print result
            status_icon = "✅" if test_passed else "❌"
            print(f"{status_icon} {test_name}: {response.status_code} - {'PASS' if test_passed else 'FAIL'}")
            
            if not test_passed:
                print(f"   Expected: {expected_status}, Got: {response.status_code}")
                if not json_valid:
                    print(f"   JSON Error: {response_data.get('error', 'Unknown')}")
            
            return result
            
        except Exception as e:
            result = {
                "test_name": test_name or f"{method} {endpoint}",
                "method": method.upper(),
                "endpoint": endpoint,
                "url": url,
                "status_code": 0,
                "expected_status": expected_status,
                "status_ok": False,
                "json_valid": False,
                "test_passed": False,
                "response_data": {"error": str(e)},
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(result)
            print(f"❌ {test_name}: ERROR - {str(e)}")
            return result

    def run_website_analyzer_tests(self):
        """Test Website Analyzer endpoints (5 endpoints)"""
        print("\n🔍 TESTING WEBSITE ANALYZER ENDPOINTS")
        print("=" * 50)
        
        # 1. GET /api/website-intelligence/dashboard
        self.test_endpoint(
            "GET", 
            "/api/website-intelligence/dashboard",
            test_name="Website Intelligence Dashboard"
        )
        
        # 2. POST /api/website-intelligence/website/add
        website_data = {
            "domain": "example.com",
            "name": "Example Website",
            "type": "E-commerce",
            "membership_tier": "professional",
            "current_websites": 2
        }
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/add",
            data=website_data,
            test_name="Add New Website"
        )
        
        # 3. POST /api/website-intelligence/website/{website_id}/analyze
        analysis_options = {
            "type": "full",
            "depth": "comprehensive",
            "subdomains": True,
            "competitor_analysis": True
        }
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/website/web_001/analyze",
            data=analysis_options,
            test_name="Analyze Website (web_001)"
        )
        
        # 4. POST /api/website-intelligence/update-all
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/update-all",
            test_name="Update All Websites"
        )
        
        # 5. GET /api/website-intelligence/website/{website_id}/detailed-report
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/website/web_001/detailed-report",
            test_name="Detailed Website Report (web_001)"
        )

    def run_performance_monitor_tests(self):
        """Test Performance Monitor endpoints (3 endpoints)"""
        print("\n⚡ TESTING PERFORMANCE MONITOR ENDPOINTS")
        print("=" * 50)
        
        # 1. GET /api/website-intelligence/performance-dashboard
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/performance-dashboard",
            test_name="Performance Dashboard"
        )
        
        # 2. GET /api/website-intelligence/website/{website_id}/performance-report
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/website/web_001/performance-report",
            test_name="Website Performance Report (web_001)"
        )
        
        # 3. POST /api/website-intelligence/performance-test
        performance_test_data = {
            "website_id": "web_002",
            "test_type": "full",
            "locations": ["us-east", "europe"],
            "device_types": ["desktop", "mobile"]
        }
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/performance-test",
            data=performance_test_data,
            test_name="Performance Test (web_002)"
        )

    def run_seo_intelligence_tests(self):
        """Test SEO Intelligence endpoints (3 endpoints)"""
        print("\n🎯 TESTING SEO INTELLIGENCE ENDPOINTS")
        print("=" * 50)
        
        # 1. GET /api/website-intelligence/seo-dashboard
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/seo-dashboard",
            test_name="SEO Intelligence Dashboard"
        )
        
        # 2. GET /api/website-intelligence/keyword-research
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/keyword-research",
            test_name="Keyword Research"
        )
        
        # 3. POST /api/website-intelligence/content-optimization
        content_optimization_data = {
            "url": "https://example.com/premium-coffee",
            "title": "Premium Coffee Beans",
            "word_count": 340,
            "keyword": "premium coffee beans"
        }
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/content-optimization",
            data=content_optimization_data,
            test_name="Content Optimization"
        )

    def run_membership_manager_tests(self):
        """Test Membership Manager endpoints (5 endpoints)"""
        print("\n👤 TESTING MEMBERSHIP MANAGER ENDPOINTS")
        print("=" * 50)
        
        # 1. GET /api/website-intelligence/membership-status
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/membership-status",
            test_name="Membership Status"
        )
        
        # 2. POST /api/website-intelligence/upgrade-tier
        upgrade_data = {
            "new_tier": "Enterprise",
            "billing_cycle": "yearly"
        }
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/upgrade-tier",
            data=upgrade_data,
            test_name="Upgrade Membership Tier"
        )
        
        # 3. POST /api/website-intelligence/add-websites
        add_websites_data = {
            "additional_websites": 2,
            "current_tier": "Professional"
        }
        self.test_endpoint(
            "POST",
            "/api/website-intelligence/add-websites",
            data=add_websites_data,
            test_name="Purchase Additional Websites"
        )
        
        # 4. GET /api/website-intelligence/billing-history
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/billing-history",
            test_name="Billing History"
        )
        
        # 5. GET /api/website-intelligence/feature-comparison
        self.test_endpoint(
            "GET",
            "/api/website-intelligence/feature-comparison",
            test_name="Feature Comparison"
        )

    def run_all_tests(self):
        """Run all Website Intelligence Hub tests"""
        print("🚀 STARTING WEBSITE INTELLIGENCE HUB BACKEND TESTING")
        print("=" * 60)
        print(f"Backend URL: {self.base_url}")
        print(f"Test Start Time: {datetime.now().isoformat()}")
        
        # Run all test suites
        self.run_website_analyzer_tests()
        self.run_performance_monitor_tests()
        self.run_seo_intelligence_tests()
        self.run_membership_manager_tests()
        
        # Print summary
        self.print_summary()
        
        return self.results

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 WEBSITE INTELLIGENCE HUB TESTING SUMMARY")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Group results by category
        categories = {
            "Website Analyzer": [],
            "Performance Monitor": [],
            "SEO Intelligence": [],
            "Membership Manager": []
        }
        
        for result in self.results:
            test_name = result["test_name"]
            if any(x in test_name.lower() for x in ["dashboard", "add", "analyze", "update", "report"]) and "performance" not in test_name.lower() and "seo" not in test_name.lower():
                categories["Website Analyzer"].append(result)
            elif "performance" in test_name.lower():
                categories["Performance Monitor"].append(result)
            elif "seo" in test_name.lower() or "keyword" in test_name.lower() or "content" in test_name.lower():
                categories["SEO Intelligence"].append(result)
            elif any(x in test_name.lower() for x in ["membership", "upgrade", "billing", "feature"]):
                categories["Membership Manager"].append(result)
        
        print("\n📋 RESULTS BY CATEGORY:")
        for category, results in categories.items():
            if results:
                passed = sum(1 for r in results if r["test_passed"])
                total = len(results)
                rate = (passed / total * 100) if total > 0 else 0
                print(f"  {category}: {passed}/{total} ({rate:.1f}%)")
        
        # Show failed tests
        failed_tests = [r for r in self.results if not r["test_passed"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test_name']}: {test['status_code']} - {test['response_data'].get('error', 'Unknown error')}")
        
        # Show successful tests with key data
        successful_tests = [r for r in self.results if r["test_passed"]]
        if successful_tests:
            print(f"\n✅ SUCCESSFUL TESTS ({len(successful_tests)}):")
            for test in successful_tests:
                response_data = test["response_data"]
                if isinstance(response_data, dict):
                    # Extract key information from response
                    key_info = ""
                    if "status" in response_data:
                        key_info += f"Status: {response_data['status']}"
                    if "dashboard" in response_data:
                        key_info += " | Dashboard data present"
                    if "website_id" in response_data:
                        key_info += f" | Website ID: {response_data['website_id']}"
                    if "analysis_id" in response_data:
                        key_info += f" | Analysis ID: {response_data['analysis_id']}"
                    if "membership_details" in response_data:
                        tier = response_data["membership_details"].get("current_tier", "Unknown")
                        key_info += f" | Tier: {tier}"
                    
                    print(f"  • {test['test_name']}: {test['status_code']} - {key_info}")
        
        print(f"\nTest Completed: {datetime.now().isoformat()}")
        
        # Overall assessment
        if success_rate >= 90:
            print("🎉 EXCELLENT: Website Intelligence Hub backend is working excellently!")
        elif success_rate >= 75:
            print("✅ GOOD: Website Intelligence Hub backend is working well with minor issues.")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Website Intelligence Hub backend has some issues that need attention.")
        else:
            print("❌ POOR: Website Intelligence Hub backend has significant issues requiring immediate attention.")

def main():
    """Main testing function"""
    tester = WebsiteIntelligenceHubTester(BACKEND_URL)
    results = tester.run_all_tests()
    
    # Save results to file for analysis
    with open('/app/website_intelligence_test_results.json', 'w') as f:
        json.dump({
            "test_summary": {
                "total_tests": tester.total_tests,
                "passed_tests": tester.passed_tests,
                "success_rate": (tester.passed_tests / tester.total_tests * 100) if tester.total_tests > 0 else 0,
                "test_timestamp": datetime.now().isoformat()
            },
            "detailed_results": results
        }, f, indent=2, default=str)
    
    return tester.passed_tests, tester.total_tests

if __name__ == "__main__":
    passed, total = main()
    
    # Exit with appropriate code
    if passed == total:
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed