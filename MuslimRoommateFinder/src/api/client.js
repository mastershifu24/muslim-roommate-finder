import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Django API URL - Using your Render.com deployment
// For local testing: use 'http://YOUR_IP:8000/api' (e.g., 'http://10.0.0.209:8000/api')
// For production: use your Render.com URL with /api endpoint
const API_BASE_URL = 'https://muslim-roommate-finder.onrender.com/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to all requests if it exists
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Authentication endpoints
export const authAPI = {
  login: async (username, password) => {
    const response = await apiClient.post('/auth/login/', { username, password });
    return response.data;
  },
  
  register: async (userData) => {
    const response = await apiClient.post('/auth/register/', userData);
    return response.data;
  },
  
  logout: async () => {
    await AsyncStorage.removeItem('authToken');
    await AsyncStorage.removeItem('userId');
  },
};

// Profile endpoints
export const profileAPI = {
  getMyProfile: async () => {
    const response = await apiClient.get('/profiles/me/');
    return response.data;
  },
  
  getAllProfiles: async (params) => {
    const response = await apiClient.get('/profiles/', { params });
    return response.data;
  },
  
  getProfileById: async (id) => {
    const response = await apiClient.get(`/profiles/${id}/`);
    return response.data;
  },
  
  updateProfile: async (data) => {
    const response = await apiClient.patch('/profiles/me/', data);
    return response.data;
  },
  
  getCompatibilityScore: async (profileId) => {
    const response = await apiClient.get(`/profiles/${profileId}/compatibility/`);
    return response.data;
  },
};

// Room endpoints
export const roomAPI = {
  getAllRooms: async (params) => {
    const response = await apiClient.get('/rooms/', { params });
    return response.data;
  },
  
  getRoomById: async (id) => {
    const response = await apiClient.get(`/rooms/${id}/`);
    return response.data;
  },
  
  getMyRooms: async () => {
    const response = await apiClient.get('/rooms/my_listings/');
    return response.data;
  },
  
  createRoom: async (data) => {
    const response = await apiClient.post('/rooms/', data);
    return response.data;
  },
  
  updateRoom: async (id, data) => {
    const response = await apiClient.patch(`/rooms/${id}/`, data);
    return response.data;
  },
  
  deleteRoom: async (id) => {
    await apiClient.delete(`/rooms/${id}/`);
  },
};

// Message endpoints
export const messageAPI = {
  getInbox: async () => {
    const response = await apiClient.get('/messages/');
    return response.data;
  },
  
  sendMessage: async (recipientId, content) => {
    const response = await apiClient.post('/messages/', {
      recipient: recipientId,
      content,
    });
    return response.data;
  },
  
  markAsRead: async (messageId) => {
    const response = await apiClient.post(`/messages/${messageId}/mark_read/`);
    return response.data;
  },
};

export default apiClient;

