import React, { useState, useEffect } from 'react';

const ScreenReaderAnnouncer = ({ message, priority = 'polite', clearAfter = 5000 }) => {
  const [announcement, setAnnouncement] = useState('');

  useEffect(() => {
    if (message) {
      setAnnouncement(message);
      
      if (clearAfter > 0) {
        const timer = setTimeout(() => {
          setAnnouncement('');
        }, clearAfter);
        
        return () => clearTimeout(timer);
      }
    }
  }, [message, clearAfter]);

  if (!announcement) return null;

  return (
    <div
      aria-live={priority}
      aria-atomic="true"
      className="sr-only"
      role={priority === 'assertive' ? 'alert' : 'status'}
    >
      {announcement}
    </div>
  );
};

// Hook for easy announcements
export const useScreenReaderAnnouncer = () => {
  const [message, setMessage] = useState('');
  const [priority, setPriority] = useState('polite');

  const announce = (text, announcementPriority = 'polite') => {
    setMessage(''); // Clear first to ensure re-announcement
    setTimeout(() => {
      setMessage(text);
      setPriority(announcementPriority);
    }, 100);
  };

  const announceError = (text) => announce(text, 'assertive');
  const announceSuccess = (text) => announce(text, 'polite');

  return {
    announce,
    announceError,
    announceSuccess,
    ScreenReaderAnnouncer: () => (
      <ScreenReaderAnnouncer message={message} priority={priority} />
    )
  };
};

export default ScreenReaderAnnouncer;