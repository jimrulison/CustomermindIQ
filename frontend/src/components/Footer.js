import React from 'react';
import { Link } from 'react-router-dom';
import { Mail, MapPin, Phone } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const openCookieSettings = () => {
    // Remove existing consent to show the banner again
    localStorage.removeItem('cookieConsent');
    localStorage.removeItem('cookieConsentDate');
    // Reload the page to show cookie banner
    window.location.reload();
  };

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* Company Info */}
          <div className="col-span-1 lg:col-span-2">
            <div className="mb-6">
              <h3 className="text-xl font-bold mb-4">Customer Mind IQ</h3>
              <p className="text-gray-300 mb-4">
                AI-driven customer intelligence platform helping businesses understand and optimize their customer relationships.
              </p>
            </div>
            
            {/* Contact Information */}
            <div className="space-y-3">
              <h4 className="font-semibold text-lg mb-3">Contact Information</h4>
              
              <div className="flex items-start gap-3">
                <MapPin className="h-5 w-5 text-blue-400 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-medium">Fancy Free Living LLC</p>
                  <p className="text-gray-300">7901 4th St N STE 300</p>
                  <p className="text-gray-300">St. Petersburg, FL 33702 USA</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <Mail className="h-5 w-5 text-blue-400 flex-shrink-0" />
                <a 
                  href="mailto:info@FancyFreeLiving.com" 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  info@FancyFreeLiving.com
                </a>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-lg mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-300 hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-gray-300 hover:text-white transition-colors">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link to="/pricing" className="text-gray-300 hover:text-white transition-colors">
                  Pricing
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-300 hover:text-white transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold text-lg mb-4">Legal</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/privacy-policy" className="text-gray-300 hover:text-white transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link to="/terms-of-service" className="text-gray-300 hover:text-white transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <button 
                  onClick={openCookieSettings}
                  className="text-gray-300 hover:text-white transition-colors text-left"
                >
                  Cookie Settings
                </button>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-center md:text-left">
              <p className="text-gray-400 text-sm font-medium">
                © {currentYear} Fancy Free Living LLC. All rights reserved.
              </p>
              <p className="text-gray-500 text-xs mt-1">
                Customer Mind IQ™ is a trademark of Fancy Free Living LLC
              </p>
            </div>
            <div className="flex items-center space-x-6 mt-4 md:mt-0">
              <p className="text-gray-400 text-sm">
                Made with ❤️ for better customer relationships
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;