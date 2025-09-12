#!/usr/bin/env python3
"""
Training Documents Backend Test
Tests basic server health and training document serving capability
"""

import requests
import sys
import json
from datetime import datetime
import time

class TrainingDocumentsBackendTester:
    def __init__(self, base_url="https://customer-iq-touch.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        
    def run_test(self, name, method, endpoint, expected_status, timeout=30):
        """Run a basic API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing: {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            else:
                print(f"   ❌ Unsupported method: {method}")
                return False
                
            print(f"   Status: {response.status_code}")
            
            if response.status_code == expected_status:
                print(f"   ✅ PASSED: {name}")
                self.tests_passed += 1
                return True
            else:
                print(f"   ❌ FAILED: Expected {expected_status}, got {response.status_code}")
                if response.text:
                    print(f"   Response: {response.text[:200]}...")
                return False
                
        except requests.exceptions.Timeout:
            print(f"   ❌ TIMEOUT: Request timed out after {timeout} seconds")
            return False
        except requests.exceptions.ConnectionError:
            print(f"   ❌ CONNECTION ERROR: Could not connect to {url}")
            return False
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            return False

    def test_health_check(self):
        """Test basic server health check"""
        print("\n" + "="*60)
        print("🏥 TESTING BACKEND HEALTH CHECK")
        print("="*60)
        
        return self.run_test(
            "Backend Health Check",
            "GET", 
            "api/health",
            200
        )

    def test_training_documents(self):
        """Test training document serving capability"""
        print("\n" + "="*60)
        print("📚 TESTING TRAINING DOCUMENT SERVING")
        print("="*60)
        
        # List of professional training documents to test
        documents = [
            "training/documents/Professional_Quick_Start_Guide.md",
            "training/documents/Website_Intelligence_Hub_Professional_User_Guide.md", 
            "training/documents/Website_Intelligence_Hub_Professional_Sales_Guide.md",
            "training/documents/Professional_Quick_Reference_Guide.md"
        ]
        
        all_passed = True
        
        for doc in documents:
            doc_name = doc.split('/')[-1]
            passed = self.run_test(
                f"Training Document: {doc_name}",
                "GET",
                doc,
                200
            )
            if not passed:
                all_passed = False
                
        return all_passed

    def run_all_tests(self):
        """Run all training document tests"""
        print("🚀 STARTING TRAINING DOCUMENTS BACKEND TESTING")
        print(f"📍 Backend URL: {self.base_url}")
        print(f"⏰ Test Started: {datetime.now()}")
        
        # Test 1: Health Check
        health_passed = self.test_health_check()
        
        # Test 2: Training Documents
        docs_passed = self.test_training_documents()
        
        # Final Results
        print("\n" + "="*60)
        print("📊 FINAL TEST RESULTS")
        print("="*60)
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if health_passed:
            print("🏥 ✅ Backend Health: HEALTHY")
        else:
            print("🏥 ❌ Backend Health: FAILED")
            
        if docs_passed:
            print("📚 ✅ Training Documents: ACCESSIBLE")
        else:
            print("📚 ❌ Training Documents: NOT ACCESSIBLE")
            
        print(f"⏰ Test Completed: {datetime.now()}")
        
        # Return overall success
        return health_passed and docs_passed

if __name__ == "__main__":
    tester = TrainingDocumentsBackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL TESTS PASSED - Backend is healthy and documents are accessible!")
        sys.exit(0)
    else:
        print("\n💥 SOME TESTS FAILED - Check the results above")
        sys.exit(1)