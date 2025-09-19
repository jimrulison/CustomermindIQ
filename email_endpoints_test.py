#!/usr/bin/env python3
"""
Test the correct email endpoint paths
"""

import requests
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BACKEND_URL = os.getenv("REACT_APP_BACKEND_URL", "https://customer-insights-12.preview.emergentagent.com")
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

def test_email_endpoints():
    # Get admin token
    response = requests.post(f"{API_BASE}/auth/login", json=ADMIN_CREDENTIALS, timeout=30, verify=False)
    if response.status_code != 200:
        print("❌ Admin login failed")
        return
    
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test correct email endpoint paths
    email_endpoints = [
        "/email/email/campaigns",
        "/email/email/providers/current",
        "/email/email/stats",
        "/email/email/send-simple"
    ]
    
    print("🔍 Testing correct email endpoint paths:")
    for endpoint in email_endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", headers=headers, timeout=15, verify=False)
            status = "✅ WORKING" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"   {endpoint}: {status}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"      → Returned {len(data)} items")
                elif isinstance(data, dict):
                    print(f"      → Returned data with {len(data)} fields")
        except Exception as e:
            print(f"   {endpoint}: ❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_email_endpoints()