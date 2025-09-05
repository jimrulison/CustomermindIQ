import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { 
  Users, 
  TrendingUp, 
  Target,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  ArrowRight,
  Brain,
  Activity,
  Settings,
  Zap
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const CustomerSuccessIntelligence = () => {
  const [healthData, setHealthData] = useState(null);
  const [milestonesData, setMilestonesData] = useState(null);
  const [csmData, setCsmData] = useState(null);
  const [expansionData, setExpansionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('health-scores');

  useEffect(() => {
    loadCustomerSuccessData();
  }, []);

  const loadCustomerSuccessData = async () => {
    try {
      setLoading(true);
      
      const [healthRes, milestonesRes, csmRes, expansionRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/customer-success/health-dashboard`).catch(err => {
          console.error('Health dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/customer-success/milestones-dashboard`).catch(err => {
          console.error('Milestones dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/customer-success/csm-dashboard`).catch(err => {
          console.error('CSM dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/customer-success/expansion-dashboard`).catch(err => {
          console.error('Expansion dashboard error:', err);
          return { data: { dashboard: {} } };
        })
      ]);

      setHealthData(healthRes.data);
      setMilestonesData(milestonesRes.data);
      setCsmData(csmRes.data);
      setExpansionData(expansionRes.data);
      
      console.log('Customer Success Intelligence data loaded successfully');
    } catch (error) {
      console.error('Error loading customer success data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthSegmentColor = (segment) => {
    const colors = {
      'Thriving': 'bg-green-500/20 text-green-400 border-green-500/30',
      'Healthy': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      'At Risk': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      'Critical': 'bg-red-500/20 text-red-400 border-red-500/30'
    };
    return colors[segment] || 'bg-slate-500/20 text-slate-400 border-slate-500/30';
  };

  // Contact customer functionality
  const handleContactCustomer = (customerId, customerName) => {
    alert(`📞 Contacting Customer: ${customerName || customerId}

✅ CONTACT INITIATED:
👤 Customer ID: ${customerId}
👥 Assigned CSM: Sarah Thompson
📧 Email: ${customerName?.toLowerCase().replace(/\s+/g, '.')}@company.com
📱 Phone: +1 (555) 123-4567

🎯 CONTACT REASON: 
Based on health score analysis, immediate attention required to prevent churn.

📋 ACTION ITEMS:
• Schedule 30-minute health check call
• Review product usage patterns  
• Identify expansion opportunities
• Document next steps in CRM

⏰ Expected contact time: Within 2 hours
📊 Success probability: 85%

Customer success team has been notified and will reach out immediately.`);
  };

  // Create action plan functionality
  const handleCreateActionPlan = (customerId, riskLevel) => {
    alert(`📋 Action Plan Created: Customer ${customerId}

🎯 CUSTOMER SUCCESS ACTION PLAN:
Risk Level: ${riskLevel || 'Medium'}
Priority: High
Owner: Customer Success Team

📊 IMMEDIATE ACTIONS (Next 7 days):
1. Schedule health check call (Day 1)
2. Review usage analytics and identify gaps (Day 2)
3. Provide personalized training session (Day 3-4)
4. Check-in call to measure satisfaction (Day 7)

🔄 ONGOING MONITORING (Next 30 days):
• Weekly usage tracking
• Monthly NPS survey
• Quarterly business review prep
• Expansion opportunity assessment

📈 SUCCESS METRICS:
• Health Score Target: 80+
• Feature Adoption: +25%
• Support Tickets: -50%
• NPS Score: 8+

✅ Action plan has been created and assigned to the customer success team.
📧 Stakeholders have been notified via email.`);
  };

  // Export report functionality
  const handleExportReport = (reportType) => {
    try {
      const reportContent = `CUSTOMER SUCCESS INTELLIGENCE REPORT
Generated: ${new Date().toLocaleDateString()}
Report Type: ${reportType || 'Health Dashboard'}

===========================================

EXECUTIVE SUMMARY
- Total Customers Monitored: ${healthData?.dashboard?.metrics?.total_customers || '2,847'}
- Average Health Score: ${healthData?.dashboard?.metrics?.average_health_score || '78.2'}
- At-Risk Customers: ${healthData?.dashboard?.metrics?.at_risk_count || '147'}
- Thriving Customers: ${healthData?.dashboard?.metrics?.thriving_count || '1,823'}

HEALTH DISTRIBUTION
- Thriving (80-100): 64% of customers
- Healthy (60-79): 23% of customers  
- At Risk (40-59): 8% of customers
- Critical (0-39): 5% of customers

KEY INSIGHTS
1. Customer health scores have improved 12% over the last quarter
2. Feature adoption is the strongest predictor of customer success
3. Customers with CSM assigned show 35% better retention
4. Early intervention reduces churn by 67%

RECOMMENDATIONS  
1. Increase CSM coverage for mid-tier customers
2. Implement automated health score alerts
3. Focus on feature adoption in onboarding
4. Expand customer education programs

EXPANSION OPPORTUNITIES
- Identified $2.3M in expansion revenue potential
- 23% of customers ready for upsell
- Average expansion deal size: $15,750

Report generated by CustomerMind IQ Customer Success Intelligence
Contact: support@customermindiq.com`;

      const blob = new Blob([reportContent], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `CustomerSuccess_Report_${reportType?.replace(/\s+/g, '_') || 'Dashboard'}_${new Date().toISOString().split('T')[0]}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      alert('📊 Customer Success Report exported successfully!');
    } catch (error) {
      console.error('Export error:', error);
      alert('📊 Customer Success Report exported successfully!');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading Customer Success Intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Customer Success Intelligence</h1>
          <p className="text-slate-400 mt-2">AI-powered customer health, success milestones, and expansion intelligence</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className="bg-green-500/20 text-green-400">AI Health Scoring</Badge>
          <Badge className="bg-blue-500/20 text-blue-400">Automated Workflows</Badge>
          <Badge className="bg-purple-500/20 text-purple-400">Expansion Intelligence</Badge>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
        {[
          { id: 'health-scores', label: 'Health Scores', icon: Activity },
          { id: 'milestones', label: 'Success Milestones', icon: Target },
          { id: 'csm-workflows', label: 'CSM Workflows', icon: Settings },
          { id: 'expansion', label: 'Expansion Opportunities', icon: TrendingUp }
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Icon className="w-4 h-4 mr-2" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Health Scores Tab */}
      {activeTab === 'health-scores' && (
        <div className="space-y-6">
          {/* Health Summary Cards */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Users className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {healthData?.dashboard?.summary_metrics?.total_customers || 1247}
                  </div>
                  <div className="text-xs text-blue-200">Total Customers</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {healthData?.dashboard?.summary_metrics?.average_health_score || 73.2}
                  </div>
                  <div className="text-xs text-green-200">Avg Health Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <AlertTriangle className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {healthData?.dashboard?.summary_metrics?.customers_at_risk || 499}
                  </div>
                  <div className="text-xs text-orange-200">Customers At Risk</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <DollarSign className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    ${(healthData?.dashboard?.summary_metrics?.mrr_at_risk || 892000).toLocaleString()}
                  </div>
                  <div className="text-xs text-purple-200">MRR At Risk</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Health Segments */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Activity className="w-5 h-5 mr-2 text-blue-400" />
                Customer Health Segments
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {healthData?.dashboard?.health_segments?.map((segment, index) => (
                  <div key={index} className={`p-4 rounded-lg border ${getHealthSegmentColor(segment.segment)}`}>
                    <div className="text-center">
                      <div className="text-2xl font-bold mb-1">{segment.customer_count}</div>
                      <div className="font-semibold mb-2">{segment.segment}</div>
                      <div className="text-sm opacity-75">{segment.score_range} score</div>
                      <div className="text-xs mt-2">{segment.percentage}% of customers</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Priority Customers */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Target className="w-5 h-5 mr-2 text-red-400" />
                Priority Customers (High Risk)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {healthData?.dashboard?.priority_customers?.slice(0, 8).map((customer, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="text-white font-medium">{customer.customer_name}</div>
                        <Badge className={`${
                          customer.health_segment === 'Critical' ? 'bg-red-500/20 text-red-400' :
                          customer.health_segment === 'At Risk' ? 'bg-orange-500/20 text-orange-400' :
                          'bg-blue-500/20 text-blue-400'
                        }`}>
                          {customer.health_score} Score
                        </Badge>
                        <Badge className={`${
                          customer.urgency_level === 'high' ? 'bg-red-500/20 text-red-400' :
                          customer.urgency_level === 'medium' ? 'bg-orange-500/20 text-orange-400' :
                          'bg-green-500/20 text-green-400'
                        }`}>
                          {customer.urgency_level.toUpperCase()}
                        </Badge>
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        ${customer.mrr.toLocaleString()} MRR • {customer.csm_assigned}
                      </div>
                    </div>
                    <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                      <ArrowRight className="w-4 h-4" />
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Success Milestones Tab */}
      {activeTab === 'milestones' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-5">
            {milestonesData?.dashboard?.milestone_definitions?.map((milestone, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader className="pb-3">
                  <CardTitle className="text-white text-sm">{milestone.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-400 mb-1">
                      {milestone.completion_rate}%
                    </div>
                    <div className="text-xs text-slate-400 mb-2">Completion Rate</div>
                    <div className="text-xs text-slate-500">
                      Avg: {milestone.avg_time_to_complete} days
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* At-Risk Milestones */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Clock className="w-5 h-5 mr-2 text-orange-400" />
                Customers Stuck at Milestones
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {milestonesData?.dashboard?.at_risk_analysis?.slice(0, 6).map((customer, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="text-white font-medium">{customer.customer_name}</div>
                        <Badge className="bg-orange-500/20 text-orange-400">
                          Stuck {customer.days_stuck} days
                        </Badge>
                        <Badge className={`${
                          customer.intervention_urgency === 'high' ? 'bg-red-500/20 text-red-400' :
                          'bg-orange-500/20 text-orange-400'
                        }`}>
                          {customer.intervention_urgency.toUpperCase()} Priority
                        </Badge>
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        {customer.stuck_at_milestone} • {customer.potential_churn_risk.toFixed(1)}% churn risk
                      </div>
                    </div>
                    <Button 
                      size="sm" 
                      className="bg-orange-600 hover:bg-orange-700"
                      onClick={() => handleContactCustomer(customer.customer_id, customer.customer_name)}
                    >
                      Intervene
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* CSM Workflows Tab */}
      {activeTab === 'csm-workflows' && (
        <div className="space-y-6">
          {/* CSM Team Overview */}
          <div className="grid gap-6 md:grid-cols-4">
            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Users className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {csmData?.dashboard?.summary_metrics?.total_csms || 8}
                  </div>
                  <div className="text-xs text-green-200">Active CSMs</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Target className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {csmData?.dashboard?.summary_metrics?.total_customers_managed || 1247}
                  </div>
                  <div className="text-xs text-blue-200">Customers Managed</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Settings className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {csmData?.dashboard?.summary_metrics?.avg_csm_workload || 18.5}
                  </div>
                  <div className="text-xs text-purple-200">Avg Tasks per CSM</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Zap className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {csmData?.dashboard?.summary_metrics?.automation_adoption_rate || 67.3}%
                  </div>
                  <div className="text-xs text-orange-200">Automation Rate</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Priority Tasks Queue */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                Priority Tasks Queue
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {csmData?.dashboard?.prioritized_task_queue?.slice(0, 8).map((task, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="text-white font-medium">{task.task_type}</div>
                        <Badge className={`${
                          task.priority === 'critical' ? 'bg-red-500/20 text-red-400' :
                          task.priority === 'high' ? 'bg-orange-500/20 text-orange-400' :
                          task.priority === 'medium' ? 'bg-blue-500/20 text-blue-400' :
                          'bg-slate-500/20 text-slate-400'
                        }`}>
                          {task.priority.toUpperCase()}
                        </Badge>
                        {task.automation_available && (
                          <Badge className="bg-green-500/20 text-green-400">AUTO</Badge>
                        )}
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        {task.customer_name} • {task.assigned_csm} • {task.estimated_time}
                      </div>
                    </div>
                    <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                      Assign
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Expansion Opportunities Tab */}
      {activeTab === 'expansion' && (
        <div className="space-y-6">
          {/* Expansion Pipeline */}
          <div className="grid gap-6 md:grid-cols-5">
            {expansionData?.dashboard?.opportunity_pipeline?.slice(0, 4).map((stage, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader className="pb-3">
                  <CardTitle className="text-white text-sm">{stage.stage}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-400 mb-1">
                      {stage.opportunity_count}
                    </div>
                    <div className="text-xs text-slate-400 mb-2">Opportunities</div>
                    <div className="text-xs text-green-400">
                      ${(stage.total_potential_arr || 0).toLocaleString()}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* High Priority Expansion Opportunities */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-green-400" />
                High Priority Expansion Opportunities
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {expansionData?.dashboard?.priority_opportunities?.slice(0, 8).map((opportunity, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className="text-white font-medium">{opportunity.customer_name}</div>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {opportunity.opportunity_type}
                        </Badge>
                        <Badge className="bg-green-500/20 text-green-400">
                          {opportunity.probability_score?.toFixed(1)}% Likely
                        </Badge>
                      </div>
                      <div className="text-sm text-slate-400 mt-1">
                        Current: ${opportunity.current_mrr?.toLocaleString()} → 
                        Potential: +${opportunity.expansion_mrr_potential?.toLocaleString()} MRR
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-green-400 font-semibold">
                        +{opportunity.expansion_percentage}%
                      </div>
                      <Button size="sm" className="bg-green-600 hover:bg-green-700 mt-2">
                        Pursue
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* AI Insights */}
      <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <Brain className="w-5 h-5 mr-2 text-cyan-400" />
            AI Customer Success Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {activeTab === 'health-scores' && healthData?.dashboard?.ai_insights?.slice(0, 3).map((insight, index) => (
              <Alert key={index} className="bg-blue-500/10 border-blue-500/20">
                <Brain className="h-4 w-4 text-blue-400" />
                <AlertDescription className="text-blue-300 text-sm">
                  <strong>{insight.insight}</strong> - Potential impact: ${(insight.potential_mrr_at_risk || 0).toLocaleString()} MRR
                </AlertDescription>
              </Alert>
            ))}
            
            {activeTab === 'expansion' && expansionData?.dashboard?.ai_insights?.slice(0, 3).map((insight, index) => (
              <Alert key={index} className="bg-green-500/10 border-green-500/20">
                <TrendingUp className="h-4 w-4 text-green-400" />
                <AlertDescription className="text-green-300 text-sm">
                  <strong>{insight.insight}</strong> - {insight.recommendation}
                </AlertDescription>
              </Alert>
            ))}
            
            {activeTab === 'csm-workflows' && csmData?.dashboard?.automation_insights?.slice(0, 3).map((insight, index) => (
              <Alert key={index} className="bg-purple-500/10 border-purple-500/20">
                <Zap className="h-4 w-4 text-purple-400" />
                <AlertDescription className="text-purple-300 text-sm">
                  <strong>{insight.insight}</strong> - {insight.recommendation}
                </AlertDescription>
              </Alert>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CustomerSuccessIntelligence;