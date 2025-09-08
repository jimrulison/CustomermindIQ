import React, { useState, useEffect, useRef } from 'react';
import { 
    MessageCircle, 
    Send, 
    Clock, 
    User, 
    AlertCircle,
    CheckCircle,
    Star,
    Tag,
    UserCheck,
    MessageSquare,
    RefreshCw,
    Search,
    Filter
} from 'lucide-react';

const AdminAffiliateChatManager = ({ currentAdmin }) => {
    const [chatSessions, setChatSessions] = useState([]);
    const [selectedSession, setSelectedSession] = useState(null);
    const [messages, setMessages] = useState([]);
    const [currentMessage, setCurrentMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [isConnected, setIsConnected] = useState(false);
    const [stats, setStats] = useState(null);
    const [filterStatus, setFilterStatus] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');
    
    const messagesEndRef = useRef(null);
    const wsRef = useRef(null);
    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://mindiq-portal.preview.emergentagent.com';

    useEffect(() => {
        loadChatStats();
        loadChatSessions();
        connectWebSocket();
        
        // Refresh data every 30 seconds
        const interval = setInterval(() => {
            loadChatSessions();
            loadChatStats();
        }, 30000);
        
        return () => {
            clearInterval(interval);
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    // Connect to WebSocket for real-time updates
    const connectWebSocket = () => {
        if (!currentAdmin?.email) return;

        const wsUrl = backendUrl.replace('http', 'ws') + `/api/affiliate-chat/ws/admin/${encodeURIComponent(currentAdmin.email)}`;
        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
            setIsConnected(true);
            console.log('Admin WebSocket connected');
        };

        wsRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'new_session') {
                // New chat session created
                loadChatSessions();
                loadChatStats();
                playNotificationSound();
            } else if (data.type === 'new_message') {
                // New message in existing session
                if (selectedSession && data.session_id === selectedSession.id) {
                    setMessages(prev => [...prev, data.message]);
                } else {
                    // Update session list to show unread count
                    loadChatSessions();
                }
                playNotificationSound();
            }
        };

        wsRef.current.onclose = () => {
            setIsConnected(false);
            console.log('Admin WebSocket disconnected');
            
            // Attempt to reconnect after 3 seconds
            setTimeout(() => {
                if (currentAdmin?.email) {
                    connectWebSocket();
                }
            }, 3000);
        };

        wsRef.current.onerror = (error) => {
            console.error('Admin WebSocket error:', error);
            setIsConnected(false);
        };
    };

    const playNotificationSound = () => {
        // Create notification sound for new messages
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 1000;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
        
        // Update page title
        document.title = '🔔 New Chat Message - Admin Portal';
        setTimeout(() => {
            document.title = 'Admin Portal - Customer Mind IQ';
        }, 5000);
    };

    // Load chat statistics
    const loadChatStats = async () => {
        try {
            const token = localStorage.getItem('access_token') || localStorage.getItem('token');
            const response = await fetch(`${backendUrl}/api/affiliate-chat/admin/stats`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setStats(data.stats);
            }
        } catch (error) {
            console.error('Error loading chat stats:', error);
        }
    };

    // Load chat sessions
    const loadChatSessions = async () => {
        try {
            const token = localStorage.getItem('access_token') || localStorage.getItem('token');
            let url = `${backendUrl}/api/affiliate-chat/sessions`;
            
            if (filterStatus !== 'all') {
                url += `?status=${filterStatus}`;
            }
            
            const response = await fetch(url, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setChatSessions(data.sessions || []);
            }
        } catch (error) {
            console.error('Error loading chat sessions:', error);
        } finally {
            setLoading(false);
        }
    };

    // Load messages for selected session
    const loadSessionMessages = async (sessionId) => {
        try {
            const token = localStorage.getItem('access_token') || localStorage.getItem('token');
            const response = await fetch(`${backendUrl}/api/affiliate-chat/sessions/${sessionId}/messages`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setMessages(data.messages || []);
                setSelectedSession(data.session);
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    };

    // Send message
    const sendMessage = async () => {
        if (!currentMessage.trim() || !selectedSession) return;

        const messageText = currentMessage.trim();
        setCurrentMessage('');

        try {
            const token = localStorage.getItem('access_token') || localStorage.getItem('token');
            const response = await fetch(`${backendUrl}/api/affiliate-chat/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    session_id: selectedSession.id,
                    content: messageText,
                    message_type: 'text'
                })
            });

            const data = await response.json();
            
            if (data.success) {
                // Add message to UI immediately
                setMessages(prev => [...prev, {
                    id: data.message_id || Date.now().toString(),
                    sender_type: 'admin',
                    sender_name: currentAdmin?.name || 'Admin',
                    content: messageText,
                    timestamp: new Date().toISOString()
                }]);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message. Please try again.');
        }
    };

    // Update chat session status
    const updateSessionStatus = async (sessionId, status) => {
        try {
            const token = localStorage.getItem('access_token') || localStorage.getItem('token');
            const response = await fetch(`${backendUrl}/api/affiliate-chat/sessions/${sessionId}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    status: status,
                    assigned_admin: currentAdmin?.email
                })
            });

            if (response.ok) {
                loadChatSessions();
                if (selectedSession && selectedSession.id === sessionId) {
                    setSelectedSession(prev => ({ ...prev, status }));
                }
            }
        } catch (error) {
            console.error('Error updating session status:', error);
        }
    };

    // Filter sessions based on search term
    const filteredSessions = chatSessions.filter(session => {
        if (searchTerm) {
            return session.affiliate_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                   session.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                   session.affiliate_email.toLowerCase().includes(searchTerm.toLowerCase());
        }
        return true;
    });

    const getStatusColor = (status) => {
        switch (status) {
            case 'waiting': return 'text-yellow-600 bg-yellow-100';
            case 'active': return 'text-green-600 bg-green-100';
            case 'resolved': return 'text-blue-600 bg-blue-100';
            case 'closed': return 'text-gray-600 bg-gray-100';
            default: return 'text-gray-600 bg-gray-100';
        }
    };

    const getPriorityColor = (priority) => {
        switch (priority) {
            case 'urgent': return 'text-red-600 bg-red-100';
            case 'high': return 'text-orange-600 bg-orange-100';
            case 'normal': return 'text-blue-600 bg-blue-100';
            case 'low': return 'text-green-600 bg-green-100';
            default: return 'text-gray-600 bg-gray-100';
        }
    };

    if (loading) {
        return (
            <div className="p-6 text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-2 text-gray-600">Loading affiliate chats...</p>
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col">
            {/* Stats Header */}
            {stats && (
                <div className="bg-white p-4 border-b">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center">
                            <div className="text-2xl font-bold text-yellow-600">{stats.waiting_sessions}</div>
                            <div className="text-sm text-gray-600">Waiting</div>
                        </div>
                        <div className="text-center">
                            <div className="text-2xl font-bold text-green-600">{stats.active_sessions}</div>
                            <div className="text-sm text-gray-600">Active</div>
                        </div>
                        <div className="text-center">
                            <div className="text-2xl font-bold text-blue-600">{stats.today_sessions}</div>
                            <div className="text-sm text-gray-600">Today</div>
                        </div>
                        <div className="text-center">
                            <div className="text-2xl font-bold text-purple-600">{stats.avg_response_time_minutes}m</div>
                            <div className="text-sm text-gray-600">Avg Response</div>
                        </div>
                    </div>
                </div>
            )}

            <div className="flex flex-1 overflow-hidden">
                {/* Sessions List */}
                <div className="w-1/3 border-r bg-white">
                    <div className="p-4 border-b">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-semibold">Affiliate Chats</h2>
                            <div className="flex items-center">
                                <div className={`w-2 h-2 rounded-full mr-2 ${
                                    isConnected ? 'bg-green-500' : 'bg-red-500'
                                }`} />
                                <button
                                    onClick={() => {
                                        loadChatSessions();
                                        loadChatStats();
                                    }}
                                    className="p-1 hover:bg-gray-100 rounded"
                                >
                                    <RefreshCw className="h-4 w-4" />
                                </button>
                            </div>
                        </div>
                        
                        {/* Search */}
                        <div className="mb-4">
                            <div className="relative">
                                <Search className="h-4 w-4 absolute left-3 top-3 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Search chats..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>
                        </div>
                        
                        {/* Status Filter */}
                        <div className="mb-4">
                            <select
                                value={filterStatus}
                                onChange={(e) => setFilterStatus(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="all">All Chats</option>
                                <option value="waiting">Waiting</option>
                                <option value="active">Active</option>
                                <option value="resolved">Resolved</option>
                                <option value="closed">Closed</option>
                            </select>
                        </div>
                    </div>
                    
                    <div className="overflow-y-auto h-full">
                        {filteredSessions.map((session) => (
                            <div
                                key={session.id}
                                onClick={() => loadSessionMessages(session.id)}
                                className={`p-4 border-b cursor-pointer hover:bg-gray-50 ${
                                    selectedSession?.id === session.id ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                                }`}
                            >
                                <div className="flex items-start justify-between mb-2">
                                    <div className="font-medium text-sm">{session.affiliate_name}</div>
                                    <div className="flex items-center space-x-1">
                                        <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(session.status)}`}>
                                            {session.status}
                                        </span>
                                        {session.unread_count_admin > 0 && (
                                            <div className="bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                                                {session.unread_count_admin}
                                            </div>
                                        )}
                                    </div>
                                </div>
                                
                                <div className="text-sm text-gray-600 mb-2 truncate">
                                    {session.subject}
                                </div>
                                
                                <div className="flex items-center justify-between text-xs text-gray-500">
                                    <span>{new Date(session.updated_at).toLocaleDateString()}</span>
                                    <span className={`px-2 py-1 rounded-full ${getPriorityColor(session.priority)}`}>
                                        {session.priority}
                                    </span>
                                </div>
                            </div>
                        ))}
                        
                        {filteredSessions.length === 0 && (
                            <div className="p-8 text-center text-gray-500">
                                <MessageCircle className="h-12 w-12 mx-auto mb-4 opacity-50" />
                                <p>No chat sessions found</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 flex flex-col">
                    {selectedSession ? (
                        <>
                            {/* Chat Header */}
                            <div className="bg-white p-4 border-b">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <h3 className="font-semibold">{selectedSession.affiliate_name}</h3>
                                        <p className="text-sm text-gray-600">{selectedSession.subject}</p>
                                    </div>
                                    
                                    <div className="flex items-center space-x-2">
                                        <button
                                            onClick={() => updateSessionStatus(selectedSession.id, 'active')}
                                            className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                                        >
                                            Mark Active
                                        </button>
                                        <button
                                            onClick={() => updateSessionStatus(selectedSession.id, 'resolved')}
                                            className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                                        >
                                            Resolve
                                        </button>
                                        <button
                                            onClick={() => updateSessionStatus(selectedSession.id, 'closed')}
                                            className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
                                        >
                                            Close
                                        </button>
                                    </div>
                                </div>
                            </div>
                            
                            {/* Messages */}
                            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                                {messages.map((message) => (
                                    <div
                                        key={message.id}
                                        className={`flex ${message.sender_type === 'admin' ? 'justify-end' : 'justify-start'}`}
                                    >
                                        <div className={`max-w-md px-4 py-2 rounded-lg ${
                                            message.sender_type === 'admin'
                                                ? 'bg-blue-600 text-white'
                                                : 'bg-gray-200 text-gray-800'
                                        }`}>
                                            <div className="flex items-center mb-1">
                                                <User className="h-3 w-3 mr-1" />
                                                <span className="text-xs font-medium">
                                                    {message.sender_name}
                                                </span>
                                                <span className="text-xs opacity-75 ml-2">
                                                    {new Date(message.timestamp).toLocaleTimeString()}
                                                </span>
                                            </div>
                                            <p className="text-sm">{message.content}</p>
                                        </div>
                                    </div>
                                ))}
                                <div ref={messagesEndRef} />
                            </div>
                            
                            {/* Message Input */}
                            <div className="bg-white border-t p-4">
                                <div className="flex items-center space-x-2">
                                    <input
                                        type="text"
                                        value={currentMessage}
                                        onChange={(e) => setCurrentMessage(e.target.value)}
                                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                                        placeholder="Type your response..."
                                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                    <button
                                        onClick={sendMessage}
                                        disabled={!currentMessage.trim()}
                                        className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        <Send className="h-4 w-4" />
                                    </button>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="flex-1 flex items-center justify-center bg-gray-50">
                            <div className="text-center">
                                <MessageCircle className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                                <p className="text-gray-600">Select a chat to start messaging</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminAffiliateChatManager;