import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Alert, AlertDescription } from './ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
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
  Reply,
  Headphones,
  Phone,
  Crown,
  Star,
  Users,
  Zap,
  Shield,
  Calendar,
  Eye,
  Loader2,
  FileText,
  PlusCircle
} from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const SupportEnhanced = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('tickets');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Support tier information
  const [supportTierInfo, setSupportTierInfo] = useState(null);
  
  // Tickets state
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [showCreateTicket, setShowCreateTicket] = useState(false);
  const [showTicketDetails, setShowTicketDetails] = useState(false);

  // Forms state
  const [createTicketForm, setCreateTicketForm] = useState({
    subject: '',
    message: '',
    category: 'general',
    priority: 'medium'
  });
  
  const [responseForm, setResponseForm] = useState({
    message: ''
  });

  // Live chat state
  const [liveChatSession, setLiveChatSession] = useState(null);
  const [showLiveChat, setShowLiveChat] = useState(false);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    };
  };

  // Load support data
  useEffect(() => {
    if (user) {
      loadSupportTierInfo();
      loadUserTickets();
    }
  }, [user]);

  const loadSupportTierInfo = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/support/tier-info`, {
        headers: getAuthHeaders()
      });
      setSupportTierInfo(response.data);
    } catch (error) {
      console.error('Failed to load support tier info:', error);
    }
  };

  const loadUserTickets = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${backendUrl}/api/support/tickets/my`, {
        headers: getAuthHeaders()
      });
      setTickets(response.data.tickets || []);
    } catch (error) {
      console.error('Failed to load tickets:', error);
      setError('Failed to load support tickets');
    } finally {
      setLoading(false);
    }
  };

  const createTicket = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError('');

      const response = await axios.post(`${backendUrl}/api/support/tickets/create`, createTicketForm, {
        headers: getAuthHeaders()
      });

      if (response.data.status === 'success') {
        setShowCreateTicket(false);
        setCreateTicketForm({
          subject: '',
          message: '',
          category: 'general',
          priority: 'medium'
        });
        loadUserTickets();
        
        alert(`Support ticket created successfully! Ticket #${response.data.ticket.ticket_id.slice(-8)}`);
      }
    } catch (error) {
      console.error('Failed to create ticket:', error);
      setError('Failed to create support ticket');
    } finally {
      setLoading(false);
    }
  };

  const viewTicketDetails = async (ticket) => {
    try {
      const response = await axios.get(`${backendUrl}/api/support/tickets/${ticket.ticket_id}`, {
        headers: getAuthHeaders()
      });
      setSelectedTicket(response.data.ticket);
      setShowTicketDetails(true);
    } catch (error) {
      console.error('Failed to load ticket details:', error);
      setError('Failed to load ticket details');
    }
  };

  const addTicketResponse = async (e) => {
    e.preventDefault();
    if (!selectedTicket || !responseForm.message.trim()) return;

    try {
      setLoading(true);
      await axios.post(`${backendUrl}/api/support/tickets/${selectedTicket.ticket_id}/respond`, responseForm, {
        headers: getAuthHeaders()
      });

      setResponseForm({ message: '' });
      
      // Reload ticket details
      const response = await axios.get(`${backendUrl}/api/support/tickets/${selectedTicket.ticket_id}`, {
        headers: getAuthHeaders()
      });
      setSelectedTicket(response.data.ticket);
      loadUserTickets();
    } catch (error) {
      console.error('Failed to add response:', error);
      setError('Failed to add response');
    } finally {
      setLoading(false);
    }
  };

  const startLiveChat = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${backendUrl}/api/support/live-chat/start`, {}, {
        headers: getAuthHeaders()
      });

      if (response.data.status === 'success') {
        setLiveChatSession(response.data.session);
        setShowLiveChat(true);
      }
    } catch (error) {
      console.error('Failed to start live chat:', error);
      if (error.response?.status === 403) {
        alert('Live chat is not available for your current subscription tier. Please upgrade to Professional or Enterprise.');
      } else if (error.response?.status === 503) {
        alert('Live chat is only available during business hours (9am-6pm EST).');
      } else {
        setError('Failed to start live chat');
      }
    } finally {
      setLoading(false);
    }
  };

  const closeTicket = async (ticketId, rating = null) => {
    try {
      const params = rating ? `?satisfaction_rating=${rating}` : '';
      await axios.post(`${backendUrl}/api/support/tickets/${ticketId}/close${params}`, {}, {
        headers: getAuthHeaders()
      });
      
      loadUserTickets();
      if (selectedTicket?.ticket_id === ticketId) {
        setShowTicketDetails(false);
        setSelectedTicket(null);
      }
    } catch (error) {
      console.error('Failed to close ticket:', error);
      setError('Failed to close ticket');
    }
  };

  const getSupportTierIcon = (tier) => {
    switch (tier) {
      case 'basic': return <Users className="w-5 h-5 text-blue-500" />;
      case 'professional': return <Star className="w-5 h-5 text-purple-500" />;
      case 'enterprise': return <Crown className="w-5 h-5 text-yellow-500" />;
      default: return <HelpCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'waiting_customer': return 'bg-yellow-100 text-yellow-800';
      case 'resolved': return 'bg-purple-100 text-purple-800';
      case 'closed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (!user) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <Card>
          <CardContent className="p-8 text-center">
            <Shield className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Login Required</h2>
            <p className="text-gray-600">Please log in to access customer support.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header with Support Tier Information */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-200 p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-white rounded-lg shadow-sm">
              <Headphones className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">CustomerMind IQ Support</h1>
              <p className="text-gray-600">Get help from our expert support team</p>
            </div>
          </div>
          
          {supportTierInfo && (
            <div className="text-right">
              <div className="flex items-center space-x-2 mb-2">
                {getSupportTierIcon(supportTierInfo.support_tier)}
                <span className="font-semibold text-gray-900 capitalize">
                  {supportTierInfo.support_tier} Support
                </span>
              </div>
              <div className="text-sm text-gray-600">
                <div className="flex items-center space-x-2">
                  <Clock className="w-4 h-4" />
                  <span>Response within {supportTierInfo.tier_info?.response_time_hours}h</span>
                </div>
                {supportTierInfo.tier_info?.live_chat && (
                  <div className="flex items-center space-x-2 mt-1">
                    <MessageCircle className="w-4 h-4" />
                    <span>Live chat: {supportTierInfo.tier_info.live_chat_hours}</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <Alert className="border-red-200 bg-red-50">
          <AlertTriangle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-800">{error}</AlertDescription>
        </Alert>
      )}

      {/* Main Support Interface */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="tickets" className="flex items-center space-x-2">
            <FileText className="w-4 h-4" />
            <span>My Tickets</span>
          </TabsTrigger>
          <TabsTrigger value="create" className="flex items-center space-x-2">
            <PlusCircle className="w-4 h-4" />
            <span>Create Ticket</span>
          </TabsTrigger>
          <TabsTrigger value="live-chat" className="flex items-center space-x-2">
            <MessageCircle className="w-4 h-4" />
            <span>Live Chat</span>
          </TabsTrigger>
          <TabsTrigger value="faq" className="flex items-center space-x-2">
            <HelpCircle className="w-4 h-4" />
            <span>FAQ</span>
          </TabsTrigger>
        </TabsList>

        {/* My Tickets Tab */}
        <TabsContent value="tickets" className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold">My Support Tickets</h2>
            <Button onClick={() => setActiveTab('create')}>
              <PlusCircle className="w-4 h-4 mr-2" />
              Create New Ticket
            </Button>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin mr-2" />
              <span>Loading tickets...</span>
            </div>
          ) : tickets.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No Support Tickets</h3>
                <p className="text-gray-600 mb-4">You haven't created any support tickets yet.</p>
                <Button onClick={() => setActiveTab('create')}>
                  Create Your First Ticket
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {tickets.map((ticket) => (
                <Card key={ticket.ticket_id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div>
                          <CardTitle className="text-lg">{ticket.subject}</CardTitle>
                          <CardDescription>
                            Ticket #{ticket.ticket_id.slice(-8)} • Created {new Date(ticket.created_at).toLocaleDateString()}
                          </CardDescription>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={getStatusColor(ticket.status)}>
                          {ticket.status.replace('_', ' ')}
                        </Badge>
                        <Badge className={getPriorityColor(ticket.priority)}>
                          {ticket.priority}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4 line-clamp-2">{ticket.message}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>Category: {ticket.category.replace('_', ' ')}</span>
                        <span>Responses: {ticket.responses?.length || 0}</span>
                        <span>Due: {new Date(ticket.due_date).toLocaleDateString()}</span>
                      </div>
                      <div className="flex space-x-2">
                        <Button variant="outline" size="sm" onClick={() => viewTicketDetails(ticket)}>
                          <Eye className="w-4 h-4 mr-1" />
                          View
                        </Button>
                        {ticket.status !== 'closed' && (
                          <Button variant="outline" size="sm" onClick={() => closeTicket(ticket.ticket_id)}>
                            <CheckCircle className="w-4 h-4 mr-1" />
                            Close
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        {/* Create Ticket Tab */}
        <TabsContent value="create">
          <Card>
            <CardHeader>
              <CardTitle>Create Support Ticket</CardTitle>
              <CardDescription>
                Describe your issue and we'll get back to you within {supportTierInfo?.tier_info?.response_time_hours || 24} hours
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={createTicket} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Subject</label>
                  <Input
                    type="text"
                    value={createTicketForm.subject}
                    onChange={(e) => setCreateTicketForm({...createTicketForm, subject: e.target.value})}
                    placeholder="Brief description of your issue"
                    required
                    minLength={5}
                    maxLength={200}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Category</label>
                    <Select 
                      value={createTicketForm.category} 
                      onValueChange={(value) => setCreateTicketForm({...createTicketForm, category: value})}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="technical">Technical Issue</SelectItem>
                        <SelectItem value="billing">Billing Question</SelectItem>
                        <SelectItem value="feature_request">Feature Request</SelectItem>
                        <SelectItem value="bug_report">Bug Report</SelectItem>
                        <SelectItem value="account">Account Issue</SelectItem>
                        <SelectItem value="general">General Question</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Priority</label>
                    <Select 
                      value={createTicketForm.priority} 
                      onValueChange={(value) => setCreateTicketForm({...createTicketForm, priority: value})}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="low">Low</SelectItem>
                        <SelectItem value="medium">Medium</SelectItem>
                        <SelectItem value="high">High</SelectItem>
                        <SelectItem value="urgent">Urgent</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Message</label>
                  <Textarea
                    value={createTicketForm.message}
                    onChange={(e) => setCreateTicketForm({...createTicketForm, message: e.target.value})}
                    placeholder="Please provide detailed information about your issue..."
                    rows={6}
                    required
                    minLength={10}
                    maxLength={5000}
                  />
                </div>

                <Button type="submit" disabled={loading} className="w-full">
                  {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                  Create Support Ticket
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Live Chat Tab */}
        <TabsContent value="live-chat">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageCircle className="w-5 h-5" />
                <span>Live Chat Support</span>
              </CardTitle>
              <CardDescription>
                {supportTierInfo?.tier_info?.live_chat ? 
                  `Get instant help during business hours (${supportTierInfo.tier_info.live_chat_hours})` :
                  'Live chat is available for Professional and Enterprise subscribers'
                }
              </CardDescription>
            </CardHeader>
            <CardContent>
              {supportTierInfo?.tier_info?.live_chat ? (
                <div className="space-y-4">
                  {!liveChatSession ? (
                    <div className="text-center py-8">
                      <MessageCircle className="w-16 h-16 text-blue-400 mx-auto mb-4" />
                      <h3 className="text-lg font-semibold mb-2">Start Live Chat</h3>
                      <p className="text-gray-600 mb-4">
                        Connect with our support team for immediate assistance
                      </p>
                      <Button onClick={startLiveChat} disabled={loading}>
                        {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                        Start Chat Session
                      </Button>
                    </div>
                  ) : (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="font-medium">Chat Session Active</span>
                      </div>
                      <p className="text-sm text-gray-600">
                        Session ID: {liveChatSession.session_id.slice(-8)}
                      </p>
                      <p className="text-sm text-gray-600">
                        Status: {liveChatSession.status}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Crown className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Upgrade for Live Chat</h3>
                  <p className="text-gray-600 mb-4">
                    Live chat support is available for Professional and Enterprise subscribers
                  </p>
                  <div className="space-y-2">
                    <div className="text-sm text-gray-500">
                      Professional: 12-hour response + live chat during business hours
                    </div>
                    <div className="text-sm text-gray-500">
                      Enterprise: 4-hour response + live chat + phone support
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* FAQ Tab */}
        <TabsContent value="faq">
          <Card>
            <CardHeader>
              <CardTitle>Frequently Asked Questions</CardTitle>
              <CardDescription>Find quick answers to common questions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Alert>
                  <Info className="h-4 w-4" />
                  <AlertDescription>
                    For more detailed information, check out our comprehensive training materials in the Training section.
                  </AlertDescription>
                </Alert>
                
                <div className="text-center py-8">
                  <Book className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">FAQ Coming Soon</h3>
                  <p className="text-gray-600">
                    We're building a comprehensive FAQ section. For now, please create a support ticket for any questions.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Ticket Details Modal */}
      <Dialog open={showTicketDetails} onOpenChange={setShowTicketDetails}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          {selectedTicket && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center justify-between">
                  <span>{selectedTicket.subject}</span>
                  <Badge className={getStatusColor(selectedTicket.status)}>
                    {selectedTicket.status.replace('_', ' ')}
                  </Badge>
                </DialogTitle>
                <DialogDescription>
                  Ticket #{selectedTicket.ticket_id.slice(-8)} • Created {new Date(selectedTicket.created_at).toLocaleDateString()}
                </DialogDescription>
              </DialogHeader>
              
              <div className="space-y-6">
                {/* Original Message */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-2">
                    <User className="w-4 h-4 text-gray-500" />
                    <span className="text-sm font-medium">{selectedTicket.user_email}</span>
                    <span className="text-sm text-gray-500">{new Date(selectedTicket.created_at).toLocaleString()}</span>
                  </div>
                  <p className="text-gray-800">{selectedTicket.message}</p>
                </div>

                {/* Responses */}
                {selectedTicket.responses && selectedTicket.responses.length > 0 && (
                  <div className="space-y-4">
                    <h4 className="font-medium">Responses</h4>
                    {selectedTicket.responses.map((response) => (
                      <div key={response.response_id} className="bg-blue-50 rounded-lg p-4">
                        <div className="flex items-center space-x-2 mb-2">
                          <MessageSquare className="w-4 h-4 text-blue-500" />
                          <span className="text-sm font-medium">{response.created_by_name}</span>
                          <Badge variant="outline" className="text-xs">
                            {response.created_by_role || 'customer'}
                          </Badge>
                          <span className="text-sm text-gray-500">{new Date(response.created_at).toLocaleString()}</span>
                        </div>
                        <p className="text-gray-800">{response.message}</p>
                      </div>
                    ))}
                  </div>
                )}

                {/* Add Response */}
                {selectedTicket.status !== 'closed' && (
                  <form onSubmit={addTicketResponse} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Add Response</label>
                      <Textarea
                        value={responseForm.message}
                        onChange={(e) => setResponseForm({message: e.target.value})}
                        placeholder="Type your response..."
                        rows={4}
                        required
                      />
                    </div>
                    <div className="flex space-x-2">
                      <Button type="submit" disabled={loading}>
                        {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                        <Send className="w-4 h-4 mr-2" />
                        Send Response
                      </Button>
                      <Button 
                        type="button" 
                        variant="outline" 
                        onClick={() => closeTicket(selectedTicket.ticket_id)}
                      >
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Close Ticket
                      </Button>
                    </div>
                  </form>
                )}
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default SupportEnhanced;