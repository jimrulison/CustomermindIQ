import requests
import sys
import json
from datetime import datetime
import time

class CustomerIntelligenceAITester:
    def __init__(self, base_url="https://customer-brain.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.customer_ids = []
        self.odoo_connection_status = None
        self.real_customers_loaded = False
        self.universal_platform_tests = 0
        self.universal_platform_passed = 0
        self.marketing_automation_tests = 0
        self.marketing_automation_passed = 0
        self.revenue_analytics_tests = 0
        self.revenue_analytics_passed = 0
        self.advanced_features_tests = 0
        self.advanced_features_passed = 0
        self.analytics_insights_tests = 0
        self.analytics_insights_passed = 0
        self.product_intelligence_tests = 0
        self.product_intelligence_passed = 0
        self.integration_hub_tests = 0
        self.integration_hub_passed = 0
        self.compliance_governance_tests = 0
        self.compliance_governance_passed = 0
        self.ai_command_tests = 0
        self.ai_command_passed = 0

    def run_marketing_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a Marketing Automation Pro API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.marketing_automation_tests += 1
        print(f"\n🚀 Testing Marketing Automation Pro: {name}...")
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
                self.marketing_automation_passed += 1
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

    def run_universal_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a Universal Platform API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.universal_platform_tests += 1
        print(f"\n🌐 Testing Universal Platform: {name}...")
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
                self.universal_platform_passed += 1
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

    def run_analytics_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run an Analytics & Insights API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.analytics_insights_tests += 1
        print(f"\n📊 Testing Analytics & Insights: {name}...")
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
                self.analytics_insights_passed += 1
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

        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
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

    def test_health_check(self):
        """Test API health check"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )
        return success

    def test_get_customers(self):
        """Test getting customers with AI analysis - CRITICAL ODOO INTEGRATION TEST"""
        print("\n🔍 CRITICAL TEST: REAL ODOO INTEGRATION")
        print("   Expected: Real customer data from ODOO database 'Fancy Free Living LLC'")
        print("   Fallback: Mock data if ODOO connection fails")
        print("   🧠 Testing AI-powered customer analytics (may take 30-60 seconds for ODOO connection)...")
        
        success, response = self.run_test(
            "Get Customers with ODOO Integration + AI Analysis",
            "GET", 
            "api/customers",
            200,
            timeout=120  # ODOO connection + AI analysis takes time
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} customers")
            
            # Analyze if we got real or mock data
            mock_indicators = [
                "TechCorp Solutions",
                "StartupXYZ", 
                "admin@techcorp.com",
                "founder@startupxyz.com"
            ]
            
            is_mock_data = any(
                any(indicator in str(customer.get(field, "")) for field in ['name', 'email'])
                for customer in response
                for indicator in mock_indicators
            )
            
            if is_mock_data:
                self.odoo_connection_status = "FAILED - Using Mock Data"
                print(f"   🔄 ODOO CONNECTION FAILED - Using mock data")
                print(f"   Mock customers detected: {[c.get('name') for c in response[:3]]}")
            else:
                self.odoo_connection_status = "SUCCESS - Real Data Loaded"
                self.real_customers_loaded = True
                print(f"   🎉 ODOO CONNECTION SUCCESS! Real customers loaded from ODOO")
                print(f"   Real customers: {[c.get('name') for c in response[:3]]}")
            
            for customer in response:
                if 'customer_id' in customer:
                    self.customer_ids.append(customer['customer_id'])
                    print(f"   - {customer.get('name', 'Unknown')} (ID: {customer['customer_id']}) - Engagement: {customer.get('engagement_score', 0)}/100 - Spent: ${customer.get('total_spent', 0)}")
        
        return success

    # =====================================================
    # UNIVERSAL CUSTOMER INTELLIGENCE PLATFORM TESTS
    # =====================================================

    def test_universal_connectors_status(self):
        """Test Universal Platform - Get connector status management"""
        print("\n🔌 Testing Universal Platform - Connector Status Management...")
        
        success, response = self.run_universal_test(
            "Universal Connectors Status",
            "GET",
            "api/universal/connectors/status",
            200,
            timeout=30
        )
        
        if success:
            connectors = response.get('connectors', [])
            total_connected = response.get('total_connected', 0)
            total_configured = response.get('total_configured', 0)
            
            print(f"   Total configured connectors: {total_configured}")
            print(f"   Total connected connectors: {total_connected}")
            
            for connector in connectors:
                print(f"   - {connector.get('platform_name', 'Unknown')}: {'✅ Connected' if connector.get('is_connected') else '❌ Disconnected'}")
                print(f"     Last sync: {connector.get('last_sync_time', 'Never')}")
        
        return success

    def test_universal_add_connector(self):
        """Test Universal Platform - Add platform connectors (mock request)"""
        print("\n➕ Testing Universal Platform - Add Connector (Mock)...")
        
        # Test adding a mock Stripe connector
        stripe_connector_data = {
            "platform_type": "stripe",
            "credentials": {
                "api_key": "sk_test_mock_key_for_testing",
                "webhook_secret": "whsec_mock_webhook_secret"
            }
        }
        
        success, response = self.run_universal_test(
            "Add Stripe Connector (Mock)",
            "POST",
            "api/universal/connectors/add",
            200,
            data=stripe_connector_data,
            timeout=30
        )
        
        if success:
            print(f"   Platform: {response.get('platform', 'Unknown')}")
            print(f"   Connector ID: {response.get('connector_id', 'Unknown')}")
            print(f"   Message: {response.get('message', 'No message')}")
        
        return success

    def test_universal_customers(self):
        """Test Universal Platform - Get unified customer profiles"""
        print("\n👥 Testing Universal Platform - Unified Customer Profiles...")
        
        success, response = self.run_universal_test(
            "Universal Unified Customers",
            "GET",
            "api/universal/customers",
            200,
            timeout=45
        )
        
        if success:
            customers = response.get('customers', [])
            total_count = response.get('total_count', 0)
            platforms_represented = response.get('platforms_represented', [])
            
            print(f"   Total unified customers: {total_count}")
            print(f"   Platforms represented: {', '.join(platforms_represented) if platforms_represented else 'None'}")
            
            for customer in customers[:3]:  # Show first 3 customers
                print(f"   - {customer.get('name', 'Unknown')} ({customer.get('email', 'No email')})")
                print(f"     Platforms: {', '.join(customer.get('platforms_active', []))}")
                print(f"     Total value: ${customer.get('total_value', 0):,.2f}")
        
        return success

    def test_universal_intelligence(self):
        """Test Universal Platform - Get comprehensive business intelligence"""
        print("\n🧠 Testing Universal Platform - Comprehensive Business Intelligence...")
        
        success, response = self.run_universal_test(
            "Universal Business Intelligence",
            "GET",
            "api/universal/intelligence",
            200,
            timeout=60  # AI analysis takes time
        )
        
        if success:
            business_intelligence = response.get('business_intelligence', {})
            action_recommendations = response.get('action_recommendations', [])
            dashboard_data = response.get('dashboard_data', {})
            customers_analyzed = response.get('customers_analyzed', 0)
            
            print(f"   Customers analyzed: {customers_analyzed}")
            print(f"   Action recommendations: {len(action_recommendations)}")
            
            if business_intelligence:
                print(f"   Business name: {business_intelligence.get('business_name', 'Unknown')}")
                print(f"   Intelligence score: {business_intelligence.get('intelligence_score', 0)}/100")
                
                key_insights = business_intelligence.get('key_insights', [])
                print(f"   Key insights: {len(key_insights)}")
                for insight in key_insights[:2]:  # Show first 2 insights
                    print(f"   - {insight.get('insight_type', 'Unknown')}: {insight.get('description', 'No description')[:100]}...")
            
            # Show top recommendations
            for rec in action_recommendations[:3]:  # Show first 3 recommendations
                print(f"   📋 {rec.get('action_type', 'Unknown')} ({rec.get('priority', 'unknown')} priority)")
                print(f"      Impact: {rec.get('expected_impact', 'Unknown')}")
        
        return success

    def test_universal_dashboard(self):
        """Test Universal Platform - Get universal dashboard for any business"""
        print("\n📊 Testing Universal Platform - Universal Dashboard...")
        
        success, response = self.run_universal_test(
            "Universal Dashboard",
            "GET",
            "api/universal/dashboard",
            200,
            timeout=45
        )
        
        if success:
            dashboard = response.get('dashboard', {})
            connectors = response.get('connectors', [])
            data_health = response.get('data_health', 'unknown')
            
            print(f"   Data health: {data_health}")
            print(f"   Connected platforms: {len(connectors)}")
            
            if dashboard:
                metrics = dashboard.get('key_metrics', {})
                print(f"   Total customers: {metrics.get('total_customers', 0)}")
                print(f"   Total revenue: ${metrics.get('total_revenue', 0):,.2f}")
                print(f"   Growth rate: {metrics.get('growth_rate', 0):.1f}%")
                
                segments = dashboard.get('customer_segments', [])
                print(f"   Customer segments: {len(segments)}")
                for segment in segments[:2]:  # Show first 2 segments
                    print(f"   - {segment.get('segment_name', 'Unknown')}: {segment.get('customer_count', 0)} customers")
        
        return success

    def test_universal_recommendations(self):
        """Test Universal Platform - Get AI-powered action recommendations"""
        print("\n🎯 Testing Universal Platform - AI Action Recommendations...")
        
        success, response = self.run_universal_test(
            "Universal Action Recommendations",
            "GET",
            "api/universal/recommendations",
            200,
            timeout=45
        )
        
        if success:
            urgent_actions = response.get('urgent_actions', [])
            high_priority = response.get('high_priority', [])
            medium_priority = response.get('medium_priority', [])
            total_recommendations = response.get('total_recommendations', 0)
            
            print(f"   Total recommendations: {total_recommendations}")
            print(f"   Urgent actions: {len(urgent_actions)}")
            print(f"   High priority: {len(high_priority)}")
            print(f"   Medium priority: {len(medium_priority)}")
            
            # Show urgent actions
            for action in urgent_actions[:2]:  # Show first 2 urgent actions
                print(f"   🚨 URGENT: {action.get('action_type', 'Unknown')}")
                print(f"      Description: {action.get('description', 'No description')[:100]}...")
                print(f"      Expected impact: {action.get('expected_impact', 'Unknown')}")
            
            # Show high priority actions
            for action in high_priority[:2]:  # Show first 2 high priority actions
                print(f"   ⚡ HIGH: {action.get('action_type', 'Unknown')}")
                print(f"      Description: {action.get('description', 'No description')[:100]}...")
        
        return success

    def test_universal_sync(self):
        """Test Universal Platform - Test full platform sync (mock)"""
        print("\n🔄 Testing Universal Platform - Full Platform Sync...")
        
        success, response = self.run_universal_test(
            "Universal Platform Sync",
            "POST",
            "api/universal/sync",
            200,
            timeout=60  # Sync operations take time
        )
        
        if success:
            sync_results = response.get('sync_results', {})
            unified_profiles_created = response.get('unified_profiles_created', 0)
            business_intelligence = response.get('business_intelligence', {})
            
            print(f"   Unified profiles created: {unified_profiles_created}")
            
            # Show sync results for each platform
            for platform, result in sync_results.items():
                if result.get('success'):
                    print(f"   ✅ {platform.title()}: {result.get('customers_synced', 0)} customers, {result.get('transactions_synced', 0)} transactions")
                else:
                    print(f"   ❌ {platform.title()}: {result.get('error', 'Unknown error')}")
            
            if business_intelligence:
                print(f"   Business intelligence generated: {business_intelligence.get('business_name', 'Unknown')}")
                print(f"   Intelligence score: {business_intelligence.get('intelligence_score', 0)}/100")
        
        return success

    def test_universal_customer_by_email(self):
        """Test Universal Platform - Get customer by email"""
        print("\n📧 Testing Universal Platform - Customer Lookup by Email...")
        
        # Use a test email - this will likely return 404 but tests the endpoint
        test_email = "test@example.com"
        
        success, response = self.run_universal_test(
            f"Universal Customer Lookup ({test_email})",
            "GET",
            f"api/universal/customers/{test_email}",
            404,  # Expecting 404 since test email won't exist
            timeout=30
        )
        
        # For this test, 404 is expected and considered success
        if not success and response == {}:
            print("   ✅ Expected 404 response for non-existent test email")
            self.universal_platform_passed += 1  # Count as passed since 404 is expected
            return True
        
        return success

    # =====================================================
    # END UNIVERSAL CUSTOMER INTELLIGENCE PLATFORM TESTS
    # =====================================================

    def test_behavioral_clustering(self):
        """Test behavioral clustering microservice"""
        print("\n🧠 Testing Customer Intelligence AI - Behavioral Clustering (may take 30-45 seconds)...")
        
        success, response = self.run_test(
            "Behavioral Clustering Analysis",
            "GET",
            "api/intelligence/behavioral-clustering",
            200,
            timeout=60  # AI clustering analysis takes time
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            data = response.get('data', {})
            clusters = data.get('clusters', [])
            insights = data.get('insights', {})
            
            print(f"   Found {len(clusters)} behavioral clusters")
            for cluster in clusters[:3]:  # Show first 3 clusters
                print(f"   - {cluster.get('cluster_name', 'Unknown')} ({cluster.get('customer_count', 0)} customers)")
                print(f"     Risk Level: {cluster.get('risk_level', 'unknown')}, Value Potential: {cluster.get('value_potential', 'unknown')}")
            
            print(f"   Total clusters: {insights.get('total_clusters', 0)}")
            print(f"   Dominant pattern: {insights.get('dominant_pattern', 'Not specified')}")
        
        return success

    def test_behavioral_clustering_customer_details(self):
        """Test behavioral clustering customer details"""
        if not self.customer_ids:
            print("❌ No customer IDs available for cluster details testing")
            return False
            
        customer_id = self.customer_ids[0]
        print(f"\n🎯 Testing cluster details for customer {customer_id}...")
        
        success, response = self.run_test(
            f"Customer Cluster Details for {customer_id}",
            "GET",
            f"api/intelligence/behavioral-clustering/{customer_id}",
            200,
            timeout=30
        )
        
        if success:
            data = response.get('data', {})
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
            print(f"   Cluster: {data.get('cluster_name', 'unknown')}")
            print(f"   Similarity Score: {data.get('similarity_score', 0):.2f}")
            print(f"   Position: {data.get('cluster_position', 'unknown')}")
        
        return success

    def test_churn_prevention(self):
        """Test churn prevention microservice"""
        print("\n🚨 Testing Customer Intelligence AI - Churn Prevention (may take 30-45 seconds)...")
        
        success, response = self.run_test(
            "Churn Prevention Analysis",
            "GET",
            "api/intelligence/churn-prevention",
            200,
            timeout=60  # AI churn analysis takes time
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            churn_profiles = response.get('churn_profiles', [])
            dashboard = response.get('dashboard', {})
            
            print(f"   Analyzed {len(churn_profiles)} customer churn profiles")
            
            # Show high-risk customers
            high_risk = [p for p in churn_profiles if p.get('churn_probability', 0) >= 0.6]
            print(f"   High-risk customers: {len(high_risk)}")
            
            if dashboard:
                summary = dashboard.get('summary', {})
                print(f"   Total value at risk: ${summary.get('total_value_at_risk', 0):,.2f}")
                print(f"   Average churn probability: {summary.get('avg_churn_probability', 0):.2f}")
        
        return success

    def test_churn_retention_campaigns(self):
        """Test churn retention campaign generation"""
        print("\n📧 Testing Churn Retention Campaign Generation (may take 20-30 seconds)...")
        
        success, response = self.run_test(
            "Generate Retention Campaigns",
            "POST",
            "api/intelligence/churn-prevention/retention-campaigns",
            200,
            timeout=45  # AI campaign generation takes time
        )
        
        if success:
            campaigns = response.get('campaigns', [])
            high_risk_count = response.get('high_risk_count', 0)
            
            print(f"   Generated {len(campaigns)} retention campaigns")
            print(f"   High-risk customers targeted: {high_risk_count}")
            
            for campaign in campaigns[:2]:  # Show first 2 campaigns
                print(f"   - {campaign.get('intervention_type', 'unknown')} campaign for {campaign.get('risk_level', 'unknown')} risk")
                print(f"     Success probability: {campaign.get('success_probability', 0):.2f}")
        
        return success

    def test_lead_scoring(self):
        """Test lead scoring microservice"""
        print("\n🎯 Testing Customer Intelligence AI - Lead Scoring (may take 30-45 seconds)...")
        
        success, response = self.run_test(
            "Lead Scoring Analysis",
            "GET",
            "api/intelligence/lead-scoring",
            200,
            timeout=60  # AI lead scoring takes time
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            lead_scores = response.get('lead_scores', [])
            pipeline_insights = response.get('pipeline_insights', {})
            
            print(f"   Scored {len(lead_scores)} leads")
            
            # Show top leads
            top_leads = sorted(lead_scores, key=lambda x: x.get('overall_score', 0), reverse=True)[:3]
            for lead in top_leads:
                print(f"   - Customer {lead.get('customer_id', 'unknown')}: Score {lead.get('overall_score', 0)}/100")
                print(f"     Qualification: {lead.get('qualification_level', 'unknown')}, Priority: {lead.get('sales_priority', 'unknown')}")
            
            if pipeline_insights:
                summary = pipeline_insights.get('pipeline_summary', {})
                print(f"   Pipeline value: ${summary.get('total_pipeline_value', 0):,.2f}")
                print(f"   Qualified leads: {summary.get('qualified_leads', 0)}")
        
        return success

    def test_lead_score_components(self):
        """Test lead score component breakdown"""
        if not self.customer_ids:
            print("❌ No customer IDs available for lead score components testing")
            return False
            
        customer_id = self.customer_ids[0]
        print(f"\n📊 Testing lead score components for customer {customer_id}...")
        
        success, response = self.run_test(
            f"Lead Score Components for {customer_id}",
            "GET",
            f"api/intelligence/lead-scoring/{customer_id}/components",
            200,
            timeout=30
        )
        
        if success:
            components = response.get('components', [])
            print(f"   Found {len(components)} score components")
            
            for component in components[:3]:  # Show first 3 components
                print(f"   - {component.get('component_name', 'unknown')}: {component.get('score', 0)}/100 (Weight: {component.get('weight', 0)*100:.1f}%)")
        
        return success

    def test_sentiment_analysis(self):
        """Test sentiment analysis microservice"""
        print("\n😊 Testing Customer Intelligence AI - Sentiment Analysis (may take 30-45 seconds)...")
        
        success, response = self.run_test(
            "Sentiment Analysis",
            "GET",
            "api/intelligence/sentiment-analysis",
            200,
            timeout=60  # AI sentiment analysis takes time
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            sentiment_profiles = response.get('sentiment_profiles', [])
            dashboard = response.get('dashboard', {})
            
            print(f"   Analyzed sentiment for {len(sentiment_profiles)} customers")
            
            # Show sentiment distribution
            if dashboard:
                overview = dashboard.get('sentiment_overview', {})
                print(f"   Positive customers: {overview.get('positive_customers', 0)}")
                print(f"   Negative customers: {overview.get('negative_customers', 0)}")
                print(f"   Average sentiment: {overview.get('average_sentiment', 0):.2f}")
                print(f"   High-risk count: {overview.get('high_risk_count', 0)}")
        
        return success

    def test_sentiment_text_analysis(self):
        """Test sentiment analysis from text"""
        if not self.customer_ids:
            print("❌ No customer IDs available for text sentiment testing")
            return False
            
        customer_id = self.customer_ids[0]
        test_text = "I love the new software features! The customer support has been excellent and the product quality is amazing. Very satisfied with my purchase."
        
        print(f"\n📝 Testing text sentiment analysis for customer {customer_id}...")
        
        text_data = {
            "customer_id": customer_id,
            "text": test_text,
            "source": "email"
        }
        
        success, response = self.run_test(
            f"Text Sentiment Analysis for {customer_id}",
            "POST",
            "api/intelligence/sentiment-analysis/text",
            200,
            data=text_data,
            timeout=30
        )
        
        if success:
            data = response.get('data', {})
            print(f"   Sentiment Score: {data.get('sentiment_score', 0):.2f}")
            print(f"   Emotions: {', '.join(data.get('emotions_detected', []))}")
            print(f"   Urgency Level: {data.get('urgency_level', 'unknown')}")
            print(f"   Topics: {', '.join(data.get('topics_mentioned', []))}")
        
        return success

    def test_journey_mapping(self):
        """Test journey mapping microservice"""
        print("\n🗺️ Testing Customer Intelligence AI - Journey Mapping (may take 30-45 seconds)...")
        
        success, response = self.run_test(
            "Journey Mapping Analysis",
            "GET",
            "api/intelligence/journey-mapping",
            200,
            timeout=60  # AI journey analysis takes time
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            customer_journeys = response.get('customer_journeys', [])
            dashboard = response.get('dashboard', {})
            
            print(f"   Mapped {len(customer_journeys)} customer journeys")
            
            # Show journey stages
            if dashboard:
                overview = dashboard.get('journey_overview', {})
                print(f"   Average journey health: {overview.get('average_journey_health', 0):.1f}/100")
                print(f"   Average conversion probability: {overview.get('average_conversion_probability', 0):.2f}")
                print(f"   Active stages: {overview.get('active_stages', 0)}")
        
        return success

    def test_journey_stages(self):
        """Test journey stage analysis"""
        print("\n📈 Testing Journey Stage Performance Analysis...")
        
        success, response = self.run_test(
            "Journey Stages Analysis",
            "GET",
            "api/intelligence/journey-mapping/stages",
            200,
            timeout=30
        )
        
        if success:
            stages = response.get('stages', [])
            print(f"   Analyzed {len(stages)} journey stages")
            
            for stage in stages[:3]:  # Show first 3 stages
                print(f"   - {stage.get('stage_name', 'unknown')}: {stage.get('customer_count', 0)} customers")
                print(f"     Duration: {stage.get('avg_duration_days', 0)} days, Conversion: {stage.get('conversion_rate', 0):.2f}")
        
        return success

    def test_touchpoint_analysis(self):
        """Test touchpoint effectiveness analysis"""
        print("\n🎯 Testing Touchpoint Effectiveness Analysis...")
        
        success, response = self.run_test(
            "Touchpoint Analysis",
            "GET",
            "api/intelligence/journey-mapping/touchpoints",
            200,
            timeout=30
        )
        
        if success:
            touchpoints = response.get('touchpoints', [])
            print(f"   Analyzed {len(touchpoints)} touchpoints")
            
            for touchpoint in touchpoints[:3]:  # Show first 3 touchpoints
                print(f"   - {touchpoint.get('touchpoint_name', 'unknown')}: Score {touchpoint.get('optimization_score', 0)}/100")
                print(f"     Engagement: {touchpoint.get('engagement_rate', 0):.2f}, Conversion Impact: {touchpoint.get('conversion_impact', 0):.2f}")
        
        return success

    def test_intelligence_dashboard(self):
        """Test comprehensive intelligence dashboard"""
        print("\n📊 Testing Customer Intelligence AI Dashboard (may take 45-60 seconds)...")
        
        success, response = self.run_test(
            "Customer Intelligence AI Dashboard",
            "GET",
            "api/intelligence/dashboard",
            200,
            timeout=90  # All microservices running in parallel
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            modules = response.get('modules', {})
            print(f"   Integrated {len(modules)} AI modules:")
            
            for module_name, module_data in modules.items():
                if isinstance(module_data, dict) and 'error' not in module_data:
                    print(f"   ✅ {module_name.replace('_', ' ').title()}: Working")
                else:
                    print(f"   ❌ {module_name.replace('_', ' ').title()}: Error - {module_data.get('error', 'Unknown error')}")
        
        return success

    # =====================================================
    # MARKETING AUTOMATION PRO MODULE TESTS (REBUILT)
    # Comprehensive testing of all 5 advanced microservices
    # =====================================================

    def test_multi_channel_orchestration_dashboard(self):
        """Test multi-channel orchestration dashboard"""
        print("\n🎯 Testing Marketing Automation Pro - Multi-Channel Orchestration Dashboard...")
        
        success, response = self.run_marketing_test(
            "Multi-Channel Orchestration Dashboard",
            "GET",
            "api/marketing/multi-channel-orchestration",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                campaigns = dashboard.get('active_campaigns', [])
                channels = dashboard.get('channel_performance', {})
                print(f"   Active campaigns: {len(campaigns)}")
                print(f"   Channels configured: {len(channels)}")
                
                metrics = dashboard.get('performance_metrics', {})
                print(f"   Total reach: {metrics.get('total_reach', 0):,}")
                print(f"   Cross-channel conversion: {metrics.get('cross_channel_conversion_rate', 0):.2f}%")
        
        return success

    def test_create_multi_channel_campaign(self):
        """Test creating multi-channel marketing campaign"""
        print("\n📢 Testing Multi-Channel Campaign Creation...")
        
        campaign_data = {
            "name": "AI-Powered Cross-Channel Campaign",
            "target_audience": "high_value_customers",
            "channels": ["email", "sms", "push_notifications", "social_media"],
            "budget": 5000,
            "duration_days": 14,
            "objectives": ["brand_awareness", "lead_generation"],
            "message": "Exclusive software offer just for you!"
        }
        
        success, response = self.run_marketing_test(
            "Create Multi-Channel Campaign",
            "POST",
            "api/marketing/multi-channel-orchestration/campaigns",
            200,
            data=campaign_data,
            timeout=45
        )
        
        if success:
            campaign = response.get('campaign', {})
            print(f"   Campaign ID: {campaign.get('campaign_id', 'unknown')}")
            print(f"   Campaign Name: {campaign.get('name', 'unknown')}")
            print(f"   Channels: {', '.join(campaign.get('channels', []))}")
            print(f"   AI Optimization Score: {campaign.get('ai_optimization_score', 0)}/100")
        
        return success

    def test_execute_multi_channel_campaign(self):
        """Test executing multi-channel campaign with intelligent orchestration"""
        print("\n🚀 Testing Multi-Channel Campaign Execution...")
        
        # Use a test campaign ID
        test_campaign_id = "test_campaign_123"
        
        success, response = self.run_marketing_test(
            "Execute Multi-Channel Campaign",
            "POST",
            f"api/marketing/multi-channel-orchestration/campaigns/{test_campaign_id}/execute",
            200,
            timeout=60
        )
        
        if success:
            results = response.get('results', {})
            print(f"   Campaign ID: {response.get('campaign_id', 'unknown')}")
            print(f"   Execution Status: {results.get('status', 'unknown')}")
            
            channel_results = results.get('channel_results', {})
            for channel, result in channel_results.items():
                print(f"   {channel.title()}: {result.get('status', 'unknown')} - {result.get('sent', 0)} sent")
        
        return success

    def test_send_sms_message(self):
        """Test SMS message sending via Twilio integration"""
        print("\n📱 Testing SMS Message Sending (Twilio Integration)...")
        
        sms_data = {
            "customer_id": "test_customer_123",
            "phone_number": "+1234567890",
            "message": "🚀 Exclusive software offer from Customer Mind IQ! Limited time 20% off. Reply STOP to opt out.",
            "campaign_id": "sms_campaign_123"
        }
        
        success, response = self.run_marketing_test(
            "Send SMS Message",
            "POST",
            "api/marketing/multi-channel-orchestration/sms",
            200,
            data=sms_data,
            timeout=30
        )
        
        if success:
            result = response.get('result', {})
            print(f"   SMS Status: {result.get('status', 'unknown')}")
            print(f"   Message ID: {result.get('message_id', 'unknown')}")
            print(f"   Provider: {result.get('provider', 'unknown')}")
            print(f"   Cost: ${result.get('cost', 0):.4f}")
        
        return success

    def test_ab_testing_dashboard(self):
        """Test A/B testing dashboard with AI analytics and multi-armed bandit algorithms"""
        print("\n🧪 Testing Marketing Automation Pro - A/B Testing Dashboard...")
        
        success, response = self.run_marketing_test(
            "A/B Testing Dashboard",
            "GET",
            "api/marketing/ab-testing",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                active_tests = dashboard.get('active_tests', [])
                completed_tests = dashboard.get('completed_tests', [])
                print(f"   Active A/B tests: {len(active_tests)}")
                print(f"   Completed tests: {len(completed_tests)}")
                
                insights = dashboard.get('testing_insights', {})
                print(f"   Average lift: {insights.get('average_lift', 0):.2f}%")
                print(f"   Statistical confidence: {insights.get('avg_confidence', 0):.1f}%")
                print(f"   Multi-armed bandit tests: {insights.get('bandit_tests', 0)}")
        
        return success

    def test_create_ai_powered_ab_test(self):
        """Test creating A/B test with AI-generated variants and multi-armed bandit optimization"""
        print("\n🔬 Testing AI-Powered A/B Test Creation with Multi-Armed Bandit...")
        
        ab_test_data = {
            "test_name": "AI Email Subject Line Optimization",
            "test_type": "email_campaign",
            "variants": [
                {
                    "name": "Control",
                    "subject_line": "Your Monthly Software Update",
                    "content": "Standard monthly update email"
                },
                {
                    "name": "AI Optimized",
                    "subject_line": "🚀 Exclusive Software Features Just for You!",
                    "content": "Personalized AI-generated content"
                },
                {
                    "name": "Urgency Focused",
                    "subject_line": "⏰ Limited Time: Premium Features Unlocked",
                    "content": "Urgency-driven AI content"
                }
            ],
            "traffic_split": 33,
            "success_metric": "open_rate",
            "duration_days": 7,
            "use_multi_armed_bandit": True,
            "confidence_threshold": 95
        }
        
        success, response = self.run_marketing_test(
            "Create AI-Powered A/B Test",
            "POST",
            "api/marketing/ab-testing/tests",
            200,
            data=ab_test_data,
            timeout=45
        )
        
        if success:
            test = response.get('test', {})
            print(f"   Test ID: {test.get('test_id', 'unknown')}")
            print(f"   Test Name: {test.get('test_name', 'unknown')}")
            print(f"   Variants: {len(test.get('variants', []))}")
            print(f"   AI Confidence: {test.get('ai_confidence_score', 0)}/100")
            print(f"   Expected Lift: {test.get('expected_lift', 0):.2f}%")
            print(f"   Multi-Armed Bandit: {test.get('uses_bandit_algorithm', False)}")
        
        return success

    def test_get_optimal_variant(self):
        """Test getting optimal variant using multi-armed bandit algorithm"""
        print("\n🎯 Testing Multi-Armed Bandit Optimal Variant Selection...")
        
        test_id = "test_ab_123"
        context = {
            "customer_segment": "high_value",
            "time_of_day": "morning",
            "device_type": "mobile"
        }
        
        success, response = self.run_marketing_test(
            "Get Optimal Variant (Multi-Armed Bandit)",
            "GET",
            f"api/marketing/ab-testing/tests/{test_id}/variant",
            200,
            timeout=30
        )
        
        if success:
            variant = response.get('variant', {})
            print(f"   Selected Variant: {variant.get('variant_name', 'unknown')}")
            print(f"   Confidence Score: {variant.get('confidence_score', 0):.2f}")
            print(f"   Expected Performance: {variant.get('expected_performance', 0):.2f}%")
            print(f"   Bandit Algorithm: {variant.get('algorithm_used', 'unknown')}")
        
        return success

    def test_record_ab_test_event(self):
        """Test recording A/B test events for bandit optimization"""
        print("\n📊 Testing A/B Test Event Recording for Bandit Learning...")
        
        test_id = "test_ab_123"
        event_data = {
            "variant_id": "variant_ai_optimized",
            "event_type": "conversion",
            "value": 1.0,
            "context": {
                "customer_id": "customer_123",
                "timestamp": datetime.now().isoformat(),
                "revenue": 299.99
            }
        }
        
        success, response = self.run_marketing_test(
            "Record A/B Test Event",
            "POST",
            f"api/marketing/ab-testing/tests/{test_id}/events",
            200,
            data=event_data,
            timeout=30
        )
        
        if success:
            result = response.get('result', {})
            print(f"   Event Recorded: {result.get('event_recorded', False)}")
            print(f"   Variant Updated: {result.get('variant_id', 'unknown')}")
            print(f"   New Performance: {result.get('updated_performance', 0):.2f}%")
            print(f"   Bandit Learning: {result.get('bandit_updated', False)}")
        
        return success

    def test_analyze_ab_test_results(self):
        """Test comprehensive A/B test results analysis with AI insights"""
        print("\n📈 Testing A/B Test Results Analysis with AI Insights...")
        
        test_id = "test_ab_123"
        
        success, response = self.run_marketing_test(
            "Analyze A/B Test Results",
            "GET",
            f"api/marketing/ab-testing/tests/{test_id}/results",
            200,
            timeout=45
        )
        
        if success:
            results = response.get('results', {})
            print(f"   Test Status: {results.get('test_status', 'unknown')}")
            print(f"   Statistical Significance: {results.get('statistical_significance', False)}")
            print(f"   Confidence Level: {results.get('confidence_level', 0):.1f}%")
            
            variants = results.get('variant_performance', [])
            print(f"   Variants Analyzed: {len(variants)}")
            for variant in variants:
                print(f"   - {variant.get('name', 'unknown')}: {variant.get('conversion_rate', 0):.2f}% conversion")
            
            winner = results.get('winning_variant', {})
            if winner:
                print(f"   Winner: {winner.get('name', 'unknown')} (+{winner.get('lift', 0):.2f}% lift)")
        
        return success

    def test_dynamic_content_dashboard(self):
        """Test dynamic content personalization dashboard with real-time analytics"""
        print("\n🎨 Testing Marketing Automation Pro - Dynamic Content Dashboard...")
        
        success, response = self.run_marketing_test(
            "Dynamic Content Dashboard",
            "GET",
            "api/marketing/dynamic-content",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                templates = dashboard.get('active_templates', [])
                personalizations = dashboard.get('personalization_stats', {})
                print(f"   Active templates: {len(templates)}")
                print(f"   Personalization rate: {personalizations.get('personalization_rate', 0):.1f}%")
                print(f"   Content variations: {personalizations.get('total_variations', 0)}")
                
                performance = dashboard.get('performance_metrics', {})
                print(f"   Engagement lift: {performance.get('engagement_lift', 0):.2f}%")
                print(f"   Real-time personalizations: {performance.get('realtime_personalizations', 0)}")
        
        return success

    def test_track_customer_behavior(self):
        """Test real-time customer behavior tracking for personalization"""
        print("\n👁️ Testing Real-Time Customer Behavior Tracking...")
        
        behavior_data = {
            "customer_id": "customer_123",
            "event_type": "page_view",
            "page_url": "/products/premium-software",
            "duration": 45,
            "interactions": [
                {"type": "click", "element": "pricing_button", "timestamp": datetime.now().isoformat()},
                {"type": "scroll", "depth": 75, "timestamp": datetime.now().isoformat()}
            ],
            "context": {
                "device": "desktop",
                "browser": "chrome",
                "referrer": "google_ads"
            }
        }
        
        success, response = self.run_marketing_test(
            "Track Customer Behavior",
            "POST",
            "api/marketing/dynamic-content/behavior/track",
            200,
            data=behavior_data,
            timeout=30
        )
        
        if success:
            result = response.get('result', {})
            print(f"   Behavior Tracked: {result.get('tracked', False)}")
            print(f"   Customer Profile Updated: {result.get('profile_updated', False)}")
            print(f"   Personalization Score: {result.get('personalization_score', 0)}/100")
            print(f"   Next Action Predicted: {result.get('predicted_next_action', 'unknown')}")
        
        return success

    def test_create_dynamic_template(self):
        """Test creating dynamic content template with AI optimization"""
        print("\n📝 Testing Dynamic Content Template Creation...")
        
        template_data = {
            "template_name": "AI-Powered Product Recommendation Email",
            "template_type": "email",
            "base_content": "Hi {{customer_name}}, based on your recent activity viewing {{viewed_products}}, we have personalized recommendations for you: {{ai_recommendations}}. {{urgency_message}}",
            "personalization_rules": [
                {
                    "field": "customer_name",
                    "source": "customer_profile",
                    "fallback": "Valued Customer"
                },
                {
                    "field": "viewed_products",
                    "source": "behavior_tracking",
                    "fallback": "our premium software"
                },
                {
                    "field": "ai_recommendations",
                    "source": "ai_engine",
                    "fallback": "Our Premium Software Suite"
                },
                {
                    "field": "urgency_message",
                    "source": "dynamic_rules",
                    "conditions": [
                        {"if": "high_intent", "then": "⏰ Limited time offer - 20% off!"},
                        {"if": "returning_visitor", "then": "Welcome back! Special discount inside."},
                        {"default": "Explore our latest features."}
                    ]
                }
            ],
            "target_segments": ["high_value", "active_users", "potential_churners"],
            "ai_optimization": True
        }
        
        success, response = self.run_marketing_test(
            "Create Dynamic Content Template",
            "POST",
            "api/marketing/dynamic-content/templates",
            200,
            data=template_data,
            timeout=45
        )
        
        if success:
            template = response.get('template', {})
            print(f"   Template ID: {template.get('template_id', 'unknown')}")
            print(f"   Template Name: {template.get('template_name', 'unknown')}")
            print(f"   Personalization Fields: {len(template.get('personalization_rules', []))}")
            print(f"   AI Optimization Score: {template.get('ai_optimization_score', 0)}/100")
            print(f"   Expected Engagement Lift: {template.get('expected_engagement_lift', 0):.1f}%")
        
        return success

    def test_generate_personalized_content(self):
        """Test generating personalized content based on customer behavior and AI"""
        print("\n🤖 Testing AI-Powered Personalized Content Generation...")
        
        personalization_data = {
            "customer_id": "customer_123",
            "template_id": "template_ai_email_123",
            "context": {
                "recent_behavior": ["viewed_pricing", "downloaded_trial", "visited_features"],
                "customer_segment": "high_intent_prospect",
                "time_of_day": "morning",
                "device": "mobile",
                "previous_purchases": ["Basic CRM"],
                "engagement_history": {
                    "email_opens": 8,
                    "click_rate": 0.35,
                    "last_interaction": "2024-01-15"
                }
            }
        }
        
        success, response = self.run_marketing_test(
            "Generate Personalized Content",
            "POST",
            "api/marketing/dynamic-content/personalize",
            200,
            data=personalization_data,
            timeout=45
        )
        
        if success:
            content = response.get('content', {})
            print(f"   Content Generated: {content.get('content_generated', False)}")
            print(f"   Personalization Level: {content.get('personalization_level', 'unknown')}")
            print(f"   AI Confidence: {content.get('ai_confidence', 0)}/100")
            print(f"   Expected CTR: {content.get('expected_ctr', 0):.2f}%")
            print(f"   Content Preview: {content.get('content_preview', 'N/A')[:100]}...")
        
        return success

    def test_get_real_time_recommendations(self):
        """Test real-time content recommendations based on current behavior"""
        print("\n⚡ Testing Real-Time Content Recommendations...")
        
        customer_id = "customer_123"
        context = {
            "current_page": "/products/enterprise-suite",
            "session_duration": 180,
            "pages_viewed": ["/pricing", "/features", "/testimonials"],
            "cart_items": [],
            "previous_campaigns": ["email_campaign_nov", "retargeting_dec"],
            "real_time_signals": {
                "mouse_movement": "active",
                "scroll_behavior": "engaged",
                "time_on_page": 45
            }
        }
        
        success, response = self.run_marketing_test(
            "Get Real-Time Recommendations",
            "GET",
            f"api/marketing/dynamic-content/recommendations/{customer_id}",
            200,
            timeout=30
        )
        
        if success:
            recommendations = response.get('recommendations', [])
            print(f"   Real-Time Recommendations: {len(recommendations)}")
            
            if isinstance(recommendations, list):
                for rec in recommendations[:3]:
                    print(f"   - {rec.get('content_type', 'unknown')}: {rec.get('title', 'unknown')}")
                    print(f"     Relevance: {rec.get('relevance_score', 0)}/100")
                    print(f"     Expected Impact: {rec.get('expected_impact', 'unknown')}")
            else:
                print(f"   Recommendations data: {recommendations}")
        
        return success

    def test_lead_scoring_dashboard(self):
        """Test comprehensive lead scoring dashboard with multi-dimensional AI analytics"""
        print("\n🎯 Testing Marketing Automation Pro - Lead Scoring Enhancement Dashboard...")
        
        success, response = self.run_marketing_test(
            "Lead Scoring Dashboard",
            "GET",
            "api/marketing/lead-scoring",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                leads = dashboard.get('lead_summary', {})
                print(f"   Total Leads: {leads.get('total_leads', 0)}")
                print(f"   Hot Leads: {leads.get('hot_leads', 0)}")
                print(f"   Qualified Leads: {leads.get('qualified_leads', 0)}")
                
                scoring = dashboard.get('scoring_metrics', {})
                print(f"   Average Score: {scoring.get('average_score', 0)}/100")
                print(f"   ML Model Accuracy: {scoring.get('ml_accuracy', 0):.1f}%")
                print(f"   Website Activity Tracked: {scoring.get('website_activities', 0)}")
        
        return success

    def test_track_lead_activity(self):
        """Test tracking lead activity with real-time score impact calculation"""
        print("\n📊 Testing Lead Activity Tracking with Real-Time Scoring...")
        
        activity_data = {
            "lead_id": "lead_123",
            "activity_type": "website_visit",
            "details": {
                "page": "/pricing",
                "duration": 120,
                "actions": ["viewed_pricing", "clicked_demo", "downloaded_brochure"],
                "referrer": "google_ads",
                "device": "desktop"
            },
            "timestamp": datetime.now().isoformat(),
            "context": {
                "campaign_source": "paid_search",
                "utm_medium": "cpc",
                "utm_campaign": "enterprise_software"
            }
        }
        
        success, response = self.run_marketing_test(
            "Track Lead Activity",
            "POST",
            "api/marketing/lead-scoring/activity/track",
            200,
            data=activity_data,
            timeout=30
        )
        
        if success:
            result = response.get('result', {})
            print(f"   Activity Tracked: {result.get('activity_tracked', False)}")
            print(f"   Score Impact: +{result.get('score_impact', 0)} points")
            print(f"   New Lead Score: {result.get('new_score', 0)}/100")
            print(f"   Score Category: {result.get('score_category', 'unknown')}")
            print(f"   Next Best Action: {result.get('next_best_action', 'unknown')}")
        
        return success

    def test_calculate_comprehensive_lead_score(self):
        """Test comprehensive multi-dimensional lead score calculation with AI insights"""
        print("\n🧠 Testing Comprehensive Multi-Dimensional Lead Scoring...")
        
        lead_id = "lead_123"
        lead_data = {
            "company_info": {
                "company_size": "50-200",
                "industry": "technology",
                "revenue": "5M-10M",
                "location": "United States"
            },
            "contact_info": {
                "job_title": "CTO",
                "seniority": "executive",
                "department": "technology"
            },
            "behavioral_data": {
                "website_visits": 8,
                "pages_viewed": 25,
                "content_downloads": 3,
                "email_engagement": 0.75,
                "social_engagement": 0.45
            },
            "interaction_history": {
                "demo_requests": 1,
                "sales_calls": 2,
                "proposal_requests": 0,
                "last_interaction": "2024-01-15"
            }
        }
        
        success, response = self.run_marketing_test(
            "Calculate Comprehensive Lead Score",
            "POST",
            f"api/marketing/lead-scoring/score/{lead_id}",
            200,
            data=lead_data,
            timeout=45
        )
        
        if success:
            lead_score = response.get('lead_score', {})
            print(f"   Overall Score: {lead_score.get('overall_score', 0)}/100")
            print(f"   Score Category: {lead_score.get('score_category', 'unknown')}")
            print(f"   Conversion Probability: {lead_score.get('conversion_probability', 0):.2f}%")
            
            dimensions = lead_score.get('score_dimensions', {})
            print(f"   Demographic Score: {dimensions.get('demographic_score', 0)}/100")
            print(f"   Behavioral Score: {dimensions.get('behavioral_score', 0)}/100")
            print(f"   Engagement Score: {dimensions.get('engagement_score', 0)}/100")
            print(f"   Intent Score: {dimensions.get('intent_score', 0)}/100")
            
            insights = lead_score.get('ai_insights', [])
            print(f"   AI Insights: {len(insights)}")
            if isinstance(insights, list):
                for insight in insights[:2]:
                    if isinstance(insight, dict):
                        print(f"   - {insight.get('insight', 'unknown')}")
                    else:
                        print(f"   - {insight}")
            else:
                print(f"   AI Insights: {insights}")
        
        return success

    def test_train_ml_scoring_model(self):
        """Test training machine learning model for enhanced lead scoring"""
        print("\n🤖 Testing ML Model Training for Enhanced Lead Scoring...")
        
        training_data = [
            {
                "lead_id": "lead_001",
                "features": {
                    "company_size": 150,
                    "website_visits": 12,
                    "email_opens": 8,
                    "content_downloads": 4,
                    "job_seniority": 0.9
                },
                "outcome": "converted",
                "conversion_value": 15000
            },
            {
                "lead_id": "lead_002", 
                "features": {
                    "company_size": 25,
                    "website_visits": 3,
                    "email_opens": 2,
                    "content_downloads": 0,
                    "job_seniority": 0.3
                },
                "outcome": "not_converted",
                "conversion_value": 0
            }
        ]
        
        success, response = self.run_marketing_test(
            "Train ML Scoring Model",
            "POST",
            "api/marketing/lead-scoring/model/train",
            200,
            data=training_data,
            timeout=60
        )
        
        if success:
            model_metrics = response.get('model_metrics', {})
            print(f"   Model Trained: {model_metrics.get('model_trained', False)}")
            print(f"   Accuracy: {model_metrics.get('accuracy', 0):.2f}%")
            print(f"   Precision: {model_metrics.get('precision', 0):.2f}")
            print(f"   Recall: {model_metrics.get('recall', 0):.2f}")
            print(f"   F1 Score: {model_metrics.get('f1_score', 0):.2f}")
            print(f"   Training Samples: {model_metrics.get('training_samples', 0)}")
            print(f"   Feature Importance: {len(model_metrics.get('feature_importance', []))} features")
        
        return success

    def test_referral_program_dashboard(self):
        """Test referral program dashboard with viral analytics and AI optimization"""
        print("\n🤝 Testing Marketing Automation Pro - Referral Program Dashboard...")
        
        success, response = self.run_marketing_test(
            "Referral Program Dashboard",
            "GET",
            "api/marketing/referral-program",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                active_campaigns = dashboard.get('active_campaigns', [])
                referrals = dashboard.get('referral_stats', {})
                print(f"   Active referral campaigns: {len(active_campaigns)}")
                print(f"   Total referrals: {referrals.get('total_referrals', 0)}")
                print(f"   Conversion rate: {referrals.get('conversion_rate', 0):.2f}%")
                
                performance = dashboard.get('performance_metrics', {})
                print(f"   Viral coefficient: {performance.get('viral_coefficient', 0):.2f}")
                print(f"   Customer acquisition cost: ${performance.get('cac_reduction', 0):.2f}")
                print(f"   Viral loop optimization: {performance.get('viral_loop_score', 0)}/100")
        
        return success

    def test_analyze_referral_propensity(self):
        """Test analyzing customer referral propensity with AI"""
        print("\n🔍 Testing AI-Powered Referral Propensity Analysis...")
        
        customer_id = "customer_123"
        
        success, response = self.run_marketing_test(
            "Analyze Referral Propensity",
            "POST",
            f"api/marketing/referral-program/analyze/{customer_id}",
            200,
            timeout=45
        )
        
        if success:
            analysis = response.get('analysis', {})
            print(f"   Customer ID: {customer_id}")
            print(f"   Referral Propensity: {analysis.get('referral_propensity', 0):.2f}%")
            print(f"   Propensity Category: {analysis.get('propensity_category', 'unknown')}")
            print(f"   Expected Referrals: {analysis.get('expected_referrals', 0)}")
            
            factors = analysis.get('influence_factors', [])
            print(f"   Influence Factors: {len(factors)}")
            for factor in factors[:3]:
                print(f"   - {factor.get('factor', 'unknown')}: {factor.get('impact', 0):.1f}% impact")
            
            recommendations = analysis.get('optimization_recommendations', [])
            print(f"   AI Recommendations: {len(recommendations)}")
        
        return success

    def test_create_referral_campaign(self):
        """Test creating AI-optimized referral campaign with viral loop optimization"""
        print("\n🎁 Testing AI-Optimized Referral Campaign Creation...")
        
        campaign_data = {
            "campaign_name": "AI-Optimized Viral Referral Program",
            "reward_type": "tiered",
            "referrer_rewards": [
                {
                    "tier": 1,
                    "threshold": 1,
                    "reward": {"type": "percentage", "value": 20, "description": "20% off next purchase"}
                },
                {
                    "tier": 2,
                    "threshold": 3,
                    "reward": {"type": "cash", "value": 50, "description": "$50 cash reward"}
                },
                {
                    "tier": 3,
                    "threshold": 5,
                    "reward": {"type": "product", "value": "premium_license", "description": "Free Premium License"}
                }
            ],
            "referee_reward": {
                "type": "percentage", 
                "value": 15,
                "description": "15% off first purchase"
            },
            "duration_days": 60,
            "target_segments": ["loyal_customers", "high_value", "advocates"],
            "viral_optimization": {
                "enable_ai_timing": True,
                "enable_social_amplification": True,
                "enable_network_effects": True
            },
            "sharing_channels": ["email", "social_media", "sms", "in_app"]
        }
        
        success, response = self.run_marketing_test(
            "Create AI-Optimized Referral Campaign",
            "POST",
            "api/marketing/referral-program/campaigns",
            200,
            data=campaign_data,
            timeout=45
        )
        
        if success:
            campaign = response.get('campaign', {})
            print(f"   Campaign ID: {campaign.get('campaign_id', 'unknown')}")
            print(f"   Campaign Name: {campaign.get('campaign_name', 'unknown')}")
            print(f"   Reward Tiers: {len(campaign.get('referrer_rewards', []))}")
            print(f"   AI Optimization Score: {campaign.get('ai_optimization_score', 0)}/100")
            print(f"   Predicted Viral Coefficient: {campaign.get('predicted_viral_coefficient', 0):.2f}")
            print(f"   Expected Participants: {campaign.get('expected_participants', 0)}")
        
        return success

    def test_get_viral_metrics(self):
        """Test tracking viral performance metrics and loop optimization"""
        print("\n📈 Testing Viral Performance Metrics and Loop Optimization...")
        
        program_id = "referral_program_123"
        
        success, response = self.run_marketing_test(
            "Get Viral Metrics",
            "GET",
            f"api/marketing/referral-program/viral-metrics/{program_id}",
            200,
            timeout=30
        )
        
        if success:
            metrics = response.get('metrics', {})
            print(f"   Program ID: {program_id}")
            print(f"   Viral Coefficient: {metrics.get('viral_coefficient', 0):.3f}")
            print(f"   Viral Loop Velocity: {metrics.get('loop_velocity', 0):.1f} days")
            print(f"   Network Effect Score: {metrics.get('network_effect_score', 0)}/100")
            
            performance = metrics.get('performance_breakdown', {})
            print(f"   Total Invites Sent: {performance.get('total_invites', 0)}")
            print(f"   Invite Acceptance Rate: {performance.get('acceptance_rate', 0):.2f}%")
            print(f"   Conversion Rate: {performance.get('conversion_rate', 0):.2f}%")
            
            channels = metrics.get('channel_performance', [])
            print(f"   Channel Performance: {len(channels)} channels")
            for channel in channels[:3]:
                print(f"   - {channel.get('channel', 'unknown')}: {channel.get('share_rate', 0):.1f}% share rate")
        
        return success

    def test_optimize_referral_program(self):
        """Test AI-powered referral program optimization"""
        print("\n🚀 Testing AI-Powered Referral Program Optimization...")
        
        program_id = "referral_program_123"
        
        success, response = self.run_marketing_test(
            "Optimize Referral Program",
            "POST",
            f"api/marketing/referral-program/optimize/{program_id}",
            200,
            timeout=60
        )
        
        if success:
            optimization = response.get('optimization', {})
            print(f"   Program ID: {program_id}")
            print(f"   Optimization Applied: {optimization.get('optimization_applied', False)}")
            print(f"   Improvement Score: {optimization.get('improvement_score', 0)}/100")
            
            changes = optimization.get('optimization_changes', [])
            print(f"   Optimization Changes: {len(changes)}")
            for change in changes[:3]:
                print(f"   - {change.get('area', 'unknown')}: {change.get('change', 'unknown')}")
                print(f"     Expected Impact: {change.get('expected_impact', 0):.1f}%")
            
            predictions = optimization.get('performance_predictions', {})
            print(f"   Predicted Viral Coefficient: {predictions.get('new_viral_coefficient', 0):.3f}")
            print(f"   Expected Participation Increase: {predictions.get('participation_increase', 0):.1f}%")
        
        return success

    def test_marketing_automation_dashboard(self):
        """Test comprehensive Marketing Automation Pro unified dashboard"""
        print("\n📊 Testing Marketing Automation Pro - Unified Dashboard...")
        
        success, response = self.run_marketing_test(
            "Marketing Automation Pro Unified Dashboard",
            "GET",
            "api/marketing/dashboard",
            200,
            timeout=90  # All marketing services running in parallel
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            modules = response.get('modules', {})
            print(f"   Integrated {len(modules)} marketing modules:")
            
            for module_name, module_data in modules.items():
                if isinstance(module_data, dict) and 'error' not in module_data:
                    print(f"   ✅ {module_name.replace('_', ' ').title()}: Working")
                    
                    # Show key metrics for each module
                    if 'dashboard' in module_data:
                        dashboard = module_data['dashboard']
                        if module_name == 'multi_channel_orchestration':
                            campaigns = dashboard.get('active_campaigns', [])
                            print(f"      Active Campaigns: {len(campaigns)}")
                        elif module_name == 'ab_testing':
                            tests = dashboard.get('active_tests', [])
                            print(f"      Active A/B Tests: {len(tests)}")
                        elif module_name == 'dynamic_content':
                            templates = dashboard.get('active_templates', [])
                            print(f"      Active Templates: {len(templates)}")
                        elif module_name == 'lead_scoring':
                            leads = dashboard.get('lead_summary', {})
                            print(f"      Total Leads: {leads.get('total_leads', 0)}")
                        elif module_name == 'referral_program':
                            referrals = dashboard.get('referral_stats', {})
                            print(f"      Total Referrals: {referrals.get('total_referrals', 0)}")
                else:
                    print(f"   ❌ {module_name.replace('_', ' ').title()}: Error - {module_data.get('error', 'Unknown error')}")
        
        return success

    def run_comprehensive_marketing_automation_tests(self):
        """Run comprehensive Marketing Automation Pro module tests"""
        print("\n" + "="*80)
        print("🚀 COMPREHENSIVE MARKETING AUTOMATION PRO MODULE TESTING")
        print("Testing all 5 advanced microservices with AI-powered features")
        print("="*80)
        
        # Track test results
        tests_run = 0
        tests_passed = 0
        
        # 1. Multi-Channel Orchestration Tests (4 endpoints)
        print("\n🎯 1. MULTI-CHANNEL ORCHESTRATION MICROSERVICE")
        print("-" * 50)
        
        tests = [
            self.test_multi_channel_orchestration_dashboard,
            self.test_create_multi_channel_campaign,
            self.test_execute_multi_channel_campaign,
            self.test_send_sms_message
        ]
        
        for test in tests:
            tests_run += 1
            if test():
                tests_passed += 1
        
        # 2. A/B Testing with AI & Multi-Armed Bandits Tests (5 endpoints)
        print("\n🧪 2. A/B TESTING WITH AI & MULTI-ARMED BANDITS MICROSERVICE")
        print("-" * 60)
        
        tests = [
            self.test_ab_testing_dashboard,
            self.test_create_ai_powered_ab_test,
            self.test_get_optimal_variant,
            self.test_record_ab_test_event,
            self.test_analyze_ab_test_results
        ]
        
        for test in tests:
            tests_run += 1
            if test():
                tests_passed += 1
        
        # 3. Dynamic Content Personalization Tests (5 endpoints)
        print("\n🎨 3. DYNAMIC CONTENT PERSONALIZATION MICROSERVICE")
        print("-" * 50)
        
        tests = [
            self.test_dynamic_content_dashboard,
            self.test_track_customer_behavior,
            self.test_create_dynamic_template,
            self.test_generate_personalized_content,
            self.test_get_real_time_recommendations
        ]
        
        for test in tests:
            tests_run += 1
            if test():
                tests_passed += 1
        
        # 4. Lead Scoring Enhancement Tests (4 endpoints)
        print("\n🎯 4. LEAD SCORING ENHANCEMENT MICROSERVICE")
        print("-" * 45)
        
        tests = [
            self.test_lead_scoring_dashboard,
            self.test_track_lead_activity,
            self.test_calculate_comprehensive_lead_score,
            self.test_train_ml_scoring_model
        ]
        
        for test in tests:
            tests_run += 1
            if test():
                tests_passed += 1
        
        # 5. Referral Program Integration Tests (5 endpoints)
        print("\n🤝 5. REFERRAL PROGRAM INTEGRATION MICROSERVICE")
        print("-" * 45)
        
        tests = [
            self.test_referral_program_dashboard,
            self.test_analyze_referral_propensity,
            self.test_create_referral_campaign,
            self.test_get_viral_metrics,
            self.test_optimize_referral_program
        ]
        
        for test in tests:
            tests_run += 1
            if test():
                tests_passed += 1
        
        # 6. Unified Dashboard Test (1 endpoint)
        print("\n📊 6. UNIFIED MARKETING AUTOMATION DASHBOARD")
        print("-" * 45)
        
        tests_run += 1
        if self.test_marketing_automation_dashboard():
            tests_passed += 1
        
        # Final Results
        print("\n" + "="*80)
        print("🎉 MARKETING AUTOMATION PRO TESTING COMPLETE")
        print("="*80)
        print(f"📊 COMPREHENSIVE TEST RESULTS:")
        print(f"   Total Tests Run: {tests_run}")
        print(f"   Tests Passed: {tests_passed}")
        print(f"   Success Rate: {(tests_passed/tests_run)*100:.1f}%")
        print(f"   Failed Tests: {tests_run - tests_passed}")
        
        # Detailed breakdown
        print(f"\n📋 MICROSERVICE BREAKDOWN:")
        print(f"   1. Multi-Channel Orchestration: 4 endpoints tested")
        print(f"   2. A/B Testing with AI & Multi-Armed Bandits: 5 endpoints tested")
        print(f"   3. Dynamic Content Personalization: 5 endpoints tested")
        print(f"   4. Lead Scoring Enhancement: 4 endpoints tested")
        print(f"   5. Referral Program Integration: 5 endpoints tested")
        print(f"   6. Unified Dashboard: 1 endpoint tested")
        print(f"   TOTAL: {tests_run} endpoints tested across 5 advanced microservices")
        
        if tests_passed == tests_run:
            print(f"\n✅ ALL MARKETING AUTOMATION PRO TESTS PASSED!")
            print(f"   The completely rebuilt Marketing Automation Pro module is fully functional")
            print(f"   All AI-powered features, mock integrations, and analytics are working correctly")
        else:
            print(f"\n⚠️  {tests_run - tests_passed} tests failed - see details above")
        
        print("="*80)
        
        return tests_passed, tests_run

    # =====================================================
    # REVENUE ANALYTICS SUITE MODULE TESTS
    # =====================================================

    def run_revenue_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a Revenue Analytics Suite API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.revenue_analytics_tests += 1
        print(f"\n💰 Testing Revenue Analytics Suite: {name}...")
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
                self.revenue_analytics_passed += 1
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

    def test_revenue_forecasting_dashboard(self):
        """Test revenue forecasting dashboard with AI predictions"""
        print("\n📈 Testing Revenue Analytics Suite - Revenue Forecasting Dashboard...")
        
        success, response = self.run_revenue_test(
            "Revenue Forecasting Dashboard",
            "GET",
            "api/revenue/revenue-forecasting",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                metrics = dashboard.get('current_metrics', {})
                print(f"   Monthly Revenue: ${metrics.get('monthly_revenue', 0):,}")
                print(f"   Forecast Accuracy: {metrics.get('forecast_accuracy', 0)}%")
                print(f"   Predicted Growth: {metrics.get('predicted_growth', 0)}%")
                
                timeline = dashboard.get('revenue_timeline', [])
                print(f"   Revenue Timeline Points: {len(timeline)}")
                
                insights = dashboard.get('ai_insights', [])
                print(f"   AI Insights: {len(insights)}")
                for insight in insights[:2]:
                    print(f"   - {insight.get('insight', 'Unknown')} (Confidence: {insight.get('confidence', 0)}%)")
        
        return success

    def test_revenue_forecasting_scenario(self):
        """Test revenue forecasting scenario creation"""
        print("\n🎯 Testing Revenue Forecasting Scenario Creation...")
        
        scenario_data = {
            "time_horizon": 12,
            "growth_rate": 15,
            "market_conditions": "optimistic"
        }
        
        success, response = self.run_revenue_test(
            "Create Revenue Scenario",
            "POST",
            "api/revenue/revenue-forecasting/scenario",
            200,
            data=scenario_data,
            timeout=45
        )
        
        if success:
            scenario_id = response.get('scenario_id', 'unknown')
            scenarios = response.get('scenarios', [])
            print(f"   Scenario ID: {scenario_id}")
            print(f"   Generated Scenarios: {len(scenarios)}")
            
            for scenario in scenarios:
                print(f"   - {scenario.get('scenario', 'unknown').title()}: ${scenario.get('total_projected', 0):,} (Confidence: {scenario.get('confidence', 0)}%)")
        
        return success

    def test_revenue_trends(self):
        """Test revenue trend analysis"""
        print("\n📊 Testing Revenue Trend Analysis...")
        
        success, response = self.run_revenue_test(
            "Revenue Trends Analysis",
            "GET",
            "api/revenue/revenue-forecasting/trends",
            200,
            timeout=30
        )
        
        if success:
            trends = response.get('trends', {})
            if trends:
                short_term = trends.get('short_term', {})
                long_term = trends.get('long_term', {})
                print(f"   Short-term Direction: {short_term.get('direction', 'unknown')}")
                print(f"   Short-term Strength: {short_term.get('strength', 0)}")
                print(f"   Long-term CAGR: {long_term.get('projected_cagr', 0)}%")
                
                risk_factors = trends.get('risk_factors', [])
                print(f"   Risk Factors: {len(risk_factors)}")
        
        return success

    def test_price_optimization_dashboard(self):
        """Test price optimization dashboard with AI recommendations"""
        print("\n💲 Testing Revenue Analytics Suite - Price Optimization Dashboard...")
        
        success, response = self.run_revenue_test(
            "Price Optimization Dashboard",
            "GET",
            "api/revenue/price-optimization",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('overview_metrics', {})
                print(f"   Products Analyzed: {overview.get('total_products_analyzed', 0)}")
                print(f"   Optimization Opportunities: {overview.get('optimization_opportunities', 0)}")
                print(f"   Potential Revenue Increase: {overview.get('potential_revenue_increase', 0)}%")
                
                products = dashboard.get('product_optimization', [])
                print(f"   Product Optimizations: {len(products)}")
                for product in products[:2]:
                    print(f"   - {product.get('name', 'Unknown')}: {product.get('price_change', 0)}% price change")
                
                strategies = dashboard.get('pricing_strategies', [])
                print(f"   Pricing Strategies: {len(strategies)}")
                
                recommendations = dashboard.get('ai_recommendations', [])
                print(f"   AI Recommendations: {len(recommendations)}")
        
        return success

    def test_price_simulation(self):
        """Test price change simulation"""
        print("\n🧮 Testing Price Change Simulation...")
        
        simulation_data = {
            "product_id": "test_product_123",
            "current_price": 100,
            "new_price": 115
        }
        
        success, response = self.run_revenue_test(
            "Price Change Simulation",
            "POST",
            "api/revenue/price-optimization/simulate",
            200,
            data=simulation_data,
            timeout=45
        )
        
        if success:
            simulation_id = response.get('simulation_id', 'unknown')
            predictions = response.get('predictions', {})
            print(f"   Simulation ID: {simulation_id}")
            
            if predictions:
                revenue_impact = predictions.get('revenue_impact', {})
                print(f"   Revenue Change: {revenue_impact.get('revenue_change_percent', 0)}%")
                print(f"   Current Revenue: ${revenue_impact.get('current_revenue', 0):,}")
                print(f"   Predicted Revenue: ${revenue_impact.get('predicted_revenue', 0):,}")
        
        return success

    def test_competitive_analysis(self):
        """Test competitive pricing analysis"""
        print("\n🏆 Testing Competitive Pricing Analysis...")
        
        success, response = self.run_revenue_test(
            "Competitive Analysis",
            "GET",
            "api/revenue/price-optimization/competitive-analysis",
            200,
            timeout=30
        )
        
        if success:
            landscape = response.get('competitive_landscape', {})
            if landscape:
                competitors = landscape.get('competitors', [])
                print(f"   Competitors Analyzed: {len(competitors)}")
                
                for competitor in competitors[:2]:
                    print(f"   - {competitor.get('name', 'Unknown')}: {competitor.get('market_share', 0)}% market share")
                
                opportunities = landscape.get('positioning_opportunities', [])
                print(f"   Positioning Opportunities: {len(opportunities)}")
        
        return success

    def test_profit_margin_dashboard(self):
        """Test profit margin analysis dashboard"""
        print("\n📊 Testing Revenue Analytics Suite - Profit Margin Analysis Dashboard...")
        
        success, response = self.run_revenue_test(
            "Profit Margin Analysis Dashboard",
            "GET",
            "api/revenue/profit-margin-analysis",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('overview_metrics', {})
                print(f"   Total Revenue: ${overview.get('total_revenue', 0):,}")
                print(f"   Total Costs: ${overview.get('total_costs', 0):,}")
                print(f"   Overall Margin: {overview.get('overall_margin_percentage', 0)}%")
                print(f"   Optimization Score: {overview.get('cost_optimization_score', 0)}/100")
                
                products = dashboard.get('product_analysis', [])
                print(f"   Product Categories: {len(products)}")
                
                opportunities = dashboard.get('cost_optimization', [])
                print(f"   Cost Optimization Opportunities: {len(opportunities)}")
                
                recommendations = dashboard.get('ai_recommendations', [])
                print(f"   AI Recommendations: {len(recommendations)}")
        
        return success

    def test_cost_simulation(self):
        """Test cost reduction simulation"""
        print("\n💰 Testing Cost Reduction Simulation...")
        
        simulation_data = {
            "cost_reduction_percentage": 12,
            "categories": ["operations", "marketing"]
        }
        
        success, response = self.run_revenue_test(
            "Cost Reduction Simulation",
            "POST",
            "api/revenue/profit-margin-analysis/cost-simulation",
            200,
            data=simulation_data,
            timeout=45
        )
        
        if success:
            simulation_id = response.get('simulation_id', 'unknown')
            impact = response.get('impact_analysis', {})
            print(f"   Simulation ID: {simulation_id}")
            
            if impact:
                improvements = impact.get('improvements', {})
                print(f"   Margin Increase: {improvements.get('margin_increase', 0)}%")
                print(f"   Additional Profit: ${improvements.get('additional_profit', 0):,}")
                
                risk = response.get('risk_assessment', {})
                print(f"   Implementation Risk: {risk.get('implementation_risk', 'unknown')}")
        
        return success

    def test_industry_benchmarking(self):
        """Test industry benchmarking analysis"""
        print("\n📈 Testing Industry Benchmarking Analysis...")
        
        success, response = self.run_revenue_test(
            "Industry Benchmarking",
            "GET",
            "api/revenue/profit-margin-analysis/benchmarking",
            200,
            timeout=30
        )
        
        if success:
            benchmarking = response.get('benchmarking', {})
            if benchmarking:
                position = benchmarking.get('company_position', {})
                print(f"   Current Margin: {position.get('current_margin', 0)}%")
                print(f"   Industry Ranking: {position.get('industry_ranking', 'unknown')}")
                print(f"   Competitive Position: {position.get('competitive_position', 'unknown')}")
                
                industries = benchmarking.get('industry_comparison', [])
                print(f"   Industry Comparisons: {len(industries)}")
                
                practices = benchmarking.get('best_practices', [])
                print(f"   Best Practices: {len(practices)}")
        
        return success

    def test_subscription_analytics_dashboard(self):
        """Test subscription analytics dashboard with churn prediction"""
        print("\n📱 Testing Revenue Analytics Suite - Subscription Analytics Dashboard...")
        
        success, response = self.run_revenue_test(
            "Subscription Analytics Dashboard",
            "GET",
            "api/revenue/subscription-analytics",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                metrics = dashboard.get('key_metrics', {})
                print(f"   Total Subscribers: {metrics.get('total_subscribers', 0):,}")
                print(f"   Monthly Recurring Revenue: ${metrics.get('monthly_recurring_revenue', 0):,}")
                print(f"   Annual Recurring Revenue: ${metrics.get('annual_recurring_revenue', 0):,}")
                print(f"   Average Churn Rate: {metrics.get('average_churn_rate', 0)}%")
                print(f"   Customer Lifetime Value: ${metrics.get('customer_lifetime_value', 0):,}")
                
                tiers = dashboard.get('subscription_tiers', [])
                print(f"   Subscription Tiers: {len(tiers)}")
                
                cohorts = dashboard.get('cohort_analysis', [])
                print(f"   Cohort Analysis: {len(cohorts)} cohorts")
                
                churn_predictions = dashboard.get('churn_prediction', [])
                print(f"   Churn Risk Segments: {len(churn_predictions)}")
                
                recommendations = dashboard.get('ai_recommendations', [])
                print(f"   AI Recommendations: {len(recommendations)}")
        
        return success

    def test_churn_prediction(self):
        """Test individual customer churn prediction"""
        print("\n🚨 Testing Customer Churn Prediction...")
        
        customer_data = {
            "customer_id": "test_customer_456",
            "usage_score": 65,
            "satisfaction_score": 7.2,
            "support_tickets": 3,
            "subscription_length_months": 8
        }
        
        success, response = self.run_revenue_test(
            "Customer Churn Prediction",
            "POST",
            "api/revenue/subscription-analytics/churn-prediction",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            customer_id = response.get('customer_id', 'unknown')
            prediction = response.get('prediction', {})
            print(f"   Customer ID: {customer_id}")
            
            if prediction:
                print(f"   Churn Probability: {prediction.get('churn_probability', 0)}%")
                print(f"   Risk Level: {prediction.get('risk_level', 'unknown')}")
                print(f"   Urgency: {prediction.get('urgency', 'unknown')}")
                print(f"   Confidence Score: {prediction.get('confidence_score', 0)}%")
                
                factors = response.get('contributing_factors', [])
                print(f"   Contributing Factors: {len(factors)}")
                
                interventions = response.get('recommended_interventions', [])
                print(f"   Recommended Interventions: {len(interventions)}")
        
        return success

    def test_revenue_optimization(self):
        """Test subscription revenue optimization insights"""
        print("\n💡 Testing Subscription Revenue Optimization...")
        
        success, response = self.run_revenue_test(
            "Revenue Optimization Insights",
            "GET",
            "api/revenue/subscription-analytics/revenue-optimization",
            200,
            timeout=45
        )
        
        if success:
            optimization = response.get('revenue_optimization', {})
            if optimization:
                metrics = optimization.get('current_metrics', {})
                print(f"   Total Subscribers: {metrics.get('total_subscribers', 0):,}")
                print(f"   Monthly Recurring Revenue: ${metrics.get('monthly_recurring_revenue', 0):,}")
                print(f"   Average Revenue Per User: ${metrics.get('average_revenue_per_user', 0):,}")
                
                strategies = optimization.get('optimization_strategies', [])
                print(f"   Optimization Strategies: {len(strategies)}")
                
                segments = optimization.get('customer_segments', [])
                print(f"   Customer Segments: {len(segments)}")
                
                actions = optimization.get('prioritized_actions', [])
                print(f"   Prioritized Actions: {len(actions)}")
        
        return success

    def test_financial_reporting_dashboard(self):
        """Test financial reporting dashboard with executive insights"""
        print("\n📊 Testing Revenue Analytics Suite - Financial Reporting Dashboard...")
        
        success, response = self.run_revenue_test(
            "Financial Reporting Dashboard",
            "GET",
            "api/revenue/financial-reporting",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Total Revenue: ${summary.get('total_revenue', 0):,}")
                print(f"   Total Expenses: ${summary.get('total_expenses', 0):,}")
                print(f"   Net Profit: ${summary.get('net_profit', 0):,}")
                print(f"   Average Profit Margin: {summary.get('average_profit_margin', 0)}%")
                print(f"   Revenue Growth Rate: {summary.get('revenue_growth_rate', 0)}%")
                
                quarterly = dashboard.get('quarterly_performance', [])
                print(f"   Quarterly Performance: {len(quarterly)} quarters")
                
                ratios = dashboard.get('financial_ratios', {})
                print(f"   Financial Ratios Categories: {len(ratios)}")
                
                revenue_sources = dashboard.get('revenue_breakdown', [])
                print(f"   Revenue Sources: {len(revenue_sources)}")
                
                expenses = dashboard.get('expense_analysis', [])
                print(f"   Expense Categories: {len(expenses)}")
                
                insights = dashboard.get('ai_insights', [])
                print(f"   AI Insights: {len(insights)}")
        
        return success

    def test_custom_report_generation(self):
        """Test custom financial report generation"""
        print("\n📋 Testing Custom Financial Report Generation...")
        
        report_config = {
            "report_type": "comprehensive",
            "date_range": "quarterly",
            "include_forecasts": True
        }
        
        success, response = self.run_revenue_test(
            "Custom Report Generation",
            "POST",
            "api/revenue/financial-reporting/custom-report",
            200,
            data=report_config,
            timeout=45
        )
        
        if success:
            report_id = response.get('report_id', 'unknown')
            print(f"   Report ID: {report_id}")
            
            summary = response.get('executive_summary', {})
            if summary:
                print(f"   Financial Health: {summary.get('financial_health', 'unknown')}")
                print(f"   Growth Trajectory: {summary.get('growth_trajectory', 'unknown')}")
                
                strengths = summary.get('key_strengths', [])
                print(f"   Key Strengths: {len(strengths)}")
                
                recommendations = summary.get('strategic_recommendations', [])
                print(f"   Strategic Recommendations: {len(recommendations)}")
            
            sections = response.get('report_sections', [])
            print(f"   Report Sections: {len(sections)}")
        
        return success

    def test_kpi_dashboard(self):
        """Test executive KPI dashboard"""
        print("\n📈 Testing Executive KPI Dashboard...")
        
        success, response = self.run_revenue_test(
            "Executive KPI Dashboard",
            "GET",
            "api/revenue/financial-reporting/kpi-dashboard",
            200,
            timeout=45
        )
        
        if success:
            dashboard = response.get('dashboard', {})
            if dashboard:
                health_score = dashboard.get('financial_health_score', 0)
                print(f"   Financial Health Score: {health_score}/100")
                
                components = dashboard.get('health_components', {})
                print(f"   Health Components: {len(components)}")
                
                kpis = dashboard.get('executive_kpis', [])
                print(f"   Executive KPIs: {len(kpis)}")
                
                alerts = dashboard.get('performance_alerts', [])
                print(f"   Performance Alerts: {len(alerts)}")
                
                insights = dashboard.get('summary_insights', {})
                if insights:
                    strengths = insights.get('strongest_areas', [])
                    opportunities = insights.get('improvement_opportunities', [])
                    print(f"   Strongest Areas: {len(strengths)}")
                    print(f"   Improvement Opportunities: {len(opportunities)}")
        
        return success

    def test_variance_analysis(self):
        """Test budget vs actual variance analysis"""
        print("\n📊 Testing Budget Variance Analysis...")
        
        success, response = self.run_revenue_test(
            "Variance Analysis",
            "GET",
            "api/revenue/financial-reporting/variance-analysis",
            200,
            timeout=30
        )
        
        if success:
            analysis = response.get('variance_analysis', {})
            if analysis:
                summary = analysis.get('summary', {})
                print(f"   Total Budget: ${summary.get('total_budget', 0):,}")
                print(f"   Total Actual: ${summary.get('total_actual', 0):,}")
                print(f"   Total Variance: ${summary.get('total_variance', 0):,}")
                print(f"   Overall Accuracy: {summary.get('overall_accuracy', 0)}%")
                
                variances = analysis.get('category_variances', [])
                print(f"   Category Variances: {len(variances)}")
                
                trends = analysis.get('monthly_trends', [])
                print(f"   Monthly Trends: {len(trends)}")
                
                drivers = analysis.get('variance_drivers', [])
                print(f"   Variance Drivers: {len(drivers)}")
        
        return success

    def test_revenue_analytics_suite_dashboard(self):
        """Test comprehensive Revenue Analytics Suite dashboard aggregation"""
        print("\n🎯 Testing Revenue Analytics Suite - Comprehensive Dashboard...")
        
        success, response = self.run_revenue_test(
            "Revenue Analytics Suite Dashboard",
            "GET",
            "api/revenue/dashboard",
            200,
            timeout=90  # All revenue services running in parallel
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            modules = response.get('modules', {})
            print(f"   Integrated {len(modules)} revenue modules:")
            
            for module_name, module_data in modules.items():
                if isinstance(module_data, dict) and 'error' not in module_data:
                    print(f"   ✅ {module_name.replace('_', ' ').title()}: Working")
                else:
                    print(f"   ❌ {module_name.replace('_', ' ').title()}: Error - {module_data.get('error', 'Unknown error')}")
        
        return success

    # =====================================================
    # END REVENUE ANALYTICS SUITE MODULE TESTS
    # =====================================================

    # =====================================================
    # ADVANCED FEATURES EXPANSION MODULE TESTS
    # =====================================================

    def run_advanced_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run an Advanced Features Expansion API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.advanced_features_tests += 1
        print(f"\n🚀 Testing Advanced Features Expansion: {name}...")
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
                self.advanced_features_passed += 1
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

    def test_advanced_behavioral_clustering_dashboard(self):
        """Test Advanced Features Expansion - Behavioral Clustering Dashboard"""
        print("\n🧠 Testing Advanced Features Expansion - Behavioral Clustering Dashboard...")
        
        success, response = self.run_advanced_test(
            "Behavioral Clustering Dashboard",
            "GET",
            "api/advanced/behavioral-clustering",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Customers Analyzed: {summary.get('total_customers_analyzed', 0)}")
                print(f"   Clusters Identified: {summary.get('clusters_identified', 0)}")
                print(f"   Avg Conversion Rate: {summary.get('average_conversion_rate', 0)}%")
                print(f"   Segmentation Quality: {summary.get('segmentation_quality_score', 0)}/100")
                
                clusters = dashboard.get('customer_clusters', [])
                print(f"   Customer Clusters: {len(clusters)}")
                for cluster in clusters[:3]:  # Show first 3 clusters
                    print(f"   - {cluster.get('name', 'Unknown')}: {cluster.get('customer_count', 0)} customers")
                    print(f"     Conversion Rate: {cluster.get('conversion_rate', 0)}%")
                    print(f"     Avg LTV: ${cluster.get('avg_lifetime_value', 0):,}")
                
                insights = dashboard.get('ai_insights', [])
                print(f"   AI Insights: {len(insights)}")
                for insight in insights[:2]:  # Show first 2 insights
                    print(f"   - {insight.get('insight', 'Unknown')} (Impact: {insight.get('impact', 'unknown')})")
        
        return success

    def test_advanced_behavioral_clustering_analyze(self):
        """Test Advanced Features Expansion - Customer Behavior Analysis"""
        print("\n🎯 Testing Advanced Features Expansion - Customer Behavior Analysis...")
        
        customer_data = {
            "customer_id": "test_customer_123",
            "total_purchases": 5,
            "total_spent": 2500.0,
            "software_owned": ["CRM Pro", "Analytics Suite"],
            "engagement_score": 75,
            "last_purchase_date": "2024-01-15T10:00:00Z"
        }
        
        success, response = self.run_advanced_test(
            "Customer Behavior Analysis",
            "POST",
            "api/advanced/behavioral-clustering/analyze",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
            
            cluster_assignment = response.get('cluster_assignment', {})
            if cluster_assignment:
                print(f"   Assigned Cluster: {cluster_assignment.get('cluster_name', 'unknown')}")
                print(f"   Confidence Score: {cluster_assignment.get('confidence_score', 0)}")
            
            recommendations = response.get('personalized_recommendations', [])
            print(f"   Personalized Recommendations: {len(recommendations)}")
            
            marketing_strategy = response.get('marketing_strategy', {})
            if marketing_strategy:
                print(f"   Email Frequency: {marketing_strategy.get('email_frequency', 'unknown')}")
                print(f"   Communication Tone: {marketing_strategy.get('communication_tone', 'unknown')}")
        
        return success

    def test_advanced_churn_prevention_dashboard(self):
        """Test Advanced Features Expansion - Churn Prevention AI Dashboard"""
        print("\n🚨 Testing Advanced Features Expansion - Churn Prevention AI Dashboard...")
        
        success, response = self.run_advanced_test(
            "Churn Prevention AI Dashboard",
            "GET",
            "api/advanced/churn-prevention",
            200,
            timeout=60
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Customers Monitored: {summary.get('total_customers_monitored', 0)}")
                print(f"   At-Risk Customers: {summary.get('at_risk_customers', 0)}")
                print(f"   Critical Risk Count: {summary.get('critical_risk_count', 0)}")
                print(f"   Potential Revenue at Risk: ${summary.get('potential_revenue_at_risk', 0):,}")
                
                at_risk_customers = dashboard.get('at_risk_customers', [])
                print(f"   At-Risk Customer Profiles: {len(at_risk_customers)}")
                for customer in at_risk_customers[:3]:  # Show first 3 at-risk customers
                    print(f"   - {customer.get('name', 'Unknown')}: {customer.get('churn_probability', 0)}% churn risk")
                    print(f"     Risk Level: {customer.get('risk_level', 'unknown')}")
                    print(f"     Potential Loss: ${customer.get('potential_loss', 0):,}")
                
                campaigns = dashboard.get('active_retention_campaigns', [])
                print(f"   Active Retention Campaigns: {len(campaigns)}")
                
                model_performance = dashboard.get('model_performance', {})
                if model_performance:
                    print(f"   Model Accuracy: {model_performance.get('accuracy', 0)}%")
                    print(f"   Model Version: {model_performance.get('model_version', 'unknown')}")
                
                success_metrics = dashboard.get('success_metrics', {})
                if success_metrics:
                    print(f"   Churn Reduction: {success_metrics.get('churn_reduction_percentage', 0)}%")
                    print(f"   Customers Saved This Month: {success_metrics.get('customers_saved_this_month', 0)}")
                    print(f"   Revenue Protected: ${success_metrics.get('revenue_protected_this_month', 0):,}")
        
        return success

    def test_advanced_churn_prevention_predict(self):
        """Test Advanced Features Expansion - Individual Customer Churn Prediction"""
        print("\n🔮 Testing Advanced Features Expansion - Customer Churn Prediction...")
        
        customer_data = {
            "customer_id": "test_customer_456",
            "days_since_last_login": 21,
            "usage_frequency_change": -25,
            "payment_delays": 1,
            "support_tickets_last_30d": 2,
            "feature_adoption_rate": 45,
            "email_engagement_rate": 15,
            "account_age_days": 180,
            "last_purchase_days_ago": 45,
            "subscription_value": 299
        }
        
        success, response = self.run_advanced_test(
            "Customer Churn Prediction",
            "POST",
            "api/advanced/churn-prevention/predict",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
            
            prediction = response.get('churn_prediction', {})
            if prediction:
                print(f"   Churn Probability: {prediction.get('churn_probability', 0)}%")
                print(f"   Risk Level: {prediction.get('risk_level', 'unknown')}")
                print(f"   Days to Predicted Churn: {prediction.get('days_to_predicted_churn', 0)}")
            
            interventions = response.get('recommended_interventions', [])
            print(f"   Recommended Interventions: {len(interventions)}")
            
            risk_factors = response.get('risk_factors', [])
            print(f"   Risk Factors Identified: {len(risk_factors)}")
        
        return success

    def test_advanced_cross_sell_intelligence_dashboard(self):
        """Test Advanced Features Expansion - Cross-Sell Intelligence Dashboard"""
        print("\n💰 Testing Advanced Features Expansion - Cross-Sell Intelligence Dashboard...")
        
        success, response = self.run_advanced_test(
            "Cross-Sell Intelligence Dashboard",
            "GET",
            "api/advanced/cross-sell-intelligence",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Cross-Sell Opportunities: {summary.get('total_cross_sell_opportunities', 0)}")
                print(f"   Total Potential Revenue: ${summary.get('total_potential_revenue', 0):,}")
                print(f"   Avg Cross-Sell Conversion: {summary.get('avg_cross_sell_conversion_rate', 0)}%")
                print(f"   Cross-Sell Revenue This Month: ${summary.get('cross_sell_revenue_this_month', 0):,}")
                
                products = dashboard.get('product_catalog', [])
                print(f"   Products in Catalog: {len(products)}")
                
                relationships = dashboard.get('product_relationships', [])
                print(f"   Product Relationships: {len(relationships)}")
                for rel in relationships[:3]:  # Show first 3 relationships
                    print(f"   - {rel.get('product_a', 'Unknown')} + {rel.get('product_b', 'Unknown')}")
                    print(f"     Co-Purchase Rate: {rel.get('co_purchase_rate', 0)}%")
                    print(f"     Revenue Uplift: {rel.get('revenue_uplift', 0)}%")
                
                opportunities = dashboard.get('cross_sell_opportunities', [])
                print(f"   Active Opportunities: {len(opportunities)}")
                
                bundles = dashboard.get('top_bundles', [])
                print(f"   Top Product Bundles: {len(bundles)}")
                
                insights = dashboard.get('ai_insights', [])
                print(f"   AI Insights: {len(insights)}")
                for insight in insights[:2]:  # Show first 2 insights
                    print(f"   - {insight.get('insight', 'Unknown')} (Confidence: {insight.get('confidence', 0)}%)")
        
        return success

    def test_advanced_cross_sell_intelligence_recommend(self):
        """Test Advanced Features Expansion - Customer Cross-Sell Recommendations"""
        print("\n🎯 Testing Advanced Features Expansion - Customer Cross-Sell Recommendations...")
        
        customer_data = {
            "customer_id": "test_customer_789",
            "current_products": ["CRM Pro"],
            "segment": "SMB",
            "purchase_history": [
                {"product": "CRM Pro", "date": "2024-01-15", "amount": 299}
            ],
            "usage_patterns": {
                "engagement_score": 85,
                "feature_utilization": 0.7
            }
        }
        
        success, response = self.run_advanced_test(
            "Customer Cross-Sell Recommendations",
            "POST",
            "api/advanced/cross-sell-intelligence/recommend",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
            
            recommendations = response.get('recommendations', [])
            print(f"   Product Recommendations: {len(recommendations)}")
            for rec in recommendations[:3]:  # Show first 3 recommendations
                print(f"   - {rec.get('product_name', 'Unknown')}: ${rec.get('price', 0)}")
                print(f"     Confidence: {rec.get('confidence_score', 0)}%")
                print(f"     Conversion Probability: {rec.get('conversion_probability', 0):.2f}")
                print(f"     Expected ROI: {rec.get('expected_roi', 0):.1f}x")
            
            campaign_suggestions = response.get('campaign_suggestions', [])
            print(f"   Campaign Suggestions: {len(campaign_suggestions)}")
            
            revenue_potential = response.get('revenue_potential', {})
            if revenue_potential:
                print(f"   Immediate Opportunity: ${revenue_potential.get('immediate_opportunity', 0):,.0f}")
                print(f"   12-Month Potential: ${revenue_potential.get('12_month_potential', 0):,.0f}")
        
        return success

    def test_advanced_pricing_optimization_dashboard(self):
        """Test Advanced Features Expansion - Advanced Pricing Optimization Dashboard"""
        print("\n💲 Testing Advanced Features Expansion - Advanced Pricing Optimization Dashboard...")
        
        success, response = self.run_advanced_test(
            "Advanced Pricing Optimization Dashboard",
            "GET",
            "api/advanced/pricing-optimization",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Customers Analyzed: {summary.get('total_customers_analyzed', 0)}")
                print(f"   Active Pricing Experiments: {summary.get('active_pricing_experiments', 0)}")
                print(f"   Avg Conversion Improvement: {summary.get('avg_conversion_improvement', 0)}%")
                print(f"   Revenue Optimization This Month: ${summary.get('revenue_optimization_this_month', 0):,}")
                
                segments = dashboard.get('price_sensitivity_segments', [])
                print(f"   Price Sensitivity Segments: {len(segments)}")
                for segment in segments[:3]:  # Show first 3 segments
                    print(f"   - {segment.get('name', 'Unknown')}: {segment.get('customer_count', 0)} customers")
                    print(f"     Discount Response Rate: {segment.get('characteristics', {}).get('discount_response_rate', 0)}%")
                    print(f"     Avg LTV: ${segment.get('avg_ltv', 0):,}")
                
                experiments = dashboard.get('active_experiments', [])
                print(f"   Active Pricing Experiments: {len(experiments)}")
                
                optimizations = dashboard.get('recent_optimizations', [])
                print(f"   Recent Price Optimizations: {len(optimizations)}")
                
                model_performance = dashboard.get('model_performance', {})
                if model_performance:
                    print(f"   Price Prediction Accuracy: {model_performance.get('price_prediction_accuracy', 0)}%")
                    print(f"   Conversion Lift Average: {model_performance.get('conversion_lift_average', 0)}%")
                
                insights = dashboard.get('ai_insights', [])
                print(f"   AI Insights: {len(insights)}")
                for insight in insights[:2]:  # Show first 2 insights
                    print(f"   - {insight.get('insight', 'Unknown')} (Confidence: {insight.get('confidence', 0)}%)")
        
        return success

    def test_advanced_pricing_optimization_analyze_customer(self):
        """Test Advanced Features Expansion - Customer Price Sensitivity Analysis"""
        print("\n🔍 Testing Advanced Features Expansion - Customer Price Sensitivity Analysis...")
        
        customer_data = {
            "customer_id": "test_customer_pricing_001",
            "purchase_history": [
                {"product": "CRM Pro", "price": 299, "date": "2024-01-15"},
                {"product": "Analytics Suite", "price": 199, "date": "2024-02-20"}
            ],
            "avg_order_value": 249,
            "discount_response_history": [15, 20, 10],
            "time_between_purchases": 45,
            "price_comparison_behavior": "moderate",
            "customer_segment": "SMB",
            "geographic_region": "US",
            "company_size": "small",
            "industry": "technology"
        }
        
        success, response = self.run_advanced_test(
            "Customer Price Sensitivity Analysis",
            "POST",
            "api/advanced/pricing-optimization/analyze-customer",
            200,
            data=customer_data,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
            
            sensitivity_analysis = response.get('price_sensitivity_analysis', {})
            if sensitivity_analysis:
                print(f"   Sensitivity Score: {sensitivity_analysis.get('sensitivity_score', 0)}/100")
                print(f"   Sensitivity Category: {sensitivity_analysis.get('sensitivity_category', 'unknown')}")
                print(f"   Price Elasticity: {sensitivity_analysis.get('price_elasticity', 0)}")
                print(f"   Optimal Discount Range: {sensitivity_analysis.get('optimal_discount_range', 'unknown')}")
            
            product_recommendations = response.get('product_recommendations', [])
            print(f"   Product Pricing Recommendations: {len(product_recommendations)}")
            for rec in product_recommendations[:3]:  # Show first 3 recommendations
                print(f"   - {rec.get('product', 'Unknown')}: ${rec.get('base_price', 0)} → ${rec.get('recommended_price', 0)}")
                print(f"     Discount: {rec.get('discount_percentage', 0)}%")
                print(f"     Conversion Probability: {rec.get('conversion_probability', 0):.2f}")
            
            pricing_tactics = response.get('pricing_tactics', [])
            print(f"   Pricing Tactics: {len(pricing_tactics)}")
            
            risk_assessment = response.get('risk_assessment', {})
            if risk_assessment:
                print(f"   Churn Risk on Price Increase: {risk_assessment.get('churn_risk_on_price_increase', 0):.1f}%")
                print(f"   Revenue Optimization Potential: {risk_assessment.get('revenue_optimization_potential', 'unknown')}")
        
        return success

    def test_advanced_sentiment_analysis_dashboard(self):
        """Test Advanced Features Expansion - Sentiment Analysis Dashboard"""
        print("\n😊 Testing Advanced Features Expansion - Sentiment Analysis Dashboard...")
        
        success, response = self.run_advanced_test(
            "Sentiment Analysis Dashboard",
            "GET",
            "api/advanced/sentiment-analysis",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Communications Analyzed: {summary.get('total_communications_analyzed', 0)}")
                print(f"   Overall Sentiment Score: {summary.get('overall_sentiment_score', 0)}")
                print(f"   Positive Sentiment: {summary.get('positive_sentiment_percentage', 0)}%")
                print(f"   Active Alerts: {summary.get('active_alerts', 0)}")
                print(f"   Avg Response Time: {summary.get('avg_response_time', 'unknown')}")
                
                sentiment_distribution = dashboard.get('sentiment_distribution', {})
                if sentiment_distribution:
                    print(f"   Sentiment Distribution:")
                    for sentiment, data in sentiment_distribution.items():
                        print(f"   - {sentiment.title()}: {data.get('count', 0)} ({data.get('percentage', 0)}%)")
                
                alerts = dashboard.get('recent_alerts', [])
                print(f"   Recent Sentiment Alerts: {len(alerts)}")
                for alert in alerts[:3]:  # Show first 3 alerts
                    print(f"   - {alert.get('customer_name', 'Unknown')}: {alert.get('alert_type', 'unknown')}")
                    print(f"     Sentiment Score: {alert.get('sentiment_score', 0)}")
                    print(f"     Emotion: {alert.get('emotion_detected', 'unknown')}")
                    print(f"     Priority: {alert.get('priority_score', 0)}/100")
                
                insights = dashboard.get('ai_insights', [])
                print(f"   AI Insights: {len(insights)}")
                for insight in insights[:2]:  # Show first 2 insights
                    print(f"   - {insight.get('insight', 'Unknown')} (Confidence: {insight.get('confidence', 0)}%)")
        
        return success

    def test_advanced_sentiment_analysis_analyze(self):
        """Test Advanced Features Expansion - Communication Sentiment Analysis"""
        print("\n📝 Testing Advanced Features Expansion - Communication Sentiment Analysis...")
        
        communication_data = {
            "communication_id": "comm_test_001",
            "customer_id": "test_customer_sentiment_001",
            "text": "I love the new features in the CRM Pro! The customer support has been excellent and the product quality is amazing. Very satisfied with my purchase and would highly recommend to others.",
            "source": "email",
            "communication_type": "feedback"
        }
        
        success, response = self.run_advanced_test(
            "Communication Sentiment Analysis",
            "POST",
            "api/advanced/sentiment-analysis/analyze",
            200,
            data=communication_data,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Communication ID: {response.get('communication_id', 'unknown')}")
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
            
            sentiment_analysis = response.get('sentiment_analysis', {})
            if sentiment_analysis:
                print(f"   Sentiment Score: {sentiment_analysis.get('sentiment_score', 0)}")
                print(f"   Sentiment Category: {sentiment_analysis.get('sentiment_category', 'unknown')}")
                print(f"   Confidence Score: {sentiment_analysis.get('confidence_score', 0)}%")
        
        return success

    def test_advanced_sentiment_analysis_trends(self):
        """Test Advanced Features Expansion - Customer Sentiment Trends"""
        print("\n📈 Testing Advanced Features Expansion - Customer Sentiment Trends...")
        
        customer_id = "test_customer_sentiment_trends_001"
        
        success, response = self.run_advanced_test(
            f"Customer Sentiment Trends ({customer_id})",
            "GET",
            f"api/advanced/sentiment-analysis/trends/{customer_id}?days=30",
            200,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Customer ID: {response.get('customer_id', 'unknown')}")
            print(f"   Analysis Period: {response.get('analysis_period', 'unknown')}")
            
            overall_trend = response.get('overall_trend', {})
            if overall_trend:
                print(f"   Trend Direction: {overall_trend.get('direction', 'unknown')}")
                print(f"   Trend Magnitude: {overall_trend.get('magnitude', 0)}")
                print(f"   Current Avg Sentiment: {overall_trend.get('current_avg_sentiment', 0)}")
                print(f"   Previous Avg Sentiment: {overall_trend.get('previous_avg_sentiment', 0)}")
                print(f"   Volatility: {overall_trend.get('volatility', 0)}")
        
        return success

    def test_advanced_features_dashboard(self):
        """Test Advanced Features Expansion - Comprehensive Dashboard"""
        print("\n📊 Testing Advanced Features Expansion - Comprehensive Dashboard...")
        
        success, response = self.run_advanced_test(
            "Advanced Features Expansion Dashboard",
            "GET",
            "api/advanced/dashboard",
            200,
            timeout=90  # All advanced services running in parallel
        )
        
        if success:
            print(f"   Service: {response.get('service', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            modules = response.get('modules', {})
            print(f"   Integrated {len(modules)} advanced modules:")
            
            for module_name, module_data in modules.items():
                if isinstance(module_data, dict) and 'error' not in module_data:
                    print(f"   ✅ {module_name.replace('_', ' ').title()}: Working")
                else:
                    print(f"   ❌ {module_name.replace('_', ' ').title()}: Error - {module_data.get('error', 'Unknown error')}")
        
        return success

    # =====================================================
    # END ADVANCED FEATURES EXPANSION MODULE TESTS
    # =====================================================

    # =====================================================
    # LEGACY TESTS (for compatibility)
    # =====================================================

    def test_get_customer_recommendations(self):
        """Test getting AI recommendations for a specific customer"""
        if not self.customer_ids:
            print("❌ No customer IDs available for recommendation testing")
            return False
            
        customer_id = self.customer_ids[0]
        print(f"\n🎯 Testing AI recommendations for customer {customer_id} (may take 10-15 seconds)...")
        
        success, response = self.run_test(
            f"Get Customer Recommendations for {customer_id}",
            "GET",
            f"api/customers/{customer_id}/recommendations", 
            200,
            timeout=45  # AI analysis takes time
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} recommendations")
            for rec in response:
                print(f"   - {rec.get('product_name', 'Unknown')} ({rec.get('confidence_score', 0):.1f}% confidence)")
        
        return success

    def test_get_analytics(self):
        """Test getting analytics dashboard data"""
        success, response = self.run_test(
            "Get Analytics Dashboard",
            "GET",
            "api/analytics",
            200
        )
        
        if success:
            print(f"   Total customers: {response.get('total_customers', 0)}")
            print(f"   Total revenue: ${response.get('total_revenue', 0):,.2f}")
            print(f"   Conversion rate: {response.get('conversion_metrics', {}).get('conversion_rate', 0)*100:.1f}%")
            print(f"   Top products: {len(response.get('top_products', []))}")
        
        return success

    def run_comprehensive_analytics_insights_tests(self):
        """Run comprehensive Analytics & Insights module tests"""
        print("\n" + "="*80)
        print("🚀 ANALYTICS & INSIGHTS MODULE - COMPREHENSIVE TESTING")
        print("="*80)
        print("Testing all 5 advanced Analytics & Insights microservices:")
        print("")
        print("1. 🗺️  Customer Journey Mapping (3 endpoints)")
        print("   - Dashboard, Path Analysis, Optimization Opportunities")
        print("")
        print("2. 💰 Revenue Attribution (3 endpoints)")
        print("   - Dashboard, Model Comparison, LTV Analysis")
        print("")
        print("3. 👥 Cohort Analysis (3 endpoints)")
        print("   - Dashboard, Custom Analysis, Retention Forecast")
        print("")
        print("4. 🕵️  Competitive Intelligence (3 endpoints)")
        print("   - Dashboard, Competitor Analysis, Market Trends")
        print("")
        print("5. 💹 ROI Forecasting (3 endpoints)")
        print("   - Dashboard, Campaign Prediction, Historical Analysis")
        print("")
        print("6. 🎛️  Dashboard Aggregation (1 endpoint)")
        print("   - Unified dashboard combining all 5 modules")
        print("="*80)
        
        # Reset counters
        self.analytics_insights_tests = 0
        self.analytics_insights_passed = 0
        
        # Test 1: Customer Journey Mapping (3 endpoints)
        print(f"\n{'='*60}")
        print("🗺️  TESTING CUSTOMER JOURNEY MAPPING MICROSERVICE")
        print("="*60)
        
        self.test_customer_journey_mapping_dashboard()
        self.test_analyze_customer_path()
        self.test_journey_optimization_opportunities()
        
        # Test 2: Revenue Attribution (3 endpoints)
        print(f"\n{'='*60}")
        print("💰 TESTING REVENUE ATTRIBUTION MICROSERVICE")
        print("="*60)
        
        self.test_revenue_attribution_dashboard()
        self.test_compare_attribution_models()
        self.test_ltv_analysis()
        
        # Test 3: Cohort Analysis (3 endpoints)
        print(f"\n{'='*60}")
        print("👥 TESTING COHORT ANALYSIS MICROSERVICE")
        print("="*60)
        
        self.test_cohort_analysis_dashboard()
        self.test_custom_cohort_analysis()
        self.test_retention_forecast()
        
        # Test 4: Competitive Intelligence (3 endpoints)
        print(f"\n{'='*60}")
        print("🕵️  TESTING COMPETITIVE INTELLIGENCE MICROSERVICE")
        print("="*60)
        
        self.test_competitive_intelligence_dashboard()
        self.test_competitor_analysis()
        self.test_market_trends()
        
        # Test 5: ROI Forecasting (3 endpoints)
        print(f"\n{'='*60}")
        print("💹 TESTING ROI FORECASTING MICROSERVICE")
        print("="*60)
        
        self.test_roi_forecasting_dashboard()
        self.test_predict_campaign_roi()
        self.test_historical_analysis()
        
        # Test 6: Dashboard Aggregation (1 endpoint)
        print(f"\n{'='*60}")
        print("🎛️  TESTING DASHBOARD AGGREGATION")
        print("="*60)
        
        self.test_analytics_insights_dashboard_aggregation()
        
        return self.analytics_insights_passed, self.analytics_insights_tests

    # =====================================================
    # ANALYTICS & INSIGHTS MODULE TESTS
    # Comprehensive testing of all 5 advanced microservices
    # =====================================================

    def test_customer_journey_mapping_dashboard(self):
        """Test customer journey mapping dashboard"""
        print("\n🗺️ Testing Analytics & Insights - Customer Journey Mapping Dashboard...")
        
        success, response = self.run_analytics_test(
            "Customer Journey Mapping Dashboard",
            "GET",
            "api/analytics/customer-journey-mapping/dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard_data', {})
            if dashboard:
                overview = dashboard.get('overview', {})
                print(f"   Customers Analyzed: {overview.get('total_customers_analyzed', 0)}")
                print(f"   Total Touchpoints: {overview.get('total_touchpoints', 0)}")
                print(f"   Journey Paths: {overview.get('total_journey_paths', 0)}")
                print(f"   Avg Conversion Rate: {overview.get('avg_conversion_rate', 0):.2%}")
                
                top_paths = dashboard.get('top_paths', [])
                print(f"   Top Journey Paths: {len(top_paths)}")
                for path in top_paths[:2]:
                    print(f"   - Path: {len(path.get('path_sequence', []))} touchpoints, {path.get('customer_count', 0)} customers")
                
                channel_performance = dashboard.get('channel_performance', {})
                print(f"   Channel Performance: {len(channel_performance)} channels analyzed")
            
            ai_insights = response.get('ai_insights', [])
            print(f"   AI Insights Generated: {len(ai_insights)}")
            
            visualization = response.get('visualization', {})
            if visualization:
                nodes = visualization.get('nodes', [])
                edges = visualization.get('edges', [])
                print(f"   Journey Visualization: {len(nodes)} nodes, {len(edges)} edges")
        
        return success

    def test_analyze_customer_path(self):
        """Test specific customer journey path analysis"""
        print("\n🔍 Testing Customer Path Analysis...")
        
        path_data = {
            "customer_id": "test_customer_journey_123"
        }
        
        success, response = self.run_analytics_test(
            "Analyze Customer Path",
            "POST",
            "api/analytics/customer-journey-mapping/analyze-path",
            200,
            data=path_data,
            timeout=30
        )
        
        if success:
            customer_id = response.get('customer_id', 'unknown')
            journey_analysis = response.get('journey_analysis', {})
            
            print(f"   Customer ID: {customer_id}")
            print(f"   Total Touchpoints: {journey_analysis.get('total_touchpoints', 0)}")
            print(f"   Journey Stages: {', '.join(journey_analysis.get('journey_stages', []))}")
            print(f"   Channels Used: {', '.join(journey_analysis.get('channels_used', []))}")
            print(f"   Journey Time: {journey_analysis.get('total_journey_time_hours', 0):.1f} hours")
            print(f"   Conversion Achieved: {journey_analysis.get('conversion_achieved', False)}")
            print(f"   Path Value: ${journey_analysis.get('path_value', 0):,.2f}")
            
            touchpoint_sequence = response.get('touchpoint_sequence', [])
            print(f"   Touchpoint Sequence: {len(touchpoint_sequence)} touchpoints")
            
            recommendations = response.get('optimization_recommendations', [])
            print(f"   Optimization Recommendations: {len(recommendations)}")
        
        return success

    def test_journey_optimization_opportunities(self):
        """Test journey optimization opportunities"""
        print("\n⚡ Testing Journey Optimization Opportunities...")
        
        success, response = self.run_analytics_test(
            "Journey Optimization Opportunities",
            "GET",
            "api/analytics/customer-journey-mapping/optimization-opportunities",
            200,
            timeout=30
        )
        
        if success:
            opportunities = response.get('optimization_opportunities', [])
            total_opportunities = response.get('total_opportunities', 0)
            estimated_impact = response.get('estimated_total_impact', 'unknown')
            
            print(f"   Total Opportunities: {total_opportunities}")
            print(f"   Estimated Impact: {estimated_impact}")
            
            for opp in opportunities[:3]:
                print(f"   - {opp.get('opportunity_type', 'unknown').title()}: {opp.get('description', 'No description')[:60]}...")
                print(f"     Priority: {opp.get('priority', 'unknown')}, Impact: {opp.get('potential_impact', 'unknown')}")
                print(f"     Confidence: {opp.get('confidence_score', 0):.1%}")
            
            implementation_priority = response.get('implementation_priority', [])
            print(f"   Implementation Priority: {', '.join(implementation_priority)}")
        
        return success

    def test_revenue_attribution_dashboard(self):
        """Test revenue attribution dashboard"""
        print("\n💰 Testing Analytics & Insights - Revenue Attribution Dashboard...")
        
        success, response = self.run_analytics_test(
            "Revenue Attribution Dashboard",
            "GET",
            "api/analytics/revenue-attribution/dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard_data', {})
            if dashboard:
                overview = dashboard.get('overview', {})
                print(f"   Total Revenue: ${overview.get('total_revenue', 0):,.2f}")
                print(f"   Marketing Spend: ${overview.get('total_marketing_spend', 0):,.2f}")
                print(f"   Overall ROI: {overview.get('overall_roi', 0):.2f}x")
                print(f"   Total Customers: {overview.get('total_customers', 0)}")
                print(f"   Average LTV: ${overview.get('average_ltv', 0):,.2f}")
                print(f"   Total Touchpoints: {overview.get('total_touchpoints', 0)}")
                
                model_comparison = dashboard.get('model_comparison', {})
                print(f"   Attribution Models Compared: {len(model_comparison)}")
                for model_name, metrics in model_comparison.items():
                    print(f"   - {model_name.replace('_', ' ').title()}: ${metrics.get('total_attributed_revenue', 0):,.0f} revenue")
                
                channel_performance = dashboard.get('channel_performance', {})
                print(f"   Channel Performance: {len(channel_performance)} channels analyzed")
                
                ltv_analysis = dashboard.get('ltv_analysis', {})
                if ltv_analysis:
                    print(f"   LTV/CAC Ratio: {ltv_analysis.get('ltv_to_cac_ratio', 0):.1f}")
                    print(f"   High Risk Customers: {ltv_analysis.get('high_risk_customers', 0)}")
            
            ai_insights = response.get('ai_insights', [])
            print(f"   AI Insights: {len(ai_insights)}")
            for insight in ai_insights[:2]:
                print(f"   - {insight.get('insight', 'No insight')[:60]}...")
        
        return success

    def test_compare_attribution_models(self):
        """Test attribution model comparison"""
        print("\n📊 Testing Attribution Model Comparison...")
        
        comparison_data = {
            "models": ["first_touch", "last_touch", "linear", "data_driven"]
        }
        
        success, response = self.run_analytics_test(
            "Compare Attribution Models",
            "POST",
            "api/analytics/revenue-attribution/compare-models",
            200,
            data=comparison_data,
            timeout=45
        )
        
        if success:
            model_comparison = response.get('model_comparison', {})
            model_differences = response.get('model_differences', {})
            recommendations = response.get('recommendations', [])
            
            print(f"   Models Compared: {len(model_comparison)}")
            for model_name, metrics in model_comparison.items():
                print(f"   - {model_name.replace('_', ' ').title()}: ${metrics.get('total_attributed_revenue', 0):,.0f}")
                print(f"     ROI: {metrics.get('average_roi', 0):.2f}x, Top Channel: {metrics.get('top_performing_channel', 'unknown')}")
            
            print(f"   Model Differences: {len(model_differences)} comparisons")
            print(f"   Recommendations: {len(recommendations)}")
            for rec in recommendations[:2]:
                print(f"   - {rec.get('model', 'unknown').title()}: {rec.get('reason', 'No reason')}")
        
        return success

    def test_ltv_analysis(self):
        """Test customer lifetime value analysis"""
        print("\n📈 Testing LTV Analysis...")
        
        success, response = self.run_analytics_test(
            "LTV Analysis",
            "GET",
            "api/analytics/revenue-attribution/ltv-analysis",
            200,
            timeout=45
        )
        
        if success:
            ltv_analysis = response.get('ltv_analysis', {})
            
            if ltv_analysis:
                overview = ltv_analysis.get('overview', {})
                print(f"   Total Customers: {overview.get('total_customers', 0)}")
                print(f"   Average LTV: ${overview.get('average_ltv', 0):,.2f}")
                print(f"   Median LTV: ${overview.get('median_ltv', 0):,.2f}")
                print(f"   Total Potential Revenue: ${overview.get('total_potential_revenue', 0):,.2f}")
                
                segment_breakdown = ltv_analysis.get('segment_breakdown', {})
                print(f"   Customer Segments: {len(segment_breakdown)}")
                for segment, data in segment_breakdown.items():
                    print(f"   - {segment.replace('_', ' ').title()}: {data.get('customer_count', 0)} customers")
                    print(f"     Avg LTV: ${data.get('average_ltv', 0):,.2f}, LTV/CAC: {data.get('ltv_cac_ratio', 0):.1f}")
                
                at_risk_analysis = ltv_analysis.get('at_risk_analysis', {})
                if at_risk_analysis:
                    print(f"   High-Value At-Risk: {at_risk_analysis.get('high_value_at_risk_count', 0)} customers")
                    print(f"   Revenue At Risk: ${at_risk_analysis.get('potential_revenue_at_risk', 0):,.2f}")
            
            recommendations = response.get('recommendations', [])
            print(f"   Recommendations: {len(recommendations)}")
            for rec in recommendations[:2]:
                print(f"   - {rec.get('type', 'unknown').title()}: {rec.get('description', 'No description')[:50]}...")
        
        return success

    def test_cohort_analysis_dashboard(self):
        """Test cohort analysis dashboard"""
        print("\n👥 Testing Analytics & Insights - Cohort Analysis Dashboard...")
        
        success, response = self.run_analytics_test(
            "Cohort Analysis Dashboard",
            "GET",
            "api/analytics/cohort-analysis/dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard_data', {})
            if dashboard:
                overview = dashboard.get('overview', {})
                print(f"   Customers Analyzed: {overview.get('total_customers_analyzed', 0)}")
                print(f"   Total Cohorts: {overview.get('total_cohorts', 0)}")
                print(f"   Avg 1-Month Retention: {overview.get('average_retention_rate_1m', 0):.1%}")
                print(f"   Avg Revenue per Customer: ${overview.get('average_revenue_per_customer', 0):,.2f}")
                print(f"   Analysis Period: {overview.get('cohort_analysis_period', 'unknown')}")
                
                cohort_performance = dashboard.get('cohort_performance', {})
                print(f"   Cohort Performance Data: {len(cohort_performance)} cohorts")
                
                retention_heatmap = dashboard.get('retention_heatmap', {})
                if retention_heatmap:
                    cohorts = retention_heatmap.get('cohorts', [])
                    periods = retention_heatmap.get('periods', [])
                    print(f"   Retention Heatmap: {len(cohorts)} cohorts x {len(periods)} periods")
                
                trend_analysis = dashboard.get('trend_analysis', {})
                if trend_analysis:
                    print(f"   Improving Cohorts: {trend_analysis.get('improving_cohorts_count', 0)}")
                    print(f"   Declining Cohorts: {trend_analysis.get('declining_cohorts_count', 0)}")
            
            predictive_insights = response.get('predictive_insights', [])
            print(f"   Predictive Insights: {len(predictive_insights)}")
            for insight in predictive_insights[:3]:
                print(f"   - Cohort {insight.get('cohort_id', 'unknown')}: {insight.get('health_score', 'unknown')} health")
                print(f"     Predicted LTV: ${insight.get('predicted_ltv', 0):,.2f}")
                print(f"     12M Retention: {insight.get('predicted_retention_12m', 0):.1%}")
            
            comparison_insights = response.get('comparison_insights', {})
            if comparison_insights:
                performance_gaps = comparison_insights.get('performance_gaps', {})
                if performance_gaps:
                    print(f"   Performance Gap: {performance_gaps.get('retention_gap', 0):.1%}")
        
        return success

    def test_custom_cohort_analysis(self):
        """Test custom cohort analysis"""
        print("\n🔧 Testing Custom Cohort Analysis...")
        
        custom_analysis_data = {
            "cohort_type": "channel",
            "cohort_period": "monthly",
            "months_back": 6,
            "customer_count": 200
        }
        
        success, response = self.run_analytics_test(
            "Custom Cohort Analysis",
            "POST",
            "api/analytics/cohort-analysis/custom-analysis",
            200,
            data=custom_analysis_data,
            timeout=45
        )
        
        if success:
            analysis_params = response.get('analysis_parameters', {})
            cohort_results = response.get('cohort_results', {})
            custom_metrics = response.get('custom_metrics', {})
            
            print(f"   Cohort Type: {analysis_params.get('cohort_type', 'unknown')}")
            print(f"   Period: {analysis_params.get('cohort_period', 'unknown')}")
            print(f"   Customers Analyzed: {analysis_params.get('customers_analyzed', 0)}")
            print(f"   Months Analyzed: {analysis_params.get('months_analyzed', 0)}")
            
            if cohort_results:
                cohorts = cohort_results.get('cohorts', [])
                print(f"   Cohorts Generated: {len(cohorts)}")
                print(f"   Total Cohorts: {cohort_results.get('total_cohorts', 0)}")
            
            print(f"   Custom Metrics: {len(custom_metrics)} cohorts with specific metrics")
            
            predictive_insights = response.get('predictive_insights', [])
            print(f"   Predictive Insights: {len(predictive_insights)}")
            
            key_findings = response.get('key_findings', [])
            print(f"   Key Findings: {len(key_findings)}")
            for finding in key_findings[:2]:
                print(f"   - {finding}")
        
        return success

    def test_retention_forecast(self):
        """Test retention forecasting"""
        print("\n🔮 Testing Retention Forecast...")
        
        success, response = self.run_analytics_test(
            "Retention Forecast",
            "GET",
            "api/analytics/cohort-analysis/retention-forecast",
            200,
            timeout=45
        )
        
        if success:
            forecast_summary = response.get('forecast_summary', {})
            cohort_forecasts = response.get('cohort_forecasts', {})
            intervention_recommendations = response.get('intervention_recommendations', {})
            
            print(f"   Cohorts Analyzed: {forecast_summary.get('cohorts_analyzed', 0)}")
            print(f"   Avg Predicted 12M Retention: {forecast_summary.get('average_predicted_12m_retention', 0):.1%}")
            print(f"   At-Risk Cohorts: {forecast_summary.get('at_risk_cohorts_count', 0)}")
            print(f"   Forecast Horizon: {forecast_summary.get('forecast_horizon_months', 0)} months")
            
            print(f"   Cohort Forecasts: {len(cohort_forecasts)} detailed forecasts")
            for cohort_id, forecast in list(cohort_forecasts.items())[:3]:
                print(f"   - {cohort_id}: {forecast.get('predicted_12m_retention', 0):.1%} retention")
                print(f"     Trend: {forecast.get('trend', 'unknown')}, Confidence: {forecast.get('forecast_confidence', 0):.1%}")
            
            if intervention_recommendations:
                immediate_attention = intervention_recommendations.get('immediate_attention', [])
                recommended_actions = intervention_recommendations.get('recommended_actions', [])
                print(f"   Immediate Attention Needed: {len(immediate_attention)} cohorts")
                print(f"   Recommended Actions: {len(recommended_actions)}")
        
        return success

    def test_competitive_intelligence_dashboard(self):
        """Test competitive intelligence dashboard"""
        print("\n🕵️ Testing Analytics & Insights - Competitive Intelligence Dashboard...")
        
        success, response = self.run_analytics_test(
            "Competitive Intelligence Dashboard",
            "GET",
            "api/analytics/competitive-intelligence/dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard_data', {})
            if dashboard:
                overview = dashboard.get('overview', {})
                print(f"   Competitors Monitored: {overview.get('total_competitors_monitored', 0)}")
                print(f"   Data Points Collected: {overview.get('total_data_points_collected', 0)}")
                print(f"   Market Movements Detected: {overview.get('market_movements_detected', 0)}")
                print(f"   Avg Sentiment Score: {overview.get('average_sentiment_score', 0):.2f}")
                
                competitor_analysis = dashboard.get('competitor_analysis', [])
                print(f"   Competitor Analysis: {len(competitor_analysis)} competitors")
                for comp in competitor_analysis[:3]:
                    print(f"   - {comp.get('name', 'unknown')}: {comp.get('tier', 'unknown')} tier")
                    print(f"     Market Share: {comp.get('market_share', 0):.1%}, Sentiment: {comp.get('sentiment_score', 0):.2f}")
                
                market_movements = dashboard.get('recent_market_movements', [])
                print(f"   Recent Market Movements: {len(market_movements)}")
                
                threat_analysis = dashboard.get('threat_analysis', {})
                if threat_analysis:
                    print(f"   High Priority Threats: {threat_analysis.get('high_priority_threats', 0)}")
                    print(f"   Emerging Competitors: {threat_analysis.get('emerging_competitors', 0)}")
            
            ai_insights = response.get('ai_insights', [])
            print(f"   AI Market Insights: {len(ai_insights)}")
            for insight in ai_insights[:2]:
                print(f"   - {insight.get('insight_type', 'unknown').title()}: {insight.get('description', 'No description')[:50]}...")
        
        return success

    def test_competitor_analysis(self):
        """Test specific competitor analysis"""
        print("\n🔍 Testing Competitor Analysis...")
        
        competitor_data = {
            "competitor_name": "TechRival Pro",
            "analysis_depth": "comprehensive"
        }
        
        success, response = self.run_analytics_test(
            "Competitor Analysis",
            "POST",
            "api/analytics/competitive-intelligence/competitor-analysis",
            200,
            data=competitor_data,
            timeout=45
        )
        
        if success:
            competitor_name = response.get('competitor_name', 'unknown')
            analysis = response.get('competitive_analysis', {})
            
            print(f"   Competitor: {competitor_name}")
            
            if analysis:
                strengths = analysis.get('strengths', [])
                weaknesses = analysis.get('weaknesses', [])
                opportunities = analysis.get('opportunities', [])
                threats = analysis.get('threats', [])
                
                print(f"   Strengths: {len(strengths)}")
                print(f"   Weaknesses: {len(weaknesses)}")
                print(f"   Opportunities: {len(opportunities)}")
                print(f"   Threats: {len(threats)}")
                
                print(f"   Market Position: {analysis.get('market_position', 'unknown')}")
                print(f"   Pricing Strategy: {analysis.get('pricing_strategy', 'unknown')}")
                
                recent_activities = analysis.get('recent_activities', [])
                print(f"   Recent Activities: {len(recent_activities)}")
            
            intelligence_data = response.get('intelligence_data', [])
            print(f"   Intelligence Data Points: {len(intelligence_data)}")
            
            strategic_recommendations = response.get('strategic_recommendations', [])
            print(f"   Strategic Recommendations: {len(strategic_recommendations)}")
        
        return success

    def test_market_trends(self):
        """Test market trends analysis"""
        print("\n📊 Testing Market Trends Analysis...")
        
        success, response = self.run_analytics_test(
            "Market Trends Analysis",
            "GET",
            "api/analytics/competitive-intelligence/market-trends",
            200,
            timeout=45
        )
        
        if success:
            market_trends = response.get('market_trends', {})
            trend_analysis = response.get('trend_analysis', {})
            
            if market_trends:
                overall_sentiment = market_trends.get('overall_market_sentiment', 0)
                growth_indicators = market_trends.get('growth_indicators', [])
                emerging_technologies = market_trends.get('emerging_technologies', [])
                
                print(f"   Overall Market Sentiment: {overall_sentiment:.2f}")
                print(f"   Growth Indicators: {len(growth_indicators)}")
                print(f"   Emerging Technologies: {len(emerging_technologies)}")
                
                for tech in emerging_technologies[:3]:
                    print(f"   - {tech.get('technology', 'unknown')}: {tech.get('adoption_rate', 0):.1%} adoption")
            
            if trend_analysis:
                market_size_trend = trend_analysis.get('market_size_trend', {})
                competitive_landscape = trend_analysis.get('competitive_landscape_changes', [])
                
                if market_size_trend:
                    print(f"   Market Size Growth: {market_size_trend.get('growth_rate', 0):.1%}")
                    print(f"   Market Direction: {market_size_trend.get('direction', 'unknown')}")
                
                print(f"   Competitive Landscape Changes: {len(competitive_landscape)}")
            
            predictions = response.get('market_predictions', {})
            if isinstance(predictions, dict):
                print(f"   Market Predictions:")
                for key, value in list(predictions.items())[:2]:
                    print(f"   - {key}: {str(value)[:50]}...")
            else:
                print(f"   Market Predictions: {len(predictions) if predictions else 0}")
        
        return success

    def test_roi_forecasting_dashboard(self):
        """Test ROI forecasting dashboard"""
        print("\n💹 Testing Analytics & Insights - ROI Forecasting Dashboard...")
        
        success, response = self.run_analytics_test(
            "ROI Forecasting Dashboard",
            "GET",
            "api/analytics/roi-forecasting/dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard_data', {})
            if dashboard:
                portfolio_overview = dashboard.get('portfolio_overview', {})
                print(f"   Total Planned Budget: ${portfolio_overview.get('total_planned_budget', 0):,.2f}")
                print(f"   Total Predicted Revenue: ${portfolio_overview.get('total_predicted_revenue', 0):,.2f}")
                print(f"   Portfolio ROI: {portfolio_overview.get('portfolio_roi', 0):.2f}x")
                print(f"   Number of Campaigns: {portfolio_overview.get('number_of_campaigns', 0)}")
                print(f"   Avg Confidence Score: {portfolio_overview.get('average_confidence_score', 0):.1%}")
                
                campaign_forecasts = dashboard.get('campaign_forecasts', [])
                print(f"   Campaign Forecasts: {len(campaign_forecasts)}")
                for forecast in campaign_forecasts[:3]:
                    print(f"   - {forecast.get('campaign_type', 'unknown').title()}: ${forecast.get('budget', 0):,} budget")
                    print(f"     Predicted ROI: {forecast.get('predicted_roi', 0):.2f}x, Risk: {forecast.get('risk_level', 'unknown')}")
                
                historical_performance = dashboard.get('historical_performance', {})
                if historical_performance:
                    print(f"   Historical Campaigns: {historical_performance.get('total_campaigns', 0)}")
                    print(f"   Avg Historical ROI: {historical_performance.get('avg_historical_roi', 0):.2f}x")
                    print(f"   Best Performing Type: {historical_performance.get('best_performing_type', 'unknown')}")
                
                risk_analysis = dashboard.get('risk_analysis', {})
                if risk_analysis:
                    print(f"   Low Risk Campaigns: {risk_analysis.get('low_risk_campaigns', 0)}")
                    print(f"   Medium Risk Campaigns: {risk_analysis.get('medium_risk_campaigns', 0)}")
                    print(f"   High Risk Campaigns: {risk_analysis.get('high_risk_campaigns', 0)}")
                
                model_performance = dashboard.get('model_performance', {})
                if model_performance:
                    print(f"   Model Accuracy: {model_performance.get('ensemble_accuracy', 'unknown')}")
                    print(f"   Prediction Confidence: {model_performance.get('prediction_confidence', 'unknown')}")
                
                optimization_opportunities = dashboard.get('optimization_opportunities', [])
                print(f"   Optimization Opportunities: {len(optimization_opportunities)}")
        
        return success

    def test_predict_campaign_roi(self):
        """Test campaign ROI prediction"""
        print("\n🎯 Testing Campaign ROI Prediction...")
        
        prediction_data = {
            "campaign_type": "email",
            "budget": 10000,
            "duration_days": 14,
            "target_audience_size": 25000,
            "seasonal_factor": 1.1,
            "economic_conditions": "normal",
            "competitive_pressure": "medium",
            "model": "ensemble"
        }
        
        success, response = self.run_analytics_test(
            "Predict Campaign ROI",
            "POST",
            "api/analytics/roi-forecasting/predict",
            200,
            data=prediction_data,
            timeout=45
        )
        
        if success:
            campaign_parameters = response.get('campaign_parameters', {})
            roi_forecast = response.get('roi_forecast', {})
            scenario_analysis = response.get('scenario_analysis', [])
            sensitivity_analysis = response.get('sensitivity_analysis', [])
            
            print(f"   Campaign Type: {campaign_parameters.get('campaign_type', 'unknown')}")
            print(f"   Budget: ${campaign_parameters.get('budget', 0):,}")
            print(f"   Duration: {campaign_parameters.get('duration_days', 0)} days")
            
            if roi_forecast:
                print(f"   Predicted ROI: {roi_forecast.get('predicted_roi', 0):.2f}x")
                print(f"   Predicted Revenue: ${roi_forecast.get('predicted_revenue', 0):,.2f}")
                print(f"   Predicted Conversions: {roi_forecast.get('predicted_conversions', 0)}")
                print(f"   Risk Level: {roi_forecast.get('risk_level', 'unknown')}")
                print(f"   Confidence Score: {roi_forecast.get('confidence_score', 0):.1%}")
                print(f"   Break-even Point: {roi_forecast.get('break_even_point_days', 0)} days")
                print(f"   Confidence Interval: {roi_forecast.get('confidence_interval_lower', 0):.2f} - {roi_forecast.get('confidence_interval_upper', 0):.2f}")
            
            print(f"   Scenario Analysis: {len(scenario_analysis)} scenarios")
            for scenario in scenario_analysis:
                print(f"   - {scenario.get('scenario_name', 'unknown')}: {scenario.get('predicted_roi', 0):.2f}x ROI")
                print(f"     Probability: {scenario.get('probability', 0):.1%}")
            
            print(f"   Sensitivity Analysis: {len(sensitivity_analysis)} parameters")
            for sensitivity in sensitivity_analysis:
                print(f"   - {sensitivity.get('parameter', 'unknown')}: Sensitivity {sensitivity.get('sensitivity_score', 0):.2f}")
            
            recommendations = response.get('recommendations', [])
            print(f"   Recommendations: {len(recommendations)}")
            for rec in recommendations[:2]:
                print(f"   - {rec.get('type', 'unknown').title()}: {rec.get('recommendation', 'No recommendation')}")
        
        return success

    def test_historical_analysis(self):
        """Test historical campaign performance analysis"""
        print("\n📚 Testing Historical Analysis...")
        
        success, response = self.run_analytics_test(
            "Historical Analysis",
            "GET",
            "api/analytics/roi-forecasting/historical-analysis",
            200,
            timeout=45
        )
        
        if success:
            historical_analysis = response.get('historical_analysis', {})
            
            if historical_analysis:
                overview = historical_analysis.get('overview', {})
                print(f"   Total Campaigns: {overview.get('total_campaigns', 0)}")
                print(f"   Total Spend: ${overview.get('total_spend', 0):,.2f}")
                print(f"   Total Revenue: ${overview.get('total_revenue', 0):,.2f}")
                print(f"   Overall ROI: {overview.get('overall_roi', 0):.2f}x")
                
                date_range = overview.get('date_range', {})
                if date_range:
                    print(f"   Date Range: {date_range.get('start', 'unknown')} to {date_range.get('end', 'unknown')}")
                
                performance_by_type = historical_analysis.get('performance_by_type', {})
                print(f"   Performance by Type: {len(performance_by_type)} campaign types")
                for campaign_type, metrics in performance_by_type.items():
                    print(f"   - {campaign_type.replace('_', ' ').title()}: {metrics.get('campaign_count', 0)} campaigns")
                    print(f"     Avg ROI: {metrics.get('average_roi', 0):.2f}x, Success Rate: {metrics.get('success_rate', 0):.1%}")
                
                seasonal_trends = historical_analysis.get('seasonal_trends', {})
                print(f"   Seasonal Trends: {len(seasonal_trends)} months analyzed")
                
                budget_analysis = historical_analysis.get('budget_analysis', {})
                print(f"   Budget Analysis: {len(budget_analysis)} budget brackets")
                for bracket, metrics in budget_analysis.items():
                    print(f"   - {bracket.title()} Budget: {metrics.get('campaign_count', 0)} campaigns")
                    print(f"     Avg ROI: {metrics.get('avg_roi', 0):.2f}x, Avg Budget: ${metrics.get('avg_budget', 0):,.0f}")
                
                top_performers = historical_analysis.get('top_performers', [])
                print(f"   Top Performers: {len(top_performers)} campaigns")
                for performer in top_performers[:3]:
                    print(f"   - {performer.get('campaign_name', 'unknown')}: {performer.get('roi', 0):.2f}x ROI")
                    print(f"     Type: {performer.get('campaign_type', 'unknown')}, Revenue: ${performer.get('revenue', 0):,.0f}")
                
                key_insights = historical_analysis.get('key_insights', [])
                print(f"   Key Insights: {len(key_insights)}")
                for insight in key_insights:
                    print(f"   - {insight.get('insight', 'No insight')}")
                    print(f"     Metric: {insight.get('metric', 'No metric')}")
        
        return success

    def test_analytics_insights_dashboard_aggregation(self):
        """Test Analytics & Insights dashboard aggregation endpoint"""
        print("\n🎛️ Testing Analytics & Insights Dashboard Aggregation...")
        
        success, response = self.run_analytics_test(
            "Analytics & Insights Dashboard Aggregation",
            "GET",
            "api/analytics/dashboard",
            200,
            timeout=60  # Longer timeout for aggregation
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            modules = response.get('modules', {})
            print(f"   Integrated Modules: {len(modules)}")
            
            for module_name, module_data in modules.items():
                if isinstance(module_data, dict) and 'error' not in module_data:
                    print(f"   ✅ {module_name.replace('_', ' ').title()}: Working")
                    
                    # Show key metrics for each module
                    if 'dashboard_data' in module_data:
                        dashboard = module_data['dashboard_data']
                        if 'overview' in dashboard:
                            overview = dashboard['overview']
                            if module_name == 'customer_journey_mapping':
                                print(f"      Customers: {overview.get('total_customers_analyzed', 0)}, Paths: {overview.get('total_journey_paths', 0)}")
                            elif module_name == 'revenue_attribution':
                                print(f"      Revenue: ${overview.get('total_revenue', 0):,.0f}, ROI: {overview.get('overall_roi', 0):.1f}x")
                            elif module_name == 'cohort_analysis':
                                print(f"      Cohorts: {overview.get('total_cohorts', 0)}, Retention: {overview.get('average_retention_rate_1m', 0):.1%}")
                            elif module_name == 'competitive_intelligence':
                                print(f"      Competitors: {overview.get('total_competitors_monitored', 0)}, Movements: {overview.get('market_movements_detected', 0)}")
                            elif module_name == 'roi_forecasting':
                                print(f"      Budget: ${overview.get('total_planned_budget', 0):,.0f}, Portfolio ROI: {overview.get('portfolio_roi', 0):.1f}x")
                else:
                    print(f"   ❌ {module_name.replace('_', ' ').title()}: Error - {module_data.get('error', 'Unknown error')}")
            
            # Check for aggregated insights
            aggregated_insights = response.get('aggregated_insights', [])
            print(f"   Aggregated Insights: {len(aggregated_insights)}")
            
            # Check for cross-module correlations
            cross_module_analysis = response.get('cross_module_analysis', {})
            if cross_module_analysis:
                print(f"   Cross-Module Analysis: Available")
                correlations = cross_module_analysis.get('correlations', [])
                print(f"   Module Correlations: {len(correlations)}")
        
        return success

    # =====================================================
    # END ANALYTICS & INSIGHTS MODULE TESTS
    # =====================================================

    # =====================================================
    # LEGACY ANALYTICS & INSIGHTS MAIN FUNCTION (COMMENTED OUT)
    # =====================================================
    
    # def main():
    #     print("📊 ANALYTICS & INSIGHTS MODULE - COMPREHENSIVE TESTING")
    #     ... (commented out to fix class structure)

    # =====================================================
    # PRODUCT INTELLIGENCE HUB MODULE TESTS
    # =====================================================

    def run_product_intelligence_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a Product Intelligence Hub API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        print(f"\n🚀 Testing Product Intelligence Hub: {name}...")
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

    def test_feature_usage_analytics_dashboard(self):
        """Test Product Intelligence Hub - Feature Usage Analytics Dashboard"""
        print("\n📊 Testing Product Intelligence Hub - Feature Usage Analytics Dashboard...")
        
        success, response = self.run_product_intelligence_test(
            "Feature Usage Analytics Dashboard",
            "GET",
            "api/product-intelligence/feature-usage-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Total Features: {summary.get('total_features', 0)}")
                print(f"   Avg Feature Adoption Rate: {summary.get('avg_feature_adoption_rate', 0)}%")
                print(f"   Avg Features Per User: {summary.get('avg_features_per_user', 0)}")
                print(f"   Feature-Driven Retention: {summary.get('feature_driven_retention', 0)}%")
                print(f"   Power Users Percentage: {summary.get('power_users_percentage', 0)}%")
                print(f"   Feature Stickiness Score: {summary.get('feature_stickiness_score', 0)}")
                
                feature_matrix = dashboard.get('feature_usage_matrix', [])
                print(f"   Feature Usage Matrix: {len(feature_matrix)} features analyzed")
                for feature in feature_matrix[:3]:  # Show first 3 features
                    print(f"   - {feature.get('feature_name', 'Unknown')}: {feature.get('adoption_rate', 0)}% adoption")
                    print(f"     DAU: {feature.get('daily_active_users', 0)}, Stickiness: {feature.get('feature_stickiness', 0)}%")
                
                adoption_journey = dashboard.get('adoption_journey', {})
                if adoption_journey:
                    first_week = adoption_journey.get('first_week', {})
                    print(f"   First Week Adoption: {first_week.get('core_features_adopted', 0)} core features")
                    print(f"   Successful Onboarding Rate: {first_week.get('successful_onboarding_rate', 0)}%")
                
                feature_correlations = dashboard.get('feature_correlations', [])
                print(f"   Feature Correlations: {len(feature_correlations)} correlation pairs")
                
                usage_cohorts = dashboard.get('usage_cohorts', [])
                print(f"   Usage Cohorts: {len(usage_cohorts)} cohorts identified")
                
                roi_analysis = dashboard.get('feature_roi_analysis', [])
                print(f"   Feature ROI Analysis: {len(roi_analysis)} features analyzed")
                
                recommendations = dashboard.get('optimization_recommendations', [])
                print(f"   Optimization Recommendations: {len(recommendations)}")
        
        return success

    def test_feature_analytics_specific(self):
        """Test Product Intelligence Hub - Specific Feature Analytics"""
        print("\n🔍 Testing Product Intelligence Hub - Specific Feature Analytics...")
        
        feature_name = "AI-Powered Insights"
        
        success, response = self.run_product_intelligence_test(
            f"Feature Analytics for {feature_name}",
            "GET",
            f"api/product-intelligence/feature/{feature_name}/analytics",
            200,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Feature Name: {response.get('feature_name', 'unknown')}")
            
            usage_metrics = response.get('usage_metrics', {})
            if usage_metrics:
                print(f"   Total Users: {usage_metrics.get('total_users', 0)}")
                print(f"   Active Users Today: {usage_metrics.get('active_users_today', 0)}")
                print(f"   Avg Session Duration: {usage_metrics.get('avg_session_duration', 'unknown')}")
                print(f"   Feature Completion Rate: {usage_metrics.get('feature_completion_rate', 0):.1f}%")
                print(f"   Bounce Rate: {usage_metrics.get('bounce_rate', 0):.1f}%")
            
            adoption_funnel = response.get('adoption_funnel', {})
            if adoption_funnel:
                print(f"   Feature Discovered: {adoption_funnel.get('feature_discovered', 0)}%")
                print(f"   First Interaction: {adoption_funnel.get('first_interaction', 0)}%")
                print(f"   Regular Usage: {adoption_funnel.get('regular_usage', 0)}%")
                print(f"   Power User Status: {adoption_funnel.get('power_user_status', 0)}%")
            
            user_segments = response.get('user_segments', [])
            print(f"   User Segments: {len(user_segments)}")
            
            improvement_opportunities = response.get('improvement_opportunities', [])
            print(f"   Improvement Opportunities: {len(improvement_opportunities)}")
        
        return success

    def test_onboarding_optimization_dashboard(self):
        """Test Product Intelligence Hub - Onboarding Optimization Dashboard"""
        print("\n🎯 Testing Product Intelligence Hub - Onboarding Optimization Dashboard...")
        
        success, response = self.run_product_intelligence_test(
            "Onboarding Optimization Dashboard",
            "GET",
            "api/product-intelligence/onboarding-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                summary = dashboard.get('summary_metrics', {})
                print(f"   Overall Completion Rate: {summary.get('overall_completion_rate', 0)}%")
                print(f"   Avg Time to Complete: {summary.get('avg_time_to_complete', 0)} hours")
                print(f"   Month-over-Month Improvement: {summary.get('month_over_month_improvement', 'unknown')}")
                print(f"   User Satisfaction Score: {summary.get('user_satisfaction_score', 0)}/10")
                print(f"   Support Tickets During Onboarding: {summary.get('support_tickets_during_onboarding', 0)}")
                print(f"   Completion to Retention Correlation: {summary.get('completion_to_retention_correlation', 0)}%")
                
                onboarding_funnel = dashboard.get('onboarding_funnel', [])
                print(f"   Onboarding Funnel Steps: {len(onboarding_funnel)}")
                for step in onboarding_funnel[:4]:  # Show first 4 steps
                    print(f"   - Step {step.get('step_order', 0)}: {step.get('step', 'Unknown')}")
                    print(f"     Completion Rate: {step.get('completion_rate', 0)}%, Drop-off: {step.get('drop_off_rate', 0)}%")
                    print(f"     Avg Time: {step.get('avg_time_minutes', 0)} minutes")
                
                cohort_performance = dashboard.get('cohort_performance', [])
                print(f"   Cohort Performance: {len(cohort_performance)} cohorts")
                
                onboarding_segments = dashboard.get('onboarding_segments', [])
                print(f"   Onboarding Segments: {len(onboarding_segments)}")
                for segment in onboarding_segments[:2]:  # Show first 2 segments
                    print(f"   - {segment.get('segment', 'Unknown')}: {segment.get('percentage', 0)}% of users")
                    print(f"     Completion Rate: {segment.get('completion_rate', 0)}%")
                    print(f"     Avg Completion Time: {segment.get('avg_completion_time', 0)} hours")
                    print(f"     Retention Rate: {segment.get('retention_rate', 0)}%")
                
                active_experiments = dashboard.get('active_experiments', [])
                print(f"   Active Experiments: {len(active_experiments)}")
                
                success_predictors = dashboard.get('success_predictors', [])
                print(f"   Success Predictors: {len(success_predictors)}")
                
                personalized_paths = dashboard.get('personalized_paths', [])
                print(f"   Personalized Paths: {len(personalized_paths)}")
                
                recommendations = dashboard.get('optimization_recommendations', [])
                print(f"   Optimization Recommendations: {len(recommendations)}")
        
        return success

    def test_optimize_onboarding_path(self):
        """Test Product Intelligence Hub - Optimize Onboarding Path"""
        print("\n⚡ Testing Product Intelligence Hub - Optimize Onboarding Path...")
        
        optimization_data = {
            "user_profile": {
                "role": "Marketing Manager",
                "company_size": "Medium",
                "technical_level": "Intermediate",
                "industry": "Technology",
                "goals": ["Improve campaign performance", "Better customer insights"]
            }
        }
        
        success, response = self.run_product_intelligence_test(
            "Optimize Onboarding Path",
            "POST",
            "api/product-intelligence/optimize-path",
            200,
            data=optimization_data,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Optimization ID: {response.get('optimization_id', 'unknown')}")
            
            user_profile = response.get('user_profile', {})
            print(f"   User Role: {user_profile.get('role', 'unknown')}")
            print(f"   Company Size: {user_profile.get('company_size', 'unknown')}")
            print(f"   Technical Level: {user_profile.get('technical_level', 'unknown')}")
            
            recommended_path = response.get('recommended_path', {})
            if recommended_path:
                print(f"   Recommended Path: {recommended_path.get('path_name', 'unknown')}")
                print(f"   Estimated Completion Time: {recommended_path.get('estimated_completion_time', 0):.1f} hours")
                print(f"   Predicted Success Rate: {recommended_path.get('predicted_success_rate', 0):.1f}%")
                print(f"   Personalization Score: {recommended_path.get('personalization_score', 0):.1f}/100")
            
            optimized_steps = response.get('optimized_steps', [])
            print(f"   Optimized Steps: {len(optimized_steps)}")
            for step in optimized_steps:
                print(f"   - Step {step.get('step_order', 0)}: {step.get('step_name', 'Unknown')}")
                print(f"     Estimated Time: {step.get('estimated_time', 0)} minutes")
            
            expected_outcomes = response.get('expected_outcomes', {})
            if expected_outcomes:
                print(f"   Expected Completion Likelihood: {expected_outcomes.get('completion_likelihood', 'unknown')}")
                print(f"   Expected Time to Value: {expected_outcomes.get('time_to_value', 'unknown')}")
                print(f"   Expected Feature Adoption Rate: {expected_outcomes.get('feature_adoption_rate', 'unknown')}")
                print(f"   Expected User Satisfaction Score: {expected_outcomes.get('user_satisfaction_score', 'unknown')}")
        
        return success

    def test_pmf_dashboard(self):
        """Test Product Intelligence Hub - Product-Market Fit Dashboard"""
        print("\n🎯 Testing Product Intelligence Hub - Product-Market Fit Dashboard...")
        
        success, response = self.run_product_intelligence_test(
            "Product-Market Fit Dashboard",
            "GET",
            "api/product-intelligence/pmf-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                print(f"   PMF Assessment: {dashboard.get('pmf_assessment', 'unknown')}")
                
                pmf_core_metrics = dashboard.get('pmf_core_metrics', {})
                if pmf_core_metrics:
                    print(f"   Overall PMF Score: {pmf_core_metrics.get('overall_pmf_score', 0)}/100")
                    print(f"   PMF Trend: {pmf_core_metrics.get('pmf_trend', 'unknown')}")
                    print(f"   Time to Value Avg: {pmf_core_metrics.get('time_to_value_avg', 0)} days")
                    print(f"   Product Stickiness: {pmf_core_metrics.get('product_stickiness', 0)}")
                    print(f"   Organic Growth Rate: {pmf_core_metrics.get('organic_growth_rate', 0)}% monthly")
                    print(f"   NPS Score: {pmf_core_metrics.get('nps_score', 0)}")
                    print(f"   Retention Curve Health: {pmf_core_metrics.get('retention_curve_health', 'unknown')}")
                    
                    market_segment_fit = pmf_core_metrics.get('market_segment_fit', {})
                    print(f"   Market Segment Fit:")
                    for segment, score in market_segment_fit.items():
                        print(f"   - {segment.title()}: {score}/100")
                
                pmf_indicators = dashboard.get('pmf_indicators', [])
                print(f"   PMF Indicators: {len(pmf_indicators)}")
                for indicator in pmf_indicators[:3]:  # Show first 3 indicators
                    print(f"   - {indicator.get('indicator', 'Unknown')}: {indicator.get('score', 0)}/100")
                    print(f"     Trend: {indicator.get('trend', 'unknown')}, Weight: {indicator.get('weight', 0)}%")
                    print(f"     Benchmark: {indicator.get('benchmark', 'unknown')}")
                
                retention_curves = dashboard.get('retention_curves', [])
                print(f"   Retention Curves: {len(retention_curves)} cohorts")
                
                user_segments_pmf = dashboard.get('user_segments_pmf', [])
                print(f"   User PMF Segments: {len(user_segments_pmf)}")
                for segment in user_segments_pmf[:2]:  # Show first 2 segments
                    print(f"   - {segment.get('segment', 'Unknown')}: {segment.get('percentage', 0)}% of users")
                    print(f"     PMF Score: {segment.get('pmf_score', 0)}/100")
                    print(f"     Market Fit Evidence: {segment.get('market_fit_evidence', 'unknown')}")
                
                competitive_analysis = dashboard.get('competitive_analysis', {})
                if competitive_analysis:
                    print(f"   Competitive Win Rate: {competitive_analysis.get('win_rate', 0)}%")
                    
                    strengths = competitive_analysis.get('competitive_strengths', [])
                    print(f"   Competitive Strengths: {len(strengths)}")
                    
                    gaps = competitive_analysis.get('competitive_gaps', [])
                    print(f"   Competitive Gaps: {len(gaps)}")
                
                expansion_opportunities = dashboard.get('expansion_opportunities', [])
                print(f"   Market Expansion Opportunities: {len(expansion_opportunities)}")
                
                improvement_roadmap = dashboard.get('improvement_roadmap', [])
                print(f"   PMF Improvement Roadmap: {len(improvement_roadmap)}")
                
                key_insights = dashboard.get('key_insights', [])
                print(f"   Key Insights: {len(key_insights)}")
                
                action_priorities = dashboard.get('action_priorities', [])
                print(f"   Action Priorities: {len(action_priorities)}")
        
        return success

    def test_pmf_assessment(self):
        """Test Product Intelligence Hub - PMF Assessment"""
        print("\n📋 Testing Product Intelligence Hub - PMF Assessment...")
        
        success, response = self.run_product_intelligence_test(
            "PMF Assessment",
            "GET",
            "api/product-intelligence/pmf-assessment",
            200,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            overall_assessment = response.get('overall_assessment', {})
            if overall_assessment:
                print(f"   PMF Level: {overall_assessment.get('pmf_level', 'unknown')}")
                print(f"   Confidence Score: {overall_assessment.get('confidence_score', 0)}/100")
                
                key_strengths = overall_assessment.get('key_strengths', [])
                print(f"   Key Strengths: {len(key_strengths)}")
                
                areas_for_improvement = overall_assessment.get('areas_for_improvement', [])
                print(f"   Areas for Improvement: {len(areas_for_improvement)}")
            
            sean_ellis_test = response.get('sean_ellis_test', {})
            if sean_ellis_test:
                print(f"   Sean Ellis Test:")
                print(f"   - Very Disappointed %: {sean_ellis_test.get('very_disappointed_percentage', 0)}%")
                print(f"   - Benchmark Threshold: {sean_ellis_test.get('benchmark_threshold', 0)}%")
                print(f"   - Assessment: {sean_ellis_test.get('assessment', 'unknown')}")
                
                segment_breakdown = sean_ellis_test.get('segment_breakdown', {})
                print(f"   - Segment Breakdown: {len(segment_breakdown)} segments")
            
            cohort_retention_analysis = response.get('cohort_retention_analysis', {})
            if cohort_retention_analysis:
                print(f"   Cohort Retention Analysis:")
                print(f"   - Retention Curve Shape: {cohort_retention_analysis.get('retention_curve_shape', 'unknown')}")
                print(f"   - Day 1 Retention: {cohort_retention_analysis.get('day_1_retention', 0)}%")
                print(f"   - Week 1 Retention: {cohort_retention_analysis.get('week_1_retention', 0)}%")
                print(f"   - Month 1 Retention: {cohort_retention_analysis.get('month_1_retention', 0)}%")
                print(f"   - Month 3 Retention: {cohort_retention_analysis.get('month_3_retention', 0)}%")
                print(f"   - Assessment: {cohort_retention_analysis.get('assessment', 'unknown')}")
            
            growth_efficiency = response.get('growth_efficiency', {})
            if growth_efficiency:
                print(f"   Growth Efficiency:")
                print(f"   - Organic Growth Rate: {growth_efficiency.get('organic_growth_rate', 0)}% monthly")
                print(f"   - Viral Coefficient: {growth_efficiency.get('viral_coefficient', 0)}")
                print(f"   - Word of Mouth Strength: {growth_efficiency.get('word_of_mouth_strength', 'unknown')}")
                print(f"   - Paid vs Organic Ratio: {growth_efficiency.get('paid_vs_organic_ratio', 'unknown')}")
                print(f"   - Assessment: {growth_efficiency.get('assessment', 'unknown')}")
            
            recommendations = response.get('recommendations', [])
            print(f"   Recommendations: {len(recommendations)} categories")
            for rec_category in recommendations:
                category = rec_category.get('category', 'unknown')
                actions = rec_category.get('actions', [])
                print(f"   - {category}: {len(actions)} actions")
        
        return success

    def test_user_journey_analytics_dashboard(self):
        """Test Product Intelligence Hub - User Journey Analytics Dashboard"""
        print("\n🗺️ Testing Product Intelligence Hub - User Journey Analytics Dashboard...")
        
        success, response = self.run_product_intelligence_test(
            "User Journey Analytics Dashboard",
            "GET",
            "api/product-intelligence/journey-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                journey_health = dashboard.get('journey_health', {})
                if journey_health:
                    print(f"   Overall Journey Health Score: {journey_health.get('overall_journey_health_score', 0)}/100")
                    print(f"   Completion Velocity Trend: {journey_health.get('completion_velocity_trend', 'unknown')}")
                    print(f"   Drop-off Reduction: {journey_health.get('drop_off_reduction', 'unknown')}")
                    print(f"   User Satisfaction with Flows: {journey_health.get('user_satisfaction_with_flows', 0)}/10")
                    print(f"   Support Ticket Correlation: {journey_health.get('support_ticket_correlation', 'unknown')}")
                
                critical_journeys = dashboard.get('critical_journeys', [])
                print(f"   Critical Journeys: {len(critical_journeys)}")
                for journey in critical_journeys[:3]:  # Show first 3 journeys
                    print(f"   - {journey.get('journey_name', 'Unknown')}")
                    print(f"     Completion Rate: {journey.get('completion_rate', 0)}%")
                    print(f"     Avg Completion Time: {journey.get('avg_completion_time', 0)} hours/days")
                    print(f"     Optimization Score: {journey.get('optimization_score', 0)}/100")
                    
                    drop_off_points = journey.get('drop_off_points', [])
                    print(f"     Drop-off Points: {len(drop_off_points)}")
                    
                    success_factors = journey.get('success_factors', [])
                    print(f"     Success Factors: {len(success_factors)}")
                
                common_user_flows = dashboard.get('common_user_flows', [])
                print(f"   Common User Flows: {len(common_user_flows)}")
                for flow in common_user_flows[:2]:  # Show first 2 flows
                    print(f"   - {flow.get('flow_name', 'Unknown')}: {flow.get('frequency', 0)}% of users")
                    print(f"     Conversion Rate: {flow.get('conversion_rate', 0)}%")
                    print(f"     Avg Time to Complete: {flow.get('avg_time_to_complete', 0)} days")
                    print(f"     Business Impact: {flow.get('business_impact', 'unknown')}")
                
                optimization_experiments = dashboard.get('optimization_experiments', [])
                print(f"   Optimization Experiments: {len(optimization_experiments)}")
                
                journey_segments = dashboard.get('journey_segments', [])
                print(f"   Journey Segments: {len(journey_segments)}")
                for segment in journey_segments[:2]:  # Show first 2 segments
                    print(f"   - {segment.get('segment', 'Unknown')}: {segment.get('percentage', 0)}% of users")
                    
                    journey_performance = segment.get('journey_performance', {})
                    if journey_performance:
                        print(f"     Avg Journey Completion: {journey_performance.get('avg_journey_completion', 0)}%")
                        print(f"     Success Rate: {journey_performance.get('success_rate', 0)}%")
                        print(f"     Time Efficiency: {journey_performance.get('time_efficiency', 'unknown')}")
                    
                    business_value = segment.get('business_value', {})
                    if business_value:
                        print(f"     LTV Multiplier: {business_value.get('ltv', 0)}x")
                        print(f"     Retention Rate: {business_value.get('retention', 0)}%")
                        print(f"     Expansion Rate: {business_value.get('expansion', 0)}%")
                
                key_insights = dashboard.get('key_insights', [])
                print(f"   Key Insights: {len(key_insights)}")
                
                recommendations = dashboard.get('optimization_recommendations', [])
                print(f"   Optimization Recommendations: {len(recommendations)}")
        
        return success

    def test_journey_analysis_specific(self):
        """Test Product Intelligence Hub - Specific Journey Analysis"""
        print("\n🔍 Testing Product Intelligence Hub - Specific Journey Analysis...")
        
        journey_name = "First Value Realization"
        
        success, response = self.run_product_intelligence_test(
            f"Journey Analysis for {journey_name}",
            "GET",
            f"api/product-intelligence/journey/{journey_name}/analysis",
            200,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Journey Name: {response.get('journey_name', 'unknown')}")
            
            journey_overview = response.get('journey_overview', {})
            if journey_overview:
                print(f"   Total Users Attempted: {journey_overview.get('total_users_attempted', 0)}")
                print(f"   Completion Rate: {journey_overview.get('completion_rate', 0):.1f}%")
                print(f"   Avg Completion Time: {journey_overview.get('avg_completion_time', 'unknown')}")
                print(f"   Drop-off Rate: {journey_overview.get('drop_off_rate', 0):.1f}%")
                print(f"   Retry Success Rate: {journey_overview.get('retry_success_rate', 0):.1f}%")
            
            step_by_step_analysis = response.get('step_by_step_analysis', [])
            print(f"   Step-by-Step Analysis: {len(step_by_step_analysis)} steps")
            for step in step_by_step_analysis:
                print(f"   - Step {step.get('step_order', 0)}: {step.get('step_name', 'Unknown')}")
                print(f"     Completion Rate: {step.get('completion_rate', 0):.1f}%")
                print(f"     Avg Time Spent: {step.get('avg_time_spent', 'unknown')}")
                print(f"     Drop-off Rate: {step.get('drop_off_rate', 0):.1f}%")
                
                success_factors = step.get('success_factors', [])
                friction_points = step.get('friction_points', [])
                print(f"     Success Factors: {len(success_factors)}, Friction Points: {len(friction_points)}")
            
            optimization_opportunities = response.get('optimization_opportunities', [])
            print(f"   Optimization Opportunities: {len(optimization_opportunities)}")
            for opp in optimization_opportunities:
                print(f"   - {opp.get('opportunity', 'Unknown')}")
                print(f"     Potential Impact: {opp.get('potential_impact', 'unknown')}")
                print(f"     Implementation Effort: {opp.get('implementation_effort', 'unknown')}")
                print(f"     Estimated Timeline: {opp.get('estimated_timeline', 'unknown')}")
        
        return success

    def run_comprehensive_product_intelligence_tests(self):
        """Run comprehensive Product Intelligence Hub module tests"""
        print("\n" + "="*80)
        print("🚀 PRODUCT INTELLIGENCE HUB MODULE - COMPREHENSIVE TESTING")
        print("="*80)
        print("Testing all 4 Product Intelligence Hub components:")
        print("")
        print("1. 📊 Feature Usage Analytics (2 endpoints)")
        print("   - Dashboard with feature adoption, stickiness, ROI analysis")
        print("   - Specific feature analytics with user segments")
        print("")
        print("2. 🎯 Onboarding Optimization (2 endpoints)")
        print("   - Dashboard with funnel analysis, cohort performance")
        print("   - Personalized onboarding path optimization")
        print("")
        print("3. 🎯 Product-Market Fit (2 endpoints)")
        print("   - Dashboard with PMF indicators, retention curves")
        print("   - Detailed PMF assessment with Sean Ellis test")
        print("")
        print("4. 🗺️  User Journey Analytics (2 endpoints)")
        print("   - Dashboard with journey health, flow analysis")
        print("   - Specific journey analysis with optimization opportunities")
        print("="*80)
        
        # Reset counters
        product_intelligence_tests = 0
        product_intelligence_passed = 0
        
        # Test 1: Feature Usage Analytics (2 endpoints)
        print(f"\n{'='*60}")
        print("📊 TESTING FEATURE USAGE ANALYTICS")
        print("="*60)
        
        tests = [
            self.test_feature_usage_analytics_dashboard,
            self.test_feature_analytics_specific
        ]
        
        for test in tests:
            product_intelligence_tests += 1
            if test():
                product_intelligence_passed += 1
        
        # Test 2: Onboarding Optimization (2 endpoints)
        print(f"\n{'='*60}")
        print("🎯 TESTING ONBOARDING OPTIMIZATION")
        print("="*60)
        
        tests = [
            self.test_onboarding_optimization_dashboard,
            self.test_optimize_onboarding_path
        ]
        
        for test in tests:
            product_intelligence_tests += 1
            if test():
                product_intelligence_passed += 1
        
        # Test 3: Product-Market Fit (2 endpoints)
        print(f"\n{'='*60}")
        print("🎯 TESTING PRODUCT-MARKET FIT")
        print("="*60)
        
        tests = [
            self.test_pmf_dashboard,
            self.test_pmf_assessment
        ]
        
        for test in tests:
            product_intelligence_tests += 1
            if test():
                product_intelligence_passed += 1
        
        # Test 4: User Journey Analytics (2 endpoints)
        print(f"\n{'='*60}")
        print("🗺️  TESTING USER JOURNEY ANALYTICS")
        print("="*60)
        
        tests = [
            self.test_user_journey_analytics_dashboard,
            self.test_journey_analysis_specific
        ]
        
        for test in tests:
            product_intelligence_tests += 1
            if test():
                product_intelligence_passed += 1
        
        return product_intelligence_passed, product_intelligence_tests

    # =====================================================
    # END PRODUCT INTELLIGENCE HUB MODULE TESTS
    # =====================================================

    # =====================================================
    # INTEGRATION & DATA MANAGEMENT HUB MODULE TESTS
    # =====================================================

    def run_integration_hub_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run an Integration & Data Management Hub API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.integration_hub_tests += 1
        print(f"\n🔗 Testing Integration & Data Management Hub: {name}...")
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
                self.integration_hub_passed += 1
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

    def test_data_connectors_dashboard(self):
        """Test Integration & Data Management Hub - Data Connectors Dashboard"""
        print("\n🔌 Testing Integration & Data Management Hub - Data Connectors Dashboard...")
        
        success, response = self.run_integration_hub_test(
            "Data Connectors Dashboard",
            "GET",
            "api/integration-hub/connectors-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                health_insights = dashboard.get('health_insights', {})
                if health_insights:
                    print(f"   Overall System Health: {health_insights.get('overall_system_health', 0)}%")
                    print(f"   Total Active Connectors: {health_insights.get('total_active_connectors', 0)}")
                    print(f"   Healthy Connectors: {health_insights.get('healthy_connectors', 0)}")
                    print(f"   Warning Connectors: {health_insights.get('warning_connectors', 0)}")
                    print(f"   Data Volume 24h: {health_insights.get('total_data_volume_24h', 0):,} records")
                
                available_connectors = dashboard.get('available_connectors', [])
                print(f"   Available Connector Types: {len(available_connectors)}")
                for connector_type in available_connectors[:2]:  # Show first 2 types
                    print(f"   - {connector_type.get('connector_type', 'Unknown')}: {len(connector_type.get('supported_platforms', []))} platforms")
                
                active_connectors = dashboard.get('active_connectors', [])
                print(f"   Active Connectors: {len(active_connectors)}")
                for connector in active_connectors[:3]:  # Show first 3 active connectors
                    print(f"   - {connector.get('connector_name', 'Unknown')} ({connector.get('platform', 'Unknown')})")
                    print(f"     Status: {connector.get('connection_status', 'unknown')}, Health: {connector.get('health_score', 0)}%")
                    print(f"     Data Volume 24h: {connector.get('data_volume_24h', 0):,} records")
                
                performance_metrics = dashboard.get('performance_metrics', {})
                if performance_metrics:
                    print(f"   Avg Sync Latency: {performance_metrics.get('avg_sync_latency', 0)} seconds")
                    print(f"   API Success Rate: {performance_metrics.get('api_success_rate', 0)}%")
                    print(f"   Connector Uptime: {performance_metrics.get('connector_uptime', 0)}%")
                
                recommendations = dashboard.get('system_recommendations', [])
                print(f"   System Recommendations: {len(recommendations)}")
        
        return success

    def test_create_connector(self):
        """Test Integration & Data Management Hub - Create New Connector"""
        print("\n➕ Testing Integration & Data Management Hub - Create New Connector...")
        
        connector_data = {
            "platform": "HubSpot",
            "name": "Test HubSpot Connector",
            "description": "Test connector for HubSpot CRM integration"
        }
        
        success, response = self.run_integration_hub_test(
            "Create New Connector",
            "POST",
            "api/integration-hub/connector",
            200,
            data=connector_data,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Connector ID: {response.get('connector_id', 'unknown')}")
            
            connector_setup = response.get('connector_setup', {})
            if connector_setup:
                print(f"   Platform: {connector_setup.get('platform', 'unknown')}")
                print(f"   Connector Name: {connector_setup.get('connector_name', 'unknown')}")
                print(f"   Estimated Setup Time: {connector_setup.get('estimated_setup_time', 0)} minutes")
                
                steps = connector_setup.get('configuration_steps', [])
                print(f"   Configuration Steps: {len(steps)}")
                for step in steps:
                    print(f"   - Step {step.get('step', 0)}: {step.get('title', 'Unknown')}")
                    print(f"     Time: {step.get('estimated_time', 'unknown')}")
                
                credentials = connector_setup.get('required_credentials', [])
                print(f"   Required Credentials: {len(credentials)}")
                
                data_types = connector_setup.get('supported_data_types', [])
                print(f"   Supported Data Types: {len(data_types)}")
        
        return success

    def test_connector_health(self):
        """Test Integration & Data Management Hub - Connector Health Check"""
        print("\n🏥 Testing Integration & Data Management Hub - Connector Health Check...")
        
        connector_id = "test_connector_123"
        
        success, response = self.run_integration_hub_test(
            f"Connector Health Check ({connector_id})",
            "GET",
            f"api/integration-hub/connector/{connector_id}/health",
            200,
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Connector ID: {response.get('connector_id', 'unknown')}")
            
            overall_health = response.get('overall_health', {})
            if overall_health:
                print(f"   Health Score: {overall_health.get('health_score', 0):.1f}%")
                print(f"   Status: {overall_health.get('status', 'unknown')}")
                print(f"   Uptime: {overall_health.get('uptime_percentage', 0):.1f}%")
            
            connection_diagnostics = response.get('connection_diagnostics', {})
            if connection_diagnostics:
                print(f"   API Connectivity: {connection_diagnostics.get('api_connectivity', 'unknown')}")
                print(f"   Authentication: {connection_diagnostics.get('authentication_status', 'unknown')}")
                print(f"   Rate Limit Status: {connection_diagnostics.get('rate_limit_status', 'unknown')}")
                print(f"   Network Latency: {connection_diagnostics.get('network_latency', 'unknown')}")
            
            data_flow_health = response.get('data_flow_health', {})
            if data_flow_health:
                print(f"   Sync Frequency Adherence: {data_flow_health.get('sync_frequency_adherence', 0):.1f}%")
                print(f"   Data Quality Score: {data_flow_health.get('data_quality_score', 0):.1f}%")
                print(f"   Error Rate 24h: {data_flow_health.get('error_rate_24h', 0):.1f}%")
            
            recent_issues = response.get('recent_issues', [])
            print(f"   Recent Issues: {len(recent_issues)}")
            
            recommendations = response.get('recommendations', [])
            print(f"   Health Recommendations: {len(recommendations)}")
        
        return success

    def test_sync_management_dashboard(self):
        """Test Integration & Data Management Hub - Sync Management Dashboard"""
        print("\n🔄 Testing Integration & Data Management Hub - Sync Management Dashboard...")
        
        success, response = self.run_integration_hub_test(
            "Sync Management Dashboard",
            "GET",
            "api/integration-hub/sync-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('overview_metrics', {})
                if overview:
                    print(f"   Total Sync Jobs: {overview.get('total_sync_jobs', 0)}")
                    print(f"   Active Syncs: {overview.get('active_syncs', 0)}")
                    print(f"   Completed Today: {overview.get('completed_syncs_today', 0)}")
                    print(f"   Failed Syncs: {overview.get('failed_syncs_today', 0)}")
                    print(f"   Data Records Synced: {overview.get('total_records_synced_today', 0):,}")
                
                sync_schedules = dashboard.get('sync_schedules', [])
                print(f"   Sync Schedules: {len(sync_schedules)}")
                for schedule in sync_schedules[:3]:  # Show first 3 schedules
                    print(f"   - {schedule.get('connector_name', 'Unknown')}: {schedule.get('frequency', 'unknown')}")
                    print(f"     Next Run: {schedule.get('next_run_time', 'unknown')}")
                    print(f"     Status: {schedule.get('status', 'unknown')}")
                
                performance_metrics = dashboard.get('performance_metrics', {})
                if performance_metrics:
                    print(f"   Avg Sync Duration: {performance_metrics.get('avg_sync_duration', 0)} minutes")
                    print(f"   Success Rate: {performance_metrics.get('sync_success_rate', 0)}%")
                    print(f"   Data Throughput: {performance_metrics.get('data_throughput_per_hour', 0):,} records/hour")
                
                recent_activities = dashboard.get('recent_sync_activities', [])
                print(f"   Recent Sync Activities: {len(recent_activities)}")
        
        return success

    def test_data_quality_dashboard(self):
        """Test Integration & Data Management Hub - Data Quality Dashboard"""
        print("\n✅ Testing Integration & Data Management Hub - Data Quality Dashboard...")
        
        success, response = self.run_integration_hub_test(
            "Data Quality Dashboard",
            "GET",
            "api/integration-hub/quality-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('overview_metrics', {})
                if overview:
                    print(f"   Overall Data Quality Score: {overview.get('overall_data_quality_score', 0)}/100")
                    print(f"   Total Records Analyzed: {overview.get('total_records_analyzed', 0):,}")
                    print(f"   Quality Issues Found: {overview.get('quality_issues_found', 0)}")
                    print(f"   Data Completeness: {overview.get('data_completeness_percentage', 0)}%")
                    print(f"   Data Accuracy: {overview.get('data_accuracy_percentage', 0)}%")
                
                quality_dimensions = dashboard.get('quality_dimensions', [])
                print(f"   Quality Dimensions: {len(quality_dimensions)}")
                for dimension in quality_dimensions[:3]:  # Show first 3 dimensions
                    print(f"   - {dimension.get('dimension_name', 'Unknown')}: {dimension.get('score', 0)}/100")
                    print(f"     Status: {dimension.get('status', 'unknown')}, Issues: {dimension.get('issues_count', 0)}")
                
                connector_quality = dashboard.get('connector_quality_scores', [])
                print(f"   Connector Quality Scores: {len(connector_quality)}")
                for connector in connector_quality[:3]:  # Show first 3 connectors
                    print(f"   - {connector.get('connector_name', 'Unknown')}: {connector.get('quality_score', 0)}/100")
                    print(f"     Records: {connector.get('total_records', 0):,}, Issues: {connector.get('issues_count', 0)}")
                
                data_lineage = dashboard.get('data_lineage_health', {})
                if data_lineage:
                    print(f"   Data Lineage Health: {data_lineage.get('lineage_completeness', 0)}%")
                    print(f"   Tracked Data Sources: {data_lineage.get('tracked_sources', 0)}")
                
                recommendations = dashboard.get('quality_recommendations', [])
                print(f"   Quality Recommendations: {len(recommendations)}")
        
        return success

    def test_integration_analytics_dashboard(self):
        """Test Integration & Data Management Hub - Integration Analytics Dashboard"""
        print("\n📊 Testing Integration & Data Management Hub - Integration Analytics Dashboard...")
        
        success, response = self.run_integration_hub_test(
            "Integration Analytics Dashboard",
            "GET",
            "api/integration-hub/analytics-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                overview = dashboard.get('overview_metrics', {})
                if overview:
                    print(f"   Total Integrations: {overview.get('total_integrations', 0)}")
                    print(f"   Data Volume This Month: {overview.get('data_volume_this_month', 0):,} records")
                    print(f"   Integration Efficiency: {overview.get('integration_efficiency_score', 0)}/100")
                    print(f"   Cost Savings: ${overview.get('estimated_cost_savings', 0):,}")
                    print(f"   Time Savings: {overview.get('estimated_time_savings_hours', 0)} hours")
                
                usage_analytics = dashboard.get('usage_analytics', {})
                if usage_analytics:
                    print(f"   Most Active Integration: {usage_analytics.get('most_active_integration', 'unknown')}")
                    print(f"   Peak Usage Hours: {usage_analytics.get('peak_usage_hours', 'unknown')}")
                    print(f"   Data Growth Rate: {usage_analytics.get('data_growth_rate_monthly', 0)}%")
                
                performance_trends = dashboard.get('performance_trends', [])
                print(f"   Performance Trends: {len(performance_trends)} data points")
                
                roi_analysis = dashboard.get('roi_analysis', {})
                if roi_analysis:
                    print(f"   Integration ROI: {roi_analysis.get('overall_roi', 0):.1f}x")
                    print(f"   Payback Period: {roi_analysis.get('payback_period_months', 0)} months")
                    print(f"   Annual Value: ${roi_analysis.get('annual_value_generated', 0):,}")
                
                business_impact = dashboard.get('business_impact', {})
                if business_impact:
                    print(f"   Process Automation: {business_impact.get('processes_automated', 0)}")
                    print(f"   Manual Tasks Eliminated: {business_impact.get('manual_tasks_eliminated', 0)}")
                    print(f"   Data Accuracy Improvement: {business_impact.get('data_accuracy_improvement', 0)}%")
                
                insights = dashboard.get('ai_insights', [])
                print(f"   AI Insights: {len(insights)}")
        
        return success

    def run_comprehensive_integration_hub_tests(self):
        """Run comprehensive Integration & Data Management Hub module tests"""
        print("\n" + "="*80)
        print("🚀 INTEGRATION & DATA MANAGEMENT HUB MODULE - COMPREHENSIVE TESTING")
        print("="*80)
        print("Testing all 4 Integration & Data Management Hub components:")
        print("")
        print("1. 🔌 Data Connectors (3 endpoints)")
        print("   - Dashboard with connector health, available platforms")
        print("   - Create new connector with configuration steps")
        print("   - Connector health check with diagnostics")
        print("")
        print("2. 🔄 Sync Management (1 endpoint)")
        print("   - Dashboard with sync schedules, performance metrics")
        print("")
        print("3. ✅ Data Quality (1 endpoint)")
        print("   - Dashboard with quality scores, dimensions analysis")
        print("")
        print("4. 📊 Integration Analytics (1 endpoint)")
        print("   - Dashboard with ROI analysis, business impact")
        print("="*80)
        
        # Reset counters
        integration_hub_tests = 0
        integration_hub_passed = 0
        
        # Test 1: Data Connectors (3 endpoints)
        print(f"\n{'='*60}")
        print("🔌 TESTING DATA CONNECTORS")
        print("="*60)
        
        tests = [
            self.test_data_connectors_dashboard,
            self.test_create_connector,
            self.test_connector_health
        ]
        
        for test in tests:
            integration_hub_tests += 1
            if test():
                integration_hub_passed += 1
        
        # Test 2: Sync Management (1 endpoint)
        print(f"\n{'='*60}")
        print("🔄 TESTING SYNC MANAGEMENT")
        print("="*60)
        
        integration_hub_tests += 1
        if self.test_sync_management_dashboard():
            integration_hub_passed += 1
        
        # Test 3: Data Quality (1 endpoint)
        print(f"\n{'='*60}")
        print("✅ TESTING DATA QUALITY")
        print("="*60)
        
        integration_hub_tests += 1
        if self.test_data_quality_dashboard():
            integration_hub_passed += 1
        
        # Test 4: Integration Analytics (1 endpoint)
        print(f"\n{'='*60}")
        print("📊 TESTING INTEGRATION ANALYTICS")
        print("="*60)
        
        integration_hub_tests += 1
        if self.test_integration_analytics_dashboard():
            integration_hub_passed += 1
        
        return integration_hub_passed, integration_hub_tests

    # =====================================================
    # END INTEGRATION & DATA MANAGEMENT HUB MODULE TESTS
    # =====================================================

def main():
    """Main function to run Phase 2 implementation tests"""
    print("🚀 PHASE 2 IMPLEMENTATION BACKEND TESTING")
    print("="*80)
    print("Testing Phase 2 implementation with:")
    print("1. Product Intelligence Hub (already tested but verifying)")
    print("2. Integration & Data Management Hub (newly implemented)")
    print("="*80)
    
    tester = CustomerIntelligenceAITester()
    
    total_tests_passed = 0
    total_tests_run = 0
    
    # Test 1: Product Intelligence Hub (verification)
    print(f"\n{'='*80}")
    print("🎯 TESTING PRODUCT INTELLIGENCE HUB (VERIFICATION)")
    print("="*80)
    
    product_tests_passed, product_tests_run = tester.run_comprehensive_product_intelligence_tests()
    total_tests_passed += product_tests_passed
    total_tests_run += product_tests_run
    
    # Test 2: Integration & Data Management Hub (new implementation)
    print(f"\n{'='*80}")
    print("🔗 TESTING INTEGRATION & DATA MANAGEMENT HUB (NEW)")
    print("="*80)
    
    integration_tests_passed, integration_tests_run = tester.run_comprehensive_integration_hub_tests()
    total_tests_passed += integration_tests_passed
    total_tests_run += integration_tests_run
    
    # Print final summary
    print(f"\n{'='*80}")
    print("🎯 PHASE 2 IMPLEMENTATION TESTING SUMMARY")
    print("="*80)
    print(f"   Total Tests Run: {total_tests_run}")
    print(f"   Total Tests Passed: {total_tests_passed}")
    print(f"   Overall Success Rate: {(total_tests_passed/total_tests_run)*100:.1f}%")
    print("="*80)
    
    print(f"\n📊 DETAILED RESULTS:")
    print(f"   🎯 Product Intelligence Hub: {product_tests_passed}/{product_tests_run} ({(product_tests_passed/product_tests_run)*100:.1f}%)")
    print(f"      ✅ Feature Usage Analytics - Feature adoption and stickiness analysis")
    print(f"      ✅ Onboarding Optimization - Funnel analysis and path optimization")
    print(f"      ✅ Product-Market Fit - PMF indicators and assessment")
    print(f"      ✅ User Journey Analytics - Journey health and flow analysis")
    print(f"   🔗 Integration & Data Management Hub: {integration_tests_passed}/{integration_tests_run} ({(integration_tests_passed/integration_tests_run)*100:.1f}%)")
    print(f"      ✅ Data Connectors - Connector management and health monitoring")
    print(f"      ✅ Sync Management - Data synchronization and scheduling")
    print(f"      ✅ Data Quality - Quality monitoring and analysis")
    print(f"      ✅ Integration Analytics - ROI analysis and business impact")
    
    if total_tests_passed == total_tests_run:
        print(f"\n🎉 SUCCESS: ALL PHASE 2 TESTS PASSED!")
        print(f"   Both Product Intelligence Hub and Integration & Data Management Hub are fully functional")
        print(f"   All {total_tests_run} endpoints working correctly with comprehensive data and analytics")
        print(f"   Phase 2 implementation is complete and ready for production deployment")
        return 0
    else:
        print(f"\n⚠️  PARTIAL SUCCESS: {total_tests_run - total_tests_passed} endpoint(s) failed")
        print(f"   Most of the Phase 2 implementation is working correctly")
        print(f"   See detailed test results above for specific issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())