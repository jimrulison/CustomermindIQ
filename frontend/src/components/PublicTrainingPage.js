import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { 
  Play,
  Star,
  Video,
  Clock,
  Users,
  CheckCircle,
  Zap,
  TrendingUp,
  Award,
  Globe,
  BarChart3,
  Target,
  Sparkles,
  ExternalLink
} from 'lucide-react';

const PublicTrainingPage = () => {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [showVideoModal, setShowVideoModal] = useState(false);

  // All training videos - same as in Training.js but for public access
  const allTrainingVideos = [
    {
      id: 0,
      title: "Growth Acceleration Engine - Introduction",
      description: "Complete introduction to the Growth Acceleration Engine and how it can accelerate your business growth",
      duration: "Video",
      difficulty: "All Levels",
      category: "Growth",
      thumbnail: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=225&fit=crop",
      videoUrl: "https://customer-assets.emergentagent.com/job_customer-mind-iq-4/artifacts/anrdp8b3_Growth%20Acceleration%20intro%20slide%20show.mp4",
      topics: ["Growth Engine Overview", "Business Acceleration", "AI-Powered Growth", "Revenue Optimization"],
      featured: true
    },
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
      featured: true
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
      featured: true
    },
    {
      id: 3,
      title: "Getting Started with Website Intelligence Hub",
      description: "Complete overview of the platform and how to add your first website",
      duration: "8:45",
      difficulty: "Beginner",
      category: "Overview",
      thumbnail: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/getting_started.mp4",
      topics: ["Platform Navigation", "Adding Websites", "Dashboard Overview", "Basic Setup"]
    },
    {
      id: 4,
      title: "Understanding Performance Metrics",
      description: "Deep dive into Core Web Vitals and performance optimization",
      duration: "12:30",
      difficulty: "Intermediate",
      category: "Performance",
      thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/performance_metrics.mp4",
      topics: ["Core Web Vitals", "Load Times", "Performance Scoring", "Optimization Tips"]
    },
    {
      id: 5,
      title: "SEO Intelligence Mastery",
      description: "Maximize your search engine optimization with our SEO tools",
      duration: "15:22",
      difficulty: "Advanced",
      category: "SEO",
      thumbnail: "https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/seo_mastery.mp4",
      topics: ["Keyword Research", "Technical SEO", "Content Optimization", "Competitor Analysis"]
    },
    {
      id: 6,
      title: "Multi-Website Management",
      description: "Best practices for managing multiple websites and client accounts",
      duration: "10:15",
      difficulty: "Intermediate",
      category: "Management",
      thumbnail: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/multi_website_management.mp4",
      topics: ["Website Organization", "Bulk Operations", "Client Reporting", "Workflow Optimization"]
    },
    {
      id: 7,
      title: "Membership Tiers & Scaling",
      description: "Understanding plans, limits, and when to upgrade your membership",
      duration: "6:30",
      difficulty: "Beginner",
      category: "Account",
      thumbnail: "https://images.unsplash.com/photo-1553028826-f4804151e0b2?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/membership_scaling.mp4",
      topics: ["Plan Comparison", "Upgrade Benefits", "Usage Tracking", "ROI Calculation"]
    },
    {
      id: 8,
      title: "Advanced Analytics & Reporting",
      description: "Create professional reports and track ROI from your optimizations",
      duration: "18:45",
      difficulty: "Advanced",
      category: "Analytics",
      thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop",
      videoUrl: "/training/videos/advanced_analytics.mp4",
      topics: ["Custom Reports", "ROI Tracking", "Client Dashboards", "Performance Trends"]
    }
  ];

  // Pricing plans
  const pricingPlans = [
    {
      name: "Launch",
      originalPrice: "$99",
      price: "$49",
      yearlyPrice: "$490",
      yearlyOriginal: "$1188",
      description: "Perfect for growing businesses",
      badge: null,
      features: [
        "Up to 5 websites",
        "Basic AI analytics",
        "Email support",
        "Dashboard insights",
        "Performance monitoring"
      ],
      popular: false
    },
    {
      name: "Growth",
      originalPrice: "$199",
      price: "$75",
      yearlyPrice: "$750",
      yearlyOriginal: "$2388",
      description: "Most popular for scaling companies",
      badge: "Most Popular",
      features: [
        "Up to 15 websites",
        "Advanced AI insights",
        "Priority support",
        "Growth Acceleration Engine (Annual Only)",
        "Custom reporting",
        "Live chat support"
      ],
      popular: true
    },
    {
      name: "Scale",
      originalPrice: "$399",
      price: "$199",
      yearlyPrice: "$1990",
      yearlyOriginal: "$4788",
      description: "For enterprise-level operations",
      badge: null,
      features: [
        "Unlimited websites",
        "Enterprise AI features",
        "24/7 phone support",
        "Growth Acceleration Engine (Annual Only)",
        "White-label options",
        "Dedicated account manager"
      ],
      popular: false
    },
    {
      name: "White Label",
      originalPrice: "Custom",
      price: "Contact Sales",
      yearlyPrice: "Contact Sales", 
      yearlyOriginal: "Custom",
      description: "Complete white-label solution",
      badge: "Enterprise",
      features: [
        "Complete white-labeling",
        "Custom branding",
        "API access",
        "Growth Acceleration Engine (Annual Only)",
        "Custom integrations",
        "Dedicated infrastructure"
      ],
      popular: false
    }
  ];

  const getCategoryColor = (category) => {
    const colors = {
      'Growth': 'bg-green-500/20 text-green-400 border-green-500/30',
      'Getting Started': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      'Advanced Features': 'bg-purple-500/20 text-purple-400 border-purple-500/30',
      'Overview': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      'Performance': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      'SEO': 'bg-purple-500/20 text-purple-400 border-purple-500/30',
      'Management': 'bg-green-500/20 text-green-400 border-green-500/30',
      'Account': 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
      'Analytics': 'bg-pink-500/20 text-pink-400 border-pink-500/30'
    };
    return colors[category] || 'bg-gray-500/20 text-gray-400 border-gray-500/30';
  };

  const handleVideoClick = (video) => {
    setSelectedVideo(video);
    setShowVideoModal(true);
  };

  const handleTrialSignup = () => {
    // Redirect to main site trial signup
    window.location.href = '/#trial-signup';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header Section */}
      <div className="container mx-auto px-6 py-12">
        {/* Logo */}
        <div className="text-center mb-8">
          <img 
            src="https://customer-assets.emergentagent.com/job_customer-mind-iq-4/artifacts/pntu3yqm_Customer%20Mind%20IQ%20logo.png" 
            alt="CustomerMind IQ" 
            className="mx-auto h-24 w-auto mb-6"
          />
          <h1 className="text-4xl font-bold text-white mb-4">
            Want to really know what the Customer Mind IQ software is all about?
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Here are our training videos that we are glad to share.
          </p>
        </div>

        {/* Training Videos Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4 flex items-center justify-center">
              <Video className="w-8 h-8 mr-3 text-blue-400" />
              Training Videos
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Get hands-on training with our comprehensive video library covering all aspects of the CustomerMind IQ platform
            </p>
          </div>

          {/* Video Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {allTrainingVideos.map((video) => (
              <Card 
                key={video.id} 
                className={`bg-slate-800/50 border-slate-700 hover:border-blue-500/50 transition-all duration-300 cursor-pointer group ${
                  video.featured ? 'ring-2 ring-green-500/20 bg-gradient-to-br from-green-600/10 to-blue-600/10' : ''
                }`}
                onClick={() => handleVideoClick(video)}
              >
                <CardHeader className="pb-3">
                  <div className="relative">
                    <img 
                      src={video.thumbnail} 
                      alt={video.title}
                      className="w-full h-32 object-cover rounded-lg mb-4"
                    />
                    <div className="absolute inset-0 bg-black/40 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <Play className="w-12 h-12 text-white" />
                    </div>
                    {video.featured && (
                      <div className="absolute top-2 left-2">
                        <Badge className="bg-green-500/20 text-green-400 border-green-500/30">
                          <Star className="w-3 h-3 mr-1" />
                          FEATURED
                        </Badge>
                      </div>
                    )}
                  </div>
                  <CardTitle className="text-white text-lg leading-tight">
                    {video.title}
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    {video.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between mb-3">
                    <Badge className={getCategoryColor(video.category)}>
                      {video.category}
                    </Badge>
                    <Badge className="bg-slate-700 text-slate-300">
                      {video.difficulty}
                    </Badge>
                  </div>
                  <div className="flex items-center text-sm text-slate-400 mb-4">
                    <Clock className="w-4 h-4 mr-1" />
                    {video.duration}
                  </div>
                  
                  {/* Topics */}
                  <div className="space-y-1">
                    <p className="text-sm font-medium text-slate-300">Topics covered:</p>
                    <div className="flex flex-wrap gap-1">
                      {video.topics.slice(0, 3).map((topic, index) => (
                        <Badge key={index} className="bg-slate-700/50 text-slate-400 text-xs">
                          {topic}
                        </Badge>
                      ))}
                      {video.topics.length > 3 && (
                        <Badge className="bg-slate-700/50 text-slate-400 text-xs">
                          +{video.topics.length - 3} more
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Pricing Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4 flex items-center justify-center">
              <TrendingUp className="w-8 h-8 mr-3 text-green-400" />
              Choose Your Plan
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Get started with our powerful AI-driven customer intelligence platform
            </p>
            <div className="mt-6">
              <Badge className="bg-green-500/20 text-green-400 border-green-500/30 text-lg px-4 py-2">
                <Award className="w-5 h-5 mr-2" />
                12 months for the price of 10 with annual plans!
              </Badge>
            </div>
          </div>

          {/* Pricing Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {pricingPlans.map((plan, index) => (
              <Card 
                key={index}
                className={`bg-slate-800/50 border-slate-700 relative ${
                  plan.popular ? 'ring-2 ring-blue-500/50 scale-105' : ''
                }`}
              >
                {plan.badge && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <Badge className={
                      plan.badge === "Most Popular" 
                        ? "bg-blue-500 text-white" 
                        : "bg-purple-500 text-white"
                    }>
                      {plan.badge}
                    </Badge>
                  </div>
                )}
                
                <CardHeader className="text-center pb-4">
                  <CardTitle className="text-white text-xl">{plan.name}</CardTitle>
                  <CardDescription className="text-slate-400">{plan.description}</CardDescription>
                  
                  <div className="mt-4">
                    {plan.price !== "Contact Sales" ? (
                      <>
                        <div className="flex items-center justify-center mb-2">
                          <span className="text-2xl text-slate-400 line-through mr-2">{plan.originalPrice}</span>
                          <span className="text-4xl font-bold text-white">{plan.price}</span>
                          <span className="text-slate-400 ml-1">/month</span>
                        </div>
                        <div className="text-center">
                          <p className="text-sm text-slate-400">or</p>
                          <div className="flex items-center justify-center">
                            <span className="text-lg text-slate-400 line-through mr-2">{plan.yearlyOriginal}</span>
                            <span className="text-xl font-bold text-green-400">{plan.yearlyPrice}</span>
                            <span className="text-slate-400 ml-1">/year</span>
                          </div>
                          <Badge className="bg-green-500/20 text-green-400 mt-2">
                            Save 2 months!
                          </Badge>
                        </div>
                      </>
                    ) : (
                      <div className="text-center">
                        <span className="text-2xl font-bold text-white">{plan.price}</span>
                      </div>
                    )}
                  </div>
                </CardHeader>
                
                <CardContent>
                  <ul className="space-y-3">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center text-slate-300">
                        <CheckCircle className="w-4 h-4 text-green-400 mr-3 flex-shrink-0" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  
                  <Button className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white">
                    {plan.price === "Contact Sales" ? "Contact Sales" : "Get Started"}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Annual Bonus Section */}
          <div className="mt-12 text-center">
            <Card className="bg-gradient-to-r from-green-600/20 to-blue-600/20 border-green-500/30">
              <CardContent className="py-8">
                <div className="flex items-center justify-center mb-4">
                  <Sparkles className="w-8 h-8 text-green-400 mr-3" />
                  <h3 className="text-2xl font-bold text-white">Exclusive Annual Member Bonus</h3>
                </div>
                <p className="text-xl text-slate-300 mb-4">
                  Get the <strong className="text-green-400 italic">FREE</strong> $3,000 Growth Acceleration Engine
                </p>
                <p className="text-slate-400 max-w-2xl mx-auto">
                  Available with Launch, Growth, and Scale annual plans. Unlock AI-powered growth opportunities, 
                  automated A/B testing, and revenue optimization tools.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Call-to-Action Section */}
        <div className="text-center">
          <Card className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border-blue-500/30">
            <CardContent className="py-12">
              <h3 className="text-3xl font-bold text-white mb-4">
                Ready to Transform Your Business?
              </h3>
              <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
                Start your 7-day free trial today and experience the power of AI-driven customer intelligence
              </p>
              <Button 
                size="lg"
                className="bg-green-600 hover:bg-green-700 text-white text-xl px-12 py-4"
                onClick={handleTrialSignup}
              >
                <Zap className="w-6 h-6 mr-2" />
                Start 7-Day Free Trial - No Credit Card Required
              </Button>
              <p className="text-sm text-slate-400 mt-4">
                Full access to all features • Cancel anytime • No commitments
              </p>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Video Modal */}
      {showVideoModal && selectedVideo && (
        <Dialog open={showVideoModal} onOpenChange={setShowVideoModal}>
          <DialogContent className="max-w-4xl bg-slate-800 border-slate-700">
            <DialogHeader>
              <DialogTitle className="text-white text-xl">
                {selectedVideo.title}
              </DialogTitle>
              <DialogDescription className="text-slate-400">
                {selectedVideo.description}
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-6">
              {/* Video Player */}
              <div className="aspect-video bg-black rounded-lg overflow-hidden">
                <video 
                  controls 
                  className="w-full h-full"
                  poster={selectedVideo.thumbnail}
                >
                  <source src={selectedVideo.videoUrl} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
              
              {/* Video Info */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h4 className="text-white font-medium mb-2">Category</h4>
                  <Badge className={getCategoryColor(selectedVideo.category)}>
                    {selectedVideo.category}
                  </Badge>
                </div>
                <div>
                  <h4 className="text-white font-medium mb-2">Difficulty</h4>
                  <Badge className="bg-slate-700 text-slate-300">
                    {selectedVideo.difficulty}
                  </Badge>
                </div>
                <div>
                  <h4 className="text-white font-medium mb-2">Duration</h4>
                  <p className="text-slate-400">{selectedVideo.duration}</p>
                </div>
              </div>
              
              {/* Topics */}
              <div>
                <h4 className="text-white font-medium mb-3">What you'll learn:</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {selectedVideo.topics.map((topic, index) => (
                    <div key={index} className="flex items-center text-slate-300">
                      <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                      {topic}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
};

export default PublicTrainingPage;