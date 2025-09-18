#!/usr/bin/env python3
"""
Affiliate Resources Media Assets Testing
Testing the updated affiliate resources endpoint to verify 4 new media assets have been added successfully.

Test Requirements:
1. GET /api/affiliate/resources - Should now return 10 total resources (6 existing + 4 new)
2. Verify the new resources are included:
   - trial_audio (7-day free trial audio.mp3)
   - growth_acceleration_video (Growth Acceleration intro slideshow.mp4) 
   - intro_brief_video (Intro brief video.mp3)
   - prompt_explanation_presentation (Prompt explanation presentation.pptx)
3. Check that the new "training" category is included
4. Test download tracking for the new resources
5. Verify all download URLs are accessible
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://customeriq-fix.preview.emergentagent.com"

class AffiliateResourcesMediaTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session = None
        self.test_results = []
        
    async def setup_session(self):
        """Setup HTTP session"""
        connector = aiohttp.TCPConnector(ssl=False)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    def log_result(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   {message}")
        if details:
            print(f"   Details: {details}")
        print()
        
    async def test_health_check(self):
        """Test backend health"""
        try:
            async with self.session.get(f"{self.backend_url}/api/health") as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_result(
                        "Backend Health Check",
                        True,
                        f"Backend is healthy: {data.get('service', 'Unknown')} v{data.get('version', 'Unknown')}",
                        {"status_code": response.status, "response": data}
                    )
                    return True
                else:
                    self.log_result(
                        "Backend Health Check",
                        False,
                        f"Backend health check failed with status {response.status}",
                        {"status_code": response.status}
                    )
                    return False
        except Exception as e:
            self.log_result(
                "Backend Health Check",
                False,
                f"Backend health check error: {str(e)}",
                {"error": str(e)}
            )
            return False
            
    async def test_affiliate_resources_endpoint(self):
        """Test GET /api/affiliate/resources endpoint"""
        try:
            async with self.session.get(f"{self.backend_url}/api/affiliate/resources") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check response structure
                    if not data.get("success"):
                        self.log_result(
                            "Affiliate Resources Endpoint",
                            False,
                            "Response indicates failure",
                            {"response": data}
                        )
                        return None
                        
                    resources = data.get("resources", [])
                    total_resources = data.get("total_resources", 0)
                    categories = data.get("categories", [])
                    
                    self.log_result(
                        "Affiliate Resources Endpoint",
                        True,
                        f"Successfully retrieved {total_resources} resources with {len(categories)} categories",
                        {
                            "total_resources": total_resources,
                            "categories": categories,
                            "resource_count": len(resources)
                        }
                    )
                    return data
                else:
                    response_text = await response.text()
                    self.log_result(
                        "Affiliate Resources Endpoint",
                        False,
                        f"Failed with status {response.status}",
                        {"status_code": response.status, "response": response_text}
                    )
                    return None
        except Exception as e:
            self.log_result(
                "Affiliate Resources Endpoint",
                False,
                f"Request error: {str(e)}",
                {"error": str(e)}
            )
            return None
            
    async def test_total_resource_count(self, resources_data: Dict):
        """Test that we have 10 total resources (6 existing + 4 new)"""
        if not resources_data:
            self.log_result(
                "Total Resource Count",
                False,
                "No resources data available for testing"
            )
            return False
            
        resources = resources_data.get("resources", [])
        total_resources = resources_data.get("total_resources", 0)
        
        expected_count = 10
        actual_count = len(resources)
        
        if actual_count == expected_count and total_resources == expected_count:
            self.log_result(
                "Total Resource Count",
                True,
                f"Correct resource count: {actual_count} resources (expected {expected_count})",
                {"expected": expected_count, "actual": actual_count, "total_resources": total_resources}
            )
            return True
        else:
            self.log_result(
                "Total Resource Count",
                False,
                f"Incorrect resource count: {actual_count} resources (expected {expected_count})",
                {"expected": expected_count, "actual": actual_count, "total_resources": total_resources}
            )
            return False
            
    async def test_new_media_resources(self, resources_data: Dict):
        """Test that the 4 new media resources are present"""
        if not resources_data:
            self.log_result(
                "New Media Resources",
                False,
                "No resources data available for testing"
            )
            return False
            
        resources = resources_data.get("resources", [])
        
        # Expected new media resources
        expected_new_resources = {
            "trial_audio": {
                "title": "7-Day Free Trial Audio",
                "file_type": "mp3",
                "type": "audio"
            },
            "growth_acceleration_video": {
                "title": "Growth Acceleration Intro Slideshow", 
                "file_type": "mp4",
                "type": "video"
            },
            "intro_brief_video": {
                "title": "Customer Mind IQ Intro Brief Video",
                "file_type": "mp4", 
                "type": "video"
            },
            "prompt_explanation_presentation": {
                "title": "AI Prompt Explanation Presentation",
                "file_type": "pptx",
                "type": "presentation"
            }
        }
        
        found_resources = {}
        missing_resources = []
        
        # Check each expected resource
        for resource in resources:
            resource_id = resource.get("id")
            if resource_id in expected_new_resources:
                expected = expected_new_resources[resource_id]
                found_resources[resource_id] = {
                    "title": resource.get("title"),
                    "file_type": resource.get("file_type"),
                    "type": resource.get("type"),
                    "category": resource.get("category"),
                    "download_url": resource.get("download_url")
                }
                
                # Verify resource properties
                title_match = resource.get("title") == expected["title"]
                file_type_match = resource.get("file_type") == expected["file_type"]
                type_match = resource.get("type") == expected["type"]
                
                if not (title_match and file_type_match and type_match):
                    self.log_result(
                        f"New Media Resource - {resource_id}",
                        False,
                        f"Resource properties mismatch",
                        {
                            "expected": expected,
                            "actual": {
                                "title": resource.get("title"),
                                "file_type": resource.get("file_type"),
                                "type": resource.get("type")
                            }
                        }
                    )
        
        # Check for missing resources
        for resource_id in expected_new_resources:
            if resource_id not in found_resources:
                missing_resources.append(resource_id)
                
        if len(found_resources) == 4 and len(missing_resources) == 0:
            self.log_result(
                "New Media Resources",
                True,
                f"All 4 new media resources found: {', '.join(found_resources.keys())}",
                {"found_resources": found_resources}
            )
            return True
        else:
            self.log_result(
                "New Media Resources", 
                False,
                f"Missing or incorrect media resources. Found: {len(found_resources)}, Missing: {missing_resources}",
                {"found_resources": found_resources, "missing_resources": missing_resources}
            )
            return False
            
    async def test_training_category(self, resources_data: Dict):
        """Test that the new 'training' category is included"""
        if not resources_data:
            self.log_result(
                "Training Category",
                False,
                "No resources data available for testing"
            )
            return False
            
        categories = resources_data.get("categories", [])
        
        if "training" in categories:
            # Also check if any resource uses the training category
            resources = resources_data.get("resources", [])
            training_resources = [r for r in resources if r.get("category") == "training"]
            
            self.log_result(
                "Training Category",
                True,
                f"Training category found with {len(training_resources)} resources",
                {"categories": categories, "training_resources": len(training_resources)}
            )
            return True
        else:
            self.log_result(
                "Training Category",
                False,
                f"Training category not found in categories: {categories}",
                {"categories": categories}
            )
            return False
            
    async def test_download_tracking(self, resources_data: Dict):
        """Test download tracking for the new resources"""
        if not resources_data:
            self.log_result(
                "Download Tracking",
                False,
                "No resources data available for testing"
            )
            return False
            
        new_resource_ids = ["trial_audio", "growth_acceleration_video", "intro_brief_video", "prompt_explanation_presentation"]
        successful_tracking = 0
        
        for resource_id in new_resource_ids:
            try:
                # Test download tracking endpoint
                tracking_data = {
                    "affiliate_id": "test_affiliate_media"
                }
                
                async with self.session.post(
                    f"{self.backend_url}/api/affiliate/resources/{resource_id}/download",
                    json=tracking_data
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            successful_tracking += 1
                            self.log_result(
                                f"Download Tracking - {resource_id}",
                                True,
                                f"Download tracking successful: {data.get('message')}",
                                {"resource_id": resource_id, "response": data}
                            )
                        else:
                            self.log_result(
                                f"Download Tracking - {resource_id}",
                                False,
                                f"Download tracking failed: {data.get('message')}",
                                {"resource_id": resource_id, "response": data}
                            )
                    else:
                        response_text = await response.text()
                        self.log_result(
                            f"Download Tracking - {resource_id}",
                            False,
                            f"Download tracking failed with status {response.status}",
                            {"resource_id": resource_id, "status_code": response.status, "response": response_text}
                        )
            except Exception as e:
                self.log_result(
                    f"Download Tracking - {resource_id}",
                    False,
                    f"Download tracking error: {str(e)}",
                    {"resource_id": resource_id, "error": str(e)}
                )
                
        if successful_tracking == len(new_resource_ids):
            self.log_result(
                "Download Tracking Summary",
                True,
                f"All {successful_tracking} new resources have working download tracking",
                {"successful_tracking": successful_tracking, "total_tested": len(new_resource_ids)}
            )
            return True
        else:
            self.log_result(
                "Download Tracking Summary",
                False,
                f"Only {successful_tracking}/{len(new_resource_ids)} resources have working download tracking",
                {"successful_tracking": successful_tracking, "total_tested": len(new_resource_ids)}
            )
            return False
            
    async def test_download_urls_accessibility(self, resources_data: Dict):
        """Test that all download URLs are accessible"""
        if not resources_data:
            self.log_result(
                "Download URLs Accessibility",
                False,
                "No resources data available for testing"
            )
            return False
            
        resources = resources_data.get("resources", [])
        new_resource_ids = ["trial_audio", "growth_acceleration_video", "intro_brief_video", "prompt_explanation_presentation"]
        
        accessible_urls = 0
        total_urls = 0
        
        for resource in resources:
            if resource.get("id") in new_resource_ids:
                total_urls += 1
                download_url = resource.get("download_url")
                
                if not download_url:
                    self.log_result(
                        f"URL Accessibility - {resource.get('id')}",
                        False,
                        "No download URL provided",
                        {"resource_id": resource.get("id")}
                    )
                    continue
                    
                try:
                    # Test URL accessibility with HEAD request
                    async with self.session.head(download_url) as response:
                        if response.status in [200, 302, 301]:  # Allow redirects
                            accessible_urls += 1
                            self.log_result(
                                f"URL Accessibility - {resource.get('id')}",
                                True,
                                f"Download URL accessible (status {response.status})",
                                {"resource_id": resource.get("id"), "url": download_url, "status_code": response.status}
                            )
                        else:
                            self.log_result(
                                f"URL Accessibility - {resource.get('id')}",
                                False,
                                f"Download URL not accessible (status {response.status})",
                                {"resource_id": resource.get("id"), "url": download_url, "status_code": response.status}
                            )
                except Exception as e:
                    self.log_result(
                        f"URL Accessibility - {resource.get('id')}",
                        False,
                        f"URL accessibility test error: {str(e)}",
                        {"resource_id": resource.get("id"), "url": download_url, "error": str(e)}
                    )
                    
        if accessible_urls == total_urls and total_urls > 0:
            self.log_result(
                "Download URLs Accessibility Summary",
                True,
                f"All {accessible_urls} new resource URLs are accessible",
                {"accessible_urls": accessible_urls, "total_urls": total_urls}
            )
            return True
        else:
            self.log_result(
                "Download URLs Accessibility Summary",
                False,
                f"Only {accessible_urls}/{total_urls} new resource URLs are accessible",
                {"accessible_urls": accessible_urls, "total_urls": total_urls}
            )
            return False
            
    async def run_all_tests(self):
        """Run all affiliate resources media tests"""
        print("🎯 AFFILIATE RESOURCES MEDIA ASSETS TESTING")
        print("=" * 60)
        print(f"Backend URL: {self.backend_url}")
        print(f"Test Started: {datetime.now().isoformat()}")
        print()
        
        await self.setup_session()
        
        try:
            # Test 1: Health Check
            health_ok = await self.test_health_check()
            if not health_ok:
                print("❌ Backend health check failed. Stopping tests.")
                return
                
            # Test 2: Get affiliate resources
            resources_data = await self.test_affiliate_resources_endpoint()
            if not resources_data:
                print("❌ Could not retrieve affiliate resources. Stopping tests.")
                return
                
            # Test 3: Verify total resource count (10 resources)
            await self.test_total_resource_count(resources_data)
            
            # Test 4: Verify new media resources are present
            await self.test_new_media_resources(resources_data)
            
            # Test 5: Verify training category is included
            await self.test_training_category(resources_data)
            
            # Test 6: Test download tracking for new resources
            await self.test_download_tracking(resources_data)
            
            # Test 7: Test download URLs accessibility
            await self.test_download_urls_accessibility(resources_data)
            
        finally:
            await self.cleanup_session()
            
        # Print summary
        return self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
                    
        print(f"\nTest Completed: {datetime.now().isoformat()}")
        
        # Return success status
        return failed_tests == 0

async def main():
    """Main test function"""
    tester = AffiliateResourcesMediaTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Affiliate resources media assets are working correctly.")
        sys.exit(0)
    else:
        print("\n💥 SOME TESTS FAILED! Check the summary above for details.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())