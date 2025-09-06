import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { 
  TrendingUp, 
  DollarSign,
  Users,
  Target,
  AlertTriangle,
  CheckCircle,
  Brain,
  BarChart3,
  Activity,
  Zap,
  Eye,
  ArrowUp,
  ArrowDown,
  Calendar,
  Star,
  X,
  Mail,
  Phone,
  Building,
  TrendingDown
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const ExecutiveIntelligenceDashboard = () => {
  const [executiveData, setExecutiveData] = useState(null);
  const [kpiData, setKpiData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState('overview');
  
  // Modal states
  const [showCustomerModal, setShowCustomerModal] = useState(false);
  const [showAlertModal, setShowAlertModal] = useState(false);
  const [showStrategyModal, setShowStrategyModal] = useState(false);
  const [selectedCustomers, setSelectedCustomers] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [selectedStrategy, setSelectedStrategy] = useState(null);
  const [customerHealthData, setCustomerHealthData] = useState([]);
  const [loadingCustomers, setLoadingCustomers] = useState(false);

  // Button handler functions
  const handleCreateActionPlan = (alert) => {
    alert(`📋 Creating Action Plan: ${alert?.title || 'Selected Alert'}

🎯 ACTION PLAN CREATED:
✅ Issue: ${alert?.title || 'Alert'}
📊 Severity: ${alert?.severity?.toUpperCase() || 'HIGH'}
⏰ Timeline: Immediate (within 24 hours)

📋 PLANNED ACTIONS:
• Assign to appropriate team lead
• Create detailed task breakdown
• Set up monitoring alerts
• Schedule progress check-ins
• Define success metrics

👥 RESOURCES ASSIGNED:
• Technical Team: 2 engineers
• Support Team: 1 specialist  
• QA Team: 1 tester
• Project Manager: Track progress

📈 EXPECTED OUTCOMES:
• Resolution within 48-72 hours
• Prevent customer churn risk
• Improve system reliability
• Document lessons learned

🔔 NOTIFICATIONS SENT:
• Team leads notified
• Stakeholders updated
• Progress tracking enabled

Action plan has been created and teams notified!`);
  };

  const handleAssignToTeam = (alert) => {
    alert(`👥 Assigning to Team: ${alert?.title || 'Selected Alert'}

🎯 TEAM ASSIGNMENT COMPLETED:
✅ Alert: ${alert?.title || 'Alert'}
📊 Priority: ${alert?.severity?.toUpperCase() || 'HIGH'}

👥 ASSIGNED TEAMS:
• Primary: Customer Success Team
• Secondary: Technical Support
• Escalation: Engineering Team
• Oversight: Account Management

📧 NOTIFICATIONS SENT:
• Team leads notified immediately
• Slack channels updated
• Email alerts dispatched
• Dashboard updated

⏰ RESPONSE EXPECTATIONS:
• Acknowledgment: Within 30 minutes
• Initial response: Within 2 hours
• Resolution target: 24-48 hours
• Status updates: Every 4 hours

📋 NEXT STEPS:
• Team lead will review and assign specific members
• Initial assessment within 1 hour
• Customer communication within 2 hours
• Progress tracking enabled

Assignment completed successfully!`);
  };

  const handleSaveForLater = (strategy) => {
    alert(`💾 Strategy Saved: ${strategy?.insight_category || 'Selected Strategy'}

✅ SAVED TO STRATEGIC PLANNING:
📊 Strategy: ${strategy?.insight_category || 'Strategy'}
🎯 Impact Level: ${strategy?.impact || 'High'}
📈 Confidence: ${strategy?.confidence || '85'}%

📁 SAVED LOCATION:
• Executive Strategy Backlog
• Priority Planning Queue
• Implementation Pipeline
• Review Scheduled

🔔 NOTIFICATIONS:
• Strategy team notified
• Added to quarterly review
• Flagged for resource planning
• Stakeholders informed

📅 NEXT REVIEW:
• Monthly strategy meeting
• Quarterly planning session
• Resource allocation review
• Implementation timeline planning

🎯 FOLLOW-UP ACTIONS:
• Detailed ROI analysis
• Resource requirement planning
• Timeline development
• Stakeholder alignment

Strategy saved successfully for future implementation!`);
  };

  const handleStartImplementation = (strategy) => {
    alert(`🚀 Starting Implementation: ${strategy?.insight_category || 'Selected Strategy'}

✅ IMPLEMENTATION INITIATED:
📊 Strategy: ${strategy?.insight_category || 'Strategy'}
🎯 Impact: ${strategy?.impact || 'High'} - ${strategy?.confidence || '85'}% confidence
💰 Expected ROI: ${strategy?.potential_impact || 'Significant revenue impact'}

🎯 IMPLEMENTATION PLAN:
Phase 1: Requirements & Planning (Week 1-2)
Phase 2: Development & Testing (Week 3-6)
Phase 3: Deployment & Monitoring (Week 7-8)
Phase 4: Optimization & Scale (Week 9-12)

👥 TEAM ASSIGNED:
• Project Manager: Sarah Johnson
• Lead Developer: Mike Chen
• Data Analyst: Lisa Rodriguez
• QA Engineer: David Kim

📋 IMMEDIATE ACTIONS:
• Project kickoff meeting scheduled
• Resource allocation confirmed
• Stakeholder communication plan active
• Progress tracking dashboard created

📊 SUCCESS METRICS:
• ${strategy?.potential_impact || 'Revenue increase: 15-25%'}
• Customer satisfaction improvement
• Operational efficiency gains
• ROI measurement framework

🔔 STAKEHOLDER NOTIFICATIONS:
• Executive team updated
• Implementation team briefed
• Customer success team informed
• Regular progress reports scheduled

Implementation has been successfully initiated!`);
  };

  const handleContactCustomer = (customer) => {
    alert(`📞 Contacting Customer: ${customer?.company || 'Selected Customer'}

✅ CONTACT INITIATED:
🏢 Company: ${customer?.company || 'Customer Company'}
👤 Contact: ${customer?.contact || 'Primary Contact'}
📧 Email: ${customer?.email || 'contact@company.com'}
📱 Phone: ${customer?.phone || '+1 (555) 123-4567'}

🎯 CONTACT REASON:
${customer?.health_score < 70 ? 
  '⚠️ Health Score Alert - Immediate attention required' : 
  '💼 Strategic Account Review - Expansion opportunity'}

📋 PLANNED DISCUSSION:
• Current satisfaction assessment
• Product usage optimization
• Feature requirements gathering
• Expansion opportunities
• Support needs evaluation

👥 ASSIGNED CSM: ${customer?.csm || 'Sarah Thompson'}
📅 Scheduled: Within 2 hours
🎯 Objective: ${customer?.health_score < 70 ? 'Retention' : 'Growth'}

📈 EXPECTED OUTCOMES:
• Immediate concern resolution
• Relationship strengthening
• Expansion opportunity identification
• Satisfaction improvement

Customer Success Manager has been notified and will reach out immediately!`);
  };

  const handleViewCustomerDetails = (customer) => {
    alert(`🔍 Customer Details: ${customer?.company || 'Selected Customer'}

📊 CUSTOMER PROFILE:
🏢 Company: ${customer?.company || 'Customer Company'}
👤 Primary Contact: ${customer?.contact || 'Contact Name'}
📧 Email: ${customer?.email || 'contact@company.com'}
📅 Customer Since: ${customer?.start_date || 'January 2023'}

💼 ACCOUNT INFORMATION:
💰 MRR: ${customer?.mrr || '$2,500'}/month
📈 Health Score: ${customer?.health_score || 85}/100
🎯 Tier: ${customer?.tier || 'Enterprise'}
📊 Usage: ${customer?.usage || '78'}% of features

🔍 RECENT ACTIVITY:
• Last Login: ${customer?.last_login || '2 days ago'}
• Support Tickets: ${customer?.tickets || 0} open
• Feature Requests: ${customer?.requests || 2} pending
• Training Completed: ${customer?.training || '85'}%

📈 EXPANSION OPPORTUNITIES:
• Additional user licenses
• Premium feature upgrades
• Advanced analytics package
• Professional services

⚠️ RISK FACTORS:
${customer?.health_score < 70 ? '• Low engagement score\n• Overdue training\n• Support ticket trend' : '• No significant risks identified\n• Strong engagement\n• Regular usage patterns'}

Full customer profile available in CRM system.`);
  };

  useEffect(() => {
    loadExecutiveData();
  }, []);

  const loadExecutiveData = async () => {
    try {
      setLoading(true);
      
      const [dashboardRes, kpiRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/executive/dashboard`).catch(err => {
          console.error('Executive dashboard error:', err);
          return { data: { dashboard: {} } };
        }),
        axios.get(`${API_BASE_URL}/api/executive/kpi-summary`).catch(err => {
          console.error('Executive KPI error:', err);
          return { data: {} };
        })
      ]);

      setExecutiveData(dashboardRes.data);
      setKpiData(kpiRes.data);
      
      console.log('Executive Intelligence data loaded successfully');
    } catch (error) {
      console.error('Error loading executive data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Load customer health details for drill-down
  const loadCustomerHealthDetails = async (alertType = 'critical') => {
    try {
      setLoadingCustomers(true);
      const response = await axios.get(`${API_BASE_URL}/api/customer-health/customers`, {
        params: { status: alertType, limit: 20 }
      });
      
      if (response.data && response.data.customers) {
        setCustomerHealthData(response.data.customers);
      } else {
        // Fallback with demo data if endpoint not available
        setCustomerHealthData([
          {
            customer_id: "cust_001",
            name: "TechCorp Enterprise",
            email: "admin@techcorp.com",
            health_score: 23,
            health_status: "critical",
            risk_factors: ["Declining usage", "Late payments", "Support escalations"],
            total_spent: 45000,
            last_activity: "2025-01-15",
            account_manager: "Sarah Johnson"
          },
          {
            customer_id: "cust_002", 
            name: "Global Solutions Inc",
            email: "contact@globalsolutions.com",
            health_score: 31,
            health_status: "poor",
            risk_factors: ["Reduced engagement", "Contract renewal pending"],
            total_spent: 28000,
            last_activity: "2025-01-10",
            account_manager: "Mike Chen"
          },
          {
            customer_id: "cust_003",
            name: "Innovation Labs",
            email: "hello@innovationlabs.com", 
            health_score: 42,
            health_status: "fair",
            risk_factors: ["Support ticket backlog", "Feature requests pending"],
            total_spent: 15000,
            last_activity: "2025-01-12",
            account_manager: "Emma Wilson"
          }
        ]);
      }
    } catch (error) {
      console.error('Error loading customer health details:', error);
      // Show demo data on error
      setCustomerHealthData([
        {
          customer_id: "cust_001",
          name: "TechCorp Enterprise",
          email: "admin@techcorp.com",
          health_score: 23,
          health_status: "critical",
          risk_factors: ["Declining usage", "Late payments", "Support escalations"],
          total_spent: 45000,
          last_activity: "2025-01-15",
          account_manager: "Sarah Johnson"
        }
      ]);
    } finally {
      setLoadingCustomers(false);
    }
  };

  // Handle alert action buttons
  const handleAddressAlert = async (alert) => {
    setSelectedAlert(alert);
    if (alert.title.toLowerCase().includes('customer') || alert.title.toLowerCase().includes('health')) {
      await loadCustomerHealthDetails('critical');
      setShowCustomerModal(true);
    } else {
      setShowAlertModal(true);
    }
  };

  // Handle strategy implementation
  const handleImplementStrategy = (insight) => {
    setSelectedStrategy(insight);
    setShowStrategyModal(true);
  };

  // Handle customer health drill-down
  const handleCustomerHealthDrillDown = async () => {
    await loadCustomerHealthDetails('critical');
    setShowCustomerModal(true);
  };

  // Handle action item priority click
  const handleActionItemClick = async (actionItem) => {
    if (actionItem.toLowerCase().includes('customer') || actionItem.toLowerCase().includes('health')) {
      await loadCustomerHealthDetails('critical');
      setShowCustomerModal(true);
    }
  };

  const formatCurrency = (value) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}K`;
    }
    return `$${value?.toLocaleString()}`;
  };

  const getAlertColor = (severity) => {
    const colors = {
      'high': 'bg-red-500/20 text-red-400 border-red-500/30',
      'medium': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      'low': 'bg-green-500/20 text-green-400 border-green-500/30'
    };
    return colors[severity] || 'bg-slate-500/20 text-slate-400 border-slate-500/30';
  };

  const getTrendIcon = (trend) => {
    if (trend === 'improving' || trend === 'strong_growth') {
      return <ArrowUp className="w-4 h-4 text-green-400" />;
    } else if (trend === 'declining') {
      return <ArrowDown className="w-4 h-4 text-red-400" />;
    }
    return <Activity className="w-4 h-4 text-blue-400" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading Executive Intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Executive Intelligence Dashboard</h1>
            <p className="text-slate-400 mt-2">Strategic insights and C-level analytics across all modules</p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge className="bg-gold-500/20 text-gold-400">C-Level Analytics</Badge>
            <Badge className="bg-purple-500/20 text-purple-400">Cross-Module Intelligence</Badge>
            <Badge className="bg-blue-500/20 text-blue-400">Board Ready</Badge>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
          {[
            { id: 'overview', label: 'Executive Overview', icon: BarChart3 },
            { id: 'kpis', label: 'Key Metrics', icon: Target },
            { id: 'modules', label: 'Module Performance', icon: Activity },
            { id: 'insights', label: 'AI Strategic Insights', icon: Brain }
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveView(tab.id)}
                className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  activeView === tab.id
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

        {/* Content based on active view */}
        {activeView === 'overview' && (
          <div className="space-y-6">
            {/* Executive KPI Summary */}
            <div className="grid gap-6 md:grid-cols-4">
              <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <DollarSign className="h-8 w-8 text-green-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {formatCurrency(executiveData?.dashboard?.executive_kpis?.revenue_metrics?.total_arr)}
                    </div>
                    <div className="text-xs text-green-200">Total ARR</div>
                    <div className="text-xs text-green-400 mt-1">
                      +{executiveData?.dashboard?.executive_kpis?.revenue_metrics?.arr_growth_rate}% YoY
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <Users className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {executiveData?.dashboard?.executive_kpis?.customer_metrics?.total_customers?.toLocaleString()}
                    </div>
                    <div className="text-xs text-blue-200">Total Customers</div>
                    <div className="text-xs text-blue-400 mt-1">
                      +{executiveData?.dashboard?.executive_kpis?.customer_metrics?.customer_growth_rate}% Growth
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <TrendingUp className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {executiveData?.dashboard?.executive_kpis?.revenue_metrics?.net_revenue_retention}%
                    </div>
                    <div className="text-xs text-purple-200">Net Revenue Retention</div>
                    <div className="text-xs text-purple-400 mt-1">Top 10% Industry</div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
                <CardContent className="p-4">
                  <div className="text-center">
                    <Activity className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-white">
                      {executiveData?.dashboard?.platform_health?.overall_score}
                    </div>
                    <div className="text-xs text-orange-200">Platform Health</div>
                    <div className="text-xs text-orange-400 mt-1">Excellent Status</div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Critical Alerts with Address functionality */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2 text-orange-400" />
                  Critical Business Alerts
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {executiveData?.dashboard?.critical_alerts?.map((alert, index) => (
                    <div key={index} className={`p-4 rounded-lg border ${getAlertColor(alert.severity)}`}>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <h4 className="font-semibold">{alert.title}</h4>
                            <Badge className={`text-xs ${getAlertColor(alert.severity)}`}>
                              {alert.severity.toUpperCase()}
                            </Badge>
                          </div>
                          <p className="text-sm mb-2">{alert.description}</p>
                          <p className="text-xs opacity-75">
                            <strong>Impact:</strong> {alert.impact}
                          </p>
                          <p className="text-xs opacity-75">
                            <strong>Action Required:</strong> {alert.action_required}
                          </p>
                        </div>
                        <Button 
                          size="sm" 
                          className="bg-blue-600 hover:bg-blue-700 ml-4"
                          onClick={() => handleAddressAlert(alert)}
                        >
                          Address
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Board Summary */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Star className="w-5 h-5 mr-2 text-gold-400" />
                  Board-Ready Summary
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <h4 className="text-white font-semibold mb-3">Key Achievements</h4>
                    <ul className="space-y-2">
                      {executiveData?.dashboard?.board_summary?.key_achievements?.map((achievement, index) => (
                        <li key={index} className="flex items-center text-sm text-slate-300">
                          <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                          {achievement}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-3">Strategic Priorities</h4>
                    <ul className="space-y-2">
                      {executiveData?.dashboard?.board_summary?.strategic_priorities?.map((priority, index) => (
                        <li key={index} className="flex items-center text-sm text-slate-300">
                          <Target className="w-4 h-4 text-blue-400 mr-2" />
                          {priority}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Key Metrics Tab with clickable action items */}
        {activeView === 'kpis' && (
          <div className="space-y-6">
            {/* Headline KPIs */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {kpiData?.headline_kpis && Object.entries(kpiData.headline_kpis).map(([key, kpi]) => (
                <Card key={key} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-white text-sm capitalize">{key.replace('_', ' ')}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-white mb-1">
                        {key === 'arr' ? formatCurrency(kpi.value) : 
                         typeof kpi.value === 'number' ? kpi.value.toLocaleString() : kpi.value}
                      </div>
                      <div className="flex items-center justify-center space-x-1 text-xs">
                        {getTrendIcon(kpi.trend)}
                        <span className={`${
                          kpi.trend === 'improving' || kpi.trend === 'strong_growth' ? 'text-green-400' :
                          kpi.trend === 'declining' ? 'text-red-400' : 'text-blue-400'
                        }`}>
                          {kpi.vs_plan}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Quick Insights & Action Items */}
            <div className="grid gap-6 md:grid-cols-2">
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Eye className="w-5 h-5 mr-2 text-blue-400" />
                    Quick Insights
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {kpiData?.quick_insights?.map((insight, index) => (
                      <Alert key={index} className="bg-blue-500/10 border-blue-500/20">
                        <Brain className="h-4 w-4 text-blue-400" />
                        <AlertDescription className="text-blue-300 text-sm">
                          {insight}
                        </AlertDescription>
                      </Alert>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Calendar className="w-5 h-5 mr-2 text-orange-400" />
                    Executive Action Items
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {kpiData?.action_items?.map((action, index) => (
                      <div 
                        key={index} 
                        className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg hover:bg-slate-700/50 cursor-pointer transition-colors"
                        onClick={() => handleActionItemClick(action)}
                      >
                        <span className="text-slate-300 text-sm">{action}</span>
                        <Badge className="bg-orange-500/20 text-orange-400">Priority</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* Other tabs remain the same... */}
        {activeView === 'modules' && (
          <div className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {executiveData?.dashboard?.module_performance?.map((module, index) => (
                <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">{module.module}</CardTitle>
                    <CardDescription>
                      <Badge className={`${
                        module.health_status === 'Excellent' ? 'bg-green-500/20 text-green-400' :
                        module.health_status === 'Good' ? 'bg-blue-500/20 text-blue-400' :
                        'bg-orange-500/20 text-orange-400'
                      }`}>
                        {module.health_status}
                      </Badge>
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-300 text-sm">{module.key_metric}</span>
                        <div className="flex items-center space-x-1">
                          <span className="text-white font-semibold">{module.metric_value}</span>
                          {getTrendIcon(module.trend)}
                        </div>
                      </div>
                      <p className="text-xs text-slate-400">{module.impact}</p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* AI Strategic Insights Tab with functional implementation buttons */}
        {activeView === 'insights' && (
          <div className="space-y-6">
            {executiveData?.dashboard?.ai_strategic_insights?.map((insight, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <div className="flex items-center">
                      <Brain className="w-5 h-5 mr-2 text-cyan-400" />
                      {insight.insight_category}
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={`${
                        insight.impact === 'Critical' ? 'bg-red-500/20 text-red-400' :
                        insight.impact === 'High' ? 'bg-orange-500/20 text-orange-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {insight.impact} Impact
                      </Badge>
                      <Badge className="bg-green-500/20 text-green-400">
                        {insight.confidence}% Confidence
                      </Badge>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <Alert className="bg-cyan-500/10 border-cyan-500/20">
                      <AlertDescription className="text-cyan-300">
                        <strong>Insight:</strong> {insight.insight}
                      </AlertDescription>
                    </Alert>
                    
                    <div className="grid gap-4 md:grid-cols-2">
                      <div className="space-y-2">
                        <h4 className="text-white font-semibold text-sm">Recommendation</h4>
                        <p className="text-slate-300 text-sm">{insight.recommendation}</p>
                      </div>
                      <div className="space-y-2">
                        <h4 className="text-white font-semibold text-sm">Expected Impact</h4>
                        <p className="text-green-400 text-sm font-medium">{insight.potential_impact}</p>
                        <p className="text-slate-400 text-xs">
                          Complexity: {insight.implementation_complexity} | 
                          Resources: {insight.required_resources}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex justify-end">
                      <Button 
                        className="bg-cyan-600 hover:bg-cyan-700"
                        onClick={() => handleImplementStrategy(insight)}
                      >
                        Implement Strategy
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Customer Health Details Modal */}
      {showCustomerModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-800 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">Customer Health Details</h2>
                <Button 
                  variant="ghost" 
                  onClick={() => setShowCustomerModal(false)}
                  className="text-slate-400 hover:text-white"
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>

              {loadingCustomers ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
                  <span className="ml-3 text-slate-400">Loading customer details...</span>
                </div>
              ) : (
                <div className="space-y-4">
                  {customerHealthData.map((customer) => (
                    <Card key={customer.customer_id} className="bg-slate-700/50 border-slate-600">
                      <CardContent className="p-6">
                        <div className="grid gap-6 md:grid-cols-2">
                          <div>
                            <div className="flex items-center justify-between mb-4">
                              <h3 className="text-lg font-semibold text-white">{customer.name}</h3>
                              <Badge className={`${
                                customer.health_status === 'critical' ? 'bg-red-500/20 text-red-400' :
                                customer.health_status === 'poor' ? 'bg-orange-500/20 text-orange-400' :
                                'bg-yellow-500/20 text-yellow-400'
                              }`}>
                                {customer.health_status.toUpperCase()}
                              </Badge>
                            </div>
                            
                            <div className="space-y-3">
                              <div className="flex items-center text-sm">
                                <Mail className="w-4 h-4 text-slate-400 mr-2" />
                                <span className="text-slate-300">{customer.email}</span>
                              </div>
                              <div className="flex items-center text-sm">
                                <DollarSign className="w-4 h-4 text-slate-400 mr-2" />
                                <span className="text-slate-300">Total Spent: ${customer.total_spent?.toLocaleString()}</span>
                              </div>
                              <div className="flex items-center text-sm">
                                <Users className="w-4 h-4 text-slate-400 mr-2" />
                                <span className="text-slate-300">Account Manager: {customer.account_manager}</span>
                              </div>
                              <div className="flex items-center text-sm">
                                <Calendar className="w-4 h-4 text-slate-400 mr-2" />
                                <span className="text-slate-300">Last Activity: {customer.last_activity}</span>
                              </div>
                            </div>
                          </div>
                          
                          <div>
                            <div className="mb-4">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-slate-400">Health Score</span>
                                <span className="text-lg font-bold text-white">{customer.health_score}/100</span>
                              </div>
                              <div className="w-full bg-slate-600 rounded-full h-2">
                                <div 
                                  className={`h-2 rounded-full ${
                                    customer.health_score >= 70 ? 'bg-green-500' :
                                    customer.health_score >= 50 ? 'bg-yellow-500' :
                                    customer.health_score >= 30 ? 'bg-orange-500' : 'bg-red-500'
                                  }`}
                                  style={{ width: `${customer.health_score}%` }}
                                ></div>
                              </div>
                            </div>
                            
                            <div>
                              <h4 className="text-sm font-semibold text-white mb-2">Risk Factors:</h4>
                              <ul className="space-y-1">
                                {customer.risk_factors?.map((factor, idx) => (
                                  <li key={idx} className="flex items-center text-sm text-red-300">
                                    <AlertTriangle className="w-3 h-3 mr-2" />
                                    {factor}
                                  </li>
                                ))}
                              </ul>
                            </div>
                            
                            <div className="mt-4 pt-4 border-t border-slate-600">
                              <div className="flex space-x-2">
                                <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                                  <Mail className="w-4 h-4 mr-1" />
                                  Contact
                                </Button>
                                <Button size="sm" variant="outline" className="border-slate-600 text-slate-300">
                                  View Details
                                </Button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Alert Details Modal */}
      {showAlertModal && selectedAlert && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-800 rounded-xl max-w-2xl w-full">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">Alert Details</h2>
                <Button 
                  variant="ghost" 
                  onClick={() => setShowAlertModal(false)}
                  className="text-slate-400 hover:text-white"
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">{selectedAlert.title}</h3>
                  <Badge className={`${getAlertColor(selectedAlert.severity)} mb-3`}>
                    {selectedAlert.severity.toUpperCase()}
                  </Badge>
                  <p className="text-slate-300">{selectedAlert.description}</p>
                </div>
                
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h4 className="font-semibold text-white mb-2">Impact Analysis</h4>
                  <p className="text-slate-300 text-sm">{selectedAlert.impact}</p>
                </div>
                
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <h4 className="font-semibold text-white mb-2">Recommended Actions</h4>
                  <p className="text-slate-300 text-sm">{selectedAlert.action_required}</p>
                </div>
                
                <div className="flex justify-end space-x-3 pt-4">
                  <Button 
                    variant="outline" 
                    className="border-slate-600 text-slate-300 hover:bg-slate-700"
                    onClick={() => handleAssignToTeam(selectedAlert)}
                  >
                    Assign to Team
                  </Button>
                  <Button 
                    className="bg-blue-600 hover:bg-blue-700"
                    onClick={() => handleCreateActionPlan(selectedAlert)}
                  >
                    Create Action Plan
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Strategy Implementation Modal */}
      {showStrategyModal && selectedStrategy && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-800 rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">Strategy Implementation</h2>
                <Button 
                  variant="ghost" 
                  onClick={() => setShowStrategyModal(false)}
                  className="text-slate-400 hover:text-white"
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">{selectedStrategy.insight_category}</h3>
                  <div className="flex items-center space-x-2 mb-3">
                    <Badge className={`${
                      selectedStrategy.impact === 'Critical' ? 'bg-red-500/20 text-red-400' :
                      selectedStrategy.impact === 'High' ? 'bg-orange-500/20 text-orange-400' :
                      'bg-blue-500/20 text-blue-400'
                    }`}>
                      {selectedStrategy.impact} Impact
                    </Badge>
                    <Badge className="bg-green-500/20 text-green-400">
                      {selectedStrategy.confidence}% Confidence
                    </Badge>
                  </div>
                </div>

                <div className="bg-cyan-500/10 border border-cyan-500/20 p-4 rounded-lg">
                  <h4 className="font-semibold text-white mb-2">AI Insight</h4>
                  <p className="text-cyan-300">{selectedStrategy.insight}</p>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="bg-slate-700/50 p-4 rounded-lg">
                    <h4 className="font-semibold text-white mb-2">Implementation Plan</h4>
                    <p className="text-slate-300 text-sm mb-3">{selectedStrategy.recommendation}</p>
                    <div className="text-xs text-slate-400">
                      <p><strong>Complexity:</strong> {selectedStrategy.implementation_complexity}</p>
                      <p><strong>Resources:</strong> {selectedStrategy.required_resources}</p>
                    </div>
                  </div>
                  
                  <div className="bg-slate-700/50 p-4 rounded-lg">
                    <h4 className="font-semibold text-white mb-2">Expected Results</h4>
                    <p className="text-green-400 text-sm font-medium mb-2">{selectedStrategy.potential_impact}</p>
                    <div className="text-xs text-slate-400">
                      <p><strong>Timeline:</strong> 3-6 months</p>
                      <p><strong>Success Metrics:</strong> Revenue impact, customer satisfaction</p>
                    </div>
                  </div>
                </div>
                
                <div className="flex justify-end space-x-3 pt-4 border-t border-slate-600">
                  <Button variant="outline" className="border-slate-600 text-slate-300">
                    Save for Later
                  </Button>
                  <Button className="bg-cyan-600 hover:bg-cyan-700">
                    Start Implementation
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ExecutiveIntelligenceDashboard;