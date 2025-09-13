#!/usr/bin/env python3
"""
Frontend Admin Portal Access Testing

This script tests the frontend admin portal access and routing to diagnose
why the admin portal is not loading properly for authenticated admin users.

SPECIFIC TEST OBJECTIVES FROM REVIEW REQUEST:
1. **Frontend Admin Portal Access:**
   - Test if the admin portal component loads correctly
   - Verify that admin navigation is visible for admin users
   - Check if routing to admin-portal works correctly

2. **Role-Based UI Elements:**
   - Verify that admin-specific UI elements are shown
   - Check if the admin portal button appears in the header
   - Test role-based conditional rendering

3. **Frontend-Backend Integration:**
   - Test if frontend can successfully call admin endpoints
   - Verify JWT token is properly sent with admin requests
   - Check if admin data loads correctly in the frontend

The issue is that the admin portal is not loading properly - the user gets redirected 
to Customer Analytics instead of seeing the AdminPortal component.
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BACKEND_URL = "https://portal-rescue.preview.emergentagent.com"
FRONTEND_URL = "https://portal-rescue.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
ADMIN_CREDENTIALS = {
    "email": "admin@customermindiq.com",
    "password": "CustomerMindIQ2025!"
}

class FrontendAdminPortalTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        self.jwt_token = None
        self.user_profile = None
        self.test_results = []
        self.start_time = datetime.now()
        self.driver = None
        
    def setup_browser(self):
        """Setup Chrome browser for frontend testing"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in headless mode
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            
            self.log_test(
                "Browser Setup",
                True,
                "Chrome browser initialized successfully",
                {"headless": True, "window_size": "1920x1080"}
            )
            return True
            
        except Exception as e:
            self.log_test(
                "Browser Setup",
                False,
                f"Failed to setup browser: {str(e)}",
                {"error": str(e)}
            )
            return False
        
    def log_test(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        print(f"     Details: {details}")
        if response_data and isinstance(response_data, dict):
            for key, value in response_data.items():
                if key not in ['error', 'full_profile']:
                    print(f"     {key}: {value}")
        print()

    def get_jwt_token(self) -> bool:
        """Get JWT token for admin user"""
        try:
            response = self.session.post(
                f"{API_BASE}/auth/login",
                json=ADMIN_CREDENTIALS,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.jwt_token = data["access_token"]
                    self.user_profile = data.get("user", {})
                    
                    self.log_test(
                        "JWT Token Acquisition",
                        True,
                        f"JWT token obtained successfully. User role: {self.user_profile.get('role', 'NOT_FOUND')}",
                        {
                            "has_token": True,
                            "token_length": len(self.jwt_token),
                            "user_role": self.user_profile.get('role', 'NOT_FOUND')
                        }
                    )
                    return True
                else:
                    self.log_test(
                        "JWT Token Acquisition",
                        False,
                        "Login response missing access_token",
                        data
                    )
                    return False
            else:
                self.log_test(
                    "JWT Token Acquisition",
                    False,
                    f"Login failed with status {response.status_code}",
                    {"status_code": response.status_code, "response": response.text[:200]}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "JWT Token Acquisition",
                False,
                f"Login error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_frontend_login(self) -> bool:
        """Test frontend login process"""
        if not self.driver:
            return False
            
        try:
            # Navigate to the frontend
            self.driver.get(FRONTEND_URL)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check if login form is present
            try:
                email_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
                )
                password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
                
                # Fill in credentials
                email_input.clear()
                email_input.send_keys(ADMIN_CREDENTIALS["email"])
                
                password_input.clear()
                password_input.send_keys(ADMIN_CREDENTIALS["password"])
                
                # Find and click login button
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button:contains('Sign In'), button:contains('Login')")
                login_button.click()
                
                # Wait for login to complete (either redirect or dashboard load)
                time.sleep(3)
                
                # Check if we're logged in by looking for user-specific elements
                try:
                    # Look for elements that indicate successful login
                    user_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='user-menu'], .user-profile, .dashboard")
                    
                    if user_elements or "dashboard" in self.driver.current_url.lower():
                        self.log_test(
                            "Frontend Login Process",
                            True,
                            "Successfully logged in through frontend",
                            {"current_url": self.driver.current_url, "page_title": self.driver.title}
                        )
                        return True
                    else:
                        self.log_test(
                            "Frontend Login Process",
                            False,
                            "Login form submitted but no user elements found",
                            {"current_url": self.driver.current_url, "page_title": self.driver.title}
                        )
                        return False
                        
                except Exception as e:
                    self.log_test(
                        "Frontend Login Process",
                        False,
                        f"Error checking login success: {str(e)}",
                        {"current_url": self.driver.current_url, "error": str(e)}
                    )
                    return False
                    
            except TimeoutException:
                # Maybe already logged in or no login form
                if "dashboard" in self.driver.current_url.lower() or "analytics" in self.driver.current_url.lower():
                    self.log_test(
                        "Frontend Login Process",
                        True,
                        "Already logged in or redirected to dashboard",
                        {"current_url": self.driver.current_url, "page_title": self.driver.title}
                    )
                    return True
                else:
                    self.log_test(
                        "Frontend Login Process",
                        False,
                        "No login form found and not on dashboard",
                        {"current_url": self.driver.current_url, "page_title": self.driver.title}
                    )
                    return False
                    
        except Exception as e:
            self.log_test(
                "Frontend Login Process",
                False,
                f"Frontend login error: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_admin_button_visibility(self) -> bool:
        """Test if admin portal button is visible in the header"""
        if not self.driver:
            return False
            
        try:
            # Look for admin portal button or settings button
            admin_button_selectors = [
                "button[title='Admin Portal']",
                "button:contains('Admin')",
                ".admin-portal-button",
                "button[data-testid='admin-portal']",
                "a[href*='admin']",
                "button:has(svg):contains('Settings')"  # Settings icon might be admin button
            ]
            
            admin_button_found = False
            button_details = {}
            
            for selector in admin_button_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        admin_button_found = True
                        button_details[selector] = len(elements)
                        
                        # Check if button is visible
                        for element in elements:
                            if element.is_displayed():
                                button_details[f"{selector}_visible"] = True
                                break
                except:
                    continue
            
            # Also check for any buttons with admin-related text or icons
            try:
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for button in all_buttons:
                    button_text = button.get_attribute("textContent") or ""
                    button_title = button.get_attribute("title") or ""
                    if "admin" in button_text.lower() or "admin" in button_title.lower():
                        admin_button_found = True
                        button_details["text_match"] = f"Found button with text/title containing 'admin': {button_text} / {button_title}"
                        break
            except:
                pass
            
            if admin_button_found:
                self.log_test(
                    "Admin Button Visibility",
                    True,
                    "Admin portal button found in header",
                    button_details
                )
                return True
            else:
                self.log_test(
                    "Admin Button Visibility",
                    False,
                    "Admin portal button not found in header",
                    {"checked_selectors": admin_button_selectors, "page_source_length": len(self.driver.page_source)}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Button Visibility",
                False,
                f"Error checking admin button visibility: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_admin_portal_navigation(self) -> bool:
        """Test navigation to admin portal"""
        if not self.driver:
            return False
            
        try:
            # Try multiple ways to navigate to admin portal
            navigation_methods = [
                # Method 1: Direct URL
                lambda: self.driver.get(f"{FRONTEND_URL}/#admin-portal"),
                # Method 2: Hash navigation
                lambda: self.driver.execute_script("window.location.hash = '#admin-portal'"),
                # Method 3: Click admin button if found
                lambda: self.click_admin_button(),
                # Method 4: Direct URL with admin path
                lambda: self.driver.get(f"{FRONTEND_URL}/admin"),
            ]
            
            for i, method in enumerate(navigation_methods):
                try:
                    method()
                    time.sleep(2)  # Wait for navigation
                    
                    # Check if we're on admin portal
                    current_url = self.driver.current_url
                    page_title = self.driver.title
                    page_source = self.driver.page_source
                    
                    # Look for admin portal indicators
                    admin_indicators = [
                        "admin" in current_url.lower(),
                        "admin" in page_title.lower(),
                        "Admin Portal" in page_source,
                        "AdminPortal" in page_source,
                        "admin-portal" in page_source,
                        "Dashboard" in page_source and "Users" in page_source,  # Admin dashboard content
                    ]
                    
                    if any(admin_indicators):
                        self.log_test(
                            "Admin Portal Navigation",
                            True,
                            f"Successfully navigated to admin portal using method {i+1}",
                            {
                                "method": i+1,
                                "current_url": current_url,
                                "page_title": page_title,
                                "admin_indicators": [ind for ind in admin_indicators if ind]
                            }
                        )
                        return True
                        
                except Exception as method_error:
                    continue
            
            # If no method worked
            self.log_test(
                "Admin Portal Navigation",
                False,
                "Failed to navigate to admin portal using any method",
                {
                    "final_url": self.driver.current_url,
                    "final_title": self.driver.title,
                    "methods_tried": len(navigation_methods)
                }
            )
            return False
            
        except Exception as e:
            self.log_test(
                "Admin Portal Navigation",
                False,
                f"Error during admin portal navigation: {str(e)}",
                {"error": str(e)}
            )
            return False

    def click_admin_button(self):
        """Helper method to click admin button"""
        admin_button_selectors = [
            "button[title='Admin Portal']",
            "button:contains('Admin')",
            ".admin-portal-button",
            "button[data-testid='admin-portal']"
        ]
        
        for selector in admin_button_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        return
            except:
                continue
        
        # If no specific admin button found, try settings button
        try:
            settings_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button:has(svg)")
            for button in settings_buttons:
                if button.is_displayed() and "settings" in button.get_attribute("title").lower():
                    button.click()
                    return
        except:
            pass

    def test_admin_portal_content(self) -> bool:
        """Test if admin portal content loads correctly"""
        if not self.driver:
            return False
            
        try:
            # Look for admin portal specific content
            admin_content_indicators = [
                "Users",
                "Banners", 
                "Discounts",
                "Analytics",
                "Email Templates",
                "API Keys",
                "Workflows",
                "Dashboard",
                "Admin"
            ]
            
            page_source = self.driver.page_source
            found_indicators = []
            
            for indicator in admin_content_indicators:
                if indicator in page_source:
                    found_indicators.append(indicator)
            
            # Check for admin-specific UI elements
            admin_elements = []
            try:
                # Look for common admin UI elements
                tabs = self.driver.find_elements(By.CSS_SELECTOR, "[role='tab'], .tab, .nav-tab")
                buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
                
                admin_elements.extend([f"tabs: {len(tabs)}", f"buttons: {len(buttons)}", f"headings: {len(headings)}"])
                
            except:
                pass
            
            if len(found_indicators) >= 3:  # At least 3 admin indicators found
                self.log_test(
                    "Admin Portal Content Loading",
                    True,
                    f"Admin portal content loaded successfully. Found {len(found_indicators)} admin indicators",
                    {
                        "found_indicators": found_indicators,
                        "admin_elements": admin_elements,
                        "page_title": self.driver.title
                    }
                )
                return True
            else:
                self.log_test(
                    "Admin Portal Content Loading",
                    False,
                    f"Admin portal content not fully loaded. Only found {len(found_indicators)} admin indicators",
                    {
                        "found_indicators": found_indicators,
                        "admin_elements": admin_elements,
                        "page_source_length": len(page_source)
                    }
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Portal Content Loading",
                False,
                f"Error checking admin portal content: {str(e)}",
                {"error": str(e)}
            )
            return False

    def cleanup(self):
        """Cleanup browser resources"""
        if self.driver:
            try:
                self.driver.quit()
                self.log_test(
                    "Browser Cleanup",
                    True,
                    "Browser resources cleaned up successfully",
                    None
                )
            except Exception as e:
                self.log_test(
                    "Browser Cleanup",
                    False,
                    f"Error during cleanup: {str(e)}",
                    {"error": str(e)}
                )

    def run_comprehensive_test(self):
        """Run all frontend admin portal tests"""
        print("🖥️  FRONTEND ADMIN PORTAL ACCESS TESTING")
        print("=" * 60)
        print(f"Frontend URL: {FRONTEND_URL}")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Credentials: {ADMIN_CREDENTIALS['email']}")
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Test sequence
        tests = [
            ("Browser Setup", self.setup_browser),
            ("JWT Token Acquisition", self.get_jwt_token),
            ("Frontend Login Process", self.test_frontend_login),
            ("Admin Button Visibility", self.test_admin_button_visibility),
            ("Admin Portal Navigation", self.test_admin_portal_navigation),
            ("Admin Portal Content Loading", self.test_admin_portal_content),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {str(e)}", {"error": str(e)})
        
        # Cleanup
        self.cleanup()
        
        # Summary
        print("=" * 60)
        print("🎯 FRONTEND ADMIN PORTAL TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests} tests passed)")
        print()
        
        # Key findings
        print("🔍 KEY FINDINGS:")
        
        if self.user_profile:
            role = self.user_profile.get("role", "NOT_FOUND")
            print(f"• User Role: {role}")
            print(f"• Is Admin Role: {role in ['admin', 'super_admin']}")
        else:
            print("• User Profile: NOT RETRIEVED")
            
        if self.jwt_token:
            print(f"• JWT Token: PRESENT (length: {len(self.jwt_token)})")
        else:
            print("• JWT Token: MISSING")
        
        print()
        
        # Diagnosis
        print("🩺 FRONTEND ADMIN PORTAL ISSUE DIAGNOSIS:")
        
        failed_tests = [result for result in self.test_results if not result["success"]]
        
        if not failed_tests:
            print("• All frontend admin portal tests passed")
            print("• Admin portal should be accessible and working correctly")
        else:
            print("• Issues found in frontend admin portal access:")
            for failed_test in failed_tests:
                print(f"  - {failed_test['test']}: {failed_test['details']}")
        
        print()
        print("📊 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        return success_rate >= 70  # Consider successful if 70% or more tests pass

def main():
    """Main test execution"""
    tester = FrontendAdminPortalTester()
    
    try:
        success = tester.run_comprehensive_test()
        
        if success:
            print("\n🎉 FRONTEND ADMIN PORTAL TESTING COMPLETED SUCCESSFULLY")
            sys.exit(0)
        else:
            print("\n⚠️  FRONTEND ADMIN PORTAL TESTING COMPLETED WITH ISSUES")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}")
        tester.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()