import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Textarea } from './ui/textarea';
import { 
  Settings,
  Megaphone,
  MessageSquare,
  Users,
  Plus,
  Trash2,
  Edit,
  Eye,
  EyeOff,
  Pin,
  PinOff,
  Calendar,
  Clock,
  AlertCircle,
  CheckCircle,
  Info
} from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Admin = () => {
  const [activeTab, setActiveTab] = useState('announcements');
  const [announcements, setAnnouncements] = useState([]);
  const [communityPosts, setCommunityPosts] = useState([]);
  const [showNewAnnouncement, setShowNewAnnouncement] = useState(false);
  const [newAnnouncement, setNewAnnouncement] = useState({
    message: '',
    type: 'info',
    active: true,
    dismissible: true
  });

  // Load data
  useEffect(() => {
    loadAnnouncements();
    loadCommunityPosts();
  }, []);

  const loadAnnouncements = async () => {
    try {
      // Fix: Use the correct backend endpoint for admin banners
      const response = await axios.get(`${API_BASE_URL}/api/admin/banners`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setAnnouncements(response.data.banners || []);
    } catch (error) {
      console.error('Error loading announcements:', error);
      // Set demo data
      setAnnouncements([
        {
          id: 1,
          message: "🎓 New Training Session: Advanced SEO Strategies - December 20, 2PM EST. Register now!",
          type: "info",
          active: true,
          dismissible: true,
          created: "2024-12-15",
          author: "Admin"
        },
        {
          id: 2,
          message: "⚠️ Scheduled maintenance on December 18, 2AM-4AM EST. Services may be temporarily unavailable.",
          type: "warning",
          active: false,
          dismissible: true,
          created: "2024-12-14",
          author: "Admin"
        },
        {
          id: 3,
          message: "🚀 New Website Intelligence Hub features now available! Check out the enhanced performance monitoring.",
          type: "info",
          active: true,
          dismissible: false,
          created: "2024-12-13",
          author: "Admin"
        }
      ]);
    }
  };

  const loadCommunityPosts = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/support/community/posts`);
      setCommunityPosts(response.data.posts || []);
    } catch (error) {
      console.error('Error loading community posts:', error);
      // Set demo data
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
          isPinned: false,
          isVisible: true
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
          isPinned: false,
          isVisible: true
        }
      ]);
    }
  };

  const handleCreateAnnouncement = async (e) => {
    e.preventDefault();
    try {
      const announcementData = {
        ...newAnnouncement,
        id: Date.now(),
        created: new Date().toISOString().split('T')[0],
        author: 'Admin'
      };

      const response = await axios.post(`${API_BASE_URL}/api/admin/announcements`, announcementData);
      setAnnouncements([announcementData, ...announcements]);
      setNewAnnouncement({ message: '', type: 'info', active: true, dismissible: true });
      setShowNewAnnouncement(false);
      alert('Announcement created successfully!');
    } catch (error) {
      console.error('Error creating announcement:', error);
      const mockAnnouncement = {
        id: Date.now(),
        ...newAnnouncement,
        created: new Date().toISOString().split('T')[0],
        author: 'Admin'
      };
      setAnnouncements([mockAnnouncement, ...announcements]);
      setNewAnnouncement({ message: '', type: 'info', active: true, dismissible: true });
      setShowNewAnnouncement(false);
      alert('Announcement created successfully!');
    }
  };

  const toggleAnnouncementStatus = async (id) => {
    try {
      const announcement = announcements.find(a => a.id === id);
      const updatedAnnouncement = { ...announcement, active: !announcement.active };
      
      await axios.put(`${API_BASE_URL}/api/admin/announcements/${id}`, updatedAnnouncement);
      setAnnouncements(announcements.map(a => a.id === id ? updatedAnnouncement : a));
    } catch (error) {
      console.error('Error updating announcement:', error);
      setAnnouncements(announcements.map(a => 
        a.id === id ? { ...a, active: !a.active } : a
      ));
    }
  };

  const deleteAnnouncement = async (id) => {
    if (!confirm('Are you sure you want to delete this announcement?')) return;
    
    try {
      await axios.delete(`${API_BASE_URL}/api/admin/announcements/${id}`);
      setAnnouncements(announcements.filter(a => a.id !== id));
    } catch (error) {
      console.error('Error deleting announcement:', error);
      setAnnouncements(announcements.filter(a => a.id !== id));
    }
  };

  const togglePostPin = async (id) => {
    try {
      const post = communityPosts.find(p => p.id === id);
      const updatedPost = { ...post, isPinned: !post.isPinned };
      
      await axios.put(`${API_BASE_URL}/api/support/community/posts/${id}`, updatedPost);
      setCommunityPosts(communityPosts.map(p => p.id === id ? updatedPost : p));
    } catch (error) {
      console.error('Error updating post:', error);
      setCommunityPosts(communityPosts.map(p => 
        p.id === id ? { ...p, isPinned: !p.isPinned } : p
      ));
    }
  };

  const togglePostVisibility = async (id) => {
    try {
      const post = communityPosts.find(p => p.id === id);
      const updatedPost = { ...post, isVisible: !post.isVisible };
      
      await axios.put(`${API_BASE_URL}/api/support/community/posts/${id}`, updatedPost);
      setCommunityPosts(communityPosts.map(p => p.id === id ? updatedPost : p));
    } catch (error) {
      console.error('Error updating post:', error);
      setCommunityPosts(communityPosts.map(p => 
        p.id === id ? { ...p, isVisible: !p.isVisible } : p
      ));
    }
  };

  const deletePost = async (id) => {
    if (!confirm('Are you sure you want to delete this community post?')) return;
    
    try {
      await axios.delete(`${API_BASE_URL}/api/support/community/posts/${id}`);
      setCommunityPosts(communityPosts.filter(p => p.id !== id));
    } catch (error) {
      console.error('Error deleting post:', error);
      setCommunityPosts(communityPosts.filter(p => p.id !== id));
    }
  };

  const getAnnouncementTypeIcon = (type) => {
    switch (type) {
      case 'warning': return <AlertCircle className="w-4 h-4 text-yellow-400" />;
      case 'error': return <AlertCircle className="w-4 h-4 text-red-400" />;
      case 'success': return <CheckCircle className="w-4 h-4 text-green-400" />;
      default: return <Info className="w-4 h-4 text-blue-400" />;
    }
  };

  const getAnnouncementTypeBadge = (type) => {
    const colors = {
      'info': 'bg-blue-500/20 text-blue-400',
      'warning': 'bg-yellow-500/20 text-yellow-400',
      'error': 'bg-red-500/20 text-red-400',
      'success': 'bg-green-500/20 text-green-400'
    };
    return colors[type] || 'bg-gray-500/20 text-gray-400';
  };

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <Settings className="w-8 h-8 mr-3 text-purple-400" />
            Admin Panel
          </h1>
          <p className="text-slate-400 mt-2">
            Manage announcements, community posts, and platform settings
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge className="bg-purple-500/20 text-purple-400">
            Admin Access
          </Badge>
        </div>
      </div>

      {/* Admin Stats Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{announcements.length}</div>
                <div className="text-xs text-blue-200">Total Announcements</div>
              </div>
              <Megaphone className="h-8 w-8 text-blue-400" />
            </div>
            <div className="mt-2 text-xs text-slate-400">
              {announcements.filter(a => a.active).length} active
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{communityPosts.length}</div>
                <div className="text-xs text-green-200">Community Posts</div>
              </div>
              <MessageSquare className="h-8 w-8 text-green-400" />
            </div>
            <div className="mt-2 text-xs text-slate-400">
              {communityPosts.filter(p => p.isPinned).length} pinned
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">247</div>
                <div className="text-xs text-purple-200">Active Users</div>
              </div>
              <Users className="h-8 w-8 text-purple-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-slate-800/50 p-1 h-auto">
          <TabsTrigger value="announcements" className="flex items-center">
            <Megaphone className="w-4 h-4 mr-2" />
            Announcements
          </TabsTrigger>
          <TabsTrigger value="community" className="flex items-center">
            <MessageSquare className="w-4 h-4 mr-2" />
            Community Moderation
          </TabsTrigger>
          <TabsTrigger value="settings" className="flex items-center">
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </TabsTrigger>
        </TabsList>

        {/* Announcements Tab */}
        <TabsContent value="announcements" className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white">Manage Announcements</h2>
            <Dialog open={showNewAnnouncement} onOpenChange={setShowNewAnnouncement}>
              <DialogTrigger asChild>
                <Button className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4 mr-2" />
                  New Announcement
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-slate-800 border-slate-700">
                <DialogHeader>
                  <DialogTitle className="text-white">Create New Announcement</DialogTitle>
                  <DialogDescription className="text-slate-400">
                    Create a banner announcement for all users
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleCreateAnnouncement} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm text-slate-300">Message</label>
                    <Textarea
                      placeholder="Enter your announcement message..."
                      value={newAnnouncement.message}
                      onChange={(e) => setNewAnnouncement(prev => ({ ...prev, message: e.target.value }))}
                      className="bg-slate-700 border-slate-600 text-white"
                      required
                    />
                  </div>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <label className="text-sm text-slate-300">Type</label>
                      <select
                        value={newAnnouncement.type}
                        onChange={(e) => setNewAnnouncement(prev => ({ ...prev, type: e.target.value }))}
                        className="w-full p-2 bg-slate-700 border border-slate-600 rounded text-white"
                      >
                        <option value="info">Info</option>
                        <option value="warning">Warning</option>
                        <option value="error">Error</option>
                        <option value="success">Success</option>
                      </select>
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm text-slate-300">Options</label>
                      <div className="space-y-2">
                        <label className="flex items-center text-sm text-slate-300">
                          <input
                            type="checkbox"
                            checked={newAnnouncement.active}
                            onChange={(e) => setNewAnnouncement(prev => ({ ...prev, active: e.target.checked }))}
                            className="mr-2"
                          />
                          Active
                        </label>
                        <label className="flex items-center text-sm text-slate-300">
                          <input
                            type="checkbox"
                            checked={newAnnouncement.dismissible}
                            onChange={(e) => setNewAnnouncement(prev => ({ ...prev, dismissible: e.target.checked }))}
                            className="mr-2"
                          />
                          Dismissible
                        </label>
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-end space-x-2">
                    <Button variant="outline" onClick={() => setShowNewAnnouncement(false)}>
                      Cancel
                    </Button>
                    <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                      Create Announcement
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </div>

          {/* Announcements List */}
          <div className="space-y-4">
            {announcements.map(announcement => (
              <Card key={announcement.id} className={`bg-slate-800/50 backdrop-blur-xl border-slate-700 ${announcement.active ? 'border-l-4 border-l-green-500' : 'border-l-4 border-l-slate-600'}`}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        {getAnnouncementTypeIcon(announcement.type)}
                        <Badge className={getAnnouncementTypeBadge(announcement.type)}>
                          {announcement.type.charAt(0).toUpperCase() + announcement.type.slice(1)}
                        </Badge>
                        {announcement.active && (
                          <Badge className="bg-green-500/20 text-green-400">Active</Badge>
                        )}
                      </div>
                      
                      <p className="text-white mb-3">{announcement.message}</p>
                      
                      <div className="flex items-center space-x-4 text-xs text-slate-400">
                        <div className="flex items-center space-x-1">
                          <Calendar className="w-3 h-3" />
                          Created: {announcement.created}
                        </div>
                        <div>Author: {announcement.author}</div>
                        <div>Dismissible: {announcement.dismissible ? 'Yes' : 'No'}</div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => toggleAnnouncementStatus(announcement.id)}
                        className={`${announcement.active ? 'text-green-400 border-green-600' : 'text-slate-400 border-slate-600'}`}
                      >
                        {announcement.active ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => deleteAnnouncement(announcement.id)}
                        className="text-red-400 border-red-600 hover:bg-red-600/20"
                      >
                        <Trash2 className="w-3 h-3" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Community Moderation Tab */}
        <TabsContent value="community" className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white">Community Moderation</h2>
            <div className="text-sm text-slate-400">
              Manage community posts, pin important discussions, and moderate content
            </div>
          </div>

          <div className="space-y-4">
            {communityPosts.map(post => (
              <Card key={post.id} className={`bg-slate-800/50 backdrop-blur-xl border-slate-700 ${post.isPinned ? 'border-l-4 border-l-yellow-500' : ''}`}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        {post.isPinned && <Pin className="w-4 h-4 text-yellow-400" />}
                        <Badge className={`${
                          post.type === 'question' ? 'bg-blue-500/20 text-blue-400' :
                          post.type === 'suggestion' ? 'bg-green-500/20 text-green-400' :
                          post.type === 'issue' ? 'bg-red-500/20 text-red-400' :
                          'bg-purple-500/20 text-purple-400'
                        }`}>
                          {post.type.charAt(0).toUpperCase() + post.type.slice(1)}
                        </Badge>
                        {!post.isVisible && (
                          <Badge className="bg-slate-500/20 text-slate-400">Hidden</Badge>
                        )}
                      </div>
                      
                      <h3 className="text-lg font-semibold text-white mb-2">{post.title}</h3>
                      <p className="text-slate-300 mb-3 line-clamp-2">{post.content}</p>
                      
                      <div className="flex items-center space-x-4 text-xs text-slate-400">
                        <div>Author: {post.author}</div>
                        <div>Date: {post.date}</div>
                        <div>Likes: {post.likes}</div>
                        <div>Replies: {post.replies}</div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => togglePostPin(post.id)}
                        className={`${post.isPinned ? 'text-yellow-400 border-yellow-600' : 'text-slate-400 border-slate-600'}`}
                      >
                        {post.isPinned ? <PinOff className="w-3 h-3" /> : <Pin className="w-3 h-3" />}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => togglePostVisibility(post.id)}
                        className={`${post.isVisible ? 'text-green-400 border-green-600' : 'text-slate-400 border-slate-600'}`}
                      >
                        {post.isVisible ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => deletePost(post.id)}
                        className="text-red-400 border-red-600 hover:bg-red-600/20"
                      >
                        <Trash2 className="w-3 h-3" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Settings Tab */}
        <TabsContent value="settings" className="space-y-6">
          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Platform Settings</CardTitle>
              <CardDescription className="text-slate-400">
                Configure platform-wide settings and preferences
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-white mb-4">General Settings</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white">Maintenance Mode</div>
                        <div className="text-sm text-slate-400">Put the platform in maintenance mode</div>
                      </div>
                      <Button variant="outline" className="border-slate-600 text-slate-300">
                        Configure
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white">User Registration</div>
                        <div className="text-sm text-slate-400">Enable or disable new user registrations</div>
                      </div>
                      <Button variant="outline" className="border-slate-600 text-slate-300">
                        Manage
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white">Email Notifications</div>
                        <div className="text-sm text-slate-400">Configure system email settings</div>
                      </div>
                      <Button variant="outline" className="border-slate-600 text-slate-300">
                        Setup
                      </Button>
                    </div>
                  </div>
                </div>
                
                <div className="pt-6 border-t border-slate-700">
                  <h3 className="text-lg font-medium text-white mb-4">Support Settings</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white">Support Email</div>
                        <div className="text-sm text-slate-400">Current: Support@CustomerMindIQ.com</div>
                      </div>
                      <Button variant="outline" className="border-slate-600 text-slate-300">
                        Change
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white">Auto-Response</div>
                        <div className="text-sm text-slate-400">Automatic responses to support requests</div>
                      </div>
                      <Button variant="outline" className="border-slate-600 text-slate-300">
                        Configure
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Admin;