import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API service functions
export const authService = {
  login: (credentials) => apiClient.post('/auth/login', credentials),
  register: (userData) => apiClient.post('/auth/register', userData),
  getCurrentUser: () => apiClient.get('/auth/me'),
};

export const sourcesService = {
  getAll: (params = {}) => apiClient.get('/sources', { params }),
  getById: (id) => apiClient.get(`/sources/${id}`),
  create: (data) => apiClient.post('/sources', data),
  update: (id, data) => apiClient.put(`/sources/${id}`, data),
  delete: (id) => apiClient.delete(`/sources/${id}`),
};

export const breachesService = {
  getAll: (params = {}) => apiClient.get('/breaches', { params }),
  getById: (id) => apiClient.get(`/breaches/${id}`),
  getStats: () => apiClient.get('/breaches/stats'),
  verify: (id) => apiClient.put(`/breaches/${id}/verify`),
  markFalsePositive: (id) => apiClient.put(`/breaches/${id}/false-positive`),
};

export const alertsService = {
  getAll: (params = {}) => apiClient.get('/alerts', { params }),
  getById: (id) => apiClient.get(`/alerts/${id}`),
};

export const healthService = {
  getStatus: () => apiClient.get('/health'),
  getDatabaseStatus: () => apiClient.get('/health/database'),
  getSystemStatus: () => apiClient.get('/health/system'),
};