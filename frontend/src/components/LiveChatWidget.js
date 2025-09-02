import React, { useState, useEffect, useRef } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { 
  MessageCircle, 
  X, 
  Send, 
  Minimize2, 
  User, 
  Clock,
  CheckCircle,
  AlertCircle,
  Crown
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const LiveChatWidget = () => {
  const { user, apiCall } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [hasAccess, setHasAccess] = useState(false);
  const [accessLoading, setAccessLoading] = useState(true);
  const [chatSession, setChatSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [adminAvailable, setAdminAvailable] = useState(false);
  const [estimatedWait, setEstimatedWait] = useState('');
  const messagesEndRef = useRef(null);

  // Check chat access on component mount
  useEffect(() => {
    checkChatAccess();
    checkAdminAvailability();
  }, [user]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkChatAccess = async () => {
    try {
      setAccessLoading(true);
      const response = await apiCall('/api/chat/access-check');
      const data = await response.json();
      
      setHasAccess(data.has_access);
    } catch (error) {
      console.error('Error checking chat access:', error);
      setHasAccess(false);
    } finally {
      setAccessLoading(false);
    }
  };

  const checkAdminAvailability = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/chat/availability`);
      const data = await response.json();
      
      setAdminAvailable(data.chat_available);
      setEstimatedWait(data.estimated_wait_time);
    } catch (error) {
      console.error('Error checking admin availability:', error);
    }
  };

  const startChatSession = async () => {
    try {
      const response = await apiCall('/api/chat/start-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          initial_message: 'Hello, I need help with my account.'
        })
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        setChatSession({
          session_id: data.session_id,
          status: data.session_status,
          estimated_wait: data.estimated_wait_time
        });
        
        // Load existing messages
        loadMessages(data.session_id);
      }
    } catch (error) {
      console.error('Error starting chat session:', error);
    }
  };

  const loadMessages = async (sessionId) => {
    try {
      const response = await apiCall(`/api/chat/messages/${sessionId}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setMessages(data.messages);
        setChatSession(prev => ({
          ...prev,
          status: data.session.status,
          admin_name: data.session.admin_name
        }));
      }
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !chatSession || sending) return;
    
    try {
      setSending(true);
      
      const response = await apiCall('/api/chat/send-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: chatSession.session_id,
          message: newMessage.trim()
        })
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        // Add message to local state immediately for better UX
        const message = {
          message_id: data.message_id,
          session_id: chatSession.session_id,
          sender_type: 'user',
          sender_name: `${user.first_name} ${user.last_name}`,
          message: newMessage.trim(),
          timestamp: data.timestamp
        };
        
        setMessages(prev => [...prev, message]);
        setNewMessage('');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setSending(false);
    }
  };

  const closeChatSession = async () => {
    if (!chatSession) return;
    
    try {
      await apiCall(`/api/chat/close-session/${chatSession.session_id}`, {
        method: 'POST'
      });
      
      setChatSession(null);
      setMessages([]);
      setIsOpen(false);
    } catch (error) {
      console.error('Error closing chat session:', error);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getStatusBadge = () => {
    if (!chatSession) return null;
    
    switch (chatSession.status) {
      case 'waiting':
        return (
          <Badge className="bg-yellow-500/20 text-yellow-400">
            <Clock className="w-3 h-3 mr-1" />
            Waiting for admin
          </Badge>
        );
      case 'active':
        return (
          <Badge className="bg-green-500/20 text-green-400">
            <CheckCircle className="w-3 h-3 mr-1" />
            {chatSession.admin_name || 'Admin'} is helping
          </Badge>
        );
      case 'closed':
        return (
          <Badge className="bg-gray-500/20 text-gray-400">
            Chat closed
          </Badge>
        );
      default:
        return null;
    }
  };

  // Don't show widget if user doesn't have access
  if (accessLoading) {
    return null; // Loading
  }

  if (!hasAccess) {
    // Show upgrade prompt for restricted users
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 max-w-sm shadow-xl">
          <div className="flex items-center mb-2">
            <Crown className="w-5 h-5 text-yellow-400 mr-2" />
            <span className="text-white font-medium">Premium Live Chat</span>
          </div>
          <p className="text-slate-300 text-sm mb-3">
            Live chat support is available for Growth, Scale, and Custom plan subscribers.
          </p>
          <Button 
            size="sm" 
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600"
            onClick={() => window.location.href = '#subscription'}
          >
            Upgrade to Access Chat
          </Button>
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Chat Widget Button */}
      {!isOpen && (
        <div className="fixed bottom-4 right-4 z-50">
          <Button
            onClick={() => setIsOpen(true)}
            className="h-14 w-14 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg"
          >
            <MessageCircle className="w-6 h-6" />
          </Button>
          {adminAvailable && (
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-pulse"></div>
          )}
        </div>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={`fixed bottom-4 right-4 z-50 transition-all duration-300 ${
          isMinimized ? 'h-16' : 'h-96'
        }`}>
          <Card className="w-80 bg-slate-900 border-slate-700 shadow-xl">
            {/* Chat Header */}
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <MessageCircle className="w-5 h-5 text-blue-400" />
                  <CardTitle className="text-white text-sm">Live Chat Support</CardTitle>
                  {adminAvailable && (
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  )}
                </div>
                <div className="flex items-center space-x-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsMinimized(!isMinimized)}
                    className="h-6 w-6 p-0 text-slate-400 hover:text-white"
                  >
                    <Minimize2 className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsOpen(false)}
                    className="h-6 w-6 p-0 text-slate-400 hover:text-white"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              </div>

              {/* Status Badge and Admin Availability */}
              <div className="flex items-center justify-between text-xs">
                {getStatusBadge()}
                {!chatSession && (
                  <span className={`${adminAvailable ? 'text-green-400' : 'text-yellow-400'}`}>
                    {adminAvailable ? `Available • ${estimatedWait}` : 'Currently offline'}
                  </span>
                )}
              </div>
            </CardHeader>

            {/* Chat Content */}
            {!isMinimized && (
              <CardContent className="p-0">
                {!chatSession ? (
                  // Start Chat View
                  <div className="p-4 text-center">
                    <div className="mb-4">
                      <MessageCircle className="w-12 h-12 text-blue-400 mx-auto mb-2" />
                      <h3 className="text-white font-medium mb-1">Need Help?</h3>
                      <p className="text-slate-400 text-sm">
                        Connect with our support team for instant assistance.
                      </p>
                    </div>
                    
                    {adminAvailable ? (
                      <Button
                        onClick={startChatSession}
                        className="w-full bg-blue-600 hover:bg-blue-700"
                      >
                        Start Chat Session
                      </Button>
                    ) : (
                      <div className="text-center">
                        <AlertCircle className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                        <p className="text-slate-400 text-sm mb-3">
                          Our support team is currently offline. Please try again later or contact us via email.
                        </p>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => window.location.href = 'mailto:support@customermindiq.com'}
                        >
                          Email Support
                        </Button>
                      </div>
                    )}
                  </div>
                ) : (
                  // Chat Session View
                  <>
                    {/* Messages Area */}
                    <div className="h-64 overflow-y-auto p-4 space-y-3">
                      {messages.map((message) => (
                        <div
                          key={message.message_id}
                          className={`flex ${
                            message.sender_type === 'user' ? 'justify-end' : 'justify-start'
                          }`}
                        >
                          <div
                            className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                              message.sender_type === 'user'
                                ? 'bg-blue-600 text-white'
                                : 'bg-slate-700 text-slate-100'
                            }`}
                          >
                            <div className="font-medium text-xs mb-1 opacity-75">
                              {message.sender_type === 'user' ? 'You' : message.sender_name}
                            </div>
                            <div>{message.message}</div>
                            <div className="text-xs opacity-50 mt-1">
                              {formatTime(message.timestamp)}
                            </div>
                          </div>
                        </div>
                      ))}
                      
                      {messages.length === 0 && (
                        <div className="text-center text-slate-400 text-sm py-8">
                          {chatSession.status === 'waiting' ? (
                            <>
                              <Clock className="w-8 h-8 mx-auto mb-2 text-yellow-400" />
                              <p>Waiting for an admin to join...</p>
                              <p className="text-xs mt-1">Estimated wait: {chatSession.estimated_wait}</p>
                            </>
                          ) : (
                            <>
                              <MessageCircle className="w-8 h-8 mx-auto mb-2" />
                              <p>Start the conversation!</p>
                            </>
                          )}
                        </div>
                      )}
                      <div ref={messagesEndRef} />
                    </div>

                    {/* Message Input */}
                    <div className="p-4 border-t border-slate-700">
                      <div className="flex space-x-2">
                        <Input
                          value={newMessage}
                          onChange={(e) => setNewMessage(e.target.value)}
                          placeholder="Type your message..."
                          className="flex-1 bg-slate-800 border-slate-600 text-white"
                          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                          disabled={sending}
                        />
                        <Button
                          onClick={sendMessage}
                          disabled={!newMessage.trim() || sending}
                          size="sm"
                          className="bg-blue-600 hover:bg-blue-700"
                        >
                          <Send className="w-4 h-4" />
                        </Button>
                      </div>
                      
                      {chatSession.status === 'active' && (
                        <div className="flex justify-between items-center mt-2">
                          <span className="text-xs text-slate-400">
                            Connected to {chatSession.admin_name || 'Admin'}
                          </span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={closeChatSession}
                            className="text-xs h-6 text-slate-400 hover:text-white"
                          >
                            End Chat
                          </Button>
                        </div>
                      )}
                    </div>
                  </>
                )}
              </CardContent>
            )}
          </Card>
        </div>
      )}
    </>
  );
};

export default LiveChatWidget;