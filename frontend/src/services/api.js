import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const predictRUL = async (sensorData) => {
    try {
        const response = await api.post('/predict', sensorData);
        return response.data;
    } catch (error) {
        console.error('Prediction error:', error);
        throw error;
    }
};

export const healthCheck = async () => {
    try {
        const response = await api.get('/');
        return response.data;
    } catch (error) {
        console.error('Health check error:', error);
        throw error;
    }
};

export default api;
