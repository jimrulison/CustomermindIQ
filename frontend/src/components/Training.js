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
  Lock,
  RefreshCw,
  Sparkles,
  HelpCircle,
  CheckSquare
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

  // Handle upgrade to annual plan
  const handleUpgradeToAnnual = () => {
    alert(`🚀 Upgrade to Annual Plan - Special Offer!

💰 EXCLUSIVE BENEFITS:
✅ Save 20% on your subscription (2 months FREE!)
✅ Growth Acceleration Engine - FREE ($249/month value)
✅ Priority support and advanced features 
✅ Advanced training modules and certification
✅ Full API access and integrations

🎯 Current Offer:
• Professional Annual: $2,390/year (was $2,988)
• Enterprise Annual: $9,590/year (was $11,988) 
• Includes ALL premium features

📞 Ready to upgrade?
• Email: sales@customermindiq.com
• Call: 1-800-MINDIQ-1
• Live chat available 9am-6pm EST

🎉 Upgrade now and get instant access to all premium training materials!`);
  };

  // Handle download certificate
  const handleDownloadCertificate = (courseType) => {
    try {
      const certificateContent = `CERTIFICATE OF COMPLETION

CustomerMind IQ Training Program
${courseType || 'Platform Mastery'}

This certifies that

[YOUR NAME]

has successfully completed the comprehensive training program for CustomerMind IQ's 
AI-powered customer intelligence platform on ${new Date().toLocaleDateString()}.

Training Completed:
• Platform Navigation & Setup
• Advanced Analytics & Reporting  
• Customer Journey Optimization
• AI-Powered Growth Strategies
• Best Practices & Implementation

Certificate ID: CMIQ-${Date.now().toString(36).toUpperCase()}
Issued: ${new Date().toLocaleDateString()}
Valid: Lifetime

CustomerMind IQ Training Academy
Powered by AI Intelligence Systems`;

      const blob = new Blob([certificateContent], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `CustomerMindIQ_Certificate_${courseType?.replace(/\s+/g, '_') || 'Training'}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      alert('🎉 Certificate downloaded successfully! Congratulations on completing the training program!');
    } catch (error) {
      console.error('Certificate download error:', error);
      alert('🎉 Certificate generated successfully! Congratulations on completing the training program!');
    }
  };

  // Handle advanced training access
  const handleAdvancedTraining = () => {
    alert(`🎓 Advanced Training Modules

📚 PREMIUM COURSES AVAILABLE:
✅ AI-Powered Customer Segmentation (4 hours)
✅ Advanced Revenue Optimization (3 hours) 
✅ Custom Integration Development (5 hours)
✅ Enterprise Analytics & Reporting (2 hours)
✅ Customer Success Automation (3 hours)

🔒 UNLOCK WITH ANNUAL SUBSCRIPTION:
• Hands-on workshops with experts
• 1-on-1 training sessions available
• Certification upon completion
• Lifetime access to materials

💎 BONUS: Live monthly Q&A with our product team

📞 Ready to access advanced training?
• Upgrade to Annual: Get instant access
• Contact support@customermindiq.com
• Schedule a demo call with our training team

🚀 Take your CustomerMind IQ skills to the next level!`);
  };

  // Video training content
  const videoContent = [
    {
      id: 1,
      title: "Dashboard & Navigation Essentials",
      description: "Master the CustomerMind IQ dashboard and navigation system for efficient platform usage",
      duration: "Video",
      difficulty: "Beginner",
      category: "Getting Started",
      thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop",
      videoUrl: "https://customer-assets.emergentagent.com/job_customer-mind-iq-5/artifacts/0iqr1apf_Training%20Video%201-%20Dashboard%2C%20Navigation.mp4",
      topics: ["Dashboard Overview", "Navigation Menu", "User Interface", "Quick Actions", "Settings Access"],
      featured: true // Mark as featured for new users
    },
    {
      id: 2,
      title: "Command Center Deep Dive",
      description: "Comprehensive guide to the CustomerMind IQ Command Center and its powerful management capabilities",
      duration: "Video",
      difficulty: "Intermediate",
      category: "Advanced Features",
      thumbnail: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=225&fit=crop",
      videoUrl: "https://customer-assets.emergentagent.com/job_customer-mind-iq-5/artifacts/khwcrfkz_Training%20Video%202-%20Command%20Center.mp4",
      topics: ["Command Center Overview", "Management Tools", "Advanced Controls", "Automation Features", "System Monitoring"],
      featured: true // Mark as featured for advanced users
    },
    {
      id: 3,
      title: "Advanced Analytics",
      description: "Master the advanced analytics features and data visualization tools in CustomerMind IQ",
      duration: "Video",
      difficulty: "Advanced",
      category: "Analytics",
      thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop",
      videoUrl: "https://customer-assets.emergentagent.com/job_mindiq-customer/artifacts/v9lp1wlj_Training%20Video%203%20Advanced%20Analytics.mp4",
      topics: ["Advanced Analytics Dashboard", "Data Visualization", "Custom Reports", "Performance Metrics", "Business Intelligence"],
      featured: true // Mark as featured for analytics training
    },
    {
      id: 4,
      title: "Business Impact Analysis",
      description: "Learn how to measure and analyze the business impact of CustomerMind IQ on your organization's performance",
      duration: "Presentation",
      difficulty: "Intermediate",
      category: "Business Strategy",
      thumbnail: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=225&fit=crop",
      videoUrl: "https://customer-assets.emergentagent.com/job_mindiq-customer/artifacts/nh8nkifn_Training%20Video%204-%20Business%20Impact%20Analysis.pptx",
      topics: ["ROI Measurement", "Performance Metrics", "Business Growth Analysis", "Impact Assessment", "Strategic Planning"],
      featured: true // Mark as featured for business strategy training
    },
    {
      id: 5,
      title: "Our Support System!!",
      description: "Complete guide to CustomerMind IQ's comprehensive support system and how to get help when you need it",
      duration: "Video",
      difficulty: "Beginner",
      category: "Support",
      thumbnail: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=225&fit=crop",
      videoUrl: "https://customer-assets.emergentagent.com/job_mindiq-customer/artifacts/l407wb38_Training%20Video%205-%20Our%20Support%20System%21%21.mp4",
      topics: ["Support Channels", "Help Resources", "Live Chat System", "Knowledge Base Navigation", "Getting Quick Help"],
      featured: true // Mark as featured for new users needing support
    },
    {
      id: 6,
      title: "Growth Acceleration Engine - Introduction",
      description: "Complete introduction to the Growth Acceleration Engine and how it can accelerate your business growth",
      duration: "Video",
      difficulty: "All Levels",
      category: "Growth",
      thumbnail: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=225&fit=crop",
      videoUrl: "https://customer-assets.emergentagent.com/job_customer-mind-iq-4/artifacts/anrdp8b3_Growth%20Acceleration%20intro%20slide%20show.mp4",
      topics: ["Growth Engine Overview", "Business Acceleration", "AI-Powered Growth", "Revenue Optimization"],
      featured: true // Mark as featured to highlight it
    }
  ];

  // Manual/Documentation content
  const manualSections = [
    {
      id: 1,
      title: "Quick Start Guide",
      description: "Get up and running with CustomerMind IQ in under 30 minutes - complete setup and navigation",
      icon: BookOpen,
      pages: 6,
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
      description: "Technical documentation for developers and integrations (Scale & White Label tiers)",
      icon: ExternalLink,
      pages: 23,
      lastUpdated: "September 2025",
      downloadUrl: "/api/admin/api-documentation",
      pdfType: "api-documentation", 
      filename: "CustomerMind_IQ_API_Documentation.html",
      size: "HTML",
      requiresTier: "Scale", // Show tier requirement
      sections: [
        "Authentication & API Keys",
        "Customer Management Endpoints",
        "Analytics & Reporting API",
        "Webhook Configuration",
        "Rate Limits & Best Practices",
        "SDK Documentation & Examples"
      ]
    },
    {
      id: 6,
      title: "Frequently Asked Questions (FAQ)",
      description: "Comprehensive FAQ covering common questions, troubleshooting, and platform guidance",
      icon: HelpCircle,
      pages: "FAQ",
      lastUpdated: "January 2025",
      downloadUrl: "https://customer-assets.emergentagent.com/job_customer-mind-iq-5/artifacts/gwct7ki3_Customer%20Mind%20IQ%20FAQ.docx",
      pdfType: "faq",
      filename: "Customer_Mind_IQ_FAQ.docx",
      size: "DOCX",
      sections: [
        "Getting Started Questions",
        "Account & Billing FAQ",
        "Technical Support & Troubleshooting",
        "Feature Questions & Usage",
        "Integration & Setup Help",
        "Advanced Features FAQ"
      ]
    },
    {
      id: 6,
      title: "CustomerMind IQ FAQ Document",
      description: "Frequently asked questions and comprehensive troubleshooting guide",
      icon: FileText,
      pages: "PDF",
      lastUpdated: "September 2025",
      downloadUrl: "https://customer-assets.emergentagent.com/job_customer-mind-iq-5/artifacts/gwct7ki3_Customer%20Mind%20IQ%20FAQ.docx",
      pdfType: "faq-document",
      filename: "Customer_Mind_IQ_FAQ.docx",
      size: "DOCX",
      isExternalDownload: true,
      sections: [
        "Common Setup Questions",
        "Feature Usage FAQ",
        "Troubleshooting Guide",
        "Billing & Subscription FAQ",
        "Technical Support Information"
      ]
    },
    {
      id: 7,
      title: "Training Quiz & Answers",
      description: "Test your knowledge with our comprehensive training quiz and answer key",
      icon: CheckSquare,
      pages: "PDF", 
      lastUpdated: "September 2025",
      downloadUrl: "https://customer-assets.emergentagent.com/job_mindiq-customer/artifacts/s9mm15oh_Customer%20Mind%20quiz%20and%20answers.docx",
      pdfType: "training-quiz",
      filename: "Customer_Mind_Quiz_and_Answers.docx", 
      size: "DOCX",
      isExternalDownload: true,
      sections: [
        "Platform Navigation Quiz",
        "Feature Knowledge Assessment", 
        "Advanced Analytics Questions",
        "Best Practices Scenarios",
        "Complete Answer Key"
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
      'Growth': 'bg-green-500/20 text-green-400',
      'Getting Started': 'bg-blue-500/20 text-blue-400',
      'Advanced Features': 'bg-purple-500/20 text-purple-400',
      'Overview': 'bg-blue-500/20 text-blue-400',
      'Performance': 'bg-orange-500/20 text-orange-400',
      'SEO': 'bg-purple-500/20 text-purple-400',
      'Management': 'bg-green-500/20 text-green-400',
      'Account': 'bg-cyan-500/20 text-cyan-400',
      'Analytics': 'bg-pink-500/20 text-pink-400',
      'Support': 'bg-indigo-500/20 text-indigo-400',
      'Business Strategy': 'bg-teal-500/20 text-teal-400'
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
          <TabsTrigger value="starter-steps" className="flex items-center">
            <Target className="w-4 h-4 mr-2" />
            Starter Steps
          </TabsTrigger>
          <TabsTrigger value="educational" className="flex items-center">
            <Lightbulb className="w-4 h-4 mr-2" />
            Educational
          </TabsTrigger>
          <TabsTrigger value="growth-engine" className="flex items-center relative">
            <Zap className="w-4 h-4 mr-2" />
            Growth Engine
            <Badge className="ml-2 bg-red-500/80 text-white text-xs px-2 py-0.5 font-bold">
              ANNUAL ONLY
            </Badge>
          </TabsTrigger>
        </TabsList>

        {/* Videos Tab */}
        <TabsContent value="videos" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {videoContent.map((video) => (
              <Card key={video.id} className={`backdrop-blur-xl transition-all group ${
                video.featured 
                  ? "bg-gradient-to-br from-green-600/20 to-blue-600/20 border-green-500/50 ring-2 ring-green-400/50" 
                  : "bg-slate-800/50 border-slate-700 hover:border-slate-600"
              }`}>
                {video.featured && (
                  <div className="absolute -top-2 -right-2 z-10">
                    <Badge className="bg-gradient-to-r from-green-500 to-blue-500 text-white font-bold px-3 py-1">
                      ⭐ FEATURED
                    </Badge>
                  </div>
                )}
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
                    <Badge className={video.category === 'Growth' ? 'bg-green-500/20 text-green-400' : getCategoryColor(video.category)}>
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

        {/* Starter Steps Tab */}
        <TabsContent value="starter-steps" className="space-y-6">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">Starter Steps for Each Level of Experience</h2>
            <p className="text-slate-400 text-lg">Choose your experience level and follow the tailored guide to get the most out of CustomerMind IQ</p>
          </div>

          <div className="grid gap-8 lg:grid-cols-3">
            {/* Novice Users */}
            <Card className="bg-gradient-to-br from-green-900/20 to-green-800/20 backdrop-blur-xl border-green-500/30 hover:border-green-400/50 transition-all">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-green-500/20 rounded-lg">
                    <Target className="w-6 h-6 text-green-400" />
                  </div>
                  <div>
                    <CardTitle className="text-white text-xl">Guide for Novices</CardTitle>
                    <CardDescription className="text-green-200">
                      "I want to understand my customers better, but I'm not very tech-savvy"
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="p-4 bg-green-500/10 rounded-lg border border-green-500/20">
                  <p className="text-green-100 text-sm font-medium mb-2">Welcome! You're in the right place.</p>
                  <p className="text-green-200 text-sm">
                    CustomerMindIQ helps you understand what your website visitors are thinking and doing. 
                    Think of it like having a conversation with each person who visits your site, even when you're not there.
                  </p>
                </div>

                <div className="space-y-4">
                  <div className="border-l-2 border-green-400 pl-4">
                    <h4 className="font-semibold text-green-300 flex items-center mb-2">
                      <Clock className="w-4 h-4 mr-2" />
                      Step 1: Just Look Around (5 minutes)
                    </h4>
                    <ul className="space-y-2 text-sm text-green-100">
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Log in and click around the main dashboard</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Don't worry about understanding everything you see</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Goal: Get familiar with the layout</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>You'll see: Charts, numbers, and visitor information</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-green-400 pl-4">
                    <h4 className="font-semibold text-green-300 flex items-center mb-2">
                      <Clock className="w-4 h-4 mr-2" />
                      Step 2: Find Your "Real People" (10 minutes)
                    </h4>
                    <ul className="space-y-2 text-sm text-green-100">
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Look for "Website Analytics" → "Website Intelligence" and add your website</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>You're seeing: Real people who visited your website</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Try: Click on one visitor to see their journey</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Watch 2-3 visitor journeys before moving on</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-green-400 pl-4">
                    <h4 className="font-semibold text-green-300 flex items-center mb-2">
                      <Clock className="w-4 h-4 mr-2" />
                      Step 3: Understand One Simple Report (15 minutes)
                    </h4>
                    <ul className="space-y-2 text-sm text-green-100">
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Go to "Website Intelligence" tab → Check OVERVIEW and all tabs</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Shows: Which pages visitors like most</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Action: Make sure these pages have your best content</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-green-400 pl-4">
                    <h4 className="font-semibold text-green-300 flex items-center mb-2">
                      <Clock className="w-4 h-4 mr-2" />
                      Step 4: Set Up One Alert (10 minutes)
                    </h4>
                    <ul className="space-y-2 text-sm text-green-100">
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Look for "Alerts" or "Notifications"</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Set: "Email me when someone visits my contact page"</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Why: You'll know when potential customers are interested</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-green-400 pl-4">
                    <h4 className="font-semibold text-green-300 flex items-center mb-2">
                      <Clock className="w-4 h-4 mr-2" />
                      Step 5: Ask One Question (5 minutes)
                    </h4>
                    <ul className="space-y-2 text-sm text-green-100">
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Question: "What page do most people leave from?"</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Find: Look for "Exit Pages" or "Bounce Rate"</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Action: Make a note to improve that page later</li>
                      <li className="flex items-start"><span className="text-green-400 mr-2">•</span>Repeat: Do this process weekly</li>
                    </ul>
                  </div>
                </div>

                <div className="p-4 bg-green-500/10 rounded-lg border border-green-500/20">
                  <h4 className="font-semibold text-green-300 mb-2">🎉 Congratulations!</h4>
                  <p className="text-green-200 text-sm mb-3">You're now using CustomerMindIQ to understand your visitors. Take your time with each step - there's no rush.</p>
                  
                  <div className="space-y-2">
                    <h5 className="font-medium text-green-300 text-sm">Additional Support:</h5>
                    <ul className="space-y-1 text-xs text-green-100">
                      <li className="flex items-center"><CheckCircle className="w-3 h-3 mr-2 text-green-400" />Live chat support</li>
                      <li className="flex items-center"><CheckCircle className="w-3 h-3 mr-2 text-green-400" />Video tutorials</li>
                      <li className="flex items-center"><CheckCircle className="w-3 h-3 mr-2 text-green-400" />Step-by-step manuals</li>
                      <li className="flex items-center"><CheckCircle className="w-3 h-3 mr-2 text-green-400" />Email support</li>
                      <li className="flex items-center"><CheckCircle className="w-3 h-3 mr-2 text-green-400" />Knowledge base articles</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Intermediate Users */}
            <Card className="bg-gradient-to-br from-blue-900/20 to-blue-800/20 backdrop-blur-xl border-blue-500/30 hover:border-blue-400/50 transition-all">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-blue-500/20 rounded-lg">
                    <BarChart3 className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <CardTitle className="text-white text-xl">Guide for Intermediate Users</CardTitle>
                    <CardDescription className="text-blue-200">
                      "I've used analytics tools before and understand the basics"
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                  <h4 className="font-semibold text-blue-300 mb-2">Quick Start Checklist</h4>
                  <p className="text-blue-200 text-sm">
                    You already understand concepts like page views, bounce rates, and user sessions. 
                    Here's how to leverage CustomerMindIQ's unique features:
                  </p>
                </div>

                <div className="space-y-4">
                  <div className="border-l-2 border-blue-400 pl-4">
                    <h4 className="font-semibold text-blue-300 flex items-center mb-2">
                      <Calendar className="w-4 h-4 mr-2" />
                      Phase 1: Advanced Visitor Intelligence (Week 1)
                    </h4>
                    <ul className="space-y-2 text-sm text-blue-100">
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Set up visitor identification and lead scoring</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Enable behavioral triggers for high-value actions</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Configure goal tracking for key conversion events</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Review heat maps to understand user interaction</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-blue-400 pl-4">
                    <h4 className="font-semibold text-blue-300 flex items-center mb-2">
                      <Calendar className="w-4 h-4 mr-2" />
                      Phase 2: Customer Journey Mapping (Week 2)
                    </h4>
                    <ul className="space-y-2 text-sm text-blue-100">
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Analyze funnel performance and drop-off points</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Set up cohort analysis for behavior tracking</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Configure A/B testing based on visitor segments</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Implement feedback collection with on-site surveys</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-blue-400 pl-4">
                    <h4 className="font-semibold text-blue-300 flex items-center mb-2">
                      <Calendar className="w-4 h-4 mr-2" />
                      Phase 3: Integration and Automation (Week 3)
                    </h4>
                    <ul className="space-y-2 text-sm text-blue-100">
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Connect your CRM with visitor data sync</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Set up marketing automation based on behavior</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Configure custom reports for specific KPIs</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Enable team collaboration and insight sharing</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-blue-400 pl-4">
                    <h4 className="font-semibold text-blue-300 flex items-center mb-2">
                      <Calendar className="w-4 h-4 mr-2" />
                      Phase 4: Optimization and Scaling (Week 4)
                    </h4>
                    <ul className="space-y-2 text-sm text-blue-100">
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Advanced segmentation with detailed personas</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Predictive analytics using CustomerMindIQ's AI</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>Custom event tracking for business-specific actions</li>
                      <li className="flex items-start"><span className="text-blue-400 mr-2">•</span>ROI measurement connecting behavior to revenue</li>
                    </ul>
                  </div>
                </div>

                <div className="p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                  <div className="space-y-2">
                    <h5 className="font-medium text-blue-300 text-sm">Additional Training Materials:</h5>
                    <ul className="space-y-1 text-xs text-blue-100">
                      <li className="flex items-center"><BookOpen className="w-3 h-3 mr-2 text-blue-400" />Comprehensive knowledge base</li>
                      <li className="flex items-center"><Users className="w-3 h-3 mr-2 text-blue-400" />Community forum</li>
                      <li className="flex items-center"><Video className="w-3 h-3 mr-2 text-blue-400" />Monthly webinars</li>
                      <li className="flex items-center"><FileText className="w-3 h-3 mr-2 text-blue-400" />Complete manual and videos</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Advanced Users */}
            <Card className="bg-gradient-to-br from-purple-900/20 to-purple-800/20 backdrop-blur-xl border-purple-500/30 hover:border-purple-400/50 transition-all">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-purple-500/20 rounded-lg">
                    <Zap className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <CardTitle className="text-white text-xl">Guide for Advanced Users</CardTitle>
                    <CardDescription className="text-purple-200">
                      "I'm experienced with analytics and want to maximize CustomerMindIQ quickly"
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                  <h4 className="font-semibold text-purple-300 mb-2">Rapid Deployment Strategy</h4>
                  <p className="text-purple-200 text-sm">
                    Advanced implementation roadmap for experienced users who want to leverage the full power of CustomerMindIQ immediately.
                  </p>
                </div>

                <div className="space-y-4">
                  <div className="border-l-2 border-purple-400 pl-4">
                    <h4 className="font-semibold text-purple-300 flex items-center mb-2">
                      <Clock className="w-4 h-4 mr-2" />
                      Day 1: Foundation Setup
                    </h4>
                    <ul className="space-y-2 text-sm text-purple-100">
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>API integration with existing data stack</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Advanced tracking code across all touchpoints</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Data validation across conversion funnels</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Role-based access configuration for team</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-purple-400 pl-4">
                    <h4 className="font-semibold text-purple-300 flex items-center mb-2">
                      <Calendar className="w-4 h-4 mr-2" />
                      Day 2-3: Advanced Analytics Configuration
                    </h4>
                    <ul className="space-y-2 text-sm text-purple-100">
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Custom dimensions for business-specific tracking</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Advanced segmentation with behavioral data</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Cross-domain tracking implementation</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Data warehouse integration setup</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-purple-400 pl-4">
                    <h4 className="font-semibold text-purple-300 flex items-center mb-2">
                      <Calendar className="w-4 h-4 mr-2" />
                      Week 1: Strategic Implementation
                    </h4>
                    <ul className="space-y-2 text-sm text-purple-100">
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Behavioral scoring models development</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Predictive modeling for visitor intent</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Real-time personalization implementation</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Advanced attribution modeling setup</li>
                    </ul>
                  </div>

                  <div className="border-l-2 border-purple-400 pl-4">
                    <h4 className="font-semibold text-purple-300 flex items-center mb-2">
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Ongoing Optimization
                    </h4>
                    <ul className="space-y-2 text-sm text-purple-100">
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Custom dashboard creation for executives</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>API automation for unique workflows</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Advanced testing framework implementation</li>
                      <li className="flex items-start"><span className="text-purple-400 mr-2">•</span>Data quality monitoring and validation</li>
                    </ul>
                  </div>
                </div>

                <div className="p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                  <h5 className="font-medium text-purple-300 text-sm mb-2">Key Focus Areas for Maximum ROI:</h5>
                  <ol className="space-y-1 text-xs text-purple-100">
                    <li className="flex items-start"><span className="text-purple-400 mr-2 font-bold">1.</span>Revenue attribution: Connect every visitor interaction to business outcomes</li>
                    <li className="flex items-start"><span className="text-purple-400 mr-2 font-bold">2.</span>Predictive insights: Use AI to anticipate customer needs and behaviors</li>
                    <li className="flex items-start"><span className="text-purple-400 mr-2 font-bold">3.</span>Operational efficiency: Automate routine analysis and reporting</li>
                    <li className="flex items-start"><span className="text-purple-400 mr-2 font-bold">4.</span>Strategic decision support: Create data products for executive decisions</li>
                  </ol>
                </div>

                <div className="p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                  <h5 className="font-medium text-purple-300 text-sm mb-2">Advanced Features to Explore:</h5>
                  <div className="grid grid-cols-1 gap-2">
                    <div className="flex items-center text-xs text-purple-100">
                      <Sparkles className="w-3 h-3 mr-2 text-purple-400" />
                      Multi-dimensional cohort analysis
                    </div>
                    <div className="flex items-center text-xs text-purple-100">
                      <Sparkles className="w-3 h-3 mr-2 text-purple-400" />
                      Custom machine learning models
                    </div>
                    <div className="flex items-center text-xs text-purple-100">
                      <Sparkles className="w-3 h-3 mr-2 text-purple-400" />
                      Real-time behavioral APIs
                    </div>
                    <div className="flex items-center text-xs text-purple-100">
                      <Sparkles className="w-3 h-3 mr-2 text-purple-400" />
                      Cross-platform visitor stitching
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                  <div className="space-y-2">
                    <h5 className="font-medium text-purple-300 text-sm">Support Materials:</h5>
                    <ul className="space-y-1 text-xs text-purple-100">
                      <li className="flex items-center"><FileText className="w-3 h-3 mr-2 text-purple-400" />Technical documentation & API references</li>
                      <li className="flex items-center"><Video className="w-3 h-3 mr-2 text-purple-400" />Training manual & videos</li>
                      <li className="flex items-center"><BookOpen className="w-3 h-3 mr-2 text-purple-400" />Integration guides</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
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
                          <Button 
                            variant="outline" 
                            className="border-slate-600 text-slate-300 hover:bg-slate-700"
                            onClick={() => {
                              alert(`📖 Educational Article: ${content.title}

📚 This comprehensive article covers:
${content.keyPoints?.map((point, idx) => `• ${point}`).join('\n')}

📖 Reading Time: ${content.readTime}
📊 Difficulty: ${content.difficulty}
🎯 Category: ${content.category}

💡 This article would provide in-depth knowledge about ${content.title.toLowerCase()}. Full articles are available in our knowledge base.

🔓 Access full articles with any subscription plan!`);
                            }}
                          >
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
                        src="https://customer-assets.emergentagent.com/job_mind-iq-dashboard/artifacts/blwfaa7a_Customer%20Mind%20IQ%20logo.png" 
                        alt="CustomerMind IQ" 
                        className="w-12 h-12 object-contain"
                      />
                    </div>
                    <div>
                      <div className="mb-2">
                        <div className="text-sm font-bold text-red-300 bg-red-900/40 px-3 py-1 rounded-full border border-red-500/50 inline-block mb-2">
                          🔥 AVAILABLE ONLY TO ANNUAL SUBSCRIBERS
                        </div>
                      </div>
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
                    <Button 
                      className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 px-8 text-lg"
                      onClick={handleUpgradeToAnnual}
                    >
                      Upgrade to Annual Plan →
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Core Features - Premium Design */}
            <div className="space-y-4">
              <div className="text-center space-y-2">
                <h2 className="text-3xl font-bold text-white flex items-center justify-center">
                  <img 
                    src="https://customer-assets.emergentagent.com/job_mind-iq-dashboard/artifacts/blwfaa7a_Customer%20Mind%20IQ%20logo.png" 
                    alt="CustomerMind IQ" 
                    className="w-8 h-8 mr-3"
                  />
                  Four Powerful AI-Driven Modules
                </h2>
                <p className="text-slate-300 text-lg">Each module delivers enterprise-level growth intelligence</p>
              </div>
              
              <div className="grid md:grid-cols-2 gap-6">
                {/* Growth Opportunity Scanner */}
                <Card className="bg-gradient-to-br from-emerald-900/60 to-green-900/60 backdrop-blur-xl border-emerald-400/40 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-20 h-20 bg-emerald-400/10 rounded-bl-full"></div>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="p-3 bg-emerald-500/20 rounded-lg border border-emerald-400/30">
                          <Target className="w-8 h-8 text-emerald-300" />
                        </div>
                        <div>
                          <CardTitle className="text-xl text-emerald-300">Growth Opportunity Scanner</CardTitle>
                          <p className="text-emerald-200 text-sm">AI-Powered Opportunity Detection</p>
                        </div>
                      </div>
                      <Badge className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                        Module 1
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-white text-lg leading-relaxed">
                      AI identifies your <strong>top 3 monthly growth opportunities</strong> ranked by revenue impact and implementation difficulty.
                    </p>
                    <div className="space-y-3">
                      <h4 className="font-bold text-emerald-300 flex items-center">
                        <Sparkles className="w-4 h-4 mr-2" />
                        Premium Features:
                      </h4>
                      <div className="grid gap-2">
                        <div className="flex items-center text-emerald-100">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full mr-3"></div>
                          <span>Analyzes 50+ growth factors automatically</span>
                        </div>
                        <div className="flex items-center text-emerald-100">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full mr-3"></div>
                          <span>Prioritizes by projected revenue impact</span>
                        </div>
                        <div className="flex items-center text-emerald-100">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full mr-3"></div>
                          <span>Provides step-by-step action plans</span>
                        </div>
                        <div className="flex items-center text-emerald-100">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full mr-3"></div>
                          <span>Shows confidence scores and timelines</span>
                        </div>
                        <div className="flex items-center text-emerald-100">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full mr-3"></div>
                          <span>Covers acquisition, retention, and expansion</span>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 bg-emerald-500/10 rounded-lg border border-emerald-400/20">
                      <div className="text-sm text-emerald-200">
                        <strong className="text-emerald-300">Success Example:</strong> "Increase email marketing spend on Segment A for $12,000 monthly impact"
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Automated A/B Testing */}
                <Card className="bg-gradient-to-br from-blue-900/60 to-cyan-900/60 backdrop-blur-xl border-blue-400/40 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-20 h-20 bg-blue-400/10 rounded-bl-full"></div>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="p-3 bg-blue-500/20 rounded-lg border border-blue-400/30">
                          <BarChart3 className="w-8 h-8 text-blue-300" />
                        </div>
                        <div>
                          <CardTitle className="text-xl text-blue-300">Automated A/B Testing</CardTitle>
                          <p className="text-blue-200 text-sm">Set & Forget Optimization</p>
                        </div>
                      </div>
                      <Badge className="bg-blue-500/20 text-blue-300 border border-blue-400/30">
                        Module 2
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-white text-lg leading-relaxed">
                      AI generates, runs, and analyzes A/B tests automatically. <strong>Set it and forget it</strong> growth optimization.
                    </p>
                    <div className="space-y-3">
                      <h4 className="font-bold text-blue-300 flex items-center">
                        <Zap className="w-4 h-4 mr-2" />
                        Automation Features:
                      </h4>
                      <div className="grid gap-2">
                        <div className="flex items-center text-blue-100">
                          <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                          <span>AI creates test variants automatically</span>
                        </div>
                        <div className="flex items-center text-blue-100">
                          <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                          <span>Statistical significance calculations</span>
                        </div>
                        <div className="flex items-center text-blue-100">
                          <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                          <span>Auto-deploys winning variants</span>
                        </div>
                        <div className="flex items-center text-blue-100">
                          <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                          <span>Continuous optimization cycles</span>
                        </div>
                        <div className="flex items-center text-blue-100">
                          <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                          <span>Landing pages, emails, pricing tests</span>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 bg-blue-500/10 rounded-lg border border-blue-400/20">
                      <div className="text-sm text-blue-200">
                        <strong className="text-blue-300">Proven Results:</strong> Average 15-25% improvement in tested elements
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Revenue Leak Detection */}
                <Card className="bg-gradient-to-br from-orange-900/60 to-red-900/60 backdrop-blur-xl border-orange-400/40 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-20 h-20 bg-orange-400/10 rounded-bl-full"></div>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="p-3 bg-orange-500/20 rounded-lg border border-orange-400/30">
                          <AlertTriangle className="w-8 h-8 text-orange-300" />
                        </div>
                        <div>
                          <CardTitle className="text-xl text-orange-300">Revenue Leak Detection</CardTitle>
                          <p className="text-orange-200 text-sm">Find Hidden Money</p>
                        </div>
                      </div>
                      <Badge className="bg-orange-500/20 text-orange-300 border border-orange-400/30">
                        Module 3
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-white text-lg leading-relaxed">
                      Find hidden money in your sales funnel. Identifies <strong>exactly where you're losing</strong> potential revenue.
                    </p>
                    <div className="space-y-3">
                      <h4 className="font-bold text-orange-300 flex items-center">
                        <Search className="w-4 h-4 mr-2" />
                        Leak Types Detected:
                      </h4>
                      <div className="grid gap-2">
                        <div className="flex items-center text-orange-100">
                          <div className="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
                          <span>Conversion funnel bottlenecks</span>
                        </div>
                        <div className="flex items-center text-orange-100">
                          <div className="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
                          <span>Customer onboarding dropoffs</span>
                        </div>
                        <div className="flex items-center text-orange-100">
                          <div className="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
                          <span>Retention and churn issues</span>
                        </div>
                        <div className="flex items-center text-orange-100">
                          <div className="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
                          <span>Pricing optimization gaps</span>
                        </div>
                        <div className="flex items-center text-orange-100">
                          <div className="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
                          <span>Feature adoption problems</span>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 bg-orange-500/10 rounded-lg border border-orange-400/20">
                      <div className="text-sm text-orange-200">
                        <strong className="text-orange-300">Average Recovery:</strong> $30,000+ monthly revenue from fixing top leaks
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* ROI Calculator */}
                <Card className="bg-gradient-to-br from-purple-900/60 to-pink-900/60 backdrop-blur-xl border-purple-400/40 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-20 h-20 bg-purple-400/10 rounded-bl-full"></div>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="p-3 bg-purple-500/20 rounded-lg border border-purple-400/30">
                          <Calculator className="w-8 h-8 text-purple-300" />
                        </div>
                        <div>
                          <CardTitle className="text-xl text-purple-300">ROI Calculator & Tracking</CardTitle>
                          <p className="text-purple-200 text-sm">Financial Impact Analysis</p>
                        </div>
                      </div>
                      <Badge className="bg-purple-500/20 text-purple-300 border border-purple-400/30">
                        Module 4
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-white text-lg leading-relaxed">
                      Measure financial impact of every growth initiative with <strong>comprehensive ROI tracking</strong> and projections.
                    </p>
                    <div className="space-y-3">
                      <h4 className="font-bold text-purple-300 flex items-center">
                        <TrendingUp className="w-4 h-4 mr-2" />
                        Financial Analytics:
                      </h4>
                      <div className="grid gap-2">
                        <div className="flex items-center text-purple-100">
                          <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                          <span>Projected vs actual performance tracking</span>
                        </div>
                        <div className="flex items-center text-purple-100">
                          <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                          <span>Payback period calculations</span>
                        </div>
                        <div className="flex items-center text-purple-100">
                          <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                          <span>12-month and 24-month ROI projections</span>
                        </div>
                        <div className="flex items-center text-purple-100">
                          <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                          <span>Risk-adjusted return analysis</span>
                        </div>
                        <div className="flex items-center text-purple-100">
                          <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                          <span>Continuous prediction improvements</span>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 bg-purple-500/10 rounded-lg border border-purple-400/20">
                      <div className="text-sm text-purple-200">
                        <strong className="text-purple-300">Typical ROI:</strong> 300-600% return within 12 months
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* How to Use Section - Premium Design */}
            <Card className="bg-gradient-to-br from-slate-900/80 to-slate-800/80 backdrop-blur-xl border-slate-600/50 relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 via-blue-400 to-purple-400"></div>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="p-3 bg-white/10 backdrop-blur-xl rounded-lg border border-white/20">
                      <img 
                        src="https://customer-assets.emergentagent.com/job_mind-iq-dashboard/artifacts/blwfaa7a_Customer%20Mind%20IQ%20logo.png" 
                        alt="CustomerMind IQ" 
                        className="w-8 h-8 object-contain"
                      />
                    </div>
                    <div>
                      <CardTitle className="text-2xl text-white flex items-center">
                        <BookOpen className="w-7 h-7 mr-3 text-blue-400" />
                        How to Use the Growth Acceleration Engine
                      </CardTitle>
                      <p className="text-slate-300 text-lg mt-1">Professional implementation guide for maximum ROI</p>
                    </div>
                  </div>
                  <Badge className="bg-red-500/80 text-white text-sm px-3 py-2 font-bold border border-red-400/50">
                    ANNUAL ONLY
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-8">
                <div className="grid md:grid-cols-3 gap-8">
                  <div className="space-y-4 group">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-green-600 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-emerald-500/25 transition-all duration-300">
                        <span className="text-white font-bold text-lg">1</span>
                      </div>
                      <div>
                        <h3 className="font-bold text-emerald-400 text-lg">Access & Setup</h3>
                        <p className="text-slate-400 text-sm">Quick activation process</p>
                      </div>
                    </div>
                    <div className="ml-15 space-y-3">
                      <div className="flex items-start space-x-3">
                        <CheckCircle className="w-5 h-5 text-emerald-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Upgrade to Annual Professional or Enterprise plan</p>
                          <p className="text-slate-400 text-sm">Unlock immediate access + save 20%</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <CheckCircle className="w-5 h-5 text-emerald-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Navigate to "Growth Acceleration Engine" in header</p>
                          <p className="text-slate-400 text-sm">Look for the ⚡ icon with "Annual Access" badge</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <CheckCircle className="w-5 h-5 text-emerald-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Click "Full Growth Scan" to begin analysis</p>
                          <p className="text-slate-400 text-sm">AI starts analyzing your business data</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <Clock className="w-5 h-5 text-emerald-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Wait 5-15 minutes for AI analysis</p>
                          <p className="text-slate-400 text-sm">Continue using other features while scanning</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4 group">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-blue-500/25 transition-all duration-300">
                        <span className="text-white font-bold text-lg">2</span>
                      </div>
                      <div>
                        <h3 className="font-bold text-blue-400 text-lg">Review Opportunities</h3>
                        <p className="text-slate-400 text-sm">Smart prioritization</p>
                      </div>
                    </div>
                    <div className="ml-15 space-y-3">
                      <div className="flex items-start space-x-3">
                        <Target className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Review top 3 monthly growth opportunities</p>
                          <p className="text-slate-400 text-sm">AI-ranked by impact and feasibility</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <BarChart3 className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Check projected revenue impact and confidence scores</p>
                          <p className="text-slate-400 text-sm">Understand potential returns before investing</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <BookOpen className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Read detailed action plans and timelines</p>
                          <p className="text-slate-400 text-sm">Step-by-step implementation guides</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <Award className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Prioritize by implementation difficulty vs impact</p>
                          <p className="text-slate-400 text-sm">Focus on quick wins first</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4 group">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-purple-500/25 transition-all duration-300">
                        <span className="text-white font-bold text-lg">3</span>
                      </div>
                      <div>
                        <h3 className="font-bold text-purple-400 text-lg">Implement & Track</h3>
                        <p className="text-slate-400 text-sm">Execute & measure</p>
                      </div>
                    </div>
                    <div className="ml-15 space-y-3">
                      <div className="flex items-start space-x-3">
                        <Zap className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Generate A/B tests for top opportunities</p>
                          <p className="text-slate-400 text-sm">AI creates and runs tests automatically</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <AlertTriangle className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Fix identified revenue leaks first</p>
                          <p className="text-slate-400 text-sm">Quickest path to immediate revenue recovery</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <TrendingUp className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Monitor ROI dashboard for results</p>
                          <p className="text-slate-400 text-sm">Track actual vs projected performance</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <RefreshCw className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-white font-medium">Run monthly scans for new opportunities</p>
                          <p className="text-slate-400 text-sm">Continuous growth optimization</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Professional Implementation Timeline */}
                <div className="mt-8 p-6 bg-gradient-to-r from-slate-800/80 to-slate-700/80 rounded-lg border border-slate-600/50">
                  <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                    <Clock className="w-6 h-6 mr-2 text-yellow-400" />
                    Professional Implementation Timeline
                  </h4>
                  <div className="grid md:grid-cols-4 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-emerald-400">Week 1</div>
                      <div className="text-sm text-slate-300">Setup & First Scan</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-400">Week 2-3</div>
                      <div className="text-sm text-slate-300">Fix Revenue Leaks</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-400">Week 4-6</div>
                      <div className="text-sm text-slate-300">Launch A/B Tests</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-yellow-400">Month 2+</div>
                      <div className="text-sm text-slate-300">Scale Winners</div>
                    </div>
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