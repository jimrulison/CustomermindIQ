import React from 'react';
import SEOHead from './SEOHead';
import StructuredDataScript, { MultipleStructuredData } from './StructuredDataScript';
import { seoData, generateOrganizationSchema, generateSoftwareApplicationSchema, generateFAQSchema } from '../utils/seoData';
import { 
  Brain, 
  TrendingUp, 
  Target, 
  Shield, 
  Zap, 
  BarChart3,
  Users,
  DollarSign,
  CheckCircle,
  ArrowRight,
  Star,
  Award,
  Lightbulb,
  RefreshCw
} from 'lucide-react';

const OptimizedLandingPage = () => {
  // FAQ data for structured data
  const faqs = [
    {
      question: "What is CustomerMind IQ?", 
      answer: "CustomerMind IQ is an AI-powered customer intelligence platform that helps businesses achieve 300-500% ROI through predictive analytics, churn prevention, and revenue optimization. Our platform offers 91.8% accurate churn prediction, 40% better marketing ROI, and comprehensive business intelligence."
    },
    {
      question: "How accurate is the churn prediction?",
      answer: "Our AI models provide 91.8% accurate churn prediction, helping you identify at-risk customers before they leave. This allows for proactive retention campaigns that can reduce churn by 20-30%."
    },
    {
      question: "What's included in the free trial?",
      answer: "The 7-day free trial includes full access to Launch tier features with no credit card required. You'll get customer analytics, basic automation, and website intelligence to experience the platform's value firsthand."
    },
    {
      question: "How does CustomerMind IQ integrate with existing tools?",
      answer: "We offer 50+ pre-built integrations with popular tools like Salesforce, HubSpot, Google Analytics, Mailchimp, and more. Real-time data sync ensures your insights are always current."
    },
    {
      question: "What ROI can I expect?",
      answer: "Typical customers see 300-500% ROI within the first 12 months through improved marketing efficiency, reduced churn, optimized pricing, and automated processes that save 40+ hours weekly."
    }
  ];

  const structuredDataArray = [
    generateOrganizationSchema(),
    generateSoftwareApplicationSchema(),
    generateFAQSchema(faqs)
  ];

  const features = [
    {
      icon: Brain,
      title: "91.8% Accurate Churn Prediction",
      description: "Identify at-risk customers before they leave with our AI-powered prediction models. Reduce churn by 20-30% through proactive retention campaigns.",
      benefit: "20-30% churn reduction"
    },
    {
      icon: DollarSign,
      title: "95% Accurate Revenue Forecasting", 
      description: "Predict revenue 3-6 months in advance with 95% accuracy. Make informed budget decisions and optimize resource allocation.",
      benefit: "95% forecast accuracy"
    },
    {
      icon: TrendingUp,
      title: "40% Better Marketing ROI",
      description: "Optimize campaigns with AI-powered automation, A/B testing, and personalization. Automate 78.9% of routine marketing tasks.",
      benefit: "40% ROI improvement"
    },
    {
      icon: Target,
      title: "Customer Behavioral Clustering",
      description: "Discover hidden customer patterns with AI segmentation. Create laser-focused campaigns that increase effectiveness by 35%+.",
      benefit: "35% campaign boost"
    },
    {
      icon: BarChart3,
      title: "Real-Time Business Intelligence",
      description: "Transform data silos into unified insights. Save 40+ hours weekly on manual data compilation and reporting.",
      benefit: "40+ hours saved weekly"
    },
    {
      icon: Shield,
      title: "Enterprise Security & Compliance",
      description: "GDPR, HIPAA, SOX compliant with AES-256 encryption. Reduce compliance overhead by 60% with automated monitoring.",
      benefit: "60% compliance efficiency"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "VP Marketing, TechCorp",
      company: "TechCorp Solutions",
      content: "CustomerMind IQ helped us reduce churn by 28% and increase marketing ROI by 45%. The churn prediction accuracy is incredible - we can now save customers before they even think about leaving.",
      rating: 5
    },
    {
      name: "Michael Chen", 
      role: "CEO",
      company: "GrowthStartup",
      content: "Within 3 months, we saw 320% ROI. The revenue forecasting helped us secure funding by showing investors our predictable growth trajectory. Game-changing platform.",
      rating: 5
    },
    {
      name: "Lisa Rodriguez",
      role: "Head of Customer Success",
      company: "ScaleEnterprise", 
      content: "The customer intelligence suite transformed how we understand our users. We've increased customer lifetime value by 31% and our satisfaction scores hit all-time highs.",
      rating: 5
    }
  ];

  const stats = [
    { value: "91.8%", label: "Churn Prediction Accuracy" },
    { value: "95%", label: "Revenue Forecast Accuracy" },
    { value: "40%", label: "Marketing ROI Improvement" }, 
    { value: "300-500%", label: "Platform ROI in 12 Months" }
  ];

  return (
    <>
      <SEOHead {...seoData.home} />
      <MultipleStructuredData dataArray={structuredDataArray} />
      
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        {/* Hero Section */}
        <header className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10"></div>
          <div className="relative container mx-auto px-6 py-16 lg:py-24">
            <div className="max-w-4xl mx-auto text-center">
              <div className="mb-6">
                <span className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold">
                  <Award className="w-4 h-4 mr-2" />
                  #1 Customer Intelligence Platform - 300-500% ROI
                </span>
              </div>
              
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-6">
                Transform Your Business with 
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> AI-Powered</span> Customer Intelligence
              </h1>
              
              <p className="text-xl lg:text-2xl text-gray-600 mb-8 leading-relaxed">
                Achieve <strong>300-500% ROI</strong> with 91.8% accurate churn prediction, 40% better marketing performance, and real-time business intelligence. Join 1,000+ businesses growing faster with CustomerMind IQ.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
                <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:shadow-xl transform hover:scale-105 transition-all duration-200">
                  Start Free 7-Day Trial
                  <ArrowRight className="w-5 h-5 ml-2 inline" />
                </button>
                <button className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-lg text-lg font-semibold hover:border-blue-600 hover:text-blue-600 transition-all">
                  Watch Demo (2 min)
                </button>
              </div>
              
              <div className="text-sm text-gray-500">
                ✅ No credit card required • ✅ 7-day free trial • ✅ Cancel anytime
              </div>
            </div>
          </div>
        </header>

        {/* Stats Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Proven Results Across 1,000+ Businesses
              </h2>
              <p className="text-xl text-gray-600">
                Real metrics from real customers using CustomerMind IQ
              </p>
            </div>
            
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-4xl lg:text-5xl font-bold text-blue-600 mb-2">
                    {stat.value}
                  </div>
                  <div className="text-gray-600 font-medium">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-6">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                47 AI-Powered Features That Drive Growth
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Every feature is designed to deliver measurable business impact. See how our customers achieve extraordinary results.
              </p>
            </div>
            
            <div className="grid lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
                  <div className="flex items-center mb-6">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                      <feature.icon className="w-6 h-6 text-blue-600" />
                    </div>
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                      {feature.benefit}
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-4">
                    {feature.title}
                  </h3>
                  
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="py-20 bg-white">
          <div className="container mx-auto px-6">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Trusted by 1,000+ Growing Businesses
              </h2>
              <p className="text-xl text-gray-600">
                See what our customers say about their results with CustomerMind IQ
              </p>
            </div>
            
            <div className="grid lg:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <div key={index} className="bg-gray-50 rounded-xl p-8">
                  <div className="flex items-center mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  
                  <blockquote className="text-gray-700 mb-6 italic">
                    "{testimonial.content}"
                  </blockquote>
                  
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold mr-4">
                      {testimonial.name.charAt(0)}
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">
                        {testimonial.name}
                      </div>
                      <div className="text-gray-600">
                        {testimonial.role}, {testimonial.company}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section className="py-20 bg-gradient-to-r from-blue-50 to-purple-50">
          <div className="container mx-auto px-6">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Simple, Transparent Pricing
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Start with our 7-day free trial. No credit card required.
              </p>
              
              <div className="inline-flex items-center bg-green-100 text-green-800 px-6 py-3 rounded-full text-lg font-semibold mb-8">
                <Zap className="w-5 h-5 mr-2" />
                Limited Time: 50% Off All Plans
              </div>
            </div>
            
            <div className="grid lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {/* Launch Plan */}
              <div className="bg-white rounded-xl shadow-lg p-8">
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">Launch</h3>
                  <div className="text-4xl font-bold text-blue-600 mb-2">
                    $49<span className="text-lg text-gray-500">/month</span>
                  </div>
                  <div className="text-gray-500 line-through">$99/month</div>
                  <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold mt-4">
                    Perfect for Small Businesses
                  </div>
                </div>
                
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    5 websites monitored
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    50 keywords tracked
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Basic customer analytics
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Email support (48hr)
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    7-day free trial
                  </li>
                </ul>
                
                <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                  Start Free Trial
                </button>
              </div>

              {/* Growth Plan - Most Popular */}
              <div className="bg-white rounded-xl shadow-xl p-8 border-2 border-blue-500 relative">
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-500 text-white px-6 py-2 rounded-full text-sm font-semibold">
                    Most Popular
                  </span>
                </div>
                
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">Growth</h3>
                  <div className="text-4xl font-bold text-blue-600 mb-2">
                    $75<span className="text-lg text-gray-500">/month</span>
                  </div>
                  <div className="text-gray-500 line-through">$149/month</div>
                  <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-semibold mt-4">
                    Best for Growing Businesses
                  </div>
                </div>
                
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    10 websites monitored
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    200 keywords tracked
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Full analytics suite
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Live chat + Email (12hr)
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Marketing automation
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Advanced features
                  </li>
                </ul>
                
                <button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all">
                  Start Free Trial
                </button>
              </div>

              {/* Scale Plan */}
              <div className="bg-white rounded-xl shadow-lg p-8">
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">Scale</h3>
                  <div className="text-4xl font-bold text-blue-600 mb-2">
                    $199<span className="text-lg text-gray-500">/month</span>
                  </div>
                  <div className="text-gray-500 line-through">$399/month</div>
                  <div className="bg-yellow-100 text-yellow-800 px-4 py-2 rounded-full text-sm font-semibold mt-4">
                    Enterprise Features
                  </div>
                </div>
                
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Unlimited websites
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    500+ keywords
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Advanced analytics
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Live chat + Phone (4hr)
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Premium support + SLA
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    Enterprise features
                  </li>
                </ul>
                
                <button className="w-full bg-yellow-600 text-white py-3 rounded-lg font-semibold hover:bg-yellow-700 transition-colors">
                  Start Free Trial
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-20 bg-white">
          <div className="container mx-auto px-6">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Frequently Asked Questions
              </h2>
              <p className="text-xl text-gray-600">
                Everything you need to know about CustomerMind IQ
              </p>
            </div>
            
            <div className="max-w-3xl mx-auto space-y-8">
              {faqs.map((faq, index) => (
                <div key={index} className="bg-gray-50 rounded-xl p-8">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">
                    {faq.question}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {faq.answer}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Join 1,000+ businesses achieving 300-500% ROI with CustomerMind IQ. Start your free trial today and see results in the first week.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:shadow-xl transform hover:scale-105 transition-all duration-200">
                Start Free 7-Day Trial
                <ArrowRight className="w-5 h-5 ml-2 inline" />
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-white hover:text-blue-600 transition-all">
                Schedule Demo
              </button>
            </div>
            
            <div className="text-blue-100 mt-6">
              ✅ No credit card required • ✅ Cancel anytime • ✅ 24/7 support
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-gray-900 text-white py-16">
          <div className="container mx-auto px-6">
            <div className="grid lg:grid-cols-4 gap-8">
              <div>
                <h3 className="text-2xl font-bold mb-4">CustomerMind IQ</h3>
                <p className="text-gray-400 mb-6">
                  AI-powered customer intelligence platform helping businesses achieve 300-500% ROI through predictive analytics and automation.
                </p>
                <div className="flex space-x-4">
                  {/* Social media icons would go here */}
                </div>
              </div>
              
              <div>
                <h4 className="text-lg font-semibold mb-4">Platform</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white">Customer Intelligence</a></li>
                  <li><a href="#" className="hover:text-white">Revenue Analytics</a></li>
                  <li><a href="#" className="hover:text-white">Marketing Automation</a></li>
                  <li><a href="#" className="hover:text-white">Website Intelligence</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="text-lg font-semibold mb-4">Company</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white">About Us</a></li>
                  <li><a href="#" className="hover:text-white">Careers</a></li>
                  <li><a href="#" className="hover:text-white">Blog</a></li>
                  <li><a href="#" className="hover:text-white">Contact</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="text-lg font-semibold mb-4">Support</h4>
                <ul className="space-y-2 text-gray-400">
                  <li><a href="#" className="hover:text-white">Help Center</a></li>
                  <li><a href="#" className="hover:text-white">Documentation</a></li>
                  <li><a href="#" className="hover:text-white">API Reference</a></li>
                  <li><a href="#" className="hover:text-white">Status</a></li>
                </ul>
              </div>
            </div>
            
            <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
              <p>&copy; 2025 CustomerMind IQ. All rights reserved. | Privacy Policy | Terms of Service</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default OptimizedLandingPage;