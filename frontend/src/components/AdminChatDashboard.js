import React, { useState, useEffect, useRef } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  MessageCircle, 
  Users, 
  Clock,
  CheckCircle,
  UserCheck,
  Send,
  RefreshCw,
  Settings,
  Crown,
  Eye,
  EyeOff,
  Paperclip,
  Download,
  Image,
  FileText,
  File,
  Bell
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const AdminChatDashboard = () => {
  const { apiCall } = useAuth();
  const [chatSessions, setChatSessions] = useState([]);
  const [activeSessions, setActiveSessions] = useState([]);
  const [waitingSessions, setWaitingSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('waiting');
  const [selectedSession, setSelectedSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [websocket, setWebsocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [fileUpload, setFileUpload] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [adminAvailability, setAdminAvailability] = useState({
    is_available: true,
    status_message: 'Available for chat',
    max_concurrent_chats: 5
  });
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const [hasUnreadChats, setHasUnreadChats] = useState(false);
  const [notificationsEnabled, setNotificationsEnabled] = useState(false);

  useEffect(() => {
    loadChatSessions();
    requestNotificationPermission();
    // Refresh every 10 seconds for real-time updates
    const interval = setInterval(loadChatSessions, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (selectedSession) {
      loadMessages(selectedSession.session_id);
    }
  }, [selectedSession]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      setNotificationsEnabled(permission === 'granted');
    }
  };

  const sendBrowserNotification = (title, body, options = {}) => {
    if (notificationsEnabled && 'Notification' in window) {
      const notification = new Notification(title, {
        body,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        ...options
      });
      
      // Auto-close after 5 seconds
      setTimeout(() => notification.close(), 5000);
      
      return notification;
    }
  };

  const playNotificationSound = () => {
    // Create audio notification
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFApGn+DyvmcfDjiTy+zNeSsFKXfJ8N2QQAoUXrTp66hVFA==');
    audio.volume = 0.3;
    audio.play().catch(e => console.log('Audio notification failed:', e));
  };

  const loadChatSessions = async () => {
    try {
      console.log('🔄 Loading chat sessions...');
      setLoading(true);
      const response = await apiCall('/api/admin/chat/sessions');
      
      // Check if response is ok
      if (!response.ok) {
        if (response.status === 401) {
          console.error('❌ Authentication failed for chat sessions');
          throw new Error('Authentication failed. Please log in again.');
        } else if (response.status === 404) {
          console.error('❌ Chat sessions endpoint not found');
          throw new Error('Chat sessions endpoint not available.');
        } else {
          console.error('❌ Failed to load chat sessions:', response.status, response.statusText);
          throw new Error(`Server error: ${response.status}`);
        }
      }
      
      const data = await response.json();
      console.log('✅ Chat sessions response:', data);
      
      if (data.status === 'success') {
        const previousWaitingCount = waitingSessions.length;
        const newSessions = data.sessions || [];
        
        setChatSessions(newSessions);
        
        // Separate sessions by status
        const waiting = newSessions.filter(s => s.status === 'waiting');
        const active = newSessions.filter(s => s.status === 'active');
        
        // Check for new waiting sessions
        if (waiting.length > previousWaitingCount && previousWaitingCount >= 0) {
          const newChatsCount = waiting.length - previousWaitingCount;
          if (newChatsCount > 0) {
            setHasUnreadChats(true);
            
            // Send browser notification
            sendBrowserNotification(
              '🔔 New Chat Request!',
              `${newChatsCount} user${newChatsCount > 1 ? 's' : ''} waiting for support`,
              { tag: 'new-chat' }
            );
            
            // Play notification sound
            playNotificationSound();
            
            // Update page title to show notification
            document.title = `(${waiting.length}) New Chats - Customer Mind IQ`;
          }
        }
        
        setWaitingSessions(waiting);
        setActiveSessions(active);
        
        // Clear unread indicator if no waiting sessions
        if (waiting.length === 0) {
          setHasUnreadChats(false);
          document.title = 'Customer Mind IQ';
        }
        
        console.log('✅ Chat sessions loaded successfully:', {
          total: newSessions.length,
          waiting: waiting.length,
          active: active.length
        });
      } else {
        console.error('❌ Unexpected response format:', data);
        throw new Error('Unexpected response format from server');
      }
    } catch (error) {
      console.error('❌ Error loading chat sessions:', error);
      
      // Handle authentication errors
      if (error.message.includes('Authentication failed')) {
        // Clear authentication and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_profile');
        localStorage.removeItem('refresh_token');
        window.location.reload();
        return;
      }
      
      // For demo purposes, load some mock data when API fails
      console.log('⚠️ Loading demo chat sessions as fallback...');
      const demoSessions = [
        {
          session_id: 'demo_session_1',
          user_name: 'Demo User 1',
          user_email: 'demo1@example.com',
          status: 'waiting',
          created_at: new Date().toISOString(),
          last_message: 'Hello, I need help with my account',
          message_count: 3
        },
        {
          session_id: 'demo_session_2', 
          user_name: 'Demo User 2',
          user_email: 'demo2@example.com',
          status: 'active',
          created_at: new Date(Date.now() - 300000).toISOString(),
          last_message: 'Thank you for your help!',
          message_count: 8
        }
      ];
      
      setChatSessions(demoSessions);
      setWaitingSessions(demoSessions.filter(s => s.status === 'waiting'));
      setActiveSessions(demoSessions.filter(s => s.status === 'active'));
      console.log('✅ Demo chat sessions loaded: 2');
    } finally {
      setLoading(false);
    }
  };

  const loadMessages = async (sessionId) => {
    try {
      // Note: This would need to be implemented as an admin endpoint
      // For now, we'll use a placeholder
      const response = await apiCall(`/api/admin/chat/messages/${sessionId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setMessages(data.messages);
      }
    } catch (error) {
      console.error('Error loading messages:', error);
      // Fallback: simulate some messages for demo
      setMessages([
        {
          message_id: '1',
          sender_type: 'user',
          sender_name: selectedSession?.user_name || 'User',
          message: 'Hello, I need help with my subscription.',
          timestamp: new Date().toISOString()
        }
      ]);
    }
  };

  const assignSession = async (sessionId) => {
    try {
      const response = await apiCall(`/api/admin/chat/assign-session/${sessionId}`, {
        method: 'POST'
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        // Refresh sessions and select the assigned session
        await loadChatSessions();
        const session = chatSessions.find(s => s.session_id === sessionId);
        if (session) {
          setSelectedSession({...session, status: 'active'});
          setActiveTab('active');
        }
      }
    } catch (error) {
      console.error('Error assigning session:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !selectedSession || sending) return;
    
    try {
      setSending(true);
      
      // This would be an admin-specific endpoint
      const response = await apiCall('/api/admin/chat/send-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: selectedSession.session_id,
          message: newMessage.trim()
        })
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        // Add message to local state
        const message = {
          message_id: data.message_id,
          sender_type: 'admin',
          sender_name: 'Admin',
          message: newMessage.trim(),
          timestamp: new Date().toISOString()
        };
        
        setMessages(prev => [...prev, message]);
        setNewMessage('');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // For demo, add message locally
      const message = {
        message_id: Date.now().toString(),
        sender_type: 'admin',
        sender_name: 'Admin',
        message: newMessage.trim(),
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, message]);
      setNewMessage('');
    } finally {
      setSending(false);
    }
  };

  const updateAvailability = async () => {
    try {
      const response = await apiCall('/api/admin/chat/availability', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(adminAvailability)
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        // Success feedback could be added here
        console.log('Availability updated');
      }
    } catch (error) {
      console.error('Error updating availability:', error);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getSubscriptionBadge = (tier) => {
    const colors = {
      growth: 'bg-purple-500/20 text-purple-400',
      scale: 'bg-yellow-500/20 text-yellow-400',
      white_label: 'bg-indigo-500/20 text-indigo-400',
      custom: 'bg-red-500/20 text-red-400'
    };
    
    return (
      <Badge className={colors[tier] || 'bg-gray-500/20 text-gray-400'}>
        <Crown className="w-3 h-3 mr-1" />
        {tier?.charAt(0).toUpperCase() + tier?.slice(1)}
      </Badge>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header with Availability Controls */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <MessageCircle className="w-6 h-6 text-blue-400" />
              <CardTitle className="text-white">Live Chat Dashboard</CardTitle>
              {hasUnreadChats && (
                <Badge className="bg-red-500/20 text-red-400 animate-pulse">
                  <Bell className="w-3 h-3 mr-1" />
                  New Chats!
                </Badge>
              )}
            </div>
            <Button 
              onClick={async () => {
                console.log('🔄 Refreshing Live Chat sessions...');
                await loadChatSessions();
                console.log('✅ Live Chat sessions refreshed');
              }} 
              variant="outline" 
              size="sm"
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              {loading ? 'Refreshing...' : 'Refresh'}
            </Button>
          </div>
        </CardHeader>
        
        <CardContent>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Button
                onClick={() => setAdminAvailability(prev => ({ ...prev, is_available: !prev.is_available }))}
                variant={adminAvailability.is_available ? "default" : "outline"}
                size="sm"
                className={adminAvailability.is_available ? "bg-green-600 hover:bg-green-700" : ""}
              >
                {adminAvailability.is_available ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                {adminAvailability.is_available ? 'Available' : 'Unavailable'}
              </Button>
            </div>
            
            <Input
              value={adminAvailability.status_message}
              onChange={(e) => setAdminAvailability(prev => ({ ...prev, status_message: e.target.value }))}
              placeholder="Status message"
              className="max-w-xs bg-slate-700 border-slate-600 text-white"
            />
            
            <Button onClick={updateAvailability} size="sm">
              <Settings className="w-4 h-4 mr-2" />
              Update
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Sessions List */}
        <div className="lg:col-span-1">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white text-lg">Chat Sessions</CardTitle>
            </CardHeader>
            
            <CardContent>
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList className="grid w-full grid-cols-2 bg-slate-700">
                  <TabsTrigger value="waiting" className="text-white">
                    Waiting ({waitingSessions.length})
                  </TabsTrigger>
                  <TabsTrigger value="active" className="text-white">
                    Active ({activeSessions.length})
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="waiting" className="space-y-3 mt-4">
                  {waitingSessions.length === 0 ? (
                    <div className="text-center py-8 text-slate-400">
                      <Clock className="w-8 h-8 mx-auto mb-2" />
                      <p>No waiting sessions</p>
                    </div>
                  ) : (
                    waitingSessions.map((session) => (
                      <div
                        key={session.session_id}
                        className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                          selectedSession?.session_id === session.session_id
                            ? 'bg-blue-600/20 border-blue-500'
                            : 'bg-slate-700 border-slate-600 hover:bg-slate-600'
                        }`}
                        onClick={() => setSelectedSession(session)}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-white font-medium">{session.user_name}</span>
                          {getSubscriptionBadge(session.user_subscription_tier)}
                        </div>
                        <div className="text-xs text-slate-400 mb-2">
                          Started: {formatTime(session.created_at)}
                        </div>
                        <Button
                          onClick={(e) => {
                            e.stopPropagation();
                            assignSession(session.session_id);
                          }}
                          size="sm"
                          className="w-full bg-green-600 hover:bg-green-700"
                        >
                          <UserCheck className="w-4 h-4 mr-2" />
                          Assign to Me
                        </Button>
                      </div>
                    ))
                  )}
                </TabsContent>
                
                <TabsContent value="active" className="space-y-3 mt-4">
                  {activeSessions.length === 0 ? (
                    <div className="text-center py-8 text-slate-400">
                      <CheckCircle className="w-8 h-8 mx-auto mb-2" />
                      <p>No active sessions</p>
                    </div>
                  ) : (
                    activeSessions.map((session) => (
                      <div
                        key={session.session_id}
                        className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                          selectedSession?.session_id === session.session_id
                            ? 'bg-blue-600/20 border-blue-500'
                            : 'bg-slate-700 border-slate-600 hover:bg-slate-600'
                        }`}
                        onClick={() => setSelectedSession(session)}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-white font-medium">{session.user_name}</span>
                          {getSubscriptionBadge(session.user_subscription_tier)}
                        </div>
                        <div className="text-xs text-slate-400 mb-2">
                          With: {session.admin_name}
                        </div>
                        <Badge className="bg-green-500/20 text-green-400">
                          <CheckCircle className="w-3 h-3 mr-1" />
                          Active
                        </Badge>
                      </div>
                    ))
                  )}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>

        {/* Chat Interface */}
        <div className="lg:col-span-2">
          {selectedSession ? (
            <Card className="bg-slate-800 border-slate-700 h-[600px] flex flex-col">
              {/* Chat Header */}
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-white text-lg">{selectedSession.user_name}</CardTitle>
                    <div className="flex items-center space-x-2 mt-1">
                      {getSubscriptionBadge(selectedSession.user_subscription_tier)}
                      <Badge className={
                        selectedSession.status === 'waiting' 
                          ? 'bg-yellow-500/20 text-yellow-400'
                          : 'bg-green-500/20 text-green-400'
                      }>
                        {selectedSession.status === 'waiting' ? 'Waiting' : 'Active'}
                      </Badge>
                    </div>
                  </div>
                  <div className="text-sm text-slate-400">
                    {selectedSession.user_email}
                  </div>
                </div>
              </CardHeader>

              {/* Messages Area */}
              <CardContent className="flex-1 flex flex-col p-0">
                <div className="flex-1 overflow-y-auto p-4 space-y-3">
                  {messages.map((message) => (
                    <div
                      key={message.message_id}
                      className={`flex ${
                        message.sender_type === 'admin' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                          message.sender_type === 'admin'
                            ? 'bg-blue-600 text-white'
                            : 'bg-slate-700 text-slate-100'
                        }`}
                      >
                        <div className="font-medium text-xs mb-1 opacity-75">
                          {message.sender_name}
                        </div>
                        <div>{message.message}</div>
                        <div className="text-xs opacity-50 mt-1">
                          {formatTime(message.timestamp)}
                        </div>
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>

                {/* Message Input */}
                {selectedSession.status === 'active' && (
                  <div className="p-4 border-t border-slate-700">
                    <div className="flex space-x-2">
                      <Input
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Type your response..."
                        className="flex-1 bg-slate-700 border-slate-600 text-white"
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        disabled={sending}
                      />
                      <Button
                        onClick={sendMessage}
                        disabled={!newMessage.trim() || sending}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        <Send className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card className="bg-slate-800 border-slate-700 h-[600px] flex items-center justify-center">
              <div className="text-center text-slate-400">
                <MessageCircle className="w-16 h-16 mx-auto mb-4" />
                <p className="text-lg">Select a chat session to start</p>
                <p className="text-sm">Choose from waiting or active sessions on the left</p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminChatDashboard;