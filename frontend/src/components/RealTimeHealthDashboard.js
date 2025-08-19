import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Heart,
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  Users,
  Clock,
  Shield,
  Activity,
  Bell,
  CheckCircle,
  XCircle,
  Eye,
  RefreshCw,
  Zap,
  Target,
  Pulse,
  Phone,
  Mail,
  MessageSquare,
  ChevronUp,
  ChevronDown,
  Calendar,
  Timer,
  BarChart3
} from 'lucide-react';

const RealTimeHealthDashboard = ({ onNavigate }) => {
  const [healthData, setHealthData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isRealTimeActive, setIsRealTimeActive] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const wsRef = useRef(null);

  // Health status color mapping
  const getHealthColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    if (score >= 40) return 'text-orange-400';
    return 'text-red-400';
  };

  const getHealthBadgeColor = (status) => {
    const colors = {
      'excellent': 'bg-green-500/20 text-green-400',
      'good': 'bg-blue-500/20 text-blue-400',
      'fair': 'bg-yellow-500/20 text-yellow-400',
      'poor': 'bg-orange-500/20 text-orange-400',
      'critical': 'bg-red-500/20 text-red-400'
    };
    return colors[status] || 'bg-gray-500/20 text-gray-400';
  };

  const getSeverityColor = (severity) => {
    const colors = {
      'low': 'bg-blue-500/20 text-blue-400',
      'medium': 'bg-yellow-500/20 text-yellow-400',
      'high': 'bg-orange-500/20 text-orange-400',
      'critical': 'bg-red-500/20 text-red-400'
    };
    return colors[severity] || 'bg-gray-500/20 text-gray-400';
  };

  // Fetch health dashboard data
  const fetchHealthData = async () => {
    try {
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/customer-health/dashboard`);
      if (!response.ok) throw new Error('Failed to fetch health data');
      
      const data = await response.json();
      setHealthData(data);
      setLastUpdate(new Date());
    } catch (err) {
      setError(err.message);
    }
  };

  // Fetch active alerts
  const fetchAlerts = async () => {
    try {
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/customer-health/alerts`);
      if (!response.ok) throw new Error('Failed to fetch alerts');
      
      const data = await response.json();
      setAlerts(data.alerts || []);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    }
  };

  // Resolve alert
  const resolveAlert = async (alertId) => {
    try {
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL}/api/customer-health/alerts/${alertId}/resolve`, {
        method: 'POST'
      });
      
      if (response.ok) {
        setAlerts(alerts.filter(alert => alert.alert_id !== alertId));
      }
    } catch (err) {
      console.error('Error resolving alert:', err);
    }
  };

  // Setup WebSocket for real-time updates
  const setupWebSocket = () => {
    if (wsRef.current) return;

    const wsUrl = `${import.meta.env.REACT_APP_BACKEND_URL}/api/customer-health/ws/health-monitoring`.replace('http', 'ws');
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      setIsRealTimeActive(true);
      console.log('Real-time health monitoring connected');
    };

    wsRef.current.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        
        if (message.type === 'health_update') {
          setHealthData(message.data);
          setLastUpdate(new Date());
        } else if (message.type === 'health_alert') {
          setAlerts(prev => [message.data, ...prev.slice(0, 9)]); // Keep latest 10 alerts
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    wsRef.current.onclose = () => {
      setIsRealTimeActive(false);
      wsRef.current = null;
      // Attempt to reconnect after 5 seconds
      setTimeout(setupWebSocket, 5000);
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsRealTimeActive(false);
    };
  };

  // Initial data load
  useEffect(() => {
    const initializeData = async () => {
      setLoading(true);
      await Promise.all([fetchHealthData(), fetchAlerts()]);
      setLoading(false);
    };

    initializeData();
    setupWebSocket();

    // Cleanup WebSocket on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-400 mx-auto mb-4" />
          <p className="text-slate-400">Loading real-time health data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert className="bg-red-500/20 border-red-500/30">
        <AlertTriangle className="h-5 w-5 text-red-400" />
        <AlertDescription className="text-red-300">
          Failed to load health dashboard: {error}
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white flex items-center">
            <Heart className="w-10 h-10 mr-4 text-red-400" />
            Real-Time Customer Health
          </h1>
          <p className="text-slate-400 mt-2 text-lg">
            Live customer health monitoring with AI-powered alerts and intervention recommendations
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Badge className={`text-sm px-3 py-1 ${isRealTimeActive ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            <Pulse className="w-4 h-4 mr-1" />
            {isRealTimeActive ? 'Live Monitoring' : 'Disconnected'}
          </Badge>
          {lastUpdate && (
            <Badge className="bg-blue-500/20 text-blue-400 text-sm px-3 py-1">
              <Clock className="w-4 h-4 mr-1" />
              Updated {lastUpdate.toLocaleTimeString()}
            </Badge>
          )}
        </div>
      </div>

      {/* Health Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {healthData?.summary?.total_customers || 0}
                </div>
                <div className="text-xs text-blue-200">Customers Monitored</div>
              </div>
              <Users className="h-8 w-8 text-blue-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {healthData?.summary?.average_health_score || 0}
                </div>
                <div className="text-xs text-green-200">Average Health Score</div>
              </div>
              <Activity className="h-8 w-8 text-green-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {healthData?.summary?.at_risk_customers || 0}
                </div>
                <div className="text-xs text-orange-200">At Risk Customers</div>
              </div>
              <AlertTriangle className="h-8 w-8 text-orange-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-red-600/20 to-red-800/20 border-red-500/30">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {healthData?.summary?.active_alerts || 0}
                </div>
                <div className="text-xs text-red-200">Active Alerts</div>
              </div>
              <Bell className="h-8 w-8 text-red-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Health Distribution & Trends */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Health Distribution */}
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-blue-400" />
              Health Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {healthData?.health_distribution && Object.entries(healthData.health_distribution).map(([status, count]) => (
                <div key={status} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Badge className={`mr-3 ${getHealthBadgeColor(status)}`}>
                      {status.charAt(0).toUpperCase() + status.slice(1)}
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="text-white font-semibold">{count}</div>
                    <div className="w-24 bg-slate-700 rounded-full h-2">
                      <div 
                        className="bg-blue-400 h-2 rounded-full"
                        style={{ width: `${(count / (healthData?.summary?.total_customers || 1)) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Trend Analysis */}
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-400" />
              Health Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {healthData?.trends && Object.entries(healthData.trends).map(([trend, count]) => {
                const TrendIcon = trend === 'improving' ? TrendingUp : trend === 'declining' ? TrendingDown : Activity;
                const trendColor = trend === 'improving' ? 'text-green-400' : trend === 'declining' ? 'text-red-400' : 'text-blue-400';
                
                return (
                  <div key={trend} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <TrendIcon className={`w-5 h-5 mr-3 ${trendColor}`} />
                      <span className="text-slate-300 capitalize">{trend}</span>
                    </div>
                    <div className="text-white font-semibold">{count}</div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Top Risk Customers */}
      {healthData?.top_risk_customers && healthData.top_risk_customers.length > 0 && (
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Shield className="w-5 h-5 mr-2 text-red-400" />
              Top Risk Customers - Immediate Attention Required
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {healthData.top_risk_customers.map((customer, index) => (
                <div key={customer.customer_id} className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center mr-3">
                        <span className="text-red-400 font-bold">{index + 1}</span>
                      </div>
                      <div>
                        <div className="text-white font-semibold">Customer {customer.customer_id}</div>
                        <div className={`text-sm font-medium ${getHealthColor(customer.health_score)}`}>
                          Health Score: {customer.health_score}/100
                        </div>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                        <Eye className="w-4 h-4 mr-1" />
                        View
                      </Button>
                      <Button size="sm" className="bg-green-600 hover:bg-green-700">
                        <Phone className="w-4 h-4 mr-1" />
                        Contact
                      </Button>
                    </div>
                  </div>
                  
                  <div className="mb-3">
                    <Progress value={customer.health_score} className="h-2" />
                  </div>
                  
                  {customer.risk_factors && customer.risk_factors.length > 0 && (
                    <div>
                      <div className="text-sm text-slate-400 mb-2">Key Risk Factors:</div>
                      <div className="flex flex-wrap gap-2">
                        {customer.risk_factors.map((factor, idx) => (
                          <Badge key={idx} className="bg-red-500/20 text-red-300 text-xs">
                            {factor}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Active Alerts */}
      {alerts.length > 0 && (
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Bell className="w-5 h-5 mr-2 text-yellow-400" />
              Active Health Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {alerts.map((alert) => (
                <div key={alert.alert_id} className="bg-slate-700/50 border border-slate-600 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <Badge className={`mr-3 ${getSeverityColor(alert.severity)}`}>
                        {alert.severity.toUpperCase()}
                      </Badge>
                      <div>
                        <div className="text-white font-medium">Customer {alert.customer_id}</div>
                        <div className="text-slate-400 text-sm">
                          {new Date(alert.created_at).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => resolveAlert(alert.alert_id)}
                        className="border-green-500/30 text-green-400 hover:bg-green-500/20"
                      >
                        <CheckCircle className="w-4 h-4 mr-1" />
                        Resolve
                      </Button>
                    </div>
                  </div>
                  
                  <div className="text-slate-300 mb-3">{alert.message}</div>
                  
                  {alert.escalation_level > 0 && (
                    <Badge className="bg-orange-500/20 text-orange-400">
                      Escalation Level {alert.escalation_level}
                    </Badge>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Monitor Individual Customer</h3>
                <p className="text-slate-400 text-sm">Deep dive into specific customer health</p>
              </div>
              <Button 
                onClick={() => onNavigate('customers')}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Target className="w-4 h-4 mr-2" />
                Monitor
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Create Intervention Campaign</h3>
                <p className="text-slate-400 text-sm">Launch targeted outreach for at-risk customers</p>
              </div>
              <Button 
                onClick={() => onNavigate('create')}
                className="bg-purple-600 hover:bg-purple-700"
              >
                <Zap className="w-4 h-4 mr-2" />
                Create
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Health Analytics</h3>
                <p className="text-slate-400 text-sm">View detailed health trends and patterns</p>
              </div>
              <Button 
                onClick={() => onNavigate('analytics')}
                className="bg-green-600 hover:bg-green-700"
              >
                <BarChart3 className="w-4 h-4 mr-2" />
                Analyze
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Status Footer */}
      <div className="text-center text-slate-500 text-sm">
        Real-time customer health monitoring powered by AI analysis and predictive analytics
      </div>
    </div>
  );
};

export default RealTimeHealthDashboard;