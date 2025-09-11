import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { FileText, Shield, ArrowLeft, ExternalLink, Calendar, Users, Mail } from 'lucide-react';

const LegalDocuments = ({ onBack }) => {
    const { t } = useTranslation();
    const [activeDocument, setActiveDocument] = useState('privacy');

    const documents = [
        {
            id: 'privacy',
            title: 'Privacy Policy',
            icon: Shield,
            description: 'How we collect, use, and protect your personal information',
            lastUpdated: 'January 9, 2025'
        },
        {
            id: 'terms',
            title: 'Terms of Service',
            icon: FileText,
            description: 'Legal agreement governing your use of our platform',
            lastUpdated: 'January 9, 2025'
        }
    ];

    const privacyContent = {
        sections: [
            {
                title: "1. Introduction",
                content: "Customer Mind IQ is committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI-powered customer intelligence platform and related services."
            },
            {
                title: "2. Information We Collect",
                content: "We collect Personal Information including account information (name, email, phone, company details), usage information (login data, service usage patterns, API usage), and communication information (support tickets, chat messages, feedback). We also collect Customer Data through your use of our Service and automatically collected technical information.",
                subsections: [
                    "Account Information: Name, email, phone, company details, billing information",
                    "Usage Information: Login credentials, service usage patterns, feature utilization",
                    "Customer Data: Demographics, transaction history, analytics, customer journey data",
                    "Technical Information: IP address, browser type, access times, cookies"
                ]
            },
            {
                title: "3. How We Use Your Information",
                content: "We use your information to provide and improve our Service, process transactions, authenticate users, deliver customer support, generate AI-powered business insights, analyze customer behavior trends, and communicate service updates.",
                subsections: [
                    "Service provision and maintenance",
                    "Analytics and AI-powered business insights", 
                    "Customer support and communication",
                    "Legal compliance and security protection"
                ]
            },
            {
                title: "4. Information Sharing and Disclosure",
                content: "We may share your information with trusted service providers (cloud hosting, payment processing, analytics tools), during business transfers, when legally required, and as aggregate/de-identified information for research purposes."
            },
            {
                title: "5. Data Security",
                content: "We implement comprehensive security measures including encryption of data in transit and at rest, access controls, regular security assessments, and employee training. We have established data breach response procedures to notify users within 72 hours when required."
            },
            {
                title: "6. Your Rights and Choices",
                content: "You have rights to access, correct, and control your personal information. EU users have additional GDPR rights including erasure, data portability, and processing restrictions. California users have CCPA rights including knowing what information we collect and requesting deletion.",
                subsections: [
                    "Access and correct your personal information",
                    "GDPR rights for EU users (erasure, portability, restriction)",
                    "CCPA rights for California users",
                    "Cookie management and preferences"
                ]
            },
            {
                title: "7. International Data Transfers",
                content: "We may transfer your information internationally with appropriate safeguards including Standard Contractual Clauses, adequacy decisions, and binding corporate rules. Data is primarily processed in the United States with EU processing for EU customers."
            },
            {
                title: "8. Contact Information",
                content: "For privacy inquiries, contact us at privacy@customermindiq.com. EU users may contact our Data Protection Officer at dpo@customermindiq.com. You have the right to lodge complaints with supervisory authorities."
            }
        ]
    };

    const termsContent = {
        sections: [
            {
                title: "1. Agreement to Terms",
                content: "These Terms of Service constitute a legally binding agreement regarding your use of our AI-powered customer intelligence platform. By accessing or using our Service, you agree to be bound by these Terms."
            },
            {
                title: "2. Service Description",
                content: "Customer Mind IQ provides an AI-driven customer intelligence system with core modules including AI Business Insights, Daily Productivity Intelligence, Customer Analytics, Website Analytics, Real-Time Health monitoring, Competitive Intelligence, Executive Intelligence, Growth Acceleration Engine, and Knowledge Base.",
                subsections: [
                    "Launch Plan: Essential features for small businesses",
                    "Growth Plan: Advanced features for growing companies",
                    "Scale Plan: Enterprise features for large organizations",
                    "Affiliate Program: Commission-based referral system"
                ]
            },
            {
                title: "3. Account Registration and Eligibility",
                content: "You must be at least 18 years old with legal capacity to enter binding agreements. You're responsible for maintaining account security, providing accurate information, and promptly notifying us of unauthorized use."
            },
            {
                title: "4. Subscription Plans and Billing",
                content: "Subscriptions are billed in advance monthly or annually. All fees are non-refundable except as expressly stated. We reserve the right to modify pricing with 30 days' notice. Failed payments may result in service suspension.",
                subsections: [
                    "Payment processing through secure third-party processors",
                    "Price changes with 30-day notice",
                    "Free trials and promotional offers",
                    "Automatic conversion from trial to paid plans"
                ]
            },
            {
                title: "5. Acceptable Use Policy",
                content: "You may use our Service for lawful business purposes including analyzing customer data and generating business insights. Prohibited uses include illegal activities, service misuse, unauthorized access attempts, and data processing violations."
            },
            {
                title: "6. Data and Privacy",
                content: "You retain ownership of your Customer Data. We implement industry-standard security measures and process data according to our Privacy Policy and applicable laws. Upon termination, you may export data for a limited period before deletion."
            },
            {
                title: "7. Intellectual Property Rights",
                content: "We own all Service-related technology, software, algorithms, interfaces, and brand elements. You receive a limited license to use our Service. Any feedback you provide becomes our property."
            },
            {
                title: "8. Service Availability and Performance",
                content: "We target 99.9% uptime with regular maintenance windows. Our Service is provided 'as is' without warranties. We may perform updates and modifications to improve performance."
            },
            {
                title: "9. Limitation of Liability",
                content: "Our total liability is limited to the amount you paid in the preceding 12 months or $1,000, whichever is greater. We're not liable for indirect damages, lost profits, or business interruption except where prohibited by law."
            },
            {
                title: "10. Termination",
                content: "You may terminate your account anytime. We may terminate for Terms violations, non-payment, or illegal activities. Upon termination, access is discontinued and data export may be available for a limited period."
            }
        ]
    };

    const renderDocument = () => {
        const content = activeDocument === 'privacy' ? privacyContent : termsContent;
        const doc = documents.find(d => d.id === activeDocument);

        return (
            <div className="space-y-8">
                {/* Document Header */}
                <div className="text-center border-b border-slate-700 pb-8">
                    <div className="flex items-center justify-center mb-4">
                        <doc.icon className="w-12 h-12 text-blue-400 mr-4" />
                        <h1 className="text-4xl font-bold text-white">{doc.title}</h1>
                    </div>
                    <p className="text-slate-400 text-lg mb-4">{doc.description}</p>
                    <div className="flex items-center justify-center text-sm text-slate-500">
                        <Calendar className="w-4 h-4 mr-2" />
                        <span>Last Updated: {doc.lastUpdated}</span>
                    </div>
                </div>

                {/* Document Content */}
                <div className="prose prose-invert max-w-none">
                    {content.sections.map((section, index) => (
                        <div key={index} className="mb-8">
                            <h2 className="text-2xl font-semibold text-white mb-4 border-l-4 border-blue-500 pl-4">
                                {section.title}
                            </h2>
                            <div className="text-slate-300 leading-relaxed mb-4">
                                {section.content}
                            </div>
                            {section.subsections && (
                                <ul className="space-y-2 ml-6">
                                    {section.subsections.map((subsection, subIndex) => (
                                        <li key={subIndex} className="text-slate-400 text-sm flex items-start">
                                            <span className="w-2 h-2 bg-blue-400 rounded-full mr-3 mt-2 flex-shrink-0"></span>
                                            {subsection}
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    ))}
                </div>

                {/* Contact Information */}
                <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6 mt-12">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                        <Mail className="w-5 h-5 mr-2 text-blue-400" />
                        Contact Information
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-300">
                        <div>
                            <strong className="text-white">General Inquiries:</strong><br />
                            support@customermindiq.com
                        </div>
                        <div>
                            <strong className="text-white">Legal Matters:</strong><br />
                            legal@customermindiq.com
                        </div>
                        {activeDocument === 'privacy' && (
                            <>
                                <div>
                                    <strong className="text-white">Privacy Inquiries:</strong><br />
                                    privacy@customermindiq.com
                                </div>
                                <div>
                                    <strong className="text-white">Data Protection Officer:</strong><br />
                                    dpo@customermindiq.com
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
            <div className="container mx-auto px-4 py-8">
                {/* Header Navigation */}
                <div className="flex items-center justify-between mb-8">
                    <button
                        onClick={onBack}
                        className="flex items-center text-slate-400 hover:text-white transition-colors"
                    >
                        <ArrowLeft className="w-5 h-5 mr-2" />
                        Back to Dashboard
                    </button>

                    <div className="flex items-center space-x-2">
                        <Users className="w-5 h-5 text-slate-400" />
                        <span className="text-slate-400 text-sm">Customer Mind IQ Legal Center</span>
                    </div>
                </div>

                {/* Document Selector */}
                <div className="flex flex-col lg:flex-row gap-8">
                    {/* Sidebar */}
                    <div className="lg:w-1/4">
                        <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-6 sticky top-8">
                            <h3 className="text-lg font-semibold text-white mb-4">Legal Documents</h3>
                            <div className="space-y-2">
                                {documents.map((doc) => (
                                    <button
                                        key={doc.id}
                                        onClick={() => setActiveDocument(doc.id)}
                                        className={`w-full text-left p-4 rounded-lg transition-all duration-200 ${
                                            activeDocument === doc.id
                                                ? 'bg-blue-600 text-white shadow-lg'
                                                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
                                        }`}
                                    >
                                        <div className="flex items-center">
                                            <doc.icon className={`w-5 h-5 mr-3 ${
                                                activeDocument === doc.id ? 'text-white' : 'text-slate-500'
                                            }`} />
                                            <div>
                                                <div className="font-medium">{doc.title}</div>
                                                <div className="text-xs opacity-75 mt-1">
                                                    Updated {doc.lastUpdated}
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                ))}
                            </div>

                            {/* Quick Actions */}
                            <div className="mt-8 pt-6 border-t border-slate-700">
                                <h4 className="text-sm font-medium text-slate-400 mb-3">Quick Actions</h4>
                                <div className="space-y-2">
                                    <button className="w-full text-left text-sm text-slate-400 hover:text-white flex items-center">
                                        <ExternalLink className="w-4 h-4 mr-2" />
                                        Download PDF
                                    </button>
                                    <button className="w-full text-left text-sm text-slate-400 hover:text-white flex items-center">
                                        <Mail className="w-4 h-4 mr-2" />
                                        Contact Legal Team
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Main Content */}
                    <div className="lg:w-3/4">
                        <div className="bg-slate-800/30 rounded-xl border border-slate-700 p-8">
                            {renderDocument()}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LegalDocuments;