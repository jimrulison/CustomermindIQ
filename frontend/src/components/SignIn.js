import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Alert, AlertDescription } from './ui/alert';
import { Mail, Lock, Brain, TrendingUp, Users, BarChart3, Gift, CheckCircle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const SignIn = ({ onSignIn }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSignUp, setShowSignUp] = useState(false);
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
      const result = await login(email, password, false);
      
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
      const result = await register({
        ...signUpData,
        role: 'user',
        subscription_tier: 'free'
      });
      
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
              <Brain className="w-12 h-12 text-blue-400 mr-3" />
              <h1 className="text-3xl font-bold text-white">CustomerMind IQ</h1>
            </div>
            <p className="text-slate-300">Universal Customer Intelligence Platform</p>
          </div>

          <Card className="bg-slate-800/50 backdrop-blur-xl border-slate-700">
            <CardHeader className="text-center">
              <CardTitle className="text-white text-2xl">Create Account</CardTitle>
              <CardDescription className="text-slate-400">
                Join the Universal Customer Intelligence Platform
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSignUp} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Full Name
                  </label>
                  <Input
                    type="text"
                    placeholder="John Doe"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Company Name
                  </label>
                  <Input
                    type="text"
                    placeholder="Your Company"
                    className="bg-slate-700/50 border-slate-600 text-white placeholder-slate-400"
                    required
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

                <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4">
                  <h3 className="text-blue-300 font-semibold mb-2">Subscription Plans</h3>
                  <div className="space-y-2 text-sm text-slate-300">
                    <div className="flex justify-between">
                      <span>• Starter Plan</span>
                      <span className="text-green-400">$49/month</span>
                    </div>
                    <div className="flex justify-between">
                      <span>• Pro Plan</span>
                      <span className="text-green-400">$99/month</span>
                    </div>
                    <div className="flex justify-between">
                      <span>• Enterprise Plan</span>
                      <span className="text-green-400">$199/month</span>
                    </div>
                  </div>
                  <p className="text-xs text-slate-400 mt-2">
                    Payment integration coming soon! All plans include 14-day free trial.
                  </p>
                </div>

                <Button
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                >
                  Create Account & Choose Plan
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
            <Brain className="w-12 h-12 text-blue-400 mr-3" />
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
                    placeholder="demo@customermindiq.com"
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
                    placeholder="demo1234"
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
                  Email: demo@customermindiq.com<br />
                  Password: demo1234
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
                  Don't have an account? Sign Up
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