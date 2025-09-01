import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Alert, AlertDescription } from './ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { 
  GraduationCap,
  Play,
  Book,
  Lightbulb,
  Clock,
  Users,
  Download,
  ExternalLink,
  CheckCircle,
  Star,
  Video,
  FileText,
  BookOpen,
  Target,
  TrendingUp,
  Globe,
  Search,
  BarChart3,
  Zap,
  AlertTriangle,
  Calculator,
  Award,
  Lock
} from 'lucide-react';

const Training = () => {
  const [activeTab, setActiveTab] = useState('videos');

  // State for video modal
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [showVideoModal, setShowVideoModal] = useState(false);

  // State for downloads
  const [downloading, setDownloading] = useState({});

  // PDF Download function
  const downloadPDF = async (pdfType, filename) => {
    try {
      setDownloading({ ...downloading, [pdfType]: true });
      console.log(`Downloading ${filename}...`);
      
      // Get backend URL from environment
      const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || window.location.origin;
      
      // Make API request
      const response = await fetch(`${API_BASE_URL}/api/download/${pdfType}`);
      
      if (!response.ok) {
        throw new Error(`Download failed: ${response.status} ${response.statusText}`);
      }
      
      // Get the PDF blob
      const blob = await response.blob();
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      console.log(`✅ Successfully downloaded: ${filename}`);
      
    } catch (error) {
      console.error('PDF Download Error:', error);
      alert(`Sorry, there was an error downloading the PDF. Please try again.\n\nError: ${error.message}`);
    } finally {
      setDownloading({ ...downloading, [pdfType]: false });
    }
  };

  // Video training content
  const videoContent = [
    {
      id: 1,
      title: "Getting Started with Website Intelligence Hub",
      description: "Complete overview of the platform and how to add your first website",
      duration: "8:45",
      difficulty: "Beginner",
      category: "Overview",
      thumbnail: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/getting_started.mp4", // You'll upload this
      topics: ["Platform Navigation", "Adding Websites", "Dashboard Overview", "Basic Setup"]
    },
    {
      id: 2,
      title: "Understanding Performance Metrics",
      description: "Deep dive into Core Web Vitals and performance optimization",
      duration: "12:30",
      difficulty: "Intermediate",
      category: "Performance",
      thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/performance_metrics.mp4", // You'll upload this
      topics: ["Core Web Vitals", "Load Times", "Performance Scoring", "Optimization Tips"]
    },
    {
      id: 3,
      title: "SEO Intelligence Mastery",
      description: "Maximize your search engine optimization with our SEO tools",
      duration: "15:22",
      difficulty: "Advanced",
      category: "SEO",
      thumbnail: "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/seo_mastery.mp4", // You'll upload this
      topics: ["Keyword Research", "Technical SEO", "Content Optimization", "Competitor Analysis"]
    },
    {
      id: 4,
      title: "Multi-Website Management",
      description: "Best practices for managing multiple websites and client accounts",
      duration: "10:15",
      difficulty: "Intermediate",
      category: "Management",
      thumbnail: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/multi_website_management.mp4", // You'll upload this
      topics: ["Website Organization", "Bulk Operations", "Client Reporting", "Workflow Optimization"]
    },
    {
      id: 5,
      title: "Membership Tiers & Scaling",
      description: "Understanding plans, limits, and when to upgrade your membership",
      duration: "6:30",
      difficulty: "Beginner",
      category: "Account",
      thumbnail: "https://images.unsplash.com/photo-1553028826-f4804151e0b2?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/membership_scaling.mp4", // You'll upload this
      topics: ["Plan Comparison", "Upgrade Benefits", "Usage Tracking", "ROI Calculation"]
    },
    {
      id: 6,
      title: "Advanced Analytics & Reporting",
      description: "Create professional reports and track ROI from your optimizations",
      duration: "18:45",
      difficulty: "Advanced",
      category: "Analytics",
      thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/advanced_analytics.mp4", // You'll upload this
      topics: ["Custom Reports", "ROI Tracking", "Client Dashboards", "Performance Trends"]
    }
  ];

  // Manual/Documentation content
  const manualSections = [
    {
      id: 1,
      title: "Quick Start Guide",
      description: "Get up and running with CustomerMind IQ in under 30 minutes - complete setup and navigation",
      icon: BookOpen,
      pages: 7,
      lastUpdated: "January 2025",
      downloadUrl: "/api/download/quick-start-guide",
      pdfType: "quick-start-guide",
      filename: "CustomerMind_IQ_Quick_Start_Guide.html",
      size: "HTML",
      sections: [
        "Authentication & Login Setup",
        "7-Day Free Trial Registration", 
        "Subscription Plans & Pricing Overview",
        "Dashboard Navigation & Basic Features",
        "Essential Features Walkthrough & First Steps"
      ]
    },
    {
      id: 2,
      title: "Complete Training Manual",
      description: "Comprehensive guide covering all 14 AI modules and advanced platform capabilities",
      icon: GraduationCap,
      pages: 42,
      lastUpdated: "January 2025",
      downloadUrl: "/api/download/complete-training-manual",
      pdfType: "complete-training-manual", 
      filename: "CustomerMind_IQ_Complete_Training_Manual.html",
      size: "HTML",
      sections: [
        "Authentication & Security Systems",
        "Customer Analytics & Intelligence Modules", 
        "Website Analytics & Performance Monitoring",
        "Marketing Automation & Revenue Analytics",
        "Data Integrations & Best Practices",
        "Troubleshooting Guide & Advanced Features"
      ]
    },
    {
      id: 3,
      title: "Admin Training Manual", 
      description: "Advanced administrative features, user management, and platform administration guide",
      icon: Target,
      pages: 28,
      lastUpdated: "January 2025",
      downloadUrl: "/api/download/admin-training-manual",
      pdfType: "admin-training-manual",
      filename: "CustomerMind_IQ_Admin_Training_Manual.html", 
      size: "HTML",
      sections: [
        "Banner & Announcement Management",
        "Discount & Promotion System Administration",
        "User Account Impersonation & Support Tools",
        "Analytics Dashboard & Reporting Features",
        "Security & Compliance Management",
        "Support & Escalation Procedures"
      ]
    },
    {
      id: 4,
      title: "Professional Quick Reference Guide",
      description: "Essential daily operations reference for power users and optimization professionals",
      icon: FileText,
      pages: 10,
      lastUpdated: "January 2025",
      downloadUrl: "/api/download/quick-reference-guide",
      pdfType: "quick-reference-guide",
      filename: "CustomerMind_IQ_Quick_Reference_Guide.html",
      size: "HTML",
      sections: [
        "Navigation Reference & Platform Architecture",
        "Performance Metrics Glossary & Scoring Framework",
        "SEO Optimization Checklist & Best Practices", 
        "Troubleshooting Guide & Problem Resolution",
        "Advanced Power User Techniques & Shortcuts",
        "Support & Contact Information"
      ]
    },
    {
      id: 5,
      title: "API Documentation",
      description: "Technical documentation for developers and integrations",
      icon: ExternalLink,
      pages: 23,
      lastUpdated: "December 2024",
      downloadUrl: "#",
      sections: [
        "Authentication & Setup",
        "Endpoint Reference & Examples",
        "Webhook Configuration",
        "Rate Limits & Best Practices",
        "SDK Documentation"
      ]
    }
  ];

  // Educational content
  const educationalContent = [
    {
      id: 1,
      category: "Performance Optimization",
      title: "Understanding Core Web Vitals",
      description: "Learn why Google's Core Web Vitals matter for your business and how to optimize them",
      icon: Zap,
      readTime: "5 min read",
      difficulty: "Beginner",
      keyPoints: [
        "LCP (Largest Contentful Paint) - Load performance indicator",
        "FID (First Input Delay) - Interactivity measurement", 
        "CLS (Cumulative Layout Shift) - Visual stability metric",
        "How Core Web Vitals affect search rankings",
        "Quick wins for improving each metric"
      ]
    },
    {
      id: 2,
      category: "SEO Strategy",
      title: "Technical SEO Fundamentals", 
      description: "Master the technical aspects of SEO that drive organic traffic growth",
      icon: Search,
      readTime: "8 min read",
      difficulty: "Intermediate",
      keyPoints: [
        "Site structure and URL optimization",
        "Meta tags and structured data implementation",
        "XML sitemaps and robots.txt configuration",
        "Page speed optimization for SEO",
        "Mobile-first indexing considerations"
      ]
    },
    {
      id: 3,
      category: "Business Intelligence",
      title: "ROI Measurement for Website Optimization",
      description: "Calculate and demonstrate the business value of website improvements",
      icon: TrendingUp,
      readTime: "6 min read", 
      difficulty: "Advanced",
      keyPoints: [
        "Setting up conversion tracking",
        "Measuring traffic quality improvements",
        "Calculating cost savings from optimization",
        "Building business cases for optimization projects",
        "Reporting ROI to stakeholders"
      ]
    },
    {
      id: 4,
      category: "Analytics",
      title: "Reading Website Health Scores",
      description: "Interpret health scores and prioritize optimization efforts effectively",
      icon: BarChart3,
      readTime: "4 min read",
      difficulty: "Beginner", 
      keyPoints: [
        "How health scores are calculated",
        "Understanding score components and weighting",
        "Prioritizing fixes by impact vs. effort",
        "Tracking improvement over time",
        "Benchmarking against industry standards"
      ]
    },
    {
      id: 5,
      category: "Competitive Analysis",
      title: "Benchmarking Against Competitors",
      description: "Use competitive intelligence to identify opportunities and threats",
      icon: Target,
      readTime: "7 min read",
      difficulty: "Intermediate",
      keyPoints: [
        "Identifying relevant competitors",
        "Comparing performance metrics",
        "Finding content and keyword opportunities", 
        "Analyzing competitor strengths and weaknesses",
        "Developing competitive advantage strategies"
      ]
    },
    {
      id: 6,
      category: "Scaling",
      title: "Managing Multiple Websites Efficiently",
      description: "Best practices for agencies and businesses with multiple web properties",
      icon: Globe,
      readTime: "9 min read",
      difficulty: "Advanced",
      keyPoints: [
        "Organizing websites for efficient management",
        "Bulk operations and automated workflows",
        "Creating standardized reporting processes",
        "Scaling monitoring as your portfolio grows",
        "Client communication and expectation management"
      ]
    }
  ];

  const getDifficultyColor = (difficulty) => {
    switch(difficulty) {
      case 'Beginner': return 'bg-green-500/20 text-green-400';
      case 'Intermediate': return 'bg-yellow-500/20 text-yellow-400'; 
      case 'Advanced': return 'bg-red-500/20 text-red-400';
      default: return 'bg-gray-500/20 text-gray-400';
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Overview': 'bg-blue-500/20 text-blue-400',
      'Performance': 'bg-orange-500/20 text-orange-400',
      'SEO': 'bg-purple-500/20 text-purple-400',
      'Management': 'bg-green-500/20 text-green-400',
      'Account': 'bg-cyan-500/20 text-cyan-400',
      'Analytics': 'bg-pink-500/20 text-pink-400'
    };
    return colors[category] || 'bg-gray-500/20 text-gray-400';
  };

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <GraduationCap className="w-8 h-8 mr-3 text-green-400" />
            Training Center
          </h1>
          <p className="text-slate-400 mt-2">
            Master the Website Intelligence Hub with comprehensive training resources
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge className="bg-green-500/20 text-green-400">
            <Star className="w-4 h-4 mr-1" />
            All Access
          </Badge>
        </div>
      </div>

      {/* Training Progress Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">6</div>
                <div className="text-xs text-green-200">Video Tutorials</div>
              </div>
              <Video className="h-8 w-8 text-green-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">5</div>
                <div className="text-xs text-blue-200">Documentation Guides</div>
              </div>
              <BookOpen className="h-8 w-8 text-blue-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">6</div>
                <div className="text-xs text-purple-200">Educational Articles</div>
              </div>
              <Lightbulb className="h-8 w-8 text-purple-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">72</div>
                <div className="text-xs text-orange-200">Total Minutes</div>
              </div>
              <Clock className="h-8 w-8 text-orange-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-slate-800/50 p-1 h-auto">
          <TabsTrigger value="videos" className="flex items-center">
            <Play className="w-4 h-4 mr-2" />
            Videos
          </TabsTrigger>
          <TabsTrigger value="manual" className="flex items-center">
            <Book className="w-4 h-4 mr-2" />
            Manual
          </TabsTrigger>
          <TabsTrigger value="educational" className="flex items-center">
            <Lightbulb className="w-4 h-4 mr-2" />
            Educational
          </TabsTrigger>
          <TabsTrigger value="growth-engine" className="flex items-center">
            <Zap className="w-4 h-4 mr-2" />
            Growth Engine
          </TabsTrigger>
        </TabsList>

        {/* Videos Tab */}
        <TabsContent value="videos" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {videoContent.map((video) => (
              <Card key={video.id} className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:border-slate-600 transition-all group">
                <div className="relative">
                  <img 
                    src={video.thumbnail} 
                    alt={video.title}
                    className="w-full h-48 object-cover rounded-t-lg"
                  />
                  <div className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button 
                      className="bg-white/20 backdrop-blur-sm hover:bg-white/30 text-white border-white/20"
                      onClick={() => {
                        setSelectedVideo(video);
                        setShowVideoModal(true);
                      }}
                    >
                      <Play className="w-4 h-4 mr-2" />
                      Play Video
                    </Button>
                  </div>
                  <div className="absolute top-2 right-2">
                    <Badge className={getCategoryColor(video.category)}>
                      {video.category}
                    </Badge>
                  </div>
                  <div className="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
                    {video.duration}
                  </div>
                </div>
                
                <CardContent className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <CardTitle className="text-white text-lg line-clamp-2">{video.title}</CardTitle>
                  </div>
                  
                  <CardDescription className="text-slate-400 text-sm mb-3 line-clamp-2">
                    {video.description}
                  </CardDescription>
                  
                  <div className="flex items-center justify-between mb-3">
                    <Badge className={getDifficultyColor(video.difficulty)}>
                      {video.difficulty}
                    </Badge>
                    <div className="flex items-center text-xs text-slate-500">
                      <Clock className="w-3 h-3 mr-1" />
                      {video.duration}
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-xs font-medium text-slate-300">Topics Covered:</div>
                    <div className="flex flex-wrap gap-1">
                      {video.topics.map((topic, index) => (
                        <Badge key={index} variant="outline" className="text-xs text-slate-400 border-slate-600">
                          {topic}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Manual Tab */}
        <TabsContent value="manual" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {manualSections.map((manual) => {
              const Icon = manual.icon;
              return (
                <Card key={manual.id} className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:border-slate-600 transition-all">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <Icon className="w-6 h-6 text-blue-400 mr-3" />
                        <CardTitle className="text-white">{manual.title}</CardTitle>
                      </div>
                      <Badge className="bg-blue-500/20 text-blue-400">
                        {manual.pages} pages
                      </Badge>
                    </div>
                    <CardDescription className="text-slate-400">
                      {manual.description}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="space-y-4">
                      {/* Last Updated */}
                      <div className="flex items-center text-xs text-slate-500">
                        <Clock className="w-3 h-3 mr-1" />
                        Last updated: {manual.lastUpdated}
                      </div>
                      
                      {/* Sections List */}
                      <div>
                        <div className="text-sm font-medium text-slate-300 mb-2">Sections Include:</div>
                        <div className="space-y-1">
                          {manual.sections.map((section, index) => (
                            <div key={index} className="flex items-center text-sm text-slate-400">
                              <CheckCircle className="w-3 h-3 text-green-400 mr-2 flex-shrink-0" />
                              {section}
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      {/* Download Button */}
                      <Button 
                        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                        disabled={downloading[manual.pdfType]}
                        onClick={() => {
                          if (manual.pdfType && manual.filename) {
                            // Use our PDF download function
                            downloadPDF(manual.pdfType, manual.filename);
                          } else if (manual.downloadUrl.startsWith('/')) {
                            // Create download link for other files
                            const link = document.createElement('a');
                            link.href = manual.downloadUrl;
                            link.download = manual.title.replace(/\s+/g, '_') + '.md';
                            link.target = '_blank';
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                          } else {
                            // For placeholder links
                            alert('This manual will be available for download soon!');
                          }
                        }}
                      >
                        {downloading[manual.pdfType] ? (
                          <>
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Downloading...
                          </>
                        ) : (
                          <>
                            <Download className="w-4 h-4 mr-2" />
                            Download {manual.size ? `Guide (${manual.size})` : 'Guide'}
                          </>
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Educational Tab */}
        <TabsContent value="educational" className="space-y-6">
          <div className="grid gap-6">
            {educationalContent.map((content) => {
              const Icon = content.icon;
              return (
                <Card key={content.id} className="bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:border-slate-600 transition-all">
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="bg-slate-700/50 p-3 rounded-lg">
                        <Icon className="w-6 h-6 text-blue-400" />
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <Badge className="bg-blue-500/20 text-blue-400 text-xs">
                            {content.category}
                          </Badge>
                          <div className="flex items-center space-x-2">
                            <Badge className={getDifficultyColor(content.difficulty)}>
                              {content.difficulty}
                            </Badge>
                            <div className="flex items-center text-xs text-slate-500">
                              <Clock className="w-3 h-3 mr-1" />
                              {content.readTime}
                            </div>
                          </div>
                        </div>
                        
                        <h3 className="text-xl font-semibold text-white mb-2">{content.title}</h3>
                        <p className="text-slate-400 mb-4">{content.description}</p>
                        
                        <div className="space-y-2">
                          <div className="text-sm font-medium text-slate-300">Key Learning Points:</div>
                          <div className="grid gap-2 md:grid-cols-2">
                            {content.keyPoints.map((point, index) => (
                              <div key={index} className="flex items-start text-sm text-slate-400">
                                <CheckCircle className="w-3 h-3 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                                {point}
                              </div>
                            ))}
                          </div>
                        </div>
                        
                        <div className="mt-4 pt-4 border-t border-slate-700">
                          <Button variant="outline" className="border-slate-600 text-slate-300 hover:bg-slate-700">
                            <BookOpen className="w-4 h-4 mr-2" />
                            Read Article
                          </Button>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Growth Acceleration Engine Tab */}
        <TabsContent value="growth-engine" className="space-y-6">
          <div className="grid gap-6">
            {/* Premium Feature Header with Logo */}
            <Card className="bg-gradient-to-r from-red-900/40 via-orange-900/40 to-yellow-900/40 backdrop-blur-xl border-red-500/50 relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500/10 to-yellow-500/10"></div>
              <CardHeader className="relative">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="p-4 bg-white/10 backdrop-blur-xl rounded-lg border border-white/20">
                      <img 
                        src="https://customer-assets.emergentagent.com/job_mongodb-fix-1/artifacts/qr1tdbbk_Customer%20Mind%20IQ%20logo.png" 
                        alt="CustomerMind IQ" 
                        className="w-12 h-12 object-contain"
                      />
                    </div>
                    <div>
                      <CardTitle className="text-3xl text-white mb-2">Growth Acceleration Engine</CardTitle>
                      <CardDescription className="text-xl text-orange-200 font-medium">
                        AI-Powered Growth Intelligence • Worth $249/month
                      </CardDescription>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="px-6 py-3 bg-red-600/80 backdrop-blur-xl rounded-lg border border-red-400/50 shadow-lg">
                      <div className="text-lg font-bold text-white">AVAILABLE ONLY TO</div>
                      <div className="text-xl font-black text-yellow-300">ANNUAL SUBSCRIBERS</div>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="relative space-y-6">
                <div className="grid md:grid-cols-2 gap-8">
                  <div className="space-y-4">
                    <h3 className="text-xl font-bold text-orange-300 flex items-center">
                      <Zap className="w-6 h-6 mr-2" />
                      What This Premium Module Does
                    </h3>
                    <p className="text-white text-lg leading-relaxed">
                      Transform your customer data into <strong>actionable growth strategies</strong>. Our AI continuously analyzes 
                      your business to identify the top growth opportunities, automatically test optimizations, 
                      detect revenue leaks, and track ROI for every initiative.
                    </p>
                    <div className="space-y-2">
                      <div className="flex items-center text-emerald-300">
                        <CheckCircle className="w-5 h-5 mr-2" />
                        <span>Identifies $10K-$50K+ monthly opportunities</span>
                      </div>
                      <div className="flex items-center text-emerald-300">
                        <CheckCircle className="w-5 h-5 mr-2" />
                        <span>Automates A/B testing and optimization</span>
                      </div>
                      <div className="flex items-center text-emerald-300">
                        <CheckCircle className="w-5 h-5 mr-2" />
                        <span>Finds hidden revenue leaks in your funnel</span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <h3 className="text-xl font-bold text-yellow-300 flex items-center">
                      <Award className="w-6 h-6 mr-2" />
                      Exclusive Annual Subscriber Value
                    </h3>
                    <div className="p-6 bg-gradient-to-br from-green-900/50 to-emerald-900/50 rounded-lg border border-green-400/30">
                      <div className="text-center space-y-3">
                        <div className="text-3xl font-black text-green-300">$249/month</div>
                        <div className="text-lg text-white font-semibold">Standalone Value</div>
                        <div className="text-2xl font-bold text-yellow-300">100% FREE</div>
                        <div className="text-white">for Annual Professional & Enterprise</div>
                      </div>
                    </div>
                    <div className="text-center">
                      <Badge className="bg-red-500/80 text-white text-lg px-4 py-2 font-bold">
                        🔒 PREMIUM FEATURE
                      </Badge>
                    </div>
                  </div>
                </div>
                
                {/* Upgrade CTA for Non-Annual Users */}
                <div className="p-6 bg-gradient-to-r from-blue-900/50 to-purple-900/50 rounded-lg border border-blue-400/30">
                  <div className="text-center space-y-4">
                    <h3 className="text-2xl font-bold text-white">🚀 Ready to Accelerate Your Growth?</h3>
                    <p className="text-blue-200 text-lg">
                      Upgrade to an Annual plan today and unlock the Growth Acceleration Engine 
                      plus save 20% on your subscription.
                    </p>
                    <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 px-8 text-lg">
                      Upgrade to Annual Plan →
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Core Features */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Growth Opportunity Scanner */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <Target className="w-6 h-6 text-emerald-400" />
                    <CardTitle className="text-emerald-400">Growth Opportunity Scanner</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-slate-300">
                    AI identifies your top 3 monthly growth opportunities ranked by revenue impact and 
                    implementation difficulty.
                  </p>
                  <div className="space-y-2">
                    <h4 className="font-semibold text-white">Key Features:</h4>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• Analyzes 50+ growth factors automatically</li>
                      <li>• Prioritizes by projected revenue impact</li>
                      <li>• Provides step-by-step action plans</li>
                      <li>• Shows confidence scores and timelines</li>
                      <li>• Covers acquisition, retention, and expansion</li>
                    </ul>
                  </div>
                  <div className="p-3 bg-emerald-500/10 rounded-lg border border-emerald-500/20">
                    <p className="text-xs text-emerald-300">
                      <strong>Example:</strong> "Increase email marketing spend on Segment A for $12,000 monthly impact"
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Automated A/B Testing */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <BarChart3 className="w-6 h-6 text-blue-400" />
                    <CardTitle className="text-blue-400">Automated A/B Testing</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-slate-300">
                    AI generates, runs, and analyzes A/B tests automatically. Set it and forget it growth optimization.
                  </p>
                  <div className="space-y-2">
                    <h4 className="font-semibold text-white">Automation Features:</h4>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• AI creates test variants automatically</li>
                      <li>• Statistical significance calculations</li>
                      <li>• Auto-deploys winning variants</li>
                      <li>• Continuous optimization cycles</li>
                      <li>• Landing pages, emails, pricing tests</li>
                    </ul>
                  </div>
                  <div className="p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
                    <p className="text-xs text-blue-300">
                      <strong>Result:</strong> Average 15-25% improvement in tested elements
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Revenue Leak Detection */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <AlertTriangle className="w-6 h-6 text-orange-400" />
                    <CardTitle className="text-orange-400">Revenue Leak Detection</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-slate-300">
                    Find hidden money in your sales funnel. Identifies exactly where you're losing potential revenue.
                  </p>
                  <div className="space-y-2">
                    <h4 className="font-semibold text-white">Leak Types Detected:</h4>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• Conversion funnel bottlenecks</li>
                      <li>• Customer onboarding dropoffs</li>
                      <li>• Retention and churn issues</li>
                      <li>• Pricing optimization gaps</li>
                      <li>• Feature adoption problems</li>
                    </ul>
                  </div>
                  <div className="p-3 bg-orange-500/10 rounded-lg border border-orange-500/20">
                    <p className="text-xs text-orange-300">
                      <strong>Impact:</strong> Average recovery of $30,000+ monthly revenue from top leaks
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* ROI Calculator */}
              <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <Calculator className="w-6 h-6 text-purple-400" />
                    <CardTitle className="text-purple-400">ROI Calculator & Tracking</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-slate-300">
                    Measure financial impact of every growth initiative with comprehensive ROI tracking and projections.
                  </p>
                  <div className="space-y-2">
                    <h4 className="font-semibold text-white">Financial Analytics:</h4>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• Projected vs actual performance tracking</li>
                      <li>• Payback period calculations</li>
                      <li>• 12-month and 24-month ROI projections</li>
                      <li>• Risk-adjusted return analysis</li>
                      <li>• Continuous prediction improvements</li>
                    </ul>
                  </div>
                  <div className="p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
                    <p className="text-xs text-purple-300">
                      <strong>Typical ROI:</strong> 300-600% return within 12 months
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* How to Use Section */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-xl text-white flex items-center">
                  <BookOpen className="w-6 h-6 mr-3 text-blue-400" />
                  How to Use the Growth Acceleration Engine
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 bg-emerald-500/20 rounded-full flex items-center justify-center">
                        <span className="text-emerald-400 font-bold">1</span>
                      </div>
                      <h3 className="font-semibold text-emerald-400">Access & Setup</h3>
                    </div>
                    <ul className="space-y-2 text-sm text-slate-300 ml-10">
                      <li>• Upgrade to Annual Professional or Enterprise plan</li>
                      <li>• Navigate to "Growth Acceleration Engine" in header</li>
                      <li>• Click "Full Growth Scan" to begin analysis</li>
                      <li>• Wait 5-15 minutes for AI to analyze your data</li>
                    </ul>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
                        <span className="text-blue-400 font-bold">2</span>
                      </div>
                      <h3 className="font-semibold text-blue-400">Review Opportunities</h3>
                    </div>
                    <ul className="space-y-2 text-sm text-slate-300 ml-10">
                      <li>• Review top 3 monthly growth opportunities</li>
                      <li>• Check projected revenue impact and confidence scores</li>
                      <li>• Read detailed action plans and timelines</li>
                      <li>• Prioritize by implementation difficulty vs impact</li>
                    </ul>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 bg-purple-500/20 rounded-full flex items-center justify-center">
                        <span className="text-purple-400 font-bold">3</span>
                      </div>
                      <h3 className="font-semibold text-purple-400">Implement & Track</h3>
                    </div>
                    <ul className="space-y-2 text-sm text-slate-300 ml-10">
                      <li>• Generate A/B tests for top opportunities</li>
                      <li>• Fix identified revenue leaks first</li>
                      <li>• Monitor ROI dashboard for results</li>
                      <li>• Run monthly scans for new opportunities</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Best Practices */}
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-xl text-white flex items-center">
                  <Award className="w-6 h-6 mr-3 text-yellow-400" />
                  Best Practices for Maximum Results
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <h3 className="font-semibold text-yellow-400">🎯 Getting Started Right</h3>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• Start with revenue leak fixes (quickest wins)</li>
                      <li>• Focus on "high impact, low effort" opportunities first</li>
                      <li>• Implement one opportunity fully before starting the next</li>
                      <li>• Allow 2-4 weeks to see measurable results</li>
                      <li>• Run new growth scans monthly for fresh insights</li>
                    </ul>
                  </div>
                  
                  <div className="space-y-3">
                    <h3 className="font-semibold text-yellow-400">📊 Maximizing ROI</h3>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• Trust the AI confidence scores - they improve over time</li>
                      <li>• Let A/B tests run to statistical significance</li>
                      <li>• Track actual vs projected results to teach the AI</li>
                      <li>• Use the 80/20 rule: focus on top opportunities</li>
                      <li>• Compound wins by reinvesting returns into new opportunities</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Success Story */}
            <Card className="bg-gradient-to-r from-green-900/20 to-emerald-900/20 backdrop-blur-xl border-green-500/30">
              <CardHeader>
                <CardTitle className="text-xl text-white flex items-center">
                  <TrendingUp className="w-6 h-6 mr-3 text-green-400" />
                  Real Success Story
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-green-500/10 rounded-lg">
                    <div className="text-2xl font-bold text-green-400">$55K</div>
                    <div className="text-sm text-slate-300">Additional MRR</div>
                  </div>
                  <div className="text-center p-4 bg-green-500/10 rounded-lg">
                    <div className="text-2xl font-bold text-green-400">34%</div>
                    <div className="text-sm text-slate-300">Revenue Growth</div>
                  </div>
                  <div className="text-center p-4 bg-green-500/10 rounded-lg">
                    <div className="text-2xl font-bold text-green-400">6</div>
                    <div className="text-sm text-slate-300">Months to Result</div>
                  </div>
                </div>
                <p className="text-slate-300 text-sm">
                  <strong>B2B SaaS Company ($2M ARR):</strong> Growth Engine identified three key opportunities: 
                  optimizing LinkedIn vs Google Ads (28% better conversion), launching at-risk customer retention 
                  sequences, and adding social proof to pricing pages. Result: $55K additional MRR within 6 months.
                </p>
              </CardContent>
            </Card>

            {/* Access Information */}
            <Card className="bg-yellow-900/20 backdrop-blur-xl border-yellow-500/30">
              <CardHeader>
                <CardTitle className="text-xl text-white flex items-center">
                  <Lock className="w-6 h-6 mr-3 text-yellow-400" />
                  Access Requirements
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <h3 className="font-semibold text-yellow-400">✅ Who Has Access</h3>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• Annual Professional plan subscribers</li>
                      <li>• Annual Enterprise plan subscribers</li>
                      <li>• All admin and super admin users</li>
                      <li>• 7-day free trial includes full access</li>
                    </ul>
                  </div>
                  
                  <div className="space-y-3">
                    <h3 className="font-semibold text-yellow-400">❌ Access Restrictions</h3>
                    <ul className="space-y-1 text-sm text-slate-300">
                      <li>• Monthly plan subscribers (upgrade required)</li>
                      <li>• Free tier users</li>
                      <li>• Starter plan subscribers</li>
                      <li>• Shows upgrade prompt with pricing details</li>
                    </ul>
                  </div>
                </div>
                <div className="p-4 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                  <p className="text-sm text-yellow-300">
                    <strong>💡 Tip:</strong> The Growth Acceleration Engine typically pays for itself within 2-4 months 
                    through identified opportunities. Annual plans also save 20% compared to monthly billing.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Video Player Modal */}
      <Dialog open={showVideoModal} onOpenChange={setShowVideoModal}>
        <DialogContent className="bg-slate-800 border-slate-700 max-w-4xl">
          <DialogHeader>
            <DialogTitle className="text-white flex items-center">
              <Play className="w-5 h-5 mr-2 text-green-400" />
              {selectedVideo?.title}
            </DialogTitle>
            <DialogDescription className="text-slate-400">
              {selectedVideo?.description}
            </DialogDescription>
          </DialogHeader>
          
          {selectedVideo && (
            <div className="space-y-4">
              {/* Video Player */}
              <div className="relative bg-slate-900 rounded-lg overflow-hidden">
                <video
                  width="100%"
                  height="400"
                  controls
                  className="w-full"
                  poster={selectedVideo.thumbnail}
                >
                  <source src={selectedVideo.videoUrl} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
              
              {/* Video Info */}
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <div className="flex items-center space-x-3">
                    <Badge className={getCategoryColor(selectedVideo.category)}>
                      {selectedVideo.category}
                    </Badge>
                    <Badge className={getDifficultyColor(selectedVideo.difficulty)}>
                      {selectedVideo.difficulty}
                    </Badge>
                    <div className="flex items-center text-xs text-slate-500">
                      <Clock className="w-3 h-3 mr-1" />
                      {selectedVideo.duration}
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-sm font-medium text-slate-300">Topics Covered:</div>
                    <div className="flex flex-wrap gap-1">
                      {selectedVideo.topics?.map((topic, index) => (
                        <Badge key={index} variant="outline" className="text-xs text-slate-400 border-slate-600">
                          {topic}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="text-sm font-medium text-slate-300">Video Actions:</div>
                  <div className="space-y-2">
                    <Button variant="outline" className="w-full border-slate-600 text-slate-300">
                      Download Video
                    </Button>
                    <Button variant="outline" className="w-full border-slate-600 text-slate-300">
                      Add to Favorites
                    </Button>
                    <Button variant="outline" className="w-full border-slate-600 text-slate-300">
                      Share Video
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Training;