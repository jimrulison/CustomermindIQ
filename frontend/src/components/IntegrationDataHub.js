import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Database, 
  Zap, 
  Shield, 
  BarChart3, 
  Settings,
  CheckCircle,
  AlertTriangle,
  Clock,
  TrendingUp,
  DollarSign,
  Activity,
  Link,
  RefreshCw,
  Eye,
  Target
} from 'lucide-react';

const IntegrationDataHub = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [connectorsData, setConnectorsData] = useState(null);
  const [syncData, setSyncData] = useState(null);
  const [qualityData, setQualityData] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadIntegrationData();
  }, []);

  const loadIntegrationData = async () => {
    try {
      setLoading(true);
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      
      const [connectors, sync, quality, analytics] = await Promise.all([
        fetch(`${backendUrl}/api/integration-hub/connectors-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/integration-hub/sync-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/integration-hub/quality-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/integration-hub/analytics-dashboard`).then(r => r.json())
      ]);
      
      setConnectorsData(connectors);
      setSyncData(sync);
      setQualityData(quality);
      setAnalyticsData(analytics);
    } catch (error) {
      console.error('Error loading Integration Data Hub data:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'connectors', name: 'Data Connectors', icon: Link },
    { id: 'sync', name: 'Sync Management', icon: Sync },
    { id: 'quality', name: 'Data Quality', icon: Shield },
    { id: 'analytics', name: 'Integration Analytics', icon: TrendingUp }
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
          <h1 className="text-3xl font-bold text-white">Integration & Data Management Hub</h1>
          <p className="text-slate-400 mt-2">Centralized data integration, sync management, and quality monitoring</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className="bg-green-500/20 text-green-400">
            {connectorsData?.dashboard?.health_insights?.healthy_connectors || '0'} Healthy
          </Badge>
          <Badge className="bg-blue-500/20 text-blue-400">4 Core Modules</Badge>
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
                  <Link className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {connectorsData?.dashboard?.health_insights?.total_active_connectors || '0'}
                  </div>
                  <div className="text-xs text-green-200">Active Connectors</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Sync className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {syncData?.dashboard?.sync_overview?.sync_success_rate || '0'}%
                  </div>
                  <div className="text-xs text-blue-200">Sync Success Rate</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Shield className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {qualityData?.dashboard?.quality_overview?.overall_quality_score || '0'}
                  </div>
                  <div className="text-xs text-purple-200">Quality Score</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {analyticsData?.dashboard?.roi_analysis?.total_roi || '0'}%
                  </div>
                  <div className="text-xs text-orange-200">Integration ROI</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* System Health Overview */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-cyan-400" />
                  System Health Status
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Overall System Health</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
                          style={{ width: `${connectorsData?.dashboard?.health_insights?.overall_system_health || 0}%` }}
                        ></div>
                      </div>
                      <span className="text-white font-semibold">{connectorsData?.dashboard?.health_insights?.overall_system_health || 0}%</span>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Data Quality</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                          style={{ width: `${qualityData?.dashboard?.quality_overview?.overall_quality_score || 0}%` }}
                        ></div>
                      </div>
                      <span className="text-white font-semibold">{qualityData?.dashboard?.quality_overview?.overall_quality_score || 0}%</span>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Sync Performance</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full"
                          style={{ width: `${syncData?.dashboard?.sync_overview?.sync_success_rate || 0}%` }}
                        ></div>
                      </div>
                      <span className="text-white font-semibold">{syncData?.dashboard?.sync_overview?.sync_success_rate || 0}%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <DollarSign className="w-5 h-5 mr-2 text-green-400" />
                  Business Impact
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-400">
                      ${(analyticsData?.dashboard?.business_impact?.revenue_attribution?.direct_revenue_enabled / 1000 || 0).toFixed(0)}K
                    </div>
                    <div className="text-xs text-slate-400">Revenue Enabled</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-400">
                      {analyticsData?.dashboard?.business_impact?.operational_efficiency?.hours_saved_monthly || 0}h
                    </div>
                    <div className="text-xs text-slate-400">Hours Saved/Month</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-400">
                      {analyticsData?.dashboard?.business_impact?.operational_efficiency?.error_reduction || 0}%
                    </div>
                    <div className="text-xs text-slate-400">Error Reduction</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-400">
                      {analyticsData?.dashboard?.business_impact?.operational_efficiency?.team_capacity_freed || 0}
                    </div>
                    <div className="text-xs text-slate-400">FTE Freed</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Data Connectors Tab */}
      {activeTab === 'connectors' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {connectorsData?.dashboard?.active_connectors?.map((connector, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span>{connector.connector_name}</span>
                    <Badge className={`text-xs ${
                      connector.connection_status === 'healthy' 
                        ? 'bg-green-500/20 text-green-400' 
                        : connector.connection_status === 'warning'
                          ? 'bg-yellow-500/20 text-yellow-400'
                          : 'bg-red-500/20 text-red-400'
                    }`}>
                      {connector.connection_status}
                    </Badge>
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Platform: {connector.platform} • {connector.sync_frequency}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center">
                      <div className="text-lg font-bold text-blue-400">
                        {connector.health_score}
                      </div>
                      <div className="text-xs text-slate-400">Health Score</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-green-400">
                        {connector.data_volume_24h?.toLocaleString() || 'N/A'}
                      </div>
                      <div className="text-xs text-slate-400">Records (24h)</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-purple-400">
                        {connector.total_records?.toLocaleString() || 'N/A'}
                      </div>
                      <div className="text-xs text-slate-400">Total Records</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-orange-400">
                        {connector.data_types?.length || 0}
                      </div>
                      <div className="text-xs text-slate-400">Data Types</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Sync Management Tab */}
      {activeTab === 'sync' && (
        <div className="space-y-6">
          <div className="grid gap-6">
            {syncData?.dashboard?.active_sync_jobs?.map((job, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span>{job.connector_name}</span>
                    <div className="flex items-center space-x-2">
                      <Badge className={`text-xs ${
                        job.status === 'running' 
                          ? 'bg-blue-500/20 text-blue-400' 
                          : job.status === 'completed'
                            ? 'bg-green-500/20 text-green-400'
                            : job.status === 'error'
                              ? 'bg-red-500/20 text-red-400'
                              : 'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {job.status}
                      </Badge>
                      <Badge className="bg-slate-600/50 text-slate-300">
                        {job.sync_type}
                      </Badge>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {job.status === 'running' && (
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-slate-300">Progress</span>
                          <span className="text-white font-semibold">{job.progress}%</span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${job.progress}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <div className="text-lg font-bold text-blue-400">
                          {job.records_processed?.toLocaleString() || 'N/A'}
                        </div>
                        <div className="text-xs text-slate-400">Records Processed</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-green-400">
                          {job.records_remaining?.toLocaleString() || job.expected_records?.toLocaleString() || 'N/A'}
                        </div>
                        <div className="text-xs text-slate-400">
                          {job.status === 'running' ? 'Remaining' : 'Expected'}
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-purple-400">
                          {job.duration ? `${job.duration}s` : job.estimated_duration ? `${job.estimated_duration}s` : 'N/A'}
                        </div>
                        <div className="text-xs text-slate-400">
                          {job.status === 'completed' ? 'Duration' : 'Est. Duration'}
                        </div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-orange-400">
                          {job.sync_frequency}
                        </div>
                        <div className="text-xs text-slate-400">Frequency</div>
                      </div>
                    </div>
                    
                    <div className="text-sm text-slate-400">
                      <strong>Status:</strong> {job.current_operation}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Data Quality Tab */}
      {activeTab === 'quality' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Quality Dimensions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {qualityData?.dashboard?.quality_dimensions?.slice(0, 4).map((dimension, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-300">{dimension.dimension}</span>
                        <div className="flex items-center space-x-2">
                          <span className="text-white font-semibold">{dimension.score}</span>
                          <Badge className={`text-xs ${
                            dimension.trend === 'improving' 
                              ? 'bg-green-500/20 text-green-400' 
                              : dimension.trend === 'stable'
                                ? 'bg-blue-500/20 text-blue-400'
                                : 'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {dimension.trend}
                          </Badge>
                        </div>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                          style={{ width: `${dimension.score}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-slate-400">
                        {dimension.issues_count} issues • {dimension.improvement_trend}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Data Sources Quality</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {qualityData?.dashboard?.quality_by_source?.map((source, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{source.source}</h4>
                        <Badge className={`text-xs ${
                          source.quality_trend === 'improving' 
                            ? 'bg-green-500/20 text-green-400' 
                            : source.quality_trend === 'stable'
                              ? 'bg-blue-500/20 text-blue-400'
                              : 'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {source.overall_score}
                        </Badge>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="text-slate-400">
                          Records: {source.records_count?.toLocaleString()}
                        </div>
                        <div className="text-slate-400">
                          Issues: {source.issues_count}
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

      {/* Integration Analytics Tab */}
      {activeTab === 'analytics' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-3">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">ROI Overview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center mb-4">
                  <div className="text-4xl font-bold text-green-400">
                    {analyticsData?.dashboard?.roi_analysis?.total_roi || 0}%
                  </div>
                  <div className="text-slate-400">Total ROI</div>
                </div>
                <div className="space-y-2">
                  {analyticsData?.dashboard?.roi_analysis?.roi_by_category?.map((category, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-slate-300 text-sm">{category.category}</span>
                      <span className="text-white font-semibold">${(category.value / 1000).toFixed(0)}K</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Performance Metrics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-xl font-bold text-blue-400">
                      {analyticsData?.dashboard?.performance_overview?.overall_health_score || 0}%
                    </div>
                    <div className="text-xs text-slate-400">System Health</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl font-bold text-green-400">
                      {analyticsData?.dashboard?.performance_overview?.uptime_percentage || 0}%
                    </div>
                    <div className="text-xs text-slate-400">Uptime</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl font-bold text-purple-400">
                      {analyticsData?.dashboard?.performance_overview?.avg_response_time || 0}s
                    </div>
                    <div className="text-xs text-slate-400">Avg Response</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl font-bold text-orange-400">
                      {analyticsData?.dashboard?.performance_overview?.error_rate || 0}%
                    </div>
                    <div className="text-xs text-slate-400">Error Rate</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Cost Analysis</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center mb-4">
                  <div className="text-2xl font-bold text-blue-400">
                    ${analyticsData?.dashboard?.cost_analysis?.total_monthly_costs?.toLocaleString() || 0}
                  </div>
                  <div className="text-slate-400">Monthly Costs</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-green-400">
                    ${analyticsData?.dashboard?.cost_analysis?.projected_savings?.annual?.toLocaleString() || 0}
                  </div>
                  <div className="text-xs text-slate-400">Projected Annual Savings</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

export default IntegrationDataHub;