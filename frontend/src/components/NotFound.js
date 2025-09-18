import React from 'react';
import { Link } from 'react-router-dom';
import SEOHead from './SEOHead';
import { ArrowLeft, Home, Search, Mail, Phone, MapPin } from 'lucide-react';

const NotFound = () => {
  return (
    <>
      <SEOHead
        title="Page Not Found (404) - CustomerMind IQ"
        description="The page you're looking for doesn't exist. Explore our AI-powered customer intelligence platform or return to the homepage."
        keywords="404, page not found, CustomerMind IQ, customer intelligence"
        canonicalUrl="https://customermindiq.com/404"
        noIndex={true}
      />
      
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center px-4">
        <div className="max-w-4xl mx-auto text-center">
          {/* 404 Visual */}
          <div className="mb-8">
            <div className="text-8xl lg:text-9xl font-bold text-transparent bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text mb-4">
              404
            </div>
            <div className="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
          </div>

          {/* Main Message */}
          <div className="mb-12">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
              Oops! Page Not Found
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
              The page you're looking for seems to have vanished into the digital void. 
              But don't worry – our AI-powered customer intelligence platform is still here to help you succeed!
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Link 
              to="/" 
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              <Home className="w-5 h-5 mr-2" />
              Go Home
            </Link>
            
            <Link 
              to="/dashboard" 
              className="inline-flex items-center px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-blue-600 hover:text-blue-600 transition-all duration-200"
            >
              <Search className="w-5 h-5 mr-2" />
              View Dashboard
            </Link>
            
            <Link 
              to="/contact" 
              className="inline-flex items-center px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-purple-600 hover:text-purple-600 transition-all duration-200"
            >
              <Mail className="w-5 h-5 mr-2" />
              Contact Support
            </Link>
          </div>

          {/* Popular Links */}
          <div className="bg-white rounded-2xl p-8 shadow-lg mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Popular Pages</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Link to="/customer-intelligence" className="p-4 rounded-lg hover:bg-blue-50 transition-colors group">
                <div className="text-blue-600 font-semibold group-hover:text-blue-700">Customer Intelligence</div>
                <div className="text-sm text-gray-500">91.8% accurate churn prediction</div>
              </Link>
              
              <Link to="/revenue-analytics" className="p-4 rounded-lg hover:bg-purple-50 transition-colors group">
                <div className="text-purple-600 font-semibold group-hover:text-purple-700">Revenue Analytics</div>
                <div className="text-sm text-gray-500">95% accurate forecasting</div>
              </Link>
              
              <Link to="/pricing" className="p-4 rounded-lg hover:bg-green-50 transition-colors group">
                <div className="text-green-600 font-semibold group-hover:text-green-700">Pricing Plans</div>
                <div className="text-sm text-gray-500">Starting at $49/month</div>
              </Link>
              
              <Link to="/support" className="p-4 rounded-lg hover:bg-orange-50 transition-colors group">
                <div className="text-orange-600 font-semibold group-hover:text-orange-700">Get Support</div>
                <div className="text-sm text-gray-500">24/7 customer success</div>
              </Link>
            </div>
          </div>

          {/* Search Box */}
          <div className="bg-gray-50 rounded-2xl p-8 mb-12">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Still looking for something?</h3>
            <div className="max-w-md mx-auto">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search our platform..."
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      window.location.href = `/?search=${encodeURIComponent(e.target.value)}`;
                    }
                  }}
                />
                <Search className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl p-8">
            <h3 className="text-2xl font-bold mb-6">Need Help? Contact Us</h3>
            <div className="grid md:grid-cols-3 gap-6 text-center">
              <div className="flex flex-col items-center">
                <Mail className="w-8 h-8 mb-3 text-blue-100" />
                <div className="font-semibold">Email Support</div>
                <a href="mailto:info@FancyFreeLiving.com" className="text-blue-100 hover:text-white transition-colors">
                  info@FancyFreeLiving.com
                </a>
              </div>
              
              <div className="flex flex-col items-center">
                <Phone className="w-8 h-8 mb-3 text-blue-100" />
                <div className="font-semibold">Phone Support</div>
                <a href="tel:+18002646373" className="text-blue-100 hover:text-white transition-colors">
                  1-800-CMIND-IQ
                </a>
              </div>
              
              <div className="flex flex-col items-center">
                <MapPin className="w-8 h-8 mb-3 text-blue-100" />
                <div className="font-semibold">Office Address</div>
                <div className="text-blue-100">
                  7901 4th St N STE 300<br />
                  St. Petersburg, FL 33702
                </div>
              </div>
            </div>
          </div>

          {/* Fun Message */}
          <div className="mt-12 text-center">
            <p className="text-gray-500 italic">
              "Even our 404 page is powered by customer intelligence – we know you'll find what you need!" 🚀
            </p>
          </div>
        </div>
      </div>
    </>
  );
};

export default NotFound;