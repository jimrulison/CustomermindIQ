#!/usr/bin/env python3
"""
CustomerMind IQ - Celebration Flow Trial Registration Test
Testing the exact sample data from the review request to ensure frontend celebration flow works.
"""

import requests
import json
import os
from datetime import datetime
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customeriq-hub.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

def test_celebration_flow():
    """Test the exact sample data from review request"""
    print("🎉 Testing Trial Registration for Frontend Celebration Flow")
    print("=" * 60)
    
    # Exact sample data from review request
    trial_data = {
        "email": "celebrationtest@example.com",
        "first_name": "Celebration",
        "last_name": "Test",
        "company_name": "Test Company"
    }
    
    print(f"📝 Testing with sample data:")
    print(json.dumps(trial_data, indent=2))
    print()
    
    try:
        # Test the trial registration endpoint
        print("🚀 Sending POST request to /api/subscriptions/trial/register...")
        response = requests.post(
            f"{API_BASE}/subscriptions/trial/register",
            json=trial_data,
            timeout=30,
            verify=False
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            print("✅ SUCCESS - Registration completed!")
            print()
            
            # Verify required fields for frontend celebration flow
            print("🔍 Verifying required fields for celebration flow:")
            
            # 1. Check status field
            status = response_json.get("status")
            print(f"   Status: {status} {'✅' if status == 'success' else '❌'}")
            
            # 2. Check user object
            user_obj = response_json.get("user", {})
            has_user = bool(user_obj)
            print(f"   User Object: {'Present' if has_user else 'Missing'} {'✅' if has_user else '❌'}")
            
            # 3. Check password field for auto-login
            has_password = "password" in user_obj
            print(f"   Password Field: {'Present' if has_password else 'Missing'} {'✅' if has_password else '❌'}")
            
            # 4. Check trial setup
            has_trial_end = "trial_end" in response_json or "trial_end_date" in response_json
            print(f"   Trial Setup: {'Configured' if has_trial_end else 'Missing'} {'✅' if has_trial_end else '❌'}")
            
            # 5. Check message field
            has_message = "message" in response_json
            print(f"   Message Field: {'Present' if has_message else 'Missing'} {'✅' if has_message else '❌'}")
            
            print()
            print("📋 Complete Response Structure:")
            print(json.dumps(response_json, indent=2, default=str))
            
            # Verify all requirements are met
            all_requirements_met = (
                status == "success" and
                has_user and
                has_password and
                has_trial_end and
                has_message
            )
            
            print()
            if all_requirements_met:
                print("🎉 ALL REQUIREMENTS MET FOR FRONTEND CELEBRATION FLOW!")
                print("   ✅ Status: 'success'")
                print("   ✅ User object with password for auto-login")
                print("   ✅ Proper trial setup")
                print("   ✅ Message field present")
                print()
                print("🚀 Frontend can now:")
                print("   - Show celebration animation/fireworks")
                print("   - Play celebration audio")
                print("   - Auto-login user with provided credentials")
                print("   - Redirect to dashboard")
                return True
            else:
                print("❌ SOME REQUIREMENTS MISSING FOR CELEBRATION FLOW")
                return False
                
        elif response.status_code == 400:
            # Check if it's a duplicate registration (expected behavior)
            response_json = response.json()
            error_detail = response_json.get("detail", "")
            
            if "already registered" in error_detail.lower():
                print("ℹ️  DUPLICATE REGISTRATION DETECTED")
                print(f"   Details: {error_detail}")
                print("   This is expected behavior - user already exists")
                print()
                print("🔄 Testing with unique email...")
                
                # Try with unique email
                unique_trial_data = trial_data.copy()
                unique_trial_data["email"] = f"celebrationtest{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
                
                unique_response = requests.post(
                    f"{API_BASE}/subscriptions/trial/register",
                    json=unique_trial_data,
                    timeout=30,
                    verify=False
                )
                
                if unique_response.status_code == 200:
                    print("✅ SUCCESS with unique email!")
                    unique_json = unique_response.json()
                    
                    # Quick verification
                    all_good = (
                        unique_json.get("status") == "success" and
                        unique_json.get("user", {}).get("password") and
                        ("trial_end" in unique_json or "trial_end_date" in unique_json)
                    )
                    
                    if all_good:
                        print("🎉 CELEBRATION FLOW READY!")
                        return True
                    else:
                        print("❌ Missing required fields in unique registration")
                        return False
                else:
                    print(f"❌ Unique registration also failed: {unique_response.status_code}")
                    return False
            else:
                print(f"❌ Registration failed: {error_detail}")
                return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

def main():
    """Main test execution"""
    success = test_celebration_flow()
    
    print("=" * 60)
    if success:
        print("🎊 CELEBRATION FLOW TEST: PASSED")
        print("Frontend celebration with fireworks and audio will work properly!")
    else:
        print("💥 CELEBRATION FLOW TEST: FAILED")
        print("Issues detected that may prevent proper frontend celebration")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())