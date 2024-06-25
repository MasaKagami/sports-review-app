// src/authService.js

import axios from 'axios';
import jwtDecode from 'jwt-decode';
import { ACCESS_TOKEN, REFRESH_TOKEN } from './constants';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

const login = async (username, password) => {
  try {
    const response = await apiClient.post('/token/', { username, password });
    const { access, refresh } = response.data;
    localStorage.setItem(ACCESS_TOKEN, access);
    localStorage.setItem(REFRESH_TOKEN, refresh);
    return jwtDecode(access);
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

const refreshAccessToken = async () => {
  try {
    const refreshToken = getRefreshToken();
    const response = await apiClient.post('/token/refresh/', { refresh: refreshToken });
    const { access } = response.data;
    localStorage.setItem(ACCESS_TOKEN, access);
    return jwtDecode(access);
  } catch (error) {
    console.error('Token refresh error:', error);
    logout();
    throw error;
  }
};

const logout = () => {
  localStorage.removeItem(ACCESS_TOKEN);
  localStorage.removeItem(REFRESH_TOKEN);
};

const getAccessToken = () => localStorage.getItem(ACCESS_TOKEN);
const getRefreshToken = () => localStorage.getItem(REFRESH_TOKEN);

const getDecodedAccessToken = () => {
  const token = getAccessToken();
  if (token) {
    return jwtDecode(token);
  }
  return null;
};

export { login, logout, refreshAccessToken, getAccessToken, getRefreshToken, getDecodedAccessToken };
