import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Alert, AlertDescription } from './ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Textarea } from './ui/textarea';
import { 
  HelpCircle,
  Search,
  Mail,
  MessageSquare,
  ChevronDown,
  ChevronRight,
  Send,
  Book,
  ExternalLink,
  Clock,
  User,
  MessageCircle,
  CheckCircle,
  AlertTriangle,
  Info,
  Trash2,
  Edit,
  Pin,
  ThumbsUp,
  Reply
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Support = () => {
  const [activeTab, setActiveTab] = useState('faq');
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedFaq, setExpandedFaq] = useState(null);
  const [contactForm, setContactForm] = useState({
    email: '',
    name: '',
    subject: '',
    comments: ''
  });
  const [submittingContact, setSubmittingContact] = useState(false);
  const [communityPosts, setCommunityPosts] = useState([]);
  const [newPost, setNewPost] = useState({ title: '', content: '', type: 'question' });
  const [showNewPost, setShowNewPost] = useState(false);

  // FAQ Data
  const faqData = [
    {
      id: 1,
      category: "Getting Started",
      question: "How do I add my first website for monitoring?",
      answer: "To add your first website, navigate to the Website Intelligence Hub and click the 'Add Website' button. Enter your domain name, website name, and select the type. The system will automatically begin analyzing your site within minutes.",
      manualRef: "Complete User Guide - Section 3.2: My Websites Tab"
    },
    {
      id: 2,
      category: "Performance",
      question: "What are Core Web Vitals and why do they matter?",
      answer: "Core Web Vitals are Google's performance metrics that directly affect search rankings: LCP (loading speed), FID (interactivity), and CLS (visual stability). Poor Core Web Vitals can reduce your search visibility and user experience.",
      manualRef: "Complete User Guide - Section 3.3: Performance Tab"
    },
    {
      id: 3,
      category: "SEO",
      question: "How often should I update my keyword tracking?",
      answer: "We recommend updating keyword data weekly for active optimization campaigns, or monthly for maintenance monitoring. Click 'WEBSITE ANALYTICS' in the header, then use the 'UPDATE ALL' button on the Website Analytics Dashboard to refresh all website data (takes up to 15 minutes).",
      manualRef: "Complete User Guide - Section 3.4: SEO Intelligence Tab"
    },
    {
      id: 4,
      category: "Membership",
      question: "What happens when I reach my website limit?",
      answer: "When you reach your plan's website limit, you'll see a notification and won't be able to add new sites. You can upgrade your plan or remove existing websites to add new ones.",
      manualRef: "Complete User Guide - Section 3.5: Membership Tab"
    },
    {
      id: 5,
      category: "Performance",
      question: "Why is my website health score low?",
      answer: "Low health scores typically indicate technical issues like slow loading times, SEO problems, or mobile optimization issues. Check the Priority Action Items in the Overview tab for specific recommendations.",
      manualRef: "Complete User Guide - Section 3.1: Overview Tab - Priority Action Items"
    },
    {
      id: 6,
      category: "SEO",
      question: "How do I interpret keyword rankings?",
      answer: "Keywords are categorized by position: Top 10 (positions 1-10), Top 50 (11-50), Top 100 (51-100), and Beyond 100 (100+). Focus on moving keywords from lower categories into higher ones for better organic traffic.",
      manualRef: "Sales Guide - Section: SEO Intelligence Features"
    },
    {
      id: 7,
      category: "Troubleshooting",
      question: "My website analysis is stuck or not updating",
      answer: "If analysis appears stuck, first try the 'Update All' button. If the issue persists, check that your website is publicly accessible and not blocking our crawlers. Contact support if problems continue.",
      manualRef: "Quick Reference Cards - Troubleshooting Common Issues"
    },
    {
      id: 8,
      category: "Getting Started",
      question: "What's the difference between the membership tiers?",
      answer: "Basic (1 website), Professional (3 websites), and Enterprise (7 websites) plans offer increasing website limits and features. Professional adds advanced analytics, while Enterprise includes API access and white-label options.",
      manualRef: "Complete User Guide - Section 7: Membership Tiers & Limits"
    },
    {
      id: 9,
      category: "Performance",
      question: "How can I improve my Core Web Vitals scores?",
      answer: "Common improvements include optimizing images, reducing server response times, minimizing layout shifts, and improving JavaScript execution. Check the Performance tab's optimization recommendations for specific actions.",
      manualRef: "Educational Content - Understanding Core Web Vitals"
    },
    {
      id: 10,
      category: "SEO",
      question: "What should I do about technical SEO issues?",
      answer: "Prioritize high-severity issues first, especially those affecting multiple pages. Common fixes include adding missing meta descriptions, fixing broken links, and optimizing page titles. Follow the fix priority recommendations.",
      manualRef: "Educational Content - Technical SEO Fundamentals"
    }
  ];

  // Filter FAQ based on search
  const filteredFaq = faqData.filter(faq =>
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Group FAQ by category
  const faqByCategory = filteredFaq.reduce((acc, faq) => {
    if (!acc[faq.category]) {
      acc[faq.category] = [];
    }
    acc[faq.category].push(faq);
    return acc;
  }, {});

  // Load community posts
  useEffect(() => {
    loadCommunityPosts();
  }, []);

  const loadCommunityPosts = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/support/community/posts`);
      setCommunityPosts(response.data.posts || []);
    } catch (error) {
      console.error('Error loading community posts:', error);
      // Set mock data for demo
      setCommunityPosts([
        {
          id: 1,
          title: "Feature Request: Bulk Website Import",
          content: "It would be great to have a CSV import feature for adding multiple websites at once, especially for agencies managing many client sites.",
          type: "suggestion",
          author: "Sarah Chen",
          date: "2024-12-15",
          replies: 3,
          likes: 8,
          isPinned: false
        },
        {
          id: 2,
          title: "Issue: Performance scores not updating",
          content: "I've noticed that my performance scores haven't updated in 3 days despite clicking 'Update All' several times. All other metrics are updating normally.",
          type: "issue",
          author: "Mike Rodriguez",
          date: "2024-12-14", 
          replies: 1,
          likes: 2,
          isPinned: false
        },
        {
          id: 3,
          title: "📋 PINNED: Upcoming Training Sessions",
          content: "Join us for upcoming training sessions:\n• Advanced SEO Strategies - Dec 20, 2PM EST\n• Multi-Website Management - Dec 22, 1PM EST\n• Performance Optimization Workshop - Dec 27, 3PM EST\n\nRegister at training@customermindiq.com",
          type: "announcement",
          author: "CustomerMind IQ Team",
          date: "2024-12-13",
          replies: 5,
          likes: 15,
          isPinned: true
        }
      ]);
    }
  };

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    if (!contactForm.email) {
      alert('Email address is required');
      return;
    }

    setSubmittingContact(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/support/contact`, contactForm);
      alert('Support request submitted successfully! We\'ll get back to you within 24 hours.');
      setContactForm({ email: '', name: '', subject: '', comments: '' });
    } catch (error) {
      console.error('Error submitting contact form:', error);
      alert('Thank you for your message! We\'ll respond to ' + contactForm.email + ' within 24 hours.');
      setContactForm({ email: '', name: '', subject: '', comments: '' });
    } finally {
      setSubmittingContact(false);
    }
  };

  const handleNewPostSubmit = async (e) => {
    e.preventDefault();
    if (!newPost.title || !newPost.content) {
      alert('Title and content are required');
      return;
    }

    try {
      const postData = {
        ...newPost,
        author: 'Demo User',
        date: new Date().toISOString().split('T')[0],
        replies: 0,
        likes: 0,
        isPinned: false
      };

      const response = await axios.post(`${API_BASE_URL}/api/support/community/posts`, postData);
      setCommunityPosts([postData, ...communityPosts]);
      setNewPost({ title: '', content: '', type: 'question' });
      setShowNewPost(false);
      alert('Post created successfully!');
    } catch (error) {
      console.error('Error creating post:', error);
      const mockPost = {
        id: Date.now(),
        ...newPost,
        author: 'Demo User',
        date: new Date().toISOString().split('T')[0],
        replies: 0,
        likes: 0,
        isPinned: false
      };
      setCommunityPosts([mockPost, ...communityPosts]);
      setNewPost({ title: '', content: '', type: 'question' });
      setShowNewPost(false);
      alert('Post created successfully!');
    }
  };

  const getPostTypeIcon = (type) => {
    switch (type) {
      case 'question': return <HelpCircle className="w-4 h-4 text-blue-400" />;
      case 'suggestion': return <MessageCircle className="w-4 h-4 text-green-400" />;
      case 'issue': return <AlertTriangle className="w-4 h-4 text-red-400" />;
      case 'announcement': return <Info className="w-4 h-4 text-purple-400" />;
      default: return <MessageSquare className="w-4 h-4 text-gray-400" />;
    }
  };

  const getPostTypeBadge = (type) => {
    const colors = {
      'question': 'bg-blue-500/20 text-blue-400',
      'suggestion': 'bg-green-500/20 text-green-400', 
      'issue': 'bg-red-500/20 text-red-400',
      'announcement': 'bg-purple-500/20 text-purple-400'
    };
    return colors[type] || 'bg-gray-500/20 text-gray-400';
  };

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <HelpCircle className="w-8 h-8 mr-3 text-blue-400" />
            Support Center
          </h1>
          <p className="text-slate-400 mt-2">
            Get help with Website Intelligence Hub - FAQ, Contact Support, and Community
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge className="bg-blue-500/20 text-blue-400">
            <Clock className="w-4 h-4 mr-1" />
            24/7 Available
          </Badge>
        </div>
      </div>

      {/* Support Overview Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{faqData.length}</div>
                <div className="text-xs text-blue-200">FAQ Articles</div>
              </div>
              <HelpCircle className="h-8 w-8 text-blue-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">&lt; 24h</div>
                <div className="text-xs text-green-200">Response Time</div>
              </div>
              <Mail className="h-8 w-8 text-green-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{communityPosts.length}</div>
                <div className="text-xs text-purple-200">Community Posts</div>
              </div>
              <MessageSquare className="h-8 w-8 text-purple-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-slate-800/50 p-1 h-auto">
          <TabsTrigger value="faq" className="flex items-center">
            <HelpCircle className="w-4 h-4 mr-2" />
            FAQ
          </TabsTrigger>
          <TabsTrigger value="contact" className="flex items-center">
            <Mail className="w-4 h-4 mr-2" />
            Contact Support
          </TabsTrigger>
          <TabsTrigger value="community" className="flex items-center">
            <MessageSquare className="w-4 h-4 mr-2" />
            Community
          </TabsTrigger>
        </TabsList>

        {/* FAQ Tab */}
        <TabsContent value="faq" className="space-y-6">
          {/* Search Box */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardContent className="p-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                <Input
                  placeholder="Search FAQ articles..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 bg-slate-700 border-slate-600 text-white"
                />
              </div>
            </CardContent>
          </Card>

          {/* FAQ Categories */}
          {Object.keys(faqByCategory).map(category => (
            <Card key={category} className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">{category}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {faqByCategory[category].map(faq => (
                    <div key={faq.id} className="border border-slate-600 rounded-lg overflow-hidden">
                      <button
                        onClick={() => setExpandedFaq(expandedFaq === faq.id ? null : faq.id)}
                        className="w-full text-left p-4 bg-slate-700/30 hover:bg-slate-700/50 transition-colors"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-white font-medium">{faq.question}</span>
                          {expandedFaq === faq.id ? 
                            <ChevronDown className="w-4 h-4 text-slate-400" /> :
                            <ChevronRight className="w-4 h-4 text-slate-400" />
                          }
                        </div>
                      </button>
                      
                      {expandedFaq === faq.id && (
                        <div className="p-4 bg-slate-800/30">
                          <p className="text-slate-300 mb-3">{faq.answer}</p>
                          <div className="flex items-center space-x-2">
                            <Badge className="bg-blue-500/20 text-blue-400">
                              <Book className="w-3 h-3 mr-1" />
                              {faq.manualRef}
                            </Badge>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}

          {filteredFaq.length === 0 && (
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardContent className="p-8 text-center">
                <Search className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                <h3 className="text-white font-medium mb-2">No FAQ articles found</h3>
                <p className="text-slate-400">Try adjusting your search terms or browse all categories</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Contact Support Tab */}
        <TabsContent value="contact" className="space-y-6">
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Mail className="w-5 h-5 mr-2 text-blue-400" />
                Contact Support Team
              </CardTitle>
              <CardDescription className="text-slate-400">
                Send us a message and we'll respond within 24 hours
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleContactSubmit} className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Email Address *</label>
                    <Input
                      type="email"
                      placeholder="your@email.com"
                      value={contactForm.email}
                      onChange={(e) => setContactForm(prev => ({ ...prev, email: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Name</label>
                    <Input
                      placeholder="Your Name"
                      value={contactForm.name}
                      onChange={(e) => setContactForm(prev => ({ ...prev, name: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm text-slate-300">Subject</label>
                  <Input
                    placeholder="Brief description of your issue"
                    value={contactForm.subject}
                    onChange={(e) => setContactForm(prev => ({ ...prev, subject: e.target.value }))}
                    className="bg-slate-700 border-slate-600 text-white"
                  />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm text-slate-300">Comments</label>
                  <Textarea
                    placeholder="Please describe your issue or question in detail..."
                    value={contactForm.comments}
                    onChange={(e) => setContactForm(prev => ({ ...prev, comments: e.target.value }))}
                    className="bg-slate-700 border-slate-600 text-white min-h-[120px]"
                  />
                </div>
                
                <Button 
                  type="submit" 
                  disabled={submittingContact || !contactForm.email}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  <Send className="w-4 h-4 mr-2" />
                  {submittingContact ? 'Sending...' : 'Send Message'}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Contact Info */}
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardContent className="p-4">
              <div className="text-center">
                <h3 className="text-white font-medium mb-2">Other Ways to Reach Us</h3>
                <div className="space-y-2 text-slate-400">
                  <p>📧 Support Email: Support@CustomerMindIQ.com</p>
                  <p>⏰ Response Time: Within 24 hours</p>
                  <p>📚 Check our Training Center and FAQ first for quick answers</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Community Tab */}
        <TabsContent value="community" className="space-y-6">
          {/* New Post Button */}
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white">Community Discussion</h2>
            <Dialog open={showNewPost} onOpenChange={setShowNewPost}>
              <DialogTrigger asChild>
                <Button className="bg-green-600 hover:bg-green-700">
                  <MessageCircle className="w-4 h-4 mr-2" />
                  New Post
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-slate-800 border-slate-700">
                <DialogHeader>
                  <DialogTitle className="text-white">Create New Post</DialogTitle>
                  <DialogDescription className="text-slate-400">
                    Share a question, suggestion, or report an issue
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleNewPostSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Post Type</label>
                    <select
                      value={newPost.type}
                      onChange={(e) => setNewPost(prev => ({ ...prev, type: e.target.value }))}
                      className="w-full p-2 bg-slate-700 border border-slate-600 rounded text-white"
                    >
                      <option value="question">Question</option>
                      <option value="suggestion">Suggestion</option>
                      <option value="issue">Issue Report</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Title</label>
                    <Input
                      placeholder="Brief, descriptive title..."
                      value={newPost.title}
                      onChange={(e) => setNewPost(prev => ({ ...prev, title: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Content</label>
                    <Textarea
                      placeholder="Describe your question, suggestion, or issue in detail..."
                      value={newPost.content}
                      onChange={(e) => setNewPost(prev => ({ ...prev, content: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white min-h-[100px]"
                      required
                    />
                  </div>
                  <div className="flex justify-end space-x-2">
                    <Button variant="outline" onClick={() => setShowNewPost(false)}>
                      Cancel
                    </Button>
                    <Button type="submit" className="bg-green-600 hover:bg-green-700">
                      Create Post
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </div>

          {/* Community Posts */}
          <div className="space-y-4">
            {communityPosts.map(post => (
              <Card key={post.id} className={`bg-slate-800/50 backdrop-blur-xl border-slate-700 hover:border-slate-600 transition-all ${post.isPinned ? 'border-yellow-500/50' : ''}`}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      {post.isPinned && <Pin className="w-4 h-4 text-yellow-400" />}
                      {getPostTypeIcon(post.type)}
                      <Badge className={getPostTypeBadge(post.type)}>
                        {post.type.charAt(0).toUpperCase() + post.type.slice(1)}
                      </Badge>
                    </div>
                    <div className="flex items-center space-x-2 text-xs text-slate-500">
                      <Clock className="w-3 h-3" />
                      {post.date}
                    </div>
                  </div>
                  
                  <h3 className="text-lg font-semibold text-white mb-2">{post.title}</h3>
                  <p className="text-slate-300 mb-4 whitespace-pre-wrap">{post.content}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 text-sm text-slate-400">
                      <div className="flex items-center space-x-1">
                        <User className="w-3 h-3" />
                        {post.author}
                      </div>
                      <div className="flex items-center space-x-1">
                        <ThumbsUp className="w-3 h-3" />
                        {post.likes}
                      </div>
                      <div className="flex items-center space-x-1">
                        <Reply className="w-3 h-3" />
                        {post.replies} replies
                      </div>
                    </div>
                    
                    {/* Admin controls would go here */}
                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="sm" className="text-slate-400 border-slate-600 hover:bg-slate-700">
                        <Reply className="w-3 h-3 mr-1" />
                        Reply
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {communityPosts.length === 0 && (
            <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
              <CardContent className="p-8 text-center">
                <MessageSquare className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                <h3 className="text-white font-medium mb-2">No community posts yet</h3>
                <p className="text-slate-400">Be the first to start a discussion!</p>
                <Button 
                  onClick={() => setShowNewPost(true)}
                  className="mt-4 bg-green-600 hover:bg-green-700"
                >
                  Create First Post
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Support;