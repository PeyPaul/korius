import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getCheaperAlternatives = async (minSavingsPercent = 5.0, productId = null) => {
  const params = { min_savings_percent: minSavingsPercent };
  if (productId) {
    params.product_id = productId;
  }
  const response = await api.get('/api/suppliers/cheaper-alternatives', { params });
  return response.data;
};

export const getInnovativeProducts = async (minSuppliers = 1, sortBy = 'suppliers') => {
  const params = { min_suppliers: minSuppliers, sort_by: sortBy };
  const response = await api.get('/api/products/innovative', { params });
  return response.data;
};

