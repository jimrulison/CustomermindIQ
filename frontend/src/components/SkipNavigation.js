import React from 'react';

const SkipNavigation = () => {
  return (
    <div className="skip-navigation">
      <a 
        href="#main-content" 
        className="skip-link focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-md focus:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 sr-only"
      >
        Skip to main content
      </a>
      <a 
        href="#main-navigation" 
        className="skip-link focus:not-sr-only focus:absolute focus:top-2 focus:left-40 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-md focus:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 sr-only"
      >
        Skip to navigation
      </a>
    </div>
  );
};

export default SkipNavigation;