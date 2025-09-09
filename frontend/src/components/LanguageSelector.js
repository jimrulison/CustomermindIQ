import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Globe, ChevronDown } from 'lucide-react';

const LanguageSelector = () => {
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

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-md text-gray-700 hover:text-gray-900 hover:bg-gray-100 transition-colors duration-200"
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
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-50">
                    <div className="py-1">
                        <div className="px-3 py-2 text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-100">
                            {t('language.selectLanguage')}
                        </div>
                        {languages.map((language) => (
                            <button
                                key={language.code}
                                onClick={() => changeLanguage(language.code)}
                                className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-3 ${
                                    i18n.language === language.code 
                                        ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500' 
                                        : 'text-gray-700'
                                }`}
                            >
                                <span className="text-lg">{language.flag}</span>
                                <span className="flex-1">{language.name}</span>
                                {i18n.language === language.code && (
                                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
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