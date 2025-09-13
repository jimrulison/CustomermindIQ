import React, { useState, useEffect } from 'react';
import {
    Layout,
    Palette,
    Eye,
    Save,
    Send,
    Copy,
    Edit,
    Trash2,
    Plus,
    Grid,
    Type,
    Image,
    Link,
    Star,
    Users,
    TrendingUp,
    Check
} from 'lucide-react';

const AffiliatePageBuilder = ({ affiliateId }) => {
    const [templates, setTemplates] = useState([]);
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    const [currentPage, setCurrentPage] = useState(null);
    const [userPages, setUserPages] = useState([]);
    const [activeView, setActiveView] = useState('templates'); // 'templates', 'editor', 'pages'
    const [loading, setLoading] = useState(false);
    const [previewMode, setPreviewMode] = useState(false);
    
    const [pageData, setPageData] = useState({
        page_title: '',
        page_slug: '',
        custom_content: {}
    });

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://admin-portal-fix-9.preview.emergentagent.com';

    useEffect(() => {
        loadTemplates();
        loadUserPages();
    }, []);

    const loadTemplates = async () => {
        try {
            const response = await fetch(`${backendUrl}/api/affiliate-pages/templates`);
            const data = await response.json();
            if (data.success) {
                setTemplates(data.templates);
            }
        } catch (error) {
            console.error('Error loading templates:', error);
        }
    };

    const loadUserPages = async () => {
        try {
            const response = await fetch(`${backendUrl}/api/affiliate-pages/affiliate/${affiliateId}`);
            const data = await response.json();
            if (data.success) {
                setUserPages(data.pages);
            }
        } catch (error) {
            console.error('Error loading user pages:', error);
        }
    };

    const selectTemplate = (template) => {
        setSelectedTemplate(template);
        setPageData({
            page_title: `My ${template.name} Page`,
            page_slug: `${template.template_id}-page`,
            custom_content: {
                headline: 'Transform Your Business with CustomerMind IQ',
                subtitle: 'Discover the power of AI-driven customer intelligence',
                cta_text: 'Start Free Trial',
                features: `
                    <div class="feature-item">
                        <h3>🎯 Customer Intelligence</h3>
                        <p>Understand your customers like never before with AI-powered insights.</p>
                    </div>
                    <div class="feature-item">
                        <h3>📊 Real-time Analytics</h3>
                        <p>Get instant insights into customer behavior and preferences.</p>
                    </div>
                    <div class="feature-item">
                        <h3>🚀 Growth Acceleration</h3>
                        <p>Boost revenue with data-driven customer engagement strategies.</p>
                    </div>
                `,
                testimonial: '"CustomerMind IQ transformed how we understand our customers. Revenue increased by 40% in just 3 months!" - Sarah Johnson, CEO'
            }
        });
        setActiveView('editor');
    };

    const createPage = async () => {
        if (!selectedTemplate || !pageData.page_title) return;
        
        setLoading(true);
        try {
            const response = await fetch(`${backendUrl}/api/affiliate-pages/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    affiliate_id: affiliateId,
                    template_id: selectedTemplate.template_id,
                    page_title: pageData.page_title,
                    page_slug: pageData.page_slug,
                    custom_content: pageData.custom_content
                })
            });
            
            const data = await response.json();
            if (data.success) {
                setCurrentPage({
                    page_id: data.page_id,
                    affiliate_number: data.affiliate_number,
                    page_url: data.page_url
                });
                loadUserPages();
                alert(`Page created successfully! Your affiliate number is: ${data.affiliate_number}`);
            }
        } catch (error) {
            console.error('Error creating page:', error);
            alert('Error creating page');
        } finally {
            setLoading(false);
        }
    };

    const updatePageContent = (field, value) => {
        setPageData(prev => ({
            ...prev,
            custom_content: {
                ...prev.custom_content,
                [field]: value
            }
        }));
    };

    const savePage = async () => {
        if (!currentPage) return;
        
        setLoading(true);
        try {
            const response = await fetch(`${backendUrl}/api/affiliate-pages/update/${currentPage.page_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    page_title: pageData.page_title,
                    custom_content: pageData.custom_content
                })
            });
            
            const data = await response.json();
            if (data.success) {
                alert('Page saved successfully!');
                loadUserPages();
            }
        } catch (error) {
            console.error('Error saving page:', error);
            alert('Error saving page');
        } finally {
            setLoading(false);
        }
    };

    const publishPage = async () => {
        if (!currentPage) return;
        
        setLoading(true);
        try {
            const response = await fetch(`${backendUrl}/api/affiliate-pages/update/${currentPage.page_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    is_published: true
                })
            });
            
            const data = await response.json();
            if (data.success) {
                alert('Page published successfully!');
                loadUserPages();
            }
        } catch (error) {
            console.error('Error publishing page:', error);
            alert('Error publishing page');
        } finally {
            setLoading(false);
        }
    };

    const copyPageUrl = () => {
        if (currentPage) {
            const fullUrl = `${backendUrl}${currentPage.page_url}`;
            navigator.clipboard.writeText(fullUrl);
            alert('Page URL copied to clipboard!');
        }
    };

    // Template Gallery View
    const renderTemplateGallery = () => (
        <div className="space-y-6">
            <div className="text-center">
                <h2 className="text-3xl font-bold text-white mb-4">Choose Your Landing Page Template</h2>
                <p className="text-slate-400 text-lg">20+ professional templates to boost your conversions</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {templates.map((template) => (
                    <div key={template.template_id} className="bg-slate-800 rounded-lg overflow-hidden hover:bg-slate-700 transition-colors cursor-pointer" onClick={() => selectTemplate(template)}>
                        <div className="h-48 bg-gradient-to-br from-blue-600 to-purple-600 flex flex-col items-center justify-center p-4">
                            <img 
                                src="https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/wzbjjt9q_download.svg" 
                                alt="CustomerMind IQ brand logo - Transform your business with AI-powered insights" 
                                className="h-12 mb-4 filter brightness-0 invert"
                            />
                            <div className="text-white text-center">
                                <h4 className="font-bold text-lg mb-2">Transform Your Business</h4>
                                <p className="text-sm opacity-75">AI-powered customer intelligence</p>
                                <button className="mt-3 bg-red-500 px-4 py-2 rounded text-sm font-medium">Start Free Trial</button>
                            </div>
                        </div>
                        <div className="p-4">
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="text-white font-semibold">{template.name}</h3>
                                <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded">{template.category}</span>
                            </div>
                            <p className="text-slate-400 text-sm mb-3">{template.description}</p>
                            <div className="flex items-center justify-between">
                                <div className="flex items-center space-x-1">
                                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                                </div>
                                <button className="text-blue-400 hover:text-blue-300 text-sm font-medium">
                                    Use Template
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

    // Page Editor View
    const renderPageEditor = () => (
        <div className="grid lg:grid-cols-2 gap-8">
            {/* Editor Panel */}
            <div className="bg-slate-800 rounded-lg p-6">
                <h3 className="text-white text-xl font-bold mb-6">Customize Your Page</h3>
                
                <div className="space-y-6">
                    {/* Page Settings */}
                    <div>
                        <label className="block text-white text-sm font-medium mb-2">Page Title</label>
                        <input
                            type="text"
                            value={pageData.page_title}
                            onChange={(e) => setPageData(prev => ({ ...prev, page_title: e.target.value }))}
                            className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter page title"
                        />
                    </div>
                    
                    <div>
                        <label className="block text-white text-sm font-medium mb-2">Page URL Slug</label>
                        <input
                            type="text"
                            value={pageData.page_slug}
                            onChange={(e) => setPageData(prev => ({ ...prev, page_slug: e.target.value }))}
                            className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="page-url-slug"
                        />
                    </div>

                    {/* Content Fields */}
                    <div>
                        <label className="block text-white text-sm font-medium mb-2">Main Headline</label>
                        <input
                            type="text"
                            value={pageData.custom_content.headline || ''}
                            onChange={(e) => updatePageContent('headline', e.target.value)}
                            className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Your compelling headline"
                        />
                    </div>
                    
                    <div>
                        <label className="block text-white text-sm font-medium mb-2">Subtitle</label>
                        <textarea
                            value={pageData.custom_content.subtitle || ''}
                            onChange={(e) => updatePageContent('subtitle', e.target.value)}
                            rows="2"
                            className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                            placeholder="Supporting description"
                        />
                    </div>
                    
                    <div>
                        <label className="block text-white text-sm font-medium mb-2">Call-to-Action Button Text</label>
                        <input
                            type="text"
                            value={pageData.custom_content.cta_text || ''}
                            onChange={(e) => updatePageContent('cta_text', e.target.value)}
                            className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Start Free Trial"
                        />
                    </div>
                    
                    <div>
                        <label className="block text-white text-sm font-medium mb-2">Features (HTML)</label>
                        <textarea
                            value={pageData.custom_content.features || ''}
                            onChange={(e) => updatePageContent('features', e.target.value)}
                            rows="6"
                            className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none font-mono text-sm"
                            placeholder="HTML for features section"
                        />
                    </div>
                    
                    <div>
                        <label className="block text-white text-sm font-medium mb-2">Customer Testimonial</label>
                        <textarea
                            value={pageData.custom_content.testimonial || ''}
                            onChange={(e) => updatePageContent('testimonial', e.target.value)}
                            rows="3"
                            className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                            placeholder="Customer testimonial with name and title"
                        />
                    </div>
                </div>
                
                {/* Action Buttons */}
                <div className="flex flex-wrap gap-3 mt-8">
                    <button
                        onClick={createPage}
                        disabled={loading || !pageData.page_title}
                        className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Create Page
                    </button>
                    
                    {currentPage && (
                        <>
                            <button
                                onClick={savePage}
                                disabled={loading}
                                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                            >
                                <Save className="w-4 h-4 mr-2" />
                                Save Changes
                            </button>
                            
                            <button
                                onClick={publishPage}
                                disabled={loading}
                                className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
                            >
                                <Send className="w-4 h-4 mr-2" />
                                Publish
                            </button>
                            
                            <button
                                onClick={copyPageUrl}
                                className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
                            >
                                <Copy className="w-4 h-4 mr-2" />
                                Copy URL
                            </button>
                        </>
                    )}
                </div>
                
                {currentPage && (
                    <div className="mt-4 p-3 bg-green-600/20 border border-green-500/30 rounded-lg">
                        <p className="text-green-400 text-sm">
                            <Check className="w-4 h-4 inline mr-1" />
                            Affiliate Number: <strong>{currentPage.affiliate_number}</strong>
                        </p>
                        <p className="text-green-400 text-sm">
                            Page URL: <code className="bg-slate-700 px-2 py-1 rounded">{currentPage.page_url}</code>
                        </p>
                    </div>
                )}
            </div>
            
            {/* Preview Panel */}
            <div className="bg-slate-800 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-white text-xl font-bold">Live Preview</h3>
                    <button
                        onClick={() => setPreviewMode(!previewMode)}
                        className="flex items-center px-3 py-1 bg-slate-700 text-white rounded-lg hover:bg-slate-600"
                    >
                        <Eye className="w-4 h-4 mr-2" />
                        {previewMode ? 'Edit' : 'Preview'}
                    </button>
                </div>
                
                    <div className="bg-white rounded-lg p-4 min-h-96">
                        <div className="preview-content">
                            <div className="hero-section text-center py-12 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg mb-6">
                                <div className="logo-container mb-6">
                                    <img 
                                        src="https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/wzbjjt9q_download.svg" 
                                        alt="CustomerMind IQ logo - AI customer intelligence dashboard preview" 
                                        className="h-12 mx-auto filter brightness-0 invert"
                                    />
                                </div>
                                <h1 className="text-3xl font-bold mb-4">{pageData.custom_content.headline}</h1>
                                <p className="text-lg mb-6">{pageData.custom_content.subtitle}</p>
                                <button className="bg-red-500 text-white px-6 py-3 rounded-lg font-semibold shadow-lg hover:bg-red-600 transition-colors">
                                    {pageData.custom_content.cta_text}
                                </button>
                            </div>
                            
                            <div className="features-section mb-6">
                                <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">Why Choose CustomerMind IQ?</h2>
                                <div dangerouslySetInnerHTML={{ __html: pageData.custom_content.features }} />
                            </div>
                            
                            {pageData.custom_content.testimonial && (
                                <div className="testimonial-section text-center py-6 bg-gray-50 rounded-lg">
                                    <blockquote className="text-lg italic text-gray-600">
                                        {pageData.custom_content.testimonial}
                                    </blockquote>
                                </div>
                            )}
                            
                            {currentPage && (
                                <div className="footer-section text-center py-4 bg-gray-800 text-white rounded-lg mt-6">
                                    <div className="footer-branding flex flex-col items-center gap-2">
                                        <img 
                                            src="https://customer-assets.emergentagent.com/job_ced7e1b3-1a48-45ae-9e54-46819c066d8a/artifacts/wzbjjt9q_download.svg" 
                                            alt="CustomerMind IQ company logo - AI-powered customer intelligence platform" 
                                            className="h-8 filter brightness-0 invert"
                                        />
                                        <p>Affiliate #{currentPage.affiliate_number} | CustomerMind IQ</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
            </div>
        </div>
    );

    // User Pages Management View
    const renderUserPages = () => (
        <div className="space-y-6">
            <div className="text-center">
                <h2 className="text-3xl font-bold text-white mb-4">Your Landing Pages</h2>
                <p className="text-slate-400 text-lg">Manage all your custom affiliate landing pages</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {userPages.map((page) => (
                    <div key={page.page_id} className="bg-slate-800 rounded-lg p-6">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-white font-semibold">{page.page_title}</h3>
                            <span className={`px-2 py-1 text-xs rounded ${page.is_published ? 'bg-green-600 text-white' : 'bg-gray-600 text-white'}`}>
                                {page.is_published ? 'Published' : 'Draft'}
                            </span>
                        </div>
                        
                        <div className="space-y-2 mb-4">
                            <p className="text-slate-400 text-sm">
                                <strong>Affiliate #:</strong> {page.affiliate_number}
                            </p>
                            <p className="text-slate-400 text-sm">
                                <strong>Views:</strong> {page.view_count || 0}
                            </p>
                            <p className="text-slate-400 text-sm">
                                <strong>Conversions:</strong> {page.conversion_count || 0}
                            </p>
                        </div>
                        
                        <div className="flex space-x-2">
                            <button className="flex-1 flex items-center justify-center px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                                <Edit className="w-4 h-4 mr-1" />
                                Edit
                            </button>
                            <button className="flex items-center justify-center px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700">
                                <Eye className="w-4 h-4" />
                            </button>
                            <button className="flex items-center justify-center px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
                                <Trash2 className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                ))}
                
                {userPages.length === 0 && (
                    <div className="col-span-full text-center py-12">
                        <Layout className="w-16 h-16 text-slate-600 mx-auto mb-4" />
                        <h3 className="text-white text-xl font-semibold mb-2">No Pages Yet</h3>
                        <p className="text-slate-400 mb-4">Create your first landing page to get started</p>
                        <button
                            onClick={() => setActiveView('templates')}
                            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                        >
                            Create First Page
                        </button>
                    </div>
                )}
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Navigation */}
                <div className="flex items-center justify-between mb-8">
                    <h1 className="text-3xl font-bold text-white">Affiliate Page Builder</h1>
                    <div className="flex space-x-2">
                        <button
                            onClick={() => setActiveView('templates')}
                            className={`px-4 py-2 rounded-lg font-medium ${activeView === 'templates' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
                        >
                            <Grid className="w-4 h-4 inline mr-2" />
                            Templates
                        </button>
                        <button
                            onClick={() => setActiveView('pages')}
                            className={`px-4 py-2 rounded-lg font-medium ${activeView === 'pages' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
                        >
                            <Layout className="w-4 h-4 inline mr-2" />
                            My Pages ({userPages.length})
                        </button>
                    </div>
                </div>

                {/* Content */}
                {activeView === 'templates' && renderTemplateGallery()}
                {activeView === 'editor' && renderPageEditor()}
                {activeView === 'pages' && renderUserPages()}
            </div>
        </div>
    );
};

export default AffiliatePageBuilder;