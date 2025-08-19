import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Brain,
  Users, 
  TrendingUp, 
  Mail, 
  Target, 
  BarChart3, 
  Zap,
  DollarSign,
  ShoppingCart,
  Calendar,
  Send,
  Eye,
  MousePointer,
  CheckCircle,
  Megaphone,
  TestTube,
  Palette,
  TrendingDown,
  Gift,
  Settings,
  Activity,
  PieChart,
  ArrowRightLeft,
  MessageSquare,
  AlertTriangle,
  Star,
  Award,
  Sparkles,
  Heart,
  Route,
  Sword
} from 'lucide-react';

const CustomerAnalyticsDashboard = ({ 
  dashboardData, 
  customerData, 
  marketingData, 
  revenueAnalyticsData,
  advancedFeaturesData,
  onNavigate 
}) => {
  const [selectedModule, setSelectedModule] = useState(null);

  // Customer Analytics focused modules
  const customerModules = [
    {
      id: 'customers',
      title: 'Customer Intelligence AI',
      description: 'AI-powered customer behavior analysis and predictive insights',
      icon: Brain,
      color: 'from-blue-600/20 to-blue-800/20',
      borderColor: 'border-blue-500/30',
      iconColor: 'text-blue-400',
      metrics: {
        customers: customerData?.dashboard_data?.total_customers || 0,
        engagement: '78.4%',
        predictions: '94.2%'
      },
      features: ['Behavioral Analysis', 'Purchase Predictions', 'Engagement Scoring', 'Lifecycle Tracking']
    },
    {
      id: 'marketing',
      title: 'Marketing Automation Pro',
      description: 'AI-powered multi-channel marketing orchestration and campaign management',
      icon: Megaphone,
      color: 'from-purple-600/20 to-purple-800/20',
      borderColor: 'border-purple-500/30',
      iconColor: 'text-purple-400',
      metrics: {
        campaigns: marketingData?.campaigns_count || 0,
        automation: '87.5%',
        roi: '340%'
      },
      features: ['Multi-Channel Campaigns', 'A/B Testing', 'Dynamic Content', 'Lead Scoring']
    },
    {
      id: 'revenue',
      title: 'Revenue Analytics Suite',
      description: 'Comprehensive revenue intelligence, forecasting, and optimization',
      icon: DollarSign,
      color: 'from-green-600/20 to-green-800/20',
      borderColor: 'border-green-500/30',
      iconColor: 'text-green-400',
      metrics: {
        revenue: '$891K',
        growth: '+24.1%',
        forecast: '88.7%'
      },
      features: ['Revenue Forecasting', 'Price Optimization', 'Profit Analysis', 'Subscription Analytics']
    },
    {
      id: 'advanced',
      title: 'Advanced Customer Features',
      description: 'AI-driven behavioral clustering, churn prevention, and cross-sell intelligence',
      icon: Zap,
      color: 'from-orange-600/20 to-orange-800/20',
      borderColor: 'border-orange-500/30',
      iconColor: 'text-orange-400',
      metrics: {
        clusters: '5 Groups',
        churn: '78.4%',
        upsell: '$74K'
      },
      features: ['Behavioral Clustering', 'Churn Prevention', 'Cross-Sell Intelligence', 'Sentiment Analysis']
    },
    {
      id: 'customer-success',
      title: 'Customer Success Intelligence',
      description: 'Customer health monitoring, success metrics, and retention strategies',
      icon: Target,
      color: 'from-cyan-600/20 to-cyan-800/20',
      borderColor: 'border-cyan-500/30',
      iconColor: 'text-cyan-400',
      metrics: {
        health: '85.2/100',
        retention: '94.1%',
        satisfaction: '4.8/5'
      },
      features: ['Health Scoring', 'Success Metrics', 'Retention Strategies', 'Risk Assessment']
    },
    {
      id: 'executive',
      title: 'Executive Intelligence Dashboard',
      description: 'High-level customer and business performance insights for executives',
      icon: BarChart3,
      color: 'from-indigo-600/20 to-indigo-800/20',
      borderColor: 'border-indigo-500/30',
      iconColor: 'text-indigo-400',
      metrics: {
        kpis: '12 Metrics',
        performance: '92.3%',
        insights: '45 Active'
      },
      features: ['Executive KPIs', 'Performance Summaries', 'Strategic Insights', 'Board Reports']
    },
    {
      id: 'real-time-health',
      title: 'Real-Time Customer Health',
      description: 'Live customer health monitoring with AI-powered alerts and intervention automation',
      icon: Heart,
      color: 'from-red-600/20 to-red-800/20',
      borderColor: 'border-red-500/30',
      iconColor: 'text-red-400',
      metrics: {
        monitored: '24/7',
        alerts: '3 Active',
        interventions: '94.2%'
      },
      features: ['Live Health Scoring', 'Automatic Alerts', 'Intervention Workflows', 'Escalation Management']
    },
    {
      id: 'growth',
      title: 'Growth Intelligence Suite',
      description: 'Customer acquisition, expansion, and growth optimization strategies',
      icon: TrendingUp,
      color: 'from-emerald-600/20 to-emerald-800/20',
      borderColor: 'border-emerald-500/30',
      iconColor: 'text-emerald-400',
      metrics: {
        acquisition: '+45%',
        expansion: '$156K',
        opportunities: '23 Active'
      },
      features: ['Acquisition Analysis', 'Expansion Tracking', 'Growth Opportunities', 'Market Intelligence']
    },
    {
      id: 'customer-journey',
      title: 'Advanced Customer Journey Visualization',
      description: 'AI-powered journey mapping with touchpoint analysis and optimization insights',
      icon: Route,
      color: 'from-violet-600/20 to-violet-800/20',
      borderColor: 'border-violet-500/30',
      iconColor: 'text-violet-400',
      metrics: {
        journeys: '8 Paths',
        touchpoints: '12 Active',
        optimization: '85.3%'
      },
      features: ['Journey Mapping', 'Touchpoint Analysis', 'Path Optimization', 'Conversion Insights']
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white flex items-center">
            <Brain className="w-10 h-10 mr-4 text-blue-400" />
            Customer Analytics Intelligence
          </h1>
          <p className="text-slate-400 mt-2 text-lg">
            AI-powered customer behavior analysis and purchase optimization platform
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge className="bg-blue-500/20 text-blue-400 text-sm px-3 py-1">
            <Sparkles className="w-4 h-4 mr-1" />
            AI-Powered Platform
          </Badge>
          <Badge className="bg-green-500/20 text-green-400 text-sm px-3 py-1">
            <Award className="w-4 h-4 mr-1" />
            Customer Focus
          </Badge>
        </div>
      </div>

      {/* Key Performance Indicators */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {customerData?.dashboard_data?.total_customers || 0}
                </div>
                <div className="text-xs text-blue-200">Total Customers</div>
              </div>
              <Users className="h-8 w-8 text-blue-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  ${dashboardData?.total_revenue ? (dashboardData.total_revenue / 1000).toFixed(0) + 'K' : '0'}
                </div>
                <div className="text-xs text-green-200">Total Revenue</div>
              </div>
              <DollarSign className="h-8 w-8 text-green-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {dashboardData?.conversion_metrics?.conversion_rate ? 
                    (dashboardData.conversion_metrics.conversion_rate * 100).toFixed(1) + '%' : '0%'}
                </div>
                <div className="text-xs text-purple-200">Conversion Rate</div>
              </div>
              <Target className="h-8 w-8 text-purple-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {marketingData?.campaigns_count || 0}
                </div>
                <div className="text-xs text-orange-200">Active Campaigns</div>
              </div>
              <Megaphone className="h-8 w-8 text-orange-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Insights Banner */}
      <Alert className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border-blue-500/30">
        <Brain className="h-5 w-5 text-blue-400" />
        <AlertDescription className="text-blue-300">
          <strong>AI Insight:</strong> Customer engagement is up 23% this month. 
          High-value customers show 67% higher likelihood to purchase add-on services. 
          Recommended focus: Cross-sell campaigns to engaged segments.
        </AlertDescription>
      </Alert>

      {/* Customer Analytics Modules Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {customerModules.map((module) => {
          const Icon = module.icon;
          return (
            <Card key={module.id} className={`bg-gradient-to-br ${module.color} ${module.borderColor} hover:scale-105 transform transition-all duration-200 cursor-pointer`}
                  onClick={() => onNavigate(module.id)}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Icon className={`w-6 h-6 ${module.iconColor} mr-3`} />
                    <CardTitle className="text-white text-lg">{module.title}</CardTitle>
                  </div>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    className="text-slate-400 hover:text-white"
                    onClick={(e) => {
                      e.stopPropagation();
                      onNavigate(module.id);
                    }}
                  >
                    <ArrowRightLeft className="w-4 h-4" />
                  </Button>
                </div>
                <CardDescription className="text-slate-300">
                  {module.description}
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-4">
                  {/* Key Metrics */}
                  <div className="grid grid-cols-3 gap-3">
                    {Object.entries(module.metrics).map(([key, value]) => (
                      <div key={key} className="text-center">
                        <div className="text-lg font-bold text-white">{value}</div>
                        <div className="text-xs text-slate-400 capitalize">{key}</div>
                      </div>
                    ))}
                  </div>
                  
                  {/* Features List */}
                  <div className="space-y-2">
                    <div className="text-sm font-medium text-slate-300">Key Features:</div>
                    <div className="grid grid-cols-2 gap-1">
                      {module.features.map((feature, index) => (
                        <div key={index} className="flex items-center text-xs text-slate-400">
                          <CheckCircle className="w-3 h-3 text-green-400 mr-1 flex-shrink-0" />
                          {feature}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Create Campaign</h3>
                <p className="text-slate-400 text-sm">Launch AI-powered email campaigns</p>
              </div>
              <Button 
                onClick={() => onNavigate('create')}
                className="bg-purple-600 hover:bg-purple-700"
              >
                <Send className="w-4 h-4 mr-2" />
                Create
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Customer Analysis</h3>
                <p className="text-slate-400 text-sm">Analyze customer behavior patterns</p>
              </div>
              <Button 
                onClick={() => onNavigate('customers')}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Brain className="w-4 h-4 mr-2" />
                Analyze
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Revenue Insights</h3>
                <p className="text-slate-400 text-sm">View revenue forecasts and trends</p>
              </div>
              <Button 
                onClick={() => onNavigate('revenue')}
                className="bg-green-600 hover:bg-green-700"
              >
                <TrendingUp className="w-4 h-4 mr-2" />
                View
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Switch to Website Analytics */}
      <Card className="bg-gradient-to-r from-slate-800/50 to-slate-700/50 backdrop-blur-xl border-slate-600">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-semibold text-white mb-2 flex items-center">
                <ArrowRightLeft className="w-5 h-5 mr-2 text-slate-400" />
                Need Website Analytics?
              </h3>
              <p className="text-slate-400">
                Switch to Website Analytics for SEO, performance monitoring, and technical optimization.
              </p>
            </div>
            <Button 
              onClick={() => onNavigate('website-analytics-dashboard')}
              variant="outline"
              className="border-slate-500 text-slate-300 hover:bg-slate-700"
            >
              <TrendingUp className="w-4 h-4 mr-2" />
              Website Analytics
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CustomerAnalyticsDashboard;