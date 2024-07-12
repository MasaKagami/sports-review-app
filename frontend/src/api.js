import axios from 'axios';
import { ACCESS_TOKEN } from "./constants";

// will intercept any request we send.
// configures the axios, which is used to maakr HTTP requests to the backend API.

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Sets the base URL for all requests.
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
},
  (error) => {
    return Promise.reject(error);
  }
);

export default API;
