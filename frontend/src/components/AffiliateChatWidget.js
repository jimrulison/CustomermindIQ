import React, { useState, useEffect, useRef } from 'react';
import { 
    MessageCircle, 
    Send, 
    X, 
    Minimize2, 
    Maximize2,
    User,
    Clock,
    Check,
    AlertCircle
} from 'lucide-react';

const AffiliateChatWidget = ({ affiliateId, affiliateName, affiliateEmail }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [isMinimized, setIsMinimized] = useState(false);
    const [messages, setMessages] = useState([]);
    const [currentMessage, setCurrentMessage] = useState('');
    const [sessionId, setSessionId] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [chatStatus, setChatStatus] = useState('offline'); // 'offline', 'waiting', 'active'
    const [unreadCount, setUnreadCount] = useState(0);
    
    const messagesEndRef = useRef(null);
    const wsRef = useRef(null);
    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://pagebuilder-iq.preview.emergentagent.com';

    // Scroll to bottom of messages
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Initialize WebSocket connection
    const connectWebSocket = () => {
        if (!affiliateId) return;

        const wsUrl = backendUrl.replace('http', 'ws') + `/api/affiliate-chat/ws/affiliate/${affiliateId}`;
        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
            setIsConnected(true);
            console.log('WebSocket connected');
        };

        wsRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'new_message') {
                setMessages(prev => [...prev, data.message]);
                
                // If chat is closed or minimized, show unread count
                if (!isOpen || isMinimized) {
                    setUnreadCount(prev => prev + 1);
                }
                
                // Play notification sound (optional)
                if (data.message.sender_type === 'admin') {
                    playNotificationSound();
                }
            }
        };

        wsRef.current.onclose = () => {
            setIsConnected(false);
            console.log('WebSocket disconnected');
            
            // Attempt to reconnect after 3 seconds
            setTimeout(() => {
                if (affiliateId && (isOpen || sessionId)) {
                    connectWebSocket();
                }
            }, 3000);
        };

        wsRef.current.onerror = (error) => {
            console.error('WebSocket error:', error);
            setIsConnected(false);
        };
    };

    const playNotificationSound = () => {
        // Create a simple notification sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    };

    // Start new chat session
    const startChatSession = async (subject, initialMessage) => {
        try {
            const response = await fetch(`${backendUrl}/api/affiliate-chat/sessions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    affiliate_id: affiliateId,
                    affiliate_name: affiliateName,
                    affiliate_email: affiliateEmail,
                    subject: subject,
                    initial_message: initialMessage,
                    priority: 'normal'
                })
            });

            const data = await response.json();
            
            if (data.success) {
                setSessionId(data.session_id);
                setChatStatus('waiting');
                
                // Add the initial message to UI
                setMessages([{
                    id: Date.now().toString(),
                    sender_type: 'affiliate',
                    sender_name: affiliateName,
                    content: initialMessage,
                    timestamp: new Date().toISOString()
                }]);
                
                // Connect WebSocket
                connectWebSocket();
                
                return true;
            } else {
                throw new Error(data.message || 'Failed to start chat');
            }
        } catch (error) {
            console.error('Error starting chat:', error);
            alert('Failed to start chat. Please try again.');
            return false;
        }
    };

    // Send message
    const sendMessage = async () => {
        if (!currentMessage.trim() || !sessionId) return;

        const messageText = currentMessage.trim();
        setCurrentMessage('');

        try {
            const response = await fetch(`${backendUrl}/api/affiliate-chat/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    content: messageText,
                    message_type: 'text'
                })
            });

            const data = await response.json();
            
            if (data.success) {
                // Add message to UI immediately
                setMessages(prev => [...prev, {
                    id: data.message_id || Date.now().toString(),
                    sender_type: 'affiliate',
                    sender_name: affiliateName,
                    content: messageText,
                    timestamp: new Date().toISOString()
                }]);
            } else {
                throw new Error(data.message || 'Failed to send message');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message. Please try again.');
        }
    };

    // Handle chat open
    const handleChatOpen = () => {
        setIsOpen(true);
        setUnreadCount(0);
        
        if (!sessionId) {
            // Show initial chat form
            return;
        }
        
        // Load existing messages if session exists
        loadMessages();
        
        // Connect WebSocket if not connected
        if (!isConnected) {
            connectWebSocket();
        }
    };

    // Load existing messages
    const loadMessages = async () => {
        if (!sessionId) return;

        try {
            const response = await fetch(`${backendUrl}/api/affiliate-chat/sessions/${sessionId}/messages`);
            const data = await response.json();
            
            if (data.success) {
                setMessages(data.messages || []);
                setChatStatus(data.session?.status || 'waiting');
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    };

    // Initial chat form component
    const InitialChatForm = () => {
        const [subject, setSubject] = useState('');
        const [initialMessage, setInitialMessage] = useState('');
        const [isSubmitting, setIsSubmitting] = useState(false);

        const handleSubmit = async (e) => {
            e.preventDefault();
            if (!subject.trim() || !initialMessage.trim()) return;

            setIsSubmitting(true);
            const success = await startChatSession(subject, initialMessage);
            setIsSubmitting(false);
            
            if (!success) {
                setSubject('');
                setInitialMessage('');
            }
        };

        return (
            <form onSubmit={handleSubmit} className="p-4 space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Subject
                    </label>
                    <input
                        type="text"
                        value={subject}
                        onChange={(e) => setSubject(e.target.value)}
                        placeholder="What can we help you with?"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
                
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Message
                    </label>
                    <textarea
                        value={initialMessage}
                        onChange={(e) => setInitialMessage(e.target.value)}
                        placeholder="Please describe your question or issue..."
                        rows={4}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
                
                <button
                    type="submit"
                    disabled={isSubmitting || !subject.trim() || !initialMessage.trim()}
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                    {isSubmitting ? (
                        <>
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Starting Chat...
                        </>
                    ) : (
                        <>
                            <MessageCircle className="h-4 w-4 mr-2" />
                            Start Chat
                        </>
                    )}
                </button>
            </form>
        );
    };

    // Chat messages component
    const ChatMessages = () => (
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((message) => (
                <div
                    key={message.id}
                    className={`flex ${message.sender_type === 'affiliate' ? 'justify-end' : 'justify-start'}`}
                >
                    <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.sender_type === 'affiliate'
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
            
            {chatStatus === 'waiting' && (
                <div className="text-center py-4">
                    <div className="inline-flex items-center px-4 py-2 bg-yellow-100 text-yellow-800 rounded-lg">
                        <Clock className="h-4 w-4 mr-2" />
                        Waiting for admin response...
                    </div>
                </div>
            )}
            
            <div ref={messagesEndRef} />
        </div>
    );

    // Chat input component
    const ChatInput = () => (
        <div className="border-t p-4">
            <div className="flex items-center space-x-2">
                <input
                    type="text"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Type your message..."
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
            
            <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                <div className="flex items-center">
                    <div className={`w-2 h-2 rounded-full mr-2 ${
                        isConnected ? 'bg-green-500' : 'bg-red-500'
                    }`} />
                    {isConnected ? 'Connected' : 'Disconnected'}
                </div>
                
                <div className="flex items-center">
                    {chatStatus === 'active' && (
                        <span className="text-green-600 flex items-center">
                            <Check className="h-3 w-3 mr-1" />
                            Admin online
                        </span>
                    )}
                </div>
            </div>
        </div>
    );

    if (!affiliateId) {
        return null; // Don't render if no affiliate ID
    }

    return (
        <>
            {/* Chat Toggle Button */}
            <button
                onClick={handleChatOpen}
                className="fixed bottom-6 right-6 bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-lg transition-all duration-200 z-50"
            >
                <MessageCircle className="h-6 w-6" />
                {unreadCount > 0 && (
                    <div className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-6 w-6 flex items-center justify-center">
                        {unreadCount}
                    </div>
                )}
            </button>

            {/* Chat Window */}
            {isOpen && (
                <div className={`fixed bottom-20 right-6 w-80 bg-white rounded-lg shadow-xl border z-50 transition-all duration-200 ${
                    isMinimized ? 'h-12' : 'h-96'
                }`}>
                    {/* Chat Header */}
                    <div className="flex items-center justify-between p-4 border-b bg-blue-600 text-white rounded-t-lg">
                        <div className="flex items-center">
                            <MessageCircle className="h-5 w-5 mr-2" />
                            <span className="font-medium">Support Chat</span>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                            <button
                                onClick={() => setIsMinimized(!isMinimized)}
                                className="p-1 hover:bg-blue-700 rounded"
                            >
                                {isMinimized ? <Maximize2 className="h-4 w-4" /> : <Minimize2 className="h-4 w-4" />}
                            </button>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-1 hover:bg-blue-700 rounded"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        </div>
                    </div>

                    {/* Chat Content */}
                    {!isMinimized && (
                        <div className="flex flex-col h-80">
                            {sessionId ? (
                                <>
                                    <ChatMessages />
                                    <ChatInput />
                                </>
                            ) : (
                                <InitialChatForm />
                            )}
                        </div>
                    )}
                </div>
            )}
        </>
    );
};

export default AffiliateChatWidget;