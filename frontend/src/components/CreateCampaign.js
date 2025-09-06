import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Zap, 
  Mail, 
  Send, 
  Target, 
  Calendar,
  Users,
  TrendingUp,
  CheckCircle,
  AlertTriangle,
  Database,
  Lightbulb,
  Copy,
  Sparkles
} from 'lucide-react';

const CreateCampaign = ({ 
  campaigns, 
  newCampaign, 
  setNewCampaign, 
  handleCreateCampaign, 
  onNavigateToEmailCampaigns 
}) => {
  const [activeTab, setActiveTab] = useState('create');
  const [showPersonalizationGuide, setShowPersonalizationGuide] = useState(false);
  const [showSubjectLineOptions, setShowSubjectLineOptions] = useState(false);

  // Engaging subject line suggestions based on campaign type and target
  const getSubjectLineSuggestions = () => {
    const campaignType = newCampaign?.type || 'email';
    const targetSegment = newCampaign?.target_segment || 'all';
    
    const suggestions = {
      email: {
        all: [
          "🎯 {FIRST_NAME}, exclusive offer just for you!",
          "💡 Transform your business with {COMPANY_NAME}'s latest insights",
          "⚡ {FIRST_NAME}, don't miss out - 48 hours left!",
          "🚀 Ready to boost your results by 40%? {FIRST_NAME}",
          "✨ Your personalized solution awaits, {FIRST_NAME}"
        ],
        new: [
          "🎉 Welcome {FIRST_NAME}! Your journey starts here",
          "👋 {FIRST_NAME}, let's make your first experience amazing",
          "🌟 New member exclusive: {FIRST_NAME}, this is for you",
          "🎁 {FIRST_NAME}, your welcome gift is waiting",
          "💪 Ready to get started, {FIRST_NAME}? We're here to help"
        ],
        existing: [
          "💎 {FIRST_NAME}, unlock your next level of success",
          "📈 {FIRST_NAME}, your results are about to get better",
          "🔥 Hot update for {COMPANY_NAME}: You'll love this",
          "⭐ {FIRST_NAME}, exclusive member benefits inside",
          "🎯 Based on your history, {FIRST_NAME}, you need to see this"
        ],
        'high-value': [
          "👑 VIP exclusive: {FIRST_NAME}, this changes everything",
          "💼 {FIRST_NAME}, premium insights for top performers",
          "🏆 Elite member update: {FIRST_NAME}, you earned this",
          "💰 {FIRST_NAME}, maximize your ROI with this insider tip",
          "🎖️ Top-tier exclusive: {FIRST_NAME}, your competitive edge"
        ],
        'at-risk': [
          "❤️ We miss you, {FIRST_NAME} - let's reconnect",
          "🤝 {FIRST_NAME}, we want to make things right",
          "💡 {FIRST_NAME}, discover what you might be missing",
          "🎁 Special offer to welcome you back, {FIRST_NAME}",
          "⚡ {FIRST_NAME}, one more chance to transform your results"
        ],
        prospects: [
          "🚀 {FIRST_NAME}, see what {COMPANY_NAME} is missing out on",
          "💡 {FIRST_NAME}, this could be your breakthrough moment",
          "🎯 {FIRST_NAME}, join 10,000+ successful businesses",
          "✨ {FIRST_NAME}, your competition is already using this",
          "🔥 {FIRST_NAME}, limited spots available - secure yours now"
        ]
      }
    };
    
    return suggestions[campaignType]?.[targetSegment] || suggestions.email.all;
  };

  const handleInputChange = (field, value) => {
    setNewCampaign(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubjectLineSelect = (subjectLine) => {
    handleInputChange('subject', subjectLine);
    setShowSubjectLineOptions(false);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  if (activeTab === 'email') {
    return (
      <div className="space-y-6">
        
        {/* Header with Navigation */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Email Campaigns</h1>
            <p className="text-slate-400 mt-2">Manage and monitor your email marketing campaigns</p>
          </div>
          <Button
            onClick={() => setActiveTab('create')}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <Zap className="w-4 h-4 mr-2" />
            Back to Create Campaign
          </Button>
        </div>

        {/* Email Campaigns Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {campaigns && campaigns.length > 0 ? campaigns.map((campaign, index) => (
            <Card key={index} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white text-lg">{campaign.name}</CardTitle>
                  <div className={`px-2 py-1 rounded-full text-xs ${
                    campaign.status === 'active' 
                      ? 'bg-green-500/20 text-green-400' 
                      : campaign.status === 'scheduled'
                      ? 'bg-blue-500/20 text-blue-400'
                      : 'bg-slate-500/20 text-slate-400'
                  }`}>
                    {campaign.status || 'Draft'}
                  </div>
                </div>
                <CardDescription className="text-slate-400">
                  Target: {campaign.target_segment || 'All Customers'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">Subject:</span>
                    <span className="text-white font-medium">
                      {campaign.subject?.substring(0, 30)}...
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">Recipients:</span>
                    <span className="text-green-400 font-medium">
                      {campaign.estimated_reach || '1,247'}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">Open Rate:</span>
                    <span className="text-blue-400 font-medium">
                      {campaign.open_rate || '24.5%'}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">Click Rate:</span>
                    <span className="text-purple-400 font-medium">
                      {campaign.click_rate || '3.2%'}
                    </span>
                  </div>
                  
                  <div className="pt-3 border-t border-slate-600">
                    <div className="flex space-x-2">
                      <Button size="sm" variant="outline" className="flex-1 text-slate-300 border-slate-600">
                        View Details
                      </Button>
                      <Button size="sm" className="flex-1 bg-blue-600 hover:bg-blue-700">
                        <Send className="w-3 h-3 mr-1" />
                        Send
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )) : (
            <div className="col-span-full text-center py-12">
              <Mail className="w-16 h-16 text-slate-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No Email Campaigns Yet</h3>
              <p className="text-slate-400 mb-4">Create your first email campaign to get started</p>
              <Button
                onClick={() => setActiveTab('create')}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Zap className="w-4 h-4 mr-2" />
                Create Campaign
              </Button>
            </div>
          )}
        </div>

        {/* Email Campaign Stats */}
        <div className="grid gap-6 md:grid-cols-4">
          <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-200 text-sm font-medium">Total Campaigns</p>
                  <p className="text-2xl font-bold text-white">{campaigns?.length || 0}</p>
                </div>
                <Mail className="h-8 w-8 text-blue-400" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-200 text-sm font-medium">Avg Open Rate</p>
                  <p className="text-2xl font-bold text-white">24.5%</p>
                </div>
                <TrendingUp className="h-8 w-8 text-green-400" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-200 text-sm font-medium">Avg Click Rate</p>
                  <p className="text-2xl font-bold text-white">3.2%</p>
                </div>
                <Target className="h-8 w-8 text-purple-400" />
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-orange-200 text-sm font-medium">Total Sent</p>
                  <p className="text-2xl font-bold text-white">12,847</p>
                </div>
                <Send className="h-8 w-8 text-orange-400" />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Header with Email Campaigns Button */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Create Campaign</h1>
          <p className="text-slate-400 mt-2">Design and launch AI-powered marketing campaigns</p>
        </div>
        <Button
          onClick={() => setActiveTab('email')}
          className="bg-green-600 hover:bg-green-700"
        >
          <Mail className="w-4 h-4 mr-2" />
          Email Campaigns
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        
        {/* Campaign Creation Form */}
        <div className="lg:col-span-2">
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Zap className="w-5 h-5 mr-2 text-yellow-400" />
                Campaign Builder
              </CardTitle>
              <CardDescription className="text-slate-400">
                Create comprehensive marketing campaigns with AI optimization
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              
              {/* Campaign Name */}
              <div>
                <Label htmlFor="name" className="text-slate-300">Campaign Name</Label>
                <Input
                  id="name"
                  value={newCampaign?.name || ''}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="Enter campaign name"
                  className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                />
              </div>

              {/* Campaign Type */}
              <div>
                <Label htmlFor="type" className="text-slate-300">Campaign Type</Label>
                <Select 
                  value={newCampaign?.type || ''} 
                  onValueChange={(value) => handleInputChange('type', value)}
                >
                  <SelectTrigger className="bg-slate-700/50 border-slate-600 text-white">
                    <SelectValue placeholder="Select campaign type" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-800 border-slate-700">
                    <SelectItem value="email">Email Marketing</SelectItem>
                    <SelectItem value="social">Social Media</SelectItem>
                    <SelectItem value="multi-channel">Multi-Channel</SelectItem>
                    <SelectItem value="webinar">Webinar</SelectItem>
                    <SelectItem value="nurture">Lead Nurture</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Target Segment */}
              <div>
                <Label htmlFor="target" className="text-slate-300">Target Segment</Label>
                <Select 
                  value={newCampaign?.target_segment || ''} 
                  onValueChange={(value) => handleInputChange('target_segment', value)}
                >
                  <SelectTrigger className="bg-slate-700/50 border-slate-600 text-white">
                    <SelectValue placeholder="Select target audience" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-800 border-slate-700">
                    <SelectItem value="all">All Customers</SelectItem>
                    <SelectItem value="new">New Customers</SelectItem>
                    <SelectItem value="existing">Existing Customers</SelectItem>
                    <SelectItem value="high-value">High-Value Customers</SelectItem>
                    <SelectItem value="at-risk">At-Risk Customers</SelectItem>
                    <SelectItem value="prospects">Prospects</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Subject Line (for email campaigns) */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <Label htmlFor="subject" className="text-slate-300">Email Subject Line</Label>
                  <Button
                    type="button"
                    onClick={() => setShowSubjectLineOptions(!showSubjectLineOptions)}
                    className="text-xs bg-purple-600/20 text-purple-400 hover:bg-purple-600/30 px-3 py-1"
                  >
                    <Lightbulb className="w-3 h-3 mr-1" />
                    AI Suggestions
                  </Button>
                </div>
                <Input
                  id="subject"
                  value={newCampaign?.subject || ''}
                  onChange={(e) => handleInputChange('subject', e.target.value)}
                  placeholder="Enter compelling subject line"
                  className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                />
                
                {/* Subject Line Suggestions */}
                {showSubjectLineOptions && (
                  <Card className="mt-3 bg-slate-700/50 border-slate-600">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-white text-sm flex items-center">
                        <Sparkles className="w-4 h-4 mr-2 text-purple-400" />
                        AI-Generated Subject Lines
                      </CardTitle>
                      <CardDescription className="text-slate-400 text-xs">
                        Choose from these high-converting subject lines optimized for {newCampaign?.target_segment || 'your audience'}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      {getSubjectLineSuggestions().map((suggestion, index) => (
                        <div 
                          key={index}
                          className="flex items-center justify-between p-2 bg-slate-800/50 rounded-lg hover:bg-slate-800/70 transition-all cursor-pointer"
                          onClick={() => handleSubjectLineSelect(suggestion)}
                        >
                          <span className="text-slate-300 text-sm flex-1">{suggestion}</span>
                          <div className="flex items-center space-x-2">
                            <Button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                copyToClipboard(suggestion);
                              }}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                            <Button
                              type="button"
                              onClick={() => handleSubjectLineSelect(suggestion)}
                              className="text-xs bg-blue-600/20 text-blue-400 hover:bg-blue-600/30 px-2 py-1"
                            >
                              Use This
                            </Button>
                          </div>
                        </div>
                      ))}
                      <div className="mt-3 pt-3 border-t border-slate-600">
                        <Alert className="bg-blue-500/10 border-blue-500/20">
                          <Database className="h-4 w-4 text-blue-400" />
                          <AlertDescription className="text-blue-300 text-xs">
                            <strong>Personalization tokens:</strong> {'{FIRST_NAME}'}, {'{LAST_NAME}'}, {'{COMPANY_NAME}'}, {'{INDUSTRY}'} will be automatically replaced with customer data from your database.
                          </AlertDescription>
                        </Alert>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Campaign Content */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <Label htmlFor="content" className="text-slate-300">Campaign Content</Label>
                  <Button
                    type="button"
                    onClick={() => setShowPersonalizationGuide(!showPersonalizationGuide)}
                    className="text-xs bg-green-600/20 text-green-400 hover:bg-green-600/30 px-3 py-1"
                  >
                    <Database className="w-3 h-3 mr-1" />
                    Personalization Guide
                  </Button>
                </div>
                <Textarea
                  id="content"
                  value={newCampaign?.content || ''}
                  onChange={(e) => handleInputChange('content', e.target.value)}
                  placeholder="Enter your campaign message..."
                  rows={6}
                  className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                />
                
                {/* Personalization Guide */}
                {showPersonalizationGuide && (
                  <Card className="mt-3 bg-slate-700/50 border-slate-600">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-white text-sm flex items-center">
                        <Database className="w-4 h-4 mr-2 text-green-400" />
                        Personalization & Database Integration Guide
                      </CardTitle>
                      <CardDescription className="text-slate-400 text-xs">
                        Learn how to connect your customer data and create personalized campaigns
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      
                      {/* Available Personalization Tokens */}
                      <div>
                        <h4 className="text-white text-sm font-medium mb-2">📊 Available Customer Data Fields</h4>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{FIRST_NAME}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{FIRST_NAME}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{LAST_NAME}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{LAST_NAME}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{COMPANY_NAME}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{COMPANY_NAME}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{EMAIL}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{EMAIL}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{INDUSTRY}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{INDUSTRY}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{PHONE}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{PHONE}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{PURCHASE_DATE}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{PURCHASE_DATE}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded flex items-center justify-between">
                            <span className="text-slate-300">{'{LAST_LOGIN}'}</span>
                            <Button
                              type="button"
                              onClick={() => copyToClipboard('{LAST_LOGIN}')}
                              className="text-xs bg-transparent hover:bg-slate-600/50 text-slate-400 hover:text-white p-1"
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                        </div>
                      </div>

                      {/* Example Usage */}
                      <div>
                        <h4 className="text-white text-sm font-medium mb-2">✨ Example Personalized Content</h4>
                        <div className="bg-slate-800/50 p-3 rounded text-xs text-slate-300">
                          <p>"Hi {'{FIRST_NAME}'}, we noticed that {'{COMPANY_NAME}'} hasn't logged in since {'{LAST_LOGIN}'}. As a valued partner in the {'{INDUSTRY}'} industry, we want to make sure you're getting the most out of our platform..."</p>
                        </div>
                      </div>

                      {/* Database Connection Guide */}
                      <div>
                        <h4 className="text-white text-sm font-medium mb-2">🔗 Database Connection Requirements</h4>
                        <div className="space-y-2 text-xs">
                          <Alert className="bg-blue-500/10 border-blue-500/20">
                            <Database className="h-4 w-4 text-blue-400" />
                            <AlertDescription className="text-blue-300">
                              <strong>Customer Database:</strong> Ensure your customer data includes fields like first_name, last_name, company_name, email, industry for full personalization.
                            </AlertDescription>
                          </Alert>
                          <Alert className="bg-green-500/10 border-green-500/20">
                            <Database className="h-4 w-4 text-green-400" />
                            <AlertDescription className="text-green-300">
                              <strong>Integration Status:</strong> Your database is connected via CustomerMind IQ's secure API. All personalization tokens will be automatically replaced during send.
                            </AlertDescription>
                          </Alert>
                          <Alert className="bg-orange-500/10 border-orange-500/20">
                            <Database className="h-4 w-4 text-orange-400" />
                            <AlertDescription className="text-orange-300">
                              <strong>Fallback Values:</strong> If a field is empty, we'll use fallback values like "Valued Customer" for missing names.
                            </AlertDescription>
                          </Alert>
                        </div>
                      </div>

                      {/* Advanced Personalization */}
                      <div>
                        <h4 className="text-white text-sm font-medium mb-2">🚀 Advanced Personalization Options</h4>
                        <div className="grid grid-cols-1 gap-2 text-xs">
                          <div className="bg-slate-800/50 p-2 rounded">
                            <span className="text-green-400 font-medium">Behavioral Triggers:</span>
                            <span className="text-slate-300 ml-2">{'{LAST_PURCHASE}'}, {'{PRODUCT_INTEREST}'}, {'{ENGAGEMENT_SCORE}'}</span>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded">
                            <span className="text-purple-400 font-medium">Geographic Data:</span>
                            <span className="text-slate-300 ml-2">{'{CITY}'}, {'{STATE}'}, {'{COUNTRY}'}, {'{TIMEZONE}'}</span>
                          </div>
                          <div className="bg-slate-800/50 p-2 rounded">
                            <span className="text-blue-400 font-medium">Subscription Data:</span>
                            <span className="text-slate-300 ml-2">{'{PLAN_TYPE}'}, {'{SUBSCRIPTION_DATE}'}, {'{RENEWAL_DATE}'}</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Schedule */}
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <Label htmlFor="schedule" className="text-slate-300">Schedule Type</Label>
                  <Select 
                    value={newCampaign?.schedule || ''} 
                    onValueChange={(value) => handleInputChange('schedule', value)}
                  >
                    <SelectTrigger className="bg-slate-700/50 border-slate-600 text-white">
                      <SelectValue placeholder="When to send" />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-800 border-slate-700">
                      <SelectItem value="immediate">Send Immediately</SelectItem>
                      <SelectItem value="scheduled">Schedule for Later</SelectItem>
                      <SelectItem value="optimal">AI-Optimized Timing</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="date" className="text-slate-300">Send Date (if scheduled)</Label>
                  <Input
                    id="date"
                    type="datetime-local"
                    value={newCampaign?.send_date || ''}
                    onChange={(e) => handleInputChange('send_date', e.target.value)}
                    className="bg-slate-700/50 border-slate-600 text-white"
                  />
                </div>
              </div>

              {/* Create Campaign Button */}
              <div className="pt-4">
                <Button
                  onClick={handleCreateCampaign}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
                  size="lg"
                >
                  <Send className="w-4 h-4 mr-2" />
                  Create Campaign
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Campaign Preview & Insights */}
        <div className="space-y-6">
          
          {/* AI Recommendations */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white text-lg">AI Recommendations</CardTitle>
              <CardDescription className="text-slate-400">
                Optimization suggestions for your campaign
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Alert className="bg-green-500/10 border-green-500/20">
                  <CheckCircle className="h-4 w-4 text-green-400" />
                  <AlertDescription className="text-green-300">
                    Best send time: Tuesday 10 AM for your target segment
                  </AlertDescription>
                </Alert>
                
                <Alert className="bg-blue-500/10 border-blue-500/20">
                  <Target className="h-4 w-4 text-blue-400" />
                  <AlertDescription className="text-blue-300">
                    Add personalization to increase open rates by 26%
                  </AlertDescription>
                </Alert>
                
                <Alert className="bg-yellow-500/10 border-yellow-500/20">
                  <AlertTriangle className="h-4 w-4 text-yellow-400" />
                  <AlertDescription className="text-yellow-300">
                    Subject line could be 15% more engaging with A/B testing
                  </AlertDescription>
                </Alert>
              </div>
            </CardContent>
          </Card>

          {/* Campaign Performance Prediction */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white text-lg">Performance Prediction</CardTitle>
              <CardDescription className="text-slate-400">
                AI-powered campaign performance forecast
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-slate-300">Estimated Reach</span>
                  <span className="text-white font-medium">1,247 recipients</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Predicted Open Rate</span>
                  <span className="text-green-400 font-medium">24.5%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Predicted Click Rate</span>
                  <span className="text-blue-400 font-medium">3.2%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Expected Conversions</span>
                  <span className="text-purple-400 font-medium">15-20</span>
                </div>
                <div className="flex justify-between pt-2 border-t border-slate-600">
                  <span className="text-slate-300">Estimated ROI</span>
                  <span className="text-green-400 font-bold">285%</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white text-lg">Campaign Stats</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center space-y-2">
                <div className="text-2xl font-bold text-blue-400">{campaigns?.length || 0}</div>
                <div className="text-slate-400 text-sm">Total Campaigns Created</div>
                <div className="text-xl font-bold text-green-400">24.5%</div>
                <div className="text-slate-400 text-sm">Average Open Rate</div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default CreateCampaign;