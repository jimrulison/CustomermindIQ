import React from 'react';
import { Helmet } from 'react-helmet-async';

const TermsOfService = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Helmet>
        <title>Terms of Service - Customer Mind IQ</title>
        <meta name="description" content="Terms of Service for Customer Mind IQ platform. Learn about the terms and conditions of using our services." />
        <meta name="robots" content="index, follow" />
      </Helmet>
      
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Terms of Service</h1>
        <p className="text-sm text-gray-600 mb-8">Last updated: {new Date().toLocaleDateString()}</p>
        
        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">1. Acceptance of Terms</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                By accessing or using Customer Mind IQ services, you agree to be bound by these Terms of Service. 
                If you do not agree to these terms, please do not use our services.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">2. Description of Service</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                Customer Mind IQ is an AI-driven customer intelligence platform that provides analytics, insights, 
                and tools to help businesses understand and optimize their customer relationships. Our services include:
              </p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Customer analytics and behavioral insights</li>
                <li>AI-powered recommendations and predictions</li>
                <li>Dashboard and reporting tools</li>
                <li>Integration capabilities with third-party platforms</li>
                <li>Customer support and training resources</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">3. User Accounts and Registration</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                To access certain features of our service, you must create an account. You agree to:
              </p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Provide accurate and complete information during registration</li>
                <li>Maintain the security of your account credentials</li>
                <li>Notify us immediately of any unauthorized use</li>
                <li>Accept responsibility for all activities under your account</li>
                <li>Use the service only for lawful purposes</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">4. Subscription and Payment Terms</h2>
            <div className="prose max-w-none">
              <h3 className="text-lg font-medium text-gray-700 mb-2">Subscription Plans</h3>
              <p className="text-gray-600 mb-4">
                We offer various subscription plans with different features and usage limits. 
                Subscription fees are billed in advance on a monthly or annual basis.
              </p>
              
              <h3 className="text-lg font-medium text-gray-700 mb-2 mt-6">Free Trial</h3>
              <p className="text-gray-600 mb-4">
                We may offer a free trial period for new users. Trial accounts are subject to usage limitations 
                and may be converted to paid subscriptions at the end of the trial period.
              </p>
              
              <h3 className="text-lg font-medium text-gray-700 mb-2 mt-6">Payments and Refunds</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>All fees are non-refundable unless otherwise specified</li>
                <li>You authorize us to charge your payment method for applicable fees</li>
                <li>Failure to pay may result in suspension or termination of service</li>
                <li>We reserve the right to change pricing with 30 days notice</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">5. Acceptable Use Policy</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">You agree not to:</p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>Use the service for any illegal or unauthorized purpose</li>
                <li>Attempt to gain unauthorized access to our systems</li>
                <li>Upload or transmit malicious code or content</li>
                <li>Violate any applicable laws or regulations</li>
                <li>Interfere with the operation of the service</li>
                <li>Share your account credentials with others</li>
                <li>Use the service to harm or harass others</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">6. Data and Privacy</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                Your use of our service is also governed by our Privacy Policy. We collect and process data 
                as described in our Privacy Policy to provide and improve our services.
              </p>
              <h3 className="text-lg font-medium text-gray-700 mb-2 mt-4">Your Data</h3>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>You retain ownership of your data and content</li>
                <li>You grant us necessary rights to process your data for service provision</li>
                <li>You are responsible for the accuracy and legality of your data</li>
                <li>We implement appropriate security measures to protect your data</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">7. Intellectual Property</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                The Customer Mind IQ platform, including all software, content, and intellectual property, 
                is owned by Fancy Free Living LLC and protected by copyright and other intellectual property laws.
              </p>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                <li>We grant you a limited, non-exclusive license to use our service</li>
                <li>You may not copy, modify, or distribute our intellectual property</li>
                <li>All trademarks and service marks are the property of their respective owners</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">8. Service Availability</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                While we strive to maintain high service availability, we do not guarantee uninterrupted access. 
                We may temporarily suspend service for maintenance, updates, or due to circumstances beyond our control.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">9. Limitation of Liability</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                To the maximum extent permitted by law, Fancy Free Living LLC shall not be liable for any indirect, 
                incidental, special, consequential, or punitive damages arising from your use of our service.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">10. Termination</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                Either party may terminate this agreement at any time. We may suspend or terminate your account 
                for violation of these terms. Upon termination, your right to use the service ceases immediately.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">11. Changes to Terms</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                We reserve the right to modify these terms at any time. Material changes will be communicated 
                through our platform or via email. Continued use of our service constitutes acceptance of updated terms.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">12. Governing Law</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                These terms are governed by the laws of the State of Florida, United States, without regard to 
                conflict of law principles.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">13. Contact Information</h2>
            <div className="prose max-w-none">
              <p className="text-gray-600 mb-4">
                If you have any questions about these Terms of Service, please contact us:
              </p>
              <div className="bg-gray-100 p-4 rounded-lg">
                <p className="font-semibold text-gray-800">Fancy Free Living LLC</p>
                <p className="text-gray-600">7901 4th St N STE 300</p>
                <p className="text-gray-600">St. Petersburg, FL 33702 USA</p>
                <p className="text-gray-600">Email: info@FancyFreeLiving.com</p>
              </div>
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

export default TermsOfService;