// src/ProtectedRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';
import { getAccessToken } from '../authService';

const ProtectedRoute = ({ children }) => {
  const token = getAccessToken();
  if (!token) {
    return <Navigate to="/login" />;
  }
  return children;
};

export default ProtectedRoute;
