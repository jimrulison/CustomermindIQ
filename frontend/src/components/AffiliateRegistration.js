import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
    User, 
    Mail, 
    Phone, 
    MapPin, 
    CreditCard, 
    Shield,
    Check,
    AlertCircle,
    Eye,
    EyeOff
} from 'lucide-react';

const AffiliateRegistration = ({ onRegistrationComplete }) => {
    const { t } = useTranslation();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        website: '',
        promotion_method: 'email',
        password: '',
        confirm_password: '',
        address: {
            street: '',
            city: '',
            state: '',
            zip_code: '',
            country: 'US'
        },
        payment_method: 'paypal',
        payment_details: {
            paypal_email: '',
            bank_name: '',
            routing_number: '',
            account_number: '',
            account_type: 'checking'
        },
        terms_accepted: false
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showPassword, setShowPassword] = useState(true);
    const [showConfirmPassword, setShowConfirmPassword] = useState(true);

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://mindiq-portal.preview.emergentagent.com';

    const handleInputChange = (field, value) => {
        if (field.includes('.')) {
            const keys = field.split('.');
            setFormData(prev => ({
                ...prev,
                [keys[0]]: {
                    ...prev[keys[0]],
                    [keys[1]]: value
                }
            }));
        } else {
            setFormData(prev => ({
                ...prev,
                [field]: value
            }));
        }
    };

    const validateStep = (stepNumber) => {
        switch (stepNumber) {
            case 1:
                return formData.first_name && formData.last_name && formData.email && 
                       formData.password && formData.password === formData.confirm_password;
            case 2:
                return formData.address.street && formData.address.city && 
                       formData.address.state && formData.address.zip_code;
            case 3:
                if (formData.payment_method === 'paypal') {
                    return formData.payment_details.paypal_email;
                } else if (formData.payment_method === 'bank') {
                    return formData.payment_details.bank_name && 
                           formData.payment_details.routing_number && 
                           formData.payment_details.account_number;
                }
                return true;
            default:
                return true;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${backendUrl}/api/affiliate/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                onRegistrationComplete && onRegistrationComplete(data);
            } else {
                setError(data.detail || 'Registration failed');
            }
        } catch (err) {
            setError('Network error. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const renderStep1 = () => (
        <div className="space-y-6">
            <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900">{t('pages.affiliate.registration.personalInfo')}</h2>
                <p className="mt-2 text-gray-600">{t('pages.affiliate.registration.personalInfoSubtitle')}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        {t('forms.firstName')} *
                    </label>
                    <input
                        type="text"
                        value={formData.first_name}
                        onChange={(e) => handleInputChange('first_name', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder={t('forms.placeholders.enterFirstName')}
                        required
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        {t('forms.lastName')} *
                    </label>
                    <input
                        type="text"
                        value={formData.last_name}
                        onChange={(e) => handleInputChange('last_name', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder={t('forms.placeholders.enterLastName')}
                        required
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t('forms.email')} *
                </label>
                <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={t('forms.placeholders.enterEmail')}
                    required
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        {t('forms.phone')} *
                    </label>
                    <input
                        type="tel"
                        value={formData.phone}
                        onChange={(e) => handleInputChange('phone', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder={t('forms.placeholders.enterPhone')}
                        required
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        {t('forms.website')}
                    </label>
                    <input
                        type="url"
                        value={formData.website}
                        onChange={(e) => handleInputChange('website', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder={t('forms.placeholders.enterWebsite')}
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t('forms.promotionMethod')}
                </label>
                <select
                    value={formData.promotion_method}
                    onChange={(e) => handleInputChange('promotion_method', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    <option value="email">{t('promotionMethods.email')}</option>
                    <option value="social">{t('promotionMethods.social')}</option>
                    <option value="content">{t('promotionMethods.content')}</option>
                    <option value="paid">{t('promotionMethods.paid')}</option>
                    <option value="network">{t('promotionMethods.network')}</option>
                    <option value="speaking">{t('promotionMethods.speaking')}</option>
                    <option value="other">{t('promotionMethods.other')}</option>
                </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        {t('forms.password')} *
                    </label>
                    <div className="relative">
                        <input
                            type={showPassword ? 'text' : 'password'}
                            value={formData.password}
                            onChange={(e) => handleInputChange('password', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder={t('forms.placeholders.enterPassword')}
                            required
                            minLength="8"
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-2 text-gray-500 hover:text-gray-700"
                        >
                            {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                        </button>
                    </div>
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        {t('forms.confirmPassword')} *
                    </label>
                    <div className="relative">
                        <input
                            type={showConfirmPassword ? 'text' : 'password'}
                            value={formData.confirm_password}
                            onChange={(e) => handleInputChange('confirm_password', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder={t('forms.confirmPassword')}
                            required
                        />
                        <button
                            type="button"
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            className="absolute right-3 top-2 text-gray-500 hover:text-gray-700"
                        >
                            {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                        </button>
                    </div>
                    {formData.password !== formData.confirm_password && formData.confirm_password && (
                        <p className="mt-1 text-sm text-red-600">{t('forms.validation.passwordsDoNotMatch')}</p>
                    )}
                </div>
            </div>
        </div>
    );

    const renderStep2 = () => (
        <div className="space-y-6">
            <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900">Address Information</h2>
                <p className="mt-2 text-gray-600">We need your address for tax and payment purposes</p>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Street Address *
                </label>
                <input
                    type="text"
                    value={formData.address.street}
                    onChange={(e) => handleInputChange('address.street', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        City *
                    </label>
                    <input
                        type="text"
                        value={formData.address.city}
                        onChange={(e) => handleInputChange('address.city', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        State/Province *
                    </label>
                    <input
                        type="text"
                        value={formData.address.state}
                        onChange={(e) => handleInputChange('address.state', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        ZIP/Postal Code *
                    </label>
                    <input
                        type="text"
                        value={formData.address.zip_code}
                        onChange={(e) => handleInputChange('address.zip_code', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Country
                    </label>
                    <select
                        value={formData.address.country}
                        onChange={(e) => handleInputChange('address.country', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="US">United States</option>
                        <option value="CA">Canada</option>
                        <option value="GB">United Kingdom</option>
                        <option value="AU">Australia</option>
                        <option value="OTHER">Other</option>
                    </select>
                </div>
            </div>
        </div>
    );

    const renderStep3 = () => (
        <div className="space-y-6">
            <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900">Payment Information</h2>
                <p className="mt-2 text-gray-600">How would you like to receive your commissions?</p>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Payment Method
                </label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button
                        type="button"
                        onClick={() => handleInputChange('payment_method', 'paypal')}
                        className={`p-4 border rounded-lg text-center ${
                            formData.payment_method === 'paypal' 
                                ? 'border-blue-500 bg-blue-50' 
                                : 'border-gray-300'
                        }`}
                    >
                        <div className="font-medium">PayPal</div>
                        <div className="text-sm text-gray-600">Instant payments</div>
                    </button>
                    <button
                        type="button"
                        onClick={() => handleInputChange('payment_method', 'bank')}
                        className={`p-4 border rounded-lg text-center ${
                            formData.payment_method === 'bank' 
                                ? 'border-blue-500 bg-blue-50' 
                                : 'border-gray-300'
                        }`}
                    >
                        <div className="font-medium">Bank Transfer</div>
                        <div className="text-sm text-gray-600">Direct deposit</div>
                    </button>
                    <button
                        type="button"
                        onClick={() => handleInputChange('payment_method', 'check')}
                        className={`p-4 border rounded-lg text-center ${
                            formData.payment_method === 'check' 
                                ? 'border-blue-500 bg-blue-50' 
                                : 'border-gray-300'
                        }`}
                    >
                        <div className="font-medium">Check</div>
                        <div className="text-sm text-gray-600">Mailed check</div>
                    </button>
                </div>
            </div>

            {formData.payment_method === 'paypal' && (
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        PayPal Email Address *
                    </label>
                    <input
                        type="email"
                        value={formData.payment_details.paypal_email}
                        onChange={(e) => handleInputChange('payment_details.paypal_email', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
            )}

            {formData.payment_method === 'bank' && (
                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Bank Name *
                        </label>
                        <input
                            type="text"
                            value={formData.payment_details.bank_name}
                            onChange={(e) => handleInputChange('payment_details.bank_name', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Routing Number *
                            </label>
                            <input
                                type="text"
                                value={formData.payment_details.routing_number}
                                onChange={(e) => handleInputChange('payment_details.routing_number', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Account Number *
                            </label>
                            <input
                                type="text"
                                value={formData.payment_details.account_number}
                                onChange={(e) => handleInputChange('payment_details.account_number', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            />
                        </div>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Account Type
                        </label>
                        <select
                            value={formData.payment_details.account_type}
                            onChange={(e) => handleInputChange('payment_details.account_type', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="checking">Checking</option>
                            <option value="savings">Savings</option>
                        </select>
                    </div>
                </div>
            )}

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex items-start">
                    <Shield className="h-5 w-5 text-yellow-600 mt-0.5 mr-3" />
                    <div>
                        <h3 className="text-sm font-medium text-yellow-800">Security Note</h3>
                        <p className="mt-1 text-sm text-yellow-700">
                            Your payment information is encrypted and stored securely. We never share your financial details with third parties.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl mx-auto">
                <div className="bg-white rounded-lg shadow-sm border p-8">
                    {/* NO PROGRESS BAR - REMOVED COMPLETELY */}

                    {/* Error Message */}
                    {error && (
                        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
                            <div className="flex items-center">
                                <AlertCircle className="h-5 w-5 text-red-600 mr-3" />
                                <p className="text-red-700">{error}</p>
                            </div>
                        </div>
                    )}

                    {/* Form Content */}
                    <form onSubmit={handleSubmit}>
                        {step === 1 && renderStep1()}
                        {step === 2 && renderStep2()}
                        {step === 3 && renderStep3()}

                        {/* Navigation Buttons */}
                        <div className="flex justify-between pt-8 border-t">
                            <button
                                type="button"
                                onClick={() => setStep(Math.max(1, step - 1))}
                                className={`px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 ${
                                    step === 1 ? 'invisible' : ''
                                }`}
                            >
                                {t('common.previous')}
                            </button>

                            {step < 3 ? (
                                <button
                                    type="button"
                                    onClick={() => setStep(step + 1)}
                                    disabled={!validateStep(step)}
                                    className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {t('common.next')}
                                </button>
                            ) : (
                                <button
                                    type="submit"
                                    disabled={!validateStep(step) || loading}
                                    className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                                >
                                    {loading ? (
                                        <>
                                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                            {t('pages.affiliate.registration.submitting')}
                                        </>
                                    ) : (
                                        t('pages.affiliate.registration.completeRegistration')
                                    )}
                                </button>
                            )}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AffiliateRegistration;