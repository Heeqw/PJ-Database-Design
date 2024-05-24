import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Django 后端的 URL
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

export default {
  getMerchants() {
    return apiClient.get('/merchants/');
  },
  getMerchant(id) {
    return apiClient.get(`/merchants/${id}/`);
  },
  getDishes() {
    return apiClient.get('/dishes/');
  },
  getDish(id) {
    return apiClient.get(`/dishes/${id}/`);
  }
};
