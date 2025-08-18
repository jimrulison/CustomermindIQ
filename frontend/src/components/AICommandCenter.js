import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Brain, 
  Cpu, 
  Zap, 
  TrendingUp, 
  BarChart3,
  Settings,
  CheckCircle,
  AlertTriangle,
  Clock,
  Activity,
  Target,
  Database,
  Eye,
  Lightbulb,
  Workflow
} from 'lucide-react';

const AICommandCenter = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [orchestrationData, setOrchestrationData] = useState(null);
  const [modelsData, setModelsData] = useState(null);
  const [automationData, setAutomationData] = useState(null);
  const [insightsData, setInsightsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAICommandData();
  }, []);

  const loadAICommandData = async () => {
    try {
      setLoading(true);
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      
      const [orchestration, models, automation, insights] = await Promise.all([
        fetch(`${backendUrl}/api/ai-command/orchestration-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/ai-command/models-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/ai-command/automation-dashboard`).then(r => r.json()),
        fetch(`${backendUrl}/api/ai-command/insights-dashboard`).then(r => r.json())
      ]);
      
      setOrchestrationData(orchestration);
      setModelsData(models);
      setAutomationData(automation);
      setInsightsData(insights);
    } catch (error) {
      console.error('Error loading AI Command Center data:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'orchestration', name: 'AI Orchestration', icon: Workflow },
    { id: 'models', name: 'Model Management', icon: Cpu },
    { id: 'automation', name: 'Automation Control', icon: Zap },
    { id: 'insights', name: 'AI Insights Engine', icon: Lightbulb }
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
          <h1 className="text-3xl font-bold text-white">AI Command Center</h1>
          <p className="text-slate-400 mt-2">Centralized AI operations, model orchestration, and intelligent automation control</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className="bg-cyan-500/20 text-cyan-400">
            {orchestrationData?.dashboard?.ai_overview?.total_ai_models || '0'} AI Models
          </Badge>
          <Badge className="bg-purple-500/20 text-purple-400">4 Command Modules</Badge>
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
            <Card className="bg-gradient-to-br from-cyan-600/20 to-cyan-800/20 border-cyan-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Brain className="h-8 w-8 text-cyan-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {orchestrationData?.dashboard?.ai_overview?.total_ai_models || '0'}
                  </div>
                  <div className="text-xs text-cyan-200">AI Models</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Zap className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {automationData?.dashboard?.automation_overview?.automation_coverage || '0'}%
                  </div>
                  <div className="text-xs text-green-200">Automation Coverage</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <Lightbulb className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    {insightsData?.dashboard?.insights_overview?.total_insights_generated || '0'}
                  </div>
                  <div className="text-xs text-purple-200">AI Insights</div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
              <CardContent className="p-4">
                <div className="text-center">
                  <TrendingUp className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-white">
                    ${(insightsData?.dashboard?.impact_tracking?.total_value_created / 1000 || 0).toFixed(0)}K
                  </div>
                  <div className="text-xs text-orange-200">Value Created</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Key Performance Metrics */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-cyan-400" />
                  AI System Performance
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-400">
                      {orchestrationData?.dashboard?.ai_overview?.model_performance_avg || '0'}%
                    </div>
                    <div className="text-xs text-slate-400">Avg Performance</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-400">
                      {orchestrationData?.dashboard?.ai_overview?.active_models || '0'}
                    </div>
                    <div className="text-xs text-slate-400">Active Models</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-400">
                      {(orchestrationData?.dashboard?.ai_overview?.inference_requests / 1000 || 0).toFixed(0)}K
                    </div>
                    <div className="text-xs text-slate-400">Inferences/24h</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-400">
                      {orchestrationData?.dashboard?.ai_overview?.ai_efficiency_score || '0'}%
                    </div>
                    <div className="text-xs text-slate-400">Efficiency Score</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Target className="w-5 h-5 mr-2 text-orange-400" />
                  Business Impact
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-400">
                      {automationData?.dashboard?.business_impact?.productivity_improvement || '0'}h
                    </div>
                    <div className="text-xs text-slate-400">Hours Saved/Day</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-400">
                      ${(automationData?.dashboard?.business_impact?.cost_reduction / 1000 || 0).toFixed(0)}K
                    </div>
                    <div className="text-xs text-slate-400">Cost Reduction/Day</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-400">
                      {automationData?.dashboard?.automation_overview?.automation_accuracy || '0'}%
                    </div>
                    <div className="text-xs text-slate-400">Decision Accuracy</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-400">
                      {(automationData?.dashboard?.automation_overview?.decisions_automated_24h / 1000 || 0).toFixed(0)}K
                    </div>
                    <div className="text-xs text-slate-400">Decisions/Day</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* AI Orchestration Tab */}
      {activeTab === 'orchestration' && (
        <div className="space-y-6">
          <div className="grid gap-6">
            {orchestrationData?.dashboard?.model_performance?.map((model, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span>{model.model_name}</span>
                    <div className="flex items-center space-x-2">
                      <Badge className={`text-xs ${
                        model.drift_detection === 'stable'
                          ? 'bg-green-500/20 text-green-400'
                          : model.drift_detection === 'mild_drift'
                            ? 'bg-yellow-500/20 text-yellow-400'
                            : 'bg-red-500/20 text-red-400'
                      }`}>
                        {model.drift_detection}
                      </Badge>
                      <Badge className="bg-slate-600/50 text-slate-300">
                        {model.model_type}
                      </Badge>
                    </div>
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Domain: {model.domain} • Status: {model.status}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <div className="text-lg font-bold text-green-400">
                          {model.performance_score}%
                        </div>
                        <div className="text-xs text-slate-400">Performance</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-blue-400">
                          {model.accuracy}%
                        </div>
                        <div className="text-xs text-slate-400">Accuracy</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-purple-400">
                          {model.inference_latency}ms
                        </div>
                        <div className="text-xs text-slate-400">Latency</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-orange-400">
                          {(model.throughput || 0).toLocaleString()}
                        </div>
                        <div className="text-xs text-slate-400">Req/min</div>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="text-slate-300">
                        Last Training: {new Date(model.last_training).toLocaleDateString()}
                      </div>
                      <div className="text-slate-300">
                        Next Retrain: {new Date(model.next_retrain).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* AI Workflows */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Workflow className="w-5 h-5 mr-2 text-cyan-400" />
                Active AI Workflows
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {orchestrationData?.dashboard?.ai_workflows?.map((workflow, index) => (
                  <div key={index} className="border border-slate-600 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-semibold text-white">{workflow.workflow_name}</h4>
                      <Badge className={`text-xs ${
                        workflow.status === 'running'
                          ? 'bg-green-500/20 text-green-400'
                          : workflow.status === 'paused'
                            ? 'bg-yellow-500/20 text-yellow-400'
                            : 'bg-red-500/20 text-red-400'
                      }`}>
                        {workflow.status}
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div className="text-slate-300">
                        Trigger: {workflow.trigger_type}
                      </div>
                      <div className="text-slate-300">
                        Frequency: {workflow.frequency}
                      </div>
                      <div className="text-slate-300">
                        Success Rate: {workflow.success_rate}%
                      </div>
                    </div>
                    
                    <div className="mt-2">
                      <div className="text-xs text-slate-400 mb-1">Models Involved:</div>
                      <div className="flex flex-wrap gap-1">
                        {workflow.models_involved?.map((model, modelIndex) => (
                          <Badge key={modelIndex} className="bg-blue-500/10 text-blue-300 text-xs">
                            {model}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Model Management Tab */}
      {activeTab === 'models' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Model Categories</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {modelsData?.dashboard?.model_categories?.map((category, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{category.category}</h4>
                        <Badge className={`text-xs ${
                          category.business_impact === 'Critical'
                            ? 'bg-red-500/20 text-red-400'
                            : category.business_impact === 'High'
                              ? 'bg-orange-500/20 text-orange-400'
                              : 'bg-blue-500/20 text-blue-400'
                        }`}>
                          {category.business_impact}
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 mb-2">
                        <div className="text-center">
                          <div className="text-lg font-bold text-blue-400">
                            {category.models_count}
                          </div>
                          <div className="text-xs text-slate-400">Models</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-green-400">
                            {category.avg_performance}%
                          </div>
                          <div className="text-xs text-slate-400">Avg Performance</div>
                        </div>
                      </div>
                      
                      <div className="text-xs text-slate-400">
                        Status: {category.deployment_status}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Deployment Pipeline</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {modelsData?.dashboard?.deployment_pipeline?.map((stage, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{stage.pipeline_stage}</h4>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {stage.models_in_stage} models
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-xs">
                        <div className="text-slate-300">
                          Duration: {stage.avg_stage_duration}
                        </div>
                        <div className="text-slate-300">
                          Success Rate: {stage.success_rate}%
                        </div>
                      </div>
                      
                      {stage.current_models && (
                        <div className="mt-2">
                          <div className="text-xs text-slate-400 mb-1">Current Models:</div>
                          {stage.current_models.slice(0, 2).map((model, modelIndex) => (
                            <div key={modelIndex} className="flex justify-between items-center text-xs">
                              <span className="text-slate-300">{model.name}</span>
                              <span className="text-blue-400">{model.progress}%</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* A/B Testing */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Settings className="w-5 h-5 mr-2 text-purple-400" />
                Active A/B Tests
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {modelsData?.dashboard?.ab_testing?.current_tests?.map((test, index) => (
                  <div key={index} className="border border-slate-600 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-semibold text-white">Test {test.test_id}</h4>
                      <Badge className="bg-purple-500/20 text-purple-400">
                        {test.traffic_split} split
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm mb-2">
                      <div className="text-slate-300">
                        Model A: {test.model_a}
                      </div>
                      <div className="text-slate-300">
                        Model B: {test.model_b}
                      </div>
                    </div>
                    
                    <div className="mb-2">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-xs text-slate-400">Progress</span>
                        <span className="text-xs text-white">{test.progress}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-1">
                        <div 
                          className="bg-gradient-to-r from-purple-500 to-pink-500 h-1 rounded-full"
                          style={{ width: `${test.progress}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <div className="text-xs text-slate-300">
                      Winner: <span className="text-green-400">{test.preliminary_winner}</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Automation Control Tab */}
      {activeTab === 'automation' && (
        <div className="space-y-6">
          <div className="grid gap-6">
            {automationData?.dashboard?.automation_categories?.map((category, index) => (
              <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span>{category.category}</span>
                    <div className="flex items-center space-x-2">
                      <Badge className={`text-xs ${
                        category.business_impact === 'Critical'
                          ? 'bg-red-500/20 text-red-400'
                          : category.business_impact === 'High'
                            ? 'bg-orange-500/20 text-orange-400'
                            : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {category.business_impact}
                      </Badge>
                      <Badge className="bg-green-500/20 text-green-400">
                        {category.automation_level}% automated
                      </Badge>
                    </div>
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    {category.processes_count} processes • ROI: {category.roi}%
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {category.processes?.slice(0, 2).map((process, processIndex) => (
                      <div key={processIndex} className="border border-slate-600 rounded-lg p-3">
                        <div className="flex justify-between items-center mb-2">
                          <h5 className="font-medium text-white">{process.name}</h5>
                          <Badge className="bg-blue-500/20 text-blue-400 text-xs">
                            {process.status}
                          </Badge>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-3 text-sm">
                          <div className="text-center">
                            <div className="text-lg font-bold text-green-400">
                              {process.automation_level}%
                            </div>
                            <div className="text-xs text-slate-400">Automation</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-blue-400">
                              {(process.decisions_per_day || 0).toLocaleString()}
                            </div>
                            <div className="text-xs text-slate-400">Decisions/Day</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-purple-400">
                              {process.accuracy}%
                            </div>
                            <div className="text-xs text-slate-400">Accuracy</div>
                          </div>
                        </div>
                        
                        <div className="text-xs text-slate-300 mt-2">
                          Time Saved: {process.time_saved}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* AI Insights Engine Tab */}
      {activeTab === 'insights' && (
        <div className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Insight Categories</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {insightsData?.dashboard?.insight_categories?.map((category, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{category.category}</h4>
                        <Badge className={`text-xs ${
                          category.business_value === 'Critical'
                            ? 'bg-red-500/20 text-red-400'
                            : category.business_value === 'High'
                              ? 'bg-orange-500/20 text-orange-400'
                              : 'bg-blue-500/20 text-blue-400'
                        }`}>
                          {category.business_value}
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-3 gap-3 mb-2">
                        <div className="text-center">
                          <div className="text-lg font-bold text-blue-400">
                            {category.insights_count}
                          </div>
                          <div className="text-xs text-slate-400">Insights</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-green-400">
                            {category.accuracy}%
                          </div>
                          <div className="text-xs text-slate-400">Accuracy</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-purple-400">
                            {category.implementation_rate}%
                          </div>
                          <div className="text-xs text-slate-400">Implemented</div>
                        </div>
                      </div>
                      
                      <div className="text-xs text-slate-300">
                        ROI: {category.avg_roi}%
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Strategic Intelligence</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {insightsData?.dashboard?.strategic_intelligence?.strategic_themes?.map((theme, index) => (
                    <div key={index} className="border border-slate-600 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-semibold text-white">{theme.theme}</h4>
                        <Badge className="bg-blue-500/20 text-blue-400">
                          {theme.insights} insights
                        </Badge>
                      </div>
                      
                      <div className="mb-2">
                        <div className="text-sm text-green-400 font-semibold">
                          {theme.potential_impact}
                        </div>
                        <div className="text-xs text-slate-400">
                          Confidence: {theme.confidence}%
                        </div>
                      </div>
                      
                      <div className="space-y-1">
                        {theme.key_recommendations?.slice(0, 2).map((rec, recIndex) => (
                          <div key={recIndex} className="text-xs text-slate-300">
                            • {rec}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Insights */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Eye className="w-5 h-5 mr-2 text-cyan-400" />
                Recent AI Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {insightsData?.dashboard?.insight_categories?.slice(0, 2).map((category, categoryIndex) => (
                  <div key={categoryIndex}>
                    {category.recent_insights?.map((insight, insightIndex) => (
                      <div key={insightIndex} className="border-l-4 border-cyan-500 pl-4 mb-4">
                        <div className="flex justify-between items-start">
                          <div>
                            <h5 className="font-semibold text-white mb-1">{category.category}</h5>
                            <p className="text-sm text-slate-300 mb-2">{insight.insight}</p>
                            <div className="flex items-center space-x-4 text-xs">
                              <span className="text-green-400">
                                Confidence: {insight.confidence}%
                              </span>
                              <span className="text-blue-400">
                                Impact: {insight.potential_impact}
                              </span>
                            </div>
                            <div className="text-xs text-slate-400 mt-1">
                              Recommendation: {insight.recommendation}
                            </div>
                          </div>
                          <div className="text-xs text-slate-400">
                            {new Date(insight.timestamp).toLocaleDateString()}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default AICommandCenter;