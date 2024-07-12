import React, { createContext, useState, useEffect } from 'react';
import jwt_decode from 'jwt-decode';
import API from '../api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem('authTokens')
      ? JSON.parse(localStorage.getItem('authTokens'))
      : null
  );

  const loginUser = async (username, password) => {
    const response = await API.post('token/', {
      username,
      password,
    });
    if (response.status === 200) {
      setAuthTokens(response.data);
      setUser(jwt_decode(response.data.access));
      localStorage.setItem('authTokens', JSON.stringify(response.data));
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
  };

  useEffect(() => {
    if (authTokens) {
      setUser(jwt_decode(authTokens.access));
    }
  }, [authTokens]);

  const contextData = {
    user,
    authTokens,
    loginUser,
    logoutUser,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
