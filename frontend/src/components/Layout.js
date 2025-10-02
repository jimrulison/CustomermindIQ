import React, { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import SchemaMarkup from './SchemaMarkup';
import BreadcrumbSchema from './BreadcrumbSchema';

// Lazy load Footer
const Footer = React.lazy(() => import('./Footer'));

// Loading component for Suspense
const LoadingSpinner = () => (
  <div className="flex items-center justify-center h-64">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
      <p className="text-slate-400">Loading...</p>
    </div>
  </div>
);

const Layout = ({ 
  currentPage, 
  onNavigate, 
  onSignOut, 
  pageHistory,
  handleGoBack,
  user, 
  analyticsSection,
  announcements,
  dismissAnnouncement,
  showLegalDocs,
  setShowLegalDocs 
}) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Schema Markup for SEO */}
      <SchemaMarkup />
      <BreadcrumbSchema currentPage={currentPage} />
      
      <Header 
        currentPage={currentPage}
        onNavigate={onNavigate}
        onSignOut={onSignOut}
        onGoBack={pageHistory.length > 1 ? handleGoBack : null}
        user={user}
        analyticsSection={analyticsSection}
      />
      
      {/* Announcement Banner */}
      {announcements.filter(ann => ann.active).map(announcement => (
        <div key={announcement.id} className={`${
          announcement.type === 'warning' ? 'bg-yellow-600/90' :
          announcement.type === 'error' ? 'bg-red-600/90' :
          'bg-blue-600/90'
        } backdrop-blur-sm text-white px-6 py-3`}>
          <div className="container mx-auto flex items-center justify-between">
            <span className="text-sm font-medium">{announcement.message}</span>
            {announcement.dismissible && (
              <button 
                onClick={() => dismissAnnouncement(announcement.id)}
                className="text-white/80 hover:text-white"
              >
                ✕
              </button>
            )}
          </div>
        </div>
      ))}
      
      {/* Main content area */}
      <main>
        <Outlet />
      </main>

      {/* Footer */}
      <Suspense fallback={<LoadingSpinner />}>
        <Footer onLegalClick={(type) => {
          if (type === 'privacy') {
            setShowLegalDocs(true);
            // Update URL to show privacy policy
            const url = new URL(window.location);
            url.searchParams.set('legal', 'true');
            url.hash = '#privacy';
            window.history.pushState({}, '', url);
          } else if (type === 'terms') {
            setShowLegalDocs(true);
            // Update URL to show terms of service
            const url = new URL(window.location);
            url.searchParams.set('legal', 'true');
            url.hash = '#terms';
            window.history.pushState({}, '', url);
          }
        }} />
      </Suspense>
    </div>
  );
};

export default Layout;