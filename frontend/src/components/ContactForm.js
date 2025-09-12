import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Mail,
  Phone,
  Building,
  Globe,
  Send,
  CheckCircle,
  Loader2
} from 'lucide-react';
import axios from 'axios';

const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    website: '',
    subject: '',
    message: ''
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [reference, setReference] = useState('');

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      const response = await axios.post(`${backendUrl}/api/odoo/contact-form/submit`, {
        ...formData,
        source: 'website_contact_form'
      });

      if (response.data.status === 'success') {
        setSuccess(true);
        setReference(response.data.reference);
        setFormData({
          name: '',
          email: '',
          phone: '',
          company: '',
          website: '',
          subject: '',
          message: ''
        });
      }
    } catch (error) {
      console.error('Contact form submission error:', error);
      setError('Failed to submit your message. Please try again or contact us directly.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <div className="mb-6">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Message Sent Successfully!</h2>
            <p className="text-gray-600 mb-4">
              Thank you for contacting CustomerMind IQ. We've received your message and will get back to you soon.
            </p>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-600">
                Your reference number: <span className="font-mono font-semibold text-gray-900">{reference}</span>
              </p>
            </div>
          </div>
          <Button 
            onClick={() => setSuccess(false)}
            variant="outline"
          >
            Send Another Message
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-4 sm:p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
        {/* Contact Information */}
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">Get in Touch</h1>
            <p className="text-gray-600 text-base sm:text-lg leading-relaxed">
              Ready to transform your customer intelligence? Contact our team to learn how CustomerMind IQ can help you unlock growth opportunities.
            </p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-50 transition-colors">
              <Mail className="w-6 h-6 text-blue-600 flex-shrink-0" />
              <span className="text-gray-600 text-sm sm:text-base break-all">support@customermindiq.com</span>
            </div>
            <div className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-50 transition-colors">
              <Phone className="w-6 h-6 text-blue-600 flex-shrink-0" />
              <span className="text-gray-600 text-sm sm:text-base">+1 (555) 123-4567</span>
            </div>
            <div className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-50 transition-colors">
              <Globe className="w-6 h-6 text-blue-600 flex-shrink-0" />
              <span className="text-gray-600 text-sm sm:text-base break-all">www.customermindiq.com</span>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 sm:p-6">
            <h3 className="font-semibold text-blue-900 mb-3">Why Choose CustomerMind IQ?</h3>
            <ul className="text-blue-800 text-sm sm:text-base space-y-2">
              <li>• AI-powered customer intelligence platform</li>
              <li>• 14 specialized analytics modules</li>
              <li>• Growth acceleration engine for annual subscribers</li>
              <li>• Real-time insights and predictions</li>
              <li>• Comprehensive support and training</li>
            </ul>
          </div>
        </div>

        {/* Contact Form */}
        <Card className="h-fit">
          <CardHeader className="pb-4">
            <CardTitle className="text-xl sm:text-2xl">Send us a Message</CardTitle>
            <CardDescription className="text-sm sm:text-base">
              Fill out the form below and we'll get back to you within 24 hours.
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0">
            {error && (
              <Alert className="mb-6 border-red-200 bg-red-50">
                <AlertDescription className="text-red-800">{error}</AlertDescription>
              </Alert>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Full Name *
                  </label>
                  <Input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder="John Doe"
                    className="min-h-[48px] text-base"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Email Address *
                  </label>
                  <Input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="john@company.com"
                    className="min-h-[48px] text-base"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Phone Number
                  </label>
                  <Input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="+1 (555) 123-4567"
                    className="min-h-[48px] text-base"
                  />
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Company Name
                  </label>
                  <Input
                    type="text"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    placeholder="Your Company"
                    className="min-h-[48px] text-base"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">
                  Website
                </label>
                <Input
                  type="url"
                  name="website"
                  value={formData.website}
                  onChange={handleChange}
                  placeholder="https://yourcompany.com"
                  className="min-h-[48px] text-base"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">
                  Subject *
                </label>
                <Input
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  placeholder="How can we help you?"
                  className="min-h-[48px] text-base"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">
                  Message *
                </label>
                <Textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={6}
                  placeholder="Tell us about your needs, challenges, or questions..."
                  className="min-h-[120px] text-base resize-none"
                />
              </div>

              <Button 
                type="submit" 
                disabled={loading}
                className="w-full min-h-[56px] text-base font-semibold"
              >
                {loading && <Loader2 className="w-5 h-5 mr-2 animate-spin" />}
                <Send className="w-5 h-5 mr-2" />
                Send Message
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ContactForm;