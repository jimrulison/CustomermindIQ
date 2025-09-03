import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Alert, AlertDescription } from './ui/alert';
import { Mail, Lock, Brain, TrendingUp, Users, BarChart3, Gift, CheckCircle, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const SignIn = ({ onSignIn }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSignUp, setShowSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showSignUpPassword, setShowSignUpPassword] = useState(false);
  const [signUpData, setSignUpData] = useState({
    first_name: '',
    last_name: '',
    company_name: '',
    email: '',
    password: ''
  });
  const [subscriptionPlans, setSubscriptionPlans] = useState({});
  const [plansLoading, setPlansLoading] = useState(true);

  const { login, register } = useAuth();

  // Load subscription plans on component mount
  useEffect(() => {
    loadSubscriptionPlans();
  }, []);

  const loadSubscriptionPlans = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/plans`);
      if (response.ok) {
        const data = await response.json();
        setSubscriptionPlans(data.plans);
      } else {
        console.error('Failed to load subscription plans');
        // Fallback to default plans if API fails
        setSubscriptionPlans({
          launch: { name: 'Launch Plan', monthly_price: 49, annual_price: 490 },
          growth: { name: 'Growth Plan', monthly_price: 75, annual_price: 750, most_popular: true },
          scale: { name: 'Scale Plan', monthly_price: 199, annual_price: 1990 },
          custom: { name: 'Custom Plan', monthly_price: 'contact_sales' }
        });
      }
    } catch (error) {
      console.error('Error loading subscription plans:', error);
      // Fallback plans
      setSubscriptionPlans({
        launch: { name: 'Launch Plan', monthly_price: 49, annual_price: 490 },
        growth: { name: 'Growth Plan', monthly_price: 75, annual_price: 750, most_popular: true },
        scale: { name: 'Scale Plan', monthly_price: 199, annual_price: 1990 },
        custom: { name: 'Custom Plan', monthly_price: 'contact_sales' }
      });
    } finally {
      setPlansLoading(false);
    }
  };

  const handleSignIn = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Make email case-insensitive by converting to lowercase
      const normalizedEmail = email.trim().toLowerCase();
      const result = await login(normalizedEmail, password, false);
      
      if (result.success) {
        onSignIn(result.user);
      } else {
        setError(result.error);
      }
    } catch (error) {
      setError('Unable to connect to server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Make email case-insensitive by converting to lowercase
      const registrationData = {
        ...signUpData,
        email: signUpData.email.trim().toLowerCase(),
        role: 'user',
        subscription_tier: 'free'
      };
      
      const result = await register(registrationData);
      
      if (result.success) {
        onSignIn(result.data.user_profile);
      } else {
        setError(result.error);
      }
    } catch (error) {
      setError('Unable to connect to server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTrialSignUp = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Register for 7-day free trial with case-insensitive email
      const trialResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/trial/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: signUpData.email.trim().toLowerCase(),
          first_name: signUpData.first_name,
          last_name: signUpData.last_name,
          company_name: signUpData.company_name,
        }),
      });

      const trialData = await trialResponse.json();

      if (trialResponse.ok && trialData.status === 'success') {
        // Auto-login the trial user with the returned password
        const loginResult = await login(
          signUpData.email.trim().toLowerCase(), 
          trialData.user.password, 
          false
        );
        if (loginResult.success) {
          onSignIn(loginResult.user);
        } else {
          setError('Trial created but login failed. Please contact support.');
        }
      } else {
        setError(trialData.detail || trialData.message || 'Failed to start trial');
      }
    } catch (error) {
      setError('Unable to connect to server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setSignUpData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (showSignUp) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <img 
                src="https://customer-assets.emergentagent.com/job_mindiq-auth/artifacts/bi9l7mag_Customer%20Mind%20IQ%20logo.png" 
                alt="CustomerMind IQ Logo" 
                className="w-16 h-16 mr-3"
              />
              <h1 className="text-3xl font-bold text-white">CustomerMind IQ</h1>
            </div>
            <p className="text-slate-300">Universal Customer Intelligence Platform</p>
          </div>

          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader className="text-center">
              <CardTitle className="text-white text-2xl">Start Your Free Trial</CardTitle>
              <CardDescription className="text-slate-400">
                7 days free - No credit card required
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSignUp} className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      First Name
                    </label>
                    <Input
                      type="text"
                      value={signUpData.first_name}
                      onChange={(e) => handleInputChange('first_name', e.target.value)}
                      placeholder="John"
                      className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Last Name
                    </label>
                    <Input
                      type="text"
                      value={signUpData.last_name}
                      onChange={(e) => handleInputChange('last_name', e.target.value)}
                      placeholder="Doe"
                      className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Company Name
                  </label>
                  <Input
                    type="text"
                    value={signUpData.company_name}
                    onChange={(e) => handleInputChange('company_name', e.target.value)}
                    placeholder="Your Company"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                    <Input
                      type="email"
                      value={signUpData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      placeholder="you@company.com"
                      className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 pl-10"
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                    <Input
                      type={showSignUpPassword ? "text" : "password"}
                      value={signUpData.password}
                      onChange={(e) => handleInputChange('password', e.target.value)}
                      placeholder="Create a strong password"
                      className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 pl-10 pr-10"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowSignUpPassword(!showSignUpPassword)}
                      className="absolute right-3 top-3 text-slate-400 hover:text-slate-300"
                    >
                      {showSignUpPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </div>

                {error && (
                  <Alert className="bg-red-500/10 border-red-500/20">
                    <AlertDescription className="text-red-300">
                      {error}
                    </AlertDescription>
                  </Alert>
                )}

                {/* 7-Day Free Trial Highlight */}
                <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 border border-green-500/20 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <Gift className="w-5 h-5 text-green-400 mr-2" />
                    <h3 className="text-green-300 font-semibold">7-Day Free Trial</h3>
                  </div>
                  <div className="space-y-2 text-sm text-slate-300">
                    <div className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                      <span>No credit card required</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                      <span>Full Starter tier access</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                      <span>Cancel anytime</span>
                    </div>
                  </div>
                </div>

                {/* Updated Subscription Plans - Dynamic from API */}
                <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4">
                  <h3 className="text-blue-300 font-semibold mb-3">Choose Your Plan After Trial</h3>
                  {plansLoading ? (
                    <div className="text-center text-slate-400">Loading plans...</div>
                  ) : (
                    <div className="space-y-3 text-sm">
                      {Object.entries(subscriptionPlans).map(([planId, plan]) => {
                        if (planId === 'free') return null; // Don't show free plan in signup
                        
                        return (
                          <div key={planId} className={`bg-slate-700/30 rounded-lg p-3 ${plan.most_popular ? 'ring-2 ring-purple-500/50' : ''}`}>
                            <div className="flex justify-between items-center mb-1">
                              <div className="flex items-center">
                                <span className="text-white font-medium">{plan.name}</span>
                                {plan.most_popular && (
                                  <span className="ml-2 text-xs bg-purple-600 text-white px-2 py-1 rounded">Most Popular</span>
                                )}
                              </div>
                              <span className="text-green-400 font-semibold">
                                {typeof plan.monthly_price === 'number' ? `$${plan.monthly_price}/month` : 'Contact Sales'}
                              </span>
                            </div>
                            <div className="flex justify-between items-center">
                              <p className="text-slate-400 text-xs">
                                {planId === 'launch' && '5 websites • 50 keywords • Basic analytics'}
                                {planId === 'growth' && '10 websites • 200 keywords • Full analytics'}
                                {planId === 'scale' && 'Unlimited • Advanced features • Priority support'}
                                {planId === 'white_label' && 'White-label branding • Reseller dashboard'}
                                {planId === 'custom' && 'Custom features • Dedicated IT support'}
                              </p>
                              {typeof plan.annual_price === 'number' && (
                                <span className="text-xs text-green-300">
                                  ${plan.annual_price}/year (2 months free!)
                                </span>
                              )}
                            </div>
                            {(planId === 'launch' || planId === 'growth' || planId === 'scale') && (
                              <p className="text-xs text-yellow-300 mt-1">
                                • Growth Acceleration Engine (Annual Only)
                              </p>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white"
                >
                  {loading ? 'Starting Trial...' : 'Start 7-Day Free Trial'}
                </Button>
                
                <div className="text-center">
                  <button
                    type="button"
                    onClick={() => setShowSignUp(false)}
                    className="text-blue-400 hover:text-blue-300 text-sm"
                  >
                    Already have an account? Sign In
                  </button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <img 
              src="https://customer-assets.emergentagent.com/job_mindiq-auth/artifacts/bi9l7mag_Customer%20Mind%20IQ%20logo.png" 
              alt="CustomerMind IQ Logo" 
              className="w-16 h-16 mr-3"
            />
            <h1 className="text-3xl font-bold text-white">CustomerMind IQ</h1>
          </div>
          <p className="text-slate-300">Universal Customer Intelligence Platform</p>
        </div>

        <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
          <CardHeader className="text-center">
            <CardTitle className="text-white text-2xl">Welcome Back</CardTitle>
            <CardDescription className="text-slate-400">
              Sign in to your CustomerMind IQ account
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSignIn} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your@email.com"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 pl-10"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 pl-10 pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-slate-400 hover:text-slate-300"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {error && (
                <Alert className="bg-red-500/10 border-red-500/20">
                  <AlertDescription className="text-red-300">
                    {error}
                  </AlertDescription>
                </Alert>
              )}

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </Button>
              
              <Button
                type="button"
                onClick={() => setShowSignUp(true)}
                className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white mt-3"
              >
                SIGN UP NOW - FREE 7-Day Trial
              </Button>
              
              <div className="text-center mt-2">
                <span className="text-slate-400 text-xs">
                  No Credit Card Required • Cancel Anytime
                </span>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Features Preview */}
        <div className="mt-8 grid grid-cols-2 gap-4">
          <div className="bg-slate-800/30 backdrop-blur-xl border border-slate-700 rounded-lg p-4 text-center">
            <Users className="w-8 h-8 text-blue-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Customer Intelligence</h3>
            <p className="text-slate-400 text-xs">AI-powered insights</p>
          </div>
          <div className="bg-slate-800/30 backdrop-blur-xl border border-slate-700 rounded-lg p-4 text-center">
            <TrendingUp className="w-8 h-8 text-green-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Revenue Analytics</h3>
            <p className="text-slate-400 text-xs">Advanced forecasting</p>
          </div>
          <div className="bg-slate-800/30 backdrop-blur-xl border border-slate-700 rounded-lg p-4 text-center">
            <BarChart3 className="w-8 h-8 text-purple-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Marketing Automation</h3>
            <p className="text-slate-400 text-xs">Multi-channel campaigns</p>
          </div>
          <div className="bg-slate-800/30 backdrop-blur-xl border border-slate-700 rounded-lg p-4 text-center">
            <Brain className="w-8 h-8 text-orange-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Analytics & Insights</h3>
            <p className="text-slate-400 text-xs">Journey mapping & ROI</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignIn;