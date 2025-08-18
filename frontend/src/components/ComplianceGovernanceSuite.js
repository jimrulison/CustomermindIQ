import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Shield, 
  FileText, 
  Database, 
  BarChart3, 
  CheckCircle,
  AlertTriangle,
  Clock,
  Settings,
  Users,
  Lock,
  Scale,
  BookOpen,
  Eye,
  Award
} from 'lucide-react';

const ComplianceGovernanceSuite = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [complianceData, setComplianceData] = useState(null);
  const [auditData, setAuditData] = useState(null);
  const [governanceData, setGovernanceData] = useState(null);
  const [reportingData, setReportingData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadComplianceData();
  }, []);

  const loadComplianceData = async () => {
    try {
      setLoading(true);
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      
      const [compliance, audit, governance, reporting] = await Promise.all([
        fetch(`${backendUrl}/api/compliance-governance/compliance-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/compliance-governance/audit-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/compliance-governance/governance-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/compliance-governance/reporting-dashboard`).then(r => r.json())
      ]);
      
      setComplianceData(compliance);
      setAuditData(audit);
      setGovernanceData(governance);
      setReportingData(reporting);
    } catch (error) {
      console.error('Error loading Compliance & Governance data:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'compliance', name: 'Compliance Monitoring', icon: Shield },
    { id: 'audit', name: 'Audit Management', icon: FileText },
    { id: 'governance', name: 'Data Governance', icon: Database },
    { id: 'reporting', name: 'Regulatory Reporting', icon: BookOpen }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Compliance & Governance Suite</h1>
          <p className="text-slate-400 mt-2">Enterprise-grade compliance management, audit trails, and data governance</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className="bg-green-500/20 text-green-400">
            {complianceData?.dashboard?.compliance_status?.overall_compliance_score || '0'}% Compliant
          </Badge>
          <Badge className="bg-purple-500/20 text-purple-400">4 Core Modules</Badge>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Icon className="w-4 h-4 mr-2" />
              {tab.name}
            </button>
          );
        })}
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Shield className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {complianceData?.dashboard?.compliance_status?.overall_compliance_score || '0'}%
                  </div>
                  <div className="text-xs text-green-200">Compliance Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <FileText className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {auditData?.dashboard?.audit_overview?.completed_audits || '0'}
                  </div>
                  <div className="text-xs text-blue-200">Completed Audits</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Database className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {governanceData?.dashboard?.governance_overview?.classification_coverage || '0'}%
                  </div>
                  <div className="text-xs text-purple-200">Data Classification</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <BookOpen className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {reportingData?.dashboard?.reporting_overview?.automation_rate || '0'}%
                  </div>
                  <div className="text-xs text-orange-200">Report Automation</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Key Metrics */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Award className="w-5 h-5 mr-2 text-cyan-400" />
                  Compliance Frameworks
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {complianceData?.dashboard?.framework_compliance?.map((framework, index) => (
                  <div key={index} className="flex justify-between items-center">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${
                        framework.compliance_percentage > 95 
                          ? 'bg-green-400' 
                          : framework.compliance_percentage > 85 
                            ? 'bg-yellow-400' 
                            : 'bg-red-400'
                      }`}></div>
                      <span className="text-slate-300">{framework.framework}</span>
                    </div>
                    <div className="text-right">
                      <div className="text-white font-semibold">{framework.compliance_percentage}%</div>
                      <Badge className={`text-xs ${
                        framework.certification_status === 'certified'
                          ? 'bg-green-500/20 text-green-400'
                          : framework.certification_status === 'in_progress'
                            ? 'bg-blue-500/20 text-blue-400'
                            : 'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {framework.certification_status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Lock className="w-5 h-5 mr-2 text-orange-400" />
                  Risk Assessment
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-400 mb-1">
                    {complianceData?.dashboard?.risk_assessment?.overall_risk_level?.toUpperCase() || 'UNKNOWN'}
                  </div>
                  <div className="text-slate-400">Overall Risk Level</div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-xl font-bold text-red-400">
                      {complianceData?.dashboard?.risk_assessment?.critical_risks || '0'}
                    </div>
                    <div className="text-xs text-slate-400">Critical Risks</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl font-bold text-yellow-400">
                      {complianceData?.dashboard?.risk_assessment?.high_risks || '0'}
                    </div>
                    <div className="text-xs text-slate-400">High Risks</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Compliance Monitoring Tab */}
      {activeTab === 'compliance' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {complianceData?.dashboard?.policy_compliance?.map((policy, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span>{policy.policy_category}</span>
                    <Badge className={`text-xs ${
                      policy.trend === 'improving' 
                        ? 'bg-green-500/20 text-green-400' 
                        : policy.trend === 'stable'
                          ? 'bg-blue-500/20 text-blue-400'
                          : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {policy.trend}
                    </Badge>
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Criticality: {policy.criticality} • Frameworks: {policy.frameworks?.join(', ')}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">Compliance Score</span>
                      <span className="text-2xl font-bold text-green-400">{policy.compliance_score}%</span>
                    </div>
                    
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
                        style={{ width: `${policy.compliance_score}%` }}
                      ></div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <div className="text-lg font-bold text-blue-400">
                          {policy.total_rules}
                        </div>
                        <div className="text-xs text-slate-400">Total Rules</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-red-400">
                          {policy.violations_count}
                        </div>
                        <div className="text-xs text-slate-400">Violations</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Recent Violations */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2 text-red-400" />
                Recent Compliance Violations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {complianceData?.dashboard?.recent_violations?.map((violation, index) => (
                  <div key={index} className="border-l-4 border-red-500 pl-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-semibold text-white">{violation.policy}</h4>
                        <p className="text-sm text-slate-400">{violation.description}</p>
                        <div className="flex items-center mt-2 space-x-2">
                          <Badge className={`text-xs ${
                            violation.severity === 'high'
                              ? 'bg-red-500/20 text-red-400'
                              : violation.severity === 'medium'
                                ? 'bg-yellow-500/20 text-yellow-400'
                                : 'bg-blue-500/20 text-blue-400'
                          }`}>
                            {violation.severity}
                          </Badge>
                          <Badge className={`text-xs ${
                            violation.status === 'resolved'
                              ? 'bg-green-500/20 text-green-400'
                              : violation.status === 'investigating'
                                ? 'bg-blue-500/20 text-blue-400'
                                : 'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {violation.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs text-slate-400">
                          {new Date(violation.timestamp).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Audit Management Tab */}
      {activeTab === 'audit' && (
        <div className="space-y-6">
          <div className="grid gap-6">
            {auditData?.dashboard?.active_audits?.map((audit, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span>{audit.audit_name}</span>
                    <div className="flex items-center space-x-2">
                      <Badge className={`text-xs ${
                        audit.status === 'in_progress'
                          ? 'bg-blue-500/20 text-blue-400'
                          : audit.status === 'completed'
                            ? 'bg-green-500/20 text-green-400'
                            : 'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {audit.status}
                      </Badge>
                      <Badge className="bg-slate-600/50 text-slate-300">
                        {audit.framework}
                      </Badge>
                    </div>
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Lead Auditor: {audit.lead_auditor} • Firm: {audit.audit_firm}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {audit.status === 'in_progress' && (
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-slate-300">Progress</span>
                          <span className="text-white font-semibold">{audit.progress}%</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${audit.progress}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <div className="text-lg font-bold text-blue-400">
                          {audit.findings_count}
                        </div>
                        <div className="text-xs text-slate-400">Total Findings</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-red-400">
                          {audit.critical_findings}
                        </div>
                        <div className="text-xs text-slate-400">Critical</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-purple-400">
                          {audit.scope?.length || 0}
                        </div>
                        <div className="text-xs text-slate-400">Scope Areas</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-orange-400">
                          {audit.current_phase}
                        </div>
                        <div className="text-xs text-slate-400">Current Phase</div>
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-2">
                      {audit.scope?.map((item, scopeIndex) => (
                        <Badge key={scopeIndex} className="bg-blue-500/10 text-blue-300 text-xs">
                          {item}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Data Governance Tab */}
      {activeTab === 'governance' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Data Classification</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {governanceData?.dashboard?.data_classification?.map((classification, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-300">{classification.classification}</span>
                        <div className="flex items-center space-x-2">
                          <span className="text-white font-semibold">{classification.percentage}%</span>
                          <Badge className={`text-xs ${
                            classification.encryption_required
                              ? 'bg-red-500/20 text-red-400'
                              : 'bg-green-500/20 text-green-400'
                          }`}>
                            {classification.encryption_required ? 'Encrypted' : 'Standard'}
                          </Badge>
                        </div>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                          style={{ width: `${classification.percentage}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-slate-400">
                        {classification.asset_count?.toLocaleString()} assets • Protection: {classification.protection_level}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Data Stewards</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {governanceData?.dashboard?.data_stewardship?.map((steward, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{steward.steward}</h4>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {steward.department}
                        </Badge>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs mb-2">
                        <div className="text-slate-400">
                          Domain: {steward.domain}
                        </div>
                        <div className="text-slate-400">
                          Assets: {steward.assets_managed?.toLocaleString()}
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="text-slate-300">
                          Quality: <span className="text-green-400 font-semibold">{steward.quality_score}</span>
                        </div>
                        <div className="text-slate-300">
                          Compliance: <span className="text-blue-400 font-semibold">{steward.policy_compliance}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Regulatory Reporting Tab */}
      {activeTab === 'reporting' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Active Reports</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reportingData?.dashboard?.active_reports?.map((report, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{report.report_name}</h4>
                        <Badge className={`text-xs ${
                          report.status === 'in_progress'
                            ? 'bg-blue-500/20 text-blue-400'
                            : report.status === 'completed'
                              ? 'bg-green-500/20 text-green-400'
                              : report.status === 'review'
                                ? 'bg-purple-500/20 text-purple-400'
                                : 'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {report.status}
                        </Badge>
                      </div>
                      
                      {report.status === 'in_progress' && (
                        <div className="mb-3">
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-xs text-slate-400">Progress</span>
                            <span className="text-xs text-white">{report.progress}%</span>
                          </div>
                          <div className="w-full bg-slate-700 rounded-full h-1">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-purple-500 h-1 rounded-full"
                              style={{ width: `${report.progress}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                      
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="text-slate-400">
                          Framework: {report.framework}
                        </div>
                        <div className="text-slate-400">
                          Type: {report.report_type}
                        </div>
                        <div className="text-slate-400">
                          Assigned: {report.assigned_to}
                        </div>
                        <div className="text-slate-400">
                          Automation: {report.automation_level}
                        </div>
                      </div>
                      
                      <div className="flex flex-wrap gap-1 mt-2">
                        {report.data_sources?.slice(0, 3).map((source, sourceIndex) => (
                          <Badge key={sourceIndex} className="bg-slate-600/30 text-slate-300 text-xs">
                            {source}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Regulatory Frameworks</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reportingData?.dashboard?.regulatory_frameworks?.map((framework, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{framework.framework}</h4>
                        <Badge className={`text-xs ${
                          framework.compliance_status === 'compliant'
                            ? 'bg-green-500/20 text-green-400'
                            : 'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {framework.compliance_status}
                        </Badge>
                      </div>
                      <div className="text-xs text-slate-400 mb-2">
                        {framework.jurisdiction}
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="text-slate-300">
                          Reports: {framework.reports_completed}/{framework.reports_required}
                        </div>
                        <div className="text-slate-300">
                          Frequency: {framework.reporting_frequency}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComplianceGovernanceSuite;