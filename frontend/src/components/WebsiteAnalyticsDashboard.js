import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import axios from 'axios';
import { 
  Globe,
  TrendingUp, 
  BarChart3,
  Target,
  Activity,
  Database,
  Shield,
  Cpu,
  Search,
  Zap,
  Monitor,
  Settings,
  ArrowRightLeft,
  CheckCircle,
  Brain,
  Sparkles,
  Lightbulb,
  Award,
  RefreshCw,
  Clock,
  X,
  Info,
  TrendingUp as TrendIcon,
  PieChart,
  Eye
} from 'lucide-react';

const WebsiteAnalyticsDashboard = ({ 
  analyticsInsightsDashboard,
  onNavigate 
}) => {

  const [updating, setUpdating] = useState(false);
  const [updateMessage, setUpdateMessage] = useState('');
  const [showDataSourceModal, setShowDataSourceModal] = useState(false);
  const [selectedDataSource, setSelectedDataSource] = useState(null);
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Handle UPDATE ALL button click
  const handleUpdateAll = async () => {
    try {
      setUpdating(true);
      setUpdateMessage('Initiating comprehensive website analysis...');
      
      const response = await axios.post(`${backendUrl}/api/website-intelligence/update-all`);
      console.log('Update initiated:', response.data);
      
      setUpdateMessage('✅ Update started! This may take up to 15 minutes to complete. You can continue using other features while the analysis runs in the background.');
      
      // Clear message after 8 seconds
      setTimeout(() => {
        setUpdateMessage('');
        setUpdating(false);
      }, 8000);
      
    } catch (error) {
      console.error('Error updating websites:', error);
      setUpdateMessage('❌ Update failed. Please try again or contact support.');
      setTimeout(() => {
        setUpdateMessage('');
        setUpdating(false);
      }, 5000);
    }
  };

  // Data source drill-down handlers for Analytics & Insights
  const showDataSource = (section, metricType, metricName, currentValue) => {
    const sourceDetails = {
      // WEBSITE ANALYTICS KPI DATA SOURCES
      'kpi_websites_monitored': {
        title: 'Websites Monitored - Data Source',
        description: 'Total number of websites actively tracked by the analytics platform',
        sources: [
          '• Website Intelligence Hub: Active website configurations and monitoring setup',
          '• Domain Registry: Verified domain ownership and access permissions',  
          '• Analytics SDK: Deployed tracking scripts and measurement codes',
          '• Health Monitoring System: Continuous uptime and availability checks'
        ],
        methodology: 'Website count includes all configured domains with active monitoring, verified ownership, and successful data collection within last 7 days. Excludes paused or archived websites.',
        dataPoints: 'Domain names, monitoring status, last data collection timestamp, tracking configuration',
        updateFrequency: 'Real-time tracking with immediate updates when websites are added/removed',
        currentValue: currentValue,
        icon: Globe,
        color: 'emerald'
      },
      'kpi_overall_health_score': {
        title: 'Overall Health Score - Data Source',
        description: 'Comprehensive health assessment across all monitored websites',
        sources: [
          '• Performance Monitoring: Core Web Vitals and page speed measurements',
          '• SEO Analysis Engine: Technical SEO audit results and optimization scores',
          '• Security Scanners: SSL certificates, security headers, and vulnerability checks',
          '• Accessibility Testing: WCAG compliance and usability assessments'
        ],
        methodology: 'Health Score = weighted average of Performance (30%), SEO (25%), Security (25%), Accessibility (20%). Each dimension scored 0-100 using industry standards and best practices.',
        dataPoints: 'Core Web Vitals, SEO scores, security ratings, accessibility compliance, uptime metrics',
        updateFrequency: 'Continuous monitoring with hourly health score recalculation',
        currentValue: currentValue,
        icon: Activity,
        color: 'blue'
      },
      'kpi_keywords_tracked': {
        title: 'Keywords Tracked - Data Source',
        description: 'Total number of SEO keywords monitored across all websites',
        sources: [
          '• SEO Intelligence Engine: Keyword research and ranking data collection',
          '• Search Console Integration: Google Search Console API data import',
          '• Keyword Research Tools: Third-party SEO tool integrations',
          '• Competitor Analysis: Market positioning and keyword gap analysis'
        ],
        methodology: 'Keyword count includes primary target keywords, long-tail variations, and competitor keywords. Updated based on search volume trends and business priority adjustments.',
        dataPoints: 'Keyword phrases, search volume, ranking positions, click-through rates, competition levels',
        updateFrequency: 'Daily keyword ranking updates with weekly keyword list optimization',
        currentValue: currentValue,
        icon: Search,
        color: 'purple'
      },
      'kpi_performance_score': {
        title: 'Performance Score - Data Source',
        description: 'Aggregate performance measurement across all monitored websites',
        sources: [
          '• Lighthouse Performance Audits: Google Lighthouse automated testing',
          '• Real User Monitoring (RUM): Actual visitor experience data collection',
          '• Synthetic Testing: Automated performance tests from multiple locations', 
          '• Core Web Vitals API: Google\'s official performance metrics tracking'
        ],
        methodology: 'Performance Score = weighted average of LCP (40%), FID (30%), CLS (30%) normalized to 0-100 scale. Includes both lab data and field data for comprehensive assessment.',
        dataPoints: 'Largest Contentful Paint, First Input Delay, Cumulative Layout Shift, Speed Index, Time to Interactive',
        updateFrequency: 'Continuous real-user monitoring with daily synthetic test runs',
        currentValue: currentValue,
        icon: Zap,
        color: 'orange'
      }
    };

    const key = `${section}_${metricType}`;
    const details = sourceDetails[key] || {
      title: `${metricName} - Data Source`,
      description: 'Data source information for this analytics metric',
      sources: ['• Website analytics platform', '• Performance monitoring tools', '• SEO tracking systems', '• Business intelligence dashboards'],
      methodology: 'Calculated using advanced analytics algorithms and real-time data processing',
      dataPoints: 'Website metrics, user behavior data, performance indicators, business outcomes',
      updateFrequency: 'Updated regularly based on monitoring schedules and data availability',
      currentValue: currentValue,
      icon: BarChart3,
      color: 'slate'
    };

    setSelectedDataSource(details);
    setShowDataSourceModal(true);
  };

  // Website Analytics focused modules
  const websiteModules = [
    {
      id: 'website-intelligence',
      title: 'Website Intelligence Hub',
      description: 'Comprehensive website performance, SEO, and technical analysis',
      icon: Globe,
      color: 'from-emerald-600/20 to-emerald-800/20',
      borderColor: 'border-emerald-500/30',
      iconColor: 'text-emerald-400',
      metrics: {
        websites: '3 Sites',
        health: '87.4%',
        keywords: '156'
      },
      features: ['Performance Analysis', 'SEO Intelligence', 'Technical Audits', 'Mobile Optimization']
    },
    {
      id: 'ai-insights',
      title: 'AI Website Insights',
      description: 'Custom AI-powered website analysis with intelligent prompts and recommendations',
      icon: Lightbulb,
      color: 'from-yellow-600/20 to-yellow-800/20',
      borderColor: 'border-yellow-500/30',
      iconColor: 'text-yellow-400',
      metrics: {
        prompts: '25+ Templates',
        accuracy: '94.8%',
        insights: 'Real-time'
      },
      features: ['Website Prompts', 'SEO Analysis', 'Performance Insights', 'Technical Recommendations']
    },
    {
      id: 'analytics',
      title: 'Analytics & Insights',
      description: 'Customer journey mapping, attribution analysis, and competitive intelligence',
      icon: TrendingUp,
      color: 'from-indigo-600/20 to-indigo-800/20',
      borderColor: 'border-indigo-500/30',
      iconColor: 'text-indigo-400',
      metrics: {
        journeys: '50 Paths',
        attribution: '$485K',
        cohorts: '13 Groups'
      },
      features: ['Journey Mapping', 'Revenue Attribution', 'Cohort Analysis', 'Competitive Intel']
    },
    {
      id: 'product',
      title: 'Product Intelligence Hub',
      description: 'Feature usage analytics, onboarding optimization, and user journey analysis',
      icon: Target,
      color: 'from-teal-600/20 to-teal-800/20',
      borderColor: 'border-teal-500/30',
      iconColor: 'text-teal-400',
      metrics: {
        features: '6 Tracked',
        adoption: '61.3%',
        retention: '91.7%'
      },
      features: ['Feature Analytics', 'Onboarding Flow', 'Product-Market Fit', 'User Journeys']
    },
    {
      id: 'integration',
      title: 'Integration & Data Hub',
      description: 'Data connectors, sync management, and integration analytics',
      icon: Database,
      color: 'from-blue-600/20 to-blue-800/20',
      borderColor: 'border-blue-500/30',
      iconColor: 'text-blue-400',
      metrics: {
        connectors: '4 Active',
        health: '91.2%',
        records: '11.5K'
      },
      features: ['Data Connectors', 'Sync Management', 'Quality Monitoring', 'Integration Analytics']
    },
    {
      id: 'compliance',
      title: 'Compliance & Governance',
      description: 'Compliance monitoring, audit management, and regulatory reporting',
      icon: Shield,
      color: 'from-purple-600/20 to-purple-800/20',
      borderColor: 'border-purple-500/30',
      iconColor: 'text-purple-400',
      metrics: {
        compliance: '94.7%',
        audits: '47 YTD',
        frameworks: '5 Active'
      },
      features: ['Compliance Monitoring', 'Audit Management', 'Data Governance', 'Regulatory Reports']
    },
    {
      id: 'ai-command',
      title: 'AI Command Center',
      description: 'AI orchestration, model management, and automation control',
      icon: Cpu,
      color: 'from-cyan-600/20 to-cyan-800/20',
      borderColor: 'border-cyan-500/30',
      iconColor: 'text-cyan-400',
      metrics: {
        models: '47 Active',
        efficiency: '92.4%',
        insights: '2,847'
      },
      features: ['AI Orchestration', 'Model Management', 'Automation Control', 'AI Insights Engine']
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white flex items-center">
            <Globe className="w-10 h-10 mr-4 text-emerald-400" />
            Website Analytics Intelligence
          </h1>
          <p className="text-slate-400 mt-2 text-lg">
            Comprehensive website performance, SEO optimization, and technical analysis platform
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge className="bg-emerald-500/20 text-emerald-400 text-sm px-3 py-1">
            <Monitor className="w-4 h-4 mr-1" />
            Website Focus
          </Badge>
          <Badge className="bg-blue-500/20 text-blue-400 text-sm px-3 py-1">
            <Zap className="w-4 h-4 mr-1" />
            Performance Optimized
          </Badge>
          <Button
            onClick={handleUpdateAll}
            disabled={updating}
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${updating ? 'animate-spin' : ''}`} />
            {updating ? 'Updating...' : 'UPDATE ALL'}
          </Button>
        </div>
      </div>

      {/* Update Status Message */}
      {updateMessage && (
        <Alert className="bg-emerald-500/10 border-emerald-500/30">
          <Clock className="h-4 w-4 text-emerald-400" />
          <AlertDescription className="text-emerald-300">
            {updateMessage}
          </AlertDescription>
        </Alert>
      )}

      {/* Key Performance Indicators */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="bg-gradient-to-br from-emerald-600/20 to-emerald-800/20 border-emerald-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">3</div>
                <div className="text-xs text-emerald-200">Websites Monitored</div>
              </div>
              <Globe className="h-8 w-8 text-emerald-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">87.4%</div>
                <div className="text-xs text-blue-200">Overall Health Score</div>
              </div>
              <Activity className="h-8 w-8 text-blue-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">156</div>
                <div className="text-xs text-purple-200">Keywords Tracked</div>
              </div>
              <Search className="h-8 w-8 text-purple-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">87.3%</div>
                <div className="text-xs text-orange-200">Performance Score</div>
              </div>
              <Zap className="h-8 w-8 text-orange-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Technical Insights Banner */}
      <Alert className="bg-gradient-to-r from-emerald-600/20 to-blue-600/20 border-emerald-500/30">
        <Monitor className="h-5 w-5 text-emerald-400" />
        <AlertDescription className="text-emerald-300">
          <strong>Technical Insight:</strong> Website performance improved by 15% this month. 
          Core Web Vitals are in the "Good" range. SEO rankings increased for 23 target keywords. 
          Recommended focus: Mobile optimization and page speed enhancement.
        </AlertDescription>
      </Alert>

      {/* Website Analytics Modules Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {websiteModules.map((module) => {
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
                <h3 className="text-lg font-semibold text-white mb-2">Website Analysis</h3>
                <p className="text-slate-400 text-sm">Analyze website performance and SEO</p>
              </div>
              <Button 
                onClick={() => onNavigate('website-intelligence')}
                className="bg-emerald-600 hover:bg-emerald-700"
              >
                <Globe className="w-4 h-4 mr-2" />
                Analyze
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Product Analytics</h3>
                <p className="text-slate-400 text-sm">Track feature usage and adoption</p>
              </div>
              <Button 
                onClick={() => onNavigate('product')}
                className="bg-teal-600 hover:bg-teal-700"
              >
                <Target className="w-4 h-4 mr-2" />
                Track
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">AI Command</h3>
                <p className="text-slate-400 text-sm">Manage AI models and automation</p>
              </div>
              <Button 
                onClick={() => onNavigate('ai-command')}
                className="bg-cyan-600 hover:bg-cyan-700"
              >
                <Cpu className="w-4 h-4 mr-2" />
                Control
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Switch to Customer Analytics */}
      <Card className="bg-gradient-to-r from-slate-800/50 to-slate-700/50 backdrop-blur-xl border-slate-600">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-semibold text-white mb-2 flex items-center">
                <ArrowRightLeft className="w-5 h-5 mr-2 text-slate-400" />
                Need Customer Analytics?
              </h3>
              <p className="text-slate-400">
                Switch to Customer Analytics for customer behavior analysis, marketing automation, and revenue optimization.
              </p>
            </div>
            <Button 
              onClick={() => onNavigate('customer-analytics-dashboard')}
              variant="outline"
              className="border-slate-500 text-slate-300 hover:bg-slate-700"
            >
              <Brain className="w-4 h-4 mr-2" />
              Customer Analytics
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default WebsiteAnalyticsDashboard;