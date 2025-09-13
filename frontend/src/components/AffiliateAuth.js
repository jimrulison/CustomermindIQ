import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
    Users, 
    Mail, 
    Phone, 
    MapPin, 
    CreditCard, 
    Shield,
    Check,
    AlertCircle,
    Eye,
    EyeOff,
    ArrowRight,
    Sparkles,
    DollarSign,
    TrendingUp
} from 'lucide-react';
import AffiliateRegistration from './AffiliateRegistration';
import AffiliatePortal from './AffiliatePortal';
import LanguageSelector from './LanguageSelector';

const AffiliateAuth = () => {
    const { t } = useTranslation();
    const [currentView, setCurrentView] = useState('landing'); // 'landing', 'login', 'register', 'portal'
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [affiliateData, setAffiliateData] = useState(null);
    
    const [loginForm, setLoginForm] = useState({
        email: '',
        password: ''
    });

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://admin-portal-fix-9.preview.emergentagent.com';

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await fetch(`${backendUrl}/api/affiliate/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginForm)
            });

            const data = await response.json();
            
            if (data.success) {
                // Store affiliate token
                localStorage.setItem('affiliate_token', data.token);
                localStorage.setItem('affiliate_data', JSON.stringify(data.affiliate));
                
                setAffiliateData(data.affiliate);
                setCurrentView('portal');
            } else {
                setError(data.detail || 'Login failed');
            }
        } catch (err) {
            setError('Network error. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleRegistrationComplete = (data) => {
        setError('');
        // Show success message and redirect to login
        alert(`Registration successful! Your Affiliate ID is: ${data.affiliate_id}\n\nPlease check your email for verification instructions. You can now login once your account is approved.`);
        setCurrentView('login');
    };

    const handleLogout = () => {
        localStorage.removeItem('affiliate_token');
        localStorage.removeItem('affiliate_data');
        setAffiliateData(null);
        setCurrentView('landing');
        setLoginForm({ email: '', password: '' });
    };

    // Check if already logged in
    React.useEffect(() => {
        const token = localStorage.getItem('affiliate_token');
        const data = localStorage.getItem('affiliate_data');
        
        if (token && data) {
            try {
                const parsedData = JSON.parse(data);
                setAffiliateData(parsedData);
                setCurrentView('portal');
            } catch (error) {
                // Clear invalid data
                localStorage.removeItem('affiliate_token');
                localStorage.removeItem('affiliate_data');
            }
        }
    }, []);

    // Landing Page
    const renderLanding = () => (
        <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
            {/* Language Selector - Top Right */}
            <div className="absolute top-4 right-4 z-10">
                <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-2">
                    <LanguageSelector theme="dark" />
                </div>
            </div>
            
            <div className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl w-full">
                    {/* Hero Section */}
                    <div className="text-center mb-12">
                        <div className="flex items-center justify-center mb-6">
                            <img
                                src="https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/wzbjjt9q_download.svg"
                                alt="CustomerMind IQ company logo - Join our affiliate partner program"
                                className="w-16 h-16 mr-4"
                            />
                            <div className="text-left">
                                <h1 className="text-4xl font-bold text-white">CustomerMind IQ</h1>
                                <p className="text-xl text-indigo-200">Affiliate Partner Program</p>
                            </div>
                        </div>
                        
                        <h2 className="text-3xl font-bold text-white mb-4">
                            {t('pages.affiliate.registration.title')}
                        </h2>
                        <p className="text-xl text-gray-100 mb-8 max-w-2xl mx-auto">
                            Earn exceptional commissions promoting the world's most advanced customer intelligence platform
                        </p>
                    </div>

                    {/* Features Grid */}
                    <div className="grid md:grid-cols-3 gap-8 mb-12">
                        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mb-4">
                                <DollarSign className="h-6 w-6 text-white" />
                            </div>
                            <h3 className="text-xl font-semibold text-white mb-2">High Commissions</h3>
                            <p className="text-gray-100">Earn up to 50% initial commission + 20% recurring for 12 months + 10% for months 13-24</p>
                        </div>

                        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
                                <TrendingUp className="h-6 w-6 text-white" />
                            </div>
                            <h3 className="text-xl font-semibold text-white mb-2">Growing Market</h3>
                            <p className="text-gray-100">Customer intelligence is a $50B+ market with massive growth potential</p>
                        </div>

                        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mb-4">
                                <Sparkles className="h-6 w-6 text-white" />
                            </div>
                            <h3 className="text-xl font-semibold text-white mb-2">Premium Product</h3>
                            <p className="text-gray-100">Promote cutting-edge AI-powered customer analytics that customers love</p>
                        </div>
                    </div>

                    {/* Commission Structure */}
                    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20 mb-12">
                        <h3 className="text-2xl font-bold text-white mb-6 text-center">Commission Structure</h3>
                        <div className="grid md:grid-cols-3 gap-6">
                            <div className="text-center">
                                <div className="bg-green-500/20 rounded-lg p-4 mb-3">
                                    <h4 className="text-lg font-semibold text-green-300">Launch Plan</h4>
                                    <p className="text-2xl font-bold text-green-400">30%</p>
                                </div>
                                <p className="text-sm text-gray-200">Initial + 20% recurring (2-12 months) + 10% (13-24 months)</p>
                            </div>
                            
                            <div className="text-center">
                                <div className="bg-blue-500/20 rounded-lg p-4 mb-3">
                                    <h4 className="text-lg font-semibold text-blue-300">Growth Plan</h4>
                                    <p className="text-2xl font-bold text-blue-400">40%</p>
                                </div>
                                <p className="text-sm text-gray-200">Initial + 20% recurring (2-12 months) + 10% (13-24 months)</p>
                            </div>
                            
                            <div className="text-center">
                                <div className="bg-purple-500/20 rounded-lg p-4 mb-3">
                                    <h4 className="text-lg font-semibold text-purple-300">Scale Plan</h4>
                                    <p className="text-2xl font-bold text-purple-400">50%</p>
                                </div>
                                <p className="text-sm text-gray-200">Initial + 20% recurring (2-12 months) + 10% (13-24 months)</p>
                            </div>
                        </div>
                    </div>

                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <button
                            onClick={() => setCurrentView('register')}
                            className="flex items-center justify-center px-8 py-4 min-h-[44px] bg-gradient-to-r from-green-600 to-blue-600 text-white font-semibold rounded-lg hover:from-green-700 hover:to-blue-700 transition-all duration-200 shadow-lg"
                        >
                            {t('pages.affiliate.registration.joinNow')}
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </button>
                        
                        <button
                            onClick={() => setCurrentView('login')}
                            className="flex items-center justify-center px-8 py-4 min-h-[44px] bg-white/10 backdrop-blur-sm text-white font-semibold rounded-lg hover:bg-white/20 transition-all duration-200 border border-white/30"
                        >
                            {t('pages.affiliate.registration.alreadyPartner')}
                        </button>
                    </div>

                    {/* Additional Info */}
                    <div className="text-center mt-12">
                        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                            <p className="text-white text-sm font-medium">
                                Questions? Contact our affiliate team at{' '}
                                <a href="mailto:affiliates@customermindiq.com" className="text-blue-300 hover:text-blue-100 underline font-semibold">
                                    affiliates@customermindiq.com
                                </a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    // Login Page
    const renderLogin = () => (
        <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center px-4 sm:px-6 lg:px-8">
            {/* Language Selector - Top Right */}
            <div className="absolute top-4 right-4 z-10">
                <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-2">
                    <LanguageSelector theme="dark" />
                </div>
            </div>
            
            <div className="max-w-md w-full">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20">
                    <div className="text-center mb-8">
                        <h2 className="text-3xl font-bold text-white">Affiliate Sign In</h2>
                        <p className="text-indigo-200 mt-2">Access your affiliate dashboard</p>
                    </div>

                    {error && (
                        <div className="mb-6 bg-red-500/20 border border-red-500/50 rounded-lg p-4">
                            <div className="flex items-center">
                                <AlertCircle className="w-5 h-5 text-red-400 mr-2" />
                                <span className="text-red-300">{error}</span>
                            </div>
                        </div>
                    )}

                    <form onSubmit={handleLogin} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-white mb-2">
                                Email Address
                            </label>
                            <input
                                type="email"
                                value={loginForm.email}
                                onChange={(e) => setLoginForm(prev => ({ ...prev, email: e.target.value }))}
                                className="w-full px-4 py-4 min-h-[44px] bg-white/10 border border-white/30 rounded-lg text-white placeholder-indigo-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Enter your email"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-white mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    value={loginForm.password}
                                    onChange={(e) => setLoginForm(prev => ({ ...prev, password: e.target.value }))}
                                    className="w-full px-4 py-4 min-h-[44px] bg-white/10 border border-white/30 rounded-lg text-white placeholder-indigo-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder="Enter your password"
                                    required
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-3 min-h-[44px] min-w-[44px] flex items-center justify-center text-indigo-300 hover:text-white"
                                >
                                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                                </button>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-4 min-h-[44px] bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                        >
                            {loading ? (
                                <div className="flex items-center justify-center">
                                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                                    Signing In...
                                </div>
                            ) : (
                                'Sign In'
                            )}
                        </button>
                    </form>

                    <div className="mt-8 text-center">
                        <p className="text-indigo-200">
                            Don't have an account?{' '}
                            <button
                                onClick={() => setCurrentView('register')}
                                className="text-blue-300 hover:text-blue-200 underline font-medium min-h-[44px] inline-flex items-center"
                            >
                                Apply to become an affiliate
                            </button>
                        </p>
                        
                        <button
                            onClick={() => setCurrentView('landing')}
                            className="mt-4 text-indigo-300 hover:text-white underline text-sm min-h-[44px] inline-flex items-center"
                        >
                            ← Back to Program Info
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );

    // Main render logic
    if (currentView === 'portal' && affiliateData) {
        return (
            <div className="min-h-screen bg-gray-50">
                {/* Affiliate Portal Header */}
                <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4">
                    <div className="max-w-7xl mx-auto flex items-center justify-between">
                        <div className="flex items-center">
                            <img
                                src="https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/wzbjjt9q_download.svg"
                                alt="CustomerMind IQ Logo"
                                className="w-8 h-8 mr-3"
                            />
                            <div>
                                <h1 className="text-xl font-bold">CustomerMind IQ Affiliates</h1>
                                <p className="text-sm opacity-90">Welcome, {affiliateData.name}!</p>
                            </div>
                        </div>
                        
                        <button
                            onClick={handleLogout}
                            className="px-4 py-3 min-h-[44px] bg-white/20 hover:bg-white/30 rounded-lg transition-colors text-sm"
                        >
                            Sign Out
                        </button>
                    </div>
                </div>
                
                <AffiliatePortal />
            </div>
        );
    }

    if (currentView === 'register') {
        return (
            <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
                {/* Language Selector - Top Right */}
                <div className="absolute top-4 right-4 z-10">
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-2">
                        <LanguageSelector theme="dark" />
                    </div>
                </div>
                
                <div className="p-4">
                    <button
                        onClick={() => setCurrentView('landing')}
                        className="text-indigo-200 hover:text-white mb-4 flex items-center min-h-[44px]"
                    >
                        ← Back to Program Info
                    </button>
                </div>
                <AffiliateRegistration onRegistrationComplete={handleRegistrationComplete} />
            </div>
        );
    }

    if (currentView === 'login') {
        return renderLogin();
    }

    return renderLanding();
};

export default AffiliateAuth;