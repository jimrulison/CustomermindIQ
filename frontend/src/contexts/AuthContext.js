import React, { createContext, useContext, useState, useEffect, useMemo } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Use environment variable for backend URL with fallback
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
  
  // Debug: Log the backend URL
  console.log('AUTH CONTEXT - Backend URL (from env):', backendUrl);
  console.log('AUTH CONTEXT - Environment REACT_APP_BACKEND_URL:', process.env.REACT_APP_BACKEND_URL);

  // Check for stored authentication on app start - optimized
  useEffect(() => {
    console.log('🔍 AuthContext useEffect: Starting authentication check...');
    const storedToken = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user_profile');
    
    console.log('🔍 AuthContext: Stored token exists:', !!storedToken);
    console.log('🔍 AuthContext: Stored user exists:', !!storedUser);
    
    if (storedToken && storedUser) {
      try {
        const userProfile = JSON.parse(storedUser);
        console.log('🔍 AuthContext: Parsed user profile:', userProfile);
        console.log('🔍 AuthContext: User role:', userProfile.role, 'isAdmin:', ['admin', 'super_admin'].includes(userProfile.role));
        
        setToken(storedToken);
        setUser(userProfile);
        console.log('✅ Authentication restored from localStorage');
        console.log('✅ User role:', userProfile.role, 'isAdmin:', ['admin', 'super_admin'].includes(userProfile.role));
      } catch (error) {
        console.error('❌ Error parsing stored user profile:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_profile');
      }
    } else {
      console.log('⚠️ No stored authentication found');
    }
    
    // Set loading to false after state synchronization to prevent race condition
    // Use setTimeout to ensure React state updates are processed
    setTimeout(() => {
      setLoading(false);
      console.log('✅ AuthContext initialization complete - Loading set to false');
    }, 0);
  }, []);

  // Register new user
  const register = async (registrationData) => {
    try {
      const response = await fetch(`${backendUrl}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
      });

      const data = await response.json();

      if (response.ok) {
        // Store tokens and user info
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user_profile', JSON.stringify(data.user_profile));
        
        setToken(data.access_token);
        setUser(data.user_profile);
        
        return { success: true, data };
      } else {
        return { success: false, error: data.detail || 'Registration failed' };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: 'Unable to connect to server. Please try again.' };
    }
  };

  // Login user
  const login = async (email, password, rememberMe = false) => {
    try {
      console.log('Attempting login to:', `${backendUrl}/api/auth/login`);
      
      const response = await fetch(`${backendUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          remember_me: rememberMe,
        }),
      });

      console.log('Login response status:', response.status);
      const data = await response.json();

      if (response.ok) {
        console.log('Login successful');
        // Store tokens and user info
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user_profile', JSON.stringify(data.user_profile));
        
        setToken(data.access_token);
        setUser(data.user_profile);
        
        return { success: true, user: data.user_profile };
      } else {
        console.log('Login failed:', data);
        return { success: false, error: data.detail || 'Invalid email or password' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Unable to connect to server. Please try again.' };
    }
  };

  // Logout user
  const logout = async () => {
    try {
      if (token) {
        // Call backend logout endpoint
        await fetch(`${backendUrl}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage and state regardless of API call result
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_profile');
      setToken(null);
      setUser(null);
    }
  };

  // Refresh token
  const refreshToken = async () => {
    try {
      const refreshTokenValue = localStorage.getItem('refresh_token');
      if (!refreshTokenValue) {
        throw new Error('No refresh token available');
      }

      const response = await fetch(`${backendUrl}/api/auth/refresh-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshTokenValue }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user_profile', JSON.stringify(data.user_profile));
        
        setToken(data.access_token);
        setUser(data.user_profile);
        
        return { success: true, token: data.access_token };
      } else {
        throw new Error(data.detail || 'Token refresh failed');
      }
    } catch (error) {
      console.error('Token refresh error:', error);
      // If refresh fails, logout user
      logout();
      return { success: false, error: error.message };
    }
  };

  // Get user profile
  const getUserProfile = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/auth/profile`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (response.ok) {
        setUser(data);
        localStorage.setItem('user_profile', JSON.stringify(data));
        return { success: true, user: data };
      } else {
        return { success: false, error: data.detail || 'Failed to get user profile' };
      }
    } catch (error) {
      console.error('Get profile error:', error);
      return { success: false, error: 'Unable to connect to server. Please try again.' };
    }
  };

  // Update user profile
  const updateProfile = async (profileData) => {
    try {
      const response = await fetch(`${backendUrl}/api/auth/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
      });

      const data = await response.json();

      if (response.ok) {
        setUser(data);
        localStorage.setItem('user_profile', JSON.stringify(data));
        return { success: true, user: data };
      } else {
        return { success: false, error: data.detail || 'Failed to update profile' };
      }
    } catch (error) {
      console.error('Update profile error:', error);
      return { success: false, error: 'Unable to connect to server. Please try again.' };
    }
  };

  // Check if user has required role
  const hasRole = (requiredRoles) => {
    if (!user || !user.role) return false;
    if (Array.isArray(requiredRoles)) {
      return requiredRoles.includes(user.role);
    }
    return user.role === requiredRoles;
  };

  // Check if user has admin access
  const isAdmin = () => {
    return hasRole(['admin', 'super_admin']);
  };

  // Check if user has subscription tier
  const hasSubscriptionTier = (requiredTiers) => {
    if (!user || !user.subscription_tier) return false;
    if (Array.isArray(requiredTiers)) {
      return requiredTiers.includes(user.subscription_tier);
    }
    return user.subscription_tier === requiredTiers;
  };

  // API helper with automatic token handling
  const apiCall = async (endpoint, options = {}) => {
    const url = `${backendUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      // If token expired, try to refresh
      if (response.status === 401 && token) {
        const refreshResult = await refreshToken();
        if (refreshResult.success) {
          // Retry the request with new token
          headers['Authorization'] = `Bearer ${refreshResult.token}`;
          return fetch(url, { ...options, headers });
        } else {
          // Refresh failed, redirect to login
          logout();
          return response;
        }
      }

      return response;
    } catch (error) {
      console.error('API call error:', error);
      throw error;
    }
  };

  // Memoize isAuthenticated to ensure proper dependency tracking
  const isAuthenticated = useMemo(() => {
    const hasUser = !!user;
    const hasToken = !!token;
    const result = hasUser && hasToken;
    console.log('🔍 AuthContext - isAuthenticated calculated:', {
      hasUser,
      hasToken, 
      result,
      userRole: user?.role,
      loading
    });
    return result;
  }, [user, token, loading]);

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    refreshToken,
    getUserProfile,
    updateProfile,
    hasRole,
    isAdmin,
    hasSubscriptionTier,
    apiCall,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};