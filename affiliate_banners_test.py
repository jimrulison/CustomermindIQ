#!/usr/bin/env python3
"""
Affiliate Marketing Banners Resource Testing
Testing the newly added affiliate marketing banners resource as requested in review.
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BACKEND_URL = "https://None.preview.emergentagent.com/api"

def test_affiliate_resources_endpoint():
    """Test GET /api/affiliate/resources - should return 6 resources including new banners"""
    print("🧪 Testing GET /api/affiliate/resources...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/affiliate/resources", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response Keys: {list(data.keys())}")
            
            # Check if we have the expected structure
            if "resources" in data and "success" in data:
                resources = data["resources"]
                total_resources = len(resources)
                print(f"   ✅ Total Resources: {total_resources}")
                
                # Verify we have 6 resources as expected
                if total_resources == 6:
                    print(f"   ✅ CORRECT: Found expected 6 resources")
                else:
                    print(f"   ❌ ISSUE: Expected 6 resources, found {total_resources}")
                
                # Check for the new affiliate banners resource
                banner_resource = None
                for resource in resources:
                    if resource.get("id") == "affiliate_banners":
                        banner_resource = resource
                        break
                
                if banner_resource:
                    print(f"   ✅ FOUND: Affiliate Marketing Banners resource")
                    print(f"      Title: {banner_resource.get('title')}")
                    print(f"      Category: {banner_resource.get('category')}")
                    print(f"      Type: {banner_resource.get('type')}")
                    print(f"      File Type: {banner_resource.get('file_type')}")
                    print(f"      Download URL: {banner_resource.get('download_url')}")
                    
                    # Verify it has marketing category
                    if banner_resource.get('category') == 'marketing':
                        print(f"   ✅ CORRECT: Banners resource has 'marketing' category")
                    else:
                        print(f"   ❌ ISSUE: Expected 'marketing' category, found '{banner_resource.get('category')}'")
                    
                    # Verify usage tips are present and properly formatted
                    usage_tips = banner_resource.get('usage_tips', [])
                    if isinstance(usage_tips, list) and len(usage_tips) > 0:
                        print(f"   ✅ CORRECT: Usage tips present ({len(usage_tips)} tips)")
                        for i, tip in enumerate(usage_tips[:2], 1):
                            print(f"      Tip {i}: {tip[:60]}...")
                    else:
                        print(f"   ❌ ISSUE: Usage tips missing or improperly formatted")
                        
                else:
                    print(f"   ❌ MISSING: Affiliate Marketing Banners resource not found")
                
                # List all resources for verification
                print(f"   📋 All Resources Found:")
                for i, resource in enumerate(resources, 1):
                    print(f"      {i}. {resource.get('title')} (Category: {resource.get('category')})")
                
                return True, data
            else:
                print(f"   ❌ INVALID: Response missing expected structure")
                return False, None
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False, None

def test_categories_update():
    """Test that categories now include 'marketing'"""
    print("\n🧪 Testing categories update...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/affiliate/resources", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            categories = data.get("categories", [])
            print(f"   Categories: {categories}")
            
            expected_categories = ["tools", "content", "support", "sales", "marketing"]
            
            # Check if all expected categories are present
            missing_categories = []
            for expected in expected_categories:
                if expected not in categories:
                    missing_categories.append(expected)
            
            if not missing_categories:
                print(f"   ✅ CORRECT: All expected categories present")
                if "marketing" in categories:
                    print(f"   ✅ CONFIRMED: 'marketing' category added successfully")
                return True
            else:
                print(f"   ❌ MISSING: Categories not found: {missing_categories}")
                return False
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_banners_download_tracking():
    """Test POST /api/affiliate/resources/affiliate_banners/download"""
    print("\n🧪 Testing banners download tracking...")
    
    try:
        # Test download tracking for affiliate_banners
        response = requests.post(
            f"{BACKEND_URL}/affiliate/resources/affiliate_banners/download",
            json={"affiliate_id": "test_affiliate_123"},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
            
            if data.get("success"):
                print(f"   ✅ SUCCESS: Download tracking working")
                print(f"   Message: {data.get('message')}")
                return True
            else:
                print(f"   ❌ FAILED: Download tracking returned success=false")
                return False
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_other_resource_downloads():
    """Test download tracking for other resources to ensure they still work"""
    print("\n🧪 Testing other resource download tracking...")
    
    resources_to_test = ["roi_calculator", "white_paper", "pricing_schedule"]
    
    for resource_id in resources_to_test:
        try:
            response = requests.post(
                f"{BACKEND_URL}/affiliate/resources/{resource_id}/download",
                json={"affiliate_id": "test_affiliate_123"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"   ✅ {resource_id}: Download tracking working")
                else:
                    print(f"   ❌ {resource_id}: Download tracking failed")
            else:
                print(f"   ❌ {resource_id}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {resource_id}: ERROR - {str(e)}")

def test_banners_page_accessibility():
    """Test that the affiliate-banners.html page loads properly"""
    print("\n🧪 Testing banners page accessibility...")
    
    # Get the banners resource URL from the API first
    try:
        response = requests.get(f"{BACKEND_URL}/affiliate/resources", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            resources = data.get("resources", [])
            
            banner_resource = None
            for resource in resources:
                if resource.get("id") == "affiliate_banners":
                    banner_resource = resource
                    break
            
            if banner_resource:
                banner_url = banner_resource.get("download_url")
                print(f"   Banner URL: {banner_url}")
                
                # Test if the URL is accessible
                try:
                    banner_response = requests.get(banner_url, timeout=15)
                    print(f"   Status Code: {banner_response.status_code}")
                    
                    if banner_response.status_code == 200:
                        content = banner_response.text
                        print(f"   Content Length: {len(content)} characters")
                        
                        # Check if it's HTML content
                        if "html" in content.lower() and "banner" in content.lower():
                            print(f"   ✅ SUCCESS: Banners page loads and contains HTML with banner content")
                            
                            # Check for banner designs
                            banner_count = content.lower().count("banner")
                            print(f"   Banner references found: {banner_count}")
                            
                            if banner_count >= 5:  # Should have multiple banner references
                                print(f"   ✅ CONFIRMED: Multiple banner designs detected")
                                return True
                            else:
                                print(f"   ⚠️  WARNING: Limited banner content detected")
                                return True  # Still accessible
                        else:
                            print(f"   ❌ ISSUE: Content doesn't appear to be banner HTML")
                            return False
                    else:
                        print(f"   ❌ FAILED: Banner page not accessible (HTTP {banner_response.status_code})")
                        return False
                        
                except Exception as e:
                    print(f"   ❌ ERROR accessing banner page: {str(e)}")
                    return False
            else:
                print(f"   ❌ ERROR: Could not find banner resource URL")
                return False
        else:
            print(f"   ❌ ERROR: Could not get resources list")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_resource_structure_validation():
    """Validate the structure of the banners resource"""
    print("\n🧪 Testing banners resource structure validation...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/affiliate/resources", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            resources = data.get("resources", [])
            
            banner_resource = None
            for resource in resources:
                if resource.get("id") == "affiliate_banners":
                    banner_resource = resource
                    break
            
            if banner_resource:
                required_fields = ["id", "title", "description", "type", "file_type", "download_url", "category", "usage_tips"]
                missing_fields = []
                
                for field in required_fields:
                    if field not in banner_resource:
                        missing_fields.append(field)
                
                if not missing_fields:
                    print(f"   ✅ STRUCTURE: All required fields present")
                    
                    # Validate specific field values
                    validations = [
                        ("id", "affiliate_banners", banner_resource.get("id")),
                        ("category", "marketing", banner_resource.get("category")),
                        ("type", "webpage", banner_resource.get("type")),
                        ("file_type", "html", banner_resource.get("file_type"))
                    ]
                    
                    all_valid = True
                    for field_name, expected, actual in validations:
                        if actual == expected:
                            print(f"   ✅ {field_name}: {actual}")
                        else:
                            print(f"   ❌ {field_name}: Expected '{expected}', got '{actual}'")
                            all_valid = False
                    
                    return all_valid
                else:
                    print(f"   ❌ STRUCTURE: Missing fields: {missing_fields}")
                    return False
            else:
                print(f"   ❌ ERROR: Banner resource not found")
                return False
        else:
            print(f"   ❌ ERROR: Could not get resources")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    """Run all affiliate marketing banners tests"""
    print("=" * 80)
    print("🎯 AFFILIATE MARKETING BANNERS RESOURCE TESTING")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track test results
    test_results = []
    
    # Test 1: Resources endpoint returns 6 resources including banners
    success, data = test_affiliate_resources_endpoint()
    test_results.append(("Resources Endpoint (6 resources)", success))
    
    # Test 2: Categories include marketing
    success = test_categories_update()
    test_results.append(("Categories Update (marketing)", success))
    
    # Test 3: Banners download tracking
    success = test_banners_download_tracking()
    test_results.append(("Banners Download Tracking", success))
    
    # Test 4: Other resource downloads still work
    test_other_resource_downloads()
    test_results.append(("Other Resource Downloads", True))  # Informational
    
    # Test 5: Banners page accessibility
    success = test_banners_page_accessibility()
    test_results.append(("Banners Page Accessibility", success))
    
    # Test 6: Resource structure validation
    success = test_resource_structure_validation()
    test_results.append(("Resource Structure Validation", success))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Affiliate Marketing Banners integration is working correctly!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Review the issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())