import React, { useState, useEffect } from 'react';

const PaymentTest = () => {
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Function to get URL parameters
  const getUrlParameter = (name) => {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(window.location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  };

  // Function to update status display
  const updateStatus = (message, type) => {
    setStatus(message);
    setError(type === 'error' ? message : '');
  };

  // Function to poll payment status
  const pollPaymentStatus = async (sessionId, attempts = 0) => {
    const maxAttempts = 5;
    const pollInterval = 2000; // 2 seconds

    if (attempts >= maxAttempts) {
      updateStatus('Payment status check timed out. Please check your email for confirmation.', 'error');
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/checkout/status/${sessionId}`);
      if (!response.ok) {
        throw new Error('Failed to check payment status');
      }

      const data = await response.json();
      
      if (data.payment_status === 'paid') {
        updateStatus('Payment successful! Thank you for your purchase.', 'success');
        return;
      } else if (data.status === 'expired') {
        updateStatus('Payment session expired. Please try again.', 'error');
        return;
      }

      // If payment is still pending, continue polling
      updateStatus('Payment is being processed...', 'pending');
      setTimeout(() => pollPaymentStatus(sessionId, attempts + 1), pollInterval);
    } catch (error) {
      console.error('Error checking payment status:', error);
      updateStatus('Error checking payment status. Please try again.', 'error');
    }
  };

  // Function to check if we're returning from Stripe
  const checkReturnFromStripe = () => {
    const sessionId = getUrlParameter('session_id');
    if (sessionId) {
      updateStatus('Checking payment status...', 'pending');
      pollPaymentStatus(sessionId);
    }
  };

  const initiatePayment = async (planId) => {
    setError('');
    setLoading(true);

    try {
      // Get current URL for success and cancel URLs
      const currentUrl = window.location.href.split('?')[0];

      const requestBody = {
        plan_id: planId,
        origin_url: window.location.origin,
        metadata: {
          source: 'payment_test',
          test_user: 'demo@customermindiq.com'
        }
      };

      // Call the checkout session API
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/subscription/checkout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create checkout session');
      }

      const data = await response.json();
      
      if (planId === 'free') {
        updateStatus('Free subscription activated successfully!', 'success');
      } else if (data.checkout_url) {
        // Redirect to Stripe Checkout
        window.location.href = data.checkout_url;
      } else {
        throw new Error('No checkout URL received');
      }
    } catch (error) {
      setError(error.message);
      console.error('Payment error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Check if we're returning from Stripe when the page loads
  useEffect(() => {
    checkReturnFromStripe();
  }, []);

  const getStatusColor = (type) => {
    switch (type) {
      case 'success':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'error':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'pending':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4 sm:p-6">
      <div className="bg-white shadow-lg rounded-lg p-4 sm:p-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-center mb-6 sm:mb-8 text-gray-900">
          Customer Mind IQ - Payment Integration Test
        </h1>
        
        {/* Status Display */}
        {status && (
          <div className={`mb-6 p-4 rounded-md border ${getStatusColor(error ? 'error' : 'success')}`}>
            <p className="font-medium">{status}</p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 rounded-md border border-red-200 bg-red-50">
            <p className="text-red-600 font-medium">Error: {error}</p>
          </div>
        )}

        {/* Subscription Plans */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          
          {/* Free Plan */}
          <div className="border border-gray-200 rounded-lg p-6 bg-gray-50">
            <div className="text-center">
              <h3 className="text-xl font-bold mb-2">Free Tier</h3>
              <div className="text-3xl font-bold mb-4">$0<span className="text-lg text-gray-600">/month</span></div>
              <ul className="text-sm text-left mb-6 space-y-2">
                <li>✅ Basic customer intelligence</li>
                <li>✅ Up to 1,000 customer profiles</li>
                <li>✅ 5 AI insights per month</li>
                <li>✅ Email support</li>
                <li>✅ Basic dashboard</li>
              </ul>
              <button
                onClick={() => initiatePayment('free')}
                disabled={loading}
                className="w-full bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Get Free'}
              </button>
            </div>
          </div>

          {/* Professional Plan */}
          <div className="border border-purple-200 rounded-lg p-6 bg-purple-50 relative">
            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-medium">
              Most Popular
            </div>
            <div className="text-center">
              <h3 className="text-xl font-bold mb-2">Professional</h3>
              <div className="text-3xl font-bold mb-4">$99<span className="text-lg text-gray-600">/month</span></div>
              <ul className="text-sm text-left mb-6 space-y-2">
                <li>✅ Full customer intelligence suite</li>
                <li>✅ Up to 50,000 customer profiles</li>
                <li>✅ Unlimited AI insights</li>
                <li>✅ Marketing automation</li>
                <li>✅ Revenue analytics</li>
                <li>✅ Website intelligence</li>
                <li>✅ Priority support</li>
              </ul>
              <button
                onClick={() => initiatePayment('professional')}
                disabled={loading}
                className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Upgrade to Professional'}
              </button>
            </div>
          </div>

          {/* Enterprise Plan */}
          <div className="border border-yellow-200 rounded-lg p-6 bg-yellow-50">
            <div className="text-center">
              <h3 className="text-xl font-bold mb-2">Enterprise</h3>
              <div className="text-3xl font-bold mb-4">$299<span className="text-lg text-gray-600">/month</span></div>
              <ul className="text-sm text-left mb-6 space-y-2">
                <li>✅ Everything in Professional</li>
                <li>✅ Unlimited customer profiles</li>
                <li>✅ White-label options</li>
                <li>✅ Custom integrations</li>
                <li>✅ Dedicated account manager</li>
                <li>✅ Phone support</li>
                <li>✅ SLA guarantees</li>
              </ul>
              <button
                onClick={() => initiatePayment('enterprise')}
                disabled={loading}
                className="w-full bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Get Enterprise'}
              </button>
            </div>
          </div>
        </div>

        {/* Information */}
        <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
          <h4 className="font-medium text-blue-900 mb-2">Payment Test Information</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• This is a test implementation of the Stripe payment system</li>
            <li>• Free tier activates immediately without payment processing</li>
            <li>• Professional and Enterprise tiers redirect to Stripe Checkout</li>
            <li>• Use Stripe test cards for testing (e.g., 4242 4242 4242 4242)</li>
            <li>• Payment status is automatically checked when returning from Stripe</li>
            <li>• All transactions are stored in the payment_transactions collection</li>
          </ul>
        </div>

        {/* Debug Information */}
        <div className="mt-6 bg-gray-50 border border-gray-200 rounded-md p-4">
          <h4 className="font-medium text-gray-900 mb-2">Debug Information</h4>
          <div className="text-sm text-gray-700 space-y-1">
            <p><strong>Backend URL:</strong> {process.env.REACT_APP_BACKEND_URL}</p>
            <p><strong>Current URL:</strong> {window.location.href}</p>
            <p><strong>Origin:</strong> {window.location.origin}</p>
            <p><strong>Session ID from URL:</strong> {getUrlParameter('session_id') || 'None'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentTest;