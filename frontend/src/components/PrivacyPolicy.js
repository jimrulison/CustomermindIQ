import React from 'react';
import SEOHead from './SEOHead';
import FAQSchema from './FAQSchema';

const PrivacyPolicy = () => {
  const seoData = {
    title: "Privacy Policy - Customer Mind IQ | Data Protection & Security Compliance",
    description: "Comprehensive privacy policy for Customer Mind IQ platform. Learn how we protect your data with enterprise-grade security, GDPR compliance, and transparent data practices. Your privacy is our priority.",
    keywords: "privacy policy, data protection, GDPR compliance, customer data security, AI platform privacy, business intelligence privacy, data processing agreement, customer intelligence privacy, enterprise data security, privacy compliance",
    canonicalUrl: "https://customermindiq.com/privacy-policy",
    structuredData: {
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "Privacy Policy - Customer Mind IQ",
      "description": "Privacy policy and data protection information for Customer Mind IQ platform",
      "url": "https://customermindiq.com/privacy-policy",
      "isPartOf": {
        "@type": "WebSite",
        "name": "Customer Mind IQ",
        "url": "https://customermindiq.com"
      },
      "lastReviewed": new Date().toISOString().split('T')[0],
      "publisher": {
        "@type": "Organization",
        "name": "Fancy Free Living LLC",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "7901 4th St N STE 300",
          "addressLocality": "St. Petersburg",
          "addressRegion": "FL",
          "postalCode": "33702",
          "addressCountry": "US"
        }
      }
    }
  };

  const privacyFAQs = [
    {
      question: "How does Customer Mind IQ protect my customer data?",
      answer: "Customer Mind IQ uses enterprise-grade security measures including end-to-end encryption, regular security audits, SOC 2 compliance, and strict access controls. All data is encrypted both in transit and at rest using industry-standard AES-256 encryption."
    },
    {
      question: "Is Customer Mind IQ GDPR compliant?",
      answer: "Yes, Customer Mind IQ is fully GDPR compliant. We provide data processing agreements, support data subject rights, implement privacy by design, and ensure lawful basis for all data processing activities."
    },
    {
      question: "What personal information does Customer Mind IQ collect?",
      answer: "We collect only necessary information including contact details, account credentials, usage analytics, and business data you provide. We never collect sensitive personal information without explicit consent."
    },
    {
      question: "Can I delete my data from Customer Mind IQ?",
      answer: "Yes, you have the right to request deletion of your personal data. Contact us at info@FancyFreeLiving.com to request data deletion, and we will process your request within 30 days."
    },
    {
      question: "Does Customer Mind IQ share data with third parties?",
      answer: "We only share data with trusted service providers necessary for platform operation, and only under strict data processing agreements. We never sell your data to third parties."
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <SEOHead 
        title={seoData.title}
        description={seoData.description}
        keywords={seoData.keywords}
        canonicalUrl={seoData.canonicalUrl}
        structuredData={seoData.structuredData}
        pageType="article"
      />
      
      <FAQSchema 
        faqs={privacyFAQs} 
        pageTitle="Privacy Policy - Customer Mind IQ FAQ" 
      />
      
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Privacy Policy</h1>
        <p className="text-sm text-gray-600 mb-8">Last updated: {new Date().toLocaleDateString()}</p>
        
        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">1. Information We Collect</h2>
            <div className="prose max-w-none">
              <h3 className="text-lg font-medium text-gray-700 mb-2">Personal Information</h3>
              <p className="text-gray-600 mb-4">
                We collect information you provide directly to us, such as when you create an account, subscribe to our service, 
                or contact us for support. This may include:
              </p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Name and contact information (email address, phone number)</li>
                <li>Company information and billing details</li>
                <li>Account credentials and preferences</li>
                <li>Communication records and support requests</li>
              </ul>
              
              <h3 className="text-lg font-medium text-gray-700 mb-2 mt-6">Usage Information</h3>
              <p className="text-gray-600 mb-4">
                We automatically collect certain information about your use of our services, including:
              </p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Device information and IP address</li>
                <li>Usage patterns and feature interactions</li>
                <li>Log data and performance metrics</li>
                <li>Cookies and similar tracking technologies</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">2. How We Use Your Information</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">We use the information we collect to:</p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Provide, maintain, and improve our services</li>
                <li>Process transactions and manage your account</li>
                <li>Send you service-related communications</li>
                <li>Provide customer support and respond to inquiries</li>
                <li>Analyze usage patterns and optimize user experience</li>
                <li>Ensure security and prevent fraud</li>
                <li>Comply with legal obligations</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">3. Information Sharing</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                We do not sell, trade, or otherwise transfer your personal information to third parties except in the following circumstances:
              </p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>With your explicit consent</li>
                <li>To trusted service providers who assist in operating our platform</li>
                <li>When required by law or to protect our rights</li>
                <li>In connection with a business transaction (merger, acquisition, etc.)</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">4. Data Security</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                We implement appropriate technical and organizational measures to protect your personal information against 
                unauthorized access, alteration, disclosure, or destruction. These measures include:
              </p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Encryption of data in transit and at rest</li>
                <li>Regular security audits and monitoring</li>
                <li>Access controls and authentication requirements</li>
                <li>Employee training on data protection</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">5. Your Rights</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">You have the right to:</p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Access and update your personal information</li>
                <li>Request deletion of your data</li>
                <li>Opt-out of marketing communications</li>
                <li>Request data portability</li>
                <li>Object to processing in certain circumstances</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">6. Cookies and Tracking</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                We use cookies and similar technologies to enhance your experience, analyze usage, and provide personalized content. 
                You can manage your cookie preferences through our cookie consent banner or your browser settings.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">7. International Transfers</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                Your information may be transferred to and processed in countries other than your own. 
                We ensure appropriate safeguards are in place to protect your data in accordance with applicable privacy laws.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">8. Changes to This Policy</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                We may update this privacy policy from time to time. We will notify you of any material changes by posting 
                the new policy on our website and updating the "last updated" date.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">9. Contact Us</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                If you have any questions about this privacy policy or our data practices, please contact us:
              </p>
              <div className="bg-gray-100 p-4 rounded-lg">
                <p className="font-semibold text-gray-800">Fancy Free Living LLC</p>
                <p className="text-gray-600">7901 4th St N STE 300</p>
                <p className="text-gray-600">St. Petersburg, FL 33702 USA</p>
                <p className="text-gray-600">Email: info@FancyFreeLiving.com</p>
              </div>
            </div>
          </section>
          
          {/* Frequently Asked Questions */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Frequently Asked Questions</h2>
            <div className="space-y-6">
              {privacyFAQs.map((faq, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-6">
                  <h3 className="font-semibold text-gray-800 mb-3">{faq.question}</h3>
                  <p className="text-gray-600">{faq.answer}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
        
        {/* Copyright Notice */}
        <div className="mt-12 pt-8 border-t border-gray-200 text-center">
          <p className="text-gray-600 text-sm">
            © {new Date().getFullYear()} Fancy Free Living LLC. All rights reserved.
          </p>
          <p className="text-gray-500 text-xs mt-1">
            Customer Mind IQ™ is a trademark of Fancy Free Living LLC
          </p>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;