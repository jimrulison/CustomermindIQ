import React from 'react';
import { ExternalLink, Mail, Phone, MapPin } from 'lucide-react';

const Footer = ({ onLegalClick }) => {
    const currentYear = new Date().getFullYear();

    const handleLegalClick = (type) => {
        if (onLegalClick) {
            onLegalClick(type);
        } else {
            // Fallback to URL navigation
            const url = new URL(window.location);
            url.searchParams.set('legal', 'true');
            if (type === 'privacy') {
                url.hash = '#privacy';
            } else if (type === 'terms') {
                url.hash = '#terms';
            }
            window.location.href = url.toString();
        }
    };

    return (
        <footer className="bg-slate-900 border-t border-slate-800 mt-auto">
            <div className="container mx-auto px-4 py-12">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    {/* Company Information */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-bold text-white">Customer Mind IQ</h3>
                        <p className="text-slate-400 text-sm">
                            AI-powered customer intelligence platform helping businesses understand and optimize their customer relationships.
                        </p>
                        <div className="flex space-x-4">
                            <a href="#" className="text-slate-400 hover:text-white transition-colors">
                                <ExternalLink className="w-5 h-5" />
                            </a>
                        </div>
                    </div>

                    {/* Product Links */}
                    <div className="space-y-4">
                        <h4 className="text-md font-semibold text-white">Platform</h4>
                        <ul className="space-y-2 text-sm">
                            <li><button onClick={() => window.location.hash = 'customer-analytics'} className="text-slate-400 hover:text-white transition-colors text-left">AI Business Insights</button></li>
                            <li><button onClick={() => window.location.hash = 'customer-analytics'} className="text-slate-400 hover:text-white transition-colors text-left">Customer Analytics</button></li>
                            <li><button onClick={() => window.location.hash = 'productivity'} className="text-slate-400 hover:text-white transition-colors text-left">Productivity Intelligence</button></li>
                            <li><button onClick={() => window.location.hash = 'growth-acceleration'} className="text-slate-400 hover:text-white transition-colors text-left">Growth Acceleration</button></li>
                            <li><a href="?affiliate=true" className="text-slate-400 hover:text-white transition-colors">Affiliate Program</a></li>
                        </ul>
                    </div>

                    {/* Support Links */}
                    <div className="space-y-4">
                        <h4 className="text-md font-semibold text-white">Support</h4>
                        <ul className="space-y-2 text-sm">
                            <li><button onClick={() => window.location.hash = 'support'} className="text-slate-400 hover:text-white transition-colors text-left">Help Center</button></li>
                            <li><button onClick={() => window.location.hash = 'training'} className="text-slate-400 hover:text-white transition-colors text-left">Documentation</button></li>
                            <li><button onClick={() => window.location.hash = 'knowledge-base'} className="text-slate-400 hover:text-white transition-colors text-left">API Reference</button></li>
                            <li><a href="https://status.customermindiq.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-colors">Status Page</a></li>
                            <li><a href="mailto:support@customermindiq.com" className="text-slate-400 hover:text-white transition-colors">Contact Support</a></li>
                        </ul>
                    </div>

                    {/* Contact Information */}
                    <div className="space-y-4">
                        <h4 className="text-md font-semibold text-white">Contact</h4>
                        <div className="space-y-3 text-sm text-slate-400">
                            <div className="flex items-center">
                                <Mail className="w-4 h-4 mr-2 flex-shrink-0" />
                                <a href="mailto:support@customermindiq.com" className="hover:text-white transition-colors">
                                    support@customermindiq.com
                                </a>
                            </div>
                            <div className="flex items-center">
                                <Phone className="w-4 h-4 mr-2 flex-shrink-0" />
                                <span>1-800-MIND-IQ</span>
                            </div>
                            <div className="flex items-start">
                                <MapPin className="w-4 h-4 mr-2 flex-shrink-0 mt-0.5" />
                                <span>
                                    San Francisco, CA<br />
                                    United States
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bottom Section */}
                <div className="border-t border-slate-800 mt-12 pt-8">
                    <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                        <div className="text-sm text-slate-400">
                            © {currentYear} Customer Mind IQ. All rights reserved.
                        </div>
                        
                        {/* Legal Links */}
                        <div className="flex space-x-6 text-sm">
                            <button 
                                onClick={() => handleLegalClick('privacy')}
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                Privacy Policy
                            </button>
                            <button 
                                onClick={() => handleLegalClick('terms')}
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                Terms of Service
                            </button>
                            <a href="?affiliate=true" className="text-slate-400 hover:text-white transition-colors">
                                Affiliate Terms
                            </a>
                            <a href="#" className="text-slate-400 hover:text-white transition-colors">
                                Cookie Policy
                            </a>
                        </div>
                    </div>

                    {/* Compliance Notice */}
                    <div className="mt-6 pt-6 border-t border-slate-800">
                        <p className="text-xs text-slate-500 text-center">
                            Customer Mind IQ is committed to data protection and privacy. We comply with GDPR, CCPA, and other applicable data protection regulations. 
                            For privacy inquiries, contact us at privacy@customermindiq.com.
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;