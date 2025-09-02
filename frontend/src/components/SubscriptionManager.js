import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  CheckCircle, 
  XCircle, 
  CreditCard, 
  Crown, 
  Star,
  Users,
  BarChart3,
  Shield,
  Headphones,
  Zap,
  ArrowRight,
  Loader2
} from 'lucide-react';

const SubscriptionManager = () => {
  const [currentSubscription, setCurrentSubscription] = useState(null);
  const [subscriptionPlans, setSubscriptionPlans] = useState({});
  const [loading, setLoading] = useState(true);
  const [processingPayment, setProcessingPayment] = useState(null);
  const [transactionHistory, setTransactionHistory] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSubscriptionData();
    loadTransactionHistory();
    
    // Check for returning from Stripe
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    if (sessionId) {
      pollPaymentStatus(sessionId);
    }
  }, []);

  const loadSubscriptionData = async () => {
    try {
      // Load subscription plans using new API endpoint
      const plansResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/plans`);
      if (plansResponse.ok) {
        const plansData = await plansResponse.json();
        setSubscriptionPlans(plansData.plans);
      }

      // Load current subscription (using authentication token in production)
      const currentResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/check-access/demo@customermindiq.com`);
      if (currentResponse.ok) {
        const currentData = await currentResponse.json();
        setCurrentSubscription(currentData.access);
      }
    } catch (error) {
      console.error('Error loading subscription data:', error);
      setError('Failed to load subscription information');
    } finally {
      setLoading(false);
    }
  };

  const loadTransactionHistory = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/transactions/history?email=demo@customermindiq.com`);
      if (response.ok) {
        const data = await response.json();
        setTransactionHistory(data.transactions);
      }
    } catch (error) {
      console.error('Error loading transaction history:', error);
    }
  };

  const initiateSubscription = async (planId) => {
    if (planId === 'free') {
      // Handle free subscription
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/subscription/checkout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            plan_id: planId,
            origin_url: window.location.origin,
            metadata: { email: 'demo@customermindiq.com' }
          })
        });

        if (response.ok) {
          const data = await response.json();
          setCurrentSubscription({ current_plan: 'free', status: 'active' });
          alert('Free subscription activated successfully!');
        }
      } catch (error) {
        setError('Failed to activate free subscription');
      }
      return;
    }

    // Handle paid subscriptions
    setProcessingPayment(planId);
    setError(null);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/subscription/checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan_id: planId,
          origin_url: window.location.origin,
          metadata: { 
            email: 'demo@customermindiq.com',
            source: 'subscription_upgrade'
          }
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Redirect to Stripe Checkout
        window.location.href = data.checkout_url;
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to create checkout session');
      }
    } catch (error) {
      console.error('Subscription error:', error);
      setError('Failed to initiate subscription. Please try again.');
    } finally {
      setProcessingPayment(null);
    }
  };

  const pollPaymentStatus = async (sessionId, attempts = 0) => {
    const maxAttempts = 5;
    const pollInterval = 2000;

    if (attempts >= maxAttempts) {
      setError('Payment status check timed out. Please refresh the page to check your subscription status.');
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/checkout/status/${sessionId}`);
      if (!response.ok) {
        throw new Error('Failed to check payment status');
      }

      const data = await response.json();
      
      if (data.payment_status === 'paid') {
        // Payment successful - reload subscription data
        await loadSubscriptionData();
        await loadTransactionHistory();
        
        // Clear URL parameters
        window.history.replaceState({}, document.title, window.location.pathname);
        
        alert('Payment successful! Your subscription has been activated.');
        return;
      } else if (data.status === 'expired') {
        setError('Payment session expired. Please try again.');
        return;
      }

      // If payment is still pending, continue polling
      setTimeout(() => pollPaymentStatus(sessionId, attempts + 1), pollInterval);
    } catch (error) {
      console.error('Error checking payment status:', error);
      setError('Error checking payment status. Please refresh the page.');
    }
  };

  const cancelSubscription = async () => {
    if (!confirm('Are you sure you want to cancel your subscription? You will lose access to premium features at the end of your billing period.')) {
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/subscription/cancel`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'demo@customermindiq.com' })
      });

      if (response.ok) {
        await loadSubscriptionData();
        alert('Subscription cancelled successfully');
      } else {
        setError('Failed to cancel subscription');
      }
    } catch (error) {
      console.error('Cancel subscription error:', error);
      setError('Failed to cancel subscription');
    }
  };

  const getPlanIcon = (planId) => {
    switch (planId) {
      case 'free':
        return <Users className="h-8 w-8 text-blue-600" />;
      case 'launch':
        return <Star className="h-8 w-8 text-green-600" />;
      case 'growth':
        return <TrendingUp className="h-8 w-8 text-purple-600" />;
      case 'scale':
        return <Crown className="h-8 w-8 text-yellow-600" />;
      case 'white_label':
        return <Shield className="h-8 w-8 text-indigo-600" />;
      case 'custom':
        return <Zap className="h-8 w-8 text-red-600" />;
      default:
        return <CreditCard className="h-8 w-8 text-gray-600" />;
    }
  };

  const getPlanColor = (planId) => {
    switch (planId) {
      case 'free':
        return 'border-blue-200 bg-blue-50';
      case 'professional':
        return 'border-purple-200 bg-purple-50';
      case 'enterprise':
        return 'border-yellow-200 bg-yellow-50';
      default:
        return 'border-gray-200 bg-gray-50';
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800"><CheckCircle className="h-4 w-4 mr-1" />Active</Badge>;
      case 'cancelled':
        return <Badge className="bg-red-100 text-red-800"><XCircle className="h-4 w-4 mr-1" />Cancelled</Badge>;
      default:
        return <Badge className="bg-gray-100 text-gray-800">Unknown</Badge>;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-lg">Loading subscription information...</span>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Subscription Management</h1>
        <p className="text-gray-600">Manage your Customer Mind IQ subscription and billing</p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex items-center">
            <XCircle className="h-5 w-5 text-red-400 mr-2" />
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      )}

      {/* Current Subscription */}
      {currentSubscription && (
        <Card className="border-l-4 border-l-blue-500">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {getPlanIcon(currentSubscription.current_plan)}
                <div>
                  <h2 className="text-xl font-semibold">Current Subscription</h2>
                  <p className="text-gray-600">
                    {subscriptionPlans[currentSubscription.current_plan]?.name || 'Free Tier'}
                  </p>
                </div>
              </div>
              {getStatusBadge(currentSubscription.status)}
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium mb-3">Plan Features</h3>
                <ul className="space-y-2">
                  {currentSubscription.features?.map((feature, index) => (
                    <li key={index} className="flex items-center text-sm">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="font-medium mb-3">Usage Limits</h3>
                <div className="space-y-2 text-sm">
                  {currentSubscription.limits && (
                    <>
                      <div className="flex justify-between">
                        <span>Customer Profiles:</span>
                        <span className="font-medium">
                          {currentSubscription.limits.customer_profiles === -1 ? 'Unlimited' : currentSubscription.limits.customer_profiles.toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>AI Insights:</span>
                        <span className="font-medium">
                          {currentSubscription.limits.ai_insights === -1 ? 'Unlimited' : currentSubscription.limits.ai_insights.toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>Data Storage:</span>
                        <span className="font-medium">{currentSubscription.limits.data_storage} GB</span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
            
            {currentSubscription.current_plan !== 'free' && currentSubscription.status === 'active' && (
              <div className="mt-6 pt-4 border-t">
                <Button 
                  variant="outline" 
                  onClick={cancelSubscription}
                  className="text-red-600 border-red-300 hover:bg-red-50"
                >
                  Cancel Subscription
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Available Plans */}
      <div>
        <h2 className="text-2xl font-bold text-center mb-8">Choose Your Plan</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {Object.entries(subscriptionPlans).map(([planId, plan]) => {
            const isCurrentPlan = currentSubscription?.current_plan === planId;
            const isUpgrade = currentSubscription && (
              (currentSubscription.current_plan === 'free' && planId !== 'free') ||
              (currentSubscription.current_plan === 'professional' && planId === 'enterprise')
            );

            return (
              <Card key={planId} className={`relative ${getPlanColor(planId)} ${isCurrentPlan ? 'ring-2 ring-blue-500' : ''}`}>
                {planId === 'professional' && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <Badge className="bg-purple-600 text-white px-3 py-1">Most Popular</Badge>
                  </div>
                )}
                
                <CardHeader className="text-center">
                  <div className="flex justify-center mb-4">
                    {getPlanIcon(planId)}
                  </div>
                  <h3 className="text-xl font-bold">{plan.name}</h3>
                  <div className="mt-4">
                    <span className="text-4xl font-bold">${plan.price}</span>
                    {planId !== 'free' && <span className="text-gray-600">/month</span>}
                  </div>
                </CardHeader>
                
                <CardContent>
                  <ul className="space-y-3 mb-6">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-start text-sm">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  
                  <Button 
                    className="w-full"
                    onClick={() => initiateSubscription(planId)}
                    disabled={isCurrentPlan || processingPayment === planId}
                    variant={isCurrentPlan ? "outline" : "default"}
                  >
                    {processingPayment === planId && (
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    )}
                    {isCurrentPlan ? 'Current Plan' : 
                     isUpgrade ? `Upgrade to ${plan.name}` : 
                     planId === 'free' ? 'Start Free' : 
                     `Get ${plan.name}`}
                    {!isCurrentPlan && !processingPayment && (
                      <ArrowRight className="h-4 w-4 ml-2" />
                    )}
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Transaction History */}
      {transactionHistory.length > 0 && (
        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold flex items-center">
              <BarChart3 className="h-5 w-5 mr-2" />
              Transaction History
            </h2>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Plan
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {transactionHistory.slice(0, 5).map((transaction) => (
                    <tr key={transaction.transaction_id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(transaction.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">
                        {transaction.plan_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${transaction.amount} {transaction.currency?.toUpperCase()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Badge 
                          className={
                            transaction.payment_status === 'paid' ? 'bg-green-100 text-green-800' :
                            transaction.payment_status === 'failed' ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                          }
                        >
                          {transaction.payment_status}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Support Information */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-center text-center">
            <div>
              <Headphones className="h-8 w-8 text-blue-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Need Help?</h3>
              <p className="text-gray-600 mb-4">
                Our support team is here to assist you with any subscription or billing questions.
              </p>
              <div className="flex justify-center space-x-4">
                <Button variant="outline" size="sm">
                  <Shield className="h-4 w-4 mr-2" />
                  View Legal Docs
                </Button>
                <Button variant="outline" size="sm">
                  <Headphones className="h-4 w-4 mr-2" />
                  Contact Support
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SubscriptionManager;