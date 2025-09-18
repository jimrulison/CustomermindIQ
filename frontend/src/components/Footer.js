import React from 'react';
import { Link } from 'react-router-dom';
import { Mail, Phone, MapPin, ExternalLink } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-16">
      <div className="container mx-auto px-6">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-2xl font-bold mb-4">CustomerMind IQ</h3>
            <p className="text-gray-400 mb-6">
              AI-powered customer intelligence platform helping businesses achieve 300-500% ROI through predictive analytics and automation.
            </p>
            
            {/* Company Details */}
            <div className="space-y-3">
              <div className="text-sm text-gray-300 font-medium">Powered by:</div>
              <div className="text-white font-semibold">Fancy Free Living LLC</div>
            </div>
          </div>
          
          {/* Platform Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Platform</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link to="/customer-intelligence" className="hover:text-white transition-colors">Customer Intelligence</Link></li>
              <li><Link to="/revenue-analytics" className="hover:text-white transition-colors">Revenue Analytics</Link></li>
              <li><Link to="/marketing-automation" className="hover:text-white transition-colors">Marketing Automation</Link></li>
              <li><Link to="/website-intelligence" className="hover:text-white transition-colors">Website Intelligence</Link></li>
              <li><Link to="/integrations" className="hover:text-white transition-colors">Integrations</Link></li>
              <li><Link to="/pricing" className="hover:text-white transition-colors">Pricing</Link></li>
            </ul>
          </div>
          
          {/* Company Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link to="/about" className="hover:text-white transition-colors">About Us</Link></li>
              <li><Link to="/blog" className="hover:text-white transition-colors">Blog</Link></li>
              <li><Link to="/careers" className="hover:text-white transition-colors">Careers</Link></li>
              <li><Link to="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              <li><Link to="/affiliates" className="hover:text-white transition-colors">Affiliate Program</Link></li>
              <li><Link to="/security" className="hover:text-white transition-colors">Security</Link></li>
            </ul>
          </div>
          
          {/* Contact Information */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Information</h4>
            <div className="space-y-4">
              <div className="flex items-start">
                <MapPin className="w-5 h-5 text-gray-400 mt-1 mr-3 flex-shrink-0" />
                <div>
                  <div className="text-white font-medium">Fancy Free Living LLC</div>
                  <div className="text-gray-400 text-sm">
                    7901 4th St N STE 300<br />
                    St. Petersburg, FL 33702<br />
                    United States
                  </div>
                </div>
              </div>
              
              <div className="flex items-center">
                <Mail className="w-5 h-5 text-gray-400 mr-3" />
                <a 
                  href="mailto:info@FancyFreeLiving.com" 
                  className="text-blue-400 hover:text-blue-300 transition-colors text-sm"
                >
                  info@FancyFreeLiving.com
                </a>
              </div>
              
              <div className="flex items-center">
                <Phone className="w-5 h-5 text-gray-400 mr-3" />
                <a 
                  href="tel:+18002646373" 
                  className="text-blue-400 hover:text-blue-300 transition-colors text-sm"
                >
                  1-800-CMIND-IQ
                </a>
              </div>
            </div>

            {/* Business Hours */}
            <div className="mt-6">
              <div className="text-sm text-gray-300 font-medium mb-2">Business Hours:</div>
              <div className="text-xs text-gray-400">
                Monday - Friday: 9:00 AM - 6:00 PM EST<br />
                Weekend: Emergency support only
              </div>
            </div>
          </div>
        </div>
        
        {/* Support & Legal Links */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-lg font-semibold mb-4">Support & Resources</h4>
              <ul className="grid grid-cols-2 gap-2 text-gray-400 text-sm">
                <li><Link to="/support" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link to="/training" className="hover:text-white transition-colors">Training</Link></li>
                <li><Link to="/documentation" className="hover:text-white transition-colors">Documentation</Link></li>
                <li><Link to="/api" className="hover:text-white transition-colors">API Reference</Link></li>
                <li><Link to="/status" className="hover:text-white transition-colors">System Status</Link></li>
                <li><Link to="/community" className="hover:text-white transition-colors">Community</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold mb-4">Legal & Compliance</h4>
              <ul className="grid grid-cols-2 gap-2 text-gray-400 text-sm">
                <li><Link to="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link to="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
                <li><Link to="/compliance" className="hover:text-white transition-colors">Compliance</Link></li>
                <li><Link to="/gdpr" className="hover:text-white transition-colors">GDPR</Link></li>
                <li><Link to="/cookies" className="hover:text-white transition-colors">Cookie Policy</Link></li>
                <li><Link to="/legal" className="hover:text-white transition-colors">Legal</Link></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="text-center md:text-left mb-4 md:mb-0">
            <p className="text-gray-400 text-sm">
              &copy; 2025 Fancy Free Living LLC. All rights reserved.
            </p>
            <p className="text-gray-500 text-xs mt-1">
              CustomerMind IQ is a trademark of Fancy Free Living LLC
            </p>
          </div>
          
          {/* Social Links & Trust Badges */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-xs text-gray-400">
              <span className="inline-flex items-center px-2 py-1 bg-green-900/20 text-green-400 rounded">
                ✓ SOC 2 Compliant
              </span>
              <span className="inline-flex items-center px-2 py-1 bg-blue-900/20 text-blue-400 rounded">
                ✓ GDPR Ready
              </span>
              <span className="inline-flex items-center px-2 py-1 bg-purple-900/20 text-purple-400 rounded">
                ✓ 99.9% Uptime
              </span>
            </div>
          </div>
        </div>

        {/* Emergency Contact Notice */}
        <div className="mt-6 p-4 bg-gray-800 rounded-lg">
          <div className="text-center text-sm text-gray-300">
            <strong>Emergency Support:</strong> For critical system issues affecting multiple users, 
            contact our emergency hotline: 
            <a href="tel:+18002646373" className="text-blue-400 hover:text-blue-300 ml-1">
              1-800-CMIND-IQ
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;