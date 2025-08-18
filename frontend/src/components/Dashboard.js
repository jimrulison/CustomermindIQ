import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Users, 
  TrendingUp, 
  Mail, 
  Target, 
  BarChart3, 
  Brain, 
  Zap,
  DollarSign,
  ShoppingCart,
  Megaphone,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  TrendingDown,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';

const Dashboard = ({ 
  dashboardData,
  customerData,
  marketingData,
  advancedFeaturesData,
  revenueAnalyticsData,
  analyticsInsightsDashboard
}) => {
  return (
    <div className="space-y-6">
      
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600/10 to-purple-600/10 border border-blue-500/20 rounded-xl p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Welcome to CustomerMind IQ</h1>
            <p className="text-slate-300 text-lg">Your Universal Customer Intelligence Platform</p>
            <p className="text-slate-400 mt-2">Advanced AI-powered insights across 8 major modules with 40+ microservices</p>
          </div>
          <div className="hidden lg:flex items-center space-x-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">8</div>
              <div className="text-xs text-slate-400">Modules</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">40+</div>
              <div className="text-xs text-slate-400">Services</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-400">100%</div>
              <div className="text-xs text-slate-400">AI-Powered</div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        
        {/* Customer Intelligence Stats */}
        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-blue-200">Customer Intelligence</CardTitle>
            <Users className="h-4 w-4 text-blue-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {customerData?.dashboard_data?.total_customers || 1247}
            </div>
            <p className="text-xs text-blue-300">
              <ArrowUpRight className="inline h-3 w-3 mr-1" />
              +12.5% from last month
            </p>
            <div className="mt-2 text-xs text-slate-300">
              AI Insights: {customerData?.dashboard_data?.insights_count || 15} active recommendations
            </div>
          </CardContent>
        </Card>

        {/* Marketing Automation Stats */}
        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-purple-200">Marketing Automation</CardTitle>
            <Megaphone className="h-4 w-4 text-purple-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {marketingData?.leadScoringData?.dashboard_data?.total_leads || 3847}
            </div>
            <p className="text-xs text-purple-300">
              <ArrowUpRight className="inline h-3 w-3 mr-1" />
              +18.3% campaign performance
            </p>
            <div className="mt-2 text-xs text-slate-300">
              Active Campaigns: {marketingData?.campaigns_count || 12}
            </div>
          </CardContent>
        </Card>

        {/* Revenue Analytics Stats */}
        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-green-200">Revenue Analytics</CardTitle>
            <DollarSign className="h-4 w-4 text-green-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              ${(revenueAnalyticsData?.revenueForecastingData?.dashboard_data?.total_revenue || 487650).toLocaleString()}
            </div>
            <p className="text-xs text-green-300">
              <ArrowUpRight className="inline h-3 w-3 mr-1" />
              +24.1% revenue growth
            </p>
            <div className="mt-2 text-xs text-slate-300">
              ROI: {(revenueAnalyticsData?.roi || 3.4).toFixed(1)}x average
            </div>
          </CardContent>
        </Card>

        {/* Analytics & Insights Stats */}
        <Card className="bg-gradient-to-br from-indigo-600/20 to-indigo-800/20 border-indigo-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-indigo-200">Analytics & Insights</CardTitle>
            <TrendingUp className="h-4 w-4 text-indigo-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {analyticsInsightsDashboard?.modules?.customer_journey_mapping?.dashboard_data?.overview?.total_customers_analyzed || 245}
            </div>
            <p className="text-xs text-indigo-300">
              <ArrowUpRight className="inline h-3 w-3 mr-1" />
              Customer journeys analyzed
            </p>
            <div className="mt-2 text-xs text-slate-300">
              Conversion Rate: {((analyticsInsightsDashboard?.modules?.customer_journey_mapping?.dashboard_data?.overview?.avg_conversion_rate || 0.24) * 100).toFixed(1)}%
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Module Status Overview */}
      <div className="grid gap-6 md:grid-cols-2">
        
        {/* Active Modules */}
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Activity className="w-5 h-5 mr-2 text-green-400" />
              Module Status
            </CardTitle>
            <CardDescription className="text-slate-400">
              Real-time status of all platform modules
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                  <span className="text-slate-300">Customer Intelligence</span>
                </div>
                <span className="text-green-400 text-sm">Online</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                  <span className="text-slate-300">Marketing Automation</span>
                </div>
                <span className="text-green-400 text-sm">Online</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                  <span className="text-slate-300">Revenue Analytics</span>
                </div>
                <span className="text-green-400 text-sm">Online</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                  <span className="text-slate-300">Advanced Features</span>
                </div>
                <span className="text-green-400 text-sm">Online</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                  <span className="text-slate-300">Analytics & Insights</span>
                </div>
                <span className="text-green-400 text-sm">Online</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-blue-400" />
              Recent Activity
            </CardTitle>
            <CardDescription className="text-slate-400">
              Latest platform activities and insights
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-blue-400 rounded-full mt-2"></div>
                <div>
                  <p className="text-slate-300 text-sm">New customer journey analysis completed</p>
                  <p className="text-slate-500 text-xs">2 minutes ago</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full mt-2"></div>
                <div>
                  <p className="text-slate-300 text-sm">Revenue forecasting model updated</p>
                  <p className="text-slate-500 text-xs">15 minutes ago</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-purple-400 rounded-full mt-2"></div>
                <div>
                  <p className="text-slate-300 text-sm">Marketing campaign performance analyzed</p>
                  <p className="text-slate-500 text-xs">1 hour ago</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-orange-400 rounded-full mt-2"></div>
                <div>
                  <p className="text-slate-300 text-sm">Churn prevention model triggered alerts</p>
                  <p className="text-slate-500 text-xs">3 hours ago</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <Zap className="w-5 h-5 mr-2 text-yellow-400" />
            Quick Actions
          </CardTitle>
          <CardDescription className="text-slate-400">
            Common tasks and shortcuts for your workflow
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <Alert className="bg-blue-500/10 border-blue-500/20 cursor-pointer hover:bg-blue-500/20 transition-colors">
              <Users className="h-4 w-4 text-blue-400" />
              <AlertDescription className="text-blue-300">
                <strong>Analyze Customer Segments</strong><br />
                Get AI-powered customer insights and recommendations
              </AlertDescription>
            </Alert>
            
            <Alert className="bg-purple-500/10 border-purple-500/20 cursor-pointer hover:bg-purple-500/20 transition-colors">
              <Mail className="h-4 w-4 text-purple-400" />
              <AlertDescription className="text-purple-300">
                <strong>Create Marketing Campaign</strong><br />
                Launch AI-optimized multi-channel campaigns
              </AlertDescription>
            </Alert>
            
            <Alert className="bg-green-500/10 border-green-500/20 cursor-pointer hover:bg-green-500/20 transition-colors">
              <TrendingUp className="h-4 w-4 text-green-400" />
              <AlertDescription className="text-green-300">
                <strong>Revenue Forecasting</strong><br />
                Generate predictive revenue and ROI analytics
              </AlertDescription>
            </Alert>
          </div>
        </CardContent>
      </Card>

      {/* Platform Overview */}
      <div className="bg-gradient-to-r from-slate-800/50 to-slate-900/50 border border-slate-700 rounded-xl p-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Universal Customer Intelligence Platform</h2>
          <p className="text-slate-300 max-w-3xl mx-auto">
            CustomerMind IQ provides comprehensive AI-powered insights across customer intelligence, marketing automation, 
            revenue analytics, advanced features, and analytics & insights. Make data-driven decisions with our advanced 
            machine learning models and business intelligence tools.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-6 text-sm text-slate-400">
            <span>• AI-Powered Insights</span>
            <span>• Real-time Analytics</span>
            <span>• Predictive Modeling</span>
            <span>• Multi-channel Automation</span>
            <span>• Revenue Optimization</span>
            <span>• Customer Journey Mapping</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;