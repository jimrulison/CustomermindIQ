import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Globe, ChevronDown } from 'lucide-react';

const LanguageSelector = ({ theme = 'light' }) => {
    const { i18n, t } = useTranslation();
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    const languages = [
        { code: 'en', name: t('language.english'), flag: '🇺🇸' },
        { code: 'es', name: t('language.spanish'), flag: '🇪🇸' },
        { code: 'fr', name: t('language.french'), flag: '🇫🇷' },
        { code: 'de', name: t('language.german'), flag: '🇩🇪' },
        { code: 'it', name: t('language.italian'), flag: '🇮🇹' }
    ];

    const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

    const changeLanguage = (languageCode) => {
        i18n.changeLanguage(languageCode);
        setIsOpen(false);
        
        // Store the selected language in localStorage
        localStorage.setItem('i18nextLng', languageCode);
        
        // Optionally reload the page to ensure all content is updated
        // window.location.reload();
    };

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    // Theme-based styling
    const buttonClasses = theme === 'dark' 
        ? "flex items-center space-x-2 px-3 py-2 rounded-md text-white/80 hover:text-white hover:bg-white/10 transition-colors duration-200"
        : "flex items-center space-x-2 px-3 py-2 rounded-md text-gray-700 hover:text-gray-900 hover:bg-gray-100 transition-colors duration-200";
    
    const dropdownClasses = theme === 'dark'
        ? "absolute right-0 mt-2 w-48 bg-slate-800 rounded-md shadow-lg border border-slate-600 z-50"
        : "absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-50";
        
    const headerClasses = theme === 'dark'
        ? "px-3 py-2 text-xs font-medium text-slate-400 uppercase tracking-wider border-b border-slate-600"
        : "px-3 py-2 text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-100";
        
    const itemClasses = (isActive) => theme === 'dark'
        ? `w-full text-left px-3 py-2 text-sm hover:bg-slate-700 transition-colors duration-200 flex items-center space-x-3 ${
            isActive 
                ? 'bg-blue-900/50 text-blue-300 border-r-2 border-blue-400' 
                : 'text-slate-200'
        }`
        : `w-full text-left px-3 py-2 text-sm hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-3 ${
            isActive 
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500' 
                : 'text-gray-700'
        }`;

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={buttonClasses}
                aria-label={t('language.selectLanguage')}
            >
                <Globe className="h-4 w-4" />
                <span className="text-sm font-medium hidden sm:inline">
                    {currentLanguage.flag} {currentLanguage.name}
                </span>
                <span className="text-sm font-medium sm:hidden">
                    {currentLanguage.flag}
                </span>
                <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {isOpen && (
                <div className={dropdownClasses}>
                    <div className="py-1">
                        <div className={headerClasses}>
                            {t('language.selectLanguage')}
                        </div>
                        {languages.map((language) => (
                            <button
                                key={language.code}
                                onClick={() => changeLanguage(language.code)}
                                className={itemClasses(i18n.language === language.code)}
                            >
                                <span className="text-lg">{language.flag}</span>
                                <span className="flex-1">{language.name}</span>
                                {i18n.language === language.code && (
                                    <div className={`w-2 h-2 rounded-full ${theme === 'dark' ? 'bg-blue-400' : 'bg-blue-500'}`}></div>
                                )}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default LanguageSelector;