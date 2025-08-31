import React, { useState } from 'react';
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

  const { login, register } = useAuth();

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
      // Register for 7-day free trial
      const trialResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/subscriptions/trial/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: signUpData.email,
          first_name: signUpData.first_name,
          last_name: signUpData.last_name,
          company_name: signUpData.company_name,
        }),
      });

      const trialData = await trialResponse.json();

      if (trialResponse.ok) {
        // Auto-login the trial user
        const loginResult = await login(signUpData.email, 'trial_password_temp', false);
        if (loginResult.success) {
          onSignIn(loginResult.user);
        } else {
          setError('Trial created but login failed. Please contact support.');
        }
      } else {
        setError(trialData.detail || 'Failed to start trial');
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
                      type="password"
                      value={signUpData.password}
                      onChange={(e) => handleInputChange('password', e.target.value)}
                      placeholder="Create a strong password"
                      className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 pl-10"
                      required
                    />
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

                {/* Updated Subscription Plans */}
                <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4">
                  <h3 className="text-blue-300 font-semibold mb-3">Choose Your Plan After Trial</h3>
                  <div className="space-y-3 text-sm">
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-white font-medium">Starter</span>
                        <span className="text-green-400 font-semibold">$99/month</span>
                      </div>
                      <p className="text-slate-400 text-xs">3 websites • 50 keywords • Basic analytics</p>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-white font-medium">Professional</span>
                        <span className="text-green-400 font-semibold">$299/month</span>
                      </div>
                      <p className="text-slate-400 text-xs">10 websites • 200 keywords • Full analytics</p>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-white font-medium">Enterprise</span>
                        <span className="text-green-400 font-semibold">$799/month</span>
                      </div>
                      <p className="text-slate-400 text-xs">Unlimited • Advanced features • Priority support</p>
                    </div>
                    <div className="bg-slate-700/30 rounded-lg p-3">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-white font-medium">Custom</span>
                        <span className="text-blue-400 font-semibold">Contact Sales</span>
                      </div>
                      <p className="text-slate-400 text-xs">Enterprise + Custom solutions</p>
                    </div>
                  </div>
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
                    placeholder="admin@customermindiq.com"
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
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="CustomerMindIQ2025!"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 pl-10"
                    required
                  />
                </div>
              </div>

              {error && (
                <Alert className="bg-red-500/10 border-red-500/20">
                  <AlertDescription className="text-red-300">
                    {error}
                  </AlertDescription>
                </Alert>
              )}

              <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3">
                <p className="text-green-300 text-sm">
                  <strong>Demo Credentials:</strong><br />
                  Admin: admin@customermindiq.com<br />
                  Password: CustomerMindIQ2025!
                </p>
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </Button>
              
              <div className="text-center">
                <button
                  type="button"
                  onClick={() => setShowSignUp(true)}
                  className="text-blue-400 hover:text-blue-300 text-sm"
                >
                  Start 7-Day Free Trial - No Credit Card Required
                </button>
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