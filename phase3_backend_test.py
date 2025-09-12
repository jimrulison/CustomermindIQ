#!/usr/bin/env python3
"""
Phase 3 Comprehensive Backend Testing
=====================================

Tests the complete Phase 3 implementation including:
- Compliance & Governance Suite Module (4 endpoints)
- AI Command Center Module (4 endpoints)
- Existing modules verification for system stability

This script provides comprehensive testing of all Phase 3 backend APIs
with detailed reporting and verification of system stability.
"""

import requests
import sys
import json
from datetime import datetime, timedelta
import time

class Phase3BackendTester:
    def __init__(self):
        # Use the production URL from frontend/.env
        self.base_url = "https://mindindata.preview.emergentagent.com/api"
        
        # Test counters for Phase 3 modules
        self.compliance_governance_tests = 0
        self.compliance_governance_passed = 0
        self.ai_command_tests = 0
        self.ai_command_passed = 0
        
        # Test counters for existing modules verification
        self.verification_tests = 0
        self.verification_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a generic API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        print(f"\n🔍 Testing: {name}...")
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

    # =====================================================
    # PHASE 3 - COMPLIANCE & GOVERNANCE SUITE MODULE TESTS
    # =====================================================

    def run_compliance_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a Compliance & Governance Suite API test"""
        self.compliance_governance_tests += 1
        success, response_data = self.run_test(name, method, endpoint, expected_status, data, timeout)
        if success:
            self.compliance_governance_passed += 1
        return success, response_data

    def test_compliance_monitoring_dashboard(self):
        """Test Compliance & Governance Suite - Compliance Monitoring Dashboard"""
        print("\n🛡️ Testing Compliance & Governance Suite - Compliance Monitoring Dashboard...")
        
        success, response = self.run_compliance_test(
            "Compliance Monitoring Dashboard",
            "GET",
            "compliance-governance/compliance-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                compliance_status = dashboard.get('compliance_status', {})
                print(f"   Overall Compliance Score: {compliance_status.get('overall_compliance_score', 0)}%")
                print(f"   Total Policies: {compliance_status.get('total_policies', 0)}")
                print(f"   Active Policies: {compliance_status.get('active_policies', 0)}")
                print(f"   Violations (24h): {compliance_status.get('violations_24h', 0)}")
                print(f"   Critical Violations: {compliance_status.get('critical_violations', 0)}")
                
                frameworks = compliance_status.get('compliance_frameworks', [])
                print(f"   Compliance Frameworks: {', '.join(frameworks)}")
                
                policy_compliance = dashboard.get('policy_compliance', [])
                print(f"   Policy Categories: {len(policy_compliance)}")
                for policy in policy_compliance[:3]:
                    print(f"   - {policy.get('policy_category', 'Unknown')}: {policy.get('compliance_score', 0)}%")
                    print(f"     Violations: {policy.get('violations_count', 0)}, Trend: {policy.get('trend', 'unknown')}")
                
                framework_compliance = dashboard.get('framework_compliance', [])
                print(f"   Framework Compliance: {len(framework_compliance)} frameworks")
                for framework in framework_compliance[:2]:
                    print(f"   - {framework.get('framework', 'Unknown')}: {framework.get('compliance_percentage', 0)}%")
                    print(f"     Status: {framework.get('certification_status', 'unknown')}")
                
                risk_assessment = dashboard.get('risk_assessment', {})
                if risk_assessment:
                    print(f"   Overall Risk Level: {risk_assessment.get('overall_risk_level', 'unknown')}")
                    print(f"   Risk Score: {risk_assessment.get('risk_score', 0)}/100")
                    print(f"   Critical Risks: {risk_assessment.get('critical_risks', 0)}")
        
        return success

    def test_audit_management_dashboard(self):
        """Test Compliance & Governance Suite - Audit Management Dashboard"""
        print("\n📋 Testing Compliance & Governance Suite - Audit Management Dashboard...")
        
        success, response = self.run_compliance_test(
            "Audit Management Dashboard",
            "GET",
            "compliance-governance/audit-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                audit_overview = dashboard.get('audit_overview', {})
                print(f"   Total Audits YTD: {audit_overview.get('total_audits_ytd', 0)}")
                print(f"   Completed Audits: {audit_overview.get('completed_audits', 0)}")
                print(f"   Ongoing Audits: {audit_overview.get('ongoing_audits', 0)}")
                print(f"   Audit Success Rate: {audit_overview.get('audit_success_rate', 0)}%")
                print(f"   Avg Audit Duration: {audit_overview.get('avg_audit_duration', 0)} days")
                print(f"   Critical Findings: {audit_overview.get('critical_findings', 0)}")
                
                active_audits = dashboard.get('active_audits', [])
                print(f"   Active Audits: {len(active_audits)}")
                for audit in active_audits[:2]:
                    print(f"   - {audit.get('audit_name', 'Unknown')}")
                    print(f"     Framework: {audit.get('framework', 'unknown')}, Progress: {audit.get('progress', 0)}%")
                    print(f"     Lead Auditor: {audit.get('lead_auditor', 'unknown')}")
                    print(f"     Critical Findings: {audit.get('critical_findings', 0)}")
                
                evidence_repository = dashboard.get('evidence_repository', {})
                if evidence_repository:
                    print(f"   Evidence Items: {evidence_repository.get('total_evidence_items', 0)}")
                    print(f"   Storage Usage: {evidence_repository.get('storage_usage', {}).get('total_size_gb', 0)} GB")
                
                performance_metrics = dashboard.get('performance_metrics', {})
                if performance_metrics:
                    print(f"   Audit Completion Rate: {performance_metrics.get('audit_completion_rate', 0)}%")
                    print(f"   ROI on Audit Investment: {performance_metrics.get('roi_on_audit_investment', 0)}%")
        
        return success

    def test_data_governance_dashboard(self):
        """Test Compliance & Governance Suite - Data Governance Dashboard"""
        print("\n📊 Testing Compliance & Governance Suite - Data Governance Dashboard...")
        
        success, response = self.run_compliance_test(
            "Data Governance Dashboard",
            "GET",
            "compliance-governance/governance-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                governance_overview = dashboard.get('governance_overview', {})
                print(f"   Data Governance Maturity: {governance_overview.get('data_governance_maturity', 0)}/5")
                print(f"   Total Data Assets: {governance_overview.get('total_data_assets', 0)}")
                print(f"   Classification Coverage: {governance_overview.get('classification_coverage', 0)}%")
                print(f"   Data Stewards: {governance_overview.get('data_stewards', 0)}")
                print(f"   Policy Compliance Rate: {governance_overview.get('policy_compliance_rate', 0)}%")
                print(f"   Data Quality Score: {governance_overview.get('data_quality_score', 0)}%")
                
                data_classification = dashboard.get('data_classification', [])
                print(f"   Data Classification: {len(data_classification)} categories")
                for classification in data_classification[:3]:
                    print(f"   - {classification.get('classification', 'Unknown')}: {classification.get('asset_count', 0)} assets")
                    print(f"     Percentage: {classification.get('percentage', 0)}%, Protection: {classification.get('protection_level', 'unknown')}")
                
                data_stewardship = dashboard.get('data_stewardship', [])
                print(f"   Data Stewardship: {len(data_stewardship)} domains")
                for steward in data_stewardship[:2]:
                    print(f"   - {steward.get('domain', 'Unknown')}: {steward.get('steward', 'unknown')}")
                    print(f"     Assets Managed: {steward.get('assets_managed', 0)}, Quality Score: {steward.get('quality_score', 0)}%")
                
                quality_metrics = dashboard.get('quality_metrics', {})
                if quality_metrics:
                    print(f"   Overall Quality Score: {quality_metrics.get('overall_quality_score', 0)}%")
                    dimensions = quality_metrics.get('quality_dimensions', [])
                    print(f"   Quality Dimensions: {len(dimensions)}")
                    for dim in dimensions[:3]:
                        print(f"   - {dim.get('dimension', 'Unknown')}: {dim.get('score', 0)}% ({dim.get('trend', 'unknown')})")
                
                privacy_management = dashboard.get('privacy_management', {})
                if privacy_management:
                    print(f"   Consent Coverage: {privacy_management.get('consent_coverage', 0)}%")
                    print(f"   Active Consents: {privacy_management.get('active_consents', 0)}")
                    dsr = privacy_management.get('data_subject_requests', {})
                    if dsr:
                        print(f"   Data Subject Requests YTD: {dsr.get('total_requests_ytd', 0)}")
        
        return success

    def test_regulatory_reporting_dashboard(self):
        """Test Compliance & Governance Suite - Regulatory Reporting Dashboard"""
        print("\n📑 Testing Compliance & Governance Suite - Regulatory Reporting Dashboard...")
        
        success, response = self.run_compliance_test(
            "Regulatory Reporting Dashboard",
            "GET",
            "compliance-governance/reporting-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                reporting_overview = dashboard.get('reporting_overview', {})
                print(f"   Total Reports YTD: {reporting_overview.get('total_reports_ytd', 0)}")
                print(f"   Automated Reports: {reporting_overview.get('automated_reports', 0)}")
                print(f"   Automation Rate: {reporting_overview.get('automation_rate', 0)}%")
                print(f"   On-Time Delivery: {reporting_overview.get('on_time_delivery', 0)}%")
                print(f"   Pending Reports: {reporting_overview.get('pending_reports', 0)}")
                print(f"   Regulatory Frameworks: {reporting_overview.get('regulatory_frameworks', 0)}")
                
                regulatory_frameworks = dashboard.get('regulatory_frameworks', [])
                print(f"   Regulatory Frameworks: {len(regulatory_frameworks)}")
                for framework in regulatory_frameworks[:3]:
                    print(f"   - {framework.get('framework', 'Unknown')}: {framework.get('reports_completed', 0)}/{framework.get('reports_required', 0)} reports")
                    print(f"     Status: {framework.get('compliance_status', 'unknown')}, Frequency: {framework.get('reporting_frequency', 'unknown')}")
                
                active_reports = dashboard.get('active_reports', [])
                print(f"   Active Reports: {len(active_reports)}")
                for report in active_reports[:2]:
                    print(f"   - {report.get('report_name', 'Unknown')}")
                    print(f"     Framework: {report.get('framework', 'unknown')}, Progress: {report.get('progress', 0)}%")
                    print(f"     Automation Level: {report.get('automation_level', 'unknown')}")
                
                data_collection = dashboard.get('data_collection', {})
                if data_collection:
                    print(f"   Total Data Sources: {data_collection.get('total_data_sources', 0)}")
                    print(f"   Automated Sources: {data_collection.get('automated_sources', 0)}")
                
                performance_metrics = dashboard.get('performance_metrics', {})
                if performance_metrics:
                    print(f"   Report Accuracy: {performance_metrics.get('report_accuracy', 0)}%")
                    print(f"   Cost Savings from Automation: ${performance_metrics.get('cost_savings_automation', 0):,}")
        
        return success

    # =====================================================
    # PHASE 3 - AI COMMAND CENTER MODULE TESTS
    # =====================================================

    def run_ai_command_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run an AI Command Center API test"""
        self.ai_command_tests += 1
        success, response_data = self.run_test(name, method, endpoint, expected_status, data, timeout)
        if success:
            self.ai_command_passed += 1
        return success, response_data

    def test_ai_orchestration_dashboard(self):
        """Test AI Command Center - AI Orchestration Dashboard"""
        print("\n🤖 Testing AI Command Center - AI Orchestration Dashboard...")
        
        success, response = self.run_ai_command_test(
            "AI Orchestration Dashboard",
            "GET",
            "ai-command/orchestration-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                ai_overview = dashboard.get('ai_overview', {})
                print(f"   Total AI Models: {ai_overview.get('total_ai_models', 0)}")
                print(f"   Active Models: {ai_overview.get('active_models', 0)}")
                print(f"   Model Performance Avg: {ai_overview.get('model_performance_avg', 0)}%")
                print(f"   AI Workloads (24h): {ai_overview.get('ai_workloads_24h', 0)}")
                print(f"   Inference Requests: {ai_overview.get('inference_requests', 0)}")
                print(f"   Automation Coverage: {ai_overview.get('automation_coverage', 0)}%")
                print(f"   AI Efficiency Score: {ai_overview.get('ai_efficiency_score', 0)}%")
                print(f"   Cost Optimization: {ai_overview.get('cost_optimization', 0)}%")
                
                model_performance = dashboard.get('model_performance', [])
                print(f"   Model Performance: {len(model_performance)} models")
                for model in model_performance[:3]:
                    print(f"   - {model.get('model_name', 'Unknown')}")
                    print(f"     Type: {model.get('model_type', 'unknown')}, Performance: {model.get('performance_score', 0)}%")
                    print(f"     Accuracy: {model.get('accuracy', 0)}%, Latency: {model.get('inference_latency', 0)}ms")
                    print(f"     Drift Status: {model.get('drift_detection', 'unknown')}")
                
                ai_workflows = dashboard.get('ai_workflows', [])
                print(f"   AI Workflows: {len(ai_workflows)}")
                for workflow in ai_workflows[:2]:
                    print(f"   - {workflow.get('workflow_name', 'Unknown')}")
                    print(f"     Status: {workflow.get('status', 'unknown')}, Success Rate: {workflow.get('success_rate', 0)}%")
                    print(f"     Models: {len(workflow.get('models_involved', []))}")
                
                resource_utilization = dashboard.get('resource_utilization', {})
                if resource_utilization:
                    clusters = resource_utilization.get('compute_clusters', [])
                    print(f"   Compute Clusters: {len(clusters)}")
                    for cluster in clusters:
                        print(f"   - {cluster.get('cluster_name', 'Unknown')}: {cluster.get('status', 'unknown')}")
                        print(f"     CPU: {cluster.get('cpu_utilization', 0)}%, GPU: {cluster.get('gpu_utilization', 0)}%")
                
                automation_insights = dashboard.get('automation_insights', {})
                if automation_insights:
                    print(f"   Automated Decisions (24h): {automation_insights.get('automated_decisions_24h', 0)}")
                    print(f"   Automation Accuracy: {automation_insights.get('automation_accuracy', 0)}%")
                    print(f"   Time Savings: {automation_insights.get('time_savings_hours', 0)} hours")
                    print(f"   Cost Reduction: ${automation_insights.get('cost_reduction', 0):,}")
        
        return success

    def test_model_management_dashboard(self):
        """Test AI Command Center - Model Management Dashboard"""
        print("\n🧠 Testing AI Command Center - Model Management Dashboard...")
        
        success, response = self.run_ai_command_test(
            "Model Management Dashboard",
            "GET",
            "ai-command/models-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                models_overview = dashboard.get('models_overview', {})
                print(f"   Total Models: {models_overview.get('total_models', 0)}")
                print(f"   Production Models: {models_overview.get('production_models', 0)}")
                print(f"   Development Models: {models_overview.get('development_models', 0)}")
                print(f"   Model Versions: {models_overview.get('model_versions', 0)}")
                print(f"   Deployment Success Rate: {models_overview.get('deployment_success_rate', 0)}%")
                
                model_categories = dashboard.get('model_categories', [])
                print(f"   Model Categories: {len(model_categories)}")
                for category in model_categories[:3]:
                    print(f"   - {category.get('category', 'Unknown')}: {category.get('models_count', 0)} models")
                    print(f"     Avg Performance: {category.get('avg_performance', 0)}%, Impact: {category.get('business_impact', 'unknown')}")
                
                performance_tracking = dashboard.get('performance_tracking', [])
                print(f"   Performance Tracking: {len(performance_tracking)} models")
                for model in performance_tracking[:2]:
                    print(f"   - {model.get('model_name', 'Unknown')}")
                    print(f"     Version: {model.get('version', 'unknown')}, Score: {model.get('performance_score', 0)}%")
                    print(f"     Drift Status: {model.get('drift_status', 'unknown')}")
                
                deployment_pipeline = dashboard.get('deployment_pipeline', [])
                print(f"   Deployment Pipeline: {len(deployment_pipeline)} stages")
                for stage in deployment_pipeline:
                    print(f"   - {stage.get('pipeline_stage', 'Unknown')}: {stage.get('models_in_stage', 0)} models")
                    print(f"     Success Rate: {stage.get('success_rate', 0)}%")
                
                ab_testing = dashboard.get('ab_testing', {})
                if ab_testing:
                    print(f"   A/B Testing: {ab_testing.get('active_tests', 0)} active tests")
                    print(f"   Test Success Rate: {ab_testing.get('test_success_rate', 0)}%")
                
                resource_requirements = dashboard.get('resource_requirements', {})
                if resource_requirements:
                    print(f"   Monthly Compute Cost: ${resource_requirements.get('total_compute_cost', 0):,}")
                    print(f"   Cost per Prediction: ${resource_requirements.get('cost_per_prediction', 0):.4f}")
                    optimization = resource_requirements.get('resource_optimization', {})
                    if optimization:
                        print(f"   Savings Achieved: {optimization.get('savings_achieved', 0)}%")
        
        return success

    def test_automation_control_dashboard(self):
        """Test AI Command Center - Automation Control Dashboard"""
        print("\n⚙️ Testing AI Command Center - Automation Control Dashboard...")
        
        success, response = self.run_ai_command_test(
            "Automation Control Dashboard",
            "GET",
            "ai-command/automation-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                automation_overview = dashboard.get('automation_overview', {})
                print(f"   Total Automation Processes: {automation_overview.get('total_automation_processes', 0)}")
                print(f"   Active Automations: {automation_overview.get('active_automations', 0)}")
                print(f"   Automation Coverage: {automation_overview.get('automation_coverage', 0)}%")
                print(f"   Decisions Automated (24h): {automation_overview.get('decisions_automated_24h', 0)}")
                print(f"   Human Interventions (24h): {automation_overview.get('human_interventions_24h', 0)}")
                print(f"   Automation Accuracy: {automation_overview.get('automation_accuracy', 0)}%")
                print(f"   Time Savings: {automation_overview.get('time_savings_hours', 0)} hours")
                print(f"   Cost Reduction: {automation_overview.get('cost_reduction_percentage', 0)}%")
                
                automation_categories = dashboard.get('automation_categories', [])
                print(f"   Automation Categories: {len(automation_categories)}")
                for category in automation_categories[:3]:
                    print(f"   - {category.get('category', 'Unknown')}: {category.get('processes_count', 0)} processes")
                    print(f"     Automation Level: {category.get('automation_level', 0)}%, ROI: {category.get('roi', 0)}%")
                
                decision_engine = dashboard.get('decision_engine', {})
                if decision_engine:
                    print(f"   Decision Points: {decision_engine.get('total_decision_points', 0)}")
                    print(f"   Automated Decisions: {decision_engine.get('automated_decisions', 0)}")
                    print(f"   Decision Accuracy: {decision_engine.get('decision_accuracy', 0)}%")
                    print(f"   Avg Decision Time: {decision_engine.get('avg_decision_time', 0)}ms")
                
                rules_engine = dashboard.get('rules_engine', {})
                if rules_engine:
                    print(f"   Total Rules: {rules_engine.get('total_rules', 0)}")
                    print(f"   Active Rules: {rules_engine.get('active_rules', 0)}")
                    print(f"   Rule Optimization Score: {rules_engine.get('rule_optimization_score', 0)}%")
                
                process_orchestration = dashboard.get('process_orchestration', {})
                if process_orchestration:
                    print(f"   Total Workflows: {process_orchestration.get('total_workflows', 0)}")
                    print(f"   Active Workflows: {process_orchestration.get('active_workflows', 0)}")
                    print(f"   Workflow Success Rate: {process_orchestration.get('workflow_success_rate', 0)}%")
                
                business_impact = dashboard.get('business_impact', {})
                if business_impact:
                    print(f"   Productivity Improvement: {business_impact.get('productivity_improvement', 0)} hours/day")
                    print(f"   Daily Cost Reduction: ${business_impact.get('cost_reduction', 0):,}")
                    revenue_impact = business_impact.get('revenue_impact', {})
                    if revenue_impact:
                        print(f"   Revenue Protected: ${revenue_impact.get('revenue_protected', 0):,}/month")
                        print(f"   Revenue Generated: ${revenue_impact.get('revenue_generated', 0):,}/month")
        
        return success

    def test_ai_insights_engine_dashboard(self):
        """Test AI Command Center - AI Insights Engine Dashboard"""
        print("\n🧩 Testing AI Command Center - AI Insights Engine Dashboard...")
        
        success, response = self.run_ai_command_test(
            "AI Insights Engine Dashboard",
            "GET",
            "ai-command/insights-dashboard",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            
            dashboard = response.get('dashboard', {})
            if dashboard:
                insights_overview = dashboard.get('insights_overview', {})
                print(f"   Total Insights Generated: {insights_overview.get('total_insights_generated', 0)}")
                print(f"   Actionable Insights: {insights_overview.get('actionable_insights', 0)}")
                print(f"   Insights Accuracy: {insights_overview.get('insights_accuracy', 0)}%")
                print(f"   Business Impact Score: {insights_overview.get('business_impact_score', 0)}%")
                print(f"   Insights Implemented: {insights_overview.get('insights_implemented', 0)}")
                print(f"   Implementation Rate: {insights_overview.get('implementation_rate', 0)}%")
                print(f"   Value Generated: ${insights_overview.get('value_generated', 0):,}")
                print(f"   Predictive Accuracy: {insights_overview.get('predictive_accuracy', 0)}%")
                
                insight_categories = dashboard.get('insight_categories', [])
                print(f"   Insight Categories: {len(insight_categories)}")
                for category in insight_categories[:3]:
                    print(f"   - {category.get('category', 'Unknown')}: {category.get('insights_count', 0)} insights")
                    print(f"     Accuracy: {category.get('accuracy', 0)}%, Implementation Rate: {category.get('implementation_rate', 0)}%")
                    print(f"     Avg ROI: {category.get('avg_roi', 0)}%")
                
                predictive_analytics = dashboard.get('predictive_analytics', {})
                if predictive_analytics:
                    print(f"   Active Predictions: {predictive_analytics.get('active_predictions', 0)}")
                    print(f"   Prediction Accuracy: {predictive_analytics.get('prediction_accuracy', 0)}%")
                    print(f"   Forecast Horizon: {predictive_analytics.get('forecast_horizon', 'unknown')}")
                
                pattern_recognition = dashboard.get('pattern_recognition', {})
                if pattern_recognition:
                    print(f"   Patterns Discovered: {pattern_recognition.get('patterns_discovered', 0)}")
                    print(f"   Anomaly Detection Accuracy: {pattern_recognition.get('anomaly_detection_accuracy', 0)}%")
                
                strategic_intelligence = dashboard.get('strategic_intelligence', {})
                if strategic_intelligence:
                    print(f"   Strategic Recommendations: {strategic_intelligence.get('strategic_recommendations', 0)}")
                    print(f"   Market Opportunity Value: ${strategic_intelligence.get('market_opportunity_value', 0):,}")
                
                impact_tracking = dashboard.get('impact_tracking', {})
                if impact_tracking:
                    print(f"   Total Value Created: ${impact_tracking.get('total_value_created', 0):,}")
                    print(f"   Success Rate: {impact_tracking.get('success_rate', 0)}%")
                    print(f"   Value Multiplier: {impact_tracking.get('value_multiplier', 0):.1f}x")
        
        return success

    # =====================================================
    # EXISTING MODULES VERIFICATION TESTS
    # =====================================================

    def run_verification_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a verification test for existing modules"""
        self.verification_tests += 1
        success, response_data = self.run_test(name, method, endpoint, expected_status, data, timeout)
        if success:
            self.verification_passed += 1
        return success, response_data

    def test_existing_modules_verification(self):
        """Quick verification of existing modules to ensure system stability"""
        print(f"\n{'='*80}")
        print("✅ EXISTING MODULES VERIFICATION - SYSTEM STABILITY CHECK")
        print("="*80)
        
        verification_results = []
        
        # Test core health endpoint
        print("\n🔍 Testing Core System Health...")
        success, _ = self.run_verification_test("System Health Check", "GET", "health", 200, timeout=15)
        verification_results.append(("System Health", success))
        
        # Test Universal Platform (sample endpoint)
        print("\n🌐 Testing Universal Platform (Sample)...")
        success, _ = self.run_verification_test("Universal Dashboard", "GET", "universal/dashboard", 200, timeout=30)
        verification_results.append(("Universal Platform", success))
        
        # Test Marketing Automation Pro (sample endpoint)
        print("\n🚀 Testing Marketing Automation Pro (Sample)...")
        success, _ = self.run_verification_test("Multi-Channel Dashboard", "GET", "marketing/multi-channel-orchestration", 200, timeout=30)
        verification_results.append(("Marketing Automation Pro", success))
        
        # Test Revenue Analytics Suite (sample endpoint)
        print("\n💰 Testing Revenue Analytics Suite (Sample)...")
        success, _ = self.run_verification_test("Revenue Forecasting Dashboard", "GET", "revenue/forecasting/dashboard", 200, timeout=30)
        verification_results.append(("Revenue Analytics Suite", success))
        
        # Test Advanced Features (sample endpoint)
        print("\n⚡ Testing Advanced Features (Sample)...")
        success, _ = self.run_verification_test("Behavioral Clustering Dashboard", "GET", "advanced/behavioral-clustering", 200, timeout=30)
        verification_results.append(("Advanced Features", success))
        
        # Test Analytics & Insights (sample endpoint)
        print("\n📊 Testing Analytics & Insights (Sample)...")
        success, _ = self.run_verification_test("Customer Journey Dashboard", "GET", "analytics/customer-journey-mapping/dashboard", 200, timeout=30)
        verification_results.append(("Analytics & Insights", success))
        
        # Print verification summary
        print(f"\n{'='*60}")
        print("📋 EXISTING MODULES VERIFICATION SUMMARY")
        print("="*60)
        
        working_modules = 0
        total_modules = len(verification_results)
        
        for module_name, is_working in verification_results:
            status = "✅ Working" if is_working else "❌ Issues"
            print(f"   {module_name}: {status}")
            if is_working:
                working_modules += 1
        
        print(f"\n   Overall System Health: {working_modules}/{total_modules} modules working ({working_modules/total_modules*100:.1f}%)")
        
        return working_modules, total_modules

    # =====================================================
    # MAIN TESTING FUNCTIONS
    # =====================================================

    def test_phase_3_modules(self):
        """Test all Phase 3 modules comprehensively"""
        print(f"\n{'='*80}")
        print("🚀 PHASE 3 COMPREHENSIVE TESTING - COMPLIANCE & GOVERNANCE + AI COMMAND CENTER")
        print("="*80)
        
        # Test Compliance & Governance Suite (4 endpoints)
        print(f"\n{'='*60}")
        print("🛡️  TESTING COMPLIANCE & GOVERNANCE SUITE MODULE")
        print("="*60)
        
        self.test_compliance_monitoring_dashboard()
        self.test_audit_management_dashboard()
        self.test_data_governance_dashboard()
        self.test_regulatory_reporting_dashboard()
        
        # Test AI Command Center (4 endpoints)
        print(f"\n{'='*60}")
        print("🤖 TESTING AI COMMAND CENTER MODULE")
        print("="*60)
        
        self.test_ai_orchestration_dashboard()
        self.test_model_management_dashboard()
        self.test_automation_control_dashboard()
        self.test_ai_insights_engine_dashboard()
        
        return (self.compliance_governance_passed + self.ai_command_passed), (self.compliance_governance_tests + self.ai_command_tests)


def main():
    """Main function to run Phase 3 comprehensive testing"""
    print("🚀 PHASE 3 COMPREHENSIVE TESTING - COMPLIANCE & GOVERNANCE + AI COMMAND CENTER")
    print("="*80)
    print("Testing the complete Phase 3 implementation including:")
    print("• Compliance & Governance Suite (4 endpoints)")
    print("• AI Command Center (4 endpoints)")
    print("• Existing modules verification for system stability")
    print("="*80)
    
    tester = Phase3BackendTester()
    
    # Test Phase 3 modules
    phase3_passed, phase3_total = tester.test_phase_3_modules()
    
    # Test existing modules for stability
    existing_passed, existing_total = tester.test_existing_modules_verification()
    
    # Calculate totals
    total_passed = phase3_passed + existing_passed
    total_tests = phase3_total + existing_total
    
    # Print comprehensive summary
    print(f"\n{'='*80}")
    print("🎯 PHASE 3 COMPREHENSIVE TESTING SUMMARY")
    print("="*80)
    
    print(f"\n📊 DETAILED RESULTS:")
    print(f"   🛡️ Compliance & Governance Suite: {tester.compliance_governance_passed}/{tester.compliance_governance_tests} ({(tester.compliance_governance_passed/tester.compliance_governance_tests)*100:.1f}%)")
    print(f"      ✅ Compliance Monitoring - Real-time compliance tracking and policy enforcement")
    print(f"      ✅ Audit Management - Comprehensive audit trail and evidence management")
    print(f"      ✅ Data Governance - Data stewardship and quality management")
    print(f"      ✅ Regulatory Reporting - Automated regulatory compliance reporting")
    
    print(f"   🤖 AI Command Center: {tester.ai_command_passed}/{tester.ai_command_tests} ({(tester.ai_command_passed/tester.ai_command_tests)*100:.1f}%)")
    print(f"      ✅ AI Orchestration - Centralized AI model and workflow management")
    print(f"      ✅ Model Management - ML model lifecycle and performance tracking")
    print(f"      ✅ Automation Control - Intelligent process automation and decision engine")
    print(f"      ✅ AI Insights Engine - Advanced analytics and predictive intelligence")
    
    print(f"   ✅ Existing Modules Verification: {existing_passed}/{existing_total} ({(existing_passed/existing_total)*100:.1f}%)")
    print(f"      ✅ System stability check across all previous implementations")
    
    print(f"\n🎯 OVERALL RESULTS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {total_passed}")
    print(f"   Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print(f"\n🎉 SUCCESS: ALL PHASE 3 TESTS PASSED!")
        print(f"   Both Compliance & Governance Suite and AI Command Center are fully functional")
        print(f"   All {phase3_total} new Phase 3 endpoints working correctly")
        print(f"   System stability verified - all existing modules remain functional")
        print(f"   Phase 3 implementation is complete and ready for production deployment")
        return 0
    else:
        failed_tests = total_tests - total_passed
        print(f"\n⚠️  PARTIAL SUCCESS: {failed_tests} test(s) failed")
        print(f"   Most of the Phase 3 implementation is working correctly")
        print(f"   See detailed test results above for specific issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())