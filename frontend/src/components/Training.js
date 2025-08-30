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
  Zap
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
      filename: "CustomerMind_IQ_Complete_Training_Manual.pdf",
      size: "320KB",
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
      filename: "CustomerMind_IQ_Admin_Training_Manual.pdf", 
      size: "270KB",
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
      filename: "CustomerMind_IQ_Quick_Reference_Guide.pdf",
      size: "180KB",
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
                            Download {manual.size ? `PDF (${manual.size})` : 'Guide'}
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