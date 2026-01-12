import React, { createContext, useState, useContext, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authAPI, profileAPI } from '../api/client';

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
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is already logged in when app starts
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      if (token) {
        // Fetch user profile to verify token is still valid
        const profileData = await profileAPI.getMyProfile();
        setProfile(profileData);
        setUser({ id: profileData.user.id, username: profileData.user.username });
      }
    } catch (err) {
      console.log('Not authenticated:', err);
      // Token invalid or expired
      await logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      setError(null);
      setLoading(true);
      
      const data = await authAPI.login(username, password);
      
      // Save token and user ID
      await AsyncStorage.setItem('authToken', data.token);
      await AsyncStorage.setItem('userId', data.user.id.toString());
      
      // Fetch full profile
      const profileData = await profileAPI.getMyProfile();
      setProfile(profileData);
      setUser(data.user);
      
      return { success: true };
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Login failed. Please try again.';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      setLoading(true);
      
      const data = await authAPI.register(userData);
      
      // Save token and user ID
      await AsyncStorage.setItem('authToken', data.token);
      await AsyncStorage.setItem('userId', data.user.id.toString());
      
      // Fetch full profile
      const profileData = await profileAPI.getMyProfile();
      setProfile(profileData);
      setUser(data.user);
      
      return { success: true };
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Registration failed. Please try again.';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    await authAPI.logout();
    setUser(null);
    setProfile(null);
  };

  const refreshProfile = async () => {
    try {
      const profileData = await profileAPI.getMyProfile();
      setProfile(profileData);
    } catch (err) {
      console.error('Failed to refresh profile:', err);
    }
  };

  const value = {
    user,
    profile,
    loading,
    error,
    login,
    register,
    logout,
    refreshProfile,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

