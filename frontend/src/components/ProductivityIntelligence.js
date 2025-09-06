import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Zap, 
  Clock, 
  Target, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle,
  ArrowRight,
  Calendar,
  BarChart3,
  Users,
  DollarSign,
  Lightbulb,
  Settings,
  Timer
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const ProductivityIntelligence = () => {
  // Component state
  const [prompt, setPrompt] = useState('');
  const [contextType, setContextType] = useState('comprehensive');
  const [workflowFocus, setWorkflowFocus] = useState('daily');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [promptTemplates, setPromptTemplates] = useState({});
  const [activeCategory, setActiveCategory] = useState('daily_monitoring');
  const [dailyPriorities, setDailyPriorities] = useState(null);
  const [workflowSuggestions, setWorkflowSuggestions] = useState([]);
  const [error, setError] = useState(null);

  // Load data on component mount
  useEffect(() => {
    loadPromptTemplates();
    loadDailyPriorities();
    loadWorkflowSuggestions();
  }, []);

  const loadPromptTemplates = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/productivity/prompts`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setPromptTemplates(data.prompt_categories);
      }
    } catch (error) {
      console.error('Error loading prompt templates:', error);
      // Set fallback templates
      setPromptTemplates({
        daily_monitoring: [
          "What needs my immediate attention today?",
          "Show me yesterday's performance against targets",
          "Which customers should I reach out to today?"
        ],
        workflow_optimization: [
          "Show me my most time-consuming data analysis tasks",
          "What routine decisions could CustomerMindIQ make automatically?",
          "Create my personalized daily dashboard"
        ]
      });
    }
  };

  const loadDailyPriorities = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/productivity/daily-priorities`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setDailyPriorities(data.daily_priorities);
      }
    } catch (error) {
      console.error('Error loading daily priorities:', error);
    }
  };

  const loadWorkflowSuggestions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/productivity/workflow-suggestions`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setWorkflowSuggestions(data.workflow_suggestions);
      }
    } catch (error) {
      console.error('Error loading workflow suggestions:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!prompt.trim()) {
      setError('Please enter a productivity analysis prompt');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/productivity/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt.trim(),
          context_type: contextType,
          workflow_focus: workflowFocus
        })
      });

      const data = await response.json();

      if (response.ok) {
        setAnalysis(data);
      } else {
        throw new Error(data.detail || 'Analysis failed');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      setError(error.message || 'Failed to generate analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePromptSelect = (selectedPrompt) => {
    setPrompt(selectedPrompt);
  };

  const formatAnalysis = (analysisText) => {
    if (!analysisText) return '';
    
    const sections = analysisText.split('\n\n');
    return sections.map((section, index) => {
      const lines = section.split('\n');
      const title = lines[0];
      const content = lines.slice(1).join('\n');
      
      if (title.includes('Executive Summary') || title.includes('Immediate Actions') || title.includes('Opportunities')) {
        return (
          <div key={index} className="mb-4">
            <h4 className="font-semibold text-blue-300 mb-2">{title}</h4>
            <div className="text-gray-300 whitespace-pre-wrap">{content}</div>
          </div>
        );
      }
      
      return (
        <div key={index} className="mb-3 text-gray-300 whitespace-pre-wrap">
          {section}
        </div>
      );
    }).filter(Boolean);
  };

  const getCategoryIcon = (category) => {
    const icons = {
      getting_started: Settings,
      daily_monitoring: Calendar,
      weekly_analysis: BarChart3,
      monthly_strategic: TrendingUp,
      immediate_attention: AlertTriangle,
      workflow_optimization: Zap
    };
    
    const IconComponent = icons[category] || Lightbulb;
    return <IconComponent className="h-4 w-4" />;
  };

  const getCategoryColor = (category) => {
    const colors = {
      getting_started: 'bg-green-500/20 text-green-300 border-green-500/30',
      daily_monitoring: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
      weekly_analysis: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
      monthly_strategic: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
      immediate_attention: 'bg-red-500/20 text-red-300 border-red-500/30',
      workflow_optimization: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30'
    };
    
    return colors[category] || 'bg-gray-500/20 text-gray-300 border-gray-500/30';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      Critical: 'bg-red-500/20 text-red-300 border-red-500/50',
      High: 'bg-orange-500/20 text-orange-300 border-orange-500/50',
      Medium: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/50',
      Low: 'bg-green-500/20 text-green-300 border-green-500/50'
    };
    return colors[priority] || 'bg-gray-500/20 text-gray-300 border-gray-500/50';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gray-900/50 border-gray-700">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-yellow-500/20 rounded-lg">
              <Zap className="h-6 w-6 text-yellow-400" />
            </div>
            <div>
              <CardTitle className="text-xl text-white">Daily Productivity Intelligence</CardTitle>
              <CardDescription className="text-gray-400">
                Start your day with AI-powered insights combining customer analytics and website data
              </CardDescription>
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Main Analysis Panel */}
        <div className="xl:col-span-2 space-y-6">
          {/* Quick Daily Priorities */}
          {dailyPriorities && (
            <Card className="bg-gradient-to-r from-red-600/10 to-orange-600/10 border-red-500/30">
              <CardHeader>
                <CardTitle className="text-lg text-white flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-red-400" />
                  Today's Priority Items
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {dailyPriorities.urgent_attention?.critical_customers?.length > 0 && (
                    <div className="p-3 bg-red-500/10 rounded-lg border border-red-500/30">
                      <div className="flex items-center gap-2 mb-2">
                        <Users className="h-4 w-4 text-red-400" />
                        <span className="font-medium text-red-300">Critical Customers Need Attention</span>
                      </div>
                      <p className="text-gray-300 text-sm">
                        {dailyPriorities.urgent_attention.critical_customers.length} customers at high churn risk
                      </p>
                    </div>
                  )}
                  
                  {dailyPriorities.opportunities?.expansion_candidates?.length > 0 && (
                    <div className="p-3 bg-green-500/10 rounded-lg border border-green-500/30">
                      <div className="flex items-center gap-2 mb-2">
                        <DollarSign className="h-4 w-4 text-green-400" />
                        <span className="font-medium text-green-300">Expansion Opportunities</span>
                      </div>
                      <p className="text-gray-300 text-sm">
                        {dailyPriorities.opportunities.expansion_candidates.length} customers showing growth signals
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Prompt Input */}
          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <Target className="h-5 w-5 text-yellow-400" />
                Productivity Analysis Prompt
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Your Productivity Question</label>
                <Textarea
                  placeholder="Ask about daily priorities, workflow optimization, or strategic insights... (e.g., 'What should I focus on today to maximize impact?')"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-[100px] bg-gray-800 border-gray-600 text-white placeholder-gray-400"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-300">Data Context</label>
                  <Select value={contextType} onValueChange={setContextType}>
                    <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-600">
                      <SelectItem value="comprehensive">All Business Data</SelectItem>
                      <SelectItem value="priority_focus">Priority Items Only</SelectItem>
                      <SelectItem value="customer_data">Customer Data</SelectItem>
                      <SelectItem value="website_data">Website Data</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-300">Workflow Focus</label>
                  <Select value={workflowFocus} onValueChange={setWorkflowFocus}>
                    <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-600">
                      <SelectItem value="daily">Daily Tasks</SelectItem>
                      <SelectItem value="weekly">Weekly Planning</SelectItem>
                      <SelectItem value="monthly">Monthly Strategy</SelectItem>
                      <SelectItem value="immediate">Immediate Actions</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex justify-end">
                <Button 
                  onClick={handleAnalyze}
                  disabled={loading || !prompt.trim()}
                  className="bg-yellow-600 hover:bg-yellow-700"
                >
                  {loading ? (
                    <>
                      <Timer className="h-4 w-4 mr-2 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Zap className="h-4 w-4 mr-2" />
                      Get Insights
                    </>
                  )}
                </Button>
              </div>

              {error && (
                <Alert className="border-red-500/50 bg-red-500/10">
                  <AlertTriangle className="h-4 w-4 text-red-400" />
                  <AlertDescription className="text-red-300">
                    {error}
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Analysis Results */}
          {analysis && (
            <Card className="bg-gray-900/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-lg text-white flex items-center gap-2">
                  <Lightbulb className="h-5 w-5 text-yellow-400" />
                  Productivity Analysis Results
                  <Badge className={`ml-auto ${getPriorityColor(analysis.priority_level)}`}>
                    {analysis.priority_level} Priority
                  </Badge>
                </CardTitle>
                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <span>⏱️ {analysis.processing_time?.toFixed(2)}s</span>
                  <span>💾 {analysis.estimated_time_savings} potential savings</span>
                </div>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="analysis" className="w-full">
                  <TabsList className="grid w-full grid-cols-3 bg-gray-800">
                    <TabsTrigger value="analysis" className="text-gray-300">Analysis</TabsTrigger>
                    <TabsTrigger value="actions" className="text-gray-300">Action Items</TabsTrigger>
                    <TabsTrigger value="recommendations" className="text-gray-300">Recommendations</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="analysis" className="mt-4">
                    <div className="space-y-4 max-h-96 overflow-y-auto">
                      {formatAnalysis(analysis.analysis)}
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="actions" className="mt-4">
                    <div className="space-y-3">
                      {analysis.action_items?.length > 0 ? (
                        analysis.action_items.map((action, index) => (
                          <div key={index} className="flex items-start gap-3 p-3 bg-gray-800/50 rounded-lg">
                            <Target className="h-5 w-5 text-yellow-400 mt-0.5 flex-shrink-0" />
                            <div>
                              <p className="text-gray-300">{action}</p>
                              <Badge className="mt-2 bg-yellow-500/20 text-yellow-300 text-xs">
                                Action #{index + 1}
                              </Badge>
                            </div>
                          </div>
                        ))
                      ) : (
                        <p className="text-gray-400 italic">No specific action items extracted</p>
                      )}
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="recommendations" className="mt-4">
                    <div className="space-y-3">
                      {analysis.recommendations?.length > 0 ? (
                        analysis.recommendations.map((rec, index) => (
                          <div key={index} className="flex items-start gap-3 p-3 bg-gray-800/50 rounded-lg">
                            <CheckCircle className="h-5 w-5 text-green-400 mt-0.5 flex-shrink-0" />
                            <p className="text-gray-300">{rec}</p>
                          </div>
                        ))
                      ) : (
                        <p className="text-gray-400 italic">No specific recommendations extracted</p>
                      )}
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Workflow Suggestions */}
          {workflowSuggestions.length > 0 && (
            <Card className="bg-gray-900/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-lg text-white flex items-center gap-2">
                  <Settings className="h-5 w-5 text-blue-400" />
                  Quick Wins
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {workflowSuggestions.map((suggestion, index) => (
                    <div key={index} className="p-3 bg-gray-800/50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-white text-sm">{suggestion.category}</h4>
                        <Badge className={getPriorityColor(suggestion.priority)}>
                          {suggestion.priority}
                        </Badge>
                      </div>
                      <p className="text-gray-300 text-sm mb-2">{suggestion.suggestion}</p>
                      <div className="flex items-center gap-2 text-xs text-gray-400">
                        <Clock className="h-3 w-3" />
                        <span>Saves {suggestion.time_savings}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Prompt Templates */}
          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-purple-400" />
                Productivity Prompts
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Category Selection */}
                <div className="flex flex-wrap gap-2">
                  {Object.keys(promptTemplates).map((category) => (
                    <Badge
                      key={category}
                      variant={activeCategory === category ? "default" : "outline"}
                      className={`cursor-pointer transition-colors text-xs ${
                        activeCategory === category 
                          ? getCategoryColor(category)
                          : 'border-gray-600 text-gray-400 hover:text-gray-300'
                      }`}
                      onClick={() => setActiveCategory(category)}
                    >
                      {getCategoryIcon(category)}
                      <span className="ml-1 capitalize">
                        {category.replace('_', ' ')}
                      </span>
                    </Badge>
                  ))}
                </div>

                {/* Prompts List */}
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {promptTemplates[activeCategory]?.map((promptText, index) => (
                    <div
                      key={index}
                      className="p-3 bg-gray-800/50 rounded-lg cursor-pointer hover:bg-gray-800 transition-colors group"
                      onClick={() => handlePromptSelect(promptText)}
                    >
                      <p className="text-sm text-gray-300 group-hover:text-white">
                        {promptText}
                      </p>
                      <ArrowRight className="h-4 w-4 text-gray-500 group-hover:text-yellow-400 mt-1 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ProductivityIntelligence;