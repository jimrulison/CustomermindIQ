import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Brain, 
  Lightbulb, 
  TrendingUp, 
  BarChart3, 
  Users, 
  DollarSign,
  Target,
  Zap,
  Clock,
  BookOpen,
  ArrowRight,
  Sparkles,
  AlertCircle,
  CheckCircle
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const AIBusinessInsights = () => {
  // Component state
  const [prompt, setPrompt] = useState('');
  const [contextType, setContextType] = useState('customer_data');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [promptTemplates, setPromptTemplates] = useState({});
  const [activeCategory, setActiveCategory] = useState('customer_analysis');
  const [insightHistory, setInsightHistory] = useState([]);
  const [error, setError] = useState(null);

  // Load prompt templates on component mount
  useEffect(() => {
    loadPromptTemplates();
    loadInsightHistory();
  }, []);

  const loadPromptTemplates = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ai-insights/prompts`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setPromptTemplates(data.prompt_categories);
      }
    } catch (error) {
      console.error('Error loading prompt templates:', error);
      // Set fallback templates
      setPromptTemplates({
        customer_analysis: [
          "Analyze our customer churn patterns and suggest specific retention strategies",
          "What are the key characteristics of our most valuable customers?",
          "Identify customer segments with the highest growth potential"
        ],
        revenue_optimization: [
          "Analyze our revenue streams and identify optimization opportunities",
          "What pricing strategies would maximize our revenue?",
          "Identify seasonal revenue patterns and capitalize strategies"
        ],
        marketing_performance: [
          "Analyze marketing campaign performance and identify highest ROI channels",
          "What customer acquisition strategies are most effective?",
          "Identify content themes that drive the highest engagement"
        ]
      });
    }
  };

  const loadInsightHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ai-insights/history?limit=5`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setInsightHistory(data.insights);
      }
    } catch (error) {
      console.error('Error loading insight history:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!prompt.trim()) {
      setError('Please enter a business analysis prompt');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/ai-insights/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt.trim(),
          context_type: contextType,
          analysis_focus: activeCategory
        })
      });

      const data = await response.json();

      if (response.ok) {
        setAnalysis(data);
        // Save the insight automatically
        await saveInsight(data);
        // Refresh history
        loadInsightHistory();
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

  const saveInsight = async (insightData) => {
    try {
      await fetch(`${API_BASE_URL}/api/ai-insights/save-insight`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(insightData)
      });
    } catch (error) {
      console.error('Error saving insight:', error);
    }
  };

  const handlePromptSelect = (selectedPrompt) => {
    setPrompt(selectedPrompt);
  };

  const formatAnalysis = (analysisText) => {
    if (!analysisText) return '';
    
    // Split into sections and format
    const sections = analysisText.split('\n\n');
    return sections.map((section, index) => {
      const lines = section.split('\n');
      const title = lines[0];
      const content = lines.slice(1).join('\n');
      
      if (title.includes('Executive Summary') || title.includes('Key Findings') || title.includes('Recommendations')) {
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
      customer_analysis: Users,
      revenue_optimization: DollarSign,
      marketing_performance: Target,
      operational_insights: BarChart3,
      competitive_analysis: TrendingUp,
      growth_strategies: Zap
    };
    
    const IconComponent = icons[category] || Brain;
    return <IconComponent className="h-4 w-4" />;
  };

  const getCategoryColor = (category) => {
    const colors = {
      customer_analysis: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
      revenue_optimization: 'bg-green-500/20 text-green-300 border-green-500/30',
      marketing_performance: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
      operational_insights: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
      competitive_analysis: 'bg-red-500/20 text-red-300 border-red-500/30',
      growth_strategies: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30'
    };
    
    return colors[category] || 'bg-gray-500/20 text-gray-300 border-gray-500/30';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gray-900/50 border-gray-700">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <Brain className="h-6 w-6 text-blue-400" />
            </div>
            <div>
              <CardTitle className="text-xl text-white">AI Business Insights</CardTitle>
              <CardDescription className="text-gray-400">
                Get intelligent analysis of your business data with custom AI prompts
              </CardDescription>
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Main Analysis Panel */}
        <div className="xl:col-span-2 space-y-6">
          {/* Prompt Input */}
          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-blue-400" />
                Business Analysis Prompt
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Your Analysis Question</label>
                <Textarea
                  placeholder="Enter your business analysis question here... (e.g., 'Analyze our customer churn patterns and suggest retention strategies')"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-[100px] bg-gray-800 border-gray-600 text-white placeholder-gray-400"
                />
              </div>

              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="text-sm font-medium text-gray-300">Data Context</label>
                  <Select value={contextType} onValueChange={setContextType}>
                    <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-600">
                      <SelectItem value="customer_data">Customer Data</SelectItem>
                      <SelectItem value="revenue_data">Revenue Data</SelectItem>
                      <SelectItem value="marketing_data">Marketing Data</SelectItem>
                      <SelectItem value="comprehensive">All Data</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-end">
                  <Button 
                    onClick={handleAnalyze}
                    disabled={loading || !prompt.trim()}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {loading ? (
                      <>
                        <Clock className="h-4 w-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Brain className="h-4 w-4 mr-2" />
                        Analyze
                      </>
                    )}
                  </Button>
                </div>
              </div>

              {error && (
                <Alert className="border-red-500/50 bg-red-500/10">
                  <AlertCircle className="h-4 w-4 text-red-400" />
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
                  AI Analysis Results
                  <Badge className="ml-auto bg-green-500/20 text-green-300">
                    {analysis.processing_time?.toFixed(2)}s
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="analysis" className="w-full">
                  <TabsList className="grid w-full grid-cols-2 bg-gray-800">
                    <TabsTrigger value="analysis" className="text-gray-300">Analysis</TabsTrigger>
                    <TabsTrigger value="recommendations" className="text-gray-300">Recommendations</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="analysis" className="mt-4">
                    <div className="space-y-4 max-h-96 overflow-y-auto">
                      {formatAnalysis(analysis.analysis)}
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
          {/* Prompt Templates */}
          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-lg text-white flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-purple-400" />
                Prompt Templates
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
                      className={`cursor-pointer transition-colors ${
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
                      <ArrowRight className="h-4 w-4 text-gray-500 group-hover:text-blue-400 mt-1 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent Insights */}
          {insightHistory.length > 0 && (
            <Card className="bg-gray-900/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-lg text-white flex items-center gap-2">
                  <Clock className="h-5 w-5 text-green-400" />
                  Recent Insights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 max-h-64 overflow-y-auto">
                  {insightHistory.map((insight, index) => (
                    <div key={insight.insight_id || index} className="p-3 bg-gray-800/50 rounded-lg">
                      <p className="text-sm text-gray-300 mb-1">
                        {insight.prompt?.substring(0, 100)}...
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(insight.saved_at || insight.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIBusinessInsights;